# banking_knowledge v1.0.1 — upstream scorer vs revised verified scorer

Two independent reviews of the same 97 tasks on 2026-10-13 with the same model (claude-opus-5-5, effort high), task batches, inputs, verification and calibration prompts. The DB scorer differs: upstream exact-hash grading against the revised verified scorer (extra discoverable calls allowed only when every call was rejected for bad input; closure_reason ignored on bank accounts only). The verified-scorer run also used a later review prompt that adds grading facts confirmed during the upstream run and points reviewers to the calibration file. Both sides show their reviewers' and verifiers' own severities, with no reconciliation, so a difference can come from the scorer, the prompt update, or run-to-run judgment. 'Repeat' is an earlier same-scorer upstream review (draft-1) that shows how much reviewers alone vary.

## Agreement by stage

| Stage | Tasks with the same severity | Differences |
|---|---|---|
| Noise baseline: repeat (draft-1) vs upstream reviewers (same scorer) | 70/97 | 27 |
| Reviewers: upstream vs verified | 61/97 | 36 |
| After verification: upstream vs verified | 71/97 | 26 |

## Tasks that differ after verification (26)

- **task_005**: upstream Minor, verified None.
  - upstream: The gold is correct per the bypass-code document, but reaching it needs the simulated customer to come back after a transfer, which the simulator's general rules tell it to end the conversation on.
  - verified: Clean: the KB has an internal doc that accepts this exact bypass code and spells out the log_verification field values, so after the transfer the agent should log the bypass and change the email.
- **task_010**: upstream Major, verified None.
  - upstream: The diagnosis (a weekly referral cap that has now passed) is clear, but the gold expects the customer to resubmit with a tool the knowledge base never mentions. An agent that hands over the documented referral-link tool fails the DB check.
  - verified: Clean: the Platinum referral was auto-denied by the documented 2-per-rolling-7-days cap, that window has long passed, so after verifying the customer the agent explains he can retry and he resubmits the Platinum referral.
- **task_015**: upstream None, verified Major.
  - upstream: Clean: of the five referral offers the customer cites, only the Platinum Rewards Card offer matches a live documented program, and the gold gives and uses the referral-link tool for it.
  - verified: The gold expects the agent to give the referral-link tool to a customer it cannot verify (she knows only her phone number), but no document says verification is unnecessary, so cautious agents refuse and fail.
- **task_016**: upstream Minor, verified None.
  - upstream: The referral answer ($750 Silver card spend) is uniquely determined, but the customer's story says the friend has already made purchases while the database has no record of the friend at all.
  - verified: Clean: the only in-progress referral is a Silver Rewards Card referral whose documented requirement is $750 of spending, and the customer then makes exactly that purchase.
- **task_029**: upstream Major, verified Blocker.
  - upstream: To pass, the agent must refuse to update rewards because the disputes are still pending, but it has no tool to see dispute status and hears the same 'they were approved' claim that task_028 expects it to act on.
  - verified: The agent is expected to catch a customer lying that her disputes were approved, but it has no tool to check, and the twin task 028 rewards believing the same words.
- **task_035**: upstream None, verified Minor.
  - upstream: Clean: the 11/14 credit-bureau incident article clearly applies and names the emergency tool plus a transfer, which is exactly what the gold checks.
  - verified: The emergency credit-bureau transfer is well specified, but the action grader cannot tell whether the agent escalated immediately or verified first, as the task intends.
- **task_037**: upstream Minor, verified None.
  - upstream: The substance is clean: fraud reason, card opened 04/15/2024, $487.99/$299.95 within the mid-tier $5,000 cap, no prior disputes, cancel_and_reissue, last-4 5320, and the scripted work address and expedited acceptance all reproduce the gold. But both 'eligible' flags rest on criterion 4, and the only tool for checking it is documented solely in doc_016, which is absent from required_documents. That is the same missing-required-document class the review rated Minor in task_029, and the calibration rates it Minor. Under the default alltools config the agent can still retrieve doc_016, so the risk is limited to golden_retrieval.
  - verified: Clean: the replacement order and both fraud disputes are fully determined by the script, the transaction data, and the provisional-credit rules.
- **task_041**: upstream Blocker, verified Major.
  - upstream: Sixteen card disputes whose gold record stores a $69.99 partial refund and refund types the customer is never told to ask for, plus a provisional-credit cap the documents only imply.
  - verified: Sixteen-dispute task: the official answer grants provisional credit to only two disputes, which follows one reasonable reading of the 'no more than 2 disputes in 12 months' rule but not another, and several refund choices (including an exact $69.99 partial refund) are never stated by the customer.
- **task_045**: upstream None, verified Minor.
  - upstream: Reproduced the payment, reason, Business Platinum recommendation and $20 credit. The title and credit-score corruptions are cosmetic and decide nothing, so the calibration makes them notes and the task is clean. The residual closure_reason risk (not_using_card or simplifying_finances are both named by the customer) is correctly left as a note, consistent with 047/048/049.
  - verified: The Business Silver closure flow (pay $125, recommend Business Platinum, then apply a $20 retention credit) is derivable, but the customer gives two closure reasons and only one is accepted.
- **task_047**: upstream None, verified Minor.
  - upstream: The two-card flow reproduces. The only issues are cosmetic doc corruptions, which the calibration makes notes, so the task is clean. One more residual risk: bp_011 says 'Offer is for new customers only', and an agent that tells this existing Rho-Bank customer the waiver does not apply quotes a $450 fee. The script accepts only if the fee is 'waived for the first year or reasonable'. The doc's 'applies to new accounts opened within the promotion window' supports the gold, so I leave this as a note.
  - verified: The two-card retention flow (Business Platinum for the Silver Zoom, then a $50 credit on the under-2-year Platinum) is derivable, but the second closure reason is stated two ways.
- **task_054**: upstream Minor, verified Major.
  - upstream: The fraud-plus-credit-limit task is solvable from the documents, but the gold expects expedited shipping on the replacement card, and the customer's script never says whether she wants it.
  - verified: The expedited-shipping Minor holds. The review missed the ordering defect it flagged as Major in sibling task_053. An agent that handles the fraud first, as the customer asks, files the dispute and orders the replacement, then must deny the CLI under logistics_007, and fails. The gold needs the agent to anticipate the conflict and put the CLI ahead of a fraud response the customer called urgent, which no document prescribes. That is two defensible orders with different graded states, Major under calibration, and the same as 053.
- **task_057**: upstream None, verified Minor.
  - upstream: Blue Account is the only checking account that meets all of the customer's documented needs, the savings refusal leaves no DB trace, and the check deposit is scripted, so the task is clean.
  - verified: The task's headline test (refusing to open savings after the customer falsely claims 14 days have passed) is not graded, because the tool rejects the savings account anyway and the attempt leaves the compared state unchanged.
- **task_060**: upstream Major, verified None.
  - upstream: Silver Plus is the unique savings fit and the open-savings-before-closing order is documented, but the gold closure leaves the free-text closure reason at a hidden default, so an agent that records a reason fails.
  - verified: Clean: Silver Plus Account is the only savings product meeting all six needs, and the documented 14-day rule forces opening it before closing the Green Account.
- **task_061**: upstream Major, verified None.
  - upstream: The ordering and the $25 early-closure fee are documented and scripted, but the gold closure leaves the free-text closure reason at a hidden default, so an agent that records a reason fails.
  - verified: Clean: same savings choice and ordering as task_060, plus a documented $25 early-closure fee that the customer covers with a scripted $25 check deposit.
- **task_062**: upstream Major, verified None.
  - upstream: The four-step reordering puzzle is fully documented and the products are unique, but both gold closures leave the free-text closure reason at a hidden default, so an agent that records a reason fails.
  - verified: Clean: Navy Blue and Silver Plus are the only fits, and the documented eligibility rules force the one workable order (open business checking, then savings, then close accounts).
- **task_067**: upstream Major, verified None.
  - upstream: The best account-and-card combination is clearly derivable, but the grade also depends on leaving the optional closing-reason text empty.
  - verified: Clean: Purple checking + Platinum Plus savings + Platinum Rewards Card is the unique best combination for $100,000, by gross APY and after the card fee.
- **task_070**: upstream Major, verified Minor.
  - upstream: Picking Sky Blue through the active November promotion is derivable, but Sky Blue is a startup account and the customer's company age is never given.
  - verified: Sky Blue is the correct pick under the active November promotion, but the script never confirms the business meets Sky Blue's 4-year startup age limit.
- **task_072**: upstream Minor, verified Major.
  - upstream: Both refund amounts can be rebuilt exactly from the documents, but they rely on fee rows dated after 'today' and on assuming the bank's own ATM fee gets rebated.
  - verified: Both gold refund amounts include fee errors dated after the benchmark's fixed "today" (11/14/2025), so an agent that only reviews fees posted so far credits $13.50 and $3.00 instead of $14.00 and $3.50.
- **task_075**: upstream Blocker, verified Major.
  - upstream: The customer wants the account with the lowest foreign-ATM fees, but by the documents Purple and Bluest also charge $0 abroad (Purple adds operator-fee rebates), so Green Fee-Free is not the unique answer.
  - verified: Green Fee-Free is cheapest only if Purple's $2.50 out-of-network fee applies abroad and is not covered by Purple's $30 monthly ATM rebate; the benchmark's own fee-refund tasks assume the opposite on both points.
- **task_077**: upstream Major, verified Minor.
  - upstream: The lost-wallet sequence is fully documented, but the gold's choice of the PREMIUM card design depends on reading a vague 'best free option' as metallic rather than classic.
  - verified: The lost-wallet flow is derivable, but the gold records RUSH shipping and the PREMIUM card design, which the customer specifies only if asked and only as "the best option that's free".
- **task_079**: upstream Major, verified Minor.
  - upstream: The gold requires freezing three stolen cards and then unfreezing them before closing, but the policy says to recommend closing instead of freezing once a theft is confirmed, and skipping the freeze changes the graded state.
  - verified: The gold is right, but the card-closing rules say both 'no pending transactions' and 'pending refunds can be waived', and the Green account's only pending row is a refund.
- **task_087**: upstream Minor, verified Major.
  - upstream: The three-card CODE 05 diagnosis is derivable and the gold matches it; one security-alert document also tells agents to escalate when a customer reports a charge they did not make, which could lead a careful agent to transfer instead of filing the dispute.
  - verified: Fixing three declined cards is well specified, but one security document says to hand the customer to the security team when they report a charge they did not make, which would skip the gold's dispute and replacement.
- **task_092**: upstream Major, verified Minor.
  - upstream: The Blue-card fraud closure and the security-hold transfer are well-defined, but the Green card's outcome and the Evergreen 'unlock' each rely on readings that a careful agent could reasonably make differently.
  - verified: The four-card PIN-lock case reaches the gold through the customer's answers, but the 'escalate to supervisor' rule, the missing unlock tool, and an unscripted shipping choice leave room for drift.
- **task_093**: upstream None, verified Major.
  - upstream: Clean: the missing Green-checking boost and the multi-product relationship bonus are both documented, and the $33.00 correction follows directly.
  - verified: The arithmetic ($33.00) and the two Minor issues reproduce. The review rates 097 Major because its gold follows the 'may qualify / Platinum-linked only' reading. That same reading is a document-supported alternative here and gives $30.00, so the pair of readings is identical across 093 and 097. An agent applying either one consistently fails one of the two tasks. Per calibration, two document-supported readings with different graded states is Major in both.
- **task_096**: upstream None, verified Minor.
  - upstream: Clean: each savings account's highest checking boost and highest credit-card bonus are documented, and both corrections follow uniquely.
  - verified: Both savings corrections ($17.50 Bronze, $15.00 Gold Plus) are derivable, but one needed boost document is missing from the task's list, and the interest-formula and report-grading gaps apply here too.
- **task_102**: upstream Blocker, verified Major.
  - upstream: The grading requires the agent to 'recognize' that Ember is over Sky Blue's 4-year limit, but nothing the agent can see says so. 'Maximize the bonus' also points to Lime Green ($200 to the customer) rather than the gold's Sky Blue ($150).
  - verified: With one referral slot open, the customer asks to 'maximize the bonus'. Ember to Lime Green pays her more ($200), while the gold's TechFlow to Sky Blue pays more only in combined terms ($400).

## Final severity counts

| Severity | upstream | verified |
|---|---|---|
| Blocker | 14 | 12 |
| Major | 35 | 33 |
| Minor | 21 | 24 |
| None | 27 | 28 |

## Every task

| Task | v1.0.0 | Repeat | upstream reviewer | upstream verified | verified reviewer | verified verified |
|---|---|---|---|---|---|---|
| task_001 | None | None | None | None | None | None |
| task_002 | None | None | None | None | None | None |
| task_003 | None | None | None | None | None | None |
| task_004 | None | None | None | None | None | None |
| task_005 | None | None | Minor | Minor | None | None |
| task_006 | None | Minor | Minor | Minor | Minor | Minor |
| task_007 | None | None | None | None | None | None |
| task_008 | Minor | None | Minor | Minor | Minor | Minor |
| task_010 | None | None | Major | Major | None | None |
| task_012 | None | None | None | None | None | None |
| task_014 | None | Blocker | Blocker | Major | Major | Major |
| task_015 | None | None | None | None | Major | Major |
| task_016 | Minor | None | Minor | Minor | None | None |
| task_017 | Major | Major | Major | Major | Major | Major |
| task_018 | Major | Minor | Minor | Minor | Minor | Minor |
| task_019 | Major | Minor | Minor | Minor | Minor | Minor |
| task_020 | Minor | Major | Major | Major | Major | Major |
| task_021 | Major | Minor | Minor | Minor | Minor | Minor |
| task_022 | Major | Minor | Minor | Minor | Minor | Minor |
| task_023 | Minor | Minor | Minor | Minor | Minor | Minor |
| task_024 | None | Major | Major | Major | Major | Major |
| task_025 | Major | Major | Major | Major | Major | Major |
| task_026 | Minor | Blocker | Blocker | Blocker | Blocker | Blocker |
| task_027 | Minor | Blocker | Blocker | Blocker | Major | Blocker |
| task_028 | None | Major | Major | Blocker | Blocker | Blocker |
| task_029 | Major | Major | Major | Major | Blocker | Blocker |
| task_031 | None | None | None | None | None | None |
| task_032 | None | Minor | Minor | Minor | Minor | Minor |
| task_033 | None | Minor | Minor | Minor | Minor | Minor |
| task_034 | None | Major | Minor | Minor | Minor | Minor |
| task_035 | None | None | None | None | Minor | Minor |
| task_036 | None | None | None | None | None | None |
| task_037 | None | None | None | Minor | None | None |
| task_038 | None | Major | Minor | Minor | Minor | Minor |
| task_039 | Blocker | Blocker | Major | Major | Major | Major |
| task_040 | Blocker | Blocker | Major | Major | Major | Major |
| task_041 | Blocker | Blocker | Blocker | Blocker | Major | Major |
| task_043 | None | None | Minor | None | None | None |
| task_044 | None | None | Minor | None | None | None |
| task_045 | None | None | Minor | None | Minor | Minor |
| task_046 | None | Major | Major | Major | Minor | Major |
| task_047 | None | None | Minor | None | Minor | Minor |
| task_048 | None | Major | Major | Major | Major | Major |
| task_049 | None | Blocker | Blocker | Blocker | Blocker | Blocker |
| task_050 | None | None | None | Minor | Minor | Minor |
| task_051 | None | Minor | None | None | None | None |
| task_052 | None | Minor | None | None | None | None |
| task_053 | None | Blocker | Blocker | Blocker | Blocker | Blocker |
| task_054 | None | Minor | Minor | Minor | Minor | Major |
| task_055 | None | None | None | None | None | None |
| task_056 | None | Major | Major | Major | Major | Major |
| task_057 | Minor | None | None | None | Minor | Minor |
| task_058 | None | None | None | None | None | None |
| task_059 | None | Minor | Major | Major | Major | Major |
| task_060 | None | Major | Major | Major | None | None |
| task_061 | None | Major | Major | Major | None | None |
| task_062 | None | Major | Major | Major | None | None |
| task_063 | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker |
| task_064 | None | Minor | None | None | None | None |
| task_065 | None | Major | Major | Major | Major | Major |
| task_066 | None | Major | Major | Major | Minor | Major |
| task_067 | None | Major | Major | Major | None | None |
| task_068 | None | Major | Blocker | Major | Major | Major |
| task_069 | None | Blocker | Blocker | Blocker | Blocker | Blocker |
| task_070 | None | Major | Major | Major | Minor | Minor |
| task_071 | None | Major | Major | Major | Major | Major |
| task_072 | Minor | Major | Minor | Minor | Major | Major |
| task_073 | Major | Major | Minor | Major | Major | Major |
| task_074 | Blocker | Major | Major | Major | Major | Major |
| task_075 | Blocker | Major | Blocker | Blocker | Major | Major |
| task_076 | None | Major | Major | Major | Major | Major |
| task_077 | None | Major | Major | Major | Minor | Minor |
| task_078 | None | Minor | None | None | None | None |
| task_079 | None | Minor | Major | Major | Minor | Minor |
| task_080 | None | Major | Major | Minor | Minor | Minor |
| task_081 | None | Major | Major | Minor | Minor | Minor |
| task_082 | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker |
| task_083 | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker |
| task_084 | Blocker | Blocker | Blocker | Blocker | Blocker | Blocker |
| task_085 | Minor | Major | Major | Major | Major | Major |
| task_086 | Minor | Major | Major | Major | Major | Major |
| task_087 | None | Major | Minor | Minor | Major | Major |
| task_088 | Minor | Major | Major | Major | Major | Major |
| task_089 | None | None | None | None | None | None |
| task_090 | None | Minor | Minor | Minor | Minor | Minor |
| task_091 | None | Blocker | Blocker | Blocker | Blocker | Blocker |
| task_092 | Minor | Minor | Major | Major | Minor | Minor |
| task_093 | None | None | None | None | Minor | Major |
| task_094 | Minor | Minor | Major | Major | Major | Major |
| task_095 | Major | Minor | Major | Major | Major | Major |
| task_096 | None | None | None | None | Minor | Minor |
| task_097 | Major | Blocker | Blocker | Major | Major | Major |
| task_098 | None | None | None | None | None | None |
| task_099 | None | None | None | None | None | None |
| task_100 | Minor | Minor | None | None | None | None |
| task_101 | Blocker | Major | Major | Major | Minor | Major |
| task_102 | Major | Blocker | Blocker | Blocker | Major | Major |

## Notes

- The upstream side uses that run's reviewer and verifier severities (Blocker 14, Major 35, Minor 21, None 27). Its published report shows severities reconciled against the earlier, superseded verified-scorer run (11 / 40 / 25 / 21); that reconciliation is not used here.
- Four differences come from the scorer: 060, 061, 062 and 067 close a bank account, and only the verified scorer ignores a custom closure_reason there. The verified-scorer reviewers and verifiers report that no other verdict in their run depends on the scorer's relaxations, so the remaining 22 differences are differences in judgment or in what each review found, about as many as the 27 between two same-scorer reviews.
- The verified-scorer run's review prompt adds grading facts confirmed during the upstream run (read log keyed by tool name, which rejected calls are logged, ACTION grading ignores who made the call, NL assertions multiply into the reward) and points reviewers to calibration.md.
