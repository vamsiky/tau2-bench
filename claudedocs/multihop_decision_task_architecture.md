# Handling hard multi-hop decision tasks (banking_knowledge) — design notes

**Status:** design / discussion document for later review. Not implemented.
**Companion evidence:** [`hindsight_i1_trajectory_analysis.md`](./hindsight_i1_trajectory_analysis.md)
(per-task gold-vs-run deviations + proof that the decisive fact for task 058 is unrecallable
from the Hindsight bank), [`i1_fix_validation.md`](./i1_fix_validation.md) (prompt-only fix
iterations and the verified-scorer rationale).

This file captures *how to architect an agent* to handle the hardest banking_knowledge tasks
— the "selection / optimization" class (058, 063, 064, parts of 067) and the
"required-procedure" class (047) — and why the obvious fix (hand-build a deterministic tool
per use case) is the one option in the design space that does **not** scale.

---

## 1. The problem class

Several i1 tasks are not lookups; they are **retrieve → compute → compare** decisions over
data spread across many documents, where the most salient single fact points the *wrong* way.

### Worked example — task 058 (maximize net savings yield)
Customer: $20,000 for 1 year, **maximize net = interest − card annual fee**, has a checking
account, will not open another. Correct answer (gold): **Silver Account + EcoCard**. Agent
picked **Gold Account** (both plain-hindsight and fix4 runs).

The decision is decided by one cell that lives in a *second table inside each account doc*:

| combo | base APY @ $20k | EcoCard APY bonus | effective | interest |
|---|---|---|---|---|
| **Silver + EcoCard** (gold) | 4.0% | **+2.2%** | **6.2%** | ~$1,240 |
| Gold + EcoCard (agent) | 5.5% | +0.6% | 6.1% | ~$1,220 |

**Base APY alone says Gold (5.5% > 4.0%) — a trap.** The ranking only flips after adding the
card-specific bonus from a different table, in a different document, per candidate. Proving
Silver+EcoCard is *globally* optimal is an argmax over ~10 personal savings tiers × 16 cards,
each combo a multi-term sum (base + card bonus + eligibility-gated linked-checking and 0.025%
relationship bonuses) minus the card fee. One term (`[[linked_checking_apy_bonus]]`) is even a
template variable resolved from elsewhere.

### Three independent failure axes
A single "tool" tries to fix all three at once, which is exactly why it doesn't scale:

1. **Retrieval fidelity** — the exact cells (base APY by balance tier, card bonus, fee,
   eligibility) must arrive intact. *Hindsight's LLM extraction destroyed the `EcoCard +2.2%
   on Silver` cell entirely (verified: unrecallable even at high budget); raw docs preserve
   it.*
2. **Computation reliability** — base+bonus−fee then argmax over many candidates; LLMs are
   unreliable at multi-step arithmetic and silently drop candidates.
3. **Method knowledge** — the agent must know the *procedure* (enumerate eligible → sum the
   right terms → argmax) and that base-rate-alone is misleading.

### Task taxonomy (the patterns are few even though tasks vary)
| pattern | tasks | core difficulty |
|---|---|---|
| net-yield optimization over product combos | 058, 063, 064 | axes 1–3 above |
| open-before-close + selection | 067 | optimization **+** ordering rule |
| required-procedure / compliance protocol | 047 | not a calc — must execute mandated eligibility reads + logging, in order, before a mutation |

---

## 2. The reframe (why per-task tools don't scale)

A bespoke `compute_best_savings(...)` collapses all three axes into one hand-built artifact →
**O(tasks)** human engineering, brittle to policy changes, and it re-implements the business
logic the LLM was supposed to read. The instinct (computation must be **deterministic**) is
correct; the **granularity** (one tool per question) is the unscalable part.

**Principle:** keep the determinism, but push it into *general primitives*, and move the
*domain knowledge* into *retrievable structure / procedures*. Build **O(domain)**
infrastructure + **O(patterns)** playbooks, not **O(tasks)** tools.

---

## 3. The layered architecture

Each layer is general and built once; together they cover the long tail.

### Layer 1 — structured / semantic knowledge layer  *(highest leverage)*
The policy is inherently tabular (accounts × tiers × base-APY; accounts × cards × bonus;
cards × {fee, eligibility}). ETL the prose **once** into typed tables (or a small knowledge
graph). Then:
- retrieval is exact by construction — the Hindsight "which Silver? where's the EcoCard cell?"
  failure mode disappears;
- "best combo" becomes a **join + filter + argmax**, i.e. a query, not prose reasoning.

Vector RAG / extractive memory is simply the **wrong tool for numeric-decision data**.
- *Cost:* upfront ETL + keep-in-sync-with-policy + schema design.
- *Amortizes across every task touching the catalog. Doesn't cover genuinely unstructured/novel
  policy (keep Layer-2 retrieval for that).*

### Layer 2 — one general computation primitive (code execution)
A sandboxed code interpreter. The agent retrieves the numbers (ideally from Layer 1) and
*writes the formula*; the sandbox executes deterministically (Program-of-Thought). One tool
handles **all** arithmetic/argmax.
- *Rule:* an agent should never do a multi-candidate comparison in its head — route every
  numeric decision through code.
- *Cost:* sandbox/security; the agent can still write a wrong formula (→ Layer 4 still needed).

### Layer 3 — a small library of decision *patterns* (retrieved like policy)
Where "method knowledge" lives. Tasks are varied; decision **patterns** are not (~10 for this
domain). Author each once as a retrievable playbook, e.g.:
> **net-yield optimization:** enumerate *eligible* candidates → effective rate = base +
> card-specific bonus + gated relationship bonuses → net = rate×principal − fee → argmax.
> **Do not rank on base rate alone.**

That last clause defuses the 058 trap directly. **O(10) patterns, not O(tasks).**
- *Cost:* authoring + coverage gaps for novel decisions.

### Layer 4 — verification pass
Independent re-derivation of the chosen answer (second agent, or recompute-and-check) — the
SABER-style verify gate. Catches the residual rather than preventing it; cheap insurance on
the high-variance selection step.
- *Cost:* ~doubles cost on the verified step; catches but does not prevent errors.

---

## 4. The scalable form of "provide the tools": a self-growing, verified tool library

The unscalable part of the original idea is that a *human* pre-builds each tool. Let the
**system synthesize and cache** them (Voyager-style skill library):

1. First time the agent meets a net-yield task, it **writes** `net_return(account, card,
   balance)` from the retrieved policy.
2. A verifier checks it (unit-test against known cases, or LLM-judge the derivation).
3. It is **cached and reused**, improved on contradiction.

The library grows automatically, gated by verification — same determinism, without the
O(tasks) human cost. This is the concrete answer to "deterministic tools don't scale": make
the agent the tool-author and verification the quality gate.

---

## 5. Triage — when to *not* use the LLM at all

Sometimes the bespoke deterministic path *is* right, and "more agent" is the mistake. Triage
by **value × frequency × specifiability**:
- **High value, high volume, fully specified** (the fee/APY math): just **code it**. An LLM
  re-deriving a deterministic calculation every call is slower, costlier, riskier. A rules
  engine with an LLM front-end is a good architecture.
- **The long tail** (novel, ambiguous, rare): high-fidelity retrieval + code + verification +
  human escalation on low confidence.

A cheap **router** at the front decides which bucket a query is in. "Best agent" ≠ "reasons
everything from scratch"; it is one that knows when to call a deterministic path.

---

## 6. Solution mapping for the i1 tasks

| task(s) | bucket | recommended handling |
|---|---|---|
| 058, 063, 064 | selection / optimization | Layer 1 catalog + Layer 2 code + "net-yield" pattern (Layer 3); verify (Layer 4). No per-task tool. |
| 067 | optimization + ordering | same selection machinery + an "open-before-close" rule pattern. |
| 047 | required-procedure | **not** a calc: retrievable closure checklist + a pre-mutation **gate** that blocks the close until the mandated eligibility reads + closure-reason logging are done, in order. |

The taxonomy itself is a useful diagnostic: 047 failing on *procedure* while 058/063/064 fail
on *selection* means they need different machinery, and no single prompt or tool fixes both.

---

## 7. Benchmark vs deployment caveat

tau2's toolset is **fixed** — you cannot add Layers 1–2 inside the eval. There the only levers
are retrieval quality, prompt/decision patterns, and post-hoc verification (the verified
scorer). The architecture here is the answer for a **real deployment**; within the benchmark
it mainly explains *why* prompt-only fixes plateau (you can't add determinism where the task
needs it) and why the Hindsight retrieval *regressed* selection (it removed the one input the
answer depends on).

---

## 8. Unifying principle & suggested first prototype

Every scalable answer is the same move: **shift work from inference-time to build-time and
amortize it.**

| approach | build cost | per-new-task cost | reliability |
|---|---|---|---|
| per-task deterministic tool | O(tasks) | O(1) human | high but unscalable |
| pure LLM reasoning over raw docs | O(0) | O(0) | low (axes 1–3) |
| **structured catalog + code primitive + ~10 patterns + verifier + self-grown cache** | **O(domain)** | **~O(1) per task *type*** → ~0 as cache fills | high |

There is no silver bullet — a reasoning+retrieval fallback and a verifier remain necessary for
the true tail. The portfolio is what scales; "one carefully-built tool per use case" is the
single option in it that doesn't.

**Cheapest high-signal prototype to validate the thesis:** for the savings/card subset only,
hand-build the Layer-1 catalog (a few typed tables) + expose a `query_catalog` + `code_exec`
pair + the one net-yield pattern, and re-run 058/063/064. Expected outcome if the thesis
holds: the decisive cells become available and the picks become correct and *deterministic*
(no best-of-N variance), in contrast to both the Hindsight runs (cell destroyed → impossible)
and the raw-doc prompt-only runs (cell present → possible but stochastic).
