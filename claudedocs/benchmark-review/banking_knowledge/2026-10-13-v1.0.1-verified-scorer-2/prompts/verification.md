# Prompt — Independent Verification of a Benchmark Correctness Review

<!--
How to run: see ../README.md. Run in a fresh session (or with a different model) from the
one that produced the review, so the check is independent. Recommended configuration:
claude-opus-5-5 at effort `high` (set via /effort or agent settings, not in this text).
The run brief names {domain}, {benchmark_version}, {snapshot_root}, {run_dir}, and the
task ids assigned to this verifier.
-->

<role>
You are an independent verifier. A review of the tau2-bench `{domain}` benchmark at
version `{benchmark_version}` wrote one findings file per task to
`{run_dir}/findings/<task_id>.json`, following `prompts/review.md`. Your job is to audit
that review: confirm findings you can reproduce, overturn ones you cannot, and catch
errors in both directions, because a false Blocker removes a good task from the
benchmark and a missed Blocker leaves noise in every score.
</role>

<sources>
Work only from primary sources in the read-only snapshot at `{snapshot_root}` (tasks,
documents, `db.json`, tools, evaluators, as listed in `prompts/review.md`). The findings
files are claims to test, not evidence. The prior review's verdicts are in
`{run_dir}/inputs/prior_findings.json`; use them to understand why a severity moved, not
as support for either side.
</sources>

<scope>
Your run brief assigns task ids. For each one, reproduce the review's load-bearing
claims independently: re-read the quoted documents, re-query the DB values, re-run any
computation (rewards, fees, tenures, tie comparisons) yourself, and check that each cited
quote, field path, and gold action index exists and says what the review says. For a
task the review rated `None` or `Minor`, apply the review prompt's full procedure to it
yourself, since unflagged tasks get the least scrutiny and that is where missed defects
hide.

Also confirm the grading-model facts in `prompts/review.md` once against the snapshot;
if one is wrong, list the findings that depend on it.
</scope>

<verdicts>
For each assigned task, give one verdict:
`Confirmed` — the severity and the substance of every issue hold.
`Adjusted` — a real defect, but the severity or the reasoning needs correcting.
`Overturned` — the claimed defect is not real (say what the review got wrong).
`Upgraded` — the review missed a defect or under-rated one.
`Unverifiable` — you could not reproduce the evidence either way (say what blocked you).

Hold severities to the definitions in `prompts/review.md`, and flag cases where the same
defect class received different severities in different tasks without a stated reason.
A fabricated or misquoted citation is a finding in its own right; record it even when the
verdict otherwise stands.
</verdicts>

<output>
Write `{run_dir}/verification/<verifier_id>.json`:

```json
{
  "verifier_id": "v1",
  "fact_checks": [
    {"fact": "DB grading is exact-hash after gold replay", "status": "Confirmed | Wrong", "evidence": "file:symbol or quote"}
  ],
  "task_verdicts": {
    "task_074": {
      "verdict": "Confirmed | Adjusted | Overturned | Upgraded | Unverifiable",
      "review_severity": "Blocker",
      "verified_severity": "Blocker",
      "evidence": ["doc id + verbatim quote, DB path = value, gold[i].arguments.x = y"],
      "citation_problems": ["any quote, path, or value in the findings file that does not match the source"],
      "note": "two to four sentences: what you reproduced, and what you changed and why"
    }
  },
  "calibration_notes": ["same-class severity inconsistencies across tasks, with task ids"],
  "methodology_note": "one paragraph on whether the review's grading model and reasoning are sound, and any blind spot in its method"
}
```

Spend your effort where the review is wrong, unproven, or miscalibrated; where it is
right, a short confirming note with the evidence you checked is enough.
</output>
