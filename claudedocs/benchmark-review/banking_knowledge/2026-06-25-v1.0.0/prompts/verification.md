# Prompt — Verification ("second check") of the Banking Benchmark Correctness Review

> Run with a strong reasoning model at maximum effort, **ideally in a fresh session (or a different
> model) than the one that produced the review**, so the check is independent. Verify every load-bearing
> claim against primary sources (code, documents, `db.json`) — do **not** trust the review's prose.
> Cite exact evidence (file:line, doc id + quoted text, DB field path) for every verdict.

---

You are an independent verifier. A prior audit produced
`claudedocs/banking_benchmark_review.md`, which judges whether each of the 97 tasks in the
tau2-bench `banking_knowledge` domain is well-posed and deterministically solvable. **Your job is to
audit that audit** — confirm or refute its findings, catch errors in *both* directions
(false positives = a defect claimed that isn't real; false negatives = a real defect it missed or
under-rated), and check that its corrections and systemic claims actually hold against the source.

Assume the review may be wrong. A finding is "confirmed" only when you have independently reproduced
its evidence from primary sources.

## Materials

- The review under test: `claudedocs/banking_benchmark_review.md` (summary, systemic issues,
  methodology + "verifier corrections", a 97-row table, and detailed findings for every task rated
  ≥ Major).
- Tasks: `data/tau2/domains/banking_knowledge/tasks.json` (each task: `user_scenario.instructions`,
  `evaluation_criteria.{actions,communicate_info,reward_basis}`, `required_documents`, `initial_state`).
- Knowledge base: `data/tau2/domains/banking_knowledge/documents/<doc_id>.json` (the file name is the
  doc id; `.content` is the policy text).
- Database (the seed the gold is replayed against): `data/tau2/domains/banking_knowledge/db.json`.
- Domain code: `src/tau2/domains/banking_knowledge/tools.py`, `utils.py`, `environment.py`,
  `retrieval*.py`; evaluators in `src/tau2/evaluator/evaluator_env.py`, `evaluator_action.py`, and
  `Action.compare_with_tool_call` in `src/tau2/data_model/tasks.py`.

## Step 0 — Independently verify the load-bearing facts the review rests on

The review's verdicts depend on a handful of code/data facts. **Confirm each against the cited source
and report any that are wrong** — if one of these is false, every finding that relies on it is suspect.

1. **DB grading replays the gold and compares exactly.** Check `evaluator_env.py`: gold actions are
   executed to build a reference DB; the agent's DB must match table-by-table; the "verified" scorer
   only (a) lets the agent have a *superset* of gold's `agent_discoverable_tools` and (b) strips
   `closure_reason` (`_FREE_TEXT_ANNOTATION_FIELDS`). Confirm nothing else is relaxed. → This is why
   "every DB-written gold argument must be uniquely derivable" is the correct test.
2. **ACTION grading.** Check `Action.compare_with_tool_call` (`data_model/tasks.py`): with
   `compare_args=None` it compares all args present in the agent's call; otherwise only `compare_args`.
3. **Fixed clock.** `utils.py get_now()` → `datetime(2025,11,14,3,40,0)`; `tools.py get_current_time`
   returns `"... 2025-11-14 03:40:00 EST"`. → timestamps are deterministic; the review should *not*
   flag them as non-deterministic. Verify it doesn't.
4. **Always-on agent read tools (the review's central correction).** In `tools.py`, class
   `KnowledgeTools` (~line 323) defines non-discoverable `@is_tool(ToolType.READ)` methods including
   `get_credit_card_transactions_by_user` (~445), `get_credit_card_accounts_by_user` (~456),
   `get_user_information_by_{id,name,email}` (~383–410), `get_referrals_by_user` (~434). Confirm these
   are NOT decorated `@is_discoverable_tool` and that every retrieval variant inherits `KnowledgeTools`
   (`retrieval_toolkits.py`). Confirm the asymmetry: bank/debit enumeration
   `get_bank_account_transactions_9173` (~2934) and other numeric-suffixed tools ARE discoverable
   (`@is_discoverable_tool`) and so must be named in a task's `required_documents`. Confirm at least one
   gold trajectory calls an always-on read tool without unlocking it (e.g. `get_credit_card_accounts_by_user`
   in task_078/079, `get_referrals_by_user` in task_098–102).
5. **`apply_for_credit_card` is a USER tool** (class `KnowledgeUserTools`, ~4055) and its DB record id
   derives from `(card_type, customer_name, annual_income, rho_bank_subscription)`; `card_type` must be
   one of `VALID_CREDIT_CARD_TYPES` (~4308). Confirm.
6. **`credit_card_transaction_history` schema** in `db.json` (fields: `transaction_id`, `user_id`,
   `credit_card_type`, `merchant_name`, `transaction_amount`, `transaction_date`, `category`, `status`,
   `rewards_earned`) and **`rewards_earned` is stored floor-truncated** to whole points. This underpins
   the review's #1 systemic issue — verify the rounding by recomputation (Step 2).

## Step 1 — Verify EVERY Blocker (mandatory, exhaustive)

For each of the 8 Blockers in the review (currently task_027, 039, 063, 074, 075, 084, 088, 097),
reconstruct the argument from primary sources and assign a verdict. In particular:

- **task_088** — confirm a document named/needed for `provisional_credit_eligible`
  ("Debit Card Provisional Credit Guidelines") is genuinely *absent* from that task's
  `required_documents`, and that the debit enumeration tool is discoverable (so the always-on
  correction does not apply). Contrast task_037 (its guidelines doc IS present).
- **task_074** — confirm the seeded ATM-fee transactions for the task's user include dates AFTER
  2025-11-14, and that no single documented fee rule reproduces the four gold credit amounts.
- **task_063 / task_075** — confirm the claimed *tie* (two products equal on the deciding attribute,
  both eligible, no documented tie-breaker) by reading both product docs and the customer's constraints.
- **task_084** — confirm `customer_max_liability_amount` is passed in the gold but is NOT in the
  documented argument list of `file_debit_card_transaction_dispute_6281`; and that the two duplicate
  charges are indistinguishable on documented fields.
- **task_039 / task_097 / task_027** — confirm the cited rule/omission/missing-doc against the task's
  actual `required_documents` and gold.

Verdict per Blocker: **Confirmed Blocker / Overturned (with corrected severity) / Adjust**.

## Step 2 — Stress-test the 6 "verifier corrections" (highest-risk: the review may have OVER-corrected)

The review downgraded 6 reviewer-Blockers using the always-on-tool argument: task_031, 037, 041 → Minor;
task_019, 026, 029 → Major. For each, decide whether the downgrade is justified or whether a real defect
was waved away.

- For **task_031/037/041**: confirm the gold's `transaction_id`s (and dates, account_ids) actually
  appear in `db.json` for that user and are recoverable by matching the customer-described
  merchant/amount via `get_credit_card_transactions_by_user` / `get_credit_card_accounts_by_user`. If a
  gold value cannot be matched to a unique DB row from what the customer says, the downgrade is wrong.
- For **task_026 (do this computation yourself)**: load `db.json`, take the task's user, list all their
  `credit_card_transaction_history` rows, and compute expected rewards from the task's `required_documents`
  rates (Business Silver 10% travel/software else 1%, with the documented 2×-first-6-months promo keyed to
  `date_of_account_open` from `credit_card_accounts`, plus the merchant-exclusion list; Silver Rewards 4%
  else 1%; 1 point = $0.01). Using **floor** truncation, check that **exactly** the gold-disputed set is
  mis-credited and the gold corrected values reproduce. Then check what a **round()**-based agent would
  flag. Report whether the review's claims ("exactly 4 under floor; round() over-disputes; rounding is
  undocumented") hold. Confirm the promo doc is present for task_026 but ABSENT for task_027.
- For **task_019/029**: confirm the residual defect (undocumented floor-rounding / no material-discrepancy
  threshold) is real and that the enumeration tool genuinely removes the "no tool" Blocker.

Verdict per task: **Downgrade justified / Should remain Blocker / Different severity** + evidence.

## Step 3 — Re-derive a sample of Majors (≥ 8, spread across the systemic clusters)

Independently re-derive at least one Major from each systemic cluster and confirm/refute it:
floor-rounding (018/020/022), provisional-credit cap (040/082), APY relationship-bonus (094/095/096),
DB-keyed selection non-uniqueness (067/076/100/102), undocumented tool arg (087),
card→tier mapping gap (050), customer-vs-DB contradiction (091), omitted authorized action (061),
replacement `expedited_shipping` consent (038). For each, verify the quoted doc text / DB value / gold
arg actually exists and supports the claim.

## Step 4 — False-negative sweep (the review's blind spot)

The 36 "None"/clean tasks and the 29 "Minor" tasks received the least scrutiny. Independently audit a
sample of **at least 12** of them (mix of None and Minor), applying the same skeptical procedure used
for flagged tasks. Specifically look for: a DB-written gold argument that isn't uniquely derivable; a
"best/unique" selection that is actually a tie; a needed rule/threshold absent from `required_documents`;
a gold value that contradicts the customer instructions or the seeded DB. Report any task that should be
upgraded, with evidence.

## Step 5 — Internal consistency & evidence-integrity checks

- The summary counts (8/24/29/36) equal the per-task table tallies, and every task rated ≥ Major in the
  table has a detailed-findings entry (and vice versa).
- Severity calibration is consistent across tasks (same defect class → same severity, unless a stated
  reason differs). Flag inconsistencies (e.g., one "single documented option" task = Minor, an
  equivalent one = Major).
- Spot-check 10–15 quoted evidence items (doc ids, dollar values, arg names, line refs) against the
  actual files for **hallucinations or misquotes**. Any fabricated/incorrect citation is a serious finding.
- Confirm the review did not silently rely on outside banking knowledge to "rescue" or condemn a task.

## Output

Write `claudedocs/banking_benchmark_review_verification.md` containing:

1. **Verdict summary** — counts of findings Confirmed / Overturned / Severity-adjusted / Unverifiable;
   the net corrected severity tally if you change anything; and your overall confidence in the review.
2. **Step-0 fact check** — each load-bearing fact: Confirmed / Wrong (+evidence).
3. **Disagreements table** — one row per finding you change, with columns:
   `task_id | review_severity | your_severity | verdict (Confirmed/Overturned/Adjust) | evidence (file:line / doc id + quote / DB path)`.
   Include every Blocker and every verifier-correction you examined, plus any false-negative upgrades.
4. **Detailed write-ups** for each disagreement and for any Blocker/correction you could not reproduce:
   what the review claims, what you found, the exact evidence, and the corrected conclusion.
5. **Methodology-soundness note** — whether the review's grading model, the always-on-tool correction,
   and the systemic clusters are correctly reasoned, plus any blind spots in its method.

Be adversarial and evidence-based. Reproduce before you agree; cite before you disagree. Where the
review is right, say so briefly; spend your effort where it is wrong, unproven, or miscalibrated.
