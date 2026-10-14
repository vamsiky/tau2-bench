# Claude Opus 4.7 — `banking_knowledge` Failure Analysis

**Source:** `data/trajectory_data/Claude Opus 4.7_banking_knowledge_trajectories.json`
**Run:** 97 tasks × 4 trials = **388 simulations** · user simulator `gpt-5.2` · agent `claude-opus-4-7` (effort=max) · retrieval=`AllTools`

## Headline

| Metric | Value |
|---|---|
| Trials passed | **98 / 388 (25.3%)** |
| Trials failed | **290 / 388 (74.7%)** |
| Tasks passing all 4 trials | 12 |
| Tasks failing all 4 trials | **58** |
| Flaky tasks (partial) | 27 |
| Termination reason for **every** failure | `user_stop` (no crashes, no timeouts, no max-steps) |

The benchmark is **not** retrieval-bound and **not** harness-bound. Failures are overwhelmingly the agent making the wrong *decision* or wrong *argument value* after it already had the right information in front of it.

> **Per-failure evidence:** every one of the 290 failed trials is itemized with exact gold-vs-actual values in
> [`opus47_banking_failure_evidence_table.md`](opus47_banking_failure_evidence_table.md). The raw trajectories are
> split into 10 browsable files under [`data/trajectory_data/opus47_banking_split/`](../data/trajectory_data/opus47_banking_split/).
> The evidence table is an independent second labeling pass, so its category counts differ slightly from the
> first-pass figures below (notably it reclassifies several borderline GRADER cases as INCOMPLETE/POLICY on closer
> inspection: POLICY 121, INCOMPLETE 59, OVER_ACTION 40, ARG_MECHANICAL 28, GRADER 22, RETRIEVAL 14, USER_SIM 4, VERIFICATION 2).
> The direction is identical: model/agent reasoning ~88%, retrieval ~5%, grader ~8%, harness ~0%.

## How the domain works

Each task is a banking customer-service conversation. The correct trajectory almost always requires the agent to:
1. **Verify identity** (`log_verification`),
2. **Retrieve policy** — `KB_search_bm25` / `KB_search_dense` (returns docs *with* IDs) or `shell` to `cat` policy files,
3. **Unlock + call the correct "discoverable" tool** (`unlock_discoverable_agent_tool` → `call_discoverable_agent_tool`) with exactly-right arguments,
4. Sometimes hand a tool to the user, transfer, or apply a credit.

Grading basis: **87 tasks scored on `DB`** (final database state must match the gold state exactly), **9 on `ACTION`**, 1 on `DB+NL`. Under exact-match DB grading a single wrong argument among many fails the whole task.

## Root-cause breakdown (285/290 failures classified)

Every failed trajectory was read and labeled by comparing the gold action list against what the agent actually did (10 parallel review agents, gold-vs-actual diff).

| High-level category | Share | What it means |
|---|---:|---|
| **Model / agent reasoning** | **83.2%** | Agent had the info; chose/ executed wrong. Breakdown below. |
| **Grader / eval (likely false-negative)** | **10.9%** | Agent's actions matched gold intent yet reward=0. |
| **Retrieval** | **4.2%** | Agent never surfaced the right doc/tool. |
| **User-simulator** | **1.8%** | `gpt-5.2` user gave wrong info or quit while agent was on-track. |
| **Harness / infrastructure** | **~0%** | No crashes; one trial had a tool resubmit-guard as a *contributing* factor only. |

### Model/agent reasoning, decomposed (primary cause per trial)

| Cause | Trials | % of all failures | Description |
|---|---:|---:|---|
| **POLICY_REASONING** | 138 | 48.4% | Right tool, wrong *decision*: wrong account/card chosen, wrong computed value (APY, fee netting, liability), wrong dispute category, wrong provisional-credit eligibility, misapplied escalation/sequencing rules. |
| **INCOMPLETE** | 46 | 16.1% | Required action never executed — most often the agent *believed it couldn't* apply for a card / take a payment and deferred to the user; also premature transfers and skipped protocol steps. |
| **OVER_ACTION** | 32 | 11.2% | Extra DB writes beyond gold: filed extra disputes, closed cards that should stay open, did unrequested transfers. |
| **ARG_MECHANICAL** | 20 | 7.0% | Right tool & branch, mechanically wrong arg: wrong `card_last_4_digits`, wrong `transaction_id`, `account_class` string format ("Sky Blue Account" vs "Sky Blue"), wrong date. |
| **VERIFICATION** | 1 | 0.4% | Identity-verification step itself mishandled. |

## The dominant failure modes (with evidence)

### 1. Policy reasoning — the core weakness (~48%)
Recurring sub-patterns, all "agent read the right policy doc, then applied it wrong":

- **Numeric computation errors.** APY relationship-bonus *stacking* (agent computes 6.875% / $100 where gold is 6.85% / $98 — `task_094/095/097`), fee-netting on refunds (`task_072/073/074` — e.g. credited $3.00 instead of the net $1.50 after a missing fee), liability amounts.
- **Provisional-credit eligibility cap.** Multi-dispute tasks cap how many disputes get provisional credit; the agent repeatedly mis-counts (marks all eligible disputes instead of the top-N by value, ignores a prior dispute that consumes the cap). `task_039, 040, 041`.
- **Wrong account/card selection in optimization tasks.** Agent opens a sub-optimal account/card (e.g. Silver instead of Silver Plus, Bluest instead of Green Fee-Free, Diamond Elite instead of Platinum Rewards). `task_055, 056, 065, 066, 067, 068, 069, 075, 076`.
- **Wrong dispute category.** `card_not_present_fraud` filed where the PIN/in-person facts require `card_present_fraud`. `task_084, 086, 087`.
- **Misapplied procedure/sequencing.** "Process the credit-line increase *first* (it's blocked once a dispute+replacement is filed)" (`task_051/053/054`); "freeze all cards first, then unfreeze the recovered one" lost-wallet protocol — agent closes immediately and can't restore the found card (`task_079/080/081/082`); "Single Flag Escalation → close+reissue" where agent only PIN-resets (`task_091/092`); the 4-request human-transfer rule (`task_081`).

### 2. "I can't do that" — false incompleteness (~16%)
A distinct, **systematic** behavior: on account/card-optimization tasks the agent reasons to the correct recommendation, opens the savings account correctly, but then **declines to call `apply_for_credit_card`**, telling the user to apply themselves ("I'm not able to submit applications through this channel"). The gold trajectory requires the agent to make the call, so the DB write is missing. Seen across `task_058, 059, 063, 064, 066, 067, 068, 069`. Same shape for refusing to process a payment (`task_043, 045`). This is an over-conservative guardrail, not a capability gap.

### 3. Over-action (~11%)
Exact-match DB grading punishes doing *too much*. Agents file an extra dispute beyond the requested subset, close a card that has a pending replacement (and must stay open — `task_048/049`), or perform a user-requested transfer that isn't in the scenario's gold (`task_055/071`). Two adversarial tasks (`task_027/029`) bait the agent into calling `update_transaction_rewards` on a user's false "the dispute was already resolved" claim — the agent takes the bait.

### 4. Retrieval is a minor cause (~4%)
True retrieval failures exist but are rare. The clearest are the "speed-bump" tasks (`task_032/033`) where the agent never **discovers** the staged `initial_transfer_to_human_agent_*` tool and transfers directly, and `task_072/073` where it never finds the bank-account lookup tools. KB search itself generally surfaces the right document (it returns doc IDs and scored chunks); the agent usually reads the right policy and then mis-applies it.

### 5. Grader / eval false-negatives (~11%) — needs a second look
31 trials where the reviewer found the agent's actions matched the gold trajectory yet reward stayed 0. These are **all DB-basis** (exact state match) and split into:
- **Likely genuine eval/gold problems.** `task_005`'s gold trajectory *accepts a social-engineering "supervisor bypass code" and changes the account email without real verification*; the agent correctly refuses and is marked wrong (3/4 trials flagged independently). Worth auditing the gold here.
- **`account_class` string-format mismatches.** Several account-opening "matches" differ only by `"X Account"` vs `"X"` in a free-text arg (`task_060, 062, 076, 098, 099`, overlapping the ARG_MECHANICAL bucket). Ambiguous: either an agent formatting slip or a missing normalization in the DB check. Cheap to resolve and would recover several tasks.

## Structural finding: complexity, not capability, predicts failure

| Task group | # tasks | Median gold actions required |
|---|---:|---:|
| Always-fail (0/4) | 58 | **10** (mean 11.7, max 33) |
| Flaky (partial) | 27 | 5 |
| Always-pass (4/4) | 12 | 5 |

Pass rate by grading basis: **ACTION 42%** vs **DB 24%**. The long, many-action DB tasks dominate the failure set because exact-match grading compounds: with ~10–30 required writes each carrying derived arguments, the probability that *every* argument is correct collapses. The most-mismatched argument keys across all failures are computed/policy-derived: `customer_max_liability_amount`, `amount`, `expected_apy`, `eligible_for_provisional_credit`, `account_class`, `dispute_reason` — i.e. exactly the values the agent must *calculate* or *classify*, not look up.

## Always-fail tasks (0/4) by dominant cause

- **POLICY_REASONING (31):** task_020, 023, 026, 032, 039, 040, 041, 044, 049, 054, 062, 063, 065, 066, 067, 068, 069, 073, 074, 075, 080, 081, 082, 086, 087, 091, 092, 095, 097, 101, 102
- **INCOMPLETE (10):** task_010, 014, 043, 047, 058, 061, 064, 088, 099, (053)
- **OVER_ACTION (7):** task_027, 029, 046, 048, 071, 078, 084
- **GRADER — audit these first (7):** task_005, 052, 060, 076, 077, 079, 085
- **ARG_MECHANICAL (2):** task_038, 083
- **USER_SIM (1):** task_015

## Recommendations

1. **Biggest lever is reasoning, not retrieval.** Improvements should target multi-step policy application, financial arithmetic (APY/fee/liability), and eligibility-cap counting — not the RAG layer.
2. **Fix the "I can't apply / can't pay" guardrail.** ~16% of failures are the agent declining an action it was supposed to take. A prompt/policy clarification that the agent *is* authorized to call these write tools would recover a large block of tasks.
3. **Curb over-action.** Reinforce "do exactly what's requested, verify before extra writes," especially against adversarial user claims.
4. **Audit the ~11% grader-flagged set before trusting the headline number.** Start with `task_005` (gold appears to reward a scam) and the `account_class` string-normalization cases. The true pass rate may be a few points higher than 25.3%.

---
*Method: programmatic extraction of gold-action vs actual-tool-call signals for all 290 failures, then per-trajectory root-cause labeling by 10 parallel review agents diffing gold vs actual. 285/290 trials labeled (98%); 5 unlabeled due to dedup. Category counts are primary-cause; many trials have a secondary contributor (most commonly POLICY_REASONING + INCOMPLETE).*
