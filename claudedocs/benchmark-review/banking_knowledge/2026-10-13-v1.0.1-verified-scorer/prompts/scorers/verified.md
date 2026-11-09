# Scorer variant — verified DB comparison

This run grades DB-based tasks with the relaxed "verified" DB comparison implemented on
this branch (`_verified_db_match` and `use_verified_scorer` in
`src/tau2/evaluator/evaluator_env.py` of the working repository, not the snapshot). Read
that code once to confirm the points below. Task data, documents, tools, and every other
part of grading still come from the benchmark snapshot.

The gold actions are replayed exactly as in upstream grading. Only the final comparison
between the gold and agent databases changes, and it applies to both the agent-side and
user-side comparison (in this domain they are the same database):

- `agent_discoverable_tools`: every tool name the gold logged must also appear in the
  agent's table, but the agent may have more. Extra discoverable reads, and extra
  discoverable calls of any kind, therefore do not fail the task on this table. A gold-
  required discoverable call the agent skipped still fails.
- `closure_reason` is removed from every record before comparing, so a closure's
  free-text reason never decides the result.
- Every other table is compared exactly, field by field. Any state change the gold does
  not make (an extra or different write, a user-tool write, a different argument value)
  fails the task. A discoverable call that errors and only adds a log row to
  `agent_discoverable_tools` does not, because that table is the relaxed one.

ACTION, NL_ASSERTION, and COMMUNICATE grading are unchanged. When a task's validity
depends on one of the relaxed comparisons, say so in the issue, so the result can be
compared with a run that used upstream grading.
