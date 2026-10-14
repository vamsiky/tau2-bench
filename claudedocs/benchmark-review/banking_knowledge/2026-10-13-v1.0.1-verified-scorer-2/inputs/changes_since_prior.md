## Version 1.0.1 - Banking Grading Fixes ⚖️

**Release Date**: July 2026

### ⚠️ banking_knowledge scores change with this release

1.0.1 bundles the recent `banking_knowledge` grading and task fixes. Together they correct
a systematic penalty that zeroed rewards for correct-but-cautious agent behavior, plus
task-data issues surfaced by recent runs.
**Scores computed before and after this release are not comparable on banking_knowledge.**
All other domains are unaffected.

#### What was wrong

1. **Extra read calls zeroed the reward** (#329). Every `call_discoverable_agent_tool` call
   was logged to a DB table that participates in the reward's DB-hash comparison. An agent
   that did one prudent verification read not present in the golden trajectory — e.g.
   listing a user's accounts after opening one, or checking a replacement-card order it just
   placed — failed the task, even though the knowledge base encourages such reads. Reads are
   now logged only when the task's golden trajectory requires them, so "agent must verify X"
   assertions still discriminate while extra validation reads no longer poison the hash.
2. **Int-vs-float argument spelling changed DB hashes** (#397). `25` and `25.0` are the same
   JSON number but produced different deterministic record IDs and DB states. Numeric
   arguments are now normalized.
3. **Tasks 077–086 gold trajectories were not agent-realizable** (#402). The lost/stolen
   card scenarios omitted reads any real agent must perform; the golden trajectories now
   include them.
4. **Bank account transactions were returned oldest-first, contradicting the docs** (#403).
   The knowledge base documents `get_bank_account_transactions_9173` as most-recent-first,
   but the tool returned raw DB insertion order, making the "dispute the earliest duplicate"
   tie-breaker unresolvable from tool output on the duplicate-charge tasks (083–085). Output
   is now sorted by date descending (stable sort), and task_085's fixture rows were aligned
   to the same tie-break convention as 083/084. No gold actions changed.
5. **Contradictory cash-back rate in the Platinum Rewards knowledge doc** (#388). The
   document stated two different rates for the same card; the numbers now agree.
6. **task_074 under-refunded Light Blue ATM fees against its own policy docs** (#374). The
   Light Blue Account docs grant two free out-of-network and two free foreign ATM
   withdrawals per month, but the gold refund honored only one of each ($8.00 instead of
   $14.50). The fixture's fee descriptions also embedded the answer key — annotations like
   "(SHOULD BE FREE - 1ST OF 2)" and "(AFTER 2 FREE)" told the agent which fees were
   erroneous. The gold credit is now the policy-faithful $14.50 and all twelve annotated
   descriptions are scrubbed to plain statement text, so the agent must derive the free
   allowance from the policy docs. Four "AFTER FREE ALLOWANCE" annotations of the same
   kind on the task_072/073 Light Green accounts are scrubbed too (description-only, no
   grading impact). Unlike the grading fixes, this changes a gold
   value: a trajectory that reproduced the old $8.00 refund fails task_074 under 1.0.1,
   while policy-faithful $14.50 refunds now pass.

