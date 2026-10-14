# banking_knowledge v1.0.1 — upstream scorer vs verified scorer

Two independent reviews of the same 97 tasks on 2026-10-13, identical prompts, inputs, task batches, and model (claude-opus-5-5, effort high); only the DB scorer differs. 'Repeat' is an earlier same-scorer review (draft-1, unverified, older prompt wording) used to measure run-to-run noise. Reconciliation resolves differences that are not caused by the scorer; any difference left after it is a scorer effect.

## Agreement by stage

| Stage | Tasks with the same severity | Differences |
|---|---|---|
| Noise baseline: repeat (draft-1) vs upstream reviewers (same scorer) | 70/97 | 27 |
| Reviewers: upstream vs verified | 65/97 | 32 |
| After verification: upstream vs verified | 69/97 | 28 |
| After reconciliation: upstream vs verified | 93/97 | 4 |

## What remains after reconciliation

- **task_060**: upstream Major, verified None. The only defect is close_bank_account_7392's optional free-text reason: the gold omits it, so closure_reason gets the hidden default 'Customer requested closure', and no document says what reason to record. Under upstream exact-hash grading, an agent that records a sensible reason fails (no documented default, so Major by calibration). The verified scorer strips closure_reason from every record and no replacement copies it here (bank accounts, not order_debit_card_5739), so the task is clean under that scorer; every other part of the task (product choice, ordering) is derivable in both runs.
- **task_061**: upstream Major, verified None. The only defect is close_bank_account_7392's optional free-text reason: the gold omits it, so closure_reason gets the hidden default 'Customer requested closure', and no document says what reason to record. Under upstream exact-hash grading, an agent that records a sensible reason fails (no documented default, so Major by calibration). The verified scorer strips closure_reason from every record and no replacement copies it here (bank accounts, not order_debit_card_5739), so the task is clean under that scorer; every other part of the task (product choice, ordering) is derivable in both runs.
- **task_062**: upstream Major, verified None. The only defect is close_bank_account_7392's optional free-text reason: the gold omits it, so closure_reason gets the hidden default 'Customer requested closure', and no document says what reason to record. Under upstream exact-hash grading, an agent that records a sensible reason fails (no documented default, so Major by calibration). The verified scorer strips closure_reason from every record and no replacement copies it here (bank accounts, not order_debit_card_5739), so the task is clean under that scorer; every other part of the task (product choice, ordering) is derivable in both runs.
- **task_067**: upstream Major, verified None. The only defect is close_bank_account_7392's optional free-text reason: the gold omits it, so closure_reason gets the hidden default 'Customer requested closure', and no document says what reason to record. Under upstream exact-hash grading, an agent that records a sensible reason fails (no documented default, so Major by calibration). The verified scorer strips closure_reason from every record and no replacement copies it here (bank accounts, not order_debit_card_5739), so the task is clean under that scorer; every other part of the task (product choice, ordering) is derivable in both runs.

## Final severity counts

| Severity | upstream | verified |
|---|---|---|
| Blocker | 11 | 11 |
| Major | 40 | 36 |
| Minor | 25 | 25 |
| None | 21 | 25 |

## Every task

| Task | v1.0.0 | Repeat | upstream reviewer | upstream verified | verified reviewer | verified verified | upstream final | verified final | Why runs differed |
|---|---|---|---|---|---|---|---|---|---|
| task_001 | None | None | None | None | None | None | None | None | - |
| task_002 | None | None | None | None | None | None | None | None | - |
| task_003 | None | None | None | None | None | None | None | None | - |
| task_004 | None | None | None | None | None | None | None | None | - |
| task_005 | None | None | Minor | Minor | Minor | Minor | Minor | Minor | - |
| task_006 | None | Minor | Minor | Minor | Minor | Minor | Minor | Minor | - |
| task_007 | None | None | None | None | None | None | None | None | - |
| task_008 | Minor | None | Minor | Minor | Minor | Minor | Minor | Minor | - |
| task_010 | None | None | Major | Major | Major | Major | Major | Major | - |
| task_012 | None | None | None | None | None | None | None | None | - |
| task_014 | None | Blocker | Blocker | Major | Blocker | Major | Major | Major | - |
| task_015 | None | None | None | None | Minor | None | None | None | - |
| task_016 | Minor | None | Minor | Minor | None | None | Minor | Minor | judgment |
| task_017 | Major | Major | Major | Major | Major | Major | Major | Major | - |
| task_018 | Major | Minor | Minor | Minor | Minor | Minor | Minor | Minor | - |
| task_019 | Major | Minor | Minor | Minor | Minor | Minor | Minor | Minor | - |
| task_020 | Minor | Major | Major | Major | Major | Major | Major | Major | - |
| task_021 | Major | Minor | Minor | Minor | Minor | Minor | Minor | Minor | - |
| task_022 | Major | Minor | Minor | Minor | Minor | Minor | Minor | Minor | - |
| task_023 | Minor | Minor | Minor | Minor | Minor | Minor | Minor | Minor | - |
| task_024 | None | Major | Major | Major | Major | Major | Major | Major | - |
| task_025 | Major | Major | Major | Major | Major | Major | Major | Major | - |
| task_026 | Minor | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | none (already agreed) |
| task_027 | Minor | Blocker | Blocker | Blocker | Major | Major | Major | Major | judgment |
| task_028 | None | Major | Major | Blocker | Major | Major | Major | Major | judgment |
| task_029 | Major | Major | Major | Major | Major | Major | Major | Major | none (already agreed) |
| task_031 | None | None | None | None | None | None | None | None | - |
| task_032 | None | Minor | Minor | Minor | Minor | Minor | Minor | Minor | - |
| task_033 | None | Minor | Minor | Minor | Minor | Minor | Minor | Minor | - |
| task_034 | None | Major | Minor | Minor | Major | Minor | Minor | Minor | - |
| task_035 | None | None | None | None | Minor | Minor | Minor | Minor | judgment |
| task_036 | None | None | None | None | None | None | None | None | - |
| task_037 | None | None | None | Minor | None | None | Minor | Minor | coverage |
| task_038 | None | Major | Minor | Minor | Major | Minor | Minor | Minor | - |
| task_039 | Blocker | Blocker | Major | Major | Blocker | Major | Major | Major | - |
| task_040 | Blocker | Blocker | Major | Major | Blocker | Major | Major | Major | - |
| task_041 | Blocker | Blocker | Blocker | Blocker | Major | Major | Major | Major | judgment |
| task_043 | None | None | Minor | None | None | None | None | None | - |
| task_044 | None | None | Minor | None | Minor | None | None | None | - |
| task_045 | None | None | Minor | None | None | None | None | None | - |
| task_046 | None | Major | Major | Major | Major | Major | Major | Major | - |
| task_047 | None | None | Minor | None | None | None | None | None | - |
| task_048 | None | Major | Major | Major | Major | Major | Major | Major | - |
| task_049 | None | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | - |
| task_050 | None | None | None | Minor | Minor | Minor | Minor | Minor | - |
| task_051 | None | Minor | None | None | Minor | Minor | Minor | Minor | judgment |
| task_052 | None | Minor | None | None | Minor | Minor | Minor | Minor | coverage |
| task_053 | None | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | - |
| task_054 | None | Minor | Minor | Minor | Minor | Minor | Minor | Minor | - |
| task_055 | None | None | None | None | None | None | None | None | - |
| task_056 | None | Major | Major | Major | Major | Major | Major | Major | - |
| task_057 | Minor | None | None | None | None | None | None | None | - |
| task_058 | None | None | None | None | None | None | None | None | - |
| task_059 | None | Minor | Major | Major | Major | Major | Major | Major | - |
| task_060 | None | Major | Major | Major | None | None | Major | None | scorer |
| task_061 | None | Major | Major | Major | None | None | Major | None | scorer |
| task_062 | None | Major | Major | Major | None | None | Major | None | scorer |
| task_063 | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | - |
| task_064 | None | Minor | None | None | None | None | None | None | - |
| task_065 | None | Major | Major | Major | Major | Major | Major | Major | - |
| task_066 | None | Major | Major | Major | None | None | Major | Major | judgment |
| task_067 | None | Major | Major | Major | None | None | Major | None | scorer |
| task_068 | None | Major | Blocker | Major | Major | Major | Major | Major | - |
| task_069 | None | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | - |
| task_070 | None | Major | Major | Major | Minor | Minor | Major | Major | judgment |
| task_071 | None | Major | Major | Major | Major | Major | Major | Major | - |
| task_072 | Minor | Major | Minor | Minor | Minor | Major | Major | Major | coverage |
| task_073 | Major | Major | Minor | Major | Minor | Major | Major | Major | - |
| task_074 | Blocker | Major | Major | Major | Minor | Major | Major | Major | - |
| task_075 | Blocker | Major | Blocker | Blocker | Blocker | Major | Major | Major | fact_error |
| task_076 | None | Major | Major | Major | Major | Major | Major | Major | - |
| task_077 | None | Major | Major | Major | Major | Major | Major | Major | - |
| task_078 | None | Minor | None | None | Minor | Minor | Minor | Minor | judgment |
| task_079 | None | Minor | Major | Major | Minor | Minor | Major | Major | judgment |
| task_080 | None | Major | Major | Minor | Major | Major | Minor | Minor | judgment |
| task_081 | None | Major | Major | Minor | Major | Major | Minor | Minor | judgment |
| task_082 | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | - |
| task_083 | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | - |
| task_084 | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | - |
| task_085 | Minor | Major | Major | Major | Major | Major | Major | Major | - |
| task_086 | Minor | Major | Major | Major | Major | Major | Major | Major | - |
| task_087 | None | Major | Minor | Minor | Major | Major | Major | Major | judgment |
| task_088 | Minor | Major | Major | Major | Major | Major | Major | Major | - |
| task_089 | None | None | None | None | None | None | None | None | - |
| task_090 | None | Minor | Minor | Minor | Minor | Minor | Minor | Minor | - |
| task_091 | None | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker | - |
| task_092 | Minor | Minor | Major | Major | Minor | Minor | Major | Major | judgment |
| task_093 | None | None | None | None | Minor | Minor | Minor | Minor | coverage |
| task_094 | Minor | Minor | Major | Major | Major | Major | Major | Major | - |
| task_095 | Major | Minor | Major | Major | Major | Major | Major | Major | - |
| task_096 | None | None | None | None | None | None | None | None | - |
| task_097 | Major | Blocker | Blocker | Major | Blocker | Blocker | Blocker | Blocker | judgment |
| task_098 | None | None | None | None | None | None | None | None | - |
| task_099 | None | None | None | None | Minor | Minor | Minor | Minor | coverage |
| task_100 | Minor | Minor | None | None | Minor | Minor | None | None | judgment |
| task_101 | Blocker | Major | Major | Major | Minor | Minor | Major | Major | judgment |
| task_102 | Major | Blocker | Blocker | Blocker | Major | Major | Blocker | Blocker | coverage |

## Notes

- Only four differences are scorer-caused (060, 061, 062, 067): each rests solely on close_bank_account_7392's free-text closure_reason, which the verified scorer strips. task_066 shares that defect but also has the scorer-independent Green savings naming defect, so it stays Major under both scorers.
- Benchmark self-contradiction, ATM fee stacking: business-checking docs state that out-of-network and foreign fees stack (hunter_green_010, navy_blue_009), while personal-checking docs never say so, and task_074's seed data and gold treat Purple foreign withdrawals as fee-free (no stacking). task_075's gold assumes stacking. Fix in one direction across 072-075.
- Benchmark self-contradiction, relationship bonus: task_093's gold applies the Silver 0.025% multi-product relationship bonus to a 2-product customer, and task_097's gold withholds it from a 13-product customer. silver_009's Platinum-card framing is the only text that could separate them, and it calls the bonus 'existing'.
- Benchmark self-contradiction, rewards rounding: user 755bcb4d5d's seed (tasks 020, 026, 027) is rounded half-up and task_026's gold writes 1500 for 1499.9, while doc_007 mandates floor and tasks 018/019/021/022/028/029 store floor values.
- 026-029 consistency: the unobservable cash_back_disputes status defect is rated Major everywhere (two supported dispositions, each gold reachable). task_026 stays Blocker only because gold[10] '1500 points' follows no documented rounding rule.
- Provisional-credit criterion 4 is applied by every gold (039, 040, 041, 080, 081) as a running count that excludes the dispute being filed. 041 is Major because its pre-session history differs from the running count; 080/081 are Minor because both readings give all three true and only the author notes disagree.
- Calibration applied uniformly: post-clock gold values Major (072); unscripted customer facts or choices with no documented default Major (041 XFINITY, 070/071 company age); undocumented conventions Major (092 and 091 unlock-by-reset); rules the grader cannot see Minor (035, 081 transfer); missing-but-retrievable required docs Minor (037, 029, 050); deciding-value placeholders Minor (093).
- The blank Step 3 in doc_credit_cards_credit_card_account_logistics_007 affects every CLI task (050-054). It is rated Minor wherever a gold-required get_payment_history_6183 read depends on it. Run U's 050 is Minor for a different reason (tier mapping missing from required_documents), and 053/054 were not re-adjudicated here.
- Known verified-scorer gaps matter for the debit-card tasks: order_debit_card_5739 copies the closed card's reason into the new card's issue_reason, so closure reasons still decide 078/079/080/081/087/092 under the verified scorer. User-side tables (user_discoverable_tool_calls, human_transfer_requests) are compared exactly, which keeps 081's four simulator transfer requests graded under both scorers.
- Replays were not re-run for this reconciliation. Every hash claim relied on here was reproduced independently by a reviewer or verifier in at least one run, with no conflicting replay between runs; the facts adjudicated (075, 080/081, 097, 102, 066) were settled from snapshot documents, task files and db.json read directly.
