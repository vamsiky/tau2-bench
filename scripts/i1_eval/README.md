# I1 evaluation scripts

Permanent reconstructions of the post-hoc scoring scripts used in the I1
(banking_knowledge) investigation. They operate on an existing
`data/simulations/<run>/results.json` produced by the driver
(`examples/agents/claude_sdk_loop_eval.py`). See
`claudedocs/i1_run_runbook.md` for the full pipeline and the driver commands.

All scripts run from the repo root via `uv run python`.

## verified_score.py — "tau2-banking Verified" re-scorer

SABER tau-Bench-Verified style. Two relaxations vs the strict DB hash:
1. **Discoverable-tool audit as a superset:** gold's called tools must be a
   subset of the agent's calls (a *missing required* call still fails), but
   extra harmless reads are forgiven.
2. **Free-text fields excluded:** annotation-only fields (`closure_reason`) are
   dropped before comparison.

```bash
# Single task against one results file:
uv run python scripts/i1_eval/verified_score.py task_064 data/simulations/i1_fix5/results.json

# Built-in best-known I1 table (047/058/063/064/067):
uv run python scripts/i1_eval/verified_score.py
```

## diff_task.py — gold-vs-agent DB diff

Replays the recorded trajectory with `set_state` and diffs the resulting DB
against the gold DB. `+AGENT` = only in agent DB, `-GOLD` = only in gold,
`~` = differing value.

```bash
uv run python scripts/i1_eval/diff_task.py task_063 data/simulations/i1_fix5/results.json
# defaults: task_064 / data/simulations/i1_fix3/results.json
```

## bestof.py — best-of-N over trials

Across all trials of a run, reports whether ANY trial passes strict and/or
verified. Imports `verified_match` from `verified_score.py`.

```bash
uv run python scripts/i1_eval/bestof.py
# custom layout (template must contain {task}):
uv run python scripts/i1_eval/bestof.py "data/simulations/i1_g3i2_{task}/results.json"
```

## Notes

- All three import `_retrieval_env_kwargs` from `examples.agents.claude_sdk_loop_eval`
  and neutralize `sys.argv` before that import (the driver parses argv at import time).
- They assume `--domain banking_knowledge` and the `alltools` retrieval config,
  matching how the I1 runs were driven.
