# Does the deterministic path fix the majority of POLICY_REASONING failures?

Validation of the proposal in [`policy_reasoning_fixes.md`](policy_reasoning_fixes.md) — "move the
rules/computations out of the LLM and into deterministic code" — against **every** POLICY_REASONING
trial in [`opus47_banking_failure_evidence_table.md`](opus47_banking_failure_evidence_table.md).

## Bottom line

**No.** The deterministic path cleanly addresses a coherent **~36% slice** (~44 of 121 primary
POLICY_REASONING trials), and that slice is exactly the most mechanically deterministic part:
cap-counting, arithmetic, transaction-set audits, and crisp fact→enum classification. But the two
largest buckets — **MISSING_WRITE (32)** and **PRODUCT_SELECTION (30)**, together **51%** — are
structurally outside what "move the rule/computation into code" can reach.

## Two claims that must be kept separate

The proposal conflates two very different interventions:

1. **What was empirically tested** in `policy_reasoning_fixes.md` was an **LLM aux-verifier gate**
   (SABER), not deterministic code. It produced **zero value-correctness blocks** across tasks
   003/039/086/095. The only pass (095) came from the **prompt** re-derivation step, and only
   stochastically (2/5 trials). So the *gate* form of this idea is already shown to fix almost nothing.

2. **What "deterministic path" actually means** — hard-coding the real rules (cap = 3, "relationship
   bonuses don't stack", per-transaction reward audit) as genuine code, enforced as **tool/state
   invariants** — is the proposal's stronger form and is **empirically unvalidated**. The tractability
   assessment below is analytical, and it is contingent on actually implementing those invariants in
   the environment (a bigger lift than a PreToolUse gate).

The LLM aux-verifier failed precisely *because* its checks were never deterministic: it received a
6000-char policy *excerpt* (which generally did not contain the specific rate table / cap rule /
dispute-type definitions) and defaults to APPROVE on uncertainty. Real determinism requires the rule
in code, not an instruction to a second model.

## Method

Every row in the evidence table whose Category contains POLICY_REASONING was extracted and classified
by the **type of derived argument** that was wrong (121 primary rows + 14 secondary). Each type was
then judged for whether a deterministic rule/computation could compute or block the wrong value, given
that the failure's residual LLM step (fact/constraint extraction) must still happen.

## Per-bucket validation (121 primary trials)

| Derived-arg type | Trials | Deterministic-tractable? | Why / mechanism required |
|---|---:|---|---|
| **MISSING_WRITE** | 32 | ❌ No | Agent never called the write — there is no value to compute or block. Needs authorization/completion enforcement (I1/I2), not a rule-in-code. |
| **PRODUCT_SELECTION** | 30 | ⚠️ Weak / unproven | Terminal write `apply_for_credit_card` is a **user tool** → no agent-side gate can intercept it. A deterministic scorer needs a full structured catalog **and** correct LLM constraint-extraction — the exact step that failed task_003 under all 3 tested conditions. |
| **COUNT_UNDER_CAP** | 19 | ✅ Strong | Cap = `3 − priors` is pure counting. Fix is a **tool invariant** that rejects >N eligible flags and owns top-N-by-value selection. (Over-count cleanly fixed; right-count/wrong-items needs the ranking in-tool too.) |
| **COMPUTED_NUMBER** | 19 | ✅ Strong (~15) | Arithmetic + encoded rules (no-stacking, fee-netting) via a calculator/code-exec tool. Residual risk = input extraction. ~4 here (e.g. task_045) are actually MISSING_WRITE mis-bucketed. |
| **SET_SELECTION** | 6 | ✅ Strong | The "right set" = every txn whose actual reward ≠ rate-table expectation. A deterministic per-txn reward-audit tool produces the exact gold set; the agent failed doing it by hand. |
| **CLASSIFICATION_ENUM** | 8 | ◐ Half | Fraud type (086: PIN+present → `pin_purchase`) is a crisp tree, deterministic once facts are structured. Transfer-reason enums (004/008) are fuzzy situation→label mappings, far less crisp. |
| **OTHER** | 7 | ? Uncertain | Mixed. |

**Tractable: ~44 trials** (COUNT 19 + COMPUTE ~15 + SET 6 + crisp-ENUM ~4).
**Not tractable: ~69 trials** (MISSING_WRITE 32 + PRODUCT 30 + OTHER 7).

## The two structural blockers that sink the majority

### 1. MISSING_WRITE (32) is not a value problem

The agent reasoned correctly and then *declined or forgot to act* ("I can't do that through this
channel" → defers to the user), so the DB write never happened (e.g. task_010 never re-submits the
referral; task_023 never calls `apply_for_credit_card`; task_044 closes the account instead of applying
for Platinum). A deterministic value-checker has nothing to inspect. These need the **I1 authorization
fix** (state in policy that the agent *is* authorized to perform the write) or a deterministic
**completion gate** (I2 "definition of done") — a different mechanism from "move the computation into
code," and one this experiment never tested.

### 2. PRODUCT_SELECTION (30) is gate-blind

`apply_for_credit_card` is defined in `KnowledgeUserTools` (`src/tau2/domains/banking_knowledge/tools.py:4325`),
i.e. it is a **user tool**. The SABER aux-verifier only intercepts the agent's
`call_discoverable_agent_tool` WRITEs, so it provably cannot see the card application — the doc's own
task_003 run logged **0 blocks**. A deterministic decision-table *could* exist, but it requires building
a structured product catalog and still leans on the LLM to extract the customer's constraints — the
step that kept the agent anchoring on premium tiers (Platinum/Diamond) in *every* tested condition
(baseline, prompt, aux-verifier). This is also the single biggest bucket in the table author's own
P-taxonomy (P2 ≈ 87 trials across the full set).

## What the deterministic path genuinely buys you

A focused, high-confidence win on the **crisp-rule buckets** — and the key is implementing them as
**tool/environment invariants**, not as a second LLM verifier:

- **Cap enforcement (COUNT_UNDER_CAP, ~19):** make the dispute-filing tool return the remaining
  provisional allowance and reject over-cap flags; have it own the top-N-by-value selection so the agent
  cannot pick the wrong N or the wrong items within N.
- **Reward audit (SET_SELECTION + COMPUTED_NUMBER, ~21):** a deterministic "expected vs actual reward
  per transaction" function. This single tool addresses both the set-selection and the arithmetic
  buckets — the cleanest ROI in the whole analysis.
- **Fraud decision tree (crisp CLASSIFICATION_ENUM, ~4):** force the enum leaf from cited boolean facts
  (card present + PIN used → `card_present_fraud` / `pin_purchase`).

That is a coherent ~44-trial program, worth shipping — but it is a **strong minority, not a majority**.

## Recommendation

1. **Build the tool/state invariants for the tractable ~44-trial slice** (reward-audit + cap-enforcement
   first; they cover ~40 trials between them). Implement as real code in the tools, not as an LLM gate —
   the gate form is already shown to fix ~0.
2. **Do not expect this to move PRODUCT_SELECTION or MISSING_WRITE.** Those 62 trials (the actual
   majority) need orthogonal work: the I1 authorization/policy change for MISSING_WRITE, and a structured
   product catalog + constraint-matcher (callable as an *agent* tool so it is reachable) for
   PRODUCT_SELECTION.
3. **Re-test honestly.** The current empirical evidence only falsifies the LLM-aux-verifier form. Before
   claiming the deterministic path works, validate the actual code-level invariants on
   039/040/041 (cap), 018/020/022 (set), 072/073/074/094/095/097 (compute), and 086 (fraud) — multiple
   trials each, strict DB scoring.

## Caveats

- Bucket counts are from a single exhaustive pass over the table; ~4 COMPUTED_NUMBER rows (e.g. task_045)
  are arguably MISSING_WRITE, which would shift the tractable count slightly *down*.
- Tractability is analytical, not measured. "Strong" means the rule is crisp and few-lined; the residual
  risk in every ✅ bucket is the LLM still having to extract structured inputs (which tier, which facts) —
  if that extraction is wrong, the deterministic function computes the wrong answer correctly.
