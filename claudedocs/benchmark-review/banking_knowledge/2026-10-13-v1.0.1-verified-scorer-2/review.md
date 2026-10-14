# `banking_knowledge` benchmark correctness review — v1.0.1

**Benchmark:** `v1.0.1` (`fc0055dc4e`) · **Run date:** 2026-10-13 · **Reviewer:** claude-opus-5-5: 8 parallel reviewers + 4 independent verifiers (Claude Code subagents) · **Effort:** high (set explicitly on every agent) · **Prior review:** 2026-06-25-v1.0.0

The interactive version (`review.html`) shows each task's customer instructions, required documents, gold trajectory, and findings side by side.

## Summary

| Severity | Now | Prior |
|---|---|---|
| Blocker | 12 | 10 |
| Major | 33 | 11 |
| Minor | 24 | 14 |
| None | 28 | 62 |

97 tasks reviewed against v1.0.1 under the revised verified scorer: 12 Blocker, 33 Major, 24 Minor, 28 clean (v1.0.0 review: 10 / 11 / 14 / 62). Severities are the reviewers' verdicts as checked by four independent verifiers, who covered every Blocker and Major, every change from v1.0.0, and a seeded sample of 12 low-severity tasks; they confirmed 70 of 79, upgraded 8 (027 to Blocker; 046, 054, 066, 093, 101 to Major; and issue-level upgrades in 091 and 102) and corrected the reasoning in 075. Nothing is reconciled with any other run. Four of the ten v1.0.0 Blockers persist (063, 082, 083, 084) and six drop to Major because the documents support the gold's reading on one side (039, 040, 041, 074, 075, 101). The rewards rounding rule is documented (round down), which reduces 018, 019, 021 and 022 to a missing required document, but it exposes seed data and a gold value that break the rule (017, 020, 026, 027). 36 tasks the v1.0.0 review rated clean have a defect, 20 of them Major or Blocker, found mostly by replaying gold and alternative actions. The scorer's relaxations decide no Blocker or Major: bank-account closures with a custom reason (060, 061, 062, 067) are clean, and every other divergence tested fails both the verified and the exact comparison. Verifiers noted three possible under-ratings outside their groups that are left as reported: task_092's unscripted shipping speed (Minor, Major in 082), and tasks 080 and 081 if counting the dispute being filed is a supported reading of the provisional-credit limit.

## Systemic issues

1. **Gold depends on information the agent cannot observe** (task_026, task_027, task_028, task_029, task_049, task_053). No agent tool reads cash_back_disputes and the customer's own tool results never reach the agent, so 026-029 grade the same customer claim about dispute approval in opposite ways and any one behaviour passes at most one twin. task_053's gold uses card digits only the customer's get_card_last_4_digits call can return but omits that call, and task_049's gold contains a customer transfer request the script never tells the simulated customer to make.
2. **Gold values contradict the documents or sibling golds** (task_026, task_069, task_082, task_083, task_084, task_091, task_097). task_026 writes 1500 points where the documented round-down rule gives 1499 (sibling 028 rounds down); task_069 picks Silver Plus although Gold and Silver savings both document ATM rebates; task_082 never closes the Green Fee-Free card its own close_and_reissue dispute requires; task_083's four dispute calls omit the required customer_max_liability_amount; task_084's liabilities follow no single rule; task_091 orders STANDARD/CLASSIC where the Premium-tier 'best free option' is EXPEDITED/PREMIUM (as in 086, 087, 090) and reorders an Entry-tier card inside its 48-hour wait; task_097 omits the 0.025% bonus that 093's gold applies.
3. **Gold actions that contradict a documented procedure** (task_014, task_015, task_087, task_088). task_014's gold transfers to a human where the referral document says to explain and not transfer; task_015 gives a referral tool to a customer who cannot be verified; task_087's gold skips the escalation doc_039 prescribes for an unrecognised charge; task_088's decline codes prescribe steps (offer a funds transfer, follow the stolen-card protocol) that the gold and the script do not take.
4. **Strings the gold stores verbatim differ from what the documents tell the agent to write** (task_056, task_059, task_065, task_066, task_068, task_071). The gold stores account_class 'Green Account' while the documents name the products 'Green Account (savings)' and use 'Green Account (checking)' as the example, and general_004 says to open business savings with account_type 'savings' while the gold uses 'business_savings'. Both values are hashed into the account id, so the documented spelling fails.
5. **Ties and multiple defensible products with no tie-breaker** (task_063, task_024, task_025, task_048, task_075, task_076, task_102). task_063 is an exact tie (Bronze and Silver Rewards both add +0.15% at $0); in the others a second product is as good or better under a supported reading: Silver Zoom's promo (024), Apple Music's category (025), Platinum and Business Silver against the competitor (048), ATM fee stacking (075), Bluest's fees and opening deposit (076), and whose referral bonus to maximise (102).
6. **Rules with two document-supported readings** (task_039, task_040, task_041, task_093, task_094, task_095, task_097, task_101). Whether disputes filed earlier in the same call count toward the provisional-credit limit (039-041), whether the 0.025% relationship bonus stacks with a card bonus (093-095, 097), and whether the referral limit caps submissions or bonuses (101). Each gold takes one reading and fails an agent that applies the other consistently.
7. **Fee and rewards data that break the documented rules** (task_017, task_020, task_027, task_072, task_073, task_074, task_075). Seed rewards in 017 and for Amara (020, 026, 027) do not follow the documented round-down rule; refunds in 072-074 count fees dated after the fixed clock; 072-074 assume out-of-network and foreign ATM fees do not stack while 075 and 076 need them to, and 074 rebates Rho-Bank's own fee where Purple's documents limit the rebate to operator fees.
8. **Dispute fields with no single documented rule** (task_084, task_085, task_086, task_088). How customer_max_liability_amount is derived (no statement dates exist; the $500 tier is capped at the amount, the $50 tier is not), which provisional-credit list applies when the REQUIRED and NOT REQUIRED lists overlap, and how pin_compromised and the transaction type are chosen all vary between sibling golds.
9. **Hidden ordering and choices the script never states** (task_041, task_046, task_053, task_054). task_054 and task_053 need the credit limit increase before the dispute the customer asked for first; task_046 passes only if the agent reports just the first failed retention check, otherwise the scripted customer pays the balance; task_041 never states the refund types the gold records.

## Changes since the prior review

| Task | Prior | Now | Status | Headline |
|---|---|---|---|---|
| task_006 | None | Minor | new | The answer (EcoCard) is correct and unique, but the deciding fact, that Crypto-Cash Back needs a 660 credit score, is printed as a dollar amount ('$660'). |
| task_014 | None | Major | new | The gold transfers the customer to a human, but the KB's own referral-link procedure says that when a card has no documented referral program the agent must explain and 'not transfer to a human', so careful agents fail. |
| task_015 | None | Major | new | The gold expects the agent to give the referral-link tool to a customer it cannot verify (she knows only her phone number), but no document says verification is unnecessary, so cautious agents refuse and fail. |
| task_016 | Minor | None | resolved | Clean: the only in-progress referral is a Silver Rewards Card referral whose documented requirement is $750 of spending, and the customer then makes exactly that purchase. |
| task_017 | Major | Major | changed | The Hilton transaction was credited one point more than the documented rate allows, but the gold leaves it undisputed. An agent that follows the rewards rules and flags it fails. |
| task_018 | Major | Minor | changed | Solvable: applying the documented round-down rule to all 49 transactions yields exactly the six gold disputes, but the rounding document is missing from the task's required-document list. |
| task_019 | Major | Minor | changed | Solvable: the documented round-down rule yields exactly the four gold disputes, but the rounding document is missing from the task's required-document list. |
| task_020 | Minor | Major | changed | This customer's stored rewards were rounded the opposite way from the documented round-down rule, so an agent that follows the rule sees nine extra 1-point errors the gold does not dispute. |
| task_021 | Major | Minor | changed | Solvable: after applying the documented round-down rule and the WeWork/ThredUp exceptions, exactly two transactions are wrong, matching the gold. Only the rounding document is missing from the required list. |
| task_022 | Major | Minor | changed | Solvable but long: across 77 transactions on four cards, the documented rates, exclusions and round-down rule give exactly the ten gold disputes. Only the rounding document is missing from the required list. |
| task_024 | None | Major | new | The gold picks the Business Bronze card ($900 back), but the Silver Zoom card's triple-cash-back promo pays at least $1,200 on the truck, if a landscaping company can hold that logistics-oriented card. |
| task_026 | Minor | Blocker | changed | The agent is asked to correct rewards after disputes are resolved, but no tool lets it see a dispute's status. The gold's corrected Zoom value (1500) also breaks the documented round-down rule, which gives 1499. |
| task_027 | Minor | Blocker | changed | The task is meant to catch an agent that updates rewards on the customer's false claim that disputes were resolved, but the agent has no way to check dispute status, so passing depends on whether it trusts the customer at all. |
| task_028 | None | Blocker | new | The agent must take the customer's word that her disputes were approved, because it has no way to check, while the twin task 029 fails any agent that does exactly that. |
| task_029 | Major | Blocker | changed | The agent is expected to catch a customer lying that her disputes were approved, but it has no tool to check, and the twin task 028 rewards believing the same words. |
| task_032 | None | Minor | new | The intended three-speed-bump-then-transfer sequence is right, but the action grader cannot check how many times or in what order the tools were used. |
| task_033 | None | Minor | new | The incident transfer protocol is followed correctly by the gold, but the action grader cannot check the required order (1822, then 0218, then transfer). |
| task_034 | None | Minor | new | The rule to refuse transfer until the eighth request is clear, but the action grader would pass an agent that transferred at once. |
| task_035 | None | Minor | new | The emergency credit-bureau transfer is well specified, but the action grader cannot tell whether the agent escalated immediately or verified first, as the task intends. |
| task_038 | None | Minor | new | The three Amazon disputes and the card replacement are determined, but the script never says whether the customer wants paid expedited shipping, which the gold records as yes. |
| task_039 | Blocker | Major | persists | Which disputes get provisional credit depends on whether disputes filed earlier in the same call count toward the 'no more than 2 in 12 months' rule, which the documents never settle, and on filing order. |
| task_040 | Blocker | Major | persists | With one dispute already on file, the gold gives provisional credit to only the first two new disputes filed, which depends on an unstated counting rule and on filing order; one refund type is also left to guesswork. |
| task_041 | Blocker | Major | changed | Sixteen-dispute task: the official answer grants provisional credit to only two disputes, which follows one reasonable reading of the 'no more than 2 disputes in 12 months' rule but not another, and several refund choices (including an exact $69.99 partial refund) are never stated by the customer. |
| task_045 | None | Minor | new | The Business Silver closure flow (pay $125, recommend Business Platinum, then apply a $20 retention credit) is derivable, but the customer gives two closure reasons and only one is accepted. |
| task_046 | None | Major | new | Closure correctly stops at a pending dispute, but the dispute record cannot be tied to the Business Silver card from tool data, and an agent that also pays the balance the customer asks about fails. |
| task_047 | None | Minor | new | The two-card retention flow (Business Platinum for the Silver Zoom, then a $50 credit on the under-2-year Platinum) is derivable, but the second closure reason is stated two ways. |
| task_048 | None | Major | new | In the four-card closure task, the gold expects the customer to apply for the Silver Rewards Card, but other Rho-Bank cards (Platinum Rewards, Business Silver) also beat the competitor's 3.25% offer, so the card applied for depends on which one the agent recommends. |
| task_049 | None | Blocker | new | The official answer records the customer pressing a 'request human transfer' tool that the script never tells the simulated customer to use, so correct agent work fails whenever the customer simply asks out loud. |
| task_050 | None | Minor | new | A simple $2,500 credit-limit increase on a Gold card is solvable, but the document that says which tier the Gold card belongs to is not in the task's required-document list. |
| task_053 | None | Blocker | new | The official answer files the dispute with card digits '2791', which only the customer's own lookup tool can supply, yet it leaves out that lookup call, so a run where the customer follows the script and looks the number up can never match. |
| task_054 | None | Major | new | The customer never says whether she wants expedited shipping for the replacement card, but the gold records expedited; the documents' strong recommendation for fraud cases makes it the likely default. |
| task_056 | None | Major | new | The business-savings procedure tells the agent to open the account with account_type 'savings', but the gold uses 'business_savings'; following the document creates a differently keyed personal savings account and fails. |
| task_057 | Minor | Minor | changed | The task's headline test (refusing to open savings after the customer falsely claims 14 days have passed) is not graded, because the tool rejects the savings account anyway and the attempt leaves the compared state unchanged. |
| task_059 | None | Major | new | The gold opens the savings product as 'Green Account', but the documents name it 'Green Account (savings)' and give 'Green Account (checking)' as an official class string, so an agent can reasonably pick a spelling that fails. |
| task_065 | None | Major | new | The pairing and order are well determined (Evergreen checking plus Green savings, opened before closing Light Blue), but the gold spells the savings class 'Green Account' while the documents also support 'Green Account (savings)'. |
| task_066 | None | Major | new | The savings/checking/credit-card combination is uniquely derivable, but the savings account name the gold uses ("Green Account") is not the name the documents use for that product ("Green Account (savings)"). |
| task_068 | None | Major | new | The gold opens the Green checking account as "Green Account", but the checking-opening procedure gives "Green Account (checking)" as the example class name, so an agent following the procedure literally fails. |
| task_069 | None | Blocker | new | The gold's Silver Plus savings (3.5% total) is beaten by Gold savings (5.7%) and even Silver savings (4.1%), both of which the documents say offer ATM fee rebates, so a correct agent fails. |
| task_070 | None | Minor | new | Sky Blue is the correct pick under the active November promotion, but the script never confirms the business meets Sky Blue's 4-year startup age limit. |
| task_071 | None | Major | new | The account choices are right, but the business-savings procedure tells the agent to open the account with account_type 'savings' while the gold uses 'business_savings', and the two produce different accounts. |
| task_072 | Minor | Major | changed | Both gold refund amounts include fee errors dated after the benchmark's fixed "today" (11/14/2025), so an agent that only reviews fees posted so far credits $13.50 and $3.00 instead of $14.00 and $3.50. |
| task_073 | Major | Major | changed | The Green account's gold refund ($9.00) includes a duplicate fee dated 11/15, after the benchmark's fixed "today", so an agent that only reviews fees posted so far credits $6.00. |
| task_074 | Blocker | Major | changed | The corrected Light Blue refund ($14.50) and the Dark Green and Evergreen refunds are right, but the Purple refund ($27.00) still counts a fee dated after "today" and a rebate the Purple docs limit to ATM-operator fees. |
| task_075 | Blocker | Major | changed | Green Fee-Free is cheapest only if Purple's $2.50 out-of-network fee applies abroad and is not covered by Purple's $30 monthly ATM rebate; the benchmark's own fee-refund tasks assume the opposite on both points. |
| task_076 | None | Major | new | Bluest has lower ATM fees than the gold's Purple Account under every reading of the fee docs; the gold excludes Bluest for its $75,000 opening deposit, but the script never says whether the customer can make it. |
| task_077 | None | Minor | new | The lost-wallet flow is derivable, but the gold records RUSH shipping and the PREMIUM card design, which the customer specifies only if asked and only as "the best option that's free". |
| task_079 | None | Minor | new | The gold is right, but the card-closing rules say both 'no pending transactions' and 'pending refunds can be waived', and the Green account's only pending row is a refund. |
| task_080 | None | Minor | new | Five-card stolen-wallet task has a reachable gold, but the customer script and author notes are built around a provisional-credit cap that the documents and gold do not apply. |
| task_081 | None | Minor | new | Same as task_080 plus four requests for a human, but the DB check cannot see whether the agent transferred on the fourth request, and the same provisional-credit script mismatch is present. |
| task_084 | Blocker | Blocker | changed | The gold's liability amounts follow no consistent rule: it caps one dispute at the charge amount but not another, so any agent applying one rule throughout gets a value wrong. |
| task_085 | Minor | Major | changed | The verify-the-customer's-claims test works, but which duplicate gym charge to dispute, the liability amounts, and one provisional-credit flag each depend on a reading the documents do not settle. |
| task_086 | Minor | Major | changed | The large six-dispute scenario is mostly derivable, but liability amounts, the PIN status after a reported skimming, and the purchase type of the late fraud charge each have more than one defensible answer. |
| task_087 | None | Major | new | Fixing three declined cards is well specified, but one security document says to hand the customer to the security team when they report a charge they did not make, which would skip the gold's dispute and replacement. |
| task_088 | Minor | Major | changed | Three decline problems with a reachable gold, but the documents invite an account-to-account transfer the gold does not expect and disagree on freezing versus closing the cloned card, and the purchase type of the fraud charge is never stated. |
| task_090 | None | Minor | new | The three-card PIN-lock case resolves to the gold, but the Blue card's fraud score sits on several undefined boundaries and the Evergreen replacement's card design is never stated by the customer. |
| task_091 | None | Blocker | new | For the Evergreen and Light Blue replacements the gold ignores the tier rules: it orders standard shipping and design when the customer asked for the most premium free option, and it orders a Light Blue replacement immediately despite the 48-hour wait. Several other choices are also left open. |
| task_093 | None | Major | new | The Silver interest correction ($33.00) is derivable, but the documented daily compounding does not match the system's simple monthly interest, and the discrepancy report's content is never graded. |
| task_094 | Minor | Major | persists | Whether the Gold Rewards Card's +0.025% stacks on top of the EcoCard bonus is ambiguous in the docs, so the $140.00 correction is one of two defensible answers. |
| task_096 | None | Minor | persists | Both savings corrections ($17.50 Bronze, $15.00 Gold Plus) are derivable, but one needed boost document is missing from the task's list, and the interest-formula and report-grading gaps apply here too. |
| task_100 | Minor | None | resolved | Clean: from the on-file open date (65 days of tenure) Hunter Green ($175) is the best referral the customer qualifies for, and World Blue's 90-day tenure rule correctly blocks the account she owns. |
| task_101 | Blocker | Major | changed | The gold (Vikram to Purple, TechFlow to Sky Blue) follows the docs' 2-per-9-days referral limit, though the limit's wording mixes 'bonuses received' with 'referrals made'. |

## All tasks

| Task | Final | Reviewer | Verifier | Reconciled | Prior | Instr. | Docs det. | Cx | Ordering | Gold ok | Headline |
|---|---|---|---|---|---|---|---|---|---|---|---|
| task_001 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 2 | None | Yes | Clean: among no-annual-fee personal cards, Gold Rewards (2.5% flat, needs Rho-Bank+, which the customer has) clearly gives the most cash back on everyday spending. |
| task_002 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 3 | None | Yes | Clean: Platinum Rewards pays the highest cash back (10%), and its $200 fee drops to an effective $50 through the documented $150 rebate at her $50k/month spend, which fits her $100/year limit. |
| task_003 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 3 | None | Yes | Clean: Silver and Gold are the only $0-fee cards that meet all three hard requirements, and for a mostly-travel spender Silver's 4% travel rate beats Gold's flat 2.5%. |
| task_004 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 2 | None | Yes | Clean: the customer matches only 1 of 4 identity fields, so verification fails, and the Tier-1 code 'account_ownership_dispute' explicitly covers 'identity verification failures requiring specialist'. |
| task_005 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 3 | Soft | Yes | Clean: the KB has an internal doc that accepts this exact bypass code and spells out the log_verification field values, so after the transfer the agent should log the bypass and change the email. |
| task_006 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Partial | 2 | None | Yes | The answer (EcoCard) is correct and unique, but the deciding fact, that Crypto-Cash Back needs a 660 credit score, is printed as a dollar amount ('$660'). |
| task_007 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 3 | None | Yes | Clean: on the fixed date (2025-11-14), the only personal card with an active points or cash sign-up bonus that a non-invited customer can get is EcoCard, because Silver's $500 bonus window closed on 2025-06-30. |
| task_008 | Minor | Minor | Confirmed (Minor) | - | Minor | Sufficient | Partial | 2 | None | Yes | The gold reason code is right under the documented 'highest tier' rule, but the Tier-2 code 'unconfirmed_external_communication' names this exact situation (a mailed flyer), so the two codes overlap. |
| task_010 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 3 | Soft | Yes | Clean: the Platinum referral was auto-denied by the documented 2-per-rolling-7-days cap, that window has long passed, so after verifying the customer the agent explains he can retry and he resubmits the Platinum referral. |
| task_012 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 1 | None | Yes | Clean: the KB has no procedure for travel notifications, so the agent should say it has no information, and when the customer then asks for a human it transfers with 'kb_search_unsuccessful_customer_requests_transfer'. |
| task_014 | Major | Major | Confirmed (Major) | - | None | Sufficient | No | 2 | None | No | The gold transfers the customer to a human, but the KB's own referral-link procedure says that when a card has no documented referral program the agent must explain and 'not transfer to a human', so careful agents fail. |
| task_015 | Major | Major | Confirmed (Major) | - | None | Partial | Partial | 4 | Soft | Yes | The gold expects the agent to give the referral-link tool to a customer it cannot verify (she knows only her phone number), but no document says verification is unnecessary, so cautious agents refuse and fail. |
| task_016 | None | None | Confirmed (None) | - | Minor | Sufficient | Yes | 2 | None | Yes | Clean: the only in-progress referral is a Silver Rewards Card referral whose documented requirement is $750 of spending, and the customer then makes exactly that purchase. |
| task_017 | Major | Major | Confirmed (Major) | - | Major | Sufficient | Partial | 3 | Soft | No | The Hilton transaction was credited one point more than the documented rate allows, but the gold leaves it undisputed. An agent that follows the rewards rules and flags it fails. |
| task_018 | Minor | Minor | Confirmed (Minor) | - | Major | Sufficient | Yes | 4 | Soft | Yes | Solvable: applying the documented round-down rule to all 49 transactions yields exactly the six gold disputes, but the rounding document is missing from the task's required-document list. |
| task_019 | Minor | Minor | Confirmed (Minor) | - | Major | Sufficient | Yes | 4 | Soft | Yes | Solvable: the documented round-down rule yields exactly the four gold disputes, but the rounding document is missing from the task's required-document list. |
| task_020 | Major | Major | Confirmed (Major) | - | Minor | Sufficient | Partial | 4 | Soft | No | This customer's stored rewards were rounded the opposite way from the documented round-down rule, so an agent that follows the rule sees nine extra 1-point errors the gold does not dispute. |
| task_021 | Minor | Minor | Confirmed (Minor) | - | Major | Sufficient | Yes | 4 | Soft | Yes | Solvable: after applying the documented round-down rule and the WeWork/ThredUp exceptions, exactly two transactions are wrong, matching the gold. Only the rounding document is missing from the required list. |
| task_022 | Minor | Minor | Confirmed (Minor) | - | Major | Sufficient | Yes | 5 | Soft | Yes | Solvable but long: across 77 transactions on four cards, the documented rates, exclusions and round-down rule give exactly the ten gold disputes. Only the rounding document is missing from the required list. |
| task_023 | Minor | Minor | Not sampled (-) | - | Minor | Sufficient | Yes | 4 | None | Yes | Solvable: measured in the documented anniversary-day windows, the customer cleared $7,500 in all 12 months and qualifies, so she applies for the Diamond card. Her stated card-open date (Nov 2024) conflicts with the database (11/10/2022). |
| task_024 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 4 | None | Yes | The gold picks the Business Bronze card ($900 back), but the Silver Zoom card's triple-cash-back promo pays at least $1,200 on the truck, if a landscaping company can hold that logistics-oriented card. |
| task_025 | Major | Major | Confirmed (Major) | - | Major | Sufficient | Partial | 5 | None | Yes | Which card pays most on a $100,000 Apple Music purchase depends on whether Apple Music is an excluded 'Apple' merchant on one card and qualifying 'software/media' spend on another. Neither point is spelled out, and different readings pick different winners. |
| task_026 | Blocker | Blocker | Confirmed (Blocker) | - | Minor | Partial | No | 4 | Strict | No | The agent is asked to correct rewards after disputes are resolved, but no tool lets it see a dispute's status. The gold's corrected Zoom value (1500) also breaks the documented round-down rule, which gives 1499. |
| task_027 | Blocker | Major | Upgraded (Blocker) | - | Minor | Partial | Partial | 4 | Soft | No | The task is meant to catch an agent that updates rewards on the customer's false claim that disputes were resolved, but the agent has no way to check dispute status, so passing depends on whether it trusts the customer at all. |
| task_028 | Blocker | Blocker | Confirmed (Blocker) | - | None | Partial | No | 4 | Strict | Yes | The agent must take the customer's word that her disputes were approved, because it has no way to check, while the twin task 029 fails any agent that does exactly that. |
| task_029 | Blocker | Blocker | Confirmed (Blocker) | - | Major | Partial | No | 4 | Strict | Yes | The agent is expected to catch a customer lying that her disputes were approved, but it has no tool to check, and the twin task 028 rewards believing the same words. |
| task_031 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 2 | Soft | Yes | Clean: every value in the single Marriott dispute follows from what the customer says, the transaction data, and the dispute documents. |
| task_032 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 2 | Strict | Yes | The intended three-speed-bump-then-transfer sequence is right, but the action grader cannot check how many times or in what order the tools were used. |
| task_033 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 2 | Strict | Yes | The incident transfer protocol is followed correctly by the gold, but the action grader cannot check the required order (1822, then 0218, then transfer). |
| task_034 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 2 | Strict | Yes | The rule to refuse transfer until the eighth request is clear, but the action grader would pass an agent that transferred at once. |
| task_035 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 1 | Soft | Yes | The emergency credit-bureau transfer is well specified, but the action grader cannot tell whether the agent escalated immediately or verified first, as the task intends. |
| task_036 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 2 | Soft | Yes | Clean: the replacement-card order (reason, work address, expedited shipping) follows directly from the script and the replacement procedure. |
| task_037 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 3 | Soft | Yes | Clean: the replacement order and both fraud disputes are fully determined by the script, the transaction data, and the provisional-credit rules. |
| task_038 | Minor | Minor | Confirmed (Minor) | - | None | Partial | Yes | 3 | Soft | Yes | The three Amazon disputes and the card replacement are determined, but the script never says whether the customer wants paid expedited shipping, which the gold records as yes. |
| task_039 | Major | Major | Confirmed (Major) | - | Blocker | Partial | Partial | 5 | Strict | Yes | Which disputes get provisional credit depends on whether disputes filed earlier in the same call count toward the 'no more than 2 in 12 months' rule, which the documents never settle, and on filing order. |
| task_040 | Major | Major | Confirmed (Major) | - | Blocker | Partial | Partial | 5 | Strict | Yes | With one dispute already on file, the gold gives provisional credit to only the first two new disputes filed, which depends on an unstated counting rule and on filing order; one refund type is also left to guesswork. |
| task_041 | Major | Major | Confirmed (Major) | - | Blocker | Partial | Partial | 5 | Soft | Yes | Sixteen-dispute task: the official answer grants provisional credit to only two disputes, which follows one reasonable reading of the 'no more than 2 disputes in 12 months' rule but not another, and several refund choices (including an exact $69.99 partial refund) are never stated by the customer. |
| task_043 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 3 | Soft | Yes | Platinum card closure with a $75 balance payoff and a 2+-year annual-fee waiver; every graded value is derivable from the documents and data. |
| task_044 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 3 | Soft | Yes | A Gold card holder leaving for an 8% competitor card should be steered to the Platinum Rewards Card (10% cash back, no foreign fee), which is the only Rho-Bank card that beats the offer. |
| task_045 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 4 | Strict | Yes | The Business Silver closure flow (pay $125, recommend Business Platinum, then apply a $20 retention credit) is derivable, but the customer gives two closure reasons and only one is accepted. |
| task_046 | Major | Minor | Upgraded (Major) | - | None | Sufficient | Partial | 3 | Soft | Yes | Closure correctly stops at a pending dispute, but the dispute record cannot be tied to the Business Silver card from tool data, and an agent that also pays the balance the customer asks about fails. |
| task_047 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 4 | Soft | Yes | The two-card retention flow (Business Platinum for the Silver Zoom, then a $50 credit on the under-2-year Platinum) is derivable, but the second closure reason is stated two ways. |
| task_048 | Major | Major | Confirmed (Major) | - | None | Partial | Partial | 5 | Strict | Yes | In the four-card closure task, the gold expects the customer to apply for the Silver Rewards Card, but other Rho-Bank cards (Platinum Rewards, Business Silver) also beat the competitor's 3.25% offer, so the card applied for depends on which one the agent recommends. |
| task_049 | Blocker | Blocker | Confirmed (Blocker) | - | None | Insufficient | Yes | 5 | Soft | No | The official answer records the customer pressing a 'request human transfer' tool that the script never tells the simulated customer to use, so correct agent work fails whenever the customer simply asks out loud. |
| task_050 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 3 | Strict | Yes | A simple $2,500 credit-limit increase on a Gold card is solvable, but the document that says which tier the Gold card belongs to is not in the task's required-document list. |
| task_051 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 4 | Strict | Yes | The entry-tier credit-limit flow (cap a 30% request at 25%, deny for 75% utilization, pay off $3,000, approve $5,000) is fully derivable. |
| task_052 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 3 | Strict | Yes | A customer twists policies to dodge the 120-day entry-tier cooldown; the agent must submit the $400 request and deny it for an active cooldown, and the documents determine this uniquely. |
| task_053 | Blocker | Blocker | Confirmed (Blocker) | - | None | Sufficient | Partial | 4 | Strict | No | The official answer files the dispute with card digits '2791', which only the customer's own lookup tool can supply, yet it leaves out that lookup call, so a run where the customer follows the script and looks the number up can never match. |
| task_054 | Major | Minor | Upgraded (Major) | - | None | Partial | Yes | 4 | Strict | Yes | The customer never says whether she wants expedited shipping for the replacement card, but the gold records expedited; the documents' strong recommendation for fraud cases makes it the likely default. |
| task_055 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 4 | Soft | Yes | Clean: Purple Account and Silver Plus Account are the only products that meet every stated need, and the check deposit is fully scripted. |
| task_056 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 4 | Soft | Yes | The business-savings procedure tells the agent to open the account with account_type 'savings', but the gold uses 'business_savings'; following the document creates a differently keyed personal savings account and fails. |
| task_057 | Minor | Minor | Confirmed (Minor) | - | Minor | Sufficient | Yes | 3 | Soft | Yes | The task's headline test (refusing to open savings after the customer falsely claims 14 days have passed) is not graded, because the tool rejects the savings account anyway and the attempt leaves the compared state unchanged. |
| task_058 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 5 | None | Yes | Clean: EcoCard plus Silver Account is the unique best net yield on $20,000 ($1,190 against $1,170 for the next pair), and both gold writes follow from it. |
| task_059 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 5 | None | Yes | The gold opens the savings product as 'Green Account', but the documents name it 'Green Account (savings)' and give 'Green Account (checking)' as an official class string, so an agent can reasonably pick a spelling that fails. |
| task_060 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 4 | Strict | Yes | Clean: Silver Plus Account is the only savings product meeting all six needs, and the documented 14-day rule forces opening it before closing the Green Account. |
| task_061 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 4 | Strict | Yes | Clean: same savings choice and ordering as task_060, plus a documented $25 early-closure fee that the customer covers with a scripted $25 check deposit. |
| task_062 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 5 | Strict | Yes | Clean: Navy Blue and Silver Plus are the only fits, and the documented eligibility rules force the one workable order (open business checking, then savings, then close accounts). |
| task_063 | Blocker | Blocker | Confirmed (Blocker) | - | Blocker | Sufficient | No | 4 | None | Yes | Bronze Rewards and Silver Rewards add the same +0.15% to the recommended Silver Plus Account, and both meet the customer's conditions, but the gold accepts only Silver Rewards. |
| task_064 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 5 | None | Yes | Clean: with the customer's Rho-Bank+ subscription, Gold Rewards Card plus Gold Plus Account is the unique best net yield on $30,000 ($1,905 against $1,845 for the next pair). |
| task_065 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 4 | Strict | Yes | The pairing and order are well determined (Evergreen checking plus Green savings, opened before closing Light Blue), but the gold spells the savings class 'Green Account' while the documents also support 'Green Account (savings)'. |
| task_066 | Major | Minor | Upgraded (Major) | - | None | Sufficient | Partial | 5 | Strict | Yes | The savings/checking/credit-card combination is uniquely derivable, but the savings account name the gold uses ("Green Account") is not the name the documents use for that product ("Green Account (savings)"). |
| task_067 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 5 | Strict | Yes | Clean: Purple checking + Platinum Plus savings + Platinum Rewards Card is the unique best combination for $100,000, by gross APY and after the card fee. |
| task_068 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 5 | Strict | Yes | The gold opens the Green checking account as "Green Account", but the checking-opening procedure gives "Green Account (checking)" as the example class name, so an agent following the procedure literally fails. |
| task_069 | Blocker | Blocker | Confirmed (Blocker) | - | None | Sufficient | No | 5 | Strict | No | The gold's Silver Plus savings (3.5% total) is beaten by Gold savings (5.7%) and even Silver savings (4.1%), both of which the documents say offer ATM fee rebates, so a correct agent fails. |
| task_070 | Minor | Minor | Confirmed (Minor) | - | None | Partial | Yes | 3 | None | Yes | Sky Blue is the correct pick under the active November promotion, but the script never confirms the business meets Sky Blue's 4-year startup age limit. |
| task_071 | Major | Major | Confirmed (Major) | - | None | Partial | Partial | 4 | None | Yes | The account choices are right, but the business-savings procedure tells the agent to open the account with account_type 'savings' while the gold uses 'business_savings', and the two produce different accounts. |
| task_072 | Major | Major | Confirmed (Major) | - | Minor | Sufficient | Partial | 5 | None | No | Both gold refund amounts include fee errors dated after the benchmark's fixed "today" (11/14/2025), so an agent that only reviews fees posted so far credits $13.50 and $3.00 instead of $14.00 and $3.50. |
| task_073 | Major | Major | Confirmed (Major) | - | Major | Sufficient | Partial | 5 | None | No | The Green account's gold refund ($9.00) includes a duplicate fee dated 11/15, after the benchmark's fixed "today", so an agent that only reviews fees posted so far credits $6.00. |
| task_074 | Major | Major | Confirmed (Major) | - | Blocker | Sufficient | Partial | 5 | None | No | The corrected Light Blue refund ($14.50) and the Dark Green and Evergreen refunds are right, but the Purple refund ($27.00) still counts a fee dated after "today" and a rebate the Purple docs limit to ATM-operator fees. |
| task_075 | Major | Major | Adjusted (Major) | - | Blocker | Sufficient | Partial | 4 | None | Yes | Green Fee-Free is cheapest only if Purple's $2.50 out-of-network fee applies abroad and is not covered by Purple's $30 monthly ATM rebate; the benchmark's own fee-refund tasks assume the opposite on both points. |
| task_076 | Major | Major | Confirmed (Major) | - | None | Partial | Partial | 4 | None | Yes | Bluest has lower ATM fees than the gold's Purple Account under every reading of the fee docs; the gold excludes Bluest for its $75,000 opening deposit, but the script never says whether the customer can make it. |
| task_077 | Minor | Minor | Confirmed (Minor) | - | None | Partial | Partial | 4 | Strict | Yes | The lost-wallet flow is derivable, but the gold records RUSH shipping and the PREMIUM card design, which the customer specifies only if asked and only as "the best option that's free". |
| task_078 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 4 | Strict | Yes | Lost-wallet task with three debit cards is clean: every gold write follows from the customer script, the tier table, and the card-closure rules. |
| task_079 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Partial | 5 | Strict | Yes | The gold is right, but the card-closing rules say both 'no pending transactions' and 'pending refunds can be waived', and the Green account's only pending row is a refund. |
| task_080 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 5 | Strict | Yes | Five-card stolen-wallet task has a reachable gold, but the customer script and author notes are built around a provisional-credit cap that the documents and gold do not apply. |
| task_081 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Yes | 5 | Strict | Yes | Same as task_080 plus four requests for a human, but the DB check cannot see whether the agent transferred on the fourth request, and the same provisional-credit script mismatch is present. |
| task_082 | Blocker | Blocker | Confirmed (Blocker) | - | Blocker | Partial | No | 5 | Strict | No | Fraud on the Green Fee-Free card calls for closing it, and the customer asks for a reissue, but the gold never closes that card, so an agent that follows the rules is marked wrong. |
| task_083 | Blocker | Blocker | Confirmed (Blocker) | - | Blocker | Sufficient | Partial | 4 | Soft | No | Every gold dispute call leaves out a field the tool requires, and the task is graded by exact string match on those calls, so no correct agent can get credit. |
| task_084 | Blocker | Blocker | Confirmed (Blocker) | - | Blocker | Sufficient | No | 4 | Strict | No | The gold's liability amounts follow no consistent rule: it caps one dispute at the charge amount but not another, so any agent applying one rule throughout gets a value wrong. |
| task_085 | Major | Major | Confirmed (Major) | - | Minor | Sufficient | Partial | 4 | Soft | Yes | The verify-the-customer's-claims test works, but which duplicate gym charge to dispute, the liability amounts, and one provisional-credit flag each depend on a reading the documents do not settle. |
| task_086 | Major | Major | Confirmed (Major) | - | Minor | Partial | Partial | 5 | Soft | Yes | The large six-dispute scenario is mostly derivable, but liability amounts, the PIN status after a reported skimming, and the purchase type of the late fraud charge each have more than one defensible answer. |
| task_087 | Major | Major | Confirmed (Major) | - | None | Sufficient | Partial | 4 | Soft | Yes | Fixing three declined cards is well specified, but one security document says to hand the customer to the security team when they report a charge they did not make, which would skip the gold's dispute and replacement. |
| task_088 | Major | Major | Confirmed (Major) | - | Minor | Partial | Partial | 4 | Soft | Yes | Three decline problems with a reachable gold, but the documents invite an account-to-account transfer the gold does not expect and disagree on freezing versus closing the cloned card, and the purchase type of the fraud charge is never stated. |
| task_089 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 4 | Soft | Yes | ATM-limit task is clean: the one write (a $900 temporary limit on the Green card) is the only value that both covers the customer's need and stays within the 150% cap. |
| task_090 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Partial | 5 | Strict | Yes | The three-card PIN-lock case resolves to the gold, but the Blue card's fraud score sits on several undefined boundaries and the Evergreen replacement's card design is never stated by the customer. |
| task_091 | Blocker | Blocker | Upgraded (Blocker) | - | None | Partial | No | 5 | Strict | No | For the Evergreen and Light Blue replacements the gold ignores the tier rules: it orders standard shipping and design when the customer asked for the most premium free option, and it orders a Light Blue replacement immediately despite the 48-hour wait. Several other choices are also left open. |
| task_092 | Minor | Minor | Not sampled (-) | - | Minor | Sufficient | Partial | 5 | Strict | Yes | The four-card PIN-lock case reaches the gold through the customer's answers, but the 'escalate to supervisor' rule, the missing unlock tool, and an unscripted shipping choice leave room for drift. |
| task_093 | Major | Minor | Upgraded (Major) | - | None | Sufficient | Partial | 3 | Soft | Yes | The Silver interest correction ($33.00) is derivable, but the documented daily compounding does not match the system's simple monthly interest, and the discrepancy report's content is never graded. |
| task_094 | Major | Major | Confirmed (Major) | - | Minor | Sufficient | Partial | 4 | Soft | Yes | Whether the Gold Rewards Card's +0.025% stacks on top of the EcoCard bonus is ambiguous in the docs, so the $140.00 correction is one of two defensible answers. |
| task_095 | Major | Major | Confirmed (Major) | - | Major | Sufficient | Partial | 4 | Soft | Yes | As in task_094, the docs disagree on whether the Gold Rewards Card's +0.025% stacks, so the $98.00 correction is one of two defensible answers. |
| task_096 | Minor | Minor | Confirmed (Minor) | - | None | Sufficient | Partial | 5 | Soft | Yes | Both savings corrections ($17.50 Bronze, $15.00 Gold Plus) are derivable, but one needed boost document is missing from the task's list, and the interest-formula and report-grading gaps apply here too. |
| task_097 | Major | Major | Confirmed (Major) | - | Major | Sufficient | Partial | 5 | Soft | No | The Silver account's gold correction leaves out the documented +0.025% multi-product relationship bonus that the near-identical task_093 includes, so a doc-following agent credits $222.92 instead of $220.84. |
| task_098 | None | None | Not sampled (-) | - | None | Sufficient | Yes | 3 | None | Yes | Clean: the Blue Account referral ($35 + $30 = $65) is the unique best combined bonus for a $600 deposit, and the referral window allows it. |
| task_099 | None | None | Confirmed (None) | - | None | Sufficient | Yes | 4 | None | Yes | Clean: World Blue ($300 to the referrer) is the unique highest referrer bonus that a $30,000 business deposit qualifies for. |
| task_100 | None | None | Confirmed (None) | - | Minor | Sufficient | Yes | 3 | None | Yes | Clean: from the on-file open date (65 days of tenure) Hunter Green ($175) is the best referral the customer qualifies for, and World Blue's 90-day tenure rule correctly blocks the account she owns. |
| task_101 | Major | Minor | Upgraded (Major) | - | Blocker | Sufficient | Partial | 5 | Soft | Yes | The gold (Vikram to Purple, TechFlow to Sky Blue) follows the docs' 2-per-9-days referral limit, though the limit's wording mixes 'bonuses received' with 'referrals made'. |
| task_102 | Major | Major | Upgraded (Major) | - | Major | Partial | Partial | 5 | Soft | Yes | With one referral slot open, the customer asks to 'maximize the bonus'. Ember to Lime Green pays her more ($200), while the gold's TechFlow to Sky Blue pays more only in combined terms ($400). |

## Findings (Blocker and Major)

### task_014 — Major

**The gold transfers the customer to a human, but the KB's own referral-link procedure says that when a card has no documented referral program the agent must explain and 'not transfer to a human', so careful agents fail.**

- **document_contradiction (Major)** — The internal referral-link doc forbids a transfer in exactly this case (a referral link requested for a card with no documented program). The transfer-reason doc has a code that describes this case, and the gold uses that code.
  - doc_credit_cards_credit_cards_(general)_009 (title 'Generating a Credit Card Referral Link (Internal)'): "If no referral program is documented for the requested card, or if the user’s claimed terms are incorrect, ... explain why and do not provide a referral link tool. Do not transfer to a human in these cases."
  - `prompts/components/policy_header.md guideline 5: "This guidance may be overridden by specific scenario-based transfer guidance in the knowledge base."`
  - doc_bank_accounts_bank_accounts_(general)_042 (TIER 2): "unconfirmed_external_communication | Customer claims a specific promotion/program/offer exists (they have a letter, email, or flyer) but you cannot verify or find it in the KB after searching"
  - No doc_credit_cards_crypto-cash_back_* document mentions a referral program (the ones that exist are silver_011, platinum_008, ecocard_011, and business_gold_010 / silver_zoom_011)
  - `gold[0] = transfer_to_human_agents(reason="unconfirmed_external_communication"), reward_basis=["ACTION"]; required_documents omits credit_cards_(general)_009`
  - `Sibling task_015 (same customer, same Crypto-Cash Back opening line) follows doc 009: its gold never transfers`
  - *Why it matters:* The customer opens by asking 'How can I get a referral link', so doc 009 is the most directly relevant document. An agent that follows it, and the policy header's rule that scenario-specific KB transfer guidance overrides the general one, explains and declines without transferring, which fails ACTION grading. In all four earlier Opus 4.7 trials the agent cited doc 009 ('this isn't something I can transfer to a human agent for') and none matched the gold. The gold is reachable only by letting doc 042's reason-code table override doc 009's explicit prohibition.
  - *Fix:* Either change the gold to no transfer (assert via NL that the agent explains no Crypto-Cash Back referral program is documented), or narrow doc 009's 'Do not transfer' sentence so it excludes customers who hold an official-looking communication, and add credit_cards_(general)_009 to required_documents.
- **document_contradiction (Minor)** — Even when the agent does transfer, the Tier-1 code 'customer_demands_after_unavailable_offer_refusal' competes with the gold's Tier-2 code. The 'highest tier' rule picks Tier 1 whenever the customer has 'persisted multiple times' and asks for a human, which this script tells her to do ('Ask them to double-check or look harder').
  - `doc_bank_accounts_bank_accounts_(general)_042: "always select from the highest tier that applies"`
  - doc_bank_accounts_bank_accounts_(general)_042 (TIER 1): "customer_demands_after_unavailable_offer_refusal | ... customer persisted multiple times, and now demands human"
  - task_014 user_scenario: "Be politely persistent ... Ask them to double-check or look harder" / "If the agent ... offers to transfer you to a human agent: Accept the transfer"
  - `Sibling task_008 gold uses the Tier-1 code for a near-identical flyer/offer scenario`
  - *Why it matters:* Which code is correct depends on whether the agent offers the transfer or the customer asks for it, and whether her pushback counts as 'persisted multiple times'. The distinction is thin and the sibling task_008 resolves it the other way.
  - *Fix:* Accept either reason in compare_args for this task, or reword the Tier-1 row to require an explicit demand after multiple refusals.

*Verifier: Confirmed (Major → Major).* Doc 009 forbids a transfer in exactly this case, while doc 042's Tier-2 row describes the case and the gold follows it. Two document-supported readings lead to different ACTION outcomes, so Major per calibration (not Blocker, because doc 042 supports the gold). The secondary Tier-1/Tier-2 overlap is a fair Minor: the customer is scripted to accept an offered transfer rather than demand one.

### task_015 — Major

**The gold expects the agent to give the referral-link tool to a customer it cannot verify (she knows only her phone number), but no document says verification is unnecessary, so cautious agents refuse and fail.**

- **document_gap (Major)** — The KB never says whether identity verification is required before handing over get_referral_link. Doc 009's pre-check ('reason to believe the referral will be automatically rejected' plus the weekly cap) can only be evaluated by reading the customer's referral history, which the policy says requires verification. This customer can match only 1 of 4 identity fields, so the gold silently assumes no verification and no history check.
  - task_015 user_scenario: "Your user ID is 890389b165 and your phone number is 313-555-0246." (no email, DOB or address given; db.json users[890389b165] email='coffeelover_fati@protonmail.com', date_of_birth='12/05/1993')
  - policy (additional_instructions.md): "verify their identify ... ensure that they are able to give correctly any 2 out of the following values" and the example "Looking up account balances, transaction history, referral history..."
  - policy (additional_instructions.md): "You should ONLY verify a user's identity if you need to access or modify their customer information in internal databases on their behalf."
  - doc_credit_cards_credit_cards_(general)_009: "if there is reason to believe the referral will be automatically rejected, explain why and do not provide a referral link tool" / "Weekly limit: Customers can receive at most 2 referral bonuses in any rolling 7-day window"
  - `doc_credit_cards_credit_cards_(general)_020: "generate a unique referral link that's tied to your account"`
  - gold = [give_discoverable_user_tool(get_referral_link), user call_discoverable_user_tool(get_referral_link, {"user_id": "890389b165", "card_name": "Platinum Rewards Card"})], with no log_verification
  - *Why it matters:* A tool that creates a referral record tied to the customer's account, together with a pre-check that needs her referral history, leads reasonable agents to verify first. They cannot verify, so they never give the tool, and the referrals and user_discoverable_* tables then differ from the gold (I confirmed that giving the tool without the customer calling it also fails). In all four earlier Opus 4.7 trials the agent identified Platinum as the valid program and then withheld the tool for lack of verification.
  - *Fix:* Add a line to doc 009 such as 'No identity verification is required to provide this tool; the customer supplies their own user_id', or give the customer a second verification field so verifying (and logging) is possible and include log_verification in the gold.

*Verifier: Confirmed (Major → Major).* Reproduced the referral walk-through (only Platinum's terms match; Business Gold closed 2025-09-15, Silver Zoom closed 2025-10-01, EcoCard terms wrong) and the replays. The policy's 'ONLY verify if you need to access or modify' sentence supports the gold's no-verification path, so this sits at the low edge of Major, but the doc-009 weekly-cap pre-check needs referral history that this customer cannot be verified for, so a careful agent has a second defensible reading. Keep Major.

### task_017 — Major

**The Hilton transaction was credited one point more than the documented rate allows, but the gold leaves it undisputed. An agent that follows the rewards rules and flags it fails.**

- **argument_error (Major)** — Seed row txn_31fd03682992 (Hilton Seattle, $289.50, Travel, Silver 4%) stores 1159 points. The documented rate gives exactly 1158.00, so no rounding convention produces 1159. The gold disputes only the two gross errors and treats this 1-point overcredit as correct.
  - db.json credit_card_transaction_history[txn_31fd03682992]: transaction_amount "$289.50", category "Travel", rewards_earned "1159 points"; 289.50 x 4.0 = 1158.00 exactly
  - `doc_credit_cards_silver_rewards_card_002: "Pay with your card for eligible travel and software transactions to earn 4.0% back"`
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - doc_credit_cards_credit_cards_(general)_003: "Use this process when a customer believes there is a discrepancy between the cash back they received for a particular transaction and the cash back they should have received."
  - `gold[2] txn_cfabb609133d (Sushi Kashiba $87.25 Dining 1% -> 87, stored 47); gold[3] txn_913d14a20dc5 (Amazon $156.78 Shopping 1% -> floor 156, stored 15)`
  - `Replay: gold plus a dispute on txn_31fd03682992 -> verified match False (tables cash_back_disputes and user_discoverable_tool_calls differ)`
  - *Why it matters:* A careful agent that recomputes every row by the documented rules finds three discrepancies, not two. Kenji is told to follow the agent's lead, so if the agent reports the 1-point overcredit, he files a third dispute. That adds a cash_back_disputes row and a user_discoverable_tool_calls row the gold lacks, and the task fails. The gold is reached only if the agent decides on its own that a 1-point difference is not worth disputing, a threshold no document states. The verified scorer compares both tables exactly, so this result is the same as under upstream grading.
  - *Fix:* Set txn_31fd03682992.rewards_earned to "1158 points", or add txn_31fd03682992 to the gold dispute set.
- **document_gap (Minor)** — The rounding rule that decides which rows count as errors lives in doc_credit_cards_credit_cards_(general)_007, which is not listed in required_documents. The agent can still find it with KB search or grep in the default alltools configuration.
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - task_017.required_documents = ["doc_credit_cards_credit_cards_(general)_003", "doc_credit_cards_credit_cards_(general)_006", "doc_credit_cards_silver_rewards_card_001", "doc_credit_cards_silver_rewards_card_002"] (no _007)
  - *Why it matters:* Under a retrieval configuration that only shows required_documents (golden_retrieval / required_docs prompt), the agent never sees the floor rule. An agent that rounds half-up instead flags many correctly floored rows as 1-point errors and over-disputes.
  - *Fix:* Add doc_credit_cards_credit_cards_(general)_007 to required_documents.

*Verifier: Confirmed (Major → Major).* The 1159 cannot come from any rounding rule, and nothing in the KB says to skip a 1-point overcredit, so gold relies on an unstated materiality judgment (defensible here since the overcredit favours the customer and gold disputes only undercredits). Major. The required_documents omission is Minor per calibration.

### task_020 — Major

**This customer's stored rewards were rounded the opposite way from the documented round-down rule, so an agent that follows the rule sees nine extra 1-point errors the gold does not dispute.**

- **document_contradiction (Major)** — Amara's seed rewards are rounded half-up, which contradicts the documented always-floor rule. Following doc _007, nine correctly categorized transactions are over-credited by 1 point each. The gold disputes none of them, so it only matches an agent that rounds half-up or ignores 1-point differences on its own initiative.
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - `txn_a8f1c2d3e402 Adobe Creative Cloud $54.99, Business Silver Software 10% x2 promo (opened 02/13/2025) = 1099.80 -> floor 1099, stored 1100`
  - `txn_a8f1c2d3e404 Microsoft 365 $79.99, Business Silver excluded 1% x2 = 159.98 -> 159, stored 160`
  - `txn_a8f1c2d3e406 Whole Foods $127.43, 1% x2 = 254.86 -> 254, stored 255`
  - `txn_a8f1c2d3e409 Amazon $156.78, 1% x2 = 313.56 -> 313, stored 314`
  - `txn_a8f1c2d3e414 Coursera $49.99, excluded 1% = 49.99 -> 49, stored 50`
  - `txn_b7e2d4c5f503 Slack $44.99, Silver 4% = 179.96 -> 179, stored 180`
  - `txn_b7e2d4c5f507 Netflix $22.99, 1% -> 22, stored 23`
  - `txn_b7e2d4c5f509 Costco $143.56, 1% -> 143, stored 144`
  - `txn_b7e2d4c5f512 Nordstrom $187.50, 1% -> 187, stored 188`
  - `Replay (task_020 data): gold plus disputes on these 9 rows -> verified match False (cash_back_disputes and user_discoverable_tool_calls differ)`
  - *Why it matters:* A doc-faithful agent that recomputes every row finds 13 discrepancies: 4 gross and 9 one-point overcredits. The customer is told to follow the agent's lead, so if the agent presents all 13 she disputes all 13 and the task fails. Customers in sibling tasks 018/022 are told to dispute overpaid rows, so flagging overcredits is the benchmark's own convention. The gold is reached only by rounding half-up (against _007) or by an unstated materiality threshold. The verified scorer compares both affected tables exactly.
  - *Fix:* Re-seed Amara's (755bcb4d5d) non-error rows with floored values (e.g. a8f1c2d3e402 -> 1099, b7e2d4c5f503 -> 179, ...), so the documented rule reproduces the gold set; or change _007 to round half-up and re-seed the floor-convention tasks 017-019/021/022.
- **document_gap (Minor)** — The rounding rule that decides which rows count as errors lives in doc_credit_cards_credit_cards_(general)_007, which is not listed in required_documents. The agent can still find it with KB search or grep in the default alltools configuration.
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - task_020.required_documents = ["doc_credit_cards_credit_cards_(general)_003", "doc_credit_cards_credit_cards_(general)_006", "doc_business_credit_cards_business_silver_rewards_card_001", "doc_business_credit_cards_business_silver_rewards_card_002", "doc_business_credit_cards_business_silver_rewards_card_005", "doc_business_credit_cards_business_silver_rewards_card_012", "doc_credit_cards_silver_rewards_card_001", "doc_credit_cards_silver_rewards_card_002"] (no _007)
  - *Why it matters:* Under a retrieval configuration that only shows required_documents (golden_retrieval / required_docs prompt), the agent never sees the rounding rule, so whether a row counts as a 1-point error depends on whichever convention the agent assumes.
  - *Fix:* Add doc_credit_cards_credit_cards_(general)_007 to required_documents.

*Verifier: Confirmed (Major → Major).* Confirmed: this user's seed is rounded half-up, contradicting the documented floor rule, and the gold set matches only half-up. Two readings (follow general_007 and flag 9 extra rows, or ignore 1-point overcredits) give different graded states, so Major per calibration.

### task_024 — Major

**The gold picks the Business Bronze card ($900 back), but the Silver Zoom card's triple-cash-back promo pays at least $1,200 on the truck, if a landscaping company can hold that logistics-oriented card.**

- **non_determinism (Major)** — Comparing every business card on a $40,000 truck: Business Bronze 1% ($400) plus the $500 new-customer credit = $900 (gold). Silver Zoom's triple promo, claimable until 2025-12-31, pays 3 x 1.0% = 3% on non-transport purchases = $1,200 ($1,125.50 net of the fee), or 9% = $3,600 if a work truck counts as transportation. The gold is right only if Silver Zoom is off-limits to a non-logistics business, and the documents describe its target customer without stating that restriction.
  - doc_business_credit_cards_business_bronze_rewards_card_010: "This offer is available from 2025-10-01 through 2026-03-31" / "Make net new purchases totaling $10,000 within the first 2 months ... a $500 statement credit"
  - doc_business_credit_cards_silver_zoom_card_012: "You must claim the promotion within the window starting 2024-01-01 and ending 2025-12-31" / "The triple cash back earning period lasts 9 months from account opening once properly claimed" / "All other eligible purchases earn 3 × 1.0% during the promo period"
  - doc_business_credit_cards_silver_zoom_card_001: "Who this card is built for - Established transportation and logistics operators" ; doc_..._silver_zoom_card_008: "must be at or above 57 on the PAYDEX scale for logistics business approval"; annual fee $74.50
  - Other cards: Business Platinum 1.5% = $600 (first-year fee waived, doc _011); Business Silver 1% = $400 ($800 with the 2x promo if opened by 2025-11-14); Business Gold 1% (truck is not operations spend) = $400 minus $200 fee; Green Rewards 1% = $400 minus $100 fee
  - `task_024 instructions: "looking to expand your fleet"; required_documents list only Business Bronze and Business Silver docs`
  - gold[0] apply_for_credit_card card_type = "Business Bronze Rewards Card"; replay with "Silver Zoom Card" -> verified match False (credit_card_applications differs)
  - *Why it matters:* The customer applies for whatever single card the agent recommends. An agent that surveys all business cards finds Silver Zoom's promo, which beats Bronze under every category reading. Unless it concludes the card is closed to a landscaping business, it recommends Silver Zoom and the credit_card_applications row differs from gold. The documents say who the card is 'built for' but never say other businesses are ineligible.
  - *Fix:* State in the Silver Zoom docs that applicants must be transportation/logistics businesses, or end the triple-cash-back claim window before 2025-11-14, or make the purchase too small for Silver Zoom to win.

*Verifier: Confirmed (Major → Major).* Recomputed every business card: Bronze wins only if Silver Zoom is treated as closed to a landscaping business. The docs describe the target customer and a logistics PAYDEX criterion but never state that other businesses are ineligible, so two document-supported readings give different applications. Major.

### task_025 — Major

**Which card pays most on a $100,000 Apple Music purchase depends on whether Apple Music is an excluded 'Apple' merchant on one card and qualifying 'software/media' spend on another. Neither point is spelled out, and different readings pick different winners.**

- **non_determinism (Major)** — Gold = Business Platinum at 4% ($4,000). That requires two judgments at once: Apple Music is caught by Business Silver's 'Apple' exclusion (otherwise Silver pays 10% = $10,000, or $20,000 with its 2x promo), and Apple Music counts as software or media on Platinum (otherwise Platinum pays 1.5% = $1,500). In the second case Silver Zoom's triple promo (3% = $3,000) or Business Gold's operations rate (2.5% = $2,500) would beat Platinum.
  - `doc_business_credit_cards_business_silver_rewards_card_005: "Hardware/Electronics Merchants (Software Exclusion): - Apple - Microsoft - Dell"`
  - doc_business_credit_cards_business_platinum_rewards_card_002: "Travel, software, and media advertising purchases earn 4.0%"; _003 lists only advertising/media-placement purchases
  - doc_credit_cards_credit_cards_(general)_005: "Media (advertising spend, streaming services)" vs doc_credit_cards_credit_cards_(general)_019: "Entertainment: Movies, concerts, sporting events, and streaming services"
  - doc_business_credit_cards_silver_zoom_card_012: "You must claim the promotion within the window starting 2024-01-01 and ending 2025-12-31" / "The triple cash back earning period lasts 9 months from account opening once properly claimed" / "All other eligible purchases earn 3 × 1.0% during the promo period"
  - `doc_business_credit_cards_business_gold_rewards_card_003: "Cloud services and software subscriptions used for day-to-day operations" earn 2.5%`
  - `gold[0] apply_for_credit_card card_type = "Business Platinum Rewards Card"`
  - *Why it matters:* The customer applies for the single card the agent recommends, so the credit_card_applications row records the agent's reading. One reasonable reading gives Business Silver ($10,000+), another gives Silver Zoom or Business Gold, and only the specific pair of readings the gold assumes gives Business Platinum.
  - *Fix:* Name 'Apple Music' (or 'all Apple services') in the Business Silver exclusion list, and state in the Business Platinum docs that enterprise streaming/media subscriptions earn 4%. Alternatively, use a purchase that clearly falls in Platinum's software category.

*Verifier: Confirmed (Major → Major).* Reproduced the ranking under the gold's reading and the alternatives: if Apple Music is not software/media on Platinum, Silver Zoom (or a $1,500 Bronze/Platinum tie if Zoom is excluded) wins. The two category docs disagree about where streaming sits. Major.

### task_026 — Blocker

**The agent is asked to correct rewards after disputes are resolved, but no tool lets it see a dispute's status. The gold's corrected Zoom value (1500) also breaks the documented round-down rule, which gives 1499.**

- **argument_error (Blocker)** — gold[10] writes new_rewards_earned "1500 points" for txn_a8f1c2d3e411 (Zoom $149.99, Business Silver 10%, after the promo ended), i.e. 1499.9 rounded half-up. Doc _007 says rewards are always floored, giving 1499. Doc _004 tells the agent to recalculate and write 'the correct whole-number point value'.
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - `doc_credit_cards_credit_cards_(general)_004: "new_rewards_earned: a string formatted as 'X points' where X is the correct whole-number point value"`
  - `gold[10].arguments = {"transaction_id": "txn_a8f1c2d3e411", "new_rewards_earned": "1500 points"}; 149.99 x 10% = 1499.9`
  - `Replay: gold with "1499 points" -> verified match False (credit_card_transaction_history differs)`
  - *Why it matters:* An agent that follows the only documented rounding rule writes 1499 and fails. The gold's 1500 matches only an agent that never finds doc _007 or overrides it. The verified scorer compares credit_card_transaction_history exactly, so this fails under both scorers.
  - *Fix:* Change gold[10] to "1499 points" (and re-seed this user's rows to floor), or change doc _007 to round half-up.
- **document_gap (Blocker)** — Doc _004 requires the agent to look up resolved disputes in cash_back_disputes before updating rewards, but no agent tool reads that table, and the dispute tool's status message goes only to the customer. The agent cannot tell this task (disputes RESOLVED, gold updates) from task_027 (disputes SUBMITTED, gold refuses), because both customers make the identical claim.
  - doc_credit_cards_credit_cards_(general)_004: "Look up the user's resolved disputes in the cash_back_disputes database to find the transaction_id values that need rewards adjustments."
  - tools.py: the only code touching cash_back_disputes is KnowledgeUserTools.submit_cash_back_dispute_0589 (add_to_db). get_user_dispute_history_7291 reads transaction_disputes, KnowledgeUserTools.query_database has no @is_tool, and the alltools shell only sees the KB directory
  - submit_cash_back_dispute_0589 returns 'Status: RESOLVED ...' (task_026, auto_resolve_disputes=True) or 'Status: SUBMITTED ...' (task_027, False) to the user only; orchestrator routes requestor='user' ToolMessages to Role.USER
  - task_026 and task_027 differ only in initial_state.task_config.dispute_settings.auto_resolve_disputes; both customers say "I just got a notification that they've all been approved and resolved!"
  - `Replay: task_026 gold without the update calls -> verified match False (missing update_transaction_rewards_3847; credit_card_transaction_history differs)`
  - *Why it matters:* The documented precondition cannot be checked, so the agent must choose blindly between trusting the customer and refusing. Trusting passes this task and fails task_027; refusing does the reverse. A doc-faithful agent that will not update without the documented lookup fails here.
  - *Fix:* Add an agent read tool for cash_back_disputes (e.g. get_cash_back_disputes_by_user), document it in doc _004, and add that read to gold so both 026 and 027 test actual verification.
- **document_contradiction (Major)** — Amara's seed rewards are rounded half-up, which contradicts the documented always-floor rule. Following doc _007, nine correctly categorized transactions are over-credited by 1 point each. The gold disputes none of them, so it only matches an agent that rounds half-up or ignores 1-point differences on its own initiative.
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - `txn_a8f1c2d3e402 Adobe Creative Cloud $54.99, Business Silver Software 10% x2 promo (opened 02/13/2025) = 1099.80 -> floor 1099, stored 1100`
  - `txn_a8f1c2d3e404 Microsoft 365 $79.99, Business Silver excluded 1% x2 = 159.98 -> 159, stored 160`
  - `txn_a8f1c2d3e406 Whole Foods $127.43, 1% x2 = 254.86 -> 254, stored 255`
  - `txn_a8f1c2d3e409 Amazon $156.78, 1% x2 = 313.56 -> 313, stored 314`
  - `txn_a8f1c2d3e414 Coursera $49.99, excluded 1% = 49.99 -> 49, stored 50`
  - `txn_b7e2d4c5f503 Slack $44.99, Silver 4% = 179.96 -> 179, stored 180`
  - `txn_b7e2d4c5f507 Netflix $22.99, 1% -> 22, stored 23`
  - `txn_b7e2d4c5f509 Costco $143.56, 1% -> 143, stored 144`
  - `txn_b7e2d4c5f512 Nordstrom $187.50, 1% -> 187, stored 188`
  - `Replay (task_020 data): gold plus disputes on these 9 rows -> verified match False (cash_back_disputes and user_discoverable_tool_calls differ)`
  - *Why it matters:* A doc-faithful agent that recomputes every row finds 13 discrepancies: 4 gross and 9 one-point overcredits. The customer is told to follow the agent's lead, so if the agent presents all 13 she disputes all 13 and the task fails. Customers in sibling tasks 018/022 are told to dispute overpaid rows, so flagging overcredits is the benchmark's own convention. The gold is reached only by rounding half-up (against _007) or by an unstated materiality threshold. The verified scorer compares both affected tables exactly. Here the extra disputes would also be auto-resolved, inviting extra update writes.
  - *Fix:* Re-seed Amara's (755bcb4d5d) non-error rows with floored values (e.g. a8f1c2d3e402 -> 1099, b7e2d4c5f503 -> 179, ...), so the documented rule reproduces the gold set; or change _007 to round half-up and re-seed the floor-convention tasks 017-019/021/022.
- **document_gap (Minor)** — The rounding rule that decides which rows count as errors lives in doc_credit_cards_credit_cards_(general)_007, which is not listed in required_documents. The agent can still find it with KB search or grep in the default alltools configuration.
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - task_026.required_documents = ["doc_credit_cards_credit_cards_(general)_003", "doc_credit_cards_credit_cards_(general)_004", "doc_business_credit_cards_business_silver_rewards_card_001", "doc_business_credit_cards_business_silver_rewards_card_002", "doc_business_credit_cards_business_silver_rewards_card_005", "doc_business_credit_cards_business_silver_rewards_card_012", "doc_credit_cards_silver_rewards_card_001", "doc_credit_cards_silver_rewards_card_002"] (no _007)
  - *Why it matters:* Under a retrieval configuration that only shows required_documents (golden_retrieval / required_docs prompt), the agent never sees the rounding rule, so whether a row counts as a 1-point error depends on whichever convention the agent assumes.
  - *Fix:* Add doc_credit_cards_credit_cards_(general)_007 to required_documents.

*Verifier: Confirmed (Blocker → Blocker).* Both Blockers reproduce. The gold write of 1500 follows no documented rule (general_007 floors, and the sibling task_028 gold floors), and the dispute status that gates the update is unreadable by any agent tool. The Major seed-rounding issue and the Minor required_documents omission also hold.

### task_027 — Blocker

**The task is meant to catch an agent that updates rewards on the customer's false claim that disputes were resolved, but the agent has no way to check dispute status, so passing depends on whether it trusts the customer at all.**

- **non_determinism (Major)** — The author notes say the agent 'must verify dispute status and refuse to update'. No agent tool can read cash_back_disputes, and the SUBMITTED status message reaches only the customer. The gold (no update) is reached by any agent that refuses to act on an unverifiable claim, but the identical conversation in task_026 requires the update.
  - doc_credit_cards_credit_cards_(general)_004: "Look up the user's resolved disputes in the cash_back_disputes database to find the transaction_id values that need rewards adjustments."
  - tools.py: the only code touching cash_back_disputes is KnowledgeUserTools.submit_cash_back_dispute_0589 (add_to_db). get_user_dispute_history_7291 reads transaction_disputes, KnowledgeUserTools.query_database has no @is_tool, and the alltools shell only sees the KB directory
  - submit_cash_back_dispute_0589 returns 'Status: RESOLVED ...' (task_026, auto_resolve_disputes=True) or 'Status: SUBMITTED ...' (task_027, False) to the user only; orchestrator routes requestor='user' ToolMessages to Role.USER
  - task_026 and task_027 differ only in initial_state.task_config.dispute_settings.auto_resolve_disputes; both customers say "I just got a notification that they've all been approved and resolved!"
  - Replay: task_027 gold plus the four task_026 update calls -> verified match False (extra update_transaction_rewards_3847; credit_card_transaction_history differs)
  - *Why it matters:* Two readings exist. In one, the customer reports the disputes approved and doc _004 says to update approved disputes. In the other, the doc _004 lookup cannot be done, so the agent should not update. They give opposite DB states, and no agent can satisfy both 026 and 027. The task does not test the verification it claims to test.
  - *Fix:* Add an agent tool that reads cash_back_disputes, document it in doc _004, and include that read in both 026 and 027 gold.
- **document_contradiction (Major)** — Amara's seed rewards are rounded half-up, which contradicts the documented always-floor rule. Following doc _007, nine correctly categorized transactions are over-credited by 1 point each. The gold disputes none of them, so it only matches an agent that rounds half-up or ignores 1-point differences on its own initiative.
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - `txn_a8f1c2d3e402 Adobe Creative Cloud $54.99, Business Silver Software 10% x2 promo (opened 02/13/2025) = 1099.80 -> floor 1099, stored 1100`
  - `txn_a8f1c2d3e404 Microsoft 365 $79.99, Business Silver excluded 1% x2 = 159.98 -> 159, stored 160`
  - `txn_a8f1c2d3e406 Whole Foods $127.43, 1% x2 = 254.86 -> 254, stored 255`
  - `txn_a8f1c2d3e409 Amazon $156.78, 1% x2 = 313.56 -> 313, stored 314`
  - `txn_a8f1c2d3e414 Coursera $49.99, excluded 1% = 49.99 -> 49, stored 50`
  - `txn_b7e2d4c5f503 Slack $44.99, Silver 4% = 179.96 -> 179, stored 180`
  - `txn_b7e2d4c5f507 Netflix $22.99, 1% -> 22, stored 23`
  - `txn_b7e2d4c5f509 Costco $143.56, 1% -> 143, stored 144`
  - `txn_b7e2d4c5f512 Nordstrom $187.50, 1% -> 187, stored 188`
  - `Replay (task_020 data): gold plus disputes on these 9 rows -> verified match False (cash_back_disputes and user_discoverable_tool_calls differ)`
  - *Why it matters:* A doc-faithful agent that recomputes every row finds 13 discrepancies: 4 gross and 9 one-point overcredits. The customer is told to follow the agent's lead, so if the agent presents all 13 she disputes all 13 and the task fails. Customers in sibling tasks 018/022 are told to dispute overpaid rows, so flagging overcredits is the benchmark's own convention. The gold is reached only by rounding half-up (against _007) or by an unstated materiality threshold. The verified scorer compares both affected tables exactly.
  - *Fix:* Re-seed Amara's (755bcb4d5d) non-error rows with floored values (e.g. a8f1c2d3e402 -> 1099, b7e2d4c5f503 -> 179, ...), so the documented rule reproduces the gold set; or change _007 to round half-up and re-seed the floor-convention tasks 017-019/021/022.
- **document_gap (Minor)** — The rounding rule that decides which rows count as errors lives in doc_credit_cards_credit_cards_(general)_007, which is not listed in required_documents. The agent can still find it with KB search or grep in the default alltools configuration.
  - doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number. When calculating points earned on a purchase, the system always truncates (floors) fractional points rather than rounding to the nearest integer."
  - task_027.required_documents = ["doc_credit_cards_credit_cards_(general)_003", "doc_credit_cards_credit_cards_(general)_004", "doc_business_credit_cards_business_silver_rewards_card_001", "doc_business_credit_cards_business_silver_rewards_card_002", "doc_business_credit_cards_business_silver_rewards_card_005", "doc_business_credit_cards_business_silver_rewards_card_012", "doc_credit_cards_silver_rewards_card_001", "doc_credit_cards_silver_rewards_card_002"] (no _007)
  - *Why it matters:* Under a retrieval configuration that only shows required_documents (golden_retrieval / required_docs prompt), the agent never sees the rounding rule, so whether a row counts as a 1-point error depends on whichever convention the agent assumes.
  - *Fix:* Add doc_credit_cards_credit_cards_(general)_007 to required_documents.

*Verifier: Upgraded (Major → Blocker).* The defect is identical to task_029, which the review rates Blocker, and the mirror of 026/028 (Blocker): the fact that decides update-or-refuse (dispute status) does not exist on the agent side, and identical observations demand opposite DB states across the twins. That is the calibration's Blocker case ('the information or tool needed to reach it does not exist', the same logic as an undocumented tie), so it should not be Major in one twin and Blocker in the others. A refusing agent passes 027 only because of its trust disposition, not because it checked anything.

### task_028 — Blocker

**The agent must take the customer's word that her disputes were approved, because it has no way to check, while the twin task 029 fails any agent that does exactly that.**

- **non_determinism (Blocker)** — Gold actions 8-14 update rewards on the strength of the customer's claim that the disputes were resolved. Doc 004 tells the agent to confirm resolution in the cash_back_disputes table, but no agent tool reads that table. task_029 shows the agent the same conversation and expects it to refuse.
  - doc_credit_cards_credit_cards_(general)_004: "Look up the user’s resolved disputes in the cash_back_disputes database to find the transaction_id values that need rewards adjustments."
  - tools.py: the only reference to cash_back_disputes is the add_to_db write inside KnowledgeUserTools.submit_cash_back_dispute_0589; no agent tool (base or discoverable) reads that table. Agent tool list (no_knowledge variant): call_discoverable_agent_tool, change_user_email, get_credit_card_accounts_by_user, get_credit_card_transactions_by_user, get_current_time, get_referrals_by_user, get_user_information_by_*, give_discoverable_user_tool, list_discoverable_agent_tools, log_verification, transfer_to_human_agents, unlock_discoverable_agent_tool (+ KB search/shell over documents only)
  - `submit_cash_back_dispute_0589 result (status line) is returned to the user simulator only, never to the agent`
  - task_028 initial_state task_config.dispute_settings.auto_resolve_disputes = true -> replayed dispute status RESOLVED; task_029 auto_resolve_disputes = false -> status SUBMITTED
  - task_028 Phase 2 and task_029 Phase 2 scripts use the identical customer line: "Great, I've submitted all the disputes. I just got a notification that they've all been approved and resolved! Can you now update my transaction records with the correct cash back amounts?"
  - gold[8] unlock_discoverable_agent_tool update_transaction_rewards_3847; gold[9..14] call_discoverable_agent_tool update_transaction_rewards_3847 (95/1390/642/669/2049/750 points)
  - `task_029 description.notes: "Agent must verify dispute status and refuse to update transactions when disputes are still SUBMITTED (not RESOLVED)."`
  - Replay: gold[0..7] only (agent declines to update) -> verified match False: missing required discoverable calls ['update_transaction_rewards_3847'], table 'credit_card_transaction_history' differs
  - *Why it matters:* From the agent's side, task_028 and task_029 look the same. A careful agent that will not update without the doc-04 lookup fails 028. A trusting agent passes 028 and fails 029. The score depends on whether the agent is inclined to trust the customer, not on whether its work is correct.
  - *Fix:* Expose cash_back_disputes to the agent, for example a discoverable get_cash_back_dispute_status tool documented in doc 004 and added to both golds as a required read. Alternatively, have the user tool's status text reach the agent.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced the reward math, the gold values and the replay. The update is gated on unobservable dispute status and task_029 expects the opposite action on the same observations, so Blocker.

### task_029 — Blocker

**The agent is expected to catch a customer lying that her disputes were approved, but it has no tool to check, and the twin task 028 rewards believing the same words.**

- **non_determinism (Blocker)** — The gold has no update_transaction_rewards_3847 calls, because the disputes are hidden in status SUBMITTED. The agent cannot read cash_back_disputes. It sees the same 'they've all been approved and resolved' claim that task_028 expects it to act on.
  - doc_credit_cards_credit_cards_(general)_004: "Look up the user’s resolved disputes in the cash_back_disputes database to find the transaction_id values that need rewards adjustments."
  - tools.py: the only reference to cash_back_disputes is the add_to_db write inside KnowledgeUserTools.submit_cash_back_dispute_0589; no agent tool (base or discoverable) reads that table. Agent tool list (no_knowledge variant): call_discoverable_agent_tool, change_user_email, get_credit_card_accounts_by_user, get_credit_card_transactions_by_user, get_current_time, get_referrals_by_user, get_user_information_by_*, give_discoverable_user_tool, list_discoverable_agent_tools, log_verification, transfer_to_human_agents, unlock_discoverable_agent_tool (+ KB search/shell over documents only)
  - `submit_cash_back_dispute_0589 result (status line) is returned to the user simulator only, never to the agent`
  - task_028 initial_state task_config.dispute_settings.auto_resolve_disputes = true -> replayed dispute status RESOLVED; task_029 auto_resolve_disputes = false -> status SUBMITTED
  - task_028 Phase 2 and task_029 Phase 2 scripts use the identical customer line: "Great, I've submitted all the disputes. I just got a notification that they've all been approved and resolved! Can you now update my transaction records with the correct cash back amounts?"
  - `description.notes: "Agent must verify dispute status and refuse to update transactions when disputes are still SUBMITTED (not RESOLVED)."`
  - Replay: gold + unlock/call update_transaction_rewards_3847(txn_57ecc6da56c2, '95 points') -> verified match False: extra discoverable calls ['update_transaction_rewards_3847'], table 'credit_card_transaction_history' differs
  - *Why it matters:* The verification the notes require cannot be done. An agent passes only if it happens to distrust the customer, and the same disposition fails task_028. The result measures trust disposition, not correct behaviour.
  - *Fix:* Give the agent a documented read of cash_back_disputes, such as a discoverable status tool, and make that read a gold action in both 028 and 029.
- **document_gap (Minor)** — The task needs the floor rounding rule in doc_credit_cards_credit_cards_(general)_007, which is missing from required_documents here although task_028 lists it.
  - `task_029 required_documents omits "doc_credit_cards_credit_cards_(general)_007"; task_028 required_documents includes it`
  - `doc_credit_cards_credit_cards_(general)_007: "All credit card rewards points are rounded down to the nearest whole number."`
  - `Floor reproduces exactly the 6 gold dispute transactions; round-half-up flags 28`
  - *Why it matters:* The default 'alltools' retrieval can still reach the doc. A golden_retrieval run would not include it, and an agent rounding half-up would dispute 22 extra transactions.
  - *Fix:* Add doc_credit_cards_credit_cards_(general)_007 to required_documents.
- **underspecified_instructions (Minor)** — Unlike task_028, this script never says what the customer does if the agent suggests leaving the overpaid transaction (txn_e647e242ce96, 1875 points stored vs 750 correct) undisputed. The gold disputes it.
  - `task_028 script step 4: "If the agent shows an overpaid transaction but suggests not disputing it: Ask them to dispute it anyway..."; task_029 has no such step`
  - `gold[7] submit_cash_back_dispute_0589 transaction_id txn_e647e242ce96`
  - doc_credit_cards_credit_cards_(general)_003: "Use this process when a customer believes there is a discrepancy between the cash back they received for a particular transaction and the cash back they should have received."
  - *Why it matters:* If the agent frames the overpayment as a bonus, the simulated customer may skip that dispute and the user_discoverable_tool_calls and cash_back_disputes tables will differ. Doc 003's 'discrepancy' default (dispute it) matches the gold, so a doc-faithful agent passes.
  - *Fix:* Copy task_028's step 4 into the task_029 script.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced. The Blocker (unverifiable status, twin of 028) and both Minors hold.

### task_039 — Major

**Which disputes get provisional credit depends on whether disputes filed earlier in the same call count toward the 'no more than 2 in 12 months' rule, which the documents never settle, and on filing order.**

- **document_gap (Major)** — The customer has 0 disputes on file, and four of the eight disputes have a provisional-eligible reason. The gold gives credit to the first three filed and denies the fourth ($129.45 fraud). That only follows if disputes filed earlier in this conversation count as 'filed ... in the past 12 months'. Doc_015 does not say whether they do.
  - doc_credit_cards_credit_cards_(general)_015: "Eligibility Criteria — Customer is ELIGIBLE for provisional credit if ALL of the following are true: ... 4. Previous Disputes: The customer has not filed more than 2 disputes in the past 12 months"
  - `Replay: get_user_dispute_history_7291(01f21c9970) before filing -> "No transaction disputes found for this user."`
  - gold[6..8] eligible true for txn_f7ce44574766 ($312.87 dup), txn_a450807f1148 ($234.56 fraud), txn_182e896e1c97 ($215.67 dup); gold[9] eligible false for txn_2f16599b9075 ($129.45 fraud, contacted_merchant false, which fraud does not need)
  - Every other doc_015 criterion holds for all four: cc_01f21c9970_gold opened 06/15/2024; amounts are within $25 to $10,000 (Premium Tier); the two duplicates have contacted_merchant true
  - `tools.py file_credit_card_transaction_dispute_4829 stores eligible_for_provisional_credit verbatim and sets provisional_credit_given to the same value`
  - `Replay: gold with gold[9] eligible true (snapshot reading, 0 prior disputes) -> verified match False: table 'transaction_disputes' differs`
  - *Why it matters:* There are two readings of criterion 4. The cumulative one, under which in-session filings count (the gold's), is arguably the literal one. The snapshot one, which counts only history from the dispute-history tool, is equally natural. An agent that decides eligibility from the history it looked up marks all four true and fails.
  - *Fix:* State in doc_015 that disputes filed earlier in the same interaction count toward criterion 4, or set all four reason-eligible disputes to true.
- **hidden_ordering (Major)** — Under the gold's cumulative reading, the first three disputes filed in the session use up the allowance, including those with ineligible reasons. So the gold flags appear only if the agent files the three largest fraud/duplicate disputes before all the others. No document sets a filing order. The tie-breaker is the customer's 'biggest charges first' line, which the script releases only if the agent brings up provisional credit.
  - user script step 8: "If there's any limit on provisional credit, I want it applied to the biggest charges first... Do not mention this if the agent does NOT bring provisional credit up."
  - `Gold filing order: gold[6] 312.87, gold[7] 234.56, gold[8] 215.67, then gold[9] 129.45 and the four non-eligible-reason disputes`
  - Computation: filing in the customer's listed order (Costco 234.56, 312.87, 267.34, 198.23, then Amazon 129.45, 215.67, 162.54, 56.78) under the cumulative reading gives eligible = {234.56, 312.87} only; $215.67 becomes false, unlike gold[8]
  - *Why it matters:* An agent that applies the gold's own reading but files in the natural (listed or chronological) order produces different provisional flags and fails.
  - *Fix:* Have the customer state the priority unconditionally, or document that when a cap applies, credit goes to the largest eligible disputes.
- **underspecified_instructions (Minor)** — The script never scripts the replacement shipping speed or the resolution type for any dispute; the steps on these are missing from its numbering. The gold records expedited_shipping true, full_refund for seven disputes, and partial_refund $50 for the incorrect-amount dispute.
  - gold[15] order_replacement_credit_card_7291 "expedited_shipping": true; doc replacements_001: fraud -> "strongly recommend expedited shipping"; Gold Rewards is Premium tier, expedited "$0.00 (complimentary)"
  - `gold[11] resolution_requested "partial_refund", partial_refund_amount 50; script: "You were supposed to be charged $148.23 but they charged you $50 extra"`
  - `doc_credit_cards_credit_cards_(general)_014: "resolution_requested (string) - Ask user what resolution they want."`
  - *Why it matters:* The customer simulator must improvise these answers. The stated facts (free expedited shipping recommended for fraud; a known $50 overcharge; full refunds for fraud and duplicates) point to the gold values, so the risk is small.
  - *Fix:* Add explicit lines: 'accept expedited shipping', 'full refund for all except a $50 partial refund on the $198.23 charge'.

*Verifier: Confirmed (Major → Major).* Reproduced every load-bearing claim and computation. The gold follows the reading where in-session filings count, excluding the one being filed, and it also needs largest-first filing, which the customer reveals only if the agent raises provisional credit. That is two document-supported readings plus a conditional tie-breaker, which is Major under calibration, not Blocker. The unscripted resolution and expedited fields point to the gold values, so Minor is right for that issue.

### task_040 — Major

**With one dispute already on file, the gold gives provisional credit to only the first two new disputes filed, which depends on an unstated counting rule and on filing order; one refund type is also left to guesswork.**

- **document_gap (Major)** — One dispute is on file (dsp_ed3ab3dce038, submitted 09/20/2025). Four new disputes have a provisional-eligible reason. Gold credits only Grainger and Uline and denies American Airlines ($342.50 fraud) and Best Buy ($189.99 duplicate). That holds only if disputes filed in this conversation count toward criterion 4, which doc_015 leaves open.
  - doc_credit_cards_credit_cards_(general)_015: "Eligibility Criteria — Customer is ELIGIBLE for provisional credit if ALL of the following are true: ... 4. Previous Disputes: The customer has not filed more than 2 disputes in the past 12 months"
  - initial_state.agent_data.transaction_disputes.dsp_ed3ab3dce038: submitted_at "09/20/2025", status "APPROVED"; replayed get_user_dispute_history_7291 shows exactly this 1 record
  - gold[7] txn_25e23705f61f Grainger $523.45 true; gold[8] txn_fd4c3871654e Uline $412.34 true; gold[9] txn_a1b2c3d4e503 American Airlines $342.50 false; gold[10] txn_a1b2c3d4e510 Best Buy $189.99 false
  - Other criteria hold for all four: cc_01f21c9970_gold opened 06/15/2024 and cc_01f21c9970_bgold 09/01/2024 (both over 60 days); amounts within $25 to $10,000 (Premium Tier); duplicates contacted_merchant true
  - `tools.py file_credit_card_transaction_dispute_4829 stores eligible_for_provisional_credit verbatim and sets provisional_credit_given to the same value`
  - `Replay: gold with gold[9] eligible true -> verified match False: table 'transaction_disputes' differs`
  - *Why it matters:* Under the snapshot reading (1 prior dispute, which is not more than 2), all four qualify, and an agent following it fails. Only the cumulative reading (1 then 2, the third new filing is denied) reproduces the gold.
  - *Fix:* State in doc_015 that disputes filed earlier in the same interaction count toward criterion 4, or mark all four reason-eligible disputes true.
- **hidden_ordering (Major)** — Under the cumulative reading, the two remaining slots go to whichever disputes are filed first, of any reason. The gold needs Grainger and Uline filed first. The customer reveals this priority only 'If the agent mentions provisional credit or asks about it'.
  - user script step 6: "The Grainger and Uline charges are the biggest ones hurting my business cash flow right now... Please prioritize those if there's any limit."
  - Computation: filing in the customer's listed order (Gold card: AA, Best Buy, PECO, Spotify; then Business: Uline, Grainger, Best Buy, Comcast) under the cumulative reading gives eligible = {AA $342.50, Best Buy $189.99}, the opposite of gold[7..10]
  - *Why it matters:* An agent that applies the cap correctly but never raises provisional credit, or files in the customer's order, records the wrong two disputes as credited.
  - *Fix:* Have the customer state the priority up front, or document a deterministic rule such as largest-first for allocating a capped allowance.
- **underspecified_instructions (Major)** — The script never states a resolution type. For the Comcast refund_never_processed charge ($189.99), the customer was 'promised a partial refund', but the gold records full_refund. The partial amount is unknown, and doc_014 has no default.
  - `script: "Comcast $189.99 on 10/30/2025 - REFUND NOT PROCESSED. You downgraded your business internet plan and were promised a partial refund weeks ago."`
  - `gold[14] txn_3ef1a3e9bf56 resolution_requested "full_refund"`
  - doc_credit_cards_credit_cards_(general)_014: "resolution_requested (string) - Ask user what resolution they want." / "'partial_refund': Partial amount (must also provide partial_refund_amount)"
  - `Replay: gold with gold[14] partial_refund (amount 50) -> verified match False: table 'transaction_disputes' differs`
  - *Why it matters:* When asked, the customer simulator may well ask for a partial refund, which the script's facts support. The agent would then file partial_refund and fail. This is an unscripted refund-type choice with no document default.
  - *Fix:* Script the resolution for each dispute (e.g. 'full refund for all except a $24.56 partial refund on PECO'), or change the Comcast story to a full-refund case.

*Verifier: Confirmed (Major → Major).* Same counting rule as 039 with one prior dispute (gold credits 2 new); the computation in the review is right. The Comcast refund-type issue is a real unscripted choice with no document default, and the script facts lean toward partial, so Major is right under calibration. Overall Major.

### task_041 — Major

**Sixteen-dispute task: the official answer grants provisional credit to only two disputes, which follows one reasonable reading of the 'no more than 2 disputes in 12 months' rule but not another, and several refund choices (including an exact $69.99 partial refund) are never stated by the customer.**

- **non_determinism (Major)** — Criterion 4 of the provisional-credit guideline supports two graded outcomes. Counting only disputes on file before the session (1 prior dispute) makes all 10 reason-eligible disputes eligible. Counting each new filing as it is made caps new credits at 2 (or at 1 if the dispute being filed is itself counted). The gold uses the cap of 2 and resolves which two through the customer's 'prioritize Staples and Coinbase' line.
  - `doc_credit_cards_credit_cards_(general)_015: "4. Previous Disputes: The customer has not filed more than 2 disputes in the past 12 months"`
  - `initial_state transaction_disputes.dsp_dfab0685d198.submitted_at = "09/20/2025" (one prior dispute, within 12 months)`
  - gold[9] txn_645286a3dd13 (Staples) and gold[10] txn_1b4cc30a928e (Coinbase): eligible_for_provisional_credit = true; gold[11] txn_107c4fa829bd (Delta fraud, $487.50, account open 03/15/2024) and gold[12..18] (all other reason-eligible disputes): false
  - Reason-eligible set under criteria 1,2,3,5 (fraud, duplicate, GNR purchased >30 days before 11/14/2025): Delta, Apple, Amazon (10/05), Coinbase, Best Buy, Patagonia, REI, Whole Foods (10/02), Staples, Office Depot = 10 disputes
  - user_scenario step 6: "The Staples and Coinbase charges are the biggest ones ... Please prioritize those if there's any limit." (fires only if the agent mentions provisional credit)
  - Replay: marking all 10 reason-eligible disputes true -> verified=False, table 'transaction_disputes' differs; marking Delta+Apple (script order) true -> verified=False
  - *Why it matters:* An agent that reads criterion 4 as a gate on dispute history before the session marks 10 disputes eligible. An agent that applies the cap in filing order without asking the customer credits whichever two it files first (Delta and Apple in the script's order). Both runs follow the documents and both fail on transaction_disputes.
  - *Fix:* State in doc_015 that disputes filed earlier in the same interaction count toward the 12-month limit, and that the customer chooses which disputes receive credit when the limit binds. Alternatively, change the gold to mark all 10 reason-eligible disputes true.
- **underspecified_instructions (Major)** — The customer script never says which resolution to request. The gold records 'partial_refund' with partial_refund_amount 69.99 for XFINITY, derived from a usual bill of 'around $120'. It records 'full_refund' for AT&T even though the customer was 'promised a partial refund', and for Tesla, described as an overcharge.
  - `doc_credit_cards_credit_cards_(general)_014: "13. resolution_requested (string) - Ask user what resolution they want."`
  - `user_scenario: "XFINITY $189.99 on 10/28/2025 - INCORRECT AMOUNT. Your usual bill is around $120."`
  - `gold[19].arguments: resolution_requested = "partial_refund", partial_refund_amount = 69.99 (189.99 - 120.00)`
  - `user_scenario: "AT&T Business $312.50 ... were promised a partial refund weeks ago" vs gold[24] resolution_requested = "full_refund"`
  - `user_scenario: "Tesla Supercharger $67.45 ... You were overcharged at a Supercharger" vs gold[22] resolution_requested = "full_refund"`
  - `Replay: XFINITY partial_refund_amount 70 -> verified=False; XFINITY full_refund -> verified=False`
  - *Why it matters:* The simulated customer has to improvise these answers. 'About $70' produces 70.0 rather than 69.99, and an answer of 'the partial refund I was promised' for AT&T, which comes with no amount, leads away from full_refund. Every such divergence changes a transaction_disputes row.
  - *Fix:* Add the resolution and any partial amount for each dispute to the script, for example 'XFINITY: partial refund of exactly $69.99' and 'AT&T: full refund'.

*Verifier: Confirmed (Major → Major).* Gold indices, values and replay outcomes all check out. The provisional-credit cap matches 040 exactly (1 prior, 2 new credits), and the gold's pair is also the two largest reason-eligible charges. Both Major issues stand. The review files the counting issue as non_determinism where 039/040 use document_gap plus hidden_ordering; the severity is the same, but the label differs.

### task_046 — Major

**Closure correctly stops at a pending dispute, but the dispute record cannot be tied to the Business Silver card from tool data, and an agent that also pays the balance the customer asks about fails.**

- **argument_error (Minor)** — The seeded pending dispute meant to block the Business Silver closure carries card_last_4_digits 7823, which matches neither of the user's cards, and refers to a transaction that does not exist. Only the ID string 'txn_bsilver_dup_001' links it to the account.
  - `initial_state transaction_disputes.dsp_yuki_bsilver_001: card_last_4_digits = "7823", transaction_id = "txn_bsilver_dup_001", status = "UNDER_REVIEW"`
  - `get_card_last_4_digits hash: cc_224959b99e_bsilver -> 9568, cc_224959b99e_plat -> 7053`
  - `db.json credit_card_transaction_history['txn_bsilver_dup_001'] does not exist; all 60 of the user's transactions are 'Platinum Rewards Card'`
  - `doc_credit_cards_credit_card_account_logistics_003 Step 1: "The account must not have any active or pending transaction disputes."`
  - *Why it matters:* The policy is per account. An agent that checks which card the dispute is on, or gives the user get_card_last_4_digits to compare, can conclude the dispute is on another card and proceed (pay balance, log reason, offer retention). That fails, and so does giving the tool, which writes user_discoverable_tools.
  - *Fix:* Set card_last_4_digits to "9568" and add txn_bsilver_dup_001 to the Business Silver transaction history.
- **instruction_gold_mismatch (Minor)** — The script tells the customer to agree to a balance payoff whenever the balance is mentioned, but the gold contains no payment. An agent that reports all unmet requirements, including the $125 balance, and pays it on the customer's request fails.
  - `user_scenario step 3: "If you are told about an outstanding balance: ... Yes, please pay that off from my checking account."`
  - `db.json credit_card_accounts.cc_224959b99e_bsilver.current_balance = "$125.00"`
  - doc_credit_cards_credit_card_account_logistics_003 Step 1: "If any requirement is not met, explain what must be resolved and do not proceed with retention offers."
  - `Replay: gold + pay_credit_card_from_checking_9182 $125 -> verified=False (extra discoverable call; tables accounts, credit_card_accounts differ)`
  - *Why it matters:* A payoff the customer requested and doc logistics_009 permits changes accounts and credit_card_accounts. The gold quietly expects the agent to stop at the first failed check (disputes come first in Step 1) and not raise the balance.
  - *Fix:* Remove step 3 from this script, or say in the protocol that later requirements are not resolved while an earlier one blocks closure.

*Verifier: Upgraded (Minor → Major).* Both issues reproduce. I raise the payoff issue to Major. Step 1 tells the agent to 'explain what must be resolved', and a natural reading lists every unmet requirement, including the $125 balance the agent has already seen. The scripted customer then asks for a payoff, which logistics_009 permits and nothing forbids. The gold is reached only if the agent reports the first failed check alone, an undocumented convention that the review's own why_it_matters describes, and that is Major by definition. The mismatched last-4 on the seeded dispute stays Minor.

### task_048 — Major

**In the four-card closure task, the gold expects the customer to apply for the Silver Rewards Card, but other Rho-Bank cards (Platinum Rewards, Business Silver) also beat the competitor's 3.25% offer, so the card applied for depends on which one the agent recommends.**

- **non_determinism (Major)** — Retention Step 4 says to offer 'a card with similar or better benefits' with no tie-breaker. For a competitor paying 3.25% on travel and software, Silver Rewards (4% travel/software, $0 fee), Platinum Rewards (10% on everything, $200 fee, 0% foreign fee) and Business Silver (10% travel/software, first-year fee $0) all qualify. The gold records an application for Silver Rewards.
  - doc_credit_cards_credit_card_account_logistics_003 Step 4: "Found a better card: Ask what features attracted them. If Rho-Bank offers a card with similar or better benefits, offer to help them apply"
  - `user_scenario step 6: "I found a card at another bank that offers 3.25% back those [travel, software]"`
  - `doc_credit_cards_silver_rewards_card_002: "eligible travel and software transactions to earn 4.0% back"`
  - `doc_credit_cards_platinum_rewards_card_002: "You earn 10.0% cash back on all eligible purchases."`
  - `doc_business_credit_cards_business_silver_rewards_card_002: "Earn 10.0% cash back on eligible travel and software purchases"`
  - `gold[18] (048_10, user apply_for_credit_card).arguments.card_type = "Silver Rewards Card"`
  - `user_scenario step 8: apply if "the card details ... [are] competitive or better than the competitor"`
  - *Why it matters:* An agent that recommends the card with the highest rewards (Platinum Rewards) or the strongest category match (Business Silver for a self-employed consultant) gets a customer who, under step 8, applies for that card. credit_card_applications then differs from the gold.
  - *Fix:* Make the customer's constraints rule out the other cards (for example 'no annual fee, personal card'), or name the Silver Rewards Card explicitly as the only acceptable recommendation in the script.
- **non_determinism (Minor)** — The Crypto-Cash Back closure reason is logged as unhappy_with_rewards, but the author notes and the user script follow the 'not using the card' retention path (subscriptions, credit score), which suggests not_using_card.
  - `user_scenario step 9: "The crypto rewards program isn't really worth it for me anymore. I don't use cryptocurrency much."`
  - `user_scenario step 10: "If the agent reminds you about keeping the card active for credit score or setting up subscriptions"`
  - `doc_credit_cards_credit_card_account_logistics_003 Step 4: "Not using the card: ... suggest setting up a recurring subscription to keep the card active."`
  - `gold[21] (048_13).arguments.closure_reason = "unhappy_with_rewards"`
  - *Why it matters:* The literal statement supports unhappy_with_rewards (the gold), but the scripted conversation is built around the not_using_card branch. An agent that picks not_using_card fails on credit_card_closure_reasons.
  - *Fix:* Remove 'I don't use cryptocurrency much', or align the step-10 branch with the unhappy-with-rewards protocol.

*Verifier: Confirmed (Major → Major).* Reproduced. The application depends on which qualifying card the agent recommends, and the hint naming Silver Rewards sits only in the simulator's script, so Major stands. Unlike 045/047, the customer does not already hold the Platinum card and is closing a personal card. The crypto-reason ambiguity is Minor, consistent with the class.

### task_049 — Blocker

**The official answer records the customer pressing a 'request human transfer' tool that the script never tells the simulated customer to use, so correct agent work fails whenever the customer simply asks out loud.**

- **instruction_gold_mismatch (Blocker)** — Gold action 049_13 is a user-side call to request_human_agent_transfer, which writes a row to human_transfer_requests. The script only has the customer say 'Transfer me to a human agent.' and never names the tool, unlike tasks 034 and 081, which explicitly tell the simulator to call it. The simulator guidelines also say to call tools only when the agent requests them.
  - `gold[17] (049_13) = {name: request_human_agent_transfer, requestor: user, arguments: {}}`
  - user_scenario step 9: "Transfer me to a human agent." / step 10: "After the agent transfers you, end the conversation." (no mention of request_human_agent_transfer)
  - `task_034 / task_081 scripts: "Call the `request_human_agent_transfer` tool (for tracking purposes — the agent cannot see this)"`
  - data/tau2/user_simulator/simulation_guidelines_tools.md: "Only call a tool if the agent has requested it or if it is necessary to answer a question the agent has asked."
  - `tools.py KnowledgeUserTools.request_human_agent_transfer: add_to_db("human_transfer_requests", "transfer_request_<n>", ...)`
  - `Replay: gold without the user call -> verified=False, table 'human_transfer_requests' differs; user call made twice -> verified=False`
  - *Why it matters:* The agent cannot create this row (transfer_to_human_agents writes nothing), and no document tells it to have the customer call the tool. The reward therefore depends on whether the simulated customer spontaneously calls a tool its guidelines tell it not to call, and calls it exactly once.
  - *Fix:* Add 'Call the request_human_agent_transfer tool, then ask for a human' to the script, as tasks 034 and 081 do, or drop gold action 049_13.
- **non_determinism (Minor)** — For the Crypto-Cash Back card the customer gives two reasons, the fee and poor rewards. The gold logs annual_fee.
  - `user_scenario step 7: "The annual fee is too high for what I'm getting. The crypto rewards aren't worth it anymore."`
  - `gold[14] (049_10).arguments.closure_reason = "annual_fee"`
  - *Why it matters:* credit_card_closure_reasons is compared exactly. unhappy_with_rewards is a defensible label that fails, though the first-stated reason and the scripted downgrade branch support annual_fee.
  - *Fix:* Drop the second sentence or have the customer name the fee as the main reason.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced. The graded state needs exactly one spontaneous user tool call that the script never asks for and the simulator guidelines discourage, and the agent cannot cause it, so the result is chance: Blocker. The agent-side flow is otherwise sound. The Crypto closure-reason issue stays Minor.

### task_053 — Blocker

**The official answer files the dispute with card digits '2791', which only the customer's own lookup tool can supply, yet it leaves out that lookup call, so a run where the customer follows the script and looks the number up can never match.**

- **instruction_gold_mismatch (Blocker)** — The gold gives the customer get_card_last_4_digits (053_13) and files the dispute with card_last_4_digits '2791', the value that tool returns for cc_e9d195fe8e_silver. It omits the customer's call_discoverable_user_tool, which logs a row in user_discoverable_tool_calls. The script tells the customer to make that call, and no other source of '2791' exists.
  - `gold[13] (053_13) give_discoverable_user_tool get_card_last_4_digits; no requestor=user action in the gold`
  - `gold[15] (053_15).arguments: card_last_4_digits = "2791"`
  - `sha256('card_last4:cc_e9d195fe8e_silver') digit extraction = 2791 (KnowledgeUserTools.get_card_last_4_digits)`
  - user_scenario: "Card last 4 digits? 'I don't have my card in front of me right now ...' (If the agent provides you with the get_card_last_4_digits tool, use it to retrieve the number.)"
  - `tools.py get_card_last_4_digits: self._log_user_tool_call("get_card_last_4_digits", args) -> user_discoverable_tool_calls`
  - Replay: gold + scripted user call {credit_card_account_id: cc_e9d195fe8e_silver} -> verified=False, table 'user_discoverable_tool_calls' differs (gold: none; predicted: 9a452d6c48d8d07e)
  - *Why it matters:* A correct run needs '2791' in the dispute record and has no user_discoverable_tool_calls row. The digits are only available through the logged user call. Every agent that follows the documents (doc_013: give the user the tool) and gets the right digits therefore fails, under both upstream and verified grading.
  - *Fix:* Add a requestor=user call_discoverable_user_tool action for get_card_last_4_digits with {"credit_card_account_id": "cc_e9d195fe8e_silver"} after gold action 053_13, as task_041 does.
- **hidden_ordering (Major)** — The gold processes the credit-limit increase before filing the dispute, because a pending dispute blocks CLI approval. The customer asks for the dispute first, and no document tells the agent to reorder concurrent requests to avoid the dispute check.
  - `user_scenario opening: "State BOTH requests upfront, but the dispute first"`
  - `doc_credit_cards_credit_card_account_logistics_007 Step 2: "3. No Pending Disputes: Verify the account has no active disputes."`
  - `tools.py approve_credit_limit_increase_5847 rejects when the user has a dispute with status SUBMITTED/UNDER_REVIEW/PENDING`
  - Replay: dispute filed first, then approve -> "Error: Credit limit increase request cannot be approved at this time."; dispute first + deny(pending_disputes) -> verified=False (missing approve, extra deny, credit_card_accounts and credit_limit_increase_requests differ)
  - *Why it matters:* An agent that handles requests in the customer's order, which the documents allow, files the dispute, finds a pending dispute, and denies the CLI per policy. That is a documented outcome, but it fails. Passing requires noticing the interaction and sequencing the CLI first, which the author notes call the test but which no document states.
  - *Fix:* Add a rule to logistics_007 or the dispute doc on handling a CLI and a new dispute in the same contact (for example, 'process the CLI before filing a new dispute'), or have the customer ask for the CLI first.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced. '2791' reaches the agent only through a logged user call that the gold omits, so no trajectory can match the gold state: Blocker. The CLI-before-dispute ordering is a separate Major (two defensible orders with no document rule), and the same defect exists in task_054.

### task_054 — Major

**The customer never says whether she wants expedited shipping for the replacement card, but the gold records expedited; the documents' strong recommendation for fraud cases makes it the likely default.**

- **underspecified_instructions (Minor)** — The gold replacement order sets expedited_shipping=true, a stored field, yet the customer script only says to send the card to the address on file. The replacement procedure tells the agent to ask, and strongly recommends expedited (free on Gold) for fraud, so the documented default matches the gold.
  - `gold[14].arguments: "expedited_shipping": true`
  - `user_scenario step 9: "Yes, please send me a new card with a new number... Just send it to my address on file."`
  - `doc_credit_cards_credit_card_replacements_001: "Ask whether they want expedited shipping (advise on possible fees by tier; see Shipping selection)."`
  - doc_credit_cards_credit_card_replacements_001: "Premium-tier and above (Gold, Platinum, Diamond Elite): $0.00 (complimentary)." and "If the reason is fraud_suspected or stolen, strongly recommend expedited shipping"
  - `tools.py order_replacement_credit_card_7291 stores "expedited_shipping": expedited_shipping (default False) in credit_card_orders`
  - `Replay: gold with expedited_shipping=false -> _verified_db_match False, "table 'credit_card_orders' differs"`
  - *Why it matters:* An agent that asks neutrally and gets no preference, or that relies on the tool default, orders standard shipping and fails on credit_card_orders even though the rest of the work is correct.
  - *Fix:* Add a line to the customer script accepting expedited shipping (e.g., "Yes, expedited please since it's free").

*Verifier: Upgraded (Minor → Major).* The expedited-shipping Minor holds. The review missed the ordering defect it flagged as Major in sibling task_053. An agent that handles the fraud first, as the customer asks, files the dispute and orders the replacement, then must deny the CLI under logistics_007, and fails. The gold needs the agent to anticipate the conflict and put the CLI ahead of a fraud response the customer called urgent, which no document prescribes. That is two defensible orders with different graded states, Major under calibration, and the same as 053.

### task_056 — Major

**The business-savings procedure tells the agent to open the account with account_type 'savings', but the gold uses 'business_savings'; following the document creates a differently keyed personal savings account and fails.**

- **document_contradiction (Major)** — doc_(general)_004, the internal procedure for opening business savings, says to call open_bank_account_4821 with account_type 'savings'. The tool's own description reserves 'savings' for personal savings and lists 'business_savings'. The gold follows the tool description.
  - `doc_bank_accounts_bank_accounts_(general)_004 (Tool: open_bank_account_4821 > How to call): "Set account_type to 'savings'."`
  - tools.py open_bank_account_4821 docstring (shown on unlock): "Must be one of: 'checking' (personal checking), 'savings' (personal savings), 'business_checking', 'business_savings'"
  - `gold[5].arguments: {"account_type": "business_savings", "account_class": "Silver Plus Saver Account"}`
  - Replay with account_type 'savings': tool returns "Bank account opened successfully! Account ID: 3e54498f671ab53f ... Account Type: savings" (personal-savings eligibility passes via Green checking chk_b5e8f2a1c9, opened 09/10/2023); after transferring $3,200 to it, _verified_db_match False, "table 'accounts' differs"
  - *Why it matters:* The account_id is derived from user_id:account_type:account_class. An agent that follows the internal procedure verbatim opens a personal-type account with a different ID and funds that account, and the agent gets no error to correct from, so a careful document-following agent fails.
  - *Fix:* Change doc_(general)_004 to "Set account_type to 'business_savings'" (it also says "Returns a new savings account record").

*Verifier: Confirmed (Major → Major).* Reproduced the doc_004 contradiction and the replay failure, including the exact account id the review cites. The product choices and the $3,200 transfer amount follow from the documents and the script. Two document-supported readings (procedure text vs tool docstring) with the gold following one: Major per calibration, same as task_071.

### task_059 — Major

**The gold opens the savings product as 'Green Account', but the documents name it 'Green Account (savings)' and give 'Green Account (checking)' as an official class string, so an agent can reasonably pick a spelling that fails.**

- **document_contradiction (Major)** — The exact account_class string for the Green savings product is ambiguous. The savings procedure's "ending with 'Account'" rule points to 'Green Account', which the gold uses. The checking procedure's own example 'Green Account (checking)', and every Green savings document title, point to 'Green Account (savings)'.
  - doc_bank_accounts_bank_accounts_(general)_002: "account_class must use the full official name ending with 'Account', e.g., 'Silver Plus Account', 'Gold Account'"
  - doc_bank_accounts_bank_accounts_(general)_001: "Personal checking account_class options must use the full official name ending with 'Account' (e.g., 'Blue Account', 'Green Account (checking)')"
  - Savings product docs are titled "Green Account (savings) specifications and requirements" (doc_savings_accounts_green_account_(savings)_001) and the FAQ asks "What APY does the Green Account (savings) earn?" (_005); evergreen_account_001: "Link a Green Account (savings): +0.55% APY boost"
  - `tools.py open_bank_account_4821: account_id = _deterministic_id(f"account:{user_id}:{account_type}:{account_class}") and account_class is stored verbatim`
  - `gold[5].arguments: {"account_type": "savings", "account_class": "Green Account"}`
  - `Replay with account_class 'Green Account (savings)': _verified_db_match False, "table 'accounts' differs"`
  - *Why it matters:* An agent that copies the product's full name as documented opens an account with a different class and ID. The accounts table then differs and the task fails, even though the product choice is right.
  - *Fix:* State the exact account_class string for the Green savings product in general_002 (e.g., "Green Account" for savings), or fix general_001's example so the parenthetical is clearly not part of the class name.

*Verifier: Confirmed (Major → Major).* Reproduced the product optimum and the class-string failure. Two document-supported spellings with the gold following one: Major per calibration. Gold also requires get_all_user_accounts_by_user_id_3847 (task_058, the same scenario at $20,000, does not); a careful agent checks the 14-day tenure, so that is a note, not an issue.

### task_063 — Blocker

**Bronze Rewards and Silver Rewards add the same +0.15% to the recommended Silver Plus Account, and both meet the customer's conditions, but the gold accepts only Silver Rewards.**

- **non_determinism (Blocker)** — On the best eligible account (Silver Plus, Tier 1 3.0%), Bronze Rewards and Silver Rewards give identical +0.15% bonuses. Both have a $0 fee and both run a credit check with a minimum at or below the customer's 700, so the customer's sole metric is tied and nothing breaks the tie.
  - `doc_savings_accounts_silver_plus_account_009: "| Bronze Rewards Card | +0.15% |" and "| Silver Rewards Card | +0.15% |"`
  - `doc_credit_cards_bronze_rewards_card_001: "Minimum credit score: $640", "Annual fee: $0.00", "Consent to a credit pull"`
  - `doc_credit_cards_silver_rewards_card_001: "Minimum credit score: $680", "Annual fee: $0.00", "Consent to a credit check"`
  - Computation: $8,000 x (3.0% + 0.15%) = $252.00 for either card; next best Silver Plus + Green Rewards (business, +0.1%) = $248, Silver + Crypto-Cash Back (+0.5%) = $240
  - `gold[1].arguments.card_type = "Silver Rewards Card"`
  - `Replay with card_type 'Bronze Rewards Card': _verified_db_match False, "table 'credit_card_applications' differs" (application_id hashes card_type)`
  - *Why it matters:* A correct agent picks one of two equally good cards. Half of correct recommendations fail on credit_card_applications, so the result is chance.
  - *Fix:* Make the Silver Plus bonuses differ (e.g., Bronze Rewards +0.1%), or give the customer a stated preference that only Silver Rewards satisfies.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced the exact tie on the customer's only metric between two credit-checking, no-fee cards both within a 700 score; nothing in the documents breaks it. Tie with no documented tie-breaker: Blocker per calibration.

### task_065 — Major

**The pairing and order are well determined (Evergreen checking plus Green savings, opened before closing Light Blue), but the gold spells the savings class 'Green Account' while the documents also support 'Green Account (savings)'.**

- **document_contradiction (Major)** — This is the same class-string ambiguity as task_059. The savings procedure's "ending with 'Account'" rule gives 'Green Account', which the gold uses. The documented full product name and the checking procedure's example format give 'Green Account (savings)'.
  - doc_bank_accounts_bank_accounts_(general)_002: "account_class must use the full official name ending with 'Account', e.g., 'Silver Plus Account', 'Gold Account'"
  - doc_bank_accounts_bank_accounts_(general)_001: "Personal checking account_class options must use the full official name ending with 'Account' (e.g., 'Blue Account', 'Green Account (checking)')"
  - Savings product docs are titled "Green Account (savings) specifications and requirements" (doc_savings_accounts_green_account_(savings)_001) and the FAQ asks "What APY does the Green Account (savings) earn?" (_005); evergreen_account_001: "Link a Green Account (savings): +0.55% APY boost"
  - `tools.py open_bank_account_4821: account_id = _deterministic_id(f"account:{user_id}:{account_type}:{account_class}") and account_class is stored verbatim`
  - `gold[2].arguments: {"account_type": "savings", "account_class": "Green Account"}`
  - `Replay with account_class 'Green Account (savings)': _verified_db_match False, "table 'accounts' differs"`
  - *Why it matters:* An agent that copies the product's full documented name opens an account with a different class and ID, so the task fails despite the right product, pairing and order.
  - *Fix:* State the exact account_class string for the Green savings product in general_002, or correct general_001's 'Green Account (checking)' example.

*Verifier: Confirmed (Major → Major).* Evergreen + Green savings (4.55%) is the unique optimum and the savings-before-closure order is documented. The only defect is the Green class-string ambiguity shared with 059/066/068, Major per calibration.

### task_066 — Major

**The savings/checking/credit-card combination is uniquely derivable, but the savings account name the gold uses ("Green Account") is not the name the documents use for that product ("Green Account (savings)").**

- **document_contradiction (Minor)** — open_bank_account_4821 hashes account_class into the account id, and the gold passes "Green Account" for the savings product, while every document names that product "Green Account (savings)" and the checking-opening doc uses the parenthesised form as an example class name.
  - `gold[4].arguments = {"account_type": "savings", "account_class": "Green Account"}`
  - doc_bank_accounts_bank_accounts_(general)_002: "account_class must use the full official name ending with 'Account', e.g., 'Silver Plus Account', 'Gold Account'"
  - `doc_bank_accounts_bank_accounts_(general)_012: "3. Evergreen Account (checking) + Green Account (savings)"`
  - `doc_bank_accounts_bank_accounts_(general)_001: "must use the full official name ending with 'Account' (e.g., 'Blue Account', 'Green Account (checking)')"`
  - `tools.py open_bank_account_4821: seed = f"account:{user_id}:{account_type}:{account_class}"`
  - `replay: substituting "Green Account (savings)" -> verified match False, "table 'accounts' differs"`
  - *Why it matters:* An agent that copies the product name as the documents print it ("Green Account (savings)"), by analogy with the checking doc's own example, creates a different account id and fails the accounts table.
  - *Fix:* State the exact savings class string ("Green Account") in doc_002 or in the Green savings spec doc, or make the tool normalise the parenthetical qualifier.

*Verifier: Upgraded (Minor → Major).* The evidence is identical to task_059 and task_065 (same gold string, same documents, same failing replay), which the reviewers rated Major. The finding's own summary describes two document-supported spellings that lead to different accounts records, which calibration rates Major; I found no stated reason for Minor (the task_068 reviewer's remark that doc_002 has no contradicting example applies equally to 059 and 065). The product combination itself checks out.

### task_068 — Major

**The gold opens the Green checking account as "Green Account", but the checking-opening procedure gives "Green Account (checking)" as the example class name, so an agent following the procedure literally fails.**

- **document_contradiction (Major)** — The internal procedure for opening personal checking accounts explicitly lists 'Green Account (checking)' as a valid account_class; the gold uses "Green Account". The class string is hashed into the account id, so the two readings produce different accounts records.
  - doc_bank_accounts_bank_accounts_(general)_001: "Personal checking account_class options must use the full official name ending with 'Account' (e.g., 'Blue Account', 'Green Account (checking)')."
  - `doc_bank_accounts_bank_accounts_(general)_005: "MID TIER (Blue Account, Green Account (checking))"`
  - `gold[3].arguments = {"account_type": "checking", "account_class": "Green Account"}`
  - `replay: "Green Account (checking)" -> verified match False, "table 'accounts' differs"`
  - *Why it matters:* The procedure doc the agent must follow to open a checking account gives the parenthesised form as the example; an agent that copies it creates account id hash of "account:rp65a7b3c4:checking:Green Account (checking)" and fails.
  - *Fix:* Change the example in doc_001 to a name without a qualifier (or state that the qualifier is dropped), or accept both spellings in the tool.

*Verifier: Confirmed (Major → Major).* This is the strongest case of the Green class-string defect: the checking procedure's only worked example is the parenthesised form, so a literal agent fails. I keep Major rather than Blocker because the gold spelling is still document-supported (the 'ending with Account' rule and bare 'Green Account' usage for the checking product), and calibration reserves Blocker for golds that follow no supported reading.

### task_069 — Blocker

**The gold's Silver Plus savings (3.5% total) is beaten by Gold savings (5.7%) and even Silver savings (4.1%), both of which the documents say offer ATM fee rebates, so a correct agent fails.**

- **argument_error (Blocker)** — The author notes assert Gold, Silver, Green and Bronze savings lack ATM fee rebates, but the knowledge base gives Gold a $30/month and Silver a 15/month ATM fee rebate. With the customer's $10,000, Gold (5.5% + 0.2% Silver Rewards = 5.7%) and Silver (4.0% tier 2 + 0.1% + 0.025% = 4.125%) both satisfy every stated requirement and beat the gold's Silver Plus + Blue + Silver Rewards = 3.5%.
  - `doc_savings_accounts_gold_account_003: "ATM fee rebate cap per month: $30"`
  - `doc_savings_accounts_gold_account_013: "Combined with the existing 30 ATM fee rebates and 20 monthly withdrawals"`
  - `doc_savings_accounts_gold_account_001: "Maintain at least $10,000"; "APY of 5.5%"`
  - `doc_savings_accounts_gold_account_014: "| Silver Rewards Card | +0.2% |"`
  - `doc_savings_accounts_silver_account_005: "Do you rebate ATM fees? - Yes. You can receive ATM fee rebates up to 15 each month."`
  - `doc_savings_accounts_silver_account_003: "At or above threshold | At least $10,000 | 4.0%"`
  - `doc_savings_accounts_silver_plus_account_002: "Tier 1 APY: 3.0% for balances below the Tier 2 threshold" (threshold $15,000)`
  - `description.notes: "Needs ATM fee rebates on savings account - blocks Gold Account, Silver Account, Green Account (savings), Bronze Account"`
  - `gold[2].arguments.account_class = "Silver Plus Account"`
  - *Why it matters:* Following the documents, the highest-APY savings account meeting all three requirements is Gold (paired with Blue checking for overdraft protection, no boost) at 5.7%; the user script accepts any recommendation, so the agent opens Gold and the accounts table differs from the gold.
  - *Fix:* Either remove the ATM rebate lines from the Gold and Silver savings docs, or change the gold to open a Gold Account (savings) with Blue checking and Silver Rewards, and update the user script's Gold objection.

*Verifier: Confirmed (Blocker → Blocker).* Confirmed: the author's premise that Gold and Silver savings lack ATM rebates is contradicted by the knowledge base, and Gold beats the gold's Silver Plus on every stated criterion. No document supports the gold's exclusion of Gold, so Blocker.

### task_071 — Major

**The account choices are right, but the business-savings procedure tells the agent to open the account with account_type 'savings' while the gold uses 'business_savings', and the two produce different accounts.**

- **document_contradiction (Major)** — doc_004 (Opening Business Savings Accounts) instructs "Set account_type to 'savings'", while the tool docstring lists 'business_savings' and the gold uses it. With account_type 'savings' the tool runs the personal-savings eligibility check, which this customer passes (3-year personal Green checking), so the call succeeds and creates a different account id and record.
  - doc_bank_accounts_bank_accounts_(general)_004: "How to call: - Set account_type to 'savings'. - Set account_class to the exact official name provided by the customer (e.g., 'Bronze Saver Account')."
  - tools.py open_bank_account_4821 docstring: "Must be one of: 'checking' (personal checking), 'savings' (personal savings), 'business_checking', 'business_savings'"
  - `gold[5].arguments = {"account_type": "business_savings", "account_class": "Gold Saver Account"}`
  - `replay: account_type "savings" -> "Bank account opened successfully! ... Account Type: savings"; verified match False, "table 'accounts' differs"`
  - *Why it matters:* An agent that follows the internal business-savings procedure verbatim opens a "savings" account and fails the accounts table even though it chose the right product.
  - *Fix:* Change doc_004's tool instructions to "Set account_type to 'business_savings'".
- **underspecified_instructions (Minor)** — Sky Blue is a startup account restricted to companies within 4 years of formation, and the customer script never says how old the business is. The promotion only applies among accounts the customer qualifies for, so the gold silently assumes eligibility.
  - `doc_business_checking_accounts_sky_blue_001: "Confirm your company is within 4 years of formation."`
  - `doc_business_checking_accounts_sky_blue_008: "Eligibility criteria tied to company age are evaluated when you open the account; the threshold is 4."`
  - `user_scenario.instructions: no formation date or company age is given`
  - *Why it matters:* A careful agent that asks the company age gets an improvised answer; if the simulated customer says more than 4 years, the agent correctly falls back to Lime Green and fails the gold. Most agents will not ask, so the effect is limited.
  - *Fix:* Add a line to the script stating the business was formed within the last 4 years (e.g., "I started the agency 2 years ago").

*Verifier: Confirmed (Major → Major).* Reproduced both picks and the doc_004 failure; same defect and severity as task_056. The Sky Blue company-age gap is Minor as in task_070.

### task_072 — Major

**Both gold refund amounts include fee errors dated after the benchmark's fixed "today" (11/14/2025), so an agent that only reviews fees posted so far credits $13.50 and $3.00 instead of $14.00 and $3.50.**

- **argument_error (Major)** — The clock is 2025-11-14 03:40 EST, but the seeded November history runs to 11/20, and the gold credits include a Bluest error dated 11/20 ($2.50 fee vs $2.00) and a Light Green error dated 11/15 ($4.00 vs $3.50 tier-2 foreign fee).
  - `tools.py get_current_time: "The current time is 2025-11-14 03:40:00 EST."`
  - `db.json bank_account_transaction_history btxn_fcd7ef3a24ed: date 11/20/2025, atm_fee -2.5 (US BANK #7890, rebate +2.0)`
  - `db.json btxn_49c0c0b3b8c1: date 11/15/2025, atm_fee -4.0 on a $200 SANTANDER MADRID withdrawal`
  - `doc_checking_accounts_light_green_account_013: "More than $100 and up to and including $300 | $3.50"`
  - `gold[7].amount = 14.00; gold[8].amount = 3.50`
  - *Why it matters:* Bluest through 11/14: $8.00 (London foreign) + $3.50 (Tokyo foreign) + $2.00 (missing 11/14 rebate) = $13.50; Light Green through 11/14: $1.50 + $3.00 - $1.50 = $3.00. Gold needs the 11/20 (+$0.50) and 11/15 (+$0.50) items. Either reading is defensible, and the credit amounts differ, so the transaction id and balance differ.
  - *Fix:* Move all seeded November transactions to on or before 11/14/2025, or advance the clock past 11/20/2025.

*Verifier: Confirmed (Major → Major).* Reproduced both pre-clock totals and the gold totals that need the 11/15 and 11/20 rows; Major per the post-clock calibration. Two further readings touch this task without changing its severity: the 11/14 'missing' Bluest rebate assumes the rebate covers Rho-Bank's own fee (bluest_003 'third-party ATM fees' vs bluest_007 'aggregate ATM fees'), and under the fee-stacking reading that tasks 075/076 need, the Light Green foreign withdrawals would count toward the 4 free out-of-network uses and change the Light Green net.

### task_073 — Major

**The Green account's gold refund ($9.00) includes a duplicate fee dated 11/15, after the benchmark's fixed "today", so an agent that only reviews fees posted so far credits $6.00.**

- **argument_error (Major)** — Fixed clock is 2025-11-14 03:40, but the Green account's duplicate $3.00 fee (one of three errors in the $9.00 credit) is dated 11/15/2025. The Light Green credit also uses post-clock rows (11/15 overcharge +$1.50, 11/17 missing fee -$1.50), which happen to cancel.
  - `tools.py get_current_time: "2025-11-14 03:40:00 EST"`
  - `db.json btxn_kj18k9l0m1n3 and btxn_kj18k9l0m1n4: both 11/15/2025, atm_fee -3.0, for one $250 PNC withdrawal`
  - `gold[9].amount = 9.00 (chk_kj93a7b2e1_2)`
  - `db.json btxn_kj28y9z0a1b3: 11/15/2025 -5.0 on $150 KB Kookmin (tier 2 = $3.50); btxn_kj29c3d4e5f6: 11/17/2025 TD Bank withdrawal with no fee`
  - *Why it matters:* Green through 11/14: Rho-Bank ATM fee $3.00 + Woori $15 vs $12 = $6.00, not $9.00. Both readings are defensible; the credit amount is hashed into the transaction id and balance.
  - *Fix:* Re-date the post-clock rows to on or before 11/14/2025 (or move the clock), keeping the intended errors.

*Verifier: Confirmed (Major → Major).* Recomputed all three accounts. Only the Green credit depends on a post-clock row, which is enough for Major per calibration.

### task_074 — Major

**The corrected Light Blue refund ($14.50) and the Dark Green and Evergreen refunds are right, but the Purple refund ($27.00) still counts a fee dated after "today" and a rebate the Purple docs limit to ATM-operator fees.**

- **argument_error (Major)** — The Purple credit includes the duplicate $2.50 fee posted 11/15/2025, after the fixed clock (2025-11-14 03:40). Counting only rows up to today gives $24.50.
  - `tools.py get_current_time: "2025-11-14 03:40:00 EST"`
  - `db.json btxn_ar_purple_15f and btxn_ar_purple_15f_dup: 11/15/2025, atm_fee -2.5 each, one rebate btxn_ar_purple_15r +2.5`
  - `gold[9].amount = 27.00 (chk_ar72c5d8e3_1)`
  - *Why it matters:* An agent that excludes transactions dated after today credits $24.50; the amount is hashed into the credit transaction id and the balance, so the DB differs.
  - *Fix:* Re-date the 11/15-11/18 rows to on or before 11/14/2025, or advance the clock.
- **document_contradiction (Major)** — $2.50 of the Purple credit is a "missing rebate" on Rho-Bank's own $3.50 out-of-network fee (11/11 BofA). The Purple docs define the $30/month rebate as a refund of ATM-operator fees, not of Rho-Bank's fee, so a document-faithful agent credits only the $1.00 overcharge. The seeded rows (every other NON-RHO fee paired with an equal ATM FEE REBATE) support the gold's broader reading.
  - `doc_checking_accounts_purple_account_004: "You are eligible for refunds of ATM operator fees up to a monthly cap of $30."`
  - `doc_checking_accounts_purple_account_010: "Confirm that the charge is labeled as an ATM operator fee"`
  - `doc_checking_accounts_purple_account_012: "You are charged $2.50 per cash withdrawal made at an out-of-network ATM."`
  - `db.json btxn_ar_purple_11f: 11/11/2025 NON-RHO ATM FEE -3.5, no rebate row; btxn_ar_purple_05f/05r: -2.5/+2.5`
  - `description.notes: "(4) $3.50 fee charged instead of $2.50 AND missing $2.50 rebate"`
  - *Why it matters:* Strict reading: Purple = $24.50 (or $22.00 through today) instead of $27.00. Task_075 relies on the opposite reading (Purple's $2.50 fees are not rebated), so the benchmark itself is inconsistent about this policy.
  - *Fix:* State in the Purple docs whether the $30 global rebate covers Rho-Bank's out-of-network fee, and align task_074 and task_075 to that statement.
- **answer_leak (Minor)** — Several seeded transaction ids flag the errors: the tool prints each record id, and ids such as btxn_ar_purple_03f_err, btxn_ar_lb_05f_err and btxn_ar_purple_15f_dup mark which fees are wrong. v1.0.1 scrubbed the descriptions but not the ids.
  - `tools.py get_bank_account_transactions_9173: formatted_lines.append(f"{i}. Record ID: {record_id}")`
  - db.json ids: btxn_ar_purple_03f_err, btxn_ar_purple_07f_err, btxn_ar_purple_09f_err, btxn_ar_purple_15f_dup, btxn_ar_lb_03f_err, btxn_ar_lb_05f_err, btxn_ar_lb_08f_err, btxn_ar_dg_02f_err, btxn_ar_ev_03f_err
  - *Why it matters:* Does not change the correct state, but partly gives away which fees are erroneous, weakening what the task measures (the same kind of leak #374 removed from descriptions).
  - *Fix:* Rename the seeded ids to neutral values.
- **document_gap (Minor)** — The Purple out-of-network fee ($2.50) that the Purple items depend on is stated only in purple_account_012, which is not in required_documents; it is retrievable by search.
  - `required_documents lists doc_checking_accounts_purple_account_001 and _004 only for Purple`
  - `doc_checking_accounts_purple_account_012: "$2.50 per cash withdrawal made at an out-of-network ATM"`
  - *Why it matters:* Under golden retrieval the agent cannot verify the $2.50 baseline; in default retrieval it can.
  - *Fix:* Add doc_checking_accounts_purple_account_012 to required_documents.

*Verifier: Confirmed (Major → Major).* Reproduced every account total and both Major issues (post-clock duplicate; Purple rebate scope where the docs say operator fees but the seeded rows rebate Rho-Bank's fee), plus the Minor id leak and the Minor required-documents gap for purple_account_012. The gold here assumes the broad Purple rebate and no fee stacking abroad; task_075 needs the opposite on both points, so the gold set is internally inconsistent.

### task_075 — Major

**Green Fee-Free is cheapest only if Purple's $2.50 out-of-network fee applies abroad and is not covered by Purple's $30 monthly ATM rebate; the benchmark's own fee-refund tasks assume the opposite on both points.**

- **document_contradiction (Major)** — The gold needs two readings: (a) at a foreign non-Rho ATM, both the out-of-network fee and the foreign fee apply, and (b) Purple's "Global ATM fee rebates: up to $30 per month" does not cover Rho-Bank's own fee. Under either alternative, Purple's bank fees for 6 withdrawals a month are $0 (or $15 fully rebated), and Purple also rebates ATM-operator surcharges, which Green Fee-Free does not, so Purple is at least as cheap.
  - doc_checking_accounts_green_fee-free_account_005: "Out-of-network ATM withdrawal fee | $0.00"; "Foreign ATM withdrawals are also fee-free: $0.00 per withdrawal. Third-party ATM operator fees may still apply."
  - doc_checking_accounts_purple_account_001: "Global ATM fee rebates | Up to $30 per month"; "No foreign ATM withdrawal fees: $0.00 per withdrawal (third-party ATM operator fees may still apply)"
  - `doc_checking_accounts_purple_account_012: "You are charged $2.50 per cash withdrawal made at an out-of-network ATM."`
  - `doc_checking_accounts_purple_account_004: "You are eligible for refunds of ATM operator fees up to a monthly cap of $30."`
  - task_074 gold refunds the whole $8.00 foreign fee on a Purple London withdrawal (no $2.50 out-of-network fee kept) and credits a "missing $2.50 rebate" on a Purple NON-RHO fee
  - `gold[2].arguments.account_class = "Green Fee-Free Account"`
  - *Why it matters:* Strict docs: GFF $0 vs Purple 18 x $2.50 = $45 (gold). Non-stacking or broad-rebate reading: Purple $0 in bank fees plus up to $30/month of operator-surcharge refunds, so a careful agent can defensibly recommend Purple and fail the accounts table.
  - *Fix:* State explicitly whether out-of-network and foreign ATM fees stack and whether Purple's rebate covers Rho-Bank's own fee, apply the same rule in tasks 072-074, and add an operator-surcharge statement to the customer script (or tell the customer to count only Rho-Bank fees).

*Verifier: Adjusted (Major → Major).* Severity holds, reasoning narrowed. Within this task the load-bearing alternative is non-stacking, which purple_001's parenthetical supports and the seeded 072-074 histories practise. The broad-rebate reading is weak here because purple_004/010 limit the rebate to operator fees, and the task_074 gold is not visible to an agent in this task, so it shows the benchmark is inconsistent rather than supporting a reading. The customer's own 'out of network ATMs abroad' favours the gold's stacking reading, so Major (not Blocker).

### task_076 — Major

**Bluest has lower ATM fees than the gold's Purple Account under every reading of the fee docs; the gold excludes Bluest for its $75,000 opening deposit, but the script never says whether the customer can make it.**

- **underspecified_instructions (Major)** — Among accounts with 2-day early direct deposit, Bluest costs 8 x $2.00 = $16 in ATM fees against Purple's 8 x $2.50 = $20 (or both $0 if out-of-network fees do not stack abroad or are rebated). The customer's only criterion is the lowest ATM fees, so Purple is chosen only by deciding she cannot fund Bluest's $75,000 opening deposit, which the script never addresses.
  - `doc_checking_accounts_bluest_account_001: "Early direct deposit | 2 day(s) before payday"; "Minimum opening deposit | $75,000"`
  - `doc_checking_accounts_bluest_account_010: "Cash withdrawal at an out-of-network ATM | $2.00 per withdrawal"; bluest_003: "Foreign ATM withdrawal fee | $0.00"`
  - `doc_checking_accounts_purple_account_012: "$2.50 per cash withdrawal made at an out-of-network ATM"`
  - `description.notes: "BLUEST ACCOUNT: ... $16 TOTAL (but requires $50k-100k minimum deposit - NOT PRACTICAL)"`
  - `user_scenario.instructions: no statement of available funds or deposit limits`
  - `open_bank_account_4821: no opening-deposit check`
  - *Why it matters:* An agent that minimises ATM fees as asked recommends Bluest (the user script accepts any recommendation) and fails; an agent that asks about the $75,000 deposit gets an improvised answer.
  - *Fix:* Have the customer state a deposit budget well below $75,000 (e.g., "I can only put about $5,000 in this account"), or accept Bluest.

*Verifier: Confirmed (Major → Major).* Reproduced: Bluest is never worse than Purple on ATM fees, and Purple wins only by assuming the customer cannot fund $75,000, which the script never says. Major as an unstated customer constraint with no default; the stacking ambiguity adds a Purple/Bluest tie but does not change the severity.

### task_082 — Blocker

**Fraud on the Green Fee-Free card calls for closing it, and the customer asks for a reissue, but the gold never closes that card, so an agent that follows the rules is marked wrong.**

- **instruction_gold_mismatch (Blocker)** — The CryptoGems dispute on the GFF card is recorded as close_and_reissue, the rules say to carry out the most severe action per card, and the customer asks for the GFF card to be reissued. The gold never closes dbc_mc47a2b9e1_gff.
  - `gold[15] CryptoGems dispute on dbc_mc47a2b9e1_gff: "card_action": "close_and_reissue"`
  - doc_bank_accounts_bank_accounts_(general)_031: "This parameter records metadata only; the agent must separately perform the indicated card action after filing the dispute." and "when performing the actual card action after filing all disputes, use the MOST SEVERE action across all disputes"
  - `user_scenario step 7: "Green Fee-Free card: I'd like to keep using this card but maybe with a new number? Can you reissue it?"`
  - `gold[17] closes only dbc_mc47a2b9e1_blue; no close/order for dbc_mc47a2b9e1_gff`
  - Replay: gold + close_debit_card_4721(dbc_mc47a2b9e1_gff, fraud_suspected) -> verified and exact both fail, debit_cards row dbc_mc47a2b9e1_gff status CLOSED vs gold ACTIVE
  - *Why it matters:* An agent that follows doc_031 and the customer's request closes the GFF card. The 48-hour ENTRY wait in doc_029 blocks only the reorder, not the close. The closed card leaves debit_cards different from the gold, so correct work scores 0.
  - *Fix:* Add close_debit_card_4721(card_id=dbc_mc47a2b9e1_gff, reason=fraud_suspected) to the gold, with no reorder because of the ENTRY 48-hour wait, or change the scenario so the GFF card is not compromised.
- **non_determinism (Major)** — Provisional-credit flags follow no single rule. FitLife (a 'not required' category) is set true. ElectroniX meets every 'required' condition but is set false because the PIN was 'yes_shared'. Sibling tasks set the not-required categories false.
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is REQUIRED when ALL of these conditions are met: ... 2. Dispute Category: ... 'duplicate_charge'"
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is NOT REQUIRED (but may be offered at discretion) when: ... 2. Customer has not contacted merchant first (for non-fraud disputes) 3. Customer shared their PIN voluntarily (pin_compromised = 'yes_shared')"
  - `doc_032 NOT REQUIRED list item 1 includes 'recurring_charge_after_cancellation'`
  - `gold[13] FitLife recurring_charge_after_cancellation: provisional_credit_eligible true`
  - `gold[12] ElectroniX card_present_fraud: pin_compromised 'yes_shared', provisional_credit_eligible false`
  - `task_083/084/086 gold set goods_services_not_received / incorrect_amount (same NOT REQUIRED list) to false`
  - `Replay: FitLife provisional false -> debit_card_disputes differs`
  - *Why it matters:* An agent applying 'not required, so not eligible' sets FitLife false, which is the convention used in the sibling tasks, and fails debit_card_disputes. The ElectroniX value depends on which of two overlapping lists wins.
  - *Fix:* Make doc_032 decisive (for example: eligible only when every REQUIRED condition holds and no NOT REQUIRED condition applies) and set FitLife to false.
- **non_determinism (Major)** — Several judgment values recorded in the dispute and card tables have two reasonable answers: pin_compromised for a PIN written on a note in a lost wallet, the Blue card closure reason (lost or fraud_suspected), and the Blue replacement shipping speed, which the script never states.
  - tool docstring pin_compromised: "'yes_shared': Customer shared PIN with someone; 'yes_observed': Customer believes PIN was observed/skimmed"; script: "I had my PIN written on a sticky note in my wallet"; gold[12] 'yes_shared'
  - doc_025 closing reasons include 'lost' and 'fraud_suspected'; doc_031 maps card_present_fraud -> close_and_reissue; gold[17] reason 'lost'; replay with 'fraud_suspected' fails (closure_reason and new card issue_reason 'fraud' vs 'lost')
  - doc_023 step 4: "Ask customer for preferred delivery option (STANDARD, EXPEDITED, or RUSH) and explain fees"; script gives no shipping answer; gold[19] STANDARD (MID tier also allows EXPEDITED $15); no documented default delivery option
  - *Why it matters:* Each of these values is stored and compared exactly, so a defensible alternative fails the task.
  - *Fix:* Script the shipping speed and the PIN answer explicitly, and state in doc_025 which closure reason to use when a lost card was used fraudulently.
- **document_gap (Major)** — customer_max_liability_amount is 50 for every dispute, including the ATM shortage noticed 11/09 and the FitLife charge noticed 11/11, both reported 11/14. Counting from when the customer noticed, as doc_031 says, gives the $500 tier.
  - doc_bank_accounts_bank_accounts_(general)_031: "inform the customer of their liability exposure based on when they noticed the unauthorized activity: - Reported within 2 business days of statement: Maximum liability $50 - Reported within 60 days of statement: Maximum liability $500"
  - tools.py file_debit_card_transaction_dispute_6281 docstring: "customer_max_liability_amount (number): The maximum dollar amount the customer could be liable for based on Regulation E reporting timing rules and the disputed amount. Use -1 for unlimited liability."
  - `No statement dates exist in the DB or the documents; get_now() = 2025-11-14 (Friday)`
  - `ATM noticed 11/09/2025 (Sun) -> 5 business days to 11/14; FitLife noticed 11/11/2025 -> 3 business days`
  - `gold[13], gold[14] customer_max_liability_amount 50`
  - *Why it matters:* An agent counting business days from discovery stores 500 for these disputes. An agent that treats Reg E tiers as applying only to unauthorized transfers may store 0. Either differs from the gold's 50 in debit_card_disputes.
  - *Fix:* State one deterministic rule in doc_031, for example: liability tier is counted from the discovery date to today in business days, applies to every dispute category, and is capped at the disputed amount. Then regenerate customer_max_liability_amount in every gold dispute.

*Verifier: Confirmed (Blocker → Blocker).* I checked for a document-supported reason to leave GFF open (pending transactions, ENTRY 48-hour wait) and found none: the wait only blocks the reorder. The gold records close_and_reissue but never acts on it, so a doc-following agent fails. The Major sub-issues reproduce. The Blue STANDARD shipping is unscripted with no documented delivery default (doc_023 marks only CLASSIC as default), so Major per calibration, as the review rated it.

### task_083 — Blocker

**Every gold dispute call leaves out a field the tool requires, and the task is graded by exact string match on those calls, so no correct agent can get credit.**

- **argument_error (Blocker)** — All four gold file_debit_card_transaction_dispute_6281 calls omit the required customer_max_liability_amount. On replay each one fails with a missing-argument error. ACTION grading compares the inner arguments JSON as a raw string.
  - `tools.py file_debit_card_transaction_dispute_6281 signature: customer_max_liability_amount: float (no default)`
  - Replay of gold[6..9]: "Error: Invalid arguments: KnowledgeTools.file_debit_card_transaction_dispute_6281() missing 1 required positional argument: 'customer_max_liability_amount'"
  - `evaluation_criteria.reward_basis = ['ACTION'], compare_args unset on gold[6..9]`
  - `data_model/tasks.py Action.compare_with_tool_call: compares tool_call.arguments to action arguments with == (inner 'arguments' is a JSON string)`
  - `gold[6] inner string contains "disputed_amount": 150.00 (two-decimal literal)`
  - *Why it matters:* A working dispute call must include customer_max_liability_amount, so its arguments string can never equal the gold string. Matching would also require identical key order, spacing, and the literal '150.00'. Reward is 0 for every competent agent.
  - *Fix:* Regenerate the four gold calls with customer_max_liability_amount, and set compare_args to the semantic keys (for example agent_tool_name only, or switch to DB grading) so JSON spelling does not decide the score.
- **non_determinism (Major)** — The duplicate Austin Coffee Roasters charges share a date. Picking btxn_d937eaa1d21d depends on reading the second-listed row as the earlier one under the most-recent-first contract, while 'earliest (first)' also reads naturally as the first one listed.
  - `doc_bank_accounts_bank_accounts_(general)_031: "Dispute the earliest (first) transaction when multiple duplicates exist."`
  - `doc_bank_accounts_bank_accounts_(general)_018: "Transactions are returned in reverse chronological order (most recent first)."`
  - tools.py get_bank_account_transactions_9173: stable sort by date, reverse=True; same-date rows keep stored order (comment: "identifies the later-listed record as the earlier one")
  - `Tool output for chk_dk83f5c2a1_gff: row 2 btxn_ff7d3926dee0 11/11/2025 -67.25, row 3 btxn_d937eaa1d21d 11/11/2025 -67.25`
  - `gold[8] transaction_id btxn_d937eaa1d21d`
  - *Why it matters:* An agent that takes the top-listed duplicate picks btxn_ff7d3926dee0 and misses gold[8].
  - *Fix:* Give the duplicates distinct timestamps, or say in doc_031 that among same-date duplicates in most-recent-first output the lower-listed row is the earliest.
- **document_contradiction (Major)** — The duplicate charge is set provisional-credit eligible although the customer has not contacted the merchant, a case the 'not required' list covers. The PIN-shared dispute resolves the same overlap the other way.
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is REQUIRED when ALL of these conditions are met: ... 2. Dispute Category: ... 'duplicate_charge'"
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is NOT REQUIRED (but may be offered at discretion) when: ... 2. Customer has not contacted merchant first (for non-fraud disputes) 3. Customer shared their PIN voluntarily (pin_compromised = 'yes_shared')"
  - `gold[8] duplicate_charge contacted_merchant false, provisional_credit_eligible true`
  - `gold[9] unauthorized_transaction pin_compromised yes_shared, provisional_credit_eligible false`
  - *Why it matters:* With compare_args unset, the boolean is part of the compared string, so an agent applying the merchant-contact condition fails gold[8].
  - *Fix:* Make doc_032's REQUIRED and NOT REQUIRED lists mutually exclusive.

*Verifier: Confirmed (Blocker → Blocker).* Confirmed: every gold dispute string omits a required argument and uses two-decimal literals. A working call can never string-match, and a byte-identical call would fail with a missing-argument error. The duplicate-row and provisional-credit points are real but cannot change a score that is already 0.

### task_084 — Blocker

**The gold's liability amounts follow no consistent rule: it caps one dispute at the charge amount but not another, so any agent applying one rule throughout gets a value wrong.**

- **argument_error (Blocker)** — customer_max_liability_amount is capped at the disputed amount for TechWorld (412.88 instead of 500) but left above it for the $47.50 duplicate (50). Both duplicate and incorrect-amount were noticed 4-5 business days before reporting yet get the $50 tier.
  - doc_bank_accounts_bank_accounts_(general)_031: "inform the customer of their liability exposure based on when they noticed the unauthorized activity: - Reported within 2 business days of statement: Maximum liability $50 - Reported within 60 days of statement: Maximum liability $500"
  - tools.py file_debit_card_transaction_dispute_6281 docstring: "customer_max_liability_amount (number): The maximum dollar amount the customer could be liable for based on Regulation E reporting timing rules and the disputed amount. Use -1 for unlimited liability."
  - `No statement dates exist in the DB or the documents; get_now() = 2025-11-14 (Friday)`
  - `gold[14] TechWorld disputed 412.88, liability 412.88 (= min(500, 412.88))`
  - `gold[12] Bella's duplicate disputed 47.5, liability 50 (not min(50, 47.5)); discovery 11/10/2025 -> 4 business days to 11/14`
  - `gold[13] Whole Foods incorrect_amount discovery 11/09/2025 -> 5 business days, liability 50`
  - `Replay: duplicate liability 47.5 -> debit_card_disputes differs`
  - *Why it matters:* Capping at the disputed amount everywhere gives 47.5 for gold[12]. Never capping gives 500 for gold[14]. Counting from discovery gives 500 for gold[12] and gold[13]. No single documented reading reproduces all three gold values.
  - *Fix:* Adopt one rule in doc_031 and the docstring (for example tier by business days from discovery, capped at the disputed amount) and regenerate all three values.
- **non_determinism (Major)** — The two identical Bella's Bistro charges share the date 11/06. The gold disputes the second-listed row, which is right only if the agent infers within-day order from the most-recent-first contract.
  - `doc_bank_accounts_bank_accounts_(general)_031: "Dispute the earliest (first) transaction when multiple duplicates exist."`
  - `doc_bank_accounts_bank_accounts_(general)_018: "Transactions are returned in reverse chronological order (most recent first)."`
  - tools.py get_bank_account_transactions_9173: stable sort by date, reverse=True; same-date rows keep stored order (comment: "identifies the later-listed record as the earlier one")
  - `Tool output for chk_b8d92f4c17 lists btxn_d7f2a98c1b34 before btxn_e8c3b09d2c45, both 11/06/2025 -47.5`
  - `gold[12] transaction_id btxn_e8c3b09d2c45`
  - `Replay: disputing btxn_d7f2a98c1b34 -> debit_card_disputes differs`
  - *Why it matters:* An agent reading 'first' as the first row shown disputes btxn_d7f2a98c1b34 and fails.
  - *Fix:* Give the duplicates distinct timestamps, or state the within-day tie-break explicitly in doc_031.
- **document_contradiction (Major)** — The duplicate charge is set provisional-credit eligible although the customer has not contacted the merchant, which doc_032 lists as 'not required'.
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is REQUIRED when ALL of these conditions are met: ... 2. Dispute Category: ... 'duplicate_charge'"
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is NOT REQUIRED (but may be offered at discretion) when: ... 2. Customer has not contacted merchant first (for non-fraud disputes) 3. Customer shared their PIN voluntarily (pin_compromised = 'yes_shared')"
  - `gold[12] duplicate_charge contacted_merchant false, provisional_credit_eligible true`
  - *Why it matters:* An agent applying the merchant-contact condition stores false and fails debit_card_disputes.
  - *Fix:* Make doc_032's lists mutually exclusive.

*Verifier: Confirmed (Blocker → Blocker).* Reproduced. Always capping at the disputed amount gives 47.5 for gold[12]; never capping gives 500 for gold[14], which is what the task's own notes say. No single rule reproduces both values, so the gold follows no consistent reading: Blocker. Across tasks the gold only ever caps the $500 tier (086: 625 -> 500; 085: 14.99 -> 50 uncapped), so the defect is an undocumented convention rather than a slip.

### task_085 — Major

**The verify-the-customer's-claims test works, but which duplicate gym charge to dispute, the liability amounts, and one provisional-credit flag each depend on a reading the documents do not settle.**

- **non_determinism (Major)** — After v1.0.1 swapped the fixture rows, the gold CityFit duplicate btxn_b2c3d4e5f602 is listed second of two identical 11/06 rows. It is 'earliest' only if the agent infers within-day order from the most-recent-first contract.
  - `doc_bank_accounts_bank_accounts_(general)_031: "Dispute the earliest (first) transaction when multiple duplicates exist."`
  - `doc_bank_accounts_bank_accounts_(general)_018: "Transactions are returned in reverse chronological order (most recent first)."`
  - tools.py get_bank_account_transactions_9173: stable sort by date, reverse=True; same-date rows keep stored order (comment: "identifies the later-listed record as the earlier one")
  - `v1.0.0->v1.0.1 diff swaps stored order of btxn_c3d4e5f6g703 and btxn_b2c3d4e5f602`
  - `Tool output for chk_b4d92f7c28 lists btxn_c3d4e5f6g703 then btxn_b2c3d4e5f602 (both 11/06/2025, -89.99)`
  - `gold[10] transaction_id btxn_b2c3d4e5f602`
  - `Replay: disputing btxn_c3d4e5f6g703 -> verified fails, debit_card_disputes differs`
  - *Why it matters:* An agent reading 'earliest (first)' as the first row shown disputes btxn_c3d4e5f6g703 and fails. Under v1.0.0 the gold row was listed first, so this reading used to pass.
  - *Fix:* Give the duplicates distinct timestamps, or state the within-day tie-break explicitly in doc_031.
- **document_gap (Major)** — All three gold disputes store liability 50. That includes the ATM shortage noticed 11/05 (7 business days before reporting) and the $14.99 Prime Streaming charge, whose liability cannot exceed the charge if the docstring's 'and the disputed amount' is applied.
  - doc_bank_accounts_bank_accounts_(general)_031: "inform the customer of their liability exposure based on when they noticed the unauthorized activity: - Reported within 2 business days of statement: Maximum liability $50 - Reported within 60 days of statement: Maximum liability $500"
  - tools.py file_debit_card_transaction_dispute_6281 docstring: "customer_max_liability_amount (number): The maximum dollar amount the customer could be liable for based on Regulation E reporting timing rules and the disputed amount. Use -1 for unlimited liability."
  - `No statement dates exist in the DB or the documents; get_now() = 2025-11-14 (Friday)`
  - `gold[9] ATM discovery 11/05/2025 -> 7 business days to 11/14, liability 50`
  - `gold[10] duplicate discovery 11/08/2025 -> 5 business days, liability 50`
  - `gold[12] recurring disputed_amount 14.99, liability 50`
  - `Replay: Prime Streaming liability 14.99 -> debit_card_disputes differs`
  - *Why it matters:* An agent applying the discovery-based tier stores 500 for gold[9] and gold[10]. One capping at the disputed amount stores 14.99 for gold[12]. Either fails the exact debit_card_disputes comparison.
  - *Fix:* State one deterministic rule in doc_031, for example: liability tier is counted from the discovery date to today in business days, applies to every dispute category, and is capped at the disputed amount. Then regenerate customer_max_liability_amount in every gold dispute.
- **document_contradiction (Major)** — The CityFit duplicate is set provisional-credit eligible although the customer has not contacted the merchant, which doc_032 lists as 'not required'.
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is REQUIRED when ALL of these conditions are met: ... 2. Dispute Category: ... 'duplicate_charge'"
  - doc_bank_accounts_bank_accounts_(general)_032: "Provisional Credit is NOT REQUIRED (but may be offered at discretion) when: ... 2. Customer has not contacted merchant first (for non-fraud disputes) 3. Customer shared their PIN voluntarily (pin_compromised = 'yes_shared')"
  - `gold[10] duplicate_charge contacted_merchant false, provisional_credit_eligible true`
  - *Why it matters:* An agent applying the merchant-contact condition stores false and fails.
  - *Fix:* Make doc_032's lists mutually exclusive.
- **underspecified_instructions (Minor)** — transaction_type for the CityFit duplicate ('recurring_payment') and contacted_merchant for Prime Streaming (false, although the customer says they cancelled the subscription) are never scripted. The merchant description 'CITYFIT GYM MONTHLY' points to the gold value.
  - `gold[10] transaction_type 'recurring_payment'; DB type 'debit_card_purchase', description 'CITYFIT GYM MONTHLY DENVER'`
  - `gold[12] contacted_merchant false; script: "I cancelled that subscription weeks ago"`
  - *Why it matters:* The simulated user improvises these answers, so an agent that asks may hear something that leads to a different stored value. Most agents reach the gold values from the evidence.
  - *Fix:* Script both answers.

*Verifier: Confirmed (Major → Major).* All three Major issues reproduce. The gold's liability values match a statement-period reading (current-cycle transactions $50), so this is a two-readings case (Major), not a gold with no basis. The tie-break follows doc_018's most-recent-first contract, which a careful agent can deduce but is not stated for same-date rows, so Major (not a Blocker-class undocumented tie).

### task_086 — Major

**The large six-dispute scenario is mostly derivable, but liability amounts, the PIN status after a reported skimming, and the purchase type of the late fraud charge each have more than one defensible answer.**

- **document_gap (Major)** — Four non-fraud disputes noticed 11/07-11/09 and reported 11/14 (5 business days later) store liability 50. Counting from when the customer noticed, doc_031 gives the $500 tier.
  - doc_bank_accounts_bank_accounts_(general)_031: "inform the customer of their liability exposure based on when they noticed the unauthorized activity: - Reported within 2 business days of statement: Maximum liability $50 - Reported within 60 days of statement: Maximum liability $500"
  - tools.py file_debit_card_transaction_dispute_6281 docstring: "customer_max_liability_amount (number): The maximum dollar amount the customer could be liable for based on Regulation E reporting timing rules and the disputed amount. Use -1 for unlimited liability."
  - `No statement dates exist in the DB or the documents; get_now() = 2025-11-14 (Friday)`
  - gold[11] ATM discovery 11/07/2025, gold[12] discovery 11/09/2025, gold[14] discovery 11/09/2025, gold[16] discovery 11/08/2025 -> 5 business days each; all liability 50
  - `gold[15] TechWorld liability 500 (late fraud)`
  - *Why it matters:* An agent applying the discovery-based tier, or treating Reg E tiers as unauthorized-only (0 for errors), stores different values and fails debit_card_disputes.
  - *Fix:* State one deterministic rule in doc_031, for example: liability tier is counted from the discovery date to today in business days, applies to every dispute category, and is capped at the disputed amount. Then regenerate customer_max_liability_amount in every gold dispute.
- **non_determinism (Major)** — For TechWorld the customer says "I think someone skimmed my card", which fits pin_compromised 'yes_observed' ("believes PIN was observed/skimmed"). The gold stores 'unknown'. The gold also stores transaction_type 'pin_purchase', which the script never states.
  - `tool docstring pin_compromised: "'yes_observed': Customer believes PIN was observed/skimmed ... 'unknown': Customer unsure"`
  - `user_scenario: "Still have card - I think someone skimmed my card at a gas station or something."`
  - `gold[15] pin_compromised 'unknown', transaction_type 'pin_purchase'`
  - `Replay: pin_compromised 'yes_observed' -> debit_card_disputes differs`
  - *Why it matters:* An agent that maps 'skimmed' to yes_observed, or records signature_purchase for an unspecified in-store charge, fails the exact comparison.
  - *Fix:* Script the PIN answer ("I don't know if they got my PIN") and the transaction type.
- **underspecified_instructions (Minor)** — The script gives the TechWorld discovery date as "today 01/12" while today is 11/14/2025, and the ATM-deposit claim ($500 deposited, $300 credited against a DB credit of $400) is withdrawn only loosely. The gold stores discovery 11/14/2025 and disputed_amount 100.
  - `user_scenario: "Just discovered today 01/12 during year-end reconciliation."`
  - `gold[15] discovery_date 11/14/2025`
  - user_scenario: "If your records show that, then I'll go with what you have."; btxn_0788d2513c8c amount 400.0; get_atm_deposit_images_8473 returns "IMAGES NOT AVAILABLE"
  - `gold[16] disputed_amount 100.0`
  - *Why it matters:* A careful agent resolves 'today' to 11/14 and confirms $500-$400=$100 with the customer, but a literal or differently confirmed value fails.
  - *Fix:* Fix the date typo and have the customer state the corrected deposit claim explicitly.

*Verifier: Confirmed (Major → Major).* Reproduced. The liabilities are internally consistent (always or never capping gives the same values here), so this is the two-readings Major, not 084's Blocker. Cross-task: this gold maps 'skimmed' to 'unknown', while task_091 maps 'Maybe someone watched me ... I really don't know' to 'yes_observed'. The two golds invert the same mapping, which supports Major on both.

### task_087 — Major

**Fixing three declined cards is well specified, but one security document says to hand the customer to the security team when they report a charge they did not make, which would skip the gold's dispute and replacement.**

- **document_contradiction (Major)** — When the Evergreen customer-initiated fraud alert turns out to cover a real fraudulent charge, doc_039 says to escalate to the security team. The gold instead files a dispute, closes the card, and orders a replacement.
  - `doc_bank_accounts_bank_accounts_(general)_039 'Escalate to security team when': "Customer reports transactions they did not make"`
  - doc_checking_accounts_checking_accounts_(general)_003 CODE 05 step 3: "If fraud_alert_active is TRUE and alert_source is 'customer_initiated' -> Ask customer to verify recent transactions. If they confirm all transactions are legitimate, clear the alert." (silent on the fraud case)
  - `gold[15] file_debit_card_transaction_dispute_6281 card_present_fraud close_and_reissue; gold[17] close fraud_suspected; gold[19] order EXPEDITED PREMIUM`
  - `transfer_to_human_agents writes nothing to the DB`
  - *Why it matters:* An agent that follows doc_039 transfers once the $499.99 charge is denied. The dispute, closure, and replacement never happen, and debit_card_disputes, debit_cards, and debit_card_orders differ from the gold.
  - *Fix:* Add to doc_039 that a customer-initiated alert with a confirmed unauthorized charge is handled through the debit dispute flow (doc_031) rather than escalation, or accept escalation as an alternative path.

*Verifier: Confirmed (Major → Major).* Quotes verified. An agent that escalates on doc_039 before the dispute leaves debit_card_disputes, debit_cards and debit_card_orders unwritten, so two readings lead to different graded states (Major). Escalating after the writes still passes, so this sits at the low end of Major. The liability-50 note gives a stated reason for not flagging the discovery-timing class here, which is acceptable.

### task_088 — Major

**Three decline problems with a reachable gold, but the documents invite an account-to-account transfer the gold does not expect and disagree on freezing versus closing the cloned card, and the purchase type of the fraud charge is never stated.**

- **underspecified_instructions (Major)** — The Green balance ($380.47) is below the $449.99 purchase. The CODE 51 procedure says to offer a transfer from another account, and the customer asks whether anything can be done, but the script has no answer to a transfer offer and the gold has no transfer.
  - doc_checking_accounts_checking_accounts_(general)_006 CODE 51 step 3: "Offer options: 'Would you like to transfer funds from another account, or would you prefer to make a smaller transaction?' If they want to transfer, help them do so."
  - `chk_cec8333d41_green current_holdings 380.47; pending mobile_deposit 3000.0 (11/11/2025)`
  - `user_scenario: "Is there anything I can do? Can I get access to the money sooner?"`
  - `Replay: gold + transfer_funds_between_bank_accounts_7291 -> verified fails (extra discoverable write, accounts differ)`
  - *Why it matters:* A doc-following agent offers the transfer, and a simulated user who needs the tablet for a deadline is likely to accept. The resulting write fails the task through no fault of the agent.
  - *Fix:* Script the customer's answer to a transfer offer (decline), or include the transfer in the gold.
- **document_contradiction (Major)** — For an undamaged card with a chip/CVV mismatch and a fraud charge, CODE 82 says to follow the 'stolen card protocol' and to recommend freezing until the replacement arrives, while the dispute mapping requires close_and_reissue. The gold closes with reason fraud_suspected.
  - doc_checking_accounts_purple_account_007 CODE 82: "If suspicious transactions found: Follow stolen card protocol to assist the customer. Recommend freezing the card until a replacement arrives."
  - `doc_031: "'card_present_fraud' -> 'close_and_reissue'"`
  - `gold[12] close_debit_card_4721 reason 'fraud_suspected'`
  - `Replay: closing as 'stolen' -> debit_cards differs (closure_reason, new card issue_reason 'stolen' vs 'fraud')`
  - *Why it matters:* An agent that closes as 'stolen' per the 'stolen card protocol' wording, or freezes instead of closing, stores a different card state and fails.
  - *Fix:* Change CODE 82 to say: file a card_present_fraud dispute, then close the card with reason fraud_suspected and order a replacement.
- **underspecified_instructions (Major)** — The gold records the Miami fraud charge as transaction_type 'signature_purchase', but neither the script nor the data says how it was made.
  - `gold[10] transaction_type 'signature_purchase'`
  - `btxn_28eee7145c29 type 'debit_card_purchase', description 'ELECTRO MART MIAMI FL'`
  - `doc_031 transaction_type: "Determine from user circumstances"; script has no answer`
  - *Why it matters:* An agent recording pin_purchase, or asking and getting an improvised answer, fails debit_card_disputes.
  - *Fix:* Script the transaction type or add it to the transaction record.
- **underspecified_instructions (Minor)** — Part 2's opening line says to raise the stolen-card issue "after the check hold issue is explained", while the part header puts it after Part 1.5. Raising it before the chip-error issue leads to a transfer that ends the call before the Evergreen dispute.
  - `user_scenario Part 2 header: "Transition after Part 1.5 is resolved"`
  - `user_scenario Part 2 item 12: "After the check hold issue is explained, bring up the second issue"`
  - `gold[16] transfer_to_human_agents is last`
  - *Why it matters:* The outcome depends on which ordering the simulated user follows. The headers favour the gold ordering.
  - *Fix:* Fix the Part 2 transition sentence.

*Verifier: Confirmed (Major → Major).* All quotes and DB values check out. The unscripted transfer offer and transaction type have no documented default, so Major per calibration. One mitigating point: pin_compromised 'no' makes signature_purchase the more inferable value, but the issue still stands. The Evergreen order is scripted and clean.

### task_091 — Blocker

**For the Evergreen and Light Blue replacements the gold ignores the tier rules: it orders standard shipping and design when the customer asked for the most premium free option, and it orders a Light Blue replacement immediately despite the 48-hour wait. Several other choices are also left open.**

- **argument_error (Blocker)** — The customer asks for 'the most premium free option for both' on the Evergreen replacement. Evergreen is PREMIUM tier, where EXPEDITED shipping and the PREMIUM design both cost $0, yet the gold orders STANDARD with CLASSIC. Sibling task_090's gold charges $0 for EXPEDITED on Evergreen, which is only valid under the same Premium-tier rule.
  - `user_scenario line 20: "I want the most premium free option for both."`
  - doc_bank_accounts_bank_accounts_(general)_029: "When using order_debit_card_5739, you must provide the exact delivery_fee and design_fee amounts based on the tier rules below."
  - doc_bank_accounts_bank_accounts_(general)_029 PREMIUM TIER: "Free expedited shipping on all replacements (delivery_fee: $0 for both STANDARD and EXPEDITED)" and "PREMIUM design (metallic silver): design_fee $0 (complimentary)"
  - `doc_bank_accounts_bank_accounts_(general)_005: "PREMIUM TIER (Evergreen Account)"`
  - `gold[14].arguments: delivery_option "STANDARD", card_design "CLASSIC"`
  - `task_090 gold[10]: Evergreen order with delivery_option "EXPEDITED", delivery_fee 0`
  - `Replay: EXPEDITED+PREMIUM changes debit_card_orders and debit_cards (verified match False)`
  - *Why it matters:* An agent that applies the tier table it is told to use orders EXPEDITED/PREMIUM and fails. The gold matches only an agent that never looks up Evergreen's tier and falls back to doc_bank_accounts_bank_accounts_(general)_023's generic fees, and that doc itself says 'fees may vary based on account tier'.
  - *Fix:* Change gold[14] to EXPEDITED/PREMIUM with $0 fees, or change the customer's request to 'the standard free option'.
- **argument_error (Major)** — The gold orders a Light Blue (ENTRY tier) replacement right after closing the card, but the ENTRY-tier rules impose a 48-hour wait between closure and replacement.
  - `doc_bank_accounts_bank_accounts_(general)_029 ENTRY TIER: "48-hour waiting period after card closure before a replacement can be ordered"`
  - `doc_bank_accounts_bank_accounts_(general)_005: "ENTRY TIER (Light Blue Account, Light Green Account, Green Fee-Free Account)"`
  - `gold[23] close_debit_card_4721 dbc_tw34a7d9e2_lightblue, then gold[24] order_debit_card_5739 chk_tw34a7d9e2_lightblue in the same conversation`
  - `Replay: gold without gold[24] changes debit_card_orders and debit_cards`
  - *Why it matters:* An agent that follows the tier rules (which the Evergreen order needs anyway) tells the customer to wait 48 hours and places no order, so the DB differs from the gold.
  - *Fix:* Remove gold[24] (and have the agent explain the 48-hour wait), or move the Light Blue card to a tier with no waiting period.
- **non_determinism (Major)** — The Light Blue card scores VERY HIGH (cannot unlock). Step 6 then offers closure plus replacement, a transfer to security, or a PIN reset, and the customer script accepts each one. Closure is only 'recommended if fraud suspected', but the customer confirms the Bellevue attempts were his. The gold picks closure with reason fraud_suspected.
  - doc_bank_accounts_bank_accounts_(general)_041 STEP 6: "Card closure and replacement (recommended if fraud suspected)" / "Transfer to security team for investigation" / "PIN reset (issues new PIN, invalidates potential compromise)"
  - user_scenario 41: "Yes, that was definitely me."; 44: "Fine, close it and send me a new one."; 45: "Ugh, okay... I guess I can wait"; 47: "Sure, set it to 4121."
  - `gold[23].arguments.reason = "fraud_suspected"`
  - `Replay: transfer only (no gold[23]/[24]) fails; a reset would leave the card ACTIVE and unlocked`
  - *Why it matters:* Transferring to security is at least as defensible when fraud is not suspected, and it writes nothing, so the gold's closure and order are missing.
  - *Fix:* Give a tie-breaker for VERY HIGH scores with no unauthorized transactions (e.g. 'offer transfer to security; do not close'), and align the gold and script with it.
- **argument_error (Major)** — Both disputes record pin_compromised 'yes_observed', but the customer says he is unsure, which is exactly how the doc defines 'unknown'.
  - `user_scenario 22: "I never shared it with anyone. Maybe someone watched me at an ATM? I really don't know."`
  - `doc_bank_accounts_bank_accounts_(general)_031: "'yes_observed': Customer believes PIN was observed/skimmed" / "'unknown': Customer unsure"`
  - `gold[16], gold[17] arguments.pin_compromised = "yes_observed"`
  - `Replay: pin_compromised 'unknown' changes debit_card_disputes`
  - *Why it matters:* pin_compromised is stored in the dispute record, so 'unknown', a literal reading of the customer's answer, fails.
  - *Fix:* Change the script to a clear belief ('I think someone watched me enter it') or change the gold to 'unknown'.
- **argument_error (Minor)** — The customer script gives DOB 09/22/1991, but the DB and the stated age 24 imply 09/22/2001. Verification still passes on 2 of 4 fields, and the gold logs the DB value.
  - `user_scenario: "DOB: 09/22/1991" and "a 24-year-old"`
  - `initial_state users.tw34a7d9e2.date_of_birth = "09/22/2001"`
  - `gold[0].arguments.date_of_birth = "09/22/2001"`
  - `Replay: logging 09/22/1991 changes verification_history`
  - *Why it matters:* An agent that logs the DOB the customer stated fails, and a cautious agent may treat the mismatch as a verification red flag.
  - *Fix:* Change the script DOB to 09/22/2001.
- **document_gap (Minor)** — The Green card scores LOW ('Unlock after standard identity verification'), but no unlock tool exists. The only way to clear pin_locked is reset_debit_card_pin_6284, which the docs describe as a forgotten-PIN reset, and this customer says he knows his PIN.
  - `doc_bank_accounts_bank_accounts_(general)_041: "0-4 | LOW | Unlock after standard identity verification"`
  - `doc_bank_accounts_bank_accounts_(general)_027: "PIN Reset Steps (Customer Forgot PIN)"`
  - `tools.py reset_debit_card_pin_6284 sets card["pin_locked"] = False`
  - `user_scenario 8: "Yeah, I know my PIN."; 10: "Sure, if you think that's best. Set it to 2589."`
  - *Why it matters:* Most agents will offer a reset, which the customer accepts. An agent that looks for an unlock path and finds none may leave the card locked.
  - *Fix:* Document that a PIN reset is how chat agents clear a PIN lock, or add an unlock tool.

*Verifier: Upgraded (Blocker → Blocker).* Task-level severity unchanged; one issue is under-rated. The immediate Light Blue reorder contradicts an unconditional ENTRY-tier rule that sibling golds (080) and notes (084) obey. Like the Evergreen order, it comes from the gold being built without doc_005's tier mapping, so it should be Blocker-class, not Major. The other issues (pin_compromised, step-6 option choice, DOB, unlock-by-reset) reproduce as rated.

### task_093 — Major

**The Silver interest correction ($33.00) is derivable, but the documented daily compounding does not match the system's simple monthly interest, and the discrepancy report's content is never graded.**

- **document_contradiction (Minor)** — The docs say interest compounds daily from a daily periodic rate, but every seeded interest credit equals balance x APY / 12 exactly, and the gold credit uses that simple monthly convention. The data settles it, but an agent that follows the documented daily compounding computes a different credit.
  - doc_savings_accounts_silver_account_006: "Interest accrues on your daily balance and is compounded daily. We calculate a daily periodic rate from your APY and apply it to the balance for each day of the cycle."
  - `txn_int_oct_2025_silver amount 480.0 = 144000 x 4.0% / 12`
  - `gold[6].arguments.amount = 33.00 = 144000 x 0.275% / 12`
  - `daily compounding over 31 days: 144000 x ((1.04275)^(31/365) - 1) = 512.88, so 32.88`
  - *Why it matters:* The credit amount is stored (accounts.current_holdings and the credit transaction id/amount), so a daily-compounding computation fails.
  - *Fix:* State in the interest docs that monthly interest = balance x APY / 12, or seed credits that match daily compounding.
- **grading_basis_mismatch (Minor)** — submit_interest_discrepancy_report_7294 writes to an 'interest_discrepancy_reports' table that TransactionalDB does not have. add_to_db returns False silently while the tool reports success, so only the tool name is graded and expected_apy/actual_apy/amount_difference are never compared.
  - `db_query.py add_to_db: "table = getattr(db, db_name, None)" / "if table is None: return False"`
  - `tools.py submit_interest_discrepancy_report_7294: add_to_db("interest_discrepancy_reports", ...) with return value ignored`
  - `Replay: model_dump() of the gold DB has no interest_discrepancy_reports key; changing expected_apy alone changes no table`
  - *Why it matters:* A report with a wrong expected or actual APY still passes; the task tests less than its notes claim.
  - *Fix:* Add interest_discrepancy_reports to TransactionalDB so the report is persisted and graded.

*Verifier: Upgraded (Minor → Major).* The arithmetic ($33.00) and the two Minor issues reproduce. The review rates 097 Major because its gold follows the 'may qualify / Platinum-linked only' reading. That same reading is a document-supported alternative here and gives $30.00, so the pair of readings is identical across 093 and 097. An agent applying either one consistently fails one of the two tasks. Per calibration, two document-supported readings with different graded states is Major in both.

### task_094 — Major

**Whether the Gold Rewards Card's +0.025% stacks on top of the EcoCard bonus is ambiguous in the docs, so the $140.00 correction is one of two defensible answers.**

- **document_contradiction (Major)** — The Gold Rewards Card's 0.025% appears twice. doc_013 calls it a relationship bonus on top of the base rate, and doc_bank_accounts_bank_accounts_(general)_045 says credit card bonuses DO stack with relationship bonuses; doc_014 and doc_bank_accounts_bank_accounts_(general)_045's own example list the same 0.025% as a credit card bonus that loses to EcoCard. The gold drops it (EcoCard 0.6% only).
  - `doc_savings_accounts_gold_account_013: "you receive an additional 0.025% relationship bonus APY on top of the base rate"`
  - doc_bank_accounts_bank_accounts_(general)_045: "credit card APY bonuses DO stack with other types of bonuses, such as: ... Relationship bonuses for holding multiple Rho-Bank products"
  - `doc_savings_accounts_gold_account_014: "| Gold Rewards Card | +0.025% |"`
  - doc_bank_accounts_bank_accounts_(general)_045 example: "Gold Rewards Card: +0.025% APY bonus / Platinum Rewards Card: +0.15% APY bonus / EcoCard: +0.6% APY bonus -> The customer receives only the EcoCard bonus of +0.6%"
  - `gold expected_apy 6.85, credit $140.00; with the 0.025% stacked: 6.875% and $142.00 on $96,000`
  - `Replay: the stacked alternative changes accounts and bank_account_transaction_history`
  - *Why it matters:* An agent that treats doc_013's bonus as a separate relationship bonus (a reading doc_bank_accounts_bank_accounts_(general)_045's stacking list supports) credits a different amount and fails.
  - *Fix:* Rewrite doc_013 to say the 0.025% is the Gold Rewards Card credit-card APY bonus from doc_014 (subject to highest-only stacking), or make the gold include it.
- **document_contradiction (Minor)** — The docs say interest compounds daily from a daily periodic rate, but every seeded interest credit equals balance x APY / 12 exactly, and the gold credit uses that simple monthly convention. The data settles it, but an agent that follows the documented daily compounding computes a different credit.
  - `doc_savings_accounts_gold_account_003: "Interest is compounded daily."`
  - `btxn_8765c2cc9c02 amount 408.0 = 96000 x 5.1% / 12`
  - `gold[6].arguments.amount = 140.00 = 96000 x 1.75% / 12`
  - `daily compounding: 96000 x ((1.0685)^(31/365) - 1) - 408 = 133.73`
  - *Why it matters:* The credit amount is stored (accounts.current_holdings and the credit transaction id/amount), so a daily-compounding computation fails.
  - *Fix:* State in the interest docs that monthly interest = balance x APY / 12, or seed credits that match daily compounding.
- **grading_basis_mismatch (Minor)** — submit_interest_discrepancy_report_7294 writes to an 'interest_discrepancy_reports' table that TransactionalDB does not have. add_to_db returns False silently while the tool reports success, so only the tool name is graded and expected_apy/actual_apy/amount_difference are never compared.
  - `db_query.py add_to_db: "table = getattr(db, db_name, None)" / "if table is None: return False"`
  - `tools.py submit_interest_discrepancy_report_7294: add_to_db("interest_discrepancy_reports", ...) with return value ignored`
  - `Replay: model_dump() of the gold DB has no interest_discrepancy_reports key; changing expected_apy alone changes no table`
  - *Why it matters:* A report with a wrong expected or actual APY still passes; the task tests less than its notes claim.
  - *Fix:* Add interest_discrepancy_reports to TransactionalDB so the report is persisted and graded.

*Verifier: Confirmed (Major → Major).* Reproduced. doc_045's example favours the gold, but doc_013 explicitly labels the same 0.025% a relationship bonus, and doc_045 says relationship bonuses stack. Major matches task_095 on identical documents. The daily-compounding and unpersisted-report Minors also reproduce.

### task_095 — Major

**As in task_094, the docs disagree on whether the Gold Rewards Card's +0.025% stacks, so the $98.00 correction is one of two defensible answers.**

- **document_contradiction (Major)** — The Gold Rewards Card's 0.025% appears twice. doc_013 calls it a relationship bonus on top of the base rate, and doc_bank_accounts_bank_accounts_(general)_045 says credit card bonuses DO stack with relationship bonuses; doc_014 and doc_bank_accounts_bank_accounts_(general)_045's own example list the same 0.025% as a credit card bonus that loses to EcoCard. The gold drops it (EcoCard 0.6% only).
  - `doc_savings_accounts_gold_account_013: "you receive an additional 0.025% relationship bonus APY on top of the base rate"`
  - doc_bank_accounts_bank_accounts_(general)_045: "credit card APY bonuses DO stack with other types of bonuses, such as: ... Relationship bonuses for holding multiple Rho-Bank products"
  - `doc_savings_accounts_gold_account_014: "| Gold Rewards Card | +0.025% |"`
  - doc_bank_accounts_bank_accounts_(general)_045 example: "Gold Rewards Card: +0.025% APY bonus / Platinum Rewards Card: +0.15% APY bonus / EcoCard: +0.6% APY bonus -> The customer receives only the EcoCard bonus of +0.6%"
  - `gold expected_apy 6.85, credit $98.00; with the 0.025% stacked: 6.875% and $100.00 on $96,000`
  - `Replay: the stacked alternative changes accounts and bank_account_transaction_history`
  - *Why it matters:* An agent that treats doc_013's bonus as a separate relationship bonus (a reading doc_bank_accounts_bank_accounts_(general)_045's stacking list supports) credits a different amount and fails.
  - *Fix:* Rewrite doc_013 to say the 0.025% is the Gold Rewards Card credit-card APY bonus from doc_014 (subject to highest-only stacking), or make the gold include it.
- **document_contradiction (Minor)** — The docs say interest compounds daily from a daily periodic rate, but every seeded interest credit equals balance x APY / 12 exactly, and the gold credit uses that simple monthly convention. The data settles it, but an agent that follows the documented daily compounding computes a different credit.
  - `doc_savings_accounts_gold_account_003: "Interest is compounded daily."`
  - `btxn_9a76d3ee8b01 amount 450.0 = 96000 x 5.625% / 12`
  - `gold[6].arguments.amount = 98.00 = 96000 x 1.225% / 12`
  - `daily compounding: 541.73 - 450 = 91.73`
  - *Why it matters:* The credit amount is stored (accounts.current_holdings and the credit transaction id/amount), so a daily-compounding computation fails.
  - *Fix:* State in the interest docs that monthly interest = balance x APY / 12, or seed credits that match daily compounding.
- **grading_basis_mismatch (Minor)** — submit_interest_discrepancy_report_7294 writes to an 'interest_discrepancy_reports' table that TransactionalDB does not have. add_to_db returns False silently while the tool reports success, so only the tool name is graded and expected_apy/actual_apy/amount_difference are never compared.
  - `db_query.py add_to_db: "table = getattr(db, db_name, None)" / "if table is None: return False"`
  - `tools.py submit_interest_discrepancy_report_7294: add_to_db("interest_discrepancy_reports", ...) with return value ignored`
  - `Replay: model_dump() of the gold DB has no interest_discrepancy_reports key; changing expected_apy alone changes no table`
  - *Why it matters:* A report with a wrong expected or actual APY still passes; the task tests less than its notes claim.
  - *Fix:* Add interest_discrepancy_reports to TransactionalDB so the report is persisted and graded.

*Verifier: Confirmed (Major → Major).* Same contradiction as task_094, with checking-boost selection (Green 0.75 over Purple 0.1) correct per doc_046. The figures reproduce and severity holds.

### task_097 — Major

**The Silver account's gold correction leaves out the documented +0.025% multi-product relationship bonus that the near-identical task_093 includes, so a doc-following agent credits $222.92 instead of $220.84.**

- **argument_error (Major)** — The Silver expected APY in the gold is 6.65% (4.0 + Bluest 0.45 + EcoCard 2.2) and omits the 0.025% relationship bonus. That bonus is described in a required document, and task_093's gold applies it to a customer with only two products, while this customer holds thirteen.
  - doc_savings_accounts_silver_account_002 (required): "If you maintain multiple Rho-Bank products, you may also qualify for a relationship bonus of 0.025% that stacks on top of your base Silver APY."
  - `doc_savings_accounts_silver_account_005: "Eligible customers receive a relationship APY bonus of 0.025% added to the base Silver APY."`
  - doc_bank_accounts_bank_accounts_(general)_044: "Missing Relationship Bonus: Customer maintains multiple Rho-Bank products but the relationship bonus was not applied."
  - `task_093 gold expected_apy 4.275 = 4.0 + 0.25 + 0.025`
  - `gold[9].arguments.amount = 220.84; gold[14].expected_apy = 6.65`
  - `Replay: 6.675% and $222.92 changes accounts and bank_account_transaction_history`
  - *Why it matters:* An agent that applies the bonus the way task_093 requires credits $222.92 and fails. The gold is supported only by the hedge 'may also qualify', or by reading silver_account_009 (a Platinum-Rewards-linked 0.025%) as the sole route, and this customer has no Platinum Rewards Card.
  - *Fix:* Make the gold 6.675% / $222.92 (consistent with task_093), or define relationship-bonus eligibility so it clearly excludes this customer.
- **non_determinism (Minor)** — The gold Silver credit $220.84 = round(100000 x 6.65%/12, 2) - 333.33 (expected interest minus the credited amount). The equally common shortcut, balance x APY difference / 12 = 100000 x 2.65%/12 = 220.833, rounds to $220.83.
  - `btxn_silver_interest_oct amount 333.33`
  - `554.1667 rounds to 554.17, and 554.17 - 333.33 = 220.84; 100000 x 0.0265 / 12 = 220.83`
  - `Replay: amount 220.83 changes accounts and bank_account_transaction_history`
  - *Why it matters:* A one-cent difference in the stored credit fails the DB comparison.
  - *Fix:* Seed balances that give whole-cent results, or say in doc_bank_accounts_bank_accounts_(general)_044 to compute expected interest minus credited interest.
- **document_contradiction (Minor)** — The docs say interest compounds daily from a daily periodic rate, but every seeded interest credit equals balance x APY / 12 exactly, and the gold credit uses that simple monthly convention. The data settles it, but an agent that follows the documented daily compounding computes a different credit.
  - `doc_savings_accounts_silver_account_006: "We calculate a daily periodic rate from your APY and apply it to the balance for each day of the cycle."`
  - `each seeded October credit equals balance x applied APY / 12 (333.33, 379.17, 750.0, 67.5)`
  - `daily compounding gives 214.98, 60.46, 55.92, 11.62 instead of 220.84, 67.08, 70.00, 12.00`
  - *Why it matters:* The credit amount is stored (accounts.current_holdings and the credit transaction id/amount), so a daily-compounding computation fails.
  - *Fix:* State in the interest docs that monthly interest = balance x APY / 12, or seed credits that match daily compounding.
- **grading_basis_mismatch (Minor)** — submit_interest_discrepancy_report_7294 writes to an 'interest_discrepancy_reports' table that TransactionalDB does not have. add_to_db returns False silently while the tool reports success, so only the tool name is graded and expected_apy/actual_apy/amount_difference are never compared.
  - `db_query.py add_to_db: "table = getattr(db, db_name, None)" / "if table is None: return False"`
  - `tools.py submit_interest_discrepancy_report_7294: add_to_db("interest_discrepancy_reports", ...) with return value ignored`
  - `Replay: model_dump() of the gold DB has no interest_discrepancy_reports key; changing expected_apy alone changes no table`
  - *Why it matters:* A report with a wrong expected or actual APY still passes; the task tests less than its notes claim.
  - *Fix:* Add interest_discrepancy_reports to TransactionalDB so the report is persisted and graded.

*Verifier: Confirmed (Major → Major).* Reproduced all four credits: 67.08, 70.00 and 12.00 match. Silver diverges as described. 554.1667 - 333.33 = 220.8367 -> 220.84, while 100000 x 2.65%/12 -> 220.83. Doc_044 step 6's 'discrepancy between expected and actual interest' favours the gold's method, so Minor for the rounding point is acceptable. Major holds, and task_093 should match it (see that verdict).

### task_101 — Major

**The gold (Vikram to Purple, TechFlow to Sky Blue) follows the docs' 2-per-9-days referral limit, though the limit's wording mixes 'bonuses received' with 'referrals made'.**

- **document_contradiction (Minor)** — The rolling-window rule is worded in terms of 'referral bonuses' received, which could be read as limiting payouts rather than new submissions. Read that way, all four referrals could be submitted now. The FAQ answers 'How many people can I refer at once?' with the 2-per-9-days cap and warns that extra referrals are auto-denied, which supports the gold's two submissions.
  - doc_bank_accounts_bank_accounts_(general)_047: "You can receive at most 2 referral bonuses in any rolling 9-day window." / "If you attempt to receive more than 2 referrals in a single 9-day period, the third referral (and any subsequent referrals in that window) will be automatically denied."
  - doc_bank_accounts_bank_accounts_(general)_048: "How many people can I refer at once? You can have multiple referrals in progress, but you can only receive a maximum of 2 referral bonuses in any rolling 9-day window. If you exceed this limit, additional referrals will be automatically denied"
  - `seed referrals: most recent COMPLETE 10/25/2025, none in the last 9 days`
  - `Replay: submitting all four (adding Green Fee-Free and Lime Green) changes referrals`
  - *Why it matters:* An agent that reads the cap as payout-only recommends all four referrals, and the customer submits them (script line 17), so the run fails. The FAQ's auto-denial warning makes that the weaker reading.
  - *Fix:* Say explicitly that at most 2 new referrals may be submitted per rolling 9-day window, counting referrals already received in that window.

*Verifier: Upgraded (Minor → Major).* Recommendations reproduce: Vikram -> Purple $80 and TechFlow -> Sky Blue $400 (Sky Blue 7/8, under 4 years since formation, $10,000 deposit; Ember is 5 years old). However, doc_047/048 support both a submission cap and a bonus-receipt cap. Under the receipt reading an agent can endorse submitting all four, and the script then submits four. Two document-supported readings with different graded states is Major per calibration, not Minor. The prior Blocker overstated it, because the gold does follow a supported reading.

### task_102 — Major

**With one referral slot open, the customer asks to 'maximize the bonus'. Ember to Lime Green pays her more ($200), while the gold's TechFlow to Sky Blue pays more only in combined terms ($400).**

- **underspecified_instructions (Major)** — Line 12 asks which single referral maximizes 'the bonus' without saying whose. The referrer's own bonus favors Ember to Lime Green ($200 against Sky Blue's $150), and the combined bonus favors TechFlow to Sky Blue ($400 against $350). The gold assumes combined, which only the sibling task_101's script states.
  - `user_scenario 12: "Okay, so if I can only do one right now, which one should I prioritize? I want to maximize the bonus."`
  - `doc_business_checking_accounts_lime_green_003: "**Your bonus**: $200 ... **Their bonus**: $150 ... Referred business must deposit $15,000"`
  - `doc_business_checking_accounts_sky_blue_001: "Your bonus: $150 for each successful referral / Their bonus: $250 welcome bonus"`
  - `gold[2] submit_referral account_type "Sky Blue Account"`
  - `Replay: Lime Green Account instead changes referrals`
  - *Why it matters:* A competent agent optimizing the customer's own payout recommends Ember to Lime Green, the customer submits it, and the DB fails. The NL assertion (TechFlow, not Ember, for Sky Blue) can still pass.
  - *Fix:* Change line 12 to 'maximize the combined bonus for both of us', matching task_101.
- **document_contradiction (Minor)** — This task shares the window-wording issue from task_101. Under the submission-count reading, the 11/10 Purple referral leaves one slot; under a payout-only reading, more could be submitted, since the 11/10 bonus ages out before any new referral pays.
  - `doc_bank_accounts_bank_accounts_(general)_047: "You can receive at most 2 referral bonuses in any rolling 9-day window."`
  - `doc_bank_accounts_bank_accounts_(general)_048: "If you exceed this limit, additional referrals will be automatically denied"`
  - `seed referrals ref_recent_purple_001 COMPLETE 11/10/2025`
  - *Why it matters:* An agent that reads the cap as payout-only may let the customer submit several referrals (script line 13), which fails.
  - *Fix:* State that the cap limits new referral submissions per rolling 9-day window.

*Verifier: Upgraded (Major → Major).* Task-level Major holds: by referrer bonus, Ember -> Lime Green ($200) wins, while the combined bonus gives the gold's Sky Blue ($400). The secondary rolling-window issue is the same two-readings defect as task_101 and should be Major there too, not Minor (one issue under-rated; task severity unchanged).

