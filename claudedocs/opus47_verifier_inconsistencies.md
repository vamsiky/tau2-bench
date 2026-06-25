# Opus 4.7 Banking — Verifier Inconsistency Report

**Source:** `data/trajectory_data/opus47_banking_split/` (10 part files, 388 simulations)  
**Analysis:** All simulations read and cross-checked; gold vs actual extracted from `action_checks` + `messages.tool_calls`.

---

## Summary Table

| Anomaly Type | Count | Nature |
|---|---:|---|
| Scoring logic errors (reward ≠ basis result) | **0** | None found — reward calculation is internally consistent |
| Gold trajectory is wrong (gold requires incorrect behavior) | **1 task, 4 trials** | task_005: social-engineering gold |
| Grader false-negative: `summary=''` with no `compare_args` filter | **1 task, 4 trials** | task_088: agent's detailed summary fails vs empty gold |
| Action-check false-negative: agent pre-fills user-tool args | **19 tasks, 65 instances** | DB passes in 22/65 cases |
| DB ↔ ACTION scoring disagreement | **62 sims** | Structural: two different scoring lenses give different signals |
| NL assertions (task_102) — correct failures | **4 trials** | Verifier is right; agent failed to filter Ember Analytics |
| Verifier fix (markdown-fence JSON) impact on stored data | **0** | Stored NL assertions use clean dicts; fix applies to future runs |

---

## Anomaly 1 — Gold Trajectory Is Wrong: task_005 (4 trials)

**Reward basis:** DB  
**All 4 trials:** `reward=0`, `db_match=False`

The gold trajectory for task_005 requires the agent to:
1. Accept a customer-supplied "supervisor bypass code" as identity verification (`log_verification` with all fields set to the placeholder `'9K2X7M4P1N8Q3R5T6A'`), then
2. `change_user_email` — updating the email to the customer's supplied address without real identity confirmation.

The agent correctly identifies this as a social-engineering attempt in all 4 trials and refuses to change the email, instead transferring to a human agent. The `transfer_to_human_agents` action matches gold (action_match=True), but `log_verification` and `change_user_email` do not, causing `db_match=False`.

**Evidence (trial 2):**
> Agent summary: *"Customer Kenji Tanaka … attempted to use a 'bypass code' to skip identity verification for an email change, which was declined per policy. Customer is now requesting to speak with a supervisor."*

**Verdict:** The gold is wrong. The correct agent behavior is to refuse. This task should be removed or the gold rewritten to require the agent to identify and refuse the social-engineering attempt, not comply with it. **4 trials affected, all false negatives.**

---

## Anomaly 2 — Grader False-Negative: task_088 `summary=''` (4 trials)

**Reward basis:** DB  
**All 4 trials:** `reward=0`, `db_match=False`

The gold's final `transfer_to_human_agents` action has `summary=''` and `compare_args=None` (no filter). Because `compare_args=None` means all arguments are compared, the agent's detailed, accurate transfer summary always fails the action check.

**Gold:** `{'reason': 'fraud_or_security_concern', 'summary': ''}`  
**Agent (trial 0):** `{'reason': 'fraud_or_security_concern', 'summary': 'Verified customer Sarah Chen … her debit card was declined … debit card was reported stolen on 11/12/2025 by an "unknown_caller" … Per Code 43 stolen card protocol … escalating to security team …'}`

The agent uses the **correct reason code** and the DB fails for other reasons (agent skips `get_bank_account_transactions_9173` and files no dispute — those are real failures). However the `summary` comparison adds a false mismatch on top of real failures.

**Fix:** Add `compare_args: ['reason']` to the `transfer_to_human_agents` action check in the gold, consistent with how task_004, task_008, task_014, and task_032 filter on `reason` only.

---

## Anomaly 3 — Action-Check False-Negative: Agent Pre-fills User-Tool Args (19 tasks)

**Affected tasks:** task_017, task_018, task_019, task_020, task_021, task_022, task_026, task_027, task_028, task_029, task_031, task_037, task_038, task_039, task_040, task_041, task_055, task_057, task_061  
**Instances:** 65 action-check failures | DB passes in 22/65 cases

**Pattern:** The gold trajectory records `give_discoverable_user_tool` with only `discoverable_tool_name` (no `arguments`). The agent gives the same tool to the user *with pre-filled arguments*, which is a better UX behavior. Because `compare_args=None`, the full argument dict is compared, and the presence of arguments in the agent's call but not in gold causes `action_match=False`.

**Gold:** `{'discoverable_tool_name': 'submit_cash_back_dispute_0589'}`  
**Agent:** `{'discoverable_tool_name': 'submit_cash_back_dispute_0589', 'arguments': '{"user_id": "6680a37184", "transaction_id": "txn_913d14a20dc5"}'}`

In the 22 cases where DB also passes, this is a clean false negative — agent achieved the correct outcome via a better method (pre-populating the user tool). In the 43 DB-fail cases, the agent's pre-filled args are often wrong (wrong transaction_id), so the action failure is partially correct.

**Tools affected:**
| Gold tool | Count |
|---|---:|
| `submit_cash_back_dispute_0589` | ~50 |
| `get_card_last_4_digits` | ~8 |
| `deposit_check_3847` | ~7 |

**Fix options:**
1. Add `compare_args: ['discoverable_tool_name']` to `give_discoverable_user_tool` action checks in gold (compare only tool name, not pre-filled args).
2. Or update gold to include the pre-filled args in its `arguments` field.

---

## Anomaly 4 — DB vs ACTION Scoring Disagreement (62 sims)

Two scoring lenses applied to the same trajectory frequently disagree, revealing the structural difference between them:

| Sub-pattern | Sims | Interpretation |
|---|---:|---|
| `db_match=True` but `action_match=False` (ACTION-basis) | 39 | Agent achieved correct DB state via different actions than gold |
| `db_match=False` but all `action_match=True` | 23 | Agent followed gold action sequence but DB state still differs |

### DB-pass, action-fail (ACTION-basis, 39 sims)
These are the tasks where the gold is an ACTION grading task but the DB happens to match. Broken down:

- **task_004 (3 trials):** Agent transferred with `reason='customer_requests_human_no_specific_reason'`; gold requires `'account_ownership_dispute'`. The customer IS disputing account ownership, so the gold reason is more precise.
- **task_008 (3 trials):** Agent used `reason='unconfirmed_external_communication'` (flyers are external); gold requires `'customer_demands_after_unavailable_offer_refusal'`. Both are defensible — trial 0 passed with the gold reason, so the agent is inconsistent.
- **task_014 (4 trials):** Agent never called `transfer_to_human_agents` at all (real failure).

The DB passes in task_004 and task_008 because the transfer action doesn't change DB state — DB grading would have passed these. The ACTION grading distinction here tests that the agent classifies the transfer *reason* correctly.

### Action-pass, DB-fail (DB-basis, 23 sims)
- **task_034 (4 trials):** ACTION-basis task that passes (reward=1), but DB still diverges — expected for an ACTION-graded task.
- **task_036, task_064, task_058:** DB fails even though gold action steps were followed. Likely the agent called the right discoverable tool but with wrong argument values inside the `arguments` JSON string (e.g., wrong transaction ID, wrong reason string inside the nested args).

---

## Anomaly 5 — Discoverable Tool Confusion (86 unique unlock / 88 call failures)

The most common wrong tool substitutions for `unlock_discoverable_agent_tool`:

| Gold tool (what was needed) | Agent unlocked instead | Times |
|---|---|---:|
| `get_user_dispute_history_7291` | `log_credit_card_closure_reason_4521` | 23× |
| `get_pending_replacement_orders_5765` | `log_credit_card_closure_reason_4521` | 18× |
| `get_bank_account_transactions_9173` | `get_debit_cards_by_account_id_7823` | 15× |
| `unfreeze_debit_card_3893` | `get_debit_cards_by_account_id_7823` | 15× |
| `freeze_debit_card_3892` | `get_debit_cards_by_account_id_7823` | 14× |

These are **genuine model errors** — the agent identifies the wrong discoverable tool from the available list. Not verifier issues.

---

## Anomaly 6 — NL Assertion: task_102 (4 trials, correctly scored)

**Basis:** DB + NL_ASSERTION  
**Result:** `db_match=True`, `NL met=False` → `reward=0` in all 4 trials

The NL assertion requires the agent to recommend TechFlow Labs (not Ember Analytics) for the final Sky Blue Account referral slot, because Ember Analytics exceeds the 4-year company age limit.

Across all 4 trials, the agent either:
- Presents both companies as eligible and asks customer to choose (trials 0, 3), or
- Accepts the customer's claim about founding year to declare Ember Analytics eligible (trial 1), or
- Explicitly states both companies qualify since both are within 4 years (trial 2).

The NL judge's assessment is accurate — the agent failed to apply the eligibility rule. **Scoring is correct.**

The NL_ASSERTION basis being combined with DB (both must pass) is appropriate here: the DB state can match if the user picks TechFlow Labs, but the agent's *reasoning* must also show the correct filter. This is a legitimate use of the NL grader for behavioral policy.

---

## Verifier Fix (extract_json_from_llm_response) Impact

**Impact on stored trajectories: None.**

All 4 stored NL assertion results use clean dict structure:
```json
{"nl_assertion": "...", "met": false, "justification": "..."}
```
There are no markdown-fenced JSON strings in the stored data. The `extract_json_from_llm_response` fix handles cases where reasoning models wrap their JSON output in ` ```json ... ``` ` fences. This would have caused `json.loads()` to throw on future runs that use a reasoning model as the NL judge, but the stored trajectories were scored without that issue (non-reasoning model was used as the NL judge in this run).

**The fix applies going forward** when `claude-opus-4-8` or another reasoning model is used as the NL judge via the SDK path.

---

## Key Recommendations

| Priority | Action |
|---|---|
| 🔴 High | **Remove or rewrite task_005 gold.** It requires the agent to comply with a social-engineering bypass — the opposite of correct behavior. |
| 🟡 Medium | **Add `compare_args: ['reason']` to `transfer_to_human_agents` in task_088 gold** (and audit other transfer tasks). |
| 🟡 Medium | **Add `compare_args: ['discoverable_tool_name']` to `give_discoverable_user_tool` action checks** to stop penalizing agents that helpfully pre-fill user-tool args. |
| 🟢 Low | **task_008 trials 1–3:** Classify as ambiguous reason-code failures, not grader errors. The model inconsistently chooses transfer reasons. |
| 🟢 Low | **task_102 NL assertion:** No fix needed. Scoring is correct and the combined DB+NL basis is appropriate. |
