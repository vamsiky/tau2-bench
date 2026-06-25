# Benchmark the Claude Agent SDK full loop in tau2-bench

## Context

Goal: evaluate whether letting the **Claude Agent SDK own the agent-side loop**
(its own multi-step reasoning + tool execution between user turns) changes
tau2-bench scores versus tau2's standard one-model-call-per-turn agent. You
confirmed the direction: build the **full-loop** integration as the primary
deliverable (the simpler one-step adapter is just a building block, kept as a
fallback).

The integration is possible because of one verified fact: **tau2's scoring is a
pure function of `(trajectory, task)`** — `evaluate_simulation` (`evaluator.py:88`)
reads only `simulation.messages`, and even the strict DB check rebuilds a fresh
environment and **replays the tool calls recorded in the trajectory**
(`evaluator_env.py:81-117`), comparing DB hashes to a gold env. So if we let the
SDK run its loop and faithfully **capture** the run as a tau2-format trajectory,
the existing evaluator scores it unchanged.

### Feasibility verdict

- **No changes to tau2's core** (orchestrator base, environment, user simulator,
  message model, evaluator are all reused as-is).
- **But it is NOT a `tau2 run --agent X` drop-in.** The standard `Orchestrator`
  calls the agent once per turn and records only what it returns; if the SDK
  executes tools internally, those calls are invisible to `Orchestrator.trajectory`
  and the ENV/ACTION checks fail. So the full loop needs a **custom async driver**
  that records each tool call+result itself, then hands the assembled
  `SimulationRun` to the existing evaluator. This is the contained "friction" —
  it lives in the new driver, not in tau2.
- Two real constraints from the SDK (both manageable, both flagged below):
  tool-execution **ordering within a turn is undocumented** (#6), and the SDK runs
  an **async, bundled-Node-CLI subprocess** (#7) while tau2's runner is sync.

## Verified SDK mechanics (claude-agent-sdk 0.2.107, import `claude_agent_sdk`)

- Turn-by-turn: `async with ClaudeSDKClient(options) as client:` → `await
  client.query(user_text)` → `async for m in client.receive_response(): ...`
  yields until a `ResultMessage` (end-of-turn); call `query()` again for the next
  turn, context retained.
- Stream blocks: `AssistantMessage.content` holds `TextBlock(.text)` and
  `ToolUseBlock(.id,.name,.input)`; tool results arrive as `UserMessage` with
  `ToolResultBlock(.tool_use_id,.content,.is_error)`; `ResultMessage` carries
  `.result`, `.total_cost_usd`, `.usage`.
- Custom in-process tools: `@tool(name, description, input_schema_dict)` (async
  handler `(args)->{"content":[{"type":"text","text":...}],"is_error":bool}`),
  registered via `create_sdk_mcp_server(name, tools=[...])` and
  `ClaudeAgentOptions(mcp_servers={"env":server}, allowed_tools=["mcp__env__<t>"])`.
- Lockdown: `disallowed_tools=[<named builtins>]` removes built-ins from the
  model's context; `permission_mode="bypassPermissions"`; `system_prompt="<policy>"`
  (bare string replaces); `model="claude-opus-4-8"`; `setting_sources=[]` to stay
  hermetic.
- Hooks (async in-process Python callbacks): `options.hooks={"PreToolUse":
  [HookMatcher(hooks=[cb])], ...}`. `PreToolUse` payload = `tool_name`,
  `tool_input`, `tool_use_id`; `PostToolUse` adds `tool_response`;
  `PostToolUseFailure` adds `error`. `tool_use_id` == stream `ToolUseBlock.id`.
  Callback returns `{}` for no-op capture. Hooks fire for every tool call but with
  **non-deterministic firing order** (concurrent dispatch) — order must come from
  the stream.

## Architecture — custom async driver (recommended)

A new async function `run_claude_sdk_loop_simulation(task, domain, agent_model,
user_llm, max_steps, seed, ...) -> SimulationRun` that reuses tau2's components
and only adds the SDK loop + bridge + trajectory capture.

**Reused tau2 pieces (unchanged):**
- `registry.get_env_constructor(domain)` → `Environment`; `env.set_state(...)`
  (init from `task.initial_state`), `env.get_tools()`, `env.get_user_tools()`,
  `env.get_policy()`, `env.get_response(tool_call)` — same env + DB every model uses.
- `UserSimulator(llm=user_llm, instructions=..., tools=env.get_user_tools(),
  persona_config=...)`, `user.get_init_state(...)`, `user.generate_next_message(
  assistant_text_msg, state)`, `UserSimulator.is_stop(msg)` — same user simulator.
- Message model (`AssistantMessage`, `UserMessage`, `ToolCall`, `ToolMessage`),
  `DEFAULT_FIRST_AGENT_MESSAGE` (orchestrator), `get_cost` (`llm_utils`),
  `evaluate_simulation` + `EvaluationType.ALL` (evaluator), `SimulationRun` +
  `TerminationReason` (`data_model/simulation.py`).
- The agent **system prompt** must reuse tau2's `LLMAgent` prompt construction
  (`agent/llm_agent.py`) so the only variable vs. the baseline is the loop, not
  the prompt — essential for a clean "does the SDK loop help?" comparison.

**New pieces:**
1. **Tool bridge (execution only).** For each tau2 `Tool`, generate an
   `@tool`-wrapped async handler using the tau2 tool's `name`, description, and JSON
   schema (`tool.openai_schema["function"]["parameters"]` → `input_schema`). The
   handler is intentionally dumb — it only executes and returns; capture happens via
   hooks (below). Under a **single shared `asyncio.Lock`** (so each tool call sees a
   consistent env snapshot during the live run):
   - build `ToolCall(name, arguments=args, requestor="assistant")`;
   - `tool_msg = await asyncio.to_thread(env.get_response, tool_call)` (env is sync);
   - return `{"content":[{"type":"text","text":tool_msg.content}],
     "is_error":tool_msg.error}` to the SDK.
   The handler does NOT record into the trajectory and does not need the
   `tool_use_id` (it never receives one).
2. **Trajectory capture (hooks + stream).** This is the faithful-capture surface:
   - Register match-all async hooks `PreToolUse`, `PostToolUse`, `PostToolUseFailure`
     (each returns `{}` → no side effects). They record into a dict **keyed by
     `tool_use_id`**: PreToolUse → `(tool_name, tool_input)`; PostToolUse →
     `tool_response` (extract the env result text from the MCP content wrapper);
     PostToolUseFailure → `error` (sets tau2 `ToolMessage.error=True`). Hooks fire
     for **every** tool call regardless of permission rules and are the only place
     that hands us the SDK `tool_use_id` + result together.
   - **Ordering comes from the stream, not hook timing** (hook dispatch is
     concurrent/non-deterministic). Within each streamed `AssistantMessage`, the
     order of `ToolUseBlock`s is the authoritative request order; join the
     hook-captured `(input, result, error)` back by `tool_use_id`. (The stream's
     `ToolResultBlock` can serve as a cross-check / fallback for the result.)
   - Per tool call, in stream order, emit into the tau2 trajectory:
     `AssistantMessage(tool_calls=[ToolCall(id=tool_use_id, name, args,
     requestor="assistant")])` then `ToolMessage(id=tool_use_id, content=<result>,
     error=<failure?>)`.
3. **Options:** `ClaudeAgentOptions(system_prompt=<tau2 agent prompt>,
   model=agent_model, mcp_servers={"env":server},
   allowed_tools=["mcp__env__<name>" ...], disallowed_tools=[named builtins],
   permission_mode="bypassPermissions", setting_sources=[],
   hooks={"PreToolUse":[HookMatcher(hooks=[rec_pre])],
   "PostToolUse":[HookMatcher(hooks=[rec_post])],
   "PostToolUseFailure":[HookMatcher(hooks=[rec_fail])]})`.
4. **Driver loop** (mirrors tau2's turn order — agent greets first):
   - `trajectory=[AssistantMessage(content=DEFAULT_FIRST_AGENT_MESSAGE)]`; that
     greeting is the first `msg_to_user`.
   - `while not done and steps<max:` →
     `user_msg = user.generate_next_message(msg_to_user, user_state)`; append;
     if `UserSimulator.is_stop(user_msg)` → `termination=USER_STOP; break`.
   - `await client.query(user_msg.content)`; `async for m in
     client.receive_response():` walk the stream: for each `AssistantMessage`, emit
     the in-order `ToolUseBlock`→`ToolCall`+`ToolMessage` pairs (joined to hook
     captures by `tool_use_id`); collect the final `TextBlock`; on `ResultMessage`
     grab `result`, `total_cost_usd`, `usage` and end the turn.
   - `agent_msg = AssistantMessage(content=final_text, cost=ResultMessage.
     total_cost_usd, usage=ResultMessage.usage)`; append; if the agent transferred
     to human → `termination=AGENT_STOP; break`; else `msg_to_user=agent_msg`.
   - exhausting `max_steps` → `termination=MAX_STEPS` (scores 0, same as baseline).
5. **Assemble + score:** build `SimulationRun(id, task_id, start_time, end_time,
   duration, termination_reason, messages=trajectory, agent_cost/user_cost via
   get_cost, seed, mode="half_duplex")`, then `evaluate_simulation(sim, task,
   EvaluationType.ALL, solo_mode=False, domain=domain,
   mode=HALF_DUPLEX)`.

Why a custom driver and not subclassing `Orchestrator`: the orchestrator's
`step()` state machine is sync and assumes a one-step agent; the SDK is async and
owns the loop. A custom async driver reuses the valuable parts (env, user,
evaluator, cost) without fighting the sync step-machine.

## Fidelity risks & mitigations (the part that determines whether scores are trustworthy)

- **Tool ordering within a turn (#6).** Hook *firing* order is non-deterministic
  (SDK dispatches hooks as concurrent detached tasks), so it must NOT be the
  trajectory order. **Resolution:** take order from the **stream** (`ToolUseBlock`
  sequence within each `AssistantMessage` = authoritative request order) and join
  hook-captured results by `tool_use_id`. This is robust regardless of hook
  concurrency. Note the ACTION check is order-insensitive (`extract_tool_calls`
  collects by membership), and the DB check replays the recorded stream order; the
  serializing `asyncio.Lock` keeps the *live* env consistent so the results the
  model sees are coherent. Still log/flag any turn with multiple tool calls so
  parallel-call fidelity can be audited; pin the SDK version.
- **Prompt parity.** Reuse tau2's `LLMAgent` system prompt verbatim, else score
  deltas reflect prompt differences, not the loop.
- **Only-the-final-text-reaches-the-user.** The user simulator must receive only
  the agent's final `TextBlock` per turn (matches tau2, where the user never sees
  tool calls); intermediate SDK reasoning text is not sent to the user and not
  recorded as conversation turns — only `(tool_call, tool_result)` pairs and the
  final text are recorded.
- **Termination gate.** `evaluate_simulation` hard-zeros any run not ending in
  `AGENT_STOP`/`USER_STOP` (`evaluator.py:113`); ensure stop detection mirrors
  tau2 (`UserSimulator.is_stop`, agent transfer tool).
- **Subprocess/async/cost (#7).** Each simulation spawns a bundled Node CLI
  subprocess; the runner env needs `ANTHROPIC_API_KEY` and subprocess-spawn
  permission, and `--max-concurrency` now also bounds subprocess count. Map
  `ResultMessage.total_cost_usd`/`usage` onto agent turns so `get_cost` totals stay
  comparable.
- **Scope of first cut:** target domains where only the agent holds tools
  (airline / retail / telecom standard). Domains that give the *user* tools, and
  banking_knowledge retrieval, are a later extension.

## Deliverables & sequencing

1. **Add dependency:** `claude-agent-sdk` to `pyproject.toml` (and keep the
   `anthropic`-based one-step adapter from the prior plan as a cheaper baseline if
   wanted). `uv sync`.
2. **Phase A — standalone experiment script** `examples/agents/claude_sdk_loop_eval.py`:
   the async driver above + a small runner over N tasks that prints/saves
   `reward` per task and aggregate. Fastest path to answer "does the loop help?"
   without touching the CLI. Compare head-to-head against
   `tau2 run --agent llm_agent --agent-llm anthropic/<same-model>` on the same
   tasks/seed.
3. **Phase B (only if results are promising) — productionize:** wrap the driver as
   a `ClaudeSDKLoopOrchestrator` selected by a CLI flag, mirroring how
   `--audio-native` swaps in `FullDuplexOrchestrator` (`runner/build.py` +
   `cli.py`), so `tau2 run` drives it at scale with existing reporting/resume.

## Verification (end to end)

1. **Smoke (mock domain):** run the driver on one `mock` task; assert the run
   completes, the assembled `trajectory` contains `assistant(tool_calls)` +
   `tool` messages in order followed by a final text turn ending in
   `USER_STOP`/`AGENT_STOP`, and `reward_info.reward` is computed.
2. **Tools-only lockdown check:** confirm via the stream/logs that the model only
   ever calls `mcp__env__*` tools (no Bash/Read/etc.) — i.e. `disallowed_tools`
   took effect.
3. **Ordering/capture smoke:** construct/seek a task turn that triggers multiple
   tool calls; verify each call is captured (hook `tool_use_id` ↔ stream
   `ToolUseBlock.id` match, results joined correctly), recorded order follows the
   stream, and it is stable across repeated runs (validates the hooks+stream
   capture for #6).
4. **Replay fidelity:** confirm the DB check passes on a task the baseline agent
   also solves — i.e. the captured trajectory replays cleanly in
   `EnvironmentEvaluator` (no `set_state` warnings about mismatched tool results).
5. **Head-to-head:** run ~10 `airline` tasks both ways (SDK loop vs. baseline
   `llm_agent`, same model + seed) and compare reward + cost; this is the actual
   experiment.
