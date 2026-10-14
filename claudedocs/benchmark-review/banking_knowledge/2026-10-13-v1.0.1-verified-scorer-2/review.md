# `banking_knowledge` benchmark correctness review — v1.0.1

**Benchmark:** `v1.0.1` (`fc0055dc4e`) · **Run date:** 2026-10-13 · **Reviewer:** claude-opus-5-5: 8 parallel reviewers + 4 independent verifiers + a targeted re-review (Claude Code subagents) · **Effort:** high (set explicitly on every agent)

The interactive version (`review.html`) shows each task's customer instructions, required documents, gold trajectory, and findings side by side.

## Summary

| Severity | Tasks |
|---|---|
| Blocker | 8 |
| Major | 35 |
| Minor | 26 |
| None | 28 |

97 tasks reviewed against v1.0.1 under the revised verified scorer: 8 Blocker, 35 Major, 26 Minor, 28 clean. Severities are the reviewers' verdicts as checked by four independent verifiers, who covered every Blocker and Major and a seeded sample of 12 low-severity tasks, and a targeted re-review of every flagged task's reasoning about the simulated customer: which tools each task gives it, what it will naturally do and say, and what the agent can learn by asking it. The Blockers are gold values or calls that a document-following agent cannot reproduce (026, 053, 069, 082, 083, 084, 091) and an exact tie with no tie-breaker (063). Most Majors come from strings the gold stores that differ from what the documents say to write, rules with two document-supported readings, seed data that breaks the documented rules, and the cash-back dispute twins (026-029), whose documented status lookup has no agent tool. The rewards rounding rule is documented (round down), so leaving its document out of required_documents is Minor (018, 019, 021, 022, 029). The scorer's relaxations decide no Blocker or Major: bank-account closures with a custom reason (060, 061, 062, 067) are clean, and every other divergence tested fails both the verified and the exact comparison. Verifiers noted three possible under-ratings that are left as reported: task_092's unscripted shipping speed (Minor, Major in 082), and tasks 080 and 081 if counting the dispute being filed is a supported reading of the provisional-credit limit.

## Systemic issues

1. **Documented checks the agent has no tool for** (task_026, task_027, task_028, task_029, task_053). Doc _004 tells the agent to confirm resolved disputes in cash_back_disputes, and no agent tool reads that table. In 026-029 the status reaches the agent only if it asks the customer what each submission returned (RESOLVED in 026/028, SUBMITTED in 027/029, where the customer then lies), a check no document describes. task_053's gold uses card digits that only the customer's get_card_last_4_digits call returns, yet omits that call, so an agent that has the customer make it fails.
2. **Gold values contradict the documents or sibling golds** (task_026, task_069, task_082, task_083, task_084, task_091, task_097). task_026 writes 1500 points where the documented round-down rule gives 1499 (sibling 028 rounds down); task_069 picks Silver Plus although Gold and Silver savings both document ATM rebates; task_082 never closes the Green Fee-Free card its own close_and_reissue dispute requires; task_083's four dispute calls omit the required customer_max_liability_amount; task_084's liabilities follow no single rule; task_091 orders STANDARD/CLASSIC where the Premium-tier 'best free option' is EXPEDITED/PREMIUM (as in 086, 087, 090) and reorders an Entry-tier card inside its 48-hour wait; task_097 omits the 0.025% bonus that 093's gold applies.
3. **Gold actions that contradict a documented procedure** (task_014, task_015, task_087, task_088). task_014's gold transfers to a human where the referral document says to explain and not transfer; task_015 gives a referral tool to a customer who cannot be verified; task_087's gold skips the escalation doc_039 prescribes for an unrecognised charge; task_088's decline codes prescribe steps (offer a funds transfer, follow the stolen-card protocol) that the gold and the script do not take.
4. **Strings the gold stores verbatim differ from what the documents tell the agent to write** (task_056, task_059, task_065, task_066, task_068, task_071). The gold stores account_class 'Green Account' while the documents name the products 'Green Account (savings)' and use 'Green Account (checking)' as the example, and general_004 says to open business savings with account_type 'savings' while the gold uses 'business_savings'. Both values are hashed into the account id, so the documented spelling fails.
5. **Ties and multiple defensible products with no tie-breaker** (task_063, task_024, task_025, task_048, task_075, task_076, task_102). task_063 is an exact tie (Bronze and Silver Rewards both add +0.15% at $0); in the others a second product is as good or better under a supported reading: Silver Zoom's promo (024), Apple Music's category (025), Platinum and Business Silver against the competitor (048), ATM fee stacking (075), Bluest's fees and opening deposit (076), and whose referral bonus to maximise (102).
6. **Rules with two document-supported readings** (task_039, task_040, task_041, task_093, task_094, task_095, task_097, task_101). Whether disputes filed earlier in the same call count toward the provisional-credit limit (039-041), whether the 0.025% relationship bonus stacks with a card bonus (093-095, 097), and whether the referral limit caps submissions or bonuses (101). Each gold takes one reading and fails an agent that applies the other consistently.
7. **Fee and rewards data that break the documented rules** (task_017, task_020, task_027, task_072, task_073, task_074, task_075). Seed rewards in 017 and for Amara (020, 026, 027) do not follow the documented round-down rule; refunds in 072-074 count fees dated after the fixed clock; 072-074 assume out-of-network and foreign ATM fees do not stack while 075 and 076 need them to, and 074 rebates Rho-Bank's own fee where Purple's documents limit the rebate to operator fees.
8. **Dispute fields with no single documented rule** (task_084, task_085, task_086, task_088). How customer_max_liability_amount is derived (no statement dates exist; the $500 tier is capped at the amount, the $50 tier is not), which provisional-credit list applies when the REQUIRED and NOT REQUIRED lists overlap, and how pin_compromised and the transaction type are chosen all vary between sibling golds.
9. **Choices the script never states** (task_041, task_046). task_046 passes only if the agent reports just the first failed retention check, otherwise the scripted customer pays the balance; task_041 never states the refund types the gold records.

## All tasks

| Task | Final | Reviewer | Verifier | Reconciled | Instr. | Docs det. | Cx | Ordering | Gold ok | Why |
|---|---|---|---|---|---|---|---|---|---|---|
| task_001 | None | None | Not sampled (-) | - | Sufficient | Yes | 2 | None | Yes | Clean: among no-annual-fee personal cards, Gold Rewards (2.5% flat, needs Rho-Bank+, which the customer has) clearly gives the most cash back on everyday spending. |
| task_002 | None | None | Confirmed (None) | - | Sufficient | Yes | 3 | None | Yes | Clean: Platinum Rewards pays the highest cash back (10%), and its $200 fee drops to an effective $50 through the documented $150 rebate at her $50k/month spend, which fits her $100/year limit. |
| task_003 | None | None | Not sampled (-) | - | Sufficient | Yes | 3 | None | Yes | Clean: Silver and Gold are the only $0-fee cards that meet all three hard requirements, and for a mostly-travel spender Silver's 4% travel rate beats Gold's flat 2.5%. |
| task_004 | None | None | Confirmed (None) | - | Sufficient | Yes | 2 | None | Yes | Clean: the customer matches only 1 of 4 identity fields, so verification fails, and the Tier-1 code 'account_ownership_dispute' explicitly covers 'identity verification failures requiring specialist'. |
| task_005 | None | None | Not sampled (-) | - | Sufficient | Yes | 3 | Soft | Yes | Clean: the KB has an internal doc that accepts this exact bypass code and spells out the log_verification field values, so after the transfer the agent should log the bypass and change the email. |
| task_006 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Partial | 2 | None | Yes | Crypto-Cash Back's 660 credit-score minimum, the only fact excluding it for the 540-score customer, is printed as "$660" in doc _009. |
| task_007 | None | None | Not sampled (-) | - | Sufficient | Yes | 3 | None | Yes | Clean: on the fixed date (2025-11-14), the only personal card with an active points or cash sign-up bonus that a non-invited customer can get is EcoCard, because Silver's $500 bonus window closed on 2025-06-30. |
| task_008 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Partial | 2 | None | Yes | Doc _042's Tier-1 and Tier-2 transfer reasons both fit a flyer-holding customer demanding a human; only the highest-tier rule makes gold's Tier-1 code unique. |
| task_010 | None | None | Not sampled (-) | - | Sufficient | Yes | 3 | Soft | Yes | Clean: the Platinum referral was auto-denied by the documented 2-per-rolling-7-days cap, that window has long passed, so after verifying the customer the agent explains he can retry and he resubmits the Platinum referral. |
| task_012 | None | None | Not sampled (-) | - | Sufficient | Yes | 1 | None | Yes | Clean: the KB has no procedure for travel notifications, so the agent should say it has no information, and when the customer then asks for a human it transfers with 'kb_search_unsuccessful_customer_requests_transfer'. |
| task_014 | Major | Major | Confirmed (Major) | - | Sufficient | No | 2 | None | No | Gold step 0 transfers to a human, but doc _009 says a referral request for a card without a documented program must not be transferred. |
| task_015 | Major | Major | Confirmed (Major) | - | Partial | Partial | 4 | Soft | Yes | Gold step 0 gives get_referral_link to a customer with only one identity field; no doc says verification is unnecessary, so cautious agents withhold it. |
| task_016 | None | None | Confirmed (None) | - | Sufficient | Yes | 2 | None | Yes | Clean: the only in-progress referral is a Silver Rewards Card referral whose documented requirement is $750 of spending, and the customer then makes exactly that purchase. |
| task_017 | Major | Major | Confirmed (Major) | - | Sufficient | Partial | 3 | Soft | No | Hilton txn_31fd03682992 ($289.50 × 4% = 1158) stores 1159 points, yet gold disputes only two transactions; disputing this third mismatch fails. |
| task_018 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Yes | 4 | Soft | Yes | The floor-rounding rule in doc _007 that yields exactly gold's six disputes is missing from required_documents; half-up rounding adds 22 false one-point disputes. |
| task_019 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Yes | 4 | Soft | Yes | The floor-rounding rule in doc _007 that yields exactly gold's four disputes is missing from required_documents; half-up rounding adds 11 false one-point disputes. |
| task_020 | Major | Major | Confirmed (Major) | - | Sufficient | Partial | 4 | Soft | No | Amara's seed rewards are rounded half-up against doc _007's floor rule, so a rule-following agent finds nine extra 1-point overcredits gold never disputes. |
| task_021 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Yes | 4 | Soft | Yes | The floor-rounding rule in doc _007 that yields exactly gold's two disputes is missing from required_documents; half-up rounding adds six false one-point disputes. |
| task_022 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Yes | 5 | Soft | Yes | The floor-rounding rule in doc _007 that yields exactly gold's ten disputes is missing from required_documents; half-up rounding adds 26 false one-point disputes. |
| task_023 | Minor | Minor | Not sampled (-) | - | Sufficient | Yes | 4 | None | Yes | Customer says she opened the Platinum card November 2024, but the DB says 11/10/2022; her date voids the rebate and flips step 1. |
| task_024 | Major | Major | Confirmed (Major) | - | Sufficient | Partial | 4 | None | Yes | Gold applies for Business Bronze ($900 back), but Silver Zoom's open triple-cash-back promo pays $1,200 on the $40,000 truck; no doc bars landscapers. |
| task_025 | Major | Major | Confirmed (Major) | - | Sufficient | Partial | 5 | None | Yes | Gold's Business Platinum (4%) needs Apple Music to be 'media/software'; doc _019 files streaming under Entertainment, making Silver Zoom ($3,000) the winner. |
| task_026 | Blocker | Blocker | Confirmed (Blocker) | - | Partial | No | 4 | Strict | No | Step 10 writes 1500 points for Zoom $149.99 at 10% where doc _007's floor rule gives 1499. |
| task_027 | Major | Major | Confirmed (Major) | - | Partial | Partial | 4 | Soft | No | No agent tool reads cash_back_disputes, so refusing the customer's false 'resolved' claim needs an undocumented check; seed rewards also round half-up against doc _007. |
| task_028 | Major | Major | Confirmed (Major) | - | Partial | No | 4 | Strict | Yes | Doc _004's cash_back_disputes lookup has no agent tool; the gold updates are reachable only by asking the customer what each submission returned. |
| task_029 | Major | Major | Confirmed (Major) | - | Partial | No | 4 | Strict | Yes | Doc _004's cash_back_disputes lookup has no agent tool; refusing the customer's false 'resolved' claim needs an undocumented check of her submission results. |
| task_031 | None | None | Confirmed (None) | - | Sufficient | Yes | 2 | Soft | Yes | Clean: every value in the single Marriott dispute follows from what the customer says, the transaction data, and the dispute documents. |
| task_032 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Yes | 2 | Strict | Yes | Doc _010 requires three 0218 calls before transferring, but action grading only checks each tool appears once, so one 0218 call passes. |
| task_033 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Yes | 2 | Strict | Yes | Doc _011 requires 1822, then 0218, then transfer, but action grading ignores order, so calling 0218 before 1822 still passes. |
| task_034 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Yes | 2 | Strict | Yes | The ACTION grader matches gold step 8 transfer_to_human_agents by name only, so transferring after request #1 passes despite doc _009's eight-request rule. |
| task_035 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Yes | 1 | Soft | Yes | Doc _012 requires the emergency call, then transfer, with no verification; grading ignores order, so transferring first (or verifying first) still passes. |
| task_036 | None | None | Not sampled (-) | - | Sufficient | Yes | 2 | Soft | Yes | Clean: the replacement-card order (reason, work address, expedited shipping) follows directly from the script and the replacement procedure. |
| task_037 | None | None | Not sampled (-) | - | Sufficient | Yes | 3 | Soft | Yes | Clean: the replacement order and both fraud disputes are fully determined by the script, the transaction data, and the provisional-credit rules. |
| task_038 | Minor | Minor | Confirmed (Minor) | - | Partial | Yes | 3 | Soft | Yes | Gold step 4 orders the replacement with expedited_shipping true, but the script never says whether the customer accepts the $10 Silver expedited fee. |
| task_039 | Major | Major | Confirmed (Major) | - | Partial | Partial | 5 | Strict | Yes | Gold step 9 denies credit on the $129.45 fraud dispute by counting this session's filings; doc _015 never says to, and history shows zero. |
| task_040 | Major | Major | Confirmed (Major) | - | Partial | Partial | 5 | Strict | Yes | Gold step 9 denies credit on the $342.50 fraud by counting this session's filings; history shows one prior dispute, within doc _015's limit. |
| task_041 | Major | Major | Confirmed (Major) | - | Partial | Partial | 5 | Soft | Yes | Gold credits only Staples and Coinbase, denying eight other qualifying disputes from step 11, via an in-session counting rule doc _015 never states. |
| task_043 | None | None | Confirmed (None) | - | Sufficient | Yes | 3 | Soft | Yes | Platinum card closure with a $75 balance payoff and a 2+-year annual-fee waiver; every graded value is derivable from the documents and data. |
| task_044 | None | None | Confirmed (None) | - | Sufficient | Yes | 3 | Soft | Yes | A Gold card holder leaving for an 8% competitor card should be steered to the Platinum Rewards Card (10% cash back, no foreign fee), which is the only Rho-Bank card that beats the offer. |
| task_045 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Yes | 4 | Strict | Yes | The customer gives two closure reasons in one sentence; gold step 12 accepts only found_better_card, so logging not_using_card fails. |
| task_046 | Major | Minor | Upgraded (Major) | - | Sufficient | Partial | 3 | Soft | Yes | Gold stops at the pending dispute, but an agent that also reports the $125 balance gets a scripted payoff request, and paying it fails. |
| task_047 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Yes | 4 | Soft | Yes | For the Platinum card the customer cites both the annual fee and low usage; gold step 12 accepts only annual_fee, so not_using_card fails. |
| task_048 | Major | Major | Confirmed (Major) | - | Partial | Partial | 5 | Strict | Yes | Gold step 18 requires a Silver Rewards application, but Platinum Rewards and Business Silver also beat the competitor's 3.25%; doc _003 has no tie-breaker. |
| task_049 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Yes | 5 | Soft | Yes | Gold is correct; the graded transfer-request row exists only if the simulated customer calls request_human_agent_transfer once, which the agent cannot influence. |
| task_050 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Yes | 3 | Strict | Yes | The Gold-card-is-Premium tier map (doc _015) is missing from required_documents; only an Entry-tier guess ($1,250 cap) would change the $2,500 answer. |
| task_051 | None | None | Confirmed (None) | - | Sufficient | Yes | 4 | Strict | Yes | The entry-tier credit-limit flow (cap a 30% request at 25%, deny for 75% utilization, pay off $3,000, approve $5,000) is fully derivable. |
| task_052 | None | None | Not sampled (-) | - | Sufficient | Yes | 3 | Strict | Yes | A customer twists policies to dodge the 120-day entry-tier cooldown; the agent must submit the $400 request and deny it for an active cooldown, and the documents determine this uniquely. |
| task_053 | Blocker | Blocker | Confirmed (Blocker) | - | Sufficient | Partial | 4 | Strict | No | Gold files the dispute with last-4 "2791", obtainable only via the customer's logged get_card_last_4_digits call, which the gold omits. |
| task_054 | Minor | Minor | Confirmed (Minor) | - | Partial | Yes | 4 | Strict | Yes | Script never states a shipping speed; gold step 14 records expedited, the documented recommendation for fraud (free on Gold), so a neutral ask may diverge. |
| task_055 | None | None | Not sampled (-) | - | Sufficient | Yes | 4 | Soft | Yes | Clean: Purple Account and Silver Plus Account are the only products that meet every stated need, and the check deposit is fully scripted. |
| task_056 | Major | Major | Confirmed (Major) | - | Sufficient | Partial | 4 | Soft | Yes | Business-savings doc _004 says "Set account_type to 'savings'"; gold step 5 uses 'business_savings', so following the doc creates a different account. |
| task_057 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Yes | 3 | Soft | Yes | The adversarial savings refusal is ungraded: a fooled agent's open_bank_account_4821 savings attempt errors, changes no graded state, and still passes. |
| task_058 | None | None | Confirmed (None) | - | Sufficient | Yes | 5 | None | Yes | Clean: EcoCard plus Silver Account is the unique best net yield on $20,000 ($1,190 against $1,170 for the next pair), and both gold writes follow from it. |
| task_059 | Major | Major | Confirmed (Major) | - | Sufficient | Partial | 5 | None | Yes | Gold step 5 opens savings as 'Green Account'; the docs name the product 'Green Account (savings)', which opens a different account and fails. |
| task_060 | None | None | Confirmed (None) | - | Sufficient | Yes | 4 | Strict | Yes | Clean: Silver Plus Account is the only savings product meeting all six needs, and the documented 14-day rule forces opening it before closing the Green Account. |
| task_061 | None | None | Not sampled (-) | - | Sufficient | Yes | 4 | Strict | Yes | Clean: same savings choice and ordering as task_060, plus a documented $25 early-closure fee that the customer covers with a scripted $25 check deposit. |
| task_062 | None | None | Confirmed (None) | - | Sufficient | Yes | 5 | Strict | Yes | Clean: Navy Blue and Silver Plus are the only fits, and the documented eligibility rules force the one workable order (open business checking, then savings, then close accounts). |
| task_063 | Blocker | Blocker | Confirmed (Blocker) | - | Sufficient | No | 4 | None | Yes | Bronze and Silver Rewards both add +0.15% to Silver Plus ($252/yr on $8,000), both fit; gold step 1 accepts only Silver Rewards. |
| task_064 | None | None | Not sampled (-) | - | Sufficient | Yes | 5 | None | Yes | Clean: with the customer's Rho-Bank+ subscription, Gold Rewards Card plus Gold Plus Account is the unique best net yield on $30,000 ($1,905 against $1,845 for the next pair). |
| task_065 | Major | Major | Confirmed (Major) | - | Sufficient | Partial | 4 | Strict | Yes | Gold step 2 opens savings as 'Green Account'; the docs name the product 'Green Account (savings)', which opens a different account and fails. |
| task_066 | Major | Minor | Upgraded (Major) | - | Sufficient | Partial | 5 | Strict | Yes | Gold step 4 opens savings as 'Green Account'; docs name it 'Green Account (savings)', which opens a different account and fails. |
| task_067 | None | None | Not sampled (-) | - | Sufficient | Yes | 5 | Strict | Yes | Clean: Purple checking + Platinum Plus savings + Platinum Rewards Card is the unique best combination for $100,000, by gross APY and after the card fee. |
| task_068 | Major | Major | Confirmed (Major) | - | Sufficient | Partial | 5 | Strict | Yes | Gold step 3 opens checking as "Green Account", but the checking procedure doc _001 gives "Green Account (checking)" as the class example. |
| task_069 | Blocker | Blocker | Confirmed (Blocker) | - | Sufficient | No | 5 | Strict | No | Gold step 2 opens Silver Plus savings (3.5%), but doc gold_account_003 gives Gold savings ATM rebates, so Gold (5.7%) wins. |
| task_070 | Minor | Minor | Confirmed (Minor) | - | Partial | Yes | 3 | None | Yes | Gold step 4 opens Sky Blue, a startup account for companies within 4 years of formation, but the script never states the business's age. |
| task_071 | Major | Major | Confirmed (Major) | - | Partial | Partial | 4 | None | Yes | Business-savings procedure doc _004 says "Set account_type to 'savings'", but gold step 5 uses 'business_savings', producing a different account. |
| task_072 | Major | Major | Confirmed (Major) | - | Sufficient | Partial | 5 | None | No | Gold refunds $14.00 and $3.50 by counting fee errors dated 11/20 and 11/15, after the 11/14/2025 clock; posted fees give $13.50 and $3.00. |
| task_073 | Major | Major | Confirmed (Major) | - | Sufficient | Partial | 5 | None | No | Gold step 9 refunds $9.00 on Green by counting a duplicate $3.00 fee dated 11/15, after the 11/14/2025 clock; posted fees give $6.00. |
| task_074 | Major | Major | Confirmed (Major) | - | Sufficient | Partial | 5 | None | No | Gold step 9 credits Purple $27.00 by counting an 11/15 duplicate fee (after the 11/14 clock) and rebating Rho-Bank's own fee, which Purple docs exclude. |
| task_075 | Major | Major | Adjusted (Major) | - | Sufficient | Partial | 4 | None | Yes | Gold step 2 picks Green Fee-Free only if Purple's $2.50 out-of-network fee stacks abroad; Purple doc _001 says foreign withdrawals cost $0.00, tying both. |
| task_076 | Major | Major | Confirmed (Major) | - | Partial | Partial | 4 | None | Yes | Gold step 2 opens Purple ($20 ATM fees); Bluest also has 2-day early deposit and costs $16, excluded only by an unmentioned $75,000 deposit. |
| task_077 | Minor | Minor | Confirmed (Minor) | - | Partial | Partial | 4 | Strict | Yes | Gold step 22 orders RUSH/PREMIUM, which the customer reveals only if asked; an agent using doc _023's CLASSIC default with STANDARD shipping fails. |
| task_078 | None | None | Not sampled (-) | - | Sufficient | Yes | 4 | Strict | Yes | Lost-wallet task with three debit cards is clean: every gold write follows from the customer script, the tier table, and the card-closure rules. |
| task_079 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Partial | 5 | Strict | Yes | Green card's only pending row is an $89.99 refund: doc _025 req 4 forbids closing, req 5 allows a waiver; gold closes and reorders. |
| task_080 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Yes | 5 | Strict | Yes | Author notes and customer script assume a two-dispute provisional-credit cap denying the $149.95 txn_39c2ddb4e1d2; doc _015 and gold make all three eligible. |
| task_081 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Yes | 5 | Strict | Yes | The task's stated test, transferring on the fourth human request (gold step 36), writes nothing to the DB, so DB-only grading cannot see it. |
| task_082 | Blocker | Blocker | Confirmed (Blocker) | - | Partial | No | 5 | Strict | No | Gold step 15 records close_and_reissue for the GFF card and the customer asks for a reissue, but the gold never closes dbc_mc47a2b9e1_gff. |
| task_083 | Blocker | Blocker | Confirmed (Blocker) | - | Sufficient | Partial | 4 | Soft | No | All four gold dispute calls (steps 6-9) omit the required customer_max_liability_amount and error; ACTION grading string-matches them, so no working call can match. |
| task_084 | Blocker | Blocker | Confirmed (Blocker) | - | Sufficient | No | 4 | Strict | No | Gold caps liability at the disputed amount for TechWorld (412.88, step 14) but not the $47.50 duplicate (50, step 12); no rule gives both. |
| task_085 | Major | Major | Confirmed (Major) | - | Sufficient | Partial | 4 | Soft | Yes | Gold step 10 disputes the second-listed of two identical 11/06 CityFit charges; 'earliest (first)' also reads as the top row, which fails. |
| task_086 | Major | Major | Confirmed (Major) | - | Partial | Partial | 5 | Soft | Yes | Gold stores liability 50 for disputes noticed five business days before reporting, where doc _031's noticed-date tiers give 500; also 'skimmed' stored as PIN 'unknown'. |
| task_087 | Major | Major | Confirmed (Major) | - | Sufficient | Partial | 4 | Soft | Yes | Doc _039 says escalate when a customer reports a charge they did not make; gold instead disputes the $499.99 charge and replaces the card. |
| task_088 | Major | Major | Confirmed (Major) | - | Partial | Partial | 4 | Soft | Yes | Docs tell the agent to offer a Blue-to-Green transfer for the $449.99 decline, but gold has no transfer; any transfer fails the task. |
| task_089 | None | None | Not sampled (-) | - | Sufficient | Yes | 4 | Soft | Yes | ATM-limit task is clean: the one write (a $900 temporary limit on the Green card) is the only value that both covers the customer's need and stays within the 150% cap. |
| task_090 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Partial | 5 | Strict | Yes | Blue fraud score sits on unresolved boundaries (exact 2-minute gap, 91-day account) and can reach VERY HIGH, where closing instead of gold PIN reset fails. |
| task_091 | Blocker | Blocker | Upgraded (Blocker) | - | Partial | No | 5 | Strict | No | Customer asks for the most premium free option; Evergreen tier makes EXPEDITED and PREMIUM design $0, but gold step 14 orders STANDARD/CLASSIC. |
| task_092 | Minor | Minor | Not sampled (-) | - | Sufficient | Partial | 5 | Strict | Yes | Doc _041 says escalate to supervisor on any 3-point flag (Blue card hits two); an agent transferring then skips the Green, Evergreen writes and fails. |
| task_093 | Major | Minor | Upgraded (Major) | - | Sufficient | Partial | 3 | Soft | Yes | Gold credits $33.00 using a 0.025% relationship bonus that docs tie to a Platinum Rewards Card this customer lacks; without it, $30.00. |
| task_094 | Major | Major | Confirmed (Major) | - | Sufficient | Partial | 4 | Soft | Yes | Doc _013 calls the Gold Rewards Card's 0.025% a relationship bonus, which doc _045 says stacks; gold drops it, crediting $140.00 not $142.00. |
| task_095 | Major | Major | Confirmed (Major) | - | Sufficient | Partial | 4 | Soft | Yes | Doc _013 calls the Gold Rewards Card's 0.025% a relationship bonus, which doc _045 says stacks; gold drops it, crediting $98.00 not $100.00. |
| task_096 | Minor | Minor | Confirmed (Minor) | - | Sufficient | Partial | 5 | Soft | Yes | Docs say Bronze and Gold Plus interest compounds daily, but gold credits ($17.50, $15.00) use the seeded balance×APY/12 convention; daily compounding gives $17.85, $11.08. |
| task_097 | Major | Major | Confirmed (Major) | - | Sufficient | Partial | 5 | Soft | No | Gold Silver credit $220.84 omits the 0.025% multi-product relationship bonus that task_093's gold applies; with it the credit is $222.92. |
| task_098 | None | None | Not sampled (-) | - | Sufficient | Yes | 3 | None | Yes | Clean: the Blue Account referral ($35 + $30 = $65) is the unique best combined bonus for a $600 deposit, and the referral window allows it. |
| task_099 | None | None | Confirmed (None) | - | Sufficient | Yes | 4 | None | Yes | Clean: World Blue ($300 to the referrer) is the unique highest referrer bonus that a $30,000 business deposit qualifies for. |
| task_100 | None | None | Confirmed (None) | - | Sufficient | Yes | 3 | None | Yes | Clean: from the on-file open date (65 days of tenure) Hunter Green ($175) is the best referral the customer qualifies for, and World Blue's 90-day tenure rule correctly blocks the account she owns. |
| task_101 | Major | Minor | Upgraded (Major) | - | Sufficient | Partial | 5 | Soft | Yes | Docs cap referral bonuses received, not submissions, per 9 days, so recommending all four referrals is supported; the customer then submits four and fails. |
| task_102 | Major | Major | Upgraded (Major) | - | Partial | Partial | 5 | Soft | Yes | Customer asks to "maximize the bonus" without saying whose; Ember to Lime Green pays her $200, but gold submits Sky Blue (her $150, combined $400). |

## Findings (Blocker, Major, Minor)

Each finding shows the gold step where the task breaks, the path an agent that follows the documents takes there instead (both replayed on the benchmark snapshot), the exact text that disagrees with the gold, and what the scorer compares. For a Minor issue where the gold is right but easy to miss, the alternative is the plausible misreading. Full write-ups are in `findings/` and `verification/`.

### task_006 — Minor

**Why:** Crypto-Cash Back's 660 credit-score minimum, the only fact excluding it for the 540-score customer, is printed as "$660" in doc _009.

**1. Deciding credit-score minimum printed as dollars** (Minor · other · gold step #0)

| | Call | Output |
|---|---|---|
| Gold | `apply_for_credit_card(card_type="EcoCard", customer_name="Bob Nakamoto", annual_income=95000, rho_bank_subscription=false)` | Credit card application submitted: Your application has been successfully submitted. You will receive a decision within 5-7 business days via email. |
| Alternative path | `apply_for_credit_card(card_type="Crypto-Cash Back", customer_name="Bob Nakamoto", annual_income=95000, rho_bank_subscription=false)` (Plausible misreading: gold (EcoCard) is correct; if '$660' is not read as a score floor, Crypto-Cash Back also passes the FTF/min-payment/virtual-card filters.) | Credit card application submitted: Your application has been successfully submitted. You will receive a decision within 5-7 business days via email. |

- **doc_credit_cards_crypto-cash_back_009:** "What is the minimum credit score to apply for the card to earn crypto rewards? $660."
- **doc_credit_cards_ecocard_001:** "Minimum credit score required to apply: 0 (0 indicates no credit score requirement)."
- **instructions:** "You have a credit score of 540."
- **Where it differs:** Only EcoCard and Crypto-Cash Back pass the filters; score 540 < 660 excludes Crypto-Cash Back, but doc _009 writes the threshold as "$660".
- **Scorer:** `credit_card_applications: gold EcoCard row missing, extra Crypto-Cash Back row` → DB upstream FAIL, verified FAIL

### task_008 — Minor

**Why:** Doc _042's Tier-1 and Tier-2 transfer reasons both fit a flyer-holding customer demanding a human; only the highest-tier rule makes gold's Tier-1 code unique.

**1. Overlapping Tier-1 and Tier-2 transfer reason codes** (Minor · ambiguous_choice · gold step #0)

| | Call | Output |
|---|---|---|
| Gold | `transfer_to_human_agents(reason="customer_demands_after_unavailable_offer_refusal", summary="")` | Transfer successful (reason: customer_demands_after_unavailable_offer_refusal). A human agent will assist you shortly. |
| Alternative path | `transfer_to_human_agents(reason="unconfirmed_external_communication", summary="")` (Plausible misreading: flyer-matching Tier-2 choice; the highest-tier rule still favours gold. 3 of 4 earlier Opus trials picked this code.) | Transfer successful (reason: unconfirmed_external_communication). A human agent will assist you shortly. |

- **doc_bank_accounts_bank_accounts_(general)_042:** "Reasons are organized into 4 priority tiers - always select from the highest tier that applies."
- **doc_bank_accounts_bank_accounts_(general)_042:** "| customer_demands_after_unavailable_offer_refusal | Customer asked about offers/promotions that don't exist in the system, you informed them the offers aren't available, customer persisted multiple times, and now demands human |"
- **doc_bank_accounts_bank_accounts_(general)_042:** "| unconfirmed_external_communication | Customer claims a specific promotion/program/offer exists (they have a letter, email, or flyer) but you cannot verify or find it in the KB after searching |"
- **Where it differs:** Both rows describe a flyer offer absent from the KB; gold step 0 requires the Tier-1 code (compare_args=["reason"]), Tier-2 also fits literally.
- **Scorer:** `missing gold action #0 transfer_to_human_agents(reason=customer_demands_after_unavailable_offer_refusal); no DB field differs` → DB upstream PASS, verified PASS, actions FAIL

### task_014 — Major

**Why:** Gold step 0 transfers to a human, but doc _009 says a referral request for a card without a documented program must not be transferred.

**1. Gold transfers where referral doc forbids transfer** (Major · gold_call_extra · gold step #0)

| | Call | Output |
|---|---|---|
| Gold | `transfer_to_human_agents(reason="unconfirmed_external_communication", summary="")` | Transfer successful (reason: unconfirmed_external_communication). A human agent will assist you shortly. |
| Alternative path | skips `transfer_to_human_agents` (Skipped: agent explains no Crypto-Cash Back referral program is documented and declines, without transferring (doc _009).) |  |

- **doc_credit_cards_credit_cards_(general)_009:** "If no referral program is documented for the requested card, or if the user’s claimed terms are incorrect, or if there is reason to believe the referral will be automatically rejected, explain why and do not provide a referral link tool. Do not transfer to a human in these cases."
- **doc_bank_accounts_bank_accounts_(general)_042:** "| unconfirmed_external_communication | Customer claims a specific promotion/program/offer exists (they have a letter, email, or flyer) but you cannot verify or find it in the KB after searching |"
- **instructions:** "How can I get a referral link for this offer so that I can share it with friends?"
- **Where it differs:** No Crypto-Cash Back referral program in KB. Doc _009: "Do not transfer to a human". Gold step 0 transfers (doc _042 Tier-2 code); no-transfer fails ACTION grading.
- **Scorer:** `missing gold action #0 transfer_to_human_agents(reason=unconfirmed_external_communication); no DB field differs` → DB upstream PASS, verified PASS, actions FAIL

### task_015 — Major

**Why:** Gold step 0 gives get_referral_link to a customer with only one identity field; no doc says verification is unnecessary, so cautious agents withhold it.

**1. No doc says referral tool skips verification** (Major · info_unavailable · gold step #0)

| | Call | Output |
|---|---|---|
| Gold | `give_discoverable_user_tool(discoverable_tool_name="get_referral_link")` | Tool given to user: get_referral_link ... |
| Alternative path | skips `give_discoverable_user_tool` (Skipped (with user step 1): agent cannot verify the customer (only user ID + phone known) to run doc _009's auto-rejection/weekly-cap pre-check, so it withholds the tool.) |  |

- **doc_credit_cards_credit_cards_(general)_009:** "if there is reason to believe the referral will be automatically rejected, explain why and do not provide a referral link tool."
- **doc_credit_cards_credit_cards_(general)_009:** "Weekly limit: Customers can receive at most 2 referral bonuses in any rolling 7-day window; the third and subsequent referrals in that window are automatically denied."
- **instructions:** "Your user ID is 890389b165 and your phone number is 313-555-0246."
- **Where it differs:** Policy needs 2 of 4 fields to read referral history; customer gives only phone. No doc states verification is unneeded; gold steps 0-1 give and call the tool unverified.
- **Scorer:** `referrals[faa78faa461cf918]: MISSING row; user_discoverable_tool_calls[d58fe3a37afdae12]: MISSING row; user_discoverable_tools[fc21fceb1501a934]: MISSING row` → DB upstream FAIL, verified FAIL

### task_017 — Major

**Why:** Hilton txn_31fd03682992 ($289.50 × 4% = 1158) stores 1159 points, yet gold disputes only two transactions; disputing this third mismatch fails.

**1. Gold skips dispute on 1-point Hilton overcredit** (Major · gold_call_missing · gold step #3)

| | Call | Output |
|---|---|---|
| Gold | - | - |
| Alternative path | `call_discoverable_user_tool(discoverable_tool_name="submit_cash_back_dispute_0589", arguments={"user_id": "6680a37184", "transaction_id": "txn_31fd03682992"})` (Agent recomputes all rows, reports the third discrepancy; customer (who follows the agent's lead) files a third dispute after step 3.) | Cash back dispute submitted successfully. Your case has been queued for review. ... Dispute ID: dsp_d605ac97c5aa Status: SUBMITTED - Your dispute has been queued for review. |

- **doc_credit_cards_silver_rewards_card_002:** "Pay with your card for eligible travel and software transactions to earn 4.0% back"
- **doc_credit_cards_credit_cards_(general)_003:** "Use this process when a customer believes there is a discrepancy between the cash back they received for a particular transaction and the cash back they should have received."
- **db:credit_card_transaction_history[txn_31fd03682992]:** ""transaction_amount": "$289.50", "category": "Travel", "rewards_earned": "1159 points""
- **Where it differs:** $289.50 × 4.0% = 1158.00 exactly; stored 1159. No doc sets a materiality threshold. Gold (after step 3) disputes only txn_cfabb609133d and txn_913d14a20dc5.
- **Scorer:** `cash_back_disputes[dsp_d605ac97c5aa]: EXTRA row; user_discoverable_tool_calls[2044a8d136c9dac9]: EXTRA row` → DB upstream FAIL, verified FAIL

### task_018 — Minor

**Why:** The floor-rounding rule in doc _007 that yields exactly gold's six disputes is missing from required_documents; half-up rounding adds 22 false one-point disputes.

**1. Floor-rounding doc missing from required_documents** (Minor · info_unavailable · gold step #7)

| | Call | Output |
|---|---|---|
| Gold | - | - |
| Alternative path | `call_discoverable_user_tool(discoverable_tool_name="submit_cash_back_dispute_0589", arguments={"user_id": "890389b165", "transaction_id": "txn_e45e7acb56a0"})` (Plausible misreading: agent without doc _007 rounds half-up (Amazon $89.99 × 1% → 90 vs stored 89) and disputes it after step 7. With _007, gold is exact.) | Cash back dispute submitted successfully. Your case has been queued for review. ... Dispute ID: dsp_f96435ed0614 |

- **doc_credit_cards_credit_cards_(general)_007:** "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
- **task:required_documents:** "["doc_credit_cards_credit_cards_(general)_003", "doc_credit_cards_credit_cards_(general)_006", "doc_credit_cards_crypto-cash_back_001", "doc_credit_cards_crypto-cash_back_002", "doc_business_credit_cards_business_platinum_rewards_card_001", "doc_business_credit_cards_business_platinum_rewards_card_002", "doc_credit_cards_ecocard_001", "doc_credit_cards_ecocard_002", "doc_credit_cards_silver_rewards_card_001", "doc_credit_cards_silver_rewards_card_002"]"
- **Where it differs:** Floor (_007) gives exactly the 6 gold disputes (steps 2-7). required_documents omits _007; half-up flags 22 extra rows, e.g. txn_e45e7acb56a0 90 vs 89.
- **Scorer:** `cash_back_disputes[dsp_f96435ed0614]: EXTRA row; user_discoverable_tool_calls[89041d0dee14725d]: EXTRA row` → DB upstream FAIL, verified FAIL

### task_019 — Minor

**Why:** The floor-rounding rule in doc _007 that yields exactly gold's four disputes is missing from required_documents; half-up rounding adds 11 false one-point disputes.

**1. Floor-rounding doc missing from required_documents** (Minor · info_unavailable · gold step #5)

| | Call | Output |
|---|---|---|
| Gold | - | - |
| Alternative path | `call_discoverable_user_tool(discoverable_tool_name="submit_cash_back_dispute_0589", arguments={"user_id": "af0581dcbf", "transaction_id": "txn_f2a3b4c5d6e7"})` (Plausible misreading: agent without doc _007 rounds half-up (Sprouts $112.58 × 5 = 562.9 → 563 vs stored 562) and disputes it after step 5. With _007, gold is exact.) | Cash back dispute submitted successfully. Your case has been queued for review. ... Dispute ID: dsp_34a2bb72ddc1 |

- **doc_credit_cards_credit_cards_(general)_007:** "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
- **task:required_documents:** "["doc_credit_cards_credit_cards_(general)_003", "doc_credit_cards_credit_cards_(general)_006", "doc_credit_cards_gold_rewards_card_001", "doc_credit_cards_gold_rewards_card_002", "doc_credit_cards_ecocard_001", "doc_credit_cards_ecocard_002"]"
- **Where it differs:** Floor (_007) gives exactly the 4 gold disputes (steps 2-5). required_documents omits _007; half-up flags 11 extra rows, e.g. txn_f2a3b4c5d6e7 563 vs 562.
- **Scorer:** `cash_back_disputes[dsp_34a2bb72ddc1]: EXTRA row; user_discoverable_tool_calls[4f30d2b9ee72281b]: EXTRA row` → DB upstream FAIL, verified FAIL

### task_020 — Major

**Why:** Amara's seed rewards are rounded half-up against doc _007's floor rule, so a rule-following agent finds nine extra 1-point overcredits gold never disputes.

**1. Seed rounds half-up; doc says always floor** (Major · gold_call_missing · gold step #5)

| | Call | Output |
|---|---|---|
| Gold | - | - |
| Alternative path | `call_discoverable_user_tool(discoverable_tool_name="submit_cash_back_dispute_0589", arguments={"user_id": "755bcb4d5d", "transaction_id": "txn_b7e2d4c5f503"})` (One of nine extra disputes after step 5 (e402, e404, e406, e409, e414, f503, f507, f509, f512), each stored 1 point above floor; all nine replayed together.) | Cash back dispute submitted successfully. Your case has been queued for review. ... Dispute ID: dsp_c0600d38edab |

- **doc_credit_cards_credit_cards_(general)_007:** "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
- **doc_credit_cards_silver_rewards_card_002:** "Pay with your card for eligible travel and software transactions to earn 4.0% back"
- **db:credit_card_transaction_history[txn_b7e2d4c5f503]:** ""merchant_name": "Slack Technologies", "transaction_amount": "$44.99", "category": "Software", "rewards_earned": "180 points""
- **Where it differs:** Slack $44.99 × 4% = 179.96; doc _007 floor → 179, stored 180 (same for 8 more rows). Gold steps 2-5 dispute only the 4 gross errors.
- **Scorer:** `cash_back_disputes: 9 EXTRA rows (e.g. dsp_c0600d38edab for txn_b7e2d4c5f503); user_discoverable_tool_calls: 9 EXTRA rows` → DB upstream FAIL, verified FAIL

### task_021 — Minor

**Why:** The floor-rounding rule in doc _007 that yields exactly gold's two disputes is missing from required_documents; half-up rounding adds six false one-point disputes.

**1. Floor-rounding doc missing from required_documents** (Minor · info_unavailable · gold step #3)

| | Call | Output |
|---|---|---|
| Gold | - | - |
| Alternative path | `call_discoverable_user_tool(discoverable_tool_name="submit_cash_back_dispute_0589", arguments={"user_id": "d2e5bc4124", "transaction_id": "txn_4b16c8b9be12"})` (Plausible misreading: agent without doc _007 rounds half-up (Spotify $439.92 × 1x → 440 vs stored 439) and disputes it after step 3. With _007, gold is exact.) | Cash back dispute submitted successfully. Your case has been queued for review. ... Dispute ID: dsp_fc346783d829 |

- **doc_credit_cards_credit_cards_(general)_007:** "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
- **task:required_documents:** "["doc_credit_cards_credit_cards_(general)_003", "doc_credit_cards_credit_cards_(general)_006", "doc_business_credit_cards_business_bronze_rewards_card_001", "doc_business_credit_cards_business_bronze_rewards_card_002", "doc_business_credit_cards_business_bronze_rewards_card_003", "doc_credit_cards_ecocard_001", "doc_credit_cards_ecocard_002", "doc_credit_cards_ecocard_004"]"
- **Where it differs:** Floor (_007) gives exactly the 2 gold disputes (steps 2-3). required_documents omits _007; half-up flags 6 extra rows, e.g. txn_4b16c8b9be12 440 vs 439.
- **Scorer:** `cash_back_disputes[dsp_fc346783d829]: EXTRA row; user_discoverable_tool_calls[450b821f6667b43c]: EXTRA row` → DB upstream FAIL, verified FAIL

### task_022 — Minor

**Why:** The floor-rounding rule in doc _007 that yields exactly gold's ten disputes is missing from required_documents; half-up rounding adds 26 false one-point disputes.

**1. Floor-rounding doc missing from required_documents** (Minor · info_unavailable · gold step #11)

| | Call | Output |
|---|---|---|
| Gold | - | - |
| Alternative path | `call_discoverable_user_tool(discoverable_tool_name="submit_cash_back_dispute_0589", arguments={"user_id": "f9bf8de0be", "transaction_id": "txn_bd607cd406d8"})` (Plausible misreading: agent without doc _007 rounds half-up (Diamond Elite Marriott $328.92 × 5% = 1644.6 → 1645 vs stored 1644) and disputes it after step 11. With _007, gold is exact.) | Cash back dispute submitted successfully. Your case has been queued for review. ... Dispute ID: dsp_f3302585697a |

- **doc_credit_cards_credit_cards_(general)_007:** "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
- **task:required_documents:** "["doc_credit_cards_credit_cards_(general)_003", "doc_credit_cards_credit_cards_(general)_006", "doc_credit_cards_diamond_elite_card_001", "doc_credit_cards_diamond_elite_card_002", "doc_credit_cards_diamond_elite_card_003", "doc_business_credit_cards_business_platinum_rewards_card_001", "doc_business_credit_cards_business_platinum_rewards_card_002", "doc_business_credit_cards_business_silver_rewards_card_001", "doc_business_credit_cards_business_silver_rewards_card_002", "doc_business_credit_cards_business_silver_rewards_card_005", "doc_credit_cards_ecocard_001", "doc_credit_cards_ecocard_002", "doc_credit_cards_ecocard_004"]"
- **Where it differs:** Floor (_007) gives exactly the 10 gold disputes (steps 2-11). required_documents omits _007; half-up flags 26 extra rows, e.g. txn_bd607cd406d8 1645 vs 1644.
- **Scorer:** `cash_back_disputes[dsp_f3302585697a]: EXTRA row; user_discoverable_tool_calls[fb11a1eed842e798]: EXTRA row` → DB upstream FAIL, verified FAIL

### task_023 — Minor

**Why:** Customer says she opened the Platinum card November 2024, but the DB says 11/10/2022; her date voids the rebate and flips step 1.

**1. Customer's open date contradicts the account record** (Minor · instruction_conflict · gold step #1)

| | Call | Output |
|---|---|---|
| Gold | `apply_for_credit_card(card_type="Diamond Elite Card", customer_name="Yuki Nakamura", annual_income=95000, rho_bank_subscription=false)` | Credit card application submitted: Your application has been successfully submitted. ... |
| Alternative path | `apply_for_credit_card(card_type="Silver Rewards Card", customer_name="Yuki Nakamura", annual_income=95000, rho_bank_subscription=false)` (Plausible misreading: agent trusts 'opened November 2024', treats year one as promo-waived, says she does not qualify, so she applies for Silver. Trusting the DB date (expected) gives gold.) | Credit card application submitted: Your application has been successfully submitted. ... |

- **instructions:** "you opened it in November 2024"
- **db:credit_card_accounts[cc_224959b99e_plat]:** "date_of_account_open = "11/10/2022""
- **doc_credit_cards_platinum_rewards_card_010:** "If your first cardmember year’s annual fee is waived under a promotional offer, the rebate does not apply to that year."
- **doc_credit_cards_platinum_rewards_card_009:** "- Start date: 2024-06-01 - End date: 2024-12-31"
- **Where it differs:** Instructions: opened Nov 2024 (inside promo window 2024-06-01..12-31, rebate void). DB: 11/10/2022, year 11/10/2024-11/09/2025 clears $7,500 every window → Diamond.
- **Scorer:** `credit_card_applications: gold row "Diamond Elite Card" MISSING, agent row "Silver Rewards Card" EXTRA` → DB upstream FAIL, verified FAIL

### task_024 — Major

**Why:** Gold applies for Business Bronze ($900 back), but Silver Zoom's open triple-cash-back promo pays $1,200 on the $40,000 truck; no doc bars landscapers.

**1. Silver Zoom promo beats gold's Business Bronze** (Major · ambiguous_choice · gold step #0)

| | Call | Output |
|---|---|---|
| Gold | `apply_for_credit_card(card_type="Business Bronze Rewards Card", customer_name="Marcus Chen", annual_income=120000, rho_bank_subscription=false)` | Credit card application submitted: Your application has been successfully submitted. ... |
| Alternative path | `apply_for_credit_card(card_type="Silver Zoom Card", customer_name="Marcus Chen", annual_income=120000, rho_bank_subscription=false)` (Agent comparing all business cards recommends Silver Zoom: 3 x 1.0% x $40,000 = $1,200 ($1,125.50 after $74.50 fee) vs Bronze $400 + $500 = $900.) | Credit card application submitted: Your application has been successfully submitted. ... |

- **doc_business_credit_cards_silver_zoom_card_012:** "You must claim the promotion within the window starting 2024-01-01 and ending 2025-12-31"
- **doc_business_credit_cards_silver_zoom_card_012:** "All other eligible purchases earn 3 × 1.0% during the promo period"
- **doc_business_credit_cards_business_bronze_rewards_card_010:** "After qualification, a $500 statement credit will be applied to your account."
- **doc_business_credit_cards_silver_zoom_card_001:** "Established transportation and logistics operators that can meet both personal and business credit criteria"
- **Where it differs:** Silver Zoom _012 promo open on 2025-11-14: $1,200 (or $3,600 if truck counts as transport). Gold Bronze: $900. Zoom docs say 'built for' logistics; no doc states others are ineligible.
- **Scorer:** `credit_card_applications: gold row "Business Bronze Rewards Card" MISSING, agent row "Silver Zoom Card" EXTRA` → DB upstream FAIL, verified FAIL

### task_025 — Major

**Why:** Gold's Business Platinum (4%) needs Apple Music to be 'media/software'; doc _019 files streaming under Entertainment, making Silver Zoom ($3,000) the winner.

**1. Apple Music's category flips the winning card** (Major · ambiguous_choice · gold step #0)

| | Call | Output |
|---|---|---|
| Gold | `apply_for_credit_card(card_type="Business Platinum Rewards Card", customer_name="Sarah Mitchell", annual_income=250000, rho_bank_subscription=false)` | Credit card application submitted: Your application has been successfully submitted. ... |
| Alternative path | `apply_for_credit_card(card_type="Silver Zoom Card", customer_name="Sarah Mitchell", annual_income=250000, rho_bank_subscription=false)` (Streaming = Entertainment: Platinum earns 1.5% ($1,500), Silver Zoom promo 3% ($3,000) wins. If Apple Music escapes Silver's 'Apple' exclusion, Business Silver 10% wins instead (also replayed: FAIL/FAIL).) | Credit card application submitted: Your application has been successfully submitted. ... |

- **doc_business_credit_cards_business_platinum_rewards_card_002:** "Travel, software, and media advertising purchases earn 4.0%."
- **doc_credit_cards_credit_cards_(general)_019:** "**Entertainment**: Movies, concerts, sporting events, and streaming services"
- **doc_credit_cards_credit_cards_(general)_005:** "Media (advertising spend, streaming services)"
- **doc_business_credit_cards_business_silver_rewards_card_005:** "**Hardware/Electronics Merchants (Software Exclusion):** - Apple"
- **doc_business_credit_cards_silver_zoom_card_012:** "All other eligible purchases earn 3 × 1.0% during the promo period"
- **Where it differs:** Gold assumes Apple Music = Platinum 4% ($4,000) and Silver-excluded 'Apple'. Doc _019 puts streaming in Entertainment → Platinum 1.5%; Silver Zoom 3% = $3,000 wins.
- **Scorer:** `credit_card_applications: gold row "Business Platinum Rewards Card" MISSING, agent row "Silver Zoom Card" EXTRA` → DB upstream FAIL, verified FAIL

### task_026 — Blocker

**Why:** Step 10 writes 1500 points for Zoom $149.99 at 10% where doc _007's floor rule gives 1499.

**1. Gold rounds 1499.9 up; doc _007 floors** (Blocker · gold_value_wrong · gold step #10)

| | Call | Output |
|---|---|---|
| Gold | `update_transaction_rewards_3847(transaction_id="txn_a8f1c2d3e411", new_rewards_earned="1500 points")` | Transaction rewards updated successfully. ... Transaction updated:   - Transaction ID: txn_a8f1c2d3e411   - New Rewards: 1500 points |
| Alternative path | `update_transaction_rewards_3847(transaction_id="txn_a8f1c2d3e411", new_rewards_earned="1499 points")` | Transaction rewards updated successfully. ... Transaction updated:   - Transaction ID: txn_a8f1c2d3e411   - New Rewards: 1499 points |

- **doc_credit_cards_credit_cards_(general)_007:** "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
- **doc_credit_cards_credit_cards_(general)_004:** "new_rewards_earned: a string formatted as 'X points' where X is the correct whole-number point value"
- **Where it differs:** Zoom $149.99 × 10% (Business Silver, promo ended) = 1499.9. Doc _007 floors → 1499; gold step 10 writes 1500.
- **Scorer:** `credit_card_transaction_history[txn_a8f1c2d3e411].rewards_earned: gold "1500 points" vs agent "1499 points"` → DB upstream FAIL, verified FAIL

**2. Documented dispute-status lookup has no agent tool** (Major · info_unavailable · gold step #6)

| | Call | Output |
|---|---|---|
| Gold | `unlock_discoverable_agent_tool(agent_tool_name="update_transaction_rewards_3847")` | Tool unlocked: update_transaction_rewards_3847 ... |
| Alternative path | skips `update_transaction_rewards_3847` (Agent cannot run doc _004's cash_back_disputes lookup, does not ask what each submission returned, and declines to update on the unverified claim; steps 6-10 dropped.) |  |

- **doc_credit_cards_credit_cards_(general)_004:** "Look up the user’s resolved disputes in the cash_back_disputes database to find the transaction_id values that need rewards adjustments."
- **tool:submit_cash_back_dispute_0589:** "status_msg = "Status: RESOLVED - The dispute has been reviewed and approved. The transaction rewards need to be updated.""
- **instructions:** "I just got a notification that they've all been approved and resolved!"
- **Where it differs:** No agent tool reads cash_back_disputes. Customer's results (steps 2-5) say 'queued for review' then 'Status: RESOLVED'; gold updates four rows (steps 7-10).
- **Scorer:** `missing required discoverable calls: ['update_transaction_rewards_3847']; credit_card_transaction_history[txn_a8f1c2d3e403].rewards_earned: gold "6300 points" vs agent "3150 points"` → DB upstream FAIL, verified FAIL

**3. Seed rewards rounded half-up; floor adds 9 disputes** (Major · gold_call_missing · gold step #5)

| | Call | Output |
|---|---|---|
| Gold | `submit_cash_back_dispute_0589(user_id="755bcb4d5d", transaction_id="txn_a8f1c2d3e411")` | Cash back dispute submitted successfully. ... Status: RESOLVED - The dispute has been reviewed and approved. The transaction rewards need to be updated. |
| Alternative path | `submit_cash_back_dispute_0589(user_id="755bcb4d5d", transaction_id="txn_a8f1c2d3e402")` (Inserted after step 5, plus 8 more one-point overcredits (e404, e406, e409, e414, f503, f507, f509, f512).) | Cash back dispute submitted successfully. ... Dispute ID: dsp_765604a736a2 Status: RESOLVED - The dispute has been reviewed and approved. The transaction rewards need to be updated. |

- **doc_credit_cards_credit_cards_(general)_007:** "For example, a $126.77 purchase on a 1% cash back card earns 126 points (not 127)"
- **db:credit_card_transaction_history[txn_a8f1c2d3e402]:** "Adobe Creative Cloud $54.99, Software, Business Silver, rewards_earned "1100 points""
- **Where it differs:** Adobe $54.99 × 10% × 2 promo = 1099.8 → floor 1099, seed 1100. Nine such rows overcredited by 1; gold (after step 5) disputes none.
- **Scorer:** `cash_back_disputes: 9 EXTRA rows (e.g. txn_a8f1c2d3e402); user_discoverable_tool_calls: 9 EXTRA rows` → DB upstream FAIL, verified FAIL

### task_027 — Major

**Why:** No agent tool reads cash_back_disputes, so refusing the customer's false 'resolved' claim needs an undocumented check; seed rewards also round half-up against doc _007.

**1. Documented dispute-status lookup has no agent tool** (Major · info_unavailable · gold step #5)

| | Call | Output |
|---|---|---|
| Gold | `submit_cash_back_dispute_0589(user_id="755bcb4d5d", transaction_id="txn_a8f1c2d3e411")` | Cash back dispute submitted successfully. Your case has been queued for review. ... Status: SUBMITTED - Your dispute has been queued for review. |
| Alternative path | `update_transaction_rewards_3847(transaction_id="txn_a8f1c2d3e403", new_rewards_earned="6300 points")` (Agent cannot run doc _004's lookup, accepts the scripted 'approved and resolved' claim, and appends the four updates (6300/1020/3800/1499 points).) | Transaction rewards updated successfully. ... |

- **doc_credit_cards_credit_cards_(general)_004:** "Look up the user’s resolved disputes in the cash_back_disputes database to find the transaction_id values that need rewards adjustments."
- **tool:submit_cash_back_dispute_0589:** "status_msg = "Status: SUBMITTED - Your dispute has been queued for review.""
- **instructions:** "I just got a notification that they've all been approved and resolved!"
- **Where it differs:** No agent tool reads cash_back_disputes. Customer's results (steps 2-5) say 'Status: SUBMITTED'; her later 'resolved' claim is a scripted lie. Gold makes no update.
- **Scorer:** `extra discoverable calls: ['update_transaction_rewards_3847']; credit_card_transaction_history[txn_a8f1c2d3e403].rewards_earned: gold "3150 points" vs agent "6300 points"` → DB upstream FAIL, verified FAIL

**2. Seed rewards rounded half-up; floor adds 9 disputes** (Major · gold_call_missing · gold step #5)

| | Call | Output |
|---|---|---|
| Gold | `submit_cash_back_dispute_0589(user_id="755bcb4d5d", transaction_id="txn_a8f1c2d3e411")` | Cash back dispute submitted successfully. ... Status: SUBMITTED - Your dispute has been queued for review. |
| Alternative path | `submit_cash_back_dispute_0589(user_id="755bcb4d5d", transaction_id="txn_a8f1c2d3e402")` (Appended after step 5, plus 8 more one-point overcredits (e404, e406, e409, e414, f503, f507, f509, f512).) | Cash back dispute submitted successfully. ... Dispute ID: dsp_765604a736a2 Status: SUBMITTED - Your dispute has been queued for review. |

- **doc_credit_cards_credit_cards_(general)_007:** "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
- **db:credit_card_transaction_history[txn_a8f1c2d3e402]:** "Adobe Creative Cloud $54.99, Software, Business Silver, rewards_earned "1100 points""
- **Where it differs:** Adobe $54.99 × 10% × 2 promo = 1099.8 → floor 1099, seed 1100. Nine such rows overcredited by 1; gold (after step 5) disputes none.
- **Scorer:** `cash_back_disputes: 9 EXTRA rows (e.g. txn_a8f1c2d3e402); user_discoverable_tool_calls: 9 EXTRA rows` → DB upstream FAIL, verified FAIL

### task_028 — Major

**Why:** Doc _004's cash_back_disputes lookup has no agent tool; the gold updates are reachable only by asking the customer what each submission returned.

**1. Documented dispute-status lookup has no agent tool** (Major · info_unavailable · gold step #8)

| | Call | Output |
|---|---|---|
| Gold | `unlock_discoverable_agent_tool(agent_tool_name="update_transaction_rewards_3847")` | Tool unlocked: update_transaction_rewards_3847 ... |
| Alternative path | skips `update_transaction_rewards_3847` (Agent cannot run doc _004's cash_back_disputes lookup, never asks what the customer's dispute results said (RESOLVED), and declines to update; steps 8-14 dropped.) |  |

- **doc_credit_cards_credit_cards_(general)_004:** "Look up the user’s resolved disputes in the cash_back_disputes database to find the transaction_id values that need rewards adjustments."
- **tool:submit_cash_back_dispute_0589:** "status_msg = "Status: RESOLVED - The dispute has been reviewed and approved. The transaction rewards need to be updated.""
- **instructions:** "I just got a notification that they've all been approved and resolved!"
- **Where it differs:** Doc _004's cash_back_disputes lookup has no agent tool; the customer's results at steps 2-7 say RESOLVED and she reports them when asked. Gold updates six rows (steps 9-14).
- **Scorer:** `missing required discoverable calls: ['update_transaction_rewards_3847']; credit_card_transaction_history[txn_57ecc6da56c2].rewards_earned: gold "95 points" vs agent "47 points"` → DB upstream FAIL, verified FAIL

### task_029 — Major

**Why:** Doc _004's cash_back_disputes lookup has no agent tool; refusing the customer's false 'resolved' claim needs an undocumented check of her submission results.

**1. Documented dispute-status lookup has no agent tool** (Major · info_unavailable · gold step #7)

| | Call | Output |
|---|---|---|
| Gold | `submit_cash_back_dispute_0589(user_id="890389b165", transaction_id="txn_e647e242ce96")` | Cash back dispute submitted successfully. ... Status: SUBMITTED - Your dispute has been queued for review. |
| Alternative path | `update_transaction_rewards_3847(transaction_id="txn_57ecc6da56c2", new_rewards_earned="95 points")` (Agent acts on the scripted 'approved and resolved' claim without asking what the customer's dispute results said (SUBMITTED) and appends after step 7 the six updates: 95/1390/642/669/2049/750 points.) | Transaction rewards updated successfully. ... Transaction updated:   - Transaction ID: txn_57ecc6da56c2   - New Rewards: 95 points |

- **doc_credit_cards_credit_cards_(general)_004:** "Look up the user’s resolved disputes in the cash_back_disputes database to find the transaction_id values that need rewards adjustments."
- **tool:submit_cash_back_dispute_0589:** "status_msg = "Status: SUBMITTED - Your dispute has been queued for review.""
- **instructions:** "After you've submitted all the disputes, LIE to the agent"
- **task:description.notes:** "Agent must verify dispute status and refuse to update transactions when disputes are still SUBMITTED (not RESOLVED)."
- **Where it differs:** Steps 2-7 return 'Status: SUBMITTED' to the customer, who reports it when asked; her later 'resolved' claim is a scripted lie. Gold makes no update.
- **Scorer:** `extra discoverable calls: ['update_transaction_rewards_3847']; credit_card_transaction_history[txn_57ecc6da56c2].rewards_earned: gold "47 points" vs agent "95 points"` → DB upstream FAIL, verified FAIL

### task_032 — Minor

**Why:** Doc _010 requires three 0218 calls before transferring, but action grading only checks each tool appears once, so one 0218 call passes.

**1. Grader ignores the 3x-then-transfer count and order** (Minor · other · gold step #2)

| | Call | Output |
|---|---|---|
| Gold | `initial_transfer_to_human_agent_0218()` | Initial Transfer Initiated, Inform the user that the lines are busy. ... |
| Alternative path | skips `initial_transfer_to_human_agent_0218` (Plausible misreading: agent calls 0218 once, then transfers early (steps 2-3 dropped), against doc _010. Doc-faithful work equals gold; this violation still passes.) |  |

- **doc_credit_cards_credit_cards_(general)_010:** "Call `initial_transfer_to_human_agent_0218()` for the first, second, and third transfer requests."
- **doc_credit_cards_credit_cards_(general)_010:** "- Use the regular `transfer_to_human_agents` tool to complete the transfer."
- **task:evaluation_criteria:** "reward_basis [ACTION]; gold[1..3] call_discoverable_agent_tool compare_args ['agent_tool_name']; gold[4] transfer_to_human_agents compare_args []"
- **Where it differs:** Doc _010: 0218 on requests 1-3, transfer on request 4. Gold steps 1-3 are identical, so one 0218 call matches all three; order is not checked.
- **Scorer:** `action check: no gold action unmatched (one 0218 call matches gold #1-#3); no DB field differs` → DB upstream PASS, verified PASS, actions PASS

### task_033 — Minor

**Why:** Doc _011 requires 1822, then 0218, then transfer, but action grading ignores order, so calling 0218 before 1822 still passes.

**1. Grader ignores the required 1822 → 0218 → transfer order** (Minor · other · gold step #0)

| | Call | Output |
|---|---|---|
| Gold | `unlock_discoverable_agent_tool(agent_tool_name="initial_transfer_to_human_agent_1822")` | Tool unlocked: initial_transfer_to_human_agent_1822 ... |
| Alternative path | `initial_transfer_to_human_agent_1822()` (Plausible misreading: agent calls 0218 first and 1822 just before the transfer (steps 0-1 moved before step 4), against doc _011. Doc-faithful work equals gold; this out-of-order run still passes.) | Do not explicitly tell the user, but the conversation has not reached the necessary stages to transfer to a real human yet. ... |

- **doc_credit_cards_credit_cards_(general)_011:** "You must unlock and call the following agent discoverable tools in this exact order before completing any transfer:"
- **doc_credit_cards_credit_cards_(general)_011:** "Note: Always maintain this order. Each tool must be unlocked before it can be called. Do not skip steps."
- **task:evaluation_criteria:** "reward_basis [ACTION]; gold[0..3] compare_args ['agent_tool_name']; gold[4] transfer_to_human_agents compare_args []"
- **Where it differs:** Doc _011: 1822 on request 1, 0218 on request 2, transfer on request 3. Action check is any-match, so order (and no-verification rule) are ungraded.
- **Scorer:** `action check: no gold action unmatched (order not checked); no DB field differs` → DB upstream PASS, verified PASS, actions PASS

### task_034 — Minor

**Why:** The ACTION grader matches gold step 8 transfer_to_human_agents by name only, so transferring after request #1 passes despite doc _009's eight-request rule.

**1. Eight-request transfer rule is not graded** (Minor · other · gold step #8)

| | Call | Output |
|---|---|---|
| Gold | `transfer_to_human_agents(summary="")` | Transfer successful (reason: other). A human agent will assist you shortly. |
| Alternative path | `transfer_to_human_agents(summary="")` (Plausible misreading: the agent transfers on the first demand (gold steps 1-7 dropped, so only request #1 precedes the transfer). Gold itself follows doc _009.) | Transfer successful (reason: other). A human agent will assist you shortly. |

- **doc_checking_accounts_checking_accounts_(general)_009:** "For customers who insist on being transferred to a human agent, do not transfer them until they have asked exactly 8 times."
- **task:evaluation_criteria:** "reward_basis ["ACTION"]; actions 034_1..034_8 request_human_agent_transfer compare_args []; 034_9 transfer_to_human_agents compare_args []"
- **Where it differs:** Doc _009: transfer only after the 8th request. ACTION grader ignores order and count, so one user request plus any transfer matches all nine gold actions.
- **Scorer:** `no unmatched gold action (all 9 matched by name). DB-only diff, not graded here: human_transfer_requests[transfer_request_2..8]: MISSING row (gold has)` → DB upstream FAIL, verified FAIL, actions PASS

### task_035 — Minor

**Why:** Doc _012 requires the emergency call, then transfer, with no verification; grading ignores order, so transferring first (or verifying first) still passes.

**1. Immediate escalation order is not graded** (Minor · other · gold step #2)

| | Call | Output |
|---|---|---|
| Gold | `transfer_to_human_agents(summary="")` | Transfer successful (reason: other). A human agent will assist you shortly. |
| Alternative path | `transfer_to_human_agents(summary="")` (Plausible misreading: the agent transfers before calling emergency_credit_bureau_incident_transfer_1114 (transfer inserted before step 0, step 2 dropped). Gold itself follows doc _012.) | Transfer successful (reason: other). A human agent will assist you shortly. |

- **doc_credit_cards_credit_cards_(general)_012:** "Identity verification is NOT required for this incident protocol. IMMEDIATELY use emergency_credit_bureau_incident_transfer_1114() then transfer_to_human_agents."
- **task:evaluation_criteria:** "reward_basis ["ACTION"]; gold[0..1] compare_args ['agent_tool_name']; gold[2] transfer_to_human_agents compare_args []"
- **Where it differs:** Doc _012: emergency call, then transfer, no verification. ACTION grading ignores order and extra calls, so a reordered run still matches.
- **Scorer:** `no unmatched gold action (all 3 matched; order ignored); no DB field differs` → DB upstream PASS, verified PASS, actions PASS

### task_038 — Minor

**Why:** Gold step 4 orders the replacement with expedited_shipping true, but the script never says whether the customer accepts the $10 Silver expedited fee.

**1. Unscripted $10 expedited-shipping choice; gold assumes yes** (Minor · ambiguous_choice · gold step #4)

| | Call | Output |
|---|---|---|
| Gold | `order_replacement_credit_card_7291(credit_card_account_id="cc_890389b165_silver", user_id="890389b165", shipping_address="2500 Woodward Avenue, Suite 300, Detroit, MI 48201", reason="fraud_suspected", expedited_shipping=true)` | Order ID: ccord_6ed1a491c036 ... Shipping Method: Expedited Expected Delivery: 2-3 business days |
| Alternative path | `order_replacement_credit_card_7291(credit_card_account_id="cc_890389b165_silver", user_id="890389b165", shipping_address="2500 Woodward Avenue, Suite 300, Detroit, MI 48201", reason="fraud_suspected", expedited_shipping=false)` (Agent asks as the doc requires; the simulated customer, with no scripted answer, declines the $10 fee.) | Order ID: ccord_6ed1a491c036 ... Shipping Method: Standard Expected Delivery: 7-10 business days |

- **doc_credit_cards_credit_card_replacements_001:** "- Ask whether they want expedited shipping (advise on possible fees by tier; see Shipping selection)."
- **doc_credit_cards_credit_card_replacements_001:** "- Mid-tier (Silver Rewards, Business Silver, Green Rewards, Silver Zoom): $10.00."
- **doc_credit_cards_credit_card_replacements_001:** "- If the reason is fraud_suspected or stolen, strongly recommend expedited shipping to minimize exposure"
- **Where it differs:** Doc _001: speed is the customer's choice ($10 for Silver), expedited only recommended for fraud. Script has no speed line. Gold step 4 requires expedited_shipping true.
- **Scorer:** `credit_card_orders[ccord_6ed1a491c036].expedited_shipping: gold=true agent=false` → DB upstream FAIL, verified FAIL

### task_039 — Major

**Why:** Gold step 9 denies credit on the $129.45 fraud dispute by counting this session's filings; doc _015 never says to, and history shows zero.

**1. Unclear whether same-session filings count toward cap** (Major · ambiguous_choice · gold step #9)

| | Call | Output |
|---|---|---|
| Gold | `file_credit_card_transaction_dispute_4829(transaction_id="txn_2f16599b9075", contacted_merchant=false, purchase_date="10/11/2025", dispute_reason="unauthorized_fraudulent_charge", resolution_requested="full_refund", eligible_for_provisional_credit=false, ...="card/customer fields as gold")` | Credit card transaction dispute filed successfully. ... Dispute ID: dsp_6d3fd7ab85a6 Transaction: txn_2f16599b9075 Reason: Unauthorized Fraudulent Charge ... Provisional Credit: Not eligible at this time. |
| Alternative path | `file_credit_card_transaction_dispute_4829(transaction_id="txn_2f16599b9075", contacted_merchant=false, purchase_date="10/11/2025", dispute_reason="unauthorized_fraudulent_charge", resolution_requested="full_refund", eligible_for_provisional_credit=true, ...="card/customer fields as gold")` (Snapshot reading: count only the history from gold step 2, which shows no disputes, so all criteria hold.) | Credit card transaction dispute filed successfully. ... Dispute ID: dsp_6d3fd7ab85a6 Transaction: txn_2f16599b9075 Reason: Unauthorized Fraudulent Charge ... Provisional Credit: ELIGIBLE - Credit will be applied within 2 business days. |

- **doc_credit_cards_credit_cards_(general)_015:** "4. Previous Disputes: The customer has not filed more than 2 disputes in the past 12 months"
- **tool:get_user_dispute_history_7291:** "gold step 2 output: "No transaction disputes found for this user.""
- **Where it differs:** History (step 2): 0 disputes. Doc _015 is silent on in-session filings. Gold counts steps 6-8, so step 9 ($129.45 fraud) is false; snapshot reading: true.
- **Scorer:** `transaction_disputes[dsp_6d3fd7ab85a6].eligible_for_provisional_credit: gold=false agent=true; .provisional_credit_given: gold=false agent=true` → DB upstream FAIL, verified FAIL

**2. Gold flags need largest-first filing order** (Major · ambiguous_choice · gold step #8)

| | Call | Output |
|---|---|---|
| Gold | `file_credit_card_transaction_dispute_4829(transaction_id="txn_182e896e1c97", contacted_merchant=true, purchase_date="10/26/2025", dispute_reason="duplicate_charge", resolution_requested="full_refund", eligible_for_provisional_credit=true, ...="card/customer fields as gold")` | Credit card transaction dispute filed successfully. ... Dispute ID: dsp_724e3fc6e879 Transaction: txn_182e896e1c97 Reason: Duplicate Charge ... Provisional Credit: ELIGIBLE - Credit will be applied within 2 business days. |
| Alternative path | `file_credit_card_transaction_dispute_4829(transaction_id="txn_182e896e1c97", contacted_merchant=true, purchase_date="10/26/2025", dispute_reason="duplicate_charge", resolution_requested="full_refund", eligible_for_provisional_credit=false, ...="card/customer fields as gold")` (Gold's own cumulative reading, but filing in the customer's listed order (234.56, 312.87, 267.34, 198.23, 129.45, 215.67, 162.54, 56.78): only 234.56 and 312.87 are eligible; $215.67 is filed 6th with 5 prior.) | Credit card transaction dispute filed successfully. ... Transaction: txn_182e896e1c97 Reason: Duplicate Charge ... Provisional Credit: Not eligible at this time. |

- **doc_credit_cards_credit_cards_(general)_015:** "4. Previous Disputes: The customer has not filed more than 2 disputes in the past 12 months"
- **instructions:** "If there's any limit on provisional credit, I want it applied to the biggest charges first. The $312 Costco charge and the $234 fraud charge are the ones hurting my cash flow the most right now. Do not mention this if the agent does NOT bring provisional credit up."
- **Where it differs:** No doc sets filing order. Gold files 312.87, 234.56, 215.67 first (steps 6-8). Listed order makes $215.67 ineligible; the priority line appears only if the agent raises provisional credit.
- **Scorer:** `transaction_disputes[dsp_724e3fc6e879].eligible_for_provisional_credit: gold=true agent=false; .provisional_credit_given: gold=true agent=false` → DB upstream FAIL, verified FAIL

### task_040 — Major

**Why:** Gold step 9 denies credit on the $342.50 fraud by counting this session's filings; history shows one prior dispute, within doc _015's limit.

**1. Unclear whether same-session filings count toward cap** (Major · ambiguous_choice · gold step #9)

| | Call | Output |
|---|---|---|
| Gold | `file_credit_card_transaction_dispute_4829(transaction_id="txn_a1b2c3d4e503", card_action="keep_active", contacted_merchant=false, purchase_date="10/10/2025", dispute_reason="unauthorized_fraudulent_charge", resolution_requested="full_refund", eligible_for_provisional_credit=false, ...="card/customer fields as gold")` | Credit card transaction dispute filed successfully. ... Dispute ID: dsp_da37cfc4d0d6 Transaction: txn_a1b2c3d4e503 Reason: Unauthorized Fraudulent Charge ... Provisional Credit: Not eligible at this time. |
| Alternative path | `file_credit_card_transaction_dispute_4829(transaction_id="txn_a1b2c3d4e503", card_action="keep_active", contacted_merchant=false, purchase_date="10/10/2025", dispute_reason="unauthorized_fraudulent_charge", resolution_requested="full_refund", eligible_for_provisional_credit=true, ...="card/customer fields as gold")` (Snapshot reading: gold step 2 history shows 1 dispute (not more than 2), so all criteria hold.) | Credit card transaction dispute filed successfully. ... Transaction: txn_a1b2c3d4e503 ... Provisional Credit: ELIGIBLE - Credit will be applied within 2 business days. |

- **doc_credit_cards_credit_cards_(general)_015:** "4. Previous Disputes: The customer has not filed more than 2 disputes in the past 12 months"
- **tool:get_user_dispute_history_7291:** "gold step 2 output: "Found 1 record(s) in 'transaction_disputes': 1. Record ID: dsp_ed3ab3dce038""
- **Where it differs:** History (step 2): 1 dispute. Doc _015 is silent on in-session filings. Gold counts steps 7-8, so step 9 ($342.50 fraud) is false; snapshot reading: true.
- **Scorer:** `transaction_disputes[dsp_da37cfc4d0d6].eligible_for_provisional_credit: gold=false agent=true; .provisional_credit_given: gold=false agent=true` → DB upstream FAIL, verified FAIL

**2. Gold flags need Grainger and Uline filed first** (Major · ambiguous_choice · gold step #7)

| | Call | Output |
|---|---|---|
| Gold | `file_credit_card_transaction_dispute_4829(transaction_id="txn_25e23705f61f", card_action="keep_active", contacted_merchant=true, purchase_date="10/26/2025", dispute_reason="duplicate_charge", resolution_requested="full_refund", eligible_for_provisional_credit=true, ...="card/customer fields as gold")` | Credit card transaction dispute filed successfully. ... Dispute ID: dsp_e78437c39cf5 Transaction: txn_25e23705f61f Reason: Duplicate Charge ... Provisional Credit: ELIGIBLE - Credit will be applied within 2 business days. |
| Alternative path | `file_credit_card_transaction_dispute_4829(transaction_id="txn_25e23705f61f", card_action="keep_active", contacted_merchant=true, purchase_date="10/26/2025", dispute_reason="duplicate_charge", resolution_requested="full_refund", eligible_for_provisional_credit=false, ...="card/customer fields as gold")` (Gold's own cumulative reading, filing in the customer's listed order (AA, Best Buy dup, PECO, Spotify, Uline, Grainger, Best Buy, Comcast): AA and Best Buy $189.99 get credit; Uline and Grainger do not.) | Credit card transaction dispute filed successfully. ... Transaction: txn_25e23705f61f ... Provisional Credit: Not eligible at this time. |

- **doc_credit_cards_credit_cards_(general)_015:** "4. Previous Disputes: The customer has not filed more than 2 disputes in the past 12 months"
- **instructions:** "If the agent mentions provisional credit or asks about it, say: "Yes, I'd like provisional credit on whatever qualifies. The Grainger and Uline charges are the biggest ones hurting my business cash flow right now - those are on my business card. Please prioritize those if there's any limit.""
- **Where it differs:** No doc sets filing order. Gold files Grainger, Uline first (steps 7-8). Listed order flips all four flags; the priority line appears only if the agent raises provisional credit.
- **Scorer:** `transaction_disputes[dsp_092ef9bd9397].eligible_for_provisional_credit: gold=true agent=false; transaction_disputes[dsp_1d6efbdca7c9].eligible_for_provisional_credit: gold=false agent=true; transaction_disputes[dsp_e78437c39cf5].eligible_for_provisional_credit: gold=true agent=false` → DB upstream FAIL, verified FAIL

**3. Comcast refund type unscripted; story says partial** (Major · instruction_conflict · gold step #14)

| | Call | Output |
|---|---|---|
| Gold | `file_credit_card_transaction_dispute_4829(transaction_id="txn_3ef1a3e9bf56", card_action="keep_active", contacted_merchant=true, purchase_date="10/30/2025", dispute_reason="refund_never_processed", resolution_requested="full_refund", eligible_for_provisional_credit=false, ...="card/customer fields as gold")` | Credit card transaction dispute filed successfully. ... Dispute ID: dsp_faf3282bff07 Transaction: txn_3ef1a3e9bf56 Reason: Refund Never Processed Resolution Requested: Full Refund |
| Alternative path | `file_credit_card_transaction_dispute_4829(transaction_id="txn_3ef1a3e9bf56", card_action="keep_active", contacted_merchant=true, purchase_date="10/30/2025", dispute_reason="refund_never_processed", resolution_requested="partial_refund", partial_refund_amount=50, eligible_for_provisional_credit=false, ...="card/customer fields as gold")` (Agent asks per doc _014; the simulated customer, told only that a partial refund was promised, asks for a partial refund (amount 50 is illustrative; the script gives none).) | Credit card transaction dispute filed successfully. ... Resolution Requested: Partial Refund Partial Refund Amount: $50.00 |

- **doc_credit_cards_credit_cards_(general)_014:** "13. resolution_requested (string) - Ask user what resolution they want."
- **instructions:** "You downgraded your business internet plan and were promised a partial refund weeks ago."
- **Where it differs:** Doc _014: ask the customer. Script never scripts a resolution, and its Comcast story says 'partial refund'. Gold step 14 requires full_refund.
- **Scorer:** `transaction_disputes[dsp_faf3282bff07].partial_refund_amount: gold=null agent=50.0; .resolution_requested: gold="full_refund" agent="partial_refund"` → DB upstream FAIL, verified FAIL

### task_041 — Major

**Why:** Gold credits only Staples and Coinbase, denying eight other qualifying disputes from step 11, via an in-session counting rule doc _015 never states.

**1. Two readings of the 2-dispute limit** (Major · ambiguous_choice · gold step #11)

| | Call | Output |
|---|---|---|
| Gold | `file_credit_card_transaction_dispute_4829(transaction_id="txn_107c4fa829bd", card_action="keep_active", contacted_merchant=false, purchase_date="10/08/2025", dispute_reason="unauthorized_fraudulent_charge", resolution_requested="full_refund", eligible_for_provisional_credit=false, ...="card/customer fields as gold")` | Credit card transaction dispute filed successfully. ... Dispute ID: dsp_f8596fa0b690 Transaction: txn_107c4fa829bd Reason: Unauthorized Fraudulent Charge ... Provisional Credit: Not eligible at this time. |
| Alternative path | `file_credit_card_transaction_dispute_4829(transaction_id="txn_107c4fa829bd", card_action="keep_active", contacted_merchant=false, purchase_date="10/08/2025", dispute_reason="unauthorized_fraudulent_charge", resolution_requested="full_refund", eligible_for_provisional_credit=true, ...="card/customer fields as gold")` (Snapshot reading (history at step 2 shows 1 prior dispute): steps 11-18, all reason-eligible fraud/duplicate/old not-received disputes, are set true.) | Credit card transaction dispute filed successfully. ... Provisional Credit: ELIGIBLE - Credit will be applied within 2 business days. |

- **doc_credit_cards_credit_cards_(general)_015:** "4. Previous Disputes: The customer has not filed more than 2 disputes in the past 12 months"
- **tool:get_user_dispute_history_7291:** "gold step 2 output: "Found 1 record(s) in 'transaction_disputes': 1. Record ID: dsp_dfab0685d198""
- **instructions:** "Please prioritize those if there's any limit."
- **Where it differs:** History: 1 prior dispute (≤2). Doc _015 is silent on in-session filings. Gold counts steps 9-10, so steps 11-18 are false; snapshot reading makes all ten true.
- **Scorer:** `transaction_disputes[dsp_0f439ab38556].eligible_for_provisional_credit: gold=false agent=true; transaction_disputes[dsp_16978243efb8].eligible_for_provisional_credit: gold=false agent=true; transaction_disputes[dsp_2260d9f89d7f].eligible_for_provisional_credit: gold=false agent=true` → DB upstream FAIL, verified FAIL

**2. Unscripted XFINITY partial amount must be exactly 69.99** (Major · instruction_conflict · gold step #19)

| | Call | Output |
|---|---|---|
| Gold | `file_credit_card_transaction_dispute_4829(transaction_id="txn_dd095dee227f", card_action="keep_active", contacted_merchant=true, purchase_date="10/28/2025", dispute_reason="incorrect_amount", resolution_requested="partial_refund", partial_refund_amount=69.99, eligible_for_provisional_credit=false, ...="card/customer fields as gold")` | Credit card transaction dispute filed successfully. ... Dispute ID: dsp_f603ba75fc0c ... Resolution Requested: Partial Refund Partial Refund Amount: $69.99 |
| Alternative path | `file_credit_card_transaction_dispute_4829(transaction_id="txn_dd095dee227f", card_action="keep_active", contacted_merchant=true, purchase_date="10/28/2025", dispute_reason="incorrect_amount", resolution_requested="partial_refund", partial_refund_amount=70, eligible_for_provisional_credit=false, ...="card/customer fields as gold")` (Agent asks per doc _014; customer, knowing only a usual bill of 'around $120', asks for about $70 back.) | Credit card transaction dispute filed successfully. ... Resolution Requested: Partial Refund Partial Refund Amount: $70.00 |

- **doc_credit_cards_credit_cards_(general)_014:** "13. resolution_requested (string) - Ask user what resolution they want."
- **instructions:** "XFINITY $189.99 on 10/28/2025** - INCORRECT AMOUNT. Your usual bill is around $120."
- **Where it differs:** Script gives no resolution or amount, only 'around $120'. Gold step 19 needs exactly 69.99. AT&T ('promised a partial refund') and Tesla are gold full_refund.
- **Scorer:** `transaction_disputes[dsp_f603ba75fc0c].partial_refund_amount: gold=69.99 agent=70.0` → DB upstream FAIL, verified FAIL

### task_045 — Minor

**Why:** The customer gives two closure reasons in one sentence; gold step 12 accepts only found_better_card, so logging not_using_card fails.

**1. Two stated closure reasons; gold accepts one** (Minor · ambiguous_choice · gold step #12)

| | Call | Output |
|---|---|---|
| Gold | `log_credit_card_closure_reason_4521(credit_card_account_id="cc_224959b99e_bsilver", user_id="224959b99e", closure_reason="found_better_card")` | Closure reason 'found_better_card' logged for account cc_224959b99e_bsilver. |
| Alternative path | `log_credit_card_closure_reason_4521(credit_card_account_id="cc_224959b99e_bsilver", user_id="224959b99e", closure_reason="not_using_card")` (Agent logs the customer's second stated reason, also a valid doc category.) | Closure reason 'not_using_card' logged for account cc_224959b99e_bsilver. |

- **instructions:** "I found a better card at another bank and I don't really use this one much anymore."
- **doc_credit_cards_credit_card_account_logistics_003:** "- closure_reason (string, required): One of: 'annual_fee', 'not_using_card', 'found_better_card', 'unhappy_with_rewards', 'simplifying_finances', 'negative_experience', 'other'."
- **Where it differs:** Opening line maps to both found_better_card and not_using_card (doc _003 lists both). Gold step 12 accepts only found_better_card; first-stated reason and later flow favor it.
- **Scorer:** `credit_card_closure_reasons[clsr_dbc2e6bee274].closure_reason: gold="found_better_card" agent="not_using_card"` → DB upstream FAIL, verified FAIL

### task_046 — Major

**Why:** Gold stops at the pending dispute, but an agent that also reports the $125 balance gets a scripted payoff request, and paying it fails.

**1. Scripted $125 payoff request; gold has no payment** (Major · instruction_conflict · gold step #2)

| | Call | Output |
|---|---|---|
| Gold | `get_user_dispute_history_7291(user_id="224959b99e")` | Found 1 record(s) in 'transaction_disputes':  1. Record ID: dsp_yuki_bsilver_001 ... status: UNDER_REVIEW |
| Alternative path | `pay_credit_card_from_checking_9182(user_id="224959b99e", checking_account_id="05", credit_card_account_id="cc_224959b99e_bsilver", amount=125.0)` (After step 2 the agent explains every unmet requirement (pending dispute and $125 balance); the customer asks for a payoff, which the agent makes (after get_all_user_accounts_by_user_id_3847).) | Payment processed successfully!   - Payment Amount: $125.00   - From Checking Account: 05   - To Credit Card Account: cc_224959b99e_bsilver   - New Checking Balance: $2725.00   - New Credit Card Balance: $0.00 |

- **doc_credit_cards_credit_card_account_logistics_003:** "4. Outstanding balance: The account must have no outstanding balance. If a balance remains, the customer must pay it off before closure. If any requirement is not met, explain what must be resolved and do not proceed with retention offers."
- **instructions:** "Oh, I didn't realize there was still a balance. Yes, please pay that off from my checking account."
- **db:credit_card_accounts[cc_224959b99e_bsilver]:** "current_balance: $125.00"
- **Where it differs:** Doc _003: explain what must be resolved (dispute and $125 balance both unmet). Script then requests payoff. Gold stops at step 2 with no payment.
- **Scorer:** `accounts[05].current_holdings: gold="2850.00" agent="2725.00"; credit_card_accounts[cc_224959b99e_bsilver].current_balance: gold="$125.00" agent="$0.00"; extra discoverable call pay_credit_card_from_checking_9182` → DB upstream FAIL, verified FAIL

### task_047 — Minor

**Why:** For the Platinum card the customer cites both the annual fee and low usage; gold step 12 accepts only annual_fee, so not_using_card fails.

**1. Two stated Platinum closure reasons; gold accepts one** (Minor · ambiguous_choice · gold step #12)

| | Call | Output |
|---|---|---|
| Gold | `log_credit_card_closure_reason_4521(credit_card_account_id="cc_c7d8e9f0a1_plat", user_id="c7d8e9f0a1", closure_reason="annual_fee")` | Closure reason logged successfully. ... Closure reason 'annual_fee' logged for account cc_c7d8e9f0a1_plat. |
| Alternative path | `log_credit_card_closure_reason_4521(credit_card_account_id="cc_c7d8e9f0a1_plat", user_id="c7d8e9f0a1", closure_reason="not_using_card")` (Agent logs the customer's second stated reason, also a valid doc category.) | Closure reason logged successfully. ... Closure reason 'not_using_card' logged for account cc_c7d8e9f0a1_plat. |

- **instructions:** "The annual fee on that one is really bothering me. I don't use it as much as I used to."
- **doc_credit_cards_credit_card_account_logistics_003:** "- closure_reason (string, required): One of: 'annual_fee', 'not_using_card', 'found_better_card', 'unhappy_with_rewards', 'simplifying_finances', 'negative_experience', 'other'."
- **Where it differs:** Customer line maps to annual_fee and not_using_card (both in doc _003's list). Gold step 12 accepts only annual_fee; goal and downgrade branch favor it.
- **Scorer:** `credit_card_closure_reasons[clsr_4e79f7cf01a9].closure_reason: gold="annual_fee" agent="not_using_card"` → DB upstream FAIL, verified FAIL

### task_048 — Major

**Why:** Gold step 18 requires a Silver Rewards application, but Platinum Rewards and Business Silver also beat the competitor's 3.25%; doc _003 has no tie-breaker.

**1. Several Rho-Bank cards qualify; gold accepts Silver only** (Major · ambiguous_choice · gold step #18)

| | Call | Output |
|---|---|---|
| Gold | `apply_for_credit_card(card_type="Silver Rewards Card", customer_name="Valentina Kostopoulos", annual_income=125000, rho_bank_subscription=false)` | Credit card application submitted: Your application has been successfully submitted. You will receive a decision within 5-7 business days via email. |
| Alternative path | `apply_for_credit_card(card_type="Platinum Rewards Card", customer_name="Valentina Kostopoulos", annual_income=125000, rho_bank_subscription=false)` (Agent recommends Platinum Rewards (10% on everything); under script step 8 the customer applies for whichever competitive card is presented.) | Credit card application submitted: Your application has been successfully submitted. You will receive a decision within 5-7 business days via email. |

- **doc_credit_cards_credit_card_account_logistics_003:** "Found a better card: Ask what features attracted them. If Rho-Bank offers a card with similar or better benefits, offer to help them apply instead of closing the current account."
- **doc_credit_cards_silver_rewards_card_002:** "- Pay with your card for eligible travel and software transactions to earn 4.0% back"
- **doc_credit_cards_platinum_rewards_card_002:** "- You earn 10.0% cash back on all eligible purchases."
- **doc_business_credit_cards_business_silver_rewards_card_002:** "- Earn 10.0% cash back on eligible travel and software purchases"
- **Where it differs:** Competitor: 3.25% travel/software. Doc _003 allows any 'similar or better' card: Silver 4%, Platinum 10%, Business Silver 10%. Gold step 18 accepts only Silver Rewards Card.
- **Scorer:** `credit_card_applications[128ca98041beb963]: EXTRA row (Platinum Rewards Card); credit_card_applications[58141e96e8835ce3]: MISSING row (Silver Rewards Card)` → DB upstream FAIL, verified FAIL

### task_049 — Minor

**Why:** Gold is correct; the graded transfer-request row exists only if the simulated customer calls request_human_agent_transfer once, which the agent cannot influence.

**1. Graded row depends on the customer's own tool call** (Minor · other · gold step #17)

| | Call | Output |
|---|---|---|
| Gold | `request_human_agent_transfer()` | Transfer request #1 submitted. The agent will process your request. |
| Alternative path | skips `request_human_agent_transfer` (Plausible misreading: the simulator says 'Transfer me to a human agent.' aloud but does not call its tool; the agent still transfers (step 18).) |  |

- **instructions:** "Transfer me to a human agent."
- **tool:request_human_agent_transfer:** "Use this when you want to speak with a real human agent instead of the automated system."
- **task:user_tools:** "["apply_for_credit_card", "call_discoverable_user_tool", "request_human_agent_transfer"]"
- **Where it differs:** Tool is given to the customer and its docstring matches the scripted request, so the gold call is expected; without it the row is missing.
- **Scorer:** `human_transfer_requests[transfer_request_1]: MISSING row (gold has)` → DB upstream FAIL, verified FAIL

### task_050 — Minor

**Why:** The Gold-card-is-Premium tier map (doc _015) is missing from required_documents; only an Entry-tier guess ($1,250 cap) would change the $2,500 answer.

**1. Card-to-tier map not in required documents** (Minor · info_unavailable · gold step #2)

| | Call | Output |
|---|---|---|
| Gold | `submit_credit_limit_increase_request_7392(credit_card_account_id="cc_584f9c5d00_gold", user_id="584f9c5d00", requested_increase_amount=2500)` | Credit limit increase request submitted successfully. ...   - Requested Increase: $2,500   - Status: PENDING |
| Alternative path | `submit_credit_limit_increase_request_7392(credit_card_account_id="cc_584f9c5d00_gold", user_id="584f9c5d00", requested_increase_amount=1250)` (Plausible misreading: the Entry-tier guess an agent might make without _015 (25% cap); also step 12 new_credit_limit 6250. Gold is correct if _015 is retrieved.) | Credit limit increase request submitted successfully. ...   - Requested Increase: $1,250   - Status: PENDING |

- **doc_credit_cards_credit_cards_(general)_015:** "Premium Tier (Gold Rewards Card, Business Gold Rewards Card): Maximum $10000.00"
- **doc_credit_cards_credit_card_account_logistics_006:** "- Entry-tier cards: Maximum increase of 25% of current credit limit per request."
- **task:required_documents:** "logistics_004, logistics_005, logistics_006, logistics_007, replacements_005, (general)_016 (no (general)_015)"
- **Where it differs:** Logistics_006 caps by tier but never maps cards to tiers; mapping is only in unlisted _015. Premium/Mid give 2500→7500 (gold); Entry guess gives 1250→6250.
- **Scorer:** `credit_card_accounts[cc_584f9c5d00_gold].credit_limit: gold "$7500.00" agent "$6250.00"; credit_limit_increase_requests[cli_4fe9de112e66]: MISSING row` → DB upstream FAIL, verified FAIL

### task_053 — Blocker

**Why:** Gold files the dispute with last-4 "2791", obtainable only via the customer's logged get_card_last_4_digits call, which the gold omits.

**1. Gold omits the scripted customer last-4 lookup** (Blocker · gold_call_missing · gold step #13)

| | Call | Output |
|---|---|---|
| Gold | - | - |
| Alternative path | `call_discoverable_user_tool(discoverable_tool_name="get_card_last_4_digits", arguments={"credit_card_account_id": "cc_e9d195fe8e_silver"})` (Customer (requestor user) uses the tool given at step 13, before step 14, as the script says.) | Card information retrieved successfully. ... Last 4 digits of card: 2791 |

- **instructions:** "(If the agent provides you with the get_card_last_4_digits tool, use it to retrieve the number.)"
- **tool:get_card_last_4_digits:** "self._log_user_tool_call("get_card_last_4_digits", args)"
- **task:evaluation_criteria.actions[15]:** ""card_last_4_digits": "2791""
- **Where it differs:** Gold step 13 gives the tool; no user call follows, yet step 15 uses "2791". The scripted call (after step 13) logs a user_discoverable_tool_calls row gold lacks.
- **Scorer:** `user_discoverable_tool_calls[9a452d6c48d8d07e]: EXTRA row in agent DB` → DB upstream FAIL, verified FAIL

### task_054 — Minor

**Why:** Script never states a shipping speed; gold step 14 records expedited, the documented recommendation for fraud (free on Gold), so a neutral ask may diverge.

**1. Expedited shipping never stated by customer** (Minor · ambiguous_choice · gold step #14)

| | Call | Output |
|---|---|---|
| Gold | `order_replacement_credit_card_7291(credit_card_account_id="cc_584f9c5d00_gold", user_id="584f9c5d00", shipping_address="1456 Astoria Boulevard, Queens, NY 11102", reason="fraud_suspected", expedited_shipping=true)` | Order ID: ccord_ad344b6a4227 ... Shipping Method: Expedited |
| Alternative path | `order_replacement_credit_card_7291(credit_card_account_id="cc_584f9c5d00_gold", user_id="584f9c5d00", shipping_address="1456 Astoria Boulevard, Queens, NY 11102", reason="fraud_suspected", expedited_shipping=false)` (Plausible misreading: agent asks neutrally and, with no scripted preference, orders standard shipping instead of recommending expedited as replacements_001 says for fraud.) | Order ID: ccord_ad344b6a4227 ... Shipping Method: Standard |

- **doc_credit_cards_credit_card_replacements_001:** "Ask whether they want expedited shipping (advise on possible fees by tier; see Shipping selection)."
- **doc_credit_cards_credit_card_replacements_001:** "If the reason is fraud_suspected or stolen, strongly recommend expedited shipping to minimize exposure"
- **instructions:** "Just send it to my address on file."
- **Where it differs:** Script never states a shipping speed; doc says ask and recommend expedited (free on Gold). Gold step 14: expedited true; neutral ask gives false.
- **Scorer:** `credit_card_orders[ccord_ad344b6a4227].expedited_shipping: gold=true agent=false` → DB upstream FAIL, verified FAIL

**2. Gold does CLI before fraud steps; script endorses reorder** (Minor · other · gold step #12)

| | Call | Output |
|---|---|---|
| Gold | `approve_credit_limit_increase_5847(credit_card_account_id="cc_584f9c5d00_gold", user_id="584f9c5d00", new_credit_limit=7500)` | Credit limit increase approved! |
| Alternative path | `deny_credit_limit_increase_5848(credit_card_account_id="cc_584f9c5d00_gold", user_id="584f9c5d00", denial_reason="pending_disputes")` (Plausible misreading: agent follows the opening's fraud-first order without weighing logistics_007, orders the replacement and files the dispute, then approve errors and it denies the CLI.) | Credit limit increase request denied. |

- **instructions:** "but let's handle the fraud situation first since that's the priority"
- **instructions:** "Can we do the credit limit increase FIRST before the fraud stuff, so I can still get everything done?"
- **doc_credit_cards_credit_card_account_logistics_007:** "3. No Pending Disputes: Verify the account has no active disputes."
- **Where it differs:** Opening: fraud first. logistics_007: dispute/replacement blocks CLI. Script step 3: customer asks for CLI first once told. Gold approves 7500 at step 12, before steps 14/16.
- **Scorer:** `credit_card_accounts[cc_584f9c5d00_gold].credit_limit: gold "$7500.00" agent "$5,000.00"; credit_limit_increase_requests[cli_439086eb3c3b]: EXTRA row; extra discoverable call deny_credit_limit_increase_5848` → DB upstream FAIL, verified FAIL

### task_056 — Major

**Why:** Business-savings doc _004 says "Set account_type to 'savings'"; gold step 5 uses 'business_savings', so following the doc creates a different account.

**1. Doc says account_type 'savings'; gold uses 'business_savings'** (Major · ambiguous_choice · gold step #5)

| | Call | Output |
|---|---|---|
| Gold | `open_bank_account_4821(user_id="b5e8f2a1c9", account_type="business_savings", account_class="Silver Plus Saver Account")` | Bank account opened successfully!   - Account ID: c1b48f17bb35e876   ...   - Account Type: business_savings |
| Alternative path | `open_bank_account_4821(user_id="b5e8f2a1c9", account_type="savings", account_class="Silver Plus Saver Account")` (No error; step 7 then transfers $3,200 to 3e54498f671ab53f.) | Bank account opened successfully!   - Account ID: 3e54498f671ab53f   ...   - Account Type: savings |

- **doc_bank_accounts_bank_accounts_(general)_004:** "Set account_type to 'savings'."
- **tool:open_bank_account_4821:** "Must be one of: 'checking' (personal checking), 'savings' (personal savings), 'business_checking', 'business_savings'"
- **Where it differs:** Business-savings procedure _004 says 'savings'; tool docstring calls that personal and lists 'business_savings'. Gold step 5 follows the docstring; account ID changes (c1b48f… vs 3e5449…).
- **Scorer:** `accounts[3e54498f671ab53f]: EXTRA row; accounts[c1b48f17bb35e876]: MISSING row (gold has)` → DB upstream FAIL, verified FAIL

### task_057 — Minor

**Why:** The adversarial savings refusal is ungraded: a fooled agent's open_bank_account_4821 savings attempt errors, changes no graded state, and still passes.

**1. Fooled savings attempt is invisible to grading** (Minor · other · no gold step)

| | Call | Output |
|---|---|---|
| Gold | - | - |
| Alternative path | `open_bank_account_4821(user_id="a8c4e2f7b3", account_type="savings", account_class="Silver Account")` (Plausible misreading: the fooled agent, believing the customer's '14 days have passed' lie, tries to open savings after step 6. Tool refuses; DB unchanged.) | Error: Account eligibility requirements not met. |

- **doc_bank_accounts_bank_accounts_(general)_002:** "Insufficient checking tenure: If the checking account has been open fewer than 14 days, advise the customer when they will become eligible."
- **task:description.notes:** "Agent MUST call get_current_time to verify time has NOT passed, and deny the request AGAIN."
- **Where it differs:** Notes make the second refusal the test, but the tool itself rejects savings (Blue checking 0 days old) and open_bank_account_4821 is already gold-logged, so the violation is unscored.
- **Scorer:** `(none): no DB field differs` → DB upstream PASS, verified PASS

### task_059 — Major

**Why:** Gold step 5 opens savings as 'Green Account'; the docs name the product 'Green Account (savings)', which opens a different account and fails.

**1. Two documented spellings for Green savings class** (Major · ambiguous_choice · gold step #5)

| | Call | Output |
|---|---|---|
| Gold | `open_bank_account_4821(user_id="cr59b4d8e3", account_type="savings", account_class="Green Account")` | Bank account opened successfully!   - Account ID: 6bec25bde54c963e   ...   - Account Class: Green Account |
| Alternative path | `open_bank_account_4821(user_id="cr59b4d8e3", account_type="savings", account_class="Green Account (savings)")` (Agent copies the product's full documented name, following general_001's 'Green Account (checking)' pattern.) | Bank account opened successfully!   - Account ID: f9386249cd4ade09   ...   - Account Class: Green Account (savings) |

- **doc_bank_accounts_bank_accounts_(general)_001:** "Personal checking account_class options must use the full official name ending with 'Account' (e.g., 'Blue Account', 'Green Account (checking)')"
- **doc_savings_accounts_green_account_(savings)_005:** "What APY does the Green Account (savings) earn?"
- **doc_bank_accounts_bank_accounts_(general)_002:** "account_class must use the full official name ending with 'Account', e.g., 'Silver Plus Account', 'Gold Account'"
- **Where it differs:** Savings docs name it 'Green Account (savings)' (13 uses); general_001 keeps the suffix in a class example. Gold step 5 uses bare 'Green Account'; account ID changes.
- **Scorer:** `accounts[6bec25bde54c963e]: MISSING row (gold has); accounts[f9386249cd4ade09]: EXTRA row` → DB upstream FAIL, verified FAIL

### task_063 — Blocker

**Why:** Bronze and Silver Rewards both add +0.15% to Silver Plus ($252/yr on $8,000), both fit; gold step 1 accepts only Silver Rewards.

**1. Bronze and Silver Rewards tie exactly** (Blocker · ambiguous_choice · gold step #1)

| | Call | Output |
|---|---|---|
| Gold | `apply_for_credit_card(card_type="Silver Rewards Card", customer_name="Taylor Brooks", annual_income=85000, rho_bank_subscription=false)` | Credit card application submitted: Your application has been successfully submitted. ... |
| Alternative path | `apply_for_credit_card(card_type="Bronze Rewards Card", customer_name="Taylor Brooks", annual_income=85000, rho_bank_subscription=false)` (Agent recommends the equally good Bronze Rewards; customer applies with "whatever card the agent recommended".) | Credit card application submitted: Your application has been successfully submitted. ... |

- **doc_savings_accounts_silver_plus_account_009:** "| Bronze Rewards Card | +0.15% |"
- **doc_savings_accounts_silver_plus_account_009:** "| Silver Rewards Card | +0.15% |"
- **doc_credit_cards_bronze_rewards_card_001:** "Consent to a credit pull (minimum score requirement is $640)."
- **instructions:** "card_type: Use whatever card the agent recommended"
- **Where it differs:** Both cards: $0 fee, credit check, minimum ≤700, +0.15% on Silver Plus → $8,000 × 3.15% = $252. No doc tie-breaker; gold step 1 takes Silver Rewards only.
- **Scorer:** `credit_card_applications[df7bfcce497828d4]: MISSING row (gold has); credit_card_applications[834b05512cd56ec5]: EXTRA row (Bronze Rewards Card)` → DB upstream FAIL, verified FAIL

### task_065 — Major

**Why:** Gold step 2 opens savings as 'Green Account'; the docs name the product 'Green Account (savings)', which opens a different account and fails.

**1. Two documented spellings for Green savings class** (Major · ambiguous_choice · gold step #2)

| | Call | Output |
|---|---|---|
| Gold | `open_bank_account_4821(user_id="rp65a7b3c4", account_type="savings", account_class="Green Account")` | Bank account opened successfully!   - Account ID: 4ba63ba5b4a98c12   ...   - Account Class: Green Account |
| Alternative path | `open_bank_account_4821(user_id="rp65a7b3c4", account_type="savings", account_class="Green Account (savings)")` (Agent uses the product's full documented name, as in the Evergreen pairing rule and general_001's class example.) | Bank account opened successfully!   - Account ID: 248a704a4fbe44b2   ...   - Account Class: Green Account (savings) |

- **doc_checking_accounts_evergreen_account_001:** "Link a Green Account (savings): +0.55% APY boost"
- **doc_bank_accounts_bank_accounts_(general)_001:** "Personal checking account_class options must use the full official name ending with 'Account' (e.g., 'Blue Account', 'Green Account (checking)')"
- **doc_bank_accounts_bank_accounts_(general)_002:** "account_class must use the full official name ending with 'Account', e.g., 'Silver Plus Account', 'Gold Account'"
- **Where it differs:** Docs name it 'Green Account (savings)' and general_001 keeps the suffix in a class example; general_002's 'ending with Account' rule gives bare 'Green Account', which gold step 2 uses.
- **Scorer:** `accounts[4ba63ba5b4a98c12]: MISSING row (gold has); accounts[248a704a4fbe44b2]: EXTRA row` → DB upstream FAIL, verified FAIL

### task_066 — Major

**Why:** Gold step 4 opens savings as 'Green Account'; docs name it 'Green Account (savings)', which opens a different account and fails.

**1. Two documented spellings for Green savings class** (Major · ambiguous_choice · gold step #4)

| | Call | Output |
|---|---|---|
| Gold | `open_bank_account_4821(user_id="rp65a7b3c4", account_type="savings", account_class="Green Account")` | Bank account opened successfully!   - Account ID: 4ba63ba5b4a98c12   ...   - Account Class: Green Account |
| Alternative path | `open_bank_account_4821(user_id="rp65a7b3c4", account_type="savings", account_class="Green Account (savings)")` (Agent copies the name as general_012 prints the pairing (same defect as 059/065).) | Bank account opened successfully!   - Account ID: 248a704a4fbe44b2   ...   - Account Class: Green Account (savings) |

- **doc_bank_accounts_bank_accounts_(general)_012:** "3. Evergreen Account (checking) + Green Account (savings)"
- **doc_bank_accounts_bank_accounts_(general)_001:** "Personal checking account_class options must use the full official name ending with 'Account' (e.g., 'Blue Account', 'Green Account (checking)')"
- **doc_bank_accounts_bank_accounts_(general)_002:** "account_class must use the full official name ending with 'Account', e.g., 'Silver Plus Account', 'Gold Account'"
- **Where it differs:** general_012 names it 'Green Account (savings)'; general_001's example keeps the suffix. Gold step 4 uses bare 'Green Account' per general_002's rule; account ID changes.
- **Scorer:** `accounts[4ba63ba5b4a98c12]: MISSING row (gold has); accounts[248a704a4fbe44b2]: EXTRA row` → DB upstream FAIL, verified FAIL

### task_068 — Major

**Why:** Gold step 3 opens checking as "Green Account", but the checking procedure doc _001 gives "Green Account (checking)" as the class example.

**1. Checking class example is "Green Account (checking)"** (Major · ambiguous_choice · gold step #3)

| | Call | Output |
|---|---|---|
| Gold | `open_bank_account_4821(user_id="rp65a7b3c4", account_type="checking", account_class="Green Account")` | Bank account opened successfully!   - Account ID: 722980a6c8eec6ab   ...   - Account Class: Green Account |
| Alternative path | `open_bank_account_4821(user_id="rp65a7b3c4", account_type="checking", account_class="Green Account (checking)")` (Copies the class name from the procedure's own example; the class string is hashed into the account id.) | Bank account opened successfully!   - Account ID: 662d6d08711816cc   ...   - Account Class: Green Account (checking) |

- **doc_bank_accounts_bank_accounts_(general)_001:** "Personal checking account_class options must use the full official name ending with 'Account' (e.g., 'Blue Account', 'Green Account (checking)')."
- **doc_bank_accounts_bank_accounts_(general)_005:** "MID TIER (Blue Account, Green Account (checking))"
- **Where it differs:** Doc _001 example: "Green Account (checking)". Gold step 3: "Green Account". Both readings are document-supported, gold accepts only one.
- **Scorer:** `accounts[662d6d08711816cc]: EXTRA row (Green Account (checking)); accounts[722980a6c8eec6ab]: MISSING row (Green Account)` → DB upstream FAIL, verified FAIL

### task_069 — Blocker

**Why:** Gold step 2 opens Silver Plus savings (3.5%), but doc gold_account_003 gives Gold savings ATM rebates, so Gold (5.7%) wins.

**1. Gold savings has ATM rebates; gold excludes it** (Blocker · gold_value_wrong · gold step #2)

| | Call | Output |
|---|---|---|
| Gold | `open_bank_account_4821(user_id="rp65a7b3c4", account_type="savings", account_class="Silver Plus Account")` | Bank account opened successfully!   - Account ID: 4974e9096233f54e   ...   - Account Class: Silver Plus Account |
| Alternative path | `open_bank_account_4821(user_id="rp65a7b3c4", account_type="savings", account_class="Gold Account")` (Gold savings meets the ATM-rebate requirement and the $10,000 minimum; Blue checking and Silver Rewards stay the same (5.5% + 0.2% = 5.7%).) | Bank account opened successfully!   - Account ID: ea5af121ea163b18   ...   - Account Class: Gold Account |

- **doc_savings_accounts_gold_account_003:** "ATM fee rebate cap per month: $30"
- **doc_savings_accounts_gold_account_001:** "Your account earns an APY of 5.5% on the balance you maintain."
- **doc_savings_accounts_silver_account_005:** "Yes. You can receive ATM fee rebates up to 15 each month."
- **task:description.notes:** "Needs ATM fee rebates on savings account - blocks Gold Account, Silver Account, Green Account (savings), Bronze Account"
- **Where it differs:** Author notes say Gold/Silver savings lack ATM rebates; docs _003 and silver_005 say they have them. Gold 5.7% and Silver 4.125% beat gold's Silver Plus 3.5%.
- **Scorer:** `accounts[4974e9096233f54e]: MISSING row (Silver Plus Account); accounts[ea5af121ea163b18]: EXTRA row (Gold Account)` → DB upstream FAIL, verified FAIL

### task_070 — Minor

**Why:** Gold step 4 opens Sky Blue, a startup account for companies within 4 years of formation, but the script never states the business's age.

**1. Sky Blue age limit; company age never given** (Minor · info_unavailable · gold step #4)

| | Call | Output |
|---|---|---|
| Gold | `open_bank_account_4821(user_id="224959b99e", account_type="business_checking", account_class="Sky Blue")` | Bank account opened successfully!   - Account ID: 3befd297b57bc9c1   ...   - Account Class: Sky Blue |
| Alternative path | `open_bank_account_4821(user_id="224959b99e", account_type="business_checking", account_class="Lime Green")` (Agent asks the company age; the script gives none, so the customer cannot confirm. An agent that will not open Sky Blue unconfirmed picks Lime Green, next in the promotion.) | Bank account opened successfully!   - Account ID: 598255c47ac66e19   ...   - Account Class: Lime Green |

- **doc_business_checking_accounts_sky_blue_001:** "Confirm your company is within 4 years of formation."
- **instructions:** "You've had a personal Green Account with Rho-Bank for about 3 years and have roughly $2,850 in it. Your business has grown and you need to separate personal and business finances."
- **Where it differs:** Doc sky_blue_001 requires company age within 4 years; instructions give no formation date. Gold step 4 assumes eligibility the customer cannot confirm; a cautious agent picks Lime Green.
- **Scorer:** `accounts[3befd297b57bc9c1]: MISSING row (Sky Blue); accounts[598255c47ac66e19]: EXTRA row (Lime Green)` → DB upstream FAIL, verified FAIL

### task_071 — Major

**Why:** Business-savings procedure doc _004 says "Set account_type to 'savings'", but gold step 5 uses 'business_savings', producing a different account.

**1. Doc _004 says account_type 'savings'; gold uses business_savings** (Major · gold_value_wrong · gold step #5)

| | Call | Output |
|---|---|---|
| Gold | `open_bank_account_4821(user_id="yt71c9e4f2", account_type="business_savings", account_class="Gold Saver Account")` | Bank account opened successfully!   - Account ID: 00babd93acc4dd4e   - User ID: yt71c9e4f2   - Account Type: business_savings   - Account Class: Gold Saver Account |
| Alternative path | `open_bank_account_4821(user_id="yt71c9e4f2", account_type="savings", account_class="Gold Saver Account")` (Follows doc _004 verbatim; the personal-savings eligibility check passes, so the call succeeds with a different id.) | Bank account opened successfully!   - Account ID: b8329f69ab675fe5   - User ID: yt71c9e4f2   - Account Type: savings   - Account Class: Gold Saver Account |

- **doc_bank_accounts_bank_accounts_(general)_004:** "Set account_type to 'savings'."
- **tool:open_bank_account_4821:** "Must be one of: 'checking' (personal checking), 'savings' (personal savings), 'business_checking', 'business_savings'"
- **Where it differs:** Doc _004 (Opening Business Savings Accounts): account_type 'savings'. Gold step 5: 'business_savings'. The tool accepts both; the account id hash differs.
- **Scorer:** `accounts[00babd93acc4dd4e]: MISSING row (business_savings); accounts[b8329f69ab675fe5]: EXTRA row (savings)` → DB upstream FAIL, verified FAIL

### task_072 — Major

**Why:** Gold refunds $14.00 and $3.50 by counting fee errors dated 11/20 and 11/15, after the 11/14/2025 clock; posted fees give $13.50 and $3.00.

**1. Gold refunds count fee rows dated after today** (Major · gold_value_wrong · gold step #7)

| | Call | Output |
|---|---|---|
| Gold | `apply_checking_account_credit_5829(account_id="chk_lj82d4f1a9", amount=14.0, credit_type="fee_refund")` | Credit applied successfully!   - Transaction ID: txn_c23cb7ee097281e4   ...   - Amount: $14.00 |
| Alternative path | `apply_checking_account_credit_5829(account_id="chk_lj82d4f1a9", amount=13.5, credit_type="fee_refund")` (Reviews only fees posted through 11/14. Step 8 likewise becomes chk_538bfb9cba 3.0 (gold 3.5): "Transaction ID: txn_323de4c8907d002b ... Amount: $3.00".) | Credit applied successfully!   - Transaction ID: txn_ef6d58a37349c63f   ...   - Amount: $13.50 |

- **tool:get_current_time:** "The current time is 2025-11-14 03:40:00 EST."
- **db:bank_account_transaction_history[btxn_fcd7ef3a24ed]:** "account_id: chk_lj82d4f1a9, date: 11/20/2025, description: NON-RHO ATM FEE, amount: -2.5"
- **doc_checking_accounts_bluest_account_010:** "| Cash withdrawal at an out-of-network ATM | $2.00 per withdrawal |"
- **db:bank_account_transaction_history[btxn_49c0c0b3b8c1]:** "account_id: chk_538bfb9cba, date: 11/15/2025, description: FOREIGN ATM FEE - 2% OF WITHDRAWAL (MIN $3.00), amount: -4.0"
- **doc_checking_accounts_light_green_account_013:** "| More than $100 and up to and including $300 | $3.50 |"
- **Where it differs:** Clock 11/14. Step 7 adds $0.50 for 11/20 Bluest fee ($2.50 vs $2.00): 14.00 vs 13.50. Step 8 adds $0.50 for 11/15 Light Green fee: 3.50 vs 3.00.
- **Scorer:** `accounts[chk_538bfb9cba].current_holdings: gold "$1851.00" vs agent "$1850.50"; accounts[chk_lj82d4f1a9].current_holdings: gold "$127464.00" vs agent "$127463.50"; bank_account_transaction_history[txn_c23cb7ee097281e4]: MISSING row` → DB upstream FAIL, verified FAIL

### task_073 — Major

**Why:** Gold step 9 refunds $9.00 on Green by counting a duplicate $3.00 fee dated 11/15, after the 11/14/2025 clock; posted fees give $6.00.

**1. Green refund counts a duplicate fee dated after today** (Major · gold_value_wrong · gold step #9)

| | Call | Output |
|---|---|---|
| Gold | `apply_checking_account_credit_5829(account_id="chk_kj93a7b2e1_2", amount=9.0, credit_type="fee_refund")` | Credit applied successfully!   - Transaction ID: txn_6d3e75024589f071   ...   - Amount: $9.00 |
| Alternative path | `apply_checking_account_credit_5829(account_id="chk_kj93a7b2e1_2", amount=6.0, credit_type="fee_refund")` (Reviews only fees posted through 11/14: RHO-BANK ATM fee $3.00 + Woori $15 vs $12 = $6.00. Light Green's post-clock items (+1.50, -1.50) cancel, so step 10 is unchanged.) | Credit applied successfully!   - Transaction ID: txn_e9acb4a3f542db9f   ...   - Amount: $6.00 |

- **tool:get_current_time:** "The current time is 2025-11-14 03:40:00 EST."
- **db:bank_account_transaction_history[btxn_kj18k9l0m1n3, btxn_kj18k9l0m1n4]:** "account_id: chk_kj93a7b2e1_2, date: 11/15/2025, description: NON-RHO ATM FEE, amount: -3.0 (twice, one $250 PNC withdrawal)"
- **doc_bank_accounts_bank_accounts_(general)_017:** "Check the transaction history to confirm each fee discrepancy"
- **Where it differs:** Clock 11/14. Gold step 9 adds +$3.00 for the 11/15 duplicate fee: 9.00 vs 6.00. No doc says whether future-dated rows count.
- **Scorer:** `accounts[chk_kj93a7b2e1_2].current_holdings: gold "$12759.00" vs agent "$12756.00"; bank_account_transaction_history[txn_6d3e75024589f071]: MISSING row; bank_account_transaction_history[txn_e9acb4a3f542db9f]: EXTRA row` → DB upstream FAIL, verified FAIL

### task_074 — Major

**Why:** Gold step 9 credits Purple $27.00 by counting an 11/15 duplicate fee (after the 11/14 clock) and rebating Rho-Bank's own fee, which Purple docs exclude.

**1. Purple refund counts a duplicate fee dated after today** (Major · gold_value_wrong · gold step #9)

| | Call | Output |
|---|---|---|
| Gold | `apply_checking_account_credit_5829(account_id="chk_ar72c5d8e3_1", amount=27.0, credit_type="fee_refund")` | Credit applied successfully!   - Transaction ID: txn_a3e3028990be09a3   ...   - Amount: $27.00 |
| Alternative path | `apply_checking_account_credit_5829(account_id="chk_ar72c5d8e3_1", amount=24.5, credit_type="fee_refund")` (Excludes the 11/15 duplicate $2.50 fee; everything else as gold.) | Credit applied successfully!   - Transaction ID: txn_1700c9f29a0f203a   ...   - Amount: $24.50 |

- **tool:get_current_time:** "The current time is 2025-11-14 03:40:00 EST."
- **db:bank_account_transaction_history[btxn_ar_purple_15f_dup]:** "account_id: chk_ar72c5d8e3_1, date: 11/15/2025, description: NON-RHO ATM FEE, amount: -2.5"
- **doc_bank_accounts_bank_accounts_(general)_017:** "Check the transaction history to confirm each fee discrepancy"
- **Where it differs:** Clock 11/14. Gold step 9 includes +$2.50 for the 11/15 duplicate: 27.00 vs 24.50. No doc says whether future-dated rows count.
- **Scorer:** `accounts[chk_ar72c5d8e3_1].current_holdings: gold "$4527.00" vs agent "$4524.50"; bank_account_transaction_history[txn_a3e3028990be09a3]: MISSING row; bank_account_transaction_history[txn_1700c9f29a0f203a]: EXTRA row` → DB upstream FAIL, verified FAIL

**2. Purple rebate covers operator fees, not Rho-Bank's fee** (Major · gold_value_wrong · gold step #9)

| | Call | Output |
|---|---|---|
| Gold | `apply_checking_account_credit_5829(account_id="chk_ar72c5d8e3_1", amount=27.0, credit_type="fee_refund")` | Credit applied successfully!   - Transaction ID: txn_a3e3028990be09a3   ...   - Amount: $27.00 |
| Alternative path | `apply_checking_account_credit_5829(account_id="chk_ar72c5d8e3_1", amount=24.5, credit_type="fee_refund")` (Refunds only the $1.00 overcharge on the 11/11 $3.50 fee, not a $2.50 'missing rebate'. Combined with point 1 the amount is $22.00 (also FAIL per verifier).) | Credit applied successfully!   - Transaction ID: txn_1700c9f29a0f203a   ...   - Amount: $24.50 |

- **doc_checking_accounts_purple_account_004:** "You are eligible for refunds of ATM operator fees up to a monthly cap of $30."
- **doc_checking_accounts_purple_account_010:** "Confirm that the charge is labeled as an ATM operator fee"
- **db:bank_account_transaction_history[btxn_ar_purple_11f]:** "account_id: chk_ar72c5d8e3_1, date: 11/11/2025, description: NON-RHO ATM FEE, amount: -3.5 (no rebate row)"
- **Where it differs:** Docs _004/_010 rebate ATM-operator fees only. Gold adds a $2.50 rebate on Rho-Bank's own 11/11 NON-RHO fee: 27.00 vs 24.50. Task_075 assumes the opposite reading.
- **Scorer:** `accounts[chk_ar72c5d8e3_1].current_holdings: gold "$4527.00" vs agent "$4524.50"; bank_account_transaction_history[txn_a3e3028990be09a3]: MISSING row` → DB upstream FAIL, verified FAIL

### task_075 — Major

**Why:** Gold step 2 picks Green Fee-Free only if Purple's $2.50 out-of-network fee stacks abroad; Purple doc _001 says foreign withdrawals cost $0.00, tying both.

**1. Purple foreign withdrawals $0.00 ties Green Fee-Free** (Major · ambiguous_choice · gold step #2)

| | Call | Output |
|---|---|---|
| Gold | `open_bank_account_4821(user_id="mv93f8a7b2", account_type="checking", account_class="Green Fee-Free Account")` | Bank account opened successfully!   - Account ID: 4331e92d1f21702f   ...   - Account Class: Green Fee-Free Account |
| Alternative path | `open_bank_account_4821(user_id="mv93f8a7b2", account_type="checking", account_class="Purple Account")` (Non-stacking reading (as seeded in tasks 072-074): Purple foreign withdrawals cost $0, equal to Green Fee-Free, and Purple also refunds operator surcharges up to $30/month.) | Bank account opened successfully!   - Account ID: 2e186e760e69e28a   ...   - Account Class: Purple Account |

- **doc_checking_accounts_purple_account_001:** "No foreign ATM withdrawal fees: $0.00 per withdrawal (third-party ATM operator fees may still apply)"
- **doc_checking_accounts_purple_account_012:** "You are charged $2.50 per cash withdrawal made at an out-of-network ATM."
- **doc_checking_accounts_green_fee-free_account_005:** "Foreign ATM withdrawals are also fee-free: $0.00 per withdrawal."
- **instructions:** "You'll need to withdraw cash regularly from out of network ATMs abroad in a foreign currency."
- **Where it differs:** Gold needs fee stacking: Purple 18 x $2.50 = $45 vs GFF $0. Without stacking (purple_001): Purple $0 = GFF $0. Customer's wording favours stacking.
- **Scorer:** `accounts[2e186e760e69e28a]: EXTRA row (Purple Account); accounts[4331e92d1f21702f]: MISSING row (Green Fee-Free Account)` → DB upstream FAIL, verified FAIL

### task_076 — Major

**Why:** Gold step 2 opens Purple ($20 ATM fees); Bluest also has 2-day early deposit and costs $16, excluded only by an unmentioned $75,000 deposit.

**1. Bluest is cheaper; deposit capacity never stated** (Major · instruction_conflict · gold step #2)

| | Call | Output |
|---|---|---|
| Gold | `open_bank_account_4821(user_id="av96d4e7f1", account_type="checking", account_class="Purple Account")` | Bank account opened successfully!   - Account ID: 0516a4f7bca2d8d1   ...   - Account Class: Purple Account |
| Alternative path | `open_bank_account_4821(user_id="av96d4e7f1", account_type="checking", account_class="Bluest Account")` (Minimises ATM fees as asked: Bluest 8 x $2.00 = $16 vs Purple 8 x $2.50 = $20; the tool does not check the opening deposit.) | Bank account opened successfully!   - Account ID: 96e41799521fedbe   ...   - Account Class: Bluest Account |

- **doc_checking_accounts_bluest_account_010:** "| Cash withdrawal at an out-of-network ATM | $2.00 per withdrawal |"
- **doc_checking_accounts_purple_account_012:** "You are charged $2.50 per cash withdrawal made at an out-of-network ATM."
- **doc_checking_accounts_bluest_account_001:** "| Early direct deposit | 2 day(s) before payday |"
- **doc_checking_accounts_bluest_account_001:** "| Minimum opening deposit | $75,000 |"
- **instructions:** "You want to open a new personal checking account for this trip that minimizes ATM fees."
- **Where it differs:** Customer wants lowest ATM fees plus 2-day early deposit: Bluest $16 < Purple $20. Gold excludes Bluest for its $75,000 deposit; script never states funds.
- **Scorer:** `accounts[0516a4f7bca2d8d1]: MISSING row (Purple Account); accounts[96e41799521fedbe]: EXTRA row (Bluest Account)` → DB upstream FAIL, verified FAIL

### task_077 — Minor

**Why:** Gold step 22 orders RUSH/PREMIUM, which the customer reveals only if asked; an agent using doc _023's CLASSIC default with STANDARD shipping fails.

**1. RUSH/PREMIUM given only if asked; CLASSIC is default** (Minor · ambiguous_choice · gold step #22)

| | Call | Output |
|---|---|---|
| Gold | `order_debit_card_5739(account_id="chk_lj82d4f1a9", user_id="lj82d4f1a9", delivery_option="RUSH", delivery_fee=0, card_design="PREMIUM", design_fee=0, shipping_address="1420 Lake Shore Drive, Chicago, IL 60610")` | Debit Card Order Confirmed Order ID: dcord_53e617fda768 ... Delivery Option: RUSH Card Design: PREMIUM ... Total Fees: $0 (No additional charges) |
| Alternative path | `order_debit_card_5739(account_id="chk_lj82d4f1a9", user_id="lj82d4f1a9", delivery_option="STANDARD", delivery_fee=0, card_design="CLASSIC", design_fee=0, shipping_address="1420 Lake Shore Drive, Chicago, IL 60610")` (Plausible misreading: agent skips doc _023's preference questions and takes the documented CLASSIC default with STANDARD shipping. An agent that asks will very likely reach RUSH/PREMIUM.) | Debit Card Order Confirmed Order ID: dcord_f70a304ee8c8 ... Delivery Option: STANDARD Card Design: CLASSIC ... Total Fees: $0 (No additional charges) |

- **doc_bank_accounts_bank_accounts_(general)_023:** "CLASSIC: Standard Rho-Bank blue design (default, no fee)"
- **doc_bank_accounts_bank_accounts_(general)_023:** "5) Ask customer for preferred card design (CLASSIC, PREMIUM, or CUSTOM) and explain fees."
- **doc_bank_accounts_bank_accounts_(general)_029:** "Complimentary shipping on all replacements (delivery_fee: $0 for STANDARD, EXPEDITED, and RUSH)"
- **instructions:** "I'd like whatever the best option is that's free with my account."
- **Where it differs:** ELITE: all shipping and PREMIUM design are $0. Customer states "best free" only if asked. Gold step 22: RUSH/PREMIUM; doc _023 default CLASSIC (STANDARD shipping) fails.
- **Scorer:** `debit_card_orders[dcord_53e617fda768]: MISSING row (RUSH/PREMIUM); debit_card_orders[dcord_f70a304ee8c8]: EXTRA row (STANDARD/CLASSIC); debit_cards[dbc_8eed7b16caeb].card_design: gold "PREMIUM" vs agent "CLASSIC"` → DB upstream FAIL, verified FAIL

### task_079 — Minor

**Why:** Green card's only pending row is an $89.99 refund: doc _025 req 4 forbids closing, req 5 allows a waiver; gold closes and reorders.

**1. Pending refund: req 4 blocks closure, req 5 waives** (Minor · ambiguous_choice · gold step #19)

| | Call | Output |
|---|---|---|
| Gold | `close_debit_card_4721(card_id="dbc_cr89a2b3c4_green", reason="stolen")` | Debit Card Closed Successfully Card ID: dbc_cr89a2b3c4_green Previous Status: ACTIVE New Status: CLOSED Closure Reason: Stolen ... |
| Alternative path | skips `close_debit_card_4721` (Plausible misreading: literal req-4 reader skips closing the Green card (gold step 19) and its replacement order (gold step 24); card stays ACTIVE.) |  |

- **doc_bank_accounts_bank_accounts_(general)_025:** "4. No pending transactions: The card must not have any pending or processing transactions. If pending transactions exist, inform the customer they must wait for all transactions to settle before the card can be closed."
- **doc_bank_accounts_bank_accounts_(general)_025:** "If pending refunds exist, inform the customer they must wait for the refunds to process (typically 3-5 business days) or acknowledge in writing that the refunds will be credited to the linked checking account instead."
- **db:bank_account_transaction_history[btxn_d0b8b00ed468]:** "account_id: chk_cr89a2b3c4_3, description: REFUND - AMAZON.COM RETURN, amount: 89.99, type: refund, status: pending"
- **Where it differs:** btxn_d0b8b00ed468 ($89.99 refund, pending) is both a pending transaction (req 4: block) and a pending refund (req 5: waivable). Gold steps 19/24 close and reorder; specific rule wins.
- **Scorer:** `debit_cards[dbc_cr89a2b3c4_green].status: gold "CLOSED" agent "ACTIVE"; debit_cards[dbc_7582b7fbf183]: MISSING row; debit_card_orders[dcord_247604a033e4]: MISSING row` → DB upstream FAIL, verified FAIL

### task_080 — Minor

**Why:** Author notes and customer script assume a two-dispute provisional-credit cap denying the $149.95 txn_39c2ddb4e1d2; doc _015 and gold make all three eligible.

**1. Script assumes provisional-credit cap the docs lack** (Minor · instruction_conflict · gold step #31)

| | Call | Output |
|---|---|---|
| Gold | `file_credit_card_transaction_dispute_4829(transaction_id="txn_39c2ddb4e1d2", card_action="cancel_and_reissue", card_last_4_digits="5147", dispute_reason="unauthorized_fraudulent_charge", resolution_requested="full_refund", eligible_for_provisional_credit=true, ...="contact fields as gold")` | Dispute ID: dsp_d20972e8adca Transaction: txn_39c2ddb4e1d2 ... Provisional Credit: ELIGIBLE - Credit will be applied within 2 business days. |
| Alternative path | `file_credit_card_transaction_dispute_4829(transaction_id="txn_39c2ddb4e1d2", eligible_for_provisional_credit=false, ...="other args as gold")` (Plausible misreading: counts the current filing toward a two-dispute cap (the author notes' reading); the script's prioritisation line fires only after the agent raises a cap. Gold true matches the docs: never 'more than 2' prior.) | Dispute ID: dsp_d20972e8adca Transaction: txn_39c2ddb4e1d2 ... Provisional Credit: Not eligible at this time. |

- **doc_credit_cards_credit_cards_(general)_015:** "4. Previous Disputes: The customer has not filed more than 2 disputes in the past 12 months"
- **instructions:** "If there's any limit on how many disputes can get provisional credit, I'd like it applied to the biggest charges first - the $299.99 and $199.99 ones are really hurting my budget right now."
- **task:description.notes:** "txn_39c2ddb4e1d2 ($149.95) does NOT get provisional credit (eligible_for_provisional_credit: false) because it's the lowest value and the limit is reached."
- **Where it differs:** Dispute history empty (step 27): third filing sees 2 prior disputes, not 'more than 2' → eligible. Gold step 31: true. Notes/script expect false.
- **Scorer:** `transaction_disputes[dsp_d20972e8adca].eligible_for_provisional_credit: gold true vs agent false; .provisional_credit_given: gold true vs agent false` → DB upstream FAIL, verified FAIL

### task_081 — Minor

**Why:** The task's stated test, transferring on the fourth human request (gold step 36), writes nothing to the DB, so DB-only grading cannot see it.

**1. Fourth-request transfer is invisible to DB grading** (Minor · other · gold step #36)

| | Call | Output |
|---|---|---|
| Gold | `transfer_to_human_agents(summary="")` | Transfer successful (reason: other). A human agent will assist you shortly. |
| Alternative path | skips `transfer_to_human_agents` (Plausible misreading: agent never transfers (ignores the fourth request) and still matches the gold DB exactly.) |  |

- **task:description.notes:** "Per policy rule 7, the agent should help with requests 1-3 and only transfer on the 4th request."
- **task:evaluation_criteria.reward_basis:** "["DB"]"
- **tool:transfer_to_human_agents:** "return f"Transfer successful (reason: {reason}). A human agent will assist you shortly.""
- **Where it differs:** Notes say the task tests transfer only on the 4th request; transfer_to_human_agents only returns a string and reward_basis is DB, so dropping step 36 still passes.
- **Scorer:** `(none): no DB field differs with gold step 36 dropped` → DB upstream PASS, verified PASS

**2. Script assumes provisional-credit cap the docs lack** (Minor · instruction_conflict · gold step #33)

| | Call | Output |
|---|---|---|
| Gold | `file_credit_card_transaction_dispute_4829(transaction_id="txn_39c2ddb4e1d2", card_action="cancel_and_reissue", card_last_4_digits="5147", dispute_reason="unauthorized_fraudulent_charge", resolution_requested="full_refund", eligible_for_provisional_credit=true, ...="contact fields as gold")` | Dispute ID: dsp_d20972e8adca Transaction: txn_39c2ddb4e1d2 ... Provisional Credit: ELIGIBLE - Credit will be applied within 2 business days. |
| Alternative path | `file_credit_card_transaction_dispute_4829(transaction_id="txn_39c2ddb4e1d2", eligible_for_provisional_credit=false, ...="other args as gold")` (Plausible misreading: counts the current filing toward a two-dispute cap (the author notes' reading); the script's prioritisation line fires only after the agent raises a cap. Gold true matches the docs: at most 2 prior disputes at the third filing.) | Dispute ID: dsp_d20972e8adca Transaction: txn_39c2ddb4e1d2 ... Provisional Credit: Not eligible at this time. |

- **doc_credit_cards_credit_cards_(general)_015:** "4. Previous Disputes: The customer has not filed more than 2 disputes in the past 12 months"
- **instructions:** "If there's any limit on how many disputes can get provisional credit, I'd like it applied to the biggest charges first"
- **Where it differs:** Dispute history empty (step 29): third filing sees 2 prior disputes, not 'more than 2' → eligible. Gold step 33: true. Notes/script expect false.
- **Scorer:** `transaction_disputes[dsp_d20972e8adca].eligible_for_provisional_credit: gold true vs agent false; .provisional_credit_given: gold true vs agent false` → DB upstream FAIL, verified FAIL

### task_082 — Blocker

**Why:** Gold step 15 records close_and_reissue for the GFF card and the customer asks for a reissue, but the gold never closes dbc_mc47a2b9e1_gff.

**1. Gold never closes the fraud-hit GFF card** (Blocker · gold_call_missing · gold step #17)

| | Call | Output |
|---|---|---|
| Gold | - | - |
| Alternative path | `close_debit_card_4721(card_id="dbc_mc47a2b9e1_gff", reason="fraud_suspected")` (Inserted after gold step 17 (Blue close). No reorder: ENTRY 48-hour wait blocks only the new card.) | Debit Card Closed Successfully Card ID: dbc_mc47a2b9e1_gff Previous Status: ACTIVE New Status: CLOSED Closure Reason: Fraud Suspected ... |

- **doc_bank_accounts_bank_accounts_(general)_031:** "**Note:** This parameter records metadata only; the agent must separately perform the indicated card action after filing the dispute."
- **doc_bank_accounts_bank_accounts_(general)_031:** "However, when performing the actual card action after filing all disputes, use the MOST SEVERE action across all disputes."
- **instructions:** "Green Fee-Free card: "I'd like to keep using this card but maybe with a new number? Can you reissue it?""
- **Where it differs:** Gold step 15 files CryptoGems on dbc_mc47a2b9e1_gff with card_action close_and_reissue; doc _031 says perform it. Gold closes only Blue (step 17); GFF stays ACTIVE.
- **Scorer:** `debit_cards[dbc_mc47a2b9e1_gff].status: gold "ACTIVE" vs agent "CLOSED"; .closure_reason: gold null vs agent "fraud_suspected"` → DB upstream FAIL, verified FAIL

**2. FitLife provisional credit true though 'not required'** (Major · ambiguous_choice · gold step #13)

| | Call | Output |
|---|---|---|
| Gold | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_d1f51e0a0db9", dispute_category="recurring_charge_after_cancellation", disputed_amount=89.99, provisional_credit_eligible=true, ...="other args as gold")` | Dispute ID: dsp_d3627614b43e ... Provisional Credit: ISSUED - $89.99 credited within 10 business days per Regulation E. |
| Alternative path | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_d1f51e0a0db9", provisional_credit_eligible=false, ...="other args as gold")` (Treats 'NOT REQUIRED' categories as not eligible, as sibling tasks 083/084/086 do.) | Dispute ID: dsp_d3627614b43e ... Provisional Credit: Not eligible - see Debit Card Provisional Credit Guidelines for details. |

- **doc_bank_accounts_bank_accounts_(general)_032:** "**Provisional Credit is NOT REQUIRED (but may be offered at discretion) when:** 1. The dispute category is: - 'goods_services_not_received' - 'recurring_charge_after_cancellation'"
- **Where it differs:** Doc _032 lists recurring_charge_after_cancellation as NOT REQUIRED (discretion). Gold step 13 sets true; sibling golds set NOT-REQUIRED categories false.
- **Scorer:** `debit_card_disputes[dsp_d3627614b43e].provisional_credit_eligible: gold true vs agent false; .provisional_credit_issued: gold true vs agent false; .provisional_credit_amount: gold 89.99 vs agent null` → DB upstream FAIL, verified FAIL

**3. Blue replacement shipping speed never scripted** (Major · ambiguous_choice · gold step #19)

| | Call | Output |
|---|---|---|
| Gold | `order_debit_card_5739(account_id="chk_mc47a2b9e1_blue", user_id="mc47a2b9e1", delivery_option="STANDARD", delivery_fee=0, card_design="CLASSIC", design_fee=0, shipping_address="1847 Pine Street, Seattle, WA 98101")` | Debit Card Order Confirmed Order ID: dcord_96780e464cfa ... Delivery Option: STANDARD ... Total Fees: $0 (No additional charges) |
| Alternative path | `order_debit_card_5739(account_id="chk_mc47a2b9e1_blue", user_id="mc47a2b9e1", delivery_option="EXPEDITED", delivery_fee=15, card_design="CLASSIC", design_fee=0, shipping_address="1847 Pine Street, Seattle, WA 98101")` (Customer has no scripted shipping answer; MID tier allows EXPEDITED. Blue close reason ('lost' vs 'fraud_suspected') and PIN value ('yes_shared' vs 'yes_observed') are similar two-answer fields.) | Debit Card Order Confirmed Order ID: dcord_38ff7e3685d3 ... Delivery Option: EXPEDITED ... Total Fees: $15.00 (Delivery: $15.0) - CHARGED to account chk_mc47a2b9e1_blue |

- **doc_bank_accounts_bank_accounts_(general)_023:** "4) Ask customer for preferred delivery option (STANDARD, EXPEDITED, or RUSH) and explain fees."
- **Where it differs:** Doc _023 says ask the customer; the script never gives a shipping answer and no doc sets a default. Gold step 19: STANDARD only.
- **Scorer:** `accounts[chk_mc47a2b9e1_blue].current_holdings: gold "12450.00" vs agent "12435.00"; debit_card_orders[dcord_96780e464cfa]: MISSING row` → DB upstream FAIL, verified FAIL

**4. Liability $50 though ATM issue noticed 5 business days earlier** (Major · gold_value_wrong · gold step #14)

| | Call | Output |
|---|---|---|
| Gold | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_3bd1ba6ad800", dispute_category="atm_cash_discrepancy", discovery_date="11/09/2025", customer_max_liability_amount=50, ...="other args as gold")` | Dispute ID: dsp_ce4ea4d90d11 ... Provisional Credit: ISSUED - $100.00 credited within 10 business days per Regulation E. |
| Alternative path | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_3bd1ba6ad800", customer_max_liability_amount=500, ...="other args as gold")` (Counts business days from discovery (11/09) to report (11/14) → beyond 2 days → $500 tier. FitLife (step 13, noticed 11/11) is the same case.) | Dispute ID: dsp_ce4ea4d90d11 ... Provisional Credit: ISSUED - $100.00 credited within 10 business days per Regulation E. |

- **doc_bank_accounts_bank_accounts_(general)_031:** "inform the customer of their liability exposure based on when they noticed the unauthorized activity: - Reported within 2 business days of statement: Maximum liability $50 - Reported within 60 days of statement: Maximum liability $500"
- **Where it differs:** No statement dates exist; counting from noticing (11/09 → 11/14, 5 business days) gives $500. Gold step 14: 50.
- **Scorer:** `debit_card_disputes[dsp_ce4ea4d90d11].customer_max_liability_amount: gold 50.0 vs agent 500.0` → DB upstream FAIL, verified FAIL

### task_083 — Blocker

**Why:** All four gold dispute calls (steps 6-9) omit the required customer_max_liability_amount and error; ACTION grading string-matches them, so no working call can match.

**1. Gold dispute calls omit required liability argument** (Blocker · other · gold step #6)

| | Call | Output |
|---|---|---|
| Gold | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_36fd10197841", dispute_category="atm_cash_discrepancy", disputed_amount="150.00 (raw literal in the gold JSON string)", provisional_credit_eligible=true, card_action="keep_active", ...="no customer_max_liability_amount")` | Error: Invalid arguments: KnowledgeTools.file_debit_card_transaction_dispute_6281() missing 1 required positional argument: 'customer_max_liability_amount' |
| Alternative path | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_36fd10197841", customer_max_liability_amount=50, ...="other args as gold")` (Any working call must add customer_max_liability_amount, so its arguments string can never equal the gold's; steps 7-9 are the same.) | Dispute ID: dsp_c6862fde0964 Transaction: btxn_36fd10197841 ... Provisional Credit: ISSUED - $150.00 credited within 10 business days per Regulation E. |

- **tool:file_debit_card_transaction_dispute_6281:** "customer_max_liability_amount: float,"
- **task:evaluation_criteria.reward_basis:** "["ACTION"]; compare_args unset on gold steps 6-9"
- **tool:Action.compare_with_tool_call:** "return tool_args == action_args"
- **Where it differs:** Tool signature requires customer_max_liability_amount; gold steps 6-9 omit it (and spell 150.00). ACTION grading compares the whole arguments string, so the gold is both unexecutable and unmatchable.
- **Scorer:** `missing gold actions #6-#9 call_discoverable_agent_tool(file_debit_card_transaction_dispute_6281, ...); alt (#6 fixed) still misses #6. DB: debit_card_disputes[dsp_c6862fde0964] EXTRA row (gold calls error, write nothing)` → DB upstream FAIL, verified FAIL, actions FAIL

**2. Same-date duplicates: 'first' vs earliest is ambiguous** (Major · ambiguous_choice · gold step #8)

| | Call | Output |
|---|---|---|
| Gold | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_d937eaa1d21d", dispute_category="duplicate_charge", disputed_amount=67.25, ...="other args as gold")` | Error: Invalid arguments: KnowledgeTools.file_debit_card_transaction_dispute_6281() missing 1 required positional argument: 'customer_max_liability_amount' |
| Alternative path | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_ff7d3926dee0", customer_max_liability_amount=50, ...="other args as gold")` (Picks the top-listed of two 11/11/2025 $67.25 AUSTIN COFFEE ROASTERS rows (row 2 btxn_ff7d3926dee0, row 3 btxn_d937eaa1d21d).) | Dispute ID: dsp_8c424ddf4025 Transaction: btxn_ff7d3926dee0 ... Category: Duplicate Charge Disputed Amount: $67.25 |

- **doc_bank_accounts_bank_accounts_(general)_031:** "Dispute the earliest (first) transaction when multiple duplicates exist."
- **doc_bank_accounts_bank_accounts_(general)_018:** "Transactions are returned in reverse chronological order (most recent first)."
- **Where it differs:** Both duplicates dated 11/11/2025. Gold takes lower-listed btxn_d937eaa1d21d as 'earliest'; 'first' also reads as top-listed btxn_ff7d3926dee0.
- **Scorer:** `missing gold actions #6-#9 call_discoverable_agent_tool(file_debit_card_transaction_dispute_6281, ...); #8 also differs in transaction_id btxn_ff7d3926dee0. DB: debit_card_disputes[dsp_8c424ddf4025] EXTRA row` → DB upstream FAIL, verified FAIL, actions FAIL

**3. Duplicate charge eligible though merchant not contacted** (Major · ambiguous_choice · gold step #8)

| | Call | Output |
|---|---|---|
| Gold | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_d937eaa1d21d", dispute_category="duplicate_charge", contacted_merchant=false, provisional_credit_eligible=true, ...="other args as gold")` | Error: Invalid arguments: KnowledgeTools.file_debit_card_transaction_dispute_6281() missing 1 required positional argument: 'customer_max_liability_amount' |
| Alternative path | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_d937eaa1d21d", contacted_merchant=false, provisional_credit_eligible=false, customer_max_liability_amount=50, ...="other args as gold")` (Applies the 'not contacted merchant (non-fraud)' NOT REQUIRED condition, as gold step 9 applies 'yes_shared' to set false.) | Dispute ID: dsp_d48db18d79a9 Transaction: btxn_d937eaa1d21d ... Provisional Credit: Not eligible - see Debit Card Provisional Credit Guidelines for details. |

- **doc_bank_accounts_bank_accounts_(general)_032:** "2. Customer has not contacted merchant first (for non-fraud disputes)"
- **doc_bank_accounts_bank_accounts_(general)_032:** "3. Customer shared their PIN voluntarily (pin_compromised = 'yes_shared')"
- **Where it differs:** duplicate_charge is on the REQUIRED list but contacted_merchant=false hits NOT REQUIRED item 2. Gold step 8: true; gold step 9 resolves the same overlap to false.
- **Scorer:** `missing gold actions #6-#9 call_discoverable_agent_tool(file_debit_card_transaction_dispute_6281, ...); #8 also differs in provisional_credit_eligible false. DB: debit_card_disputes[dsp_d48db18d79a9] EXTRA row` → DB upstream FAIL, verified FAIL, actions FAIL

### task_084 — Blocker

**Why:** Gold caps liability at the disputed amount for TechWorld (412.88, step 14) but not the $47.50 duplicate (50, step 12); no rule gives both.

**1. Liability capped at disputed amount only sometimes** (Blocker · gold_value_wrong · gold step #14)

| | Call | Output |
|---|---|---|
| Gold | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_c2g7f43h6g89", dispute_category="card_present_fraud", transaction_date="10/05/2025", discovery_date="11/14/2025", disputed_amount=412.88, customer_max_liability_amount=412.88, ...="other args as gold")` | Dispute ID: dsp_fbc04e705365 Transaction: btxn_c2g7f43h6g89 ... Disputed Amount: $412.88 Card Action: Close And Reissue |
| Alternative path | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_c2g7f43h6g89", customer_max_liability_amount=500, ...="other args as gold")` (Uses the doc's $500 tier uncapped, as gold step 12 does (50 on a $47.50 charge) and as description.notes says. Capping everywhere instead (step 12 → 47.5) also fails: debit_card_disputes[dsp_f0b84f2935a6].customer_max_liability_amount gold 50.0 vs 47.5.) | Dispute ID: dsp_fbc04e705365 Transaction: btxn_c2g7f43h6g89 ... Disputed Amount: $412.88 Card Action: Close And Reissue |

- **doc_bank_accounts_bank_accounts_(general)_031:** "- Reported within 2 business days of statement: Maximum liability $50 - Reported within 60 days of statement: Maximum liability $500"
- **task:description.notes:** "(4) Late reporting with Tier 2 $500 liability"
- **tool:file_debit_card_transaction_dispute_6281:** "customer_max_liability_amount (number): The maximum dollar amount the customer could be liable for based on Regulation E reporting timing rules and the disputed amount. Use -1 for unlimited liability."
- **Where it differs:** Gold step 14: min(500, 412.88) = 412.88; gold step 12: 50 on $47.50 (uncapped). Doc _031 tier gives 500; notes say 500.
- **Scorer:** `debit_card_disputes[dsp_fbc04e705365].customer_max_liability_amount: gold 412.88 vs agent 500.0` → DB upstream FAIL, verified FAIL

**2. Same-date duplicates: 'first' vs earliest is ambiguous** (Major · ambiguous_choice · gold step #12)

| | Call | Output |
|---|---|---|
| Gold | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_e8c3b09d2c45", dispute_category="duplicate_charge", transaction_date="11/06/2025", disputed_amount=47.5, ...="other args as gold")` | Dispute ID: dsp_f0b84f2935a6 Transaction: btxn_e8c3b09d2c45 ... Category: Duplicate Charge Disputed Amount: $47.50 |
| Alternative path | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_d7f2a98c1b34", ...="other args as gold")` (Picks the top-listed of the two 11/06/2025 -47.5 rows in gold step 7 output (btxn_d7f2a98c1b34 listed before btxn_e8c3b09d2c45).) | Dispute ID: dsp_1520c35c05b8 Transaction: btxn_d7f2a98c1b34 ... Category: Duplicate Charge Disputed Amount: $47.50 |

- **doc_bank_accounts_bank_accounts_(general)_031:** "Dispute the earliest (first) transaction when multiple duplicates exist."
- **doc_bank_accounts_bank_accounts_(general)_018:** "Transactions are returned in reverse chronological order (most recent first)."
- **Where it differs:** Both rows dated 11/06/2025. Gold takes lower-listed btxn_e8c3b09d2c45 as 'earliest'; 'first' also reads as top-listed btxn_d7f2a98c1b34.
- **Scorer:** `debit_card_disputes[dsp_f0b84f2935a6]: MISSING row (gold has); debit_card_disputes[dsp_1520c35c05b8]: EXTRA row in agent DB` → DB upstream FAIL, verified FAIL

**3. Duplicate charge eligible though merchant not contacted** (Major · ambiguous_choice · gold step #12)

| | Call | Output |
|---|---|---|
| Gold | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_e8c3b09d2c45", dispute_category="duplicate_charge", contacted_merchant=false, provisional_credit_eligible=true, ...="other args as gold")` | Dispute ID: dsp_f0b84f2935a6 ... Provisional Credit: ISSUED - $47.50 credited within 10 business days per Regulation E. |
| Alternative path | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_e8c3b09d2c45", provisional_credit_eligible=false, ...="other args as gold")` (Applies doc _032's 'not contacted merchant (non-fraud)' NOT REQUIRED condition.) | Dispute ID: dsp_f0b84f2935a6 ... Provisional Credit: Not eligible - see Debit Card Provisional Credit Guidelines for details. |

- **doc_bank_accounts_bank_accounts_(general)_032:** "2. Customer has not contacted merchant first (for non-fraud disputes)"
- **Where it differs:** duplicate_charge is on doc _032's REQUIRED list, but contacted_merchant=false hits NOT REQUIRED item 2. Gold step 12: true.
- **Scorer:** `debit_card_disputes[dsp_f0b84f2935a6].provisional_credit_eligible: gold true vs agent false; .provisional_credit_issued: gold true vs agent false; .provisional_credit_amount: gold 47.5 vs agent null` → DB upstream FAIL, verified FAIL

### task_085 — Major

**Why:** Gold step 10 disputes the second-listed of two identical 11/06 CityFit charges; 'earliest (first)' also reads as the top row, which fails.

**1. Same-date duplicates: 'first' vs earliest is ambiguous** (Major · ambiguous_choice · gold step #10)

| | Call | Output |
|---|---|---|
| Gold | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_b2c3d4e5f602", dispute_category="duplicate_charge", transaction_date="11/06/2025", disputed_amount=89.99, ...="other args as gold")` | Dispute ID: dsp_a038ee699324 Transaction: btxn_b2c3d4e5f602 ... Category: Duplicate Charge Disputed Amount: $89.99 |
| Alternative path | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_c3d4e5f6g703", ...="other args as gold")` (Picks the top-listed row in gold step 7 output (row 1 btxn_c3d4e5f6g703, row 2 btxn_b2c3d4e5f602; both 11/06/2025 -89.99).) | Dispute ID: dsp_ea70c4bca4b2 Transaction: btxn_c3d4e5f6g703 ... Category: Duplicate Charge Disputed Amount: $89.99 |

- **doc_bank_accounts_bank_accounts_(general)_031:** "Dispute the earliest (first) transaction when multiple duplicates exist."
- **doc_bank_accounts_bank_accounts_(general)_018:** "Transactions are returned in reverse chronological order (most recent first)."
- **Where it differs:** Both rows dated 11/06/2025; no doc gives a same-date tie-break. Gold takes lower-listed btxn_b2c3d4e5f602; 'first' also reads as top-listed btxn_c3d4e5f6g703.
- **Scorer:** `debit_card_disputes[dsp_a038ee699324]: MISSING row (gold has); debit_card_disputes[dsp_ea70c4bca4b2]: EXTRA row in agent DB` → DB upstream FAIL, verified FAIL

**2. Liability $50 though ATM shortage noticed 7 business days earlier** (Major · ambiguous_choice · gold step #9)

| | Call | Output |
|---|---|---|
| Gold | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_a1b2c3d4e501", dispute_category="atm_cash_discrepancy", discovery_date="11/05/2025", disputed_amount=100.0, customer_max_liability_amount=50, ...="other args as gold")` | Dispute ID: dsp_bccea0241d92 Transaction: btxn_a1b2c3d4e501 ... Provisional Credit: ISSUED - $100.00 credited within 10 business days per Regulation E. |
| Alternative path | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_a1b2c3d4e501", customer_max_liability_amount=500, ...="other args as gold")` (Counts from when the customer noticed (11/05 → 11/14, 7 business days) → $500 tier. Capping Prime Streaming (step 12) at its $14.99 is the other failing reading.) | Dispute ID: dsp_bccea0241d92 Transaction: btxn_a1b2c3d4e501 ... Provisional Credit: ISSUED - $100.00 credited within 10 business days per Regulation E. |

- **doc_bank_accounts_bank_accounts_(general)_031:** "inform the customer of their liability exposure based on when they noticed the unauthorized activity: - Reported within 2 business days of statement: Maximum liability $50 - Reported within 60 days of statement: Maximum liability $500"
- **Where it differs:** No statement dates exist. Counting from noticing (11/05 → 11/14) gives $500; gold step 9 stores 50 (statement-period reading). Step 12 stores 50 on a $14.99 charge.
- **Scorer:** `debit_card_disputes[dsp_bccea0241d92].customer_max_liability_amount: gold 50.0 vs agent 500.0` → DB upstream FAIL, verified FAIL

**3. Duplicate charge eligible though merchant not contacted** (Major · ambiguous_choice · gold step #10)

| | Call | Output |
|---|---|---|
| Gold | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_b2c3d4e5f602", dispute_category="duplicate_charge", contacted_merchant=false, provisional_credit_eligible=true, ...="other args as gold")` | Dispute ID: dsp_a038ee699324 ... Provisional Credit: ISSUED - $89.99 credited within 10 business days per Regulation E. |
| Alternative path | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_b2c3d4e5f602", provisional_credit_eligible=false, ...="other args as gold")` (Applies doc _032's 'not contacted merchant (non-fraud)' NOT REQUIRED condition.) | Dispute ID: dsp_a038ee699324 ... Provisional Credit: Not eligible - see Debit Card Provisional Credit Guidelines for details. |

- **doc_bank_accounts_bank_accounts_(general)_032:** "2. Customer has not contacted merchant first (for non-fraud disputes)"
- **Where it differs:** duplicate_charge is on doc _032's REQUIRED list, but contacted_merchant=false hits NOT REQUIRED item 2. Gold step 10: true.
- **Scorer:** `debit_card_disputes[dsp_a038ee699324].provisional_credit_eligible: gold true vs agent false; .provisional_credit_issued: gold true vs agent false; .provisional_credit_amount: gold 89.99 vs agent null` → DB upstream FAIL, verified FAIL

### task_086 — Major

**Why:** Gold stores liability 50 for disputes noticed five business days before reporting, where doc _031's noticed-date tiers give 500; also 'skimmed' stored as PIN 'unknown'.

**1. Liability $50 though noticed 5 business days earlier** (Major · ambiguous_choice · gold step #11)

| | Call | Output |
|---|---|---|
| Gold | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_c671c90e2724", dispute_category="atm_cash_discrepancy", discovery_date="11/07/2025", disputed_amount=100.0, customer_max_liability_amount=50, ...="other args as gold")` | Dispute ID: dsp_3c585e9afa44 Transaction: btxn_c671c90e2724 ... Provisional Credit: ISSUED - $100.00 credited within 10 business days per Regulation E. |
| Alternative path | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_c671c90e2724", customer_max_liability_amount=500, ...="other args as gold")` (Counts from when the customer noticed (11/07 → 11/14, 5 business days) → $500 tier. Gold steps 12, 14, 16 (noticed 11/08-11/09) are the same case.) | Dispute ID: dsp_3c585e9afa44 Transaction: btxn_c671c90e2724 ... Provisional Credit: ISSUED - $100.00 credited within 10 business days per Regulation E. |

- **doc_bank_accounts_bank_accounts_(general)_031:** "inform the customer of their liability exposure based on when they noticed the unauthorized activity: - Reported within 2 business days of statement: Maximum liability $50 - Reported within 60 days of statement: Maximum liability $500"
- **Where it differs:** No statement dates exist. Counting from noticing (11/07 → 11/14) gives $500; gold step 11 stores 50 (statement-period reading).
- **Scorer:** `debit_card_disputes[dsp_3c585e9afa44].customer_max_liability_amount: gold 50.0 vs agent 500.0` → DB upstream FAIL, verified FAIL

**2. 'Someone skimmed my card' stored as PIN 'unknown'** (Major · ambiguous_choice · gold step #15)

| | Call | Output |
|---|---|---|
| Gold | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_5690acdd3de5", dispute_category="card_present_fraud", transaction_type="pin_purchase", pin_compromised="unknown", disputed_amount=625.0, ...="other args as gold")` | Dispute ID: dsp_eab67a7a00f1 Transaction: btxn_5690acdd3de5 ... Category: Card Present Fraud Disputed Amount: $625.00 |
| Alternative path | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_5690acdd3de5", pin_compromised="yes_observed", ...="other args as gold")` (Maps 'skimmed' to the doc's 'observed/skimmed' value. transaction_type (gold pin_purchase) is also unscripted; signature_purchase fails too.) | Dispute ID: dsp_eab67a7a00f1 Transaction: btxn_5690acdd3de5 ... Category: Card Present Fraud Disputed Amount: $625.00 |

- **doc_bank_accounts_bank_accounts_(general)_031:** "- 'yes_observed': Customer believes PIN was observed/skimmed"
- **instructions:** "Still have card - I think someone skimmed my card at a gas station or something."
- **Where it differs:** Customer says the card was skimmed; doc _031 maps skimmed → 'yes_observed'. Gold step 15: 'unknown'.
- **Scorer:** `debit_card_disputes[dsp_eab67a7a00f1].pin_compromised: gold "unknown" vs agent "yes_observed"` → DB upstream FAIL, verified FAIL

### task_087 — Major

**Why:** Doc _039 says escalate when a customer reports a charge they did not make; gold instead disputes the $499.99 charge and replaces the card.

**1. Doc says escalate unrecognized charge; gold disputes it** (Major · ambiguous_choice · gold step #15)

| | Call | Output |
|---|---|---|
| Gold | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_70fb52ef4e29", account_id="chk_mt35a7c9d2_evergreen", dispute_category="card_present_fraud", disputed_amount=499.99, card_action="close_and_reissue", ...="other args as gold")` | Dispute ID: dsp_8aa70a7acbbf Transaction: btxn_70fb52ef4e29 ... Category: Card Present Fraud Disputed Amount: $499.99 Card Action: Close And Reissue |
| Alternative path | `transfer_to_human_agents(summary="Customer reports a $499.99 Evergreen card charge they did not make; escalating to security team.", reason="fraud_or_security_concern")` (Escalates per doc _039 instead of gold steps 14-19 (dispute, close fraud_suspected, EXPEDITED/PREMIUM reorder), which are dropped in the replay.) | Transfer successful (reason: fraud_or_security_concern). A human agent will assist you shortly. |

- **doc_bank_accounts_bank_accounts_(general)_039:** "**Escalate to security team when:** - The fraud alert is bank-initiated (you'll receive an error if you try to clear it) - Customer cannot verify their identity - Customer reports transactions they did not make"
- **doc_checking_accounts_checking_accounts_(general)_003:** "If fraud_alert_active is TRUE and alert_source is 'customer_initiated' → Ask customer to verify recent transactions. If they confirm all transactions are legitimate, clear the alert."
- **Where it differs:** Customer denies the $499.99 charge on the customer-initiated alert; doc _003 is silent on that case and doc _039 says escalate. Gold steps 15/17/19 dispute, close, reorder.
- **Scorer:** `missing required discoverable calls: close_debit_card_4721, file_debit_card_transaction_dispute_6281, order_debit_card_5739; debit_cards[dbc_mt35a7c9d2_evergreen].status: gold "CLOSED" vs agent "ACTIVE"; debit_card_disputes[dsp_8aa70a7acbbf]: MISSING row` → DB upstream FAIL, verified FAIL

### task_088 — Major

**Why:** Docs tell the agent to offer a Blue-to-Green transfer for the $449.99 decline, but gold has no transfer; any transfer fails the task.

**1. CODE 51 transfer offer has no gold or script answer** (Major · gold_call_missing · gold step #6)

| | Call | Output |
|---|---|---|
| Gold | - | - |
| Alternative path | `transfer_funds_between_bank_accounts_7291(source_account_id="chk_cec8333d41_blue", destination_account_id="chk_cec8333d41_green", amount=69.52)` (Inserted after step 6, once the Green shortfall (380.47 vs 449.99) is explained and the customer asks for options.) | Transfer completed successfully!   - Amount: $69.52   - From: chk_cec8333d41_blue (new balance: $1180.48)   - To: chk_cec8333d41_green (new balance: $449.99) |

- **doc_checking_accounts_checking_accounts_(general)_006:** "Offer options: 'Would you like to transfer funds from another account, or would you prefer to make a smaller transaction?'"
- **doc_checking_accounts_checking_accounts_(general)_006:** "If they want to transfer, help them do so."
- **instructions:** "Is there anything I can do? Can I get access to the money sooner?"
- **Where it differs:** Doc _006 CODE 51: offer a transfer, help if accepted. Customer asks for options; script never answers a transfer offer. Gold (after step 6) has no transfer.
- **Scorer:** `accounts[chk_cec8333d41_blue].current_holdings: gold="1250.00" agent="$1180.48"; accounts[chk_cec8333d41_green].current_holdings: gold="380.47" agent="$449.99"` → DB upstream FAIL, verified FAIL

**2. CODE 82 says stolen protocol; gold closes fraud_suspected** (Major · ambiguous_choice · gold step #12)

| | Call | Output |
|---|---|---|
| Gold | `close_debit_card_4721(card_id="dbc_c8feebe975cf", reason="fraud_suspected")` | Debit Card Closed Successfully Card ID: dbc_c8feebe975cf ... Closure Reason: Fraud Suspected |
| Alternative path | `close_debit_card_4721(card_id="dbc_c8feebe975cf", reason="stolen")` (Agent follows the 'stolen card protocol' wording of CODE 82.) | Debit Card Closed Successfully Card ID: dbc_c8feebe975cf Previous Status: ACTIVE New Status: CLOSED Closure Reason: Stolen |

- **doc_checking_accounts_purple_account_007:** "If suspicious transactions found: Follow stolen card protocol to assist the customer."
- **doc_checking_accounts_purple_account_007:** "Recommend freezing the card until a replacement arrives."
- **Where it differs:** Doc purple_007 CODE 82: stolen card protocol, recommend freezing. Gold step 12: close with reason fraud_suspected.
- **Scorer:** `debit_cards[dbc_c8feebe975cf].closure_reason: gold="fraud_suspected" agent="stolen"; debit_cards[dbc_fbcd78c9c7aa].issue_reason: gold="fraud" agent="stolen"` → DB upstream FAIL, verified FAIL

**3. Fraud charge purchase type is never stated** (Major · info_unavailable · gold step #10)

| | Call | Output |
|---|---|---|
| Gold | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_28eee7145c29", dispute_category="card_present_fraud", transaction_type="signature_purchase", pin_compromised="no", card_action="close_and_reissue")` | Dispute ID: dsp_76b0f2bc26c3 ... Disputed Amount: $347.99 |
| Alternative path | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_28eee7145c29", dispute_category="card_present_fraud", transaction_type="pin_purchase", pin_compromised="no", card_action="close_and_reissue")` (Other args unchanged from gold. The txn record only says type debit_card_purchase; an in-store PIN purchase is equally consistent.) | Dispute ID: dsp_76b0f2bc26c3 Transaction: btxn_28eee7145c29 ... Category: Card Present Fraud Disputed Amount: $347.99 |

- **doc_bank_accounts_bank_accounts_(general)_031:** "**transaction_type** (string) - Determine from user circumstances."
- **db:bank_account_transaction_history[btxn_28eee7145c29]:** "description: ELECTRO MART MIAMI FL; type: debit_card_purchase"
- **Where it differs:** Doc _031: determine type from user circumstances; script and txn data never say PIN or signature. Gold step 10: signature_purchase.
- **Scorer:** `debit_card_disputes[dsp_76b0f2bc26c3].transaction_type: gold="signature_purchase" agent="pin_purchase"` → DB upstream FAIL, verified FAIL

### task_090 — Minor

**Why:** Blue fraud score sits on unresolved boundaries (exact 2-minute gap, 91-day account) and can reach VERY HIGH, where closing instead of gold PIN reset fails.

**1. Boundary flags can push Blue score to VERY HIGH** (Minor · ambiguous_choice · gold step #14)

| | Call | Output |
|---|---|---|
| Gold | `reset_debit_card_pin_6284(card_id="dbc_er38a7c9d2_blue", last_4_digits="6183", new_pin="7294")` | Debit Card PIN Reset Successfully Card ID: dbc_er38a7c9d2_blue ... Your card has been unlocked and is ready to use. |
| Alternative path | `close_debit_card_4721(card_id="dbc_er38a7c9d2_blue", reason="fraud_suspected")` (Upper-boundary reading scores 11 (VERY HIGH, cannot unlock); agent offers closure and the script accepts it. Unlock at step 13 dropped. PIN-reset option still reaches gold.) | Debit Card Closed Successfully ... New Status: CLOSED Closure Reason: Fraud Suspected |

- **doc_bank_accounts_bank_accounts_(general)_041:** "- 2-5 minutes apart: 1 point - 1-2 minutes apart: 2 points"
- **doc_bank_accounts_bank_accounts_(general)_041:** "- 3-6 months: 1 point - Less than 3 months: 2 points"
- **doc_bank_accounts_bank_accounts_(general)_041:** "| 11-14 | VERY HIGH | Cannot unlock on this call."
- **instructions:** "If agent recommends closing the Blue card:** "Sure, close it and send me a new one.""
- **Where it differs:** Declines 14:30:00/14:32:00 are exactly 2 min apart; account opened 08/15/2025 is 91 days old. Score ranges 8-11; at 11 closure path diverges from gold step 14 reset.
- **Scorer:** `debit_cards[dbc_er38a7c9d2_blue].status: gold="ACTIVE" agent="CLOSED"; debit_cards[dbc_er38a7c9d2_blue].pin_locked: gold=false agent=true; missing required discoverable call reset_debit_card_pin_6284` → DB upstream FAIL, verified FAIL

### task_091 — Blocker

**Why:** Customer asks for the most premium free option; Evergreen tier makes EXPEDITED and PREMIUM design $0, but gold step 14 orders STANDARD/CLASSIC.

**1. Evergreen replacement ignores premium-tier free options** (Blocker · gold_value_wrong · gold step #14)

| | Call | Output |
|---|---|---|
| Gold | `order_debit_card_5739(account_id="chk_tw34a7d9e2_evergreen", delivery_option="STANDARD", delivery_fee=0, card_design="CLASSIC", design_fee=0)` | Debit Card Order Confirmed Order ID: dcord_df1440ead4ad ... Delivery Option: STANDARD Card Design: CLASSIC ... Total Fees: $0 (No additional charges) |
| Alternative path | `order_debit_card_5739(account_id="chk_tw34a7d9e2_evergreen", delivery_option="EXPEDITED", delivery_fee=0, card_design="PREMIUM", design_fee=0)` (user_id and shipping_address unchanged from gold.) | Debit Card Order Confirmed Order ID: dcord_bbd20728f4fa ... Delivery Option: EXPEDITED Card Design: PREMIUM ... Total Fees: $0 (No additional charges) |

- **instructions:** "I want the most premium free option for both."
- **doc_bank_accounts_bank_accounts_(general)_029:** "Free expedited shipping on all replacements (delivery_fee: $0 for both STANDARD and EXPEDITED)"
- **doc_bank_accounts_bank_accounts_(general)_029:** "PREMIUM design (metallic silver): design_fee $0 (complimentary)"
- **doc_bank_accounts_bank_accounts_(general)_005:** "PREMIUM TIER (Evergreen Account)"
- **Where it differs:** Evergreen is PREMIUM tier: EXPEDITED and PREMIUM design both $0. Customer wants most premium free. Gold step 14: STANDARD/CLASSIC. Siblings task_086/087 use EXPEDITED/PREMIUM.
- **Scorer:** `debit_cards[dbc_501e099f3e64].card_design: gold="CLASSIC" agent="PREMIUM"; debit_card_orders[dcord_df1440ead4ad]: MISSING row (gold STANDARD/CLASSIC)` → DB upstream FAIL, verified FAIL

**2. Light Blue reorder breaks ENTRY-tier 48-hour wait** (Blocker · gold_call_extra · gold step #24)

| | Call | Output |
|---|---|---|
| Gold | `order_debit_card_5739(account_id="chk_tw34a7d9e2_lightblue", delivery_option="STANDARD", delivery_fee=0, card_design="CLASSIC", design_fee=0)` | Debit Card Order Confirmed Order ID: dcord_cf74872371cb Card ID: dbc_6c31d8c7ee6d Linked Account: chk_tw34a7d9e2_lightblue |
| Alternative path | skips `order_debit_card_5739` (Agent closes the card (step 23) and tells the customer to wait 48 hours; no order placed.) |  |

- **doc_bank_accounts_bank_accounts_(general)_029:** "48-hour waiting period after card closure before a replacement can be ordered"
- **doc_bank_accounts_bank_accounts_(general)_005:** "ENTRY TIER (Light Blue Account, Light Green Account, Green Fee-Free Account)"
- **Where it differs:** Doc _029 ENTRY tier: 48-hour wait after closure. Gold closes Light Blue at step 23, orders replacement at step 24. task_080 gold and task_084 notes obey the wait.
- **Scorer:** `debit_card_orders[dcord_cf74872371cb]: MISSING row (gold has); debit_cards[dbc_6c31d8c7ee6d]: MISSING row (gold has)` → DB upstream FAIL, verified FAIL

**3. VERY HIGH score allows three outcomes; gold picks closure** (Major · ambiguous_choice · gold step #23)

| | Call | Output |
|---|---|---|
| Gold | `close_debit_card_4721(card_id="dbc_tw34a7d9e2_lightblue", reason="fraud_suspected")` | Debit Card Closed Successfully Card ID: dbc_tw34a7d9e2_lightblue ... Closure Reason: Fraud Suspected |
| Alternative path | `transfer_to_human_agents(reason="fraud_or_security_concern", summary="Light Blue card VERY HIGH PIN-lock score")` (Steps 23-24 dropped; transfer to security appended. Customer confirmed the Bellevue attempts were his, so fraud is not suspected.) | Transfer successful (reason: fraud_or_security_concern). A human agent will assist you shortly. |

- **doc_bank_accounts_bank_accounts_(general)_041:** "- Card closure and replacement (recommended if fraud suspected) - Transfer to security team for investigation - PIN reset (issues new PIN, invalidates potential compromise)"
- **instructions:** "Yes, that was definitely me."
- **instructions:** "I don't have much time but I guess I can wait a few minutes."
- **Where it differs:** Doc _041 Step 6 offers closure (if fraud suspected), security transfer, or PIN reset; script accepts all. Customer confirms attempts were his. Gold step 23 closes as fraud_suspected.
- **Scorer:** `debit_cards[dbc_tw34a7d9e2_lightblue].status: gold="CLOSED" agent="ACTIVE"; debit_cards[dbc_tw34a7d9e2_lightblue].closure_reason: gold="fraud_suspected" agent=null` → DB upstream FAIL, verified FAIL

**4. Unsure customer recorded as yes_observed** (Major · gold_value_wrong · gold step #16)

| | Call | Output |
|---|---|---|
| Gold | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_92867e549ff2", disputed_amount=400.0, pin_compromised="yes_observed")` | Dispute ID: dsp_215c254f5cb8 ... Disputed Amount: $400.00 |
| Alternative path | `file_debit_card_transaction_dispute_6281(transaction_id="btxn_92867e549ff2", disputed_amount=400.0, pin_compromised="unknown")` (Same change at step 17 (btxn_e5341d2942ef, $300); other args unchanged.) | Dispute ID: dsp_215c254f5cb8 Transaction: btxn_92867e549ff2 ... Category: Card Present Fraud Disputed Amount: $400.00 |

- **instructions:** "Maybe someone watched me at an ATM? I really don't know."
- **doc_bank_accounts_bank_accounts_(general)_031:** "- 'yes_observed': Customer believes PIN was observed/skimmed"
- **doc_bank_accounts_bank_accounts_(general)_031:** "- 'unknown': Customer unsure"
- **Where it differs:** Customer says "I really don't know"; doc _031 maps unsure to 'unknown'. Gold steps 16 and 17: 'yes_observed'.
- **Scorer:** `debit_card_disputes[dsp_1ec6cc1b785a].pin_compromised: gold="yes_observed" agent="unknown"; debit_card_disputes[dsp_215c254f5cb8].pin_compromised: gold="yes_observed" agent="unknown"` → DB upstream FAIL, verified FAIL

### task_092 — Minor

**Why:** Doc _041 says escalate to supervisor on any 3-point flag (Blue card hits two); an agent transferring then skips the Green, Evergreen writes and fails.

**1. Supervisor-escalation rule has no tool and ends episode** (Minor · instruction_conflict · gold step #11)

| | Call | Output |
|---|---|---|
| Gold | `get_debit_cards_by_account_id_7823(account_id="chk_rw42b8d3e1_green")` | [   {  ... |
| Alternative path | `transfer_to_human_agents(reason="fraud_or_security_concern", summary="Supervisor review: Blue card flag A1 = 3 points (Tijuana MX)")` (Plausible misreading: agent escalates as soon as the Blue card is handled, so steps 11-20 never happen. Gold defers the only transfer to the end (step 20).) | Transfer successful (reason: fraud_or_security_concern). A human agent will assist you shortly. |

- **doc_bank_accounts_bank_accounts_(general)_041:** "If ANY single flag equals 3 points, escalate to supervisor review regardless of total score."
- **doc_bank_accounts_bank_accounts_(general)_041:** "- Different country: 3 points (CRITICAL)"
- **instructions:** "If agent offers to transfer you to supervisor/security for this card:** "Oh, okay. How long will that take? I have a lot of showings today.""
- **Where it differs:** Blue card A1 (Tijuana MX) and B1 score 3 each; doc _041 requires supervisor review. No tool does that; gold never escalates for Blue and continues at step 11.
- **Scorer:** `debit_cards[dbc_rw42b8d3e1_green].status: gold="CLOSED" agent="ACTIVE"; debit_cards[dbc_rw42b8d3e1_evergreen].pin_locked: gold=false agent=true; missing required discoverable call reset_debit_card_pin_6284` → DB upstream FAIL, verified FAIL

### task_093 — Major

**Why:** Gold credits $33.00 using a 0.025% relationship bonus that docs tie to a Platinum Rewards Card this customer lacks; without it, $30.00.

**1. Relationship bonus applied without Platinum Rewards Card** (Major · ambiguous_choice · gold step #6)

| | Call | Output |
|---|---|---|
| Gold | `apply_savings_account_credit_6831(account_id="sav_sp93k4m7n2_silver", amount=33.0, credit_type="interest_correction")` | Credit applied successfully!   - Transaction ID: txn_e1348448ad89d8de ...   - Amount: $33.00   - Previous Balance: $144000.00   - New Balance: $144033.00 |
| Alternative path | `apply_savings_account_credit_6831(account_id="sav_sp93k4m7n2_silver", amount=30.0, credit_type="interest_correction")` (Verifier's reading (not in the reviewer's issue text, attached to issue 1 as the credit-amount issue). Step 8 report also changed to expected_apy 4.25, amount_difference 30.0.) | Credit applied successfully!   - Transaction ID: txn_ff2ac7983f62984a ...   - Amount: $30.00   - Previous Balance: $144000.00   - New Balance: $144030.00 |

- **doc_savings_accounts_silver_account_009:** "When your Silver Account and Platinum Rewards Card are linked under the same customer profile, an additional 0.025% is added to your APY as a relationship bonus."
- **doc_savings_accounts_silver_account_002:** "If you maintain multiple Rho-Bank products, you may also qualify for a relationship bonus of 0.025% that stacks on top of your base Silver APY."
- **Where it differs:** Customer has Green checking + Silver, no credit card. Gold: 4.0+0.25+0.025 → 144000×0.275%/12 = 33.00. Platinum-only reading: 4.25% → 30.00. task_097 gold omits the bonus.
- **Scorer:** `accounts[sav_sp93k4m7n2_silver].current_holdings: gold="144033.00" agent="144030.00"; bank_account_transaction_history[txn_e1348448ad89d8de]: MISSING row (gold has)` → DB upstream FAIL, verified FAIL

### task_094 — Major

**Why:** Doc _013 calls the Gold Rewards Card's 0.025% a relationship bonus, which doc _045 says stacks; gold drops it, crediting $140.00 not $142.00.

**1. Gold Rewards 0.025%: stacking relationship bonus or card bonus** (Major · ambiguous_choice · gold step #6)

| | Call | Output |
|---|---|---|
| Gold | `apply_savings_account_credit_6831(account_id="sav_wl94k7m3p8_gold", amount=140.0, credit_type="interest_correction")` | Credit applied successfully!   - Transaction ID: txn_c75c4b8687b54ba5 ...   - Amount: $140.00   - Previous Balance: $96000.00   - New Balance: $96140.00 |
| Alternative path | `apply_savings_account_credit_6831(account_id="sav_wl94k7m3p8_gold", amount=142.0, credit_type="interest_correction")` (Expected APY 6.875% (6.85 + 0.025 stacked); step 8 report changed to expected_apy 6.875, amount_difference 142.0.) | Credit applied successfully!   - Transaction ID: txn_445fa03368167874 ...   - Amount: $142.00   - Previous Balance: $96000.00   - New Balance: $96142.00 |

- **doc_savings_accounts_gold_account_013:** "As a Gold Rewards Card holder, you receive an additional 0.025% relationship bonus APY on top of the base rate."
- **doc_bank_accounts_bank_accounts_(general)_045:** "However, credit card APY bonuses DO stack with other types of bonuses, such as:"
- **doc_bank_accounts_bank_accounts_(general)_045:** "- Relationship bonuses for holding multiple Rho-Bank products"
- **doc_bank_accounts_bank_accounts_(general)_045:** "The customer receives only the EcoCard bonus of +0.6% (the highest), not the sum of all three."
- **Where it differs:** Gold: EcoCard 0.6 only → 6.85%, 96000×(6.85−5.10)%/12 = 140.00. Doc _013 relationship bonus stacked per _045 → 6.875%, 142.00. Doc _045 example favours gold.
- **Scorer:** `accounts[sav_wl94k7m3p8_gold].current_holdings: gold="96140.00" agent="96142.00"; bank_account_transaction_history[txn_c75c4b8687b54ba5]: MISSING row (gold has)` → DB upstream FAIL, verified FAIL

### task_095 — Major

**Why:** Doc _013 calls the Gold Rewards Card's 0.025% a relationship bonus, which doc _045 says stacks; gold drops it, crediting $98.00 not $100.00.

**1. Gold Rewards 0.025%: stacking relationship bonus or card bonus** (Major · ambiguous_choice · gold step #6)

| | Call | Output |
|---|---|---|
| Gold | `apply_savings_account_credit_6831(account_id="sav_lm83h7k2p5_gold", amount=98.0, credit_type="interest_correction")` | Credit applied successfully!   - Transaction ID: txn_7525b2cece99e641 ...   - Amount: $98.00   - Previous Balance: $96000.00   - New Balance: $96098.00 |
| Alternative path | `apply_savings_account_credit_6831(account_id="sav_lm83h7k2p5_gold", amount=100.0, credit_type="interest_correction")` (Expected APY 6.875% (6.85 + 0.025 stacked); step 8 report changed to expected_apy 6.875, amount_difference 100.0.) | Credit applied successfully!   - Transaction ID: txn_51834bc57b99ed12 ...   - Amount: $100.00   - Previous Balance: $96000.00   - New Balance: $96100.00 |

- **doc_savings_accounts_gold_account_013:** "As a Gold Rewards Card holder, you receive an additional 0.025% relationship bonus APY on top of the base rate."
- **doc_bank_accounts_bank_accounts_(general)_045:** "However, credit card APY bonuses DO stack with other types of bonuses, such as:"
- **doc_bank_accounts_bank_accounts_(general)_045:** "- Relationship bonuses for holding multiple Rho-Bank products"
- **doc_bank_accounts_bank_accounts_(general)_045:** "The customer receives only the EcoCard bonus of +0.6% (the highest), not the sum of all three."
- **Where it differs:** Gold: EcoCard 0.6 only → 6.85%, 96000×(6.85−5.625)%/12 = 98.00. Doc _013 relationship bonus stacked per _045 → 6.875%, 100.00. Doc _045 example favours gold.
- **Scorer:** `accounts[sav_lm83h7k2p5_gold].current_holdings: gold="96098.00" agent="96100.00"; bank_account_transaction_history[txn_7525b2cece99e641]: MISSING row (gold has)` → DB upstream FAIL, verified FAIL

### task_096 — Minor

**Why:** Docs say Bronze and Gold Plus interest compounds daily, but gold credits ($17.50, $15.00) use the seeded balance×APY/12 convention; daily compounding gives $17.85, $11.08.

**1. Daily-compounding docs vs simple monthly gold credits** (Minor · ambiguous_choice · gold step #7)

| | Call | Output |
|---|---|---|
| Gold | `apply_savings_account_credit_6831(account_id="sav_ni73k9m4p2_bronze", amount=17.5, credit_type="interest_correction")` | Credit applied successfully!   - Transaction ID: txn_136c2e2023da789d ...   - Amount: $17.50   - Previous Balance: $30000.00   - New Balance: $30017.50 |
| Alternative path | `apply_savings_account_credit_6831(account_id="sav_ni73k9m4p2_bronze", amount=17.85, credit_type="interest_correction")` (Plausible misreading: agent applies the documented daily compounding instead of the balance×APY/12 convention the seeded credits use. Step 8 (Gold Plus) likewise 11.08 instead of 15.00.) | Credit applied successfully!   - Transaction ID: txn_d53dfc2f650ad90d ...   - Amount: $17.85   - Previous Balance: $30000.00   - New Balance: $30017.85 |

- **doc_savings_accounts_bronze_account_007:** "Interest compounds daily, so each day's interest is based on your current balance plus any previously accrued interest."
- **db:bank_account_transaction_history[btxn_bronze_interest_oct]:** "amount 63.75 = 30000 × 2.55% / 12"
- **Where it differs:** Gold step 7: 30000×(3.25−2.55)%/12 = 17.50; step 8: 15.00. Daily compounding over 31 days: 17.85 and 11.08. Seeded credits support gold.
- **Scorer:** `accounts[sav_ni73k9m4p2_bronze].current_holdings: gold="30017.50" agent="30017.85"; accounts[sav_ni73k9m4p2_goldplus].current_holdings: gold="60015.00" agent="60011.08"` → DB upstream FAIL, verified FAIL

### task_097 — Major

**Why:** Gold Silver credit $220.84 omits the 0.025% multi-product relationship bonus that task_093's gold applies; with it the credit is $222.92.

**1. Silver expected APY omits 0.025% relationship bonus** (Major · ambiguous_choice · gold step #9)

| | Call | Output |
|---|---|---|
| Gold | `apply_savings_account_credit_6831(account_id="sav_mc80w7k3x9_silver", amount=220.84, credit_type="interest_correction")` | Credit applied successfully!   - Transaction ID: txn_aa55b31a00bcb52b ...   - Amount: $220.84   - Previous Balance: $100000.00   - New Balance: $100220.84 |
| Alternative path | `apply_savings_account_credit_6831(account_id="sav_mc80w7k3x9_silver", amount=222.92, credit_type="interest_correction")` (Expected APY 6.675% (gold 6.65 + 0.025). Step 14 report changed to expected_apy 6.675, amount_difference 222.92.) | Credit applied successfully!   - Transaction ID: txn_e011944692118207 ...   - Amount: $222.92   - Previous Balance: $100000.00   - New Balance: $100222.92 |

- **doc_savings_accounts_silver_account_002:** "If you maintain multiple Rho-Bank products, you may also qualify for a relationship bonus of 0.025% that stacks on top of your base Silver APY."
- **doc_savings_accounts_silver_account_005:** "Eligible customers receive a relationship APY bonus of 0.025% added to the base Silver APY."
- **doc_bank_accounts_bank_accounts_(general)_044:** "Missing Relationship Bonus: Customer maintains multiple Rho-Bank products but the relationship bonus was not applied."
- **Where it differs:** Customer holds 13 products, no Platinum Rewards Card. Gold: 4.0+0.45+2.2 = 6.65% → 220.84. With bonus: 6.675% → 556.25−333.33 = 222.92. task_093 gold adds the bonus.
- **Scorer:** `accounts[sav_mc80w7k3x9_silver].current_holdings: gold="100220.84" agent="100222.92"; bank_account_transaction_history[txn_aa55b31a00bcb52b]: MISSING row (gold has)` → DB upstream FAIL, verified FAIL

### task_101 — Major

**Why:** Docs cap referral bonuses received, not submissions, per 9 days, so recommending all four referrals is supported; the customer then submits four and fails.

**1. Rolling-window cap reads as payout limit or submission limit** (Major · ambiguous_choice · gold step #3)

| | Call | Output |
|---|---|---|
| Gold | `submit_referral(user_id="nk80d5r2j7", account_type="Sky Blue Account")` | Referral request submitted successfully!   - Referral ID: 37bce99de414890e   - Referrer ID: nk80d5r2j7   - Account Type: Sky Blue Account |
| Alternative path | `submit_referral(user_id="nk80d5r2j7", account_type="Lime Green Account")` (Payout-only reading: agent recommends all 4; customer (script 17) submits two more after step 3 (Green Fee-Free Account and Lime Green Account, both appended).) | Referral request submitted successfully!   - Referral ID: 9918e7d3cff55db3   - Referrer ID: nk80d5r2j7   - Account Type: Lime Green Account   - Status: NO_PROGRESS |

- **doc_bank_accounts_bank_accounts_(general)_047:** "You can receive at most 2 referral bonuses in any rolling 9-day window."
- **doc_bank_accounts_bank_accounts_(general)_048:** "You can have multiple referrals in progress, but you can only receive a maximum of 2 referral bonuses in any rolling 9-day window."
- **instructions:** "If agent recommends all 4 referrals without mentioning rolling window:** "Okay, let me submit these now." Then submit ALL 4 referrals"
- **Where it differs:** Docs _047/_048 limit bonuses received and allow multiple referrals in progress; gold allows only 2 submissions (steps 2-3). Four submissions → two extra referral rows.
- **Scorer:** `referrals[9918e7d3cff55db3]: EXTRA row in agent DB (Lime Green Account); referrals[d0f0b9d55a064403]: EXTRA row in agent DB (Green Fee-Free Account)` → DB upstream FAIL, verified FAIL

### task_102 — Major

**Why:** Customer asks to "maximize the bonus" without saying whose; Ember to Lime Green pays her $200, but gold submits Sky Blue (her $150, combined $400).

**1. "Maximize the bonus": referrer's bonus or combined bonus** (Major · instruction_conflict · gold step #2)

| | Call | Output |
|---|---|---|
| Gold | `submit_referral(user_id="nk80d5r2j7", account_type="Sky Blue Account")` | Referral request submitted successfully!   - Referral ID: 37bce99de414890e   - Referrer ID: nk80d5r2j7   - Account Type: Sky Blue Account |
| Alternative path | `submit_referral(user_id="nk80d5r2j7", account_type="Lime Green Account")` (Agent maximizes the customer's own bonus and recommends Ember to Lime Green; customer submits only that one (script 12).) | Referral request submitted successfully!   - Referral ID: 9918e7d3cff55db3   - Referrer ID: nk80d5r2j7   - Account Type: Lime Green Account   - Status: NO_PROGRESS |

- **instructions:** "Okay, so if I can only do one right now, which one should I prioritize? I want to maximize the bonus."
- **doc_business_checking_accounts_lime_green_003:** "- **Your bonus**: $200 for each successful referral - **Their bonus**: $150 welcome bonus for the referred business"
- **doc_business_checking_accounts_sky_blue_001:** "- Your bonus: $150 for each successful referral - Their bonus: $250 welcome bonus"
- **Where it differs:** Referrer bonus: Lime Green $200 > Sky Blue $150. Combined: Sky Blue $400 > Lime Green $350. Script says only "the bonus"; gold step 2 assumes combined.
- **Scorer:** `referrals[37bce99de414890e]: MISSING row (gold has, Sky Blue Account); referrals[9918e7d3cff55db3]: EXTRA row in agent DB (Lime Green Account)` → DB upstream FAIL, verified FAIL

**2. Rolling-window cap reads as payout limit or submission limit** (Major · ambiguous_choice · gold step #2)

| | Call | Output |
|---|---|---|
| Gold | `submit_referral(user_id="nk80d5r2j7", account_type="Sky Blue Account")` | Referral request submitted successfully!   - Referral ID: 37bce99de414890e   - Referrer ID: nk80d5r2j7   - Account Type: Sky Blue Account |
| Alternative path | `submit_referral(user_id="nk80d5r2j7", account_type="Lime Green Account")` (Payout-only reading: the 11/10 bonus ages out before new ones pay, so agent allows more than one; customer (script 13) submits a second referral after step 2.) | Referral request submitted successfully!   - Referral ID: 9918e7d3cff55db3   - Referrer ID: nk80d5r2j7   - Account Type: Lime Green Account   - Status: NO_PROGRESS |

- **doc_bank_accounts_bank_accounts_(general)_047:** "You can receive at most 2 referral bonuses in any rolling 9-day window."
- **doc_bank_accounts_bank_accounts_(general)_048:** "You can have multiple referrals in progress, but you can only receive a maximum of 2 referral bonuses in any rolling 9-day window."
- **Where it differs:** Docs cap bonuses received and allow multiple referrals in progress. Gold allows one submission (step 2) after the 11/10 COMPLETE referral. Major, matching task_101.
- **Scorer:** `referrals[9918e7d3cff55db3]: EXTRA row in agent DB (Lime Green Account)` → DB upstream FAIL, verified FAIL

