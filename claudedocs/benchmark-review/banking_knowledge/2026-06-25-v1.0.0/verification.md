# Verification of `banking_benchmark_review.md`

## Verdict summary

I independently checked the review against the evaluator code, banking tools,
`tasks.json`, task-specific `initial_state`, `db.json`, and required-document
content. The review is broadly sound on severity and on the always-on-tool
correction, but it overstates one load-bearing systemic fact: rewards are not
universally stored by floor truncation. In `task_026`, exact floor math creates
many one-point discrepancies, while `round()` identifies exactly the four gold
disputes. The real defect is an undocumented rounding/materiality convention,
not specifically floor truncation.

Finding counts for items I reproduced:

| category | count |
|---|---:|
| Confirmed | 33 |
| Overturned | 0 |
| Severity-adjusted | 0 |
| Evidence/rationale adjusted | 2 |
| Unverifiable | 0 |

Net severity tally remains the review's tally: **8 Blocker / 24 Major / 29
Minor / 36 None**. Overall confidence in the review: **high for severity
outcomes, medium-high for detailed rationales**.

## Step 0 fact check

| fact | verdict | evidence |
|---|---|---|
| DB grading replays gold and compares exactly, except verified scorer relaxes extra `agent_discoverable_tools` and strips `closure_reason`. | Confirmed | `src/tau2/evaluator/evaluator_env.py:151-188` replays gold actions into `gold_environment`; `_verified_db_match` at lines 34-69 only permits gold tool-name subset and skips `agent_discoverable_tools`, after `_strip_free_text` removes only `closure_reason` from `_FREE_TEXT_ANNOTATION_FIELDS` at line 19. |
| ACTION grading uses all agent args when `compare_args=None`; otherwise only listed args. | Confirmed | `src/tau2/data_model/tasks.py:178-195`; line 187 uses `tool_call.arguments.keys()` when `compare_args is None`. |
| Fixed clock is deterministic and not flagged by the review. | Confirmed | `src/tau2/domains/banking_knowledge/utils.py:30-35` returns `datetime(2025, 11, 14, 3, 40, 0)`; `tools.py:374-381` returns `2025-11-14 03:40:00 EST`. I found no review finding treating timestamps as nondeterministic. |
| Always-on read tools exist and are not discoverable; retrieval variants inherit them. | Confirmed | `tools.py:383-467` defines `get_user_information_by_*`, `get_referrals_by_user`, `get_credit_card_transactions_by_user`, and `get_credit_card_accounts_by_user` with `@is_tool(ToolType.READ)`, not `@is_discoverable_tool`. `retrieval_toolkits.py:34-99` composes every toolkit with `KnowledgeTools`. Gold examples: `task_078` calls `get_credit_card_accounts_by_user` directly; `task_098`, `task_099`, `task_101`, `task_102` call `get_referrals_by_user` directly. |
| Debit/bank enumeration is discoverable and must be documented/unlocked. | Confirmed | `tools.py:2933-2934` decorates `get_bank_account_transactions_9173` with `@is_discoverable_tool(ToolType.READ)`. |
| `apply_for_credit_card` is a user-side tool and IDs derive from application inputs; card type is validated. | Confirmed | `KnowledgeUserTools` begins at `tools.py:4055`; `apply_for_credit_card` is at `tools.py:4324-4365`, validates against `VALID_CREDIT_CARD_TYPES` at `tools.py:4308-4322`, and calls `generate_application_id(card_type, customer_name, annual_income, rho_bank_subscription)`. |
| `credit_card_transaction_history` schema and floor-truncated rewards. | **Adjusted** | Schema confirmed from `db.json`: rows contain `transaction_id`, `user_id`, `credit_card_type`, `merchant_name`, `transaction_amount`, `transaction_date`, `category`, `status`, `rewards_earned`. The blanket floor-truncation claim is false/overbroad. For `task_026`, Adobe `$54.99` at 20 points per dollar is `1099.8`; DB stores `1100 points`, i.e. rounded, not floor. Several other Amara rows behave the same. |

## Blockers and verifier corrections

| task_id | review_severity | my_severity | verdict | evidence |
|---|---|---|---|---|
| task_027 | Blocker | Blocker | Confirmed Blocker | Required docs omit `doc_business_credit_cards_business_silver_rewards_card_012` promo; gold disputes `txn_a8f1c2d3e403` as 6300 points, but without promo the documented Business Silver travel rate gives 3150 points, matching DB. |
| task_039 | Blocker | Blocker | Confirmed Blocker | `doc_credit_cards_credit_cards_(general)_015` lists criteria including "not filed more than 2 disputes in past 12 months" but no "max three provisional credits in this batch" cap. Gold marks first three eligible and fourth fraud/amount-eligible dispute ineligible. |
| task_063 | Blocker | Blocker | Confirmed Blocker | `doc_savings_accounts_silver_plus_account_009` gives both Bronze Rewards and Silver Rewards `+0.15%`; both cards have `$0` annual fee and the customer's 700 score meets both. No tie-breaker selects Silver. |
| task_074 | Blocker | Blocker | Confirmed Blocker | Gold credits `27.00`, `8.00`, `4.75`, `3.70`; base DB includes ATM/fee rows dated `11/15`-`11/17` even though fixed today is `2025-11-14`. No posted-to-date fee rule reproduces all four gold credits. |
| task_075 | Blocker | Blocker | Confirmed Blocker | Green Fee-Free has foreign ATM fee `$0.00` (`doc_checking_accounts_green_fee-free_account_005`); Purple also says foreign ATM withdrawal fee `$0.00` and rebates up to `$30` (`doc_checking_accounts_purple_account_001`). Gold picks Green Fee-Free without a documented tie-breaker. |
| task_084 | Blocker | Blocker | Confirmed Blocker | Gold passes `customer_max_liability_amount`; KB doc `doc_bank_accounts_bank_accounts_(general)_031` argument list includes args 1-16 ending with `card_action`, not this field. Initial state has two indistinguishable Bella's Bistro rows (`btxn_d7f2a98c1b34`, `btxn_e8c3b09d2c45`) with same account/date/description/amount/type/status. |
| task_088 | Blocker | Blocker | Confirmed Blocker | Required docs include debit dispute filing doc `031`, but omit `doc_bank_accounts_bank_accounts_(general)_032` "Debit Card Provisional Credit Guidelines"; `031` says `provisional_credit_eligible` must be determined from that guideline. Debit transaction enumeration is discoverable, so always-on correction does not apply. `task_037` does include its credit-card provisional guideline doc. |
| task_097 | Blocker | Blocker | Confirmed Blocker | `doc_savings_accounts_silver_account_002` says Silver may receive `0.025%` relationship bonus; `doc_bank_accounts_bank_accounts_(general)_044` says to calculate base/tier/checking/card/relationship components. Gold Silver expected APY omits the +0.025%. |
| task_031 | Minor | Minor | Downgrade justified | Gold transaction `txn_adea68821a1d` is uniquely in DB for Fatima: Marriott Hotels, `$167.34`, `11/07/2025`, Silver Rewards. Recoverable via always-on `get_credit_card_transactions_by_user`. |
| task_037 | Minor | Minor | Downgrade justified | Gold fraud txns `txn_d3b830f4a2a4` and `txn_da8c64c97f95` uniquely match Electronics Express Miami `$487.99` and GamerZone LA `$299.95`; account ID is recoverable via always-on `get_credit_card_accounts_by_user`; provisional guideline doc is present. |
| task_041 | Minor | Minor | Downgrade justified | All 16 gold transaction IDs map one-to-one by merchant/amount/date in Claire's DB rows; four card account IDs are recoverable via always-on account reader. |
| task_019 | Major | Major | Downgrade justified | The missing-enumeration Blocker premise is wrong because `get_credit_card_transactions_by_user` is always-on. Residual issue remains: no document states a rounding/material discrepancy threshold, and exact reward comparison can produce extra one-point disputes depending rounding. |
| task_026 | Major | Major | **Rationale adjusted** | Downgrade from Blocker is justified by always-on readers and the included Business Silver promo doc. However the review's specific claim that a `round()` agent over-disputes is wrong: with the documented promo/exclusion rules, `round()` flags exactly the four gold txns; exact floor flags many additional one-point rows. |
| task_029 | Major | Major | Downgrade justified | Same always-on reader correction as `task_018`; residual reward math/materiality ambiguity remains, not a missing transaction-list tool. |

## Detailed adjustments

### `task_026`: severity confirmed, rationale corrected

The review claims `task_026` is Major because the gold set is reproducible only
under floor truncation and a `round()`-based agent over-disputes. I recomputed
the task from `db.json` for user `755bcb4d5d` using:

- Business Silver: 10% on travel/software, 1% otherwise
  (`doc_business_credit_cards_business_silver_rewards_card_002`).
- Business Silver merchant exclusions, including Microsoft and Coursera
  (`doc_business_credit_cards_business_silver_rewards_card_005`).
- Business Silver 2x promo for first six months, keyed to account opening date
  (`doc_business_credit_cards_business_silver_rewards_card_012`).
- Silver Rewards: 4% on travel/software (`doc_credit_cards_silver_rewards_card_002`).

The four material mismatches are the gold set:
`txn_a8f1c2d3e403`, `txn_b7e2d4c5f506`,
`txn_a8f1c2d3e410`, `txn_a8f1c2d3e411`, with corrected values
`6300`, `1020`, `3800`, `1500`.

But exact floor also flags one-point rows such as Adobe `$54.99`:
`54.99 * 20 = 1099.8`, floor `1099`, DB `1100`. `round()` flags exactly the
gold four. So the review's "floor is the DB convention" and "round over-disputes"
claims are not reproduced here. The task still has a Major-level defect because
the expected tolerance/materiality rule is undocumented, but the corrected
description should say the gold relies on ignoring one-point rounding noise, not
on floor truncation.

### Step-0 rewards rounding

The review's systemic issue #1 should be narrowed. Some tasks do show one-point
rounding/materiality hazards, but the DB is not uniformly floor-truncated. The
better systemic claim is:

> Credit-card reward dispute tasks require exact transaction selection while the
> policy packet does not specify a rounding convention or material-discrepancy
> threshold. Therefore agents can select different one-point discrepancy sets
> and fail DB/action exact matching.

## Major sample re-derivation

| cluster | task checked | verdict | evidence |
|---|---|---|---|
| Reward rounding/materiality | task_018 / task_029 spot | Confirmed cluster | Always-on transaction reader removes the no-tool objection, but no required doc states rounding/tolerance for points. One-point rows are plausible false positives. |
| Provisional-credit cap | task_040 | Confirmed Major | `doc_credit_cards_credit_cards_(general)_015` uses previous disputes criterion "not filed more than 2 disputes in past 12 months." Gold eligibility flips within an 8-dispute batch without a documented batch-cap rule. |
| APY relationship/card bonus ambiguity | task_094 | Confirmed Major | `doc_savings_accounts_gold_account_013` calls Gold Rewards `+0.025%` a relationship bonus; `doc_savings_accounts_gold_account_014` also lists Gold Rewards Card `+0.025%` as a credit-card APY bonus; `doc_bank_accounts_bank_accounts_(general)_045` says credit-card bonuses do not stack but relationship bonuses do. |
| DB-keyed selection contradiction | task_100 | Confirmed Major | Customer says first account opened "mid-July ... about four months"; initial state says earliest business checking opened `09/10/2025`. Referral tenure depends on earliest account date per `doc_bank_accounts_bank_accounts_(general)_047`. |
| Undocumented tool arg | task_087 | Confirmed Major | Gold debit dispute passes `customer_max_liability_amount=50`; required KB doc `031` omits that argument, although implementation requires/stores it (`tools.py:933`, `tools.py:1071`). |
| Card-to-tier mapping gap | task_050 | Confirmed Major | Gold approves Gold Rewards limit to `$7500` using a tier-dependent max-increase rule. Required docs include tier thresholds but no mapping from "Gold Rewards Card" to Entry/Mid/Premium tier. |
| Customer-vs-DB contradiction | task_091 | Confirmed Major | User script DOB is `09/22/1991`; initial-state user record and gold `log_verification` use `09/22/2001`. DB reward exact-match makes the logged value material. |
| Omitted authorized funding action | task_061 | Confirmed Major | `doc_bank_accounts_bank_accounts_(general)_002` requires asking about opening-deposit funding; customer agrees to transfer the Silver Plus minimum deposit; gold opens Silver Plus but has no `transfer_funds_between_bank_accounts_7291` action for the `$1,000` minimum. |
| Replacement expedited consent | task_038 | Confirmed Major | Gold writes `expedited_shipping=true`; user gives only a work shipping address. `doc_credit_cards_credit_card_replacements_001` says to ask whether expedited shipping is wanted and capture fee acknowledgment if a fee applies. |

## False-negative sweep

I sampled 14 tasks rated None/Minor: `task_001`, `task_004`, `task_005`,
`task_007`, `task_010`, `task_016`, `task_023`, `task_024`, `task_028`,
`task_032`, `task_036`, `task_044`, `task_049`, `task_093`.

No sampled task needed an upgrade. Notes:

- The cosmetic `$` corruption findings in `task_001`, `task_028`, `task_036`,
  and `task_044` are real but non-fatal because the corrupted fields are not
  DB-written arguments or do not change the unique outcome.
- `task_004`, `task_005`, `task_007`, `task_010`, `task_016`, `task_023`,
  `task_024`, and `task_032` had deterministic gold paths under the available
  docs and DB state.
- `task_093` correctly applies the Silver Account `+0.025%` relationship bonus,
  which reinforces that `task_097` is a real omission rather than a general
  interpretation choice.

## Internal consistency and evidence integrity

- The table has 97 rows and tallies exactly **8 Blocker / 24 Major / 29 Minor /
  36 None**.
- Every table row rated Major or Blocker has a matching detailed section, and
  every detailed Major/Blocker section corresponds to a Major/Blocker table row.
- I spot-checked cited doc IDs and values for provisional credit, debit dispute
  args, replacement expedited shipping, CLI tiers, APY stacking, referral
  tenure, and ATM fee docs. I found no fabricated document IDs or invented tool
  names.
- The main evidence-integrity issue is not hallucination but overgeneralization:
  the review repeatedly says "floor truncation" where the source supports the
  broader "undocumented rounding/materiality" problem.
- I found no instance where the review needed outside banking knowledge to make
  a finding. The strongest findings are grounded in required docs, task scripts,
  gold actions, and seeded DB rows.

## Methodology-soundness note

The review's grading model is correct: for DB-reward tasks, the gold trajectory
is replayed and the final DB must match exactly except for the verified-scorer
relaxations. Therefore every DB-written gold argument must be uniquely derivable
from the user's scripted facts, the task's required documents, always-on tools,
and the seed DB/task initial state.

The always-on-tool correction is also correct. Credit-card transaction/account
enumeration and referral enumeration are base `KnowledgeTools` reads, not
discoverable tools; several gold tasks call them without unlocking. The review
properly downgrades earlier "missing read tool" Blockers where these readers
make IDs recoverable.

The blind spot is reward arithmetic. The review treats floor truncation as a
stable DB-wide fact, but `task_026` shows rounded "correct" rows. The benchmark
problem is still real: exact reward-dispute gold requires a hidden tolerance or
materiality convention. Future fixes should document the point rounding rule and
state whether one-point discrepancies should be ignored.
