# Hindsight i1 trajectory analysis — gold vs run, step-by-step deviations

Per-task gold-vs-run trajectory comparison for the 5 i1 banking_knowledge tasks, for
**two configurations on the Hindsight-backed retrieval (consolidated `tau2-banking-register`
bank, 3565 facts)**:

- **PLAIN** — `hindsight` variant, plain prompt, 1 trial
  (`data/simulations/hs_task_*` / `hs_smoke_064`).
- **FIX4** — `hindsight` variant + `claudedocs/i1_fixes/fix4_pointed.txt`, 1 trial
  (`data/simulations/hs_fix4_task_*`).

Agent `claude-opus-4-8`, SDK user-sim opus-4-8/high, `--sdk-nl-judge`. Sequences resolve
discoverable wrappers (`unlock:`/`call:`/`give:`) to their real target tool and surface the
state-changing arguments (`account_class`, `card_type`, …). Always-on reads (`KB_search`,
`get_user_information`, `get_current_time`) are collapsed; discoverable audit calls are kept
(they are hash-relevant in this domain). Both runs scored **strict 0 and verified FAIL**
except plain-064 (strict+verified PASS).

## Headline

| task | PLAIN (no fix4) | FIX4 | nature of deviation |
|---|---|---|---|
| 047 | skipped entire closure protocol (4 required checks/logs) | skipped protocol; substituted "give the user closure tools" | **under-action / wrong approach** |
| 058 | wrong savings tier (Gold≠Silver); card ✓ | wrong savings tier (Gold≠Silver); card ✓ | **selection** (identical both runs) |
| 063 | never opened the account; card ✓ | opened, but wrong tier + wrong card | **under-action → selection** |
| 064 | **PASS** (card ✓, tier ✓) | wrong card (EcoCard≠Gold Rewards); tier ✓ | **selection (regressed)** |
| 067 | wrong card (Diamond Elite≠Platinum Rewards); accounts ✓, close ✓ | wrong card + both accounts wrong | **selection** |

**The dominant failure in both runs is product/tier selection**, not retrieval and (with
fix4) not under-action. fix4 fixed under-action (063 now opens; the agent acts) but traded
it for selection errors and **regressed 064** (a clean pass → wrong card). 047 is the
structural outlier — a closure-protocol/under-action failure in both.

What fix4 changed, head to head:
- **063**: PLAIN never opened the account → FIX4 opens it (procedure fixed) but picks the
  wrong tier *and* wrong card.
- **064**: PLAIN picked both correctly (PASS) → FIX4 flipped the card to EcoCard (regression).
- **067**: PLAIN opened both correct accounts → FIX4 opened two wrong accounts.
- **058**: identical wrong-tier pick in both.
- **047**: both skip the required eligibility checks; fix4 additionally takes a wrong
  "delegate closure to the user" path.

---

## task_047 — credit-card retention / closure protocol

**Gold (15 steps):** verify → check dispute history → check pending replacement orders →
check closure-reason history → log closure reason (`found_better_card`) → *user applies for
Business Platinum* → re-check pending → re-check closure-reason → log closure reason
(`annual_fee`) → apply statement credit (`retention_offer`).

```
PLAIN agent:                              FIX4 agent:
1 log_verification              ✓         1 log_verification                    ✓
2 (user) apply Business Platinum ✓        2 (user) apply Business Platinum      ✓
3 apply_statement_credit         ✓        3 give:close_credit_card_account   ✗ wrong approach
  (skips ALL 4 eligibility          ✗     4 give:close_account               ✗  (tries to hand
   checks + both closure-reason          5 give:submit_account_closure_req   ✗   the customer
   logs)                                 6 apply_statement_credit            ✓   self-service
                                            (skips ALL 4 checks + logs)    ✗     closure tools)
```
**Deviation (both):** right after verification the agent skips the entire required protocol
— `get_user_dispute_history`, `get_pending_replacement_orders`, `get_closure_reason_history`,
`log_credit_card_closure_reason`. PLAIN just applies the statement credit; FIX4 additionally
tries to *give the customer* closure tools. **Genuine under-action / wrong-procedure, not a
selection error.**

---

## task_058 — open savings + apply card  (should open **Silver** savings)

**Gold:** verify → *user applies EcoCard* → open `Silver Account` (savings).

```
PLAIN:                                    FIX4:
verify                          ✓         verify                              ✓
(user) apply EcoCard            ✓         (user) apply EcoCard                ✓
open account_class=Gold Account ✗         open account_class=Gold Account     ✗
```
**Deviation (identical in both):** opened **Gold Account**; gold = **Silver Account**. Card
correct. Single, identical wrong-tier pick — fix4 did not change it.

---

## task_063 — open savings + apply card  (should open **Silver Plus** + **Silver Rewards Card**)

**Gold:** verify → *user applies Silver Rewards Card* → open `Silver Plus Account` (savings).

```
PLAIN:                                    FIX4:
verify                          ✓         verify                              ✓
(user) apply Silver Rewards     ✓         open account=Gold Savings Account   ✗ wrong tier
— never opened the account      ✗         (user) apply Green Rewards Card     ✗ wrong card
  (under-action)
```
**Deviation:** PLAIN never opened the savings account at all (under-action; card was
correct). FIX4 *does* open it — fixing the under-action — but picks the **wrong tier**
(Gold Savings ≠ Silver Plus) **and the wrong card** (Green ≠ Silver Rewards).

---

## task_064 — open savings + apply card  (should open **Gold Plus** + **Gold Rewards Card**)

**Gold:** verify → *user applies Gold Rewards Card* → open `Gold Plus Account` (savings).

```
PLAIN (PASS):                             FIX4 (regressed):
verify                          ✓         verify                              ✓
open account=Gold Plus Account  ✓         open account=Gold Plus Account      ✓ (tier correct)
(user) apply Gold Rewards Card  ✓         (user) apply EcoCard                ✗ wrong card
= no deviation, PASS                      = wrong card
```
**Deviation:** PLAIN matched gold exactly (strict + verified PASS). **FIX4 regressed** — same
correct tier, but the card flipped to **EcoCard** (gold = Gold Rewards Card). A pure
selection regression introduced by the fix4 prompt.

---

## task_067 — open 2 accounts + apply card + close old checking

**Gold (9):** verify → get_all_user_accounts → open `Platinum Plus Account` (savings) + open
`Purple Account` (checking) → *user applies Platinum Rewards Card* → close `chk_rp65a7b3c4`.

```
PLAIN:                                          FIX4:
verify                                ✓         verify                                ✓
get_all_user_accounts                 ✓         get_all_user_accounts                 ✓
open Purple (checking)                ✓         open Blue Account (checking)          ✗ wrong
open Platinum Plus (savings)          ✓         open Platinum Savings (savings)       ✗ wrong
(user) apply Diamond Elite Card       ✗         (user) apply Gold Rewards Card        ✗ wrong card
close chk_rp65a7b3c4                  ✓         close chk_rp65a7b3c4                  ✓
```
**Deviation:** PLAIN got the structure, both accounts, the required read and the closure all
correct — **single deviation: wrong card** (Diamond Elite ≠ Platinum Rewards). FIX4 is
**worse**: same correct procedure but **all three product picks wrong** (Blue ≠ Purple,
Platinum Savings ≠ Platinum Plus, Gold Rewards ≠ Platinum Rewards).

---

## Conclusion

Across both configurations, **4 of 5 tasks fail on product/tier selection** (058, 063, 064,
067) and **047 fails on the closure protocol** (under-action). fix4 reliably fixes
*under-action* (the agent now executes the open/close it previously skipped) but **does not
fix — and can worsen — selection**: it regressed 064 from a pass and turned 067's correct
accounts into wrong ones. Selection is stochastic and prompt-sensitive (the i1 doc reached
5/5 verified only with best-of-2).

Because the failure is selection rather than retrieval *reach*, the open question is whether
the `KB_search` results the agent saw actually contained the facts needed to pick correctly
(e.g. for 058: that **Silver** is the right savings tier given the customer's stated
criteria / net-APY). That analysis follows in the next section.

---

## Did `KB_search` surface the facts needed to pick correctly?  (worked example: 058)

**Short answer: no.** For task 058 the single decisive fact was *never retrievable from the
bank*, in either run — Hindsight's fact extraction/consolidation **dropped and garbled the
dense per-tier credit-card-APY-bonus tables** that product selection depends on. The agent's
wrong pick was *rational given what it could retrieve.*

### The decision (ground truth)
Customer Taylor Brooks: $20,000, 1 year, **maximize net return = interest − card annual
fee**, correct card = EcoCard, will not open a new checking account. Balance ≥ $10k clears
both tiers. From the source corpus:

| combo | base APY | EcoCard APY bonus | total | interest on $20k |
|---|---|---|---|---|
| **Silver Account + EcoCard** (gold) | 4.0% | **+2.2%** | **6.2%** | **~$1,240** |
| Gold Account + EcoCard (agent pick) | 5.5% | +0.6% | 6.1% | ~$1,220 |

Silver wins **only** because `doc_savings_accounts_silver_account` lists **`EcoCard: +2.2%`**
(vs `EcoCard: +0.6%` on Gold). That one number decides the task.

### What the agent actually retrieved
The agent issued **28 `KB_search` queries** on 058 (thrashing), and across ~87 KB of
retrieved text:
- `'2.2%'` appeared **0 times** (PLAIN run: also 0).
- It retrieved the base APYs prominently — *"Gold Account earns an APY of 5.5%"* (a `world`
  fact) and *"Silver Account … 2.5% / 4.0%"* — which make **Gold look strictly better**.
- For EcoCard it got only garbled fragments: *"EcoCard holders receive a 0.5%"*, *"bonus for
  EcoCard holders, totaling 4.75%"*, *"…EcoCard, +0.1%"* — never the real +2.2% on Silver.
- The **Silver Account's own per-card bonus table never surfaced.**

### The fact is in the corpus but not in the bank
`grep` confirms `EcoCard: +2.2%` is verbatim in `doc_savings_accounts_silver_account.json`.
But three *targeted, high-budget* recalls ("EcoCard APY bonus on Silver Account", …) each
returned ~120 facts and **none** contained it. Instead the bank returns:
- two **contradictory** consolidated "Silver **Plus** Account" bonus lists (different numbers
  in each), and a "Gold Account holders" list — i.e. consolidation **conflated the
  Silver / Silver Plus / Gold per-card bonus tables** and lost the precise values;
- for "Silver Account card bonuses" it returns only the base-APY facts (2.5% / 4.0%) — the
  per-card bonus table for the plain Silver Account is simply **absent**.

### Conclusion
The 058 selection failure is **retrieval-bound under Hindsight**: LLM-based fact extraction
on dense, near-duplicate numeric tables (Silver vs Silver Plus vs Gold; eight cards each)
dropped/merged the decisive cells. The agent could not have picked Silver — the fact that
makes Silver correct was not recallable. This is the *"loses procedural precision"* risk of
extractive memory flagged at the start of this effort, and it very likely drives the other
selection misses too (063 tier+card, 064 card, 067 card) since they depend on the same
garbled bonus/eligibility tables.

**Implication:** for tau2-banking's selection tasks, Hindsight's extract-then-recall is a
*downgrade* from raw-document retrieval (grep/BM25/`alltools` over intact docs), where the
agent can read the Silver Account's bonus table cell-for-cell. Hindsight's strength (linking,
contradiction surfacing, concise facts) does not compensate for losing exact tabular values
that the grader checks. Candidate fixes if pursuing Hindsight here: ingest each per-tier
bonus table as an atomic non-summarized chunk (disable fact-extraction for those docs / use a
verbatim retain mode), or surface `recall(include_chunks=True)` source chunks preferentially
over synthesized facts for numeric lookups.

---

## How hard is the 058 selection *even with raw docs*?  (multi-doc + calculation)

Determining **Silver > Gold** is not a lookup. The answer is stated in **no single
document** — it must be assembled from cells in *different tables across multiple docs* and
then computed. This holds independent of retrieval tech (assume intact raw docs).

### Minimal chain — just Silver vs Gold, holding EcoCard fixed

| term | value | source doc / location |
|---|---|---|
| Silver base APY @ $20k | 4.0% (≥ $10k tier) | `silver_account` → balance-tier table (pick the tier from the $20k balance) |
| **EcoCard bonus on Silver** | **+2.2%** | `silver_account` → *separate* "credit card APY bonuses" table |
| Gold base APY @ $20k | 5.5% | `gold_account` → APY / min-balance table |
| **EcoCard bonus on Gold** | **+0.6%** | `gold_account` → *separate* card-bonus table |
| EcoCard annual fee | $50 | `ecocard` doc (cancels in the 2-way compare; needed for full net) |

Calculation:
- Silver effective APY = 4.0 + 2.2 = **6.2%** → ×$20,000 = **$1,240**
- Gold effective APY = 5.5 + 0.6 = **6.1%** → ×$20,000 = **$1,220**
- → **Silver wins by ~$20/yr.**

So even the narrow comparison needs **2 account docs** (each contributing two cells from two
*different* tables) **+ 1 card doc**, a per-account **tier selection** ($20k → which APY row),
and a **summation** (base + card-specific bonus). Retrieve-the-right-cells → add → compare.

### The trap: the most salient fact points the wrong way
**Base APY alone says Gold (5.5%) > Silver (4.0%).** The ranking only flips after pulling the
EcoCard row from a *second table in each doc* and adding it. An agent that anchors on the
obvious "Gold has the higher rate" gets it wrong — which is exactly why selection is
fragile/stochastic in the i1 results even on raw-doc retrieval.

### It is actually an argmax over a cross-product
The customer asked for the **best combination**, and the corpus has **~10 personal savings
tiers × 16 cards**. Proving Silver+EcoCard is *optimal* (not just beating Gold) is an argmax
over that grid — each combo a multi-term APY sum (base + card-bonus + **eligibility-gated**
linked-checking and 0.025% relationship bonuses; note Gold's relationship bonus requires a
*Gold Rewards Card*, so it is $0 with EcoCard) minus the card's annual fee. The Silver doc
even contains a `[[linked_checking_apy_bonus]]` **template variable** whose value must be
resolved from elsewhere — another hop.

### Key distinction: raw docs make it *possible*; Hindsight makes it *impossible*
- **Raw docs**: every decisive cell is present and readable. The task is *possible* — a
  failure is a **reasoning/synthesis** failure (didn't run the full calc, anchored on base
  APY). Hard, multi-hop, arithmetic-on-retrieved-facts — but solvable.
- **Hindsight**: the decisive cell (`EcoCard +2.2% on Silver`) is **destroyed** by
  extraction/consolidation, so the task is *unsolvable* regardless of agent reasoning — the
  required input is not recallable.

Net: Hindsight does not merely make a hard task harder; for this class of selection task it
removes the one input that makes the correct answer derivable at all.
