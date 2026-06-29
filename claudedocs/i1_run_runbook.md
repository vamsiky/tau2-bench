# I1 (banking_knowledge) Task Run Runbook

Reproducible commands for running the Claude Agent SDK full-loop pipeline against the
**I1** task category in `banking_knowledge`. Reconstructed from the 2026-06-25 session.

All commands run from the repo root: `/Users/vamsiconversive/github/tau2-bench`.

## Key architecture fact

The **driver, user-simulator, and NL-judge evaluation are a single fused command** —
`examples/agents/claude_sdk_loop_eval.py`. One process runs:

1. the Claude Agent SDK agent loop,
2. the SDK user-simulator (model defaults inside the driver: opus-4-8 / high — not a CLI flag),
3. the internal `evaluate_simulation` scorer (`--sdk-nl-judge` selects the SDK natural-language judge).

The **verified scorer** is a *separate, post-hoc* re-scoring step run on the produced
`results.json` — it is **not** a CLI flag.

## I1 task IDs

| Task ID  | Issue |
|----------|-------|
| task_047 | Missing required eligibility / completion checks |
| task_058 | Over-conservative write guard + wrong product selection |
| task_063 | Over-conservative write guard + missing action execution |
| task_064 | Over-conservative write guard |
| task_067 | Free-text `closure_reason` over-specification (grader artifact) |

## 1. Driver + user-sim + judge (the fused run)

Every run shares the same shape; only `--task-ids`, `--num-trials`,
`--agent-extra-instruction-file`, and `--save-to` change.

### Smoke (1 task, 1 trial)

```bash
timeout 600 uv run python examples/agents/claude_sdk_loop_eval.py \
  --domain banking_knowledge --task-ids task_047 --num-trials 1 \
  --agent-model claude-opus-4-8 --sdk-nl-judge \
  --save-to i1_smoke --log-level INFO 2>&1 | tail -40
```

### Validation (4 tasks x 4 trials)

```bash
nohup uv run python examples/agents/claude_sdk_loop_eval.py \
  --domain banking_knowledge --task-ids task_047 task_058 task_064 task_067 --num-trials 4 \
  --agent-model claude-opus-4-8 --sdk-nl-judge \
  --save-to i1_validation --auto-resume --log-level INFO \
  > data/simulations/i1_validation_stdout.log 2>&1 &
```

### Fix iterations (5 tasks, 1 trial)

Only `--agent-extra-instruction-file` and `--save-to` vary between iterations:

| Iter | instruction file                              | `--save-to` | task-ids                          |
|------|-----------------------------------------------|-------------|-----------------------------------|
| fix1 | `claudedocs/i1_fixes/fix1_act_on_behalf.txt`  | `i1_fix1`   | 047 058 063 064 067               |
| fix2 | `claudedocs/i1_fixes/fix2_minimality.txt`     | `i1_fix2`   | 047 058 063 064 067               |
| fix3 | `claudedocs/i1_fixes/fix3_policy_calibrated.txt` | `i1_fix3` | 047 058 063 064                   |
| fix4 | `claudedocs/i1_fixes/fix4_pointed.txt`        | `i1_fix4`   | 047 058 063 064                   |
| fix5 | `claudedocs/i1_fixes/fix5_premutation_reflection.txt` | `i1_fix5` | 047 058 063 064            |

Template:

```bash
nohup uv run python examples/agents/claude_sdk_loop_eval.py \
  --domain banking_knowledge --task-ids task_047 task_058 task_063 task_064 task_067 --num-trials 1 \
  --agent-model claude-opus-4-8 --sdk-nl-judge \
  --agent-extra-instruction-file claudedocs/i1_fixes/fix1_act_on_behalf.txt \
  --save-to i1_fix1 --auto-resume --log-level INFO \
  > data/simulations/i1_fix1_stdout.log 2>&1 &
```

### Final parallel runs (one process per task — avoids rate limits)

```bash
# Iteration G3.2 - fix6 pre-closure checklist, 1 trial each
for t in task_047 task_058 task_063 task_064 task_067; do
  nohup uv run python examples/agents/claude_sdk_loop_eval.py \
    --domain banking_knowledge --task-ids $t --num-trials 1 \
    --agent-model claude-opus-4-8 --sdk-nl-judge \
    --agent-extra-instruction-file claudedocs/i1_fixes/fix6_preclosure_checklist.txt \
    --save-to i1_g3i2_$t --auto-resume --log-level INFO \
    > data/simulations/i1_g3i2_${t}_stdout.log 2>&1 &
  sleep 3
done

# Iteration G3.3 - fix4 prompt, best-of-2 trials each
for t in task_047 task_058 task_063 task_064 task_067; do
  nohup uv run python examples/agents/claude_sdk_loop_eval.py \
    --domain banking_knowledge --task-ids $t --num-trials 2 \
    --agent-model claude-opus-4-8 --sdk-nl-judge \
    --agent-extra-instruction-file claudedocs/i1_fixes/fix4_pointed.txt \
    --save-to i1_g3i3_$t --auto-resume --log-level INFO \
    > data/simulations/i1_g3i3_${t}_stdout.log 2>&1 &
  sleep 3
done
```

## 2. Evaluation pipeline (post-hoc, on `results.json`)

The strict score is produced inside the driver run above. The **verified scorer**,
DB-diff, and best-of-N analysis are now permanent scripts under
[`scripts/i1_eval/`](../scripts/i1_eval/) (see its README). Run from the repo root:

```bash
# Verified score one task against its results.json
uv run python scripts/i1_eval/verified_score.py task_064 data/simulations/i1_fix5/results.json

# Verified-score summary table (built-in best-known I1 layout: 047/058/063/064/067)
uv run python scripts/i1_eval/verified_score.py

# Per-iteration verified-score (all 5 tasks, one results dir per task)
for t in task_047 task_058 task_063 task_064 task_067; do
  uv run python scripts/i1_eval/verified_score.py $t data/simulations/i1_g3i2_$t/results.json | tail -1
done

# DB diff (predicted vs gold final DB) for a task
uv run python scripts/i1_eval/diff_task.py task_063 data/simulations/i1_fix5/results.json

# Best-of-N across trials (default: iteration-3 i1_g3i3_{task} layout)
uv run python scripts/i1_eval/bestof.py
uv run python scripts/i1_eval/bestof.py "data/simulations/i1_g3i2_{task}/results.json"
```

> These were reconstructed from the original session scratchpad (which is ephemeral
> under `/private/tmp/.../scratchpad/`) into permanent, verified-working scripts.

**Verified-scorer logic:** the discoverable-tool audit is compared as a *superset*
(gold's required calls must be present; extra reads are forgiven), and free-text
fields like `closure_reason` are excluded from the DB comparison. A *missing required*
call still fails (e.g. task_047). Everything else (accounts, applications, ...) is
compared exactly.

## Flag reference

| Flag | Meaning |
|------|---------|
| `--domain banking_knowledge` | Task domain |
| `--task-ids …` | Space-separated I1 task IDs |
| `--num-trials 1\|2\|4` | Trials per task |
| `--agent-model claude-opus-4-8` | Agent (driver) model |
| `--sdk-nl-judge` | Use the SDK NL judge in the internal evaluation step |
| `--agent-extra-instruction-file …` | Append a policy/fix snippet to the agent system prompt |
| `--save-to NAME` | Output dir → `data/simulations/NAME/results.json` |
| `--auto-resume` | Resume partial runs |
| `--log-level INFO` | Log verbosity |

User-sim and judge models are **not** CLI flags — they default inside the driver
(opus-4-8 / high). Verified scoring is applied post-hoc, not via a flag.

## Notes

- Run parallel (one process per task) rather than one process with many `--task-ids`
  when you hit rate limits — observed ~8.5 min parallel vs ~28 min sequential for 5 tasks.
- Output of each run: `data/simulations/<save-to>/results.json` plus a
  `*_stdout.log` next to it.
