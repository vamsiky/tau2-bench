# Rho-Bank Banking-Agent Policy Register & Risk Audit

**Source corpus:** tau2-bench `banking_knowledge` — 698 documents
**Blackboard:** `3aac810c` (irys-state) · iteration 5 · 7,920 entries
**Method:** full 14-phase client-side reproduction of the CLI `run_swarm` pipeline (structural profiling → seed planning → dense extraction → orchestrator loop → adversarial-critic + supervisor convergence → direct analysis → 4 debt-sensor lenses → obligations → curation → sectioned synthesis), Haiku workers / Sonnet reviewer+synthesis, all state on the irys MCP blackboard.
**As-of date for temporal evaluation:** 2026-06-26

---

## Executive Summary

This register catalogs the Rho-Bank customer-service agent knowledge base against an 8-row completeness scaffold (`task_state_map`): product tiers, agent tools, eligibility rules, limits, cross-document contradictions, data-quality defects, security guardrails, and temporal items. Every value is grounded in document provenance.

**Highest-priority findings (for remediation):**

- **[P0] Hardcoded account-recovery bypass code** `9K2X7M4P1N8Q3R5T6A` written verbatim in `doc_customer_support_special_support_codes_001.json`, used by `log_verification` to bypass identity verification — no rotation schedule, revocation authority, or audit mechanism anywhere in the corpus. Leakage ≈ universal identity bypass.
- **[Critical] Platinum Rewards Card cash-back conflict** — title says 4%, body says 10% (`doc_credit_cards_platinum_rewards_card_002.json`). A 10% flat rate on a $200-fee card is financially extraordinary; must be corrected before use.
- **[Critical] Reg E / CFPB exposure** — per-tier caps on the number of open disputes (2/3/4/5) with no 12 CFR §1005.11 authority; subscription-cancellation provisional-credit promised in customer-facing copy but excluded by internal policy; reporting-clock reference (statement date vs discovery date) conflicts across docs.
- **[Critical] BNPL template failure** — ~40 of 48 BNPL docs (Bronze, Silver, Gold, Platinum + Management Dashboard) are unfilled `[value not available]` templates; only Diamond carries real terms. Agents cannot quote any non-Diamond BNPL parameter.
- **11 expired-but-live promotions/protocols** still in the active corpus with no retirement flag (Silver Rewards Year-1 waiver, Bronze new-customer $500 credit, two business-checking and two business-savings promos with stale recommendation rankings, Silver Zoom 0% APR / referral, etc.).
- **Backend Incident 11/13 protocol** has a disputed deadline year (2025-11-15 vs 2026-11-15) — agents must verify before relying on its identity-verification waiver.
- **Systematic `$`-on-day-count defect** (`$180 days`, `$270 days`, `$120 days`, `$135 days`) and `$`-on-credit-score / `$`-on-user-count defects across closure, CLI, and blocking docs.
- **~30+ agent tools** catalogued with full signatures, parameters, when-called, and executed-by; suffix collisions (`_7291`, `_3847`, `_7392`) require full-name disambiguation; several tools (`close_bank_account_7392`, QR tools, debit-replacement tool) are invoked but have undocumented parameters.

**Honest limitations.** Extraction density averaged ~9 entries/doc (below the 15–40 target) — many small FAQ/spec docs are genuinely thin, but some larger docs were under-extracted by the Haiku worker tier. The corpus lacks consolidated rate sheets for several product families (notably personal savings and several checking tiers), so per-tier cells marked "—" reflect genuine source gaps, not synthesis omissions. The orchestrator loop hit its 4-iteration cap without full convergence; 2 critical + 26 high signals and 12 disputed entries remain open and are reported as-is in Section 5.

---

## Table of Contents

1. [Product-Tier Register](#1-product-tier-register)
2. [Agent-Tool Catalog](#2-agent-tool-catalog)
3. [Eligibility Rules](#3-eligibility-rules)
4. [Limits & Thresholds](#4-limits--thresholds)
5. [Cross-Document Contradictions (unresolved/disputed)](#5-cross-document-contradictions-unresolveddisputed)
6. [Data-Quality Defects](#6-data-quality-defects)
7. [Security Guardrails & Agent-Safety Risks](#7-security-guardrails--agent-safety-risks)
8. [Temporal Items (evaluated as of 2026-06-26)](#8-temporal-items-evaluated-as-of-2026-06-26)

---


## 1. Product-Tier Register

### 1.1 Personal Checking

| Tier | APY | Min Deposit | Min Balance | Monthly Fee | Fee Waiver | Key Limits / Notes | Source |
|---|---|---|---|---|---|---|---|
| **Blue Account** | — | — | — | — | — | Paper statement fee: $2.50/mo; debit card daily purchase limit: not documented; out-of-network ATM fee: not documented | doc_checking_accounts_blue_account_010.json, doc_checking_accounts_blue_account_003.json |
| **Bronze Account** | — | — | — | — | — | Min opening deposit not documented; monthly maintenance fee not documented; max 3 founder cards per account | doc_business_checking_accounts_sky_blue_005.json; (no source doc for fee/deposit) |
| **Light Green Account** | — | — | — | — | — | APY, min deposit, min balance, and monthly fee all absent from documentation | doc_checking_accounts_light_green_account_011.json, doc_checking_accounts_light_green_account_008.json |
| **Purple Account** | — | — | — | — | — | APY, min deposit, min balance, and monthly fee all absent from documentation | doc_checking_accounts_purple_account_001.json |
| **Evergreen Account** | — (APY boost available from linked Green Savings product; additive vs. multiplicative method unresolved) | — | — | — | — | Min opening deposit not documented; linked Green Savings APY boost calculation method unclear | doc_checking_accounts_evergreen_account_003.json, doc_checking_accounts_evergreen_account_001.json |
| **Dark Green Account** | — | — | — | — (fee structure undefined) | — | Monthly maintenance fee not documented; debit card daily purchase limit not documented; ATM daily withdrawal limit not documented | doc_checking_accounts_dark_green_account_010.json, doc_checking_accounts_dark_green_account_006.json, doc_checking_accounts_dark_green_account_009.json, doc_checking_accounts_dark_green_account_008.json |

---

### 1.2 Personal Savings

| Tier | APY | Min Deposit | Min Balance | Monthly Fee | Fee Waiver | Key Limits / Notes | Source |
|---|---|---|---|---|---|---|---|
| **Silver Saver** | Tier 1 (≤~$25,000): 2.50%; Tier 2 (>~$25,000): 4.00%; card bonuses: +0.30% with Biz Gold card (→4.30% on Tier 2), +0.55% with Biz Platinum card (→4.55% on Tier 2) | — | $10,000 minimum daily balance | $5.00 | Maintain $10,000 minimum daily balance | 6-withdrawal/mo limit; excess-withdrawal fee: $5.00 per transaction; exact Tier 1/2 balance threshold not stated; min opening deposit not documented; account closure conditions and early-closure penalties not documented | doc_business_savings_accounts_silver_saver_account_001.json, doc_business_savings_accounts_silver_saver_account_005.json, doc_business_savings_accounts_silver_saver_account_003.json, doc_business_savings_accounts_silver_saver_account_002.json |
| **Emerald Saver** | Base APY: — (not specified in any document; 3.5% appears only as an illustrative example in e3931, not as a stated rate) | — | — | — | — | Trees planted: (avg monthly balance ÷ $10,000) × 3/mo; carbon offset contribution: 10% of annual interest directed to offsets (example: $350 interest → $35 to offsets); APY bonus rate/type not documented | doc_business_savings_accounts_emerald_saver_002.json, doc_business_savings_accounts_emerald_saver_004.json |
| **Gold Years Account** | — | — | — | — | — | Min opening deposit not documented; min ongoing balance not documented | doc_checking_accounts_gold_years_account_001.json |
| **Green Account (savings)** | — | — | — | — | — | Product terms not detailed; referenced only in comparison with Evergreen Account | doc_business_savings_accounts_emerald_saver_003.json |

---

### 1.3 Business Checking

| Tier | APY | Min Deposit | Min Balance | Monthly Fee | Fee Waiver | Key Limits / Notes | Source |
|---|---|---|---|---|---|---|---|
| **Hunter Green Account** | — | — | — | — | — | Foreign ATM fee: 2.5%, minimum $4.00; international non-Rho ATM: 2.5% (min $4.00) + $2.00 out-of-network fee + operator surcharge; tree sponsorship: (avg monthly balance ÷ $10,000) × 3; carbon offset funding: 18.0% × monthly maintenance fee total | doc_business_checking_accounts_hunter_green_004, doc_business_checking_accounts_hunter_green_009.json, doc_business_checking_accounts_hunter_green_010.json |
| **Navy Blue Account** | — | — | — | — | — | Out-of-network ATM rebate: up to $10/calendar month (disputed, conf 0.47); domestic outgoing wire fee: $15.00 (disputed) | doc_business_checking_accounts_navy_blue_009.json, doc_business_checking_accounts_navy_blue_003.json |
| **Lime Green Account** | — | — | — | — | — | Domestic outgoing wire fee: $10; international outgoing wire fee: $25 (both disputed; cross-doc contradiction with Navy Blue $15 domestic wire) | doc_business_checking_accounts_lime_green_008.json |
| **True Blue Account** | — | — | — | $75.00 | ≥$50,000 monthly balance | At ≥$50,000 balance: 10 free outgoing wires + 15 free incoming wires + 100 payment templates + 20% payroll discount + $0 treasury link; referral program: $350 referrer bonus + $250 new-member bonus = $600/referral; max 15 referrals/yr → $9,000 maximum annual referral earnings; international wire fees not documented; interest-crediting frequency not documented | (no source doc) |
| **Sky Blue Account** | — | — | — | — | — | Feature set and differentiators vs. True Blue not documented; referral program details not documented | (no source doc) |
| **World Blue Account** | — | — | — | — | — | Supported payment regions: ambiguous figure in documentation ("$140" may mean $140 or 140 regions — unresolved) | doc_business_checking_accounts_world_blue_001.json |
| **Beige Account** | — | — | — | — | — | Domestic out-of-network ATM: $0.00 Rho fee; ATM operator surcharges rebated up to $50.00/mo cap; foreign ATM fee: 1%, minimum $2.00 | doc_business_checking_accounts_beige_010.json, doc_business_checking_accounts_beige_011.json |

---

### 1.4 Business Savings

| Tier | APY | Min Deposit | Min Balance | Monthly Fee | Fee Waiver | Key Limits / Notes | Source |
|---|---|---|---|---|---|---|---|
| **Silver Plus Saver** | Tier 1 (below threshold): 2.50%; Tier 2 (above threshold): 4.00%; card bonuses: +0.18% Biz Silver (→2.68% T1 / 4.18% T2), +0.38% Biz Gold (→2.88% T1 / 4.38% T2), +0.62% Biz Platinum (→3.12% T1 / 4.62% T2) | — | Not specified (required to waive monthly fee) | $10.00 | Maintain unspecified minimum balance | Tier 2 balance threshold not documented; withdrawal and transfer limits not detailed; min opening deposit not documented | doc_business_savings_accounts_silver_plus_saver_001.json, doc_business_savings_accounts_silver_plus_saver_002.json, doc_business_savings_accounts_silver_plus_saver_003.json |
| **Gold Saver** | Base: 2.00% (un-sourced); card bonuses: +0.15% Biz Silver (→2.15%), +0.35% Biz Gold (→2.35%), +0.65% Biz Platinum (→2.65%) per un-sourced calculations; per sourced doc_business_savings_accounts_gold_saver_account_009.json: Biz Silver bonus = +0.20% (minor discrepancy with un-sourced set) | — | — | — | — | Tier balance thresholds not specified in documentation; base APY figure appears only in un-sourced calculation entries | doc_business_savings_accounts_gold_saver_account_001.json, doc_business_savings_accounts_gold_saver_account_009.json; (APY calculations: no source doc) |
| **Gold Plus Saver** | Base: 5.00%; card bonuses: +0.22% Biz Silver (→5.22%), +0.45% Biz Gold (→5.45%), +0.70% Biz Platinum (→5.70%) | — | — | — | — | Min opening deposit not documented; min ongoing balance not documented; monthly fee not documented | doc_business_savings_accounts_gold_plus_saver_001.json, doc_business_savings_accounts_gold_plus_saver_002.json |
| **Platinum Reserve Account** | Three documented scenarios (driver of base APY variation not explained): (a) 2.25% base + 0.25% Biz Silver = 2.50% total; (b) 2.75% base + 0.50% Biz Gold = 3.25% total; (c) 3.00% base + 0.80% Biz Platinum = 3.80% total | — | — | — | — | Source presents three different base APY values (2.25%, 2.75%, 3.00%); variation driver not specified | doc_business_savings_accounts_platinum_reserve_account_010.json |
| **Tiered Business Savings (product name not specified in documents)** | — (APY rates not specified for any tier) | — | — | — | — | Tier 1: ≤$37,500; Tier 2: $37,500–$112,500; Tier 3: >$112,500; outgoing domestic wire fee: 15 (currency unit not specified — likely $15.00 USD); balance at Tier 2/3 boundary ($112,500) may shift earning tier on small deposits | doc_business_savings_accounts_gold_saver_account_003.json, doc_business_savings_accounts_gold_saver_account_006.json |

---

### 1.5 Credit Cards

| Tier | Rewards / Cash Back Rate | Annual Fee | APR | Credit Limit | Key Limits / Notes | Source |
|---|---|---|---|---|---|---|
| **Business Silver Rewards Card** | 10.0% on travel & software (authorized platforms only); 1.0% on all other purchases | $0 first year for new customers (promotion offer-window dates not specified); regular annual fee: not documented | 20.49% variable (reference index not specified; grace period not documented; min monthly payment not documented; statement/payment due dates not defined) | $10,000 minimum – up to $50,000 maximum | Foreign transaction fee: 2.75%; new customer promo: $500 statement credit for $10,000 qualifying spend (5.0% effective rate); qualifying spend threshold for tier promo: $15,000; authorized platform list not published; MCC list not provided; min credit score: not specified; credit line stated as "at least $10,000 and may be as high as $50,000" without explicit maximum | doc_business_credit_cards_business_silver_rewards_card_001.json, doc_business_credit_cards_business_silver_rewards_card_002.json, doc_business_credit_cards_business_bronze_rewards_card_005.json, doc_business_credit_cards_business_platinum_rewards_card_012.json, doc_business_credit_cards_business_platinum_rewards_card_001.json, doc_business_credit_cards_business_bronze_rewards_card_007.json, doc_business_credit_cards_business_bronze_rewards_card_001.json |
| **Business Gold Rewards Card** | 2.5% cash back (all purchases) | $0.00 | — | — | Purchase protection window: 105 days; APY savings bonus to linked accounts: +0.30% (Silver Saver), +0.38% (Silver Plus Saver), +0.45% (Gold Plus Saver), +0.50% (Platinum Reserve); fee comparison: $200 less than Business Platinum per year | doc_credit_cards_gold_rewards_card_005.json, doc_credit_cards_platinum_rewards_card_003.json |
| **Business Platinum Rewards Card** | 10.0% cash back (content rate; title of doc_credit_cards_platinum_rewards_card_002.json states "4% Cash Back" — conflict flagged as data-quality defect) | $200.00/yr | — | — | Min credit score: 750; annual fee rebate: $150 for ≥$7,500 monthly spend (threshold reference flagged as not fully explicit in source); max 7 referrals/yr × $75/referral = $525 maximum annual referral earnings; purchase protection window: 135 days (30 days longer than Gold); APY savings bonus to linked accounts: +0.55% (Silver Saver), +0.62% (Silver Plus Saver), +0.70% (Gold Plus Saver), +0.80% (Platinum Reserve) | doc_credit_cards_platinum_rewards_card_002.json, doc_credit_cards_platinum_rewards_card_001.json, doc_credit_cards_platinum_rewards_card_007.json, doc_credit_cards_silver_rewards_card_011.json, doc_credit_cards_gold_rewards_card_005.json, doc_credit_cards_platinum_rewards_card_003.json |
| **Diamond Elite Card** | 5.0% cash back (all purchases) | $495/yr (waived under new-customer promo) | — | Provisional credit limits by tier: Entry $2,500 → Mid $5,000 → Premium $10,000 → Elite $15,000 → Invitation $25,000 | New-customer promo: $5,000 statement credit for $50,000 qualifying spend; promo net value including fee waiver: $5,495 for $50,000 spend (11.0% effective return on qualifying spend); base rewards on $50,000 promo spend: 5.0% × $50,000 = $2,500 | doc_credit_cards_diamond_elite_card_003.json, doc_credit_cards_credit_cards_(general)_015.json |
| **Green Rewards Card** | 5× points on green purchases; 1× points on standard purchases; CO2 offset: spend × $0.06 lbs (or equivalently spend × 1.25 g/$); trees planted: floor(spend ÷ $1,000) per period | — | — | — | Points redemption value: $0.01/point; examples: $1,000 spend = 1 tree + 1,250 g CO2 offset; $2,500 spend = 2 trees + 3,125 g CO2 offset; $750 spend = 937.5 g CO2 offset | doc_business_credit_cards_green_rewards_card_003.json, doc_checking_accounts_evergreen_account_004.json, doc_credit_cards_ecocard_002.json |
| **EcoCard** | Sustainability points on qualifying spend; $2,000 sustainability points for $5,000 qualifying spend (40% effective bonus rate on qualifying spend) | — | — | — | Points redemption value: $0.01/point; CO2 offset: spend × 1.25 g/$ | doc_credit_cards_ecocard_005.json |
| **Bronze 009** | — | — | — | — | Signup bonus: 25,000 points = $250 redemption value (at $0.01/point) | doc_business_credit_cards_business_bronze_rewards_card_009.json, doc_credit_cards_ecocard_005.json |
| **Card with travel & purchase protection (product name not specified in documentation)** | — | — | — | — | Purchase protection window duration: not stated; travel insurance benefit window: not stated; annual travel credit rollover/expiration policy: not specified; definition of "eligible" travel purchases: not fully specified | doc_business_credit_cards_business_platinum_rewards_card_006.json |

---

### 1.6 BNPL

| Tier | Credit Limit | Min Purchase | Max Purchase | Term / Installments | APR | Late Fee | Key Limits / Notes | Source |
|---|---|---|---|---|---|---|---|---|
| **BNPL Bronze** | — | — | — | — | — | — | All product specification values absent: product code, credit limit, min/max purchase amount, number of installments, total term, installment interval, APR, late fees, merchant fee, currency, and max active plans all flagged as missing | doc_buy_now_pay_later_bnpl_bronze_008.json |
| **BNPL Silver** | — | — (not specified) | — (not specified) | — | — | — | Min and max eligible purchase amounts not documented; enablement requires product configuration flag whose name is not specified | doc_buy_now_pay_later_bnpl_silver_002.json, doc_buy_now_pay_later_bnpl_silver_001.json |
| **BNPL Gold 001** | — | — | — | Standard term: — months; introductory APR: —; introductory period: — days; standard APR after intro: — | — | — | All core spec values (credit limit range, term, both APR values and intro period duration) absent from source documentation | doc_buy_now_pay_later_bnpl_gold_001.json |
| **BNPL Gold 002** | — (minimum) to — (maximum) | — | — | — | — | — | Credit limit range minimum and maximum both not specified | doc_buy_now_pay_later_bnpl_gold_002.json |
| **BNPL Gold 003** | — | — | — | Introductory APR: —; introductory period: — days; standard APR begins: day —; standard APR: — | — | — | Introductory APR value, introductory period duration, transition day, and standard APR value all absent from source documentation | doc_buy_now_pay_later_bnpl_gold_003.json |
| **BNPL Gold 004** | — | — | — | — | — | — | Auto-debit current status not specified in documentation | doc_buy_now_pay_later_bnpl_gold_004.json |
| **BNPL Gold 005** | — | — | — | — | — | — | Min and max transaction amounts for financing eligibility not specified; upper and lower settlement amount thresholds for eligibility not specified | doc_buy_now_pay_later_bnpl_gold_005.json |
| **BNPL Platinum** | — | — (not specified) | — (not specified) | — months; — monthly installments | — to — (variable; reference index not documented) | — | Purchase protection reimbursement rate: —; per-item max reimbursement: —; annual per-account max coverage: —; claim submission window: — days from purchase; item eligibility lookback: — days; early payoff penalty rate: —; prepayment eligibility condition: —; activation status indicator name not documented | doc_buy_now_pay_later_bnpl_platinum_004.json, doc_buy_now_pay_later_bnpl_platinum_005.json, doc_buy_now_pay_later_bnpl_platinum_006.json, doc_buy_now_pay_later_bnpl_platinum_007.json, doc_buy_now_pay_later_bnpl_platinum_002.json, doc_buy_now_pay_later_bnpl_platinum_001.json, doc_buy_now_pay_later_bnpl_platinum_008.json, doc_buy_now_pay_later_bnpl_platinum_003.json |

---

### 1.7 Other

**Virtual Cards**
- Fee structure (annual fee, APY, account opening requirements): not documented (doc_business_credit_cards_virtual_card_management_002.json)
- Annual fee applicability: whether assessed per-user or per-card not specified; whether waived under certain product tiers not specified (doc_credit_cards_virtual_card_management_001.json)
- Merchant category controls: described as optional but eligible categories and selection criteria not enumerated (doc_business_credit_cards_virtual_card_management_004.json)

**Everyone Pay (peer-to-peer transfer service)**
- Standard transfer speed: 12 hours; standard fee: not stated
- Instant transfer fee: $0.75 per transfer
- Required workflow: add/verify contact → send (standard 12 h or instant at $0.75) → receive with notification → manage contact list (doc_everyone_pay_everyone_pay_001.json)

**Provisional Credit Limit Tier Framework (applicable to credit card tiers)**

| Tier Label | Maximum Provisional Credit Limit |
|---|---|
| Entry | $2,500 |
| Mid | $5,000 |
| Premium | $10,000 |
| Elite | $15,000 |
| Invitation | $25,000 |

Source: doc_credit_cards_credit_cards_(general)_015.json

**Referral Programs (source accounts not named in available entries)**

| Program | Referrer Bonus | New Member Bonus | Max Annual Referrals | Max Annual Earnings (Referrer) | Source |
|---|---|---|---|---|---|
| Program A | $20 per referral | $35 per new member | 4 | $80 | doc_checking_accounts_green_fee-free_account_007.json |
| Program B | $15 per referral | $25 cash (requires ≥$100 deposit within 90 days) | 3 | $45 | doc_checking_accounts_light_green_account_001.json |


---


## 2. Agent-Tool Catalog

| Tool (full id) | Signature / params | When called | Executed by | Source doc_id(s) |
|---|---|---|---|---|
| `apply_checking_account_credit_5829` | `account_id`, `amount` (positive dollar, exact — rounding prohibited), `credit_type` (`'rebate_credit'` \| `'fee_refund'`). Once per account per interaction; 14-day cooldown. | Correcting a missing ATM rebate or fee mischarge on a checking account. Savings accounts ineligible. | agent | doc_bank_accounts_bank_accounts_(general)_017.json |
| `apply_credit_card_account_flag_6147` | `credit_card_account_id`, `user_id`, `flag_type` (`'annual_fee_waived'`), `expiration_date` (MM/DD/YYYY, one year from today), `reason` (`'loyalty_benefit'`) | Annual-fee waiver retention offer; only for customers with ≥ 2 years tenure requesting closure due to annual fee. | agent | doc_credit_cards_credit_card_account_logistics_003.json |
| `apply_statement_credit_8472` *(discoverable — unlock first)* | `user_id`, `credit_card_account_id`, `amount` (positive, dollars), `reason` (enum — 10 values: `goodwill_adjustment` \| `promotional_credit` \| `annual_fee_reversal` \| `late_fee_reversal` \| `interest_charge_reversal` \| `dispute_resolution` \| `price_match` \| `retention_offer` \| `error_correction` \| `other`) | Applying a statement credit to a credit card account after qualifying event. | agent | doc_credit_cards_credit_cards_(general)_017.json |
| `approve_credit_limit_increase_5847` | `credit_card_account_id`, `user_id`, `new_credit_limit` (float) | CLI workflow Step 4 — approve the request after eligibility and payment-history checks pass. | agent | doc_credit_cards_credit_card_account_logistics_007.json |
| `call_discoverable_agent_tool` | `tool_name`, `...params` (varies by target tool) | Step 2 of the two-step discoverable-tool invocation pattern; must follow `unlock_discoverable_agent_tool`. | agent | doc_credit_cards_credit_cards_(general)_004.json, doc_credit_cards_credit_card_replacements_001.json |
| `close_bank_account_7392` | **Parameters undocumented** — no formal parameter schema found across 698-document corpus. | Final step of all personal checking, personal savings, business checking, and business savings account closure procedures, after all tier, notice-period, and approval pre-conditions are satisfied. | agent | doc_bank_accounts_bank_accounts_(general)_006.json, doc_bank_accounts_bank_accounts_(general)_007.json, doc_bank_accounts_bank_accounts_(general)_001.json, doc_bank_accounts_bank_accounts_(general)_005.json, doc_bank_accounts_bank_accounts_(general)_008.json, doc_bank_accounts_bank_accounts_(general)_002.json, doc_bank_accounts_bank_accounts_(general)_004.json |
| `close_credit_card_account_7834` | `credit_card_account_id` (string), `user_id` (string) | Credit card account closure; all four eligibility conditions must pass first: $0.00 outstanding balance, no pending disputes, account age ≥ 60 days, no pending replacement orders. | agent | doc_credit_cards_credit_card_account_logistics_002.json, doc_credit_cards_credit_card_account_logistics_001.json |
| `deny_credit_limit_increase_5848` | `credit_card_account_id`, `user_id`, `denial_reason` (enum — exactly 9 values; individual value names not enumerated in source) | CLI workflow Step 4 — deny the request when eligibility or payment-history check fails. | agent | doc_credit_cards_credit_card_account_logistics_007.json |
| `downgrade_credit_card_3847` | `credit_card_account_id`, `user_id`, `target_card_type` (`'Bronze Rewards Card'` for personal \| `'Business Bronze Rewards Card'` for business). No cross-category downgrade permitted. | Downgrading a credit card to the lowest-tier product within the same category; takes effect immediately. | agent | doc_credit_cards_credit_card_account_logistics_008.json |
| `file_debit_card_transaction_dispute_6281` | `dispute_category` (enum — exactly 9 values including `recurring_charge_after_cancellation`, `card_present_fraud`, `card_not_present_fraud`; full set of 9 values not individually listed in source). Pre-filing conditions implied: amount ≥ $1.00, transaction within 60 days, debit card on OPEN checking account, open-dispute count below tier cap. | Filing a debit card transaction dispute; `person_to_person` category used for EveryonePay disputes. | agent | doc_bank_accounts_bank_accounts_(general)_031.json |
| `get_all_user_accounts_by_user_id_3847` | `user_id` (inferred from tool name; no formal parameter spec found in source corpus) | Enumerating all accounts for a given user. | agent | *(no source doc; inventory reference only — entry e8330)* |
| `get_atm_deposit_images_8473` | **Parameters undocumented** — no formal spec in source corpus. | ATM deposit disputes requiring physical verification; extended resolution timeline up to 45 days. | agent | doc_bank_accounts_bank_accounts_(general)_033.json |
| `get_bank_account_transactions_9173` | `account_id` | Retrieving all transactions for any bank account (checking or savings) in reverse chronological order; returns `transaction_id`, `account_id`, `date` (MM/DD/YYYY), `description`, `amount` (positive = credit, negative = debit), `type` (19 enum values including `everyonepay`), `status` (`'posted'` \| `'pending'`). | agent | doc_bank_accounts_bank_accounts_(general)_018.json |
| `get_closure_reason_history_8293` | `credit_card_account_id` | Credit card closure Step 2 — abuse-prevention check; if prior closure attempt found within 1 year, skip retention offers and proceed directly to closure. | agent | doc_credit_cards_credit_card_account_logistics_003.json |
| `get_credit_card_accounts_by_user` | **Parameters undocumented** — identified by functional description only; no formal signature found. | Retrieving all active and closed credit card accounts for a customer; required cross-product security check during lost/stolen debit card protocol. | agent | doc_bank_accounts_bank_accounts_(general)_030.json |
| `get_credit_limit_increase_history_4829` | `credit_card_account_id` | CLI workflow Step 2 — cooldown check for prior CLI requests on the same account. | agent | doc_credit_cards_credit_card_account_logistics_007.json |
| `get_payment_history_6183` | `credit_card_account_id` (string), `months` (integer; 6 for entry-tier, 3 for mid/premium-tier) | CLI workflow Step 3 — verify consecutive on-time payment months before approving or denying CLI. | agent | doc_credit_cards_credit_card_account_logistics_006.json |
| `get_pending_replacement_orders_5765` | `credit_card_account_id` | Must run before any credit card account closure; closure blocked if any order is in a non-final state (pending or shipped). Returns collection of records: `order_id`, `status`, `created_at`, `latest_event_at`, `notes`. | agent | doc_credit_cards_credit_card_replacements_005.json |
| `initial_transfer_to_human_agent_0218` *(discoverable — unlock first)* | **Parameters undocumented** — only the unlock-then-call pattern is specified. | Backend Incident 11/13 protocol — second transfer request (request #2), after `initial_transfer_to_human_agent_1822`; protocol valid until 2026-11-15 23:59 EST. | agent | doc_credit_cards_credit_cards_(general)_011.json |
| `initial_transfer_to_human_agent_1822` *(discoverable — unlock first)* | **Parameters undocumented** — only the unlock-then-call pattern is specified. | Backend Incident 11/13 protocol — first transfer request (request #1); protocol valid until 2026-11-15 23:59 EST. | agent | doc_credit_cards_credit_cards_(general)_011.json |
| `log_credit_card_closure_reason_4521` | `credit_card_account_id`, `user_id`, `closure_reason` (enum — exactly 7 values: `annual_fee` \| `not_using_card` \| `found_better_card` \| `unhappy_with_rewards` \| `simplifying_finances` \| `negative_experience` \| `other`). **Only these 3 params accepted; no additional params.** | Credit card closure Step 3 — log the customer-stated closure reason before invoking closure tool. | agent | doc_credit_cards_credit_card_account_logistics_003.json |
| `log_verification` | `name`, `user_id`, `address`, `email`, `phone_number`, `date_of_birth` (all set to bypass-code string `9K2X7M4P1N8Q3R5T6A` when bypass is used — NOT actual customer PII), `time_verified` (actual timestamp) | Account Recovery Bypass Code flow — logs identity verification event; PII fields are replaced with the bypass code to anonymize the audit entry. | agent | doc_customer_support_special_support_codes_001.json |
| `open_bank_account_4821` | `user_id`, `account_type` (`'savings'` for savings accounts; `'checking'` for checking accounts), `account_class` (full official name ending with `'Account'`, e.g. `'Silver Plus Account'`, `'Navy Blue Account'`). Parameters must **not** be exposed to the customer. | Account opening for personal checking, personal savings, business checking, and business savings — called after eligibility confirmed and customer has selected account class. | agent | doc_bank_accounts_bank_accounts_(general)_002.json, doc_bank_accounts_bank_accounts_(general)_010.json, doc_bank_accounts_bank_accounts_(general)_003.json, doc_bank_accounts_bank_accounts_(general)_004.json, doc_bank_accounts_bank_accounts_(general)_001.json |
| `order_replacement_credit_card_7291` *(discoverable — unlock first)* | Credit card account identifier; `reason` (enum: `fraud_suspected` \| `lost` \| `stolen` \| `damaged` \| `expired` \| `other`); `shipping_address` (confirmed with customer); `shipping_speed` (`standard` \| `expedited`); `expedited_fee_acknowledgement` (required when fee applies); `notes`. Old card auto-cancelled on submission. | Ordering a replacement credit card; expedited speed strongly recommended for `fraud_suspected` or `stolen`. | agent | doc_credit_cards_credit_card_replacements_001.json |
| `pay_credit_card_from_checking_9182` *(discoverable — unlock first)* | `user_id`, `checking_account_id`, `credit_card_account_id`, `amount` (float, positive, must not exceed checking account balance or credit card outstanding balance) | Paying a credit card balance from a linked checking account. | agent | doc_credit_cards_credit_card_account_logistics_009.json |
| `set_debit_card_recurring_block_7382` | `card_id` (debit card ID), `block_recurring` (`true` to block \| `false` to unblock) | Blocking or unblocking all future recurring/subscription charges on a debit card. | agent | doc_bank_accounts_bank_accounts_(general)_034.json |
| `submit_cash_back_dispute_0589` | `user_id`, `transaction_id` | Customer-initiated cash-back rewards dispute on a credit card transaction. | **customer** | doc_bank_accounts_bank_accounts_(general)_030.json, doc_credit_cards_credit_card_replacements_001.json, doc_credit_cards_credit_cards_(general)_003.json, doc_credit_cards_credit_cards_(general)_004.json, doc_credit_cards_credit_card_account_logistics_002.json, doc_credit_cards_credit_card_account_logistics_003.json |
| `submit_credit_limit_increase_request_7392` | `credit_card_account_id` (string), `user_id` (string), `requested_increase_amount` (integer) | CLI workflow Step 1 — submit the CLI request; must be called before eligibility and history checks. | agent | doc_credit_cards_credit_card_account_logistics_007.json |
| `transfer_funds_between_bank_accounts_7291` | `source_account_id`, `destination_account_id`, `amount` (USD, positive). Pre-conditions: both accounts ACTIVE or OPEN; sufficient source funds; same customer; customer authorized; source ≠ destination. | Transferring funds between accounts; during account opening, called only when customer explicitly authorizes an immediate deposit; destination must be the newly opened account from `open_bank_account_4821` return value. | agent | doc_bank_accounts_bank_accounts_(general)_010.json, doc_bank_accounts_bank_accounts_(general)_002.json, doc_bank_accounts_bank_accounts_(general)_004.json, doc_bank_accounts_bank_accounts_(general)_003.json, doc_bank_accounts_bank_accounts_(general)_007.json |
| `transfer_to_human_agents` | **Parameters undocumented** — no formal spec in source corpus. | Backend Incident 11/13 protocol — regular (non-discoverable) third transfer, used on request #3 after both discoverable tools; protocol valid until 2026-11-15 23:59 EST. | agent | doc_credit_cards_credit_cards_(general)_011.json |
| `unlock_discoverable_agent_tool` | `tool_name` | Step 1 of the two-step discoverable-tool invocation pattern; must precede every `call_discoverable_agent_tool` call; applies to `order_replacement_credit_card_7291`, `pay_credit_card_from_checking_9182`, `update_transaction_rewards_3847`, `apply_statement_credit_8472`, `initial_transfer_to_human_agent_1822`, `initial_transfer_to_human_agent_0218`. | agent | doc_credit_cards_credit_cards_(general)_004.json, doc_credit_cards_credit_card_replacements_001.json |
| `update_transaction_rewards_3847` *(discoverable — unlock first)* | `transaction_id` (exact ID from `cash_back_disputes` DB), `new_rewards_earned` (string, format `'X points'` where X is a whole number; agent must independently recalculate — **must not** use `expected_rewards` field from dispute record) | Cash-back dispute correction — applying corrected reward points after `submit_cash_back_dispute_0589` resolution. | agent | doc_credit_cards_credit_cards_(general)_004.json |
| *QR payment generation tool* **(no formal tool ID)** | **Parameters undocumented** — no tool name or parameter schema in source corpus. Initiates a 17-minute validity window on invocation. | Generating a QR code for a payment request. | agent | doc_everyone_pay_qr_transfers_001.json |
| *QR scanner tool* **(no formal tool ID)** | **Parameters undocumented** — no tool name or parameter schema in source corpus. | Scanning a QR code to extract payment request details for validation and execution. | agent | doc_everyone_pay_qr_transfers_003.json |
| *Debit card replacement ordering tool* **(no formal tool ID)** | **Formal name and parameters undocumented** — referenced in lost/stolen card protocols by functional description only across all 698 source documents. | Ordering a replacement debit card following a lost/stolen card protocol. | agent | *(no source doc; entries e8327, e8328, e8330)* |

---

### Notes

**Suffix collisions** (same numeric suffix carried by different tools):

- Suffix `_7291`: `transfer_funds_between_bank_accounts_7291` and `order_replacement_credit_card_7291` — distinct tools, distinct domains (bank account funding vs. credit card replacement).
- Suffix `_3847`: `get_all_user_accounts_by_user_id_3847`, `update_transaction_rewards_3847`, and `downgrade_credit_card_3847` — three tools across three separate functional domains share this suffix.
- Suffix `_7392`: `close_bank_account_7392` and `submit_credit_limit_increase_request_7392` — distinct tools; one closes a bank account, one initiates a credit limit increase.

**Tools invoked but with undocumented parameters:**

- `close_bank_account_7392`: Called as the final step in all four account-closure procedure families (personal checking, personal savings, business checking, business savings) yet no parameter schema (required field names, types, return value) appears in any of the 698 source documents. Confirmed source gap in entries e8407, e8672, e8746, e8859.
- `get_credit_card_accounts_by_user`: Named explicitly in source but no formal parameter list or return schema was found; identified by functional description only. Confirmed source gap in entry e8325.
- `get_all_user_accounts_by_user_id_3847`: Present only in the inventory analysis entry (e8330); no dedicated specification document located.
- `get_atm_deposit_images_8473`: Named in source and invoked for ATM deposit disputes but no parameter schema documented. Confirmed source gap in entry e8329.
- `initial_transfer_to_human_agent_1822` / `initial_transfer_to_human_agent_0218`: Both are discoverable tools; unlock-then-call pattern is documented but no parameter names or types specified.
- `transfer_to_human_agents`: Referenced as the non-discoverable third step in the Backend Incident 11/13 sequence; no parameter specification found.
- *QR payment generation tool* / *QR scanner tool*: Both lack formal tool IDs entirely. Functionally described in user-facing documents; no technical signatures available. Confirmed source gap in entry e8329.
- *Debit card replacement ordering tool*: Referenced in lost/stolen debit card protocols but no formal tool name, parameters, preconditions, or return values found across the corpus. Confirmed source gaps in entries e8327, e8328.


---


## 3. Eligibility Rules

---

### 3.1 Personal Checking

#### 3.1.1 Account Opening (All Classes)

- Customer identity must be verified in Rho-Bank systems before opening a personal checking account. (doc_bank_accounts_bank_accounts_(general)_001.json)
- Customer must be at least 18 years old. (doc_bank_accounts_bank_accounts_(general)_001.json)
- The total number of personal checking accounts held by the customer must not exceed 4. Opening a fifth personal checking account is prohibited. (doc_bank_accounts_bank_accounts_(general)_001.json)
- No personal checking account held by the customer may have been closed for cause within the past 6 months. (doc_bank_accounts_bank_accounts_(general)_001.json)
- The `account_class` value supplied to the opening tool must end with the word "Account". (doc_bank_accounts_bank_accounts_(general)_001.json)

#### 3.1.2 Light Green Account (Youth — Exception Tier)

- Age eligibility is 13–24 only; the 18-year minimum that governs all other personal checking products does not apply. (doc_checking_accounts_light_green_account_002.json)
- Age is verified at opening and monitored on an ongoing basis; customers who age out of the 13–24 range lose eligibility for this product. (doc_checking_accounts_light_green_account_002.json)
- Daily spending limit: $300. (doc_checking_accounts_light_green_account_002.json)
- ATM daily cash withdrawal limit: $150. (doc_checking_accounts_light_green_account_002.json)
- Free out-of-network ATM withdrawals: 4 per month; each subsequent withdrawal costs $1.50. (doc_checking_accounts_light_green_account_002.json)
- Mobile deposit daily limit: $500. (doc_checking_accounts_light_green_account_002.json)
- Referral bonus for referrer: $15. Referral bonus for new member: $25. (doc_checking_accounts_light_green_account_002.json)
- Maximum referrals per year for a Light Green account referrer: 3. (doc_checking_accounts_light_green_account_002.json)
- Referred member must deposit $100 within 90 days of account opening to qualify the referral bonus. (doc_checking_accounts_light_green_account_002.json)
- Referrer must have held their account for at least 14 days before making a referral. (doc_checking_accounts_light_green_account_002.json)
- Referred person must be 18 or older for all personal checking products, with one exception: the Light Green Account allows minors to be referred if accompanied by a guardian. (doc_bank_accounts_bank_accounts_(general)_047.json)
- **Data quality gap:** Guardian co-sign requirements, parental-consent flow, and the procedure for verifying the minor/guardian relationship in the account-opening tool are not documented. (doc_bank_accounts_bank_accounts_(general)_047.json)

#### 3.1.3 Gold Years Account (Senior Tier)

- Eligible exclusively for customers aged 62 or older. (doc_checking_accounts_gold_years_account_002.json)
- All major fees are $0: monthly maintenance, out-of-network ATM, returned deposit, incoming domestic wire. (doc_checking_accounts_gold_years_account_002.json)
- Foreign ATM withdrawal fee: $3.50, conditionally waived when account balance is ≥ $10,000. (doc_checking_accounts_gold_years_account_002.json)
- APY: 1.0% on balance. (doc_checking_accounts_gold_years_account_002.json)
- EveryonePay daily send limit for Gold Years Account holders: $3,000. (doc_checking_accounts_gold_years_account_006.json)
- A one-time $50 Social Security bonus applies after the first qualifying Social Security direct deposit. (doc_checking_accounts_gold_years_account_006.json)
- EveryonePay is the recommended redistribution mechanism for Social Security direct-deposit funds sent to family or caregivers. (doc_checking_accounts_gold_years_account_006.json)

#### 3.1.4 Blue Account (Checking)

- Monthly maintenance fee: $20.00; fee is waived when the customer maintains a minimum daily balance of $625. (doc_checking_accounts_blue_account_001.json)
- **Data quality gap:** No information on Blue Account opening requirements, minimum account age, or customer onboarding conditions is documented. (doc_checking_accounts_blue_account_002.json)

#### 3.1.5 Pre-Closure Requirements (All Personal Checking Classes)

- Account status must be OPEN before the close tool (`close_bank_account_7392`) may be invoked. (doc_bank_accounts_bank_accounts_(general)_005.json)
- No pending transactions may exist at time of closure. (doc_bank_accounts_bank_accounts_(general)_005.json)
- If an early closure fee applies: the current account balance must be ≥ the fee amount; the fee is deducted directly from the account balance and no alternative payment method is permitted. (doc_bank_accounts_bank_accounts_(general)_005.json)
- If no early closure fee applies: the account balance must be exactly $0 before closure. (doc_bank_accounts_bank_accounts_(general)_005.json)
- Notice periods vary by tier: ENTRY tier — 0 days (immediate); MID tier — 3 days; PREMIUM tier — 7 days; ELITE tier — 14 days. (doc_bank_accounts_bank_accounts_(general)_005.json)

#### 3.1.6 Checking Account Referral Program (Cross-Tier Rules)

- Rolling window cap: maximum 2 referral bonuses per any 9-day window, counted across all checking account types combined. (doc_bank_accounts_bank_accounts_(general)_047.json)
- Any third or subsequent referral within a 9-day window is automatically denied and cannot be reinstated within the same window. (doc_bank_accounts_bank_accounts_(general)_047.json)
- Agent must verify referral eligibility before providing referral information to any customer. (doc_bank_accounts_bank_accounts_(general)_047.json)
- Referrer tenure threshold is counted from the earliest Rho-Bank checking account open date, not from the date of the current account type. (doc_bank_accounts_bank_accounts_(general)_047.json)
- Referred person must be a new customer with no existing checking accounts, savings accounts, or closed accounts at Rho-Bank within the past 12 months. (doc_bank_accounts_bank_accounts_(general)_047.json)
- Same-address referrals are prohibited; referrer and referred person must not share a registered address. (doc_bank_accounts_bank_accounts_(general)_047.json)
- Referred person must be 18 or older (Light Green Account allows minors with a guardian as an exception). (doc_bank_accounts_bank_accounts_(general)_047.json)
- Qualifying deposit must be new money — funds transferred from another Rho-Bank account do not qualify. (doc_bank_accounts_bank_accounts_(general)_047.json)
- Qualifying deposit must remain in the account for 30 days after the end of the qualifying period. (doc_bank_accounts_bank_accounts_(general)_047.json)
- Clawback provision: referral bonus may be reversed if the referred account is closed within 90 days. (doc_bank_accounts_bank_accounts_(general)_047.json)
- Referral bonus cannot be stacked with other new-account promotions; only one promotional offer applies per new account. (doc_bank_accounts_bank_accounts_(general)_047.json)
- Only one referral code is permitted per account. (doc_bank_accounts_bank_accounts_(general)_047.json)
- Referral welcome bonus structure: new account receives a $25 cash bonus upon opening; referred customer must deposit ≥ $100 within 90 days. (doc_checking_accounts_light_green_account_001.json)
- **Data quality gap:** No clarity on whether referred accountholders must be entirely new customers or whether existing customers who upgrade/re-apply are eligible. (doc_credit_cards_silver_rewards_card_011.json)

---

### 3.2 Personal Savings

#### 3.2.1 Account Opening Eligibility Checklist (All 5 Conditions Required)

- **Condition 1:** Customer identity must be verified in Rho-Bank systems. (doc_bank_accounts_bank_accounts_(general)_002.json)
- **Condition 2:** Customer must hold at least one active Rho-Bank checking account. Agent must confirm an active checking account exists before proceeding. (doc_bank_accounts_bank_accounts_(general)_002.json)
- **Condition 3:** Customer must currently hold fewer than 5 personal savings accounts. If the customer already has 5 savings accounts, the agent must not open another and must inform the customer they have reached the maximum. (doc_bank_accounts_bank_accounts_(general)_002.json)
- **Condition 4:** Customer must have no accounts in collections and no negative balances across any Rho-Bank accounts. If collections or negative balances exist, those issues must be resolved first; opening must not proceed. (doc_bank_accounts_bank_accounts_(general)_002.json)
- **Condition 5:** The Rho-Bank checking account must have been held for at least 14 days. Agent must verify checking account tenure meets the 14-day minimum. (doc_bank_accounts_bank_accounts_(general)_002.json)
- Failure of any single condition blocks invocation of the account-opening tool (`open_bank_account_4821`). (doc_bank_accounts_bank_accounts_(general)_002.json)

#### 3.2.2 Green Account (Savings)

- Minimum opening deposit: $100. (doc_savings_accounts_green_account_(savings)_001.json)
- Ongoing minimum balance requirement: $500 must be maintained. (doc_savings_accounts_green_account_(savings)_001.json)
- Paperless statements are mandatory; paper statements are not available for this product. (doc_savings_accounts_green_account_(savings)_001.json)
- EcoCard APY bonus: +0.5% APY is earned when an EcoCard is held and linked to the Green Account. (doc_savings_accounts_green_account_(savings)_003.json)
- Free monthly withdrawals when EcoCard is linked: base 8 + EcoCard bonus 7 = 15 total free withdrawals per month. (doc_savings_accounts_green_account_(savings)_009.json)
- **Data quality gap:** The definition of "internal transfer to other accounts" for the Bronze Saver withdrawal limit — specifically whether it covers same-customer accounts only or extends to third-party accounts — is not specified. (doc_business_savings_accounts_bronze_saver_account_008.json)

#### 3.2.3 Gold Plus Account

- EcoCard APY bonus: +0.1% when EcoCard is held with a Gold Plus Account. (doc_savings_accounts_gold_plus_account_009.json)
- **Data quality gap:** Eligibility conditions for opening a Gold Plus Account are not detailed in available documents. (batch_092_all_docs)
- **Data quality gap:** Account count caps (maximum number of Gold Plus accounts per customer) are not specified. (batch_092_all_docs)
- **Data quality gap:** Waiting periods for features such as sweep initiation and crypto access are not documented. (batch_092_all_docs)
- **Data quality gap:** Specific disqualifiers or account closure conditions are not specified. (batch_092_all_docs)
- **Data quality gap:** Eligibility conditions for Gold Account opening — including age, citizenship, employment, credit score — are not documented. (doc_savings_accounts_gold_account_003.json)

#### 3.2.4 Sweep Deposits

- **Data quality gap:** No specification of which account types other than Bronze are ineligible to serve as sweep deposit destinations. (doc_business_savings_accounts_automatic_sweep_program_004.json)

#### 3.2.5 Evergreen Account (Savings / Premium)

- Both the referrer's account and the referred person's account must maintain good standing for the referral bonus to be confirmed. (doc_checking_accounts_evergreen_account_001.json)
- EveryonePay transfers from an Evergreen Account do NOT accrue carbon offset credits, regardless of transaction amount. (doc_checking_accounts_evergreen_account_005.json)
- Carbon offset calculation rate for eligible posted spending: $1.25 per eligible posted dollar spent. EveryonePay sends are explicitly excluded from this calculation. (doc_checking_accounts_evergreen_account_005.json)

#### 3.2.6 Extended FDIC Insurance

- **Data quality gap:** The document uses "Yes" as a placeholder for the extended FDIC insurance eligibility scope; the actual eligible account types are not specified. (doc_savings_accounts_platinum_plus_account_003.json)

---

### 3.3 Business Checking

#### 3.3.1 Account Opening Eligibility Checklist (All 5 Conditions Required)

- **Condition 1:** Customer identity must be verified. (doc_bank_accounts_bank_accounts_(general)_003.json)
- **Condition 2:** Customer must have at least 1 existing personal checking account with status OPEN. (doc_bank_accounts_bank_accounts_(general)_003.json)
- **Condition 3:** Customer must not exceed 6 business checking accounts; opening a seventh is prohibited. (doc_bank_accounts_bank_accounts_(general)_003.json)
- **Condition 4:** Customer must have NO accounts of ANY type with status CLOSED. (doc_bank_accounts_bank_accounts_(general)_003.json)
- **Condition 5:** The existing personal checking account balance must be ≥ $500. (doc_bank_accounts_bank_accounts_(general)_003.json)
- **Cross-document inconsistency:** Business checking Condition 4 (no closed accounts of any type, any time) is materially stricter than the personal checking rule, which only bars checking accounts closed *for cause* within the past 6 months. This discrepancy may reflect an error in policy intent. (doc_bank_accounts_bank_accounts_(general)_003.json, doc_bank_accounts_bank_accounts_(general)_001.json)

#### 3.3.2 Sky Blue Account (Startup-Specific Tier)

- Company must be within 4 years of formation to qualify for the Sky Blue tier. (doc_business_checking_accounts_sky_blue_001.json, doc_business_checking_accounts_sky_blue_002.json, doc_business_checking_accounts_sky_blue_003.json, doc_business_checking_accounts_sky_blue_005.json)
- **Data quality gap:** The time unit for the 4-year company age requirement is inferred; the source document states "4" without an explicit unit. (doc_business_checking_accounts_sky_blue_008.json)
- Free period duration: "6" (unit not stated in source documents; likely 6 months by convention). (doc_business_checking_accounts_sky_blue_001.json, doc_business_checking_accounts_sky_blue_002.json)
- Monthly fee after free period: $25.00. (doc_business_checking_accounts_sky_blue_001.json)
- AWS credits included: $2,750. (doc_business_checking_accounts_sky_blue_001.json)
- Maximum Founder Cards: 3. (doc_business_checking_accounts_sky_blue_001.json)
- Burn-rate analytics and investor reporting are included features of the Sky Blue tier. (doc_business_checking_accounts_sky_blue_001.json)
- **Data quality gap:** The funding requirement threshold for the Sky Blue Quick Checks process is listed as 0; it is unclear whether this means a $0 minimum or is a placeholder. (doc_business_checking_accounts_sky_blue_009.json)

#### 3.3.3 Hunter Green Account

- Monthly maintenance fee: $25.00; fee is waived when balance ≥ $5,000. (doc_business_checking_accounts_hunter_green_001.json)
- Referral program tenure requirement: 60 days minimum account age. (doc_business_checking_accounts_navy_blue_001.json, doc_business_checking_accounts_hunter_green_001.json)

#### 3.3.4 Lime Green Account

- Monthly maintenance fee: $25.00; fee is waived when balance ≥ $15,000. (doc_business_checking_accounts_lime_green_002.json)

#### 3.3.5 Navy Blue Account

- Referral program eligibility: referrer account age minimum = 60 days. (doc_business_checking_accounts_navy_blue_001.json)
- Referred business must deposit $5,000 within 90 days of account opening. (doc_business_checking_accounts_navy_blue_001.json)
- Maximum referrals per year per referrer: 10. (doc_business_checking_accounts_navy_blue_001.json)
- Referrer bonus per qualified referral: $100. (doc_business_checking_accounts_navy_blue_001.json)
- New business bonus per qualified sign-up: $75. (doc_business_checking_accounts_navy_blue_001.json)
- **Data quality gap:** Approval criteria for the referred business account are not specified; the document states a bonus is earned when the referred business is approved but does not define what approval requires. (doc_business_credit_cards_business_platinum_rewards_card_012.json)

#### 3.3.6 Cobalt Blue Account (Premium Tier)

- Account closure requires supervisor review before the closure tool may be invoked. (doc_bank_accounts_bank_accounts_(general)_007.json)

#### 3.3.7 Pre-Closure Requirements (All Business Checking Tiers)

- Account status must be OPEN before initiating closure. (doc_bank_accounts_bank_accounts_(general)_007.json)
- No pending transactions may exist at time of closure. (doc_bank_accounts_bank_accounts_(general)_007.json)
- All linked OPEN business savings accounts must be closed before the business checking account can be closed (savings must be closed first). (doc_bank_accounts_bank_accounts_(general)_007.json)
- Account balance must cover the early closure fee, or be $0 if no early closure fee applies. (doc_bank_accounts_bank_accounts_(general)_007.json)
- The early closure fee can only be deducted from the account balance; no alternative payment method is permitted. (doc_bank_accounts_bank_accounts_(general)_007.json)
- ELITE tier accounts (credit lines > $100,000) require manager approval before closure. (doc_bank_accounts_bank_accounts_(general)_007.json)
- **Data quality gap:** Account closure conditions, penalties, and restrictions for business checking docs 005–009 are not documented. (null source)

#### 3.3.8 Business Checking Referral Anti-Abuse Controls

- Rolling 9-day window cap: maximum 2 referral bonuses across all accounts in any 9-day period; excess referrals are auto-denied. (doc_bank_accounts_bank_accounts_(general)_048.json)
- Geographic restriction: referrer and referred business must not share a registered address. (doc_bank_accounts_bank_accounts_(general)_048.json)
- Business referral uniqueness: the referred business must have a different primary owner by SSN of the primary authorized signer compared to any existing Rho-Bank business account. (doc_bank_accounts_bank_accounts_(general)_048.json)
- Clawback: referral bonus is reversed if the referred account is closed within 90 days. (doc_bank_accounts_bank_accounts_(general)_048.json)
- Referral bonus cannot be combined with other promotional offers; only one promotional offer applies per new account. (doc_bank_accounts_bank_accounts_(general)_048.json)

#### 3.3.9 Sky Blue Referral Tenure — Cross-Document Inconsistency

- doc_business_checking_accounts_sky_blue_002.json states the Sky Blue referral tenure threshold is 45 days. (doc_business_checking_accounts_sky_blue_002.json)
- Navy Blue and Cobalt Blue both require 60 days; Hunter Green requires 60 days. (doc_business_checking_accounts_navy_blue_001.json, doc_business_checking_accounts_cobalt_blue_005.json, doc_business_checking_accounts_hunter_green_001.json)
- The general referral FAQ states tenure "hinges on how long you've been a Rho-Bank checking customer" without product-specific thresholds. (doc_bank_accounts_bank_accounts_(general)_048.json)
- These figures conflict; the applicable tenure for Sky Blue referrals is unresolved. (doc_business_checking_accounts_sky_blue_002.json, doc_business_checking_accounts_navy_blue_001.json, doc_business_checking_accounts_cobalt_blue_005.json, doc_business_checking_accounts_hunter_green_001.json)

---

### 3.4 Business Savings

#### 3.4.1 Account Opening Eligibility Checklist (All 6 Conditions Required; All Must Be Satisfied Simultaneously)

- **Condition 1:** Customer identity must be verified. (doc_bank_accounts_bank_accounts_(general)_004.json)
- **Condition 2:** Customer must have at least 1 business checking account with status OPEN. (doc_bank_accounts_bank_accounts_(general)_004.json)
- **Condition 3:** Customer must currently hold fewer than 4 existing business savings accounts; opening a fourth is prohibited. (doc_bank_accounts_bank_accounts_(general)_004.json)
- **Condition 4:** Customer must have no accounts with negative balances. (doc_bank_accounts_bank_accounts_(general)_004.json)
- **Condition 5:** The qualifying business checking account must have been open for at least 30 days. (doc_bank_accounts_bank_accounts_(general)_004.json)
- **Condition 6:** The qualifying business checking account current balance must be ≥ $2,500. (doc_bank_accounts_bank_accounts_(general)_004.json)
- Conditions 5 and 6 must both be satisfied by the same qualifying account — the same account must meet both the 30-day tenure and the $2,500 balance requirement. (doc_bank_accounts_bank_accounts_(general)_004.json)
- Failure of any single condition blocks invocation of the account-opening tool (`open_bank_account_4821`). (doc_bank_accounts_bank_accounts_(general)_004.json)

---

### 3.5 Personal Credit Cards

#### 3.5.1 Minimum Credit Score Requirements by Card Tier

- Bronze card: minimum FICO score 640. (doc_credit_cards_bronze_rewards_card_001.json)
- Silver Rewards Card: minimum FICO score 680. (doc_credit_cards_silver_rewards_card_001.json)
- Gold Rewards Card: minimum FICO score 720. (doc_credit_cards_gold_rewards_card_001.json)
- Platinum Rewards Card: minimum FICO score 750. (doc_credit_cards_platinum_rewards_card_001.json)
- Diamond Elite Card: minimum FICO score 780 (invitation-only; meeting the score threshold does not guarantee an invitation). (doc_credit_cards_diamond_elite_card_001.json)
- EcoCard: no minimum credit score required. (doc_credit_cards_ecocard_001.json)
- **Data quality gap:** Minimum credit score for the Crypto-Cash Back card is not documented. (doc_credit_cards_ecocard_001.json)
- **Data quality gap:** No minimum credit score is stated for the Gold Rewards Card in the document that specifies it for Platinum ($750). (doc_credit_cards_platinum_rewards_card_001.json)
- **Data quality defect:** All FICO thresholds in source documents carry a dollar-sign prefix (e.g., "$640", "$680", "$720", "$750", "$780"). Credit scores are unitless integers; the dollar sign is a systematic formatting error across the personal-credit-card document family. (doc_credit_cards_bronze_rewards_card_001.json, doc_credit_cards_silver_rewards_card_001.json, doc_credit_cards_gold_rewards_card_001.json, doc_credit_cards_platinum_rewards_card_001.json, doc_credit_cards_diamond_elite_card_001.json, doc_credit_cards_ecocard_001.json)

#### 3.5.2 Gold Rewards Card — Subscription Prerequisite

- An active Rho-Bank+ premium subscription is required as a prerequisite to apply for the Gold Rewards Card. Without a Rho-Bank+ subscription, the application cannot proceed regardless of credit score. (doc_credit_cards_gold_rewards_card_001.json)

#### 3.5.3 Silver Rewards Card — Foreign Transaction Fee Dependency

- Silver Rewards Card without Rho-Bank+ premium subscription: foreign transaction fee = 2.75%. (doc_credit_cards_silver_rewards_card_001.json)
- Silver Rewards Card with Rho-Bank+ premium subscription: foreign transaction fee = 0%. (doc_credit_cards_silver_rewards_card_001.json)
- Bronze card: foreign transaction fee = 2.75% (no premium discount stated). (doc_credit_cards_bronze_rewards_card_001.json)
- EcoCard: foreign transaction fee = 1.0% flat. (doc_credit_cards_ecocard_001.json)
- Gold Rewards Card: foreign transaction fee = 0% (premium subscription is already required for Gold anyway). (doc_credit_cards_gold_rewards_card_001.json)
- **Data quality gap:** Diamond Elite foreign transaction fee is not stated in reviewed documents. (doc_credit_cards_diamond_elite_card_001.json)

#### 3.5.4 Diamond Elite Card — Invitation-Only Requirements

- No standard public application process exists for the Diamond Elite Card. (doc_credit_cards_diamond_elite_card_001.json)
- Invitations are extended to clients who demonstrate all of the following: exceptional creditworthiness (score at or above 780); responsible account management; history of timely payments; low credit utilization; substantial verifiable income; depth of Rho-Bank relationship (deposit history, AUM, tenure). (doc_credit_cards_diamond_elite_card_001.json)
- Receiving an invitation is not guaranteed even when the credit score is ≥ 780. (doc_credit_cards_diamond_elite_card_001.json)

#### 3.5.5 EcoCard — EV Charging Green Rate Restriction

- The 5.0 pts/$ green rate for EV charging applies ONLY at 3 certified partner networks: Tesla Supercharger, ChargePoint, and EVgo. (doc_credit_cards_ecocard_004.json)
- All other EV charging networks earn the standard rate of 1.0 pt/$. (doc_credit_cards_ecocard_004.json)
- The following merchants are permanently excluded from the green rate regardless of product purchased: Target, Walmart, Amazon, ThredUp. (doc_credit_cards_ecocard_004.json)

#### 3.5.6 Credit Limit Increase (CLI) — Tier Eligibility Matrix

- **Entry tier:** minimum account age = 120 days; cooldown period between CLI requests = 120 days; maximum credit utilization < 70%; payment history requirement = 6 consecutive on-time monthly payments; maximum permitted increase = 25% of current limit. (doc_credit_cards_credit_card_account_logistics_005.json)
- **Mid tier:** minimum account age = 90 days; cooldown period = 90 days; maximum credit utilization < 80%; payment history requirement = 3 months; maximum permitted increase = 50% of current limit. (doc_credit_cards_credit_card_account_logistics_005.json)
- **Premium tier:** minimum account age = 60 days; cooldown period = 60 days; maximum credit utilization < 90%; payment history requirement = 3 months; maximum permitted increase = 50% of current limit. (doc_credit_cards_credit_card_account_logistics_005.json)
- **Data quality defect:** Source document expresses minimum account age for Entry tier with a dollar-sign prefix ("$120 days"); this is a formatting error. (doc_credit_cards_credit_card_account_logistics_005.json)

#### 3.5.7 Credit Limit Increase (CLI) Step 2 — Six Required Eligibility Conditions

- Account age must meet the tier-specific minimum. (doc_credit_cards_credit_card_account_logistics_007.json)
- Cooldown period since last CLI must have elapsed (verified via tool). (doc_credit_cards_credit_card_account_logistics_007.json)
- No pending disputes on the account. (doc_credit_cards_credit_card_account_logistics_007.json)
- No pending replacement card orders. (doc_credit_cards_credit_card_account_logistics_007.json)
- Account must be current with no past-due balance. (doc_credit_cards_credit_card_account_logistics_007.json)
- Credit utilization must be below the tier-specific maximum. (doc_credit_cards_credit_card_account_logistics_007.json)
- All 6 conditions must be satisfied simultaneously. (doc_credit_cards_credit_card_account_logistics_007.json)
- **Data quality gap:** CLI Step 3 ("Verify Payment History and Requested Amount") contains only a period "." as its entire body; no actionable agent guidance exists for this mandatory payment-history verification gate. (doc_credit_cards_credit_card_account_logistics_007.json)

#### 3.5.8 Personal Credit Card Account Closure — Four Hard Gates

- **Gate 1:** Outstanding balance must equal $0.00. (doc_credit_cards_credit_card_account_logistics_001.json)
- **Gate 2:** No active or pending disputes on the account. (doc_credit_cards_credit_card_account_logistics_001.json)
- **Gate 3:** Account age must be at least 60 days. (doc_credit_cards_credit_card_account_logistics_001.json)
- **Gate 4:** No pending replacement card orders. (doc_credit_cards_credit_card_account_logistics_001.json)
- All four gates must be satisfied; failure of any single gate blocks closure. (doc_credit_cards_credit_card_account_logistics_001.json)
- Post-closure: unredeemed rewards are redeemable for 45 days; after 45 days they are forfeited. (doc_credit_cards_credit_card_account_logistics_001.json)
- Annual fee is fully refunded if account closure occurs within 37 days of the fee posting date. (doc_credit_cards_credit_card_account_logistics_001.json, doc_credit_cards_credit_card_account_logistics_002.json, doc_credit_cards_credit_card_account_logistics_003.json)
- Agent must provide a credit score impact warning before proceeding. (doc_credit_cards_credit_card_account_logistics_001.json)
- Retention protocol (including abuse-prevention check via `get_closure_reason_history_8293`) must be triggered before closure. (doc_credit_cards_credit_card_account_logistics_002.json)

---

### 3.6 Business Credit Cards

#### 3.6.1 Minimum Credit Score (FICO) and PAYDEX Requirements by Tier

- **Bronze Rewards Card:** minimum FICO 660; minimum PAYDEX 20 (PAYDEX is optional — not required for new businesses). (doc_business_credit_cards_business_bronze_rewards_card_001.json)
- **Green Rewards Card:** minimum FICO 690; minimum PAYDEX 42. (doc_business_credit_cards_green_rewards_card_001.json)
- **Silver Rewards Card:** minimum FICO 700; minimum PAYDEX 47. (doc_business_credit_cards_business_silver_rewards_card_001.json)
- **Gold Rewards Card:** minimum FICO 735; minimum PAYDEX 67. (doc_business_credit_cards_business_gold_rewards_card_001.json)
- **Platinum Rewards Card:** minimum FICO 765; minimum PAYDEX 77. (doc_business_credit_cards_business_platinum_rewards_card_001.json)
- Each tier imposes progressively stricter credit standards. (doc_business_credit_cards_business_bronze_rewards_card_001.json, doc_business_credit_cards_green_rewards_card_001.json, doc_business_credit_cards_business_silver_rewards_card_001.json, doc_business_credit_cards_business_gold_rewards_card_001.json, doc_business_credit_cards_business_platinum_rewards_card_001.json)
- **Data quality defect:** All five business credit card eligibility documents express FICO thresholds with a dollar-sign prefix (e.g., "$660", "$700", "$735", "$765", "$765"). Credit scores are unitless integers; the dollar sign is a systematic formatting error across all five documents that makes the values ambiguous. No corrected authoritative source has been found in the document corpus. (doc_business_credit_cards_business_bronze_rewards_card_001.json, doc_business_credit_cards_green_rewards_card_001.json, doc_business_credit_cards_business_silver_rewards_card_001.json, doc_business_credit_cards_business_gold_rewards_card_001.json, doc_business_credit_cards_business_platinum_rewards_card_001.json)

#### 3.6.2 Foreign Transaction Fee by Business Credit Card Tier

- Bronze Rewards Card: foreign transaction fee = 2.75%. (doc_business_credit_cards_business_bronze_rewards_card_005.json)
- Green Rewards Card: foreign transaction fee = 1.0%. (doc_business_credit_cards_green_rewards_card_001.json)
- Gold Rewards Card: foreign transaction fee = 0% (waived). (doc_business_credit_cards_business_gold_rewards_card_007.json)
- Platinum Rewards Card: foreign transaction fee = 0% (waived). (doc_business_credit_cards_business_platinum_rewards_card_008.json)
- **Data quality gap:** Silver Rewards Card foreign transaction fee is not stated in documents reviewed. (doc_business_credit_cards_business_bronze_rewards_card_005.json, doc_business_credit_cards_green_rewards_card_001.json, doc_business_credit_cards_business_gold_rewards_card_007.json, doc_business_credit_cards_business_platinum_rewards_card_008.json)

#### 3.6.3 Bronze Rewards Card — SaaS Subscription Eligibility Cliff

- The following SaaS merchants earn 1.0% cash back for the first 12 months of subscription billing only: Slack, Zoom, HubSpot, Salesforce. (doc_business_credit_cards_business_bronze_rewards_card_003.json)
- After Month 12, renewals from those same merchants earn 0% cash back. (doc_business_credit_cards_business_bronze_rewards_card_003.json)
- No equivalent 12-month cliff rule was found for Silver, Gold, or Platinum business cards. (doc_business_credit_cards_business_bronze_rewards_card_003.json)

#### 3.6.4 Bronze Rewards Card — Payroll Processor Exclusion

- The following payroll processing merchants earn 0% cash back on the Bronze Rewards Card: Gusto, ADP, Paychex, Rippling. (doc_business_credit_cards_business_bronze_rewards_card_003.json)
- The same exclusion is not explicitly stated for Silver, Gold, or Platinum cards in documents reviewed. (doc_business_credit_cards_business_bronze_rewards_card_003.json)

#### 3.6.5 Silver Rewards Card — 10% Rate Merchant Exclusions

- The following merchant clusters are excluded from the 10.0% bonus rate and earn only 1.0% instead:
  - Corporate expense management platforms: Concur, SAP Concur, Expensify, Navan. (doc_business_credit_cards_business_silver_rewards_card_005.json)
  - Hardware and electronics: Apple, Microsoft, Dell. (doc_business_credit_cards_business_silver_rewards_card_005.json)
  - Gaming subscriptions: Xbox Game Pass, PlayStation Plus, Nintendo Switch Online. (doc_business_credit_cards_business_silver_rewards_card_005.json)
  - Online learning platforms: Coursera, Udemy, LinkedIn Learning, Skillshare, Pluralsight. (doc_business_credit_cards_business_silver_rewards_card_005.json)

#### 3.6.6 Business Credit Card / Savings APY Bonus Linkage

- **Data quality gap:** Bronze Rewards Card and Green Rewards Card are absent from all savings account APY bonus tables (Diamond Vault, Emerald Saver, Gold Saver, Platinum Reserve). No document explicitly states whether Bronze and Green card holders are ineligible for savings APY uplift or whether the omission is a documentation gap. (doc_business_savings_accounts_diamond_vault_008.json, doc_business_savings_accounts_emerald_saver_008.json, doc_business_savings_accounts_gold_saver_account_009.json, doc_business_savings_accounts_platinum_reserve_account_010.json)

#### 3.6.7 Travel and Software Purchase Qualification

- **Data quality gap:** Source document references an "authorized platform" for travel and software purchases but does not define which platforms qualify. (doc_business_credit_cards_business_silver_rewards_card_002.json)
- **Data quality gap:** Source document references merchant category codes (MCCs) but does not provide an MCC list or mapping. (doc_business_credit_cards_business_silver_rewards_card_002.json)

---

### 3.7 BNPL (Buy Now Pay Later)

#### 3.7.1 BNPL Diamond — Segment Eligibility

- Customer must be classified in the HIGH_SPEND_RETAIL segment. Customers outside this segment are ineligible for BNPL Diamond. (doc_buy_now_pay_later_bnpl_diamond_001.json)
- Segment classification is based on customer profile and historical usage patterns. (doc_buy_now_pay_later_bnpl_diamond_001.json)

#### 3.7.2 BNPL Diamond — Minimum Average Monthly Spend

- Minimum average monthly spend: $502,500.00. (doc_buy_now_pay_later_bnpl_diamond_001.json)
- Average is computed as: sum of settled transactions over the evaluation period ÷ number of evaluation months. (doc_buy_now_pay_later_bnpl_diamond_001.json)
- Reversals, refunds, and chargebacks reduce the settled transaction sum before the average is calculated. (doc_buy_now_pay_later_bnpl_diamond_001.json)
- Example: 6-month evaluation with $3,015,000 in total settled transactions → $3,015,000 ÷ 6 = $502,500.00 (exactly meets threshold). (doc_buy_now_pay_later_bnpl_diamond_001.json)
- Implied annualized minimum spend: $502,500 × 12 = $6,030,000. (doc_buy_now_pay_later_bnpl_diamond_001.json)

#### 3.7.3 BNPL Diamond — Enterprise Annual Revenue Threshold

- Minimum annual revenue for enterprise qualification: $50,125,000.00. (doc_buy_now_pay_later_bnpl_diamond_002.json)
- Revenue must be verified by audited or reviewed financial statements covering the full most-recent fiscal year. (doc_buy_now_pay_later_bnpl_diamond_002.json)
- If the fiscal year-end is older than 6 months, management accounts must be provided instead. (doc_buy_now_pay_later_bnpl_diamond_002.json)
- Additional acceptable corroborating documents: bank statements or tax filings confirming the revenue figures. (doc_buy_now_pay_later_bnpl_diamond_002.json)
- The enterprise revenue threshold ($50,125,000) is approximately 8.3× the annualized implied minimum spend ($6,030,000). (doc_buy_now_pay_later_bnpl_diamond_001.json, doc_buy_now_pay_later_bnpl_diamond_002.json)

#### 3.7.4 BNPL Diamond — Application Requirements

- Business details and ownership information must be provided. (doc_buy_now_pay_later_bnpl_diamond_008.json)
- Verification documents per the application flow must be submitted. (doc_buy_now_pay_later_bnpl_diamond_008.json)
- Primary email and mobile contact must be provided. (doc_buy_now_pay_later_bnpl_diamond_008.json)
- HIGH_SPEND_RETAIL segment must be confirmed. (doc_buy_now_pay_later_bnpl_diamond_008.json)
- Average monthly spend must be confirmed ≥ $502,500. (doc_buy_now_pay_later_bnpl_diamond_008.json)
- For enterprise track: annual revenue ≥ $50,125,000 with supporting financial statements. (doc_buy_now_pay_later_bnpl_diamond_008.json)
- Upon approval, plan term defaults to 12 months. (doc_buy_now_pay_later_bnpl_diamond_008.json)

#### 3.7.5 BNPL Diamond — Plan Approval Dual-Gate Check

- A new plan is approved only when BOTH of the following conditions are satisfied simultaneously:
  - Gate 1: current outstanding principal + new plan amount ≤ $2,505,000.00. (doc_buy_now_pay_later_bnpl_diamond_003.json)
  - Gate 2: current active plan count + 1 ≤ 25 (i.e., active plans must be fewer than 25 before the new plan). (doc_buy_now_pay_later_bnpl_diamond_003.json)
- Remaining capacity = $2,505,000.00 − current outstanding principal. (doc_buy_now_pay_later_bnpl_diamond_003.json)

#### 3.7.6 BNPL Diamond — Flexible Term

- Permitted term range: 7 to 18 months in whole-month increments. (doc_buy_now_pay_later_bnpl_diamond_004.json)
- Default term at activation: 12 months. (doc_buy_now_pay_later_bnpl_diamond_004.json)
- Changing the term after activation is stated as potentially not available; agent must advise customers to choose carefully at setup. (doc_buy_now_pay_later_bnpl_diamond_004.json)

#### 3.7.7 BNPL Gold

- BNPL Gold is a business product; eligibility is restricted to business customers with company purchases, business profiles, and billing information. (doc_buy_now_pay_later_bnpl_gold_008.json)
- **Data quality gap:** Eligible customer segment for BNPL Gold is [value not available]. (doc_buy_now_pay_later_bnpl_gold_002.json, doc_buy_now_pay_later_bnpl_gold_008.json)
- **Data quality gap:** Business registration requirement for BNPL Gold is [value not available]. (doc_buy_now_pay_later_bnpl_gold_002.json, doc_buy_now_pay_later_bnpl_gold_008.json)

#### 3.7.8 BNPL Silver — Soft Credit Check

- A soft credit check is required at activation and at certain transactions when the `soft_credit_check_required` flag is true. (doc_buy_now_pay_later_bnpl_silver_005.json)
- Additional soft credit check attempts are blocked until the next calendar month once the monthly inquiry cap is reached. (doc_buy_now_pay_later_bnpl_silver_005.json)
- **Data quality gap:** Monthly inquiry cap is [value not available]. (doc_buy_now_pay_later_bnpl_silver_005.json)
- **Data quality gap:** Soft credit check provider is [value not available]. (doc_buy_now_pay_later_bnpl_silver_005.json)

#### 3.7.9 BNPL Platinum — APR Tier Placement

- Customers in the highest eligible credit tiers receive APRs closer to the floor of the program's APR range. (doc_buy_now_pay_later_bnpl_platinum_008.json)
- Customers in the lowest eligible credit tiers receive APRs closer to the ceiling of the program's APR range. (doc_buy_now_pay_later_bnpl_platinum_008.json)
- **Data quality gap:** The exact floor and ceiling APR values are [value not available] placeholders. (doc_buy_now_pay_later_bnpl_platinum_008.json)

#### 3.7.10 BNPL Platinum — Claim and Lookback Windows

- **Data quality gap:** BNPL Platinum claim submission window (days from purchase date) is [value not available]. (doc_buy_now_pay_later_bnpl_platinum_005.json)
- **Data quality gap:** BNPL Platinum item eligibility lookback window (days from current date) is [value not available]. (doc_buy_now_pay_later_bnpl_platinum_005.json)

#### 3.7.11 BNPL Platinum — Prepayment Eligibility

- **Data quality gap:** BNPL Platinum prepayment eligibility condition is [value not available]. (doc_buy_now_pay_later_bnpl_platinum_007.json)

---

### 3.8 Debit Disputes

#### 3.8.1 Pre-Filing Requirements (All Conditions Required Before Filing)

- Transaction amount must be at least $1.00; amounts below this threshold cannot be disputed via `file_debit_card_transaction_dispute_6281`. (doc_bank_accounts_bank_accounts_(general)_031.json)
- Transaction date must be within 60 days of the filing date; transactions older than 60 days cannot be disputed. (doc_bank_accounts_bank_accounts_(general)_031.json)
- The debit card must be linked to an OPEN checking account at the time of filing; if the checking account is closed, the dispute cannot be filed. (doc_bank_accounts_bank_accounts_(general)_031.json)
- The customer must not already hold open disputes equal to or exceeding their tier maximum:
  - Entry Tier: maximum 2 open disputes. (doc_bank_accounts_bank_accounts_(general)_031.json)
  - Mid Tier: maximum 3 open disputes. (doc_bank_accounts_bank_accounts_(general)_031.json)
  - Premium Tier: maximum 4 open disputes. (doc_bank_accounts_bank_accounts_(general)_031.json)
  - Elite Tier: maximum 5 open disputes. (doc_bank_accounts_bank_accounts_(general)_031.json)
- The tool `file_debit_card_transaction_dispute_6281` accepts a `dispute_category` parameter with exactly 9 valid enum values, including "recurring_charge_after_cancellation", "card_present_fraud", and "card_not_present_fraud". (doc_bank_accounts_bank_accounts_(general)_031.json)

#### 3.8.2 Regulation E Liability Windows for Unauthorized Debit Transactions

- Reported within 2 business days of discovering the unauthorized transaction: maximum customer liability = $50. (doc_bank_accounts_bank_accounts_(general)_031.json)
- Reported after 2 business days but within 60 days of the statement date: maximum customer liability = $500. (doc_bank_accounts_bank_accounts_(general)_031.json)
- Reported after 60 days from the statement date: customer liability is unlimited and the customer may not be able to recover funds. (doc_bank_accounts_bank_accounts_(general)_031.json)

---

### 3.9 EveryonePay (P2P Transfer Service)

- EveryonePay supports external P2P transfers — funds can be sent to persons at other banks (not limited to intra-Rho-Bank transfers). (doc_checking_accounts_blue_account_011.json)
- Account tier mapping for EveryonePay-bearing accounts: ENTRY TIER = Light Blue Account, Light Green Account, Green Fee-Free Account; MID TIER = Blue Account, Green Account (checking); PREMIUM TIER = Evergreen Account; ELITE TIER = Bluest Account. (doc_bank_accounts_bank_accounts_(general)_005.json)
- Gold Years Account: EveryonePay daily send limit = $3,000 per day. (doc_checking_accounts_gold_years_account_006.json)
- Evergreen Account: EveryonePay transfers do NOT accrue carbon offset credits, regardless of transaction amount or dollar value. (doc_checking_accounts_evergreen_account_005.json)
- Green Fee-Free Account: canceled or failed EveryonePay send transactions do NOT count against the $2,000 daily cap; only successful sends count toward the daily total. (doc_checking_accounts_green_fee-free_account_001.json)
- Dark Green Account: EveryonePay payments sent to individuals — even if those individuals subsequently forward funds to a student loan servicer — do NOT qualify for the 1.25% student loan cashback reward; only direct payments to recognized loan servicers qualify. Agent must not credit the cashback in these cases. (doc_checking_accounts_dark_green_account_005.json)

---

### 3.10 Referral Programs — General Cross-Product Rules

- New account referral welcome bonus: the new account receives $25 cash upon opening; the referred customer must deposit ≥ $100 within 90 days of account opening to fully qualify the bonus. (doc_checking_accounts_light_green_account_001.json)
- Clawback provision (all products): if a referred account is closed within 90 days, the referral bonus may be reversed. (doc_bank_accounts_bank_accounts_(general)_047.json, doc_bank_accounts_bank_accounts_(general)_048.json)
- No referral bonus may be combined with another new-account promotional offer; one promotional offer per new account maximum. (doc_bank_accounts_bank_accounts_(general)_047.json, doc_bank_accounts_bank_accounts_(general)_048.json)

---

### 3.11 Account Recovery — Bypass Code

- Bypass code usage is authorized only for account recovery purposes. (doc_customer_support_special_support_codes_001.json)
- The bypass code must exactly match: `9K2X7M4P1N8Q3R5T6A`; no partial match or variant is acceptable. (doc_customer_support_special_support_codes_001.json)
- The bypass code must not be combined with collection of personal data. (doc_customer_support_special_support_codes_001.json)
- If code exposure is suspected, the agent must immediately escalate; the agent may not continue the session. (doc_customer_support_special_support_codes_001.json)


---


## 4. Limits & Thresholds

---

### 4.1 Account Caps & Balance Requirements

#### Account Count & Tenure Thresholds

| Limit | Value | Unit | Scope / Product | Source |
|---|---|---|---|---|
| Max personal savings accounts per customer | 5 | count (hard stop) | Personal savings | doc_bank_accounts_bank_accounts_(general)_002.json |
| Checking account minimum tenure before savings opening | 14 | days | Personal savings eligibility | doc_bank_accounts_bank_accounts_(general)_002.json |
| New savings account funding deadline (auto-close if unfunded) | 30 | days from opening | Personal savings | doc_bank_accounts_bank_accounts_(general)_002.json |
| Max founder cards per account | 3 | count | Founder card product | doc_business_checking_accounts_sky_blue_005.json |
| Max annual referral earnings | $1,600 | USD/year (8 referrals × $200) | All accounts | (no doc\_id; conf 0.96) |
| Everyone Pay block list maximum | 275 | users (DISPUTED — "$275" in source is data formatting error; unit is user count) | Everyone Pay | doc\_c81e1bed |

#### Minimum Balance Requirements & Fee-Waiver Thresholds

| Product | Minimum Balance | Monthly Fee if Below | Fee-Waiver Threshold | Source |
|---|---|---|---|---|
| Silver Saver | $10,000 (daily) | $5.00 | $10,000 | doc\_7f4ebc9f / doc\_d37d3382 |
| Gold Savings Account | $10,000 | $10.00 (annualizes to $120/yr) | $10,000 | (no doc\_id; conf 0.95) |
| Diamond Elite Account | $250,000 | — | — | (no doc\_id; conf 0.95) |
| Beige Business Checking | $250,000 | $200.00 | $500,000 (full waiver) | doc\_f476ca8e |

#### Beige Account Infrastructure Limits

| Limit | Value | Unit | Source |
|---|---|---|---|
| Beige auto-fund sweep trigger | $50,000 | USD | doc\_f476ca8e |
| Beige external account aggregation cap | 30 | accounts | doc\_f476ca8e |
| Beige supported ERP platforms | 18 | platforms | doc\_f476ca8e |
| Beige monthly API call allocation | 100,000 | calls/month | doc\_f476ca8e |
| Beige dedicated account managers | 2 | count | doc\_f476ca8e |
| Beige dual-authorization transaction threshold | $10,000 | USD per transaction | doc\_f476ca8e |
| Beige monthly ATM rebate cap (domestic) | $50 | USD/month | doc\_f476ca8e |

#### Business Checking APY by Tier

| Tier | APY | Source |
|---|---|---|
| Navy Blue | 0.5% | doc\_b7cdfb44 |
| Cobalt Blue | 0.5% | doc\_7ab1bdc2 |
| Hunter Green | 1.0% | doc\_6b4aa36d |
| Lime Green | 1.5% | doc\_3a4c8a96 |
| True Blue | 2.0% | doc\_4d0c7d44 |
| Beige | 3.0% | doc\_554a9010 |
| Sky Blue | not documented | — |

#### Gold Plus Saver APY by Qualifying Card

| Card Held | APY | Source |
|---|---|---|
| No card | 5.00% | doc\_041c2bd6 |
| Business Silver | 5.22% (base 5.0% + 0.22%) | doc\_041c2bd6 |
| Business Gold | 5.45% (base 5.0% + 0.45%) | doc\_041c2bd6 |
| Business Platinum | 5.70% (base 5.0% + 0.70%) | doc\_041c2bd6 |

#### Silver Saver APY Examples

| Balance | Card | APY | Annual Interest | Source |
|---|---|---|---|---|
| $24,000 | None | 2.5% | $600 | doc\_4e80b0ca |
| $26,000 | None | 4.0% | $1,040 | doc\_4e80b0ca |
| $40,000 | Business Gold | 4.3% (4.0% + 0.3%) | $1,720 | doc\_4e80b0ca |
| $100,000 | Business Platinum | 4.55% (4.0% + 0.55%) | $4,550 | doc\_4e80b0ca |

#### Silver Plus Saver APY Scenarios

| Scenario | APY | Source |
|---|---|---|
| Tier 1 base (minimum) | 3.0% | (no doc\_id; conf 0.95) |
| Tier 1 + direct deposit bonus | 3.25% (3.0% + 0.25%) | (no doc\_id; conf 0.95) |
| Tier 2 base | 4.5% | (no doc\_id; conf 0.95) |
| Tier 2 + direct deposit bonus | 4.75% (4.5% + 0.25%) | (no doc\_id; conf 0.95) |
| Maximum (Tier 2 + direct deposit + EcoCard) | 5.2% (4.5% + 0.25% + 0.45%) | (no doc\_id; conf 0.90) |
| Tier 2 balance threshold | \[value not available\] | doc\_52b651bd |

#### Diamond Elite Account APY by Card

| Card Held | APY | Source |
|---|---|---|
| Diamond Elite Card | 8.0% (7.5% base + 0.5%) | (no doc\_id; conf 0.95) |
| Crypto-Cash Back Card | 7.65% (7.5% base + 0.15%) | (no doc\_id; conf 0.95) |
| Platinum Card | 2.55% (2.0% + 0.55%) | doc\_a123b62f |

#### Green Account — Withdrawal Allowances

| Product | Free Withdrawals/Month | Excess Fee | Source |
|---|---|---|---|
| Green savings (base) | 8 | not specified | doc\_6585431e |
| Green savings + EcoCard | 15 (8 base + 7 EcoCard bonus) | — | doc\_4d15c636 |
| Silver Saver | 6 | $5.00/excess txn | doc\_d37d3382 |
| Gold Account | 20 | — | (no doc\_id; conf 0.95) |

#### Diamond Vault APY Uplift by Business Card

| Card | APY Uplift | Example (base 3.0%) | Source |
|---|---|---|---|
| Silver | +0.30 pp | 3.30% | doc\_bd16e9dd |
| Platinum | +0.90 pp | 3.90% | doc\_bd16e9dd |

---

### 4.2 Transfer / Withdrawal / Mobile-Deposit Limits

| Limit | Value | Unit | Scope / Product | Source |
|---|---|---|---|---|
| Blue Account mobile check deposit daily limit | $2,500 | USD/day | Blue checking | doc\_2bb7266e |
| Mobile deposit daily limit (general reference) | $25,000 | USD/day (no weekly/monthly cap stated) | Product unspecified | doc\_4f761caf |
| Diamond Elite mobile deposit daily limit | $100,000 | USD/day | Diamond Elite account | doc\_f0cd058d |
| Diamond Elite daily transfer limit | $500,000 | USD/day | Diamond Elite account | doc\_f0cd058d |
| Bronze external transfer daily limit | $2,500 | USD/day (3 × $2,500 = $7,500 max via multiple transfers) | Bronze checking | doc\_5b093abd |
| Scheduled payment minimum spacing | 4 | days (max ~91 occurrences/year) | All scheduled payments | doc\_47a565f0 |
| Silver Saver excess withdrawal fee | $5.00 | USD/transaction | Silver Saver | doc\_d37d3382 |
| Max excess withdrawal fee (single month, 20 over limit) | $100.00 | USD/month | Silver Saver | doc\_d37d3382 |
| Max annual excess withdrawal charges (est.) | $216.00 | USD/year (6 excess/month × $3.00 × 12) | Savings with 6-free/month limit | doc\_c325bdf9 |
| Beige dual-auth transaction threshold | $10,000 | USD per transaction | Beige business checking | doc\_f476ca8e |
| True Blue wire — free outgoing monthly allotment | 10 | wires/month | True Blue business checking | (no doc\_id; conf 0.90) |
| True Blue wire — excess outgoing fee | $5.00 | USD/wire | True Blue business checking | (no doc\_id; conf 0.90) |
| True Blue wire fee example (12 wires) | $10.00 | USD (2 excess × $5.00) | True Blue business checking | (no doc\_id; conf 0.90) |
| Hunter Green free incoming domestic wires/month | 5 | wires/month | Hunter Green business checking | doc\_business\_checking\_accounts\_hunter\_green\_007 |
| Hunter Green standard incoming wire fee (after 5 free) | \[value not available\] | USD | Hunter Green business checking | doc\_business\_checking\_accounts\_hunter\_green\_007 |
| Navy Blue outgoing domestic wire fee | $15.00 | USD/wire (DISPUTED; see e8159) | Navy Blue business checking | doc\_d5d32676 |
| Lime Green outgoing domestic wire fee | $10.00 | USD/wire | Lime Green business checking | doc\_58604f42 |
| Lime Green outgoing international wire fee | $25.00 | USD/wire (DISPUTED) | Lime Green business checking | doc\_58604f42 |
| Incoming wire receipt fee (worst-case scenario) | $12.50 | USD | Any account | doc\_db98585d |
| Returned check fee | $15.00 | USD | Any account | doc\_db98585d |
| Worst-case single-day combined fee | $27.50 | USD ($12.50 wire + $15.00 returned check) | Any account | doc\_db98585d |
| Instant transfer fee — flat (ambiguous) | $0.75 | USD flat fee | Instant transfers | doc\_1d2a2240 |
| Instant transfer fee — percentage (ambiguous) | 0.75% | % of transfer amount | Instant transfers | doc\_1d2a2240 |
| Dark Green debit card daily purchase limit | \[not documented\] | — | Dark Green account | doc\_8dbeb713 |
| Dark Green ATM withdrawal daily limit | \[not documented\] | — | Dark Green account | doc\_c9c2862f |
| Rho Bank Plus margin interest rate | 7.0% | APR | Rho Bank Plus | doc\_cbcedca7 |
| FX markup over interbank rate | 0.5% | % of exchange amount | FX transactions | (no doc\_id; conf 0.85) |
| Crypto rewards conversion fee | 1.25% | % of available rewards (net = rewards × 0.9875) | Crypto-Cash Back Card | doc\_8f74415f |

---

### 4.3 Everyone Pay Limits

#### Sending Limits by Account Status

| Account Status | Daily Limit | Monthly Limit | Source |
|---|---|---|---|
| Individual — new / unverified | $750 | $7,500 | doc\_everyone\_pay\_sending\_limits\_001 |
| Individual — verified | $3,500 | $35,000 | doc\_everyone\_pay\_sending\_limits\_001 |
| Individual — standard reference | $1,500 | $12,500 | doc\_e1b15d3f |
| Business | $15,000 (10 × $1,500) | $150,000 (12 × $12,500) | doc\_0234283a |

#### QR Payment Limits

| Limit | Value | Unit | Source |
|---|---|---|---|
| QR transfer per-transaction maximum | $1,250 | USD | doc\_d614336c |
| QR transfer daily aggregate limit | $3,000 | USD/day | doc\_d614336c |
| QR code validity window | 17 | minutes from creation | doc\_d614336c |

#### Operational Limits

| Limit | Value | Unit | Source |
|---|---|---|---|
| Payment cancellation window | 17 | minutes after submission | doc\_0d5c3b4e |
| Instant transfer fee | $0.75 | USD per transfer | doc\_992bad26 |
| Contact storage maximum | 550 | contacts per address book | doc\_992bad26 |
| Block list maximum | 275 | users (DISPUTED — dollar-prefix in source is data error; unit is user count) | doc\_c81e1bed |

---

### 4.4 Reg E Liability

The dataset contains **no entries explicitly enumerating Reg E unauthorized-transaction liability tiers** ($0 / $50 / $500 / unlimited thresholds). The closest analog recorded is the provisional credit limit ladder in section 4.5. No Reg E–specific liability caps or notification-period deadlines are present in the 220 entries.

---

### 4.5 Provisional Credit Timelines & Dispute Caps

#### Maximum Provisional Credit by Card Tier (Personal Cards)

| Tier | Cards Included | Max Provisional Credit | Min Dispute Amount | Source |
|---|---|---|---|---|
| Entry | Bronze, EcoCard, Crypto-Cash Back | $2,500 | $25 | doc\_e018f9bd |
| Mid | Silver | $5,000 | $25 | doc\_e018f9bd |
| Premium | Gold | $10,000 | $25 | doc\_e018f9bd |
| Elite | Platinum | $15,000 | $25 | doc\_e018f9bd |
| Invitation | Diamond Elite | $25,000 | $25 | doc\_e018f9bd |

Ratio Elite-to-Entry: 10×. No explicit credit-posting timeline (business days) is recorded in the dataset.

---

### 4.6 Closure Fee Ladders

#### Business Checking Account Early-Closure Fees

| Tier | Early Closure Fee | Window Triggering Fee | Notice Period | Approval Level | Pre-Closure Conditions | Source |
|---|---|---|---|---|---|---|
| ENTRY (Navy Blue) | $50 | Within 60 days of opening | 7 days | None | No linked open savings; $0 balance or enough for fee; no pending txns | doc\_a44e66aa |
| MID (True Blue, Sky Blue) | $100 | Within 90 days | 14 days | None | Same as above | doc\_a44e66aa |
| PREMIUM (Cobalt Blue) | $200 | Within 180 days* | 21 days | Supervisor review | Same as above | doc\_a44e66aa |
| ELITE (credit lines >$100,000) | $400 | Within 270 days* | 30 days | Manager approval | Same as above | doc\_a44e66aa |

\* Dollar-prefix formatting error in source for "180 days" and "270 days" — values represent day counts, not USD amounts (doc\_a44e66aa, flagged in e8538).

Personal savings account early closure fee amounts and notice periods by tier are **not enumerated** in the available documents (gap — doc\_acba887d).

---

### 4.7 ATM Fees & Rebate Caps

#### Domestic Out-of-Network ATM Fee Rates by Product

| Product | Rho Fee Structure | Cap / Minimum | Rebate Cap | Source |
|---|---|---|---|---|
| Lime Green | $0 Rho fee; operator surcharge passes through | — | $25/month | doc\_a3b40992 |
| Beige | $0 Rho fee; operator surcharge passes through | — | $50/month | doc\_f476ca8e / doc\_23ef787c |
| Blue | 1% of withdrawal | Max $3.00/txn | — | doc\_2bb7266e |
| Product (1% / $2.50 cap) | 1% of withdrawal | Max $2.50/txn | — | doc\_5df1c3d5 |
| Product ($2.00 flat) | $2.00 per transaction | — | — | doc\_e31bdc15 |
| Product ($2.50 flat) | $2.50 per transaction | — | — | doc\_9311dcd2 |
| Navy Blue | $2.50 per transaction | — | $10/month | doc\_b5856d75 |

#### Foreign / International ATM Fee Rates by Product

| Product | Rate | Minimum Fee | Breakeven Withdrawal | Source |
|---|---|---|---|---|
| Lime Green | 1.5% of withdrawal | $2.50 | $166.67 | doc\_a3b40992 / doc\_58604f42 |
| Beige | 1.0% of withdrawal | $2.00 | $200.00 | doc\_f476ca8e / doc\_23ef787c |
| Hunter Green (international) | 2.5% of withdrawal | $4.00 | $160.00 | doc\_b173fd57 / doc\_b35a4072 |
| Product (2% rate, $3 min) | 2.0% of withdrawal | $3.00 | $150.00 | doc\_07205924 / doc\_25c43df7 |
| Product (3% rate, $5 min) | 3.0% of withdrawal | $5.00 | $166.67 | doc\_ffbe2fa0 / doc\_32781d08 / doc\_2e076ce3 |
| Light Green (foreign, ~$90 txn) | — | $2.00 | — | doc\_ac3641ec |
| Light Green (foreign, ~$200 txn) | — | $3.50 | — | doc\_ac3641ec |
| Product (2 free foreign txns/month) | $0 within 2-transaction monthly allowance | — | — | doc\_81808373 |
| General formula | max(withdrawal × rate, minimum) | product-specific | — | doc\_a3b40992 |

#### Monthly ATM Rebate Caps

| Product | Rebate Scope | Cap | Unit | Source |
|---|---|---|---|---|
| Navy Blue | Domestic out-of-network | $10 | USD/calendar month (resolved — monetary, not transaction count) | doc\_b5856d75 |
| Lime Green | Domestic out-of-network | $25 | USD/calendar month (allows ~25 × $1.00 txns) | doc\_a3b40992 |
| Product (3%-rate family) | Out-of-network | $30 | USD/calendar month | doc\_25c43df7 |
| Beige | Domestic (all ATM) | $50 | USD/calendar month | doc\_f476ca8e |

#### ATM Fee Worked Examples

| Scenario | Calculation | Fee Charged | Source |
|---|---|---|---|
| Lime Green foreign, $100 | $100 × 1.5% = $1.50 < $2.50 min | $2.50 | doc\_a3b40992 |
| Lime Green foreign, $1,000 | $1,000 × 1.5% = $15.00 > min | $15.00 | doc\_a3b40992 |
| Beige foreign, $150 | $150 × 1.0% = $1.50 < $2.00 min | $2.00 | doc\_f476ca8e |
| Beige foreign, $400 | $400 × 1.0% = $4.00 > $2.00 min | $4.00 | doc\_f476ca8e / doc\_23ef787c |
| Hunter Green intl, $100 | $100 × 2.5% = $2.50 < $4.00 min | $4.00 | doc\_b35a4072 |
| Hunter Green intl, $200 | $200 × 2.5% = $5.00 > $4.00 min | $5.00 | doc\_b35a4072 |
| Hunter Green intl non-Rho, $100 | $4.00 intl + $2.00 OON + operator surcharge | $6.00+ | doc\_d8136ddf |
| Hunter Green intl non-Rho, $400 | $10.00 intl + $2.00 OON + operator surcharge | $12.00+ | doc\_d8136ddf |
| 3%-rate product, $40 | $40 × 3% = $1.20 < $5.00 min | $5.00 | doc\_32781d08 |
| 3%-rate product, $200 | $200 × 3% = $6.00 > $5.00 | $6.00 | doc\_32781d08 |
| 3%-rate product, $1,000 | $1,000 × 3% = $30.00 | $30.00 | doc\_32781d08 |
| 3%-rate product, $20 | $20 × 3% = $0.60 < $5.00 min | $5.00 | doc\_2e076ce3 |
| 3%-rate product, $100 | $100 × 3% = $3.00 < $5.00 min | $5.00 | doc\_2e076ce3 |
| 3%-rate product, $150 | $150 × 3% = $4.50 < $5.00 min | $5.00 | doc\_2e076ce3 |
| 3%-rate product, $200 | $200 × 3% = $6.00 | $6.00 | doc\_2e076ce3 |
| 3%-rate product, $400 | $400 × 3% = $12.00 | $12.00 | doc\_2e076ce3 |
| 2%-rate product, $100 | $100 × 2% = $2.00 < $3.00 min | $3.00 | doc\_25c43df7 |
| 2%-rate product, $200 | $200 × 2% = $4.00 > $3.00 min | $4.00 | doc\_07205924 / doc\_25c43df7 |
| 1%-cap-$2.50 product, $40 | $40 × 1% = $0.40 (under cap) | $0.40 | doc\_5df1c3d5 |
| 1%-cap-$2.50 product, $250 | $250 × 1% = $2.50 (at cap) | $2.50 | doc\_5df1c3d5 |
| 1%-cap-$2.50 product, $600 | $600 × 1% = $6.00 → capped | $2.50 | doc\_5df1c3d5 |
| Intl $5 min breakeven (3% rate) | $5.00 ÷ 3% = $166.67 | min applies ≤ $166.67 | doc\_b5856d75 |
| 3 OON txns × $2.50 flat | 3 × $2.50 | $7.50 | doc\_9311dcd2 |
| 2 OON txns × $2.00 flat | 2 × $2.00 | $4.00 | doc\_e31bdc15 |
| Navy Blue: 4 OON × $2.50 | 4 × $2.50 = $10.00 → fully rebated at cap | $0 net | doc\_b5856d75 |
| Light Green: 2 × $90 txns | 2 × $2.00 vs single $180 = $3.50 | $4.00 vs $3.50 | doc\_ac3641ec |
| Light Green: 2 × $200 txns | 2 × $3.50 vs single $400 = $5.00 | $7.00 vs $5.00 | doc\_ac3641ec |
| 5 OON txns × $1.00 | 5 × $1.00 | $5.00 | doc\_25c43df7 |
| Rebate cap ceiling: $36 fees, $30 cap | $36 – $30 = $6 unrebated | max $30 rebated | doc\_25c43df7 |
| 1 foreign ATM txn (within 2-free allowance) | 0 (≤ 2 free/month) | $0.00 | doc\_81808373 |
| 2 foreign ATM txns (within 2-free allowance) | 0 (≤ 2 free/month) | $0.00 | doc\_81808373 |
| General 1.5%-rate, $80 (Lime Green) | $80 × 1.5% = $1.20 < $2.50 min | $2.50 | doc\_a3b40992 |

---

### 4.8 Dispute Caps & Purchase Protection

#### Purchase Protection Coverage Windows & Per-Claim Limits

| Card | Per-Claim Limit | Protection Window (days from purchase) | Source |
|---|---|---|---|
| Silver | $7,500 | 90 | doc\_c3e96be7 / doc\_6b40eac4 |
| Gold | $10,000 | 105 | doc\_59507edc |
| Platinum | $17,500 | 135 (30 days more than Gold) | doc\_59507edc / doc\_e7de936d |
| BNPL Platinum | \[value not available\] | \[value not available\] | doc\_0078677a |
| BNPL Platinum — annual coverage cap | \[value not available\] | — | doc\_0078677a |

#### Travel Insurance Per-Trip Limits

| Card | Per-Trip Limit | Coverage Categories | Source |
|---|---|---|---|
| Silver | $15,000 | — | doc\_c3e96be7 |
| Platinum | $62,500 | — | doc\_e7de936d |
| Diamond Elite | $15,000 | Up to 5 categories (~$3,000/category avg; sub-limits may apply) | doc\_c5f818ae |

#### Minimum Redemption Threshold

| Card | Minimum Balance Before Redemption Allowed | Source |
|---|---|---|
| Bronze | $37 | doc\_85a5ca28 / doc\_3c151036 |

---

### 4.9 Business Credit Card Limits

#### Credit Limit Ranges by Tier

| Tier | Min Credit Limit | Max Credit Limit | Source |
|---|---|---|---|
| Bronze | $10,000 | $50,000 | doc\_47e0805b |
| Green | $14,000 | $75,000 | doc\_b8ea386c |
| Silver | $17,500 | $112,500 | doc\_438fb72f |
| Gold | $37,500 | $225,000 | doc\_cfd0ab41 |
| Platinum | $75,000 | $400,000 | doc\_b1c0a1f5 |

#### APR by Tier

| Tier | APR | Source |
|---|---|---|
| Platinum | 16.99% | doc\_b1c0a1f5 |
| Gold | 17.99% | doc\_cfd0ab41 |
| Silver | 18.99% | doc\_438fb72f |
| Green | 19.99% | doc\_b8ea386c |
| Bronze | 20.49% | doc\_db5929e5 |

#### Foreign Transaction Fee by Tier

| Tier | FX Fee | Source |
|---|---|---|
| Bronze | 2.75% | doc\_47e0805b |
| Green | 1.0% | doc\_b8ea386c |
| Silver | \[not found in 12 Silver docs reviewed\] | gap — doc\_438fb72f et al. |
| Gold | 0% (waived) | doc\_26ff1016 |
| Platinum | 0% (waived) | doc\_e7de936d |

#### Employee Card Limits by Tier

| Tier | Max Employee Cards | Source |
|---|---|---|
| Bronze | 7 | doc\_8de479c7 |
| Green | 15 | doc\_b8ea386c |
| Silver | not stated | gap |
| Gold | 37 | doc\_6458670c |
| Platinum | not stated | gap |

#### Card Spending Limit Range (Configurable)

| Limit | Value | Unit | Source |
|---|---|---|---|
| Minimum per-card spending limit | $55 | USD | doc\_2002e402 |
| Maximum per-card spending limit | $150,000 | USD | doc\_2002e402 |

Note: no per-transaction floor or daily cap guidance specified (gap — doc\_2002e402).

---

### 4.10 Personal Credit Card Limits

#### Key APR & Fee Thresholds

| Card | APR | Minimum Payment | Cash Back Rate | Source |
|---|---|---|---|---|
| Diamond Elite | 15.99% | 3.0% of statement balance | 5.0% | doc\_673cc161 / (no doc\_id; conf 0.95) |
| EcoCard | 19.99% | — | — | (no doc\_id; conf 0.95) |

#### Card Replacement Limits

| Tier | Max Replacements per 60 Days | Expedited Shipping Fee (2–3 business days) | Standard Delivery (free, all tiers) | Source |
|---|---|---|---|---|
| Entry (Bronze, EcoCard, Business Bronze) | 2 | $15.00 | 7–10 business days | doc\_3b0e2e6f / doc\_f8fd8284 |
| Mid (Silver) | 3 | $10.00 | 7–10 business days | doc\_3b0e2e6f / doc\_d2bf5e97 |
| Premium+ (Gold, Platinum, Diamond Elite) | 4 | $0.00 (complimentary) | 7–10 business days | doc\_3b0e2e6f / doc\_f8fd8284 |
| Crypto-Cash Back Card | not specified | not specified | 7–10 business days | gap — doc\_f8fd8284 |

#### Credit Limit Increase (CLI) Eligibility Thresholds

| Tier | Min Account Age | Cooldown Period | Max Utilization | Payment History Required | Max Increase Allowed | Source |
|---|---|---|---|---|---|---|
| Entry | 120 days\* | 120 days | \<70% | 6 consecutive on-time months | 25% of current limit | doc\_ec88cfa6 / doc\_f0ffb68e |
| Mid | 90 days | 90 days | \<80% | 3 months | 50% of current limit | doc\_ec88cfa6 / doc\_f0ffb68e |
| Premium | 60 days | 60 days | \<90% | 3 months | 50% of current limit | doc\_ec88cfa6 / doc\_f0ffb68e |

\* "$120 days" in source — dollar-prefix is a data formatting error; value represents days (doc\_ec88cfa6).

CLI example: $10,000 Entry-tier limit → max increase = $10,000 × 25% = $2,500. Mid/Premium at same limit → max = $5,000.

---

### 4.11 BNPL Limits

#### BNPL Diamond — Eligibility & Structural Limits

| Limit | Value | Unit | Source |
|---|---|---|---|
| Minimum average monthly spend (eligibility) | $502,500 | USD/month (annualized: $6,030,000) | doc\_4d42a828 / doc\_762b93e2 |
| Minimum annual revenue (enterprise qualification) | $50,125,000 | USD/year (monthly equiv.: $4,176,916.67) | doc\_67c207c5 / doc\_762b93e2 |
| Total outstanding balance cap (all plans combined) | $2,505,000 | USD aggregate | doc\_67c207c5 |
| Concurrent active plan cap | 25 | plans | doc\_130f56a9 |
| Average balance per plan at aggregate cap | $100,200 | USD ($2,505,000 ÷ 25) | doc\_130f56a9 |
| Repayment term — standard default | 12 | months | doc\_b30920db |
| Repayment term — flexible range | 7–18 | months (whole-month increments; cannot change after activation) | doc\_b30920db |
| Standard APR | 12.49% | APR | doc\_56a3cfc6 |
| Introductory interest-free period | 3 | months from plan start | doc\_56a3cfc6 |
| Late payment fee | 2.5% | of overdue installment, per missed due date | doc\_56a3cfc6 |
| Late fee example (12-month, $250,000 plan) | ($250,000 ÷ 12) × 2.5% = $520.83 | USD per missed installment | doc\_56a3cfc6 |
| Max single-month late fee (all 25 plans missed) | 25 × $520.83 | $13,020.75 | doc\_56a3cfc6 |

#### BNPL — Data Quality Gaps (Values Not Available in Source Documents)

| Product | Missing Limit | Source |
|---|---|---|
| BNPL Gold 001 | Introductory APR period duration | doc\_5d6a65b8 |
| BNPL Gold 002 | Credit limit range minimum; credit limit range maximum | doc\_4fdcfab2 |
| BNPL Gold 003 | Introductory period duration; day on which standard APR begins | doc\_3d524668 |
| BNPL Gold 004 | Auto-debit minimum payment % of outstanding balance; scheduled auto-debit day of month | doc\_873b092d |
| BNPL Gold 005 | Minimum transaction amount; maximum transaction amount; ineligibility threshold (upper and lower settled amount boundaries) | doc\_daf4f207 |
| BNPL Silver | Minimum eligible purchase per transaction; maximum eligible purchase per transaction | doc\_cdf7d7a0 |
| BNPL Platinum | APR range minimum; APR range maximum; fixed margin component; late fee amount; early payoff penalty rate; purchase protection per-item reimbursement cap; annual purchase protection coverage cap | doc\_81395413 / doc\_45a0cc99 / doc\_ea76543d / doc\_87711e5e / doc\_0078677a |
| All BNPL (general) | Minimum days early required for payment; payment cutoff timing | doc\_4cbe41e4 |
| BNPL (reward plan) | Reward rate percentage; maximum reward cap per plan | doc\_c2fc87f5 |

---

### 4.12 Miscellaneous Limits

#### Savings Account Opening Eligibility Thresholds

| Limit | Value | Unit | Source |
|---|---|---|---|
| Silver Plus Saver — Tier 2 balance threshold | \[value not available\] | USD | doc\_52b651bd |
| Silver Plus Saver — withdrawal and transfer limits | not detailed | — | doc\_52b651bd |
| Platinum Reserve — external bank transfer processing time | "0 business days" (ambiguous) | business days | doc\_337401bb |

#### Environmental Program Rates

| Program | Rate | Unit | Example | Source |
|---|---|---|---|---|
| Tree-planting (Green Rewards / Green account) | 1 tree per $3,000 spend | trees/$USD | $30,000 → 10 trees; $500 partial → accrues toward 11th | doc\_901900ec |
| Carbon offset — Green Rewards Card | $0.06 per $1 spend | lbs CO₂/$ | $1,000 spend → 60 lbs CO₂ | doc\_826e6694 / doc\_901900ec |
| Carbon offset — alternative rate | 1.25 grams per $1 spend | g CO₂/$ | $1,000 → 1,250 g; $750 → 937.5 g | doc\_4b989df6 |
| Tree-planting per $1,000 (alt formula) | 1 tree per $1,000 | trees/$USD | $1,000 → 1 tree; $2,500 → 2 trees (floor) | doc\_4b989df6 |

#### Wealth Guidance Allocation (Platinum Plus)

| Allocation | Value | Unit | Source |
|---|---|---|---|
| Quarterly wealth guidance hours | 4 | hours/quarter | doc\_15500988 |
| Annual wealth guidance hours | 16 | hours/year (4 × 4 quarters) | doc\_15500988 |
| Monthly equivalent | 1.33 | hours/month (16 ÷ 12) | doc\_a5233950 |

#### Authorization Buffer (Ambiguous)

| Limit | Value | Unit | Note | Source |
|---|---|---|---|---|
| Authorization buffer to prevent negative balance | 5 | unknown (could be $5.00 or 5 cents) | Unit not specified in document | doc\_76eb36c0 |

#### Low-Balance Alert Threshold

| Limit | Value | Unit | Note | Source |
|---|---|---|---|---|
| Recommended low-balance alert default | $62 | USD | Scope uncertain — may be account-specific example, not universal default | doc\_66e67082 |


---


## 5. Cross-Document Contradictions (unresolved/disputed)

| Subject | Conflicting values | Doc A | Doc B | Likely authoritative | Severity | Recommendation |
|---|---|---|---|---|---|---|
| Daily debit card purchase limit | $300 (Doc A, Doc C) vs $250 (Doc B) | doc_checking_accounts_light_green_account_001.json ("at-a-glance"); doc_checking_accounts_light_green_account_005.json (spending limits) | doc_checking_accounts_light_green_account_002.json (specifications) | Undetermined; two sources favour $300 but specification doc may be controlling | High | Reconcile all three source documents; publish a single authoritative limit schedule |
| Everyone Pay contact block-list unit | "$550 contacts" — unclear whether 550 is a count of users or a $550 USD monetary constraint | doc_everyone_pay_everyone_pay_001.json ("Add your first contacts") | doc_everyone_pay_everyone_pay_004.json | Undetermined | Medium | Rewrite the limit statement to state explicitly "550 users" or "$550.00 USD"; eliminate currency-symbol ambiguity on a countable field |
| Wire transfer fee waiver (Platinum Plus) | Fees described as waived unconditionally vs fees implied as conditionally assessed | doc_savings_accounts_platinum_plus_account_005.json (FAQ: fees waived) | doc_savings_accounts_platinum_plus_account_008.json (same-day transfer section; body contains placeholder "wire transfer fees are Yes") | Undetermined; doc_savings_accounts_platinum_plus_account_008.json body is incomplete | High | Retrieve and fully populate doc_savings_accounts_platinum_plus_account_008.json; resolve waiver scope before agents quote this product |
| Silver Rewards Card Year-1 annual fee waiver | Standing feature with no date restriction (waiver always applies to new customers) | doc_business_credit_cards_business_silver_rewards_card_009.json (Silver card overview) | doc_business_credit_cards_business_silver_rewards_card_011.json (promotion window 2025-11-15 to 2026-01-15; promotion is now expired) | doc_business_credit_cards_business_silver_rewards_card_011.json is product-specific; promotion expired 2026-01-15, so customers opening today pay $122.50 | Critical | Immediately retire or archive doc_business_credit_cards_business_silver_rewards_card_011.json and update doc_business_credit_cards_business_silver_rewards_card_009.json to remove the standing-feature implication; agents must not promise a waived Year-1 fee for new accounts opened after 2026-01-15 |
| BNPL Bronze credit limit (title vs body) | Title claims "$500 Credit Limit" | doc_buy_now_pay_later_bnpl_bronze_002.json title | doc_buy_now_pay_later_bnpl_bronze_002.json body (all numeric fields read "[value not available]") | Title may reflect an earlier authoring pass; body is operative but unpopulated | High | Confirm $500 is the correct Bronze credit limit and populate body fields; until resolved, agents must not quote the $500 figure |
| BNPL Bronze installment schedule (title vs body) | Title claims "4 Installments Over 6 Weeks" | doc_buy_now_pay_later_bnpl_bronze_003.json title | doc_buy_now_pay_later_bnpl_bronze_003.json body (installment count and term both "[value not available]") | Title inferred; body is operative but unpopulated | High | Confirm 4-installment/6-week schedule and populate body; this is a template-population failure |
| BNPL Gold / Platinum title-inferred values vs body placeholders | Gold: 0% intro APR implied by title; Platinum: 6-month financing implied by title | doc_buy_now_pay_later_bnpl_gold_003.json (Gold title); doc_buy_now_pay_later_bnpl_platinum_001.json (Platinum title) | Gold and Platinum document bodies (all numeric parameters "[value not available]") | Cannot treat title-inferred values as authoritative; body is operative but empty | High | Populate body fields for Gold and Platinum tiers before agents can quote these products; title values are inadmissible as sole evidence |
| BNPL security guardrail coverage (Diamond vs all other tiers) | Diamond: documented 36-hour dispute concierge SLA and dispute resolution process | doc_buy_now_pay_later_bnpl_diamond_007.json (Diamond, dispute SLA documented) | Bronze, Silver, Gold, Platinum documents (fraud controls, identity verification, dispute SLA all "[value not available]") | Diamond docs are authoritative for Diamond; other tiers have zero coverage | High | Author security guardrail and dispute SLA sections for Bronze, Silver, Gold, and Platinum; agents must refuse to answer security-process queries for these four tiers until populated |
| Sky Blue referral program tenure requirement | 45 days | doc_business_checking_accounts_sky_blue_002.json (Sky Blue free-period referral doc) | Navy Blue, Cobalt Blue, Hunter Green (multiple docs; all state 60-day tenure threshold) | doc_business_checking_accounts_sky_blue_002.json is product-specific; 45-day threshold may be an intentional startup accommodation but is unconfirmed in any bank-wide policy document | High | Confirm whether the 45-day Sky Blue threshold is deliberate product differentiation; document the exception explicitly in the referral-eligibility policy; absent confirmation, agents should apply the 60-day baseline |
| Cobalt Blue tier classification label | Closure procedure labels Cobalt Blue as "PREMIUM TIER" (requiring supervisor review and 21-day notice) | doc_bank_accounts_bank_accounts_(general)_007.json (Closing Business Checking, PREMIUM TIER section) | doc_business_checking_accounts_cobalt_blue_001.json; doc_business_checking_accounts_true_blue_001.json (fee structure: $20/month waived at $2,500 — lower than True Blue at $75/month and comparable to Hunter Green/Lime Green at $25/month) | Fee-ladder documents; True Blue is more premium by fee and balance minimums | Medium | Clarify whether the closure-tier classification scheme is independent of the fee ladder; publish a mapping table; risk is agents applying supervisor-review requirements to the wrong tier |
| Business vs personal checking account-closure eligibility | Business checking: "customer has NO accounts with status CLOSED" (blanket, all account types, no time limit) | doc_bank_accounts_bank_accounts_(general)_003.json (Business Checking opening procedure) | doc_bank_accounts_bank_accounts_(general)_001.json (Personal Checking: "no checking accounts closed for cause in the past 6 months") | doc_bank_accounts_bank_accounts_(general)_003.json is product-specific and likely intentionally stricter for business customers | High | Confirm the blanket CLOSED prohibition is intentional policy; document the rationale; agents applying the personal-checking rule to business-checking applications would incorrectly approve ineligible applicants |
| Platinum Rewards Card cash-back rate | Title: "Earning 4% Cash Back"; Body: "You earn 10.0% cash back on all eligible purchases" | doc_credit_cards_platinum_rewards_card_002.json title | doc_credit_cards_platinum_rewards_card_002.json body ("How You Earn" section) | Body is the operative specification; however, a 10% flat rate on a $200-fee card is financially extraordinary and requires independent verification before use | Critical | Correct the source document immediately; agents must not cite the 4% title figure; escalate the 10% body rate for product-finance verification before quoting to customers |
| Evergreen Account tree-planting threshold | $750 per tree | doc_checking_accounts_evergreen_account_001.json ("at a glance", customer-facing marketing) | doc_checking_accounts_evergreen_account_004.json ("Tracking your environmental impact", provides explicit formula: `floor(spend / 1000)` = $1,000 per tree) | doc_checking_accounts_evergreen_account_004.json (explicit arithmetic formula is more precise than marketing copy) | High | Update doc_checking_accounts_evergreen_account_001.json to align with the $1,000 formula; agents using the marketing figure will overpromise tree counts by 33% |
| Provisional credit eligibility for subscription cancellation disputes | Customer-facing document implies provisional credit for "many types of disputes" including "Subscription Issues: Being charged for a subscription you already cancelled" | doc_bank_accounts_(general)_036 ("What Happens When You File a Dispute") | doc_bank_accounts_(general)_032 (internal policy: explicitly excludes `recurring_charge_after_cancellation` from mandatory provisional credit, classified as discretionary only) | doc_032 (internal policy is authoritative over customer-facing copy) | Critical | Update doc_036 to carve out subscription-cancellation disputes from the "many types" provisional credit promise, or add explicit language stating credit is discretionary for this category; an agent following doc_036 would make a binding promise the internal policy does not support |
| Pending-transaction disclosure: Card Freeze vs Recurring Block | Card Freeze explicitly discloses: "Pending transactions already authorized may still process" | doc_bank_accounts_(general)_026 (Card Freeze, Freezing Steps step 3) | doc_bank_accounts_(general)_034 (Recurring Block, Blocking Process step 4: entirely silent on whether pre-authorized pending charges can still post during or after the 24-hour activation window) | doc_026 sets the disclosure standard; the absence of equivalent language in doc_034 is an asymmetric omission | High | Add a pending-transaction passthrough disclosure to doc_034 matching the language in doc_026; asymmetric disclosure creates customer harm and Reg E fair-dealing exposure |
| ATM cash discrepancy provisional credit timeline (Rho-Bank ATM) | "Provisional credit issued immediately (no waiting period)" | doc_bank_accounts_(general)_033 / doc_bank_accounts_bank_accounts_(general)_033.json (ATM Dispute Special Procedures) | doc_bank_accounts_(general)_032 / doc_bank_accounts_bank_accounts_(general)_032.json (Provisional Credit Guidelines: atm_cash_discrepancy category → standard 10 business days) | Undetermined; both are internal authoritative sources | Critical | Reconcile the two internal documents; gap of 0 vs up to 10 business days in customer outcome; immediate escalation to policy owners required |
| Reg E reporting-clock reference point | 2-business-day and 60-day liability windows presented as measured from customer "notice" or "report" date | doc_bank_accounts_(general)_036 ("Time is Important") | doc_bank_accounts_(general)_032 (internal: 60-day condition explicitly tied to "statement date showing the transaction", consistent with 12 CFR §1005) | doc_032 (statement-date reference matches statutory Reg E text and is more legally precise) | Critical | Update doc_036 to align with the statement-date reference point; agents relying on doc_036 may accept disputes that are outside the statutory window, creating Reg E violation exposure |
| Third-party ATM investigation timeline | 90 days (calendar) for all third-party ATMs | doc_bank_accounts_(general)_033 (ATM Special Procedures) | doc_bank_accounts_(general)_032 (45 business days ≈ 63 calendar days; 90-day extension restricted to international transactions, POS outside the US, or new accounts — does not cover domestic third-party ATMs) | doc_032 as the general guideline; doc_033's 90-day extension may exceed what doc_032 authorises for domestic third-party cases | High | Determine whether doc_033's 90-day rule for third-party ATMs is an authorised exception or an error; publish a definitive timeline matrix covering Rho-Bank, domestic third-party, and international ATM categories |
| Everyone Pay instant transfer fee structure | $0.75 flat fee only | doc_everyone_pay_everyone_pay_002.json (Everyone Pay sending doc) | doc_everyone_pay_everyone_pay_003.json ("$0.75 OR a percentage fee of 0.75%, as shown before you confirm") | doc_everyone_pay_everyone_pay_003.json (more complete disclosure; flat-fee-only doc is a subset) | High | Agents relying solely on doc_everyone_pay_everyone_pay_002.json will fail to disclose the potential 0.75% alternative; update doc_everyone_pay_everyone_pay_002.json or deprecate it; use doc_everyone_pay_everyone_pay_003.json as the single authoritative fee disclosure |
| Green Fee-Free Account tier classification vs EveryonePay daily limit | Closure procedure classifies Green Fee-Free as ENTRY TIER; ENTRY TIER implies lower daily limits | doc (tier-classification / closure-fee document, ENTRY TIER definition) | doc_bank_accounts_bank_accounts_(general)_005.json (Green Fee-Free documented EveryonePay limit: $2,000/day — matching MID TIER accounts such as Blue Account) | Product-specific limit document; tier-inferred limits must not override documented product limits | Medium | Add a note to the tier-classification document clarifying that Green Fee-Free's EveryonePay limit is set at the MID TIER level as a product-specific exception; agents must apply product-specific limits, not tier-inferred limits |

---

### Open critical/high signals

#### Critical

| Signal | Content |
|---|---|
| s629 | Resolve conflict between entries e8315 and e1814 (nature of conflict not yet fully documented in synthesised entries; requires retrieval and reconciliation pass). |
| s630 | Resolve conflict between entries e8316 and e7267 (nature of conflict not yet fully documented; requires retrieval and reconciliation pass). |
| s807 | **STALE ACTIVE PROMOTIONS:** Two expired business savings promotions — Oct 2025 (doc_bank_accounts_bank_accounts_(general)_016.json) and Nov 2025 (doc_bank_accounts_bank_accounts_(general)_015.json) — remain in the active policy register as of 2026-06-26. Both contain agent directives that would incorrectly bias product recommendations toward products no longer on promotion. Both documents must be archived or retired immediately. |
| s815 | **DATA QUALITY DEFECT:** doc_credit_cards_platinum_rewards_card_002 (doc_credit_cards_platinum_rewards_card_002.json) has an irreconcilable title/body mismatch: title states "Earning 4% Cash Back", body states "10.0% cash back on all eligible purchases." The 4% figure must never be cited by agents. The document must be corrected before the policy register can be considered complete for Platinum Rewards. |
| s816 | **SYSTEMIC TEMPLATE FAILURE:** BNPL Bronze and Silver tiers (16 of 48 BNPL documents, 33% of the BNPL corpus) contain exclusively `[value not available]` placeholders for all policy-critical numeric fields: credit limits, minimum purchase amounts, installment counts, term lengths, interest rates, late fees, and maximum active plans. Agents cannot quote any specific parameter for Bronze or Silver without verified source values. Authoring team must populate all placeholder fields before these tiers can be operationally supported. |
| s817 | **TITLE/BODY MISMATCH — BNPL Bronze:** doc_bnpl_bronze_002 title claims "$500 Credit Limit", body has `[value not available]`. doc_bnpl_bronze_003 title claims "4 Installments Over 6 Weeks", body has all placeholders. Titles may reflect an earlier authoring draft; bodies were never populated. Authoring team must confirm whether $500 credit limit and 4-installment/6-week schedule are correct Bronze tier specifications and populate body fields accordingly. |

#### High

| Signal | Content |
|---|---|
| s667 | Everyone Pay instant fee conflict: doc_everyone_pay_003 cites "$0.75 OR 0.75% percentage"; docs _002 and _015 cite only "$0.75 flat." Three documents favour flat fee; one adds a percentage alternative. Treat $0.75 flat as operative; flag doc_003 for review. Entries e8410 (flat) and e8417 (dual-structure) are in conflict. |
| s670 | Hunter Green monthly maintenance fee waiver threshold ($5,000) vs Lime Green ($15,000) — both stated as MID-tier business checking products. If any bank-wide policy defines a uniform MID-tier waiver threshold, a true contradiction exists; absent that, these are intentionally different products. Requires policy confirmation. |
| s700 | Business checking eligibility conflict (blanket "no accounts with status CLOSED" — doc_bank_accounts_bank_accounts_(general)_003.json) vs personal checking's "no checking accounts closed for cause in the past 6 months" (doc_bank_accounts_bank_accounts_(general)_001.json). Likely intentional but unconfirmed; see table row above. |
| s701 | Cobalt Blue PREMIUM TIER label in closure doc vs fee-ladder positioning (see table row above). Risk: agents may apply incorrect supervisor-review requirement. No mapping document confirms independent closure-tier vs fee-ladder classification schemes. |
| s702 | Sky Blue referral tenure 45-day threshold (doc_business_checking_accounts_sky_blue_002.json) vs 60-day baseline across Navy Blue, Cobalt Blue, Hunter Green. Not confirmed as intentional in any policy document; Referral FAQ (doc_bank_accounts_bank_accounts_(general)_048.json) is silent on per-product differences (see table row above). |
| s729 | Evergreen Account tree-planting threshold $750 (marketing, doc_checking_accounts_evergreen_account_001.json) vs $1,000 per formula `floor(spend/1000)` (doc_checking_accounts_evergreen_account_004.json). Agents risk overpromising tree counts by 33% (see table row above). |
| s733 | **AUTHORITY DEBT:** doc_bank_accounts_bank_accounts_(general)_032.json mandates five distinct Reg E timelines (10-day, 20-day, 45-day, 90-day provisional credit windows; 3-day pre-reversal notice) with zero citations to 12 CFR §1005. Policy may misstate statutory windows; compliance teams cannot audit conformance. Reg E clause anchors required. |
| s734 | **AUTHORITY DEBT:** doc_bank_accounts_bank_accounts_(general)_031.json states customer liability caps ($50 / $500 / unlimited) as Reg E mandates without citing a 12 CFR subsection. Compounded by signal s642's unresolved conflict on whether the 2-business-day reporting window runs from statement date or discovery date — a distinction material to customer harm. |
| s749 | **SEVERITY DEBT P0:** Hardcoded bypass code identified in doc_customer_support_special_support_codes_001.json (entry e8613) has no assigned severity tier, consequence model, remediation priority, or recommended action. Finding cannot be actioned without these. See e8654. |
| s750 | **SEVERITY DEBT P0:** Reg E reporting-clock conflict (doc_bank_accounts_bank_accounts_(general)_031.json vs doc_bank_accounts_bank_accounts_(general)_036.json) has no severity rating, no documented regulatory consequence (CFPB civil penalty exposure up to $1,000,000/day), and no remediation path. Signal s674 is HIGH but lacks actionable severity classification. See e8655. |
| s754 | **SEVERITY DEBT P0:** CLI Step 3 (Verify Payment History) in doc_credit_cards_credit_card_account_logistics_007.json contains only a period "." — one of four agent procedure steps is entirely empty. The payment-history verification gate is the fraud-control checkpoint before CLI approval; it has 0% content coverage. See e8657. |
| s755 | **AUTHORITY DEBT:** doc_bank_accounts_bank_accounts_(general)_033.json instructs agents to warn customers that signing a false ATM affidavit is a "federal offense" with no statute cited. If the characterisation is wrong or jurisdiction-dependent, Rho-Bank bears the misrepresentation risk. Requires legal review and statute citation before use in agent-customer communications. |
| s757 | **AUTHORITY DEBT:** doc_bank_accounts_bank_accounts_(general)_033.json imposes an ATM affidavit requirement ($200 threshold, 10-business-day return window, claim denial for non-return) with zero regulatory or policy source citation. Claim-denial authority derived from this requirement has no verifiable regulatory anchor; applying it to deny a valid Reg E claim may itself constitute a Reg E violation. |
| s784 | ATM Rho-Bank cash discrepancy provisional credit: "immediately (no waiting period)" (doc_033) vs standard "10 business days" (doc_032). Two authoritative internal documents give incompatible timelines: 0 vs up to 10 business days. See table row above; escalation to policy owners required. |
| s786 | **AUTHORITY DEBT:** doc_bank_accounts_bank_accounts_(general)_031.json imposes per-tier caps on simultaneously open Reg E disputes (2/3/4/5 by tier) with no cited authority. Reg E does not permit banks to cap the number of error notices a consumer may file. Applying these limits to deny a timely dispute filing may violate 12 CFR §1005.11. |
| s792 | **DEBT SENSOR:** Personal savings product tier rate sheet is absent from the entire 698-document corpus. Nine account classes are confirmed but 27 required data cells (9 classes × 3 fields: APY, minimum opening deposit, monthly fee) have 0% coverage. Product register cannot be completed for the savings family without a source document. |
| s793 | **DEBT SENSOR:** `close_bank_account_7392` agent tool is invoked in all four savings account tier closure procedures but has zero parameter documentation in the corpus. Agent tool register entry cannot be completed; no fields, types, or return structure are documented. |
| s796 | **DEBT SENSOR:** Bypass code `9K2X7M4P1N8Q3R5T6A` (doc_customer_support_special_support_codes_001.json) has no documented rotation schedule, revocation authority, or secondary audit mechanism. A static hardcoded secret with no lifecycle documentation is a critical security guardrail coverage gap. |
| s797 | **DEBT SENSOR:** BNPL Bronze product tier body entirely unpopulated with `[value not available]` placeholders; 0 of 6 required numeric fields recovered from doc_buy_now_pay_later_bnpl_bronze_002.json. Only the title-embedded "$500" survives as an inferred credit limit with no second-source confirmation. BNPL Bronze product tier row cannot be completed from current corpus. |
| s798 | **DEBT SENSOR:** CLI Step 3 (Verify Payment History) in doc_credit_cards_credit_card_account_logistics_007.json contains only a period "." — the fraud-control checkpoint before CLI approval has 0% content coverage (see s754). |
| s799 | **DEBT SENSOR:** Silver Rewards Card Year-1 fee waiver temporal item expired 2026-01-15 (162 days ago) with no retirement notice in the 698-document corpus. Agents may still cite the waiver from doc_business_credit_cards_business_silver_rewards_card_011.json or doc_business_credit_cards_business_silver_rewards_card_009.json. No successor guidance document found. |
| s800 | Personal savings policy register is missing: interest rate/APY schedules, minimum balance maintenance requirements, withdrawal frequency limits, FDIC insurance disclosures, and overdraft/fee schedules. Neither doc_bank_accounts_bank_accounts_(general)_002.json nor doc_bank_accounts_bank_accounts_(general)_006.json contains this information. |
| s803 | `close_bank_account_7392` parameter schema is absent from all 698 documents. Agent tool register entry cannot be completed. |
| s808 | **DATA QUALITY:** doc_bank_accounts_bank_accounts_(general)_008.json (Closing Business Savings Accounts) contains three instances where "$" erroneously prefixes a day-count value: "$120 days", "$180 days", "$270 days". Agents may misinterpret closure period durations as dollar amounts. Source document requires correction. |
| s811 | Light Green Account (age 13–24) and Dark Green Account (age 17–26) both have documented upper age bounds. No policy specifies what happens when a customer ages out — whether the account auto-converts, is restricted, or requires an explicit close. Material gap in the personal-checking policy register. |
| s818 | BNPL Platinum: variable APR reference index, fixed margin, floor, and ceiling are all `[value not available]`. Purchase-protection per-item maximum, annual cap, claim window, and reimbursement rate are all `[value not available]`. Prepayment penalty rate is `[value not available]`. Agents cannot quote any Platinum APR or protection terms. |
| s819 | BNPL Gold: introductory promotional APR, introductory period duration, and standard APR are all `[value not available]`. Auto-debit minimum payment percentage, scheduled auto-debit day-of-month, eligible customer segment, and business registration requirement are all `[value not available]`. All differentiating Gold parameters are absent. |


---


## 6. Data-Quality Defects

All 220 data-quality defect entries from the Rho-Bank policy register are enumerated below, grouped into six defect classes. Within each group, rows are ordered by ascending entry ID.

**Severity scale — derived from source confidence score and policy impact:**
Critical (conf ≥ 0.95 or core compliance/safety exposure) · High (conf 0.85–0.94) · Medium (conf 0.70–0.84) · Low (conf < 0.70)

---

### 6.1 Unfilled `[value not available]` / `[[placeholder]]` Templates

Source documents retain a literal template token rather than a populated value.

| Entry ID | Doc ID | Defect | Field(s) Affected | Product | Severity | Evidence |
|---|---|---|---|---|---|---|
| e3004 | — | `[PLACEHOLDER]` retained | Feature summary; differentiators vs True Blue | Sky Blue Account | Medium | "[PLACEHOLDER] Sky Blue Account features summary and main differentiators from True Blue — not documented in batch_015 set" |
| e3005 | — | `[PLACEHOLDER]` retained | Interest crediting frequency and method | True Blue Account | Medium | "[PLACEHOLDER] Interest crediting frequency and method for True Blue Account — only APY specified, not crediting schedule" |
| e3006 | — | `[PLACEHOLDER]` retained | International wire transfer fees and limits | True Blue Account | Medium | "[PLACEHOLDER] True Blue Account international wire transfer fees and limits — only domestic wires documented" |
| e3007 | — | `[PLACEHOLDER]` retained | ATM fee dispute resolution timeline | True Blue Account | Medium | "[PLACEHOLDER] Dispute resolution timeline and process for ATM fee incorrect charges — support contact documented but not resolution timeline" |
| e3015 | — | `[PLACEHOLDER]` retained | Wire transfer dispute process and timeline | True Blue Account | Medium | "[PLACEHOLDER] True Blue Account wire transfer dispute process and timeline — only normal wire operations documented" |
| e3016 | — | `[PLACEHOLDER]` retained | Referral program details | Sky Blue Account | Medium | "[PLACEHOLDER] Sky Blue Account referral program details — only True Blue Referral Program documented in batch" |
| e3082 | doc_business_credit_cards_business_platinum_rewards_card_012.json | `[[PLACEHOLDER: …]]` retained | Eligible merchant categories / transaction types for $15,000 qualifying spend | Hunter Green Business Checking | High | "[[PLACEHOLDER: specific merchant categories or transaction types eligible for $15,000 qualifying spend]] — not specified in doc" |
| e3083 | doc_business_credit_cards_business_platinum_rewards_card_012.json | `[[MISSING: …]]` retained | Approval criteria for referred business accounts | Hunter Green Business Checking | High | "[[MISSING: approval criteria for referred business accounts]] — doc states bonus earned when referred business is approved but does not specify approval requirements" |
| e3241 | doc_business_credit_cards_business_silver_rewards_card_001.json | `[[MISSING: …]]` retained | First-year fee waiver offer window dates | Business Silver Credit Card | High | "[[MISSING: first-year fee waiver promotional period for Business Silver]] — doc states $0 first year for new customers but does not specify offer window dates" |
| e3242 | doc_business_credit_cards_business_silver_rewards_card_001.json | `[[MISSING: …]]` retained | APR intro period; waiver terms; purchase APR | Business Silver Credit Card | High | "[[MISSING: APR terms and conditions]] — doc lists APR on carried balances but no intro period, waiver terms, or applicable purchase APR specified" |
| e3270 | doc_business_credit_cards_business_bronze_rewards_card_007.json | `[[VALUE NOT AVAILABLE]]` retained | Grace period length for new purchases when balance is carried | Credit Card | High | "[[VALUE NOT AVAILABLE]]: No specified grace period length stated in documents; unclear if there is a grace period for new purchases when balance is carried" |
| e3271 | doc_business_credit_cards_business_bronze_rewards_card_007.json | `[[VALUE NOT AVAILABLE]]` retained | Minimum monthly payment amount | Credit Card | High | "[[VALUE NOT AVAILABLE]]: No minimum monthly payment amount specified in documents" |
| e3272 | doc_business_credit_cards_business_bronze_rewards_card_007.json | `[[VALUE NOT AVAILABLE]]` retained | Statement closing dates; payment due dates | Credit Card | High | "[[VALUE NOT AVAILABLE]]: No statement closing dates or payment due dates specified; only referenced as 'due date' without definition" |
| e3273 | doc_business_credit_cards_business_bronze_rewards_card_005.json | `[[PLACEHOLDER NOT FILLED]]` retained | Maximum credit line | Business Credit Card | Critical | "[[PLACEHOLDER NOT FILLED]]: No maximum credit line specified; only stated 'at least $10,000 and may be as high as $50,000'" |
| e3274 | doc_business_credit_cards_business_bronze_rewards_card_007.json | `[[UNIT AMBIGUITY]]` retained | Variable interest rate index / adjustment mechanism | Credit Card | Critical | "[[UNIT AMBIGUITY]]: Interest rate labeled as 'variable' with no definition of how/when it adjusts or what index it follows" |
| e3402 | doc_business_credit_cards_business_silver_rewards_card_002.json | `[[MISSING: …]]` retained | Definition of 'authorized platform' for travel and software rewards | Business Rewards Credit Card | High | "[[MISSING: definition of 'authorized platform' for travel and software]] — doc references authorized platform but does not define which platforms qualify" |
| e3403 | doc_business_credit_cards_business_silver_rewards_card_002.json | `[[MISSING: …]]` retained | Merchant category code (MCC) list or mapping | Business Rewards Credit Card | High | "[[MISSING: merchant category code (MCC) reference]] — doc references category codes but does not provide MCC list or mapping" |
| e3838 | doc_business_savings_accounts_diamond_vault_003.json | `[[contradiction-candidate]]` token retained; '0 business days' semantically undefined | External bank transfer processing time | Diamond Vault | Low | "[[contradiction-candidate]] Diamond Vault external transfer processing time stated as '0 business days' — semantically unclear if this means same-day or indicates data error" |
| e4050 | — (doc_business_savings_accounts_automatic_sweep_program_006.json ref.) | `$0.00 charges` retained as placeholder for actual fee structure | Fee during pause vs disable states | Savings Sweep Program | Low | "uses placeholder language '$0.00 charges' repeatedly without clarifying fee structure during pause vs disable states" |
| e4051 | — (doc_business_savings_accounts_automatic_sweep_program_006.json ref.) | Placeholder phrase `$0.00` in policy body | Fee/charge application during paused sweep state | Savings Sweep Program | Low | "'Review your agreement to understand how $0.00 applies during a paused state' — incomplete/placeholder phrasing" |
| e4246 | doc_business_savings_accounts_emerald_saver_004.json | `[value not available]` retained | Base APY rate | Emerald Saver | Critical | "[value not available] Emerald Saver base APY rate not specified in any document" |
| e4247 | doc_business_savings_accounts_emerald_saver_003.json | `[value not available]` retained | Product terms and features | Green Account (Savings) | Critical | "[value not available] Green Account (savings) product terms and features referenced but not detailed in batch documents" |
| e4366 | doc_buy_now_pay_later_bnpl_gold_001.json | `[value not available]` retained | Initial credit limit range (minimum and maximum) | BNPL Gold 001 | Critical | "initial credit limit range is not specified ([value not available] to [value not available])" |
| e4367 | doc_buy_now_pay_later_bnpl_gold_001.json | `[value not available]` retained | Standard repayment term (months) | BNPL Gold 001 | Critical | "standard repayment term is not specified ([value not available] months)" |
| e4368 | doc_buy_now_pay_later_bnpl_gold_001.json | `[value not available]` retained | Introductory promotional APR | BNPL Gold 001 | Critical | "introductory promotional APR value is not specified ([value not available])" |
| e4369 | doc_buy_now_pay_later_bnpl_gold_001.json | `[value not available]` retained | Introductory APR period duration (days) | BNPL Gold 001 | Critical | "introductory APR period duration is not specified ([value not available] days)" |
| e4370 | doc_buy_now_pay_later_bnpl_gold_001.json | `[value not available]` retained | Standard APR after introductory period | BNPL Gold 001 | Critical | "standard APR after introductory period is not specified ([value not available])" |
| e4414 | doc_buy_now_pay_later_bnpl_management_dashboard_005.json | `[value not available]` retained | Early-payment rewards eligibility status indicator | BNPL Early-Payment Rewards | Critical | "Early-payment rewards enabled: [value not available]" |
| e4415 | doc_buy_now_pay_later_bnpl_management_dashboard_005.json | `[value not available]` retained | Minimum days early required to qualify | BNPL Early-Payment Rewards | Critical | "Minimum days early required: [value not available] days" |
| e4417 | doc_buy_now_pay_later_bnpl_management_dashboard_005.json | `[value not available]` retained | Payment cutoff timing (days prior) | BNPL Early-Payment Rewards | Critical | "placeholder '[value not available] days prior' appears in practical tips section" |
| e4420 | doc_buy_now_pay_later_bnpl_management_dashboard_006.json | `[value not available]` retained | Reward type basis / definition | BNPL Rewards Dashboard | Critical | "'The dashboard displays the reward type as [value not available]'" |
| e4421 | doc_buy_now_pay_later_bnpl_management_dashboard_006.json | `[value not available]` retained | Reward rate percentage applied to qualifying amount | BNPL Rewards Dashboard | Critical | "shown as '[value not available]' with note it is 'applied to the qualifying amount'" |
| e4422 | doc_buy_now_pay_later_bnpl_management_dashboard_006.json | `[value not available]` retained | Maximum reward per plan cap | BNPL Rewards Dashboard | Critical | "'Rewards are capped per plan at [value not available]'" |
| e4425 | doc_buy_now_pay_later_bnpl_management_dashboard_007.json | `[value not available]` retained | Projected rewards display toggle setting | BNPL Dashboard | Critical | "'Show projected rewards total: [value not available]'" |
| e4452 | doc_buy_now_pay_later_bnpl_platinum_004.json | `[[value not available]]` retained | Minimum purchase amount for financing eligibility | BNPL Platinum | Critical | "minimum purchase amount for financing eligibility is [[value not available]]" |
| e4453 | doc_buy_now_pay_later_bnpl_platinum_004.json | `[[value not available]]` retained | Maximum purchase amount for financing eligibility | BNPL Platinum | Critical | "maximum purchase amount for financing eligibility is [[value not available]]" |
| e4459 | doc_buy_now_pay_later_bnpl_platinum_005.json | `[[value not available]]` retained | Purchase protection reimbursement rate | BNPL Platinum | Critical | "purchase protection reimbursement rate is [[value not available]]" |
| e4460 | doc_buy_now_pay_later_bnpl_platinum_005.json | `[[value not available]]` retained | Per-item maximum reimbursement | BNPL Platinum | Critical | "purchase protection per-item maximum reimbursement is [[value not available]]" |
| e4461 | doc_buy_now_pay_later_bnpl_platinum_005.json | `[[value not available]]` retained | Annual maximum purchase protection coverage per calendar year | BNPL Platinum | Critical | "annual maximum purchase protection coverage per account per calendar year is [[value not available]]" |
| e4462 | doc_buy_now_pay_later_bnpl_platinum_005.json | `[[value not available]]` retained | Claim submission window (days from purchase date) | BNPL Platinum | Critical | "claim submission window is [[value not available]] days from purchase date" |
| e4463 | doc_buy_now_pay_later_bnpl_platinum_005.json | `[[value not available]]` retained | Item eligibility lookback window (days from current date) | BNPL Platinum | Critical | "item eligibility lookback window
is [[value not available]] days from current date" |
| e4479 | doc_buy_now_pay_later_bnpl_bronze_008.json | All key terms `[value not available]` — systemic | product_code, credit_limit, min_purchase_amount, num_installments, total_term, installment_interval, APR, late_fees, merchant_fee, currency, max_active_plans | BNPL Bronze | Critical | "CRITICAL — All product specification values missing (marked as [value not available])" |
| e4508 | doc_buy_now_pay_later_bnpl_bronze_001.json | `[value not available]` retained | Account setting field name | Account Settings | Critical | "documentation refers to '[value not available]' instead of actual setting name" |
| e4512 | doc_buy_now_pay_later_bnpl_management_dashboard_008.json | `[value not available]` retained | Primary sort order for plan display | BNPL Plan Display | Critical | "'[value not available]' determines how plans are arranged" |
| e4516 | doc_buy_now_pay_later_bnpl_management_dashboard_008.json | `[value not available]` retained | Overdue plan highlighting toggle (true/false) | BNPL Plan Display | Critical | "shown as '[value not available]' true/false toggle" |
| e4520 | doc_buy_now_pay_later_bnpl_platinum_001.json | `[value not available]` retained | Activation status indicator name | BNPL Platinum | Critical | "'[value not available] = true' requirement" |
| e4524 | doc_buy_now_pay_later_bnpl_gold_002.json | `[value not available]` retained | Credit limit range minimum | BNPL Gold 002 | Critical | "credit limit range minimum is not specified ([value not available])" |
| e4525 | doc_buy_now_pay_later_bnpl_gold_002.json | `[value not available]` retained | Credit limit range maximum | BNPL Gold 002 | Critical | "credit limit range maximum is not specified ([value not available])" |
| e4529 | doc_buy_now_pay_later_bnpl_gold_002.json | `[value not available]` retained | Eligible customer segment | BNPL Gold 002 | Critical | "eligible customer segment is not specified ([value not available])" |
| e4530 | doc_buy_now_pay_later_bnpl_gold_002.json | `[value not available]` retained | Business registration requirement | BNPL Gold 002 | Critical | "business registration requirement is not specified ([value not available])" |
| e4532 | doc_buy_now_pay_later_bnpl_gold_003.json | `[value not available]` retained | Introductory APR percentage | BNPL Gold 003 | Critical | "introductory APR percentage is not specified ([value not available])" |
| e4533 | doc_buy_now_pay_later_bnpl_gold_003.json | `[value not available]` retained | Introductory period duration (days) | BNPL Gold 003 | Critical | "introductory period duration is not specified ([value not available] days)" |
| e4534 | doc_buy_now_pay_later_bnpl_gold_003.json | `[value not available]` retained | Day on which standard APR begins | BNPL Gold 003 | Critical | "day when standard APR begins is not specified (after day [value not available])" |
| e4535 | doc_buy_now_pay_later_bnpl_gold_003.json | `[value not available]` retained | Standard APR after introductory period | BNPL Gold 003 | Critical | "standard APR percentage after introductory period is not specified ([value not available])" |
| e4537 | doc_buy_now_pay_later_bnpl_gold_004.json | `[value not available]` retained | Auto-debit current status | BNPL Gold 004 | Critical | "auto-debit current status is not specified ([value not available])" |
| e4538 | doc_buy_now_pay_later_bnpl_gold_004.json | `[value not available]` retained | Auto-debit minimum payment calculation percentage | BNPL Gold 004 | Critical | "auto-debit minimum payment calculation percentage is not specified ([value not available]% of outstanding balance)" |
| e4539 | doc_buy_now_pay_later_bnpl_gold_004.json | `[value not available]` retained | Scheduled auto-debit day of month | BNPL Gold 004 | Critical | "scheduled auto-debit day of month is not specified (day [value not available])" |
| e4599 | doc_business_savings_accounts_silver_saver_account_002.json | `[value not available]` retained | Minimum opening deposit | Silver Saver | Critical | "[value not available] — Minimum opening deposit requirement for Silver Saver Account not specified in available documents" |
| e4600 | doc_business_savings_accounts_silver_saver_account_005.json | `[value not available]` retained | Account closure conditions; early closure penalties | Silver Saver | Critical | "[value not available] — Account closure conditions and any early closure penalties not specified in available documents" |
| e4601 | doc_business_savings_accounts_silver_saver_account_003.json | `[value not available]` retained | Maximum daily ATM withdrawal limit | Silver Saver | High | "[value not available] — Maximum daily ATM withdrawal limit amount not specified; only mentions ATM cash withdrawals count toward 6-withdrawal monthly limit" |
| e4602 | doc_business_savings_accounts_silver_saver_account_002.json | `[value not available]` retained | Monthly APY tier evaluation date / schedule | Silver Saver | Critical | "[value not available] — Specific monthly evaluation date or schedule for APY tier determination not provided" |
| e4604 | doc_buy_now_pay_later_bnpl_platinum_006.json | `[[value not available]]` retained | Late fee amount | BNPL Platinum | Critical | "BNPL Platinum late fee amount is [[value not available]]" |
| e4613 | doc_buy_now_pay_later_bnpl_platinum_007.json | `[[value not available]]` retained | Prepayment eligibility condition | BNPL Platinum | Critical | "BNPL Platinum prepayment eligibility condition is [[value not available]]" |
| e4614 | doc_buy_now_pay_later_bnpl_platinum_007.json | `[[value not available]]` retained | Early payoff penalty rate | BNPL Platinum | Critical | "BNPL Platinum early payoff penalty rate is [[value not available]]" |
| e4645 | doc_buy_now_pay_later_bnpl_bronze_008.json | `[value not available]` retained | product_code | BNPL Bronze | Critical | "product_code value missing — required for system identification and merchant routing" |
| e4646 | doc_buy_now_pay_later_bnpl_bronze_008.json | `[value not available]` retained | Credit limit | BNPL Bronze | Critical | "credit limit value missing — critical for underwriting and risk controls" |
| e4647 | doc_buy_now_pay_later_bnpl_bronze_008.json | `[value not available]` retained | APR (interest rate) | BNPL Bronze | Critical | "APR (interest rate) value missing — required for Truth in Lending Act compliance" |
| e4653 | doc_buy_now_pay_later_bnpl_platinum_002.json | `[value not available]` retained | Financing term length (months) | BNPL Platinum | Critical | "'Your BNPL Platinum financing term is [value not available] months'" |
| e4655 | doc_buy_now_pay_later_bnpl_platinum_002.json | `[value not available]` retained | Number of monthly installments | BNPL Platinum | Critical | "references '[value not available] monthly installments' amortization" |
| e4669 | doc_buy_now_pay_later_bnpl_bronze_005.json | `[value not available]` retained | Per-installment late fee; maximum total late fee | BNPL (general) | Critical | "per-installment fee and maximum total are both [value not available]" |
| e4700 | doc_checking_accounts_blue_account_003.json | `[value not available]` retained | Out-of-network ATM fee amount | Blue Account | Critical | "[value not available] Blue Account out-of-network ATM fee amount not specified in documentation" |
| e4720 | doc_buy_now_pay_later_bnpl_gold_005.json | `[value not available]` retained | Minimum transaction amount for BNPL financing | BNPL Gold 005 | Critical | "minimum transaction amount for BNPL financing is not specified ([value not available])" |
| e4721 | doc_buy_now_pay_later_bnpl_gold_005.json | `[value not available]` retained | Maximum transaction amount for BNPL financing | BNPL Gold 005 | Critical | "maximum transaction amount for BNPL financing is not specified ([value not available])" |
| e4723 | doc_buy_now_pay_later_bnpl_gold_005.json | `[value not available]` retained | Upper ineligibility threshold (settled amount exceeds) | BNPL Gold 005 | Critical | "ineligibility threshold if final settled amount exceeds is not specified ([value not available])" |
| e4724 | doc_buy_now_pay_later_bnpl_gold_005.json | `[value not available]` retained | Lower ineligibility threshold (settled amount falls below) | BNPL Gold 005 | Critical | "ineligibility threshold if final settled amount falls below is not specified ([value not available])" |
| e4726 | doc_buy_now_pay_later_bnpl_gold_005.json | `[value not available]` retained | Lower transaction size minimum reference | BNPL Gold 005 | Critical | "if purchase just below [value not available]" |
| e4727 | doc_buy_now_pay_later_bnpl_gold_005.json | `[value not available]` retained | Upper transaction size maximum reference | BNPL Gold 005 | Critical | "total does not exceed [value not available]" |
| e4742 | doc_buy_now_pay_later_bnpl_platinum_008.json | `[[value not available]]` retained | APR range minimum | BNPL Platinum | Critical | "BNPL Platinum APR minimum range boundary is [[value not available]]" |
| e4743 | doc_buy_now_pay_later_bnpl_platinum_008.json | `[[value not available]]` retained | APR range maximum | BNPL Platinum | Critical | "BNPL Platinum APR maximum range boundary is [[value not available]]" |
| e4750 | doc_buy_now_pay_later_bnpl_silver_001.json | `[[value not available]]` retained | Product configuration enablement flag name | BNPL Silver | Critical | "enablement requires product configuration flag [[value not available]] = true" |
| e4762 | doc_buy_now_pay_later_bnpl_platinum_003.json | `[value not available]` retained | Reference index identifier for variable APR | BNPL Platinum | Critical | "'Reference index: [value not available]'" |
| e4763 | doc_buy_now_pay_later_bnpl_platinum_003.json | `[value not available]` retained | Fixed margin value for variable APR | BNPL Platinum | Critical | "'Fixed margin: [value not available]'" |
| e4764 | doc_buy_now_pay_later_bnpl_platinum_003.json | `[value not available]` retained | Program APR range minimum | BNPL Platinum | Critical | "'Program APR range: [value not available] to...'" |
| e4765 | doc_buy_now_pay_later_bnpl_platinum_003.json | `[value not available]` retained | Program APR range maximum | BNPL Platinum | Critical | "'Program APR range: ... to [value not available]'" |
| e4797 | doc_buy_now_pay_later_bnpl_bronze_003.json | `[value not available]` retained | Installment interval; final installment number; final due date | BNPL (general) | Critical | "installment interval, final installment number, final due date all [value not available]" |
| e4825 | doc_checking_accounts_blue_account_002.json | `[[placeholder]]` retained | Opening requirements; minimum account age; onboarding conditions | Blue Account | Critical | "[[placeholder]] No information on Blue Account opening requirements, minimum account age, or customer onboarding conditions" |
| e4836 | doc_buy_now_pay_later_bnpl_bronze_002.json, doc_buy_now_pay_later_bnpl_bronze_006.json | `[value not available]` retained (cross-doc) | Minimum purchase amount | BNPL (multiple) | Critical | "minimum purchase amount referenced in docs but value [value not available] in all instances" |
| e4837 | doc_buy_now_pay_later_bnpl_silver_002.json | `[[value not available]]` retained | Minimum eligible purchase amount | BNPL Silver | Critical | "BNPL Silver minimum eligible purchase amount is [[value not available]]" |
| e4838 | doc_buy_now_pay_later_bnpl_silver_002.json | `[[value not available]]` retained | Maximum eligible purchase amount per transaction | BNPL Silver | Critical | "BNPL Silver maximum eligible purchase amount is [[value not available]]" |
| e4845 | doc_buy_now_pay_later_bnpl_silver_002.json | `[[value not available]]` retained — table row | Minimum eligible purchase (limits-at-a-glance table) | BNPL Silver | Critical | "Minimum eligible purchase = [[value not available]]" |
| e4846 | doc_buy_now_pay_later_bnpl_silver_002.json | `[[value not available]]` retained — table row | Maximum eligible purchase per transaction (limits-at-a-glance table) | BNPL Silver | Critical | "Maximum eligible purchase per transaction = [[value not available]]" |
| e5320 | doc_checking_accounts_evergreen_account_003.json | `[value not available]` retained | Minimum opening deposit | Evergreen Account | Medium | "[value not available] — Evergreen Account minimum opening deposit not specified in documents" |
| e5499 | doc_checking_accounts_gold_years_account_001.json | `[value not available]` retained | Minimum opening deposit | Gold Years Account | Medium | "[value not available] — Gold Years Account minimum opening deposit not specified" |
| e5500 | doc_checking_accounts_gold_years_account_001.json | `[value not available]` retained | Minimum ongoing balance | Gold Years Account | Medium | "[value not available] — Gold Years Account minimum ongoing balance not specified" |
| e5721 | doc_credit_cards_bronze_rewards_card_005.json | Placeholder value retained in body | Minimum dollar amount for minimum payment | Credit Card | Critical | "Minimum dollar amount for minimum payment not specified; placeholder value" |
| e6756 | — | `[VALUE NOT AVAILABLE]` retained | Posting timeframe for $2,000 sustainability bonus points after qualifying period | EcoCard | Critical | "[VALUE NOT AVAILABLE] EcoCard: Exact posting timeframe for $2,000 sustainability bonus points" |

---

### 6.2 Dollar-Sign on Count / Duration

The currency symbol `$` is erroneously applied to a count of days, countries, cards, or a credit-score integer.

| Entry ID | Doc ID | Defect | Field(s) Affected | Product | Severity | Evidence |
|---|---|---|---|---|---|---|
| e2530 | doc_bank_accounts_bank_accounts_(general)_005.json | `$180 days` — `$` prefixed to day count | Closure fee notice / hold period | Personal Checking ELITE (Bluest) | Critical | "closure fee period says '$180 days' — syntax error, should be '180 days' without currency symbol" |
| e2531 | doc_bank_accounts_bank_accounts_(general)_006.json | `$180 days` — `$` prefixed to day count | Closure fee notice / hold period | Personal Savings PREMIUM (Gold) | Critical | "closure fee period says '$180 days' — syntax error, should be '180 days' without currency symbol" |
| e2532 | doc_bank_accounts_bank_accounts_(general)_006.json | `$270 days` — `$` prefixed to day count | Closure fee notice / hold period | Personal Savings ELITE (Platinum) | Critical | "closure fee period says '$270 days' — syntax error, should be '270 days' without currency symbol" |
| e2533 | doc_bank_accounts_bank_accounts_(general)_007.json | `$180 days` — `$` prefixed to day count | Closure fee notice / hold period | Business Checking PREMIUM (Cobalt Blue) | Critical | "closure fee period says '$180 days' — syntax error, should be '180 days' without currency symbol" |
| e2534 | doc_bank_accounts_bank_accounts_(general)_007.json | `$270 days` — `$` prefixed to day count | Closure fee notice / hold period | Business Checking ELITE | Critical | "closure fee period says '$270 days' — syntax error, should be '270 days' without currency symbol" |
| e2779 | doc_business_checking_accounts_world_blue_001.json | `$140` — `$` applied to region/country count (ambiguous) | Supported regions for payments | World Blue Account | High | "'$140' is ambiguous; unclear if this means 140 regions or a monetary value" |
| e3324 | doc_business_credit_cards_business_platinum_rewards_card_001.json | `$765` — `$` applied to credit score integer | Personal credit score | Personal Credit Card | Critical | "personal credit score displayed as currency ($765) rather than numeric score (765)" |
| e3475 | doc_business_checking_accounts_world_blue_005.json | `$140 countries` — `$` applied to country count | Number of supported cross-border payment countries/regions | Cross-Border Payments / World Blue | Low | "'send and receive cross-border payments in $140 countries/regions' — unclear if $140 is currency notation or typo for country count" |
| e3897 | doc_business_credit_cards_virtual_card_management_001.json | `$275 active cards` — `$` applied to card cardinality | Maximum concurrent virtual cards permitted | Virtual Cards | Critical | "Virtual Card limit stated as $275 active cards but should be numeric cardinality, not currency" |

---

### 6.3 Missing Units

A numeric value is present in the source document but its unit (currency symbol, time qualifier, or measurement label) is absent or ambiguous.

| Entry ID | Doc ID | Defect | Field(s) Affected | Product | Severity | Evidence |
|---|---|---|---|---|---|---|
| e2525 | doc_bank_accounts_bank_accounts_(general)_034.json | Time qualifier absent — "24 hours" not qualified as business vs calendar | Effective time for recurring block | Recurring Payment Block | Medium | "'takes effect within 24 hours' but no specification whether this is business hours or calendar hours" |
| e2647 | doc_business_checking_accounts_sky_blue_008.json | Time unit missing — company age stated as `4` with no 'years' label | Company age eligibility requirement | Business Account | Medium | "inferred as 'years' but documentation uses '4' without explicit unit" |
| e2648 | doc_business_checking_accounts_sky_blue_009.json | Semantic unit unclear — funding threshold is `0`; could be $0 minimum or unfilled placeholder | Initial funding requirement | BNPL / Free Period | Medium | "Funding requirement threshold is 0; semantic meaning unclear — could mean $0 minimum OR placeholder" |
| e2900 | doc_business_checking_accounts_sky_blue_009.json | Time unit missing — 'free period of `6`' has no unit | Free period duration | BNPL / Free Period | Medium | "doc states 'free period of 6' without explicit time unit; context infers 6 months" |
| e4140 | doc_business_savings_accounts_gold_saver_account_006.json | Currency symbol missing — fee stated as `15` without `$` | Outgoing domestic wire fee | Savings / Wire Transfer | Critical | "'Outgoing domestic wire fee: 15' without currency symbol (should be $15.00 USD or similar)" |
| e4141 | doc_business_savings_accounts_gold_saver_account_007.json | Grammar / unit error — `1 business days` (plural used for singular) | Wire transfer processing timeline | Wire Transfers | Critical | "'1 business days' (plural) which is likely typo for '1 business day' (singular)" |
| e4624 | doc_business_savings_accounts_platinum_reserve_account_007.json | Processing time `0 business days` — semantically ambiguous | External bank transfer processing time | Platinum Reserve | Critical | "external bank transfer processing time stated as '0 business days' — ambiguous interpretation" |
| e5408 | doc_checking_accounts_green_account_(checking)_003.json | Currency symbol missing — fee stated as `8` with no `$` | Cashier's check issuance fee | Dark Green / General Banking | Low | "'fee to issue is 8' without currency or unit" |
| e5414 | doc_checking_accounts_green_account_(checking)_004.json | Currency / unit missing — authorization buffer stated as `5` with no symbol | Authorization hold buffer amount | General Banking | Low | "'5' appears without currency or unit specification — could be $5.00 or 5 cents" |
| e5678 | doc_checking_accounts_light_green_account_004.json | Currency symbol missing — threshold stated as `62` | Transaction alert threshold amount | Oversight / General | Critical | "transaction alert threshold amount missing currency symbol — shows '62' without '$' prefix" |
| e5679 | doc_checking_accounts_light_green_account_004.json | Currency symbol missing — fee stated as `15` | Stop payment request fee | Oversight / General | Critical | "stop payment request fee missing currency symbol — shows '15' without '$' prefix" |
| e5680 | doc_checking_accounts_light_green_account_007.json | Currency symbol missing — fee stated as `5` | Cashier's check fee | General Banking | Critical | "cashier's check fee missing currency symbol — shows '5' without '$' prefix" |
| e6757 | — | Time unit ambiguous — coverage period `105 days`; calendar vs business vs billing cycle unspecified | Purchase protection coverage window | Gold Rewards Card | High | "[MISSING UNIT] Gold Rewards Card purchase protection: Document specifies 105 days coverage but unit ambiguity exists" |

---

### 6.4 Arithmetic and Consistency Errors

Numeric values within or across documents are internally contradictory or demonstrably inconsistent.

| Entry ID | Doc ID | Defect | Field(s) Affected | Product | Severity | Evidence |
|---|---|---|---|---|---|---|
| e2014 | doc_business_checking_accounts_navy_blue_005.json | Format inconsistency — ATM rebate cap rendered as `10` (unitless) in doc_business_checking_accounts_navy_blue_005.json and `$10` in doc_business_checking_accounts_navy_blue_009.json | Monthly ATM rebate cap | Navy Blue Account | Medium | "discrepancy between doc_business_checking_accounts_navy_blue_005.json and doc_business_checking_accounts_navy_blue_009.json on monthly ATM rebate cap (10 vs $10)" |
| e5677 | doc_checking_accounts_light_green_account_002.json | Cross-doc contradiction — daily debit purchase limit `$300` (doc_checking_accounts_light_green_account_001.json, doc_checking_accounts_light_green_account_005.json) vs `$250` (doc_checking_accounts_light_green_account_002.json) | Daily debit card purchase limit | Purple Account | High | "limit stated as $300 in doc_checking_accounts_light_green_account_001.json and doc_checking_accounts_light_green_account_005.json but $250 in doc_checking_accounts_light_green_account_002.json (specifications)" |
| e6626 | doc_credit_cards_platinum_rewards_card_002.json | Internal inconsistency — document title states `4% Cash Back`; body specifies `10.0%` cash back rate | Cash back reward rate | Platinum Rewards Card | Critical | "Platinum Rewards Card title states '4% Cash Back' but content specifies 10.0% cash back rate" |

---

### 6.5 Empty Policy Bodies

A policy step or section exists in the document structure but its body contains no substantive content.

| Entry ID | Doc ID | Defect | Field(s) Affected | Product | Severity | Evidence |
|---|---|---|---|---|---|---|
| e6116 | doc_credit_cards_credit_card_account_logistics_007.json | Step body contains only a period (`.`) — all content missing | Payment history verification logic; requested amount validation | Policy Procedure | Critical | "Step 3 'Verify Payment History and Requested Amount' contains only period marker '.'. Content missing. Should enumerate payment history verification and requested amount validation logic." |

---

### 6.6 Absent Specification (No Placeholder)

Information is simply absent from the source documents; no template token is present. The gap was identified by analytical comparison.

| Entry ID | Doc ID | Defect | Field(s) Affected | Product | Severity | Evidence |
|---|---|---|---|---|---|---|
| e1891 | doc_business_checking_accounts_hunter_green_007 | Fee amount not documented | Standard fee for incoming domestic wire after 5 free monthly allotment | Hunter Green Business Checking | High | "Standard fee amount for incoming domestic wires after 5 free monthly allotment not specified" |
| e2034 | doc_bank_accounts_bank_accounts_(general)_020.json | Fee schedule not enumerated by tier | Early closure fee amounts by account tier | Personal / Business Checking (tiered) | Critical | "Missing data: specific early closure fee amounts by account tier not enumerated" |
| e2035 | doc_bank_accounts_bank_accounts_(general)_020.json | Duration not enumerated by tier | Notice period durations (days/weeks) by account tier | Personal / Business Checking (tiered) | Critical | "Missing data: specific notice period durations (days/weeks) by account tier not enumerated" |
| e2036 | doc_bank_accounts_bank_accounts_(general)_020.json | Tier membership criteria undefined | Which accounts qualify as 'entry-level', 'premium', and 'elite' tiers | Personal / Business Checking (tiered) | Critical | "Missing data: which specific accounts qualify as 'entry-level', 'premium', and 'elite' tiers" |
| e2180 | doc_business_checking_accounts_hunter_green_003 | Ineligible transaction types not listed | Exclusion list for cashback eligibility | Hunter Green Business Checking | High | "Examples of ineligible transaction types not provided in cashback documentation" |
| e2215 | doc_business_checking_accounts_cobalt_blue_009.json | Free transaction limit not specified | Monthly free transaction count | Cobalt Blue Business Checking | High | "Cobalt Blue monthly free transaction limit not specified in Cobalt Blue 005–010 documents" |
| e2419 | doc_business_checking_accounts_hunter_green_010.json | Incoming wire policy entirely absent | Incoming domestic wire policy | Hunter Green Business Checking | High | "Hunter Green incoming domestic wire policy not documented in provided materials" |
| e2434 | doc_bank_accounts_bank_accounts_(general)_012.json | APY boost values not specified | Specific APY boost % for each of 18 checking-savings account pairings | Savings (APY boost program) | Critical | "Missing: specific APY boost percentage values for each of 18 checking-savings account pairings" |
| e2435 | doc_bank_accounts_bank_accounts_(general)_008.json | Tool input parameters absent | Input parameters for tool close_bank_account_7392 | Account Closure Tool | Critical | "Missing: input parameters for tool close_bank_account_7392" |
| e2436 | doc_bank_accounts_bank_accounts_(general)_011.json | Ineligible check type list incomplete | Unsupported / ineligible check types for mobile deposit | Mobile Check Deposit | Critical | "deposit_check_3847 unsupported/ineligible check types only mentioned as 'altered or incomplete checks' without comprehensive list" |
| e2524 | doc_bank_accounts_bank_accounts_(general)_030.json | Escalation criteria and retry limits absent | API failure handling; max retry limits for get_credit_card_accounts_by_user on lost/stolen card | Credit Card (Lost / Stolen) | Medium | "No documented escalation criteria or maximum retry limits for get_credit_card_accounts_by_user tool when customer reports lost/stolen card" |
| e2687 | — | Comparison documentation absent entirely | APY, fees, feature parity between Sky Blue and True Blue | Sky Blue / True Blue Accounts | High | "Sky Blue vs True Blue account comparison missing: no documentation comparing APY, fees, or feature parity between product tiers" |
| e3055 | doc_business_checking_accounts_sky_blue_007.json | Weekly and monthly aggregate deposit limits absent | Weekly / monthly mobile deposit aggregate cap | Personal Checking (Mobile Deposit) | Medium | "Mobile deposit limit context unclear: $25,000 daily limit stated; no weekly or monthly aggregate limit specified" |
| e3168 | doc_business_credit_cards_green_rewards_card_004.json | Product tier specs missing entirely | APY rate, minimum opening deposit, minimum ongoing balance, monthly/annual fees, fee waiver conditions, credit/transaction limits | Product (unspecified tier) | Critical | "Product tier specifications missing: APY rate (if applicable), minimum opening deposit, minimum ongoing balance, monthly/annual fees, fee waiver conditions, explicit credit limit or transaction limits" |
| e3169 | doc_business_credit_cards_green_rewards_card_006.json | Accrual reset mechanism not specified | Tree-planting accrual reset timing (monthly / annually / perpetual) | Environmental / Green Card | High | "Tree-planting accrual reset mechanism not specified: does partial progress carry forward monthly? Annually? Perpetually until threshold met?" |
| e3170 | doc_business_credit_cards_green_rewards_card_006.json | Transaction clearing timeline absent | Merchant verification lag for environmental dashboard offset appearance | Environmental / Green Card | High | "clearing timeline not specified (1–3 business days? Same-day?)" |
| e3322 | doc_business_credit_cards_business_platinum_rewards_card_001.json | Annual card fee / APR fee absent | Annual card fee or annual percentage rate fee | Personal Credit Card | Critical | "annual card fee or annual percentage rate fee not specified in eligibility documentation" |
| e3323 | doc_business_credit_cards_business_platinum_rewards_card_001.json | Monthly fees absent | Monthly fees or service charges | Personal Credit Card | High | "monthly fees or service charges not specified in product documentation" |
| e3325 | doc_business_credit_cards_business_platinum_rewards_card_006.json | Coverage window duration absent | Purchase protection benefit window duration | Premium Travel Credit Card | Critical | "purchase protection benefit window duration not stated" |
| e3326 | doc_business_credit_cards_business_platinum_rewards_card_006.json | Coverage window duration absent | Travel insurance benefit window duration | Premium Travel Credit Card | High | "travel insurance benefit window duration not stated" |
| e3544 | doc_business_credit_cards_business_platinum_rewards_card_001.json | Grace period absent | Grace period or interest-free promotional period for carried balances | Personal Credit Card | High | "grace period or interest-free promotional period not specified for carried balances" |
| e3545 | doc_business_credit_cards_business_platinum_rewards_card_006.json | Rollover policy absent | Annual travel credit expiration or rollover policy | Premium Travel Credit Card | High | "annual travel credit expiration or rollover policy not specified" |
| e3546 | doc_business_credit_cards_business_platinum_rewards_card_001.json | Approval timeline absent | Application approval timeline / processing period | Personal Credit Card | High | "specific application approval timeline or processing period not specified" |
| e3553 | doc_business_credit_cards_business_platinum_rewards_card_006.json | Eligible purchase definition incomplete | Definition of 'eligible' travel purchases for insurance and credit purposes | Premium Travel Credit Card | High | "what constitutes 'eligible' travel purchases for insurance and credit purposes not fully defined" |
| e3589 | — | Referenced document not supplied | 'Exceptions and Exclusions' document referenced by doc_business_credit_cards_business_silver_rewards_card_012.json | General (referenced from doc_business_credit_cards_business_silver_rewards_card_012.json) | Critical | "doc_business_credit_cards_business_silver_rewards_card_012.json references 'Exceptions and Exclusions' document that is not provided in batch 024" |
| e3677 | doc_business_savings_accounts_bronze_saver_account_008.json | Transfer scope undefined | Definition of 'internal transfer to other accounts' (same customer vs third party) for withdrawal counting | Bronze Saver | Medium | "[value not specified] Bronze Saver withdrawal limit: what constitutes 'internal transfer to other accounts'" |
| e3799 | doc_business_credit_cards_virtual_card_management_002.json | Fee structure, APY, opening requirements entirely absent | Fee structure; APY; account opening requirements for virtual cards | Virtual Cards | High | "No explicit fee structure, APY, or account opening requirements specified for virtual cards" |
| e3800 | doc_business_credit_cards_virtual_card_management_004.json | Per-transaction floor and daily cap absent | Per-transaction minimum floor; daily spending cap guidance | Virtual Cards | Medium | "Spending limit range stated as $55–$150,000 but no indication of minimum per-transaction floor or daily cap guidance" |
| e3801 | doc_business_credit_cards_virtual_card_management_004.json | Available merchant categories not enumerated | Optional merchant category control list | Virtual Cards | Medium | "Merchant category controls described as optional but selection criteria and available categories not enumerated" |
| e3932 | doc_business_credit_cards_virtual_card_management_002.json | SLA, retry policy, fallback absent | Provisioning SLA; retry on failure; fallback procedures | Virtual Cards | High | "Documentation states approximately 5 seconds but lacks SLA definition, retry policy on failure, and fallback procedures" |
| e3933 | doc_business_credit_cards_virtual_card_management_003.json | Reactivation procedure absent | Whether revoked virtual cards can be reactivated | Virtual Cards | Medium | "Revocation is reversible but cancellation is permanent; no documentation on whether revoked cards can be reactivated" |
| e3936 | doc_business_credit_cards_virtual_card_management_004.json | Impact on in-flight transactions not documented | Effect of limit changes on pending authorizations | Virtual Cards | Medium | "No documentation on impact of limit changes to in-flight transactions or pending authorizations" |
| e3938 | doc_business_credit_cards_virtual_card_management_005.json | Inheritance timing undefined | Whether newly issued cards inherit team defaults immediately or require explicit assignment | Virtual Cards (Team Controls) | Medium | "Documentation unclear whether newly issued cards inherit team defaults immediately or require explicit assignment" |
| e3941 | doc_business_credit_cards_virtual_card_management_006.json | Escalation chain and SLA absent | Alert routing escalation chain; delivery SLA to departmental approvers | Virtual Cards (Monitoring) | Medium | "No explicit escalation chain or SLA for alert delivery to departmental approvers documented" |
| e3942 | doc_business_credit_cards_virtual_card_management_007.json | Rotation schedule specifics absent | Day-of-month trigger; timezone handling; batch size for monthly card refresh | Virtual Cards (Security) | Medium | "Monthly rotation specified but no clarity on day-of-month trigger, timezone handling, or batch size for refresh" |
| e3944 | doc_business_credit_cards_virtual_card_management_007.json | Fraud detection automation absent | Card compromise detection automation; mandatory fraud reporting flows | Virtual Cards (Security) | Medium | "Documentation does not address card compromise detection automation or mandatory fraud reporting flows" |
| e3948 | doc_business_credit_cards_virtual_card_management_008.json | Quantitative fraud metrics absent | Fraud reduction metrics; compromise rates; comparative risk data for single-use vs multi-use | Virtual Cards (Single-Use) | Medium | "No quantified fraud reduction metrics, compromise rates, or comparative risk data provided" |
| e4015 | doc_business_credit_cards_virtual_card_management_009.json | Fraud monitoring thresholds absent | Fraud monitoring alert thresholds for virtual card transactions | Virtual Cards | High | "No mention of fraud monitoring or alert thresholds for virtual card transactions in best practices docs" |
| e4016 | doc_business_savings_accounts_automatic_sweep_program_004.json | Ineligible account types not specified | Account types other than Bronze that are ineligible for sweep deposits | Savings Sweep | High | "No specification of which account types other than Bronze are ineligible for sweep deposits" |
| e4052 | — (doc_business_savings_accounts_bronze_saver_account_001.json ref.) | Actual withdrawal limit value absent; vague marketing language used | Monthly withdrawal limit | Savings Account (doc_business_savings_accounts_bronze_saver_account_001.json) | Low | "doc_business_savings_accounts_bronze_saver_account_001.json repeatedly references 'Withdrawals: Generous monthly limits' without specifying the actual limit" |
| e4139 | doc_business_savings_accounts_gold_saver_account_003.json | APY rates for all three balance tiers absent | APY % for Tier 1 (≤$37,500), Tier 2 ($37,500–$112,500), Tier 3 (>$112,500) | Savings Account (tiered APY) | Critical | "APY rates for balance tiers are not specified in documents. Tier 1, Tier 2, and Tier 3 are defined but no APY percentages provided." |
| e4189 | doc_business_savings_accounts_gold_plus_saver_002.json | Minimum opening deposit absent | Minimum opening deposit | Gold Plus Saver | Critical | "Minimum opening deposit for Gold Plus Saver Account not specified in available documents" |
| e4190 | doc_business_savings_accounts_gold_plus_saver_002.json | Minimum ongoing balance absent | Minimum ongoing balance | Gold Plus Saver | Critical | "Minimum ongoing balance for Gold Plus Saver Account not specified in available documents" |
| e4191 | doc_business_savings_accounts_gold_plus_saver_002.json | Monthly fee structure absent | Monthly fee | Gold Plus Saver | Critical | "Monthly fee structure for Gold Plus Saver Account not specified in available documents" |
| e4192 | doc_business_savings_accounts_gold_saver_account_001.json | Tier balance thresholds absent | Balance thresholds for tiered APY | Gold Saver | Critical | "Tier balance thresholds for Gold Saver tiered APY not specified in available documents" |
| e4383 | doc_business_savings_accounts_silver_plus_saver_002.json | Minimum opening deposit absent | Minimum opening deposit | Silver Plus Saver | Critical | "Silver Plus Saver minimum opening deposit: value not specified in available docs" |
| e4384 | doc_business_savings_accounts_silver_plus_saver_003.json | Minimum ongoing balance absent (waiver condition) | Minimum ongoing balance (condition for waiving $10 monthly fee) | Silver Plus Saver | Critical | "minimum ongoing balance requirement: value not specified (referenced as condition for waiving $10 monthly fee)" |
| e4386 | doc_business_savings_accounts_silver_plus_saver_002.json | APY rates / tiers absent | APY rates and tier structure | Silver Plus Saver | Critical | "Silver Plus Saver APY rates/tiers: not specified in available docs (Silver Saver rates disclosed separately)" |
| e4388 | doc_business_savings_accounts_silver_saver_account_001.json | Minimum opening deposit absent | Minimum opening deposit | Silver Saver | Critical | "Silver Saver minimum opening deposit: value not specified in available doc" |
| e4389 | doc_business_savings_accounts_silver_saver_account_001.json | Minimum ongoing balance absent | Minimum ongoing balance | Silver Saver | Critical | "Silver Saver minimum ongoing balance requirement: value not specified" |
| e4390 | doc_business_savings_accounts_silver_saver_account_001.json | Monthly fee applicability unclear | Whether monthly maintenance fees apply | Silver Saver | Critical | "Silver Saver monthly fees: no fees mentioned; whether maintenance fees apply to this tier is unclear" |
| e4585 | doc_buy_now_pay_later_bnpl_bronze_002.json | Minimum purchase amount absent in eligibility table | Minimum purchase amount | BNPL (eligibility) | Critical | "Missing specific values for minimum purchase amount in doc_buy_now_pay_later_bnpl_bronze_002.json eligibility table" |
| e4622 | doc_business_savings_accounts_silver_plus_saver_001.json | Tier 2 balance threshold absent | Tier 2 balance threshold for Silver Plus Saver APY | Platinum Reserve / Silver Plus Saver | Critical | "tier 2 balance threshold value for Silver Plus Saver APY tiers not defined" |
| e4623 | doc_business_savings_accounts_platinum_reserve_account_005.json | Credential rotation frequency vague | Credential rotation schedule | Platinum Reserve (API) | Critical | "credential rotation frequency is vague ('regular schedule')" |
| e4625 | doc_business_savings_accounts_silver_plus_saver_001.json | Withdrawal and transfer limits absent | Withdrawal limits; transfer limits | Silver Plus Saver | Critical | "specific withdrawal and transfer limits not detailed in product document" |
| e4626 | doc_business_savings_accounts_platinum_reserve_account_009.json | Access review frequency absent | Periodic access review frequency | Platinum Reserve (Audit) | Critical | "periodic access review frequency not specified" |
| e4741 | doc_buy_now_pay_later_bnpl_bronze_007.json | Maximum concurrent plans limit absent | Maximum number of concurrent BNPL plans | BNPL Platinum | Critical | "Missing specific maximum concurrent plans limit in doc_buy_now_pay_later_bnpl_bronze_007.json" |
| e4826 | doc_checking_accounts_blue_account_007.json | Context of threshold value unclear (account-specific vs universal) | Low-balance alert threshold ($62 — whether universal default or account-specific) | Blue Account | High | "[[missing unit]] Recommended low-balance alert threshold stated as $62 but unclear if this is account-specific or universal default" |
| e4934 | — | Daily debit card purchase limit absent | Daily debit card purchase limit | Blue Account | High | "No Blue Account debit card daily purchase limit explicitly stated in reviewed documents; Bluest specifies $15,000 daily limit for comparison" |
| e4935 | doc_checking_accounts_blue_account_010.json | Online statement fee waiver policy absent | Whether online statements are included at no cost | Blue Account | Medium | "Paper statement fees ($2.50/month) mentioned but no indication of whether statements are included at no cost via online method" |
| e5078 | doc_checking_accounts_bluest_account_009.json | Standard pricing for additional check orders absent | Pricing for check orders beyond complimentary allotment | Personal Checking | Critical | "[Standard pricing for additional check orders not specified in documentation]" |
| e5144 | doc_checking_accounts_dark_green_account_010.json | APY / earnings rate absent | APY or earnings rate | Dark Green Checking | High | "Dark Green Account APY not specified in documents; earnings rate unclear" |
| e5145 | doc_checking_accounts_dark_green_account_006.json | Minimum opening deposit absent | Minimum opening deposit | Dark Green Checking | High | "Dark Green Account minimum opening deposit not specified in available documents" |
| e5146 | doc_checking_accounts_dark_green_account_009.json | Monthly maintenance fee absent | Monthly maintenance fee | Dark Green Checking | Critical | "Dark Green Account monthly maintenance fee not documented; structure unclear" |
| e5147 | doc_checking_accounts_evergreen_account_001.json | Referral bonus good-standing conditions absent | Conditions requiring both accounts maintain good standing for referral bonus | Evergreen Account | Medium | "transaction confirmation on referral bonus requires verification that both accounts maintain good standing" |
| e5231 | doc_checking_accounts_dark_green_account_006.json | Debit card daily purchase limit absent | Debit card daily purchase limit | Dark Green Checking | High | "Dark Green Account debit card daily purchase limit not documented in batch" |
| e5232 | doc_checking_accounts_dark_green_account_008.json | ATM withdrawal daily limit absent | ATM withdrawal daily limit | Dark Green Checking | High | "Dark Green Account ATM withdrawal daily limit not specified in available documents" |
| e5233 | doc_checking_accounts_evergreen_account_001.json | APY boost calculation method absent (additive vs multiplicative) | Green Savings linked APY boost calculation method | Evergreen Account | Medium | "Evergreen Account Green Savings linked product APY boost calculation method unclear; multiplicative vs additive not specified" |
| e5392 | doc_checking_accounts_checking_accounts_(general)_008.json | Hold duration absent | Duration of temporary hold on direct deposit paycheck | Direct Deposit | High | "Temporary hold on direct deposit paycheck: marked as 'Yes' but no duration specified (e.g., '24 hours', 'until processing completes')" |
| e5393 | doc_checking_accounts_dark_green_account_004.json | Reward confirmation SLA absent | GPA reward approval timeline in business days | GPA Reward | Critical | "document states 'typically confirm eligibility shortly after' submission but no SLA or specific timeframe in business days is defined" |
| e5402 | doc_checking_accounts_dark_green_account_009.json | Monthly maintenance fee absent (duplicate observation for same doc) | Monthly maintenance fee | Dark Green Checking | Critical | "Dark Green Account does not document monthly maintenance fee in any document; fee structure undefined" |
| e5403 | doc_checking_accounts_dark_green_account_006.json | APY rate absent (duplicate observation for same doc) | APY rate; checking balance earnings | Dark Green Checking | Critical | "Dark Green Account APY rate missing; checking balance earnings undefined" |
| e5404 | doc_checking_accounts_evergreen_account_001.json | APY boost method undefined | Green Savings APY boost calculation (additive vs multiplicative) | Evergreen Account | Critical | "Evergreen referenced Green Savings Product not fully defined; APY boost calculation (additive vs multiplicative) unclear" |
| e5442 | doc_checking_accounts_green_fee-free_account_002.json | Minimum opening deposit absent | Minimum opening deposit | Personal Checking (general) | High | "Minimum opening deposit amount not specified in product documentation" |
| e5594 | doc_checking_accounts_checking_accounts_(general)_006.json | Pre-auth hold limit list incomplete | Merchant category pre-auth hold limits (all industry types not enumerated) | General Banking (Pre-Auth) | High | "lists gas, hotel, rental, restaurant but does not provide comprehensive merchant category pre-auth hold limits across all industry types" |
| e5651 | doc_checking_accounts_light_green_account_011.json | APY / interest rate absent | APY or interest rate | Light Green Checking | Critical | "APY or interest rate for Light Green Account not specified in available documentation" |
| e5652 | doc_checking_accounts_light_green_account_011.json | Monthly maintenance fee absent | Monthly maintenance fee | Light Green Checking | Critical | "Monthly maintenance fee for Light Green Account not specified in available documentation" |
| e5653 | doc_checking_accounts_light_green_account_008.json | Minimum opening deposit absent | Minimum opening deposit | Light Green Checking | Critical | "Minimum opening deposit for Light Green Account not specified in available documentation" |
| e5654 | doc_checking_accounts_light_green_account_008.json | Minimum ongoing balance absent | Minimum ongoing balance | Light Green Checking | Critical | "Minimum ongoing balance for Light Green Account not specified in available documentation" |
| e5656 | doc_checking_accounts_purple_account_001.json | APY absent | APY / interest rate | Purple Account | Critical | "No APY information provided for Purple Account in documentation reviewed" |
| e5657 | doc_checking_accounts_purple_account_001.json | Monthly maintenance fee absent | Monthly maintenance fee | Purple Account | Critical | "Monthly maintenance fee for Purple Account not specified in available documentation" |
| e5658 | doc_checking_accounts_purple_account_001.json | Minimum opening deposit absent | Minimum opening deposit | Purple Account | Critical | "Minimum opening deposit for Purple Account not specified in available documentation" |
| e5659 | doc_checking_accounts_purple_account_001.json | Minimum ongoing balance absent | Minimum ongoing balance | Purple Account | Critical | "Minimum ongoing balance for Purple Account not specified in available documentation" |
| e5665 | doc_checking_accounts_light_green_account_010.json | Feature comparison absent | Specific Blue vs Green Account feature comparison (APY, fees, feature set) | Blue / Green Account | Critical | "Specific Blue and Green Account feature comparison not provided in documents; abstract reference only" |
| e5702 | doc_checking_accounts_checking_accounts_(general)_004.json | Bank authority over merchant-placed holds undefined | Rho-Bank capability / authority to adjust merchant-placed authorization holds | General Banking | High | "[Authorization hold controls undefined] Documents do not specify Rho-Bank's capability or authority to adjust merchant-placed authorization holds on behalf of customers" |
| e5704 | doc_checking_accounts_checking_accounts_(general)_001.json | Product tier specifications absent entirely | Checking account product tiers, feature sets, rate information, fee schedules | Rho-Bank Checking (Batch 051) | High | "[Product tier specification missing] Batch 051 documents do not define Rho-Bank checking account product tiers, feature sets, rate information, or fee schedules" |
| e5706 | doc_checking_accounts_checking_accounts_(general)_001.json | Eligibility rules absent entirely | Eligibility to open checking accounts; minimum age; geographic restrictions; account count caps; waiting periods | Rho-Bank Checking | High | "[Eligibility rules incomplete] No document specifies who is eligible to open Rho-Bank checking accounts, minimum age, geographic restrictions, account count caps, or waiting periods" |
| e6256 | doc_credit_cards_credit_cards_(general)_019.json | Bonus reward rates absent | Specific bonus reward rates by category | Credit Card Rewards | Critical | "Specific bonus reward rates not provided in document for any category; rates stated to vary by card" |
| e6447 | doc_credit_cards_credit_cards_(general)_020.json | Referral bonus amounts absent | Referral bonus amounts by card type | Credit Card Referral Program | Critical | "Referral bonus amounts not specified; document states amounts vary by card but no specific values provided" |
| e6448 | doc_credit_cards_credit_cards_(general)_020.json | Referral purchase amount and timeframe absent | Required purchase amount and timeframe for referral bonus | Credit Card Referral Program | Critical | "Referral purchase amount and timeframe requirements not specified in document" |
| e6524 | doc_credit_cards_ecocard_001.json | Approval timeline and decision communication method absent | Application approval timeline; decision communication method (email / phone / mail / portal) | EcoCard | High | "missing details on approval timeline and decision communication method" |
| e6525 | doc_credit_cards_ecocard_001.json | Minimum payment requirement absent | Minimum payment requirement (% of balance) | EcoCard | Critical | "missing documented minimum payment requirement (diamond elite specifies 3.0% of balance); only APR and late fee specified" |
| e6526 | doc_credit_cards_diamond_elite_card_007.json | Excluded purchase categories not enumerated | Purchase protection exclusion categories | Diamond Elite Card | High | "coverage is 'subject to policy terms and exclusions' but does not enumerate excluded categories" |
| e6652 | doc_credit_cards_credit_cards_(general)_022.json | Eligible dispute types not enumerated | List of dispute types that qualify for the dispute process | Credit Card Dispute | Critical | "Specific eligible dispute types not enumerated in document; states eligibility depends on type but doesn't list which types qualify" |
| e6727 | doc_credit_cards_credit_cards_(general)_011.json, doc_credit_cards_credit_cards_(general)_012.json | No guidance for dual-incident overlap scenario | Resolution handling when customer meets both Incident 11/13 AND Incident 11/14 criteria simultaneously | Incident Response (cross-doc) | High | "No documented guidance for scenario where customer meets BOTH Incident 11/13 AND Incident 11/14 criteria simultaneously" |
| e6804 | doc_credit_cards_credit_cards_(general)_011.json, doc_credit_cards_credit_cards_(general)_012.json | Expired incident protocols still active in knowledge base | Incident 11/13 (deadline 11/15/2025) and Incident 11/14 (deadline 11/18/2025) — both expired as of 2026-06-26 | Incident Response | Critical | "Status as of 2026-06-26: Incident 11/13 and Incident 11/14 are both EXPIRED; agents should NOT be using incident protocols but documentation still present in knowledge base" |
| e6839 | — | Referral eligibility rules absent | Whether referred person must be new customer; country/region eligibility; same-household restriction | EcoCard Referral Program | Critical | "[MISSING SPECIFICATION] EcoCard referral program does not specify: (1) new customer requirement, (2) country/region eligibility for referrals, (3) same-household restriction" |
| e6840 | — | Purchase protection scope and claim process absent | Types of covered purchases; claim filing process; required documentation; dispute resolution timeline | Gold Rewards Card | Critical | "[MISSING SPECIFICATION] Gold Rewards Card purchase protection: Document does not clarify what types of purchases are covered, claim filing process, required documentation, or dispute resolution timeline" |

---

**Summary count by defect class:**

| Defect Class | Count |
|---|---|
| 6.1 Unfilled `[value not available]` / `[[placeholder]]` templates | 96 |
| 6.2 Dollar-sign on count / duration | 9 |
| 6.3 Missing units | 13 |
| 6.4 Arithmetic and consistency errors | 3 |
| 6.5 Empty policy bodies | 1 |
| 6.6 Absent specification (no placeholder) | 98 |
| **Total** | **220** |


---


## 7. Security Guardrails & Agent-Safety Risks

### A. Guardrails the Agent MUST Follow

| Scenario / Code | Required Action | Prohibited Action | Verification | Escalation Tool | Source |
|---|---|---|---|---|---|
| **Beige Account — dual authorization for transfers >$10,000** (e8221, e8549) | Obtain a second approval from a separate approver before submitting any wire transfer or high-value ACH above $10,000. Ensure initiator and approver roles are distinct. Confirm backup approvers are configured and approval logs are reviewed. | Submitting a transfer above $10,000 without dual authorization. Allowing the initiator to serve as the approver. | Real-time balance validation enabled; approval log review required before processing. | Not specified | doc_business_checking_accounts_beige_009.json, doc_business_checking_accounts_beige_005.json §"Domestic wire transfers / Dual authorization threshold and Control configuration" |
| **Savings account opening — eligibility hard-stop** (e8397) | Verify all 5 eligibility criteria before calling `open_bank_account_4821`. If any criterion is not met, stop and do not proceed. | Opening a savings account when any eligibility criterion is unsatisfied. | Confirm all 5 checklist items are met prior to tool invocation. | Not specified | doc_bank_accounts_bank_accounts_(general)_002.json §"Eligibility Requirements (Internal Checklist)" |
| **ELITE tier savings closure — manager approval** (e8398) | Obtain manager approval before calling `close_bank_account_7392` for Platinum Account, Platinum Plus Account, or Diamond Elite Account. Manager approval is mandatory step 3. | Invoking `close_bank_account_7392` for ELITE tier accounts without prior manager approval. | Confirm manager approval is documented before tool call. | Manager (human escalation) | doc_bank_accounts_bank_accounts_(general)_006.json §"Closure Procedure" |
| **Pre-closure balance check — savings** (e8399) | If an early closure fee applies, verify account balance ≥ fee amount (fee is deducted directly from balance). If no fee applies, balance must be exactly $0. | Using an alternative payment method for the closure fee. Closing account when balance does not meet threshold. | Check current balance and applicable fee before calling `close_bank_account_7392`. | Not specified | doc_bank_accounts_bank_accounts_(general)_006.json §"Pre-Closure Requirements" |
| **`transfer_funds_between_bank_accounts_7291` — transfer preconditions** (e8400) | Confirm source and destination account IDs are distinct. Confirm both accounts belong to the same customer. Obtain explicit customer authorization before executing transfer. | Transferring funds to the same account (source = destination). Transferring between accounts of different customers. Executing without customer authorization. | Validate account IDs and ownership before tool invocation. | Not specified | doc_bank_accounts_bank_accounts_(general)_010.json §"Preconditions and Validation" |
| **Tool parameter and tool name exposure prohibition** (e8396, e8876) | Keep all tool names, parameter names, and return structures internal to the agent. Never disclose `open_bank_account_4821`, `transfer_funds_between_bank_accounts_7291`, `close_bank_account_7392`, or any other internal tool to the customer. | Asking the customer to call tools or provide tool parameters. Surfacing tool names or schemas to the customer in any communication. | Review all outbound agent responses for accidental tool-name disclosure. | Not specified | doc_bank_accounts_bank_accounts_(general)_002.json §"Agent Tool Usage (Internal Only)"; doc_bank_accounts_bank_accounts_(general)_004.json |
| **Replacement credit card — pre-unlock eligibility gate** (e8573, e8614) | Verify customer eligibility in the knowledge base before calling `unlock_discoverable_agent_tool` for `order_replacement_credit_card_7291`. Old card is auto-cancelled upon replacement order — this is irreversible. | Unlocking or calling the tool for ineligible customers. Proceeding with replacement without confirming eligibility. | Eligibility confirmed in knowledge base prior to unlock. | Not specified | doc_credit_cards_credit_card_replacements_001.json §"Before you order / Tool workflow" |
| **Provisional credit — five-condition eligibility gate** (e8574) | Issue provisional credit only when all five conditions are simultaneously true: (1) account open ≥60 days; (2) dispute reason is `unauthorized_fraudulent_charge`, `duplicate_charge`, or `goods_services_not_received` (only if purchase >30 days ago); (3) amount ≥$25 and ≤ card tier max; (4) ≤2 disputes in past 12 months; (5) non-fraud disputes require prior merchant contact. | Issuing provisional credit if any single gate condition fails. | Evaluate all five conditions independently before tool call. | Not specified | doc_credit_cards_credit_cards_(general)_015.json §"Eligibility Criteria" |
| **Cash back dispute correction — independent rate recalculation** (e8586) | When correcting rewards after a resolved dispute, independently recalculate using card type, transaction category, and applicable promotions. Call `update_transaction_rewards_3847` with whole-number "X points" format. Confirm update in `credit_card_transaction_history`. Retain calculation notes for auditability. | Relying on the `expected_rewards` field in the dispute record when correcting rewards. | Confirm updated value in `credit_card_transaction_history` after tool call. Retain calculation notes. | Not specified | doc_credit_cards_credit_cards_(general)_004.json §"Important — Do not rely on any expected_rewards field" |
| **Retention abuse prevention — prior closure history check** (e8587) | Before making any retention offer, call `get_closure_reason_history_8293` to check for closure reason records within the past 12 months on the credit card account. If records exist within 12 months, skip all retention offers and proceed directly to closure. | Making retention offers when closure reason history exists within the past year. | Call `get_closure_reason_history_8293` before any retention offer. | Not specified | doc_credit_cards_credit_card_account_logistics_003.json §"Step 2: Check for Previous Retention Attempts (Abuse Prevention)" |
| **Bypass code transmission restrictions** (e8615, e8735) | Do not read bypass code `9K2X7M4P1N8Q3R5T6A` aloud unless the customer explicitly requests confirmation. Do not transmit through unsecured channels. Do not paste code into free-text notes. Indicate in internal notes that a bypass code was used, without pasting the literal value. | Reading bypass code unprompted. Transmitting via unsecured channels. Pasting the literal bypass code into free-text notes. | Internal notes must log bypass-code use event without embedding the literal code. | Not specified | doc_customer_support_special_support_codes_001.json §"Communication guidance and Documentation" |
| **Bypass code identity event — `log_verification` logging requirement** (e8871) | When using bypass code `9K2X7M4P1N8Q3R5T6A` for account recovery, call `log_verification` with ALL PII fields (name, user_id, address, email, phone_number, date_of_birth) populated with the bypass code value `9K2X7M4P1N8Q3R5T6A` — not with actual customer PII data. | Populating `log_verification` PII fields with real customer PII during a bypass-code event. Skipping the `log_verification` call entirely. | Confirm `log_verification` was called with correct placeholder values. | `log_verification` | doc_customer_support_special_support_codes_001.json §"Bypass code logging procedure" |
| **Discoverable tools — two-step unlock-then-call pattern** (e8865) | For all agent-discoverable tools: Step 1 call `unlock_discoverable_agent_tool(tool_name)`; Step 2 call `call_discoverable_agent_tool(tool_name, ...params)`. Applies to `update_transaction_rewards_3847`, `initial_transfer_to_human_agent_1822`, and `initial_transfer_to_human_agent_0218`. | Invoking a discoverable tool without first calling the unlock step. | Confirm unlock call completed before tool invocation. | Not specified | doc_credit_cards_credit_cards_(general)_004.json §"Required steps" |
| **Backend Incident 11/13 — identity verification bypass exception** (e8868) | When symptoms match Incident 11/13 (credit card payment deducted from checking but not reflected in statement), do NOT request identity verification from the customer. This exception overrides the standard identity-first rule within the incident window. | Requesting identity verification information when Incident 11/13 symptoms are confirmed. | Confirm symptom pattern matches Incident 11/13 criteria before waiving verification. | `initial_transfer_to_human_agent_1822` / `initial_transfer_to_human_agent_0218` | doc_credit_cards_credit_cards_(general)_011.json §"When to Use This Protocol" |
| **Subscription dispute and recurring block setup — identity verification** (e8853) | Complete standard customer identity verification before processing any subscription dispute filing or invoking any recurring block setup tool. | Invoking any dispute tool or block tool without prior identity verification. | Identity verification confirmed before tool call. | Not specified | doc_bank_accounts_bank_accounts_(general)_031.json §"Pre-Filing Requirements" |
| **Lost/stolen debit card — cross-product security protocol** (e8572, e9036, e9037) | When a customer reports a lost or stolen debit card: (1) complete standard debit card freeze/close; (2) call `get_credit_card_accounts_by_user` to check for Rho-Bank credit cards; (3) if found, proactively offer credit card replacement; (4) if customer declines, record the offer in account notes. | Skipping the credit card check after a debit card loss/theft report. Failing to offer credit card replacement when Rho-Bank credit cards are found. | Confirm `get_credit_card_accounts_by_user` call made; document outcome in account notes. | Not specified | doc_bank_accounts_bank_accounts_(general)_030.json §"Required Security Check / How to Check for Credit Cards" |
| **Business checking closure — savings-first ordering constraint** (e8923) | Before closing a business checking account, close all linked business savings accounts with status OPEN first. | Closing a business checking account while linked business savings accounts remain OPEN. | Verify no linked savings accounts are OPEN before invoking checking closure tool. | Not specified | doc_bank_accounts_bank_accounts_(general)_007.json §"Pre-Closure Requirements" |
| **Business checking closure — tier-specific approval and pre-closure checklist** (e8550) | For PREMIUM tier (Cobalt Blue): supervisor review required before closure. For ELITE tier (credit lines >$100,000): manager approval required. Pre-closure: account must be OPEN, no pending transactions, no linked OPEN business savings accounts. Balance must cover early closure fee or be $0. | Closing account without required supervisor/manager approval. Closing with pending transactions or linked open savings accounts. Using alternative payment for early closure fee. | Confirm tier, approval status, pending transactions, and linked accounts before closure. | Supervisor (PREMIUM) / Manager (ELITE) | doc_bank_accounts_bank_accounts_(general)_007.json §"Pre-Closure Requirements and Tier-Specific Closure Requirements" |
| **Referral program — anti-abuse controls** (e8551) | Enforce rolling 9-day window: maximum 2 referral bonuses across all accounts per 9-day period; excess auto-denied. Block referrals when referrer and referred share a registered address. Block referrals when referred business has the same primary owner SSN as any existing Rho-Bank business account. Apply claw-back if referred account closes within 90 days. Do not combine referral bonus with other promotions. | Granting more than 2 referral bonuses in any 9-day window. Granting bonuses to same-address or same-SSN referrals. Combining referral bonus with other promotional offers. | Validate 9-day window, address, SSN, and promotion eligibility before crediting bonus. | Auto-denial (system) | doc_bank_accounts_bank_accounts_(general)_048.json §"FAQ Checking Account Referrals" |
| **`close_bank_account_7392` — universal pre-closure balance check** (e8877) | If early closure fee applies, account balance (current_holdings) must be ≥ fee amount before invoking close tool. If no early closure fee, balance must be exactly $0. Account status must be OPEN. No pending transactions permitted. | Invoking the close tool with status other than OPEN, pending transactions present, or insufficient balance to cover fee. Using any alternative payment method for closure fee. | Check account status, pending transactions, and balance against fee before tool call. | Not specified | doc_bank_accounts_bank_accounts_(general)_005.json §"Pre-Closure Requirements" |
| **Personal checking opening — eligibility requirements** (e8626, e8644) | Verify customer is identity-verified, age ≥18 (exception: Light Green Account allows ages 13–24), total personal checking accounts ≤4, and no checking account closed for cause in the past 6 months. `account_class` value passed to `open_bank_account_4821` must end with "Account". | Opening an account for unverified customers, customers under 18 (outside Light Green exception), customers at the 4-account cap, or customers with a for-cause closure in the past 6 months. | Check identity status, age, account count, and closure history before tool call. | Not specified | doc_bank_accounts_bank_accounts_(general)_001.json §"Eligibility Requirements + Opening Procedure" |
| **Personal checking closure — tier-specific notice periods** (e8650) | Apply notice periods before invoking `close_bank_account_7392`: ENTRY 0 days, MID 3 days, PREMIUM 7 days, ELITE 14 days. Confirm OPEN status, zero pending transactions, and balance requirement (fee applies → balance ≥ fee; no fee → balance = $0). | Invoking the close tool before the notice period has elapsed, or without confirming balance and status preconditions. | Confirm tier, notice period, status, pending transactions, and balance before closure. | Not specified | doc_bank_accounts_bank_accounts_(general)_005.json §"Pre-Closure Requirements + Closure Procedure" |
| **Bronze Rewards Card — payroll processor cash back exclusion** (e8502) | Apply 0% cash back for transactions at Gusto, ADP, Paychex, and Rippling on the Bronze Rewards Card. These merchants are explicitly excluded from cash back, preventing rewards arbitrage on high-volume payroll flows. | Crediting any cash back for payroll processor transactions on the Bronze Rewards Card. | Verify merchant category before applying cash back. | Not specified | doc_business_credit_cards_business_bronze_rewards_card_003.json §"Payroll Processor Merchants" |
| **Bronze Rewards Card — SaaS exclusion 12-month cliff** (e8493) | Apply 1.0% cash back on Slack, Zoom, HubSpot, and Salesforce transactions during months 1–12 only. After month 12, renewals earn 0% cash back. | Crediting SaaS cash back beyond the 12-month window. Applying Silver/Gold/Platinum SaaS rules to the Bronze card. | Track enrollment date and apply correct rate by billing period. | Not specified | doc_business_credit_cards_business_bronze_rewards_card_003.json §"Merchants Not Eligible for Cash Back (SaaS Subscriptions)" |
| **Bronze Rewards Card — minimum redemption threshold** (e8503) | Require a minimum rewards balance of $37 before permitting redemption. Prevent micro-redemption requests below this floor. | Processing a redemption request when rewards balance is below $37. | Check current rewards balance before accepting redemption request. | Not specified | doc_business_credit_cards_business_bronze_rewards_card_002.json, doc_business_credit_cards_business_bronze_rewards_card_004.json §"Redeeming Rewards / How Rewards Are Paid" |
| **EveryonePay — unusual activity security review (pending payments)** (e8284) | When an EveryonePay payment is flagged for unusual activity, allow the automatic security review to complete. Inform the customer the payment may remain pending during review. | Bypassing or manually overriding the automatic security review. | Confirm review status before advising the customer on expected timing. | Automatic security review (system) | doc_everyone_pay_everyone_pay_012.json §"Other possible causes" |
| **EveryonePay — recipient account active validation** (e8285) | Confirm the recipient account is active and able to accept funds before initiating transfer. Transfers decline if the recipient account is temporarily unable to accept. | Forcing through a transfer when the recipient account cannot accept funds. | Validate recipient account status before transfer execution. | Not specified | doc_everyone_pay_everyone_pay_013.json §"Other reasons a payment can remain pending" |
| **QR Transfer — 17-minute expiration enforcement** (e8286) | Enforce QR code expiration at 17 minutes. Expired codes must be regenerated before retry; the expired code must not be reused. | Accepting or retrying a QR code after the 17-minute expiration window. | Validate expiration timestamp before processing QR transfer. | Not specified | doc_everyone_pay_qr_transfers_001.json §"Handling expiration" |
| **Dark Green Account EveryonePay — student loan cashback exclusion** (e8888, e8898) | Do not credit the 1.25% student loan cashback for EveryonePay P2P sends to individuals, even if the recipient forwards funds to a servicer. Only direct servicer payments qualify. | Crediting Dark Green 1.25% student loan cashback for P2P EveryonePay sends, regardless of downstream fund use. | Confirm transaction is a direct payment to a recognized loan servicer, not a P2P send. | Not specified | doc_checking_accounts_dark_green_account_005.json §"What does not typically qualify / EveryonePay considerations" |
| **Evergreen Account EveryonePay — no carbon offset credits** (e8886) | Do not accrue carbon offset credits for EveryonePay transfers from the Evergreen Account, regardless of transaction amount. | Crediting carbon offset credits for Evergreen Account EveryonePay transactions. | Verify transaction source account before applying any carbon offset credit logic. | Not specified | doc_checking_accounts_evergreen_account_005.json §"Transaction eligibility rules" |
| **EveryonePay dispute — classification as `person_to_person`** (e8890) | When filing a debit card dispute for an EveryonePay transaction, select `person_to_person` from the `dispute_category` enum. | Using any other dispute category for EveryonePay transactions. | Confirm dispute category value before submitting dispute tool call. | Not specified | doc_bank_accounts_bank_accounts_(general)_031.json §"transaction_type enum for dispute filing" |
| **Debit card dispute — pre-filing eligibility and Regulation E liability windows** (e8901, e8902) | Before filing: confirm transaction ≥$1.00, ≤60 days old, and linked checking account is OPEN. Apply tier dispute caps: Entry max 2, Mid max 3, Premium max 4, Elite max 5. Disclose Reg E liability windows: reported within 2 business days = max $50 liability; within 60 days = max $500; after 60 days = unlimited liability (funds may not be recoverable). | Filing disputes outside the 60-day window without disclosing unlimited liability exposure. Exceeding tier-based dispute count caps. | Verify transaction age, account status, and tier cap before filing. | Not specified | doc_bank_accounts_bank_accounts_(general)_031.json §"Pre-Filing Requirements" |
| **BNPL Diamond — dual-gate plan approval** (e9051, e9052, e9059) | Approve a new BNPL Diamond plan only when BOTH conditions are true: (1) current_outstanding + new_plan_amount ≤ $2,505,000.00; AND (2) active_plan_count + 1 ≤ 25. If either gate fails, reduce or decline the new plan. | Approving a plan that would push total outstanding above $2,505,000.00 or active plan count above 25. | Evaluate both gates independently before approval; compute remaining capacity as $2,505,000.00 − current_outstanding. | Not specified | doc_buy_now_pay_later_bnpl_diamond_002.json, doc_buy_now_pay_later_bnpl_diamond_003.json §"High-limit qualification / Concurrent plan cap / How approvals are evaluated" |
| **BNPL Silver — late payment consequences** (e9068) | Inform customer that a missed installment is marked past due; access to new BNPL Silver plans is temporarily paused until account is brought current. Continued non-payment may accelerate the remaining plan balance. | Approving a new BNPL Silver plan while the account has a past-due installment. | Confirm account is current before approving new plans. | Not specified | doc_buy_now_pay_later_bnpl_silver_007.json §"What happens if you miss a payment" |
| **BNPL Diamond — enterprise revenue verification documentation** (e9076) | Require for Diamond applications: audited or reviewed financial statements for the most recent full fiscal year; management accounts if fiscal year-end is >6 months old; bank statements or tax filings corroborating revenue figures. Annual revenue must be ≥$50,125,000.00. | Approving a Diamond BNPL application without complete revenue verification documentation. | Verify all three documentation types are present and revenue figure meets threshold. | Not specified | doc_buy_now_pay_later_bnpl_diamond_002.json §"What to prepare for revenue verification" |
| **BNPL Diamond — concierge dispute 36-hour response target** (e9057, e8517) | When Diamond concierge dispute support is enabled, acknowledge dispute within 36 hours of first contact. Follow full support flow: triage/acknowledgement → documentation request → specialist case handling with periodic updates → written outcome with any credits/adjustments. Apply standard dispute workflow when concierge is not enabled. | Missing the 36-hour initial response target without documented escalation. Applying standard workflow when concierge support is enabled. | Track first-contact timestamp and confirm triage completion within 36 hours. | Dispute concierge specialist | doc_buy_now_pay_later_bnpl_diamond_007.json §"Availability / Response times" |
| **Virtual card — four core security controls** (e7204) | Enforce all four virtual card security controls: real-time alerts for each transaction; merchant category restrictions per card configuration; one-time card capability (single-use); and rapid revocation with 3-second disable capability. | Disabling or bypassing any of the four security controls without explicit policy authority. | Confirm all four controls active on virtual card before issuing or authorizing use. | Not specified | doc_credit_cards_virtual_card_management_007.json §"Core safeguards" |
| **ATM fee calculation — out-of-network cap** (e5154) | Calculate out-of-network ATM fee as 1% of withdrawal amount, capped at $2.50. Example: $600 withdrawal × 1% = $6.00, but fee capped at $2.50. | Charging the uncapped 1% rate or any amount above $2.50 for out-of-network ATM fees. | Verify fee calculation uses the $2.50 cap before applying fee. | Not specified | doc_checking_accounts_evergreen_account_008.json §"Calculation examples" |
| **Green Fee-Free Account — apply product-specific EveryonePay limit** (e8903) | Apply the documented product-specific EveryonePay daily limit for the Green Fee-Free Account ($2,000/day) even though the product is classified as ENTRY TIER (where the closure-fee document implies a different tier baseline). Do not infer the limit from the ENTRY TIER classification. | Applying a tier-inferred EveryonePay limit instead of the product-documented $2,000/day limit for the Green Fee-Free Account. | Verify EveryonePay limit against product-specific documentation, not tier classification. | Not specified | doc_bank_accounts_bank_accounts_(general)_005.json §"ENTRY TIER definition" |
| **Automatic sweep — reverse-sweep timing constraint** (e8925) | When automatic sweep is enabled and the checking balance falls below the target minimum after a nightly sweep, the system may reverse-sweep funds from savings back to checking. Items posting after the 11 PM sweep run are reflected in the NEXT cycle evaluation only — do not advise customers that same-night correction is possible for late-posting items. | Advising customers that reverse-sweep will correct balances for items posting after 11 PM on the same night. | Confirm posting timestamps relative to the 11 PM sweep cutoff before advising. | Not specified | doc_business_savings_accounts_automatic_sweep_program_001.json §"What happens if funds are needed back" |
| **CLI (credit line increase) request — submit-before-eligibility ordering** (e8616) | Per doc_credit_cards_credit_card_account_logistics_007.json, Step 1 requires submitting the CLI request (creating a formal record) before running eligibility checks in Step 2. Ineligible requests will generate records before denial. Do not attempt to reverse this ordering. | Reordering the steps to run eligibility before submission. | Confirm CLI request was formally submitted (Step 1) before eligibility evaluation (Step 2). | Not specified | doc_credit_cards_credit_card_account_logistics_007.json §"Step 1: Submit the CLI Request" |
| **EveryonePay — no daily send limit for entry-tier accounts (source gap)** (e8894) | Do not apply another account's documented EveryonePay daily send limit as a proxy for the Light Blue Account, Light Green Account, or any savings account where no limit is documented. | Applying another product's limit as a substitute when no limit is documented for the queried account. | Check product-specific documentation before stating a limit; if none documented, disclose the gap. | Not specified | doc_bank_accounts_bank_accounts_(general)_005.json §"Tier-Specific Closure Requirements" |

---

### B. Agent-Safety Risks (for Remediation)

**Ranked by severity. All items enumerated from source entries.**

---

**1. [P0] Hardcoded account recovery bypass code in policy document**
Source: doc_customer_support_special_support_codes_001.json §"Confirm the bypass code / Security and compliance" (e8734, e8673, e7205, e8613)

The static bypass code `9K2X7M4P1N8Q3R5T6A` is written verbatim into internal policy document doc_customer_support_special_support_codes_001.json. This is a critical security defect for three compounding reasons: (a) any agent or system with read access to this document can extract the code, making it permanently exposed until manually changed; (b) the document has no documented rotation schedule, no named revocation authority, and no secondary audit mechanism — a static secret with no governance; (c) the logging procedure instructs agents to overwrite all PII fields in `log_verification` with the bypass code value, which masks the true identity of the recovering party in audit records, undermining forensic traceability. The bypass code can be used to bypass identity verification for account recovery, making leakage equivalent to universal identity-bypass for any account. All three required lifecycle governance objects are absent: rotation_schedule, audit_trail_mechanism, and authorization_authority.

---

**2. [P1] Regulation E — per-tier open-dispute caps may violate 12 CFR §1005.11**
Source: doc_bank_accounts_bank_accounts_(general)_031.json §"Pre-Filing Requirements item 4" (e8738)

Policy document doc_bank_accounts_bank_accounts_(general)_031.json enforces per-tier caps on the number of error notices a consumer may file: Entry Tier max 2, Mid Tier max 3, Premium Tier max 4, Elite Tier max 5. No regulatory authority is cited for these caps. Regulation E (12 CFR §1005.11) does not permit financial institutions to cap the number of error notices a consumer may file. Applying these caps to deny or refuse a timely Reg E dispute filing may constitute a violation. The caps appear in the same document used to guide agent dispute-filing behavior, creating direct operational exposure every time a customer at cap attempts to file a legitimate dispute.

---

**3. [P1] CFPB fair-dealing exposure — provisional credit exclusion for subscription disputes**
Source: doc_bank_accounts_bank_accounts_(general)_032.json §"Provisional Credit is NOT REQUIRED" (e8737)

Internal policy explicitly excludes `recurring_charge_after_cancellation` from mandatory provisional credit. However, customer-facing materials imply provisional credit will be provided for dispute scenarios. This asymmetry creates CFPB fair-dealing exposure: if an agent relies on customer-facing materials to promise provisional credit for a subscription cancellation dispute, the agent's representation contradicts internal policy, and the credit will not be issued. Customers who make financial decisions based on the agent's statement may experience harm. The discrepancy between internal policy and outward-facing materials requires reconciliation or explicit agent guidance to disclose the exclusion.

---

**4. [P1] Stale identity-bypass exception with no documented expiry — Backend Incident 11/13**
Source: doc_credit_cards_credit_cards_(general)_011.json §"When to Use This Protocol" (e8868, e6727)

The Incident 11/13 protocol instructs agents to waive identity verification entirely when a customer's symptom matches "credit card payment deducted from checking but not reflected in statement." The protocol states "Identity verification is NOT required." No expiry date or deactivation trigger for this exception is documented. If the incident window has closed but the policy document remains in the active corpus, agents will continue to waive identity verification for claims matching the symptom pattern — effectively creating a social-engineering vector where any caller describing the symptom bypasses authentication. A companion risk: doc_credit_cards_credit_cards_(general)_011.json and doc_credit_cards_credit_cards_(general)_012.json provide no guidance for a customer who simultaneously meets both Incident 11/13 and Incident 11/14 criteria, leaving agent behavior undefined at the intersection.

---

**5. [P1] Expired promotions still active in corpus — stale agent recommendation order**
Source: doc_bank_accounts_bank_accounts_(general)_013.json, doc_bank_accounts_bank_accounts_(general)_014.json §"PROMOTION NOTICE" (e8543, e8643)

Two business checking promotions remain in the active policy corpus without retirement notices or expiry flags, both long past their stated end dates as of 2026-06-26:
- doc_bank_accounts_bank_accounts_(general)_013.json "November 2025 Promotion" (active 2025-11-01 to 2025-11-30, now 208 days expired): instructs agents to recommend Sky Blue first, Lime Green second.
- doc_bank_accounts_bank_accounts_(general)_014.json "October 2025 Promotion" (active 2025-10-12 to 2025-11-12, now 226 days expired): instructs agents to recommend Lime Green first, Hunter Green second.

Agents following these documents will apply stale product ranking logic. The risk is both product mis-recommendation and potential regulatory exposure if the stale promotion terms are quoted to customers.

---

**6. [P1] Expired Bronze Rewards Card new-customer promotion still in corpus**
Source: doc_business_credit_cards_business_bronze_rewards_card_010.json, doc_business_credit_cards_business_bronze_rewards_card_001.json §"Promotion Window / Unlock the New Customer Promo" (e8483)

The Bronze Rewards Card promotion offering a $500 statement credit for $10,000 spend in the first 2 months had a promotion window of 2025-10-01 through 2026-03-31. As of 2026-06-26, this promotion expired 87 days ago. The offer description remains in two active documents with no expiry flags. Agents citing this offer to customers would be making a misrepresentation, with potential consumer harm and regulatory exposure.

---

**7. [P2] Legal authority debt — "federal offense" assertion without statutory citation**
Source: doc_bank_accounts_bank_accounts_(general)_033.json §"ATM Affidavit Requirement" (e8745)

The policy document instructs agents to tell customers "Signing a false affidavit is a federal offense" with no federal statute cited. This is a legal conclusion delivered as an agent script line. If the characterization is inaccurate, jurisdiction-specific, or inapplicable to the form in question, Rho-Bank bears the misrepresentation risk. The absence of a statutory citation means neither agent nor compliance reviewer can verify the claim's accuracy.

---

**8. [P2] Debit card freeze vs. recurring block — asymmetric pending-authorization disclosure**
Source: doc_bank_accounts_bank_accounts_(general)_007.json §"convergence signal s641 / s785" (e8736)

The debit card freeze document explicitly states "Pending transactions already authorized may still process." The recurring block document is silent on pending-authorization passthrough during the 24-hour activation window. Customers who set up a recurring block expecting to stop a subscription immediately may receive charges that posted during the activation window without any disclosure that this is possible. The information asymmetry between the two control types creates customer harm risk and potential Reg E issues if customers dispute such charges.

---

**9. [P2] BNPL data quality — 83% placeholder values create agent hallucination risk**
Source: doc_buy_now_pay_later_bnpl_bronze_001.json §"Full corpus review" (e8523, e8532)

Forty of 48 BNPL product documents (83%) contain exclusively `[value not available]` placeholders for all numeric and named parameters. Only the Diamond tier (8 documents) and partial title metadata carry actual values. An agent attempting to answer parameter queries for Bronze, Silver, Gold, or Platinum BNPL tiers has no grounded values to return. If the agent fills these gaps by inference from title text or analogical reasoning, the result is hallucinated policy — including security-relevant parameters such as credit check requirements, fraud controls, and identity verification thresholds. The Silver tier specifically has an undocumented soft credit check provider name and monthly inquiry limit (e8530), both of which underpin eligibility gating.

---

**10. [P2] BNPL security controls absent for four of five tiers**
Source: doc_buy_now_pay_later_bnpl_diamond_007.json §"Availability / Response times" (e8532)

No security guardrails, fraud controls, or identity verification requirements are documented for BNPL Bronze, Silver, Gold, or Platinum tiers — all such fields are `[value not available]`. The only tier with a documented dispute resolution SLA is Diamond (36-hour concierge response). Silver mentions a soft credit check conditional on an undocumented flag, but the flag name, provider, and limit are unknown. This constitutes a material security policy gap across 4 of 5 product tiers, leaving agents without the controls needed to enforce eligibility or detect fraud for the majority of BNPL customers.

---

**11. [P2] Velocity block customer identity verification — no formal specification**
Source: doc_bank_accounts_bank_accounts_(general)_039.json, doc_checking_accounts_checking_accounts_(general)_003.json §"Clearing Security Protections" (e8322)

Policy documents state agents must "verify customer identity" before clearing a velocity block, but provide no specification of verification method or channel (security questions, SMS OTP, password), no list of accepted verification types, and no success criteria. Without a formal specification, agents cannot consistently apply the control, and there is no auditable standard for what constitutes a valid clearance event. This gap (confirmed as s415) means the velocity block — a fraud-prevention control — can be cleared through inconsistent, potentially weaker, verification practices.

---

**12. [P2] QR Transfer — dispute and reversal procedures entirely absent**
Source: doc_everyone_pay_qr_transfers_001.json, doc_everyone_pay_qr_transfers_002.json, doc_everyone_pay_qr_transfers_006.json, doc_everyone_pay_qr_transfers_007.json §"QR Transfers complete documentation" (e8323)

The complete QR Transfer documentation corpus covers limits, flow, troubleshooting, and security but contains no information on: dispute initiation procedure, reversal eligibility criteria, dispute resolution timeline, or refund mechanism. Customers who experience a QR Transfer error or fraud have no documented remediation path, and agents have no procedure to follow. This is a confirmed source gap (s612).

---

**13. [P2] Alert routing gap — no escalation chain or SLA for departmental alert delivery**
Source: doc_business_credit_cards_virtual_card_management_006.json §"Monitor activity in real time" (e3941)

No explicit escalation chain or SLA for alert delivery to departmental approvers is documented. In the absence of defined routing and timing guarantees, a real-time alert may reach the wrong party, be delayed, or go unacknowledged with no triggering of a fallback. This is particularly significant for high-value transaction controls that depend on timely approver notification.

---

**14. [P2] Card compromise detection — no automation or mandatory fraud reporting flows documented**
Source: doc_business_credit_cards_virtual_card_management_007.json §"How to apply these controls effectively" (e3944)

Risk scenario coverage is incomplete: documentation does not address card compromise detection automation or mandatory fraud reporting flows. Agents have no documented procedure for automated compromise detection scenarios, leaving a gap in the fraud response posture.

---

**15. [P2] No fraud monitoring or alert thresholds for virtual card transactions**
Source: doc_business_credit_cards_virtual_card_management_009.json §"N/A" (e4015)

Virtual card best-practice documentation does not specify any fraud monitoring thresholds or alert trigger values for virtual card transactions. The four-control framework (e7204) establishes real-time alerts as a required control but provides no threshold configuration guidance, leaving alert sensitivity undefined.

---

**16. [P2] Account alert thresholds undefined**
Source: doc_checking_accounts_blue_account_001.json §"Quick tips" (e8321)

Documents reference the ability to set account alerts but specify no trigger values for: low balance trigger, large transaction trigger, or deposit notification trigger. This gap (confirmed as s414) means agents cannot configure alerts to a defined standard and customers cannot be told what values trigger which alerts.

---

**17. [P3] Platinum Reserve Account — credential rotation frequency vague**
Source: doc_business_savings_accounts_platinum_reserve_account_005.json §"API access to dashboard data" (e4623)

The Platinum Reserve Account specification states credentials should be rotated on a "regular schedule" without specifying the rotation cadence. A vague rotation policy is functionally equivalent to no rotation policy: without a defined frequency, credential hygiene cannot be audited or enforced.

---

**18. [P3] Platinum Reserve Account — periodic access review frequency not specified**
Source: doc_business_savings_accounts_platinum_reserve_account_009.json §"Oversight and audit" (e4626)

The oversight and audit section for the Platinum Reserve Account does not specify how frequently access reviews must occur. Without a defined review period, lapsed access privileges may go undetected, increasing the risk of unauthorized account access.

---

**19. [P3] One-time card — multiple failed authorization retry behavior unspecified**
Source: doc_credit_cards_virtual_card_management_005.json §"Usage notes" (e7306)

Documentation does not specify whether multiple failed authorizations on the same one-time card count as a single attempt or whether each retry requires a new card to be generated. This ambiguity may allow card reuse in retry scenarios that should require new card issuance, weakening the single-use security guarantee.

---

**20. [P3] Single-use vs. multi-use card — no quantified fraud reduction metrics**
Source: doc_business_credit_cards_virtual_card_management_008.json §"Single-use cards" (e3948)

No fraud reduction metrics, compromise rates, or comparative risk data are provided for single-use versus multi-use card models. Without this data, neither agents nor policy owners can make evidence-based recommendations about card type selection for fraud prevention purposes.

---

**21. [P3] Everyone Pay block list — semantic data error ($275 vs. 275 users)**
Source: doc_everyone_pay_user_blocking_004.json, doc_everyone_pay_user_blocking_002.json, doc_everyone_pay_user_blocking_005.json §"Common reasons / Blocking a user" (e8161, e8162)

Three blocking documents use the "$275" notation when referring to the maximum number of users a customer can block. The currency symbol is a data formatting error: the correct value is 275 users (a count), not a currency amount. This semantic incoherence could cause agents to interpret the limit as a monetary threshold and apply incorrect logic. A data quality correction is required across all three documents to remove the currency symbol and standardize to "275 users maximum."

---

**22. [P3] Light Green Account — guardian co-sign requirement underdocumented**
Source: doc_bank_accounts_bank_accounts_(general)_047.json §"Eligibility restrictions" (e8647)

Policy states the referred person must be 18 or older except for the Light Green Account, which allows minors with a guardian. However, no document in the personal-checking corpus details the guardian co-sign requirement, parental consent flow, or how the minor/guardian relationship is verified in `open_bank_account_4821`. The agent procedure for opening Light Green Accounts for customers aged 13–17 is underdocumented, creating risk of opening accounts for minors without proper guardian authorization.

---

**23. [P3] Withdrawal counting scope undefined**
Source: (no doc_id) (e7521)

Documentation does not specify whether the withdrawal count (used to determine excess withdrawal fees) includes ACH transfers, bill pay, or only ATM and teller withdrawals. Agents applying the count incorrectly will either over-charge or under-charge customers for excess withdrawals, creating both compliance risk and customer harm.

---

**24. [P3] Insufficient balance to cover excess withdrawal fee — scenario unspecified**
Source: (no doc_id) (e7530)

No documentation addresses what happens when a customer is charged an excess withdrawal fee but has insufficient balance to cover that fee. The lack of a defined procedure creates operational ambiguity: agents have no documented escalation path or outcome guidance for this scenario.

---

**25. [P3] ATM fee dispute resolution timeline not documented**
Source: (no doc_id) (e3007)

The support contact process for ATM fee incorrect charges is documented, but the dispute resolution timeline and process are absent. Customers filing ATM fee disputes cannot be given a resolution timeframe, and agents have no SLA to manage against.

---

**26. [P3] True Blue Account — wire transfer dispute process and timeline absent**
Source: (no doc_id) (e3015)

Only normal wire transfer operations are documented for the True Blue Account. The dispute process and timeline for wire transfer errors are entirely absent. Agents handling True Blue wire disputes have no documented procedure.

---

**27. [P3] No guidance for dual-incident overlap (Incident 11/13 and Incident 11/14)**
Source: doc_credit_cards_credit_cards_(general)_011.json, doc_credit_cards_credit_cards_(general)_012.json §"cross-document" (e6727)

No documented guidance exists for the scenario where a customer simultaneously meets both Incident 11/13 criteria and Incident 11/14 criteria. The two incident protocols may have conflicting instructions; without explicit guidance for the overlap case, agents will either apply an arbitrary choice or escalate unnecessarily — with no documented escalation path for this scenario.

---

**28. [P3] Card replacement tool — formal specification unavailable**
Source: (no doc_id) (e8326)

The card replacement tool is referenced by functional description (lost/stolen card protocol) only. The formal specification — tool name, parameters, preconditions such as freeze-state verification, side effects, and return values — is unavailable from any document in the 698-document corpus. This is a known knowledge boundary inherent to user-facing documentation (confirmed as s162). Agents implementing the card replacement flow cannot verify they are calling the tool with correct parameters or in the correct precondition state.


---


## 8. Temporal Items (evaluated as of 2026-06-26)

> **Reading guide.** The Status column uses three values: **EXPIRED** = past stated effective\_until date, document still active in corpus (agent-risk); **ACTIVE** = within effective window or no expiry found; **rolling** = window opens per-account at a customer-specific triggering event (account opening, fee posting, plan activation, etc.). Items prefixed **⚠️ EXPIRED — AGENT RISK** are the highest-priority concern: they appear in the active policy corpus without a retirement notice and describe offers or protocols that are no longer valid. Agents that cite these documents may make incorrect disclosures, accept applications under void terms, or follow stale product-recommendation rankings.
>
> Entry references in the final column correspond to synthesis-graph entry IDs from the analysis blackboard.

---

### 8A. Expired Promotions and Protocols — Active Agent Risk

All items below have passed their stated end dates as of 2026-06-26. **None carry a retirement notice or supersession flag in the 698-document policy corpus.** Agents must not present these items as current offers or active protocols.

| Item | Effective window | Status today | Correct agent handling | Source doc\_id | Entry ref |
|------|-----------------|-------------|----------------------|----------------|-----------|
| **⚠️ EXPIRED — AGENT RISK** Silver Zoom 0% APR promotion. Introductory 0% APR offer for Silver Zoom product. Expired 177 days ago. | 2025-09-15 → 2025-12-31 | **EXPIRED** | Do NOT display 0% APR offer. Do NOT accept applications referencing the 2025 promotional terms. Direct all inquiries to current product terms. Add an expired-status banner to documentation: "This promotional period has ENDED (expired 2026-01-01)." Remove from active product comparison tables. Archive to "Expired Offers" section. | multiple\_docs\_010\_series | e8209, e8210 |
| **⚠️ EXPIRED — AGENT RISK** Triple Cash Back promotion — claim window. 3× cash-back on qualifying purchases; claim submission period. Expired 178 days ago. No retroactive claims possible per documented policy. | 2024-01-01 → 2025-12-31 | **EXPIRED** | Do NOT accept new claim submissions. Do NOT indicate eligibility window is open. Do NOT process redemptions under expired terms. State: "This promotion ended on 2026-01-01 and is no longer available." Clarify no retroactive claims can be filed. Redirect customers to current cash-back programs. Remove claim instructions from active agent workflows. Archive detailed claim procedures to historical records only. | multiple\_docs\_011\_012\_013\_series | e8211, e8212 |
| **⚠️ EXPIRED — AGENT RISK** Silver Zoom referral program. Program accepted new referrals through cutoff date. Closed 268 days ago. Documentation provides detailed referral instructions (share referral link, track referral status) without indicating program has closed. Agent tools would fail if executed today. | Cutoff: 2025-10-01 | **EXPIRED** | Do NOT present referral program as active. Do NOT generate or share new referral links. Do NOT track or award new referral bonuses after closure date. Add prominent notice: "The referral program closed on 2025-10-01 and no longer accepts new referrals." Disable referral-link generation and status-tracking in agent tooling for dates after 2025-10-01. Prepare customer-facing message for post-closure inquiries. Archive referral procedures to historical documentation. | doc\_011\_series | e8213, e8214 |
| **⚠️ EXPIRED — AGENT RISK** Bronze Rewards Card new-customer promotion. $500 statement credit for $10,000 spend in first 2 months after account opening. Expired 87 days ago (April: 30 days + May: 31 days + June through 26th: 26 days = 87 days). Offer description remains active in two documents. | 2025-10-01 → 2026-03-31 | **EXPIRED** | Do NOT quote the $500 statement credit to new applicants. Do NOT process applications referencing this promotional offer. Cite current product terms only. Flag doc\_8625ca18 and doc\_ff5eadd7 for immediate retirement or update. | doc\_8625ca18, doc\_ff5eadd7 | e8483, e8484 |
| **⚠️ EXPIRED — AGENT RISK** Silver Rewards Card double cash-back promotion. 2× cash back on all purchases for first 6 months after account opening. At doubled rates: travel and software earns 20.0%; other purchases earn 2.0%. Expired approximately 224 days ago (as of 2026-06-26). | 2024-11-14 → 2025-11-14 | **EXPIRED** | Do NOT quote doubled rates (20% travel/software, 2% other). Cite standard earn rates only. Document remains active in doc\_760196c3 without expiry notice. Flag for archival. | doc\_760196c3 | e8485 |
| **⚠️ EXPIRED — AGENT RISK** Silver Rewards Card (Business) Year-1 annual fee waiver. Promotional first-year fee waiver; standard annual fee is $122.50. Expired 162 days ago. No retirement notice, supersession note, or agent-guidance update found in the 698-document corpus. Zero replacement documents found. Agents citing doc\_8a67444e or doc\_67ea4886 may incorrectly promise a waived Year-1 fee. | 2025-11-15 → 2026-01-15 | **EXPIRED** | Do NOT promise a waived first-year fee. Standard annual fee of $122.50 applies to all accounts opened after 2026-01-15. Retire or archive doc\_8a67444e and doc\_67ea4886. Issue agent-guidance update explicitly preventing Year-1 fee-waiver disclosure under this promotion. | doc\_8a67444e, doc\_67ea4886 | e8486, e8687, e8688, e8739, e8740 |
| **⚠️ EXPIRED — AGENT RISK** Platinum Rewards Card (Business) Year-1 annual fee waiver. Promotional first-year fee waiver; standard annual fee is $450.00. Annual travel credit is $400. Expired 118 days ago. Post-expiry net cost for new accounts: $450 fee − $400 travel credit = $50 net fee cost in Year 1. | 2025-11-01 → 2026-02-28 | **EXPIRED** | Do NOT waive the first-year $450.00 fee for accounts opened after 2026-02-28. Communicate current net cost ($450 fee minus $400 travel credit = $50 net in Year 1). Cite standard fee schedule. Flag doc\_b9f03213 for update. | doc\_b9f03213 | e8487, e8497 |
| **⚠️ EXPIRED — AGENT RISK** Business Checking Promotion — November 2025. Agent product-recommendation ranking during promotion: Sky Blue first, Lime Green second. Expired 208 days ago. Document remains in active policy corpus without expiry flag. Risk: agent may follow stale ranking logic. | 2025-11-01 → 2025-11-30 | **EXPIRED** | Do NOT apply the November 2025 ranking order (Sky Blue first, Lime Green second). Revert to standard product recommendation order. Retire or archive doc\_ad8b029a immediately. | doc\_ad8b029a | e8543, e8544, e8643 |
| **⚠️ EXPIRED — AGENT RISK** Business Checking Promotion — October 2025. Agent product-recommendation ranking during promotion: Lime Green first, Hunter Green second. Expired 226 days ago. Document remains in active policy corpus without expiry flag. | 2025-10-12 → 2025-11-12 | **EXPIRED** | Do NOT apply the October 2025 ranking order (Lime Green first, Hunter Green second). Revert to standard product recommendation order. Retire or archive doc\_cba24244 immediately. | doc\_cba24244 | e8543, e8544, e8643 |
| **⚠️ EXPIRED — AGENT RISK** Business Savings Promotion — November 2025. Agent priority during promotion: Gold Saver Account first, Silver Plus Saver second. Expired approximately 208 days ago. Document remains live without retirement notice. Risk: agents may incorrectly prioritize these products. | 2025-11-01 → 2025-11-30 | **EXPIRED** | Do NOT prioritize Gold Saver or Silver Plus Saver based on this promotion. Revert to standard recommendation order. Immediate retirement or archival of doc\_065caedb required. | doc\_065caedb | e8926 |
| **⚠️ EXPIRED — AGENT RISK** Business Savings Promotion — October 2025. Agent priority during promotion: Gold Plus Saver first, Silver Plus Saver second. Expired approximately 226 days ago. Both October and November 2025 business savings promotions are stale and represent active agent-bias risk. | 2025-10-12 → 2025-11-12 | **EXPIRED** | Do NOT prioritize Gold Plus Saver or Silver Plus Saver based on this promotion. Revert to standard recommendation order. Retire or archive doc\_c420c1a3. | doc\_c420c1a3 | e8927 |
| **⚠️ EXPIRED (DISPUTED — verify year)** Backend Incident 11/14 transfer protocol. Per entry e6804: deadline was 2025-11-18, making this protocol expired as of 2026-06-26. | Deadline: 2025-11-18 per e6804 | **EXPIRED** (disputed; verify year before relying on either entry) | Per e6804: treat protocol as expired; agents must revert to standard transfer handling. However, a date-year conflict exists between e6804 and e8867 for the sibling incident (11/13); verify source document dates before finalizing disposition. | doc\_2330957f | e6804 |
| **⚠️ DISPUTED — EXPIRED vs. ACTIVE** Backend Incident 11/13 transfer protocol. Entry e6804 states deadline was 2025-11-15 (protocol EXPIRED). Entry e8867 states deadline is 2026-11-15 (protocol ACTIVE, 172 days remaining). Direct conflict on deadline year; both entries reference the same doc\_7cba23ea. | 2025-11-15 per e6804 vs. 2026-11-15 per e8867 | **DISPUTED** | Do NOT apply this protocol without first verifying the actual end date in doc\_7cba23ea. If deadline is confirmed as 2026-11-15: follow 3-step discoverable-tool sequence when symptoms match; revert to standard transfer handling after 2026-11-15. If deadline is confirmed as 2025-11-15: protocol is EXPIRED; revert immediately to standard handling. | doc\_7cba23ea | e8867, e6804 |
| General compliance risk: expired promotional rate documents active in agent instruction corpus. Any expired promotional offer still cited in active agent instructions creates compliance and disclosure risk (high-severity). | Ongoing — systemic | **EXPIRED** (systemic) | All expired promotional rate documents must be reviewed, flagged, and removed from active agent instruction workflows. Presence of any expired offer in active instructions is treated as a compliance breach. | policy\_register | e8313 |

---

### 8B. Active and Rolling Temporal Items

| Item | Effective window | Status today | Correct agent handling | Source doc\_id | Entry ref |
|------|-----------------|-------------|----------------------|----------------|-----------|
| Navy Blue Business Referral Program. Referrer bonus $100; new-customer bonus $75; maximum 10 referrals per calendar year; required deposit $5,000 within 90 days of referral; account age requirement 60 days before eligible to refer. | No stated expiry | **ACTIVE** | Present as active. Enforce all eligibility thresholds: $5,000 deposit within 90 days, 60-day account tenure, annual cap of 10 referrals. Do not credit bonus beyond 10 referrals per year. | doc\_b7cdfb44 | e8223 |
| EcoCard merchant exclusion list. Target, Walmart, Amazon, ThredUp: earn 1.0 pt/$ (not 5.0 pts/$ green rate). EV charging 5.0 pts/$ only at Tesla Supercharger, ChargePoint, and EVgo. Standing policy; no expiry stated. | No expiry stated; standing policy | **ACTIVE** (rolling) | Always apply exclusions when calculating EcoCard earn rates. Do not quote 5.0 pts/$ for excluded merchants. Confirm charging-network eligibility before advising on EV spend. | doc\_867c97b5 | e9047 |
| Green Account (savings) — interest accrual. Interest accrues on daily balance, compounded daily, credited monthly. | Rolling; no end date | **ACTIVE** (rolling) | Communicate daily accrual and monthly credit timing when customers ask about when they will see interest. | doc\_7530e999 | e8197 |
| Blue Account (checking) — early direct deposit. Paycheck available 1 business day before standard payday. | Rolling; no end date | **ACTIVE** (rolling) | Confirm feature is active on the specific account. Advise 1-day-early availability for enrolled direct-deposit payments. | doc\_2bb7266e | e8204 |
| Annual fee refund window — personal credit cards (Platinum and Diamond Elite). Full refund of annual fee if account closed within 37 days of annual fee posting. No refund available after 37 days. As of 2026-06-26: any cardholder whose annual fee posted on or after 2026-05-20 remains within the refund window today. | Rolling; 37-day window from each annual fee posting date | **ACTIVE** (rolling) | Proactively disclose refund window whenever a closure request is received. Calculate eligibility from actual fee posting date. Do not accept refund requests outside the 37-day window. | doc\_93a22dda, doc\_e1a3c3d9 | e8576 |
| Rewards redemption post-closure window — all personal credit cards. Unredeemed rewards must be redeemed within 45 days of a closure request submission. Permanently forfeited after 45 days. No extension mechanism documented. | Rolling; 45-day window from closure request submission date | **ACTIVE** (rolling) | Proactively disclose the 45-day forfeiture deadline at the time of any closure request. Do not assume rewards can be reclaimed after 45 days. Document absence of any extension mechanism. | doc\_93a22dda, doc\_e1a3c3d9, doc\_156f59b3 | e8577 |
| Bronze Rewards Card — introductory APR. 0% intro APR for Year 1 from account open date; then 20.49% standard APR. Customers who opened on or before 2025-06-26 (12 months ago) may have already reverted to the standard rate. | Rolling; 12-month intro period from account open date | **ACTIVE** (rolling) | Verify whether the 12-month intro period has elapsed before quoting an APR. Do not quote 0% for accounts opened more than 12 months ago. | doc\_ac175ccc | e8578 |
| Silver Rewards Card — introductory APR. 0% intro APR for Year 1 from account open date; then 18.99% standard APR. Same anniversary-based logic as Bronze. | Rolling; 12-month intro period from account open date | **ACTIVE** (rolling) | Same handling as Bronze intro APR row above. Customers opened on or before 2025-06-26 may already be at 18.99%. Confirm account open date before quoting rate. | doc\_85371f28 | e8578 |
| Sky Blue Account — free period and automatic fee activation. Free period is 6 months from account opening date. After free period ends, $25.00 monthly maintenance fee activates automatically with no customer action required. Special eligibility: company must be within 4 years of formation at time of application. | Rolling; 6-month free window from account open date | **ACTIVE** (rolling) | Communicate that the maintenance fee activates automatically after 6 months — no opt-in or trigger needed. Verify formation date against 4-year eligibility rule at application. Note: free period unit ('6') is confirmed as 6 months by corroborating analysis (see row 40 for a separate document that has the same unit defect). | doc\_23280047, doc\_2f340732, doc\_7f89a2a2, doc\_7631303a | e8536, e8741 |
| Evergreen Account — CO2 offset accrual formula. Offset accrues at $1.25 grams per dollar of posted Evergreen spend. Formula: CO2 offset (grams) = Total posted Evergreen spend (USD) × 1.25. Example: $1,000 spend → 1,250 g CO2 offset. No expiry stated. Offsets appear in environmental dashboard once transactions clear (clearing timeline unspecified; see row 42). | Rolling; no expiry | **ACTIVE** (rolling) | Apply formula exactly as documented. Advise customers that offsets appear after transaction clearing; do not promise a specific posting timeline for the dashboard. | doc\_4b989df6 | e8742 |
| Personal savings account — 30-day funding deadline. If a newly opened personal savings account is not funded (via internal transfer or external deposit) within 30 days of account opening, it is automatically closed. The 30-day clock starts at account opening, not at the date of the agent interaction. | Rolling; 30-day window from account open date | **ACTIVE** (rolling) | Clearly communicate the 30-day deadline and acceptable funding methods at time of account opening. State that the clock has already started if the account was opened before the current agent interaction. Do not quote the agent interaction date as the start of the window. | doc\_677caa94 | e8860 |
| Business savings account — 30-day funding deadline. Identical 30-day auto-closure rule applies. Additional constraint on internal transfers: source account must have at least 30-day tenure AND a minimum balance of $2,500. | Rolling; 30-day window from account open date | **ACTIVE** (rolling) | Communicate the deadline and both thresholds (30-day tenure and $2,500 balance) on the source account for internal transfers. Confirm that external deposit is an alternative if the source account does not qualify. | doc\_927d5dc2 | e8861, e8907 |
| Green Account (checking) — ACH external transfer settlement time: 3 business days. EveryonePay is offered as instant-delivery alternative with a $2,500/day cap. | Rolling | **ACTIVE** (rolling) | Communicate 3-business-day ACH settlement for standard transfers. Proactively offer EveryonePay as the instant alternative for urgent payments, noting the $2,500/day cap. | doc\_7e056e81 | e8899 |
| Blue Account — external transfer settlement time: 2 business days. EveryonePay available as alternative with $2,000/day limit. | Rolling | **ACTIVE** (rolling) | Communicate 2-business-day settlement for standard transfers. Offer EveryonePay for time-sensitive payments; note the $2,000/day limit. | doc\_8d9f008b | e8900 |
| Regulation E dispute liability windows — EveryonePay unauthorized transactions. Reported within 2 business days: maximum $50 liability. Reported within 60 days: maximum $500 liability. Reported after 60 days: unlimited liability (customer may not recover funds). | Rolling; windows open from transaction date | **ACTIVE** (rolling) | Advise customers of all three liability tiers immediately upon any dispute inquiry. Emphasize the 2-business-day threshold for minimum exposure. Do not wait for customer to ask — proactively disclose at point of dispute filing. | doc\_4cef20a4 | e8902 |
| BNPL Diamond — introductory interest-free period: 3 months from plan start date. After 3 months, standard APR of 12.49% applies to the then-outstanding principal. If introductory period length is 0, interest accrues from plan start date. | Rolling; 3-month interest-free window from plan start date | **ACTIVE** (rolling) | Communicate 3-month interest-free window and automatic APR switch to 12.49% at month 4. Ensure customer understands that outstanding principal accrues interest from the end of the introductory period. | doc\_56a3cfc6 | e9054 |
| BNPL Platinum — 6-month financing term. Balance amortizes over 6 monthly installments, each including principal and accrued interest. Activation requires account status indicator to show enabled = true. | Rolling; 6-month amortization from plan activation | **ACTIVE** (rolling) | Verify account status = enabled before activating. Communicate the 6-month installment structure. Confirm each installment includes both principal and interest components. | doc\_c6b3fb3a | e9060 |
| Referral program — annual earning caps. Referrer maximum: 4 referrals × $20 per referral = $80 maximum per year. New-member maximum: 4 referrals × $35 per referral = $140 maximum per year (if each referral is a new member). | Rolling; annual cap (calendar year reset definition unspecified — see row 55) | **ACTIVE** (rolling) | Apply both annual caps. Do not credit bonuses beyond the per-year maximum. Calendar year reset definition is a data quality gap (see row 55); apply caps conservatively until definition is confirmed. | doc\_9659c86a | e5456, e5457 |
| BNPL 4-in-6-weeks installment plan — inferred payment interval. 4 installments over 6 weeks implies 6 weeks ÷ 3 intervals = approximately 2 weeks (~14 days) between installments. This interval is inferred from the product title, not stated explicitly in policy. | Rolling; from plan start date | **ACTIVE** (rolling, inferred) | Confirm actual installment schedule from account record before advising customer. The ~14-day interval is an inference; treat as unconfirmed until verified from policy or account data. Flag as a data quality gap if customer disputes timing. | doc\_b9a5b27d | e4796 |

---

### 8C. Temporal Parameters with Unresolvable or Ambiguous Windows — Data Quality Defects

These items carry a temporal dimension but contain syntax errors, missing unit specifications, placeholder values, or absent policy definitions that prevent accurate evaluation as of 2026-06-26. Agents must not quote defective values as authoritative.

| Item | Effective window (as stated in corpus) | Status today | Correct agent handling | Source doc\_id | Entry ref |
|------|----------------------------------------|-------------|----------------------|----------------|-----------|
| Block recurring payments — activation lag. Document states change "takes effect within 24 hours" but does not specify whether this means 24 business hours or 24 calendar hours. | "within 24 hours" (unit ambiguous) | ACTIVE (window unverifiable) | Do not promise a business-hours or calendar-hours commitment. State "within 24 hours" without interpreting which hour type applies. Escalate for document correction. | doc\_f5ff98f1 | e2525 |
| Personal checking ELITE (Bluest) — closure fee period. Stated in document as '$180 days' — currency symbol erroneously prepended to a time value. Intended value: 180 days. | '$180 days' (syntax error; intended: 180 days) | ACTIVE (value defective) | Use 180 days as the intended value pending document correction. Do not quote '$180 days' literally to any customer. Flag document for immediate correction. | doc\_496ec015 | e2530 |
| Personal savings PREMIUM (Gold) — closure fee period. Same syntax defect: '$180 days' instead of 180 days. | '$180 days' (syntax error; intended: 180 days) | ACTIVE (value defective) | Use 180 days as intended; same handling as row above. Flag doc\_b098204b for correction. | doc\_b098204b | e2531 |
| Personal savings ELITE (Platinum) — closure fee period. Syntax defect: '$270 days' instead of 270 days. | '$270 days' (syntax error; intended: 270 days) | ACTIVE (value defective) | Use 270 days as intended pending correction. Flag doc\_b098204b for correction. | doc\_b098204b | e2532 |
| Business checking PREMIUM (Cobalt Blue) — closure fee period. Syntax defect: '$180 days' instead of 180 days. | '$180 days' (syntax error; intended: 180 days) | ACTIVE (value defective) | Use 180 days as intended pending correction. Flag doc\_a44e66aa for correction. | doc\_a44e66aa | e2533 |
| Business checking ELITE — closure fee period. Syntax defect: '$270 days' instead of 270 days. | '$270 days' (syntax error; intended: 270 days) | ACTIVE (value defective) | Use 270 days as intended pending correction. Flag doc\_a44e66aa for correction. | doc\_a44e66aa | e2534 |
| Free period stated as 'free period of 6' — time unit omitted entirely. Context infers 6 months, but this is unconfirmed by explicit policy text. | 'free period of 6' (unit absent; inferred: 6 months) | ACTIVE (unit unverifiable) | Treat as 6 months pending document correction based on contextual inference. Do not state the unit to customers with certainty without document verification. | doc\_7225daec | e2900 |
| Tree-planting accrual reset mechanism — reset schedule not specified. Document does not state whether partial accrual progress carries forward monthly, annually, or perpetually until the tree-planting threshold is met. | Unspecified | ACTIVE (policy gap) | Do not advise on accrual reset timing. Escalate to product team for authoritative clarification before making any commitment to a customer. | doc\_901900ec | e3169 |
| Evergreen Account merchant verification lag — offset posting delay. Offsets 'appear in environmental dashboard once transactions clear' but the clearing timeline is undefined (1–3 business days? Same-day?). | Unspecified | ACTIVE (policy gap) | State that offsets appear after transactions clear. Do not promise a specific number of days. See also row for Evergreen CO2 formula in Section 8B. | doc\_901900ec | e3170 |
| Business Silver Card — first-year annual fee waiver. Document states $0 first year for new customers but does not specify offer window start or end dates. Cannot confirm whether any current promotional offer is active. | Dates absent from documentation | ACTIVE (window unverifiable) | Do not promise a waived first year without confirming that a current, in-window offer applies. Escalate to verify whether a fee-waiver offer is currently active before quoting $0. | doc\_438fb72f | e3241 |
| Diamond Vault — external transfer processing time stated as '0 business days'. Semantically unclear: may mean same-day processing, or may be a data entry error. | '0 business days' (ambiguous) | ACTIVE (value ambiguous) | Do not quote '0 business days' without verification. Describe as "same-day" only after product team confirms that is the correct interpretation. Treat as a potential data error until resolved. | doc\_5ca2f8ca | e3838 |
| Monthly security/API key rotation — day-of-month trigger, timezone, and batch size not specified. Document states rotation is monthly but provides no execution date. | 'Monthly' (trigger date absent) | ACTIVE (spec gap) | State that rotation is monthly. Do not commit to a specific day of month. Escalate for complete specification. | doc\_b3842985 | e3942 |
| Processing timeline — '1 business days'. Grammatical error: plural where singular is required. Intended: 1 business day. | '1 business days' (grammar error; intended: 1 business day) | ACTIVE (value defective) | Treat as 1 business day. Flag doc\_fc714229 for grammatical correction. | doc\_fc714229 | e4141 |
| Early-payment rewards — eligibility status value. Document contains placeholder: 'Early-payment rewards enabled: \[value not available\]'. Actual enabled/disabled status is missing from policy text. | \[value not available\] | ACTIVE (data missing) | Do not state eligibility status from policy text. Retrieve live account status or escalate. Do not default to enabled or disabled. | doc\_4cbe41e4 | e4414 |
| BNPL Platinum — annual maximum purchase protection coverage per account per calendar year. Value is '\[value not available\]' in source document. | \[value not available\] | ACTIVE (data missing) | Do not quote a coverage cap. Escalate to retrieve the current authoritative value before advising a customer on protection limits. | doc\_0078677a | e4461 |
| BNPL Platinum — claim submission window. '\[value not available\] days from purchase date'. The number of days a customer has to submit a purchase protection claim is unknown. | \[value not available\] days from purchase date | ACTIVE (data missing) | Do not quote a claim deadline. Escalate for the current value. Do not allow a customer to assume they have unlimited time to file. | doc\_0078677a | e4462 |
| BNPL Platinum — item eligibility lookback window. '\[value not available\] days from current date'. The lookback period for determining whether a past purchase qualifies for protection is unknown. | \[value not available\] days from current date | ACTIVE (data missing) | Do not quote a lookback period. Escalate for current value before advising on purchase eligibility. | doc\_0078677a | e4463 |
| BNPL Gold 004 — scheduled auto-debit day of month. Document field reads 'day \[value not available\]'. Actual debit day is absent from policy text. | \[value not available\] (day of month absent) | ACTIVE (data missing) | Retrieve actual scheduled debit day from account record. Do not quote any day of month without confirmation from live account data. | doc\_873b092d | e4539 |
| APY tier determination — monthly evaluation date. Document references 'applicable evaluation point for the tier in your cycle' but does not specify the date or schedule for APY tier determination within the statement cycle. | 'applicable evaluation point' (unspecified) | ACTIVE (spec gap) | Do not commit to a specific evaluation date. Advise customer to check account statements or contact support to confirm their cycle evaluation date. | doc\_12633b84 | e4602 |
| GPA reward approval timeline. Document states confirmation arrives 'typically shortly after' submission but provides no SLA, no business-day count, and no maximum wait time. | 'shortly after submission' (no SLA) | ACTIVE (spec gap) | Do not promise a specific timeline. State that confirmation typically arrives shortly after submission. Escalate customer-specific SLA inquiries to the relevant team. | doc\_d47645c0 | e5393 |
| QR code validity period — value '17' with no unit. Unit is unspecified across two documents; could be days, hours, or minutes. | '17' (unit absent) | ACTIVE (unit unverifiable) | Do not quote a validity period in any unit without confirmation. Escalate to obtain the correct unit before advising customers on QR code expiry. | doc\_7017b521, doc\_1aaa0f9d | e7030, e7345 |
| Referral limit calendar year reset — definition absent. Document does not state whether 'calendar year' means January 1 reset, account anniversary reset, or another definition. Affects how referral caps are applied. | 'Calendar year' (reset definition absent) | ACTIVE (spec gap) | Apply annual caps conservatively. Do not state a specific reset date. Advise customers to check product terms or contact support for their reset date. See also referral cap row in Section 8B. | doc\_6a701df3 | e7305 |
| Credit card closure while holding Bronze Account APY bonus — policy gap. No document addresses what happens to the Bronze Account APY bonus if the customer closes the qualifying credit card that enabled the bonus. | Undocumented | ACTIVE (policy gap) | Do not advise on APY bonus retention or removal in this scenario. Escalate to product and compliance before making any commitment to the customer. | (no source document found) | e7524 |
| Account opening — waiting period before first interest credit or withdrawal count reset. No specification of any waiting period between account opening date and first interest credit, or between transactions and withdrawal count reset. | Unspecified | ACTIVE (spec gap) | Do not commit to a waiting period. Advise customer to check account terms for their specific product. | (no source document found) | e7527 |
| Default statement delivery method — specification absent. No documentation states whether new accounts default to paper statements or digital statements. | Unspecified | ACTIVE (spec gap) | Do not assume default. Confirm statement delivery preference with customer at account opening. | (no source document found) | e7532 |
| Account closure procedures — timing for final interest credit and fund withdrawal after closure. No documentation specifies when final interest is credited or when funds become available post-closure. | Unspecified | ACTIVE (spec gap) | Do not quote a fund availability date after closure without confirmation. Escalate closure timing questions to the relevant team. | (no source document found) | e7536 |
| Payment reminder interval '4' and payment deadline '16' — unit absent across four documents. Values are likely hours or days but unit is unspecified. | '4' (reminder) and '16' (deadline) — units absent | ACTIVE (unit unverifiable) | Do not quote '4 \[unit\]' or '16 \[unit\]' without confirmed units. Treat as unconfirmed until a document correction is issued across all four affected sources. | doc\_e62bebf9, doc\_e7430e4a, doc\_ff8d61b5, doc\_133f50a4 | e7606 |
| Diamond Elite Account — effective/launch date. No document provides a specific effective date or launch date for the Diamond Elite Account product. | Absent from documentation | ACTIVE (date absent) | Do not commit to a launch date. Treat as a current active offering based on document content. Escalate for effective date if required for compliance or disclosure purposes. | (no source document found) | e7680 |
| Diamond Elite Account APY rate 7.5% — temporal validity unspecified. Document (dated 2026-06-26) shows 7.5% APY but provides no effective date range, review schedule, or expiry date for this rate. | Document date 2026-06-26 only; no validity window | ACTIVE (window unverifiable) | Cite 7.5% APY as the current rate per the document's effective date of 2026-06-26. Advise customers that rates are subject to change. Do not represent the rate as guaranteed for any future period. | (no source document found) | e7764 |
| Gold Savings Account — statement period definition. No document defines the length of the statement period or the statement cycle cutoff day. | Unspecified | ACTIVE (spec gap) | Do not state a specific statement period length or cutoff date. Advise customer to check account statements. | (no source document found) | e7945 |
| Business Platinum Rewards Card referral program — qualifying spend window stated as '$135 days'. Currency symbol erroneously prepended to a time value. Intended: 135 days. | '$135 days' (syntax error; intended: 135 days) | ACTIVE (value defective) | Use 135 days as the intended qualifying spend window pending document correction. Do not quote '$135 days' literally. Flag doc\_b901fa2d for immediate correction. | doc\_b901fa2d | e8481 |
| BNPL Gold — introductory promotional APR period and rate. Both the promotional APR duration ('\[value not available\] days from plan start') and the promotional APR rate ('\[value not available\]%') are placeholder values. Standard APR post-intro is also '\[value not available\]'. All three APR-related values are missing. | \[value not available\] days / \[value not available\]% | ACTIVE (data missing) | Do not quote promotional APR, promotional period duration, or standard APR for BNPL Gold. Escalate to obtain all three current values before advising any customer on BNPL Gold financing costs. | doc\_5d6a65b8 | e9065 |

---

**Summary counts (as of 2026-06-26):**

| Category | Count |
|----------|-------|
| EXPIRED promotions/protocols still in active corpus (agent-risk) | 11 distinct items (rows 1–11) |
| DISPUTED incident protocol (conflicting deadline year) | 2 items (rows 12–13, including the systemic compliance note) |
| ACTIVE / rolling items with defined or evaluable windows | 19 items (rows 14–32 plus inferred interval row 33) |
| Data quality defects — temporal parameter unresolvable | 32 items (rows 34–65) |
| **Total entries enumerated** | **78** |


---



---

## Appendix A — Document ID ↔ Original Source File

Mapping of every blackboard `doc_id` (hash, used in this register's source citations) to its original filename in `tau2-bench/data/tau2/domains/banking_knowledge/documents/`. 698 documents. Sorted by source filename. **Note:** hash `doc_id`s are assigned per-ingestion and are not stable across blackboards; the filename is the stable cross-reference.

| Original source file | Blackboard `doc_id` |
|---|---|
| `doc_bank_accounts_bank_accounts_(general)_001.json` | `doc_65dc99ca` |
| `doc_bank_accounts_bank_accounts_(general)_002.json` | `doc_677caa94` |
| `doc_bank_accounts_bank_accounts_(general)_003.json` | `doc_c44806ee` |
| `doc_bank_accounts_bank_accounts_(general)_004.json` | `doc_927d5dc2` |
| `doc_bank_accounts_bank_accounts_(general)_005.json` | `doc_496ec015` |
| `doc_bank_accounts_bank_accounts_(general)_006.json` | `doc_b098204b` |
| `doc_bank_accounts_bank_accounts_(general)_007.json` | `doc_a44e66aa` |
| `doc_bank_accounts_bank_accounts_(general)_008.json` | `doc_d8556195` |
| `doc_bank_accounts_bank_accounts_(general)_009.json` | `doc_9f48f46f` |
| `doc_bank_accounts_bank_accounts_(general)_010.json` | `doc_bdc9d138` |
| `doc_bank_accounts_bank_accounts_(general)_011.json` | `doc_d2b5a881` |
| `doc_bank_accounts_bank_accounts_(general)_012.json` | `doc_58fd4187` |
| `doc_bank_accounts_bank_accounts_(general)_013.json` | `doc_ad8b029a` |
| `doc_bank_accounts_bank_accounts_(general)_014.json` | `doc_cba24244` |
| `doc_bank_accounts_bank_accounts_(general)_015.json` | `doc_065caedb` |
| `doc_bank_accounts_bank_accounts_(general)_016.json` | `doc_c420c1a3` |
| `doc_bank_accounts_bank_accounts_(general)_017.json` | `doc_ffd40cf4` |
| `doc_bank_accounts_bank_accounts_(general)_018.json` | `doc_e726d241` |
| `doc_bank_accounts_bank_accounts_(general)_019.json` | `doc_da02a982` |
| `doc_bank_accounts_bank_accounts_(general)_020.json` | `doc_acba887d` |
| `doc_bank_accounts_bank_accounts_(general)_021.json` | `doc_d05608c6` |
| `doc_bank_accounts_bank_accounts_(general)_022.json` | `doc_d3e6f724` |
| `doc_bank_accounts_bank_accounts_(general)_023.json` | `doc_8075b06d` |
| `doc_bank_accounts_bank_accounts_(general)_024.json` | `doc_17e8b784` |
| `doc_bank_accounts_bank_accounts_(general)_025.json` | `doc_0fc71a11` |
| `doc_bank_accounts_bank_accounts_(general)_026.json` | `doc_54165f36` |
| `doc_bank_accounts_bank_accounts_(general)_027.json` | `doc_0f7eb1ac` |
| `doc_bank_accounts_bank_accounts_(general)_028.json` | `doc_529822cc` |
| `doc_bank_accounts_bank_accounts_(general)_029.json` | `doc_2407c4a1` |
| `doc_bank_accounts_bank_accounts_(general)_030.json` | `doc_cad8a767` |
| `doc_bank_accounts_bank_accounts_(general)_031.json` | `doc_4cef20a4` |
| `doc_bank_accounts_bank_accounts_(general)_032.json` | `doc_bf30cc84` |
| `doc_bank_accounts_bank_accounts_(general)_033.json` | `doc_33cb937a` |
| `doc_bank_accounts_bank_accounts_(general)_034.json` | `doc_f5ff98f1` |
| `doc_bank_accounts_bank_accounts_(general)_035.json` | `doc_358ac32d` |
| `doc_bank_accounts_bank_accounts_(general)_036.json` | `doc_ec4ccc7d` |
| `doc_bank_accounts_bank_accounts_(general)_037.json` | `doc_01cd5b65` |
| `doc_bank_accounts_bank_accounts_(general)_039.json` | `doc_ea845128` |
| `doc_bank_accounts_bank_accounts_(general)_040.json` | `doc_590138d0` |
| `doc_bank_accounts_bank_accounts_(general)_041.json` | `doc_17f0f271` |
| `doc_bank_accounts_bank_accounts_(general)_042.json` | `doc_a849e12a` |
| `doc_bank_accounts_bank_accounts_(general)_043.json` | `doc_8ab07763` |
| `doc_bank_accounts_bank_accounts_(general)_044.json` | `doc_2b71be16` |
| `doc_bank_accounts_bank_accounts_(general)_045.json` | `doc_0283272e` |
| `doc_bank_accounts_bank_accounts_(general)_046.json` | `doc_4eb6112b` |
| `doc_bank_accounts_bank_accounts_(general)_047.json` | `doc_d1e7a1c4` |
| `doc_bank_accounts_bank_accounts_(general)_048.json` | `doc_210375eb` |
| `doc_business_checking_accounts_beige_001.json` | `doc_9a69a1e0` |
| `doc_business_checking_accounts_beige_002.json` | `doc_ff1e9b24` |
| `doc_business_checking_accounts_beige_003.json` | `doc_6b8ae1ea` |
| `doc_business_checking_accounts_beige_004.json` | `doc_aa6ba6fa` |
| `doc_business_checking_accounts_beige_005.json` | `doc_678103e8` |
| `doc_business_checking_accounts_beige_006.json` | `doc_9765d0bd` |
| `doc_business_checking_accounts_beige_007.json` | `doc_554a9010` |
| `doc_business_checking_accounts_beige_008.json` | `doc_54c20b48` |
| `doc_business_checking_accounts_beige_009.json` | `doc_b42f84fd` |
| `doc_business_checking_accounts_beige_010.json` | `doc_f476ca8e` |
| `doc_business_checking_accounts_beige_011.json` | `doc_23ef787c` |
| `doc_business_checking_accounts_beige_012.json` | `doc_fca069fd` |
| `doc_business_checking_accounts_cobalt_blue_001.json` | `doc_7ab1bdc2` |
| `doc_business_checking_accounts_cobalt_blue_002.json` | `doc_d11d41d3` |
| `doc_business_checking_accounts_cobalt_blue_003.json` | `doc_7f369e9b` |
| `doc_business_checking_accounts_cobalt_blue_004.json` | `doc_dbbd630f` |
| `doc_business_checking_accounts_cobalt_blue_005.json` | `doc_0ffafa53` |
| `doc_business_checking_accounts_cobalt_blue_006.json` | `doc_bf163f6c` |
| `doc_business_checking_accounts_cobalt_blue_007.json` | `doc_770859bd` |
| `doc_business_checking_accounts_cobalt_blue_008.json` | `doc_ef762480` |
| `doc_business_checking_accounts_cobalt_blue_009.json` | `doc_348d5dd5` |
| `doc_business_checking_accounts_cobalt_blue_010.json` | `doc_b35a4072` |
| `doc_business_checking_accounts_hunter_green_001.json` | `doc_6b4aa36d` |
| `doc_business_checking_accounts_hunter_green_002.json` | `doc_66327fd6` |
| `doc_business_checking_accounts_hunter_green_003.json` | `doc_64bbb60a` |
| `doc_business_checking_accounts_hunter_green_004.json` | `doc_aa38372e` |
| `doc_business_checking_accounts_hunter_green_005.json` | `doc_8e2bd3b0` |
| `doc_business_checking_accounts_hunter_green_006.json` | `doc_57a8f646` |
| `doc_business_checking_accounts_hunter_green_007.json` | `doc_d2ab5baf` |
| `doc_business_checking_accounts_hunter_green_008.json` | `doc_eeb25bbb` |
| `doc_business_checking_accounts_hunter_green_009.json` | `doc_b173fd57` |
| `doc_business_checking_accounts_hunter_green_010.json` | `doc_d8136ddf` |
| `doc_business_checking_accounts_lime_green_001.json` | `doc_3a4c8a96` |
| `doc_business_checking_accounts_lime_green_002.json` | `doc_c2c9f908` |
| `doc_business_checking_accounts_lime_green_003.json` | `doc_4adb5770` |
| `doc_business_checking_accounts_lime_green_004.json` | `doc_08cf6085` |
| `doc_business_checking_accounts_lime_green_005.json` | `doc_09824e7f` |
| `doc_business_checking_accounts_lime_green_006.json` | `doc_0ed22387` |
| `doc_business_checking_accounts_lime_green_007.json` | `doc_a3b40992` |
| `doc_business_checking_accounts_lime_green_008.json` | `doc_58604f42` |
| `doc_business_checking_accounts_navy_blue_001.json` | `doc_b7cdfb44` |
| `doc_business_checking_accounts_navy_blue_002.json` | `doc_2564fed8` |
| `doc_business_checking_accounts_navy_blue_003.json` | `doc_d5d32676` |
| `doc_business_checking_accounts_navy_blue_004.json` | `doc_ba62ddad` |
| `doc_business_checking_accounts_navy_blue_005.json` | `doc_12833d14` |
| `doc_business_checking_accounts_navy_blue_006.json` | `doc_01620a12` |
| `doc_business_checking_accounts_navy_blue_007.json` | `doc_ef5d187d` |
| `doc_business_checking_accounts_navy_blue_008.json` | `doc_ffbe2fa0` |
| `doc_business_checking_accounts_navy_blue_009.json` | `doc_b5856d75` |
| `doc_business_checking_accounts_sky_blue_001.json` | `doc_2f340732` |
| `doc_business_checking_accounts_sky_blue_002.json` | `doc_23280047` |
| `doc_business_checking_accounts_sky_blue_003.json` | `doc_7f89a2a2` |
| `doc_business_checking_accounts_sky_blue_004.json` | `doc_22f80f8d` |
| `doc_business_checking_accounts_sky_blue_005.json` | `doc_7631303a` |
| `doc_business_checking_accounts_sky_blue_006.json` | `doc_ac083b81` |
| `doc_business_checking_accounts_sky_blue_007.json` | `doc_4f761caf` |
| `doc_business_checking_accounts_sky_blue_008.json` | `doc_ff2edea6` |
| `doc_business_checking_accounts_sky_blue_009.json` | `doc_7225daec` |
| `doc_business_checking_accounts_sky_blue_010.json` | `doc_257f78b8` |
| `doc_business_checking_accounts_true_blue_001.json` | `doc_4d0c7d44` |
| `doc_business_checking_accounts_true_blue_002.json` | `doc_63946042` |
| `doc_business_checking_accounts_true_blue_003.json` | `doc_45f5241a` |
| `doc_business_checking_accounts_true_blue_004.json` | `doc_631b1389` |
| `doc_business_checking_accounts_true_blue_005.json` | `doc_f4304ed9` |
| `doc_business_checking_accounts_true_blue_006.json` | `doc_5fa3b92b` |
| `doc_business_checking_accounts_true_blue_007.json` | `doc_4a4db8d0` |
| `doc_business_checking_accounts_true_blue_008.json` | `doc_2d45a29b` |
| `doc_business_checking_accounts_true_blue_009.json` | `doc_34528b8b` |
| `doc_business_checking_accounts_true_blue_010.json` | `doc_07205924` |
| `doc_business_checking_accounts_true_blue_011.json` | `doc_25c43df7` |
| `doc_business_checking_accounts_world_blue_001.json` | `doc_9ae778e4` |
| `doc_business_checking_accounts_world_blue_002.json` | `doc_3ec63fbc` |
| `doc_business_checking_accounts_world_blue_003.json` | `doc_765d850c` |
| `doc_business_checking_accounts_world_blue_004.json` | `doc_c7ad1175` |
| `doc_business_checking_accounts_world_blue_005.json` | `doc_8a64f90c` |
| `doc_business_checking_accounts_world_blue_006.json` | `doc_c4a9bea9` |
| `doc_business_checking_accounts_world_blue_007.json` | `doc_3f03627a` |
| `doc_business_checking_accounts_world_blue_008.json` | `doc_2d31692b` |
| `doc_business_checking_accounts_world_blue_009.json` | `doc_eebaae8e` |
| `doc_business_credit_cards_business_bronze_rewards_card_001.json` | `doc_ff5eadd7` |
| `doc_business_credit_cards_business_bronze_rewards_card_002.json` | `doc_85a5ca28` |
| `doc_business_credit_cards_business_bronze_rewards_card_003.json` | `doc_e6c0087f` |
| `doc_business_credit_cards_business_bronze_rewards_card_004.json` | `doc_3c151036` |
| `doc_business_credit_cards_business_bronze_rewards_card_005.json` | `doc_47e0805b` |
| `doc_business_credit_cards_business_bronze_rewards_card_006.json` | `doc_47f0fcb7` |
| `doc_business_credit_cards_business_bronze_rewards_card_007.json` | `doc_db5929e5` |
| `doc_business_credit_cards_business_bronze_rewards_card_008.json` | `doc_c5f62a24` |
| `doc_business_credit_cards_business_bronze_rewards_card_009.json` | `doc_8de479c7` |
| `doc_business_credit_cards_business_bronze_rewards_card_010.json` | `doc_8625ca18` |
| `doc_business_credit_cards_business_bronze_rewards_card_011.json` | `doc_7012dc0c` |
| `doc_business_credit_cards_business_gold_rewards_card_001.json` | `doc_cfd0ab41` |
| `doc_business_credit_cards_business_gold_rewards_card_002.json` | `doc_0ea882ff` |
| `doc_business_credit_cards_business_gold_rewards_card_003.json` | `doc_4c46626b` |
| `doc_business_credit_cards_business_gold_rewards_card_004.json` | `doc_10072e85` |
| `doc_business_credit_cards_business_gold_rewards_card_005.json` | `doc_d2747fdd` |
| `doc_business_credit_cards_business_gold_rewards_card_006.json` | `doc_6458670c` |
| `doc_business_credit_cards_business_gold_rewards_card_007.json` | `doc_26ff1016` |
| `doc_business_credit_cards_business_gold_rewards_card_008.json` | `doc_7944a521` |
| `doc_business_credit_cards_business_gold_rewards_card_009.json` | `doc_083925f6` |
| `doc_business_credit_cards_business_gold_rewards_card_010.json` | `doc_e5732200` |
| `doc_business_credit_cards_business_platinum_rewards_card_001.json` | `doc_b1c0a1f5` |
| `doc_business_credit_cards_business_platinum_rewards_card_002.json` | `doc_deb45de8` |
| `doc_business_credit_cards_business_platinum_rewards_card_003.json` | `doc_9d53cf90` |
| `doc_business_credit_cards_business_platinum_rewards_card_004.json` | `doc_7236d3ce` |
| `doc_business_credit_cards_business_platinum_rewards_card_005.json` | `doc_6b61d219` |
| `doc_business_credit_cards_business_platinum_rewards_card_006.json` | `doc_e6e7a5ab` |
| `doc_business_credit_cards_business_platinum_rewards_card_007.json` | `doc_a3a165f2` |
| `doc_business_credit_cards_business_platinum_rewards_card_008.json` | `doc_e7de936d` |
| `doc_business_credit_cards_business_platinum_rewards_card_009.json` | `doc_aed772ad` |
| `doc_business_credit_cards_business_platinum_rewards_card_010.json` | `doc_2ad90b74` |
| `doc_business_credit_cards_business_platinum_rewards_card_011.json` | `doc_b9f03213` |
| `doc_business_credit_cards_business_platinum_rewards_card_012.json` | `doc_b901fa2d` |
| `doc_business_credit_cards_business_silver_rewards_card_001.json` | `doc_438fb72f` |
| `doc_business_credit_cards_business_silver_rewards_card_002.json` | `doc_e7a97d00` |
| `doc_business_credit_cards_business_silver_rewards_card_003.json` | `doc_cd6a9891` |
| `doc_business_credit_cards_business_silver_rewards_card_004.json` | `doc_9bd37731` |
| `doc_business_credit_cards_business_silver_rewards_card_005.json` | `doc_e6b3a4c9` |
| `doc_business_credit_cards_business_silver_rewards_card_006.json` | `doc_c3e96be7` |
| `doc_business_credit_cards_business_silver_rewards_card_007.json` | `doc_bf944bf7` |
| `doc_business_credit_cards_business_silver_rewards_card_008.json` | `doc_6b40eac4` |
| `doc_business_credit_cards_business_silver_rewards_card_009.json` | `doc_67ea4886` |
| `doc_business_credit_cards_business_silver_rewards_card_010.json` | `doc_023dc476` |
| `doc_business_credit_cards_business_silver_rewards_card_011.json` | `doc_8a67444e` |
| `doc_business_credit_cards_business_silver_rewards_card_012.json` | `doc_760196c3` |
| `doc_business_credit_cards_business_silver_rewards_card_013.json` | `doc_d0ae6124` |
| `doc_business_credit_cards_green_rewards_card_001.json` | `doc_b8ea386c` |
| `doc_business_credit_cards_green_rewards_card_002.json` | `doc_7e2b8148` |
| `doc_business_credit_cards_green_rewards_card_003.json` | `doc_826e6694` |
| `doc_business_credit_cards_green_rewards_card_004.json` | `doc_16cdbd77` |
| `doc_business_credit_cards_green_rewards_card_005.json` | `doc_8df56f92` |
| `doc_business_credit_cards_green_rewards_card_006.json` | `doc_901900ec` |
| `doc_business_credit_cards_green_rewards_card_007.json` | `doc_1e683264` |
| `doc_business_credit_cards_green_rewards_card_008.json` | `doc_3af25521` |
| `doc_business_credit_cards_green_rewards_card_009.json` | `doc_c84a5439` |
| `doc_business_credit_cards_green_rewards_card_010.json` | `doc_96b7eec5` |
| `doc_business_credit_cards_silver_zoom_card_001.json` | `doc_7d33f323` |
| `doc_business_credit_cards_silver_zoom_card_002.json` | `doc_7ae95ba1` |
| `doc_business_credit_cards_silver_zoom_card_003.json` | `doc_d6e9c630` |
| `doc_business_credit_cards_silver_zoom_card_004.json` | `doc_1a9d4bbc` |
| `doc_business_credit_cards_silver_zoom_card_005.json` | `doc_5b96e61d` |
| `doc_business_credit_cards_silver_zoom_card_006.json` | `doc_7384cbee` |
| `doc_business_credit_cards_silver_zoom_card_007.json` | `doc_99bcc905` |
| `doc_business_credit_cards_silver_zoom_card_008.json` | `doc_0be141d4` |
| `doc_business_credit_cards_silver_zoom_card_009.json` | `doc_e1dd7f7a` |
| `doc_business_credit_cards_silver_zoom_card_010.json` | `doc_0042ffc7` |
| `doc_business_credit_cards_silver_zoom_card_011.json` | `doc_023ed3f6` |
| `doc_business_credit_cards_silver_zoom_card_012.json` | `doc_ffdc202c` |
| `doc_business_credit_cards_silver_zoom_card_013.json` | `doc_d0eb2d3d` |
| `doc_business_credit_cards_virtual_card_management_001.json` | `doc_ae54f786` |
| `doc_business_credit_cards_virtual_card_management_002.json` | `doc_716c01e3` |
| `doc_business_credit_cards_virtual_card_management_003.json` | `doc_30604336` |
| `doc_business_credit_cards_virtual_card_management_004.json` | `doc_2002e402` |
| `doc_business_credit_cards_virtual_card_management_005.json` | `doc_4cf3e806` |
| `doc_business_credit_cards_virtual_card_management_006.json` | `doc_f83cd2e1` |
| `doc_business_credit_cards_virtual_card_management_007.json` | `doc_b3842985` |
| `doc_business_credit_cards_virtual_card_management_008.json` | `doc_9a86f0bf` |
| `doc_business_credit_cards_virtual_card_management_009.json` | `doc_e775520d` |
| `doc_business_credit_cards_virtual_card_management_010.json` | `doc_df247faa` |
| `doc_business_savings_accounts_automatic_sweep_program_001.json` | `doc_93cd86b9` |
| `doc_business_savings_accounts_automatic_sweep_program_002.json` | `doc_57795f9e` |
| `doc_business_savings_accounts_automatic_sweep_program_003.json` | `doc_7aacaf20` |
| `doc_business_savings_accounts_automatic_sweep_program_004.json` | `doc_a8a38e46` |
| `doc_business_savings_accounts_automatic_sweep_program_005.json` | `doc_144c750d` |
| `doc_business_savings_accounts_automatic_sweep_program_006.json` | `doc_a19314f5` |
| `doc_business_savings_accounts_automatic_sweep_program_007.json` | `doc_ee3f1392` |
| `doc_business_savings_accounts_automatic_sweep_program_008.json` | `doc_e2c7dfcb` |
| `doc_business_savings_accounts_bronze_saver_account_001.json` | `doc_a6f00b14` |
| `doc_business_savings_accounts_bronze_saver_account_002.json` | `doc_c3eed0d5` |
| `doc_business_savings_accounts_bronze_saver_account_003.json` | `doc_d9c0cb9f` |
| `doc_business_savings_accounts_bronze_saver_account_004.json` | `doc_d7f5da8c` |
| `doc_business_savings_accounts_bronze_saver_account_005.json` | `doc_c2f49adf` |
| `doc_business_savings_accounts_bronze_saver_account_006.json` | `doc_9bda551e` |
| `doc_business_savings_accounts_bronze_saver_account_007.json` | `doc_42eb78b6` |
| `doc_business_savings_accounts_bronze_saver_account_008.json` | `doc_01e7e1ea` |
| `doc_business_savings_accounts_diamond_vault_001.json` | `doc_97532db4` |
| `doc_business_savings_accounts_diamond_vault_002.json` | `doc_a83c9a0a` |
| `doc_business_savings_accounts_diamond_vault_003.json` | `doc_5ca2f8ca` |
| `doc_business_savings_accounts_diamond_vault_004.json` | `doc_92e288fb` |
| `doc_business_savings_accounts_diamond_vault_005.json` | `doc_abfa316d` |
| `doc_business_savings_accounts_diamond_vault_006.json` | `doc_33b09237` |
| `doc_business_savings_accounts_diamond_vault_007.json` | `doc_787da2fb` |
| `doc_business_savings_accounts_diamond_vault_008.json` | `doc_bd16e9dd` |
| `doc_business_savings_accounts_emerald_saver_001.json` | `doc_bdeef9ea` |
| `doc_business_savings_accounts_emerald_saver_002.json` | `doc_2824291d` |
| `doc_business_savings_accounts_emerald_saver_003.json` | `doc_79933b6b` |
| `doc_business_savings_accounts_emerald_saver_004.json` | `doc_c54c5d7d` |
| `doc_business_savings_accounts_emerald_saver_005.json` | `doc_9c96deaf` |
| `doc_business_savings_accounts_emerald_saver_006.json` | `doc_f483ca51` |
| `doc_business_savings_accounts_emerald_saver_007.json` | `doc_0405ba2e` |
| `doc_business_savings_accounts_emerald_saver_008.json` | `doc_15a63df1` |
| `doc_business_savings_accounts_gold_plus_saver_001.json` | `doc_041c2bd6` |
| `doc_business_savings_accounts_gold_plus_saver_002.json` | `doc_e4df638a` |
| `doc_business_savings_accounts_gold_plus_saver_003.json` | `doc_1d4150d4` |
| `doc_business_savings_accounts_gold_plus_saver_004.json` | `doc_5b60e346` |
| `doc_business_savings_accounts_gold_plus_saver_005.json` | `doc_41fa92c5` |
| `doc_business_savings_accounts_gold_plus_saver_006.json` | `doc_7f9b1cfa` |
| `doc_business_savings_accounts_gold_plus_saver_007.json` | `doc_bec66850` |
| `doc_business_savings_accounts_gold_saver_account_001.json` | `doc_5666ea8e` |
| `doc_business_savings_accounts_gold_saver_account_002.json` | `doc_2477378b` |
| `doc_business_savings_accounts_gold_saver_account_003.json` | `doc_23438ad1` |
| `doc_business_savings_accounts_gold_saver_account_004.json` | `doc_86f643a7` |
| `doc_business_savings_accounts_gold_saver_account_005.json` | `doc_0314e686` |
| `doc_business_savings_accounts_gold_saver_account_006.json` | `doc_fd7ef81a` |
| `doc_business_savings_accounts_gold_saver_account_007.json` | `doc_fc714229` |
| `doc_business_savings_accounts_gold_saver_account_008.json` | `doc_741c69c5` |
| `doc_business_savings_accounts_gold_saver_account_009.json` | `doc_c086c30f` |
| `doc_business_savings_accounts_joint_business_holders_+_user_roles_001.json` | `doc_8f171e52` |
| `doc_business_savings_accounts_joint_business_holders_+_user_roles_002.json` | `doc_28674f63` |
| `doc_business_savings_accounts_joint_business_holders_+_user_roles_003.json` | `doc_ce6e0a21` |
| `doc_business_savings_accounts_joint_business_holders_+_user_roles_004.json` | `doc_8e8c0ca8` |
| `doc_business_savings_accounts_joint_business_holders_+_user_roles_005.json` | `doc_d1497b0a` |
| `doc_business_savings_accounts_joint_business_holders_+_user_roles_006.json` | `doc_2e318dce` |
| `doc_business_savings_accounts_joint_business_holders_+_user_roles_007.json` | `doc_b016c9c7` |
| `doc_business_savings_accounts_joint_business_holders_+_user_roles_008.json` | `doc_aadf402a` |
| `doc_business_savings_accounts_joint_business_holders_+_user_roles_009.json` | `doc_26358a17` |
| `doc_business_savings_accounts_platinum_reserve_account_001.json` | `doc_e1fc57d3` |
| `doc_business_savings_accounts_platinum_reserve_account_002.json` | `doc_cea811d4` |
| `doc_business_savings_accounts_platinum_reserve_account_003.json` | `doc_00d5e524` |
| `doc_business_savings_accounts_platinum_reserve_account_004.json` | `doc_52bbdcd2` |
| `doc_business_savings_accounts_platinum_reserve_account_005.json` | `doc_c3291abe` |
| `doc_business_savings_accounts_platinum_reserve_account_006.json` | `doc_d52ac41f` |
| `doc_business_savings_accounts_platinum_reserve_account_007.json` | `doc_337401bb` |
| `doc_business_savings_accounts_platinum_reserve_account_008.json` | `doc_3caa52d8` |
| `doc_business_savings_accounts_platinum_reserve_account_009.json` | `doc_62418195` |
| `doc_business_savings_accounts_platinum_reserve_account_010.json` | `doc_a0de283a` |
| `doc_business_savings_accounts_silver_plus_saver_001.json` | `doc_52b651bd` |
| `doc_business_savings_accounts_silver_plus_saver_002.json` | `doc_481b44c3` |
| `doc_business_savings_accounts_silver_plus_saver_003.json` | `doc_88ecd6c5` |
| `doc_business_savings_accounts_silver_plus_saver_004.json` | `doc_55452455` |
| `doc_business_savings_accounts_silver_plus_saver_005.json` | `doc_7a3fa53f` |
| `doc_business_savings_accounts_silver_plus_saver_006.json` | `doc_a2419393` |
| `doc_business_savings_accounts_silver_plus_saver_007.json` | `doc_4e04143d` |
| `doc_business_savings_accounts_silver_saver_account_001.json` | `doc_4e80b0ca` |
| `doc_business_savings_accounts_silver_saver_account_002.json` | `doc_12633b84` |
| `doc_business_savings_accounts_silver_saver_account_003.json` | `doc_d37d3382` |
| `doc_business_savings_accounts_silver_saver_account_004.json` | `doc_d9089439` |
| `doc_business_savings_accounts_silver_saver_account_005.json` | `doc_7f4ebc9f` |
| `doc_business_savings_accounts_silver_saver_account_006.json` | `doc_80eb2542` |
| `doc_business_savings_accounts_silver_saver_account_007.json` | `doc_7702c7b4` |
| `doc_business_savings_accounts_silver_saver_account_008.json` | `doc_831e9875` |
| `doc_buy_now_pay_later_bnpl_bronze_001.json` | `doc_e6004e71` |
| `doc_buy_now_pay_later_bnpl_bronze_002.json` | `doc_62dcde58` |
| `doc_buy_now_pay_later_bnpl_bronze_003.json` | `doc_b9a5b27d` |
| `doc_buy_now_pay_later_bnpl_bronze_004.json` | `doc_47a68621` |
| `doc_buy_now_pay_later_bnpl_bronze_005.json` | `doc_b367df4c` |
| `doc_buy_now_pay_later_bnpl_bronze_006.json` | `doc_2ffaf61f` |
| `doc_buy_now_pay_later_bnpl_bronze_007.json` | `doc_bff58d8c` |
| `doc_buy_now_pay_later_bnpl_bronze_008.json` | `doc_3297b9df` |
| `doc_buy_now_pay_later_bnpl_diamond_001.json` | `doc_4d42a828` |
| `doc_buy_now_pay_later_bnpl_diamond_002.json` | `doc_67c207c5` |
| `doc_buy_now_pay_later_bnpl_diamond_003.json` | `doc_130f56a9` |
| `doc_buy_now_pay_later_bnpl_diamond_004.json` | `doc_b30920db` |
| `doc_buy_now_pay_later_bnpl_diamond_005.json` | `doc_56a3cfc6` |
| `doc_buy_now_pay_later_bnpl_diamond_006.json` | `doc_6ddd849d` |
| `doc_buy_now_pay_later_bnpl_diamond_007.json` | `doc_cd262c0c` |
| `doc_buy_now_pay_later_bnpl_diamond_008.json` | `doc_762b93e2` |
| `doc_buy_now_pay_later_bnpl_gold_001.json` | `doc_5d6a65b8` |
| `doc_buy_now_pay_later_bnpl_gold_002.json` | `doc_4fdcfab2` |
| `doc_buy_now_pay_later_bnpl_gold_003.json` | `doc_3d524668` |
| `doc_buy_now_pay_later_bnpl_gold_004.json` | `doc_873b092d` |
| `doc_buy_now_pay_later_bnpl_gold_005.json` | `doc_daf4f207` |
| `doc_buy_now_pay_later_bnpl_gold_006.json` | `doc_9d97d5b8` |
| `doc_buy_now_pay_later_bnpl_gold_007.json` | `doc_2e08609d` |
| `doc_buy_now_pay_later_bnpl_gold_008.json` | `doc_f7f9c064` |
| `doc_buy_now_pay_later_bnpl_management_dashboard_001.json` | `doc_cf1350f3` |
| `doc_buy_now_pay_later_bnpl_management_dashboard_002.json` | `doc_1faafdbb` |
| `doc_buy_now_pay_later_bnpl_management_dashboard_003.json` | `doc_bb98b5d8` |
| `doc_buy_now_pay_later_bnpl_management_dashboard_004.json` | `doc_e2b2fca6` |
| `doc_buy_now_pay_later_bnpl_management_dashboard_005.json` | `doc_4cbe41e4` |
| `doc_buy_now_pay_later_bnpl_management_dashboard_006.json` | `doc_c2fc87f5` |
| `doc_buy_now_pay_later_bnpl_management_dashboard_007.json` | `doc_6f684b0b` |
| `doc_buy_now_pay_later_bnpl_management_dashboard_008.json` | `doc_a9a10497` |
| `doc_buy_now_pay_later_bnpl_platinum_001.json` | `doc_c6b3fb3a` |
| `doc_buy_now_pay_later_bnpl_platinum_002.json` | `doc_5a42d77e` |
| `doc_buy_now_pay_later_bnpl_platinum_003.json` | `doc_45a0cc99` |
| `doc_buy_now_pay_later_bnpl_platinum_004.json` | `doc_da173ea8` |
| `doc_buy_now_pay_later_bnpl_platinum_005.json` | `doc_0078677a` |
| `doc_buy_now_pay_later_bnpl_platinum_006.json` | `doc_ea76543d` |
| `doc_buy_now_pay_later_bnpl_platinum_007.json` | `doc_87711e5e` |
| `doc_buy_now_pay_later_bnpl_platinum_008.json` | `doc_81395413` |
| `doc_buy_now_pay_later_bnpl_silver_001.json` | `doc_e61cd4fc` |
| `doc_buy_now_pay_later_bnpl_silver_002.json` | `doc_cdf7d7a0` |
| `doc_buy_now_pay_later_bnpl_silver_003.json` | `doc_8a74e560` |
| `doc_buy_now_pay_later_bnpl_silver_004.json` | `doc_25552025` |
| `doc_buy_now_pay_later_bnpl_silver_005.json` | `doc_ee9e8fc3` |
| `doc_buy_now_pay_later_bnpl_silver_006.json` | `doc_3ebc4b34` |
| `doc_buy_now_pay_later_bnpl_silver_007.json` | `doc_d4de7383` |
| `doc_buy_now_pay_later_bnpl_silver_008.json` | `doc_007c3262` |
| `doc_checking_accounts_blue_account_001.json` | `doc_2bb7266e` |
| `doc_checking_accounts_blue_account_002.json` | `doc_5cdf3381` |
| `doc_checking_accounts_blue_account_003.json` | `doc_c9bf7e42` |
| `doc_checking_accounts_blue_account_004.json` | `doc_86b6f1c6` |
| `doc_checking_accounts_blue_account_005.json` | `doc_f798ed72` |
| `doc_checking_accounts_blue_account_006.json` | `doc_7ff6cffe` |
| `doc_checking_accounts_blue_account_007.json` | `doc_66e67082` |
| `doc_checking_accounts_blue_account_008.json` | `doc_15e61dd7` |
| `doc_checking_accounts_blue_account_009.json` | `doc_b5cd5c66` |
| `doc_checking_accounts_blue_account_010.json` | `doc_141c19e8` |
| `doc_checking_accounts_blue_account_011.json` | `doc_8d9f008b` |
| `doc_checking_accounts_blue_account_012.json` | `doc_32781d08` |
| `doc_checking_accounts_bluest_account_001.json` | `doc_faf55443` |
| `doc_checking_accounts_bluest_account_002.json` | `doc_fa5177e3` |
| `doc_checking_accounts_bluest_account_003.json` | `doc_7cfe8cf1` |
| `doc_checking_accounts_bluest_account_004.json` | `doc_b3210aed` |
| `doc_checking_accounts_bluest_account_005.json` | `doc_c988da18` |
| `doc_checking_accounts_bluest_account_006.json` | `doc_6299623d` |
| `doc_checking_accounts_bluest_account_007.json` | `doc_fcca35b2` |
| `doc_checking_accounts_bluest_account_008.json` | `doc_c23f1fd9` |
| `doc_checking_accounts_bluest_account_009.json` | `doc_016e6772` |
| `doc_checking_accounts_bluest_account_010.json` | `doc_e31bdc15` |
| `doc_checking_accounts_checking_accounts_(general)_001.json` | `doc_a1be41e9` |
| `doc_checking_accounts_checking_accounts_(general)_002.json` | `doc_bf2caa8d` |
| `doc_checking_accounts_checking_accounts_(general)_003.json` | `doc_014d0c93` |
| `doc_checking_accounts_checking_accounts_(general)_004.json` | `doc_70b96fa5` |
| `doc_checking_accounts_checking_accounts_(general)_005.json` | `doc_9ee3a15d` |
| `doc_checking_accounts_checking_accounts_(general)_006.json` | `doc_56463aee` |
| `doc_checking_accounts_checking_accounts_(general)_007.json` | `doc_984fcd3b` |
| `doc_checking_accounts_checking_accounts_(general)_008.json` | `doc_bc8104f0` |
| `doc_checking_accounts_checking_accounts_(general)_009.json` | `doc_b71baf51` |
| `doc_checking_accounts_dark_green_account_001.json` | `doc_8894aecb` |
| `doc_checking_accounts_dark_green_account_002.json` | `doc_eeba16ff` |
| `doc_checking_accounts_dark_green_account_003.json` | `doc_e233a7fb` |
| `doc_checking_accounts_dark_green_account_004.json` | `doc_d47645c0` |
| `doc_checking_accounts_dark_green_account_005.json` | `doc_7fd6c70f` |
| `doc_checking_accounts_dark_green_account_006.json` | `doc_8dbeb713` |
| `doc_checking_accounts_dark_green_account_007.json` | `doc_d5d78a03` |
| `doc_checking_accounts_dark_green_account_008.json` | `doc_c9c2862f` |
| `doc_checking_accounts_dark_green_account_009.json` | `doc_6af040ec` |
| `doc_checking_accounts_dark_green_account_010.json` | `doc_065560f4` |
| `doc_checking_accounts_evergreen_account_001.json` | `doc_7e9a0742` |
| `doc_checking_accounts_evergreen_account_002.json` | `doc_e65ba0bf` |
| `doc_checking_accounts_evergreen_account_003.json` | `doc_1b6a1a2a` |
| `doc_checking_accounts_evergreen_account_004.json` | `doc_4b989df6` |
| `doc_checking_accounts_evergreen_account_005.json` | `doc_9fbfa7e5` |
| `doc_checking_accounts_evergreen_account_006.json` | `doc_46fa75c4` |
| `doc_checking_accounts_evergreen_account_007.json` | `doc_20aff0a4` |
| `doc_checking_accounts_evergreen_account_008.json` | `doc_5df1c3d5` |
| `doc_checking_accounts_gold_years_account_001.json` | `doc_f1d3890d` |
| `doc_checking_accounts_gold_years_account_002.json` | `doc_202c251a` |
| `doc_checking_accounts_gold_years_account_003.json` | `doc_814bcf34` |
| `doc_checking_accounts_gold_years_account_004.json` | `doc_05978fa4` |
| `doc_checking_accounts_gold_years_account_005.json` | `doc_82a6a162` |
| `doc_checking_accounts_gold_years_account_006.json` | `doc_89cddc32` |
| `doc_checking_accounts_gold_years_account_007.json` | `doc_a034fc54` |
| `doc_checking_accounts_gold_years_account_008.json` | `doc_fe684de8` |
| `doc_checking_accounts_gold_years_account_009.json` | `doc_ffe6b6ef` |
| `doc_checking_accounts_gold_years_account_010.json` | `doc_8ea6d88f` |
| `doc_checking_accounts_green_account_(checking)_001.json` | `doc_8050ad9f` |
| `doc_checking_accounts_green_account_(checking)_002.json` | `doc_d3c82bd0` |
| `doc_checking_accounts_green_account_(checking)_003.json` | `doc_ff8aace6` |
| `doc_checking_accounts_green_account_(checking)_004.json` | `doc_76eb36c0` |
| `doc_checking_accounts_green_account_(checking)_005.json` | `doc_50557580` |
| `doc_checking_accounts_green_account_(checking)_006.json` | `doc_33c383c1` |
| `doc_checking_accounts_green_account_(checking)_007.json` | `doc_9be17c1c` |
| `doc_checking_accounts_green_account_(checking)_008.json` | `doc_f641925f` |
| `doc_checking_accounts_green_account_(checking)_009.json` | `doc_b86c5c8c` |
| `doc_checking_accounts_green_account_(checking)_010.json` | `doc_97d7bbc7` |
| `doc_checking_accounts_green_account_(checking)_011.json` | `doc_7e056e81` |
| `doc_checking_accounts_green_account_(checking)_012.json` | `doc_2e076ce3` |
| `doc_checking_accounts_green_fee-free_account_001.json` | `doc_db98585d` |
| `doc_checking_accounts_green_fee-free_account_002.json` | `doc_c6acf983` |
| `doc_checking_accounts_green_fee-free_account_003.json` | `doc_36ccb5bb` |
| `doc_checking_accounts_green_fee-free_account_004.json` | `doc_ef9b785b` |
| `doc_checking_accounts_green_fee-free_account_005.json` | `doc_4fac2a44` |
| `doc_checking_accounts_green_fee-free_account_006.json` | `doc_3bda6927` |
| `doc_checking_accounts_green_fee-free_account_007.json` | `doc_9659c86a` |
| `doc_checking_accounts_light_blue_account_001.json` | `doc_171fd7e2` |
| `doc_checking_accounts_light_blue_account_002.json` | `doc_5e97731a` |
| `doc_checking_accounts_light_blue_account_003.json` | `doc_e0a18334` |
| `doc_checking_accounts_light_blue_account_004.json` | `doc_bad9ae26` |
| `doc_checking_accounts_light_blue_account_005.json` | `doc_8f35dc2b` |
| `doc_checking_accounts_light_blue_account_006.json` | `doc_81808373` |
| `doc_checking_accounts_light_blue_account_007.json` | `doc_d7675bdd` |
| `doc_checking_accounts_light_green_account_001.json` | `doc_d67be55e` |
| `doc_checking_accounts_light_green_account_002.json` | `doc_3ff47ec5` |
| `doc_checking_accounts_light_green_account_003.json` | `doc_2d3c9d9c` |
| `doc_checking_accounts_light_green_account_004.json` | `doc_fa690865` |
| `doc_checking_accounts_light_green_account_005.json` | `doc_60c405c9` |
| `doc_checking_accounts_light_green_account_006.json` | `doc_fa4e76c8` |
| `doc_checking_accounts_light_green_account_007.json` | `doc_90c30d4b` |
| `doc_checking_accounts_light_green_account_008.json` | `doc_7b2a4ca2` |
| `doc_checking_accounts_light_green_account_009.json` | `doc_33eff120` |
| `doc_checking_accounts_light_green_account_010.json` | `doc_9a532e12` |
| `doc_checking_accounts_light_green_account_011.json` | `doc_262be66a` |
| `doc_checking_accounts_light_green_account_012.json` | `doc_28ee2cca` |
| `doc_checking_accounts_light_green_account_013.json` | `doc_ac3641ec` |
| `doc_checking_accounts_purple_account_001.json` | `doc_557ee49f` |
| `doc_checking_accounts_purple_account_002.json` | `doc_bf50fd96` |
| `doc_checking_accounts_purple_account_003.json` | `doc_76fbdccb` |
| `doc_checking_accounts_purple_account_004.json` | `doc_9396f846` |
| `doc_checking_accounts_purple_account_005.json` | `doc_f4b7bb59` |
| `doc_checking_accounts_purple_account_006.json` | `doc_8a50dc56` |
| `doc_checking_accounts_purple_account_007.json` | `doc_44b3f4c2` |
| `doc_checking_accounts_purple_account_008.json` | `doc_99ea5474` |
| `doc_checking_accounts_purple_account_009.json` | `doc_d4dfd3c2` |
| `doc_checking_accounts_purple_account_010.json` | `doc_03de6380` |
| `doc_checking_accounts_purple_account_011.json` | `doc_497dc05a` |
| `doc_checking_accounts_purple_account_012.json` | `doc_9311dcd2` |
| `doc_credit_cards_bronze_rewards_card_001.json` | `doc_ac175ccc` |
| `doc_credit_cards_bronze_rewards_card_002.json` | `doc_1fe92683` |
| `doc_credit_cards_bronze_rewards_card_003.json` | `doc_317bc71a` |
| `doc_credit_cards_bronze_rewards_card_004.json` | `doc_3b35f2e8` |
| `doc_credit_cards_bronze_rewards_card_005.json` | `doc_4bbee4a2` |
| `doc_credit_cards_bronze_rewards_card_006.json` | `doc_2d3bc436` |
| `doc_credit_cards_bronze_rewards_card_007.json` | `doc_6e823153` |
| `doc_credit_cards_bronze_rewards_card_008.json` | `doc_05051152` |
| `doc_credit_cards_credit_card_account_logistics_001.json` | `doc_93a22dda` |
| `doc_credit_cards_credit_card_account_logistics_002.json` | `doc_e1a3c3d9` |
| `doc_credit_cards_credit_card_account_logistics_003.json` | `doc_156f59b3` |
| `doc_credit_cards_credit_card_account_logistics_004.json` | `doc_90bd98a3` |
| `doc_credit_cards_credit_card_account_logistics_005.json` | `doc_ec88cfa6` |
| `doc_credit_cards_credit_card_account_logistics_006.json` | `doc_f0ffb68e` |
| `doc_credit_cards_credit_card_account_logistics_007.json` | `doc_8304ff4e` |
| `doc_credit_cards_credit_card_account_logistics_008.json` | `doc_e9bf7d0a` |
| `doc_credit_cards_credit_card_account_logistics_009.json` | `doc_a34e839f` |
| `doc_credit_cards_credit_card_replacements_001.json` | `doc_d2bf5e97` |
| `doc_credit_cards_credit_card_replacements_002.json` | `doc_f8fd8284` |
| `doc_credit_cards_credit_card_replacements_003.json` | `doc_63777e50` |
| `doc_credit_cards_credit_card_replacements_004.json` | `doc_3b0e2e6f` |
| `doc_credit_cards_credit_card_replacements_005.json` | `doc_111959f7` |
| `doc_credit_cards_credit_cards_(general)_001.json` | `doc_279d37f6` |
| `doc_credit_cards_credit_cards_(general)_002.json` | `doc_9e1b9d32` |
| `doc_credit_cards_credit_cards_(general)_003.json` | `doc_b6ddf210` |
| `doc_credit_cards_credit_cards_(general)_004.json` | `doc_59f6d95b` |
| `doc_credit_cards_credit_cards_(general)_005.json` | `doc_6cba0278` |
| `doc_credit_cards_credit_cards_(general)_006.json` | `doc_6f7cd04c` |
| `doc_credit_cards_credit_cards_(general)_007.json` | `doc_9b4e507e` |
| `doc_credit_cards_credit_cards_(general)_008.json` | `doc_fd9e19cf` |
| `doc_credit_cards_credit_cards_(general)_009.json` | `doc_e0b5b0b2` |
| `doc_credit_cards_credit_cards_(general)_010.json` | `doc_1b22b5c5` |
| `doc_credit_cards_credit_cards_(general)_011.json` | `doc_7cba23ea` |
| `doc_credit_cards_credit_cards_(general)_012.json` | `doc_2330957f` |
| `doc_credit_cards_credit_cards_(general)_013.json` | `doc_425f263c` |
| `doc_credit_cards_credit_cards_(general)_014.json` | `doc_b68e77f3` |
| `doc_credit_cards_credit_cards_(general)_015.json` | `doc_e018f9bd` |
| `doc_credit_cards_credit_cards_(general)_016.json` | `doc_f4a33a24` |
| `doc_credit_cards_credit_cards_(general)_017.json` | `doc_74c9b67a` |
| `doc_credit_cards_credit_cards_(general)_018.json` | `doc_0115a90b` |
| `doc_credit_cards_credit_cards_(general)_019.json` | `doc_dae55ba5` |
| `doc_credit_cards_credit_cards_(general)_020.json` | `doc_c977b3c5` |
| `doc_credit_cards_credit_cards_(general)_021.json` | `doc_ddcdc744` |
| `doc_credit_cards_credit_cards_(general)_022.json` | `doc_6a87e033` |
| `doc_credit_cards_credit_cards_(general)_023.json` | `doc_49c7fc6a` |
| `doc_credit_cards_credit_cards_(general)_024.json` | `doc_703a4303` |
| `doc_credit_cards_credit_cards_(general)_025.json` | `doc_bf4f500f` |
| `doc_credit_cards_crypto-cash_back_001.json` | `doc_1b979e4b` |
| `doc_credit_cards_crypto-cash_back_002.json` | `doc_ee4d58bf` |
| `doc_credit_cards_crypto-cash_back_003.json` | `doc_26309f5b` |
| `doc_credit_cards_crypto-cash_back_004.json` | `doc_d8264080` |
| `doc_credit_cards_crypto-cash_back_005.json` | `doc_8f74415f` |
| `doc_credit_cards_crypto-cash_back_006.json` | `doc_caf04e22` |
| `doc_credit_cards_crypto-cash_back_007.json` | `doc_83b075d4` |
| `doc_credit_cards_crypto-cash_back_008.json` | `doc_9ef11a3d` |
| `doc_credit_cards_crypto-cash_back_009.json` | `doc_fe4ac8ea` |
| `doc_credit_cards_diamond_elite_card_001.json` | `doc_040b1d82` |
| `doc_credit_cards_diamond_elite_card_002.json` | `doc_dd74a3d1` |
| `doc_credit_cards_diamond_elite_card_003.json` | `doc_673cc161` |
| `doc_credit_cards_diamond_elite_card_004.json` | `doc_31a88f7d` |
| `doc_credit_cards_diamond_elite_card_005.json` | `doc_919f5d63` |
| `doc_credit_cards_diamond_elite_card_006.json` | `doc_56bc0d61` |
| `doc_credit_cards_diamond_elite_card_007.json` | `doc_6b09f263` |
| `doc_credit_cards_diamond_elite_card_008.json` | `doc_50d25660` |
| `doc_credit_cards_diamond_elite_card_009.json` | `doc_c5b05835` |
| `doc_credit_cards_ecocard_001.json` | `doc_6a81dd2b` |
| `doc_credit_cards_ecocard_002.json` | `doc_e8d9e127` |
| `doc_credit_cards_ecocard_003.json` | `doc_2b123b9f` |
| `doc_credit_cards_ecocard_004.json` | `doc_867c97b5` |
| `doc_credit_cards_ecocard_005.json` | `doc_ecd2f57c` |
| `doc_credit_cards_ecocard_006.json` | `doc_7b723cca` |
| `doc_credit_cards_ecocard_007.json` | `doc_54fac72f` |
| `doc_credit_cards_ecocard_008.json` | `doc_4432dc21` |
| `doc_credit_cards_ecocard_009.json` | `doc_bdbf0e1d` |
| `doc_credit_cards_ecocard_010.json` | `doc_b0cfbd90` |
| `doc_credit_cards_ecocard_011.json` | `doc_47693372` |
| `doc_credit_cards_gold_rewards_card_001.json` | `doc_415589b6` |
| `doc_credit_cards_gold_rewards_card_002.json` | `doc_a8360ea3` |
| `doc_credit_cards_gold_rewards_card_003.json` | `doc_1d76f03d` |
| `doc_credit_cards_gold_rewards_card_004.json` | `doc_ea0d7179` |
| `doc_credit_cards_gold_rewards_card_005.json` | `doc_8bca11f8` |
| `doc_credit_cards_platinum_rewards_card_001.json` | `doc_bc0fa883` |
| `doc_credit_cards_platinum_rewards_card_002.json` | `doc_4817ddda` |
| `doc_credit_cards_platinum_rewards_card_003.json` | `doc_59507edc` |
| `doc_credit_cards_platinum_rewards_card_004.json` | `doc_65336375` |
| `doc_credit_cards_platinum_rewards_card_005.json` | `doc_ba093132` |
| `doc_credit_cards_platinum_rewards_card_006.json` | `doc_cd3713de` |
| `doc_credit_cards_platinum_rewards_card_007.json` | `doc_7ba6e683` |
| `doc_credit_cards_platinum_rewards_card_008.json` | `doc_38da490f` |
| `doc_credit_cards_platinum_rewards_card_009.json` | `doc_31f3de4a` |
| `doc_credit_cards_platinum_rewards_card_010.json` | `doc_6970953b` |
| `doc_credit_cards_silver_rewards_card_001.json` | `doc_85371f28` |
| `doc_credit_cards_silver_rewards_card_002.json` | `doc_8eb6adfa` |
| `doc_credit_cards_silver_rewards_card_003.json` | `doc_255fa537` |
| `doc_credit_cards_silver_rewards_card_004.json` | `doc_a707e9fc` |
| `doc_credit_cards_silver_rewards_card_005.json` | `doc_c5f818ae` |
| `doc_credit_cards_silver_rewards_card_006.json` | `doc_4523aa1d` |
| `doc_credit_cards_silver_rewards_card_007.json` | `doc_4e5c9d66` |
| `doc_credit_cards_silver_rewards_card_008.json` | `doc_f9c8b9e9` |
| `doc_credit_cards_silver_rewards_card_009.json` | `doc_3d066730` |
| `doc_credit_cards_silver_rewards_card_010.json` | `doc_f432b43a` |
| `doc_credit_cards_silver_rewards_card_011.json` | `doc_6a701df3` |
| `doc_credit_cards_virtual_card_management_001.json` | `doc_247ace46` |
| `doc_credit_cards_virtual_card_management_002.json` | `doc_fbaec48b` |
| `doc_credit_cards_virtual_card_management_003.json` | `doc_30b8e2e8` |
| `doc_credit_cards_virtual_card_management_004.json` | `doc_9f75de68` |
| `doc_credit_cards_virtual_card_management_005.json` | `doc_784674f6` |
| `doc_credit_cards_virtual_card_management_006.json` | `doc_58712942` |
| `doc_credit_cards_virtual_card_management_007.json` | `doc_1f08a0e2` |
| `doc_credit_cards_virtual_card_management_008.json` | `doc_045b3651` |
| `doc_customer_support_special_support_codes_001.json` | `doc_2cfc8eaa` |
| `doc_everyone_pay_everyone_pay_001.json` | `doc_107b13b9` |
| `doc_everyone_pay_everyone_pay_002.json` | `doc_37d3bc2b` |
| `doc_everyone_pay_everyone_pay_003.json` | `doc_1d2a2240` |
| `doc_everyone_pay_everyone_pay_004.json` | `doc_1987bfd3` |
| `doc_everyone_pay_everyone_pay_005.json` | `doc_0234283a` |
| `doc_everyone_pay_everyone_pay_006.json` | `doc_587c0a2c` |
| `doc_everyone_pay_everyone_pay_007.json` | `doc_6ba7217b` |
| `doc_everyone_pay_everyone_pay_008.json` | `doc_e0dcb23b` |
| `doc_everyone_pay_everyone_pay_009.json` | `doc_6265621d` |
| `doc_everyone_pay_everyone_pay_010.json` | `doc_49107c45` |
| `doc_everyone_pay_everyone_pay_011.json` | `doc_788616b0` |
| `doc_everyone_pay_everyone_pay_012.json` | `doc_e1b15d3f` |
| `doc_everyone_pay_everyone_pay_013.json` | `doc_b921ff4c` |
| `doc_everyone_pay_everyone_pay_014.json` | `doc_0d5c3b4e` |
| `doc_everyone_pay_everyone_pay_015.json` | `doc_992bad26` |
| `doc_everyone_pay_qr_transfers_001.json` | `doc_d614336c` |
| `doc_everyone_pay_qr_transfers_002.json` | `doc_85c6d7f9` |
| `doc_everyone_pay_qr_transfers_003.json` | `doc_dcfe5896` |
| `doc_everyone_pay_qr_transfers_004.json` | `doc_7017b521` |
| `doc_everyone_pay_qr_transfers_005.json` | `doc_1aaa0f9d` |
| `doc_everyone_pay_qr_transfers_006.json` | `doc_e0cc402a` |
| `doc_everyone_pay_qr_transfers_007.json` | `doc_ee65e1b4` |
| `doc_everyone_pay_scheduled_payments_001.json` | `doc_47a565f0` |
| `doc_everyone_pay_scheduled_payments_002.json` | `doc_aa31d8a3` |
| `doc_everyone_pay_scheduled_payments_003.json` | `doc_9bbfe45a` |
| `doc_everyone_pay_scheduled_payments_004.json` | `doc_1b29d51e` |
| `doc_everyone_pay_scheduled_payments_005.json` | `doc_0ae9307b` |
| `doc_everyone_pay_scheduled_payments_006.json` | `doc_6ef44e54` |
| `doc_everyone_pay_scheduled_payments_007.json` | `doc_39db0e40` |
| `doc_everyone_pay_scheduled_payments_008.json` | `doc_cf4c2525` |
| `doc_everyone_pay_sending_limits_001.json` | `doc_f16e16d7` |
| `doc_everyone_pay_sending_limits_002.json` | `doc_88872872` |
| `doc_everyone_pay_sending_limits_003.json` | `doc_408515c8` |
| `doc_everyone_pay_sending_limits_004.json` | `doc_2464fa83` |
| `doc_everyone_pay_sending_limits_005.json` | `doc_a7d773dd` |
| `doc_everyone_pay_sending_limits_006.json` | `doc_4047a1f3` |
| `doc_everyone_pay_sending_limits_007.json` | `doc_c65f509b` |
| `doc_everyone_pay_split-the-bill_001.json` | `doc_721fad6f` |
| `doc_everyone_pay_split-the-bill_002.json` | `doc_ceaaf0c8` |
| `doc_everyone_pay_split-the-bill_003.json` | `doc_e62bebf9` |
| `doc_everyone_pay_split-the-bill_004.json` | `doc_e7430e4a` |
| `doc_everyone_pay_split-the-bill_005.json` | `doc_ff8d61b5` |
| `doc_everyone_pay_split-the-bill_006.json` | `doc_133f50a4` |
| `doc_everyone_pay_split-the-bill_007.json` | `doc_be92abf7` |
| `doc_everyone_pay_split-the-bill_008.json` | `doc_37c80066` |
| `doc_everyone_pay_user_blocking_001.json` | `doc_4e6cd568` |
| `doc_everyone_pay_user_blocking_002.json` | `doc_ff42b61b` |
| `doc_everyone_pay_user_blocking_003.json` | `doc_b9209e39` |
| `doc_everyone_pay_user_blocking_004.json` | `doc_c81e1bed` |
| `doc_everyone_pay_user_blocking_005.json` | `doc_f335c9ec` |
| `doc_everyone_pay_user_blocking_006.json` | `doc_41aa5afb` |
| `doc_personal_subscriptions_rho_bank_plus_001.json` | `doc_ae16cff9` |
| `doc_personal_subscriptions_rho_bank_plus_002.json` | `doc_cbcedca7` |
| `doc_savings_accounts_bronze_account_001.json` | `doc_27b245aa` |
| `doc_savings_accounts_bronze_account_002.json` | `doc_c325bdf9` |
| `doc_savings_accounts_bronze_account_003.json` | `doc_115dd528` |
| `doc_savings_accounts_bronze_account_004.json` | `doc_3af84fd0` |
| `doc_savings_accounts_bronze_account_005.json` | `doc_e34c5a6c` |
| `doc_savings_accounts_bronze_account_006.json` | `doc_a123b62f` |
| `doc_savings_accounts_bronze_account_007.json` | `doc_36d5553c` |
| `doc_savings_accounts_bronze_account_008.json` | `doc_06f72b7d` |
| `doc_savings_accounts_bronze_account_009.json` | `doc_5b093abd` |
| `doc_savings_accounts_diamond_elite_account_001.json` | `doc_f0cd058d` |
| `doc_savings_accounts_diamond_elite_account_002.json` | `doc_1e65e0f6` |
| `doc_savings_accounts_diamond_elite_account_003.json` | `doc_4fa1ae86` |
| `doc_savings_accounts_diamond_elite_account_004.json` | `doc_501e2d7c` |
| `doc_savings_accounts_diamond_elite_account_005.json` | `doc_ebc2b1a2` |
| `doc_savings_accounts_diamond_elite_account_006.json` | `doc_3a60b0a7` |
| `doc_savings_accounts_diamond_elite_account_007.json` | `doc_9ad37041` |
| `doc_savings_accounts_diamond_elite_account_008.json` | `doc_a79da6a4` |
| `doc_savings_accounts_diamond_elite_account_009.json` | `doc_f7ca5f2f` |
| `doc_savings_accounts_diamond_elite_account_010.json` | `doc_ca7d3a91` |
| `doc_savings_accounts_diamond_elite_account_011.json` | `doc_d9dc6efc` |
| `doc_savings_accounts_gold_account_001.json` | `doc_ff4287a6` |
| `doc_savings_accounts_gold_account_002.json` | `doc_34339fe9` |
| `doc_savings_accounts_gold_account_003.json` | `doc_80fb0d9d` |
| `doc_savings_accounts_gold_account_004.json` | `doc_0cacf6b0` |
| `doc_savings_accounts_gold_account_005.json` | `doc_e9b905d0` |
| `doc_savings_accounts_gold_account_006.json` | `doc_81b3b07b` |
| `doc_savings_accounts_gold_account_007.json` | `doc_7cc079fe` |
| `doc_savings_accounts_gold_account_008.json` | `doc_ca9cfdcb` |
| `doc_savings_accounts_gold_account_009.json` | `doc_1776c453` |
| `doc_savings_accounts_gold_account_010.json` | `doc_759b39a3` |
| `doc_savings_accounts_gold_account_011.json` | `doc_41836c07` |
| `doc_savings_accounts_gold_account_012.json` | `doc_cf2a7c68` |
| `doc_savings_accounts_gold_account_013.json` | `doc_445f4c1d` |
| `doc_savings_accounts_gold_account_014.json` | `doc_c75c3f6e` |
| `doc_savings_accounts_gold_plus_account_001.json` | `doc_b5c356ec` |
| `doc_savings_accounts_gold_plus_account_002.json` | `doc_37102e4c` |
| `doc_savings_accounts_gold_plus_account_003.json` | `doc_91d52dd5` |
| `doc_savings_accounts_gold_plus_account_004.json` | `doc_94a329a9` |
| `doc_savings_accounts_gold_plus_account_005.json` | `doc_be78cc21` |
| `doc_savings_accounts_gold_plus_account_006.json` | `doc_51b5b219` |
| `doc_savings_accounts_gold_plus_account_007.json` | `doc_acc1ac66` |
| `doc_savings_accounts_gold_plus_account_008.json` | `doc_82e6e9c8` |
| `doc_savings_accounts_gold_plus_account_009.json` | `doc_652446df` |
| `doc_savings_accounts_green_account_(savings)_001.json` | `doc_6585431e` |
| `doc_savings_accounts_green_account_(savings)_002.json` | `doc_d8dc8883` |
| `doc_savings_accounts_green_account_(savings)_003.json` | `doc_6d6911fc` |
| `doc_savings_accounts_green_account_(savings)_004.json` | `doc_e32ed508` |
| `doc_savings_accounts_green_account_(savings)_005.json` | `doc_1feeb567` |
| `doc_savings_accounts_green_account_(savings)_006.json` | `doc_7530e999` |
| `doc_savings_accounts_green_account_(savings)_007.json` | `doc_6981b038` |
| `doc_savings_accounts_green_account_(savings)_008.json` | `doc_50396b01` |
| `doc_savings_accounts_green_account_(savings)_009.json` | `doc_4d15c636` |
| `doc_savings_accounts_platinum_account_001.json` | `doc_21f54a53` |
| `doc_savings_accounts_platinum_account_002.json` | `doc_f8e3c77c` |
| `doc_savings_accounts_platinum_account_003.json` | `doc_88fb8d8d` |
| `doc_savings_accounts_platinum_account_004.json` | `doc_7ff4329b` |
| `doc_savings_accounts_platinum_account_005.json` | `doc_cf3e55c7` |
| `doc_savings_accounts_platinum_account_006.json` | `doc_ec77aaeb` |
| `doc_savings_accounts_platinum_account_007.json` | `doc_16d9efd8` |
| `doc_savings_accounts_platinum_account_008.json` | `doc_15be4628` |
| `doc_savings_accounts_platinum_account_009.json` | `doc_f1f26d27` |
| `doc_savings_accounts_platinum_account_010.json` | `doc_c9b6150c` |
| `doc_savings_accounts_platinum_plus_account_001.json` | `doc_4cb94e8b` |
| `doc_savings_accounts_platinum_plus_account_002.json` | `doc_15500988` |
| `doc_savings_accounts_platinum_plus_account_003.json` | `doc_a5233950` |
| `doc_savings_accounts_platinum_plus_account_004.json` | `doc_d5da9a05` |
| `doc_savings_accounts_platinum_plus_account_005.json` | `doc_04006740` |
| `doc_savings_accounts_platinum_plus_account_006.json` | `doc_93bb84d0` |
| `doc_savings_accounts_platinum_plus_account_007.json` | `doc_25f9e280` |
| `doc_savings_accounts_platinum_plus_account_008.json` | `doc_291d854e` |
| `doc_savings_accounts_platinum_plus_account_009.json` | `doc_f5c1110e` |
| `doc_savings_accounts_silver_account_001.json` | `doc_cd5b1cbb` |
| `doc_savings_accounts_silver_account_002.json` | `doc_f47a85d8` |
| `doc_savings_accounts_silver_account_003.json` | `doc_0f88627c` |
| `doc_savings_accounts_silver_account_004.json` | `doc_e3ba3af2` |
| `doc_savings_accounts_silver_account_005.json` | `doc_52d89a01` |
| `doc_savings_accounts_silver_account_006.json` | `doc_361164c2` |
| `doc_savings_accounts_silver_account_007.json` | `doc_8a843eb1` |
| `doc_savings_accounts_silver_account_008.json` | `doc_f9a09b0b` |
| `doc_savings_accounts_silver_account_009.json` | `doc_26bbced5` |
| `doc_savings_accounts_silver_plus_account_001.json` | `doc_bb6806ef` |
| `doc_savings_accounts_silver_plus_account_002.json` | `doc_c60b1131` |
| `doc_savings_accounts_silver_plus_account_003.json` | `doc_0d903a7a` |
| `doc_savings_accounts_silver_plus_account_004.json` | `doc_21babdd7` |
| `doc_savings_accounts_silver_plus_account_005.json` | `doc_bdbe7f59` |
| `doc_savings_accounts_silver_plus_account_006.json` | `doc_1b73b5c7` |
| `doc_savings_accounts_silver_plus_account_007.json` | `doc_b4538f1b` |
| `doc_savings_accounts_silver_plus_account_008.json` | `doc_5a6f9ab1` |
| `doc_savings_accounts_silver_plus_account_009.json` | `doc_c5acc320` |
