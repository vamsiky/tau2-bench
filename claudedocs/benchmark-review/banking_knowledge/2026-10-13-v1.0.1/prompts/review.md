# Prompt — Benchmark Correctness Review (per task)

<!--
How to run: see ../README.md. Recommended configuration: claude-opus-5-5 at effort
`high` (set it with /effort or the agent's settings, not in this text). Each reviewer
receives this prompt plus a run brief naming {domain}, {benchmark_version},
{snapshot_root}, {run_dir}, the task ids to review, and (optionally) {prior_findings}.
-->

<role>
You are auditing a tool-use agent benchmark: tau2-bench, domain `{domain}`, benchmark
version `{benchmark_version}`. Each task tests whether an AI customer-service agent,
given only a customer conversation, a knowledge base, and the domain tools, can take
the correct actions. You are not solving the tasks. You are judging whether each task
is well-posed, self-consistent, and deterministically solvable from what the agent is
actually given, because a task that a competent agent cannot reliably reproduce turns
into noise in every model's score.
</role>

<sources>
Read everything from the read-only snapshot at `{snapshot_root}`, which is the exact
benchmark version under review. Do not read the working repository's copies: that
branch carries local modifications to tools and evaluators that are not part of the
benchmark.

- Tasks: `data/tau2/domains/{domain}/tasks/<task_id>.json` (this directory is what the
  task loader reads). Each task has `user_scenario.instructions` (what the simulated
  customer knows and wants), `required_documents` (knowledge-base doc ids),
  `evaluation_criteria.actions` (the gold tool calls, in order, each with a
  `requestor`), `evaluation_criteria.reward_basis`, `initial_state`, and
  `description.notes` (author notes; the agent never sees these).
- Knowledge base: `data/tau2/domains/{domain}/documents/<doc_id>.json` (`content` is
  the text the agent can retrieve).
- Seed database: `data/tau2/domains/{domain}/db.json`.
- Tools and grading: `src/tau2/domains/{domain}/tools.py`, `environment.py`,
  `utils.py`; `src/tau2/evaluator/evaluator_env.py`;
  `src/tau2/runner/build.py` (`_derive_read_log_allowlist`);
  `Action.compare_with_tool_call` in `src/tau2/data_model/tasks.py`.
</sources>

<grading_model>
These facts decide what counts as a defect. Confirm each against the snapshot once at
the start and record anything that differs in your `notes`; if one is wrong, findings
that depend on it change. They describe the benchmark's own grading. When the run brief
names a scorer variant file (`{scorer_variant}`), read it: it states which comparisons
that run relaxes, and those statements replace the bullets below that they contradict.
Judge validity under the scorer the run brief names, since the same task can be sound
under one scorer and broken under another.

- DB grading replays the gold actions on a fresh environment and requires the agent's
  final agent-side and user-side DB hashes to match exactly. Every value a gold write
  persists (ids, amounts, dates, enums, free-text fields such as reasons) must therefore
  be uniquely derivable by a competent agent, or the task mis-grades correct work.
- Discoverable read calls are logged to the DB only when the task's gold trajectory
  makes that read (`_derive_read_log_allowlist`), so extra prudent reads do not change
  the hash, while a gold-required read the agent skips does.
- Arguments passed through `call_discoverable_agent_tool` / `call_discoverable_user_tool`
  are parsed with integers as floats, and some tools cast their own numbers, so `25`
  versus `25.0` does not change the hash on those paths. Check the specific tool before
  assuming the same for any other write.
- ACTION grading checks that the agent made at least one call matching each gold action
  on that action's `compare_args` (every argument the agent passed when `compare_args`
  is unset); it ignores order, repetition, and extra calls. For
  `call_discoverable_agent_tool` the inner `arguments` value is a JSON string, so when it
  is compared, spelling, key order, and whitespace all count.
- The agent-side and user-side toolkits share one database in this domain, and writes
  are logged even when the tool returns an error string, so a user-tool call or a failed
  write the gold does not make still changes the hash.
- The clock is fixed (`get_now()` in `utils.py`); timestamps derived from it are
  deterministic and are not a defect on their own.
- Some read tools are always available to the agent; others are discoverable and must
  be unlocked, which only works when the knowledge base documents them. Check which
  kind each gold read is before calling information unobtainable.
</grading_model>

<what_makes_a_task_valid>
A task is valid when a competent agent, using only the customer's instructions, the
documents it can retrieve, and the tool outputs it can obtain, would arrive at a final
state (and, for ACTION grading, a set of calls) identical to the gold's. Judge it the
way a careful domain expert who had never seen the gold would: reconstruct the solution
from the materials first, then compare with the gold. Do not use outside domain
knowledge to rescue a task, and do not penalize a task for requiring reasoning that the
documents support but that is hard.

The defect classes below are the ones that matter. Name the class for each issue you
report.

- `instruction_gold_mismatch`: the customer's goal or constraints do not entail the gold
  actions.
- `underspecified_instructions`: the gold needs information the customer never gives
  and the agent cannot obtain from tools or documents.
- `document_gap`: a rule, threshold, rate, or attribute needed to choose a gold action
  or argument is not in the documents the agent can retrieve.
- `document_contradiction`: documents disagree, or carry corrupted values (for example
  a credit score written as a dollar amount), so the correct answer is ambiguous.
- `non_determinism`: more than one action set is defensible under the materials, but
  the gold treats one as uniquely correct (ties, "best" with no tie-breaker, ordering
  the tools do not expose).
- `hidden_ordering`: the correct solution depends on a sequencing or prerequisite rule
  the agent cannot reasonably deduce from the documents.
- `argument_error`: a gold argument is wrong, mistyped, or inconsistent with the
  instructions, documents, or seed DB.
- `grading_basis_mismatch`: `reward_basis` does not fit the task (DB grading of an
  outcome the DB does not record; ACTION grading where the gold call is not unique).
- `answer_leak`: the agent-visible data gives away the answer in a way that defeats the
  task's purpose (for example, fee descriptions annotated "SHOULD BE FREE").

Severity is about benchmark validity, not effort:
`Blocker` — a competent agent cannot reliably reach the gold, so correct work fails or
the result is chance. `Major` — the gold is reachable but only through an undocumented
convention or a reading a reasonable agent could miss, so scores are noticeably
distorted. `Minor` — a real defect that does not change the correct final state (a typo,
a cosmetic corruption, an inconsistency the agent can resolve). `None` — clean.
Apply the same severity to the same defect class across tasks unless a stated reason
differs, so the report can be compared task to task.
</what_makes_a_task_valid>

<evidence>
Every issue cites primary-source evidence a reader can check: a doc id with a short
verbatim quote, a DB field path with its value, a gold action index with the argument,
or a code symbol. Quote, do not paraphrase, when a value is load-bearing. When you
compute something (rewards, fees, tenures), state the inputs and the result so the
computation can be re-run. If you could not verify a point, say so in the issue rather
than asserting it.
</evidence>

<prior_findings>
When `{prior_findings}` is given, it holds the previous review's verdict for each task
and a summary of what changed in the data and code since that review. Treat it as a
lead to check, not as a conclusion: re-derive the issue against the current snapshot and
set `prior_status` to `resolved` (the defect is gone), `persists`, `changed` (still
defective but different), `new` (a defect the prior review did not report), or
`not_applicable` (no prior finding and none now). The prior review used a modified
scorer that relaxed some comparisons, so a prior downgrade that relied on that scorer
needs re-checking under the grading model above.
</prior_findings>

<output>
Write one JSON file per task to `{run_dir}/findings/<task_id>.json` with exactly these
fields (the report renderer reads them; it copies the task text, documents, and gold
actions from the snapshot itself, so do not repeat them):

```json
{
  "task_id": "task_001",
  "severity": "None | Minor | Major | Blocker",
  "headline": "one plain-English sentence a non-specialist can read",
  "ratings": {
    "instructions_sufficient": "Sufficient | Partial | Insufficient",
    "docs_deterministic": "Yes | Partial | No",
    "reasoning_complexity": 1,
    "ordering_dependency": "None | Soft | Strict",
    "gold_consistent": "Yes | No"
  },
  "issues": [
    {
      "class": "document_gap",
      "severity": "Major",
      "summary": "what is wrong, in one or two sentences",
      "evidence": ["doc_x: \"verbatim quote\"", "db.json accounts[acc_1].balance = 120.5", "gold[3].arguments.amount = 27.0"],
      "gold_action_refs": [3],
      "why_it_matters": "how a competent agent ends up with a different final state",
      "suggested_fix": "the smallest concrete change that makes the task deterministic"
    }
  ],
  "solution_check": "two to four sentences: how you reconstructed the solution and whether it matched the gold",
  "prior_status": "resolved | persists | changed | new | not_applicable",
  "prior_note": "one sentence relating this verdict to the prior one, when there was a prior finding",
  "notes": "anything a verifier should know, including facts you could not confirm"
}
```

`reasoning_complexity` runs from 1 (direct lookup) to 5 (deep multi-constraint
reasoning). The task-level `severity` is the worst issue severity, or `None` when
`issues` is empty. Keep `issues` to real defects; observations that do not affect
validity go in `notes`.
</output>
