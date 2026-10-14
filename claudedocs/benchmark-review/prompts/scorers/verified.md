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
  agent's table. An extra tool name is allowed only if every call the agent made to that
  tool was rejected for bad input (missing, mistyped, or out-of-range arguments, or an ID
  that does not exist), read from the tool results in the trajectory. An extra call that
  succeeded, or that the tool rejected for status, eligibility, balance, ownership, or a
  duplicate, still fails. A gold-required discoverable call the agent skipped still fails.
  Upstream already leaves extra discoverable reads and GENERIC (transfer) calls out of
  this table unless the gold calls the same tool, so this only changes the result for
  extra write calls.
- `closure_reason` is removed from bank-account records (`accounts`) only. There it is
  an optional free-text argument of `close_bank_account_7392` with a hidden default.
  Debit-card closures (`close_debit_card_4721`) and credit-card closure logs
  (`log_credit_card_closure_reason_4521`) store a fixed category the policy asks the
  agent to choose, and those are compared exactly.
- Every other table is compared exactly, field by field, including the user-side tables
  (`user_discoverable_tools`, `user_discoverable_tool_calls`, `human_transfer_requests`).

ACTION, NL_ASSERTION, and COMMUNICATE grading are unchanged. When a task's validity
depends on one of the relaxed comparisons, say so in the issue, so the result can be
compared with a run that used upstream grading.
