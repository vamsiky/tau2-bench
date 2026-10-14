# claudedocs

Working notes for the Claude Agent SDK runner and the `banking_knowledge` domain. This
page covers how to run things; the analysis lives in the two subfolders.

| Folder | What is in it |
|---|---|
| [`benchmark-review/`](benchmark-review/README.md) | Correctness reviews of the benchmark itself (are the tasks well-posed?), one folder per domain and run: `benchmark-review/<domain>/<run date>-<benchmark version>/` |
| [`task-success/`](task-success/README.md) | Work on raising agent task success: failure analyses, prompt and policy fixes, retrieval experiments, design notes |
| [`i1_run_runbook.md`](i1_run_runbook.md) | Step-by-step commands for the I1 task runs and their post-hoc scoring |

## Run an evaluation on the Claude subscription (no API key)

The SDK runner drives the agent, the user simulator, and (with `--sdk-nl-judge`) the
NL-assertions judge through the Claude Agent SDK, using the Claude login on this machine.

```bash
# smoke test: one mock task
uv run python examples/agents/claude_sdk_loop_eval.py --domain mock --num-tasks 1 --sdk-nl-judge

# banking_knowledge with an offline retrieval config (alltools needs OPENAI_API_KEY)
uv run python examples/agents/claude_sdk_loop_eval.py --domain banking_knowledge \
    --retrieval-config bm25 --task-ids task_047 task_058 --num-trials 1 --sdk-nl-judge
```

Results go to `data/simulations/<run-name>/results.json`; browse them with
`tau2 view --file <path>`. Pass `--sdk-nl-judge` on every key-free run: without it,
tasks graded on NL assertions call the litellm judge, which needs an API key. Run
`--help` for the agent/user model and effort flags.

The `policy_register` retrieval variant reads
`task-success/policy-register/RhoBank_Policy_Register.md` at runtime, so keep that file
where it is.

## Run a benchmark correctness review

See [`benchmark-review/README.md`](benchmark-review/README.md): prompts, run layout,
and the report renderer.

## Run the I1 experiments

See [`i1_run_runbook.md`](i1_run_runbook.md).
