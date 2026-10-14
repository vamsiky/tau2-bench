# `banking_knowledge` benchmark correctness review — v1.0.1

**Benchmark:** `v1.0.1` (`fc0055dc4e`) · **Run date:** 2026-10-13 · **Reviewer:** claude-opus-5-5: 8 parallel reviewers + 4 independent verifiers (Claude Code subagents) · **Effort:** high (set explicitly on every agent) · **Prior review:** 2026-06-25-v1.0.0

The interactive version (`review.html`) shows each task's customer instructions, required documents, gold trajectory, and findings side by side.

## Summary

| Severity | Now | Prior |
|---|---|---|
| Blocker | 11 | 10 |
| Major | 36 | 11 |
| Minor | 25 | 14 |
| None | 25 | 62 |

97 tasks reviewed against v1.0.1: 11 Blocker, 36 Major, 25 Minor, 25 clean (v1.0.0 review: 10 / 11 / 14 / 62). v1.0.1's fixes hold where checked: task_074's corrected $14.50 Light Blue refund reproduces, bank transactions now sort newest-first, and the rewards rounding rule turns out to be documented, which clears the old Majors on 018, 019, 021 and 022. Four v1.0.0 Blockers persist (063, 082, 083, 084); five drop to Major because the documents support the gold's reading (039, 040, 041, 075, 101). The rise in flagged tasks comes mostly from defects the v1.0.0 review did not report: 39 tasks it rated clean have a defect now, found by replaying gold and alternative actions. Under the verified scorer, the four tasks whose only defect is the graded closure reason (060, 061, 062, 067) are clean; nothing else changes. Severities are reviewer verdicts checked by independent verifiers and reconciled with the companion run.

## Systemic issues

1. **Gold depends on information the agent cannot observe** (task_026, task_027, task_028, task_029, task_049, task_053, task_102). No agent tool reads cash_back_disputes and the customer's own tool results never reach the agent, so 026–029 grade the same customer claim in opposite ways. task_053's gold uses card digits only the customer's omitted lookup returns, task_049 needs the customer to call a transfer tool unprompted, and task_102's NL assertion needs a company age that exists only in author notes.
2. **Gold values contradict the documents or each other** (task_026, task_069, task_082, task_083, task_084, task_091, task_097). task_069 assumes Gold savings has no ATM rebates (gold_account_003 documents $30/month); task_097 omits the 0.025% relationship bonus that task_093's gold applies; task_026 writes 1500 points where the documented round-down rule gives 1499; task_083's ACTION gold omits a required argument so no call can match; 082, 084 and 091 record dispute, liability, and replacement values that no single documented rule produces.
3. **Strings the gold stores verbatim differ from what the documents tell the agent to write** (task_056, task_059, task_065, task_066, task_068, task_071). doc_001's own example spells products 'Green Account (checking)' while the gold stores 'Green Account', and general_004 says to open business savings with account_type 'savings' while the gold uses 'business_savings'. Following the documents opens a different account id and fails the DB match.
4. **Ties and multiple defensible products with no tie-breaker** (task_063, task_024, task_025, task_048, task_075, task_076). task_063 is an exact tie (Bronze and Silver Rewards both add +0.15% at $0); in the others a second product is as good or better under one supported reading (Silver Zoom's promo in 024, Apple Music's category in 025, Platinum Rewards in 048, ATM-fee stacking in 075, Bluest's unstated deposit in 076).
5. **Customer choices the gold records but the script never states** (task_041, task_070, task_077, task_079, task_092). Refund types, a company's formation date, card design, freezing before closing, and how to unlock a card are fixed in the gold but never given to the simulated customer or settled by a documented default.
6. **Fee, rebate, and rounding rules applied inconsistently across sibling tasks** (task_017, task_020, task_072, task_073, task_074, task_094, task_095). Refunds in 072–074 count fees dated after the fixed clock; 072–074 assume out-of-network and foreign ATM fees do not stack while 075 assumes they do; seed rewards in 020/026/027 use round-half-up against the documented floor rule; 094/095 hinge on whether a 0.025% card bonus stacks.
7. **Dispute fields with no single documented rule** (task_039, task_040, task_085, task_086, task_088). Whether disputes filed earlier in the same call count toward the provisional-credit limit, how customer_max_liability_amount is derived, and how pin_compromised and transaction type are chosen all have two defensible readings; the gold picks one.

## Changes since the prior review

| Task | Prior | Now | Status | Headline |
|---|---|---|---|---|
| task_005 | None | Minor | new | Gold matches the KB's bypass-code procedure, but it can only be reached if the simulated customer keeps talking after the transfer instead of ending the call as the simulator rules say. |
| task_006 | None | Minor | new | EcoCard is the unique answer, but ruling out the Crypto-Cash Back card depends on a minimum credit score that the KB writes as a dollar amount ("$660"). |
| task_010 | None | Major | new | The diagnosis (weekly referral cap) is clear, but if the agent helps the customer retry the referral the way the KB documents, by handing over the referral-link tool, the gold scores that as wrong. |
| task_014 | None | Major | new | The gold requires a transfer to a human, but the KB's internal referral-link procedure says that for a card with no documented referral program the agent must explain and must not transfer. |
| task_015 | None | None | new | The customer walks through five claimed referral offers and only the Platinum one matches the KB, so the gold of giving the referral-link tool for Platinum is sound; an over-cautious identity check would add an extra DB write and fail. |
| task_017 | Major | Major | changed | Under the bank's documented round-down rule, a third transaction (Hilton, over-credited by 1 point) is also wrong, but the gold disputes only two, so an agent that flags every error fails. |
| task_018 | Major | Minor | changed | The documented round-down rule reproduces the six gold disputes exactly; the only defect is that the rounding doc is missing from required_documents. |
| task_019 | Major | Minor | changed | The documented round-down rule reproduces the four gold disputes exactly; the only defect is that the rounding doc is missing from required_documents. |
| task_020 | Minor | Major | changed | This customer's stored rewards use normal rounding while the bank's policy doc says rewards are always rounded down, so an agent following the policy flags nine extra 1-point over-credits. |
| task_021 | Major | Minor | changed | The documented round-down rule plus the stated merchant exclusions reproduce the two gold disputes exactly; the only defect is that the rounding doc is missing from required_documents. |
| task_022 | Major | Minor | changed | Across 77 transactions on four cards, the documented rates, exclusions, and round-down rule reproduce the ten gold disputes exactly; the only defect is that the rounding doc is missing from required_documents. |
| task_024 | None | Major | new | The gold card (Business Bronze, $900 back) beats every card except the Silver Zoom Card, whose triple-cash-back promo pays at least $1,200 on the truck; the docs never say whether a landscaping company can get that card. |
| task_026 | Minor | Blocker | changed | The gold writes 1500 points for a transaction that the bank's own rounding policy says earns 1499, and it expects the agent to confirm the disputes are resolved when no agent tool can see dispute status. |
| task_027 | Minor | Major | changed | The task tests whether the agent checks that the disputes are really resolved before updating rewards, but no agent tool can see dispute status, and its twin task_026 rewards the opposite choice for the same conversation. |
| task_028 | None | Major | new | The agent is expected to update the customer's rewards because she says her disputes were approved, but it has no way to check that, and task_029 shows it the same conversation and expects it to refuse. |
| task_029 | Major | Major | changed | The test is whether the agent catches the customer lying that her disputes were approved, but the agent has no tool that shows dispute status, so passing depends on whether it refuses unverifiable requests by default. |
| task_032 | None | Minor | new | The transfer protocol is clearly documented, but the grader only checks that the special tool was used at least once, not that it was used for the first three requests before the real transfer. |
| task_033 | None | Minor | new | The incident transfer protocol is clear and the gold follows it, but the grader cannot tell whether the agent waited for the third request or skipped identity verification as instructed. |
| task_034 | None | Minor | new | The task is meant to test that the agent holds off transferring until the eighth request, but the grader passes any agent that eventually transfers, even on the first request. |
| task_035 | None | Minor | new | The emergency credit-bureau transfer is clearly documented and the gold matches it; the only gap is that the grader cannot check that the agent skipped identity verification. |
| task_037 | None | Minor | not_applicable | A clean replacement-plus-two-fraud-disputes task: every argument, including both provisional-credit flags, follows from the customer's script and the dispute docs. |
| task_038 | None | Minor | new | The gold requires expedited shipping for the replacement card, which costs this customer $10, but her script never says whether she wants it, so the result depends on how the simulated customer improvises. |
| task_039 | Blocker | Major | persists | The written rule says a customer with no past disputes qualifies for provisional credit, but the official answer denies it on the fourth qualifying dispute, which only makes sense if disputes filed earlier in the same call count and are filed in a particular order. |
| task_040 | Blocker | Major | persists | With one past dispute on file, the written rule makes all four fraud and duplicate disputes eligible for provisional credit, but the official answer grants it to only two, using a running count and a filing order the documents never state. |
| task_041 | Blocker | Major | changed | Which disputes get provisional credit depends on whether disputes filed earlier in the same call count toward the 'no more than 2 disputes in 12 months' rule, which the policy never says; the XFINITY refund amount also has to be inferred from 'around $120'. |
| task_044 | None | None | new | Mostly clean: the Platinum Rewards Card is the only Rho-Bank card that beats the competitor, though its doc still lists a credit score as a dollar amount. |
| task_046 | None | Major | new | The gold expects the agent to stop at the pending dispute and leave the $125 balance unpaid, but if the agent mentions the balance, the customer is scripted to ask for it to be paid. |
| task_048 | None | Major | new | For the Gold card, several Rho-Bank cards beat the competitor's 3.25% travel/software rate, but the gold accepts only an application for the Silver Rewards Card. |
| task_049 | None | Blocker | new | The gold includes a customer-side 'request human transfer' write that the customer is never told to perform, so the result depends on whether the user simulator happens to call that tool exactly once. |
| task_050 | None | Minor | new | Mostly clean: a straightforward credit-limit increase approval, though one step of the internal workflow document is blank. |
| task_051 | None | Minor | new | Mostly clean deny-pay-resubmit-approve flow. The resubmission returns a misleading 'similar request may already exist' error that the agent must work past, and the workflow doc's Step 3 is blank. |
| task_052 | None | Minor | new | Mostly clean: the entry-tier 120-day cooldown cleanly forces a denial however hard the customer pushes, though one step of the workflow doc is blank. |
| task_053 | None | Blocker | new | The gold leaves out the customer's own card-number lookup, but the agent cannot get the card's last 4 digits without it, so every correct trajectory leaves an extra DB row and fails. |
| task_054 | None | Minor | new | The task is solvable, but the customer is never told whether she wants expedited shipping for the replacement card, and the official answer records expedited shipping. |
| task_056 | None | Major | new | The business-savings opening procedure tells the agent to use account type 'savings', but the official answer uses 'business_savings', so an agent that follows the procedure document fails. |
| task_057 | Minor | None | resolved | Clean: Blue Account is the only personal checking that meets all four stated needs, the savings request must be refused, and the check deposit is fully determined. |
| task_059 | None | Major | new | The right products are clear (Silver Rewards Card plus Green savings), but the KB calls the savings account 'Green Account (savings)' while the official answer only accepts the account name 'Green Account'. |
| task_065 | None | Major | new | The right pairing (Evergreen checking plus Green savings, opened before closing Light Blue) is clear, but the official answer only accepts the savings name 'Green Account' while the KB calls it 'Green Account (savings)'. |
| task_066 | None | Major | not_applicable | The best savings-plus-checking-plus-card combination for $6,000 can be worked out uniquely from the documents, and the official answer matches it. |
| task_068 | None | Major | new | The right accounts are clear, but the bank's own procedure tells the agent to name the checking account 'Green Account (checking)', while the answer key only accepts 'Green Account'. |
| task_069 | None | Blocker | new | The official answer assumes the Gold savings account has no ATM-fee rebates, but the documents say it does, so the truly best combination (about 5.7% instead of 3.5%) is graded as wrong. |
| task_070 | None | Major | new | The active November promotion picks Sky Blue among the three accounts that fit, but Sky Blue's startup-age eligibility can't be confirmed because the customer is never told when her business was formed. |
| task_071 | None | Major | new | The right accounts (Sky Blue and Gold Saver) follow from the active promotions, but the bank's business-savings procedure tells the agent to open it as a personal 'savings' account, which creates the wrong record. |
| task_072 | Minor | Major | changed | Both refund amounts ($14.00 and $3.50) can be rebuilt from the fee schedules and the 'net correction' rule, but some of the fees that count are dated after the benchmark's fixed 'today'. |
| task_073 | Major | Major | changed | All three refunds ($9.50, $9.00, $1.50) follow from the fee schedules and the documented 'net correction' rule, but some of the errors that count are dated after the benchmark's fixed 'today'. |
| task_074 | Blocker | Major | changed | After the v1.0.1 fix, all four refunds ($27.00, $14.50, $4.75, $3.70) can be rebuilt from the fee documents; one Purple error the gold depends on is dated after the fixed 'today'. |
| task_075 | Blocker | Major | persists | Several checking accounts charge $0 for foreign ATM withdrawals, and Purple even refunds operator fees, but the answer key only accepts Green Fee-Free, based on a fee-stacking rule the documents never state. |
| task_076 | None | Major | new | Purple checking is the sensible answer, but Bluest also gives 2-day early deposit with equal or lower ATM fees and is ruled out only by a $75,000 opening deposit the customer is never asked about. |
| task_077 | None | Major | new | The lost-wallet procedure can be followed step by step, but the replacement card's design is ambiguous: the customer asks for the 'best free option' and no 'fancy design', and the answer key only accepts the PREMIUM design. |
| task_078 | None | Minor | new | Lost-wallet task is solvable from the documents, but the graded database records the freeze-then-unfreeze history, so closing the lost cards directly (as one document recommends) fails. |
| task_079 | None | Major | new | Stolen-wallet task is solvable, but it records the freeze-then-unfreeze history and leans on reading a pending refund as a refund rather than a pending transaction. |
| task_080 | None | Minor | new | The gold gives provisional credit on all three credit-card fraud disputes, while the task's own notes and customer script are built around a two-dispute limit that withholds it from the $149.95 charge. |
| task_081 | None | Minor | new | Same scenario and same provisional-credit mismatch as task_080, and the "transfer only on the fourth request" behavior the task is built to test is not graded. |
| task_084 | Blocker | Blocker | changed | The stored liability amounts follow no single rule: the $47.50 duplicate gets $50 (not capped) while the $412.88 late fraud gets $412.88 (capped), so any consistent calculation misses one of them. |
| task_085 | Minor | Major | changed | The verify-the-customer's-claims flow is sound, but the duplicate-row pick, liability amounts, a provisional-credit flag and an unscripted merchant-contact answer each have more than one defensible stored value. |
| task_086 | Minor | Major | changed | The six-dispute workflow is reconstructible, but whether to file the ATM-deposit dispute at all, how to code the skimmed-card fraud, and the liability amounts each have more than one defensible answer. |
| task_087 | None | Major | new | The decline-diagnosis steps are clear, but when the customer reports a fraudulent charge the KB says to escalate to the security team, while the gold files a dispute and replaces the card. |
| task_088 | Minor | Major | changed | The KB's chip-mismatch procedure says to freeze the card until a replacement arrives and to follow the stolen-card protocol, while the gold closes it as fraud; the fraud charge's PIN/signature type is also never given. |
| task_090 | None | Minor | new | The three-card PIN-lock case is solvable as written; the only soft spot is that the Evergreen replacement card has two equally free designs and the customer never picks one. |
| task_091 | None | Blocker | new | The official answer orders the cheapest replacement card although the customer asked for the most premium free one, and it orders a Light Blue replacement that the rules say must wait 48 hours. |
| task_092 | Minor | Major | persists | The four-card case is reachable because the customer's scripted answers steer each card, but the rule for a single 3-point risk flag never says whether to unlock, transfer, or replace. |
| task_093 | None | Minor | new | The Silver savings interest correction ($33.00) is derivable from the documents; one required document contains an unfilled template placeholder. |
| task_094 | Minor | Major | persists | The Gold Rewards Card's 0.025% bonus is described both as a card bonus (outranked by the EcoCard) and as a separate relationship bonus that stacks, so the correct credit could be $140 or $142. |
| task_097 | Major | Blocker | changed | For the Silver account, the official credit leaves out a 0.025% relationship bonus that this task's own document grants (and that task_093 applies), and the cent amount also depends on the rounding method. |
| task_099 | None | Minor | new | World Blue ($300) is the best referrer bonus a $30,000 deposit qualifies for; the only soft spots are a corrupted value and "international businesses" wording in the World Blue documents. |
| task_100 | Minor | None | persists | Hunter Green ($175) is correct once tenure is measured from the on-file account date; the customer's claim of "mid-July" is a resolvable red herring. |
| task_101 | Blocker | Major | changed | Purple plus Sky Blue is the right pair once the 2-per-9-days referral cap is applied to the new batch; the policy wording that justifies the cap is slightly loose. |
| task_102 | Major | Blocker | persists | With only one referral slot, the customer asks to "maximize the bonus" without saying whose bonus; the official TechFlow-to-Sky Blue pick wins on combined bonus but loses to Ember-to-Lime Green on her own bonus. |

## All tasks

| Task | Final | Reviewer | Verifier | Reconciled | Prior | Instr. | Docs det. | Cx | Ordering | Gold ok | Headline |
|---|---|---|---|---|---|---|---|---|---|---|---|
| task_001 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 2 | None | Yes | Clean: the only no-annual-fee card with the highest everyday cash back is the Gold Rewards Card, which the customer qualifies for through her Rho-Bank+ subscription. |
| task_002 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 3 | None | Yes | Clean: the Platinum Rewards Card's 10% cash back is the highest, and its $200 fee less the $150 monthly-spend rebate fits the customer's $100 effective-fee limit. |
| task_003 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 3 | None | Yes | Clean: Silver and Gold both meet the hard requirements at a $0 fee, and for a travel-heavy spender Silver's 4% travel rate beats Gold's flat 2.5%. |
| task_004 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 2 | None | Yes | Clean: the caller matches only one of four identity fields, so he cannot be verified, and the transfer-code table names identity-verification failures under account_ownership_dispute. |
| task_005 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 3 | Strict | Yes | Gold matches the KB's bypass-code procedure, but it can only be reached if the simulated customer keeps talking after the transfer instead of ending the call as the simulator rules say. |
| task_006 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 3 | None | Yes | EcoCard is the unique answer, but ruling out the Crypto-Cash Back card depends on a minimum credit score that the KB writes as a dollar amount ("$660"). |
| task_007 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 3 | None | Yes | Clean: on the fixed date, the only active points or cash sign-up bonus on a personal card open to this customer is the EcoCard's. |
| task_008 | Minor | Minor | Not sampled (-) | - | Minor | Sufficient | Yes | 2 | None | Yes | The gold transfer code is right under the KB's rule to use the highest tier that applies, but a lower-tier code describes this exact flyer scenario word for word. |
| task_010 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 3 | Soft | Yes | The diagnosis (weekly referral cap) is clear, but if the agent helps the customer retry the referral the way the KB documents, by handing over the referral-link tool, the gold scores that as wrong. |
| task_012 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 1 | None | Yes | Clean: the KB has no travel-notification procedure, so the agent should say so and transfer under kb_search_unsuccessful_customer_requests_transfer when the customer asks. |
| task_014 | Major | Blocker | Adjusted (Major) | - | None | Sufficient | No | 2 | None | No | The gold requires a transfer to a human, but the KB's internal referral-link procedure says that for a card with no documented referral program the agent must explain and must not transfer. |
| task_015 | None | Minor | Overturned (None) | - | None | Sufficient | Yes | 3 | Soft | Yes | The customer walks through five claimed referral offers and only the Platinum one matches the KB, so the gold of giving the referral-link tool for Platinum is sound; an over-cautious identity check would add an extra DB write and fail. |
| task_016 | Minor | None | Confirmed (None) | yes | Minor | Sufficient | Yes | 2 | None | Yes | Clean: the only in-progress referral is a Silver Rewards Card referral, and the Silver referral doc states the $750 spend requirement the friend's transaction must match. |
| task_017 | Major | Major | Confirmed (Major) | - | Major | Sufficient | Partial | 3 | Soft | No | Under the bank's documented round-down rule, a third transaction (Hilton, over-credited by 1 point) is also wrong, but the gold disputes only two, so an agent that flags every error fails. |
| task_018 | Minor | Minor | Confirmed (Minor) | - | Major | Sufficient | Yes | 4 | Soft | Yes | The documented round-down rule reproduces the six gold disputes exactly; the only defect is that the rounding doc is missing from required_documents. |
| task_019 | Minor | Minor | Confirmed (Minor) | - | Major | Sufficient | Yes | 4 | Soft | Yes | The documented round-down rule reproduces the four gold disputes exactly; the only defect is that the rounding doc is missing from required_documents. |
| task_020 | Major | Major | Confirmed (Major) | - | Minor | Sufficient | Partial | 4 | Soft | No | This customer's stored rewards use normal rounding while the bank's policy doc says rewards are always rounded down, so an agent following the policy flags nine extra 1-point over-credits. |
| task_021 | Minor | Minor | Confirmed (Minor) | - | Major | Sufficient | Yes | 4 | Soft | Yes | The documented round-down rule plus the stated merchant exclusions reproduce the two gold disputes exactly; the only defect is that the rounding doc is missing from required_documents. |
| task_022 | Minor | Minor | Confirmed (Minor) | - | Major | Sufficient | Yes | 5 | Soft | Yes | Across 77 transactions on four cards, the documented rates, exclusions, and round-down rule reproduce the ten gold disputes exactly; the only defect is that the rounding doc is missing from required_documents. |
| task_023 | Minor | Minor | Confirmed (Minor) | - | Minor | Sufficient | Yes | 4 | None | Yes | The customer says the card was opened in November 2024 but the bank record says November 2022; the record-based answer (qualifies, apply for Diamond) matches the gold, though believing the customer could flip it. |
| task_024 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 4 | None | Yes | The gold card (Business Bronze, $900 back) beats every card except the Silver Zoom Card, whose triple-cash-back promo pays at least $1,200 on the truck; the docs never say whether a landscaping company can get that card. |
| task_025 | Major | Major | Confirmed (Major) | - | Major | Sufficient | Partial | 4 | None | Yes | The gold card (Business Platinum) wins only if an Apple Music subscription earns its 4% 'software/media advertising' rate; the docs disagree on whether streaming is 'Media' or 'Entertainment', and the strict reading drops Platinum to a tie or a loss. |
| task_026 | Blocker | Blocker | Confirmed (Blocker) | yes | Minor | Partial | No | 5 | Soft | No | The gold writes 1500 points for a transaction that the bank's own rounding policy says earns 1499, and it expects the agent to confirm the disputes are resolved when no agent tool can see dispute status. |
| task_027 | Major | Major | Confirmed (Major) | yes | Minor | Partial | Partial | 4 | Soft | Yes | The task tests whether the agent checks that the disputes are really resolved before updating rewards, but no agent tool can see dispute status, and its twin task_026 rewards the opposite choice for the same conversation. |
| task_028 | Major | Major | Confirmed (Major) | yes | None | Partial | Partial | 4 | Strict | Yes | The agent is expected to update the customer's rewards because she says her disputes were approved, but it has no way to check that, and task_029 shows it the same conversation and expects it to refuse. |
| task_029 | Major | Major | Confirmed (Major) | yes | Major | Partial | Partial | 4 | Soft | Yes | The test is whether the agent catches the customer lying that her disputes were approved, but the agent has no tool that shows dispute status, so passing depends on whether it refuses unverifiable requests by default. |
| task_031 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 2 | Soft | Yes | A clean single-dispute task: every value in the filed dispute comes from the customer, the transaction record, or the provisional-credit rules. |
| task_032 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 2 | Strict | Yes | The transfer protocol is clearly documented, but the grader only checks that the special tool was used at least once, not that it was used for the first three requests before the real transfer. |
| task_033 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 2 | Strict | Yes | The incident transfer protocol is clear and the gold follows it, but the grader cannot tell whether the agent waited for the third request or skipped identity verification as instructed. |
| task_034 | Minor | Major | Adjusted (Minor) | - | None | Sufficient | Yes | 2 | Strict | Yes | The task is meant to test that the agent holds off transferring until the eighth request, but the grader passes any agent that eventually transfers, even on the first request. |
| task_035 | Minor | Minor | Confirmed (Minor) | yes | None | Sufficient | Yes | 1 | Soft | Yes | The emergency credit-bureau transfer is clearly documented and the gold matches it; the only gap is that the grader cannot check that the agent skipped identity verification. |
| task_036 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 2 | Soft | Yes | A clean replacement-card task: account, reason, work address, and expedited shipping all come from the customer's script and the replacement docs. |
| task_037 | Minor | None | Confirmed (None) | yes | None | Sufficient | Yes | 3 | Soft | Yes | A clean replacement-plus-two-fraud-disputes task: every argument, including both provisional-credit flags, follows from the customer's script and the dispute docs. |
| task_038 | Minor | Major | Adjusted (Minor) | - | None | Partial | Yes | 3 | Soft | Yes | The gold requires expedited shipping for the replacement card, which costs this customer $10, but her script never says whether she wants it, so the result depends on how the simulated customer improvises. |
| task_039 | Major | Blocker | Adjusted (Major) | - | Blocker | Partial | No | 5 | Strict | No | The written rule says a customer with no past disputes qualifies for provisional credit, but the official answer denies it on the fourth qualifying dispute, which only makes sense if disputes filed earlier in the same call count and are filed in a particular order. |
| task_040 | Major | Blocker | Adjusted (Major) | - | Blocker | Partial | No | 5 | Strict | No | With one past dispute on file, the written rule makes all four fraud and duplicate disputes eligible for provisional credit, but the official answer grants it to only two, using a running count and a filing order the documents never state. |
| task_041 | Major | Major | Confirmed (Major) | yes | Blocker | Partial | Partial | 5 | Strict | Yes | Which disputes get provisional credit depends on whether disputes filed earlier in the same call count toward the 'no more than 2 disputes in 12 months' rule, which the policy never says; the XFINITY refund amount also has to be inferred from 'around $120'. |
| task_043 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 3 | Strict | Yes | Clean: the retention protocol leads the agent from the $75 balance payoff to the loyalty fee waiver, and every persisted value can be derived. |
| task_044 | None | Minor | Adjusted (None) | - | None | Sufficient | Yes | 3 | Soft | Yes | Mostly clean: the Platinum Rewards Card is the only Rho-Bank card that beats the competitor, though its doc still lists a credit score as a dollar amount. |
| task_045 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 4 | Strict | Yes | Clean: after the balance payoff, the agent recommends the Business Platinum card and, when the customer declines, gives the documented mid-tier $20 retention credit. |
| task_046 | Major | Major | Confirmed (Major) | - | None | Partial | Partial | 2 | Strict | Yes | The gold expects the agent to stop at the pending dispute and leave the $125 balance unpaid, but if the agent mentions the balance, the customer is scripted to ask for it to be paid. |
| task_047 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 4 | Soft | Yes | Clean: Business Platinum is the only business card that beats the competitor, and the under-2-year tenure leads to a downgrade offer followed by the $50 premium retention credit. |
| task_048 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 4 | Strict | Yes | For the Gold card, several Rho-Bank cards beat the competitor's 3.25% travel/software rate, but the gold accepts only an application for the Silver Rewards Card. |
| task_049 | Blocker | Blocker | Confirmed (Blocker) | - | None | Partial | Yes | 4 | Strict | No | The gold includes a customer-side 'request human transfer' write that the customer is never told to perform, so the result depends on whether the user simulator happens to call that tool exactly once. |
| task_050 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 3 | Strict | Yes | Mostly clean: a straightforward credit-limit increase approval, though one step of the internal workflow document is blank. |
| task_051 | Minor | Minor | Confirmed (Minor) | yes | None | Sufficient | Yes | 4 | Strict | Yes | Mostly clean deny-pay-resubmit-approve flow. The resubmission returns a misleading 'similar request may already exist' error that the agent must work past, and the workflow doc's Step 3 is blank. |
| task_052 | Minor | Minor | Confirmed (Minor) | yes | None | Sufficient | Yes | 3 | Strict | Yes | Mostly clean: the entry-tier 120-day cooldown cleanly forces a denial however hard the customer pushes, though one step of the workflow doc is blank. |
| task_053 | Blocker | Blocker | Confirmed (Blocker) | - | None | Sufficient | Partial | 4 | Strict | No | The gold leaves out the customer's own card-number lookup, but the agent cannot get the card's last 4 digits without it, so every correct trajectory leaves an extra DB row and fails. |
| task_054 | Minor | Minor | Confirmed (Minor) | - | None | Partial | Yes | 4 | Strict | Yes | The task is solvable, but the customer is never told whether she wants expedited shipping for the replacement card, and the official answer records expedited shipping. |
| task_055 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 4 | Soft | Yes | Clean: the checking and savings criteria each single out one product, and the check-deposit funding step is fully determined. |
| task_056 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 4 | Soft | No | The business-savings opening procedure tells the agent to use account type 'savings', but the official answer uses 'business_savings', so an agent that follows the procedure document fails. |
| task_057 | None | None | Confirmed (None) | - | Minor | Sufficient | Yes | 3 | Strict | Yes | Clean: Blue Account is the only personal checking that meets all four stated needs, the savings request must be refused, and the check deposit is fully determined. |
| task_058 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 5 | None | Yes | Clean: EcoCard plus Silver Account is the single best net-return combination for $20,000, and the agent only has to open the savings account. |
| task_059 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 4 | None | Yes | The right products are clear (Silver Rewards Card plus Green savings), but the KB calls the savings account 'Green Account (savings)' while the official answer only accepts the account name 'Green Account'. |
| task_060 | None | None | Not sampled (-) | yes | None | Sufficient | Yes | 4 | Strict | Yes | Clean: Silver Plus is the only savings account meeting all six needs, and the 14-day rule forces opening it before closing the older Green checking. |
| task_061 | None | None | Not sampled (-) | yes | None | Sufficient | Yes | 4 | Strict | Yes | Clean: open Silver Plus savings first, then have the customer deposit a $25 check so the early-closure fee can be taken and the Green checking closed. |
| task_062 | None | None | Confirmed (None) | yes | None | Sufficient | Yes | 5 | Strict | Yes | Clean: Navy Blue and Silver Plus are uniquely determined, and the documented eligibility rules force opening both new accounts before either closure. |
| task_063 | Blocker | Blocker | Confirmed (Blocker) | - | Blocker | Sufficient | No | 4 | None | No | Two credit cards (Bronze Rewards and Silver Rewards) give the exact same savings boost and both meet every customer condition, but only Silver Rewards is accepted. |
| task_064 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 5 | None | Yes | Clean: with a Rho-Bank+ subscription, Gold Rewards Card plus Gold Plus Account is the single best net-return combination for $30,000. |
| task_065 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 5 | Strict | Yes | The right pairing (Evergreen checking plus Green savings, opened before closing Light Blue) is clear, but the official answer only accepts the savings name 'Green Account' while the KB calls it 'Green Account (savings)'. |
| task_066 | Major | None | Not sampled (-) | yes | None | Sufficient | Yes | 4 | Strict | Yes | The best savings-plus-checking-plus-card combination for $6,000 can be worked out uniquely from the documents, and the official answer matches it. |
| task_067 | None | None | Not sampled (-) | yes | None | Sufficient | Yes | 5 | Strict | Yes | At $100,000 the documents single out Purple checking, Platinum Plus savings and the Platinum Rewards Card, and the official answer matches. |
| task_068 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 4 | Strict | Yes | The right accounts are clear, but the bank's own procedure tells the agent to name the checking account 'Green Account (checking)', while the answer key only accepts 'Green Account'. |
| task_069 | Blocker | Blocker | Confirmed (Blocker) | - | None | Sufficient | No | 4 | Strict | No | The official answer assumes the Gold savings account has no ATM-fee rebates, but the documents say it does, so the truly best combination (about 5.7% instead of 3.5%) is graded as wrong. |
| task_070 | Major | Minor | Confirmed (Minor) | yes | None | Partial | Yes | 3 | None | Yes | The active November promotion picks Sky Blue among the three accounts that fit, but Sky Blue's startup-age eligibility can't be confirmed because the customer is never told when her business was formed. |
| task_071 | Major | Major | Confirmed (Major) | - | None | Partial | Partial | 4 | None | Yes | The right accounts (Sky Blue and Gold Saver) follow from the active promotions, but the bank's business-savings procedure tells the agent to open it as a personal 'savings' account, which creates the wrong record. |
| task_072 | Major | Minor | Adjusted (Major) | yes | Minor | Sufficient | Yes | 5 | None | Yes | Both refund amounts ($14.00 and $3.50) can be rebuilt from the fee schedules and the 'net correction' rule, but some of the fees that count are dated after the benchmark's fixed 'today'. |
| task_073 | Major | Minor | Adjusted (Major) | - | Major | Sufficient | Yes | 5 | None | Yes | All three refunds ($9.50, $9.00, $1.50) follow from the fee schedules and the documented 'net correction' rule, but some of the errors that count are dated after the benchmark's fixed 'today'. |
| task_074 | Major | Minor | Adjusted (Major) | - | Blocker | Sufficient | Yes | 5 | None | Yes | After the v1.0.1 fix, all four refunds ($27.00, $14.50, $4.75, $3.70) can be rebuilt from the fee documents; one Purple error the gold depends on is dated after the fixed 'today'. |
| task_075 | Major | Blocker | Adjusted (Major) | yes | Blocker | Partial | No | 3 | None | No | Several checking accounts charge $0 for foreign ATM withdrawals, and Purple even refunds operator fees, but the answer key only accepts Green Fee-Free, based on a fee-stacking rule the documents never state. |
| task_076 | Major | Major | Confirmed (Major) | - | None | Partial | Partial | 3 | None | Yes | Purple checking is the sensible answer, but Bluest also gives 2-day early deposit with equal or lower ATM fees and is ruled out only by a $75,000 opening deposit the customer is never asked about. |
| task_077 | Major | Major | Confirmed (Major) | - | None | Partial | Partial | 4 | Strict | Yes | The lost-wallet procedure can be followed step by step, but the replacement card's design is ambiguous: the customer asks for the 'best free option' and no 'fancy design', and the answer key only accepts the PREMIUM design. |
| task_078 | Minor | Minor | Confirmed (Minor) | yes | None | Sufficient | Yes | 4 | Strict | Yes | Lost-wallet task is solvable from the documents, but the graded database records the freeze-then-unfreeze history, so closing the lost cards directly (as one document recommends) fails. |
| task_079 | Major | Minor | Confirmed (Minor) | yes | None | Sufficient | Partial | 5 | Strict | Yes | Stolen-wallet task is solvable, but it records the freeze-then-unfreeze history and leans on reading a pending refund as a refund rather than a pending transaction. |
| task_080 | Minor | Major | Confirmed (Major) | yes | None | Sufficient | Partial | 5 | Strict | No | The gold gives provisional credit on all three credit-card fraud disputes, while the task's own notes and customer script are built around a two-dispute limit that withholds it from the $149.95 charge. |
| task_081 | Minor | Major | Confirmed (Major) | yes | None | Sufficient | Partial | 5 | Strict | No | Same scenario and same provisional-credit mismatch as task_080, and the "transfer only on the fourth request" behavior the task is built to test is not graded. |
| task_082 | Blocker | Blocker | Confirmed (Blocker) | - | Blocker | Partial | No | 5 | Strict | No | Fraud on the Green Fee-Free card maps to close-and-reissue and the customer asks for a new number, but the gold never replaces that card; several other stored dispute fields also have more than one defensible value. |
| task_083 | Blocker | Blocker | Confirmed (Blocker) | - | Blocker | Sufficient | Partial | 4 | Soft | No | This task is graded on exact tool-call text, and the official dispute calls leave out a required field, so they fail when run and no correct call can ever match them. |
| task_084 | Blocker | Blocker | Confirmed (Blocker) | - | Blocker | Sufficient | No | 4 | Strict | No | The stored liability amounts follow no single rule: the $47.50 duplicate gets $50 (not capped) while the $412.88 late fraud gets $412.88 (capped), so any consistent calculation misses one of them. |
| task_085 | Major | Major | Confirmed (Major) | - | Minor | Partial | Partial | 3 | Soft | Yes | The verify-the-customer's-claims flow is sound, but the duplicate-row pick, liability amounts, a provisional-credit flag and an unscripted merchant-contact answer each have more than one defensible stored value. |
| task_086 | Major | Major | Confirmed (Major) | - | Minor | Partial | Partial | 5 | Soft | Yes | The six-dispute workflow is reconstructible, but whether to file the ATM-deposit dispute at all, how to code the skimmed-card fraud, and the liability amounts each have more than one defensible answer. |
| task_087 | Major | Major | Confirmed (Major) | yes | None | Sufficient | Partial | 4 | Soft | Yes | The decline-diagnosis steps are clear, but when the customer reports a fraudulent charge the KB says to escalate to the security team, while the gold files a dispute and replaces the card. |
| task_088 | Major | Major | Confirmed (Major) | - | Minor | Partial | Partial | 4 | Soft | Yes | The KB's chip-mismatch procedure says to freeze the card until a replacement arrives and to follow the stolen-card protocol, while the gold closes it as fraud; the fraud charge's PIN/signature type is also never given. |
| task_089 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 4 | Soft | Yes | ATM-limit task is clean: the only write, a temporary Green-card ATM limit of $900, follows from the documents and the transaction history. |
| task_090 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Partial | 5 | Strict | Yes | The three-card PIN-lock case is solvable as written; the only soft spot is that the Evergreen replacement card has two equally free designs and the customer never picks one. |
| task_091 | Blocker | Blocker | Confirmed (Blocker) | - | None | Partial | No | 5 | Strict | No | The official answer orders the cheapest replacement card although the customer asked for the most premium free one, and it orders a Light Blue replacement that the rules say must wait 48 hours. |
| task_092 | Major | Minor | Not sampled (-) | yes | Minor | Sufficient | Partial | 5 | Strict | Yes | The four-card case is reachable because the customer's scripted answers steer each card, but the rule for a single 3-point risk flag never says whether to unlock, transfer, or replace. |
| task_093 | Minor | Minor | Confirmed (Minor) | yes | None | Sufficient | Yes | 3 | Soft | Yes | The Silver savings interest correction ($33.00) is derivable from the documents; one required document contains an unfilled template placeholder. |
| task_094 | Major | Major | Confirmed (Major) | - | Minor | Sufficient | Partial | 4 | Soft | Yes | The Gold Rewards Card's 0.025% bonus is described both as a card bonus (outranked by the EcoCard) and as a separate relationship bonus that stacks, so the correct credit could be $140 or $142. |
| task_095 | Major | Major | Confirmed (Major) | - | Major | Sufficient | Partial | 4 | Soft | Yes | As in task_094, the documents disagree on whether the Gold Rewards Card's 0.025% stacks, so the correct credit could be $98 or $100. |
| task_096 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 5 | Soft | Yes | Both savings corrections ($17.50 Bronze, $15.00 Gold Plus) follow directly from the documented rates and the highest-only stacking rules. |
| task_097 | Blocker | Blocker | Confirmed (Blocker) | yes | Major | Sufficient | No | 5 | Soft | No | For the Silver account, the official credit leaves out a 0.025% relationship bonus that this task's own document grants (and that task_093 applies), and the cent amount also depends on the rounding method. |
| task_098 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 3 | None | Yes | Blue Account is the single best combined referral bonus ($65) the friend's $600 deposit qualifies for, and the 9-day window still has room. |
| task_099 | Minor | Minor | Confirmed (Minor) | yes | None | Sufficient | Yes | 3 | None | Yes | World Blue ($300) is the best referrer bonus a $30,000 deposit qualifies for; the only soft spots are a corrupted value and "international businesses" wording in the World Blue documents. |
| task_100 | None | Minor | Not sampled (-) | yes | Minor | Sufficient | Yes | 3 | None | Yes | Hunter Green ($175) is correct once tenure is measured from the on-file account date; the customer's claim of "mid-July" is a resolvable red herring. |
| task_101 | Major | Minor | Confirmed (Minor) | yes | Blocker | Sufficient | Partial | 5 | None | Yes | Purple plus Sky Blue is the right pair once the 2-per-9-days referral cap is applied to the new batch; the policy wording that justifies the cap is slightly loose. |
| task_102 | Blocker | Major | Confirmed (Major) | yes | Major | Partial | Partial | 5 | None | Yes | With only one referral slot, the customer asks to "maximize the bonus" without saying whose bonus; the official TechFlow-to-Sky Blue pick wins on combined bonus but loses to Ember-to-Lime Green on her own bonus. |

## Findings (Blocker and Major)

### task_010 — Major

**The diagnosis (weekly referral cap) is clear, but if the agent helps the customer retry the referral the way the KB documents, by handing over the referral-link tool, the gold scores that as wrong.**

- **non_determinism (Major)** — To retry a credit-card referral, the KB documents one mechanism: give the customer the get_referral_link user tool. The gold instead expects the customer to call submit_referral, a native user tool the KB never mentions. Handing over get_referral_link writes a user_discoverable_tools row the gold lacks, which fails DB grading.
  - doc_credit_cards_credit_cards_(general)_009: "Provide the customer with this tool and instruct them to run it themselves: `get_referral_link(user_id: str, card_name: str)`"
  - doc_credit_cards_credit_cards_(general)_002: "If a referral is denied for hitting the limit, wait until enough time has passed to drop under the cap before attempting another."
  - `grep of documents/: "submit_referral" appears in no KB document; "get_referral_link" appears only in credit_cards_(general)_009`
  - `task_010 user_tools = ["apply_for_credit_card", "submit_referral"] (no call_discoverable_user_tool)`
  - `Replay: gold + give_discoverable_user_tool(get_referral_link) -> verified match False, reason "table user_discoverable_tools differs"`
  - *Why it matters:* An agent that tells Wei Chen he can now retry the Platinum referral and, following the internal referral-link doc, gives him the tool to do it fails, even though the customer still submits the gold referral. Only an agent that explains and leaves the mechanism to the customer passes, so a KB-faithful helpful step is penalized.
  - *Fix:* Either add give_discoverable_user_tool(get_referral_link) and the matching user call to the gold (and give the user call_discoverable_user_tool), or document submit_referral in the KB as the way to re-submit a rejected referral.

*Verifier: Confirmed (Major → Major).* Reproduced the failure exactly. The KB documents get_referral_link as the way a customer creates a referral, and the policy says to give a tool when the user wants an action and the KB has one; the gold expects the customer to use an undocumented native submit_referral. Two document-supported behaviours lead to different graded states, so Major per calibration.

### task_014 — Major

**The gold requires a transfer to a human, but the KB's internal referral-link procedure says that for a card with no documented referral program the agent must explain and must not transfer.**

- **document_contradiction (Blocker)** — The customer asks for a referral link for the Crypto-Cash Back card, which has no documented referral program. The referral-link procedure says not to transfer in exactly this case; the gold's only graded action is a transfer.
  - doc_credit_cards_credit_cards_(general)_009: "If no referral program is documented for the requested card, or if the user's claimed terms are incorrect, or if there is reason to believe the referral will be automatically rejected, explain why and do not provide a referral link tool. Do not transfer to a human in these cases."
  - `task_014 user_scenario opening line: "How can I get a referral link for this offer so that I can share it with friends?"`
  - `grep of documents/: no Crypto-Cash Back referral document exists (referral docs exist for Platinum, Silver, EcoCard and business cards only)`
  - doc_bank_accounts_bank_accounts_(general)_042 Tier 2: "unconfirmed_external_communication | Customer claims a specific promotion/program/offer exists (they have a letter, email, or flyer) but you cannot verify or find it in the KB after searching"
  - `policy_header.md guideline 5: transfer guidance "may be overridden by specific scenario-based transfer guidance in the knowledge base"`
  - `gold[0] transfer_to_human_agents reason = "unconfirmed_external_communication"; reward_basis = ["ACTION"]`
  - `task_015 (same customer, identical opening message) gold contains no transfer, consistent with credit_cards_(general)_009`
  - *Why it matters:* The customer's literal request ("referral link") is the title topic of credit_cards_(general)_009, so retrieval is likely to surface it, and the system policy says scenario-specific KB transfer guidance overrides the default. An agent that follows it explains and does not transfer. The scenario only has the customer accept a transfer the agent offers; it never has her demand one, so the episode ends with no transfer and ACTION reward 0. Only agents that miss or ignore the doc pass.
  - *Fix:* Either change the gold to no transfer (grade with an NL assertion that the agent explained the program is undocumented and gave no link tool), or narrow the "Do not transfer" sentence in credit_cards_(general)_009 to exclude customers citing an unverifiable official communication, and add credit_cards_(general)_009 to required_documents.
- **document_contradiction (Minor)** — Two codes in the transfer-reason table overlap. The Tier 1 customer_demands_after_unavailable_offer_refusal also covers a customer who persists about an offer the agent cannot find, and Tier 1 outranks the gold's Tier 2 code. Only the clause "now demands human", absent here because the customer merely accepts an offered transfer, keeps Tier 2 correct.
  - `doc_bank_accounts_bank_accounts_(general)_042: "always select from the highest tier that applies"`
  - `doc_bank_accounts_bank_accounts_(general)_042 Tier 1: "customer persisted multiple times, and now demands human"`
  - `task_014 user_scenario: "Express confusion since you have the letter 'right here'" / "Ask them to double-check or look harder" / "Accept the transfer"`
  - *Why it matters:* An agent that reads the customer's persistence as satisfying Tier 1 picks it under the highest-tier rule and fails ACTION grading; task_008 grades the near-identical flyer case the other way.
  - *Fix:* Make the boundary between the two codes explicit in credit_cards_(general)_042 (who initiates the transfer, how many refusals).

*Verifier: Adjusted (Blocker → Major).* The contradiction is real: doc_009 forbids a transfer for an undocumented referral program, while doc_042 defines a transfer code for exactly this letter-claim scenario and the policy default offers a transfer when an issue cannot be resolved. The gold follows the doc_042 reading, which the documents support, so per calibration ('two document-supported readings ... Major; Blocker only when the gold follows no reading the documents support') this is Major, not Blocker. doc_009 is also absent from required_documents, so the golden_retrieval config naturally reaches the gold. The secondary Tier 1/Tier 2 overlap issue (Minor) holds.

### task_017 — Major

**Under the bank's documented round-down rule, a third transaction (Hilton, over-credited by 1 point) is also wrong, but the gold disputes only two, so an agent that flags every error fails.**

- **argument_error (Major)** — The seed stores 1159 points on txn_31fd03682992 (Hilton Seattle, $289.50, Travel, Silver 4%). 289.50 x 4 = 1158.00 exactly, so the stored value is 1 point too high under any rounding rule. The gold dispute set leaves this transaction out.
  - db.json credit_card_transaction_history[txn_31fd03682992] = {merchant 'Hilton Seattle', transaction_amount '$289.50', category 'Travel', rewards_earned '1159 points'}
  - `doc_credit_cards_silver_rewards_card_002: "Pay with your card for eligible travel and software transactions to earn 4.0% back"`
  - doc_credit_cards_credit_cards_(general)_003: "Use this process when a customer believes there is a discrepancy between the cash back they received for a particular transaction and the cash back they should have received."
  - `gold[2], gold[3] dispute only txn_cfabb609133d and txn_913d14a20dc5`
  - `task_017 instructions: "you want the agent to investigate and help you fix any errors"`
  - *Why it matters:* An agent that compares every transaction against the documented rates finds three discrepancies (Amazon stored 15 vs 156, Sushi Kashiba stored 47 vs 87, Hilton stored 1159 vs 1158). If it has the customer dispute all three, cash_back_disputes and user_discoverable_tool_calls each gain a row, and replay shows the verified comparison fails on those two tables. Elsewhere the benchmark treats over-credits as dispute-worthy: task_018 has the customer insist on disputing an overpaid transaction, and task_020 disputes an over-credited one. The gold passes only for agents that choose not to dispute a 1-point over-credit, a choice nothing in the documents supports.
  - *Fix:* Set txn_31fd03682992.rewards_earned to '1158 points', or add it to the gold dispute set.
- **document_gap (Minor)** — The floor-rounding policy doc that decides which transactions are discrepant (doc_credit_cards_credit_cards_(general)_007) is not listed in required_documents, so the golden_retrieval config, which inlines only required_documents and exposes no search tool, never shows it to the agent.
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - `task_017.required_documents = [general_003, general_006, silver_rewards_card_001, silver_rewards_card_002] (no general_007)`
  - `src/tau2/domains/banking_knowledge/retrieval_toolkits.py: KnowledgeToolsPlain 'Used by: no_knowledge, full_kb, golden_retrieval' (no retrieval tools)`
  - *Why it matters:* Without doc_007, an agent naturally rounds half-up: txn_cedd88ce1f65 (Adobe, $54.99 x 4 = 219.96, stored 219) then looks under-credited and gets disputed. This applies only to the golden_retrieval config.
  - *Fix:* Add doc_credit_cards_credit_cards_(general)_007 to required_documents.

*Verifier: Confirmed (Major → Major).* Reproduced both issues. The Hilton over-credit is a discrepancy under any rounding rule; disputing it is the documented process and the customer asks to fix 'any errors', so a gold that omits it rewards only agents that skip 1-point favourable errors. Major is consistent with the same class in task_020/026; the required_documents omission is Minor per calibration.

### task_020 — Major

**This customer's stored rewards use normal rounding while the bank's policy doc says rewards are always rounded down, so an agent following the policy flags nine extra 1-point over-credits.**

- **document_contradiction (Major)** — This customer's seed rewards are rounded half-up, but doc_007 says rewards are always floored. Under the documented rule, nine non-gold transactions are over-credited by 1 point each, and the gold disputes none of them.
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - db.json credit_card_transaction_history (user 755bcb4d5d), floor value vs stored: txn_a8f1c2d3e402 (Adobe $54.99 x 20% = 1099.8, stored 1100); txn_a8f1c2d3e404 (Microsoft 365 $79.99 x 2% = 159.98, stored 160); txn_a8f1c2d3e406 (Whole Foods $127.43 x 2% = 254.86, stored 255); txn_a8f1c2d3e409 (Amazon $156.78 x 2% = 313.56, stored 314); txn_a8f1c2d3e414 (Coursera $49.99 x 1% = 49.99 pts, stored 50); txn_b7e2d4c5f503 (Slack $44.99 x 4% = 179.96, stored 180); txn_b7e2d4c5f507 (Netflix $22.99 x 1%, stored 23); txn_b7e2d4c5f509 (Costco $143.56 x 1%, stored 144); txn_b7e2d4c5f512 (Nordstrom $187.50 x 1%, stored 188)
  - `gold disputes txn_b7e2d4c5f506 (GitHub, stored 2550 vs correct 1020), an over-credit, so in this task over-credits are dispute-worthy`
  - doc_credit_cards_credit_cards_(general)_003: "Use this process when a customer believes there is a discrepancy between the cash back they received for a particular transaction and the cash back they should have received."
  - *Why it matters:* An agent that applies the documented floor rule finds 13 discrepancies. If it disputes all of them, as it disputes the GitHub over-credit, cash_back_disputes and user_discoverable_tool_calls gain rows the gold lacks; replay shows the verified comparison fails (tested with txn_a8f1c2d3e402 added). The gold is reachable only by ignoring doc_007 and rounding half-up, or by deciding without documentary support not to dispute 1-point over-credits. Other tasks in this family (018, 019, 021, 022) store floor values, so the seed is internally inconsistent.
  - *Fix:* Re-seed the nine rows with floor values (1099, 159, 254, 313, 49, 179, 22, 143, 187), or state a materiality threshold in the dispute doc.

*Verifier: Confirmed (Major → Major).* Reproduced every number. This user's seed is rounded half-up while doc_007 mandates floor and the sibling tasks 018/019/021/022 store floor values; a doc-faithful agent that disputes over-credits (as the gold does for GitHub) fails. Major is consistent with task_017.

### task_024 — Major

**The gold card (Business Bronze, $900 back) beats every card except the Silver Zoom Card, whose triple-cash-back promo pays at least $1,200 on the truck; the docs never say whether a landscaping company can get that card.**

- **non_determinism (Major)** — The Silver Zoom Card's live triple-cash-back promo pays 3 x 1.0% = 3% on a non-category purchase: $1,200 on the $40,000 truck, or 9% if a work vehicle counts as transportation spend. Minus the $74.50 annual fee, that still beats Business Bronze's 1% + $500 = $900. Whether a landscaping company is eligible is implied by 'designed for transportation and logistics businesses' but never stated as a restriction.
  - doc_business_credit_cards_silver_zoom_card_012: "You must claim the promotion within the window starting 2024-01-01 and ending 2025-12-31" and "All other eligible purchases earn 3 × 1.0% during the promo period"
  - doc_business_credit_cards_silver_zoom_card_001: "Established transportation and logistics operators that can meet both personal and business credit criteria" and "Annual membership is $74.50"
  - `doc_business_credit_cards_silver_zoom_card_008 title: "Silver Zoom Card: Eligibility Requirements for Logistics Businesses"`
  - doc_business_credit_cards_business_bronze_rewards_card_010: "This offer is available from 2025-10-01 through 2026-03-31." / "After qualification, a $500 statement credit will be applied to your account."
  - `task_024 persona: "You run a landscaping company ... and are looking to expand your fleet."`
  - `gold[0].arguments.card_type = "Business Bronze Rewards Card"`
  - *Why it matters:* An agent that treats Silver Zoom as open to any business recommends it, the customer applies for 'Silver Zoom Card', and credit_card_applications differs from the gold (replay confirmed). The gold is reachable only if the agent reads the card as limited to transportation/logistics operators. The documents frame it that way but never say other businesses are ineligible, and the persona's 'expand your fleet' points toward the fleet card.
  - *Fix:* State in silver_zoom_card_001/008 that only transportation/logistics businesses are eligible, or end the triple-cash-back claim window before 2025-11-14.

*Verifier: Confirmed (Major → Major).* Reproduced. Only an eligibility reading (Silver Zoom is framed for logistics operators but never states a restriction) separates the gold from a higher-paying card. Two document-supported readings with different graded states: Major.

### task_025 — Major

**The gold card (Business Platinum) wins only if an Apple Music subscription earns its 4% 'software/media advertising' rate; the docs disagree on whether streaming is 'Media' or 'Entertainment', and the strict reading drops Platinum to a tie or a loss.**

- **document_contradiction (Major)** — Business Platinum's 4% rate covers 'Travel, software, and media advertising purchases'. The media doc lists only advertising buys, and the two category docs disagree on whether streaming services are Media or Entertainment. So whether a $100,000 Apple Music license earns 4% ($4,000) or 1.5% ($1,500) is not determined.
  - doc_business_credit_cards_business_platinum_rewards_card_002: "Travel, software, and media advertising purchases earn 4.0%." / "Purchases outside those categories earn 1.5%."
  - `doc_business_credit_cards_business_platinum_rewards_card_003: "Streaming audio and video media placements when billed by media networks or ad platforms."`
  - `doc_credit_cards_credit_cards_(general)_005: "Media (advertising spend, streaming services)"`
  - doc_credit_cards_credit_cards_(general)_019: "**Entertainment**: Movies, concerts, sporting events, and streaming services" vs "**Media**: Advertising spend and digital media purchases"
  - `doc_business_credit_cards_business_silver_rewards_card_005: "**Hardware/Electronics Merchants (Software Exclusion):**" lists "Apple"`
  - `gold[0].arguments.card_type = "Business Platinum Rewards Card"`
  - *Why it matters:* Gold reading: Apple Music is Media (general_005) or software, so Platinum pays 4% = $4,000. Business Silver is excluded via 'Apple', giving 1% (2% if the double promo still applies on its last day) = $1,000-$2,000. Bronze is 1% + $500 = $1,500, so Platinum wins. Strict reading: a subscription is not 'media advertising' (platinum_003), and general_019 classes streaming as Entertainment, so Platinum pays 1.5% = $1,500, tying Bronze and losing to Business Silver if the double promo applies. If an agent instead treats Apple Music as software without applying the 'Apple' merchant exclusion, Business Silver pays 10%+ and wins. Any of these recommendations changes credit_card_applications and fails.
  - *Fix:* Make the purchase unambiguously a Platinum 4% category (for example a cloud/SaaS vendor), or state in platinum_002/003 that consumer streaming subscriptions earn 4%, and resolve the general_005/general_019 Media-vs-Entertainment conflict.

*Verifier: Confirmed (Major → Major).* Reproduced. The gold is reachable via the Software (platinum_007 'enterprise software licenses') or Media (general_005) reading, but general_019 classes streaming as Entertainment, under which Platinum ties Bronze. Two document-supported readings: Major.

### task_026 — Blocker

**The gold writes 1500 points for a transaction that the bank's own rounding policy says earns 1499, and it expects the agent to confirm the disputes are resolved when no agent tool can see dispute status.**

- **document_contradiction (Blocker)** — Gold action 10 sets txn_a8f1c2d3e411 (Zoom Video, $149.99, Business Silver 10% after the promo) to '1500 points'. 149.99 x 10 = 1499.9, which doc_007 floors to 1499. The gold value is rounded half-up, against the documented policy.
  - `gold[10].arguments.arguments = "{\"transaction_id\": \"txn_a8f1c2d3e411\", \"new_rewards_earned\": \"1500 points\"}"`
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - `doc_credit_cards_credit_cards_(general)_004: "new_rewards_earned: a string formatted as 'X points' where X is the correct whole-number point value"`
  - db.json credit_card_transaction_history[txn_a8f1c2d3e411].transaction_amount = "$149.99", transaction_date "09/15/2025" (after the 08/13/2025 end of the 6-month double promo for an account opened 02/13/2025)
  - *Why it matters:* An agent that follows the documented rounding policy writes '1499 points'. credit_card_transaction_history is compared exactly under the verified scorer (only closure_reason and the discoverable-tools log are relaxed), and replay shows that state fails. Policy-faithful work fails deterministically.
  - *Fix:* Change gold[10] to '1499 points' (and re-seed the half-up rows per task_020), or change doc_007 to round half-up across the benchmark.
- **underspecified_instructions (Major)** — Phase 2 requires the agent to update rewards only after the disputes are resolved, and doc_004 says to confirm resolution in the cash_back_disputes table. The agent has no tool that reads that table and never sees the user's tool output, so its only evidence is the customer's word. task_027 has an identical customer message and expects the opposite action.
  - doc_credit_cards_credit_cards_(general)_004: "Look up the user’s resolved disputes in the cash_back_disputes database to find the transaction_id values that need rewards adjustments."
  - src/tau2/domains/banking_knowledge/tools.py: the only reference to cash_back_disputes is the user-side submit_cash_back_dispute_0589 write (line ~4231); no agent tool or discoverable agent tool reads that table (get_user_dispute_history_7291 reads transaction_disputes only), and query_database exists only on KnowledgeUserTools
  - src/tau2/orchestrator/orchestrator.py: tool results for user tool calls are routed ENV -> USER only; the agent receives only the user's text messages, so it never sees the "Status: RESOLVED"/"Status: SUBMITTED" line the dispute tool returns
  - task_026 Phase 2 line: "Great, I've submitted all the disputes. I just got a notification that they've all been approved and resolved!" (task_027 Phase 2 uses the same sentence as a lie)
  - initial_state.initialization_data.agent_data.task_config.dispute_settings.auto_resolve_disputes = true (026) vs false (027): replay shows statuses RESOLVED (026) vs SUBMITTED (027), invisible to the agent
  - *Why it matters:* An agent that follows doc_004 and declines to update without confirming resolution misses update_transaction_rewards_3847 and the four transaction changes; replay confirms the verified comparison fails ('missing required discoverable calls' plus a credit_card_transaction_history diff). Any fixed policy passes at most one of task_026 and task_027, since the observable conversation is the same.
  - *Fix:* Give the agent a read tool for cash_back_disputes (and document it in doc_004), so 026 and 027 differ in observable state.
- **document_contradiction (Major)** — This customer's seed rewards are rounded half-up, but doc_007 says rewards are always floored. Under the documented rule, nine non-gold transactions are over-credited by 1 point each, and the gold disputes none of them.
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - db.json credit_card_transaction_history (user 755bcb4d5d), floor value vs stored: txn_a8f1c2d3e402 (Adobe $54.99 x 20% = 1099.8, stored 1100); txn_a8f1c2d3e404 (Microsoft 365 $79.99 x 2% = 159.98, stored 160); txn_a8f1c2d3e406 (Whole Foods $127.43 x 2% = 254.86, stored 255); txn_a8f1c2d3e409 (Amazon $156.78 x 2% = 313.56, stored 314); txn_a8f1c2d3e414 (Coursera $49.99 x 1% = 49.99 pts, stored 50); txn_b7e2d4c5f503 (Slack $44.99 x 4% = 179.96, stored 180); txn_b7e2d4c5f507 (Netflix $22.99 x 1%, stored 23); txn_b7e2d4c5f509 (Costco $143.56 x 1%, stored 144); txn_b7e2d4c5f512 (Nordstrom $187.50 x 1%, stored 188)
  - `gold disputes txn_b7e2d4c5f506 (GitHub, stored 2550 vs correct 1020), an over-credit, so in this task over-credits are dispute-worthy`
  - doc_credit_cards_credit_cards_(general)_003: "Use this process when a customer believes there is a discrepancy between the cash back they received for a particular transaction and the cash back they should have received."
  - *Why it matters:* An agent that applies the documented floor rule finds 13 discrepancies. If it disputes all of them, as it disputes the GitHub over-credit, cash_back_disputes and user_discoverable_tool_calls gain rows the gold lacks; replay shows the verified comparison fails (replay-tested on task_020, which has the same seed and Phase 1 gold). The gold is reachable only by ignoring doc_007 and rounding half-up, or by deciding without documentary support not to dispute 1-point over-credits. Other tasks in this family (018, 019, 021, 022) store floor values, so the seed is internally inconsistent.
  - *Fix:* Re-seed the nine rows with floor values (1099, 159, 254, 313, 49, 179, 22, 143, 187), or state a materiality threshold in the dispute doc.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced all three issues. The gold write value is the half-up 1500 while the only documented rounding rule gives 1499, so the gold follows no document-supported reading and policy-faithful work fails deterministically: Blocker. The unverifiable 'disputes resolved' claim (Major, twin of task_027) and the half-up seed (Major, same as task_020) hold.

*Reconciled across runs: Blocker → Blocker (none (already agreed)).* Included for 026-029 consistency; both runs already agree. The dispute-status defect is Major here as in 027-029, but gold[10] writes '1500 points' where the only documented rounding rule gives 1499, so the gold follows no document-supported reading. credit_card_transaction_history is compared exactly under both scorers.

### task_027 — Major

**The task tests whether the agent checks that the disputes are really resolved before updating rewards, but no agent tool can see dispute status, and its twin task_026 rewards the opposite choice for the same conversation.**

- **underspecified_instructions (Major)** — The author's note says 'Agent must verify dispute status and refuse to update transactions when disputes are still SUBMITTED', but no agent tool reads cash_back_disputes and the agent never sees the user's tool output. The only signal is the customer's claim, word-for-word the same as task_026's truthful claim.
  - `task_027 description.notes: "Agent must verify dispute status and refuse to update transactions when disputes are still SUBMITTED (not RESOLVED)."`
  - doc_credit_cards_credit_cards_(general)_004: "Look up the user’s resolved disputes in the cash_back_disputes database to find the transaction_id values that need rewards adjustments."
  - src/tau2/domains/banking_knowledge/tools.py: the only reference to cash_back_disputes is the user-side submit_cash_back_dispute_0589 write (line ~4231); no agent tool or discoverable agent tool reads that table (get_user_dispute_history_7291 reads transaction_disputes only), and query_database exists only on KnowledgeUserTools
  - src/tau2/orchestrator/orchestrator.py: tool results for user tool calls are routed ENV -> USER only; the agent receives only the user's text messages, so it never sees the "Status: RESOLVED"/"Status: SUBMITTED" line the dispute tool returns
  - `replay: after the gold, all four cash_back_disputes rows for 755bcb4d5d have status SUBMITTED (auto_resolve_disputes = false)`
  - *Why it matters:* The gold (no updates) is reachable by an agent that refuses to update without confirming resolution, a reading doc_004 supports. An agent that trusts the customer, which task_026 requires, unlocks and calls update_transaction_rewards_3847; replay confirms credit_card_transaction_history then differs and the verified comparison fails. The task cannot test what its note says, and an agent's score on the 026/027 pair depends on a disposition the materials cannot settle.
  - *Fix:* Give the agent a read tool for cash_back_disputes (document it in doc_004) so the SUBMITTED status is observable.
- **document_contradiction (Major)** — This customer's seed rewards are rounded half-up, but doc_007 says rewards are always floored. Under the documented rule, nine non-gold transactions are over-credited by 1 point each, and the gold disputes none of them.
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - db.json credit_card_transaction_history (user 755bcb4d5d), floor value vs stored: txn_a8f1c2d3e402 (Adobe $54.99 x 20% = 1099.8, stored 1100); txn_a8f1c2d3e404 (Microsoft 365 $79.99 x 2% = 159.98, stored 160); txn_a8f1c2d3e406 (Whole Foods $127.43 x 2% = 254.86, stored 255); txn_a8f1c2d3e409 (Amazon $156.78 x 2% = 313.56, stored 314); txn_a8f1c2d3e414 (Coursera $49.99 x 1% = 49.99 pts, stored 50); txn_b7e2d4c5f503 (Slack $44.99 x 4% = 179.96, stored 180); txn_b7e2d4c5f507 (Netflix $22.99 x 1%, stored 23); txn_b7e2d4c5f509 (Costco $143.56 x 1%, stored 144); txn_b7e2d4c5f512 (Nordstrom $187.50 x 1%, stored 188)
  - `gold disputes txn_b7e2d4c5f506 (GitHub, stored 2550 vs correct 1020), an over-credit, so in this task over-credits are dispute-worthy`
  - doc_credit_cards_credit_cards_(general)_003: "Use this process when a customer believes there is a discrepancy between the cash back they received for a particular transaction and the cash back they should have received."
  - *Why it matters:* An agent that applies the documented floor rule finds 13 discrepancies. If it disputes all of them, as it disputes the GitHub over-credit, cash_back_disputes and user_discoverable_tool_calls gain rows the gold lacks; replay shows the verified comparison fails (replay-tested on task_020, which has the same seed and Phase 1 gold). The gold is reachable only by ignoring doc_007 and rounding half-up, or by deciding without documentary support not to dispute 1-point over-credits. Other tasks in this family (018, 019, 021, 022) store floor values, so the seed is internally inconsistent.
  - *Fix:* Re-seed the nine rows with floor values (1099, 159, 254, 313, 49, 179, 22, 143, 187), or state a materiality threshold in the dispute doc.

*Verifier: Confirmed (Major → Major).* Reproduced both Major issues. The agent cannot observe dispute status, so the no-update gold depends on the agent's default trust level, and the gold's Phase 1 dispute set matches half-up rounding, not the documented floor rule. The twin task_026 (not assigned) even stores a half-up update value ('1500 points' for Zoom, floor gives 1499), which confirms that this task family was built with half-up rounding. Both issues are writes compared exactly, so the verified scorer does not change them.

*Reconciled across runs: Major → Major (judgment).* The deciding fact (cash_back_disputes.status SUBMITTED) is invisible to the agent: no agent tool reads that table and user-tool output is routed only to the user. But the no-update gold is reachable by a document-supported reading (doc_004 requires a resolved-dispute lookup the agent cannot perform, so it declines), and updating on the customer's word is the competing reading that task_026/028 reward. Calibration: two document-supported readings with different graded states is Major; Blocker is reserved for a gold that follows no supported reading, which is not the case here. The separate half-up seed vs doc_007 floor contradiction is also Major in both runs, so the task is Major under both scorers (all affected tables are writes compared exactly).

### task_028 — Major

**The agent is expected to update the customer's rewards because she says her disputes were approved, but it has no way to check that, and task_029 shows it the same conversation and expects it to refuse.**

- **underspecified_instructions (Major)** — Phase 2 gold (update_transaction_rewards_3847 x6) depends on the disputes being RESOLVED, but the documented verification step reads a table no agent tool can access, so the agent must act on the customer's unverifiable claim. task_029 gives the agent the same Phase 2 message and expects the opposite outcome (no updates).
  - doc_credit_cards_credit_cards_(general)_004: "Look up the user's resolved disputes in the cash_back_disputes database to find the transaction_id values that need rewards adjustments."
  - tools.py: no KnowledgeTools (agent) method reads cash_back_disputes; only KnowledgeUserTools.submit_cash_back_dispute_0589 writes it, and its 'Status: RESOLVED' output goes only to the user (orchestrator routes ENV->USER for user tool calls).
  - task_028 user_scenario Phase 2: "I just got a notification that they've all been approved and resolved!" (identical text in task_029, where gold has no updates and auto_resolve_disputes=false)
  - `Replay: dropping gold[8..14] (refusing agent) -> verified match False: missing update_transaction_rewards_3847, credit_card_transaction_history differs`
  - *Why it matters:* A cautious agent that follows doc_004 and declines to update without confirming resolution fails this task; a trusting agent passes it but fails task_029. Agent-visible input in Phase 2 is the same in both tasks, so no single competent policy passes both.
  - *Fix:* Give the agent a read tool for cash_back_disputes (e.g., a discoverable get_cash_back_disputes tool documented in doc_004), or show the dispute status in an agent-visible tool output, so 028 vs 029 is decided by data the agent can check.
- **document_contradiction (Minor)** — Rate and rounding docs the agent needs have cosmetic corruptions, but the stored seed values resolve them: EcoCard rates are written as dollar amounts, and the rounding example's arithmetic does not follow.
  - `doc_credit_cards_ecocard_002: "Green purchases: Earn $5.00 sustainability points per dollar spent"`
  - `doc_credit_cards_credit_cards_(general)_007: "126.77 × 0.01 = 1.2677 points, which rounds down to 1 point per dollar, giving 126 points"`
  - `db.json credit_card_transaction_history[txn_e83813b6528a] (EcoCard Green $147.63) rewards_earned = "738 points" = floor(147.63*5)`
  - *Why it matters:* Does not change the correct values: both doc_007 examples conclude floor(amount x rate-in-percent), and the 41 correctly-stored transactions confirm the convention.
  - *Fix:* Write EcoCard rates as "5 points per dollar" / "1 point per dollar" and fix doc_007's first example to "126.77 x 1 = 126.77 points, rounded down to 126".

*Verifier: Confirmed (Major → Major).* Phase 1 is fully derivable. Phase 2 requires acting on the customer's word, which is the reverse of task_029's gold for the same agent-visible message, so Major under the two-readings rule. The cosmetic EcoCard '$5.00' rate stays Minor because it decides one gold dispute.

*Reconciled across runs: Major → Major (judgment).* Same unobservable-dispute-status defect as 027/029, mirrored: the gold updates six transactions on the customer's unverifiable claim while task_029 expects refusal on identical agent-visible input. Updating is document-supported (the agent already holds the transaction ids that doc_004's lookup exists to find), and declining is the competing supported reading, so calibration gives Major, not Blocker. Run U's verifier raised it to Blocker only to match U's 026/027 ratings, which this reconciliation also sets to Major for this defect; the Phase-1 floor arithmetic reproduces exactly, and the EcoCard '$5.00 points' corruption stays Minor.

### task_029 — Major

**The test is whether the agent catches the customer lying that her disputes were approved, but the agent has no tool that shows dispute status, so passing depends on whether it refuses unverifiable requests by default.**

- **underspecified_instructions (Major)** — The discriminating fact (disputes still SUBMITTED) exists only in the cash_back_disputes table and in user-side tool output, neither of which the agent can see. The agent receives the same Phase 2 claim as in task_028, where gold expects the updates.
  - `task_029 description.notes: "Agent must verify dispute status and refuse to update transactions when disputes are still SUBMITTED"`
  - `doc_credit_cards_credit_cards_(general)_004: "Look up the user's resolved disputes in the cash_back_disputes database"`
  - `tools.py: no agent tool queries cash_back_disputes; submit_cash_back_dispute_0589 'Status: SUBMITTED' output is returned only to the user`
  - `Replay: gold + task_028's update calls -> verified match False (credit_card_transaction_history differs)`
  - *Why it matters:* An agent that refuses because it cannot do doc_004 step 1 passes, but the same agent fails task_028, and an agent that trusts the customer passes 028 and fails here. The task measures how much the agent trusts customers by default, not whether it verifies, because verification is impossible.
  - *Fix:* Same as task_028: expose dispute status through an agent-readable tool documented in doc_004 so the agent can actually verify the claim.
- **document_gap (Minor)** — Choosing the 6 disputes depends on the floor-rounding rule in doc_007, which is in the KB but missing from this task's required_documents (task_028 lists it).
  - `task_029 required_documents omits "doc_credit_cards_credit_cards_(general)_007"`
  - `doc_007: "All credit card rewards points are rounded down to the nearest whole number."`
  - `Computation: floor -> 6 mismatches (= gold set); round-half-up -> 28 mismatches`
  - *Why it matters:* With search-based retrieval the agent can still find doc_007 (and stored values on correct rows are visibly floored), so standard runs are unaffected. Under golden_retrieval / required-docs variants the rule is absent, and a round-half-up agent would dispute 22 extra transactions.
  - *Fix:* Add doc_credit_cards_credit_cards_(general)_007 to task_029 required_documents.
- **document_contradiction (Minor)** — Same cosmetic corruptions as task_028 (EcoCard rates written as dollar amounts, garbled arithmetic in the rounding example). The seed data resolves them.
  - `doc_credit_cards_ecocard_002: "Earn $5.00 sustainability points per dollar"`
  - `doc_007: "126.77 × 0.01 = 1.2677 points, which rounds down to 1 point per dollar, giving 126 points"`
  - *Why it matters:* Does not change the dispute set.
  - *Fix:* As in task_028.

*Verifier: Confirmed (Major → Major).* Reproduced. This is the mirror of task_028: the gold (no updates) is reachable only by declining an unverifiable claim. The missing-required-doc issue is Minor per calibration, since search retrieval still finds doc_007.

*Reconciled across runs: Major → Major (none (already agreed)).* Both runs already agree; kept for 026-029 consistency. The refuse-to-update gold depends on a status no agent tool exposes, while task_028 rewards updating on the same message: two document-supported readings, Major. The doc_007 omission from required_documents (Minor) and the EcoCard '$5.00' corruption (Minor) stand.

### task_039 — Major

**The written rule says a customer with no past disputes qualifies for provisional credit, but the official answer denies it on the fourth qualifying dispute, which only makes sense if disputes filed earlier in the same call count and are filed in a particular order.**

- **non_determinism (Blocker)** — doc_015 criterion 4 ("has not filed more than 2 disputes in the past 12 months") supports two readings. Read as a pre-session history check, it passes all four fraud/duplicate disputes (user has 0 prior disputes). Read as a running count that includes disputes filed earlier in the session, only the first three filed qualify. The gold uses the running count and also depends on a filing order (eligible disputes first, by descending amount) that the KB never prescribes.
  - `doc_credit_cards_credit_cards_(general)_015: "4. Previous Disputes: The customer has not filed more than 2 disputes in the past 12 months"`
  - `db.json transaction_disputes has no record for user 01f21c9970 (gold[2] history read returns none)`
  - gold[6..8] eligible=true for txn_f7ce44574766 ($312.87 dup), txn_a450807f1148 ($234.56 fraud), txn_182e896e1c97 ($215.67 dup); gold[9] eligible=false for txn_2f16599b9075 ($129.45 fraud), which meets every other criterion (Gold tier max $10000, acct opened 06/15/2024, fraud needs no merchant contact)
  - task_039 description.notes: "maximum 3 disputes can receive provisional credit (the policy states 'has not filed more than 2 disputes' which means up to 2 prior disputes is allowed" (author interpretation, not KB text); 'provisional_credit_max' appears in no doc or code
  - Replay: same disputes with all four reason-eligible = true -> verified match False (transaction_disputes differs); reversing filing order with gold flags -> match True (order matters only through the flags)
  - *Why it matters:* An agent that checks the history once (0 prior disputes, as gold[2] itself does) and applies the criteria writes eligible=true on all four and fails. Even agents using the running count fail unless they file the four reason-eligible disputes before the four ineligible ones, because ineligible filings also count toward 'filed'. The ordering hint ("biggest charges first") is only given if the agent brings up provisional credit.
  - *Fix:* State in doc_015 that disputes filed earlier in the same conversation count toward the 12-month limit and that eligible disputes should be filed first in descending amount, or change gold[9] to eligible=true (pre-session history reading).
- **underspecified_instructions (Minor)** — The user script specifies neither the replacement-card shipping preference nor the resolution wanted for each dispute, yet gold fixes expedited_shipping=true, the home address, partial_refund $50 for the incorrect-amount dispute, and full_refund for the other seven.
  - `task_039 user_scenario: no shipping, expedited, or 'resolution requested' lines (compare task_038 step 9 "I want a full refund for all three")`
  - `gold[11]: "resolution_requested": "partial_refund", "partial_refund_amount": 50; gold[15]: "expedited_shipping": true`
  - `doc_credit_card_replacements_001: Premium-tier expedited "$0.00 (complimentary)"; "strongly recommend expedited shipping" for fraud`
  - *Why it matters:* The likely answers match the gold (free and recommended expedited; '$50 extra' implies a $50 partial refund), but the simulator could answer otherwise and fail a correct agent.
  - *Fix:* Script the expedited and resolution answers (e.g., "Full refund on all except the $198.23 Costco one, where I only want the $50 overcharge back; expedited shipping is fine").

*Verifier: Adjusted (Blocker → Major).* Reproduced. Read at each filing, criterion 4 counts in-session filings, and with the customer's 'biggest first' preference it yields exactly the gold. Read as a pre-session history check, all four are eligible. The review itself concedes the running-count reading is textually supportable, so the gold follows one of two document-supported readings: Major under calibration, not Blocker. The task_041 reviewer reached Major on identical reasoning. The Minor unscripted-resolution/expedited issue holds.

### task_040 — Major

**With one past dispute on file, the written rule makes all four fraud and duplicate disputes eligible for provisional credit, but the official answer grants it to only two, using a running count and a filing order the documents never state.**

- **non_determinism (Blocker)** — Same criterion-4 ambiguity as task_039. Counted against pre-session history (1 prior dispute, dsp_ed3ab3dce038), all four reason-eligible disputes pass 'not more than 2'. The gold marks the 3rd and 4th filed (American Airlines $342.50 fraud, Best Buy $189.99 duplicate) ineligible, which holds only if in-session filings count and the user-prioritized Grainger/Uline disputes are filed first.
  - `doc_credit_cards_credit_cards_(general)_015: "4. Previous Disputes: The customer has not filed more than 2 disputes in the past 12 months"`
  - `initial_state transaction_disputes.dsp_ed3ab3dce038: submitted_at "09/20/2025", status "APPROVED" (only prior dispute for 01f21c9970)`
  - gold[7..8] eligible=true (txn_25e23705f61f Grainger $523.45 dup, txn_fd4c3871654e Uline $412.34 fraud); gold[9..10] eligible=false (txn_a1b2c3d4e503 AA $342.50 fraud, txn_a1b2c3d4e510 Best Buy $189.99 dup, merchant contacted), all otherwise eligible (Gold/Business Gold premium max $10000, accounts opened 06/15/2024 and 09/01/2024)
  - `task_040 description.notes cites "provisional_credit_max_disputes_in_period = 3"; this parameter appears in no document or tool code (only in task notes)`
  - `Replay: all four reason-eligible = true -> verified match False (transaction_disputes differs)`
  - *Why it matters:* An agent that reads criterion 4 as a history check sets eligible=true on all four and fails. The customer's 'prioritize Grainger/Uline if there's any limit' signals intent but does not establish that a limit applies, and it is only voiced if the agent raises provisional credit.
  - *Fix:* Define in doc_015 that in-session filings count toward the 12-month limit and how to order filings, or set gold[9] and gold[10] to eligible=true.
- **document_contradiction (Minor)** — The seeded prior dispute (agent-visible via get_user_dispute_history_7291) has impossible dates: it was noticed and submitted before the purchase it disputes.
  - `initial_state dsp_ed3ab3dce038: purchase_date "10/02/2025", issue_noticed_date "09/15/2025", submitted_at "09/20/2025"`
  - *Why it matters:* It does not change the count (1 dispute in the past 12 months under either date), but a careful agent may question the record.
  - *Fix:* Set issue_noticed_date/submitted_at after 10/02/2025 (e.g., 10/05 and 10/06/2025).
- **underspecified_instructions (Minor)** — The user script never states the resolution wanted per dispute; gold uses partial_refund $24.56 for PECO and full_refund for the rest.
  - `task_040 user_scenario: no 'resolution requested' line; PECO: "They overcharged you by $24.56"`
  - `gold[11]: "partial_refund_amount": 24.56`
  - *Why it matters:* The natural answers match the gold, but they are left to the simulator.
  - *Fix:* Script the resolution for each dispute.

*Verifier: Adjusted (Blocker → Major).* Same criterion-4 ambiguity as task_039, and the gold follows a document-supported reading plus the customer's scripted priority, so Major, consistent with task_041. The impossible seed-dispute dates are cosmetic (the 12-month count is 1 either way), so per calibration they belong in notes rather than as a Minor issue. The PECO partial_refund 24.56 issue stays Minor because the script states the exact overcharge.

### task_041 — Major

**Which disputes get provisional credit depends on whether disputes filed earlier in the same call count toward the 'no more than 2 disputes in 12 months' rule, which the policy never says; the XFINITY refund amount also has to be inferred from 'around $120'.**

- **non_determinism (Major)** — eligible_for_provisional_credit is persisted per dispute. The gold sets it true only for Staples and Coinbase, which matches one reading of criterion 4: count disputes filed earlier in the same session and file the customer's two priorities first. If criterion 4 counts only pre-session history (1 prior dispute), all 10 reason-eligible disputes qualify. If the 16 new filings count all at once, none do.
  - `doc_credit_cards_credit_cards_(general)_015: "4. Previous Disputes: The customer has not filed more than 2 disputes in the past 12 months"`
  - `initial_state transaction_disputes.dsp_dfab0685d198.submitted_at = "09/20/2025" (the only prior dispute)`
  - gold[9] Staples txn_645286a3dd13 eligible_for_provisional_credit = true; gold[10] Coinbase txn_1b4cc30a928e = true; gold[11] Delta txn_107c4fa829bd (fraud, $487.50, Gold card opened 03/15/2024) = false
  - user instructions: "The Staples and Coinbase charges are the biggest ones ... Please prioritize those if there's any limit." (said only if the agent raises provisional credit)
  - `file_credit_card_transaction_dispute_4829 stores "provisional_credit_given": eligible_for_provisional_credit`
  - `Replay: gold with all 10 reason-eligible disputes set true -> verified match False, transaction_disputes differs in 8 records`
  - *Why it matters:* Criteria 1, 2, 3 and 5 pass for 10 of the 16 disputes: 4 fraud, 4 duplicate, and 2 goods-not-received older than 30 days, all at least $25 and under the tier caps, on accounts open more than 60 days, with the merchant contacted where required. An agent that reads criterion 4 as a pre-session history gate marks all 10 true and fails on 8 records. The prior review took that reading. Only an agent that counts its own in-session filings, and files Staples and Coinbase before every other dispute, reaches the gold.
  - *Fix:* State in doc_015 that disputes filed earlier in the same interaction count toward criterion 4, and that the customer chooses which disputes are evaluated first. Alternatively, make the gold mark all 10 reason-eligible disputes true.
- **underspecified_instructions (Major)** — The gold files XFINITY as partial_refund with partial_refund_amount 69.99 (189.99 minus 120). The customer gives no resolution for any dispute and only says the usual bill is 'around $120'. Tesla ('overcharged ... promised a refund') and AT&T ('promised a partial refund') are filed as full_refund.
  - `user instructions: "XFINITY $189.99 on 10/28/2025 - INCORRECT AMOUNT. Your usual bill is around $120."`
  - `gold[19].arguments: "resolution_requested": "partial_refund", "partial_refund_amount": 69.99`
  - `gold[24] AT&T ("promised a partial refund") resolution_requested = "full_refund"`
  - `doc_credit_cards_credit_cards_(general)_014: "13. resolution_requested (string) - Ask user what resolution they want."`
  - `Replay: gold with XFINITY as full_refund -> verified match False (transaction_disputes differs)`
  - *Why it matters:* The doc says to ask the customer for the resolution, but the simulator has no scripted answer, so what is stored depends on what it improvises. A reply of 'full refund on all of them' or a refund of 'about $70' gives a different record and fails the task.
  - *Fix:* Script the resolution for each of the 16 disputes. For XFINITY give an exact figure, e.g. "I want a partial refund of $69.99, the amount over my usual $120.00 bill."
- **document_contradiction (Minor)** — The dispute-filing doc lists 'reversal_of_charge' as a valid resolution_requested value, but the tool rejects it.
  - `doc_credit_cards_credit_cards_(general)_014: "'reversal_of_charge': Charge reversal/chargeback"`
  - `tools.py file_credit_card_transaction_dispute_4829: valid_resolutions = ["full_refund", "partial_refund"]`
  - *Why it matters:* An agent that picks reversal_of_charge for a fraud charge gets an error and has to retry. The failed call writes nothing outside the relaxed agent_discoverable_tools table, so the final state is unaffected.
  - *Fix:* Remove reversal_of_charge from doc_014, or accept it in the tool.

*Verifier: Confirmed (Major → Major).* Both Major issues reproduce. The provisional-credit issue is rated consistently with what I set for 039/040. The XFINITY amount has no scripted figure ('around $120'), so it is Major under the no-default rule, which justifies the different rating from 039/040, where the script states the exact overcharge. The reversal_of_charge mismatch is harmless under the verified scorer.

*Reconciled across runs: Major → Major (judgment).* Two independent Majors. Provisional credit: with one prior dispute (09/20/2025), the gold's Staples/Coinbase true and the rest false follow the running-count reading of criterion 4, while the prior-history-only reading makes all 10 reason-eligible disputes true; that is two supported readings. XFINITY partial_refund_amount 69.99 is an unscripted customer choice (doc_014 says to ask), but it is derivable as 189.99 - 120 from the script's 'around $120'. Calibration caps an unscripted choice with no documented default at Major, and run U's Blocker rested on that choice, so Major under both scorers (transaction_disputes is compared exactly in both).

### task_046 — Major

**The gold expects the agent to stop at the pending dispute and leave the $125 balance unpaid, but if the agent mentions the balance, the customer is scripted to ask for it to be paid.**

- **non_determinism (Major)** — The account has an unpaid $125 balance as well as the blocking dispute. The customer's instructions say to agree to pay any balance the agent mentions, and the policy says to 'explain what must be resolved'. The gold contains no payment.
  - `db.json credit_card_accounts.cc_224959b99e_bsilver.current_balance = "$125.00"`
  - user instructions: "If the agent mentions you have an outstanding balance, agree to pay it off." and step 3: "Yes, please pay that off from my checking account."
  - doc_credit_cards_credit_card_account_logistics_003: "Check these in order: 1. Pending disputes ... 4. Outstanding balance ... If any requirement is not met, explain what must be resolved and do not proceed with retention offers."
  - `required_documents includes doc_credit_cards_credit_card_account_logistics_009 (pay balance from checking)`
  - `task notes (not agent-visible): "requirements 1-3 should be checked first since they cannot be resolved during the call"`
  - `Replay: gold + pay_credit_card_from_checking_9182($125 from 05) -> verified match False (accounts and credit_card_accounts differ)`
  - *Why it matters:* A competent agent sees the $125 balance when it looks up the card and may list it among the things that 'must be resolved'. The customer then asks for it to be paid, and paying it is a legitimate service. The resulting state fails. The gold passes only if the agent stops at the first failed check and never mentions the balance, a rule that appears only in the author notes.
  - *Fix:* Set the bsilver balance to $0.00 in this task's initial_state, or add a gold payment of $125.00 and script the customer to request it.

*Verifier: Confirmed (Major → Major).* Reproduced. Paying the balance on the customer's request is a legitimate action the materials do not forbid, and it breaks the gold, so Major. Additional unreported data defect: the blocking dispute's last-4 matches neither of the customer's cards, so the only link to the Business Silver account is the id string. An agent that checks last-4 (giving the user get_card_last_4_digits) also fails, because user_discoverable_tools is compared exactly. This does not raise the severity.

### task_048 — Major

**For the Gold card, several Rho-Bank cards beat the competitor's 3.25% travel/software rate, but the gold accepts only an application for the Silver Rewards Card.**

- **non_determinism (Major)** — The 'found a better card' step says to offer 'a card with similar or better benefits'. The Silver Rewards Card (4% travel/software, $0 fee) qualifies, but so does the Platinum Rewards Card (10% on all purchases, $200 fee, 0% FX), and Business Silver earns 10% on travel/software. The customer applies for whatever 'competitive or better' card the agent presents, and the gold stores only card_type 'Silver Rewards Card'.
  - user instructions: "I found a card at another bank that offers 3.25% back those" [travel, software]; step 8: "If the agent explains the card details and they're competitive or better than the competitor: Apply enthusiastically with the apply_for_credit_card tool."
  - doc_credit_cards_credit_card_account_logistics_003: "Found a better card: Ask what features attracted them. If Rho-Bank offers a card with similar or better benefits, offer to help them apply"
  - `doc_credit_cards_silver_rewards_card_002: travel and software transactions "earn 4.0% back"`
  - `doc_credit_cards_platinum_rewards_card_002: "You earn 10.0% cash back on all eligible purchases."`
  - `doc_business_credit_cards_business_silver_rewards_card_002: "Earn 10.0% cash back on eligible travel and software purchases"`
  - `gold[18].arguments.card_type = "Silver Rewards Card"`
  - `Replay: gold with card_type 'Platinum Rewards Card' -> verified match False (credit_card_applications differs)`
  - *Why it matters:* An agent that recommends the strictly higher-earning Platinum Rewards Card, or presents both cards, can lead the simulator to apply for a different card. The credit_card_applications record then differs and the task fails, even though the documents support that recommendation.
  - *Fix:* Give the customer a constraint that leaves only Silver Rewards, e.g. 'I won't pay an annual fee' (which rules out Platinum and Business Silver), or have the customer name the Silver Rewards Card once the agent lists options.

*Verifier: Confirmed (Major → Major).* Reproduced. The other three cards resolve deterministically, while the replacement-card recommendation has more than one document-supported answer and the gold records one, so Major. The Crypto reason ambiguity is correctly neutralized by the closure_reason strip, and this task depends on the verified scorer for that.

### task_049 — Blocker

**The gold includes a customer-side 'request human transfer' write that the customer is never told to perform, so the result depends on whether the user simulator happens to call that tool exactly once.**

- **instruction_gold_mismatch (Blocker)** — Gold action 17 is a user-side request_human_agent_transfer call, which writes a transfer_request_1 row to human_transfer_requests. The customer instructions only say to ask verbally for a transfer. The simulator guidelines say to call tools only when the agent asks, and the agent cannot see or request this tool.
  - `gold[17]: requestor user, request_human_agent_transfer {}`
  - `tools.py request_human_agent_transfer: add_to_db("human_transfer_requests", request_id, record) with request_id = f"transfer_request_{request_count}"`
  - `user instructions: "Transfer me to a human agent." (no mention of the tool)`
  - data/tau2/user_simulator/simulation_guidelines_tools.md: "Only call a tool if the agent has requested it or if it is necessary to answer a question the agent has asked."
  - `contrast task_034/task_081 instructions: "Call the `request_human_agent_transfer` tool (for tracking purposes — the agent cannot see this)"`
  - Replay: gold without gold[17] -> verified match False (human_transfer_requests: only_gold transfer_request_1); gold with the call made twice -> False (only_pred transfer_request_2)
  - *Why it matters:* The agent cannot influence this table. Unless the simulator spontaneously calls the tool exactly once, against its guidelines, a perfect agent trajectory fails the DB check.
  - *Fix:* Remove gold[17]. Otherwise, add the explicit instruction used in task_034/081 ('call the request_human_agent_transfer tool exactly once when you ask for a supervisor').

*Verifier: Confirmed (Blocker → Blocker).* Reproduced. The graded row exists only if the simulator calls the tool exactly once, unprompted, and the agent has no tool or documented instruction to make that happen, so correct work passes or fails by chance: Blocker. All agent-side actions reproduce. A failed payment attempt is tolerated only under the verified scorer.

### task_053 — Blocker

**The gold leaves out the customer's own card-number lookup, but the agent cannot get the card's last 4 digits without it, so every correct trajectory leaves an extra DB row and fails.**

- **instruction_gold_mismatch (Blocker)** — The gold gives the user get_card_last_4_digits (gold[13]) and files the dispute with card_last_4_digits '2791' (gold[15]), but it never replays the user's call_discoverable_user_tool lookup. That lookup writes a row to user_discoverable_tool_calls and is the only way to obtain '2791'.
  - `user instructions: "(If the agent provides you with the get_card_last_4_digits tool, use it to retrieve the number.)"`
  - `gold[15].arguments: "card_last_4_digits": "2791"; no user-requestor action in the gold`
  - `tools.py KnowledgeUserTools.get_card_last_4_digits -> _log_user_tool_call -> add_to_db("user_discoverable_tool_calls", ...)`
  - `get_credit_card_accounts_by_user returns no last-4 field (db.json credit_card_accounts.cc_e9d195fe8e_silver has none)`
  - Replay: gold + user call_discoverable_user_tool(get_card_last_4_digits, cc_e9d195fe8e_silver) -> returns 'Last 4 digits of card: 2791'; verified match False (user_discoverable_tool_calls only_pred 9a452d6c48d8d07e)
  - `contrast task_041 gold[4-7], which do include the user's get_card_last_4_digits calls`
  - *Why it matters:* A trajectory where the user does not look up the number cannot supply '2791', so the dispute record differs. A trajectory where the user does look it up leaves a row the gold lacks. No path matches the gold under either the exact or the verified scorer.
  - *Fix:* Add a user action call_discoverable_user_tool {discoverable_tool_name: get_card_last_4_digits, arguments: {"credit_card_account_id": "cc_e9d195fe8e_silver"}} between gold[13] and gold[15].
- **hidden_ordering (Major)** — The gold processes the CLI before filing the dispute, so the approval passes the 'no pending disputes' check. No doc says to sequence a concurrent CLI ahead of a dispute, and the customer raises the dispute first.
  - `user instructions: "State BOTH requests upfront, but the dispute first"`
  - `doc_credit_cards_credit_card_account_logistics_007 Step 2: "3. No Pending Disputes: Verify the account has no active disputes."`
  - `tools.py approve_credit_limit_increase_5847 returns 'cannot be approved' when any user dispute has status SUBMITTED/UNDER_REVIEW/PENDING`
  - `gold order: CLI submit/approve gold[10],[12] before dispute gold[15]`
  - `task notes (not agent-visible): "process the CLI FIRST before filing the dispute"`
  - *Why it matters:* An agent that handles the dispute first, in the customer's order, then correctly denies the CLI for pending_disputes, producing a different credit_limit and CLI records. Reordering to avoid an eligibility rule is a judgment call the docs neither require nor endorse.
  - *Fix:* Add guidance to logistics_007 for concurrent dispute and CLI requests (e.g. 'when a customer requests both, complete the CLI first'), or have the customer ask for the CLI first.
- **document_gap (Minor)** — The internal CLI workflow doc that 'MUST be followed in the exact order' has an empty Step 3 (payment history and amount check). The payment-history rule and the get_payment_history_6183 tool are only described in a separate doc.
  - `doc_credit_cards_credit_card_account_logistics_007: "## Step 3: Verify Payment History and Requested Amount\n\n.\n\n## Step 4"`
  - `doc_credit_cards_credit_card_account_logistics_007: "These steps MUST be followed in the exact order listed."`
  - doc_credit_cards_credit_card_account_logistics_006: "Use the get_payment_history_6183 tool to verify the customer's payment history meets the requirement for their card tier." (the only doc naming the tool)
  - *Why it matters:* get_payment_history_6183 is a gold-required read, so its tool name must appear in agent_discoverable_tools. An agent that follows only the step-by-step workflow doc finds no instruction to call it. Doc 006 is in required_documents and says to call it, so a careful agent still reaches the gold.
  - *Fix:* Fill Step 3 of logistics_007 with the payment-history check (call get_payment_history_6183 with the tier's month count) and the per-tier maximum-increase check from logistics_006.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced the Blocker: the only source of '2791' is the user tool the gold hands over, and its call writes a user_discoverable_tool_calls row the verified scorer compares exactly, so no trajectory matches. The hidden_ordering Major and the logistics_007 Minor also reproduce; the ordering issue is arguably Minor-to-Major since logistics_007 lists 'No Pending Disputes' and the agent can surface the conflict, but it does not change the task severity.

### task_056 — Major

**The business-savings opening procedure tells the agent to use account type 'savings', but the official answer uses 'business_savings', so an agent that follows the procedure document fails.**

- **document_contradiction (Major)** — The internal procedure for opening business savings tells the agent, twice, to call open_bank_account_4821 with account_type 'savings'. The tool docstring lists 'business_savings', and gold action 5 uses 'business_savings'. The account id is a hash of user_id, account_type and account_class, so the two choices create different account records.
  - `doc_bank_accounts_bank_accounts_(general)_004, Tool: open_bank_account_4821, How to call: "Set account_type to 'savings'."`
  - `doc_bank_accounts_bank_accounts_(general)_004, Tool: open_bank_account_4821, Expected outcome: "Returns a new savings account record"`
  - tools.py open_bank_account_4821 docstring: "account_type (string): Type of account to open. Must be one of: 'checking' (personal checking), 'savings' (personal savings), 'business_checking', 'business_savings'"
  - `tools.py open_bank_account_4821: seed = f"account:{user_id}:{account_type}:{account_class}"`
  - `gold[5].arguments.arguments = {"user_id": "b5e8f2a1c9", "account_type": "business_savings", "account_class": "Silver Plus Saver Account"}`
  - Replay: account_type 'savings' succeeds (the personal-savings eligibility passes on the customer's 2023 Green checking) and creates id 3e54498f671ab53f instead of gold c1b48f17bb35e876 -> verified=(False, ['table accounts differs'])
  - *Why it matters:* An agent that follows the KB's own procedure for business savings passes account_type 'savings'. The tool accepts it, the account opens, and the $3,200 transfer goes to the new id, so the conversation looks successful but the accounts table never matches gold. Only an agent that trusts the tool's enum over the explicit KB instruction passes.
  - *Fix:* Change general_004 to "Set account_type to 'business_savings'". Alternatively, have the tool reject 'savings' for a Saver-class account_class.

*Verifier: Confirmed (Major → Major).* Reproduced the account_type contradiction; two document-supported readings -> Major per calibration. The review missed that the active business-savings promotion (general_015) puts Gold Saver ahead of Silver Plus Saver; Gold Saver documents same-day ACH but no withdrawal limit and no multi-product relationship bonus, so a careful agent still cannot confirm it meets Roberto's needs and Silver Plus Saver (promotion #2) stays defensible. Worth a note, not a severity change.

### task_059 — Major

**The right products are clear (Silver Rewards Card plus Green savings), but the KB calls the savings account 'Green Account (savings)' while the official answer only accepts the account name 'Green Account'.**

- **document_contradiction (Major)** — The gold opens the savings product as account_class 'Green Account'. The KB names this product 'Green Account (savings)' in every title and in the pairing list, and the checking-opening procedure gives 'Green Account (checking)' as an example of a full official name. Only the savings procedure's rule ('ending with Account') points to the bare 'Green Account'. Because the account id is a hash of account_class, the two spellings produce different account records.
  - doc_savings_accounts_green_account_(savings)_001 title: "Green Account (savings) specifications and requirements" (all nine Green savings docs use "Green Account (savings)")
  - `doc_bank_accounts_bank_accounts_(general)_012: "3. Evergreen Account (checking) + Green Account (savings)"`
  - doc_bank_accounts_bank_accounts_(general)_001: "Personal checking account_class options must use the full official name ending with 'Account' (e.g., 'Blue Account', 'Green Account (checking)')."
  - doc_bank_accounts_bank_accounts_(general)_002: "account_class must use the full official name ending with 'Account', e.g., 'Silver Plus Account', 'Gold Account'"
  - `tools.py open_bank_account_4821: seed = f"account:{user_id}:{account_type}:{account_class}"`
  - `gold[5].arguments.arguments account_class = "Green Account"`
  - `Replay: gold with account_class 'Green Account (savings)' -> verified=(False, ['table accounts differs'])`
  - *Why it matters:* An agent that copies the product's official name from the KB ('Green Account (savings)'), or follows general_001's example where the parenthetical is part of the name, opens a correctly chosen account under a different id. The accounts table then differs and the task fails, although the product choice was right.
  - *Fix:* Make the open tool normalize account_class (strip a trailing ' (savings)'/' (checking)'), or state in general_002 that the Green savings account_class is exactly 'Green Account'.

*Verifier: Confirmed (Major → Major).* Product choice is unique; the account_class spelling has two document-supported readings ('ending with Account' vs the parenthetical official name), so Major per calibration. Consistent with 065 and 068.

### task_063 — Blocker

**Two credit cards (Bronze Rewards and Silver Rewards) give the exact same savings boost and both meet every customer condition, but only Silver Rewards is accepted.**

- **non_determinism (Blocker)** — On the optimal savings account (Silver Plus, 3.0% tier 1 at $8,000), Bronze Rewards and Silver Rewards both add +0.15%. Both have a $0 annual fee and both run a real credit check that a 700 score passes (640 and 680 minimums). Nothing in the instructions or KB breaks the tie, yet gold action 1 accepts only 'Silver Rewards Card'.
  - `doc_savings_accounts_silver_plus_account_009: "| Bronze Rewards Card | +0.15% |" and "| Silver Rewards Card | +0.15% |"`
  - `doc_credit_cards_bronze_rewards_card_001: "Minimum credit score: $640" and "Annual fee: $0.00"`
  - `doc_credit_cards_silver_rewards_card_001: "Minimum credit score: $680" and "Annual fee: $0.00"`
  - `user_scenario: "My goal is to maximize the interest I'll earn over one year"; "My credit score is around 700"; "I only want a card that actually checks credit"`
  - `gold[1].arguments.card_type = "Silver Rewards Card"`
  - Computed at $8,000: Silver Plus + Silver Rewards = 3.15% -> $252; Silver Plus + Bronze Rewards = 3.15% -> $252; next best Silver Plus + Green Rewards (business card, $100 fee) 3.1% -> $248 gross; Silver + Crypto-Cash Back 3.0% -> $240
  - `Replay: gold with card_type 'Bronze Rewards Card' -> verified=(False, ['table credit_card_applications differs'])`
  - *Why it matters:* apply_for_credit_card derives the application_id from card_type, so an agent recommending Bronze Rewards, which is equally optimal on every stated criterion, produces a different credit_card_applications row and fails. On average this is a coin flip for a correct agent. Both cards also earn the same 1.0% on the groceries and gas the customer mentions, so card rewards do not break the tie either.
  - *Fix:* Change one bonus in silver_plus_account_009 (e.g. Bronze Rewards +0.10%), or add a customer constraint that only Silver Rewards satisfies.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced the exact tie on the optimal Silver Plus account with no documented tie-breaker; Blocker per calibration. Holds under both scorers since credit_card_applications is compared exactly.

### task_065 — Major

**The right pairing (Evergreen checking plus Green savings, opened before closing Light Blue) is clear, but the official answer only accepts the savings name 'Green Account' while the KB calls it 'Green Account (savings)'.**

- **document_contradiction (Major)** — The gold opens the savings product as account_class 'Green Account'. The KB names this product 'Green Account (savings)' in every title and in the pairing list, and the checking-opening procedure gives 'Green Account (checking)' as an example of a full official name. Only the savings procedure's rule ('ending with Account') points to the bare 'Green Account'. Because the account id is a hash of account_class, the two spellings produce different account records.
  - doc_savings_accounts_green_account_(savings)_001 title: "Green Account (savings) specifications and requirements" (all nine Green savings docs use "Green Account (savings)")
  - `doc_bank_accounts_bank_accounts_(general)_012: "3. Evergreen Account (checking) + Green Account (savings)"`
  - doc_bank_accounts_bank_accounts_(general)_001: "Personal checking account_class options must use the full official name ending with 'Account' (e.g., 'Blue Account', 'Green Account (checking)')."
  - doc_bank_accounts_bank_accounts_(general)_002: "account_class must use the full official name ending with 'Account', e.g., 'Silver Plus Account', 'Gold Account'"
  - `tools.py open_bank_account_4821: seed = f"account:{user_id}:{account_type}:{account_class}"`
  - `gold[2].arguments.arguments account_class = "Green Account"`
  - `Replay: gold with account_class 'Green Account (savings)' -> verified=(False, ['table accounts differs'])`
  - *Why it matters:* An agent that copies the product's official name from the KB ('Green Account (savings)'), or follows general_001's example where the parenthetical is part of the name, opens a correctly chosen account under a different id. The accounts table then differs and the task fails, although the product choice was right.
  - *Fix:* Make the open tool normalize account_class (strip a trailing ' (savings)'/' (checking)'), or state in general_002 that the Green savings account_class is exactly 'Green Account'.

*Verifier: Confirmed (Major → Major).* Product and ordering reproduce; the Green savings account_class spelling is the only divergence, Major consistent with 059/068. closure_reason free text is irrelevant under the verified scorer.

### task_066 — Major

**The best savings-plus-checking-plus-card combination for $6,000 can be worked out uniquely from the documents, and the official answer matches it.**


*Reconciled across runs: None → Major (judgment).* The Green savings naming defect is real and scorer-independent: doc_002 requires a savings account_class 'ending with Account', but doc_001 gives 'Green Account (checking)' as an example of exactly such an official name and every savings doc titles the product 'Green Account (savings)', while the gold stores bare 'Green Account'. account_class seeds the account id, so the parenthetical form opens a different record, and the accounts table is compared exactly under both scorers. Both runs rate this same defect Major in tasks 059 and 065, so 066 takes the same Major; run U's additional closure_reason Major is upstream-only and does not change the severity.

### task_068 — Major

**The right accounts are clear, but the bank's own procedure tells the agent to name the checking account 'Green Account (checking)', while the answer key only accepts 'Green Account'.**

- **document_contradiction (Major)** — The procedure for opening personal checking accounts gives 'Green Account (checking)' as an example of the full official account_class name, but the gold opens the account with account_class 'Green Account'. open_bank_account_4821 derives the account id from the class string, so the two spellings create different records.
  - doc_bank_accounts_bank_accounts_(general)_001: "Personal checking account_class options must use the full official name ending with 'Account' (e.g., 'Blue Account', 'Green Account (checking)')."
  - `doc_bank_accounts_bank_accounts_(general)_005: "MID TIER (Blue Account, Green Account (checking))"`
  - `doc_checking_accounts_green_account_(checking)_001 title: "Green Account (checking) at a glance"`
  - `gold[3].arguments.arguments = {"user_id": "rp65a7b3c4", "account_type": "checking", "account_class": "Green Account"}`
  - `tools.py open_bank_account_4821: seed = f"account:{user_id}:{account_type}:{account_class}"`
  - `Replay: gold with account_class 'Green Account (checking)' -> _verified_db_match False ['table accounts differs']`
  - *Why it matters:* An agent that copies the documented example writes a different account_id and account_class and fails on the accounts table, even though it chose the correct product. The gold value follows only from the 'ending with Account' rule, which the same sentence's own example breaks.
  - *Fix:* Change the doc_001 example to 'Green Account', or have open_bank_account_4821 normalize the parenthetical type qualifier before deriving the id.

*Verifier: Confirmed (Major → Major).* Unique product set reproduces; the checking class string has two document-supported spellings and the doc example is the exact non-gold spelling. Major (gold follows the 'ending with Account' reading).

### task_069 — Blocker

**The official answer assumes the Gold savings account has no ATM-fee rebates, but the documents say it does, so the truly best combination (about 5.7% instead of 3.5%) is graded as wrong.**

- **argument_error (Blocker)** — The gold opens Silver Plus Account savings (3.0% tier 1). The task notes justify this by saying 'Gold Account has NO ATM rebates', but the Gold Account docs state a $30/month ATM fee rebate. With the customer's $10,000, Gold also meets its $10,000 minimum. Gold + Blue checking + Silver Rewards gives 5.5% + 0.2% = 5.70%, versus the gold's 3.0% + 0.35% + 0.15% = 3.50%.
  - `doc_savings_accounts_gold_account_003: "ATM fee rebate cap per month: $30"`
  - `doc_savings_accounts_gold_account_013: "You continue to receive up to $30 in ATM fee rebates each month."`
  - `doc_savings_accounts_gold_account_002: "Minimum balance to maintain the account: $10,000"`
  - `doc_savings_accounts_gold_account_014: "| Silver Rewards Card | +0.2% |"`
  - `task_069 description.notes: "Gold Account has NO ATM rebates."`
  - `gold[2].arguments.arguments account_class = "Silver Plus Account"`
  - `doc_savings_accounts_silver_plus_account_001: "Balances at or above $15,000 qualify for Tier 2 interest; lower balances earn the Tier 1 rate."`
  - `Replay: gold with savings account_class 'Gold Account' -> ['table accounts differs']`
  - *Why it matters:* An agent that checks the Gold Account's ATM rebate feature, as the customer prompts it to ('Wait, does the Gold Account have ATM fee rebates?'), finds that it does and correctly recommends Gold. That opens a different savings account and fails the accounts table. The gold is reachable only by ignoring two Gold Account documents.
  - *Fix:* Either remove the ATM rebate from the Gold Account docs (gold_account_003, gold_account_013) and fix the Silver Account issue below, or change the gold to Gold Account savings with Blue checking.
- **argument_error (Blocker)** — Even with Gold excluded, the Silver Account beats Silver Plus. Silver rebates ATM fees ($15/month), and at exactly $10,000 it earns its 4.0% upper tier. Silver 4.0% + Silver Rewards +0.1% (+0.025% relationship bonus) = 4.10-4.125%, above the gold's 3.50%. The notes list Silver as blocked for lacking ATM rebates.
  - `doc_savings_accounts_silver_account_005: "Yes. You can receive ATM fee rebates up to 15 each month."`
  - `doc_savings_accounts_silver_account_003: "If it is at or above that amount, the applicable APY for that day is 4.0%." (threshold $10,000)`
  - `doc_savings_accounts_silver_account_006: "Silver Rewards Card: +0.1%"`
  - `task_069 description.notes: "Needs ATM fee rebates on savings account - blocks Gold Account, Silver Account, Green Account (savings), Bronze Account"`
  - *Why it matters:* A second documented option beats the gold, so the gold is not the APY-maximizing answer under any reading of the ATM-rebate requirement.
  - *Fix:* Remove Silver's ATM rebate from the docs or raise its tier threshold above $10,000, along with the Gold fix above.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced: two documented savings options beat the gold on the customer's own criterion, so the gold follows no document-supported reading. Blocker.

### task_070 — Major

**The active November promotion picks Sky Blue among the three accounts that fit, but Sky Blue's startup-age eligibility can't be confirmed because the customer is never told when her business was formed.**

- **underspecified_instructions (Minor)** — Sky Blue is a startup account whose docs tell the customer to confirm the company is within 4 years of formation. The customer's instructions never give a formation date, so an agent that checks this gets an improvised answer from the simulator.
  - `doc_business_checking_accounts_sky_blue_001: "Confirm your company is within 4 years of formation."`
  - doc_bank_accounts_bank_accounts_(general)_003 eligibility list (verified, personal checking OPEN, <=6 business checking, no CLOSED accounts, balance >= $500) has no company-age rule
  - `db.json credit_card_accounts[cc_224959b99e_bsilver].date_of_account_open = "03/15/2023" (a business card, consistent with a business under 4 years old)`
  - *Why it matters:* If the simulator answers 'more than 4 years', a careful agent would skip Sky Blue and open Lime Green, and the accounts table would differ. The internal opening procedure doesn't require this check and the seeded data suggests a young business, so the most likely outcome is unchanged.
  - *Fix:* Add a line to the instructions such as 'Brightwave Digital was founded in 2023.'

*Verifier: Confirmed (Minor → Minor).* Promotion logic and eligibility reproduce; the formation-age gap is an unstated fact not in the internal opening checklist, Minor. Same rating as the identical issue in 071.

*Reconciled across runs: Minor → Major (judgment).* Sky Blue is a startup account whose documents state a company-age eligibility threshold of 4 years, and the customer script never gives Brightwave Digital's formation date, so an agent that performs the documented check gets an improvised answer that can move it to Lime Green. This is an unscripted customer fact with no documented default that decides the graded account_class, which calibration rates Major; the run V argument that the internal opening checklist omits the check does not remove the explicit 'Verify Eligibility' rule. The same Sky Blue issue is Major in run U's 071, so 070 takes Major under both scorers (accounts table compared exactly).

### task_071 — Major

**The right accounts (Sky Blue and Gold Saver) follow from the active promotions, but the bank's business-savings procedure tells the agent to open it as a personal 'savings' account, which creates the wrong record.**

- **document_contradiction (Major)** — The internal procedure for business savings accounts tells the agent to call open_bank_account_4821 with account_type 'savings', but the gold (and the tool docstring) use 'business_savings'. The tool accepts 'savings' for this customer (she has a 3-year-old personal checking account) and silently opens a personal savings record with a different id.
  - `doc_bank_accounts_bank_accounts_(general)_004 Tool Instructions: "Set account_type to 'savings'."`
  - tools.py open_bank_account_4821 docstring: "Must be one of: 'checking' (personal checking), 'savings' (personal savings), 'business_checking', 'business_savings'"
  - `gold[5].arguments.arguments = {"user_id": "yt71c9e4f2", "account_type": "business_savings", "account_class": "Gold Saver Account"}`
  - Replay: gold with account_type 'savings' for Gold Saver Account -> tool returns 'Bank account opened successfully!' and _verified_db_match False ['table accounts differs']
  - *Why it matters:* An agent that follows the business-savings procedure exactly writes account_type 'savings' and a different account_id and fails on the accounts table. The tool gives no error that would correct it.
  - *Fix:* Change doc_004 to "Set account_type to 'business_savings'" (or make the tool reject personal 'savings' for business account classes).
- **underspecified_instructions (Minor)** — As in task_070, Sky Blue's docs ask to confirm the company is within 4 years of formation, and the customer's instructions give no formation date.
  - `doc_business_checking_accounts_sky_blue_001: "Confirm your company is within 4 years of formation."`
  - `db.json accounts[biz_chk_yt71c9e4f2].date_opened = "09/15/2025" (Cobalt Blue opened about 2 months ago)`
  - *Why it matters:* An improvised 'over 4 years' answer would move a careful agent to Lime Green. It is unlikely given the context and is not part of the internal eligibility list.
  - *Fix:* State the studio's founding year in the instructions.

*Verifier: Confirmed (Major → Major).* Same account_type contradiction as 056, same Major; the Sky Blue formation-age Minor matches 070. Note the gold here treats Gold Saver's undocumented minimum as 'no minimum', which is consistent with keeping Silver Plus Saver in 056 only because 056 adds a withdrawal-count and relationship-bonus need Gold Saver does not document.

### task_072 — Major

**Both refund amounts ($14.00 and $3.50) can be rebuilt from the fee schedules and the 'net correction' rule, but some of the fees that count are dated after the benchmark's fixed 'today'.**

- **argument_error (Minor)** — The seeded November history runs to 11/20/2025, but the fixed clock is 11/14/2025 03:40. Two of the discrepancies that make up the gold credits are dated after 'today': Bluest's 11/20 $2.50 fee (+$0.50) and Light Green's 11/15 $4.00 foreign fee (+$0.50).
  - `src/tau2/domains/banking_knowledge/utils.py get_now(): return datetime(2025, 11, 14, 3, 40, 0)`
  - `db.json bank_account_transaction_history chk_lj82d4f1a9 11/20/2025 atm_fee -2.5 'NON-RHO ATM FEE' (posted) with fee_rebate +2.0`
  - `db.json chk_538bfb9cba 11/15/2025 atm_fee -4.0 'FOREIGN ATM FEE - 2% OF WITHDRAWAL (MIN $3.00)' on a -200.0 SANTANDER MADRID withdrawal`
  - `gold[7] amount 14.00; gold[8] amount 3.50`
  - *Why it matters:* An agent that limits the review to transactions on or before the current time gets Bluest $13.50 and Light Green $3.00 and fails. The more natural reading is the customer's November statement as returned by the tool, with every record status 'posted', and that reading reaches the gold.
  - *Fix:* Re-date the seeded November transactions to fall on or before 11/14/2025, or move the clock to after 11/20/2025.

*Verifier: Adjusted (Minor → Major).* All of the review's arithmetic reproduces, but calibration.md fixes 'Gold values that depend on data dated after the fixed clock' at Major, and both gold credits include after-clock items. The review's 'natural reading' rationale is a reason to discuss, not to depart from the calibrated severity. The unreported fee-stacking reading is a second, weaker Major-class concern.

*Reconciled across runs: Major → Major (coverage).* Both gold credits include discrepancies on fee rows dated after the fixed clock (Bluest 11/20 +$0.50; Light Green 11/15 +$0.50), so an agent that scopes the review to 'through today' credits $13.50 and $3.00 and fails. Calibration fixes gold values that depend on post-clock data at Major; run U's 072 was never verified, and its reviewer's 'natural reading' rationale does not override the calibrated severity. The Bluest own-fee rebate reading (Minor) remains as a secondary issue. Scorer-independent.

### task_073 — Major

**All three refunds ($9.50, $9.00, $1.50) follow from the fee schedules and the documented 'net correction' rule, but some of the errors that count are dated after the benchmark's fixed 'today'.**

- **argument_error (Minor)** — Three of the discrepancies in the gold credits fall after the fixed clock (11/14/2025 03:40): Green's duplicate $3.00 fee on 11/15 (+$3.00), Light Green's 11/15 $150 foreign withdrawal charged $5.00 instead of $3.50 (+$1.50), and Light Green's uncharged 11/17 withdrawal (-$1.50).
  - `src/tau2/domains/banking_knowledge/utils.py get_now(): return datetime(2025, 11, 14, 3, 40, 0)`
  - `db.json chk_kj93a7b2e1_2 11/15/2025 two atm_fee -3.0 'NON-RHO ATM FEE' rows for one -250.0 PNC withdrawal`
  - `db.json chk_kj93a7b2e1_3 11/15/2025 atm_fee -5.0 'FOREIGN ATM FEE - TIER 3 (ABOVE $300)' on -150.0 KB KOOKMIN`
  - `gold[9] amount 9.00; gold[10] amount 1.50`
  - *Why it matters:* An agent that only reviews transactions on or before today gets Green $6.00 and fails. The natural reading, the full November history as returned with status 'posted', reaches the gold.
  - *Fix:* Re-date the seeded rows to fall on or before 11/14/2025 or advance the clock.

*Verifier: Adjusted (Minor → Major).* Arithmetic reproduces; Green's $9.00 depends on an 11/15 duplicate fee dated after the 11/14 clock, so calibration puts this at Major, not Minor. The review downgraded from the prior Major for a different reason (netting is documented), which is correct, but the after-clock rule keeps it at Major.

### task_074 — Major

**After the v1.0.1 fix, all four refunds ($27.00, $14.50, $4.75, $3.70) can be rebuilt from the fee documents; one Purple error the gold depends on is dated after the fixed 'today'.**

- **argument_error (Minor)** — Purple's $27.00 includes a duplicate $2.50 out-of-network fee dated 11/15/2025, after the fixed clock of 11/14/2025 03:40.
  - `src/tau2/domains/banking_knowledge/utils.py get_now(): return datetime(2025, 11, 14, 3, 40, 0)`
  - `db.json chk_ar72c5d8e3_1 11/15/2025: atm_fee -2.5, atm_fee -2.5, fee_rebate +2.5 for one -300.0 PNC withdrawal`
  - `gold[9] amount 27.00`
  - *Why it matters:* An agent that scopes the review to 'November through today' credits Purple $24.50 and fails. Reading the full posted November history, as the customer asks, reaches $27.00.
  - *Fix:* Move the duplicate fee to a date on or before 11/14/2025.

*Verifier: Adjusted (Minor → Major).* The v1.0.1 Light Blue fix ($14.50) and all four credits reproduce. Purple's $27.00 includes a duplicate fee dated 11/15, after the clock, so calibration requires Major. The benchmark also assumes no fee stacking here while task_075's gold requires stacking.

### task_075 — Major

**Several checking accounts charge $0 for foreign ATM withdrawals, and Purple even refunds operator fees, but the answer key only accepts Green Fee-Free, based on a fee-stacking rule the documents never state.**

- **non_determinism (Blocker)** — The customer's only criterion is the lowest ATM fees for 18 foreign withdrawals of $350. Green Fee-Free, Purple and Bluest all document a $0.00 foreign ATM fee. The gold breaks the tie with a rule from the notes, 'BOTH the out-of-network ATM fee AND the foreign ATM withdrawal fee apply', which no document states. The benchmark's own tasks 072 and 074 grade the opposite convention.
  - `doc_checking_accounts_green_fee-free_account_005: "Foreign ATM withdrawals are also fee-free: $0.00 per withdrawal."`
  - `doc_checking_accounts_purple_account_001: "No foreign ATM withdrawal fees: $0.00 per withdrawal (third-party ATM operator fees may still apply)"`
  - `doc_checking_accounts_bluest_account_003: "No foreign ATM withdrawal fees: $0.00"`
  - `doc_checking_accounts_purple_account_004: "You are eligible for refunds of ATM operator fees up to a monthly cap of $30."`
  - doc_business_checking_accounts_hunter_green_009: "If you see both a foreign ATM fee and a domestic out-of-network fee for the same international withdrawal, share the transaction details for review."
  - task_074 gold credits Purple the full $8.00 and $10.50 foreign fees and treats fee-free Purple foreign withdrawals (HK, Singapore, Frankfurt, Paris, Penang) as correct, i.e. Purple charges $0 on foreign withdrawals
  - `gold[2] account_class = "Green Fee-Free Account"; Replay with 'Purple Account' -> ['table accounts differs']`
  - *Why it matters:* Purple has the same $0 bank fee and also rebates up to $30/month of ATM operator surcharges, so a competent agent can reasonably open Purple, the account most likely to minimize total ATM cost. That opens a different account and fails.
  - *Fix:* Either document fee stacking on Purple and Bluest and remove the contrary evidence in tasks 072/074 and hunter_green_009, or give Purple a non-zero foreign fee, or accept multiple accounts.

*Verifier: Adjusted (Blocker → Major).* The gold follows a document-supported reading: the customer says the ATMs are out-of-network, Purple's $2.50 fee applies to any non-Rho ATM, and GFF documents $0 for both. The no-stacking reading (Purple $0 plus operator-fee rebates) is also defensible and leads to Purple, so this is two readings with different graded states: Major per calibration, not Blocker. The cross-task inconsistency with 072-074 (which assume no stacking) is real and should be fixed in one direction.

*Reconciled across runs: Major → Major (fact_error).* Fact: no personal-checking document states that the out-of-network and foreign ATM fees stack; only business-checking docs do (hunter_green_010, navy_blue_009), and hunter_green_009 treats seeing both as a reason for review. But purple_account_012 defines Purple's $2.50 fee by network membership with no domestic limit, and the customer says the ATMs abroad are out of network, so the gold's reading (Purple 18 x $2.50 = $45, Green Fee-Free uniquely $0 on both fees) is document-supported; run U's 'no KB document states this' overlooked those texts. The no-stacking reading (Purple and Bluest $0 abroad, with Purple's operator-fee rebates) leads to Purple or a tie, so this is two supported readings with different graded states: Major, not Blocker, under both scorers (accounts compared exactly).

### task_076 — Major

**Purple checking is the sensible answer, but Bluest also gives 2-day early deposit with equal or lower ATM fees and is ruled out only by a $75,000 opening deposit the customer is never asked about.**

- **underspecified_instructions (Major)** — Among accounts with 2-day early direct deposit, Bluest's foreign ATM fee is $0.00 and its rebate cap is larger than Purple's. Under the notes' own fee-stacking arithmetic Bluest is cheaper ($16 vs $20). The gold excludes Bluest as 'NOT PRACTICAL' because of its opening deposit, but the customer's instructions say nothing about available funds.
  - `doc_checking_accounts_bluest_account_002: "Deposit at least $75,000 to open your account."`
  - `doc_checking_accounts_bluest_account_001: "| Early direct deposit | 2 day(s) before payday |"`
  - `doc_checking_accounts_bluest_account_003: "No foreign ATM withdrawal fees: $0.00"; bluest_account_007: "ATM fee rebates up to $50 per month"`
  - `doc_checking_accounts_purple_account_001: "| Early direct deposit | 2 days early |"; "Global ATM fee rebates: up to $30 monthly worldwide"`
  - `task_076 description.notes: "BLUEST ACCOUNT: $2.00 out-of-network x 8 = $16 ... (but requires $50k-100k minimum deposit - NOT PRACTICAL)"`
  - `gold[2] account_class = "Purple Account"`
  - *Why it matters:* An agent that ranks strictly on the customer's stated criterion (lowest ATM fees, 2-day early deposit) can recommend Bluest. An agent that asks whether she can deposit $75,000 gets an improvised answer. Either path can open Bluest and fail the accounts table.
  - *Fix:* Add a line such as 'You can only put a few thousand dollars into the new account' to the instructions.
- **document_gap (Minor)** — The notes' arithmetic charges an out-of-network fee on top of the foreign fee (Purple $20), but no document says the fees stack. Task_074's gold treats Purple foreign withdrawals as $0. The choice of Purple doesn't change, only the fee the agent quotes.
  - `doc_checking_accounts_purple_account_001: "No foreign ATM withdrawal fees: $0.00 per withdrawal"`
  - doc_business_checking_accounts_hunter_green_009: "If you see both a foreign ATM fee and a domestic out-of-network fee for the same international withdrawal, share the transaction details for review."
  - *Why it matters:* The final state is unaffected. It only matters if the stacking assumption is reused elsewhere (task_075).
  - *Fix:* Drop the stacking assumption from the notes or document it.

*Verifier: Confirmed (Major → Major).* The Bluest affordability gap reproduces under both fee readings (Bluest is at least as cheap as Purple on ATM fees), and the gold depends on an unstated customer constraint, so Major stands. The secondary Minor issue is mis-founded but cosmetic.

### task_077 — Major

**The lost-wallet procedure can be followed step by step, but the replacement card's design is ambiguous: the customer asks for the 'best free option' and no 'fancy design', and the answer key only accepts the PREMIUM design.**

- **non_determinism (Major)** — For the Elite-tier Bluest replacement, all three designs are free. The customer's only guidance is 'whatever the best option is that's free with my account. I don't want to pay extra for shipping or a fancy card design', and she says it only if the agent asks. The gold's card_design='PREMIUM' (metallic) is one of three defensible choices. CLASSIC fits 'no fancy design' and CUSTOM is also free. card_design is stored in both debit_card_orders and debit_cards.
  - doc_bank_accounts_bank_accounts_(general)_029 ELITE TIER: "CLASSIC design: design_fee $0", "PREMIUM design (metallic silver): design_fee $0 (complimentary)", "CUSTOM design (uploaded image): design_fee $0 (complimentary)"
  - task_077 user_scenario: "ONLY IF agent asks about shipping speed or card design options: \"I'd like whatever the best option is that's free with my account. I don't want to pay extra for shipping or a fancy card design.\""
  - `gold[22].arguments.arguments: "delivery_option": "RUSH", "card_design": "PREMIUM"`
  - Replay: card_design CLASSIC -> ['table debit_card_orders differs', 'table debit_cards differs']; delivery_option EXPEDITED -> ['table debit_card_orders differs']
  - *Why it matters:* An agent that picks CLASSIC (taking 'no fancy design' literally, or because it never asked) or CUSTOM fails on two tables despite a correct and free replacement. RUSH is reasonably derivable as the best free shipping, but the design choice is a coin flip.
  - *Fix:* Have the customer state the design ('the standard classic design is fine' or 'the metallic premium one if it's free') and say it unprompted, or don't grade card_design.

*Verifier: Confirmed (Major → Major).* Reproduced: the gold replays cleanly and every step except the design is derivable (freeze, cross-product credit-card replacement per doc_030, pending-transaction read per doc_025 req. 4, forced unfreeze before close, RUSH free for ELITE, no Light Green order). The design is a real fork: doc_023 names CLASSIC as the default and the customer says no 'fancy card design', while the gold reads 'best free option' as PREMIUM. Under calibration (unscripted choice where the documented default differs from the gold) this is Major. The review did not cite doc_023's default, which supports its rating more strongly than the free-tie argument it gave.

### task_079 — Major

**Stolen-wallet task is solvable, but it records the freeze-then-unfreeze history and leans on reading a pending refund as a refund rather than a pending transaction.**

- **non_determinism (Minor)** — Same as task_078: the gold freezes all three cards, then unfreezes all three to close them, and the freeze/unfreeze dates persist on the closed cards. Closing the confirmed-stolen cards directly gives the same outcome but a different debit_cards table.
  - `doc_bank_accounts_bank_accounts_(general)_026: "If customer confirms the card is lost/stolen, recommend closing instead of freezing"`
  - `doc_bank_accounts_bank_accounts_(general)_026: "CLOSE: Permanent deactivation - cannot be reversed. Use when card is confirmed lost/stolen"`
  - `tools.py close_debit_card_4721: "Only ACTIVE or PENDING cards can be closed." (a FROZEN card must be unfrozen first)`
  - `freeze_debit_card_3892 writes card["frozen_date"]; unfreeze_debit_card_3893 writes card["unfrozen_date"]; both fields stay on the closed card in the gold DB`
  - `gold[4..6] freeze ev/lb/green; gold[13..15] unfreeze ev/lb/green; gold[17..19] close reason "stolen"`
  - *Why it matters:* An agent that follows doc_026 for a confirmed theft fails, even though every card ends CLOSED as in the gold.
  - *Fix:* Do not persist freeze/unfreeze timestamps on cards that end CLOSED, or exclude them from the comparison.
- **document_contradiction (Minor)** — The Green account's refund appears as a transaction with status "pending". doc_025 requirement 4 forbids closing a card with any pending transaction and has no bypass. Requirement 5 allows closing with a pending refund after written acknowledgment. The gold uses requirement 5.
  - doc_bank_accounts_bank_accounts_(general)_025: "4. No pending transactions: The card must not have any pending or processing transactions. If pending transactions exist, inform the customer they must wait for all transactions to settle"
  - doc_bank_accounts_bank_accounts_(general)_025: "5. No pending refunds: ... or acknowledge in writing that the refunds will be credited to the linked checking account instead."
  - `db (task agent_data) btxn_d0b8b00ed468: account chk_cr89a2b3c4_3, "REFUND - AMAZON.COM RETURN", amount 89.99, type "refund", status "pending"`
  - `gold[19] close dbc_cr89a2b3c4_green; gold[24] order chk_cr89a2b3c4_3 STANDARD/CLASSIC`
  - *Why it matters:* An agent that applies requirement 4 literally refuses to close the Green card and orders no replacement, so debit_cards and debit_card_orders differ from the gold. The refund-specific clause is the more natural reading, and the customer script supplies the acknowledgment, so the risk is small.
  - *Fix:* Say in requirement 4 that pending refunds are governed by requirement 5, or give the refund row a non-"pending" status such as "refund_pending".

*Verifier: Confirmed (Minor → Minor).* Reproduced both issues. Req. 5 is the specific rule for pending refunds and would be meaningless if req. 4 also covered them, so an agent can resolve the overlap, and the customer script supplies the acknowledgment. That fits the 'inconsistency the agent can resolve' reading of Minor. The freeze-path dependence is the same as in task_078. Shipping and design are scripted (quickest = RUSH $35, metallic if free = PREMIUM $0 at PREMIUM tier; Green standard).

*Reconciled across runs: Minor → Major (judgment).* Same path-dependence as 078, but here the theft is confirmed in the opening line, which is exactly when doc_026 says to recommend closing instead of freezing; the script does not cover that branch and follows the agent's guidance. Following the customer's literal freeze request and following doc_026 are both document-supported, and they produce different graded debit_cards rows: Major by calibration. That stated difference (theft confirmed up front) is why 079 is rated above 078. The pending-refund req 4 vs req 5 overlap is a resolvable Minor.

### task_082 — Blocker

**Fraud on the Green Fee-Free card maps to close-and-reissue and the customer asks for a new number, but the gold never replaces that card; several other stored dispute fields also have more than one defensible value.**

- **instruction_gold_mismatch (Blocker)** — The CryptoGems dispute on the Green Fee-Free card is card_not_present_fraud with card_action close_and_reissue, doc_031 says to perform the most severe action per card after filing, and the customer asks to reissue that card. The gold closes and reorders only the Blue card.
  - `doc_bank_accounts_bank_accounts_(general)_031: "'card_not_present_fraud' → 'close_and_reissue'"`
  - doc_bank_accounts_bank_accounts_(general)_031: "when performing the actual card action after filing all disputes, use the MOST SEVERE action across all disputes"
  - `user instructions step 7: "Green Fee-Free card: 'I'd like to keep using this card but maybe with a new number? Can you reissue it?'"`
  - `gold[15] btxn_d74e8a798f95 card_id dbc_mc47a2b9e1_gff "card_action": "close_and_reissue"`
  - `gold[17] close_debit_card_4721 only for dbc_mc47a2b9e1_blue; gold[19] order_debit_card_5739 only for chk_mc47a2b9e1_blue`
  - Replay: gold + close dbc_mc47a2b9e1_gff (fraud_suspected) + order chk_mc47a2b9e1_gff STANDARD/CLASSIC -> debit_cards and debit_card_orders differ (VERIFIED MATCH False)
  - *Why it matters:* A competent agent that does what the documents and the customer ask closes and reissues the Green Fee-Free card and is graded 0.
  - *Fix:* Add close_debit_card_4721(dbc_mc47a2b9e1_gff) and order_debit_card_5739(chk_mc47a2b9e1_gff, ...) to the gold, with the shipping choice scripted for the customer.
- **non_determinism (Major)** — Provisional credit for the FitLife recurring-charge dispute is set true, though recurring_charge_after_cancellation is listed as NOT REQUIRED (discretionary). Every other discretionary-category dispute in tasks 083-086 is gold false.
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is REQUIRED when ALL of these conditions are met: ... 2. Dispute Category: ... 'unauthorized_transaction' 'card_present_fraud' 'card_not_present_fraud' 'atm_cash_discrepancy' 'duplicate_charge'"
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is NOT REQUIRED (but may be offered at discretion) when: 1. The dispute category is: 'goods_services_not_received' 'recurring_charge_after_cancellation' 'atm_deposit_not_credited' 'incorrect_amount' 2. Customer has not contacted merchant first (for non-fraud disputes) 3. Customer shared their PIN voluntarily (pin_compromised = 'yes_shared')"
  - `gold[13] btxn_d1f51e0a0db9 recurring_charge_after_cancellation "provisional_credit_eligible": true`
  - task_083 gold goods_services_not_received false; task_084 incorrect_amount false; task_085 recurring_charge_after_cancellation false; task_086 goods_services_not_received / incorrect_amount / atm_deposit_not_credited false
  - *Why it matters:* The flag is stored (and drives provisional_credit_issued/amount), so an agent applying the REQUIRED list, or the convention used everywhere else, stores false and fails.
  - *Fix:* Set FitLife provisional_credit_eligible to false, or state in doc_032 when discretionary credit is granted.
- **non_determinism (Major)** — For the ElectroniX dispute the customer wrote the PIN on a sticky note in a lost wallet. The gold records pin_compromised "yes_shared" ("Customer shared PIN with someone"), and that choice is what makes provisional credit false. "unknown" or "yes_observed" are at least as defensible, and either makes the dispute REQUIRED-eligible. transaction_type "pin_purchase" is likewise inferred from "probably has the PIN".
  - tools.py pin_compromised: "'yes_shared', 'yes_observed', 'no', 'unknown'"; doc_031: "'yes_shared': Customer shared PIN with someone; 'yes_observed': Customer believes PIN was observed/skimmed"
  - `user instructions: "I had my PIN written on a sticky note in my wallet. So whoever has the card probably has the PIN too."`
  - `gold[12] "pin_compromised": "yes_shared", "provisional_credit_eligible": false, "transaction_type": "pin_purchase"`
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is NOT REQUIRED (but may be offered at discretion) when: 1. The dispute category is: 'goods_services_not_received' 'recurring_charge_after_cancellation' 'atm_deposit_not_credited' 'incorrect_amount' 2. Customer has not contacted merchant first (for non-fraud disputes) 3. Customer shared their PIN voluntarily (pin_compromised = 'yes_shared')"
  - *Why it matters:* pin_compromised, pin_shared_voluntarily, provisional_credit_eligible/issued/amount are all stored; a different PIN classification changes all of them.
  - *Fix:* Script the customer to say they gave the PIN to someone, or change the gold to "unknown" with provisional credit true; add a doc rule for written-down PINs.
- **non_determinism (Major)** — card_in_possession for the FitLife dispute is true in the gold because the customer still had the card when charged, but the field asks whether the customer still has the card now, and the Blue card is lost.
  - `tools.py: "card_in_possession (boolean): Whether the customer still has their physical debit card in their possession"`
  - `doc_031: "Ask: 'Do you still have your physical debit card in your possession?'"`
  - `user instructions: "No, I don't have the card anymore - it was in my wallet that I lost."`
  - `gold[13] FitLife "card_in_possession": true; gold[12] ElectroniX (same card) "card_in_possession": false`
  - *Why it matters:* An agent that answers the documented question for the same card gives false on both Blue disputes and fails.
  - *Fix:* Set FitLife card_in_possession to false, or redefine the field as possession at the time of the transaction.
- **non_determinism (Major)** — customer_max_liability_amount is 50 for all four disputes. doc_031 ties the tier to when the customer noticed and reported; FitLife was noticed 11/11 and the ATM shortfall 11/09, both more than 2 business days before today (11/14), which gives the $500 tier (89.99 and 100 after capping at the disputed amount). The statement date the rule names is never available.
  - doc_bank_accounts_bank_accounts_(general)_031: "inform the customer of their liability exposure based on when they noticed the unauthorized activity: - Reported within 2 business days of statement: Maximum liability $50 - Reported within 60 days of statement: Maximum liability $500"
  - tools.py file_debit_card_transaction_dispute_6281 docstring: "customer_max_liability_amount (number): The maximum dollar amount the customer could be liable for based on Regulation E reporting timing rules and the disputed amount."
  - `gold[13] FitLife discovery_date 11/11/2025, liability 50; gold[14] ATM discovery_date 11/09/2025, liability 50; clock get_now() = 2025-11-14`
  - *Why it matters:* The value is stored in each dispute row. Agents applying discovery-to-report timing, or capping at the disputed amount, write different numbers.
  - *Fix:* Give a single formula in doc_031 (timing basis, and whether to cap at the disputed amount) and include the statement date in tool output if the statement is the basis.
- **non_determinism (Major)** — The Blue card was lost and then used fraudulently. Both "lost" and "fraud_suspected" are documented close reasons. The verified scorer strips closure_reason, but order_debit_card_5739 copies it into the new card's issue_reason (lost vs fraud), so the choice still decides the result.
  - `doc_bank_accounts_bank_accounts_(general)_025: reasons "Lost card ... Suspected fraud/unauthorized transactions"`
  - `tools.py order_debit_card_5739: issue_reason = closure_reason if it is lost/stolen, "fraud" if fraud_suspected`
  - `Replay: gold with close reason fraud_suspected -> debit_cards dbc_6845d0896ace issue_reason "fraud" vs gold "lost" (VERIFIED MATCH False)`
  - *Why it matters:* This dependency survives the verified scorer's closure_reason relaxation, so a defensible fraud_suspected close fails.
  - *Fix:* Script the reason, or exclude issue_reason derived from closure_reason when closure_reason itself is excluded.
- **underspecified_instructions (Minor)** — The customer script gives no Blue replacement shipping preference (MID tier allows STANDARD $0 or EXPEDITED $15), and gives the CryptoGems discovery date as "January 9th" while saying "today".
  - `user instructions step 8: "CryptoGems Store (online fraud): 'I discovered this one today, January 9th.'"`
  - `gold[15] "discovery_date": "11/14/2025"; gold[19] delivery_option STANDARD, delivery_fee 0`
  - *Why it matters:* The simulated customer may pick expedited or give a January date; both change stored fields.
  - *Fix:* Fix the date to November 14th and script "standard shipping is fine".

*Verifier: Confirmed (Blocker → Blocker).* Reproduced the Blocker. The documents and the customer both require closing the Green Fee-Free card after a card_not_present_fraud dispute, the gold leaves it ACTIVE, and that close changes debit_cards even with closure_reason stripped. The secondary Major forks also reproduce: FitLife discretionary credit true (it disagrees with the 083-086 convention), yes_shared for a written-down PIN, FitLife card_in_possession, the $50 liability with no statement date, and lost vs fraud_suspected surviving through issue_reason. The unscripted Blue shipping is rated Minor, but doc_023 labels a default only for design, not delivery, so by calibration it is Major; task severity is unaffected.

### task_083 — Blocker

**This task is graded on exact tool-call text, and the official dispute calls leave out a required field, so they fail when run and no correct call can ever match them.**

- **argument_error (Blocker)** — All four gold file_debit_card_transaction_dispute_6281 calls omit customer_max_liability_amount, a required parameter with no default. Replaying them returns a TypeError error and files nothing.
  - `tools.py signature: "customer_max_liability_amount: float," (no default)`
  - Replay gold[6..9]: "Error: Invalid arguments: KnowledgeTools.file_debit_card_transaction_dispute_6281() missing 1 required positional argument: 'customer_max_liability_amount'"
  - `reward_basis = ["ACTION"]`
  - *Why it matters:* A correct agent must include the field to file any dispute, so its arguments can never equal the gold's; reward is 0 for correct work.
  - *Fix:* Add customer_max_liability_amount to each gold call, or regrade the task on DB state.
- **grading_basis_mismatch (Blocker)** — ACTION grading with compare_args unset compares the inner arguments value as a literal JSON string. The gold strings use a particular key order, spacing and number spelling such as "150.00", so even a semantically identical call almost never matches byte for byte.
  - data_model/tasks.py Action.compare_with_tool_call: "if self.compare_args is None: compare_args = tool_call.arguments.keys()" ... "return tool_args == action_args"
  - `gold[6] arguments string contains "\"disputed_amount\": 150.00" and places card_action last`
  - `gold[6..9] compare_args = null`
  - *Why it matters:* Even after the missing field is added, matching depends on JSON formatting, not on correctness.
  - *Fix:* Grade on DB state, or compare parsed JSON objects (and only the decisive keys) instead of raw strings.
- **non_determinism (Major)** — The duplicate Austin Coffee Roasters charges share date, amount and description. The gold disputes the second-listed row, which is the earlier one only if the agent infers intra-day order from the most-recent-first listing; the doc's "earliest (first)" also invites picking the first-listed row.
  - `doc_bank_accounts_bank_accounts_(general)_031: "Dispute the earliest (first) transaction when multiple duplicates exist."`
  - `doc_bank_accounts_bank_accounts_(general)_018: "Transactions are returned in reverse chronological order (most recent first)."`
  - `tools.py get_bank_account_transactions_9173: stable sort by date descending; rows carry date only (MM/DD/YYYY), no time`
  - `Tool order for chk_dk83f5c2a1_gff: btxn_ff7d3926dee0 (11/11/2025, -67.25) listed before btxn_d937eaa1d21d (11/11/2025, -67.25)`
  - `gold[8] transaction_id btxn_d937eaa1d21d`
  - *Why it matters:* Secondary here because the task is already unpassable; it would decide the transaction_id once the Blockers are fixed.
  - *Fix:* Give the duplicate rows timestamps, or state the tie-break rule in terms of list position.
- **non_determinism (Major)** — doc_032 does not say which list wins when a dispute meets both the REQUIRED and NOT REQUIRED lists. The gold resolves the conflict in opposite directions: the duplicate charge with no merchant contact is true (REQUIRED wins), and the PIN-shared GameStop dispute is false (NOT REQUIRED wins).
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is REQUIRED when ALL of these conditions are met: ... 2. Dispute Category: ... 'unauthorized_transaction' 'card_present_fraud' 'card_not_present_fraud' 'atm_cash_discrepancy' 'duplicate_charge'"
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is NOT REQUIRED (but may be offered at discretion) when: 1. The dispute category is: 'goods_services_not_received' 'recurring_charge_after_cancellation' 'atm_deposit_not_credited' 'incorrect_amount' 2. Customer has not contacted merchant first (for non-fraud disputes) 3. Customer shared their PIN voluntarily (pin_compromised = 'yes_shared')"
  - `gold[8] duplicate_charge contacted_merchant false, provisional_credit_eligible true`
  - `gold[9] unauthorized_transaction pin_compromised yes_shared, provisional_credit_eligible false`
  - *Why it matters:* Secondary here (the task is unpassable); in DB-graded siblings the same conflict decides stored flags.
  - *Fix:* Add a precedence rule to doc_032.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced: the four gold dispute calls fail with a TypeError and only a byte-identical, field-omitting (and therefore failing) call could match them, so no correct agent passes. The verified scorer does not apply (ACTION-only grading). Secondary Major issues (duplicate-row inference, provisional-credit precedence) hold as stated.

### task_084 — Blocker

**The stored liability amounts follow no single rule: the $47.50 duplicate gets $50 (not capped) while the $412.88 late fraud gets $412.88 (capped), so any consistent calculation misses one of them.**

- **non_determinism (Blocker)** — customer_max_liability_amount is 50 for the $47.50 duplicate (above the disputed amount) but 412.88 = min(500, 412.88) for the late TechWorld fraud. Capping at the disputed amount, as the tool docstring says, gives 47.5 for the duplicate; not capping gives 500 for TechWorld. Discovery-based timing would also put the duplicate (noticed 11/10) and the incorrect-amount dispute (noticed 11/09) in the $500 tier.
  - doc_bank_accounts_bank_accounts_(general)_031: "inform the customer of their liability exposure based on when they noticed the unauthorized activity: - Reported within 2 business days of statement: Maximum liability $50 - Reported within 60 days of statement: Maximum liability $500"
  - tools.py file_debit_card_transaction_dispute_6281 docstring: "customer_max_liability_amount (number): The maximum dollar amount the customer could be liable for based on Regulation E reporting timing rules and the disputed amount."
  - `gold[12] btxn_e8c3b09d2c45 disputed_amount 47.5, "customer_max_liability_amount": 50`
  - `gold[13] btxn_f9d4c10e3d56 incorrect_amount discovery 11/09/2025, "customer_max_liability_amount": 50`
  - `gold[14] btxn_c2g7f43h6g89 disputed_amount 412.88, "customer_max_liability_amount": 412.88`
  - `user instructions step 9: "my liability could be up to $500 since I'm reporting it after the 2-day window? That's still better than losing the full $412."`
  - *Why it matters:* Each value is stored in debit_card_disputes. Neither "always cap" nor "never cap" reproduces the gold, so a consistent agent fails.
  - *Fix:* Document one formula (e.g. min(tier cap, disputed amount), timing measured from a stated date) and recompute all three gold values with it.
- **non_determinism (Major)** — The duplicate Bella's Bistro rows have the same date, amount and description. The gold disputes the second-listed row; that is "earliest" only by inferring intra-day order from the newest-first listing, and the doc's "earliest (first)" invites the first-listed row.
  - `doc_bank_accounts_bank_accounts_(general)_031: "Dispute the earliest (first) transaction when multiple duplicates exist."`
  - `doc_bank_accounts_bank_accounts_(general)_018: "Transactions are returned in reverse chronological order (most recent first)."`
  - `tools.py get_bank_account_transactions_9173: stable sort by date descending; rows carry date only (MM/DD/YYYY), no time`
  - `Tool order for chk_b8d92f4c17: btxn_d7f2a98c1b34 (11/06/2025, -47.5) then btxn_e8c3b09d2c45 (11/06/2025, -47.5)`
  - `gold[12] transaction_id btxn_e8c3b09d2c45`
  - *Why it matters:* The transaction_id and dispute_id are stored; picking the other row fails. v1.0.1's newest-first sort makes the gold derivable, but only through this inference.
  - *Fix:* Add timestamps to the rows or phrase the tie-break as "the lower of identical same-day rows in the tool output".
- **non_determinism (Major)** — The duplicate charge is a REQUIRED category, but the customer has not contacted the merchant, which doc_032 lists as NOT REQUIRED for non-fraud disputes. The gold stores true without a stated precedence.
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is REQUIRED when ALL of these conditions are met: ... 2. Dispute Category: ... 'unauthorized_transaction' 'card_present_fraud' 'card_not_present_fraud' 'atm_cash_discrepancy' 'duplicate_charge'"
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is NOT REQUIRED (but may be offered at discretion) when: 1. The dispute category is: 'goods_services_not_received' 'recurring_charge_after_cancellation' 'atm_deposit_not_credited' 'incorrect_amount' 2. Customer has not contacted merchant first (for non-fraud disputes) 3. Customer shared their PIN voluntarily (pin_compromised = 'yes_shared')"
  - `gold[12] duplicate_charge contacted_merchant false, provisional_credit_eligible true`
  - *Why it matters:* An agent that lets the NOT REQUIRED condition win stores false and fails.
  - *Fix:* Add a precedence rule to doc_032.

*Verifier: Confirmed (Blocker → Blocker).* Neither 'always cap at the disputed amount' nor 'never cap' reproduces both gold[12] (50 for $47.50) and gold[14] (412.88), and both values are stored exactly in debit_card_disputes, so a consistent agent fails one of them; the gold follows no single doc-supported rule, so Blocker stands under calibration. The review's note that close reason is irrelevant here is correct (replayed).

### task_085 — Major

**The verify-the-customer's-claims flow is sound, but the duplicate-row pick, liability amounts, a provisional-credit flag and an unscripted merchant-contact answer each have more than one defensible stored value.**

- **non_determinism (Major)** — The two CityFit rows are identical (11/06/2025, -89.99). After v1.0.1 swapped the fixture rows, the gold disputes the second-listed row, which is "earliest" only by inferring intra-day order from the newest-first listing.
  - `doc_bank_accounts_bank_accounts_(general)_031: "Dispute the earliest (first) transaction when multiple duplicates exist."`
  - `doc_bank_accounts_bank_accounts_(general)_018: "Transactions are returned in reverse chronological order (most recent first)."`
  - `tools.py get_bank_account_transactions_9173: stable sort by date descending; rows carry date only (MM/DD/YYYY), no time`
  - `Tool order for chk_b4d92f7c28: btxn_c3d4e5f6g703 then btxn_b2c3d4e5f602, both 11/06/2025 -89.99`
  - `gold[10] transaction_id btxn_b2c3d4e5f602`
  - `v1.0.1 diff: fixture rows btxn_b2c3d4e5f602 and btxn_c3d4e5f6g703 swapped`
  - *Why it matters:* Disputing the first-listed row stores a different transaction_id and dispute_id.
  - *Fix:* Add timestamps or phrase the tie-break in terms of list position.
- **non_determinism (Major)** — Liability is 50 for all three disputes, including the $14.99 Prime Streaming charge (uncapped, unlike task_084/086 where the $500 tier is capped at the amount). Discovery-based timing puts the ATM (noticed 11/05) and duplicate (noticed 11/08) disputes in the $500 tier.
  - doc_bank_accounts_bank_accounts_(general)_031: "inform the customer of their liability exposure based on when they noticed the unauthorized activity: - Reported within 2 business days of statement: Maximum liability $50 - Reported within 60 days of statement: Maximum liability $500"
  - tools.py file_debit_card_transaction_dispute_6281 docstring: "customer_max_liability_amount (number): The maximum dollar amount the customer could be liable for based on Regulation E reporting timing rules and the disputed amount."
  - `gold[9] ATM discovery 11/05/2025 liability 50; gold[10] duplicate discovery 11/08/2025 liability 50; gold[12] disputed_amount 14.99 liability 50`
  - *Why it matters:* An agent that caps at the disputed amount (as the docstring says) stores 14.99 and fails; discovery-based timing changes the other two.
  - *Fix:* Document one liability formula and apply it across tasks 082-088.
- **non_determinism (Major)** — The duplicate charge is a REQUIRED category but the customer has not contacted the merchant (a NOT REQUIRED condition); the gold stores true without a stated precedence.
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is REQUIRED when ALL of these conditions are met: ... 2. Dispute Category: ... 'unauthorized_transaction' 'card_present_fraud' 'card_not_present_fraud' 'atm_cash_discrepancy' 'duplicate_charge'"
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is NOT REQUIRED (but may be offered at discretion) when: 1. The dispute category is: 'goods_services_not_received' 'recurring_charge_after_cancellation' 'atm_deposit_not_credited' 'incorrect_amount' 2. Customer has not contacted merchant first (for non-fraud disputes) 3. Customer shared their PIN voluntarily (pin_compromised = 'yes_shared')"
  - `gold[10] duplicate_charge contacted_merchant false, provisional_credit_eligible true`
  - *Why it matters:* An agent that lets the NOT REQUIRED condition win stores false and fails.
  - *Fix:* Add a precedence rule to doc_032.
- **underspecified_instructions (Major)** — For the Prime Streaming dispute the script never answers "did you contact the merchant?"; the customer only says they cancelled weeks ago. The gold stores contacted_merchant false, but a simulated customer may say they contacted the merchant to cancel. transaction_type for the CityFit duplicate is also unscripted (gold recurring_payment, supported only by "MONTHLY" in the description).
  - `user instructions step 6: "I cancelled that subscription weeks ago and shouldn't have been charged." (no merchant-contact answer)`
  - `gold[12] contacted_merchant false; task_082 gold FitLife (customer called merchant) contacted_merchant true`
  - `gold[10] transaction_type "recurring_payment"; tool row description "CITYFIT GYM MONTHLY DENVER", type debit_card_purchase`
  - *Why it matters:* Both booleans and enums are stored; the outcome depends on what the user simulator improvises.
  - *Fix:* Script "No, I haven't contacted them about this charge" and the transaction type.

*Verifier: Confirmed (Major → Major).* All four issues reproduce and each changes debit_card_disputes. Unlike task_084, the gold's liability values are internally consistent under one reading (all $50 tier, never capped), so this is the two-readings case and Major is right per calibration.

### task_086 — Major

**The six-dispute workflow is reconstructible, but whether to file the ATM-deposit dispute at all, how to code the skimmed-card fraud, and the liability amounts each have more than one defensible answer.**

- **instruction_gold_mismatch (Major)** — The customer claims a $500 deposit with $300 credited; the record shows $400 credited and no images are available. When told the records differ, the scripted reply is "I might be mixing it up with another deposit. If your records show that, then I'll go with what you have." The gold still files a $100 atm_deposit_not_credited dispute (500 - 400). Accepting the record can equally mean nothing is missing and no dispute is filed.
  - user instructions step 5: "I deposited $500 in cash but only $300 was credited ... If agent says records show a different amount: 'Hmm... Actually, I might be mixing it up with another deposit. If your records show that, then I'll go with what you have.'"
  - `tool row btxn_0788d2513c8c: "RHO-BANK ATM #6172 DEPOSIT", amount 400.0, type atm_deposit`
  - `get_atm_deposit_images_8473(btxn_0788d2513c8c): "Status: IMAGES NOT AVAILABLE"`
  - `gold[16] atm_deposit_not_credited disputed_amount 100.0`
  - *Why it matters:* Filing or not filing adds or removes a whole dispute row; an agent that takes the customer's concession at face value fails.
  - *Fix:* Script the customer to keep claiming a $500 deposit after seeing $400 credited, or drop the dispute from the gold.
- **non_determinism (Major)** — For the TechWorld fraud the customer says only "I think someone skimmed my card at a gas station". The gold stores pin_compromised "unknown" and transaction_type "pin_purchase". doc_031 defines "yes_observed" as "PIN was observed/skimmed", and nothing says whether the Miami purchase used a PIN or a signature.
  - `doc_031: "'yes_observed': Customer believes PIN was observed/skimmed"; "'unknown': Customer unsure"`
  - `user instructions step 5: "Still have card - I think someone skimmed my card at a gas station or something."`
  - `tool row btxn_5690acdd3de5: type debit_card_purchase (no PIN/signature field)`
  - `gold[15] "transaction_type": "pin_purchase", "pin_compromised": "unknown"`
  - *Why it matters:* Both fields are stored; "yes_observed" or "signature_purchase" are defensible and fail.
  - *Fix:* Script the PIN/signature detail and the PIN belief, as task_084 does.
- **non_determinism (Major)** — Liability is 50 for the four recent disputes and 500 for TechWorld. Discovery-based timing (doc_031 "based on when they noticed") puts the ATM (noticed 11/07), SupplyPro (11/09), Phoenix Kitchen (11/09) and ATM deposit (11/08) disputes in the $500 tier, which after capping gives 100, 189.99, 200 and 100.
  - doc_bank_accounts_bank_accounts_(general)_031: "inform the customer of their liability exposure based on when they noticed the unauthorized activity: - Reported within 2 business days of statement: Maximum liability $50 - Reported within 60 days of statement: Maximum liability $500"
  - tools.py file_debit_card_transaction_dispute_6281 docstring: "customer_max_liability_amount (number): The maximum dollar amount the customer could be liable for based on Regulation E reporting timing rules and the disputed amount."
  - `gold[11],[12],[14],[16] liability 50 with discovery dates 11/07, 11/09, 11/09, 11/08; gold[15] TechWorld liability 500`
  - *Why it matters:* The gold is reproducible under "recent transaction -> $50, old transaction -> min($500, amount)", but not under the discovery-timing reading the doc describes.
  - *Fix:* Document one liability formula with a stated reference date.
- **underspecified_instructions (Minor)** — The script gives the TechWorld discovery date as "today 01/12" although today is 11/14; the gold uses 11/14/2025.
  - `user instructions: "Just discovered today 01/12 during year-end reconciliation."`
  - `gold[15] "discovery_date": "11/14/2025"`
  - *Why it matters:* A simulated customer may state January 12; an agent recording it fails.
  - *Fix:* Change the script to "today, November 14th".

*Verifier: Confirmed (Major → Major).* Reproduced all four issues; each changes debit_card_disputes. The close reason does matter here because a replacement is ordered, but fraud_suspected is the clear doc_025 reason for a skimmed card the customer still holds, so it is not an additional defect.

### task_087 — Major

**The decline-diagnosis steps are clear, but when the customer reports a fraudulent charge the KB says to escalate to the security team, while the gold files a dispute and replaces the card.**

- **document_contradiction (Major)** — doc_039 lists "Customer reports transactions they did not make" as a case to escalate to the security team. The gold handles the $499.99 TechZone charge by filing a dispute, closing the card and ordering a replacement (doc_031/025/029). Neither the CODE 05 steps nor doc_039 say which applies.
  - `doc_bank_accounts_bank_accounts_(general)_039: "Escalate to security team when: ... - Customer reports transactions they did not make"`
  - doc_checking_accounts_checking_accounts_(general)_003: "If fraud_alert_active is TRUE and alert_source is 'customer_initiated' → Ask customer to verify recent transactions. If they confirm all transactions are legitimate, clear the alert." (no instruction for the non-legitimate case)
  - `gold[15] dispute btxn_70fb52ef4e29 card_present_fraud; gold[17] close fraud_suspected; gold[19] order EXPEDITED/PREMIUM`
  - *Why it matters:* An agent that escalates per doc_039 transfers before filing anything and ends with no dispute, closure or order; it scores 0. The customer script accepts either path ("If agent doesn't mention filing a dispute: Accept whatever they offer").
  - *Fix:* Make doc_039 say to file a dispute and close/reissue for customer-reported fraud on a customer-initiated alert, and escalate only for bank-initiated alerts or identity doubts.

*Verifier: Confirmed (Major → Major).* The doc_039 vs dispute-and-reissue conflict reproduces and is a two-readings Major. The review keeps the liability timing risk in notes only; it is the same class it rates Major in 085/086, though here the customer's same-day fraud-alert report makes $50 the stronger reading, so the task severity is unchanged.

*Reconciled across runs: Major → Major (judgment).* doc_039 tells the agent to escalate to the security team when the customer reports transactions they did not make, which is exactly this case, and nothing tells it to file the dispute, close and reorder first. The gold handles the fraud in-channel, and an agent that escalates per doc_039 ends the episode before any of the graded writes. Run U's 'escalate after the writes' reconciliation is the agent's own invention, not documented guidance, so these are two supported readings with different graded states: Major under both scorers.

### task_088 — Major

**The KB's chip-mismatch procedure says to freeze the card until a replacement arrives and to follow the stolen-card protocol, while the gold closes it as fraud; the fraud charge's PIN/signature type is also never given.**

- **document_contradiction (Major)** — The CODE 82 procedure says "Follow stolen card protocol" and "Recommend freezing the card until a replacement arrives". The gold instead closes the Evergreen card with reason fraud_suspected (via the doc_031 close_and_reissue mapping) before ordering. Freezing and then ordering leaves the old card FROZEN and gives the new card issue_reason first_card; closing as "stolen" gives issue_reason stolen.
  - doc_checking_accounts_purple_account_007: "If suspicious transactions found: Follow stolen card protocol to assist the customer. - Recommend freezing the card until a replacement arrives."
  - `doc_031: "'card_present_fraud' → 'close_and_reissue'"`
  - `task notes: "agent must follow stolen card protocol: file dispute, CLOSE the card (not freeze), order replacement"`
  - `Replay: freeze instead of close, then order -> old card FROZEN and new card issue_reason first_card (VERIFIED MATCH False)`
  - `Replay: close reason "stolen" -> new card issue_reason stolen vs gold fraud (VERIFIED MATCH False)`
  - `user instructions step 21: "If agent says they'll freeze the card: 'Okay, if that's what needs to happen.'"`
  - *Why it matters:* Two doc-supported alternatives both fail, and the second fails even under the verified scorer because the close reason flows into the new card's issue_reason.
  - *Fix:* Rewrite the CODE 82 step to "file a dispute, close the card as fraud_suspected and order a replacement", matching the gold.
- **underspecified_instructions (Major)** — For the Electro Mart Miami dispute the gold stores transaction_type "signature_purchase" and pin_compromised "no". The customer script has no PIN or transaction-type answers, and the tool row is a generic debit_card_purchase. Signature follows only from reasoning that a cloned card used without a known PIN must be signed.
  - `tool row btxn_28eee7145c29: "ELECTRO MART MIAMI FL", -347.99, type debit_card_purchase`
  - `user instructions: no line covering PIN or PIN/signature for the Miami charge`
  - `gold[10] "transaction_type": "signature_purchase", "pin_compromised": "no"`
  - *Why it matters:* Both fields are stored; "pin_purchase" or "unknown" are defensible and fail.
  - *Fix:* Script the PIN answer and the transaction type, or set them from a field in the transaction record.

*Verifier: Confirmed (Major → Major).* Both issues reproduce, including the point that the stolen close reason fails even under the verified scorer because it flows into the new card's issue_reason. Unflagged: gold[10] liability 50 for an 11/09 charge reported 11/14 depends on the same timing reading rated Major in 085/086; the task is already Major. The Blue-card security transfer is ungraded (no DB effect), a Minor-class 'rule the grader cannot see' not listed.

### task_091 — Blocker

**The official answer orders the cheapest replacement card although the customer asked for the most premium free one, and it orders a Light Blue replacement that the rules say must wait 48 hours.**

- **argument_error (Blocker)** — The customer asks for "the most premium free option for both" shipping and card type on the Evergreen replacement. Evergreen is Premium tier, where EXPEDITED shipping and the PREMIUM design both cost $0, yet gold orders STANDARD shipping with a CLASSIC design.
  - `user instruction 20: "If agent asks about replacement card preferences for shipping or card type: \"I want the most premium free option for both.\""`
  - `doc_bank_accounts_bank_accounts_(general)_005: "PREMIUM TIER (Evergreen Account)"`
  - doc_bank_accounts_bank_accounts_(general)_029 PREMIUM TIER: "Free expedited shipping on all replacements (delivery_fee: $0 for both STANDARD and EXPEDITED)" and "PREMIUM design (metallic silver): design_fee $0 (complimentary)"
  - `gold[14].arguments: delivery_option "STANDARD", card_design "CLASSIC" for chk_tw34a7d9e2_evergreen`
  - `replay: gold with EXPEDITED + PREMIUM on gold[14] -> verified match False (debit_card_orders, debit_cards differ)`
  - *Why it matters:* An agent that follows the customer and the tier table orders EXPEDITED/PREMIUM. The order_id hash and the stored card_design both change, so correct work fails.
  - *Fix:* Change gold[14] to delivery_option "EXPEDITED", card_design "PREMIUM" (fees 0), or change the customer line to ask for the standard free option.
- **instruction_gold_mismatch (Blocker)** — The Light Blue card scores in the 11-14 band even after the customer confirms the Bellevue attempts. At that score doc_041 offers three options (closure, transfer, PIN reset), and the simulator accepts whichever is offered. Gold also orders an Entry-tier replacement right away, against the documented 48-hour wait.
  - doc_bank_accounts_bank_accounts_(general)_041: "11-14 | VERY HIGH | Cannot unlock on this call. Require callback verification OR enhanced verification (last 4 SSN + security question)."
  - doc_041 STEP 6: "If no unauthorized transactions: Explain the security concern and offer options: Card closure and replacement (recommended if fraud suspected); Transfer to security team for investigation; PIN reset (issues new PIN, invalidates potential compromise)"
  - user instructions 41/44/45/47: confirms "that was definitely me"; accepts closure ("Fine, close it and send me a new one"), transfer ("Ugh, okay"), or PIN reset ("Sure, set it to 4121")
  - doc_bank_accounts_bank_accounts_(general)_029 ENTRY TIER: "48-hour waiting period after card closure before a replacement can be ordered"; doc_005: "ENTRY TIER (Light Blue Account, ...)"
  - `gold[23] close_debit_card_4721 dbc_tw34a7d9e2_lightblue fraud_suspected; gold[24] order_debit_card_5739 chk_tw34a7d9e2_lightblue immediately after`
  - Light Blue flags after location removal: B1 1 (23:02), B2 2 (last PIN 10/08), B3 2 (87s/115s), C2 1 (all $400), C3 1-2, C4 2 (3x$400 > $700 limit), D1 1, E1 1, E2 1 (10/25 overdraft) = 12-13
  - `replay: Light Blue PIN reset instead of close, transfer only, or close without the immediate order -> all verified match False`
  - *Why it matters:* The customer insists the attempts were his, so fraud is not suspected and closure is not the recommended option. A reset or a transfer writes a different final state. An agent that does close the card must still not order an Entry-tier replacement for 48 hours, so it cannot match gold[24].
  - *Fix:* Script the customer to pick closure explicitly and drop gold[24] (or make the account a tier without a waiting period). Alternatively, raise the score into the 15+ CRITICAL band so closure is mandated.
- **non_determinism (Major)** — The customer's answer about PIN compromise ("Maybe someone watched me at an ATM? I really don't know.") fits pin_compromised "unknown" at least as well as gold's "yes_observed", and the value is stored in both dispute records.
  - `user instruction 22: "I never shared it with anyone. Maybe someone watched me at an ATM? I really don't know."`
  - `doc_bank_accounts_bank_accounts_(general)_031: "'yes_observed': Customer believes PIN was observed/skimmed" vs "'unknown': Customer unsure"`
  - `gold[16].arguments / gold[17].arguments: "pin_compromised": "yes_observed"`
  - `tools.py file_debit_card_transaction_dispute_6281 stores "pin_compromised" in the debit_card_disputes record`
  - `replay: pin_compromised "unknown" -> verified match False (debit_card_disputes differs)`
  - *Why it matters:* A careful agent that records "Customer unsure" as "unknown" writes different dispute records and fails.
  - *Fix:* Have the customer state a belief ("I think someone must have watched me enter it"), or accept either value.
- **document_gap (Minor)** — The Green card is LOW risk with no prior locks, so the protocol says "unlock". No unlock tool exists, and no document says that reset_debit_card_pin_6284 unlocks a card. The customer also says he knows his PIN, which doc_027 routes to change_debit_card_pin_6285, a tool that does not clear the lock.
  - tools.py reset_debit_card_pin_6284 docstring: "Reset a debit card PIN when the customer has forgotten it." (the code also sets pin_locked=False, but only the tool output after the call says "Your card has been unlocked")
  - `doc_bank_accounts_bank_accounts_(general)_027 PIN Reset/PIN Change steps never mention unlocking a locked card`
  - doc_bank_accounts_bank_accounts_(general)_041 STEP 3: "0-4 | LOW | Unlock after standard identity verification"; no unlock tool exists in tools.py (no discoverable method other than reset_debit_card_pin_6284 clears pin_locked)
  - `user instruction 8: "Yeah, I know my PIN. I must have just fat-fingered it a few times."`
  - `gold[8] reset_debit_card_pin_6284 dbc_tw34a7d9e2_green new_pin 2589`
  - *Why it matters:* The gold is reachable only by inferring that reset is the unlock mechanism. An agent that uses change-PIN, or tells the customer it cannot unlock, leaves pin_locked=True and fails.
  - *Fix:* State in doc_041 or doc_027 that reset_debit_card_pin_6284 also clears pin_locked and is the unlock path.
- **argument_error (Minor)** — The customer script gives DOB 09/22/1991, but the DB and gold[0] use 09/22/2001. Verification still succeeds on phone, email, and address, so the agent can resolve it by logging the on-file values.
  - `user instructions: "DOB: 09/22/1991"`
  - `task initial_state users.tw34a7d9e2.date_of_birth = "09/22/2001"`
  - `gold[0].arguments.date_of_birth = "09/22/2001"`
  - *Why it matters:* An agent that logs the DOB the customer stated, or that refuses verification over the mismatch, diverges in verification_history.
  - *Fix:* Make the script DOB 09/22/2001.

*Verifier: Confirmed (Blocker → Blocker).* Two independent Blockers reproduce: gold[14] contradicts the customer's explicit request under the Premium-tier table, and gold[24] orders an Entry-tier replacement the documents forbid for 48 hours, so the gold follows no doc-supported reading. The Green-card unlock-by-reset gap is rated Minor, but needing an undocumented convention is the Major definition; this does not change the task severity.

### task_092 — Major

**The four-card case is reachable because the customer's scripted answers steer each card, but the rule for a single 3-point risk flag never says whether to unlock, transfer, or replace.**

- **non_determinism (Minor)** — The Green card scores only 5 (MEDIUM, unlockable after the customer confirms), but B3=3 triggers "escalate to supervisor review". Gold reads that as closing and replacing the card with reason fraud_suspected even though the customer confirmed the attempts. The closure reason survives the verified scorer through the new card's issue_reason.
  - `db bank_account_transaction_history: Green declines at 11:42:15, 11:42:32, 11:42:51 (17s/19s gaps -> B3 = 3); Blue has fraud_alert_active=true (D3 +2); total 5`
  - doc_bank_accounts_bank_accounts_(general)_041: "If ANY single flag equals 3 points, escalate to supervisor review regardless of total score." and "5-7 | MEDIUM | Unlock only after asking..."
  - `user instruction 21: "If agent offers to close and replace OR transfer to security: Fine, I'll take a new card then."`
  - `gold[13] close_debit_card_4721 dbc_rw42b8d3e1_green reason "fraud_suspected"; gold[14] order STANDARD/CLASSIC`
  - `tools.py order_debit_card_5739: issue_reason = closure_reason if closure_reason != "fraud_suspected" else "fraud"; other reasons -> "first_card"`
  - `replay: Green closed with "no_longer_needed" or "damaged" -> verified match False (debit_cards differs); Green reset instead of close -> False`
  - *Why it matters:* The simulator steers to close-and-replace whenever closure or transfer is offered. Two divergences remain: an agent that transfers immediately ends the call before cards 3-4, and an agent that picks a non-fraud closure reason for a customer who confirmed the attempts writes issue_reason "first_card".
  - *Fix:* Spell out in doc_041 what "supervisor review" means for a chat agent (for example, "cannot unlock; offer closure/replacement with reason fraud_suspected").
- **document_gap (Minor)** — The Evergreen card is LOW/MEDIUM and should be unlocked, but no unlock tool exists and no document says a PIN reset unlocks. Gold uses reset_debit_card_pin_6284.
  - tools.py reset_debit_card_pin_6284 docstring: "Reset a debit card PIN when the customer has forgotten it." (the code also sets pin_locked=False, but only the tool output after the call says "Your card has been unlocked")
  - `doc_bank_accounts_bank_accounts_(general)_027 PIN Reset/PIN Change steps never mention unlocking a locked card`
  - doc_bank_accounts_bank_accounts_(general)_041 STEP 3: "0-4 | LOW | Unlock after standard identity verification"; no unlock tool exists in tools.py (no discoverable method other than reset_debit_card_pin_6284 clears pin_locked)
  - `gold[18] reset_debit_card_pin_6284 dbc_rw42b8d3e1_evergreen new_pin 8127`
  - `replay: change_debit_card_pin_6285 instead -> verified match False (reset tool name missing; debit_cards differs)`
  - *Why it matters:* An agent that does not infer reset-as-unlock leaves pin_locked=True or uses change-PIN, and fails.
  - *Fix:* Document in doc_041/027 that reset_debit_card_pin_6284 clears the PIN lock.

*Reconciled across runs: Minor → Major (judgment).* Two Majors, both on writes compared exactly under either scorer. No document or tool says how to unlock a PIN-locked card, yet the gold unlocks Evergreen via reset_debit_card_pin_6284 (documented for forgotten PINs); an undocumented convention is Major by definition, as run V's own 091 verifier noted. On the Green card, doc_041 Step 6 lists a PIN reset the script accepts ('Sure, set it to 4567') while the gold closes with fraud_suspected for a customer who confirmed the attempts, which is two supported readings; run V's 092 was never verified.

### task_094 — Major

**The Gold Rewards Card's 0.025% bonus is described both as a card bonus (outranked by the EcoCard) and as a separate relationship bonus that stacks, so the correct credit could be $140 or $142.**

- **document_contradiction (Major)** — Gold expects 6.85% (5.5 base + 0.75 Green boost + 0.6 EcoCard), which treats the Gold Rewards Card 0.025% purely as a credit-card bonus outranked by the EcoCard. doc_013 instead calls it a relationship bonus "on top of the base rate", and doc_045 says relationship bonuses stack with card bonuses, which gives 6.875% and a $142.00 credit.
  - doc_savings_accounts_gold_account_013: "As a Gold Rewards Card holder, you receive an additional 0.025% relationship bonus APY on top of the base rate." and the example "Total APY with the bonus: 6.0%" (5.5 + 0.025 is 5.525)
  - `doc_savings_accounts_gold_account_014 table: "Gold Rewards Card | +0.025%"`
  - doc_bank_accounts_bank_accounts_(general)_045: "credit card APY bonuses DO stack with other types of bonuses, such as: ... Relationship bonuses for holding multiple Rho-Bank products"; its example lists "Gold Rewards Card: +0.025% APY bonus" among non-stacking card bonuses
  - `db credit_card_accounts: cc_wl94k7m3p8_gold "Gold Rewards Card" ACTIVE, cc_wl94k7m3p8_eco "EcoCard", cc_wl94k7m3p8_platinum`
  - `gold[6].arguments.amount = 140.00; gold[8].arguments.expected_apy = 6.85`
  - `computation: 96000 x (6.875 - 5.10)% / 12 = 142.00 vs gold 96000 x 1.75% / 12 = 140.00`
  - `replay: credit 142.0 -> verified match False (accounts, bank_account_transaction_history differ)`
  - *Why it matters:* Both readings are supported by required documents. An agent that applies doc_013 literally credits $142.00 and fails the DB check.
  - *Fix:* State in doc_013 that the 0.025% is the Gold Rewards Card credit-card APY bonus (subject to highest-only stacking), and fix its "Total APY ... 6.0%" example.

*Verifier: Confirmed (Major → Major).* All quotes and arithmetic reproduce. doc_045's worked example (the customer's exact card trio) favours gold, but doc_013 explicitly labels the 0.025% a relationship bonus on top of base and doc_045 says relationship bonuses stack, so two document-supported readings give different credits: Major per calibration.

### task_095 — Major

**As in task_094, the documents disagree on whether the Gold Rewards Card's 0.025% stacks, so the correct credit could be $98 or $100.**

- **document_contradiction (Major)** — Gold expects 6.85% (5.5 + 0.75 Green + 0.6 EcoCard), treating the Gold Rewards Card 0.025% as a credit-card bonus outranked by the EcoCard. doc_013, a required doc, describes it as a separate relationship bonus that stacks, which gives 6.875% and a $100.00 credit.
  - doc_savings_accounts_gold_account_013: "As a Gold Rewards Card holder, you receive an additional 0.025% relationship bonus APY on top of the base rate." and the example "Total APY with the bonus: 6.0%" (5.5 + 0.025 is 5.525)
  - `doc_savings_accounts_gold_account_014 table: "Gold Rewards Card | +0.025%"`
  - doc_bank_accounts_bank_accounts_(general)_045: "credit card APY bonuses DO stack with other types of bonuses, such as: ... Relationship bonuses for holding multiple Rho-Bank products"; its example lists "Gold Rewards Card: +0.025% APY bonus" among non-stacking card bonuses
  - `db credit_card_accounts: cc_lm83h7k2p5_gold "Gold Rewards Card", cc_lm83h7k2p5_eco "EcoCard", cc_lm83h7k2p5_platinum`
  - `gold[6].arguments.amount = 98.00; gold[8].arguments.expected_apy = 6.85, actual_apy 5.625`
  - `computation: 96000 x (6.875 - 5.625)% / 12 = 100.00 vs gold 96000 x 1.225% / 12 = 98.00`
  - `replay: credit 100.0 -> verified match False`
  - *Why it matters:* An agent that adds the doc_013 relationship bonus credits $100.00 and fails. The actual 5.625% also decomposes either as base+Purple+GR-card bonus or as base+Purple+relationship bonus, which does not settle the question.
  - *Fix:* Make doc_013 and doc_014 non-overlapping (declare the 0.025% a card bonus subject to highest-only stacking) and fix doc_013's "6.0%" example.

*Verifier: Confirmed (Major → Major).* Same doc_013 vs doc_014/045 ambiguity as task_094, reproduced; Major is consistent across the pair. Customer's Silver/Gold card mix-up self-corrects and does not matter.

### task_097 — Blocker

**For the Silver account, the official credit leaves out a 0.025% relationship bonus that this task's own document grants (and that task_093 applies), and the cent amount also depends on the rounding method.**

- **argument_error (Blocker)** — Gold Silver expected APY 6.65% = 4.0 tier + 0.45 Bluest + 2.2 EcoCard, with no relationship bonus. The required doc silver_002 and FAQ silver_005 grant +0.025% for holding multiple Rho-Bank products, and this customer holds 13. task_093 applies the same bonus with just two products. A doc-following agent computes 6.675% and credits $222.92 instead of $220.84.
  - doc_savings_accounts_silver_account_002 (required): "If you maintain multiple Rho-Bank products, you may also qualify for a relationship bonus of 0.025% that stacks on top of your base Silver APY."
  - doc_savings_accounts_silver_account_005: "Do I get a bonus for having multiple Rho-Bank products? - Yes. Eligible customers receive a relationship APY bonus of 0.025% added to the base Silver APY."
  - doc_bank_accounts_bank_accounts_(general)_044: "Missing Relationship Bonus: Customer maintains multiple Rho-Bank products but the relationship bonus was not applied."
  - `task_093 gold[8].expected_apy = 4.275 (includes the 0.025 with two products)`
  - `gold[9].arguments.amount = 220.84; gold[14].arguments.expected_apy = 6.65`
  - `computation: 100000 x 6.675% / 12 = 556.25; 556.25 - 333.33 = 222.92`
  - `replay: Silver credit 222.92 -> verified match False (accounts, bank_account_transaction_history differ)`
  - *Why it matters:* Leaving the bonus out requires ignoring a required document and contradicts task_093. A competent agent includes it and fails. doc_savings_accounts_silver_plus_account_002 ("an additional relationship APY bonus of 0.025% when you qualify under the relationship criteria") creates the same exposure for the Silver Plus credit (12.375 vs gold 12.00).
  - *Fix:* Add the 0.025% to the Silver (and, if intended, Silver Plus) expected APY and credit, or define relationship-bonus eligibility so that it excludes this customer, and keep task_093 consistent.
- **non_determinism (Major)** — Even without the bonus, the Silver gap rounds differently depending on method. Gold uses round(expected interest) minus actual (554.17 - 333.33 = 220.84); the equally natural balance x APY difference / 12 gives 220.83.
  - `db: btxn_silver_interest_oct amount 333.33, sav_mc80w7k3x9_silver current_holdings 100000.00`
  - `computation: 100000 x 6.65% / 12 = 554.1667 -> 554.17 - 333.33 = 220.84; 100000 x 2.65% / 12 = 220.8333 -> 220.83`
  - `gold[9].arguments.amount = 220.84`
  - `replay: Silver credit 220.83 -> verified match False`
  - *Why it matters:* The credit amount is persisted and hashed into the transaction id, so a one-cent difference fails the DB check. No document specifies the rounding method.
  - *Fix:* Pick balances whose gaps are exact to the cent (as in tasks 093-096), or state the rounding convention.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced every quote and number. No document gives a reason to withhold the multi-product bonus from a 13-product customer; the only text tying the 0.025% to something narrower is silver_009 (Platinum Rewards Card holders), which calls it 'the existing ... 0.025% relationship bonus' and this customer has no Platinum card anyway, so it does not create an exclusion reading. The benchmark's own task_093 gold and doc_044 example apply the rule gold omits here, so gold follows no doc-supported reading: Blocker stands, and the stated reason distinguishes it from the Major in 094/095 (where gold follows doc_045's explicit example). The rounding ambiguity (220.84 vs 220.83) is real and independently Major; it only exists under gold's no-bonus APY.

*Reconciled across runs: Blocker → Blocker (judgment).* Fact: the required doc silver_002 and FAQ silver_005 grant the 0.025% relationship bonus to customers with multiple Rho-Bank products, this customer holds 13, and doc_044 names 'Missing Relationship Bonus' as a discrepancy type. task_093's gold applies the bonus (expected_apy 4.275) to a two-product customer with no credit card. The only text that could exclude it, silver_009's Platinum-Rewards-Card section, calls it 'the existing ... 0.025% relationship bonus' (not Platinum-only), and reading it as Platinum-only would break task_093's gold. The gold's 6.65% therefore follows no reading consistent with the documents or the benchmark's own convention: Blocker under both scorers. The 220.84 vs 220.83 rounding issue is an additional Major.

### task_101 — Major

**Purple plus Sky Blue is the right pair once the 2-per-9-days referral cap is applied to the new batch; the policy wording that justifies the cap is slightly loose.**

- **non_determinism (Minor)** — doc_047 phrases the cap as "at most 2 referral bonuses" received in 9 days but also says a third referral attempted in the window is auto-denied. The gold (submit only 2 now) follows the second sentence. An agent reading the cap as limiting only past bonuses received (none in the last 9 days) could recommend all 4, and the simulator would then submit all 4.
  - doc_bank_accounts_bank_accounts_(general)_047: "You can receive at most 2 referral bonuses in any rolling 9-day window." and "If you attempt to receive more than 2 referrals in a single 9-day period, the third referral (and any subsequent referrals in that window) will be automatically denied."
  - `doc_047 practical guidance: "Track the timing of your last two successful referral bonuses before sending additional referrals."`
  - `user instruction 17: "If agent recommends all 4 referrals without mentioning rolling window: ... submit ALL 4"`
  - `db referrals: most recent are 10/25 (Gold Years) and 10/10 (Sky Blue), so none in the last 9 days`
  - `replay: four referrals (GFF, Purple, Lime Green, Sky Blue) -> verified match False (referrals differs)`
  - *Why it matters:* Submitting four referrals now would, per the auto-denial sentence, get the third and fourth denied, so capping at two is the better-supported reading and matches tasks 098/102. The loose wording still leaves a minority path to a different state.
  - *Fix:* Reword doc_047 to say plainly that the cap counts referrals submitted in the window.

*Verifier: Confirmed (Minor → Minor).* Reproduced: Purple ($80) + Sky Blue ($400) is the best one-personal/one-business pair after the annual caps and Sky Blue's 4-year formation limit; replay confirms order does not matter and four submissions fail (referrals table). A sub-check argued for Major because doc_048 says 'You can have multiple referrals in progress' and frames rejection by bonuses already received (none in the window). I keep Minor: doc_047 states the third referral attempted in a 9-day period is denied, so submitting four new referrals at once knowingly forfeits two bonuses and is not a competing reading a careful agent would adopt; the doc_048 wording is the loose-wording soft spot the review named.

*Reconciled across runs: Minor → Major (judgment).* doc_047 and doc_048 limit bonuses received in a rolling 9-day window, and doc_048 says outright that multiple referrals may be in progress. No bonus falls in the current window (last ones 10/25 and 10/10), and a bonus is received when the referred person qualifies, not on submission, so submitting all four now is a document-supported reading, and the script then submits all four. The gold (two now) follows the competing reading that new submissions count toward the window, so this is two supported readings with different graded referrals tables: Major under both scorers.

### task_102 — Blocker

**With only one referral slot, the customer asks to "maximize the bonus" without saying whose bonus; the official TechFlow-to-Sky Blue pick wins on combined bonus but loses to Ember-to-Lime Green on her own bonus.**

- **underspecified_instructions (Major)** — Unlike task_101, the customer never says "combined". The gold maximizes combined bonus (Sky Blue $150+$250=$400). If "the bonus" means her own referrer bonus, Ember to Lime Green ($200) beats Sky Blue ($150), and Hunter Green ($175) beats it too.
  - `user instruction 12: "Okay, so if I can only do one right now, which one should I prioritize? I want to maximize the bonus."`
  - `task_101 instruction 1 (same persona): "I want to make sure I'm getting the best possible combined bonus" (absent from task_102)`
  - doc_business_checking_accounts_sky_blue_001: "Your bonus: $150 ... Their bonus: $250"; lime_green_003: "Your bonus: $200 ... Their bonus: $150"; hunter_green_001: "Referrer reward: $175"
  - `author notes: "Must choose highest value: TechFlow -> Sky Blue ($400)"`
  - `gold[2] submit_referral account_type "Sky Blue Account"`
  - `replay: submit_referral "Lime Green Account" -> verified match False (referrals differs)`
  - *Why it matters:* A competent agent that reads "maximize the bonus" from the referrer's side recommends Lime Green for Ember. The customer submits it and the referrals table diverges. The NL assertion requiring TechFlow/Sky Blue fails as well.
  - *Fix:* Have the customer say "the best combined bonus" (as in task_101), or accept Lime Green when the referrer-bonus reading is used.

*Verifier: Confirmed (Major → Major).* Reproduced: the gold is the unique answer only under the combined-bonus reading, which the script never states; the referrer-only reading picks Lime Green and fails the DB check. The NL assertion is satisfiable by an agent that also names TechFlow as the Sky Blue candidate, so it does not rescue or worsen the DB failure. The 101 rolling-window ambiguity also touches this task but does not change the one-slot count (one bonus received on 11/10 under either reading).

*Reconciled across runs: Major → Blocker (coverage).* Fact: the NL assertion requires the agent to recognize that Ember Analytics exceeds Sky Blue's 4-year limit, but Ember's real age (5 years) appears only in author notes and in task_101's script. It is in no DB record, document or tool output, and this customer says Ember incorporated in late 2022 ('about 3 years'). On agent-visible facts Ember and TechFlow both qualify for Sky Blue at the same $400 combined bonus, and the script branch where the agent 'corrects' Ember to 5 years can only fire on hallucination. reward_basis multiplies the NL result into the score, so the information needed does not exist: Blocker under both scorers, since NL grading is unchanged. Run V judged the assertion satisfiable without weighing its 'recognizing' clause; the 'maximize the bonus' referrer-vs-combined ambiguity is an additional Major.

