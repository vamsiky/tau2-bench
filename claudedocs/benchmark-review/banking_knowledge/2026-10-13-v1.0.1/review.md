# `banking_knowledge` benchmark correctness review — v1.0.1

**Benchmark:** `v1.0.1` (`fc0055dc4e`) · **Run date:** 2026-10-13 · **Reviewer:** claude-opus-5-5: 8 parallel reviewers + 4 independent verifiers (Claude Code subagents) · **Effort:** high (set explicitly on every agent) · **Prior review:** 2026-06-25-v1.0.0

The interactive version (`review.html`) shows each task's customer instructions, required documents, gold trajectory, and findings side by side.

## Summary

| Severity | Now | Prior |
|---|---|---|
| Blocker | 11 | 10 |
| Major | 40 | 11 |
| Minor | 25 | 14 |
| None | 21 | 62 |

97 tasks reviewed against v1.0.1: 11 Blocker, 40 Major, 25 Minor, 21 clean (v1.0.0 review: 10 / 11 / 14 / 62). v1.0.1's fixes hold where checked: task_074's corrected $14.50 Light Blue refund reproduces, bank transactions now sort newest-first, and the rewards rounding rule turns out to be documented, which clears the old Majors on 018, 019, 021 and 022. Four v1.0.0 Blockers persist (063, 082, 083, 084); five drop to Major because the documents support the gold's reading (039, 040, 041, 075, 101). The rise in flagged tasks comes mostly from defects the v1.0.0 review did not report: 43 tasks it rated clean have a defect now, found by replaying gold and alternative actions. Under upstream scoring, four more tasks (060, 061, 062, 067) are Major only because the free-text closure reason is graded exactly. Severities are reviewer verdicts checked by independent verifiers and reconciled with the companion run.

## Systemic issues

1. **Gold depends on information the agent cannot observe** (task_026, task_027, task_028, task_029, task_049, task_053, task_102). No agent tool reads cash_back_disputes and the customer's own tool results never reach the agent, so 026–029 grade the same customer claim in opposite ways. task_053's gold uses card digits only the customer's omitted lookup returns, task_049 needs the customer to call a transfer tool unprompted, and task_102's NL assertion needs a company age that exists only in author notes.
2. **Gold values contradict the documents or each other** (task_026, task_069, task_082, task_083, task_084, task_091, task_097). task_069 assumes Gold savings has no ATM rebates (gold_account_003 documents $30/month); task_097 omits the 0.025% relationship bonus that task_093's gold applies; task_026 writes 1500 points where the documented round-down rule gives 1499; task_083's ACTION gold omits a required argument so no call can match; 082, 084 and 091 record dispute, liability, and replacement values that no single documented rule produces.
3. **Strings the gold stores verbatim differ from what the documents tell the agent to write** (task_056, task_059, task_065, task_066, task_068, task_071). doc_001's own example spells products 'Green Account (checking)' while the gold stores 'Green Account', and general_004 says to open business savings with account_type 'savings' while the gold uses 'business_savings'. Following the documents opens a different account id and fails the DB match.
4. **Ties and multiple defensible products with no tie-breaker** (task_063, task_024, task_025, task_048, task_075, task_076). task_063 is an exact tie (Bronze and Silver Rewards both add +0.15% at $0); in the others a second product is as good or better under one supported reading (Silver Zoom's promo in 024, Apple Music's category in 025, Platinum Rewards in 048, ATM-fee stacking in 075, Bluest's unstated deposit in 076).
5. **Customer choices the gold records but the script never states** (task_041, task_070, task_077, task_079, task_092). Refund types, a company's formation date, card design, freezing before closing, and how to unlock a card are fixed in the gold but never given to the simulated customer or settled by a documented default.
6. **Fee, rebate, and rounding rules applied inconsistently across sibling tasks** (task_017, task_020, task_072, task_073, task_074, task_094, task_095). Refunds in 072–074 count fees dated after the fixed clock; 072–074 assume out-of-network and foreign ATM fees do not stack while 075 assumes they do; seed rewards in 020/026/027 use round-half-up against the documented floor rule; 094/095 hinge on whether a 0.025% card bonus stacks.
7. **Dispute fields with no single documented rule** (task_039, task_040, task_085, task_086, task_088). Whether disputes filed earlier in the same call count toward the provisional-credit limit, how customer_max_liability_amount is derived, and how pin_compromised and transaction type are chosen all have two defensible readings; the gold picks one.
8. **Free-text closure reasons are graded exactly** (task_060, task_061, task_062, task_067). close_bank_account_7392 stores its optional free-text reason; the gold relies on a hidden default and any reason the agent writes fails the DB match. These four tasks are clean under the verified scorer, which strips closure_reason. (065, 066 and 068 share this defect but are Major for their naming issue anyway.)

## Changes since the prior review

| Task | Prior | Now | Status | Headline |
|---|---|---|---|---|
| task_005 | None | Minor | new | The gold is correct per the bypass-code document, but reaching it needs the simulated customer to come back after a transfer, which the simulator's general rules tell it to end the conversation on. |
| task_006 | None | Minor | new | Valid: EcoCard is the only card that meets all three requirements. The Crypto-Cash Back lure is excluded only by a minimum credit score that the docs write as a dollar amount ('$660'). |
| task_010 | None | Major | new | The diagnosis (a weekly referral cap that has now passed) is clear, but the gold expects the customer to resubmit with a tool the knowledge base never mentions. An agent that hands over the documented referral-link tool fails the DB check. |
| task_014 | None | Major | new | The gold requires a transfer to a human, but the knowledge base's own referral-link procedure says that when a card has no documented referral program the agent should explain and 'Do not transfer to a human'. |
| task_016 | Minor | Minor | changed | The referral answer ($750 Silver card spend) is uniquely determined, but the customer's story says the friend has already made purchases while the database has no record of the friend at all. |
| task_018 | Major | Minor | changed | Applying the KB's documented round-down rule gives exactly the six gold disputes; the only flaw is that the rounding document is missing from the task's required-document list. |
| task_019 | Major | Minor | changed | Applying the KB's documented round-down rule gives exactly the four gold disputes; the rounding document is just missing from the required-document list. |
| task_020 | Minor | Major | changed | The seeded rewards were computed with ordinary rounding, but the knowledge base says rewards are always rounded down, so an agent that follows the KB finds nine extra one-point over-credits that the gold does not dispute. |
| task_021 | Major | Minor | changed | Applying the KB's documented round-down rule and the card exclusions gives exactly the two gold disputes; the rounding document is just missing from the required-document list. |
| task_022 | Major | Minor | changed | Across 77 transactions on four cards, the KB's documented round-down rule plus the card exclusions yields exactly the ten gold disputes; the rounding document is just missing from the required-document list. |
| task_024 | None | Major | new | The gold assumes the Business Bronze card ($400 cash back + $500 promo) is the best card for a $40,000 truck, but the Silver Zoom card's triple-cash-back promo pays about $1,200; it wins unless the agent decides a landscaping company cannot get a card the KB describes as built for logistics businesses. |
| task_026 | Minor | Blocker | changed | The agent is expected to trust the customer's claim that the disputes were approved and then write corrected reward values, but it has no way to check dispute status, the same conversation in task_027 expects the opposite, and one gold value (1500) contradicts the KB's round-down rule (1499). |
| task_027 | Minor | Major | changed | The agent is expected to see through the customer's false claim that the disputes were approved, but it has no tool to check dispute status, and task_026 presents the identical conversation with the opposite expected outcome. |
| task_028 | None | Major | new | The rewards math is fully documented and reproduces the gold exactly, but the agent has no way to confirm the disputes were approved, so it must update rewards on the customer's word alone. Task_029 shows the same evidence and expects a refusal. |
| task_029 | Major | Major | changed | To pass, the agent must refuse to update rewards because the disputes are still pending, but it has no tool to see dispute status and hears the same 'they were approved' claim that task_028 expects it to act on. |
| task_032 | None | Minor | new | The speed-bump protocol (three 'lines are busy' calls, then a real transfer on the fourth request) is documented clearly, but the ACTION grader only checks that each tool was called at least once, so the count it is meant to test goes unchecked. |
| task_033 | None | Minor | new | The 11/13 incident protocol (tool 1822, then tool 0218, then a real transfer) clearly applies and the gold matches it, but ACTION grading ignores order and count, so the sequence itself is never checked. |
| task_034 | None | Minor | new | The rule 'transfer only after exactly 8 requests' is documented, but the grader only checks that the user's request tool was used once and the agent transferred at some point, so a premature transfer passes. |
| task_035 | None | Minor | not_applicable | Clean: the 11/14 credit-bureau incident article clearly applies and names the emergency tool plus a transfer, which is exactly what the gold checks. |
| task_037 | None | Minor | not_applicable | Clean: a fraud replacement plus two fraud disputes; card digits, dates, reasons, and provisional-credit eligibility (both eligible) all follow from the docs and data. |
| task_038 | None | Minor | new | The three disputes and their provisional-credit flags follow cleanly from the docs, but the gold's expedited shipping relies on the simulated customer accepting an offer the script never mentions. |
| task_039 | Blocker | Major | persists | The gold grants provisional credit to only 3 of 4 qualifying disputes because it counts disputes filed earlier in the same conversation toward the 'no more than 2 in 12 months' rule; that reading is defensible but not the only one, and it also depends on filing order. |
| task_040 | Blocker | Major | persists | Same provisional-credit cap problem as task_039 (one earlier dispute plus in-session counting leaves only two eligible), and the gold asks for a full refund on a Comcast charge where the customer was promised only a partial one. |
| task_041 | Blocker | Major | changed | Sixteen card disputes whose gold record stores a $69.99 partial refund and refund types the customer is never told to ask for, plus a provisional-credit cap the documents only imply. |
| task_043 | None | None | new | Card-closure retention with a balance payoff and an annual-fee waiver; the only defect is a cosmetic credit-score typo in the card doc. |
| task_044 | None | None | new | Closure retention where the agent must recommend the Platinum Rewards Card, the only Rho-Bank card that beats the competitor; only a cosmetic credit-score typo remains. |
| task_045 | None | None | new | Closure retention with a balance payoff, a Business Platinum recommendation the customer declines, and a $20 retention credit; sound apart from cosmetic doc issues. |
| task_046 | None | Major | new | Closure is blocked by a pending dispute, but the gold quietly forbids paying off the card's $125 balance, which the customer will ask for if the agent mentions it. |
| task_047 | None | None | new | Two-card retention (a Business Platinum upgrade, then a $50 credit after the customer declines a downgrade); the logic is sound and only cosmetic doc typos remain. |
| task_048 | None | Major | new | Four-card closure where the gold requires the customer to apply for the Silver Rewards Card, though the knowledge base offers other cards that beat the competitor, including one with higher rewards. |
| task_049 | None | Blocker | new | Lying-customer closure flow whose gold needs the simulated customer to call a transfer-request tool, which nothing tells it to call. |
| task_050 | None | Minor | not_applicable | Simple credit limit increase on a premium-tier card, exactly at the 50% maximum; clean. |
| task_051 | None | Minor | not_applicable | Entry-tier CLI: cap the request at 25%, deny for 75% utilization, pay the balance, then approve; deterministic. |
| task_052 | None | Minor | not_applicable | Adversarial CLI request inside the 120-day entry-tier cooldown; the correct outcome is one documented denial; clean. |
| task_053 | None | Blocker | new | CLI plus dispute task whose gold leaves out the customer's card-number lookup, yet the dispute needs that lookup's result, so a fully correct run can never match. |
| task_054 | None | Minor | new | The fraud-plus-credit-limit task is solvable from the documents, but the gold expects expedited shipping on the replacement card, and the customer's script never says whether she wants it. |
| task_056 | None | Major | new | The product choices (Cobalt Blue checking, Silver Plus Saver savings) are unique, but the bank's own procedure tells the agent to open business savings with account_type 'savings', while the gold uses 'business_savings', which produces a different account. |
| task_057 | Minor | None | resolved | Blue Account is the only checking account that meets all of the customer's documented needs, the savings refusal leaves no DB trace, and the check deposit is scripted, so the task is clean. |
| task_059 | None | Major | new | Silver Rewards Card plus Green savings is the unique best combination for $5,000, but the gold's account name 'Green Account' is one of two plausible spellings the documents support, and the other one fails. |
| task_060 | None | Major | new | Silver Plus is the unique savings fit and the open-savings-before-closing order is documented, but the gold closure leaves the free-text closure reason at a hidden default, so an agent that records a reason fails. |
| task_061 | None | Major | new | The ordering and the $25 early-closure fee are documented and scripted, but the gold closure leaves the free-text closure reason at a hidden default, so an agent that records a reason fails. |
| task_062 | None | Major | new | The four-step reordering puzzle is fully documented and the products are unique, but both gold closures leave the free-text closure reason at a hidden default, so an agent that records a reason fails. |
| task_065 | None | Major | new | Evergreen checking plus Green savings is the unique highest-APY pairing and the ordering is documented, but two free-text values in the gold (the 'Green Account' spelling and the default closure reason) are not uniquely derivable. |
| task_066 | None | Major | new | The right accounts are derivable, but the grade also depends on two free-text strings the documents do not fix: the closing reason, and how the Green savings account is named. |
| task_067 | None | Major | new | The best account-and-card combination is clearly derivable, but the grade also depends on leaving the optional closing-reason text empty. |
| task_068 | None | Major | new | The right products are derivable, but the knowledge base's own example spells the checking account's name differently from the gold, and the grade checks that name exactly. |
| task_069 | None | Blocker | new | The gold picks a 3.0% savings account on the claim that higher-rate accounts lack ATM-fee rebates, but the documents say the 5.5% Gold Account has them, so the correct answer differs from the gold. |
| task_070 | None | Major | new | Picking Sky Blue through the active November promotion is derivable, but Sky Blue is a startup account and the customer's company age is never given. |
| task_071 | None | Major | new | Both promotion-driven picks (Sky Blue checking, Gold Saver savings) are derivable, but the customer script never answers two things the documents tell the agent to ask: company age and whether to fund the new savings account now. |
| task_072 | Minor | Major | changed | Both refund amounts can be rebuilt exactly from the documents, but they rely on fee rows dated after 'today' and on assuming the bank's own ATM fee gets rebated. |
| task_073 | Major | Major | changed | All three refunds follow from the fee schedules and the documented 'net correction' rule. The one blemish is that some errors sit on fee rows dated after 'today'. |
| task_074 | Blocker | Major | changed | Three of the four v1.0.1 refunds (including the corrected Light Blue $14.50) rebuild exactly. The Purple $27.00 counts a 'missing rebate' on the bank's own fee that the Purple docs say is not rebatable, plus a fee dated after 'today'. |
| task_075 | Blocker | Major | persists | The customer wants the account with the lowest foreign-ATM fees, but by the documents Purple and Bluest also charge $0 abroad (Purple adds operator-fee rebates), so Green Fee-Free is not the unique answer. |
| task_076 | None | Major | new | Purple is a sound pick, but Bluest also gives 2-day early deposit and $0 fees abroad with a larger rebate. It is ruled out only by a $75,000 opening deposit the customer is never asked about. |
| task_077 | None | Major | new | The lost-wallet sequence is fully documented, but the gold's choice of the PREMIUM card design depends on reading a vague 'best free option' as metallic rather than classic. |
| task_078 | None | Minor | not_applicable | Lost-wallet task with three debit cards is solvable from the documents; the gold freezes, unfreezes, closes and reorders exactly as the customer and policy require. |
| task_079 | None | Major | new | The gold requires freezing three stolen cards and then unfreezing them before closing, but the policy says to recommend closing instead of freezing once a theft is confirmed, and skipping the freeze changes the graded state. |
| task_080 | None | Minor | new | The provisional-credit rule for the third credit-card fraud dispute is ambiguous, and the gold contradicts the task author's own stated intent, so whether a careful agent passes depends on how it counts disputes. |
| task_081 | None | Minor | new | This is the task_080 lost-wallet scenario plus repeated human-transfer requests, and it inherits the same ambiguous provisional-credit rule on the third fraud dispute that the gold resolves against its own author notes. |
| task_084 | Blocker | Blocker | changed | The duplicate-charge pick is now resolvable, but the gold caps one dispute's maximum liability at the disputed amount and not another's, so no single consistent rule reproduces the official answer. |
| task_085 | Minor | Major | changed | Verifying the customer's claims against the transaction history works, but the gold's liability amounts and provisional-credit flag for the duplicate charge rest on readings the documents do not settle. |
| task_086 | Minor | Major | changed | The six-dispute task is mostly derivable, but the gold's PIN-compromise and purchase-type values for the skimmed-card fraud contradict the customer's own words, and its liability values rest on an undocumented convention. |
| task_087 | None | Major | new | The three-card CODE 05 diagnosis is derivable and the gold matches it; one security-alert document also tells agents to escalate when a customer reports a charge they did not make, which could lead a careful agent to transfer instead of filing the dispute. |
| task_088 | Minor | Major | changed | For the cloned-card fraud, the decline-code guide says to freeze the card while the gold only closes it, and the customer is never told whether the Miami charge used a PIN, so two stored dispute fields are guesswork. |
| task_090 | None | Minor | new | The fraud, PIN-reset and security-hold outcomes are all reachable from the protocol, but the customer never says which card design she wants and two designs are free for her tier. |
| task_091 | None | Blocker | new | Two gold replacement-card orders contradict the bank's own card-replacement rules, and the fourth card's outcome is a judgment call, so a policy-following agent fails. |
| task_092 | Minor | Major | changed | The Blue-card fraud closure and the security-hold transfer are well-defined, but the Green card's outcome and the Evergreen 'unlock' each rely on readings that a careful agent could reasonably make differently. |
| task_093 | None | Minor | not_applicable | Clean: the missing Green-checking boost and the multi-product relationship bonus are both documented, and the $33.00 correction follows directly. |
| task_094 | Minor | Major | persists | The KB describes the Gold Rewards Card's 0.025% both as a credit-card bonus that does not stack and as a separate relationship bonus that does, so $140 and $142 are both defensible corrections. |
| task_097 | Major | Blocker | persists | The gold leaves out the documented 0.025% multi-product relationship bonus on the Silver account, the same bonus task_093's gold requires, so a doc-following agent's Silver credit and report fail. |
| task_099 | None | Minor | not_applicable | Clean: for a $30,000 business deposit, World Blue's $300 referrer bonus is the unique maximum the customer qualifies for. |
| task_100 | Minor | None | resolved | Clean: the on-file open date gives 65 days of tenure, which rules out World Blue, so Hunter Green's $175 is the best referrer bonus available. |
| task_101 | Blocker | Major | changed | Purple plus Sky Blue is the right pair if only two referrals can go now, but the docs can also be read as allowing all four. |
| task_102 | Major | Blocker | changed | The grading requires the agent to 'recognize' that Ember is over Sky Blue's 4-year limit, but nothing the agent can see says so. 'Maximize the bonus' also points to Lime Green ($200 to the customer) rather than the gold's Sky Blue ($150). |

## All tasks

| Task | Final | Reviewer | Verifier | Reconciled | Prior | Instr. | Docs det. | Cx | Ordering | Gold ok | Headline |
|---|---|---|---|---|---|---|---|---|---|---|---|
| task_001 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 2 | None | Yes | Clean: the only no-annual-fee card with the top flat cash-back rate is the Gold Rewards Card, and the gold application matches it. |
| task_002 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 3 | None | Yes | Clean: the Platinum Rewards Card has the highest cash back, and its fee after the monthly-spend rebate ($50) fits the customer's $100 budget. |
| task_003 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 3 | None | Yes | Clean: Silver and Gold both meet the hard requirements at a $0 fee, and the cash-back tie-break picks Silver because her spending is mostly travel (4% vs 2.5%). |
| task_004 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 2 | None | Yes | Clean: the customer can match only one of the four identity fields, so the agent cannot verify him and transfers with the code for identity verification failures. |
| task_005 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 2 | Soft | Yes | The gold is correct per the bypass-code document, but reaching it needs the simulated customer to come back after a transfer, which the simulator's general rules tell it to end the conversation on. |
| task_006 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 3 | None | Yes | Valid: EcoCard is the only card that meets all three requirements. The Crypto-Cash Back lure is excluded only by a minimum credit score that the docs write as a dollar amount ('$660'). |
| task_007 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 3 | None | Yes | Clean: on the fixed date only EcoCard has an active points or cash sign-up bonus that a non-invited personal applicant can get, so the gold EcoCard application is right. |
| task_008 | Minor | Minor | Not sampled (-) | - | Minor | Sufficient | Yes | 2 | None | Yes | Mostly clean: two transfer codes fit a persistent customer waving flyers, but the knowledge base's 'highest tier wins' rule picks the gold code. |
| task_010 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 3 | Soft | Yes | The diagnosis (a weekly referral cap that has now passed) is clear, but the gold expects the customer to resubmit with a tool the knowledge base never mentions. An agent that hands over the documented referral-link tool fails the DB check. |
| task_012 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 2 | None | Yes | Clean: the knowledge base has no travel-notification procedure, so the right move is to say so and transfer with the 'search unsuccessful' code when the customer asks. |
| task_014 | Major | Blocker | Adjusted (Major) | - | None | Sufficient | No | 3 | None | No | The gold requires a transfer to a human, but the knowledge base's own referral-link procedure says that when a card has no documented referral program the agent should explain and 'Do not transfer to a human'. |
| task_015 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 3 | Soft | Yes | Clean: of the five referral offers the customer cites, only the Platinum Rewards Card offer matches a live documented program, and the gold gives and uses the referral-link tool for it. |
| task_016 | Minor | Minor | Not sampled (-) | yes | Minor | Sufficient | Yes | 2 | None | Yes | The referral answer ($750 Silver card spend) is uniquely determined, but the customer's story says the friend has already made purchases while the database has no record of the friend at all. |
| task_017 | Major | Major | Confirmed (Major) | - | Major | Sufficient | Partial | 3 | None | Yes | The gold disputes two clearly wrong rewards, but a third transaction is over-credited by one point under every rounding rule, and nothing tells the agent whether to dispute it. |
| task_018 | Minor | Minor | Confirmed (Minor) | - | Major | Sufficient | Yes | 4 | None | Yes | Applying the KB's documented round-down rule gives exactly the six gold disputes; the only flaw is that the rounding document is missing from the task's required-document list. |
| task_019 | Minor | Minor | Confirmed (Minor) | - | Major | Sufficient | Yes | 3 | None | Yes | Applying the KB's documented round-down rule gives exactly the four gold disputes; the rounding document is just missing from the required-document list. |
| task_020 | Major | Major | Confirmed (Major) | - | Minor | Sufficient | Partial | 4 | None | No | The seeded rewards were computed with ordinary rounding, but the knowledge base says rewards are always rounded down, so an agent that follows the KB finds nine extra one-point over-credits that the gold does not dispute. |
| task_021 | Minor | Minor | Confirmed (Minor) | - | Major | Sufficient | Yes | 4 | None | Yes | Applying the KB's documented round-down rule and the card exclusions gives exactly the two gold disputes; the rounding document is just missing from the required-document list. |
| task_022 | Minor | Minor | Confirmed (Minor) | - | Major | Sufficient | Yes | 5 | None | Yes | Across 77 transactions on four cards, the KB's documented round-down rule plus the card exclusions yields exactly the ten gold disputes; the rounding document is just missing from the required-document list. |
| task_023 | Minor | Minor | Not sampled (-) | - | Minor | Sufficient | Yes | 4 | None | Yes | The rebate check is fully determined by the database (every anniversary-month window clears $7,500), but the customer gives the wrong account-opening year, and believing it would point to a fee-waiver exception and the wrong card application. |
| task_024 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 4 | None | Yes | The gold assumes the Business Bronze card ($400 cash back + $500 promo) is the best card for a $40,000 truck, but the Silver Zoom card's triple-cash-back promo pays about $1,200; it wins unless the agent decides a landscaping company cannot get a card the KB describes as built for logistics businesses. |
| task_025 | Major | Major | Confirmed (Major) | - | Major | Sufficient | Partial | 5 | None | Yes | Whether the Business Platinum card is best for a $100,000 Apple Music purchase depends on treating Apple Music as a 4% 'software/media' purchase on that card. If it is ordinary spend, a different card pays more. |
| task_026 | Blocker | Blocker | Confirmed (Blocker) | yes | Minor | Insufficient | No | 4 | Soft | No | The agent is expected to trust the customer's claim that the disputes were approved and then write corrected reward values, but it has no way to check dispute status, the same conversation in task_027 expects the opposite, and one gold value (1500) contradicts the KB's round-down rule (1499). |
| task_027 | Major | Blocker | Confirmed (Blocker) | yes | Minor | Insufficient | No | 4 | Soft | Yes | The agent is expected to see through the customer's false claim that the disputes were approved, but it has no tool to check dispute status, and task_026 presents the identical conversation with the opposite expected outcome. |
| task_028 | Major | Major | Upgraded (Blocker) | yes | None | Sufficient | Partial | 4 | Strict | Yes | The rewards math is fully documented and reproduces the gold exactly, but the agent has no way to confirm the disputes were approved, so it must update rewards on the customer's word alone. Task_029 shows the same evidence and expects a refusal. |
| task_029 | Major | Major | Confirmed (Major) | yes | Major | Partial | Partial | 4 | Soft | Yes | To pass, the agent must refuse to update rewards because the disputes are still pending, but it has no tool to see dispute status and hears the same 'they were approved' claim that task_028 expects it to act on. |
| task_031 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 2 | Soft | Yes | Clean: one Marriott charge to dispute as 'not as described'. Every field can be derived from the customer, the database, or the docs, and the provisional-credit decision is clearly 'not eligible'. |
| task_032 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 2 | Strict | Yes | The speed-bump protocol (three 'lines are busy' calls, then a real transfer on the fourth request) is documented clearly, but the ACTION grader only checks that each tool was called at least once, so the count it is meant to test goes unchecked. |
| task_033 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 2 | Strict | Yes | The 11/13 incident protocol (tool 1822, then tool 0218, then a real transfer) clearly applies and the gold matches it, but ACTION grading ignores order and count, so the sequence itself is never checked. |
| task_034 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 2 | Strict | Yes | The rule 'transfer only after exactly 8 requests' is documented, but the grader only checks that the user's request tool was used once and the agent transferred at some point, so a premature transfer passes. |
| task_035 | Minor | None | Not sampled (-) | yes | None | Sufficient | Yes | 1 | Soft | Yes | Clean: the 11/14 credit-bureau incident article clearly applies and names the emergency tool plus a transfer, which is exactly what the gold checks. |
| task_036 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 2 | Soft | Yes | Clean: verify, show the transactions, then order an expedited fraud replacement to the customer's work address. Every argument comes from the customer or the database. |
| task_037 | Minor | None | Upgraded (Minor) | yes | None | Sufficient | Yes | 3 | Soft | Yes | Clean: a fraud replacement plus two fraud disputes; card digits, dates, reasons, and provisional-credit eligibility (both eligible) all follow from the docs and data. |
| task_038 | Minor | Minor | Confirmed (Minor) | - | None | Partial | Yes | 3 | Soft | Yes | The three disputes and their provisional-credit flags follow cleanly from the docs, but the gold's expedited shipping relies on the simulated customer accepting an offer the script never mentions. |
| task_039 | Major | Major | Confirmed (Major) | - | Blocker | Partial | Partial | 5 | Strict | Yes | The gold grants provisional credit to only 3 of 4 qualifying disputes because it counts disputes filed earlier in the same conversation toward the 'no more than 2 in 12 months' rule; that reading is defensible but not the only one, and it also depends on filing order. |
| task_040 | Major | Major | Confirmed (Major) | - | Blocker | Partial | Partial | 5 | Strict | Yes | Same provisional-credit cap problem as task_039 (one earlier dispute plus in-session counting leaves only two eligible), and the gold asks for a full refund on a Comcast charge where the customer was promised only a partial one. |
| task_041 | Major | Blocker | Confirmed (Blocker) | yes | Blocker | Insufficient | Partial | 5 | Soft | No | Sixteen card disputes whose gold record stores a $69.99 partial refund and refund types the customer is never told to ask for, plus a provisional-credit cap the documents only imply. |
| task_043 | None | Minor | Adjusted (None) | - | None | Sufficient | Yes | 3 | Soft | Yes | Card-closure retention with a balance payoff and an annual-fee waiver; the only defect is a cosmetic credit-score typo in the card doc. |
| task_044 | None | Minor | Adjusted (None) | - | None | Sufficient | Yes | 3 | Soft | Yes | Closure retention where the agent must recommend the Platinum Rewards Card, the only Rho-Bank card that beats the competitor; only a cosmetic credit-score typo remains. |
| task_045 | None | Minor | Adjusted (None) | - | None | Sufficient | Yes | 4 | Strict | Yes | Closure retention with a balance payoff, a Business Platinum recommendation the customer declines, and a $20 retention credit; sound apart from cosmetic doc issues. |
| task_046 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 3 | Strict | Yes | Closure is blocked by a pending dispute, but the gold quietly forbids paying off the card's $125 balance, which the customer will ask for if the agent mentions it. |
| task_047 | None | Minor | Adjusted (None) | - | None | Sufficient | Yes | 4 | Soft | Yes | Two-card retention (a Business Platinum upgrade, then a $50 credit after the customer declines a downgrade); the logic is sound and only cosmetic doc typos remain. |
| task_048 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 4 | Strict | Yes | Four-card closure where the gold requires the customer to apply for the Silver Rewards Card, though the knowledge base offers other cards that beat the competitor, including one with higher rewards. |
| task_049 | Blocker | Blocker | Confirmed (Blocker) | - | None | Insufficient | Yes | 5 | Strict | No | Lying-customer closure flow whose gold needs the simulated customer to call a transfer-request tool, which nothing tells it to call. |
| task_050 | Minor | None | Upgraded (Minor) | - | None | Sufficient | Yes | 3 | Strict | Yes | Simple credit limit increase on a premium-tier card, exactly at the 50% maximum; clean. |
| task_051 | Minor | None | Confirmed (None) | yes | None | Sufficient | Yes | 4 | Strict | Yes | Entry-tier CLI: cap the request at 25%, deny for 75% utilization, pay the balance, then approve; deterministic. |
| task_052 | Minor | None | Not sampled (-) | yes | None | Sufficient | Yes | 3 | Strict | Yes | Adversarial CLI request inside the 120-day entry-tier cooldown; the correct outcome is one documented denial; clean. |
| task_053 | Blocker | Blocker | Confirmed (Blocker) | - | None | Sufficient | Yes | 4 | Strict | No | CLI plus dispute task whose gold leaves out the customer's card-number lookup, yet the dispute needs that lookup's result, so a fully correct run can never match. |
| task_054 | Minor | Minor | Confirmed (Minor) | - | None | Partial | Yes | 4 | Strict | Yes | The fraud-plus-credit-limit task is solvable from the documents, but the gold expects expedited shipping on the replacement card, and the customer's script never says whether she wants it. |
| task_055 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 4 | Soft | Yes | The customer's requirements single out the Purple checking and Silver Plus savings accounts, and the check-deposit step is fully scripted, so the task is clean. |
| task_056 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 4 | Soft | Yes | The product choices (Cobalt Blue checking, Silver Plus Saver savings) are unique, but the bank's own procedure tells the agent to open business savings with account_type 'savings', while the gold uses 'business_savings', which produces a different account. |
| task_057 | None | None | Confirmed (None) | - | Minor | Sufficient | Yes | 3 | Soft | Yes | Blue Account is the only checking account that meets all of the customer's documented needs, the savings refusal leaves no DB trace, and the check deposit is scripted, so the task is clean. |
| task_058 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 4 | None | Yes | The net-return math (interest minus card fees on $20,000) uniquely favors EcoCard plus Silver Account under the documented rates, so the task is clean. |
| task_059 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 4 | None | Yes | Silver Rewards Card plus Green savings is the unique best combination for $5,000, but the gold's account name 'Green Account' is one of two plausible spellings the documents support, and the other one fails. |
| task_060 | Major | Major | Confirmed (Major) | yes | None | Sufficient | Partial | 4 | Strict | Yes | Silver Plus is the unique savings fit and the open-savings-before-closing order is documented, but the gold closure leaves the free-text closure reason at a hidden default, so an agent that records a reason fails. |
| task_061 | Major | Major | Confirmed (Major) | yes | None | Sufficient | Partial | 4 | Strict | Yes | The ordering and the $25 early-closure fee are documented and scripted, but the gold closure leaves the free-text closure reason at a hidden default, so an agent that records a reason fails. |
| task_062 | Major | Major | Confirmed (Major) | yes | None | Sufficient | Partial | 5 | Strict | Yes | The four-step reordering puzzle is fully documented and the products are unique, but both gold closures leave the free-text closure reason at a hidden default, so an agent that records a reason fails. |
| task_063 | Blocker | Blocker | Confirmed (Blocker) | - | Blocker | Partial | No | 4 | None | No | Two credit cards raise the savings rate by exactly the same amount and both meet the customer's conditions, yet only one is accepted. The customer also asks for an $8,000 deposit that the gold never makes. |
| task_064 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 4 | None | Yes | With Rho-Bank+, frequent withdrawals, no crypto and fees under $100, Gold Rewards Card plus Gold Plus savings is the unique best net return on $30,000, so the task is clean. |
| task_065 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 5 | Strict | Yes | Evergreen checking plus Green savings is the unique highest-APY pairing and the ordering is documented, but two free-text values in the gold (the 'Green Account' spelling and the default closure reason) are not uniquely derivable. |
| task_066 | Major | Major | Adjusted (Major) | yes | None | Sufficient | Partial | 4 | Strict | Yes | The right accounts are derivable, but the grade also depends on two free-text strings the documents do not fix: the closing reason, and how the Green savings account is named. |
| task_067 | Major | Major | Confirmed (Major) | yes | None | Sufficient | Partial | 5 | Strict | Yes | The best account-and-card combination is clearly derivable, but the grade also depends on leaving the optional closing-reason text empty. |
| task_068 | Major | Blocker | Adjusted (Major) | - | None | Sufficient | Partial | 4 | Strict | Yes | The right products are derivable, but the knowledge base's own example spells the checking account's name differently from the gold, and the grade checks that name exactly. |
| task_069 | Blocker | Blocker | Confirmed (Blocker) | - | None | Sufficient | Yes | 4 | Strict | No | The gold picks a 3.0% savings account on the claim that higher-rate accounts lack ATM-fee rebates, but the documents say the 5.5% Gold Account has them, so the correct answer differs from the gold. |
| task_070 | Major | Major | Confirmed (Major) | yes | None | Partial | Yes | 3 | None | Yes | Picking Sky Blue through the active November promotion is derivable, but Sky Blue is a startup account and the customer's company age is never given. |
| task_071 | Major | Major | Upgraded (Major) | - | None | Partial | Yes | 4 | None | Yes | Both promotion-driven picks (Sky Blue checking, Gold Saver savings) are derivable, but the customer script never answers two things the documents tell the agent to ask: company age and whether to fund the new savings account now. |
| task_072 | Major | Minor | Not sampled (-) | yes | Minor | Sufficient | Partial | 5 | None | Yes | Both refund amounts can be rebuilt exactly from the documents, but they rely on fee rows dated after 'today' and on assuming the bank's own ATM fee gets rebated. |
| task_073 | Major | Minor | Upgraded (Major) | - | Major | Sufficient | Partial | 5 | None | Yes | All three refunds follow from the fee schedules and the documented 'net correction' rule. The one blemish is that some errors sit on fee rows dated after 'today'. |
| task_074 | Major | Major | Adjusted (Major) | - | Blocker | Sufficient | Partial | 5 | None | Yes | Three of the four v1.0.1 refunds (including the corrected Light Blue $14.50) rebuild exactly. The Purple $27.00 counts a 'missing rebate' on the bank's own fee that the Purple docs say is not rebatable, plus a fee dated after 'today'. |
| task_075 | Major | Blocker | Confirmed (Blocker) | yes | Blocker | Partial | No | 3 | None | No | The customer wants the account with the lowest foreign-ATM fees, but by the documents Purple and Bluest also charge $0 abroad (Purple adds operator-fee rebates), so Green Fee-Free is not the unique answer. |
| task_076 | Major | Major | Confirmed (Major) | - | None | Partial | Partial | 3 | None | Yes | Purple is a sound pick, but Bluest also gives 2-day early deposit and $0 fees abroad with a larger rebate. It is ruled out only by a $75,000 opening deposit the customer is never asked about. |
| task_077 | Major | Major | Confirmed (Major) | - | None | Partial | Partial | 4 | Strict | Yes | The lost-wallet sequence is fully documented, but the gold's choice of the PREMIUM card design depends on reading a vague 'best free option' as metallic rather than classic. |
| task_078 | Minor | None | Not sampled (-) | yes | None | Sufficient | Yes | 4 | Strict | Yes | Lost-wallet task with three debit cards is solvable from the documents; the gold freezes, unfreezes, closes and reorders exactly as the customer and policy require. |
| task_079 | Major | Major | Confirmed (Major) | yes | None | Sufficient | Partial | 5 | Strict | Yes | The gold requires freezing three stolen cards and then unfreezing them before closing, but the policy says to recommend closing instead of freezing once a theft is confirmed, and skipping the freeze changes the graded state. |
| task_080 | Minor | Major | Adjusted (Minor) | yes | None | Sufficient | Partial | 5 | Strict | Yes | The provisional-credit rule for the third credit-card fraud dispute is ambiguous, and the gold contradicts the task author's own stated intent, so whether a careful agent passes depends on how it counts disputes. |
| task_081 | Minor | Major | Adjusted (Minor) | yes | None | Sufficient | Partial | 5 | Strict | Yes | This is the task_080 lost-wallet scenario plus repeated human-transfer requests, and it inherits the same ambiguous provisional-credit rule on the third fraud dispute that the gold resolves against its own author notes. |
| task_082 | Blocker | Blocker | Confirmed (Blocker) | - | Blocker | Partial | Partial | 5 | Strict | No | The gold records a close-and-reissue for the online fraud on the Green Fee-Free card, and the customer asks for a reissue, but the gold never closes that card, so an agent that follows the policy fails. |
| task_083 | Blocker | Blocker | Confirmed (Blocker) | - | Blocker | Sufficient | Partial | 4 | Soft | No | This task is graded by exact text match on the dispute-call arguments, but the official answer leaves out a field the tool requires and spells numbers as no tool call would, so no agent can match it. |
| task_084 | Blocker | Blocker | Confirmed (Blocker) | - | Blocker | Sufficient | Partial | 4 | Strict | No | The duplicate-charge pick is now resolvable, but the gold caps one dispute's maximum liability at the disputed amount and not another's, so no single consistent rule reproduces the official answer. |
| task_085 | Major | Major | Confirmed (Major) | - | Minor | Sufficient | Partial | 4 | Soft | Yes | Verifying the customer's claims against the transaction history works, but the gold's liability amounts and provisional-credit flag for the duplicate charge rest on readings the documents do not settle. |
| task_086 | Major | Major | Confirmed (Major) | - | Minor | Partial | Partial | 5 | Soft | Yes | The six-dispute task is mostly derivable, but the gold's PIN-compromise and purchase-type values for the skimmed-card fraud contradict the customer's own words, and its liability values rest on an undocumented convention. |
| task_087 | Major | Minor | Confirmed (Minor) | yes | None | Sufficient | Partial | 4 | Soft | Yes | The three-card CODE 05 diagnosis is derivable and the gold matches it; one security-alert document also tells agents to escalate when a customer reports a charge they did not make, which could lead a careful agent to transfer instead of filing the dispute. |
| task_088 | Major | Major | Confirmed (Major) | - | Minor | Partial | Partial | 4 | Soft | Yes | For the cloned-card fraud, the decline-code guide says to freeze the card while the gold only closes it, and the customer is never told whether the Miami charge used a PIN, so two stored dispute fields are guesswork. |
| task_089 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 4 | Soft | Yes | The three-card ATM-limit task is deterministic: the only write is a temporary limit increase whose value is fixed by both the customer's need and the 150% cap. |
| task_090 | Minor | Minor | Confirmed (Minor) | - | None | Partial | Partial | 5 | Soft | Yes | The fraud, PIN-reset and security-hold outcomes are all reachable from the protocol, but the customer never says which card design she wants and two designs are free for her tier. |
| task_091 | Blocker | Blocker | Confirmed (Blocker) | - | None | Partial | No | 5 | Strict | No | Two gold replacement-card orders contradict the bank's own card-replacement rules, and the fourth card's outcome is a judgment call, so a policy-following agent fails. |
| task_092 | Major | Major | Confirmed (Major) | yes | Minor | Sufficient | Partial | 5 | Soft | Yes | The Blue-card fraud closure and the security-hold transfer are well-defined, but the Green card's outcome and the Evergreen 'unlock' each rely on readings that a careful agent could reasonably make differently. |
| task_093 | Minor | None | Not sampled (-) | yes | None | Sufficient | Yes | 3 | Soft | Yes | Clean: the missing Green-checking boost and the multi-product relationship bonus are both documented, and the $33.00 correction follows directly. |
| task_094 | Major | Major | Confirmed (Major) | - | Minor | Sufficient | Partial | 4 | Soft | Yes | The KB describes the Gold Rewards Card's 0.025% both as a credit-card bonus that does not stack and as a separate relationship bonus that does, so $140 and $142 are both defensible corrections. |
| task_095 | Major | Major | Confirmed (Major) | - | Major | Sufficient | Partial | 4 | Soft | Yes | The wrong-boost diagnosis is solvable, but the same contested 0.025% Gold Rewards 'relationship bonus' makes $98 versus $100 a coin flip. |
| task_096 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 5 | Soft | Yes | Clean: each savings account's highest checking boost and highest credit-card bonus are documented, and both corrections follow uniquely. |
| task_097 | Blocker | Blocker | Adjusted (Major) | yes | Major | Sufficient | Partial | 5 | Soft | No | The gold leaves out the documented 0.025% multi-product relationship bonus on the Silver account, the same bonus task_093's gold requires, so a doc-following agent's Silver credit and report fail. |
| task_098 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 3 | Soft | Yes | Clean: given a $600 deposit, the Blue Account is the unique best combined referral bonus, and the rolling window allows one more referral. |
| task_099 | Minor | None | Not sampled (-) | yes | None | Sufficient | Yes | 3 | Soft | Yes | Clean: for a $30,000 business deposit, World Blue's $300 referrer bonus is the unique maximum the customer qualifies for. |
| task_100 | None | None | Confirmed (None) | yes | Minor | Sufficient | Yes | 3 | Soft | Yes | Clean: the on-file open date gives 65 days of tenure, which rules out World Blue, so Hunter Green's $175 is the best referrer bonus available. |
| task_101 | Major | Major | Confirmed (Major) | yes | Blocker | Sufficient | Partial | 5 | Strict | Yes | Purple plus Sky Blue is the right pair if only two referrals can go now, but the docs can also be read as allowing all four. |
| task_102 | Blocker | Blocker | Confirmed (Blocker) | yes | Major | Insufficient | Partial | 5 | Strict | No | The grading requires the agent to 'recognize' that Ember is over Sky Blue's 4-year limit, but nothing the agent can see says so. 'Maximize the bonus' also points to Lime Green ($200 to the customer) rather than the gold's Sky Blue ($150). |

## Findings (Blocker and Major)

### task_010 — Major

**The diagnosis (a weekly referral cap that has now passed) is clear, but the gold expects the customer to resubmit with a tool the knowledge base never mentions. An agent that hands over the documented referral-link tool fails the DB check.**

- **non_determinism (Major)** — The KB's only documented way to start a new credit-card referral is to give the customer get_referral_link via give_discoverable_user_tool. The gold instead has the customer call the base user tool submit_referral and never gives a tool. Giving the documented tool writes a user_discoverable_tools row that the gold lacks, so the hashes diverge.
  - doc_credit_cards_credit_cards_(general)_009: "Provide the customer with this tool and instruct them to run it themselves:\n  - `get_referral_link(user_id: str, card_name: str)`"
  - doc_credit_cards_credit_cards_(general)_020: "To refer a friend, you'll need to generate a unique referral link that's tied to your account. You can do this through the Rho-Bank mobile app, online banking portal, or by contacting our customer service team."
  - `No KB document mentions submit_referral (grep over documents/*.json returns only general_009 for get_referral_link and nothing for submit_referral)`
  - gold[1] = submit_referral(user_id 76ad9cc60e, account_type 'Platinum Rewards Card'), requestor user; task_010.user_tools = ['apply_for_credit_card','submit_referral'] (no call_discoverable_user_tool)
  - Replay: gold + give_discoverable_user_tool('get_referral_link') adds user_discoverable_tools['fc21fceb1501a934'] = {tool_name: get_referral_link, status: GIVEN}, and the agent DB hash no longer equals the gold hash
  - *Why it matters:* Instruction 7 makes the customer retry once the agent explains the cap has passed. A KB-faithful agent will usually help by giving the documented referral-link tool. That write alone fails the task, even though the customer, who has no tool to run get_referral_link, then resubmits correctly with submit_referral.
  - *Fix:* Make the gold path the documented one: give the user get_referral_link (add call_discoverable_user_tool to user_tools) and expect call_discoverable_user_tool(get_referral_link, {user_id, card_name: 'Platinum Rewards Card'}). Alternatively, document submit_referral in the KB as the retry path.

*Verifier: Confirmed (Major → Major).* Reproduced the diagnosis and the hash divergence. The gold credits an agent that explains the cap and leaves the retry to the customer's own undocumented submit_referral. The KB-documented retry path (giving get_referral_link) fails. That is two defensible action sets, so Major.

### task_014 — Major

**The gold requires a transfer to a human, but the knowledge base's own referral-link procedure says that when a card has no documented referral program the agent should explain and 'Do not transfer to a human'.**

- **document_contradiction (Blocker)** — The referral-link procedure doc forbids transferring when a card has no documented referral program, which is exactly the Crypto-Cash Back situation here. The transfer-code table and the gold both treat transfer as the required action.
  - doc_credit_cards_credit_cards_(general)_009: "If no referral program is documented for the requested card, or if the user’s claimed terms are incorrect, or if there is reason to believe the referral will be automatically rejected, explain why and do not provide a referral link tool. Do not transfer to a human in these cases."
  - No Crypto-Cash Back referral document exists: grep -il referral over doc_credit_cards_crypto* returns nothing (crypto docs 001-009 cover rewards, wallets, conversion, tax, FAQ)
  - doc_bank_accounts_bank_accounts_(general)_042 (Tier 2): "unconfirmed_external_communication | Customer claims a specific promotion/program/offer exists (they have a letter, email, or flyer) but you cannot verify or find it in the KB after searching"
  - policy_header.md guideline 5: "Do not transfer without asking the user first. This guidance may be overridden by specific scenario-based transfer guidance in the knowledge base."
  - gold[0] = transfer_to_human_agents(reason 'unconfirmed_external_communication'), compare_args ['reason'], reward_basis ['ACTION']; required_documents omits general_009
  - *Why it matters:* The customer is asking how to get a referral link, so general_009 ('Generating a Credit Card Referral Link (Internal)') is the procedure a competent agent will retrieve, and it explicitly forbids the transfer. The policy says scenario-specific KB transfer guidance overrides the general transfer rules. An agent that follows it explains and does not transfer, and the customer never demands one (she only accepts one if offered), so the only gold action is never made and the ACTION reward is 0. Passing depends on the agent missing or overriding general_009.
  - *Fix:* Either change general_009 to carve out claims backed by an official communication (e.g. 'If the customer cites an official Rho-Bank letter/email for a program you cannot find, offer a transfer with reason unconfirmed_external_communication'), or change the task's gold to the no-transfer outcome and grade it on communicated information.

*Verifier: Adjusted (Blocker → Major).* The conflict is real: 009 forbids a transfer for a card with no documented referral program, and the gold transfers. But 042's 'When to Use' row is itself scenario-specific transfer guidance that names exactly this situation (a letter the agent cannot verify), so the gold follows a document-supported reading. Two documents give opposite instructions for the same scenario, and the gold follows one, so the calibration rule gives Major, not Blocker.

### task_017 — Major

**The gold disputes two clearly wrong rewards, but a third transaction is over-credited by one point under every rounding rule, and nothing tells the agent whether to dispute it.**

- **non_determinism (Major)** — txn_31fd03682992 (Hilton Seattle, Travel, $289.50) earns exactly 289.50 x 4 = 1158 points, with no fractional part, yet it is stored as 1159. This is a 1-point over-credit under any rounding convention. The gold leaves it out without any stated rule for ignoring over-credits or small differences.
  - `db.json credit_card_transaction_history[txn_31fd03682992]: transaction_amount '$289.50', category 'Travel', rewards_earned '1159 points'`
  - `doc_credit_cards_silver_rewards_card_002: "Pay with your card for eligible travel and software transactions to earn 4.0% back"`
  - doc_credit_cards_credit_cards_(general)_003: "Use this process when a customer believes there is a discrepancy between the cash back they received and the cash back they should have received."
  - `task_017 instructions: "help you fix any errors"`
  - `gold disputes only txn_cfabb609133d and txn_913d14a20dc5 (gold[2], gold[3])`
  - *Why it matters:* An agent that reports every discrepancy, which is what tasks 018 and 022 reward for overpaid transactions, hands the user a third dispute. That adds a cash_back_disputes row and a user_discoverable_tool_calls row. A replay of gold plus a dispute on txn_31fd03682992 mismatches on both the agent and user hashes.
  - *Fix:* Set txn_31fd03682992.rewards_earned to '1158 points', or add it to the gold if over-credits are meant to be disputed.
- **document_gap (Minor)** — The rewards rounding rule that fixes the dispute set lives in doc_credit_cards_credit_cards_(general)_007, which is retrievable from the KB but is not listed in required_documents.
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - Without the floor rule, txn_cedd88ce1f65 (Adobe, Software, $54.99 x 4 = 219.96, stored 219) also mismatches under round-half-up (220), giving a fourth candidate dispute.
  - *Why it matters:* Under the default retrieval configs the agent can find the floor rule, so the gold is reachable. Under configs that inline only required_documents (golden_retrieval / required_docs prompts) the rule is absent, the natural round-half-up convention flags many correctly credited transactions, and the extra disputes change the DB hash.
  - *Fix:* Add doc_credit_cards_credit_cards_(general)_007 to required_documents.

*Verifier: Confirmed (Major → Major).* Recomputed all five Silver transactions. The two gross under-credits match the gold, and the 1-point over-credit on 31fd03 fits no rounding rule, so whether the user files a third dispute depends on the agent's choice: Major. The secondary Minor (rounding doc not in required_documents) also holds.

### task_020 — Major

**The seeded rewards were computed with ordinary rounding, but the knowledge base says rewards are always rounded down, so an agent that follows the KB finds nine extra one-point over-credits that the gold does not dispute.**

- **document_contradiction (Major)** — Non-error transactions for user 755bcb4d5d are stored with round-half-up values, while the KB rule is floor. Under the documented rule, nine transactions are over-credited by exactly 1 point, and the gold disputes none of them.
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - `db.json txn_a8f1c2d3e402 Adobe $54.99 Business Silver (2x promo, 20%) = 1099.8 -> floor 1099, stored '1100 points'`
  - `db.json txn_b7e2d4c5f512 Nordstrom $187.50 Silver 1% = 187.5 -> floor 187, stored '188 points'`
  - floor false positives (all stored = floor+1): a8f1c2d3e402, a8f1c2d3e404, a8f1c2d3e406, a8f1c2d3e409, a8f1c2d3e414, b7e2d4c5f503, b7e2d4c5f507, b7e2d4c5f509, b7e2d4c5f512
  - `task_020 instructions: "you like to keep track of every dollar" ... "help resolve any discrepancies"`
  - *Why it matters:* An agent that retrieves and applies the documented floor rule sees 13 discrepancies, not 4. If it treats over-credits as discrepancies to dispute, as tasks 018 and 022 reward, the user files nine extra disputes and the DB hash fails. The gold is reached only by an agent that never finds the rounding doc or that chooses to ignore 1-point over-credits.
  - *Fix:* Re-seed the nine non-error transactions with floor values (e.g. a8f1c2d3e402 -> '1099 points', b7e2d4c5f512 -> '187 points'), which keeps the gold unchanged and makes the KB rule produce exactly four disputes.

*Verifier: Confirmed (Major → Major).* Recomputed all 26 transactions with the double promo and exclusions. The seed follows round-half-up while the KB prescribes floor, so a KB-faithful agent sees nine 1-point over-credits. The gold passes only if the agent does not dispute them. Same class and severity as 017.

### task_024 — Major

**The gold assumes the Business Bronze card ($400 cash back + $500 promo) is the best card for a $40,000 truck, but the Silver Zoom card's triple-cash-back promo pays about $1,200; it wins unless the agent decides a landscaping company cannot get a card the KB describes as built for logistics businesses.**

- **non_determinism (Major)** — With a claimable 3x promo (window through 2025-12-31), Silver Zoom earns 3 x 1.0% on non-category purchases: $40,000 x 3% = $1,200, minus the $74.50 fee = $1,125.50, versus $900 for Business Bronze. The only grounds for excluding it are that the KB frames the card as 'designed for' and 'built for' transportation and logistics operators; its stated eligibility criteria are credit scores only.
  - doc_business_credit_cards_silver_zoom_card_012: "You must claim the promotion within the window starting 2024-01-01 and ending 2025-12-31" / "All other eligible purchases earn 3 × 1.0% during the promo period" / "The triple cash back earning period lasts 9 months from account opening"
  - doc_business_credit_cards_silver_zoom_card_001: "Who this card is built for - Established transportation and logistics operators" / "Annual membership is $74.50"
  - doc_business_credit_cards_silver_zoom_card_008: "Personal credit is evaluated and must be at or above $680" / "must be at or above 57 on the PAYDEX scale for logistics business approval"
  - `doc_business_credit_cards_business_bronze_rewards_card_010: promo 2025-10-01 to 2026-03-31, "$10,000 within the first 2 months" -> "$500 statement credit"`
  - `task_024 instructions (hidden from agent): "looking to expand your fleet"`
  - `gold[0].arguments.card_type = 'Business Bronze Rewards Card'`
  - *Why it matters:* An agent that surveys every business card to 'maximize the total money back', as the customer asks, will find Silver Zoom's promo and recommend it. The user then applies for 'Silver Zoom Card', which is in VALID_CREDIT_CARD_TYPES, and a replay confirms the agent and user hashes both differ from gold. The gold is reached only by reading 'designed for logistics' as a hard eligibility bar, which no document states.
  - *Fix:* State in doc_..._silver_zoom_card_008 that applicants must operate a transportation/logistics business, or end the triple-cash-back claim window before 2025-11-14, or add the Silver Zoom docs to required_documents and state the intended exclusion in the task notes.

*Verifier: Confirmed (Major → Major).* Recomputed every business card. Bronze wins only if Silver Zoom is treated as closed to a landscaping company, which the KB implies ('built for', 'for logistics business approval') but never states as a requirement. Two defensible recommendations, so Major. Note: Bronze's credit line is '$10,000 and may be as high as $50,000', which a $40,000 purchase may exceed.

### task_025 — Major

**Whether the Business Platinum card is best for a $100,000 Apple Music purchase depends on treating Apple Music as a 4% 'software/media' purchase on that card. If it is ordinary spend, a different card pays more.**

- **non_determinism (Major)** — Gold = Business Platinum at $4,000 (4%), which requires Apple Music to count as 'software' or 'media' under doc_..._business_platinum_rewards_card_002. Apple Music is a consumer music-streaming licence, and the doc's examples are SaaS, cloud hosting, and digital ad placements. Read as ordinary spend, Platinum pays 1.5% = $1,500 and loses.
  - doc_business_credit_cards_business_platinum_rewards_card_002: "Travel, software, and media advertising purchases earn 4.0%." / "Typical qualifying transactions include airfare, hotels, car rentals, rideshare, SaaS subscriptions, cloud hosting, and digital ad placements" / "Purchases outside those categories earn 1.5%."
  - `doc_business_credit_cards_business_silver_rewards_card_005: "Hardware/Electronics Merchants (Software Exclusion): - Apple"`
  - `doc_business_credit_cards_business_silver_rewards_card_012: double promo "End date: 2025-11-14" (today per get_now())`
  - `doc_business_credit_cards_silver_zoom_card_012: "All other eligible purchases earn 3 × 1.0% during the promo period" (claim window to 2025-12-31)`
  - `gold[0].arguments.card_type = 'Business Platinum Rewards Card'`
  - *Why it matters:* Under the 'not software' reading: Business Platinum $1,500; Business Bronze $1,000 + $500 = $1,500; Business Silver (Apple excluded) 1% doubled by a promo still open on 11/14 = $2,000; Silver Zoom 3% = $3,000 - $74.50 if the agent treats it as open to a software company. The agent then recommends a non-Platinum card and the user's application row differs from gold. The Silver exclusion list labels Apple a 'Software Exclusion', which hints that Apple purchases count as software, but nothing says so for Platinum.
  - *Fix:* Make the purchase an unambiguous SaaS licence (e.g. an enterprise software platform), or state in doc_..._business_platinum_rewards_card_002/003 that streaming-media subscriptions qualify for 4%.

*Verifier: Confirmed (Major → Major).* Reproduced. The Silver exclusion list hints that the author treats Apple purchases as software, but nothing places Apple Music in Platinum's 4% categories, and 'media' there means advertising. The gold depends on that classification, so Major.

### task_026 — Blocker

**The agent is expected to trust the customer's claim that the disputes were approved and then write corrected reward values, but it has no way to check dispute status, the same conversation in task_027 expects the opposite, and one gold value (1500) contradicts the KB's round-down rule (1499).**

- **underspecified_instructions (Blocker)** — Whether to apply reward corrections depends on cash_back_disputes.status (RESOLVED in task_026 via auto_resolve_disputes=True, SUBMITTED in task_027), but no agent tool reads that table, and dispute-tool results go only to the user simulator. Tasks 026 and 027 use the same user, transactions, and dispute set, and their Phase-2 user messages are word-for-word identical, so the agent sees the same conversation in both.
  - doc_credit_cards_credit_cards_(general)_004: "Look up the user's resolved disputes in the cash_back_disputes database to find the transaction_id values that need rewards adjustments."
  - tools.py get_user_dispute_history_7291 docstring: "Retrieve a user's credit card transaction dispute history from the transaction_disputes table" (not cash_back_disputes); no other KnowledgeTools method queries cash_back_disputes
  - `orchestrator.py Orchestrator.step: ENV tool results for a USER tool call are routed back to the user (to_role = from_role), never to the agent`
  - task_026 Phase 2 and task_027 Phase 2 user line: "Great, I've submitted all the disputes. I just got a notification that they've all been approved and resolved! Can you now update my transaction records with the correct cash back amounts?"
  - `task_026.initial_state: auto_resolve_disputes = true; task_027.initial_state: auto_resolve_disputes = false`
  - *Why it matters:* Replays confirm that refusing the updates fails task_026 and applying them fails task_027. Because the agent's observations are the same in both tasks, any single policy (trust the customer, or refuse without verification) passes at most one of them. Each task's outcome reflects the agent's disposition, not its use of evidence.
  - *Fix:* Add an agent read tool for cash_back_disputes (e.g. get_cash_back_disputes_by_user, documented in doc_..._(general)_004) so the agent can verify RESOLVED vs SUBMITTED, and add that read to both golds so it is logged and required.
- **argument_error (Blocker)** — gold[10] writes '1500 points' for Zoom $149.99 on Business Silver at 10% = 1499.9 points. The KB rounding policy floors this to 1499, and doc_..._(general)_004 tells the agent to write the correct whole-number value.
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - `doc_credit_cards_credit_cards_(general)_004: "new_rewards_earned: a string formatted as 'X points' where X is the correct whole-number point value"`
  - `db.json txn_a8f1c2d3e411: Zoom Video, Software, '$149.99', 09/15/2025 (after the 08/13/2025 promo end)`
  - `gold[10].arguments.arguments = {"transaction_id": "txn_a8f1c2d3e411", "new_rewards_earned": "1500 points"}`
  - *Why it matters:* An agent that follows the documented rule writes '1499 points'. A replay of gold with that one value changed gives a different agent hash (cab5086583a3...), so policy-faithful work fails. Only an agent that misses the rounding doc and rounds half-up matches.
  - *Fix:* Change gold[10] to '1499 points' (and re-seed task_020/026/027 non-error rows to floor), or change the KB rounding policy to round-half-up.
- **document_contradiction (Major)** — The dispute set is the same as task_020: seeded non-error rewards follow round-half-up, while the KB prescribes floor. Under the documented rule, nine transactions are over-credited by 1 point and are not in the gold.
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - `db.json txn_a8f1c2d3e402 Adobe $54.99 at 20% = 1099.8 -> floor 1099, stored '1100 points'`
  - `floor false positives: a8f1c2d3e402, a8f1c2d3e404, a8f1c2d3e406, a8f1c2d3e409, a8f1c2d3e414, b7e2d4c5f503, b7e2d4c5f507, b7e2d4c5f509, b7e2d4c5f512`
  - *Why it matters:* An agent that applies the documented floor rule and treats over-credits as discrepancies has the user file 13 disputes instead of 4, which changes the hash.
  - *Fix:* Re-seed the nine non-error transactions with floor values.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced all three issues. Independently of the dispute-status problem, gold[10] encodes round-half-up against the documented floor rule, so a policy-faithful agent that trusts the customer still fails. That gold value follows no document-supported reading: Blocker.

*Reconciled across runs: Blocker → Blocker (none (already agreed)).* Included for 026-029 consistency; both runs already agree. The dispute-status defect is Major here as in 027-029, but gold[10] writes '1500 points' where the only documented rounding rule gives 1499, so the gold follows no document-supported reading. credit_card_transaction_history is compared exactly under both scorers.

### task_027 — Major

**The agent is expected to see through the customer's false claim that the disputes were approved, but it has no tool to check dispute status, and task_026 presents the identical conversation with the opposite expected outcome.**

- **underspecified_instructions (Blocker)** — Whether to apply reward corrections depends on cash_back_disputes.status (RESOLVED in task_026 via auto_resolve_disputes=True, SUBMITTED in task_027), but no agent tool reads that table, and dispute-tool results go only to the user simulator. Tasks 026 and 027 use the same user, transactions, and dispute set, and their Phase-2 user messages are word-for-word identical, so the agent sees the same conversation in both.
  - doc_credit_cards_credit_cards_(general)_004: "Look up the user's resolved disputes in the cash_back_disputes database to find the transaction_id values that need rewards adjustments."
  - tools.py get_user_dispute_history_7291 docstring: "Retrieve a user's credit card transaction dispute history from the transaction_disputes table" (not cash_back_disputes); no other KnowledgeTools method queries cash_back_disputes
  - `orchestrator.py Orchestrator.step: ENV tool results for a USER tool call are routed back to the user (to_role = from_role), never to the agent`
  - task_026 Phase 2 and task_027 Phase 2 user line: "Great, I've submitted all the disputes. I just got a notification that they've all been approved and resolved! Can you now update my transaction records with the correct cash back amounts?"
  - `task_026.initial_state: auto_resolve_disputes = true; task_027.initial_state: auto_resolve_disputes = false`
  - *Why it matters:* Replays confirm that refusing the updates fails task_026 and applying them fails task_027. Because the agent's observations are the same in both tasks, any single policy (trust the customer, or refuse without verification) passes at most one of them. Each task's outcome reflects the agent's disposition, not its use of evidence.
  - *Fix:* Add an agent read tool for cash_back_disputes (e.g. get_cash_back_disputes_by_user, documented in doc_..._(general)_004) so the agent can verify RESOLVED vs SUBMITTED, and add that read to both golds so it is logged and required.
- **document_contradiction (Major)** — The dispute set is the same as task_020: seeded non-error rewards follow round-half-up, while the KB prescribes floor. Under the documented rule, nine transactions are over-credited by 1 point and are not in the gold.
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - `db.json txn_a8f1c2d3e402 Adobe $54.99 at 20% = 1099.8 -> floor 1099, stored '1100 points'`
  - `floor false positives: a8f1c2d3e402, a8f1c2d3e404, a8f1c2d3e406, a8f1c2d3e409, a8f1c2d3e414, b7e2d4c5f503, b7e2d4c5f507, b7e2d4c5f509, b7e2d4c5f512`
  - *Why it matters:* An agent that applies the documented floor rule and treats over-credits as discrepancies has the user file 13 disputes instead of 4, which changes the hash.
  - *Fix:* Re-seed the nine non-error transactions with floor values.

*Verifier: Confirmed (Blocker → Blocker).* The deciding fact (SUBMITTED vs RESOLVED) is invisible to the agent. 026/027 present identical agent-visible evidence with opposite golds, so the outcome tracks the agent's disposition, not its use of evidence. A cautious agent reaches this gold, but the benchmark rewards the opposite disposition on the same input in 026 and 028. Blocker under the 'information needed does not exist' rule, consistent with 026.

*Reconciled across runs: Blocker → Major (judgment).* The deciding fact (cash_back_disputes.status SUBMITTED) is invisible to the agent: no agent tool reads that table and user-tool output is routed only to the user. But the no-update gold is reachable by a document-supported reading (doc_004 requires a resolved-dispute lookup the agent cannot perform, so it declines), and updating on the customer's word is the competing reading that task_026/028 reward. Calibration: two document-supported readings with different graded states is Major; Blocker is reserved for a gold that follows no supported reading, which is not the case here. The separate half-up seed vs doc_007 floor contradiction is also Major in both runs, so the task is Major under both scorers (all affected tables are writes compared exactly).

### task_028 — Major

**The rewards math is fully documented and reproduces the gold exactly, but the agent has no way to confirm the disputes were approved, so it must update rewards on the customer's word alone. Task_029 shows the same evidence and expects a refusal.**

- **non_determinism (Major)** — doc_004 tells the agent to look up the customer's resolved disputes in cash_back_disputes before updating rewards. No agent tool can read that table, and the user tool's 'RESOLVED' output goes only to the user, so the agent can only take the customer's claim on trust. Updating on that claim and declining because the required lookup is impossible are both defensible, and the gold credits only the first.
  - doc_credit_cards_credit_cards_(general)_004: "Look up the user’s resolved disputes in the cash_back_disputes database to find the transaction_id values that need rewards adjustments."
  - tools.py: the only reference to cash_back_disputes is the add_to_db in KnowledgeUserTools.submit_cash_back_dispute_0589; no agent tool or discoverable tool reads it (get_user_dispute_history_7291 reads transaction_disputes only)
  - agent/base_agent.py is_valid_agent_history_message keeps only ToolMessages with requestor == 'assistant' and drops user tool-call messages, so the agent never sees the user tool's 'Status: RESOLVED - The dispute has been reviewed and approved.'
  - task_029 user_scenario: the user speaks the identical Phase 2 line ("I just got a notification that they've all been approved and resolved!") while the disputes are SUBMITTED, and its gold makes no update_transaction_rewards_3847 calls
  - `gold[8..14]: unlock + six update_transaction_rewards_3847 calls`
  - *Why it matters:* A cautious agent that won't update without the documented lookup leaves the six transactions unchanged and fails the DB hash. Because task_029 rewards exactly that refusal on the same agent-visible evidence, no fixed policy passes both tasks.
  - *Fix:* Add a discoverable read tool for cash_back_disputes (e.g. get_cash_back_dispute_status) documented in doc_004 and include it in both golds, so the agent can see RESOLVED here and SUBMITTED in task_029.
- **document_contradiction (Minor)** — The EcoCard earn-rate doc writes points as dollar amounts, and the rounding doc's worked example has broken intermediate arithmetic. The intended values (5 or 1 points per dollar, floor) can still be recovered, and the seed rewards_earned values agree with that reading.
  - `doc_credit_cards_ecocard_002: "Green purchases: Earn $5.00 sustainability points per dollar spent"`
  - `doc_credit_cards_ecocard_002: "A $100 purchase at a qualifying green merchant earns 100 × $5.00 points."`
  - `doc_credit_cards_credit_cards_(general)_007: "126.77 × 0.01 = 1.2677 points, which rounds down to 1 point per dollar, giving 126 points"`
  - `db.json credit_card_transaction_history[txn_e83813b6528a] EcoCard Green $147.63 -> rewards_earned '738 points' (= floor(147.63*5))`
  - *Why it matters:* These are cosmetic corruptions. A careful agent gets 642 points for txn_896ac64b98d7 ($128.47 x 5) either way, but the dollar sign invites a misreading.
  - *Fix:* Write 'Earn 5 sustainability points per dollar' and fix the example to '$126.77 x 1 point per dollar = 126.77, floored to 126 points'.

*Verifier: Upgraded (Major → Blocker).* The rewards math reproduces exactly. The remaining defect, applying corrections on a dispute status the agent cannot observe while task_029 expects refusal on identical evidence, is the same defect class the review rated Blocker in 026/027 with no stated reason to differ. Raised to Blocker for consistency. The Minor EcoCard '$5.00 points' issue holds.

*Reconciled across runs: Blocker → Major (judgment).* Same unobservable-dispute-status defect as 027/029, mirrored: the gold updates six transactions on the customer's unverifiable claim while task_029 expects refusal on identical agent-visible input. Updating is document-supported (the agent already holds the transaction ids that doc_004's lookup exists to find), and declining is the competing supported reading, so calibration gives Major, not Blocker. Run U's verifier raised it to Blocker only to match U's 026/027 ratings, which this reconciliation also sets to Major for this defect; the Phase-1 floor arithmetic reproduces exactly, and the EcoCard '$5.00 points' corruption stays Minor.

### task_029 — Major

**To pass, the agent must refuse to update rewards because the disputes are still pending, but it has no tool to see dispute status and hears the same 'they were approved' claim that task_028 expects it to act on.**

- **underspecified_instructions (Major)** — The gold (no reward updates) depends on cash_back_disputes rows having status SUBMITTED (auto_resolve_disputes=false). No agent tool exposes that status, and the user's tool output is invisible to the agent. The only distinguishing fact is unobservable, and the agent-visible conversation matches task_028, where updating is gold.
  - `initial_state.initialization_data.agent_data.task_config.data.dispute_settings.auto_resolve_disputes = false`
  - tools.py KnowledgeUserTools.submit_cash_back_dispute_0589 writes status 'SUBMITTED' and returns 'Status: SUBMITTED - Your dispute has been queued for review.' to the user only
  - `doc_credit_cards_credit_cards_(general)_004: "Look up the user’s resolved disputes in the cash_back_disputes database" (no tool named; none exists)`
  - `description.notes: "Agent must verify dispute status and refuse to update transactions when disputes are still SUBMITTED"`
  - `task_028 gold[9..14]: the same Phase 2 claim leads to six update_transaction_rewards_3847 calls`
  - *Why it matters:* An agent that trusts the customer calls update_transaction_rewards_3847 and fails the DB hash. Only an agent that refuses on principle passes, and that agent fails task_028. The intended skill, verifying status, cannot be exercised.
  - *Fix:* Expose a discoverable read of cash_back_disputes (documented in doc_004) so the agent can see SUBMITTED; add it to both the 028 and 029 golds.
- **document_gap (Minor)** — required_documents leaves out doc_credit_cards_credit_cards_(general)_007, the floor-rounding policy that separates the 6 real errors from 22 off-by-one rows. The doc is in the KB and searchable, so only the golden_retrieval config, which inlines required docs and has no search tool, lacks it.
  - `task_029.required_documents lacks doc_credit_cards_credit_cards_(general)_007; task_028.required_documents includes it`
  - `doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number."`
  - `Computed over user 890389b165's 47 transactions: floor gives 6 mismatches (= gold[2..7]); round-half-up gives 28`
  - `retrieval.py: golden_retrieval builds the prompt from task.required_documents and provides no retrieval tools`
  - *Why it matters:* Under golden_retrieval, an agent that rounds half-up would give 22 extra disputes to the user and fail. The seed data, where every stored value equals the floor, lets a careful agent infer truncation, so the risk is small.
  - *Fix:* Add doc_credit_cards_credit_cards_(general)_007 to task_029.required_documents.
- **document_contradiction (Minor)** — The EcoCard earn-rate doc writes points as dollar amounts, and the rounding doc's worked example has broken intermediate arithmetic. The intended values (5 or 1 points per dollar, floor) can still be recovered, and the seed rewards_earned values agree with that reading.
  - `doc_credit_cards_ecocard_002: "Green purchases: Earn $5.00 sustainability points per dollar spent"`
  - `doc_credit_cards_ecocard_002: "A $100 purchase at a qualifying green merchant earns 100 × $5.00 points."`
  - `doc_credit_cards_credit_cards_(general)_007: "126.77 × 0.01 = 1.2677 points, which rounds down to 1 point per dollar, giving 126 points"`
  - `db.json credit_card_transaction_history[txn_e83813b6528a] EcoCard Green $147.63 -> rewards_earned '738 points' (= floor(147.63*5))`
  - *Why it matters:* These are cosmetic corruptions. A careful agent gets 642 points for txn_896ac64b98d7 ($128.47 x 5) either way, but the dollar sign invites a misreading.
  - *Fix:* Write 'Earn 5 sustainability points per dollar' and fix the example to '$126.77 x 1 point per dollar = 126.77, floored to 126 points'.

*Verifier: Confirmed (Major → Major).* Reproduced: the only fact separating 029 (refuse) from 028 (update) is the cash_back_disputes status, which no agent tool exposes, while the customer makes the same 'approved and resolved' claim. Refusing is still a reading the docs support (doc_003 says submissions are 'queued for review'; doc_004 requires a lookup the agent cannot perform), so this is two document-supported readings and Major is the calibrated severity. The doc_007 omission (Minor, decisive for floor rounding) and the EcoCard '$5.00 points' corruption (Minor, because it is the deciding rate for txn_896ac64b98d7) are correctly calibrated. Unlike 028, the script has no 'insist on disputing the overpaid one' line, a residual risk for gold[7].

*Reconciled across runs: Major → Major (none (already agreed)).* Both runs already agree; kept for 026-029 consistency. The refuse-to-update gold depends on a status no agent tool exposes, while task_028 rewards updating on the same message: two document-supported readings, Major. The doc_007 omission from required_documents (Minor) and the EcoCard '$5.00' corruption (Minor) stand.

### task_039 — Major

**The gold grants provisional credit to only 3 of 4 qualifying disputes because it counts disputes filed earlier in the same conversation toward the 'no more than 2 in 12 months' rule; that reading is defensible but not the only one, and it also depends on filing order.**

- **non_determinism (Major)** — Four disputes qualify by reason: Costco dup $312.87, Costco fraud $234.56, Amazon dup $215.67, Amazon fraud $129.45. The user has zero prior disputes. The gold marks the first three filed eligible and the Amazon fraud ineligible, which only works if criterion 4 counts disputes filed earlier in this session. Reading criterion 4 against the pre-existing history (0) makes all four eligible.
  - `doc_credit_cards_credit_cards_(general)_015: "4. Previous Disputes: The customer has not filed more than 2 disputes in the past 12 months"`
  - db.json transaction_disputes: no rows for user 01f21c9970 (only dsp_7a3e91b4c2d8 for 6680a37184); get_user_dispute_history_7291 returns 'No transaction disputes found for this user.'
  - `gold[9].arguments: txn_2f16599b9075 unauthorized_fraudulent_charge, eligible_for_provisional_credit false; gold[6..8] eligible true`
  - `Replay: setting gold[9] eligible=true changes the DB hash (verified)`
  - *Why it matters:* An agent that checks history once and finds 0 prior disputes marks all four eligible and fails the exact-hash comparison. The gold's reading is supported by the literal text (when the 4th is filed, 3 disputes have been filed in the past 12 months), and get_user_dispute_history_7291 would show the in-session filings, but a reasonable agent can read 'previous' as pre-existing history.
  - *Fix:* State in doc_015 that disputes filed earlier in the same interaction count toward criterion 4, or make the history-only reading gold (all four eligible).
- **hidden_ordering (Major)** — Under the gold's in-session reading, criterion 4 counts ALL disputes, including reason-ineligible ones. The final eligible set therefore depends on filing order. The gold only results if the three largest reason-eligible disputes are filed before any other dispute; filing in the customer's listing order (Costco fraud, Costco dup, Costco not-as-described, ...) leaves only two eligible.
  - `gold[6..8] files $312.87, $234.56, $215.67 first; gold[9..13] after`
  - user_scenario step 8: "If there's any limit on provisional credit, I want it applied to the biggest charges first... Do not mention this if the agent does NOT bring provisional credit up."
  - In user listing order the 5th filing (Amazon fraud) sees 4 prior and the 6th (Amazon dup $215.67) sees 5 prior, so both are ineligible: 2 eligible vs the gold's 3
  - *Why it matters:* Even an agent that adopts the gold's reading must plan to file the three largest eligible disputes first. The tie-break preference surfaces only if the agent raises provisional-credit limits with the customer.
  - *Fix:* Define the cap as 'at most N provisional credits per 12 months' and let the customer's priority choose which ones, independent of filing order.
- **underspecified_instructions (Minor)** — Several stored values have no scripted customer answer: resolution_requested for each dispute (gold: partial_refund $50 for the incorrect-amount charge, full_refund otherwise), the replacement's shipping address (gold: registered home address), and expedited shipping (gold: true). The natural simulator answers match the gold (a $50 overcharge, free expedited on a Gold card recommended for fraud), but none is scripted.
  - `user_scenario has no resolution, shipping-address, or expedited step (steps 4 and 6 are missing)`
  - `gold[11]: "resolution_requested": "partial_refund", "partial_refund_amount": 50`
  - `gold[15]: "shipping_address": "4532 Magnolia Lane, Philadelphia, PA 19103", "expedited_shipping": true`
  - `doc_credit_cards_credit_card_replacements_002: Premium-tier (Gold Rewards Card) expedited $0.00`
  - *Why it matters:* If the simulator improvises differently (e.g. 'full refund on everything'), the record differs. This is simulator variance rather than an agent error.
  - *Fix:* Script the resolution per transaction and the shipping preference in the user scenario.

*Verifier: Confirmed (Major → Major).* Both readings of criterion 4 are document-supported: the literal 'has not filed more than 2 disputes in the past 12 months' supports counting in-session filings, and the 'Previous Disputes' label supports history only. The gold follows one of them, so Major is calibrated. The gold also requires filing the largest eligible disputes first, a preference the customer reveals only if the agent raises provisional credit. I considered Blocker, but the information needed exists, so Major holds. The unscripted resolution for the $50 overcharge is entailed by the script's facts ('charged you $50 extra'), so Minor is defensible there (see calibration notes).

### task_040 — Major

**Same provisional-credit cap problem as task_039 (one earlier dispute plus in-session counting leaves only two eligible), and the gold asks for a full refund on a Comcast charge where the customer was promised only a partial one.**

- **non_determinism (Major)** — There is one pre-existing dispute in the past 12 months (dsp_ed3ab3dce038, submitted 09/20/2025). Read against history alone (1, not more than 2), criterion 4 makes all four fraud/duplicate disputes eligible. The gold marks only Grainger and Uline eligible and American Airlines and Best Buy ineligible, which requires counting in-session filings (1 to 2 to 3) and filing Grainger and Uline before every other dispute.
  - `doc_credit_cards_credit_cards_(general)_015: "4. Previous Disputes: The customer has not filed more than 2 disputes in the past 12 months"`
  - `initial_state.agent_data.transaction_disputes.dsp_ed3ab3dce038.submitted_at = '09/20/2025'`
  - gold[9] txn_a1b2c3d4e503 (AA fraud $342.50) eligible false; gold[10] txn_a1b2c3d4e510 (Best Buy dup $189.99) eligible false; gold[7],[8] Grainger/Uline eligible true
  - `description.notes cites 'provisional_credit_max_disputes_in_period = 3', a rule that appears in no KB document`
  - `user_scenario step 6: "Please prioritize those if there's any limit." (only if the agent raises provisional credit)`
  - *Why it matters:* A history-only reading (all four eligible) fails the hash. With in-session counting, filing in the customer's listing order (AA first, Best Buy second) makes AA and Best Buy eligible instead, which also fails.
  - *Fix:* State in doc_015 that in-session disputes count and that the customer's priority decides which ones receive credit, or make all four eligible in the gold.
- **instruction_gold_mismatch (Major)** — For the Comcast $189.99 charge the customer 'was promised a partial refund' after downgrading, but the gold files resolution_requested=full_refund. The customer isn't scripted with a resolution preference or a partial amount, so 'partial refund' (amount unknown) and 'full refund' are both plausible, and the scenario text leans partial.
  - `user_scenario: "Comcast $189.99 on 10/30/2025 - REFUND NOT PROCESSED. You downgraded your business internet plan and were promised a partial refund weeks ago."`
  - `gold[14].arguments: "dispute_reason": "refund_never_processed", "resolution_requested": "full_refund"`
  - `doc_credit_cards_credit_cards_(general)_014: "13. resolution_requested (string) - Ask user what resolution they want."`
  - *Why it matters:* An agent that records the customer's 'partial refund' answer, with whatever amount it can get, stores a different resolution_requested and partial_refund_amount and fails the DB hash.
  - *Fix:* Script the resolution for each of the 8 disputes (and the Comcast partial amount if partial is intended), or change the scenario text to a full-refund story.
- **argument_error (Minor)** — The injected prior dispute is internally inconsistent: it was submitted (09/20/2025) and noticed (09/15/2025) before the purchase it disputes (10/02/2025). Both dates are within 12 months, so the criterion-4 count is unaffected.
  - `initial_state dsp_ed3ab3dce038: purchase_date '10/02/2025', issue_noticed_date '09/15/2025', submitted_at '09/20/2025'`
  - `db.json credit_card_transaction_history[txn_8d1aa1219382].transaction_date = '10/02/2025'`
  - *Why it matters:* Cosmetic. An agent reading the history may question whether the record is valid, but it still counts as one dispute in the past 12 months either way.
  - *Fix:* Set the prior dispute's purchase date before its notice and submission dates (e.g. a September transaction).

*Verifier: Confirmed (Major → Major).* Reproduced the 1-prior running count and the Comcast full-vs-partial ambiguity. Both are Major-class: two supported readings, and an unscripted customer choice with no documented default, where the gold choice is still a natural one. The fixture date inconsistency (noticed and submitted before the purchase) changes no count, so under the calibration it belongs in notes rather than as a Minor issue. Task severity is unaffected.

### task_041 — Major

**Sixteen card disputes whose gold record stores a $69.99 partial refund and refund types the customer is never told to ask for, plus a provisional-credit cap the documents only imply.**

- **underspecified_instructions (Blocker)** — Every dispute record stores resolution_requested, and the XFINITY record also stores partial_refund_amount = 69.99. The customer's instructions never say what resolution they want for any charge. The 69.99 can only be guessed from "around $120", and the AT&T charge, described as a promised partial refund, is gold full_refund.
  - `doc_credit_cards_credit_cards_(general)_014: "13. resolution_requested (string) - Ask user what resolution they want."`
  - `user_scenario.instructions (XFINITY): "Your usual bill is around $120. They overcharged you significantly." (no resolution stated)`
  - `user_scenario.instructions (AT&T): "were promised a partial refund weeks ago"`
  - `gold[19].arguments: "resolution_requested": "partial_refund", "partial_refund_amount": 69.99 (txn_dd095dee227f, $189.99)`
  - `gold[24].arguments: "resolution_requested": "full_refund" (AT&T txn_db96f3228527)`
  - `tools.py file_credit_card_transaction_dispute_4829 stores resolution_requested and partial_refund_amount in the transaction_disputes record`
  - *Why it matters:* Replay check: changing only the XFINITY dispute to full_refund, or to partial_refund 70, changes the DB hash. Which resolution the simulated customer names, and what amount, is improvised, so a correct agent that asks as the doc instructs matches only by chance. add_to_db refuses a second dispute on the same transaction, so the first answer cannot be corrected later.
  - *Fix:* Add the resolution the customer wants for each charge to the instructions, e.g. "For XFINITY, ask for a partial refund of $69.99 (the overcharge); for all others, a full refund."
- **non_determinism (Major)** — The gold marks only Staples and Coinbase eligible for provisional credit, though all 10 disputes with an eligible reason pass criteria 1, 2, 3 and 5. The cap of two comes from reading criterion 4 as a running count that includes disputes filed earlier in the same call. That reading fits the text and the other tasks, but the doc does not say whether same-call filings count, and it gives no rule for which two qualify. The gold resolves that with the customer's conditional "prioritize those" line.
  - `doc_credit_cards_credit_cards_(general)_015: "4. Previous Disputes: The customer has not filed more than 2 disputes in the past 12 months"`
  - `initial_state transaction_disputes.dsp_dfab0685d198.submitted_at = "09/20/2025" (1 prior dispute)`
  - gold[9]/gold[10]: eligible_for_provisional_credit true (Staples $623.45, Coinbase $512.34); gold[11] Delta $487.50 fraud on a Gold card opened 03/15/2024: false
  - `user_scenario.instructions: "If the agent mentions provisional credit or asks about it, say: ... Please prioritize those if there's any limit."`
  - `description.notes: "Only the 2 highest-value can get provisional credit" (tie-breaker not in any document)`
  - Cross-task: task_039 (0 prior) gold has 3 of 8 true; task_040 (1 prior) 2 true; task_080/081 (0 prior) 3 of 3 true, consistent with a running count capped at 3 total
  - *Why it matters:* Replay check: marking all 10 reason-eligible disputes true changes the hash. Reading criterion 4 as counting only disputes filed before the call gives 10 true. Counting the dispute being filed gives 1. Under the running count, an agent that never brings up provisional credit never hears the customer's priority, so it files in card order and marks Delta and Apple. Only the agent that recognises the cap and asks lands on Staples and Coinbase.
  - *Fix:* State in doc_015 that disputes filed earlier in the same interaction count toward criterion 4, and either have the customer name Staples and Coinbase unconditionally or document a tie-break rule such as highest amount first.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced all 16 records. I keep Blocker, and the stated reason that separates it from 040 is this: the gold persists a precise partial amount (69.99) that appears nowhere in the materials except as an approximation, on top of an unscripted resolution choice that the doc says to ask for. A correct agent therefore matches only if the simulator improvises exactly that value. This stacks with the AT&T full-vs-partial mismatch (the same defect 040 rates Major) and the running-count provisional cap (Major).

*Reconciled across runs: Blocker → Major (judgment).* Two independent Majors. Provisional credit: with one prior dispute (09/20/2025), the gold's Staples/Coinbase true and the rest false follow the running-count reading of criterion 4, while the prior-history-only reading makes all 10 reason-eligible disputes true; that is two supported readings. XFINITY partial_refund_amount 69.99 is an unscripted customer choice (doc_014 says to ask), but it is derivable as 189.99 - 120 from the script's 'around $120'. Calibration caps an unscripted choice with no documented default at Major, and run U's Blocker rested on that choice, so Major under both scorers (transaction_disputes is compared exactly in both).

### task_046 — Major

**Closure is blocked by a pending dispute, but the gold quietly forbids paying off the card's $125 balance, which the customer will ask for if the agent mentions it.**

- **hidden_ordering (Major)** — The gold stops after the dispute check, which is right because closure is blocked. But the account also has a $125 balance. The customer is scripted to ask for it to be paid from checking whenever the agent mentions it. Nothing in the documents says to stop checking at the first unresolvable blocker or not to process a payment the customer authorizes. That rule exists only in the author notes.
  - `db.json credit_card_accounts.cc_224959b99e_bsilver.current_balance = "$125.00"`
  - doc_credit_cards_credit_card_account_logistics_003: "Check these in order: ... 4. Outstanding balance: ... If a balance remains, the customer must pay it off before closure. If any requirement is not met, explain what must be resolved and do not proceed with retention offers."
  - user_scenario.instructions: "If you are told about an outstanding balance: Act surprised but agree to pay it. ... please pay that off from my checking account."
  - `description.notes: "Per the retention protocol, requirements 1-3 should be checked first since they cannot be resolved during the call."`
  - `gold = [log_verification, unlock+call get_user_dispute_history_7291] only`
  - *Why it matters:* Replay check: gold plus extra reads (accounts, pending replacements) matches, but gold plus a $125 pay_credit_card_from_checking_9182 does not. An agent that runs all four eligibility checks and reports every blocker, which "explain what must be resolved" invites, will be asked to pay and will fail for a customer-authorized, documented action.
  - *Fix:* Either set the bsilver balance to $0.00 in this task's initial state, or add to logistics_003: "If an earlier requirement cannot be resolved during the call, stop and do not process payments for later requirements."

*Verifier: Confirmed (Major → Major).* Confirmed. Reporting every unmet requirement and settling the resolvable balance at the customer's request is a reasonable reading of 'explain what must be resolved', and it fails the hash. Two supported readings make this Major. A new minor observation: the pending dispute cannot be tied to the bsilver account from data (the transaction does not exist, and its last-4 matches neither card). An agent can only detect this via a path that already fails, so it does not change severity.

### task_048 — Major

**Four-card closure where the gold requires the customer to apply for the Silver Rewards Card, though the knowledge base offers other cards that beat the competitor, including one with higher rewards.**

- **non_determinism (Major)** — The retention rule says to offer "a card with similar or better benefits" and gives no tie-breaker. For travel and software spend against a competitor paying 3.25%, the KB has several qualifying cards: Silver Rewards (4%, $0 fee), Platinum Rewards (10% on everything, 0% foreign fee, $200 fee), and the business cards. The gold accepts only an application for the Silver Rewards Card, and the scripted customer applies for whichever card is presented as competitive.
  - doc_credit_cards_credit_card_account_logistics_003: "Found a better card: Ask what features attracted them. If Rho-Bank offers a card with similar or better benefits, offer to help them apply instead of closing the current account."
  - `doc_credit_cards_silver_rewards_card_002: "Pay with your card for eligible travel and software transactions to earn 4.0% back"`
  - `doc_credit_cards_platinum_rewards_card_002: "You earn 10.0% cash back on all eligible purchases."`
  - `doc_business_credit_cards_business_silver_rewards_card_002: "Earn 10.0% cash back on eligible travel and software purchases"`
  - user_scenario.instructions step 8: "If the agent explains the card details and they're competitive or better than the competitor: Apply enthusiastically with the apply_for_credit_card tool."
  - `gold[18].arguments.card_type = "Silver Rewards Card"`
  - *Why it matters:* Replay check: the same trajectory with the application for "Platinum Rewards Card" instead of "Silver Rewards Card" changes the hash. An agent that recommends the strictly higher-earning Platinum Rewards Card follows policy, and the customer then applies for it and the task fails.
  - *Fix:* Add a tie-break to the retention protocol, e.g. "recommend the lowest-annual-fee card that matches or beats the competitor on the customer's stated categories", or have the customer state a no-annual-fee requirement that rules out Platinum.
- **document_contradiction (Minor)** — The Silver Rewards eligibility doc states the minimum credit score as a dollar amount. Cosmetic here.
  - `doc_credit_cards_silver_rewards_card_001: "Minimum credit score: $680"`
  - *Why it matters:* No change to the correct final state.
  - *Fix:* Change "$680" to "680".

*Verifier: Confirmed (Major → Major).* Reproduced all four card outcomes. Several cards beat 3.25% on travel and software and the doc gives no rule for picking one, so an agent that recommends Platinum is followed by the simulator and fails. That is two supported choices: Major. Not Blocker, because Silver is the closest category match with no fee and the simulator script favours it. The silver '$680' credit-score typo is cosmetic and should be a note.

### task_049 — Blocker

**Lying-customer closure flow whose gold needs the simulated customer to call a transfer-request tool, which nothing tells it to call.**

- **underspecified_instructions (Blocker)** — The gold includes one user-side request_human_agent_transfer call, which writes a human_transfer_requests record. The customer's instructions only say to ask aloud for a transfer. The simulator's guidelines tell it to call tools only when the agent requests it, and no document tells the agent to ask for that call. Whether the record exists is up to the user simulator, not the agent.
  - `gold[17]: requestor "user", name "request_human_agent_transfer", arguments {}`
  - `user_scenario.instructions step 9: "But I want to speak to a supervisor or someone else. ... Transfer me to a human agent." (no tool named)`
  - data/tau2/user_simulator/simulation_guidelines_tools.md: "Only call a tool if the agent has requested it or if it is necessary to answer a question the agent has asked."
  - `tools.py KnowledgeUserTools.request_human_agent_transfer writes record transfer_request_<n> to human_transfer_requests on every call`
  - `No document under documents/ mentions request_human_agent_transfer (grep)`
  - `Cross-task: task_034 and task_081 also require this call but their instructions name the tool; task_049 is the only one that does not`
  - *Why it matters:* Replay check: the gold without the user call does not match, and the gold with two user calls does not match either. A flawless agent passes only if the simulator spontaneously calls the tool exactly once, so the reward is chance.
  - *Fix:* Add to step 9: "Use your request_human_agent_transfer tool once to ask for the transfer." Or drop gold[17] so the transfer is graded only by the agent's no-op transfer_to_human_agents.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced. The record depends on whether the simulator happens to call the tool exactly once, with no documented way for the agent to cause it, so correct agent work passes only by chance: Blocker. The agent-side flow (close Green, refuse EcoCard, recognise the $50 checking shortfall, downgrade then $5 entry-tier credit) matches the gold.

### task_053 — Blocker

**CLI plus dispute task whose gold leaves out the customer's card-number lookup, yet the dispute needs that lookup's result, so a fully correct run can never match.**

- **argument_error (Blocker)** — The gold gives the customer the get_card_last_4_digits tool and files the dispute with card_last_4_digits "2791", but has no user-side call to that tool. The only way to learn "2791" is for the customer to call it, and that call writes a user_discoverable_tool_calls record the gold does not have.
  - `gold[13]: give_discoverable_user_tool {"discoverable_tool_name": "get_card_last_4_digits"}; gold has no call_discoverable_user_tool action`
  - `gold[15].arguments: "card_last_4_digits": "2791"`
  - user_scenario.instructions: "Card last 4 digits? 'I don't have my card in front of me right now ...' (If the agent provides you with the get_card_last_4_digits tool, use it to retrieve the number.)"
  - tools.py get_card_last_4_digits: self._log_user_tool_call(...) adds a record to user_discoverable_tool_calls, then derives last-4 from sha256("card_last4:<account_id>"), a value stored nowhere in the DB
  - `unlock_discoverable_agent_tool("get_card_last_4_digits") returns "Error: Unknown agent tool ... not available" (agent cannot look it up itself)`
  - `Cross-check: task_041's gold does include the user-side get_card_last_4_digits calls (041_4..041_7)`
  - *Why it matters:* Replay check: inserting the customer's call_discoverable_user_tool(get_card_last_4_digits, cc_e9d195fe8e_silver) into the gold changes the hash. A trajectory that gets the right last 4 digits always has that record and fails. One without it cannot know "2791" and files a different dispute record. No trajectory matches.
  - *Fix:* Add the user action {requestor: user, name: call_discoverable_user_tool, arguments: {discoverable_tool_name: get_card_last_4_digits, arguments: '{"credit_card_account_id": "cc_e9d195fe8e_silver"}'}} after gold[13], as task_041 does.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced. The only source of '2791' is the user tool, whose call writes a user_discoverable_tool_calls row the gold lacks, so no trajectory that obtains the digits matches. Blocker.

### task_056 — Major

**The product choices (Cobalt Blue checking, Silver Plus Saver savings) are unique, but the bank's own procedure tells the agent to open business savings with account_type 'savings', while the gold uses 'business_savings', which produces a different account.**

- **document_contradiction (Major)** — doc_(general)_004, the business-savings opening procedure, tells the agent to call open_bank_account_4821 with account_type 'savings'. The tool schema labels 'savings' as personal savings and offers 'business_savings', which is what gold uses. account_type is part of the deterministic account ID and is stored on the record.
  - `doc_bank_accounts_bank_accounts_(general)_004 (Agent Tool Instructions, open_bank_account_4821, How to call): "Set account_type to 'savings'."`
  - `open_bank_account_4821 docstring: "Must be one of: 'checking' (personal checking), 'savings' (personal savings), 'business_checking', 'business_savings'"`
  - `gold[5].arguments.arguments: "account_type": "business_savings", "account_class": "Silver Plus Saver Account"`
  - tools.py open_bank_account_4821: seed = f"account:{user_id}:{account_type}:{account_class}"; with 'savings' the personal-savings eligibility check passes (Green checking open since 09/10/2023), so the call succeeds with a different id
  - `replay: account_type='savings' plus the transfer to the resulting id gives a different DB hash than gold`
  - *Why it matters:* An agent that follows the internal procedure literally opens a 'savings' account with a different id and funds it. The call succeeds, so nothing signals a problem, but DB grading fails on correct, document-following work.
  - *Fix:* Change doc_(general)_004 to 'Set account_type to 'business_savings'.' (or have the tool reject account_class names containing 'Saver' under 'savings').

*Verifier: Confirmed (Major → Major).* Reproduced the doc_004 contradiction and the hash divergence. Product choices reproduce. The active November business-savings promotion (doc_(general)_015) ranks Gold Saver first, but Gold Saver documents no withdrawal allowance and only card-based APY bonuses (customer holds no business card), so it fails the multi-product bonus criterion; Silver Plus Saver stands.

### task_059 — Major

**Silver Rewards Card plus Green savings is the unique best combination for $5,000, but the gold's account name 'Green Account' is one of two plausible spellings the documents support, and the other one fails.**

- **document_contradiction (Major)** — Gold opens the savings account with account_class 'Green Account'. The KB calls this product 'Green Account (savings)' everywhere and shows the parenthetical form as an official class name ('Green Account (checking)'), while the savings procedure says the class must end with 'Account'. account_class is part of the deterministic account id.
  - `doc_bank_accounts_bank_accounts_(general)_002: "It must be the full official name ending with “Account” (for example, “Silver Plus Account”, “Gold Account”)."`
  - `doc_bank_accounts_bank_accounts_(general)_001: "must use the full official name ending with 'Account' (e.g., 'Blue Account', 'Green Account (checking)')"`
  - doc_savings_accounts_green_account_(savings)_001 title: "Green Account (savings) specifications and requirements"; doc_bank_accounts_bank_accounts_(general)_012: "Evergreen Account (checking) + Green Account (savings)"
  - `tools.py open_bank_account_4821: seed = f"account:{user_id}:{account_type}:{account_class}" (no normalization)`
  - `gold[5].arguments.arguments: "account_class": "Green Account"`
  - `replay with account_class 'Green Account (savings)' gives a different DB hash`
  - *Why it matters:* An agent that copies the product's official name, 'Green Account (savings)', by analogy with the 'Green Account (checking)' example opens an account with a different id and class string, and DB grading fails although the product choice is correct.
  - *Fix:* Normalize/validate account_class against a canonical product list in open_bank_account_4821, or state in doc_(general)_002 that the Green savings class string is exactly 'Green Account'.

*Verifier: Confirmed (Major → Major).* Reproduced the spelling ambiguity and both replays. The required read is justified by doc_(general)_009 ('essential for checking eligibility'). Major is right under the calibration rule for two document-supported readings.

### task_060 — Major

**Silver Plus is the unique savings fit and the open-savings-before-closing order is documented, but the gold closure leaves the free-text closure reason at a hidden default, so an agent that records a reason fails.**

- **non_determinism (Major)** — close_bank_account_7392 stores its optional free-text 'reason' argument in accounts[...].closure_reason. Gold omits it, so the record gets the hidden default 'Customer requested closure'. No document says which reason to pass or to leave it out, so an agent that records a sensible reason produces a different DB state.
  - `tools.py close_bank_account_7392 signature: reason: str = "Customer requested closure"; body: account["closure_reason"] = reason`
  - `unlock output: "reason: string (optional) - The reason for closing the account" (default value not shown)`
  - `doc_bank_accounts_bank_accounts_(general)_005: "3. Use close_bank_account_7392 to close the account." (no reason value anywhere in the KB)`
  - `gold[6].arguments.arguments: {"account_id": "58d57780cc15e32d"} (no reason)`
  - `replay: reason='Customer wants to consolidate checking accounts' gives a different hash; reason='Customer requested closure' gives the same hash`
  - *Why it matters:* Passing a reason (e.g. 'Customer wants to consolidate checking accounts') is a reasonable, even diligent, use of an offered parameter, but it fails DB grading. Only omitting the argument, or guessing the exact default string, matches gold.
  - *Fix:* Exclude closure_reason from the hashed state, or have the closure doc state the exact reason string and put it in the gold call.

*Verifier: Confirmed (Major → Major).* Ordering and product are derivable; the closure_reason divergence reproduces. 'Notice period: 3 days' in doc_005 is undefined and not modeled by any tool (note only).

*Reconciled across runs: Major → Major (scorer).* The only defect is close_bank_account_7392's optional free-text reason: the gold omits it, so closure_reason gets the hidden default 'Customer requested closure', and no document says what reason to record. Under upstream exact-hash grading, an agent that records a sensible reason fails (no documented default, so Major by calibration). The verified scorer strips closure_reason from every record and no replacement copies it here (bank accounts, not order_debit_card_5739), so the task is clean under that scorer; every other part of the task (product choice, ordering) is derivable in both runs.

### task_061 — Major

**The ordering and the $25 early-closure fee are documented and scripted, but the gold closure leaves the free-text closure reason at a hidden default, so an agent that records a reason fails.**

- **non_determinism (Major)** — close_bank_account_7392 stores its optional free-text 'reason' argument in accounts[...].closure_reason. Gold omits it, so the record gets the hidden default 'Customer requested closure'. No document says which reason to pass or to leave it out, so an agent that records a sensible reason produces a different DB state.
  - `tools.py close_bank_account_7392 signature: reason: str = "Customer requested closure"; body: account["closure_reason"] = reason`
  - `unlock output: "reason: string (optional) - The reason for closing the account" (default value not shown)`
  - `doc_bank_accounts_bank_accounts_(general)_005: "3. Use close_bank_account_7392 to close the account." (no reason value anywhere in the KB)`
  - `gold[8].arguments.arguments: {"account_id": "61d4e5f6a7b8c901"} (no reason)`
  - *Why it matters:* Passing a reason (e.g. 'Customer wants to consolidate checking accounts') is a reasonable, even diligent, use of an offered parameter, but it fails DB grading. Only omitting the argument, or guessing the exact default string, matches gold.
  - *Fix:* Exclude closure_reason from the hashed state, or have the closure doc state the exact reason string and put it in the gold call.

*Verifier: Confirmed (Major → Major).* Same closure_reason defect; the $25 fee path is scripted and replays. A failed first close attempt is hash-neutral (same tool-name record, no mutation).

*Reconciled across runs: Major → Major (scorer).* The only defect is close_bank_account_7392's optional free-text reason: the gold omits it, so closure_reason gets the hidden default 'Customer requested closure', and no document says what reason to record. Under upstream exact-hash grading, an agent that records a sensible reason fails (no documented default, so Major by calibration). The verified scorer strips closure_reason from every record and no replacement copies it here (bank accounts, not order_debit_card_5739), so the task is clean under that scorer; every other part of the task (product choice, ordering) is derivable in both runs.

### task_062 — Major

**The four-step reordering puzzle is fully documented and the products are unique, but both gold closures leave the free-text closure reason at a hidden default, so an agent that records a reason fails.**

- **non_determinism (Major)** — close_bank_account_7392 stores its optional free-text 'reason' argument in accounts[...].closure_reason. Gold omits it, so the record gets the hidden default 'Customer requested closure'. No document says which reason to pass or to leave it out, so an agent that records a sensible reason produces a different DB state.
  - `tools.py close_bank_account_7392 signature: reason: str = "Customer requested closure"; body: account["closure_reason"] = reason`
  - `unlock output: "reason: string (optional) - The reason for closing the account" (default value not shown)`
  - `doc_bank_accounts_bank_accounts_(general)_005: "3. Use close_bank_account_7392 to close the account." (no reason value anywhere in the KB)`
  - `gold[9] and gold[12] arguments: {"account_id": "61c9d8e7f6a5b432"} / {"account_id": "61a8b7c6d5e4f321"} (no reason)`
  - *Why it matters:* Passing a reason (e.g. 'Customer wants to consolidate checking accounts') is a reasonable, even diligent, use of an offered parameter, but it fails DB grading. Only omitting the argument, or guessing the exact default string, matches gold.
  - *Fix:* Exclude closure_reason from the hashed state, or have the closure doc state the exact reason string and put it in the gold call.

*Verifier: Confirmed (Major → Major).* Dependency chain (business checking needs no CLOSED accounts; savings needs a 14-day checking) and product choices reproduce. The November promotion (doc_013) does not apply because Sky Blue and Lime Green fail the customer's stated fee criteria.

*Reconciled across runs: Major → Major (scorer).* The only defect is close_bank_account_7392's optional free-text reason: the gold omits it, so closure_reason gets the hidden default 'Customer requested closure', and no document says what reason to record. Under upstream exact-hash grading, an agent that records a sensible reason fails (no documented default, so Major by calibration). The verified scorer strips closure_reason from every record and no replacement copies it here (bank accounts, not order_debit_card_5739), so the task is clean under that scorer; every other part of the task (product choice, ordering) is derivable in both runs.

### task_063 — Blocker

**Two credit cards raise the savings rate by exactly the same amount and both meet the customer's conditions, yet only one is accepted. The customer also asks for an $8,000 deposit that the gold never makes.**

- **non_determinism (Blocker)** — On Silver Plus, the best eligible savings account, the Bronze Rewards Card and Silver Rewards Card give the same +0.15% APY bonus, both have $0 annual fees, and both check credit at or below the customer's 700 score. Gold accepts only 'Silver Rewards Card', and card_type feeds the application id.
  - `doc_savings_accounts_silver_plus_account_009: "| Bronze Rewards Card | +0.15% |" and "| Silver Rewards Card | +0.15% |"`
  - doc_credit_cards_bronze_rewards_card_001: "Minimum credit score: $640", "Annual fee: $0.00"; doc_credit_cards_silver_rewards_card_001: "Minimum credit score: $680", "Annual fee: $0.00"
  - `gold[1].arguments.card_type = "Silver Rewards Card"`
  - tools.py apply_for_credit_card: application_id = generate_application_id(card_type, customer_name, annual_income, rho_bank_subscription); replay with 'Bronze Rewards Card' gives a different hash
  - Both cards earn 1.0% on non-category spend such as groceries and gas (silver_rewards_card_001 'Purchases outside top categories earn 1.0% back'; bronze 'You earn 1.0% cash back'), so even card rewards do not break the tie
  - *Why it matters:* The customer optimizes only savings interest: $8,000 x 3.15% = $252 with either card. An agent that recommends Bronze Rewards has done correct work and fails DB grading, so the outcome is a coin flip between equally valid answers.
  - *Fix:* Change one bonus in silver_plus_account_009 (e.g. Silver Rewards +0.2%), or give the customer a stated preference only Silver Rewards satisfies.
- **instruction_gold_mismatch (Major)** — The customer wants the savings account 'opened with my $8,000 deposit', and the KB requires the agent to offer to transfer the opening deposit. Gold makes no funding action, and the user script never says to decline. Her checking holds only $2,500.
  - `user_scenario step 7: "Great! Now let's get the savings account opened with my $8,000 deposit."; step 8: "the savings account open with my deposit"`
  - doc_bank_accounts_bank_accounts_(general)_002 step 5: "Ask the customer if they want you to transfer the opening deposit from their checking account now. If yes: use transfer_funds_between_bank_accounts_7291"
  - `db.json accounts.chk_tb58a3c9d2.current_holdings = "2500.00"; doc_savings_accounts_silver_plus_account_001: "Minimum opening deposit | $1,000"`
  - replay: an $8,000 transfer attempt (fails, insufficient funds), a $1,000 opening transfer, or giving deposit_check_3847 each change the DB hash (writes and give_discoverable_user_tool are logged even when the transfer errors)
  - *Why it matters:* A cooperative agent asks about funding, the simulated user, who wants the deposit made, says yes, and any transfer attempt or deposit-tool hand-off diverges from gold. In sibling tasks 058, 059 and 064, the user explicitly declines funding.
  - *Fix:* Script the user to say she will deposit the $8,000 herself later, matching tasks 058/059/064.
- **document_contradiction (Minor)** — Credit-score thresholds that the decision depends on are written as dollar amounts.
  - `doc_credit_cards_silver_rewards_card_001: "Minimum credit score: $680"`
  - `doc_credit_cards_platinum_rewards_card_*: "Minimum credit score required: $750."`
  - *Why it matters:* An agent can resolve it (700 vs 640/680/750), so the correct state does not change, but it adds noise on the deciding attribute.
  - *Fix:* Remove the '$' from credit-score fields.

*Verifier: Confirmed (Blocker → Blocker).* The Bronze/Silver Rewards tie at +0.15% with $0 fees reproduces, and nothing in the docs breaks it, so this is a calibration Blocker. The funding gap (Major) also stands. Unflagged reading: Gold Account's $10,000 is worded as a 'Minimum balance to maintain the account' with a '$10.00' fee if not met (gold_account_001), and Gold + Silver Rewards on $8,000 would net $456 - $120 = $336 > $252. gold_account_009 ('can affect your eligibility for the highest rate') makes exclusion the stronger reading, so I record it as a note.

### task_065 — Major

**Evergreen checking plus Green savings is the unique highest-APY pairing and the ordering is documented, but two free-text values in the gold (the 'Green Account' spelling and the default closure reason) are not uniquely derivable.**

- **document_contradiction (Major)** — Gold opens the savings account with account_class 'Green Account'. The KB calls this product 'Green Account (savings)' everywhere and shows the parenthetical form as an official class name ('Green Account (checking)'), while the savings procedure says the class must end with 'Account'. account_class is part of the deterministic account id.
  - `doc_bank_accounts_bank_accounts_(general)_002: "It must be the full official name ending with “Account” (for example, “Silver Plus Account”, “Gold Account”)."`
  - `doc_bank_accounts_bank_accounts_(general)_001: "must use the full official name ending with 'Account' (e.g., 'Blue Account', 'Green Account (checking)')"`
  - doc_savings_accounts_green_account_(savings)_001 title: "Green Account (savings) specifications and requirements"; doc_bank_accounts_bank_accounts_(general)_012: "Evergreen Account (checking) + Green Account (savings)"
  - `tools.py open_bank_account_4821: seed = f"account:{user_id}:{account_type}:{account_class}" (no normalization)`
  - `gold[2].arguments.arguments: "account_type": "savings", "account_class": "Green Account"`
  - `replay with 'Green Account (savings)' gives a different DB hash`
  - *Why it matters:* An agent that copies the product's official name, 'Green Account (savings)', by analogy with the 'Green Account (checking)' example opens an account with a different id and class string, and DB grading fails although the product choice is correct.
  - *Fix:* Normalize/validate account_class against a canonical product list in open_bank_account_4821, or state in doc_(general)_002 that the Green savings class string is exactly 'Green Account'.
- **non_determinism (Major)** — close_bank_account_7392 stores its optional free-text 'reason' argument in accounts[...].closure_reason. Gold omits it, so the record gets the hidden default 'Customer requested closure'. No document says which reason to pass or to leave it out, so an agent that records a sensible reason produces a different DB state.
  - `tools.py close_bank_account_7392 signature: reason: str = "Customer requested closure"; body: account["closure_reason"] = reason`
  - `unlock output: "reason: string (optional) - The reason for closing the account" (default value not shown)`
  - `doc_bank_accounts_bank_accounts_(general)_005: "3. Use close_bank_account_7392 to close the account." (no reason value anywhere in the KB)`
  - `gold[5].arguments.arguments: {"account_id": "chk_rp65a7b3c4"} (no reason)`
  - *Why it matters:* Passing a reason (e.g. 'Customer wants to consolidate checking accounts') is a reasonable, even diligent, use of an offered parameter, but it fails DB grading. Only omitting the argument, or guessing the exact default string, matches gold.
  - *Fix:* Exclude closure_reason from the hashed state, or have the closure doc state the exact reason string and put it in the gold call.

*Verifier: Confirmed (Major → Major).* Both Major defects (Green savings class spelling, closure_reason) reproduce, and the products are unique. Silver's '[[linked_checking_apy_bonus]]' placeholder (silver_account_002) is cosmetic here.

### task_066 — Major

**The right accounts are derivable, but the grade also depends on two free-text strings the documents do not fix: the closing reason, and how the Green savings account is named.**

- **non_determinism (Major)** — close_bank_account_7392 writes its free-text `reason` argument into the account record as `closure_reason`, and the gold closes the account without passing a reason, so only the tool default "Customer requested closure" matches. No document says what reason to record, or to leave it out.
  - `tools.py close_bank_account_7392: signature `reason: str = "Customer requested closure"`; on success `account["closure_reason"] = reason``
  - `gold[8].arguments.arguments = "{\"account_id\": \"chk_rp65a7b3c4\"}" (no reason)`
  - doc_bank_accounts_bank_accounts_(general)_005: "## Closure Procedure 1. Verify pre-closure requirements are met. 2. Determine the account tier and applicable fees/notice period. 3. Use close_bank_account_7392 to close the account." (no reason guidance)
  - `Replay in snapshot: gold with the close call given reason "Customer upgrading to a new checking account" -> agent DB hash != gold DB hash`
  - *Why it matters:* The customer gives an explicit reason (swapping the basic Light Blue for a better account), and the unlocked tool schema shows an optional `reason` parameter. An agent that records that reason closes the right account with the right fee handling but fails the exact DB-hash match.
  - *Fix:* Exclude `closure_reason` from the hashed state, or make the KB prescribe a fixed reason string (or remove the parameter) so the persisted value is derivable.
- **document_contradiction (Major)** — The persisted account_class string for the Green savings product is ambiguous. The savings procedure says names must end with 'Account', but the checking procedure's own example 'Green Account (checking)' and every KB reference to the product ('Green Account (savings)') use a parenthetical qualifier. The gold uses the bare 'Green Account'.
  - doc_bank_accounts_bank_accounts_(general)_002: "account_class must use the full official name ending with 'Account', e.g., 'Silver Plus Account', 'Gold Account'"
  - doc_bank_accounts_bank_accounts_(general)_001: "Personal checking account_class options must use the full official name ending with 'Account' (e.g., 'Blue Account', 'Green Account (checking)')"
  - doc_bank_accounts_bank_accounts_(general)_012: "3. Evergreen Account (checking) + Green Account (savings)"; doc titles e.g. "Green Account (savings) specifications and requirements"
  - `gold[4].arguments.arguments account_class = "Green Account"`
  - tools.py open_bank_account_4821: account_id = _deterministic_id(f"account:{user_id}:{account_type}:{account_class}"); account_class is stored verbatim and not validated
  - `Replay: account_class "Green Account (savings)" -> account_id 248a704a4fbe44b2 instead of 4ba63ba5b4a98c12 -> DB hash mismatch`
  - *Why it matters:* The KB's own example for the sibling product shows the parenthetical form as an acceptable official name. An agent that writes 'Green Account (savings)' opens the correct product but creates a different account record.
  - *Fix:* Make open_bank_account_4821 validate or canonicalize account_class against a fixed list. Alternatively, change doc_001's example to 'Green Account' and state the canonical savings string explicitly.
- **document_contradiction (Minor)** — One Green savings document contains corrupted arithmetic: it adds a 0.5% EcoCard bonus to the 4.0% base and gets 4.75%.
  - doc_savings_accounts_green_account_(savings)_009: "Example: 4.0% + 0.5% = 4.75% APY." and "Rate boost: 0.5% bonus APY on top of the base 4.0% rate (example total: 4.75%)"
  - `doc_savings_accounts_green_account_(savings)_003/_005: "you receive an additional bonus of 0.5%"`
  - *Why it matters:* It does not change the answer: even at +0.75%, EcoCard's $50 annual fee exceeds the extra interest on $6,000 ($45), and Silver Rewards (+0.45%, $0 fee) still wins. It is still a corrupted value on the exact product being chosen.
  - *Fix:* Change the example total to 4.5%.

*Verifier: Adjusted (Major → Major).* Task severity and both Major issues hold. The third issue (4.75% arithmetic) should be a note, not a Minor issue: per calibration a cosmetic slip is Minor only when it decides the answer. Here EcoCard loses on net either way (extra 0.05% or 0.30% on $6,000 is below its $50 fee), and on gross APY it wins either way, so the corrupted value never decides.

*Reconciled across runs: Major → Major (judgment).* The Green savings naming defect is real and scorer-independent: doc_002 requires a savings account_class 'ending with Account', but doc_001 gives 'Green Account (checking)' as an example of exactly such an official name and every savings doc titles the product 'Green Account (savings)', while the gold stores bare 'Green Account'. account_class seeds the account id, so the parenthetical form opens a different record, and the accounts table is compared exactly under both scorers. Both runs rate this same defect Major in tasks 059 and 065, so 066 takes the same Major; run U's additional closure_reason Major is upstream-only and does not change the severity.

### task_067 — Major

**The best account-and-card combination is clearly derivable, but the grade also depends on leaving the optional closing-reason text empty.**

- **non_determinism (Major)** — close_bank_account_7392 writes its free-text `reason` argument into the account record as `closure_reason`, and the gold closes the account without passing a reason, so only the tool default "Customer requested closure" matches. No document says what reason to record, or to leave it out.
  - `tools.py close_bank_account_7392: signature `reason: str = "Customer requested closure"`; on success `account["closure_reason"] = reason``
  - `gold[8].arguments.arguments = "{\"account_id\": \"chk_rp65a7b3c4\"}" (no reason)`
  - doc_bank_accounts_bank_accounts_(general)_005: "## Closure Procedure 1. Verify pre-closure requirements are met. 2. Determine the account tier and applicable fees/notice period. 3. Use close_bank_account_7392 to close the account." (no reason guidance)
  - `Replay in snapshot: gold with the close call given reason "Customer upgrading to a new checking account" -> agent DB hash != gold DB hash`
  - *Why it matters:* The customer gives an explicit reason (swapping the basic Light Blue for a better account), and the unlocked tool schema shows an optional `reason` parameter. An agent that records that reason closes the right account with the right fee handling but fails the exact DB-hash match.
  - *Fix:* Exclude `closure_reason` from the hashed state, or make the KB prescribe a fixed reason string (or remove the parameter) so the persisted value is derivable.

*Verifier: Confirmed (Major → Major).* 7.70% (net $7,500) reproduces as the unique pick on both gross and net readings. Diamond Elite (7.9% gross) is invitation-only and nets $7,405, and the customer script's fee-scrutiny step favors Platinum Rewards. Only the closure_reason defect remains.

*Reconciled across runs: Major → Major (scorer).* The only defect is close_bank_account_7392's optional free-text reason: the gold omits it, so closure_reason gets the hidden default 'Customer requested closure', and no document says what reason to record. Under upstream exact-hash grading, an agent that records a sensible reason fails (no documented default, so Major by calibration). The verified scorer strips closure_reason from every record and no replacement copies it here (bank accounts, not order_debit_card_5739), so the task is clean under that scorer; every other part of the task (product choice, ordering) is derivable in both runs.

### task_068 — Major

**The right products are derivable, but the knowledge base's own example spells the checking account's name differently from the gold, and the grade checks that name exactly.**

- **document_contradiction (Blocker)** — The procedure for opening personal checking accounts gives 'Green Account (checking)' as its example account_class, which is the exact product this task opens. The gold persists 'Green Account'. The open tool hashes and stores account_class verbatim, so following the document's example produces a different account record.
  - doc_bank_accounts_bank_accounts_(general)_001: "Personal checking account_class options must use the full official name ending with 'Account' (e.g., 'Blue Account', 'Green Account (checking)')."
  - `gold[3].arguments.arguments account_class = "Green Account"`
  - `tools.py open_bank_account_4821: seed = f"account:{user_id}:{account_type}:{account_class}"; no validation of account_class`
  - `Replay: account_class "Green Account (checking)" -> account_id 662d6d08711816cc (gold's differs) -> DB hash mismatch`
  - *Why it matters:* One sentence states both a rule ('ending with Account') and an example that breaks it for this very product. A careful agent that copies the documented example opens the right account and fails the task; whether it passes comes down to which half of that sentence it follows.
  - *Fix:* Change doc_001's example to 'Green Account', or validate and canonicalize account_class inside open_bank_account_4821.
- **non_determinism (Major)** — close_bank_account_7392 writes its free-text `reason` argument into the account record as `closure_reason`, and the gold closes the account without passing a reason, so only the tool default "Customer requested closure" matches. No document says what reason to record, or to leave it out.
  - `tools.py close_bank_account_7392: signature `reason: str = "Customer requested closure"`; on success `account["closure_reason"] = reason``
  - `gold[6].arguments.arguments = "{\"account_id\": \"chk_rp65a7b3c4\"}" (no reason)`
  - doc_bank_accounts_bank_accounts_(general)_005: "## Closure Procedure 1. Verify pre-closure requirements are met. 2. Determine the account tier and applicable fees/notice period. 3. Use close_bank_account_7392 to close the account." (no reason guidance)
  - `Replay in snapshot: gold with the close call given reason "Customer upgrading to a new checking account" -> agent DB hash != gold DB hash`
  - *Why it matters:* The customer gives an explicit reason (swapping the basic Light Blue for a better account), and the unlocked tool schema shows an optional `reason` parameter. An agent that records that reason closes the right account with the right fee handling but fails the exact DB-hash match.
  - *Fix:* Exclude `closure_reason` from the hashed state, or make the KB prescribe a fixed reason string (or remove the parameter) so the persisted value is derivable.

*Verifier: Adjusted (Blocker → Major).* The defect is real and reproduces. The gold still follows a document-supported reading, the literal rule 'ending with Account' (the same rule doc_002 states for savings), so calibration puts it at Major, the severity the review gave the identical class in 059/065/066. The explicit example makes the failure more likely than in the savings tasks, but that is a difference of probability, not of class. If the program treats the example as decisive, all four tasks should move to Blocker together. Products (Gold + Green checking + Silver Rewards = 6.45%) are unique under the customer's constraints.

### task_069 — Blocker

**The gold picks a 3.0% savings account on the claim that higher-rate accounts lack ATM-fee rebates, but the documents say the 5.5% Gold Account has them, so the correct answer differs from the gold.**

- **argument_error (Blocker)** — The gold opens a Silver Plus savings account (3.0% + 0.35% + 0.15% = 3.50%) on the premise that Gold and Silver savings have no ATM-fee rebates. The KB documents a $30/month rebate on Gold Account and $15/month on Silver Account. Gold Account at the customer's $10,000 earns 5.5% + 0.2% (Silver Rewards) = 5.70% and meets every stated requirement.
  - task_069 description.notes: "Needs ATM fee rebates on savings account - blocks Gold Account, Silver Account, Green Account (savings), Bronze Account" and "Gold Account has NO ATM rebates"
  - `doc_savings_accounts_gold_account_003: "ATM fee rebate cap per month: $30" and "Ongoing minimum balance: $10,000"`
  - `doc_savings_accounts_gold_account_001: "Your account earns an APY of 5.5%"`
  - `doc_savings_accounts_gold_account_014: "| Silver Rewards Card | +0.2% |"`
  - doc_savings_accounts_silver_account_005: "Do you rebate ATM fees? - Yes. You can receive ATM fee rebates up to 15 each month."; doc_savings_accounts_silver_account_003: "At least $10,000 | 4.0%"
  - `doc_savings_accounts_silver_plus_account_001: "Tier 1 APY: 3.0% for balances below the Tier 2 threshold" ($15,000)`
  - `gold[2].arguments.arguments account_class = "Silver Plus Account"`
  - `Replay: same trajectory with account_class "Gold Account" -> DB hash mismatch`
  - *Why it matters:* The customer asks for the highest APY that meets their requirements, and the task's own script expects the agent to propose Gold ("Wait, does the Gold Account have ATM fee rebates?"). An agent that checks the KB answers yes ($30/month), opens Gold Account (5.70%), and is scored 0. The agent that matches the gold has recommended an account that pays 2.2 points less.
  - *Fix:* Change the gold savings to 'Gold Account' (the checking stays Blue Account, since Green has no overdraft coverage and Purple's is undocumented, and the card stays Silver Rewards). Alternatively, give the customer a requirement Gold Account genuinely fails.
- **non_determinism (Major)** — close_bank_account_7392 writes its free-text `reason` argument into the account record as `closure_reason`, and the gold closes the account without passing a reason, so only the tool default "Customer requested closure" matches. No document says what reason to record, or to leave it out.
  - `tools.py close_bank_account_7392: signature `reason: str = "Customer requested closure"`; on success `account["closure_reason"] = reason``
  - `gold[6].arguments.arguments = "{\"account_id\": \"chk_rp65a7b3c4\"}" (no reason)`
  - doc_bank_accounts_bank_accounts_(general)_005: "## Closure Procedure 1. Verify pre-closure requirements are met. 2. Determine the account tier and applicable fees/notice period. 3. Use close_bank_account_7392 to close the account." (no reason guidance)
  - `Replay in snapshot: gold with the close call given reason "Customer upgrading to a new checking account" -> agent DB hash != gold DB hash`
  - *Why it matters:* The customer gives an explicit reason (swapping the basic Light Blue for a better account), and the unlocked tool schema shows an optional `reason` parameter. An agent that records that reason closes the right account with the right fee handling but fails the exact DB-hash match.
  - *Fix:* Exclude `closure_reason` from the hashed state, or make the KB prescribe a fixed reason string (or remove the parameter) so the persisted value is derivable.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced: Gold Account meets the ATM-rebate requirement and the $10,000 minimum, and Gold + Blue + Silver Rewards = 5.70% beats the gold's 3.50%. The gold follows no document-supported reading, so Blocker is correct. Blue remains the only checking with documented overdraft-protection transfers.

### task_070 — Major

**Picking Sky Blue through the active November promotion is derivable, but Sky Blue is a startup account and the customer's company age is never given.**

- **underspecified_instructions (Major)** — The gold account Sky Blue is a startup account, and its documents tell the agent to confirm the company is within 4 years of formation. The customer script (Yuki Nakamura / Brightwave Digital) never gives the company's formation date or age, so the outcome depends on whether the agent checks and on what the user simulator makes up.
  - `doc_business_checking_accounts_sky_blue_001: "## Verify Eligibility - Confirm your company is within 4 years of formation."`
  - `doc_business_checking_accounts_sky_blue_008: "Eligibility criteria tied to company age are evaluated when you open the account; the threshold is 4."`
  - `gold[4].arguments.arguments account_class = "Sky Blue"`
  - `user_scenario.instructions: no formation date or company age for the business`
  - *Why it matters:* A diligent agent asks the customer's company age before opening a startup account. If the simulated customer improvises an age over 4 years or says they don't know, the agent correctly falls back to Lime Green (second in the active promotion) and fails the gold. The gold is reached reliably only by skipping a documented eligibility check.
  - *Fix:* Add the business's formation date (under 4 years) to the user instructions, or replace the account's startup eligibility rule with one the given facts settle.

*Verifier: Confirmed (Major → Major).* The three qualifiers and the promotion logic reproduce. The customer's company age is never given, and the docs tell the agent to confirm it, so the outcome depends on simulator improvisation (Major).

*Reconciled across runs: Major → Major (judgment).* Sky Blue is a startup account whose documents state a company-age eligibility threshold of 4 years, and the customer script never gives Brightwave Digital's formation date, so an agent that performs the documented check gets an improvised answer that can move it to Lime Green. This is an unscripted customer fact with no documented default that decides the graded account_class, which calibration rates Major; the run V argument that the internal opening checklist omits the check does not remove the explicit 'Verify Eligibility' rule. The same Sky Blue issue is Major in run U's 071, so 070 takes Major under both scorers (accounts table compared exactly).

### task_071 — Major

**Both promotion-driven picks (Sky Blue checking, Gold Saver savings) are derivable, but the customer script never answers two things the documents tell the agent to ask: company age and whether to fund the new savings account now.**

- **underspecified_instructions (Major)** — The gold account Sky Blue is a startup account, and its documents tell the agent to confirm the company is within 4 years of formation. The customer script (Yumi Tanaka / Aurora Design Co) never gives the company's formation date or age, so the outcome depends on whether the agent checks and on what the user simulator makes up.
  - `doc_business_checking_accounts_sky_blue_001: "## Verify Eligibility - Confirm your company is within 4 years of formation."`
  - `doc_business_checking_accounts_sky_blue_008: "Eligibility criteria tied to company age are evaluated when you open the account; the threshold is 4."`
  - `gold[4].arguments.arguments account_class = "Sky Blue"`
  - `user_scenario.instructions: no formation date or company age for the business`
  - *Why it matters:* A diligent agent asks the customer's company age before opening a startup account. If the simulated customer improvises an age over 4 years or says they don't know, the agent correctly falls back to Lime Green (second in the active promotion) and fails the gold. The gold is reached reliably only by skipping a documented eligibility check.
  - *Fix:* Add the business's formation date (under 4 years) to the user instructions, or replace the account's startup eligibility rule with one the given facts settle.
- **underspecified_instructions (Major)** — The business-savings opening procedure requires the agent to ask whether to transfer the opening deposit from the business checking account now, and to call transfer_funds_between_bank_accounts_7291 if the customer says yes. The customer script never answers this question, and the gold contains no transfer.
  - doc_bank_accounts_bank_accounts_(general)_004: "5) Ask the customer if they would like you to transfer the opening deposit from their business checking account now. If yes, use transfer_funds_between_bank_accounts_7291 to transfer the required amount."
  - `db.json accounts[biz_chk_yt71c9e4f2].current_holdings = "12500.00" (funds available)`
  - `Gold Saver docs give no opening-deposit amount (doc_business_savings_accounts_gold_saver_account_001..009)`
  - `gold actions: no transfer_funds_between_bank_accounts_7291 call`
  - *Why it matters:* The customer wants to 'start building reserves' and has $12,500 in Cobalt Blue. A user simulator asked the required question may well say yes, and a correct agent then performs a transfer that changes both balances and fails the hash.
  - *Fix:* Add a line to the customer script (e.g. 'I'll fund the savings account myself later'), or include the transfer in the gold with a documented amount.

*Verifier: Upgraded (Major → Major).* Both reported Major issues hold. The review missed the doc_004 account_type contradiction it reported for task_056. This gold opens a business savings account through the same procedure, and following the doc's 'savings' instruction diverges (verified). Task severity stays Major, with a third Major issue added.

### task_072 — Major

**Both refund amounts can be rebuilt exactly from the documents, but they rely on fee rows dated after 'today' and on assuming the bank's own ATM fee gets rebated.**

- **non_determinism (Minor)** — The seeded transaction history includes 'posted' ATM fees dated after the fixed clock (2025-11-14 03:40), and the gold credit includes discrepancies on those future-dated rows. Including them, as the gold does, is the natural reading of 'review my November fees', but an agent that excludes transactions dated after today gets a different amount.
  - `utils.py get_now() = datetime(2025, 11, 14, 3, 40, 0); get_current_time returns "2025-11-14 03:40:00 EST"`
  - `db.json btxn_fcd7ef3a24ed (chk_lj82d4f1a9) date 11/20/2025 amount -2.5 "NON-RHO ATM FEE" status posted (gold counts $0.50 overcharge)`
  - db.json btxn_49c0c0b3b8c1 (chk_538bfb9cba) date 11/15/2025 amount -4.0 "FOREIGN ATM FEE - 2% OF WITHDRAWAL (MIN $3.00)" on a $200 withdrawal (gold counts $0.50 overcharge vs $3.50 tier 2)
  - `Excluding post-clock rows: Bluest $13.50 and Light Green $3.00 instead of gold $14.00 / $3.50`
  - *Why it matters:* Most agents take posted rows at face value and match the gold. A careful agent that notices the dates are in the future, or scopes the review to 'through today', credits a different amount and fails the exact-hash match.
  - *Fix:* Re-date the post-clock rows to on or before 11/14/2025, or move the fixed clock past the last seeded transaction.
- **document_contradiction (Minor)** — Bluest $14.00 includes a $2.00 'missing rebate' for the bank's own out-of-network fee on 11/14. One Bluest doc limits rebates to third-party ATM fees, another describes rebates of 'ATM fees' generally, and the seeded data rebates the bank's own $2.00 fee on every other withdrawal.
  - `doc_checking_accounts_bluest_account_003: "When you incur third-party ATM fees, you are rebated up to $50 per monthly statement cycle."`
  - `doc_checking_accounts_bluest_account_007: "You are eligible for ATM fee rebates up to $50 per month... If your aggregate ATM fees exceed $50"`
  - db.json chk_lj82d4f1a9: 11/02, 11/05, 11/10, 11/18 each have NON-RHO ATM FEE -2.00 followed by ATM FEE REBATE +2.00; 11/14 btxn_63306834d5ba -2.00 has no rebate
  - `gold[7] amount 14.00 = 8.00 + 3.50 + 2.00 + 0.50`
  - *Why it matters:* The data pattern and doc_007's general wording support crediting the $2.00, so most agents will match the gold. An agent reading doc_003 literally (the bank's fee is not a third-party fee) would credit $12.00.
  - *Fix:* State in the Bluest docs that the rebate covers Rho-Bank's own out-of-network fee.

*Reconciled across runs: Minor → Major (coverage).* Both gold credits include discrepancies on fee rows dated after the fixed clock (Bluest 11/20 +$0.50; Light Green 11/15 +$0.50), so an agent that scopes the review to 'through today' credits $13.50 and $3.00 and fails. Calibration fixes gold values that depend on post-clock data at Major; run U's 072 was never verified, and its reviewer's 'natural reading' rationale does not override the calibrated severity. The Bluest own-fee rebate reading (Minor) remains as a secondary issue. Scorer-independent.

### task_073 — Major

**All three refunds follow from the fee schedules and the documented 'net correction' rule. The one blemish is that some errors sit on fee rows dated after 'today'.**

- **non_determinism (Minor)** — The seeded transaction history includes 'posted' ATM fees dated after the fixed clock (2025-11-14 03:40), and the gold credit includes discrepancies on those future-dated rows. Including them, as the gold does, is the natural reading of 'review my November fees', but an agent that excludes transactions dated after today gets a different amount.
  - `utils.py get_now() = datetime(2025, 11, 14, 3, 40, 0); get_current_time returns "2025-11-14 03:40:00 EST"`
  - db.json btxn_kj18k9l0m1n3 and btxn_kj18k9l0m1n4 (chk_kj93a7b2e1_2) both 11/15/2025 -3.00 "NON-RHO ATM FEE" for one $250 withdrawal (gold counts the duplicate, +$3.00)
  - db.json btxn_kj28y9z0a1b3 (chk_kj93a7b2e1_3) 11/15/2025 -5.00 on a $150 foreign withdrawal (+$1.50); btxn_kj29c3d4e5f6 11/17/2025 $65 TD Bank withdrawal with no fee (7th domestic, -$1.50)
  - `Excluding post-clock rows: Green $6.00 instead of gold $9.00 (Blue and Light Green unchanged at $9.50 / $1.50)`
  - *Why it matters:* Most agents take posted rows at face value and match the gold. A careful agent that notices the dates are in the future, or scopes the review to 'through today', credits a different amount and fails the exact-hash match.
  - *Fix:* Re-date the post-clock rows to on or before 11/14/2025, or move the fixed clock past the last seeded transaction.

*Verifier: Upgraded (Minor → Major).* All three credits and doc_017's netting rule reproduce. The calibration file says gold values that depend on data dated after the fixed clock are Major, and the Green $9.00 depends on the 11/15 duplicate, so the task is Major, not Minor. The review's 'most agents take posted rows at face value' is the kind of likelihood argument the calibration overrides.

### task_074 — Major

**Three of the four v1.0.1 refunds (including the corrected Light Blue $14.50) rebuild exactly. The Purple $27.00 counts a 'missing rebate' on the bank's own fee that the Purple docs say is not rebatable, plus a fee dated after 'today'.**

- **document_contradiction (Major)** — The Purple $27.00 includes $2.50 for a 'missing rebate' on the 11/11 out-of-network fee. The Purple docs define the $30/month rebate as covering ATM operator surcharges, separate from Rho-Bank's own $2.50 fee, and list 'not coded as an ATM operator fee' as a legitimate reason for no rebate. The seeded data nevertheless rebates Rho's own $2.50 fee on the other withdrawals.
  - `doc_checking_accounts_purple_account_004: "You are eligible for refunds of ATM operator fees up to a monthly cap of $30."`
  - doc_checking_accounts_purple_account_012: "You are charged $2.50 per cash withdrawal made at an out-of-network ATM... This fee is separate from any surcharge the ATM owner/operator may charge"
  - `doc_checking_accounts_purple_account_010: "Common reasons... The charge was not coded as an ATM operator fee by the merchant or network."`
  - db.json chk_ar72c5d8e3_1: 11/05, 11/06, 11/12, 11/15, 11/16 NON-RHO ATM FEE -2.50 each followed by ATM FEE REBATE +2.50; 11/11 btxn_ar_purple_11f -3.50 with no rebate
  - gold[9] amount 27.00 = 2.50 (Rho ATM fee) + 8.00 + 10.50 (foreign fees, Purple foreign = $0.00) + 1.00 (3.50 vs 2.50) + 2.50 (missing rebate) + 2.50 (11/15 duplicate)
  - `Replay: Purple credit 24.50 -> DB hash mismatch`
  - *Why it matters:* A doc-faithful agent corrects the $1.00 overcharge but owes no rebate on a bank fee, and credits $24.50. An agent following the data pattern credits $27.00. Both readings are defensible, and only one passes.
  - *Fix:* Make the Purple docs say the monthly rebate covers Rho-Bank's own out-of-network fee (matching the data), or drop the missing-rebate component from the gold (and from the seeded rebate rows).
- **non_determinism (Minor)** — The seeded transaction history includes 'posted' ATM fees dated after the fixed clock (2025-11-14 03:40), and the gold credit includes discrepancies on those future-dated rows. Including them, as the gold does, is the natural reading of 'review my November fees', but an agent that excludes transactions dated after today gets a different amount.
  - `utils.py get_now() = datetime(2025, 11, 14, 3, 40, 0); get_current_time returns "2025-11-14 03:40:00 EST"`
  - `db.json btxn_ar_purple_15f_dup (chk_ar72c5d8e3_1) 11/15/2025 -2.50 "NON-RHO ATM FEE" duplicate (gold counts +$2.50)`
  - Excluding post-clock rows: Purple $24.50 (or $22.00 combined with the doc-literal rebate reading); Light Blue, Dark Green and Evergreen errors all fall on or before 11/14 and are unaffected
  - *Why it matters:* Most agents take posted rows at face value and match the gold. A careful agent that notices the dates are in the future, or scopes the review to 'through today', credits a different amount and fails the exact-hash match.
  - *Fix:* Re-date the post-clock rows to on or before 11/14/2025, or move the fixed clock past the last seeded transaction.
- **answer_leak (Minor)** — v1.0.1 removed the answer annotations from the fee descriptions, but the agent-visible transaction IDs still flag some errors with an '_err' or '_dup' suffix. The flags follow the old answer key: on Light Blue only the first of the two free withdrawals of each kind is marked.
  - `tools.py get_bank_account_transactions_9173 prints "Record ID: {record_id}" and every field, including transaction_id`
  - db.json ids: btxn_ar_purple_03f_err, btxn_ar_purple_07f_err, btxn_ar_purple_09f_err, btxn_ar_purple_15f_dup, btxn_ar_lb_03f_err, btxn_ar_lb_05f_err, btxn_ar_lb_08f_err, btxn_ar_dg_02f_err, btxn_ar_ev_03f_err
  - `btxn_ar_lb_06f (11/06, 2nd free domestic) and btxn_ar_lb_09f (11/09, 2nd free foreign) are not marked, yet the v1.0.1 gold ($14.50) treats both as errors`
  - *Why it matters:* The suffixes hint at the answer on 9 of 22 errors, which weakens the task as a test. On Light Blue they point toward the superseded $8.00 refund, so an agent that trusts them over the docs is steered wrong.
  - *Fix:* Rename the seeded transaction IDs to neutral values, as done for the descriptions.

*Verifier: Adjusted (Major → Major).* Light Blue 14.50, Dark Green 4.75 and Evergreen 3.70 reproduce, and so does Purple 27.00 under the data-pattern reading. Two corrections. (1) The post-clock sub-issue (Purple 15f_dup) should be Major per calibration, not Minor; task severity is unchanged. (2) There is a third Purple path the review missed: an agent that accepts the missing-rebate reading but follows doc_017's credit-type rule splits Purple into fee_refund 24.50 + rebate_credit 2.50, which also fails. This strengthens the Major.

### task_075 — Major

**The customer wants the account with the lowest foreign-ATM fees, but by the documents Purple and Bluest also charge $0 abroad (Purple adds operator-fee rebates), so Green Fee-Free is not the unique answer.**

- **non_determinism (Blocker)** — The gold rests on an undocumented premise: that a foreign ATM withdrawal incurs both the out-of-network fee and the foreign fee, which gives Purple $45 and Bluest $36. The docs say Purple and Bluest charge no Rho-Bank fee on foreign ATM withdrawals, which ties them with Green Fee-Free at $0. Purple also rebates up to $30/month of operator surcharges (Bluest up to $50), which Green Fee-Free does not.
  - task_075 description.notes: "When using a foreign ATM that is not in Rho-Bank's network, BOTH the out-of-network ATM fee AND the foreign ATM withdrawal fee apply" (no KB document states this)
  - `doc_checking_accounts_bluest_account_003: "Withdraw from ATMs abroad with no Rho-Bank fee: $0.00. Third-party ATM operator fees may still apply."`
  - doc_checking_accounts_purple_account_001: "No foreign ATM withdrawal fees: $0.00 per withdrawal (third-party ATM operator fees may still apply)"; "Global ATM fee rebates | Up to $30 per month"
  - doc_checking_accounts_green_fee-free_account_005: "Foreign ATM withdrawals are also fee-free: $0.00 per withdrawal. Third-party ATM operator fees may still apply."
  - Benchmark's own data contradicts the premise: task_074 seed rows for Purple foreign withdrawals (e.g. btxn_ar_purple_08 HSBC Hong Kong, btxn_ar_purple_10 UOB Singapore) carry no fee, and the gold treats them as correct; Light Blue/Evergreen foreign withdrawals carry only the foreign fee
  - `gold[2].arguments.arguments account_class = "Green Fee-Free Account"`
  - *Why it matters:* By the documents, Green Fee-Free, Purple and Bluest all cost $0 in Rho-Bank fees for 18 withdrawals of $350 abroad. No tie-breaker is given. If operator surcharges count as ATM fees, Purple (no deposit barrier) is strictly better. An agent that opens Purple has a defensible or better answer and fails the DB match.
  - *Fix:* Document that out-of-network fees also apply to foreign ATMs for Purple and Bluest (and align task_074's seed data with that), or give the customer a constraint that uniquely selects Green Fee-Free. Otherwise, accept any of the $0-fee accounts.
- **underspecified_instructions (Major)** — Bluest is ruled out only by its $75,000 minimum opening deposit, and the customer's available funds are never stated.
  - `doc_checking_accounts_bluest_account_001: "| Minimum opening deposit | $75,000 |"`
  - `tools.py open_bank_account_4821 does not check any opening deposit`
  - `user_scenario.instructions: no balance or deposit capacity given`
  - *Why it matters:* Bluest has $0 Rho-Bank fees abroad and a $50/month rebate cap. Whether the agent may recommend it depends on what the simulator improvises when asked about the deposit.
  - *Fix:* State the customer's deposit capacity in the instructions.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced the tie: Purple, Bluest and Green Fee-Free all cost $0 in Rho-Bank fees abroad by the documents, and no tie-breaker exists. If the customer's 'ATM fees' includes operator surcharges, Purple's rebate makes it strictly better than the gold. Even under the notes' 'both fees apply' premise, purple_012's $2.50 would be covered by the $30 rebate, if task_074's data reflects the rebate scope. Blocker stands.

*Reconciled across runs: Blocker → Major (fact_error).* Fact: no personal-checking document states that the out-of-network and foreign ATM fees stack; only business-checking docs do (hunter_green_010, navy_blue_009), and hunter_green_009 treats seeing both as a reason for review. But purple_account_012 defines Purple's $2.50 fee by network membership with no domestic limit, and the customer says the ATMs abroad are out of network, so the gold's reading (Purple 18 x $2.50 = $45, Green Fee-Free uniquely $0 on both fees) is document-supported; run U's 'no KB document states this' overlooked those texts. The no-stacking reading (Purple and Bluest $0 abroad, with Purple's operator-fee rebates) leads to Purple or a tie, so this is two supported readings with different graded states: Major, not Blocker, under both scorers (accounts compared exactly).

### task_076 — Major

**Purple is a sound pick, but Bluest also gives 2-day early deposit and $0 fees abroad with a larger rebate. It is ruled out only by a $75,000 opening deposit the customer is never asked about.**

- **underspecified_instructions (Major)** — Among accounts with 2-day early direct deposit, Bluest matches or beats Purple on ATM fees abroad ($0 Rho-Bank fee, $50/month rebate cap against $30). Only its $75,000 minimum opening deposit and $112,500 balance rule it out, and the customer's ability to fund it is never stated.
  - `doc_checking_accounts_bluest_account_001: "| Minimum opening deposit | $75,000 |", "| Early direct deposit | 2 day(s) before payday |"`
  - `doc_checking_accounts_bluest_account_003: "Withdraw from ATMs abroad with no Rho-Bank fee: $0.00"; "rebated up to $50 per monthly statement cycle"`
  - doc_checking_accounts_purple_account_001: "No foreign ATM withdrawal fees: $0.00 per withdrawal"; "Early direct deposit | 2 days early"; "Global ATM fee rebates | Up to $30 per month"
  - `task_076 description.notes: Bluest "requires $50k-100k minimum deposit - NOT PRACTICAL" (not derivable from the customer script)`
  - `gold[2].arguments.arguments account_class = "Purple Account"`
  - *Why it matters:* An agent that asks about the deposit gets whatever the simulator improvises. An agent that doesn't ask can reasonably choose Bluest for its larger rebate. Either path can end on Bluest and fail the DB match.
  - *Fix:* Add the customer's deposit capacity (well below $75,000) to the instructions.

*Verifier: Confirmed (Major → Major).* Purple is the answer once Bluest is excluded, and only the never-stated deposit capacity excludes Bluest, so the outcome rests on the simulator. Major is consistent with the same defect in 070/071 and the second 075 issue.

### task_077 — Major

**The lost-wallet sequence is fully documented, but the gold's choice of the PREMIUM card design depends on reading a vague 'best free option' as metallic rather than classic.**

- **non_determinism (Major)** — order_debit_card_5739 requires a card_design and stores it on both the order and the new card. For the ELITE tier, CLASSIC, PREMIUM and CUSTOM are all $0. The customer states a preference only if asked, and then says 'whatever the best option is that's free... I don't want to pay extra for shipping or a fancy card design', which does not pick between CLASSIC and PREMIUM. The gold requires PREMIUM.
  - doc_bank_accounts_bank_accounts_(general)_029: "ELITE TIER: - CLASSIC design: design_fee $0 - PREMIUM design (metallic silver): design_fee $0 (complimentary) - CUSTOM design (uploaded image): design_fee $0 (complimentary)"
  - user_scenario.instructions step 8: "ONLY IF agent asks about shipping speed or card design options: 'I'd like whatever the best option is that's free with my account. I don't want to pay extra for shipping or a fancy card design.'"
  - `gold[22].arguments.arguments: "delivery_option": "RUSH", "card_design": "PREMIUM"`
  - `tools.py order_debit_card_5739 stores card_design in debit_card_orders and debit_cards records`
  - `Replay: identical trajectory with card_design CLASSIC -> DB hash mismatch`
  - *Why it matters:* An agent that defaults to CLASSIC without asking, or reads 'I don't want ... a fancy card design' as wanting a plain card, does everything else right (freeze, credit-card replacement, unfreeze, close, RUSH order, correct activation tool) and still fails.
  - *Fix:* Have the customer name the design explicitly (e.g. 'the metallic premium design, since it's free'), or exclude card_design from the hashed state.

*Verifier: Confirmed (Major → Major).* Reproduced the gold replay (no errors, new card dbc_8eed7b16caeb) and the CLASSIC divergence. The 'fancy card design' clause gives a second reading against the gold's PREMIUM; Major per calibration (two readings). Freeze/unfreeze/close sequence is enforced by the tool, as stated.

### task_079 — Major

**The gold requires freezing three stolen cards and then unfreezing them before closing, but the policy says to recommend closing instead of freezing once a theft is confirmed, and skipping the freeze changes the graded state.**

- **non_determinism (Major)** — The customer opens by saying the wallet was stolen an hour ago. Doc_..._026 tells the agent to recommend closing rather than freezing for a confirmed lost or stolen card. The gold instead freezes all three cards, unfreezes them, and then closes them. The freeze and unfreeze leave timestamps and tool-log rows that a direct-close path never writes.
  - `user_scenario step 1: "Hi, my wallet was stolen about an hour ago and I need to freeze all my debit cards immediately."`
  - `doc_bank_accounts_bank_accounts_(general)_026: "CLOSE: Permanent deactivation - cannot be reversed. Use when card is confirmed lost/stolen"`
  - `doc_bank_accounts_bank_accounts_(general)_026: "If customer confirms the card is lost/stolen, recommend closing instead of freezing"`
  - gold[4..6] freeze_debit_card_3892 on dbc_cr89a2b3c4_ev/_lb/_green; gold[13..15] unfreeze_debit_card_3893 on the same cards; gold[17..19] close_debit_card_4721 reason 'stolen'
  - Replay (snapshot env): gold minus the freeze/unfreeze calls -> agent/user hash mismatch; diff = frozen_date and unfrozen_date '11/14/2025' on all three cards plus agent_discoverable_tools rows for freeze_debit_card_3892 and unfreeze_debit_card_3893
  - *Why it matters:* An agent that follows doc_..._026 and closes the stolen cards directly ends in the same business state (three closed cards, Evergreen and Green reordered, Light Blue waiting 48 hours) but fails the exact DB hash. Only the agent that follows the customer's literal freeze request passes.
  - *Fix:* Have the customer ask to cancel the cards rather than freeze them, and drop gold[3..6] and gold[12..15]. Alternatively, keep the freeze-first story but make the opening uncertain ('I think my wallet may have been stolen') so freezing is the policy-preferred first step.

*Verifier: Confirmed (Major → Major).* Reproduced the freeze-first vs direct-close divergence. The customer explicitly asks to freeze while doc_026 recommends closing, so both paths are document-supported and only one passes; Major holds. Tier and refund-waiver reasoning checked against doc_005/025/029.

*Reconciled across runs: Major → Major (judgment).* Same path-dependence as 078, but here the theft is confirmed in the opening line, which is exactly when doc_026 says to recommend closing instead of freezing; the script does not cover that branch and follows the agent's guidance. Following the customer's literal freeze request and following doc_026 are both document-supported, and they produce different graded debit_cards rows: Major by calibration. That stated difference (theft confirmed up front) is why 079 is rated above 078. The pending-refund req 4 vs req 5 overlap is a resolvable Minor.

### task_082 — Blocker

**The gold records a close-and-reissue for the online fraud on the Green Fee-Free card, and the customer asks for a reissue, but the gold never closes that card, so an agent that follows the policy fails.**

- **instruction_gold_mismatch (Blocker)** — Two cards each get a card_present_fraud or card_not_present_fraud dispute mapped to close_and_reissue. The gold carries out that action for the Blue card only and leaves dbc_mc47a2b9e1_gff ACTIVE.
  - `gold[15].arguments: btxn_d74e8a798f95, card_id dbc_mc47a2b9e1_gff, "dispute_category": "card_not_present_fraud", "card_action": "close_and_reissue"`
  - doc_bank_accounts_bank_accounts_(general)_031: "This parameter records metadata only; the agent must separately perform the indicated card action after filing the dispute." and "use the MOST SEVERE action across all disputes"
  - `user_scenario step 7: "Green Fee-Free card: I'd like to keep using this card but maybe with a new number? Can you reissue it?"`
  - `gold[17] close_debit_card_4721 and gold[19] order_debit_card_5739 target only dbc_mc47a2b9e1_blue / chk_mc47a2b9e1_blue`
  - Replay: gold + close_debit_card_4721(dbc_mc47a2b9e1_gff, fraud_suspected) succeeds (card ACTIVE, no pending txns) and the hash no longer matches (status/closed_date/closure_reason on dbc_mc47a2b9e1_gff)
  - *Why it matters:* Closing the GFF card is what both the policy and the customer call for. Doing it writes CLOSED/closed_date/closure_reason on dbc_mc47a2b9e1_gff, which the gold DB lacks, so correct work scores 0.
  - *Fix:* Add close_debit_card_4721(card_id='dbc_mc47a2b9e1_gff', reason='fraud_suspected') to the gold. GFF is ENTRY tier (doc_..._005), so doc_..._029's 48-hour wait means no reorder today; tell the user simulator to accept that.
- **argument_error (Major)** — The gold marks the FitLife recurring_charge_after_cancellation dispute provisional_credit_eligible=true, although doc_..._032 lists that category as not required. Tasks 083-086 set every other discretionary category to false.
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is NOT REQUIRED (but may be offered at discretion) when: 1. The dispute category is: ... 'recurring_charge_after_cancellation'"
  - `gold[13].arguments: "dispute_category": "recurring_charge_after_cancellation", "provisional_credit_eligible": true`
  - task_083 gold[7] goods_services_not_received -> false; task_084 gold[13] incorrect_amount -> false; task_085 gold[12] recurring_charge_after_cancellation -> false
  - *Why it matters:* The flag is stored as provisional_credit_eligible/issued/amount in debit_card_disputes. An agent that applies the guidelines the way the sibling tasks do writes false and fails.
  - *Fix:* Set gold[13] provisional_credit_eligible to false to match doc_032 and tasks 083-086.
- **non_determinism (Major)** — Several dispute fields for the lost Blue card have more than one defensible value. The PIN was written on a note in the lost wallet, which is neither 'shared with someone' nor clearly 'observed'. FitLife's card_in_possession=true reflects possession at charge time, while doc_031's question is in the present tense and the card is now lost. The gold's choices on these fields also decide the ElectroniX provisional-credit flag.
  - `doc_..._031: "'yes_shared': Customer shared PIN with someone"; "'yes_observed': Customer believes PIN was observed/skimmed"; "'unknown': Customer unsure"`
  - `user_scenario: "I had my PIN written on a sticky note in my wallet. So whoever has the card probably has the PIN too."`
  - `gold[12]: "pin_compromised": "yes_shared", "provisional_credit_eligible": false (doc_032 NOT REQUIRED item 3 keys on yes_shared)`
  - doc_..._031: "card_in_possession (boolean) - Ask: \"Do you still have your physical debit card in your possession?\""; gold[13] FitLife "card_in_possession": true while gold[12] (same card) is false
  - *Why it matters:* Choosing 'unknown' or 'yes_observed' for ElectroniX, which also makes provisional credit required, or card_in_possession=false for FitLife, gives different stored dispute records and fails the hash.
  - *Fix:* Have the customer say outright that they shared the PIN, or change the gold to 'unknown'. Make FitLife's card_in_possession false, or have the customer state possession explicitly in the present tense.
- **non_determinism (Major)** — Closing the lost Blue card that was used fraudulently can be recorded as 'lost' or 'fraud_suspected'. The choice also sets the new card's issue_reason ('lost' vs 'fraud'). The Blue replacement's shipping and design are never specified for the customer, while MID tier offers expedited for $15.
  - `gold[17]: close_debit_card_4721 reason "lost"; the close_and_reissue action comes from gold[12] dispute_category card_present_fraud`
  - `doc_..._025 lists 'lost' and 'fraud_suspected' as separate reasons with no precedence rule`
  - `order_debit_card_5739 maps closure_reason 'fraud_suspected' -> issue_reason 'fraud', 'lost' -> 'lost'`
  - doc_..._029 MID TIER: "Standard (delivery_fee: $0) or expedited shipping available (delivery_fee: $15)"; the user_scenario has no shipping or design preference; gold[19] STANDARD/CLASSIC
  - *Why it matters:* A 'fraud_suspected' closure, or an EXPEDITED order improvised by the user simulator, changes debit_cards and debit_card_orders, so the result depends on reasoning or simulator choices the materials do not fix.
  - *Fix:* Script the customer's shipping and design choice (e.g. 'standard, classic is fine'), and state in doc_025 which reason to use when a lost card was used fraudulently.
- **document_gap (Major)** — customer_max_liability_amount is 50 for every dispute, but the docs anchor the tiers to an unknown statement date and give no rule for non-fraud categories. A business-day count from the customer's stated discovery dates puts FitLife and the ATM dispute in the $500 tier.
  - `doc_..._031: "Reported within 2 business days of statement: Maximum liability $50 / Reported within 60 days of statement: Maximum liability $500"`
  - `Discovery dates: FitLife 11/11/2025 (Tue, Veterans Day), ATM 11/09/2025 (Sun); filing date 11/14/2025 (Fri) -> 3 and 4 business days`
  - `gold[13] and gold[14]: "customer_max_liability_amount": 50`
  - `tool docstring: "based on Regulation E reporting timing rules and the disputed amount"`
  - *Why it matters:* The value is stored in debit_card_disputes. An agent that counts business days from discovery writes 89.99 / 100 (min of $500 and the amount) instead of 50 and fails.
  - *Fix:* Document one liability rule: the anchor date, whether it applies to non-fraud categories, and whether it is capped at the disputed amount. Then regenerate all 082-088 liability values from that rule.
- **argument_error (Minor)** — The CryptoGems discovery date in the script is 'today, January 9th', which contradicts 'today' = 11/14/2025 and the gold.
  - `user_scenario step 8: "I discovered this one today, January 9th."`
  - `gold[15]: "discovery_date": "11/14/2025"`
  - *Why it matters:* An agent can resolve this from the fixed clock, but a literal agent might record 01/09.
  - *Fix:* Change the script to 'today, November 14th'.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced the missing GFF closure: the doc mandates performing close_and_reissue and the customer asks for a reissue, so the gold follows no supported reading; Blocker stands. The secondary Major issues (discretionary FitLife credit, pin_compromised for a PIN on a sticky note, lost vs fraud_suspected, unscripted shipping/design, liability anchor) all reproduce as hash-changing.

### task_083 — Blocker

**This task is graded by exact text match on the dispute-call arguments, but the official answer leaves out a field the tool requires and spells numbers as no tool call would, so no agent can match it.**

- **grading_basis_mismatch (Blocker)** — reward_basis is ACTION with compare_args unset, so each call_discoverable_agent_tool's 'arguments' JSON string must equal the gold string exactly. The four gold dispute strings omit the required customer_max_liability_amount and write numbers as 150.00 / 189.50 / 475.00, so no valid agent call can equal them.
  - `evaluation_criteria.reward_basis = ["ACTION"]; gold[6..9] compare_args = null`
  - Action.compare_with_tool_call: "if self.compare_args is None: compare_args = tool_call.arguments.keys()" ... "return tool_args == action_args" (string equality on 'arguments')
  - file_debit_card_transaction_dispute_6281 signature: "customer_max_liability_amount: float," (no default); omitting it raises TypeError -> "Error: Invalid arguments"
  - `gold[6].arguments: "...\"disputed_amount\": 150.00, ... \"card_action\": \"keep_active\"}" (no customer_max_liability_amount)`
  - *Why it matters:* A correct agent has to send customer_max_liability_amount, which makes its string differ from the gold. Even an agent that omits it would need the gold's exact key order and the non-canonical '150.00' spelling that json.dumps never emits. The action reward is therefore 0 for every trajectory.
  - *Fix:* Switch the task to DB grading with gold values that include customer_max_liability_amount, or set compare_args=['agent_tool_name'] on the dispute actions and check the content through the DB.

*Verifier: Confirmed (Blocker → Blocker).* Confirmed that ACTION grading compares the inner JSON string verbatim and that the gold strings omit a required argument, so a working agent call can never equal them. Blocker stands.

### task_084 — Blocker

**The duplicate-charge pick is now resolvable, but the gold caps one dispute's maximum liability at the disputed amount and not another's, so no single consistent rule reproduces the official answer.**

- **argument_error (Blocker)** — customer_max_liability_amount is internally inconsistent. The $47.50 duplicate gets 50 (not capped at the amount), while the $412.88 late-reported fraud gets 412.88 (capped at the amount). The tool says the value depends on the timing rules and the disputed amount.
  - file_debit_card_transaction_dispute_6281 docstring: "customer_max_liability_amount (number): The maximum dollar amount the customer could be liable for based on Regulation E reporting timing rules and the disputed amount. Use -1 for unlimited liability."
  - `gold[12].arguments: duplicate_charge "disputed_amount": 47.5, "customer_max_liability_amount": 50`
  - `gold[14].arguments: card_present_fraud "disputed_amount": 412.88, "customer_max_liability_amount": 412.88`
  - `Computation: rule min(tier, amount) -> duplicate 47.5 (gold 50); rule tier-only -> TechWorld 500 (gold 412.88)`
  - *Why it matters:* The value is stored in debit_card_disputes. Any agent applying one rule to both disputes mismatches one of them, so correct reasoning cannot reach the gold hash.
  - *Fix:* Pick one rule (e.g. min(timing tier, disputed_amount)), state it in doc_..._031, and set gold[12] to 47.5 (or gold[14] to 500 under a tier-only rule).
- **document_contradiction (Major)** — The duplicate charge is in doc_032's 'required' category list, but the customer has not contacted the merchant. Doc_032 also lists that, for non-fraud disputes, as a 'not required' condition. The gold sets eligible=true.
  - `doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is REQUIRED when ALL of these conditions are met: ... 'duplicate_charge'"`
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is NOT REQUIRED (but may be offered at discretion) when: ... 2. Customer has not contacted merchant first (for non-fraud disputes)"
  - `gold[12].arguments: "contacted_merchant": false, "provisional_credit_eligible": true`
  - *Why it matters:* An agent that applies the not-required clause, as tasks 083-086 do for other discretionary cases, writes false and fails the hash.
  - *Fix:* State in doc_032 that duplicate_charge (like ATM errors) does not need merchant contact, or set gold[12] to false.
- **document_gap (Major)** — The liability timing tier is anchored to an undisclosed statement date. The duplicate was noticed 11/10 and the incorrect amount 11/09, both reported 11/14, which is more than 2 business days, yet the gold uses the $50 tier for both.
  - `doc_..._031: "Reported within 2 business days of statement: Maximum liability $50"`
  - `user_scenario: duplicate "I noticed it on November 10th"; incorrect amount "I noticed it November 9th"`
  - `gold[12], gold[13]: "customer_max_liability_amount": 50`
  - *Why it matters:* Counting business days from discovery gives the $500 tier, so the stored values become 47.5/100 under a cap or 500 without one, and the hash fails.
  - *Fix:* Define the anchor (discovery date vs. statement date) and whether non-fraud categories carry Reg E liability at all.

*Verifier: Confirmed (Blocker → Blocker).* No single liability rule reproduces both gold values, so a consistent agent fails one dispute row; Blocker stands. The duplicate-tie fix (#403) holds. The discretionary-credit and liability-anchor Majors also reproduce.

### task_085 — Major

**Verifying the customer's claims against the transaction history works, but the gold's liability amounts and provisional-credit flag for the duplicate charge rest on readings the documents do not settle.**

- **non_determinism (Major)** — customer_max_liability_amount is 50 for all three disputes, including the $14.99 subscription charge, so the gold does not cap at the disputed amount, while task_084's gold does cap. Counting business days from the stated discovery dates also puts the ATM and duplicate disputes in the $500 tier.
  - `tool docstring: "based on Regulation E reporting timing rules and the disputed amount"`
  - `gold[12].arguments: "disputed_amount": 14.99, "customer_max_liability_amount": 50`
  - `task_084 gold[14]: disputed 412.88 -> liability 412.88 (capped)`
  - `Discovery: ATM 11/05/2025 (7 business days before 11/14), duplicate 11/08/2025 (4 business days incl. 11/11 holiday); gold[9], gold[10] liability 50`
  - *Why it matters:* An agent that applies the cap the docstring implies writes 14.99, and one that counts business days writes 100/89.99. Both differ from the hashed gold record.
  - *Fix:* Document a single liability formula (anchor date, cap, applicability to non-fraud categories) and regenerate gold[9], gold[10], gold[12].
- **document_contradiction (Major)** — The duplicate-charge dispute has contacted_merchant=false but provisional_credit_eligible=true, although doc_032's not-required list includes non-fraud disputes where the merchant was not contacted.
  - doc_bank_accounts_bank_accounts_(general)_032: "NOT REQUIRED (but may be offered at discretion) when: ... 2. Customer has not contacted merchant first (for non-fraud disputes)"
  - `gold[10].arguments: "dispute_category": "duplicate_charge", "contacted_merchant": false, "provisional_credit_eligible": true`
  - `user_scenario: "If asked about merchant contact: No, I haven't contacted them yet."`
  - *Why it matters:* Writing false here is a faithful reading of doc_032 and fails the hash.
  - *Fix:* Exempt duplicate_charge from the merchant-contact condition in doc_032, or set gold[10] to false.

*Verifier: Confirmed (Major → Major).* Reproduced the computations ($100 ATM, $89.99 duplicate, corrected $14.99 recurring) and the liability/provisional ambiguities. Two more unscripted fields add risk: dispute 2's transaction_type and dispute 4's contacted_merchant are never stated by the customer. Major holds.

### task_086 — Major

**The six-dispute task is mostly derivable, but the gold's PIN-compromise and purchase-type values for the skimmed-card fraud contradict the customer's own words, and its liability values rest on an undocumented convention.**

- **non_determinism (Major)** — For the TechWorld fraud the customer says the card was probably skimmed. Doc_031 defines 'yes_observed' as 'believes PIN was observed/skimmed', yet the gold uses 'unknown'. transaction_type 'pin_purchase' is also never established, because the customer did not make the purchase and the script gives no PIN/signature detail.
  - `user_scenario: "Still have card - I think someone skimmed my card at a gas station or something."`
  - `doc_bank_accounts_bank_accounts_(general)_031: "'yes_observed': Customer believes PIN was observed/skimmed"`
  - `gold[15].arguments: "transaction_type": "pin_purchase", "pin_compromised": "unknown"`
  - *Why it matters:* Both fields are stored in the debit_card_disputes record. An agent choosing 'yes_observed' or 'signature_purchase' fails the hash with defensible reasoning.
  - *Fix:* Have the customer state whether the fraudster used a PIN and whether they think the PIN was seen, or change the gold to 'yes_observed'.
- **document_gap (Major)** — The four non-fraud disputes use liability 50, but they were noticed 11/07-11/09 and reported 11/14 (3+ business days), and the docs give no liability rule for non-fraud categories.
  - `doc_..._031: "Reported within 2 business days of statement: Maximum liability $50 / Reported within 60 days of statement: Maximum liability $500"`
  - `gold[11] (noticed 11/07), gold[12] (11/09), gold[14] (11/09), gold[16] (11/08): "customer_max_liability_amount": 50`
  - *Why it matters:* A business-day count from discovery gives the $500 tier (stored 100/189.99/200/100 under a cap), which differs from the gold.
  - *Fix:* Document the liability anchor and the non-fraud convention once in doc_031 and regenerate.
- **non_determinism (Minor)** — The ATM deposit claim ($500 deposited, $300 credited) conflicts with the record (+$400) and no images exist. The customer then says 'I'll go with what you have', which can be read as withdrawing the claim rather than disputing $100.
  - `bank_account_transaction_history btxn_0788d2513c8c amount 400.0, type atm_deposit`
  - `get_atm_deposit_images_8473(btxn_0788d2513c8c) -> "Status: IMAGES NOT AVAILABLE"`
  - `user_scenario: "If your records show that, then I'll go with what you have."`
  - `gold[16].arguments: "disputed_amount": 100.0 (500 claimed - 400 credited)`
  - *Why it matters:* An agent that treats the customer's reply as dropping the claim files no deposit dispute and fails. The more natural reading files $100.
  - *Fix:* Script the customer to confirm 'I deposited $500, so $100 is missing' after being told the credited amount.
- **argument_error (Minor)** — The script gives the TechWorld discovery date as 'today 01/12', which contradicts the fixed clock (11/14/2025) used in the gold.
  - `user_scenario: "Just discovered today 01/12 during year-end reconciliation."`
  - `gold[15]: "discovery_date": "11/14/2025"`
  - *Why it matters:* It can be resolved from 'today' plus get_current_time, but a literal agent could record 01/12/2025.
  - *Fix:* Change the script to 'today, November 14th'.

*Verifier: Confirmed (Major → Major).* Reproduced the skimming/PIN-type ambiguity and the liability-anchor gap. The ATM-deposit issue ('I'll go with what you have' read as withdrawing the claim) is arguably Major-class rather than Minor, but the task is already Major, so the verdict stands.

### task_087 — Major

**The three-card CODE 05 diagnosis is derivable and the gold matches it; one security-alert document also tells agents to escalate when a customer reports a charge they did not make, which could lead a careful agent to transfer instead of filing the dispute.**

- **document_contradiction (Minor)** — Doc_..._039 lists 'Customer reports transactions they did not make' as a reason to escalate to the security team. The gold handles the Evergreen fraud in-channel (dispute, close, reorder) with no transfer.
  - `doc_bank_accounts_bank_accounts_(general)_039: "Escalate to security team when: ... Customer reports transactions they did not make"`
  - doc_checking_accounts_checking_accounts_(general)_003 CODE 05 step 3: customer-initiated alert -> "Ask customer to verify recent transactions. If they confirm all transactions are legitimate, clear the alert."
  - `gold[15] file_debit_card_transaction_dispute_6281, gold[17] close_debit_card_4721, gold[19] order_debit_card_5739; no transfer_to_human_agents`
  - *Why it matters:* An agent that escalates first ends the episode before the dispute, close and order writes and fails. The dispute procedure (doc_031) plus the card-action mapping is the more specific guidance, so most agents will follow the gold.
  - *Fix:* Limit doc_039's escalation bullet to bank-initiated alerts, or add 'after filing a dispute and replacing the card' to it.

*Verifier: Confirmed (Minor → Minor).* Re-derived the CODE 05 order for all three cards and the $50 liability (customer reported via the 11/06 fraud text). The doc_039 escalation conflict is resolvable by escalating after the writes, so Minor is fair. The PREMIUM design reading of 'best option that is free' is the natural one; unlike task_077 the script has no 'fancy design' counter-signal, so I did not raise it.

*Reconciled across runs: Minor → Major (judgment).* doc_039 tells the agent to escalate to the security team when the customer reports transactions they did not make, which is exactly this case, and nothing tells it to file the dispute, close and reorder first. The gold handles the fraud in-channel, and an agent that escalates per doc_039 ends the episode before any of the graded writes. Run U's 'escalate after the writes' reconciliation is the agent's own invention, not documented guidance, so these are two supported readings with different graded states: Major under both scorers.

### task_088 — Major

**For the cloned-card fraud, the decline-code guide says to freeze the card while the gold only closes it, and the customer is never told whether the Miami charge used a PIN, so two stored dispute fields are guesswork.**

- **document_contradiction (Major)** — The CODE 82 protocol, in a required document, says to recommend freezing the card until the replacement arrives. The dispute card-action mapping says close_and_reissue, and the gold closes without ever freezing. Any freeze leaves frozen_date, plus unfrozen_date when the card is then unfrozen to close it, and a freeze tool-log row that the gold lacks.
  - doc_checking_accounts_purple_account_007 (CODE 82): "If suspicious transactions found: Follow stolen card protocol to assist the customer. Recommend freezing the card until a replacement arrives."
  - `doc_bank_accounts_bank_accounts_(general)_031: "'card_present_fraud' -> 'close_and_reissue'"`
  - `user_scenario: "If agent says they'll freeze the card: Okay, if that's what needs to happen."`
  - Replay: gold with freeze_debit_card_3892 + unfreeze_debit_card_3893 on dbc_c8feebe975cf inserted before the close -> hash mismatch (frozen_date/unfrozen_date and freeze/unfreeze agent_discoverable_tools rows)
  - *Why it matters:* An agent that follows the CODE 82 text and freezes the card ends in a different DB state from the gold, even though it completes the dispute, closure and replacement.
  - *Fix:* Change CODE 82 to 'close the card and order a replacement (stolen card protocol)' or drop the freeze recommendation.
- **underspecified_instructions (Major)** — The gold dispute for ELECTRO MART MIAMI fixes transaction_type 'signature_purchase' and pin_compromised 'no'. The customer script says nothing about how the fraudulent purchase was authorized or whether the PIN may be compromised.
  - `gold[10].arguments: "transaction_type": "signature_purchase", "pin_compromised": "no"`
  - `doc_..._031: "transaction_type (string) - Determine from user circumstances"; pin_compromised options include 'unknown': Customer unsure`
  - `user_scenario PART 1.5 gives only card condition and transaction confirmations; no PIN/signature line`
  - *Why it matters:* The simulator must improvise (e.g. 'I don't know'), and an agent recording 'pin_purchase' or 'unknown' fails the hash for reasons outside its control.
  - *Fix:* Add script lines such as 'The statement shows it was signed, not PIN' and 'I don't think anyone has my PIN', or relax those fields.

*Verifier: Confirmed (Major → Major).* CODE 82 text confirmed verbatim. A freeze (or freeze-and-reorder without closing, which order_debit_card_5739 allows because FROZEN is not ACTIVE) diverges from the gold, and the PIN/signature fields depend on simulator improvisation. Major holds.

### task_091 — Blocker

**Two gold replacement-card orders contradict the bank's own card-replacement rules, and the fourth card's outcome is a judgment call, so a policy-following agent fails.**

- **argument_error (Blocker)** — The customer asks for 'the most premium free option for both' shipping and card type. Evergreen is Premium tier, where EXPEDITED shipping and the PREMIUM design are both $0, yet the gold orders STANDARD shipping and the CLASSIC design. task_090's gold gives the same account type free EXPEDITED shipping.
  - `user instructions item 20: "I want the most premium free option for both."`
  - `doc_bank_accounts_bank_accounts_(general)_005: "PREMIUM TIER (Evergreen Account)"`
  - doc_bank_accounts_bank_accounts_(general)_029 PREMIUM TIER: "Free expedited shipping on all replacements (delivery_fee: $0 for both STANDARD and EXPEDITED)" and "PREMIUM design (metallic silver): design_fee $0 (complimentary)"
  - `gold[14].arguments: "delivery_option": "STANDARD", "card_design": "CLASSIC" (account chk_tw34a7d9e2_evergreen)`
  - `task_090 gold[10] for an Evergreen account: "delivery_option": "EXPEDITED", "delivery_fee": 0`
  - *Why it matters:* A policy-following agent orders EXPEDITED shipping with the PREMIUM design at $0 each. order_debit_card_5739 stores delivery_option and card_design and derives the order_id from delivery_option, so the DB hash differs (replayed: differs).
  - *Fix:* Change gold[14] to EXPEDITED and PREMIUM with both fees at 0, or change the customer line to 'standard shipping and the classic design are fine'.
- **argument_error (Blocker)** — The gold closes the Light Blue card and orders its replacement in the same call. Light Blue is Entry tier, and the KB imposes a 48-hour wait after closure before an Entry-tier replacement can be ordered.
  - `doc_bank_accounts_bank_accounts_(general)_005: "ENTRY TIER (Light Blue Account, Light Green Account, Green Fee-Free Account)"`
  - `doc_bank_accounts_bank_accounts_(general)_029 ENTRY TIER: "48-hour waiting period after card closure before a replacement can be ordered"`
  - `gold[23]: close_debit_card_4721 dbc_tw34a7d9e2_lightblue fraud_suspected; gold[24]: order_debit_card_5739 chk_tw34a7d9e2_lightblue STANDARD`
  - *Why it matters:* A doc-faithful agent closes the card and tells the customer a replacement can be ordered after 48 hours, so the gold's debit_card_orders row and PENDING card never get created (replayed without gold[24]: hash differs). The tool does not enforce the wait, so only an agent that ignores doc_029 matches the gold.
  - *Fix:* Remove gold[24] (and add an NL assertion that the agent explains the 48-hour wait), or move the fourth card to a Mid-or-higher-tier account.
- **non_determinism (Major)** — For the Light Blue card the customer confirms the Bellevue attempts were his. The protocol then offers three equal options (close and replace, transfer to security, PIN reset), and the scripted customer accepts any of them. The gold picks close-and-replace with reason fraud_suspected.
  - doc_bank_accounts_bank_accounts_(general)_041 STEP 6: "If no unauthorized transactions: Explain the security concern and offer options: - Card closure and replacement (recommended if fraud suspected) - Transfer to security team for investigation - PIN reset"
  - doc_041 STEP 3: "11-14 | VERY HIGH | Cannot unlock on this call. Require callback verification OR enhanced verification"; "15+ | CRITICAL | ... Recommend card closure and replacement."
  - `user instructions items 41/44/45/47: confirms it was him; accepts closure, a transfer, or a PIN reset ('Sure, set it to 4121')`
  - `task notes: "Boundary case at exactly 11 points"; my count is A1 1 + A3 0/1 + B1 1 + B2 2 + B3 2 + C2 1 + C3 1 + C4 2 + D1 1 + E1 1 + E2 1 = 14-15`
  - *Why it matters:* Once the customer confirms, fraud is not obviously suspected, so 'recommended if fraud suspected' does not settle the choice. Whether the score lands in VERY HIGH (options) or CRITICAL (recommend closure) depends on how A3 is read. An agent that transfers or resets the PIN leaves a different DB.
  - *Fix:* Make the case unambiguous: either script the customer to deny the attempts, or have the docs name one required action for VERY HIGH scores once the customer confirms the attempts.
- **non_determinism (Major)** — The customer says 'I never shared it with anyone. Maybe someone watched me at an ATM? I really don't know.' The gold records pin_compromised='yes_observed', although the doc defines 'unknown' as 'Customer unsure'.
  - `user instructions item 22: "I never shared it with anyone. Maybe someone watched me at an ATM? I really don't know."`
  - `doc_bank_accounts_bank_accounts_(general)_031: "'yes_observed': Customer believes PIN was observed/skimmed" / "'unknown': Customer unsure"`
  - `gold[16], gold[17].arguments: "pin_compromised": "yes_observed"`
  - *Why it matters:* pin_compromised is stored on both debit_card_disputes rows. 'unknown' fits 'I really don't know' at least as well as 'yes_observed' does, and choosing it fails the hash (replayed: differs).
  - *Fix:* Script the customer to say plainly that someone may have watched him enter the PIN, or change the gold to 'unknown'.
- **document_gap (Major)** — The Green card scores LOW (about 2), and the protocol says to unlock it with no further steps. No tool or document describes how to unlock a card. The gold unlocks it by resetting the PIN to 2589, although the customer says he knows his PIN.
  - `doc_041 STEP 3: "0-4 | LOW | Unlock after standard identity verification"; STEP 5: "0 prior locks: Standard unlock, no additional steps."`
  - doc_bank_accounts_bank_accounts_(general)_027 describes reset_debit_card_pin_6284 as being for when the "Customer forgot their current PIN" and never mentions unlocking
  - `tools.py reset_debit_card_pin_6284 docstring: "Reset a debit card PIN when the customer has forgotten it." (the code sets card["pin_locked"] = False)`
  - `user instructions item 8: "Yeah, I know my PIN. I must have just fat-fingered it"`
  - `gold[8]: reset_debit_card_pin_6284 dbc_tw34a7d9e2_green new_pin 2589`
  - *Why it matters:* The agent has to infer, against the tool's description, that a PIN reset is how a card gets unlocked. An agent that looks for an unlock tool, finds none, and tells the customer it cannot unlock leaves pin_last_changed/pin_locked unwritten (replayed without gold[8]: hash differs).
  - *Fix:* Add an unlock tool, or state in doc_041 that 'unlock' means calling reset_debit_card_pin_6284 with a customer-chosen PIN.
- **argument_error (Minor)** — The instructions give the customer DOB as 09/22/1991, but the DB and gold log_verification use 09/22/2001. The persona is 24, which matches 2001.
  - `user instructions: "DOB: 09/22/1991"`
  - `initial_state users.tw34a7d9e2.date_of_birth = "09/22/2001"`
  - `gold[0].arguments.date_of_birth = "09/22/2001"`
  - *Why it matters:* Verification still passes on phone, email and address, and an agent that logs the DB record matches the gold. An agent that logs the DOB the customer stated would not match.
  - *Fix:* Change the instructions DOB to 09/22/2001.

*Verifier: Confirmed (Blocker → Blocker).* Both Blocker issues reproduce: the Evergreen order contradicts the customer's stated choice, and the Light Blue reorder contradicts the ENTRY wait that the gold honors in tasks 077/079/080/084. Secondary Majors (Light Blue option choice, pin_compromised, unlock-by-reset) also reproduce.

### task_092 — Major

**The Blue-card fraud closure and the security-hold transfer are well-defined, but the Green card's outcome and the Evergreen 'unlock' each rely on readings that a careful agent could reasonably make differently.**

- **non_determinism (Major)** — On the Green card the customer confirms she made the three sub-minute attempts herself (B3=3, so single-flag escalation). The protocol's Step 6 options include a PIN reset, which the customer would accept. The gold instead closes the card with reason fraud_suspected and reorders, even though no fraud is suspected.
  - `doc_bank_accounts_bank_accounts_(general)_041: "If ANY single flag equals 3 points, escalate to supervisor review regardless of total score."`
  - doc_041 STEP 6 options: "Card closure and replacement (recommended if fraud suspected)", "Transfer to security team", "PIN reset (issues new PIN, invalidates potential compromise)"
  - user instructions item 21: "If agent offers to close and replace OR transfer to security: Fine, I'll take a new card then."; item 23: "If agent offers to reset the PIN on the Green card: Sure, set it to 4567."
  - `gold[13]: close_debit_card_4721 dbc_rw42b8d3e1_green reason fraud_suspected; gold[14]: order_debit_card_5739 chk_rw42b8d3e1_green`
  - *Why it matters:* An agent that offers the PIN reset, which is the natural remedy for confirmed fat-fingering, gets 4567 from the customer and leaves a different DB (replayed: hash differs). An agent that closes the card might also choose a reason other than fraud_suspected, which changes closure_reason and the new card's issue_reason.
  - *Fix:* State in doc_041 that single-flag escalation forbids a PIN reset and requires closure, or script the customer to refuse a PIN reset.
- **document_gap (Major)** — The Evergreen card scores LOW or MEDIUM and can be unlocked. With one prior lock, the protocol only requires offering lock notifications, not a PIN reset. No document or tool describes how to unlock a card, and the gold unlocks it by resetting the PIN to 8127.
  - `doc_041 STEP 5: "1 prior lock: After unlock, MUST offer: 'Would you like me to enable PIN lock notifications...'"`
  - `doc_bank_accounts_bank_accounts_(general)_027: the reset procedure is for "Customer forgot their current PIN"; unlocking is not mentioned`
  - `tools.py reset_debit_card_pin_6284 is the only code that sets card["pin_locked"] = False`
  - `gold[18]: reset_debit_card_pin_6284 dbc_rw42b8d3e1_evergreen new_pin 8127`
  - *Why it matters:* An agent has to infer that resetting the PIN is the unlock mechanism. If it does not, the reset write is missing and the hash fails.
  - *Fix:* Document that unlocking a PIN-locked card is done with reset_debit_card_pin_6284, or add an unlock tool.

*Verifier: Confirmed (Major → Major).* Re-derived the four card outcomes. The Green card's PIN-reset alternative and the unlock-by-reset convention each change the hash; same class and severity as task_091's unlock issue. Major holds.

*Reconciled across runs: Major → Major (judgment).* Two Majors, both on writes compared exactly under either scorer. No document or tool says how to unlock a PIN-locked card, yet the gold unlocks Evergreen via reset_debit_card_pin_6284 (documented for forgotten PINs); an undocumented convention is Major by definition, as run V's own 091 verifier noted. On the Green card, doc_041 Step 6 lists a PIN reset the script accepts ('Sure, set it to 4567') while the gold closes with fraud_suspected for a customer who confirmed the attempts, which is two supported readings; run V's 092 was never verified.

### task_094 — Major

**The KB describes the Gold Rewards Card's 0.025% both as a credit-card bonus that does not stack and as a separate relationship bonus that does, so $140 and $142 are both defensible corrections.**

- **document_contradiction (Major)** — doc_013 calls the Gold Rewards Card's 0.025% a 'relationship bonus APY on top of the base rate'. doc_045 says credit-card bonuses DO stack with relationship bonuses. But doc_014 and doc_045's own example list the same 0.025% as a non-stacking credit-card bonus. The gold treats it as a credit-card bonus that loses to EcoCard's 0.6%.
  - `doc_savings_accounts_gold_account_013: "As a Gold Rewards Card holder, you receive an additional 0.025% relationship bonus APY on top of the base rate."`
  - `doc_savings_accounts_gold_account_014 table: "| Gold Rewards Card | +0.025% |" under "Credit card APY bonuses"`
  - doc_bank_accounts_bank_accounts_(general)_045: "credit card APY bonuses DO stack with other types of bonuses, such as: ... Relationship bonuses for holding multiple Rho-Bank products"
  - `doc_045 example: Gold Rewards +0.025%, Platinum +0.15%, EcoCard +0.6% -> "The customer receives only the EcoCard bonus of +0.6%"`
  - `gold[6].arguments.amount = 140.00; gold[8].arguments.expected_apy = 6.85`
  - *Why it matters:* The customer explicitly asks for 'any other boosts that I'm missing'. An agent that also adds doc_013's relationship bonus computes 5.5 + 0.75 + 0.6 + 0.025 = 6.875% and credits 96000 x 1.775% / 12 = $142.00, which fails the hash (replayed: differs).
  - *Fix:* Rewrite doc_013 to say its 0.025% is the Gold Rewards Card's credit-card APY bonus (subject to the highest-only rule), not a separate relationship bonus.
- **document_contradiction (Minor)** — doc_013's worked example adds 5.5% + 0.025% and reports a total of 6.0%, which is a corrupted value. The customer's own mistaken belief is also 6.0%.
  - `doc_savings_accounts_gold_account_013: "Base APY: 5.5% / Relationship bonus APY: +0.025% / Total APY with the bonus: 6.0%"`
  - `user instructions item 1: "so I should be at 6.0% APY"`
  - *Why it matters:* A careful agent recomputes the sum, but the corrupted total seems to confirm the customer's wrong figure and could anchor a weaker agent.
  - *Fix:* Change the total to 5.525%.

*Verifier: Confirmed (Major → Major).* Reproduced 6.85% / $140 and the alternative 6.875% / $142. doc_044 explicitly treats relationship bonus as its own component, so the doc_013 reading is genuinely supported; Major holds.

### task_095 — Major

**The wrong-boost diagnosis is solvable, but the same contested 0.025% Gold Rewards 'relationship bonus' makes $98 versus $100 a coin flip.**

- **document_contradiction (Major)** — As in task_094, the gold treats the Gold Rewards Card's 0.025% purely as a credit-card bonus that loses to EcoCard. doc_013 calls it a relationship bonus on top of the base rate, and doc_045 says relationship bonuses stack with credit-card bonuses.
  - `doc_savings_accounts_gold_account_013: "As a Gold Rewards Card holder, you receive an additional 0.025% relationship bonus APY on top of the base rate."`
  - `doc_bank_accounts_bank_accounts_(general)_045: "credit card APY bonuses DO stack with ... Relationship bonuses for holding multiple Rho-Bank products"`
  - `doc_savings_accounts_gold_account_014 table: "| Gold Rewards Card | +0.025% |"`
  - `task notes: actual 5.625% = "base 5.5% + Purple 0.1% + Gold Rewards 0.025%"`
  - `gold[6].arguments.amount = 98.00; gold[8].arguments.expected_apy = 6.85, actual_apy = 5.625`
  - *Why it matters:* Under the stacking reading the expected APY is 5.5 + 0.75 + 0.6 + 0.025 = 6.875%, the credit is 96000 x 1.25% / 12 = $100.00, and the report says 6.875. Both rows differ from the gold (replayed: hash differs).
  - *Fix:* Same as task_094: make doc_013 say the 0.025% is the Gold Rewards Card's credit-card APY bonus and does not stack.
- **document_contradiction (Minor)** — doc_013's example total of 6.0% for 5.5% + 0.025% is a corrupted value.
  - `doc_savings_accounts_gold_account_013: "Total APY with the bonus: 6.0%"`
  - *Why it matters:* It is cosmetic for a careful agent, but it adds noise to the very component that is already contested.
  - *Fix:* Change the total to 5.525%.

*Verifier: Confirmed (Major → Major).* Same defect class and severity as task_094, applied consistently. Arithmetic re-run matches the finding.

### task_097 — Blocker

**The gold leaves out the documented 0.025% multi-product relationship bonus on the Silver account, the same bonus task_093's gold requires, so a doc-following agent's Silver credit and report fail.**

- **argument_error (Blocker)** — The Silver expected APY in the gold is 4.0 + 0.45 + 2.2 = 6.65%, which omits the 0.025% relationship bonus. A required doc grants that bonus for holding multiple products, and this customer holds 13. task_093's gold adds the same bonus for a two-product customer.
  - doc_savings_accounts_silver_account_002 (required): "If you maintain multiple Rho-Bank products, you may also qualify for a relationship bonus of 0.025% that stacks on top of your base Silver APY."
  - `doc_savings_accounts_silver_account_005: "Eligible customers receive a relationship APY bonus of 0.025% added to the base Silver APY."`
  - doc_bank_accounts_bank_accounts_(general)_044: "Missing Relationship Bonus: Customer maintains multiple Rho-Bank products but the relationship bonus was not applied."
  - `task_093 gold expected_apy = 4.275 (4.0 + 0.25 + 0.025)`
  - `gold[9].arguments.amount = 220.84; gold[14].arguments.expected_apy = 6.65`
  - *Why it matters:* A doc-following agent computes 6.675%: 100000 x 6.675% / 12 = 556.25, minus the 333.33 credited = $222.92. Both the credit row and the report row differ from the gold (replayed: hash differs). No consistent reading of the docs passes both task_093 and task_097.
  - *Fix:* Change gold[9] to 222.92 and gold[14] to expected_apy 6.675 / amount_difference 222.92.
- **document_gap (Major)** — Silver Plus documents two add-ons the gold silently excludes: a 0.025% relationship bonus whose 'relationship criteria' are never defined, and a 0.25% direct-deposit bonus that does not say which account must receive the deposit. The customer has payroll direct deposit into his Blue checking account.
  - `doc_savings_accounts_silver_plus_account_002: "Earn an additional relationship APY bonus of 0.025% when you qualify under the relationship criteria."`
  - `doc_savings_accounts_silver_plus_account_004: "Set up direct deposit to receive an additional APY boost of 0.25%."`
  - `initial_state bank_account_transaction_history.btxn_blue_dd: "DIRECT DEPOSIT - PAYROLL" on chk_mc80w7k3x9_blue`
  - `gold[12].arguments.amount = 12.00; gold[17].arguments.expected_apy = 5.3`
  - *Why it matters:* An agent that applies the Silver multi-product criteria to Silver Plus gets 5.325% and $12.38 (18000 x 5.325% / 12 = 79.875, minus 67.50). Adding the direct-deposit bonus gives a different figure again. Either changes the hash.
  - *Fix:* Define the Silver Plus relationship criteria and the direct-deposit target, or state that neither applies to this customer.
- **non_determinism (Minor)** — Because the actual Silver credit is the rounded 333.33, two reasonable calculation methods differ by one cent. Expected interest minus interest credited gives 554.17 - 333.33 = $220.84 (gold). The APY difference times balance / 12 gives 2.65% x 100000 / 12 = $220.83.
  - `initial_state btxn_silver_interest_oct.amount = 333.33`
  - `doc_bank_accounts_bank_accounts_(general)_044: "amount_difference ... The dollar amount difference between expected and actual interest credited"`
  - `gold[9].arguments.amount = 220.84`
  - *Why it matters:* The docs prescribe the subtraction method, so the gold value is derivable, but a one-cent rounding difference fails the hash (replayed 220.83: differs).
  - *Fix:* Seed a Silver balance whose monthly interest is a whole number of cents at 4.0% (for example $99,000 gives $330.00), or state the rounding rule in doc_044.

*Verifier: Adjusted (Blocker → Major).* Reproduced all four account computations and the $222.92 alternative. The gold's omission has some document support ('may qualify', undefined eligibility, and silver_009 tying the 0.025% to Platinum Rewards Card holders), so per calibration this is two supported readings (Major), the same class and severity as 094/095. It would be a Blocker only if task_093's convention is treated as binding; that cross-task conflict is real and is logged in calibration_notes. The Silver Plus add-on gap (Major) and the one-cent rounding (Minor) hold. A further oddity: the 45-year-old customer holds a Light Green Account (ages 13-24 per light_green_002) whose +0.2% boost the gold uses for Diamond Elite.

*Reconciled across runs: Major → Blocker (judgment).* Fact: the required doc silver_002 and FAQ silver_005 grant the 0.025% relationship bonus to customers with multiple Rho-Bank products, this customer holds 13, and doc_044 names 'Missing Relationship Bonus' as a discrepancy type. task_093's gold applies the bonus (expected_apy 4.275) to a two-product customer with no credit card. The only text that could exclude it, silver_009's Platinum-Rewards-Card section, calls it 'the existing ... 0.025% relationship bonus' (not Platinum-only), and reading it as Platinum-only would break task_093's gold. The gold's 6.65% therefore follows no reading consistent with the documents or the benchmark's own convention: Blocker under both scorers. The 220.84 vs 220.83 rounding issue is an additional Major.

### task_101 — Major

**Purple plus Sky Blue is the right pair if only two referrals can go now, but the docs can also be read as allowing all four.**

- **non_determinism (Major)** — The docs cap bonuses received at 2 per rolling 9 days; they do not limit referrals submitted. The customer's last bonuses were on 10/25 and 10/10, so the window is currently clear, and a literal reader can conclude that all four referrals may be submitted now. The gold assumes new submissions count toward the window and caps them at two.
  - doc_bank_accounts_bank_accounts_(general)_047: "You can receive at most 2 referral bonuses in any rolling 9-day window." / "If you attempt to receive more than 2 referrals in a single 9-day period, the third referral (and any subsequent referrals in that window) will be automatically denied."
  - `doc_047: "Track the timing of your last two successful referral bonuses before sending additional referrals."`
  - doc_bank_accounts_bank_accounts_(general)_048: "You can have multiple referrals in progress, but you can only receive a maximum of 2 referral bonuses in any rolling 9-day window."
  - `initial_state referrals: latest COMPLETE dates 10/25/2025 (Gold Years) and 10/10/2025 (Sky Blue); fixed clock 11/14/2025`
  - user instructions 13a / 17: submits only 2 if the agent mentions the window limit, but all 4 'If agent recommends all 4 referrals without mentioning rolling window'
  - `gold[2] submit_referral 'Purple Account'; gold[3] submit_referral 'Sky Blue Account'`
  - *Why it matters:* If the agent decides the window does not bind and recommends all four (Green Fee-Free for Maya, Purple, Lime Green for Ember, Sky Blue for TechFlow), the customer submits four records, which fails the hash (replayed: differs). The customer script pushes toward two once the limit is mentioned, which makes the gold reachable but dependent on the agent's reading.
  - *Fix:* State in doc_047 that each submitted referral counts toward the 9-day limit from its submission date, or seed two COMPLETE bonuses within the last 9 days so the cap clearly binds.

*Verifier: Confirmed (Major → Major).* The pair Purple + Sky Blue is correct under the 'submissions count toward the window' reading; the literal 'bonuses received' reading permits all four. Two supported readings, so Major holds.

*Reconciled across runs: Major → Major (judgment).* doc_047 and doc_048 limit bonuses received in a rolling 9-day window, and doc_048 says outright that multiple referrals may be in progress. No bonus falls in the current window (last ones 10/25 and 10/10), and a bonus is received when the referred person qualifies, not on submission, so submitting all four now is a document-supported reading, and the script then submits all four. The gold (two now) follows the competing reading that new submissions count toward the window, so this is two supported readings with different graded referrals tables: Major under both scorers.

### task_102 — Blocker

**The grading requires the agent to 'recognize' that Ember is over Sky Blue's 4-year limit, but nothing the agent can see says so. 'Maximize the bonus' also points to Lime Green ($200 to the customer) rather than the gold's Sky Blue ($150).**

- **underspecified_instructions (Blocker)** — The NL assertion requires the agent to recognize that Ember Analytics is over Sky Blue's 4-year formation limit. The only age information the agent can get is the customer's statement that Ember incorporated in late 2022, about 3 years ago, which is within the limit. Ember's real 5-year age appears only in the author notes and in a different task (task_101).
  - evaluation_criteria.nl_assertions[0]: "The agent should recommend TechFlow Labs (not Ember Analytics) for the Sky Blue Account referral, recognizing that Ember Analytics exceeds the 4-year company age limit for Sky Blue eligibility."
  - `evaluation_criteria.reward_basis = ["DB", "NL_ASSERTION"]`
  - `user instructions item 7: "They incorporated in late 2022, so that's about 3 years now."`
  - `doc_business_checking_accounts_sky_blue_001: "Confirm your company is within 4 years of formation."`
  - `db.json and documents: no record mentions 'Ember' or 'TechFlow' (grep count 0)`
  - *Why it matters:* Under default EvaluationType.ALL, the NL reward is multiplied into the task reward (evaluator.py). A faithful agent cannot honestly state that Ember exceeds the limit, so the NL check fails, or passes only if the judge is lenient, regardless of the DB result. The user script's item 11 (agent 'corrects' Ember's age) can only trigger if the agent hallucinates.
  - *Fix:* Give the agent a verifiable source for Ember's formation date (a DB record or the customer's correct answer when asked), or drop the 'recognizing...' clause from the NL assertion.
- **non_determinism (Major)** — With one slot left in the window, the customer asks which referral to prioritize 'to maximize the bonus' without saying whether she means her own bonus or the combined total. Ember to Lime Green pays the referrer $200, more than Sky Blue's $150. Sky Blue only wins on the combined total ($400 vs $350).
  - `user instructions item 12: "which one should I prioritize? I want to maximize the bonus."`
  - doc_business_checking_accounts_lime_green_003: "Your bonus: $200 ... Their bonus: $150 ... Referred business must deposit $15,000 within 90 days" (Ember deposits $18,000; Lime Green 2/12 used)
  - `doc_business_checking_accounts_sky_blue_001: "Your bonus: $150 ... Their bonus: $250"`
  - `gold[2]: submit_referral 'Sky Blue Account'`
  - *Why it matters:* An agent that reads 'the bonus' as the customer's own bonus recommends Lime Green, and the referral record's account_type differs from the gold's (replayed: hash differs).
  - *Fix:* Have the customer say 'the biggest combined bonus' (as in task_101), or accept Lime Green as gold.

*Verifier: Confirmed (Blocker → Blocker).* With the agent-visible '3 years', Ember and TechFlow tie for Sky Blue, and the NL assertion requires a fact the agent cannot obtain, so the multiplied NL reward is chance. Blocker holds; the 'maximize the bonus' referrer-vs-combined ambiguity is a correct Major sub-issue.

*Reconciled across runs: Blocker → Blocker (coverage).* Fact: the NL assertion requires the agent to recognize that Ember Analytics exceeds Sky Blue's 4-year limit, but Ember's real age (5 years) appears only in author notes and in task_101's script. It is in no DB record, document or tool output, and this customer says Ember incorporated in late 2022 ('about 3 years'). On agent-visible facts Ember and TechFlow both qualify for Sky Blue at the same $400 combined bonus, and the script branch where the agent 'corrects' Ember to 5 years can only fire on hallucination. reward_basis multiplies the NL result into the score, so the information needed does not exist: Blocker under both scorers, since NL grading is unchanged. Run V judged the assertion satisfiable without weighing its 'recognizing' clause; the 'maximize the bonus' referrer-vs-combined ambiguity is an additional Major.

