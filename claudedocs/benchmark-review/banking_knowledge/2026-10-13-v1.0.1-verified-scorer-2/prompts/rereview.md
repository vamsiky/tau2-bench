# Re-review: customer-side behaviour and simulator assumptions

The banking_knowledge v1.0.1 verified-scorer review over-rated task_049. It called a gold
customer call "unscripted", cited the simulator guideline against it, counted a failure that only
happens when the agent errs, and leaned on a comparison with other tasks that was not like for like.
Re-check your tasks for the same mistakes and correct the record. The report must show only the
latest findings: write each file as if it were the first review, never "was X, now Y", and never
mention the earlier verdict or any other run.

## Paths

- Run dir `$RUN=<domain dir>/2026-10-13-v1.0.1-verified-scorer-2`
  - `findings/<task>.json`: reviewer findings (severity, headline, issues[], solution_check, notes)
  - `verification/v1..v4.json` → `task_verdicts[<task>]`: verifier verdict (verdict, review_severity, verified_severity, evidence[], citation_problems[], note)
  - `pinpoint/<task>.json`: at-a-glance evidence; schema in `$RUN/prompts/pinpoint.md`
  - Severity definitions: `$RUN/prompts/review.md`, `$RUN/prompts/calibration.md`
- Benchmark snapshot `$SNAP=<benchmark snapshot at v1.0.1>`
  - tasks `$SNAP/data/tau2/domains/banking_knowledge/tasks/<task>.json` (note the `user_tools` field)
  - docs `$SNAP/data/tau2/domains/banking_knowledge/documents/`
  - tools `$SNAP/src/tau2/domains/banking_knowledge/tools.py`
  - simulator guidelines `$SNAP/data/tau2/user_simulator/simulation_guidelines_tools.md`
- Python `$PY=python`; tools in `$PP=<tools dir: replay.py>`:
  `replay.py gold <task>`, `replay.py alt <task> -`, `replay.py check $RUN <task>...` (with `BENCH_DIR` set to the snapshot)

## Principles (established with the user; apply them, do not re-argue them)

1. **Customer tools are per task.** The simulator gets only the tools in the task's `user_tools`
   (`src/tau2/data_model/tasks.py:614`, `src/tau2/runner/build.py:160`). Check that list before
   saying the customer can or cannot call something. Every gold customer call is in its task's list.
2. **A gold customer call need not be named in the script.** If the script gives the customer a
   goal or line that the tool's docstring matches ("Transfer me to a human agent" ↔
   `request_human_agent_transfer`; "I want to apply for X" ↔ `apply_for_credit_card`), making the call
   is the expected behaviour. 47 gold customer calls in this benchmark are not named in their
   scripts. That other tasks name a tool is not evidence that this one must.
3. **The simulator guideline "Only call a tool if the agent has requested it…" is about actions the
   agent asks for.** It does not count against a customer call that carries out the customer's own
   scripted goal, and "Strictly follow the scenario instructions" ranks above it. Do not cite it as
   making such a call unlikely.
4. **Failures that only occur when the agent errs are not defects.** E.g. a second customer request
   because the agent did not act on the first; an extra write the docs do not call for.
5. **"No KB document mentions <customer tool>" is not evidence** for regular customer tools: the KB
   is for the agent. It matters only when the agent must hand over and ask for a *discoverable*
   customer tool (`give_discoverable_user_tool`) and no document names it.
6. **Customer tool output reaches the agent only through what the customer says next**, but a
   script-following simulator reports a result the agent asks about (guidelines: "ground your
   responses based on the results of tool calls"). Do not call something unobservable if the agent
   can ask the customer and the customer would answer from a tool result or the script. It is still
   unobservable if the customer has no grounded answer (not in the script, no tool returns it).
7. **Cross-task comparisons count only when like for like:** the same conversational role (an
   opening line vs a demand that is pressed and acted on), the same tool availability, the same
   grading.
8. **Severity.** If a pass depends only on the simulator doing what its script and tools naturally
   imply, the gold is correct and the issue is at most Minor (a reliability risk). Blocker/Major
   still need what the definitions in `prompts/review.md` and `prompts/calibration.md` say: the gold
   is wrong, unreachable for a competent agent working with a script-following simulator, or
   genuinely ambiguous.

Only change what these principles touch. Leave issues that rest on document readings, values,
data, or agent-side tools as they are. If an issue relies partly on a bad premise but stands on its
other evidence, keep its severity and remove the bad premise from the text.

## For each task

1. Read the findings, verifier verdict, and pinpoint. Find every argument that touches the customer's
   side: customer tool calls, what the simulator will or won't do or say, the guideline, "never
   told / unscripted", double calls, cross-task contrasts, customer-only information.
2. Check each against the principles, using the task file (`user_tools`, script), tool docstrings,
   and replays (`replay.py`). Replays decide what passes or fails; never write a verdict you did not run.
3. Decide the latest severity for each issue and for the task (task = most severe issue).
4. If anything changes (a severity, or the text of an argument), edit in place:
   - `findings/<task>.json`: `severity`, `headline`, and each affected issue's `severity`,
     `summary`, `evidence`, `why_it_matters`, `suggested_fix`; `solution_check`/`notes` if they repeat
     the bad premise. Leave `prior_status`, `prior_note`, `ratings` unless a rating is now plainly
     wrong. Keep the same issue order (pinpoint `issue` indexes into it).
   - `pinpoint/<task>.json` per `prompts/pinpoint.md` (severity = latest task severity; `reason` ≤ 25
     words; points as specified; a Minor point where the gold is correct uses
     `doc_faithful.note` starting "Plausible misreading:"). Must pass `replay.py check`.
   - Do **not** edit `verification/*.json`. Instead put the replacement verifier entry in your
     output file (below); it will be merged as the latest verdict.
5. Write `<re-review output dir>/<task>.json`
   for **every** task:
   ```json
   {"task_id": "task_0XX", "severity": "<latest task severity>", "edited": true,
    "principles": [2, 3], "summary": "<one line: what you checked and concluded>",
    "verdict": {"verdict": "Confirmed" | "Adjusted", "review_severity": "<findings severity after your edit>",
                "verified_severity": "<latest>", "evidence": ["<short, exact>", ...],
                "citation_problems": [], "note": "<≤ 70 words, latest reasoning only>"}}
   ```
   `verdict` only when `edited` is true. Use "Confirmed" when the severity stands with corrected
   reasoning, "Adjusted" when the severity changed. With `edited: false`, list the principles you
   checked and why nothing changed in `summary`.

Do not edit anything else. Put scratch files in `$PP/work_rr_<batch>/`. Finish by running
`replay.py check` on all your tasks and reply with one line per task: id, latest severity, edited yes/no,
and the reason in ≤ 15 words.
