# Fixing the other 51%: MISSING_WRITE and PRODUCT_SELECTION

Companion to [`policy_reasoning_deterministic_validation.md`](policy_reasoning_deterministic_validation.md),
which showed the reward-audit / cap-enforcement deterministic tools cover ~36% of POLICY_REASONING
(the cap/arithmetic/set/classification slice) but **not** the two largest buckets: **MISSING_WRITE (32
trials)** and **PRODUCT_SELECTION (30 trials)** — together 51%.

This document proposes fixes for those two. Each issue is written **in plain terms first** (what goes
wrong, what to do about it), then the **technical solution**. The fixes are grounded in the actual tool
wiring and knowledge-base policies, not assumed.

## Two facts that change the picture

1. **The domain's clock is frozen at 11/14/2025** (`src/tau2/domains/banking_knowledge/utils.py:17`).
   This matters because several "right answers" depend on which promotion is active on that date.
2. **Some required actions are the *customer's* to take, not the agent's.** `apply_for_credit_card`
   and `submit_referral` live in `KnowledgeUserTools` (`tools.py:4325`, `4382`) — the agent cannot call
   them. The agent's job there is to recommend and instruct; the customer clicks the button. Other
   actions (`pay_credit_card_from_checking_9182`, `close_credit_card_account_7834`,
   `order_replacement_credit_card_7291`, `apply_statement_credit_8472`) are the agent's own tools
   (`KnowledgeTools`) that it sometimes refuses to use.

---

# Part A — MISSING_WRITE (a required action never happens)

These 32 trials are **not** wrong-value errors, so no value-checking tool helps. The agent reasoned
fine and then didn't complete the write. Looking at every trial, the "didn't complete" splits into four
distinct problems, each with its own fix.

## A1. The agent won't use its own tools

**In plain terms.**
The customer asks to pay off a $75 balance, or close a card, or apply a credit. The agent has a button
that does exactly that — but it says *"I'm not able to do that, you'll need to do it yourself"* and
defers. The action never happens. (Examples: task_043, task_045 — refused to pay the balance it was
fully able to pay.)

**The fix, in plain terms.**
Tell the agent, in writing, exactly which actions it is allowed to perform for the customer, and that it
must perform them instead of pushing the work back to the customer.

**Technical solution.**
- **Policy (primary):** add an explicit authorization block to the agent policy listing the agent-side
  WRITE tools it is empowered to call on the customer's behalf — `pay_credit_card_from_checking_9182`,
  `close_credit_card_account_7834`, `order_replacement_credit_card_7291`, `apply_statement_credit_8472`,
  `log_verification`, the dispute/replacement tools — with the line: *"You are authorized to execute
  these actions directly; do not tell the customer to do it themselves."* This is the table's
  highest-ranked fix (I1) and is a near-zero-risk prompt change.
- **Deterministic backstop (Stop-hook completion gate):** when the agent tries to end the conversation,
  run a check: did the agent *state an intent to act* ("I'll process that", "let me pay that off") with
  no matching tool call in the transcript? If so, block the stop and return a reminder. The
  intent-detection step is fuzzy (a cheap classifier), but the "was the tool called?" half is fully
  deterministic. This catches refusals the prompt alone misses.

## A2. The agent forgets to hand off the actions only the customer can complete

**In plain terms.**
Applying for a card and sending a referral are things the customer does in their own app — the agent
genuinely can't do them. But instead of saying *"Here's exactly what to apply for — go ahead and submit
it now,"* the agent transfers to a human, or wrongly says it's impossible (*"that card doesn't exist",
"the referral can't be re-submitted"*), or just gives vague advice. So the customer never applies.
(Examples: task_023, task_063, task_064 — agent concluded it "has no application tool" and stalled;
task_010 — told the customer the referral couldn't be re-submitted; task_044 — said no qualifying card
exists.)

**The fix, in plain terms.**
Make the agent always close these out with a clear, specific instruction — name the exact product, tell
the customer to apply or submit right now, and confirm it's done — and never transfer just because "I
can't apply for you."

**Technical solution.**
- **Policy:** a section stating `apply_for_credit_card` and `submit_referral` are **customer-completed**
  actions, and the agent's required closing steps are: (1) name the exact `card_type` / `account_type`,
  (2) explicitly instruct the customer to complete the application/referral now, (3) confirm completion
  before ending. Forbid `transfer_to_human_agents` as a substitute for instructing the customer.
- **Deterministic backstop:** the customer already has these tools in their default toolset (they are
  `@is_tool`, not gated behind a give-step), so they *can* act the moment they're told. Extend the Stop
  gate: if the task involved a card application or referral and no `apply_for_credit_card` /
  `submit_referral` call exists, re-prompt the agent to instruct the customer before closing.
- **Residual risk:** this depends on the simulated customer following the instruction. That risk is
  small — USER_SIM accounts for only 4 trials total — but it is real and worth flagging; the agent fix
  removes the agent-side blocker, not the (rare) sim-side one.

## A3. The agent does the main action but skips the required checks around it

**In plain terms.**
Some actions have mandatory companion steps. Closing a card, for instance, requires first checking for
open disputes and any pending replacement card. The agent closes the card but skips the checks, so the
final record doesn't match what policy requires. (Examples: task_043, task_045, task_053 — paid/filed
correctly but omitted the dispute-history and pending-replacement checks.)

**The fix, in plain terms.**
Make the checks part of the action itself — the system shouldn't let you close the card without running
them — so they can't be forgotten.

**Technical solution (deterministic — the strong one).**
- **Bundle the pre-checks into the action tool.** Have `close_credit_card_account_7834` internally run
  (or require evidence of) `get_user_dispute_history_7291` and `get_pending_replacement_orders_5765`,
  and refuse with guidance if they haven't happened. Do the same for the retention/closure flow by
  exposing it as a single composite tool that performs the eligibility checklist as one transaction.
- This is the same shape as the cap-enforcement fix in the first doc: **encode the required procedure as
  a tool invariant** so the agent physically cannot skip a step. Fully deterministic.

## A4. The agent does things in the wrong order, or picks the wrong procedure

**In plain terms.**
A few jobs have a required order or a required branch. Example order: raise the credit limit *before*
filing a dispute that locks the card — do it after, and the increase is blocked (task_053, task_054).
Example branch: on a specific security flag, the rule is *close-and-reissue the card*, not *reset the
PIN* — the agent reset the PIN (task_091, task_092). Wrong order or wrong branch → the required write
never lands.

**The fix, in plain terms.**
Write the order and the branch into the tools as rules: you can't do step 2 before step 1, and the
correct procedure is chosen automatically from the security flag.

**Technical solution.**
- **Pre-flight dependency guards:** `submit_credit_limit_increase` checks the card is still
  increase-eligible (no dispute/replacement lock) before proceeding; close/order tools check
  prerequisites. A guard that *blocks the out-of-order call with a corrective message* turns an inferred
  rule into an enforced one.
- **Flag → procedure lookup:** a deterministic table mapping each security flag/code to the required
  action (e.g. `Single-Flag-Escalation → close+reissue`, not PIN-reset). The agent reads the required
  procedure rather than guessing it. Overlaps the P5 "gated procedures" recommendation.

### How A1–A4 divide up
- **Deterministic (tool invariants):** A3 (bundle pre-checks) and A4 (sequencing/branch guards) — the
  same "rule-as-code" mechanism the first doc validated for caps.
- **Policy + deterministic backstop:** A1 (authorization) and A2 (customer handoff) — these are
  fundamentally prompt/policy fixes (the table's I1/I2/I3) with a Stop-gate as a safety net. Be honest:
  they are cheap and high-leverage, but they are *not* "move the computation into code."

---

# Part B — PRODUCT_SELECTION (the agent recommends the wrong product)

**In plain terms.**
The customer describes what they need ("a travel card with no foreign-transaction fees and purchase
protection"; "the business checking account with cash-back on everyday spend"). The agent picks a card
or account — and picks the wrong one. Almost always it does one of three things: upsells to a fancier,
pricier product than needed; picks one that's missing a feature the customer specifically required; or
recommends one the customer can't even get.

**The key discovery: the right answer follows a definite rule that is written in the bank's own
policies.** It is not a judgment call. We confirmed this across all 16 tasks — the agent simply fails to
find and apply the rule.

### The rule (plain terms)
1. **Cross off what the customer can't get** — invitation-only cards (Diamond Elite), income or credit
   score below the threshold, missing subscription.
2. **Cross off anything missing a must-have the customer named** — no foreign-transaction fees, ATM-fee
   rebates, overdraft, a specific cash-back category, a high-enough credit limit, etc.
3. **Among what survives, pick the one that best serves the customer's main goal** — most cash back,
   highest interest (APY), lowest fees, or whichever product is *currently under promotion*. Promotions
   are date-specific, and the bank runs overlapping ones, so the date has to be checked.

### Why the agent fails (plain terms)
- It anchors on the first impressive product it reads about and **upsells** (task_001: picked
  invitation-only Diamond Elite; task_044: pitched the weaker existing card and closed the account).
- It **skips the feature filter** (task_069: picked the Gold account, which lacks the ATM rebates the
  customer required; task_075: picked an account with a $75k minimum the customer couldn't meet).
- It **ignores the promotion's date** (task_071: gold is Sky Blue, which is the account under promotion
  on 11/14/2025; agents picked Lime Green / Hunter Green — the winners of a *different* promotion whose
  window had already closed on 11/12).

**The fix, in plain terms.**
Give the agent a "product finder" that does the three-step filtering by rule, and require it to
recommend whatever the finder returns instead of choosing from memory. Then pair it with the
application-handoff fix (A2) so the customer actually applies for the right one.

**Technical solution.**
- **Build a structured product catalog** — one row per card / checking / savings product, with
  machine-readable fields:
  - *eligibility:* `invitation_only`, `min_income`, `min_credit_score`, `subscription_required`
  - *features:* `fx_fee`, `purchase_protection`, `atm_rebates`, `overdraft`, `cashback_categories`
  - *economics:* `annual_fee`, `cashback_rate_by_category`, `apy`, `atm_fees`, `min_balance`,
    `credit_limit_range`
  - *promotions:* `promo_priority` entries with `start_date`/`end_date` windows
  Source it from `register_corpus/` (already consolidating per-product docs into one file each). The
  attributes exist in the KB today as prose (e.g. Silver Rewards: FX 2.75% / 0% with subscription,
  purchase protection $3,000, limit ≤ $100k, $0 annual fee) — this step makes them machine-readable.
- **Add a deterministic `recommend_product` agent tool:**
  `recommend_product(category, hard_constraints, objective, today="11/14/2025")` →
  (1) filter by eligibility, (2) filter by hard constraints, (3) rank survivors by `objective`
  (`max_cashback` | `max_apy` | `min_fee`) with **promotional priority as the tie-break, using only
  promos whose date window contains `today`**. Returns the product(s) plus the reason each constraint is
  met (auditable).
- **Shrink the LLM's job** to extracting `{category, hard_constraints, objective}` from the
  conversation — far narrower and more checkable than free-selecting a product from prose.
- **Policy:** when recommending a product, the agent **must** call `recommend_product` and recommend its
  output; it may not free-select.
- **Why this avoids the gate-blindness problem:** the earlier validation noted the *customer's* apply
  call can't be intercepted. We don't try to. `recommend_product` is an **agent** tool, fully reachable;
  we fix the recommendation that precedes the apply, then use A2 to drive the customer to apply for the
  right product.

### One nuance the catalog must handle
The eligibility filter is **"what this customer can get,"** not "always drop premium cards." task_023's
gold *is* the invitation-only Diamond Elite, because that customer qualifies/requests it. So the filter
keys on the customer's actual eligibility signals, and invitation-only is excluded only when
unattainable. The recommender therefore needs the customer's income/score/subscription as inputs.

---

# Honest assessment

**What is genuinely deterministic here:**
- A3 (bundle required pre-checks into the action tool), A4 (sequencing / flag→procedure guards), and B
  (the `recommend_product` finder). These are "rule-as-tool-invariant," the same mechanism the first doc
  validated for caps and arithmetic.

**What is policy-with-a-backstop, not pure code:**
- A1 (authorization) and A2 (customer handoff). These are the I1/I2/I3 prompt fixes — cheap, high
  leverage, table-ranked #1 — but advisory at core, with a deterministic Stop-gate only as a safety net.
  Do not oversell them as "deterministic."

**Biggest cost and risk:**
- The structured product catalog (B) is the main build. Each attribute must be extracted from the KB and
  validated, then kept in sync — and an extraction error in the catalog becomes a *systematic* wrong
  recommendation. Budget for catalog validation, not just construction.
- Residual LLM steps remain everywhere they're narrowest: constraint/objective extraction (B), intent
  detection in the Stop-gate (A1/A2).

**Rough coverage of the 62 trials:**
- B addresses the ~30 PRODUCT_SELECTION trials (contingent on the catalog).
- A1–A4 address the ~32 MISSING_WRITE trials, but **split**: roughly two-thirds get a deterministic
  tool-invariant (A3 pre-checks, A4 sequencing), roughly one-third are policy + Stop-gate (A1
  authorization, A2 handoff).
- Combined with the first doc's ~44, the full program plausibly reaches the large majority of
  POLICY_REASONING — with the caveat that ~25–30 of these now rest on **policy + a structured catalog**,
  which are softer levers than the pure-arithmetic core.

**Re-test plan (multiple trials each, strict DB scoring):**
- Selection: 003, 044, 069, 071, 075
- Application handoff: 023, 063, 064
- Authorization: 043, 045
- Pre-check bundling: 043, 053
- Sequencing / branch: 053, 054, 091, 092
