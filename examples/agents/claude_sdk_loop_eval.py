#!/usr/bin/env python3
"""
Claude Agent SDK full-loop evaluation driver for tau2-bench (text / half-duplex).

The agent side is the Claude Agent SDK: it owns the inner agentic loop (multi-step
reasoning + tool calls) between user turns. tau2's environment, message model, and
evaluator are reused unchanged; only the agent (and, here, the user simulator) run
through the SDK.

Why the user simulator is also on the SDK: this machine has only a Claude
subscription (no working API key, no OpenAI key), so tau2's normal litellm path
can't authenticate. Running both participants through the SDK keeps everything on
the sanctioned subscription path and needs no API key.

Trajectory capture: SDK hooks (PreToolUse / PostToolUse / PostToolUseFailure ->
tool_use_id, input, result, error) joined with the stream (ToolUseBlock order =
authoritative ordering; ResultMessage = final text + cost). The assembled tau2
trajectory is scored by the unchanged evaluate_simulation().

With --sdk-nl-judge the NL-assertions judge ALSO runs on the SDK (subscription), so
every task scores with no API key. The whole pipeline (agent + user-sim + judge) is
then on the Claude subscription.

Output & resume: results are written in tau2's standard format to
  data/simulations/<run-name>/results.json
incrementally (one simulation checkpointed at a time), so the run is resumable -- re-
running with the same --save-to (and --auto-resume) skips already-completed tasks.
Inspect any run later with `tau2 view --file data/simulations/<run-name>/results.json`.

Logging: file logging is on by default at --log-level (written to <run-dir>/run.log);
add --log-to-terminal to also stream to stderr.

Usage:
    # a couple of tasks
    uv run python examples/agents/claude_sdk_loop_eval.py --task-ids 33 34 --sdk-nl-judge

    # the whole retail domain (all tasks), fully on subscription, resumable
    uv run python examples/agents/claude_sdk_loop_eval.py \
        --domain retail --sdk-nl-judge --save-to retail_full --auto-resume

    # resume after an interruption: same command again
"""
from __future__ import annotations

import argparse
import asyncio
import json
import multiprocessing
import os
import random
import sys
import time
import uuid
from pathlib import Path
from typing import Any, Optional

from loguru import logger

# Drop loguru's default DEBUG-to-stderr handler BEFORE importing tau2 (which logs the
# registry contents at DEBUG on import) so an unconfigured run doesn't flood the
# terminal. _setup_logging() installs the real file/terminal handlers at run time.
logger.remove()

from claude_agent_sdk import (
    AssistantMessage as SDKAssistantMessage,
    ClaudeAgentOptions,
    ClaudeSDKClient,
    HookMatcher,
    ResultMessage,
    TextBlock,
    ToolResultBlock,
    ToolUseBlock,
    UserMessage as SDKUserMessage,
    create_sdk_mcp_server,
    tool,
)

from tau2.agent.llm_agent import AGENT_INSTRUCTION, SYSTEM_PROMPT
from tau2.data_model.message import AssistantMessage, ToolCall, ToolMessage
from tau2.data_model.simulation import (
    AgentInfo,
    Info,
    Results,
    SimulationRun,
    TerminationReason,
    UserInfo,
)
from tau2.evaluator.evaluator import EvaluationType, evaluate_simulation
from tau2.orchestrator.modes import CommunicationMode
from tau2.orchestrator.orchestrator import DEFAULT_FIRST_AGENT_MESSAGE
from tau2.runner import build_environment, build_user, get_tasks
from tau2.runner.checkpoint import create_checkpoint_fns, try_resume
from tau2.runner.helpers import get_environment_info
from tau2.user.user_simulator import UserSimulator, get_global_user_sim_guidelines
from tau2.environment.toolkit import ToolType
from tau2.utils import DATA_DIR
from tau2.utils.llm_utils import get_cost
from tau2.utils.utils import get_commit_hash, get_now

# Importing tau2 loads .env, which here holds only a PLACEHOLDER ANTHROPIC_API_KEY.
# The SDK subprocess inherits the parent env (ClaudeAgentOptions.env is additive,
# not a replacement), and ANY ANTHROPIC_API_KEY -- even an invalid one -- overrides
# the subscription OAuth (apiKeySource becomes ANTHROPIC_API_KEY). Remove these from
# the parent process so the bundled CLI authenticates via the Claude subscription.
for _k in ("ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN", "ANTHROPIC_BASE_URL", "ANTHROPIC_CUSTOM_HEADERS"):
    os.environ.pop(_k, None)

MCP_SERVER_NAME = "env"
MCP_PREFIX = f"mcp__{MCP_SERVER_NAME}__"

# Generic agent-instruction augmentation (the fix under test); set in run_batch_async from
# --agent-extra-instruction-file. Single-process run, so a module global is sufficient.
_AGENT_EXTRA_INSTRUCTION = None

# Built-in Claude Code tools to remove from the model's context so it can only use
# the bridged environment tools. The PreToolUse deny-guard is the hard guarantee.
DISALLOWED_BUILTINS = [
    "Task", "Bash", "BashOutput", "KillShell", "Edit", "Write", "Read",
    "NotebookEdit", "Glob", "Grep", "WebFetch", "WebSearch", "TodoWrite",
    "ExitPlanMode", "AskUserQuestion", "Skill", "ToolSearch",
]

# Tool name prefixes that are clearly read-only (no DB mutation).
_READ_ONLY_PREFIXES = ("get_", "list_", "check_", "search_")

def _is_direct_readonly(tool_name: str) -> bool:
    """Heuristic: tool is read-only if its bare name starts with a read prefix."""
    return any(tool_name.startswith(p) for p in _READ_ONLY_PREFIXES)


def _build_recent_calls(captures: dict, mcp_prefix: str) -> list[tuple[str, dict, str]]:
    """Return completed tool calls from captures, expanding call_discoverable_agent_tool
    to show the inner tool name prominently."""
    result = []
    for cap in captures.values():
        if "result" not in cap:
            continue
        full_name = cap.get("name", "")
        if not full_name.startswith(mcp_prefix):
            continue
        bare = full_name.removeprefix(mcp_prefix)
        inp = cap.get("input", {})
        res = str(cap.get("result", ""))[:150]
        if bare == "call_discoverable_agent_tool":
            inner = inp.get("agent_tool_name", "?")
            result.append((f"call_discoverable_agent_tool[{inner}]", inp, res))
        else:
            result.append((bare, inp, res))
    return result


def _extract_conversation(trajectory: list) -> tuple[str, str]:
    """Return (first_customer_request, recent_conversation_summary).

    Walks the trajectory and formats user / assistant text turns and tool
    calls into a compact string.  We cap the summary to the last 20 lines
    so the verifier prompt stays concise.
    """
    first_req = ""
    lines: list[str] = []
    for m in trajectory:
        role = getattr(m, "role", None)
        content = getattr(m, "content", None)
        tool_calls = getattr(m, "tool_calls", None)
        if role == "user" and isinstance(content, str) and content.strip():
            if not first_req:
                first_req = content.strip()[:400]
            lines.append(f"Customer: {content.strip()[:200]}")
        elif role == "assistant" and isinstance(content, str) and content.strip():
            lines.append(f"Agent: {content.strip()[:200]}")
        elif role == "assistant" and tool_calls:
            for tc in tool_calls:
                inner = ""
                if tc.name == "call_discoverable_agent_tool":
                    inner = f"[{tc.arguments.get('agent_tool_name', '')}]"
                lines.append(f"Agent called: {tc.name}{inner}")
    return first_req, "\n".join(lines[-20:])


class AuxVerifier:
    """SABER-style auxiliary verifier gate.

    Before the agent executes a state-changing (WRITE) discoverable tool
    call, a lightweight Claude model re-reads the policy and the recent
    interaction history to verify:

      1. All policy-required preliminary steps have been performed.
      2. The chosen arguments / product / account match the customer's needs.
      3. No unnecessary optional arguments are included.

    If the proposed action fails any check the hook returns a deny with
    a specific reason, giving the agent a chance to correct itself.

    Implementation: uses `claude -p` (non-interactive CLI mode) via a
    subprocess.  This avoids the stream-conflict that arises from spawning
    a nested ClaudeSDKClient inside a PreToolUse hook callback.
    """

    _SYSTEM_PROMPT = (
        "You are a banking compliance checker reviewing a SINGLE proposed action.\n\n"
        "Your ONLY job: decide if THIS SPECIFIC proposed action is correct to execute NOW.\n\n"
        "IMPORTANT: Start your response with APPROVED or BLOCKED (no markdown, no asterisks).\n\n"
        "APPROVED — if ALL are true for THIS action:\n"
        "  1. Required preliminary checks for THIS action appear in TOOLS CALLED SO FAR\n"
        "  2. Parameters match what the customer explicitly requested\n"
        "  3. No missing required arguments\n\n"
        "BLOCKED: <reason> — ONLY if:\n"
        "  1. A required pre-check for THIS SPECIFIC action is missing from TOOLS CALLED SO FAR\n"
        "  2. Wrong product/tier/account selected (does not match customer's stated request)\n"
        "  3. A required parameter is missing or incorrect\n\n"
        "DO NOT BLOCK because:\n"
        "  - Other parts of a multi-step request are still pending (handling actions one at a time\n"
        "    is correct; a customer asking for two accounts does NOT mean both must open in one call)\n"
        "  - Customer 'hasn't explicitly confirmed' when they expressed clear intent\n"
        "  - A future related action hasn't happened yet\n\n"
        "VALUE-CORRECTNESS CHECKS (use the POLICY text provided; these are generic, not tied to any one task):\n"
        "  - COMPUTED NUMBERS: if the action sets a number you can derive from the policy\n"
        "    (an interest rate / APY, a credited or refunded amount, a fee, a liability\n"
        "    amount), re-derive it from the policy formula. Add only the rate components /\n"
        "    bonuses the policy explicitly lists, and do NOT stack bonuses unless the policy\n"
        "    says so. BLOCK if the proposed value does not match your derivation.\n"
        "  - COUNT / CAP LIMITS: if the policy caps how many items may carry a flag (e.g.\n"
        "    how many disputes are eligible_for_provisional_credit / provisional_credit_eligible),\n"
        "    count how many are flagged across THIS and prior calls, subtract any consumed by\n"
        "    prior history, and BLOCK if the count exceeds the cap or flags items other than the\n"
        "    specific ones the rule selects (e.g. the top-N by amount).\n"
        "  - CLASSIFICATION FIELDS: if the action sets a category/type enum (dispute_category,\n"
        "    transaction_type, dispute_reason), check it against the transaction's concrete facts\n"
        "    (PIN entered? card physically present? in-person vs online?) and the policy's\n"
        "    definitions. BLOCK if the enum does not match the facts (e.g. a PIN/in-person charge\n"
        "    labeled online_purchase / card_not_present_fraud).\n\n"
        "CRITICAL DOMAIN PRE-CHECK RULES (check TOOLS CALLED SO FAR):\n"
        "  log_credit_card_closure_reason_4521:\n"
        "    BLOCK unless BOTH of these appear in prior calls for the SAME credit_card_account_id:\n"
        "      - get_user_dispute_history_7291\n"
        "      - get_pending_replacement_orders_5765 (with that card's account ID)\n"
        "  order_replacement_credit_card_7291:\n"
        "    BLOCK unless BOTH appear in prior calls:\n"
        "      - get_user_dispute_history_7291\n"
        "      - get_pending_replacement_orders_5765\n"
        "  close_bank_account_7392:\n"
        "    BLOCK unless get_user_dispute_history_7291 appears in prior calls.\n\n"
        "CRITICAL FORMAT: First word of your response must be exactly APPROVED or BLOCKED.\n"
        "Do not add ** or any other formatting."
    )

    def __init__(self, policy: str, model: str, effort: str = "low"):
        self.policy = policy
        self.model = model
        self.effort = effort

    async def verify(
        self,
        proposed_tool: str,
        tool_args: dict,
        customer_request: str,
        recent_conversation: str,
        recent_calls: list[tuple[str, dict, str]],
    ) -> tuple[bool, str]:
        """Return (approved, reason). On any error, approve to avoid false blocks."""
        def _fmt_call(n: str, inp: dict, r: str) -> str:
            # Show key args (account IDs, tool names) so verifier can match pre-checks
            key_args = {k: v for k, v in inp.items()
                        if k in ("credit_card_account_id", "account_id", "user_id",
                                 "agent_tool_name", "arguments")}
            args_str = json.dumps(key_args, default=str) if key_args else ""
            return f"  {n}({args_str})  →  {r[:60]}"

        calls_str = "\n".join(
            _fmt_call(n, inp, r) for (n, inp, r) in recent_calls[-15:]
        ) or "  (none yet)"

        # Truncate policy to avoid overly long prompts; the verifier needs the
        # relevant sections, not necessarily the entire document.
        policy_excerpt = self.policy[:6000] if len(self.policy) > 6000 else self.policy

        prompt = (
            f"POLICY:\n{policy_excerpt}\n\n"
            f"CUSTOMER REQUEST: {customer_request or '(unknown)'}\n\n"
            f"RECENT CONVERSATION:\n{recent_conversation or '(none)'}\n\n"
            f"TOOLS CALLED SO FAR THIS EPISODE:\n{calls_str}\n\n"
            f"PROPOSED ACTION: {proposed_tool}(\n"
            f"  {json.dumps(tool_args, indent=2, default=str)}\n)\n\n"
            "Is this action correct and complete?\n"
            "Reply APPROVED or BLOCKED: <reason>."
        )

        # Use `claude -p` (non-interactive) to avoid nested-subprocess stream
        # conflicts that occur with ClaudeSDKClient inside a hook callback.
        cmd = [
            "claude", "-p",
            "--model", self.model,
            "--dangerously-skip-permissions",
            "--system-prompt", self._SYSTEM_PROMPT,
        ]
        if self.effort and self.effort != "default":
            cmd += ["--effort", self.effort]

        try:
            proc = await asyncio.create_subprocess_exec(
                *cmd,
                stdin=asyncio.subprocess.PIPE,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE,
                env=clean_env(),
            )
            stdout, stderr = await asyncio.wait_for(
                proc.communicate(input=prompt.encode()), timeout=120
            )
            text = stdout.decode(errors="replace").strip()
            if not text and stderr:
                err = stderr.decode(errors="replace").strip()[:200]
                logger.warning(f"[AuxVerifier] stderr for {proposed_tool}: {err}")
                return True, f"verifier stderr (allowing): {err}"
            # Normalize: strip markdown bold markers and whitespace for robust parsing
            text_norm = text.lstrip("*").strip()
            upper = text_norm.upper()
            if upper.startswith("APPROVED"):
                return True, text_norm
            if upper.startswith("BLOCKED"):
                reason = text_norm[7:].lstrip(":*").strip()
                return False, reason
            # Check if APPROVED or BLOCKED appears anywhere in the first line
            first_line = text_norm.split("\n")[0].upper()
            if "APPROVED" in first_line:
                return True, text_norm
            if "BLOCKED" in first_line:
                # Extract reason from rest of text
                rest = "\n".join(text_norm.split("\n")[1:]).strip()
                return False, rest or text_norm
            # Ambiguous response → allow through
            logger.debug(f"[AuxVerifier] ambiguous reply for {proposed_tool}: {text!r}")
            return True, text
        except asyncio.TimeoutError:
            logger.warning(f"[AuxVerifier] timeout verifying {proposed_tool}")
            return True, "timeout (allowing through)"
        except Exception as exc:
            logger.warning(f"[AuxVerifier] error verifying {proposed_tool}: {exc}")
            return True, str(exc)


def clean_env() -> dict:
    """Env for the SDK subprocess: drop anything that would route the bundled CLI
    away from its subscription OAuth (api key / base url / proxy headers), and drop
    this harness's own session vars so the subprocess starts from a clean slate."""
    drop = {
        "ANTHROPIC_API_KEY", "ANTHROPIC_AUTH_TOKEN",
        "ANTHROPIC_BASE_URL", "ANTHROPIC_CUSTOM_HEADERS",
    }
    return {
        k: v for k, v in os.environ.items()
        if k not in drop and not k.startswith("CLAUDE_CODE") and k not in ("CLAUDECODE", "CLAUDE_EFFORT")
    }


def _extract_text(resp: Any) -> str:
    """Pull plain text out of an MCP tool result / tool_response in any of its shapes."""
    if resp is None:
        return ""
    if isinstance(resp, str):
        return resp
    if isinstance(resp, dict):
        content = resp.get("content")
        if isinstance(content, list):
            parts = [b.get("text", "") for b in content
                     if isinstance(b, dict) and b.get("type") == "text"]
            return "".join(parts) if parts else json.dumps(resp)
        if isinstance(content, str):
            return content
        return json.dumps(resp)
    if isinstance(resp, list):
        parts = []
        for b in resp:
            if isinstance(b, dict) and b.get("type") == "text":
                parts.append(b.get("text", ""))
            elif isinstance(b, str):
                parts.append(b)
            else:
                t = getattr(b, "text", None)
                if t:
                    parts.append(t)
        return "".join(parts)
    return str(resp)


def _make_sdk_tool(tau2_tool, env, lock: asyncio.Lock):
    """Wrap a tau2 Tool as an in-process SDK MCP tool that executes against the env."""
    name = tau2_tool.name
    fn = tau2_tool.openai_schema["function"]
    description = fn.get("description") or name
    input_schema = fn["parameters"]

    @tool(name, description, input_schema)
    async def _handler(args: dict) -> dict:
        tc = ToolCall(name=name, arguments=dict(args), requestor="assistant")
        async with lock:  # serialize env access against concurrent tool dispatch
            tool_msg = await asyncio.to_thread(env.get_response, tc)
        text = tool_msg.content if tool_msg.content is not None else ""
        return {"content": [{"type": "text", "text": text}], "is_error": bool(tool_msg.error)}

    return _handler


def _build_agent_options(env, agent_model, captures, denials, lock,
                         agent_effort=None, agent_extra_instruction=None,
                         aux_verifier: "AuxVerifier | None" = None,
                         trajectory: "list | None" = None) -> ClaudeAgentOptions:
    tau2_tools = env.get_tools()
    sdk_tools = [_make_sdk_tool(t, env, lock) for t in tau2_tools]
    server = create_sdk_mcp_server(name=MCP_SERVER_NAME, version="1.0.0", tools=sdk_tools)
    allowed = [f"{MCP_PREFIX}{t.name}" for t in tau2_tools]
    # Generic, domain-agnostic instruction augmentation (the "fix" under test). Appended
    # to the base agent instruction -- never to the retrieved <policy> -- so it carries no
    # task/policy/tool-specific content.
    agent_instruction = AGENT_INSTRUCTION
    if agent_extra_instruction:
        agent_instruction = AGENT_INSTRUCTION + "\n\n" + agent_extra_instruction.strip()
    system_prompt = SYSTEM_PROMPT.format(
        domain_policy=env.get_policy(), agent_instruction=agent_instruction
    )

    async def rec_pre(input_data, tool_use_id, context):
        tname = input_data.get("tool_name", "")
        tool_input = input_data.get("tool_input", {})
        if not tname.startswith(MCP_PREFIX):
            denials.append(tname)
            return {"hookSpecificOutput": {
                "hookEventName": "PreToolUse",
                "permissionDecision": "deny",
                "permissionDecisionReason": "Only environment tools are allowed.",
            }}
        bare = tname.removeprefix(MCP_PREFIX)
        cap = captures.setdefault(tool_use_id, {})
        cap["name"] = tname
        cap["input"] = tool_input

        # --- SABER aux-verifier gate ---
        # Only intercept call_discoverable_agent_tool for WRITE inner tools.
        # Direct tools (log_verification, unlock_*, KB_search_*, shell, etc.)
        # are either always-correct operations or read-only and are left alone.
        if aux_verifier is not None:
            should_verify = False
            proposed_label = bare
            if bare == "call_discoverable_agent_tool":
                inner_name = tool_input.get("agent_tool_name", "")
                proposed_label = f"call_discoverable_agent_tool[{inner_name}]"
                if inner_name and hasattr(env, "tools") and env.tools is not None:
                    try:
                        tt = env.tools.tool_type(inner_name)
                        should_verify = (tt == ToolType.WRITE)
                    except (KeyError, AttributeError):
                        should_verify = True  # unknown inner tool → verify to be safe

            if should_verify:
                traj = trajectory or []
                first_req, conversation = _extract_conversation(traj)
                recent = _build_recent_calls(captures, MCP_PREFIX)
                approved, reason = await aux_verifier.verify(
                    proposed_label, tool_input, first_req, conversation, recent
                )
                if not approved:
                    logger.info(f"[AuxVerifier] BLOCKED {proposed_label}: {reason}")
                    cap["_blocked"] = reason
                    return {"hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": (
                            f"Action not yet approved: {reason}. "
                            "Complete any missing required steps first, then retry."
                        ),
                    }}
                else:
                    logger.debug(f"[AuxVerifier] APPROVED {proposed_label}")

        return {}

    async def rec_post(input_data, tool_use_id, context):
        cap = captures.setdefault(tool_use_id, {})
        cap["result"] = _extract_text(input_data.get("tool_response"))
        cap["is_error"] = False
        return {}

    async def rec_fail(input_data, tool_use_id, context):
        cap = captures.setdefault(tool_use_id, {})
        cap["result"] = str(input_data.get("error", ""))
        cap["is_error"] = True
        return {}

    return ClaudeAgentOptions(
        model=agent_model,
        effort=agent_effort,
        system_prompt=system_prompt,
        mcp_servers={MCP_SERVER_NAME: server},
        allowed_tools=allowed,
        disallowed_tools=DISALLOWED_BUILTINS,
        permission_mode="bypassPermissions",
        setting_sources=[],
        env=clean_env(),
        hooks={
            "PreToolUse": [HookMatcher(hooks=[rec_pre])],
            "PostToolUse": [HookMatcher(hooks=[rec_post])],
            "PostToolUseFailure": [HookMatcher(hooks=[rec_fail])],
        },
    )


async def _consume(client) -> dict:
    """Drive one SDK turn to completion; return final text + (ordered) tool ids + cost."""
    tool_ids: list[str] = []
    stream_results: dict[str, tuple[str, bool]] = {}
    last_text: list[str] = []
    cost: Optional[float] = None
    usage: Optional[dict] = None
    result_text: Optional[str] = None
    async for m in client.receive_response():
        if isinstance(m, SDKAssistantMessage):
            here: list[str] = []
            for b in m.content:
                if isinstance(b, ToolUseBlock):
                    tool_ids.append(b.id)
                elif isinstance(b, TextBlock):
                    here.append(b.text)
            if here:
                last_text = here
        elif isinstance(m, SDKUserMessage):
            content = m.content
            if isinstance(content, list):
                for b in content:
                    if isinstance(b, ToolResultBlock):
                        stream_results[b.tool_use_id] = (
                            _extract_text(b.content), bool(getattr(b, "is_error", False)))
        elif isinstance(m, ResultMessage):
            cost, usage, result_text = m.total_cost_usd, m.usage, m.result
    final_text = "".join(last_text).strip() or (result_text or "").strip()
    return dict(final_text=final_text, tool_ids=tool_ids, stream_results=stream_results,
                cost=cost, usage=usage)


def _retrieval_env_kwargs(domain, retrieval_config, retrieval_kwargs) -> dict:
    """env_kwargs that select the banking_knowledge retrieval variant (no-op for
    other domains, whose constructors don't accept retrieval_variant)."""
    if domain != "banking_knowledge" or not retrieval_config:
        return {}
    kw = {"retrieval_variant": retrieval_config}
    if retrieval_kwargs:
        kw["retrieval_kwargs"] = dict(retrieval_kwargs)
    return kw


async def run_episode(task, domain, *, agent_model, user_model, user_effort="high",
                      agent_effort=None, trial=0, max_steps=50, seed=42,
                      eval_type=EvaluationType.ALL, sdk_nl_judge=False,
                      verified_scorer=True,
                      retrieval_config=None, retrieval_kwargs=None,
                      agent_extra_instruction=None,
                      use_aux_verifier: bool = False,
                      aux_verifier_model: str | None = None,
                      aux_verifier_effort: str = "low") -> SimulationRun:
    if task.initial_state is not None and task.initial_state.message_history:
        raise NotImplementedError(f"Task {task.id} has seeded history; v1 supports fresh tasks only.")

    # Retrieval variant (banking_knowledge): the agent gets exactly the tau2
    # retrieval tools for this variant -- bridged like any env tool -- and the
    # evaluator rebuilds its gold/predicted envs with the SAME variant so the
    # DB/ACTION replay matches. Identical surface to the CLI, so comparable.
    eval_env_kwargs = _retrieval_env_kwargs(domain, retrieval_config, retrieval_kwargs)
    runtime_env_kwargs = dict(eval_env_kwargs)
    if domain == "banking_knowledge":
        # golden_retrieval builds its policy from the task; harmless otherwise.
        runtime_env_kwargs["task"] = task
    env = build_environment(domain, env_kwargs=runtime_env_kwargs)
    init = task.initial_state
    env.set_state(
        initialization_data=init.initialization_data if init else None,
        initialization_actions=init.initialization_actions if init else None,
        message_history=[],
    )
    # User simulator runs on the registered SDK backend (subscription, opus/high by
    # default): a persistent multi-turn SDK session, configurable via user_model /
    # user_effort. It owns its own system prompt (guidelines + scenario + persona).
    user = build_user("sdk_user_simulator", env, task, llm=user_model,
                      llm_args={"effort": user_effort})
    # Bind the env so the user simulator can execute any user-side tools (e.g.
    # banking_knowledge: apply_for_credit_card) against the same environment.
    user.bind_environment(env)
    user_state = user.get_init_state()

    # Build trajectory early so the aux-verifier hook can read it as it fills up.
    trajectory: list = []

    # Aux-verifier: optional SABER-style gate that blocks WRITE discoverable tool calls
    # that are missing required pre-checks or have wrong arguments.
    aux_verifier: AuxVerifier | None = None
    if use_aux_verifier:
        v_model = aux_verifier_model or "claude-haiku-4-5-20251001"
        aux_verifier = AuxVerifier(
            policy=env.get_policy(), model=v_model, effort=aux_verifier_effort
        )
        logger.info(f"[AuxVerifier] enabled model={v_model} effort={aux_verifier_effort}")

    captures: dict[str, dict] = {}
    denials: list[str] = []
    tools_called: list[str] = []
    multi_tool_turns = 0
    lock = asyncio.Lock()
    agent_opts = _build_agent_options(env, agent_model, captures, denials, lock,
                                      agent_effort=agent_effort,
                                      agent_extra_instruction=agent_extra_instruction,
                                      aux_verifier=aux_verifier,
                                      trajectory=trajectory)

    greeting = DEFAULT_FIRST_AGENT_MESSAGE.model_copy(deep=True)
    greeting.timestamp = get_now()
    trajectory.append(greeting)
    agent_last_text = greeting.content

    termination = TerminationReason.MAX_STEPS
    start_time = get_now()
    start_perf = time.perf_counter()
    steps_done = 0

    try:
      async with ClaudeSDKClient(options=agent_opts) as agent_client:
        for step in range(max_steps):
            steps_done = step + 1
            # ---- user turn (registered SDK user simulator; persistent session) ----
            agent_in = AssistantMessage(role="assistant", content=agent_last_text)
            user_msg, user_state = await asyncio.to_thread(
                user.generate_next_message, agent_in, user_state)
            # Any user-side tool calls made this turn (e.g. apply_for_credit_card)
            # are recorded into the trajectory before the spoken message, so the
            # evaluator's DB/ACTION replay sees them (ids already matched).
            for m in getattr(user, "last_turn_tool_messages", []):
                m.timestamp = get_now()
                trajectory.append(m)
            if not user_msg.content:
                user_msg.content = "(no response)"
            user_msg.timestamp = get_now()
            user_msg.validate()
            trajectory.append(user_msg)
            if UserSimulator.is_stop(user_msg):
                termination = TerminationReason.USER_STOP
                break

            # ---- agent turn (SDK owns inner loop; tools captured via hooks) ----
            await agent_client.query(user_msg.content)
            a = await _consume(agent_client)

            if len(a["tool_ids"]) > 1:
                multi_tool_turns += 1
            for tid in a["tool_ids"]:
                cap = captures.get(tid, {})
                full = cap.get("name") or ""
                if not full.startswith(MCP_PREFIX):
                    continue  # denied built-in / non-env tool: not part of the env trajectory
                name = full.removeprefix(MCP_PREFIX)
                tools_called.append(name)
                args = cap.get("input") or {}
                if "result" in cap:
                    res_text, is_err = cap["result"], cap.get("is_error", False)
                elif tid in a["stream_results"]:
                    res_text, is_err = a["stream_results"][tid]
                else:
                    res_text, is_err = "", False
                tc = ToolCall(id=tid, name=name, arguments=dict(args), requestor="assistant")
                trajectory.append(AssistantMessage(role="assistant", tool_calls=[tc],
                                                   cost=0.0, timestamp=get_now()))
                trajectory.append(ToolMessage(id=tid, role="tool", content=res_text,
                                              requestor="assistant", error=is_err,
                                              timestamp=get_now()))

            agent_text = a["final_text"]
            if not agent_text:
                logger.warning(f"[{task.id}] agent produced no final text on turn {step}")
                agent_text = "(no response)"
            agent_msg = AssistantMessage(role="assistant", content=agent_text,
                                         cost=a["cost"], usage=a["usage"], timestamp=get_now())
            agent_msg.validate()
            trajectory.append(agent_msg)
            agent_last_text = agent_text
    finally:
        user.close()  # tear down the persistent user-sim SDK session/subprocess

    duration = time.perf_counter() - start_perf
    try:
        cost = get_cost(trajectory)
        agent_cost, user_cost = cost if cost else (None, None)
    except Exception as e:
        logger.warning(f"get_cost failed: {e}")
        agent_cost, user_cost = None, None

    simulation = SimulationRun(
        id=uuid.uuid4().hex, task_id=task.id, start_time=start_time, end_time=get_now(),
        duration=duration, termination_reason=termination, agent_cost=agent_cost,
        user_cost=user_cost, messages=trajectory, seed=seed, trial=trial,
        mode=CommunicationMode.HALF_DUPLEX.value,
    )
    reward_info = evaluate_simulation(
        simulation=simulation, task=task, evaluation_type=eval_type, solo_mode=False,
        domain=domain, mode=CommunicationMode.HALF_DUPLEX,
        use_sdk_nl_judge=sdk_nl_judge, env_kwargs=eval_env_kwargs,
        use_verified_scorer=verified_scorer,
    )
    simulation.reward_info = reward_info

    if denials:
        logger.warning(f"[{task.id}] denied non-env tool attempts: {denials}")
    logger.info(
        f"[{task.id}] reward={reward_info.reward} term={termination.value} turns={steps_done} "
        f"tools_called={tools_called} multi_tool_turns={multi_tool_turns} "
        f"agent_cost={agent_cost} db_check={reward_info.db_check}"
    )
    return simulation


def _clean_model_name(model: str) -> str:
    """Last path segment of a model id, for use in a run-directory name."""
    return [x for x in str(model).split("/") if x][-1]


def _resolve_save_path(args) -> Path:
    """Mirror the CLI layout: data/simulations/<run_name>/results.json."""
    if args.save_to:
        name = args.save_to
    else:
        name = (
            f"{get_now(use_compact_format=True)}_{args.domain}_claude_sdk_loop_"
            f"{_clean_model_name(args.agent_model)}_sdk_user_"
            f"{_clean_model_name(args.user_model)}"
        )
    return DATA_DIR / "simulations" / name / "results.json"


def _setup_logging(log_file: Path, level: str, to_terminal: bool) -> None:
    """File logging on by default at the configured level; optionally also to stderr.

    Replaces loguru's default (DEBUG-to-stderr) handler — that default is why an
    unconfigured run floods the terminal."""
    logger.remove()
    log_file.parent.mkdir(parents=True, exist_ok=True)
    logger.add(str(log_file), level=level, enqueue=True, backtrace=False, diagnose=False)
    if to_terminal:
        logger.add(sys.stderr, level=level)


def _build_info(args, tasks, retrieval_config, retrieval_kwargs) -> Info:
    """Build a tau2 Info block describing this SDK run (used for the results file
    and for resume's config-change detection). Mirrors runner.helpers.get_info."""
    agent_info = AgentInfo(
        implementation="claude_sdk_loop",
        llm=args.agent_model,
        llm_args=({"effort": args.agent_effort} if args.agent_effort else None),
    )
    user_info = UserInfo(
        implementation="sdk_user_simulator",
        llm=args.user_model,
        llm_args={"effort": args.user_effort},
        global_simulation_guidelines=get_global_user_sim_guidelines(),
    )
    env_info_kwargs = _retrieval_env_kwargs(args.domain, retrieval_config, retrieval_kwargs)
    environment_info = get_environment_info(
        args.domain, include_tool_info=False, env_kwargs=env_info_kwargs
    )
    return Info(
        git_commit=get_commit_hash(),
        num_trials=args.num_trials,
        max_steps=args.max_steps,
        max_errors=args.max_errors,
        user_info=user_info,
        agent_info=agent_info,
        environment_info=environment_info,
        seed=args.seed,
        retrieval_config=retrieval_config,
        retrieval_config_kwargs=retrieval_kwargs,
    )


def _warm_banking_cache(retrieval_config, retrieval_kwargs) -> None:
    """Pre-warm the banking_knowledge KB cache, mirroring the CLI. Embeddings are
    computed only for embedding variants (which need an embedding API key);
    lexical variants (grep_only, bm25*, full_kb) just load documents -> no API."""
    from tau2.knowledge.embeddings_cache import (
        get_unique_embedder_configs_for_retrieval_configs,
        warm_kb_cache,
    )

    kwargs = retrieval_kwargs or {}
    embedder_configs = None
    if retrieval_config:
        embedder_configs = get_unique_embedder_configs_for_retrieval_configs(
            [retrieval_config], kwargs
        )
    if embedder_configs:
        logger.info(
            f"Warming KB embeddings cache for variant={retrieval_config} "
            f"({len(embedder_configs)} embedder config(s)); this needs an embedding API key."
        )
    else:
        logger.info(
            f"Loading KB documents for variant={retrieval_config} (lexical/in-prompt; no embedding API)."
        )
    warm_kb_cache(embedder_configs)


def _configure_judge(args) -> str:
    """Apply SDK judge model/effort overrides; return a banner note."""
    if not args.sdk_nl_judge:
        return ""
    from tau2.evaluator.evaluator_nl_assertions_sdk import SDKNLAssertionsEvaluator
    if args.judge_model:
        SDKNLAssertionsEvaluator.MODEL = args.judge_model
    if args.judge_effort:
        SDKNLAssertionsEvaluator.EFFORT = args.judge_effort
    return f" nl_judge=SDK({SDKNLAssertionsEvaluator.MODEL}/{SDKNLAssertionsEvaluator.EFFORT})"


async def run_batch_async(args) -> None:
    # ---- generic agent-instruction fix (optional) ----
    global _AGENT_EXTRA_INSTRUCTION
    if args.agent_extra_instruction_file:
        with open(args.agent_extra_instruction_file) as _f:
            _AGENT_EXTRA_INSTRUCTION = _f.read().strip()
        print(f"  agent-extra-instruction: {len(_AGENT_EXTRA_INSTRUCTION)} chars from "
              f"{args.agent_extra_instruction_file}")
    # ---- task selection ----
    tasks_all = get_tasks(args.domain, task_ids=args.task_ids, num_tasks=args.num_tasks)
    runnable, skipped = [], []
    for t in tasks_all:
        if t.initial_state and t.initial_state.message_history:
            skipped.append(t.id)
        else:
            runnable.append(t)
    if not runnable:
        raise ValueError(
            f"No runnable tasks for domain={args.domain} "
            f"(all {len(tasks_all)} have seeded history, unsupported by this driver)."
        )
    tasks = runnable

    eval_type = EvaluationType(args.eval_type)
    judge_note = _configure_judge(args)

    # ---- retrieval config (banking_knowledge only) ----
    is_banking = args.domain == "banking_knowledge"
    retrieval_kwargs = (
        json.loads(args.retrieval_config_kwargs) if args.retrieval_config_kwargs else None
    )
    if args.retrieval_config and not is_banking:
        logger.warning(
            f"--retrieval-config is only used for banking_knowledge; ignoring for domain={args.domain}."
        )
    # Banking defaults to 'alltools' (same as the CLI); make it explicit so Info,
    # the runtime env, and the evaluator all agree on one variant.
    retrieval_config = (args.retrieval_config or "alltools") if is_banking else None

    # ---- save path + logging ----
    save_path = _resolve_save_path(args)
    save_dir = save_path.parent
    log_file = Path(args.log_file) if args.log_file else save_dir / "run.log"
    _setup_logging(log_file, args.log_level, args.log_to_terminal)
    if skipped:
        logger.warning(
            f"Skipping {len(skipped)} task(s) with seeded message history "
            f"(unsupported by the SDK driver): {skipped}"
        )

    # ---- warm banking KB cache (no-op / lexical-only for non-embedding variants) ----
    if is_banking:
        _warm_banking_cache(retrieval_config, retrieval_kwargs)

    # ---- results + checkpoint resume (reuses tau2's machinery) ----
    info = _build_info(args, tasks, retrieval_config, retrieval_kwargs)
    results = Results(info=info, tasks=tasks, simulations=[])
    lock = multiprocessing.Lock()
    results, done_runs, tasks = try_resume(
        save_path=save_path,
        simulation_results=results,
        tasks=tasks,
        num_trials=args.num_trials,
        auto_resume=args.auto_resume,
        results_format="json",
    )
    save_fn, _ = create_checkpoint_fns(save_path, lock)

    # ---- seeds per trial (same scheme as the CLI batch runner) ----
    random.seed(args.seed)
    seeds = [random.randint(0, 1000000) for _ in range(args.num_trials)]

    total = len(tasks) * args.num_trials
    banner = (
        f"SDK batch: domain={args.domain} agent={args.agent_model}"
        f"{('/' + args.agent_effort) if args.agent_effort else ''} "
        f"user={args.user_model}/{args.user_effort} trials={args.num_trials} "
        f"eval={eval_type.value}{judge_note}"
        f"{(' retrieval=' + retrieval_config) if retrieval_config else ''}\n"
        f"  tasks={len(tasks)} total_runs={total} already_done={len(done_runs)} "
        f"remaining={total - len(done_runs)}\n"
        f"  save_to={save_path}\n  log={log_file} (level={args.log_level}, "
        f"terminal={'on' if args.log_to_terminal else 'off'})\n"
    )
    print(banner)
    logger.info(banner.replace("\n", " | "))

    # ---- run loop (sequential to respect subscription rate limits) ----
    n_done = 0
    for trial in range(args.num_trials):
        seed = seeds[trial]
        for task in tasks:
            key = (trial, task.id, seed)
            if key in done_runs:
                continue
            try:
                sim = await run_episode(
                    task, args.domain,
                    agent_model=args.agent_model, agent_effort=args.agent_effort,
                    user_model=args.user_model, user_effort=args.user_effort,
                    trial=trial, max_steps=args.max_steps, seed=seed,
                    eval_type=eval_type, sdk_nl_judge=args.sdk_nl_judge,
                    verified_scorer=args.verified_scorer,
                    retrieval_config=retrieval_config, retrieval_kwargs=retrieval_kwargs,
                    agent_extra_instruction=_AGENT_EXTRA_INSTRUCTION,
                    use_aux_verifier=args.use_aux_verifier,
                    aux_verifier_model=args.aux_verifier_model,
                    aux_verifier_effort=args.aux_verifier_effort,
                )
            except Exception as e:
                # Don't checkpoint a failure -> it stays out of done_runs and is
                # retried on the next (resumed) run.
                logger.exception(f"Task {task.id} (trial {trial}) failed: {e}")
                print(f"  ! task {task.id} trial {trial}: FAILED ({e})")
                continue
            await asyncio.to_thread(save_fn, sim)
            n_done += 1
            print(
                f"  [{n_done}/{total - len(done_runs)}] task {task.id} trial {trial}: "
                f"reward={sim.reward_info.reward} term={sim.termination_reason.value} "
                f"agent_cost={sim.agent_cost}"
            )

    # ---- summary from the on-disk results (includes resumed runs) ----
    final = Results.load(save_path)
    rewards = [s.reward_info.reward for s in final.simulations if s.reward_info]
    print("\n==================== SUMMARY ====================")
    print(f"  simulations on disk: {len(final.simulations)}")
    if rewards:
        print(
            f"  avg_reward={sum(rewards) / len(rewards):.3f}  n={len(rewards)}  "
            f"pass={sum(1 for r in rewards if r == 1.0)}"
        )
    print(f"\n  Results saved to: {save_path}")
    print(f"  Inspect with:     tau2 view --file {save_path}")


def main() -> None:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--domain", default="retail",
                   help="Domain / task set (retail, airline, telecom, mock, ...).")
    p.add_argument("--num-tasks", type=int, default=None,
                   help="Limit to the first N tasks. Default: all tasks in the domain.")
    p.add_argument("--task-ids", nargs="*", default=None,
                   help="Run only these task ids (overrides --num-tasks).")
    p.add_argument("--num-trials", type=int, default=1,
                   help="Number of trials per task.")
    p.add_argument("--agent-model", default="sonnet", help="SDK agent model (subscription).")
    p.add_argument("--agent-effort", default=None,
                   help="SDK agent reasoning effort: low|medium|high|max (default: SDK default).")
    p.add_argument("--user-model", default="claude-opus-4-8",
                   help="SDK user-sim model (subscription); default claude-opus-4-8.")
    p.add_argument("--user-effort", default="high",
                   help="SDK user-sim reasoning effort: low|medium|high|max (default: high).")
    p.add_argument("--eval-type", default="all", choices=[e.value for e in EvaluationType])
    p.add_argument("--no-verified-scorer", dest="verified_scorer", action="store_false",
                   help="Disable the tau2-Verified DB scorer and use the strict exact-hash "
                        "comparison instead. By default the verified scorer is on: extra "
                        "discoverable reads are allowed and free-text annotation fields "
                        "(e.g. closure_reason) are excluded.")
    p.set_defaults(verified_scorer=True)
    p.add_argument("--sdk-nl-judge", action="store_true",
                   help="Run the NL-assertions judge via the Claude SDK (subscription, "
                        "claude-opus-4-8/high) so NL-assertion tasks score with no API key.")
    p.add_argument("--judge-model", default=None,
                   help="Override the SDK NL-judge model (default: claude-opus-4-8).")
    p.add_argument("--judge-effort", default=None,
                   help="Override the SDK NL-judge effort: low|medium|high|max (default: high).")
    p.add_argument("--agent-extra-instruction-file", default=None,
                   help="Path to a text file whose contents are appended to the generic "
                        "agent instruction (NOT the policy). Used to test generic fixes.")
    # SABER aux-verifier gate
    p.add_argument("--use-aux-verifier", action="store_true",
                   help="Enable the SABER-style auxiliary verifier gate. Before each "
                        "WRITE discoverable tool call, a lightweight model checks: "
                        "(1) required pre-steps done, (2) correct parameters, "
                        "(3) minimal args. Blocks non-compliant calls with feedback.")
    p.set_defaults(use_aux_verifier=False)
    p.add_argument("--aux-verifier-model", default=None,
                   help="Model for the auxiliary verifier (default: claude-haiku-4-5-20251001).")
    p.add_argument("--aux-verifier-effort", default="low",
                   help="Reasoning effort for the auxiliary verifier: low|medium|high (default: low).")
    p.add_argument("--max-steps", type=int, default=50)
    p.add_argument("--max-errors", type=int, default=10, help="Recorded in run metadata.")
    p.add_argument("--seed", type=int, default=42)
    # banking_knowledge retrieval (ignored for other domains)
    p.add_argument("--retrieval-config", default=None,
                   help="banking_knowledge retrieval variant (e.g. grep_only, bm25_grep, "
                        "full_kb, golden_retrieval, alltools). Default for banking: alltools "
                        "(needs an OpenAI embeddings key). For a no-API-key run pick a lexical/"
                        "in-prompt variant like grep_only or full_kb.")
    p.add_argument("--retrieval-config-kwargs", default=None,
                   help="JSON dict of overrides passed to the retrieval variant (e.g. '{\"top_k\": 5}').")
    # Output / resume
    p.add_argument("--save-to", default=None,
                   help="Run name under data/simulations/<name>/results.json. "
                        "Default: <timestamp>_<domain>_claude_sdk_loop_<agent>_sdk_user_<user>. "
                        "Reusing an existing name resumes that run.")
    p.add_argument("--auto-resume", action="store_true",
                   help="Resume an existing run without prompting.")
    # Logging
    p.add_argument("--log-level", default="INFO",
                   help="Log level for the file (and terminal if enabled). Default: INFO.")
    p.add_argument("--log-to-terminal", action="store_true",
                   help="Also stream logs to the terminal (off by default; file always on).")
    p.add_argument("--log-file", default=None,
                   help="Override the log file path (default: <run-dir>/run.log).")
    args = p.parse_args()
    asyncio.run(run_batch_async(args))


if __name__ == "__main__":
    main()
