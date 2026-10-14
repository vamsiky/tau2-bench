# POLICY_REASONING 52-task run with A1–A4 fixes — results

**Date:** 2026-06-27
**Driver:** `examples/agents/claude_sdk_loop_eval.py`
**Agent:** `claude-sonnet-4-6` · **User-sim & NL-judge:** `claude-opus-4-8/high` (SDK, subscription)
**Trials:** 1 · **Retrieval:** `alltools` · **Verified scorer:** on
**Fixes applied:** A3 closure-eligibility guard (compiled into `tools.py`) + A1/A2/A4 policy text
(`claudedocs/a1a4_fixes/policy_a1a4.txt`, passed via `--agent-extra-instruction-file`)
**Run dirs:** `data/simulations/policyfix_b1..b5/`

## TL;DR

- **14 / 52 (27%) passed** with the fixes applied.
- This is a **with-fix snapshot, not a lift measurement** — no matched sonnet no-fix baseline was run on
  the identical 52 tasks, so the 14 passes cannot be attributed to the fixes vs. sonnet capability/stochasticity.
- The number is **consistent with the deterministic validation** (`policy_reasoning_deterministic_validation.md`):
  this 52-task set is dominated by **product-selection (P2) failures** that the A1–A4 path was explicitly
  concluded *not* to address. The fixes target a tiny slice of this set.
- On the targeted tasks for which a prior baseline exists (045, 053, 063, 064, 092): **zero new passes,
  zero regressions** — the fixes behave exactly as predicted.

## Headline breakdown

| Slice | Tasks | Passed | Rate |
|---|---:|---:|---:|
| **All POLICY_REASONING** | 52 | 14 | 27% |
| Involve P2 product-selection | 40 | 11 | 28% |
| Non-P2 | 12 | 3 | 25% |

The pass rate is essentially flat across the P2 / non-P2 split — i.e. the outcome tracks general task
difficulty, **not** the presence of an A1–A4-addressable failure mode.

## What A1–A4 actually targets in this set

The A1–A4 deterministic path reaches only a small subset of these 52 tasks. Each behaved as the validation
predicted:

| Fix | Targeted tasks present | Result | Matches validation? |
|---|---|---|---|
| **A3** closure-eligibility guard (forces `get_user_dispute_history_7291` + `get_pending_replacement_orders_5765` before retention writes) | 053 | 0.0 — blocked by orthogonal `user_discoverable_tool_calls` issue (out of A1–A4 scope) | ✅ predicted to stay failing |
| **A4** PIN routing (fraud-alert→close, security-hold→transfer) | 092 | 0.0 — Green card's close-vs-reset signal is *computed* from transaction velocity, not stored | ✅ predicted deterministically unfixable |
| **A1/A2** policy (write-tool authorization / apply-referral handoff / transfer-reason) | 008, 039, 040, 065, 071, 074, 084, 087, 101 | 1/9 (only 008) | ✅ A1/A2 barely reproduce on sonnet |

The remaining ~40 tasks are P2 product-selection and/or P1 financial-computation failures — the categories
the deterministic validation marked **structurally unreachable** by code guards (they require correct LLM
reasoning, not a deterministic gate).

## Why 14/52 is not attributable to the fixes

The 14 passes are overwhelmingly P2-tagged tasks that sonnet + the opus judge got right on their own
(002, 023, 044, 055, 062, 063, 064, 067, 075, 094, 095 all carry P2). Product selection is exactly what
A1–A4 does **not** touch, so these passes reflect model capability, not the deterministic fixes.

For the 5 targeted tasks with a prior sonnet baseline (from `policy_reasoning_a1a4_validation.md`):

| Task | Baseline | With-fix (this run) | Net |
|---|---|---|---|
| 045 | 1.0 (already passing) | 1.0 | no change |
| 063 | stochastic 0/1 | 1.0 | within noise |
| 064 | 1.0 (already passing) | 1.0 | no change |
| 053 | 0.0 | 0.0 | no change (orthogonal blocker) |
| 092 | 0.0 | 0.0 | no change (computed signal) |

→ **0 new passes, 0 regressions** on the targeted tasks. The fixes neither help nor hurt the broad P2 set.

## Full per-task table

`fix anchors` = the opus-4.7 failure fix-anchors from `opus47_banking_failure_evidence_table.md`
(P1 computation · P2 product-selection · P3 dispute-tree · P4 eligibility-caps · P5 ordered-procedures ·
A1/A2 arg-mechanical · O over-action · I incomplete · G grader · V verification · U user-sim).

| Task | Batch | Reward | P2? | opus-4.7 fix anchors |
|---|---|---|---|---|
| task_001 | B1 | 0.0 | P2 | P2 |
| task_002 | B1 | ✅ 1.0 | P2 | P2 |
| task_003 | B1 | 0.0 | P2 | P2 |
| task_004 | B1 | 0.0 | P2 | P2,P3 |
| task_005 | B1 | 0.0 | — | G1,G2,P3 |
| task_008 | B1 | ✅ 1.0 | — | A1,P3 |
| task_010 | B1 | 0.0 | P2 | I2,P2 |
| task_018 | B1 | 0.0 | P2 | P2 |
| task_020 | B1 | 0.0 | P2 | O1,P2 |
| task_022 | B1 | 0.0 | P2 | I3,O1,P2 |
| task_023 | B1 | ✅ 1.0 | P2 | I1,P2 |
| task_039 | B2 | 0.0 | — | A1,P4,P5 |
| task_040 | B2 | 0.0 | P2 | A1,P2,P4,P5 |
| task_041 | B2 | 0.0 | P2 | P1,P2,P4,P5 |
| task_044 | B2 | ✅ 1.0 | P2 | I1,P2,P5 |
| task_045 | B2 | ✅ 1.0 | — | G1,G2,P1,P4 |
| task_048 | B2 | ✅ 1.0 | — | O2 |
| task_049 | B2 | 0.0 | — | O1,O2,P1,P4 |
| task_053 | B2 | 0.0 | — | I1,I2 |
| task_054 | B2 | 0.0 | — | P1,P3,P4,P5 |
| task_055 | B2 | ✅ 1.0 | P2 | P1,P2,U1 |
| task_056 | B2 | 0.0 | P2 | P1,P2 |
| task_057 | B3 | 0.0 | P2 | P1,P2,V1 |
| task_062 | B3 | ✅ 1.0 | P2 | G1,G2,O1,P2,P5 |
| task_063 | B3 | ✅ 1.0 | P2 | I1,P2 |
| task_064 | B3 | ✅ 1.0 | P2 | I1,P2 |
| task_065 | B3 | 0.0 | P2 | A2,P1,P2 |
| task_066 | B3 | 0.0 | P2 | P1,P2,P5 |
| task_067 | B3 | ✅ 1.0 | P2 | I1,P2,P5 |
| task_068 | B3 | 0.0 | P2 | I1,P2 |
| task_069 | B3 | 0.0 | P2 | P2,P5 |
| task_071 | B3 | 0.0 | P2 | A2,O1,P2 |
| task_072 | B4 | 0.0 | P2 | P1,P2 |
| task_073 | B4 | 0.0 | P2 | P1,P2 |
| task_074 | B4 | 0.0 | P2 | A1,P1,P2 |
| task_075 | B4 | ✅ 1.0 | P2 | P1,P2 |
| task_077 | B4 | 0.0 | P2 | G1,G2,O1,P2,P5 |
| task_080 | B4 | 0.0 | — | O1,P4,P5 |
| task_081 | B4 | 0.0 | — | P4,P5 |
| task_082 | B4 | 0.0 | P2 | O1,P2,P4,P5 |
| task_084 | B4 | 0.0 | — | A1,O1,P3,P5 |
| task_086 | B4 | 0.0 | — | I2,P1,P3,P5 |
| task_087 | B5 | 0.0 | P2 | A1,G1,G2,P2,P3,P5 |
| task_090 | B5 | 0.0 | P2 | P2,P5 |
| task_091 | B5 | 0.0 | P2 | P2,P5 |
| task_092 | B5 | 0.0 | P2 | P2,P5 |
| task_094 | B5 | ✅ 1.0 | P2 | G1,G2,P1,P2 |
| task_095 | B5 | ✅ 1.0 | P2 | P1,P2 |
| task_097 | B5 | 0.0 | P2 | P1,P2 |
| task_099 | B5 | 0.0 | P2 | G1,G2,I1,P2,V1 |
| task_101 | B5 | 0.0 | P2 | A2,O1,P2 |
| task_102 | B5 | 0.0 | P2 | G2,I2,P2,P4 |

## Limitations

- **No matched baseline.** Lift cannot be claimed without a sonnet no-fix run on the same 52 tasks. Only the
  5 tasks above have a prior baseline.
- **Single trial per task.** DB-reward is stochastic across single trials (established earlier: 047/063
  baselines flipped 0→1). A 27% point estimate from n=1 trials carries wide per-task variance.
- **Task set ≠ A1–A4 scope.** This set was selected as the opus-4.7 POLICY_REASONING failures, not as the
  A1–A4-addressable subset. It is dominated (40/52) by product-selection, which the fixes do not target.

## Reproduce

```bash
# one batch (repeat with the other task-id groups, --save-to policyfix_b2..b5)
uv run python examples/agents/claude_sdk_loop_eval.py \
  --domain banking_knowledge \
  --task-ids task_001 task_002 task_003 task_004 task_005 task_008 task_010 task_018 task_020 task_022 task_023 \
  --agent-model claude-sonnet-4-6 --num-trials 1 --sdk-nl-judge \
  --agent-extra-instruction-file claudedocs/a1a4_fixes/policy_a1a4.txt \
  --save-to policyfix_b1 --auto-resume
```
