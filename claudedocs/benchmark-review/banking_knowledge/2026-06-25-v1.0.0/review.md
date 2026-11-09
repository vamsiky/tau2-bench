# tau2-bench `banking_knowledge` — Benchmark Correctness Review (v2, corrected)

_Audit of whether each of the 97 tasks is well-posed, self-consistent, and deterministically solvable from the customer instructions + the task's knowledge + the agent's toolset._

**Scope:** all 97 tasks, loaded from the authoritative `data/tau2/domains/banking_knowledge/tasks/` directory (what `get_tasks()` reads). **Review date:** 2026-06-25.

## 0. Corrigendum — what changed from the first review

This v2 supersedes the initial review. A second-pass verification (and a reader catch on task_027)
exposed methodology errors in v1, all corrected here by re-auditing every task from the authoritative
source against the live DB and code:

1. **Wrong task source.** v1 built materials from `tasks.json`; the benchmark actually loads from the
   `tasks/` directory, and the two diverge on 11 tasks (required_documents on 7: 027/046/048/056/081/083/088;
   instructions on 4: 048/061/062/085; gold actions on 3: 048/062/084). v1's task_027 Blocker ("2× promo
   doc absent") was the visible symptom — the promo doc *is* in the authoritative task. v2 uses `tasks/`.
2. **Reward rounding mischaracterized.** v1 claimed "undocumented floor rounding." Verified by computation:
   the seed's rounding is undocumented **and inconsistent** — floor for tasks 017/018/019/021/022/029,
   round-half-up for 020/026/027 (028 documents floor explicitly). So round-seed tasks are solvable with
   the natural convention (Minor); floor-seed tasks need a non-natural guess (Major).
3. **Discoverable-tool arguments are not hidden.** v1 flagged `customer_max_liability_amount` as an
   undocumented gold argument. Unlocking a discoverable tool returns its parameter list parsed from the
   function docstring, which documents that argument — so the agent knows it. (The real task_083 defect is
   that its *gold* omits this required arg, so no correct agent call can match.)
4. **Knowledge model: the agent reads the whole KB.** This review treats `required_documents` as a
   *relevance annotation* the agent is expected to rediscover from the knowledge base — NOT as the only
   docs it may read. This matches the default `alltools` retrieval, where the agent KB-searches the full
   698-doc knowledge base (BM25 + dense + read-only shell) rather than being handed `required_documents`.
   Consequence: **a rule that exists somewhere in the KB but is missing from a task's `required_documents`
   is NOT a solvability defect** — the agent can find it by search. Three v1/early-v2 "document gap"
   findings (task_050, 088, 096) are therefore downgraded; their `required_documents` lists are merely
   incomplete annotations (they would be Blockers only under the restrictive `golden_retrieval` variant,
   which is not assumed here).
5. **Always-on read tools.** v1 raised several "the customer can't supply transaction IDs" Blockers; the
   agent always has `get_credit_card_transactions_by_user` / `get_credit_card_accounts_by_user` /
   `get_user_information_by_*` (base toolkit), so those were premise errors, now removed.

Net effect: v1 reported 8 Blocker / 24 Major / 29 Minor / 36 clean; v2 reports the counts below. v2 is
both cleaner (many v1 false-positives removed) and catches genuine defects v1 missed (e.g. task_101).

## 1. Summary

| Severity | Count | Tasks |
|---|---|---|
| **Blocker** | 10 | task_039, task_040, task_041, task_063, task_074, task_075, task_082, task_083, task_084, task_101 |
| **Major** | 11 | task_017, task_018, task_019, task_021, task_022, task_025, task_029, task_073, task_095, task_097, task_102 |
| Minor | 14 | (cosmetic `$`-corruption, round-seed undocumented rounding, forced-choice selection — see table) |
| None (clean) | 62 | — |

**62 of 97 tasks are clean; 35 flagged** (10 Blocker, 11 Major, 14 Minor). Every Blocker/Major was re-derived by the lead auditor against the live `db.json` and `tools.py`.

## 2. Plain-English summary — what's actually wrong with each flagged task

A jargon-free one-liner per flagged task, so you can grasp the issue without reading the technical detail. (Clean tasks are omitted; the full evidence for each is in §6.)

**Blockers — the task can't be scored fairly; even a correct agent gets marked wrong:**

- **task_039** — The bank's written rule gives emergency 'provisional credit' on disputes as long as the customer hasn't filed more than 2 disputes in the past year. This customer has filed none, so by the rule all 4 of their disputes qualify — but the official answer only grants it to 3, using an unwritten 'max 3 at a time' limit. An agent that follows the actual rule gives all 4 and is marked wrong.
- **task_040** — Same issue as task_039: the official answer caps how many disputes get provisional credit using a per-conversation limit that appears in no document, so an agent following the written rule is marked wrong.
- **task_041** — Same provisional-credit problem: by the written rule about 10 of the customer's disputes qualify, but the official answer only grants it to 2, relying on an unwritten limit (plus the customer's casual 'prioritize these two').
- **task_063** — The customer wants whichever credit card boosts their savings rate the most. Two cards boost it by the exact same amount and both meet the customer's only other condition — a genuine tie — but the official answer demands one specific card, so picking the equally-good other card is marked wrong.
- **task_074** — The official refund amounts can only be reached by counting ATM fees dated after 'today' (the clock is fixed to Nov 14 but the fees are dated Nov 15–18) and by using a fee rule written nowhere. No agent working as of 'today' can reach those numbers.
- **task_075** — The customer wants the checking account with the lowest foreign-ATM fees. Two accounts both charge $0 — a tie with no tiebreaker — but the official answer insists on one specific account.
- **task_082** — There's fraud on two of the customer's cards, and the bank's rule (and the customer) says fraud means cancel-and-replace the card. The official answer does this for one card but skips the other, so an agent that correctly handles both is marked wrong.
- **task_083** — The dispute tool requires a 'maximum liability amount' field, but the official answer leaves it out. A correct agent must fill it in — and then no longer matches the incomplete official answer, so full marks are impossible.
- **task_084** — Two identical charges on the same day with nothing to tell them apart. The rule says 'dispute the first one,' but the official answer disputes the second, so an agent has no way to pick the same one. (The liability amount is also calculated inconsistently.)
- **task_101** — The customer wants to refer 4 people. A rule limits how many referral bonuses you can RECEIVE in 9 days, but this customer has received none recently, so the limit doesn't apply. The official answer still submits only 2 referrals as if it did, so an agent that correctly submits all 4 eligible ones is marked wrong.

**Majors — serious ambiguity or inconsistency; a careful agent can often still get it right:**

- **task_017** — To find the customer's wrongly-credited rewards, the agent compares each transaction's reward to what it should be. The bank rounds reward points in a way that's never written down, and here the stored numbers don't even match the obvious rounding — so a strict comparison flags extra transactions. It only works if the agent ignores tiny 1-point differences, which no document mentions.
- **task_018** — Same rounding problem: reward points are stored 'rounded down' with no rule written down, so an agent using normal rounding flags many extra transactions and is marked wrong unless it ignores tiny differences.
- **task_019** — Same undocumented rounding problem (this task rounds down).
- **task_021** — Same undocumented rounding problem (rounds down).
- **task_022** — Same undocumented rounding problem (rounds down), across many transactions and four cards.
- **task_025** — Which card is 'best' depends on whether 'Apple Music' counts as a blocked 'Apple' purchase on one card and a rewarded 'media' purchase on another — a judgment call that's never spelled out. Reading it the other way flips the winner by 10x.
- **task_029** — Same undocumented rounding problem (rounds down).
- **task_073** — The official refund needs several non-obvious leaps: treating fees charged at the bank's OWN ATMs as mistakes, voiding a duplicate fee, and canceling an overcharge against a separate undercharge. An agent that simply refunds the overcharges gets a different total.
- **task_095** — The documents contradict each other about whether a small +0.025% bonus stacks on top of the other bonuses, so the 'correct' interest figure isn't the only reasonable one.
- **task_097** — Same +0.025% bonus confusion — and it's handled inconsistently with a near-identical task (task_093) that DOES include it, so the official figure here is doubtful.
- **task_102** — The customer wants the referral that pays the biggest bonus, but the documents include an account that pays more than the official answer's pick, so a careful agent reasonably chooses the higher-paying one and is marked wrong.

**Minor — basically fine; small wrinkles a competent agent resolves:**

- **task_008** — Basically fine. Two transfer-reason codes overlap slightly, but the 'pick the highest tier' rule settles which to use.
- **task_016** — Basically fine. The referral and the spend amount are uniquely determined.
- **task_020** — Fine. The reward-rounding rule isn't written down, but normal 'round to nearest' matches the data here.
- **task_023** — Fine. The customer mis-states when they opened the card, but it doesn't change the answer.
- **task_026** — Fine. The reward-rounding rule isn't written down, but normal 'round to nearest' matches the data and gives exactly the right disputes.
- **task_027** — Fine (this is the one previously mis-flagged). The promo and exclusion docs are present, and normal rounding gives exactly the right disputes; the only nit is that the rounding rule isn't spelled out.
- **task_057** — Fine. Only one checking account is described so the choice is forced; one of the customer's wishes isn't explicitly confirmed in that account's doc, but there's no alternative.
- **task_072** — Fine but fiddly: the refund spans the whole month (including a few days after 'today') and requires netting over- and under-charges as the doc says.
- **task_085** — Fine. Two identical same-day charges, but the official pick is the natural 'first' one.
- **task_086** — Fine but involved: one refund amount needs a multi-step reconciliation, but the customer's script steers it to the right number.
- **task_088** — Fine. The provisional-credit guidelines aren't in this task's listed docs but do exist in the knowledge base (findable); the only soft point is the exact liability amount.
- **task_092** — Fine. The fraud-risk thresholds are a bit fuzzy, but the customer's answers ('I was asleep', 'set the PIN to…') pin down each outcome.
- **task_094** — Fine. A +0.025% bonus is described two ways, but they refer to the same benefit, so the natural reading gives the right number.
- **task_100** — Fine. The customer vaguely mis-states how long they've banked here, but the rule says to use the on-file account-open date, which settles it.

## 3. Top systemic issues

1. **Undocumented per-session provisional-credit cap (Blockers 039, 040, 041).** `doc_(general)_015`
   criterion 4 is a 12-month *history* gate ("not more than 2 disputes in the past 12 months"), but the
   gold trajectories treat it as a per-session cap with inconsistent limits (3 in task_039, ~2 in
   task_041) applied in filing order. With ≤1 prior dispute the literal rule leaves every reason-eligible
   dispute eligible, so a correct agent marks more `eligible_for_provisional_credit=true` than gold and
   fails the exact-DB match. The cap is nowhere documented.
2. **Reward rounding undocumented AND inconsistent (Majors 017, 018, 019, 021, 022, 029; round-seed
   Minors 020, 026, 027).** `rewards_earned` is stored rounded but no doc states the rule, and the
   convention differs across tasks (floor vs round-half-up — verified by recomputation). The genuine
   errors are gross (factor-of-N) and separable from ±1 noise, so an agent disputing only "material"
   discrepancies recovers each set — hence Major (fragile), not Blocker. task_028 alone includes the
   floor-policy doc and is clean.
3. **APY "relationship bonus" stacking is self-contradictory (Majors 095, 097).** The +0.025%
   Gold/Silver bonus is labelled both a "relationship bonus" (stacks) and a "credit-card APY bonus"
   (highest-only) across docs; task_093 *includes* it in its gold APY while task_097 *omits* it for the
   structurally identical Silver scenario, so the exact `expected_apy`/credit DB write is non-deterministic.
4. **DB-keyed product selection is non-unique (Blockers 063, 075; Major 102).** `apply_for_credit_card`
   (keyed on card_type) and `open_bank_account` (keyed on account_class) require a unique optimum, but
   task_063 has two cards with identical +0.15% bonuses, task_075 has two checking accounts both $0
   foreign-ATM, and task_102's docs contain a strictly-higher-bonus alternative than the gold.
5. **Same-date duplicate-charge ties (Blockers 083, 084).** When two identical charges share a date with
   no timestamp, "dispute the earliest (first)" has no deterministic referent; the gold disputes the
   second-in-DB-order record. (task_083 additionally: its ACTION gold omits the required
   `customer_max_liability_amount`, so no correct agent call can ever match.)
6. **Gold-trajectory construction bugs (Blockers 074, 082, 101).** task_082 omits the GFF
   close-and-reissue its own dispute mapping + the customer request require; task_101 caps referrals at 2
   with no documented basis (the 9-day window counts received bonuses and the user has zero — a correct
   agent submits all 4 eligible); task_074's gold credits require counting transactions dated *after* the
   fixed clock (11/15–11/18 vs today 11/14) plus an undocumented fee baseline.
7. **Incomplete `required_documents` annotations — NOT defects under the full-KB-read model (050, 088,
   096; data-hygiene note only).** Each omits a doc the gold uses from its `required_documents`
   (card→tier map `(general)_015`; provisional guidelines `(general)_032`; Green-Fee-Free boost
   `green_fee-free_account_005`), but every one of those docs exists in the knowledge base and is
   findable by KB search, so the agent can still solve the task. These would be Blockers only under the
   restrictive `golden_retrieval` variant; worth fixing the annotations, but not solvability defects here.
8. **Pervasive but cosmetic `$`-on-non-currency corruption (25/698 docs).** Credit scores as "$720",
   "$105 days", EcoCard "$5.00 points". Rarely load-bearing (credit score is never a tool input) → Minor.

## 4. Methodology & grading model

- **Grading.** ~88 tasks grade on final-DB exact match (gold actions replayed → reference DB; the
  verified scorer only allows extra discoverable-tool *reads* and strips `closure_reason`); ~9 grade on
  ACTION match (all args in the agent's call compared unless `compare_args` restricts them). So for DB
  tasks every DB-writing gold argument must be uniquely derivable.
- **Knowledge model (full-KB read).** `required_documents` is treated as a relevance annotation the agent
  rediscovers, not a closed reading list. The default `alltools` retrieval gives the agent BM25 + dense
  KB_search + read-only shell over the full knowledge base. So a needed rule that lives anywhere in the
  KB is reachable; only a rule absent from the ENTIRE KB (or a wrong/contradictory rule) is a defect.
- **Always-on read tools** (`get_credit_card_transactions_by_user`, `get_credit_card_accounts_by_user`,
  `get_user_information_by_*`): the agent can enumerate the customer's transactions/accounts and look up
  identity fields, so "the customer didn't state X" is not a gap when X is in the DB.
- **Discoverable tools** expose their docstring parameter list on unlock (so documented-in-docstring args
  are known to the agent).
- **Fixed clock**: today = 2025-11-14 03:40 EST (via `get_current_time`) → timestamps deterministic.
- **Rounding**: computed per task (floor vs round-half-up) directly from `db.json`.

## 5. Per-task table

The **plain-English issue** column states the problem in everyday terms; **evidence** is a short technical snippet (full write-ups for Blocker/Major are in §6). Other columns: instr_suff (instructions sufficient), docs_det (knowledge deterministic), cx (reasoning complexity 1–5), ordering (step-order dependency), gold_ok (official answer consistent), severity.

| task | severity | plain-English issue | instr_suff | docs_det | cx | ordering | gold_ok | evidence (technical) |
|---|---|---|---|---|---|---|---|---|
| task_001 | None | Clean — no issue | Sufficient | Yes | 2 | None | Yes | — |
| task_002 | None | Clean — no issue | Sufficient | Yes | 2 | None | Yes | — |
| task_003 | None | Clean — no issue | Sufficient | Yes | 3 | None | Yes | Silver and Gold both meet hard reqs (0% FTF w/ premium, purchase protection, 100k-limit possible) and both have $0 annual fee; tiebreak "highest cash back" resolves to... |
| task_004 | None | Clean — no issue | Sufficient | Yes | 3 | None | Yes | DB user 6680a37184 has email kenji.tanaka@outlook.com but customer asserts gmail and won't give DOB/address, so only phone (206-555-0293) matches → 2-of-4 verification... |
| task_005 | None | Clean — no issue | Sufficient | Yes | 2 | None | Yes | — |
| task_006 | None | Clean — no issue | Sufficient | Yes | 2 | None | Yes | — |
| task_007 | None | Clean — no issue | Sufficient | Yes | 2 | None | Yes | — |
| task_008 | Minor | Minor reason-code overlap; the 'highest tier' rule settles it | Sufficient | Yes | 2 | None | Yes | ACTION task, compare_args=["reason"]; gold reason "customer_demands_after_unavailable_offer_refusal" is the TIER-1 code; mild overlap with TIER-2 "unconfirmed_external... |
| task_010 | None | Clean — no issue | Sufficient | Yes | 3 | Soft | Yes | — |
| task_012 | None | Clean — no issue | Sufficient | Yes | 1 | None | Yes | — |
| task_014 | None | Clean — no issue | Sufficient | Yes | 2 | None | Yes | — |
| task_015 | None | Clean — no issue | Sufficient | Yes | 3 | Soft | Yes | — |
| task_016 | Minor | No real issue; uniquely determined | Sufficient | Yes | 3 | None | Yes | card type "Silver Rewards Card" and $750 spend uniquely derivable: only IN_PROGRESS referral is f2a3b4c5d6789012 (Silver Rewards Card, 11/13/2025) and doc silver_rewar... |
| task_017 | Major | Unwritten reward-rounding; strict check over-flags rows | Sufficient | Partial | 4 | None | Yes | DB-graded cash_back_disputes must match exactly; gold disputes only the 2 GROSS errors (txn_913d14a20dc5 stored 15 vs ~157 @1%; txn_cfabb609133d stored 47 vs ~87 @1%) ... |
| task_018 | Major | Unwritten 'round down'; normal rounding over-flags rows | Sufficient | Partial | 4 | None | Yes | Computed both conventions: ONLY FLOOR reproduces the gold set exactly (6 txns, 0 false positives); round-half-up (the natural default) yields 28 disputes = 22 false po... |
| task_019 | Major | Unwritten 'round down' rounding (over-flags rows) | Sufficient | Partial | 4 | None | Yes | Only FLOOR rounding reproduces the gold set exactly (4 disputes, 0 false positives); round-half-up gives ~9 false positives (e.g. txn_f2a3b4c5d6e7 stored 562 vs rhu 56... |
| task_020 | Minor | Rounding unwritten, but normal rounding works | Sufficient | Yes | 4 | None | Yes | ROUND-HALF-UP reproduces the gold set exactly (4 txns, 0 false positives); floor instead yields 13 disputes (9 false positives, all -1 noise, e.g. txn_b7e2d4c5f512 Nor... |
| task_021 | Major | Unwritten 'round down' rounding (over-flags rows) | Sufficient | Partial | 4 | None | Yes | FLOOR reproduces the gold set with zero false positives; round-half-up yields 6 false positives (ThredUp 50/51, HBO Max 142/143, Spotify 439/440, Tesla Supercharger 24... |
| task_022 | Major | Unwritten 'round down' rounding (over-flags rows) | Sufficient | Yes | 5 | Soft | Yes | Only FLOOR (truncation) reproduces the gold set EXACTLY (10 disputes, 0 FP, 0 FN); round-half-up yields 26 false positives — all pure +1 noise on $0.005-tail amounts. ... |
| task_023 | Minor | Customer mis-states card-open date; doesn't change answer | Sufficient | Yes | 4 | None | Yes | rebate-qualification deterministic — every monthly window (anniversary day 10) of the completed cardmember year 11/10/2024–11/09/2025 exceeds the $7,500 threshold (doc... |
| task_024 | None | Clean — no issue | Sufficient | Yes | 4 | None | Yes | — |
| task_025 | Major | Best card hinges on an undefined 'Apple Music' category | Sufficient | Partial | 5 | None | Yes | Gold picks Business Platinum (4% media/software = $4,000) over Business Silver (10% = $10,000); this is only correct if "Apple Music" is mapped to the excluded "Apple"... |
| task_026 | Minor | Rounding unwritten, but normal rounding works | Sufficient | Yes | 4 | Soft | Yes | round-half-up reproduces the gold set exactly (verified; floor gives 9 FPs); convention undocumented but natural. |
| task_027 | Minor | Solvable; only the rounding rule isn't spelled out | Sufficient | Yes | 4 | None | Yes | ROUND-HALF-UP reproduces the exact gold 4-dispute set (e403/f506/e410/e411) with ZERO false positives; FLOOR gives 9 false positives. Promo: Business Silver open 02/13... |
| task_028 | None | Clean — no issue | Sufficient | Yes | 4 | Strict | Yes | FLOOR reproduces the exact gold 6-dispute set with zero false positives (round gives 22 FPs); doc_credit_cards_credit_cards_(general)_007 explicitly documents floor/tr... |
| task_029 | Major | Unwritten 'round down' rounding (over-flags rows) | Sufficient | Partial | 4 | Soft | Yes | Only FLOOR rounding reproduces the gold dispute set exactly (6 txns, 0 false positives); round-half-up (the natural default) yields 22 false positives. The 6 gold erro... |
| task_031 | None | Clean — no issue | Sufficient | Yes | 2 | None | Yes | — |
| task_032 | None | Clean — no issue | Sufficient | Yes | 2 | Soft | Yes | — |
| task_033 | None | Clean — no issue | Sufficient | Yes | 2 | Strict | Yes | — |
| task_034 | None | Clean — no issue | Sufficient | Yes | 2 | Strict | Yes | — |
| task_035 | None | Clean — no issue | Sufficient | Yes | 1 | None | Yes | — |
| task_036 | None | Clean — no issue | Sufficient | Yes | 2 | None | Yes | — |
| task_037 | None | Clean — no issue | Sufficient | Yes | 3 | Soft | Yes | — |
| task_038 | None | Clean — no issue | Sufficient | Yes | 3 | Soft | Yes | — |
| task_039 | Blocker | Unwritten cap on how many disputes get provisional credit | Partial | No | 4 | Strict | No | Gold treats provisional criterion #4 ("not filed more than 2 disputes in the past 12 months", doc_015) as an undocumented PER-SESSION running cap: of the 4 reason-elig... |
| task_040 | Blocker | Unwritten per-conversation provisional-credit cap | Partial | No | 4 | Strict | No | Gold marks American Airlines fraud ($342.50, txn_a1b2c3d4e503) and Best Buy duplicate ($189.99, txn_a1b2c3d4e510) as eligible_for_provisional_credit=FALSE, yet both sa... |
| task_041 | Blocker | Unwritten provisional-credit cap (only 2 of ~10 granted) | Partial | No | 4 | Strict | No | eligible_for_provisional_credit written to DB but gold marks ONLY Staples (041_9) + Coinbase (041_10) true; doc_015 criteria yield 10 reason-eligible disputes and the ... |
| task_043 | None | Clean — no issue | Sufficient | Yes | 3 | Strict | Yes | — |
| task_044 | None | Clean — no issue | Sufficient | Yes | 3 | Soft | Yes | — |
| task_045 | None | Clean — no issue | Sufficient | Yes | 4 | Strict | Yes | — |
| task_046 | None | Clean — no issue | Sufficient | Yes | 3 | Soft | Yes | — |
| task_047 | None | Clean — no issue | Sufficient | Yes | 3 | Soft | Yes | — |
| task_048 | None | Clean — no issue | Sufficient | Yes | 4 | Strict | Yes | — |
| task_049 | None | Clean — no issue | Sufficient | Yes | 5 | Strict | Yes | — |
| task_050 | None | Clean — a needed doc isn't in the task's list but is findable in the KB | Sufficient | Yes | 3 | Strict | Yes | NOT a solvability defect under the full-KB-read model: the card→CLI-tier map (doc_(general)_015) is absent from this task's required_documents but exists in the knowle... |
| task_051 | None | Clean — no issue | Sufficient | Yes | 3 | Strict | Yes | — |
| task_052 | None | Clean — no issue | Sufficient | Yes | 3 | Strict | Yes | — |
| task_053 | None | Clean — no issue | Sufficient | Yes | 4 | Strict | Yes | — |
| task_054 | None | Clean — no issue | Sufficient | Yes | 4 | Strict | Yes | — |
| task_055 | None | Clean — no issue | Sufficient | Yes | 4 | Soft | Yes | — |
| task_056 | None | Clean — no issue | Sufficient | Yes | 3 | Soft | Yes | — |
| task_057 | Minor | Only one account described, so the choice is forced | Sufficient | Yes | 3 | Strict | Yes | Only one checking-product doc (blue_account_001) is in required_documents so Blue Account is the forced unique recommendation; Blue satisfies no-overdraft-fees, 1-day ... |
| task_058 | None | Clean — no issue | Sufficient | Yes | 3 | Soft | Yes | — |
| task_059 | None | Clean — no issue | Sufficient | Yes | 3 | Soft | Yes | — |
| task_060 | None | Clean — no issue | Sufficient | Yes | 4 | Strict | Yes | — |
| task_061 | None | Clean — no issue | Sufficient | Yes | 4 | Strict | Yes | — |
| task_062 | None | Clean — no issue | Sufficient | Yes | 5 | Strict | Yes | — |
| task_063 | Blocker | Two cards tie for 'best'; only one is accepted | Sufficient | No | 4 | None | No | card_type tie — on Silver Plus Account, doc_savings_accounts_silver_plus_account_009 gives Bronze Rewards +0.15% AND Silver Rewards +0.15% (identical); both verify cre... |
| task_064 | None | Clean — no issue | Sufficient | Yes | 4 | Soft | Yes | — |
| task_065 | None | Clean — no issue | Sufficient | Yes | 5 | Soft | Yes | — |
| task_066 | None | Clean — no issue | Sufficient | Yes | 4 | Strict | Yes | — |
| task_067 | None | Clean — no issue | Sufficient | Yes | 5 | Partial | Yes | — |
| task_068 | None | Clean — no issue | Sufficient | Yes | 4 | None | Yes | — |
| task_069 | None | Clean — no issue | Sufficient | Yes | 4 | Strict | Yes | — |
| task_070 | None | Clean — no issue | Sufficient | Yes | 3 | None | Yes | — |
| task_071 | None | Clean — no issue | Sufficient | Yes | 4 | None | Yes | — |
| task_072 | Minor | Fiddly month-long fee netting, but solvable | Sufficient | Yes | 5 | None | Yes | Both gold credits reproduce under doc_017's "net correction across all fee discrepancies": Bluest $14.00 = 8.0+3.5 foreign-ATM overcharges (Bluest foreign ATM = $0) + ... |
| task_073 | Major | Refund needs several non-obvious offsetting steps | Sufficient | Partial | 5 | Strict | Yes | round-half/floor irrelevant (all fees exact); gold nets reproduce ONLY if agent treats in-network RHO-BANK ATM fees as errors AND nets an undercharge against overcharg... |
| task_074 | Blocker | Refund needs fees dated after 'today' + an unwritten rule | Insufficient | No | 5 | Strict | No | Gold per-account credits (Purple $27.00 / Light Blue $8.00 / Dark Green $4.75 / Evergreen $3.70) are NOT deterministically reconstructable — Purple's $27.00 requires a... |
| task_075 | Blocker | Two accounts tie for lowest fees; only one is accepted | Partial | No | 3 | None | No | The DB-keyed account choice is not unique: Green Fee-Free (gold), Purple, and Bluest all have a $0.00 foreign ATM withdrawal fee (doc_..._green_fee-free_005, doc_..._p... |
| task_076 | None | Clean — no issue | Sufficient | Yes | 3 | None | Yes | — |
| task_077 | None | Clean — no issue | Sufficient | Yes | 3 | Strict | Yes | — |
| task_078 | None | Clean — no issue | Sufficient | Yes | 4 | Strict | Yes | — |
| task_079 | None | Clean — no issue | Sufficient | Yes | 5 | Strict | Yes | — |
| task_080 | None | Clean — no issue | Sufficient | Yes | 5 | Strict | Yes | — |
| task_081 | None | Clean — no issue | Sufficient | Yes | 5 | Strict | Yes | — |
| task_082 | Blocker | Fraud fixed on one card but skipped on the other | Partial | Partial | 5 | Strict | No | Gold records CryptoGems (GFF card, card_not_present_fraud) card_action='close_and_reissue' and customer explicitly asks to reissue the GFF card, but gold performs clos... |
| task_083 | Blocker | Official answer omits a required field, so it can't be matched | Sufficient | Partial | 4 | Strict | No | ACTION-graded with compare_args=None (all args compared incl. the inner arguments JSON by value), but file_debit_card_transaction_dispute_6281 has REQUIRED positional ... |
| task_084 | Blocker | Two identical charges; official picks the 'wrong' one | Partial | No | 4 | Strict | No | duplicate-charge tie — doc_..._031 "Dispute the earliest (first) transaction when multiple duplicates exist," but the two identical Bella's Bistro $47.50 11/06 charges... |
| task_085 | Minor | Two same-day charges; official picks the natural 'first' | Sufficient | Partial | 3 | Soft | Yes | duplicate-tie — two identical CityFit $89.99 charges on 11/06 (btxn_b2c3d4e5f602, btxn_c3d4e5f6g703) with no timestamp; doc_031 "dispute the earliest (first)"; gold pi... |
| task_086 | Minor | Involved refund math; the customer's script guides it | Sufficient | Partial | 5 | Soft | Yes | ATM-deposit dispute 086_13 disputed_amount=$100 is derived as customer-claimed $500 deposit minus DB-credited $400 (btxn_0788d2513c8c=+400, not the customer's $300) — ... |
| task_087 | None | Clean — no issue | Sufficient | Yes | 4 | Partial | Yes | — |
| task_088 | Minor | Guidelines doc not listed but findable; soft liability value | Partial | Yes | 4 | Soft | Yes | document-gap is NOT a defect under the full-KB-read model: the Debit Card Provisional Credit Guidelines (doc_(general)_032) exists in the KB and is findable; the resid... |
| task_089 | None | Clean — no issue | Sufficient | Yes | 4 | Soft | Yes | — |
| task_090 | None | Clean — no issue | Sufficient | Yes | 5 | Strict | Yes | — |
| task_091 | None | Clean — no issue | Sufficient | Yes | 5 | Strict | Yes | — |
| task_092 | Minor | Fuzzy fraud thresholds; the customer's answers settle it | Sufficient | Partial | 5 | Strict | Yes | Gold per-card outcomes are reachable and the user script steers each one, but the fraud-score thresholds (doc_..._041) are fuzzy for Green/Evergreen (B3 <1-min single-... |
| task_093 | None | Clean — no issue | Sufficient | Yes | 4 | Soft | Yes | — |
| task_094 | Minor | A +0.025% bonus is described twice; same benefit | Sufficient | Yes | 3 | Strict | Yes | Expected APY = 5.5% base + 0.75% Green→Gold checking boost + 0.6% EcoCard (highest CC bonus, no stacking per doc_..._045) = 6.85%; actual = $408/$96000×12 = 5.10%; cre... |
| task_095 | Major | Docs contradict whether a +0.025% bonus stacks | Sufficient | Partial | 4 | Soft | Partial | Gold expected_apy 6.85 = base 5.5 + highest cc bonus 0.6 (EcoCard, stacking doc _045) + highest checking boost 0.75 (Green, selection doc _046), treating the doc_013 "... |
| task_096 | None | Clean — a needed doc isn't in the task's list but is findable in the KB | Sufficient | Yes | 5 | Strict | Yes | NOT a solvability defect under the full-KB-read model: the Green-Fee-Free linked-checking boost doc (green_fee-free_account_005) is absent from required_documents but ... |
| task_097 | Major | +0.025% bonus dropped here but kept in task_093 | Sufficient | Partial | 5 | Soft | Partial | Silver expected_apy 6.65 = 4.0 tier + 0.45 (Bluest→Silver checking boost) + 2.2 (EcoCard highest cc bonus) OMITS the +0.025% relationship-bonus that doc_savings_accoun... |
| task_098 | None | Clean — no issue | Sufficient | Yes | 4 | None | Yes | — |
| task_099 | None | Clean — no issue | Sufficient | Yes | 4 | None | Yes | — |
| task_100 | Minor | Customer vague on tenure; use the on-file open date | Sufficient | Yes | 3 | None | Yes | gold "Hunter Green Account" ($175, 60-day tenure, hunter_green_001) is unique highest-bonus account Tomoko qualifies for at 65-day DB tenure (earliest checking open 09... |
| task_101 | Blocker | Caps referrals at 2 with no basis (should allow all 4) | Partial | No | 5 | Strict | No | gold submits only 2 referrals (Purple, Sky Blue) but the 9-day rolling window (doc_..._047) caps RECEIVING BONUSES, not submissions; submit_referral creates NO_PROGRES... |
| task_102 | Major | A higher-paying referral exists than the official pick | Partial | No | 5 | Strict | No | Rolling 9-day window correctly allows only ONE new referral now (only ref_recent_purple_001 on 11/10 is within 9 days of 11/14), but the customer's explicit goal is "m... |

## 6. Detailed findings (severity ≥ Major)

_Each finding leads with a plain-English line, then the technical evidence._

### Blockers

### task_039 — Blocker

**In plain terms.** The bank's written rule gives emergency 'provisional credit' on disputes as long as the customer hasn't filed more than 2 disputes in the past year. This customer has filed none, so by the rule all 4 of their disputes qualify — but the official answer only grants it to 3, using an unwritten 'max 3 at a time' limit. An agent that follows the actual rule gives all 4 and is marked wrong.

**Discrepancies (technical).** Gold treats provisional criterion #4 ("not filed more than 2 disputes in the past 12 months", doc_015) as an undocumented PER-SESSION running cap: of the 4 reason-eligible disputes it marks the first 3 eligible_for_provisional_credit=true and the 4th (txn_2f16599b9075, Amazon fraud $129.45) false, despite the user having ZERO prior disputes.

**Why not deterministically solvable / fix.** User 01f21c9970 has an empty dispute history; Gold account opened 06/15/2024 (>60d). By doc_015's literal 12-month-history reading, all four fraud/duplicate disputes (Costco $312.87 dup, Costco $234.56 fraud, Amazon $215.67 dup, Amazon $129.45 fraud) satisfy criterion #4 (0 prior < 2) and should be eligible=true. The gold instead applies a "no more than 2 disputes counting those filed earlier in this same session" rule, making the 3rd-filed the last eligible and the 4th ineligible — an order-dependent cap nowhere in the KB. The file_credit_card_transaction_dispute_4829 tool stores eligible_for_provisional_credit verbatim (tools.py:878), so a competent agent who reads doc_015 correctly will pass eligible=true for txn_2f16599b9075, producing a DB mismatch and failing the verified scorer. The customer's hint (#8 "apply provisional to biggest charges first") only resolves WHICH dispute is dropped if a cap exists; it does not establish that the cap exists or that "past 12 months" includes same-session disputes. Fix: either document that in-session disputes count toward the 12-month cap (and that the cap is exactly 3 provisional per session), or mark all four reason-eligible disputes eligible=true.

### task_040 — Blocker

**In plain terms.** Same issue as task_039: the official answer caps how many disputes get provisional credit using a per-conversation limit that appears in no document, so an agent following the written rule is marked wrong.

**Discrepancies (technical).** Gold marks American Airlines fraud ($342.50, txn_a1b2c3d4e503) and Best Buy duplicate ($189.99, txn_a1b2c3d4e510) as eligible_for_provisional_credit=FALSE, yet both satisfy every documented criterion in doc_..._015 (premium-tier max $10k, ≥$25, acct open >60d, fraud/duplicate reason, merchant contacted); the only thing denying them is criterion 4 ("not filed more than 2 disputes in the past 12 months") treated as a per-session running cap that depends on FILING ORDER.

**Why not deterministically solvable / fix.** The user (01f21c9970) has exactly 1 pre-existing dispute in the past 12 months (injected dsp_ed3ab3dce038, submitted 09/20/2025). Doc_..._015 criterion 4 is written as a 12-month HISTORY gate; read against the pre-existing history (count=1) ALL four fraud/duplicate disputes (Grainger, Uline, American Airlines, Best Buy) qualify for provisional credit, so a correct agent would set eligible=true for all four. The gold instead grants provisional to only the first two filed (Grainger, Uline — the ones the customer asked to "prioritize ... if there's any limit") and denies the next two, which only works if same-session disputes increment the count (1→2 after Grainger ok, →3 at American Airlines = "more than 2" → deny). Nothing in the docs says in-session disputes count toward "the past 12 months," and nothing states a per-session cap; the customer's "prioritize Grainger/Uline" line signals intent but does not document a rule. The result is order-dependent: filing American Airlines before Grainger would flip which records carry provisional_credit_given=true, producing a different final DB. A competent agent reading the documented gate literally cannot reproduce the gold provisional-credit flags → DB exact-match fails. Fix: either state explicitly that disputes filed in the current session count toward the 2-in-12-months cap and define a deterministic filing order, or set all four fraud/duplicate disputes to eligible=true.

### task_041 — Blocker

**In plain terms.** Same provisional-credit problem: by the written rule about 10 of the customer's disputes qualify, but the official answer only grants it to 2, relying on an unwritten limit (plus the customer's casual 'prioritize these two').

**Discrepancies (technical).** eligible_for_provisional_credit written to DB but gold marks ONLY Staples (041_9) + Coinbase (041_10) true; doc_015 criteria yield 10 reason-eligible disputes and the 1 prior dispute keeps the 12-mo gate open, so the gold's "exactly the 2 customer-prioritized" picks match no documented rule.

**Why not deterministically solvable / fix.** file_credit_card_transaction_dispute_4829 stores the agent-supplied eligible_for_provisional_credit (and provisional_credit_given) into the DB, so it must be uniquely derivable from doc_015. All 4 accounts opened in 2024 (>60d), all amounts $22.99–$1299.99 are ≥$25 and under tier maxima, and non-fraud disputes were contacted-merchant=true. By doc_015 criterion 2, the provisionally-eligible reasons are fraud, duplicate_charge, and goods_services_not_received(>30d): that is 4 fraud (Delta, Coinbase, Patagonia, Staples) + 4 duplicate (Apple, BestBuy, REI, OfficeDepot) + 2 GNR>30d (Amazon 10/05, WholeFoods 10/02) = 10 disputes that satisfy criteria 1,2,3,5. Criterion 4 (per primer, a 12-month HISTORY gate) sees only 1 prior dispute (dsp_dfab0685d198, 09/20/2025) ≤2, so it does not cut the set. An agent following doc_015 literally marks all 10 true → 8 DB mismatches vs gold. The gold instead marks exactly the two the customer asked to "prioritize…if there's any limit" (Delta, also fraud/in-range/>60d, is marked false), i.e. an undocumented per-session cap of 2 resolved by the customer's arbitrary preference. Not deterministically recoverable. Fix: either document a "max 2 provisional credits per interaction, customer chooses which" rule, or make the gold mark all 10 doc-eligible disputes true.

### task_063 — Blocker

**In plain terms.** The customer wants whichever credit card boosts their savings rate the most. Two cards boost it by the exact same amount and both meet the customer's only other condition — a genuine tie — but the official answer demands one specific card, so picking the equally-good other card is marked wrong.

**Discrepancies (technical).** card_type tie — on Silver Plus Account, doc_savings_accounts_silver_plus_account_009 gives Bronze Rewards +0.15% AND Silver Rewards +0.15% (identical); both verify creditworthiness (Bronze min 640, Silver min 680, score 700 eligible), so gold's apply_for_credit_card card_type="Silver Rewards Card" is not uniquely derivable vs "Bronze Rewards Card".

**Why not deterministically solvable / fix.** The customer's sole stated optimization is the savings annual return ("which ONE combination... absolute highest return," "every dollar counts") plus a card that "actually checks credit." For $8,000 with required paper statements, Silver Plus (3.0% Tier-1) is the documented best savings account (Green savings requires paperless; Gold needs $10k min the customer can't hold; Bronze 2.0%). On Silver Plus the credit-card APY bonus is +0.15% for BOTH Bronze Rewards and Silver Rewards (silver_plus_009), so total savings APY is 3.15% either way — a $0 difference on the very metric the customer cares about. Both cards perform a credit check (Bronze 640 / Silver 680, both ≤700). Nothing in the instructions or docs breaks the tie. Because apply_for_credit_card's deterministic application_id is keyed on card_type, the agent choosing Bronze Rewards produces a different credit_card_applications row than gold's Silver Rewards, failing DB exact-match though it satisfies every stated requirement. Fix: differentiate the two cards (e.g., give Silver a strictly higher Silver-Plus APY bonus, or have the customer state a goal Silver uniquely satisfies), or set compare on card behavior rather than exact card_type.

### task_074 — Blocker

**In plain terms.** The official refund amounts can only be reached by counting ATM fees dated after 'today' (the clock is fixed to Nov 14 but the fees are dated Nov 15–18) and by using a fee rule written nowhere. No agent working as of 'today' can reach those numbers.

**Discrepancies (technical).** Gold per-account credits (Purple $27.00 / Light Blue $8.00 / Dark Green $4.75 / Evergreen $3.70) are NOT deterministically reconstructable — Purple's $27.00 requires an AFTER-CLOCK 11/15/2025 duplicate fee plus an undocumented $2.50 Purple domestic-OON baseline and an inferred "missing rebate"; all four require subtracting undercharges/missing fees, a reading no reasonable agent would adopt over refund-overcharges-only.

**Why not deterministically solvable / fix.** The authoritative task notes (task_074.json description.notes) define 20 seeded errors and NET credits that "account for both overcharges AND undercharges/missing fees." (1) Fixed clock is 11/14/2025 03:40, yet Purple error #5 — the duplicate $2.50 fee — is dated 11/15/2025 (DB: chk_ar72c5d8e3_1 has two atm_fee −2.50 on 11/15 plus a +2.50 rebate). That $2.50 is load-bearing for $27.00; an agent scoping to "November through today" gets $24.50, and even a full-DB read must independently classify it as a duplicate. (2) The Purple knowledge docs (purple_account_001/004) state foreign ATM fee $0.00 and "rebates up to $30/mo" but give NO domestic out-of-network own-fee, so the gold's split — treating one domestic $2.50 as "should be free" yet another as "should be $2.50, charged $3.50" and a separate "missing $2.50 rebate" — is not derivable; my computation under every documented reading (foreign=$0 + domestic-rebated, or domestic fully erroneous) yields 24.50 or 32.00, never 27.00. (3) Doc_..._(general)_017 says "net correction across all identified fee discrepancies," but the gold uses it to SUBTRACT fees the bank failed to charge (Light Blue −$2.50 on 11/10, Dark Green −$2.75, Evergreen −$2.80); a competent agent applying the plain "refund incorrectly charged fees" intent would credit the overcharge totals ($10.50/$7.50/$6.50), not the gold NETs ($8.00/$4.75/$3.70), and would mis-grade on exact DB match. Fix: remove the 11/15 transaction (or move it before the clock), add a documented Purple domestic-OON fee and rebate-timing rule, and make doc_017 explicitly require netting missing/under-charged fees — or change the gold to overcharge-only refunds.

### task_075 — Blocker

**In plain terms.** The customer wants the checking account with the lowest foreign-ATM fees. Two accounts both charge $0 — a tie with no tiebreaker — but the official answer insists on one specific account.

**Discrepancies (technical).** The DB-keyed account choice is not unique: Green Fee-Free (gold), Purple, and Bluest all have a $0.00 foreign ATM withdrawal fee (doc_..._green_fee-free_005, doc_..._purple_001, doc_..._bluest_003), so the customer's sole criterion "lowest total ATM fees" cannot select Green Fee-Free over Purple; Purple is arguably strictly better (adds up to $30/mo operator-fee rebates).

**Why not deterministically solvable / fix.** For 18 foreign withdrawals of $350 (6/mo × 3 mo) the bank foreign-ATM fee is $0.00 for Green Fee-Free, Purple, and Bluest; all other candidates are strictly worse (Light Blue $48, Evergreen $126, Light Green $162 due to its $150 daily ATM limit forcing 3 sub-withdrawals, Blue/Green-checking $189). open_bank_account_4821 does NOT validate account_class or enforce any minimum-opening-deposit, and opens every account at $0.00 — so Bluest's $75,000 opening-deposit text and Purple's terms impose no tool-enforced eligibility barrier; a competent agent could legitimately open Purple (identical $0 foreign ATM fee plus rebates) or Bluest, yielding a different accounts-table record and failing DB exact match. Fix: give the customer a distinguishing constraint that uniquely selects Green Fee-Free (e.g. no large opening balance and a tie-break that rules out Purple's rebate advantage), or accept any of the $0-fee accounts.

### task_082 — Blocker

**In plain terms.** There's fraud on two of the customer's cards, and the bank's rule (and the customer) says fraud means cancel-and-replace the card. The official answer does this for one card but skips the other, so an agent that correctly handles both is marked wrong.

**Discrepancies (technical).** Gold records CryptoGems (GFF card, card_not_present_fraud) card_action='close_and_reissue' and customer explicitly asks to reissue the GFF card, but gold performs close_debit_card/order_debit_card ONLY for the Blue card — GFF is never closed/reissued, contradicting doc_..._031 "most severe action across all disputes" and the customer request. Also FitLife provisional_credit_eligible=True though recurring_charge_after_cancellation is "NOT required (discretionary)" per doc_..._032.

**Why not deterministically solvable / fix.** This is a DB task; file_debit_card_transaction_dispute_6281 and close/order tools (all WRITE) persist their args/effects verbatim, so every gold value and every card mutation must be uniquely reproduced. (1) BLOCKER: For the Green Fee-Free card the gold filed CryptoGems with card_action='close_and_reissue' (matching the doc_..._031 mapping card_not_present_fraud → close_and_reissue) and the customer in step 7 explicitly says "I'd like to keep using this card but maybe with a new number? Can you reissue it?" — yet the gold trajectory performs close_debit_card_4721 and order_debit_card_5739 ONLY on dbc_mc47a2b9e1_blue, never on dbc_mc47a2b9e1_gff. A competent agent following doc_..._031 ("when performing the actual card action ... use the MOST SEVERE action across all disputes" — GFF's disputes are close_and_reissue + keep_active → close_and_reissue) plus the explicit reissue request would close+reorder the GFF card, writing a CLOSED status + a new debit_card_order that the reference DB lacks → exact table-by-table match fails and the correct agent is mis-graded. (2) The gold is internally inconsistent: it executes the close_and_reissue for the Blue card's fraud dispute but omits the identical mandated action for the GFF card's fraud dispute. Fix: add close_debit_card_4721(card_id="dbc_mc47a2b9e1_gff", reason="fraud_suspected") and order_debit_card_5739 for chk_mc47a2b9e1_gff to the gold (and reconcile FitLife provisional_credit_eligible with doc_..._032's discretionary classification). Secondary defects (not independently blocking): FitLife provisional_credit_eligible=True is a discretionary "not required" category per doc_..._032 (an agent applying the required-criteria literally would set False); and instruction step 8 gives CryptoGems discovery as "January 9th" while step 6/gold use 11/14 (typo, resolvable from "discovered today").

### task_083 — Blocker

**In plain terms.** The dispute tool requires a 'maximum liability amount' field, but the official answer leaves it out. A correct agent must fill it in — and then no longer matches the incomplete official answer, so full marks are impossible.

**Discrepancies (technical).** ACTION-graded with compare_args=None (all args compared incl. the inner arguments JSON by value), but file_debit_card_transaction_dispute_6281 has REQUIRED positional param customer_max_liability_amount (tools.py:933; returns "Error: customer_max_liability_amount is required" if None) which the gold's four call_discoverable_agent_tool arguments strings (083_6..083_9) all OMIT — a correct agent must send it, so its call can never match the gold.

**Why not deterministically solvable / fix.** The tool signature requires customer_max_liability_amount and its docstring documents it (so it is surfaced on unlock — not a hidden arg). A competent agent therefore MUST include it (the tool errors otherwise: e.g. ATM $250→$100 short reported within 2 business days → liability $50). Because evaluation uses compare_args=None, ActionCheck.compare_with_tool_call compares the full outer dict {agent_tool_name, arguments}, and the inner `arguments` value is the literal JSON string; the gold string lacks customer_max_liability_amount while every correct agent string includes it, so tool_args != action_args for all four disputes → reward 0 for a correct agent. Secondary issue: the duplicate-charge gold disputes btxn_d937eaa1d21d (the second of the two identical $67.25 Austin Coffee Roasters charges) while doc _031 says "Dispute the earliest (first) transaction when multiple duplicates exist"; with no timestamp the "first" referent is ambiguous and the gold picks the later-listed id. Fix: regenerate the four gold arguments to include customer_max_liability_amount (50/-1 etc.), and disambiguate the duplicate pick.

### task_084 — Blocker

**In plain terms.** Two identical charges on the same day with nothing to tell them apart. The rule says 'dispute the first one,' but the official answer disputes the second, so an agent has no way to pick the same one. (The liability amount is also calculated inconsistently.)

**Discrepancies (technical).** duplicate-charge tie — doc_..._031 "Dispute the earliest (first) transaction when multiple duplicates exist," but the two identical Bella's Bistro $47.50 11/06 charges have btxn_d7f2a98c1b34 FIRST in DB/tool order and gold disputes the SECOND, btxn_e8c3b09d2c45; also customer_max_liability_amount is internally inconsistent (duplicate uses 50 not min(50,47.50); fraud uses min(500,412.88)=412.88).

**Why not deterministically solvable / fix.** get_bank_account_transactions_9173 returns records in DB insertion order (db_query.py performs no sort, despite doc_..._018 claiming reverse-chronological); btxn_d7f2a98c1b34 precedes btxn_e8c3b09d2c45 in the task's agent_data and shares date 11/06/2025 with no timestamp. A doc-compliant agent disputing "the earliest (first)" picks d7f2a98c1b34, but the gold disputes e8c3b09d2c45, so the stored debit_card_disputes row keys on a different transaction_id and DB exact-match fails. Separately, customer_max_liability_amount (stored in the dispute record and thus part of the table compared) is not uniquely derivable: the docstring says it is "based on Reg E timing rules AND the disputed amount," yet gold caps the TechWorld fraud at the disputed amount (412.88<500) while NOT capping the duplicate at its disputed amount (uses 50 over 47.50). Either rule applied consistently mismatches one of gold's values. Fix: give the duplicates distinct timestamps/ordering so "first" is unambiguous and point gold at the truly-first record, and document a single deterministic liability formula (e.g., always min(timing_cap, disputed_amount)) and make gold obey it.

### task_101 — Blocker

**In plain terms.** The customer wants to refer 4 people. A rule limits how many referral bonuses you can RECEIVE in 9 days, but this customer has received none recently, so the limit doesn't apply. The official answer still submits only 2 referrals as if it did, so an agent that correctly submits all 4 eligible ones is marked wrong.

**Discrepancies (technical).** gold submits only 2 referrals (Purple, Sky Blue) but the 9-day rolling window (doc_..._047) caps RECEIVING BONUSES, not submissions; submit_referral creates NO_PROGRESS records (not bonuses) and the last actual COMPLETE bonus was 10/25 (20d before 11/14), so the window is clear — there is no documented basis to refuse Maya and Ember, both of whom are eligible.

**Why not deterministically solvable / fix.** doc_bank_accounts_..._047 limits "at most 2 referral bonuses in any rolling 9-day window," evaluated on the timestamps of received bonuses. The seeded referral history's most recent COMPLETE bonuses are 10/25 and 10/10 (20 and 35 days before the fixed clock 11/14), so the window is empty, and submit_referral only creates NO_PROGRESS records (the tool sets status NO_PROGRESS, not a bonus), so submitting today triggers no auto-denial. A correct agent therefore has no basis to cap at 2 and should submit all 4 eligible referrals: Maya(19,$300)→Green Fee-Free (cap 4, 0 used; $300 meets the $300 threshold; Light Green is cap-maxed 3/3), Vikram(71,$1,200)→Purple ($1,000 threshold; Gold Years cap-maxed 6/6), Ember(5yr,$18k)→Lime Green ($15k threshold met; Sky Blue's "within 4 years of formation" excludes a 5-year company), TechFlow(2yr,$12k)→Sky Blue (best combined 150+250=$400). Because this is a DB-graded task, an agent that correctly submits 4 (or any pair other than Purple+Sky Blue) writes different referral records and is mis-graded against the 2-record gold. The gold outcome only follows if the agent (per customer instruction 13a) misapplies the rolling-window limit as a live submission cap. Fix: either seed two COMPLETE bonuses within the last 9 days so the window genuinely binds, or revise the gold to submit all 4 eligible referrals (Green Fee-Free, Purple, Lime Green, Sky Blue).

### Majors

### task_017 — Major

**In plain terms.** To find the customer's wrongly-credited rewards, the agent compares each transaction's reward to what it should be. The bank rounds reward points in a way that's never written down, and here the stored numbers don't even match the obvious rounding — so a strict comparison flags extra transactions. It only works if the agent ignores tiny 1-point differences, which no document mentions.

**Discrepancies (technical).** DB-graded cash_back_disputes must match exactly; gold disputes only the 2 GROSS errors (txn_913d14a20dc5 stored 15 vs ~157 @1%; txn_cfabb609133d stored 47 vs ~87 @1%) but NEITHER round-half-up NOR floor reproduces the full set with zero false positives — txn_31fd03682992 (computed 1158 vs stored 1159) is off-by-1 under BOTH conventions and txn_cedd88ce1f65 (219.96 → 220 round vs 219 floor=stored) is a false positive under round-half-up; floor handles cedd88 but not 31fd03.

**Why not deterministically solvable / fix.** Silver Rewards Card earns 4% on Travel/Software and 1% otherwise; points = amount×rate (1pt=$0.01). Computing all 5 of Kenji's txns: e4ed366(450 Travel)=1800=stored ok; 31fd03(289.50 Travel)=1158 but stored 1159; cedd88(54.99 Software)=219.96; 913d14(156.78 Shopping)=156.78 stored 15; cfabb6(87.25 Dining)=87.25 stored 47. The gold set is exactly the two gross discrepancies (~factor-10 and ~half). A literal "dispute every txn where stored≠computed" agent disputes 3-4 txns under either rounding because 31fd03 mismatches by 1 under both round and floor, so neither convention yields the gold set cleanly. The task is only solvable if the agent applies an undocumented "ignore ±1 rounding noise / dispute only material discrepancies" heuristic. Per the primer the gross errors are cleanly separated from noise so a material-discrepancy agent recovers the set, but the convention is unstated and a strict agent mis-grades. Fix: either correct the seed so stored = round(amount×rate) for the non-error txns (set 31fd03=1158, cedd88=220), or document the materiality/rounding rule.

### task_018 — Major

**In plain terms.** Same rounding problem: reward points are stored 'rounded down' with no rule written down, so an agent using normal rounding flags many extra transactions and is marked wrong unless it ignores tiny differences.

**Discrepancies (technical).** Computed both conventions: ONLY FLOOR reproduces the gold set exactly (6 txns, 0 false positives); round-half-up (the natural default) yields 28 disputes = 22 false positives, all +1 rounding noise (e.g. txn_e45e7acb56a0 Amazon $89.99 exp 89.99→90 vs stored 89).

**Why not deterministically solvable / fix.** Across Silver(4%/1%), Crypto(2%), EcoCard(5x/1x), Business Platinum(4%/1.5%) the 6 gold errors are all GROSS (diffs +48 to +1281, e.g. txn_0be1ccc37761 LinkedIn Ads exp 2049 vs stored 768; txn_e647e242ce96 Google Ads overpaid exp 750 vs stored 1875) and cleanly separated from ±1 noise. The rounding convention is undocumented and is inconsistent with task_020 (which needs round-half-up), so an agent applying the natural round-half-up with strict reward-equality disputes 28 txns and mismatches the gold DB. Recovery is possible only if the agent disputes "material/gross" discrepancies and ignores ±1 deltas; a literal exact-equality agent fails. Fix: document the floor rounding convention (or define a tolerance, e.g. only flag deltas >1 pt) so the dispute set is uniquely derivable.

### task_019 — Major

**In plain terms.** Same undocumented rounding problem (this task rounds down).

**Discrepancies (technical).** Only FLOOR rounding reproduces the gold set exactly (4 disputes, 0 false positives); round-half-up gives ~9 false positives (e.g. txn_f2a3b4c5d6e7 stored 562 vs rhu 563, txn_a3b4c5d6e7f8 86 vs 87). The 4 gold errors are gross (175 vs 875, 240 vs 600, 600 vs 1000, 775 vs 800).

**Why not deterministically solvable / fix.** Gold (af0581dcbf, Gold Rewards 2.5% = amount×2.5 pts; EcoCard 5pts/$ green, 1/$ other; both accounts >6mo so no promo). Correct rewards computed against stored rewards_earned: under floor the only mismatches are exactly the 4 disputed txns; under round-half-up many honest txns round up and become false positives, so an agent using the natural round-half-up convention would dispute extra transactions → DB mismatch. The rounding convention is undocumented (doc_006 only gives the 1pt=$0.01 conversion). The 4 genuine errors are gross factor-of-N discrepancies cleanly separated from ±1 rounding noise (smallest gap is 775 vs 800 = 25 pts), so an agent disputing only "material" discrepancies still recovers the exact set — which is why this is Major, not Blocker. Fix: document the rounding convention (floor) or pad the seeded reward errors so the natural round-half-up convention also reproduces the set without false positives.

### task_021 — Major

**In plain terms.** Same undocumented rounding problem (rounds down).

**Discrepancies (technical).** FLOOR reproduces the gold set with zero false positives; round-half-up yields 6 false positives (ThredUp 50/51, HBO Max 142/143, Spotify 439/440, Tesla Supercharger 240/241, Patagonia 805/806, DTE 282/283). Gold disputes only the 2 GROSS errors: txn_ccbb948ffa10 Chipotle (stored 184 vs correct 369/370) and txn_5b30a52ac9d6 Everlane (stored 270 vs correct 1352, EcoCard Green 5pt rate mis-stored at 1pt).

**Why not deterministically solvable / fix.** Computed every transaction for user d2e5bc4124 under both conventions. Business Bronze = 1% (excl. WeWork→0, applied correctly), EcoCard = 5pt/$ on Green merchants else 1pt/$ (Tesla Supercharger is a certified network → 5pt, correct at floor). The two gold disputes are gross: Chipotle off by ~185 pts (stored at ~half rate) and Everlane off by 1082 pts (stored at 1x instead of 5x). The rounding convention is undocumented; only floor makes the six ±1 transactions clean, so an agent using the natural round-half-up convention would dispute 8 transactions (6 false positives) and fail the DB exact-match. Because the genuine errors are gross and cleanly separated from the ±1 rounding noise, an agent disputing only "material" discrepancies (the customer literally asks to separate "actual errors versus legitimate policy differences") can still recover the exact set — so the task is solvable but fragile. Fix: document the floor/truncation rounding convention in the rewards KB article, or store the seed rewards with the natural round-half-up values so the natural convention reproduces the set.

### task_022 — Major

**In plain terms.** Same undocumented rounding problem (rounds down), across many transactions and four cards.

**Discrepancies (technical).** Only FLOOR (truncation) reproduces the gold set EXACTLY (10 disputes, 0 FP, 0 FN); round-half-up yields 26 false positives — all pure +1 noise on $0.005-tail amounts. Seed stores floor(amount×rate); the gold 10 are all GROSS errors (factor-of-N, 300-16,000 pts off). Rounding convention undocumented.

**Why not deterministically solvable / fix.** I pulled all 77 transactions for user f9bf8de0be and computed expected rewards per the documented rates (Diamond 5%, Business Platinum 4% travel/software/media else 1.5%, Business Silver 10% travel/software else 1% with merchant exclusions, EcoCard 5/$ green else 1/$ with exclusions), 1 pt = $0.01. Under FLOOR every non-error stored value equals floor(expected) and exactly the 10 gold transactions deviate (e.g. txn_ffeede5eeacd Dell-Software stored 18499 vs correct 1849 after the exclusion; txn_ba8b473f295d "Target - Eco Collection" stored 728 at 5x vs correct 145 at 1x). Under round-half-up, 26 correctly-credited transactions become false positives purely because halfup(x.5+)=floor+1 (e.g. amt 487.50 Diamond stored 2437 = floor(2437.5), halfup=2438). So an agent that naively uses the natural round-half-up convention over-disputes 26 transactions and fails the DB exact match; only the non-natural FLOOR convention (or a "material discrepancy only" heuristic) recovers the gold set. Because the 10 genuine errors are cleanly separated from the +-1 rounding noise, a careful agent disputing only material (factor-of-N) discrepancies recovers exactly the gold set, which is why this is Major rather than Blocker. Fix: document the truncation/floor rounding convention (or instruct disputing only material discrepancies) so the dispute boundary is deterministic.

### task_025 — Major

**In plain terms.** Which card is 'best' depends on whether 'Apple Music' counts as a blocked 'Apple' purchase on one card and a rewarded 'media' purchase on another — a judgment call that's never spelled out. Reading it the other way flips the winner by 10x.

**Discrepancies (technical).** Gold picks Business Platinum (4% media/software = $4,000) over Business Silver (10% = $10,000); this is only correct if "Apple Music" is mapped to the excluded "Apple" merchant in Silver doc_..._005 ("Hardware/Electronics ... Apple") AND simultaneously qualifies for Platinum's 4% "Travel, software, and media advertising" (doc_..._002) — a non-obvious merchant-substring inference that flips a 10x answer.

**Why not deterministically solvable / fix.** The decisive non-determinism: a competent agent reading doc_..._002 ("Earning 4% Cash Back": "Travel, software, and media advertising purchases earn 4.0%") could plausibly treat Apple Music as a consumer-media subscription that is NOT in Platinum's stated qualifying examples (airfare, hotels, SaaS, cloud hosting, digital ad placements) → Platinum drops to 1.5% = $1,500, tying/losing to Bronze ($1,000 + $500 promo = $1,500). Conversely, if the agent treats Apple Music as "software" and does NOT apply the Silver "Apple" exclusion, Silver pays 10% = $10,000 and clearly wins, making the gold (Platinum) wrong. The intended path (Silver excludes "Apple"; Platinum earns 4% on media with no exclusion list) is internally consistent and matches the primer's "Microsoft 365 -> Microsoft" exclusion-mapping note, but it rests on two simultaneous fragile reads that an equally-reasonable agent can get wrong in opposite directions. Fix: make the customer's purchase unambiguously a Platinum-only category (e.g., a clearly-SaaS vendor) or have the Silver exclusion doc explicitly name "Apple Music," and confirm Platinum's media category includes consumer streaming.

### task_029 — Major

**In plain terms.** Same undocumented rounding problem (rounds down).

**Discrepancies (technical).** Only FLOOR rounding reproduces the gold dispute set exactly (6 txns, 0 false positives); round-half-up (the natural default) yields 22 false positives. The 6 gold errors are all GROSS (factor-of-N: e.g. txn_e647e242ce96 stored 1875 vs correct 750; txn_896ac64b98d7 stored 128 vs 642; txn_adea68821a1d stored 167 vs 669).

**Why not deterministically solvable / fix.** Computing correct rewards over all 47 of user 890389b165's credit-card transactions (Silver 4% travel/software else 1%, BizPlat 4% travel/software/media else 1.5%, Crypto 2%, EcoCard 5pt/$ green else 1pt/$): under FLOOR, stored ≠ floor for EXACTLY the 6 gold transactions and no others; under round-half-up, 28 transactions mismatch (22 extra +1-noise false positives beyond the gold 6). The rounding convention is undocumented, and the agent must therefore guess FLOOR or it will dispute 22 extra transactions and fail the exact-DB match. Mitigant: every gold error is grossly off (2x-5x), cleanly separated from the ±1 round-half-up noise, so an agent that disputes only "material" discrepancies recovers the exact set without knowing the convention. Net: fragile on the natural convention but recoverable via material-threshold reasoning → Major. Concrete fix: document the FLOOR (truncation) rounding convention for points in the cash-back-dispute KB article, or re-seed rewards_earned consistent with round-half-up. (Phase 2 deception handled correctly: disputes are unresolved — auto_resolve_disputes=false — so gold rightly omits any update_transaction_rewards_3847 call.)

### task_073 — Major

**In plain terms.** The official refund needs several non-obvious leaps: treating fees charged at the bank's OWN ATMs as mistakes, voiding a duplicate fee, and canceling an overcharge against a separate undercharge. An agent that simply refunds the overcharges gets a different total.

**Discrepancies (technical).** round-half/floor irrelevant (all fees exact); gold nets reproduce ONLY if agent treats in-network RHO-BANK ATM fees as errors AND nets an undercharge against overcharges — Blue=$9.50 (WELLS +$1.50, SHINHAN +$5, RHO-BANK 11/13 +$3), Green=$9.00 (RHO-BANK 11/07 +$3, WOORI +$3, duplicate 11/15 +$3), Light Green=$1.50 (KB Kookmin foreign +$1.50, plus 11/03 overcharge +$1.50 offset by 11/17 undercharge -$1.50).

**Why not deterministically solvable / fix.** The three gold credits ($9.50/$9.00/$1.50) are exactly reconstructable but only under three non-obvious inferences. (1) Fees posted on RHO-BANK (in-network) ATM withdrawals — line items literally read "NON-RHO ATM FEE" on a Rho-Bank ATM (Blue 11/13 $3, Green 11/07 $3) — must be treated as erroneous; without this Blue=$6.50 and Green=$6.00, missing gold. (2) The Green 11/15 account has two separate $3 "NON-RHO ATM FEE" rows for one $250 withdrawal; the second must be voided. (3) Light Green nets to $1.50 via offsetting domestic discrepancies: 11/03 ($1.50 charged on the 2nd of 4 free monthly withdrawals — should be $0) is cancelled by 11/17 ($0 charged on a 5th paid withdrawal — should be $1.50), leaving only the KB Kookmin foreign overcharge (charged $5 on a $150 withdrawal that is tier-2 $3.50, +$1.50). An agent that refunds only overcharges and ignores the 11/17 undercharge gets $3.00, not $1.50. doc_..._017 does mandate "the net correction across all identified fee discrepancies," which saves a careful agent, so the task is deterministically solvable; but the in-network-fee inference plus the offsetting under/overcharge make it fragile and easy to mis-credit. Fix: add seed-level consistency (don't post NON-RHO fees on Rho-Bank ATMs; correctly label/charge the Light Green free-allowance) or document explicitly that in-network ATM fees are always erroneous and that undercharges net against overcharges.

### task_095 — Major

**In plain terms.** The documents contradict each other about whether a small +0.025% bonus stacks on top of the other bonuses, so the 'correct' interest figure isn't the only reasonable one.

**Discrepancies (technical).** Gold expected_apy 6.85 = base 5.5 + highest cc bonus 0.6 (EcoCard, stacking doc _045) + highest checking boost 0.75 (Green, selection doc _046), treating the doc_013 "0.025% Gold Rewards Card relationship bonus" as identical to the doc_014 cc-bonus (subsumed/lost to EcoCard); but doc_savings_accounts_gold_account_013 frames that 0.025% as a SEPARATE additive "relationship bonus APY on top of the base 5.5%", so an agent could compute 7.025 → credit $112 instead of the gold $98, causing a DB mismatch.

**Why not deterministically solvable / fix.** All non-relationship components are consistent: actual 5.625 = 5.5 + 0.025 (wrong cc, Gold Rewards) + 0.1 (wrong checking, Purple); expected swaps to the correct highest values 0.6 + 0.75 → 6.85, diff on $96k = $98.00. The ambiguity is solely the 0.025% Gold-Rewards-Card relationship bonus: doc_013 ("you receive an additional 0.025% relationship bonus APY on top of the base rate") reads as a standalone stackable bonus exactly like the Silver doc_002 bonus that task_093 DID add on top. The gold instead treats it as the same line item as the doc_014 credit-card bonus and lets EcoCard's 0.6 win, dropping it. A reasonable agent adding it separately gets expected_apy 7.025 and credit $112, and the apply_savings_account_credit amount + report expected_apy both diverge from gold → mis-grade. Fix: clarify whether the Gold Rewards Card 0.025% is a credit-card APY bonus (subject to highest-only stacking) or a separate relationship bonus, and make doc_013 vs doc_014 non-overlapping.

### task_097 — Major

**In plain terms.** Same +0.025% bonus confusion — and it's handled inconsistently with a near-identical task (task_093) that DOES include it, so the official figure here is doubtful.

**Discrepancies (technical).** Silver expected_apy 6.65 = 4.0 tier + 0.45 (Bluest→Silver checking boost) + 2.2 (EcoCard highest cc bonus) OMITS the +0.025% relationship-bonus that doc_savings_accounts_silver_account_002 (a required doc here) says applies for "multiple Rho-Bank products" — yet task_093's Silver gold INCLUDED that same 0.025; a doc-following agent computes 6.675 → credit $222.92 vs the gold $220.84, mismatching the DB credit and report expected_apy.

**Why not deterministically solvable / fix.** Platinum (7.65 = 6.5 + 0.8 Blue checking + 0.35 Diamond cc), Diamond Elite (8.2 = 7.5 + 0.2 Light Green checking + 0.5 Diamond cc), and Silver Plus (5.3 = 4.5 tier2 + 0.35 Blue checking + 0.45 EcoCard cc) are all internally consistent under base/tier + highest checking boost + highest cc bonus, with no relationship or direct-deposit bonus. The defect is the Silver account: doc_002 (present in required_documents) explicitly grants a stackable 0.025% relationship bonus for holding multiple products, and this customer holds many; the gold drops it (6.65, $220.84) while the structurally identical task_093 applied it (4.275). Within task_097 an agent following its own supplied doc_002 computes Silver expected_apy 6.675 and credit $222.92, mismatching the gold apply_savings_account_credit and submit_interest_discrepancy_report on the Silver account → DB mis-grade. Fix: apply the 0.025% relationship bonus consistently (either add it to task_097 Silver, matching task_093, or remove it from doc_002/task_093) so the convention is deterministic.

### task_102 — Major

**In plain terms.** The customer wants the referral that pays the biggest bonus, but the documents include an account that pays more than the official answer's pick, so a careful agent reasonably chooses the higher-paying one and is marked wrong.

**Discrepancies (technical).** Rolling 9-day window correctly allows only ONE new referral now (only ref_recent_purple_001 on 11/10 is within 9 days of 11/14), but the customer's explicit goal is "maximize the bonus" and the gold's TechFlow→Sky Blue ($150) is NOT the max: Ember Analytics ($18,000 deposit, 5yr) qualifies for Lime Green Business Checking at $200 (doc_..._lime_green_003: $15k deposit, 90-day tenure met, cap 12 with only 2 used), strictly beating Sky Blue.

**Why not deterministically solvable / fix.** Referral counts from the seed are Gold Years 6/6 (FULL → Vikram cannot be referred there), Sky Blue 7/8 (room), Lime Green 2/12 (room). After the agent corrects the customer, Ember is ~5 years old → fails Sky Blue's "within 4 years of formation" but has no documented age cap for Lime Green/Hunter Green/Cobalt Blue and deposits $18,000 ≥ Lime Green's $15,000, qualifying for the $200 bonus. Even TechFlow ($12,000) would earn $175 via Hunter Green (deposit $10,000 met) over Sky Blue's $150. Since the customer states "which one should I prioritize? I want to maximize the bonus," a competent agent maximizing the bonus would recommend Ember→Lime Green Account ($200), and submit_referral would write account_type="Lime Green Account" instead of the gold's "Sky Blue Account" → DB exact-match fails. The task is reachable only by anchoring on the "startup→Sky Blue" framing rather than the explicit maximize-bonus instruction, so the gold is non-unique. Fix: drop the "maximize the bonus" wording (or make Sky Blue uniquely the highest eligible bonus), or accept the higher-bonus Lime Green referral as gold.
