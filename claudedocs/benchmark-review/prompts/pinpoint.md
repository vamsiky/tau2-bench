# Pinpoint files: where exactly each task goes wrong

Run brief fills in `{run_dir}`, `{snapshot_root}`, and a batch of task ids with their final severities.

The benchmark review explains each verdict in long prose.
Readers can't quickly see *which step*, *which value*, and *which document sentence* make a
task Blocker/Major/Minor. You restate the decisive reasons for your tasks as short, exact,
replay-backed evidence. You do **not** re-judge severities: the final severity is fixed.

## Inputs (read-only)

- Run dir: `{run_dir}`
  - `findings/<task>.json`: reviewer findings (issues, evidence, gold_action_refs)
  - `verification/v1..v4.json` → `task_verdicts[<task>]`: verifier verdict, severity, note, evidence
- Benchmark snapshot (v1.0.1): `{snapshot_root}` (export it as `BENCH_DIR`)
  - tasks: `{snapshot_root}/data/tau2/domains/banking_knowledge/tasks/<task>.json`
  - docs: `{snapshot_root}/data/tau2/domains/banking_knowledge/documents/<doc_id>.json` (field `content`)
  - tools: `{snapshot_root}/src/tau2/domains/banking_knowledge/tools.py`
- Tools (`claudedocs/benchmark-review/replay.py`, run with `BENCH_DIR={snapshot_root} uv run python`):
  - `replay.py gold <task>`: every gold step with its exact output (`PP_LIMIT=4000` for longer outputs)
  - `echo '<EDITS>' | replay.py alt <task> -`: replays gold with your edits, prints the changed steps' outputs, the DB fields that differ, the upstream/verified DB verdicts, and the action check. The edit format is in the docstring of `replay.py`.
  - `replay.py check {run_dir} <task> ...`: validates your files (schema, step ranges, verbatim quotes, action verdict on ACTION-graded tasks). Every file must pass.

## Output: `<run_dir>/pinpoint/<task>.json`

```json
{
  "task_id": "task_026",
  "severity": "Blocker",
  "reason": "Gold writes 1500 points where the documented floor rule gives 1499, and the agent cannot see dispute status.",
  "points": [
    {
      "issue": 1,
      "severity": "Blocker",
      "title": "Gold rounds 1499.9 up; docs say floor",
      "kind": "gold_value_wrong",
      "step": 10,
      "gold": {"call": "update_transaction_rewards_3847",
               "args": {"transaction_id": "txn_a8f1c2d3e411", "new_rewards_earned": "1500 points"},
               "output": "Transaction updated: ... New Rewards: 1500 points"},
      "doc_faithful": {"call": "update_transaction_rewards_3847",
                       "args": {"transaction_id": "txn_a8f1c2d3e411", "new_rewards_earned": "1499 points"},
                       "output": "Transaction updated: ... New Rewards: 1499 points",
                       "note": ""},
      "refs": [
        {"source": "doc_credit_cards_credit_cards_(general)_007",
         "quote": "All credit card rewards points are rounded down to the nearest whole number."}
      ],
      "conflict": "Zoom $149.99 × 10% = 1499.9. Doc _007 floors → 1499; gold writes 1500.",
      "scorer": {"field": "credit_card_transaction_history[txn_a8f1c2d3e411].rewards_earned: gold \"1500 points\" vs agent \"1499 points\"",
                 "upstream": "FAIL", "verified": "FAIL"}
    }
  ]
}
```

Field rules:

- `severity`: the final severity given to you in the task list. Never change it.
- `reason`: one sentence, ≤ 25 words, naming the single decisive defect in concrete terms (values, step, doc). Plain words, no jargon like "doc-faithful".
- `points`: one per issue that carries the final severity, plus any other Blocker/Major issue; most severe first; at most 4. For a Minor task usually one point. `issue` is the 1-based index into `findings.issues`. If the verifier upgraded/adjusted the task, the point(s) must reflect the verifier's reasoning (use its note and evidence) and `severity` on the point is the severity that issue now carries.
- `title`: ≤ 10 words.
- `kind`: one of
  - `gold_value_wrong`: gold passes a value the docs contradict
  - `gold_call_missing`: docs require a call the gold does not make (or gold omits a step)
  - `gold_call_extra`: gold makes a call the docs forbid or never ask for
  - `ambiguous_choice`: docs allow two or more answers; gold accepts only one
  - `info_unavailable`: the agent cannot see something it needs (no tool, hidden status, missing doc)
  - `instruction_conflict`: customer instructions push against the gold or the docs
  - `nl_grading`: the defect is in communicate_info / nl_assertions, not DB state
  - `other`
- `step`: 0-based gold step index where the divergence happens (as numbered by `replay.py gold`). For a missing call, the gold step it should come before/after (say which in `conflict`); `null` only if no gold step applies (e.g., the whole gold is empty, or an NL assertion).
- `gold`: the gold step at `step`: tool name (for `call_discoverable_agent_tool` use the inner tool name), its args (inner args for discoverable calls), and the **exact** output from `replay.py gold`, trimmed to the lines that matter (keep exact text; use "..." for omitted parts). `null` if the gold has no such step (e.g., gold_call_missing).
- `doc_faithful`: what an agent that follows the docs / instructions does instead at that point (for a Minor issue where the gold is correct but easy to miss, e.g. a missing required document, it is the plausible wrong path; then start `note` with "Plausible misreading:"): same shape as `gold`, output taken from `replay.py alt`. If it skips the call, set `call` to the skipped tool, `args` to `{}`, `output` to `""` and say so in `note`. If the agent's choice is a refusal or a message rather than a tool call, set `call` to `"(no call)"` and describe the message in `note`. `null` only if the issue has no alternative action (e.g., a pure NL-grading defect).
- `refs`: the exact text that differs from the gold. **Quote verbatim** (`replay.py check` verifies document quotes and instruction quotes as exact substrings, so copy-paste; keep each quote to the 1–2 sentences that matter). `source` is a doc id, or `"instructions"` (the customer's instructions text), or `"tool:<function name>"` / `"db:<table>[<id>]"` / `"task:<field>"` for code, data, or task-definition evidence (not substring-checked but must be exact). Include the doc sentence the gold contradicts whenever one exists; that is the most important ref. If the issue is that no doc says something, quote the closest doc sentence and say "no doc states X" in `conflict`.
- `conflict`: ≤ 30 words: precisely where gold and doc/instructions differ, with the numbers. E.g. "Doc _007: floor → 1499. Gold step 10: 1500."
- `scorer`: from an actual `replay.py alt` run of the `doc_faithful` alternative: `field` = the first 1–3 differing DB fields as printed (or the verified-scorer reason if no field differs, e.g. "missing required discoverable call X"); `upstream`/`verified` = `PASS`/`FAIL`. Use `"n/a"` for both only when the alternative can't be replayed (NL grading, refusal-only paths where the outcome is simply the absence of gold writes — but in that case do replay with those gold steps dropped). Never write verdicts you did not get from `replay.py`.
- `scorer.action` (**required when the task's reward_basis includes ACTION**; 9 tasks are graded only on ACTION): copy the `== action check:` line's PASS/FAIL from `replay.py alt`, and for ACTION-graded tasks put the unmatched gold action (e.g. `missing gold action #0 transfer_to_human_agents(reason=...)`) in `field`. For DB-graded tasks omit it or use `"n/a"`. The task's real verdict is the one on its reward_basis: for an ACTION-only task, DB PASS + action FAIL means the task fails.

If your replay contradicts the reviewer or verifier (e.g., the doc-faithful alternative actually PASSES), keep the final severity, record what the replay shows, and add a top-level `"discrepancy": "<one sentence>"` to the file. Do not hide it.

Keep everything short. The long write-ups stay in findings/verification; your file is the at-a-glance evidence.

Work task by task: read findings + verdict, run `replay.py gold`, find the divergent step, open the doc and copy the exact sentence, build and run the edit with `replay.py alt`, write the file, run `replay.py check`. Do not edit anything outside `<run_dir>/pinpoint/`. Put scratch files in your own scratch folder.

When done, reply with: the tasks written, any `discrepancy` entries (task + one line), and any task where you could not produce a replay (and why).
