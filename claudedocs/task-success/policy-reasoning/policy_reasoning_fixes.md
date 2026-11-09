# POLICY_REASONING — candidate fixes per issue, and an empirical test

Companion to [`policy_reasoning_validation.md`](policy_reasoning_validation.md), which
confirmed all four issues reproduce (8/8 trials). This document proposes fixes for **each**
issue across every layer (prompt, retrieval, harness/gate, forced user-confirmation,
pre-mutation policy revalidation), then tests concrete candidates.

The four issues share one root cause: the agent commits a **derived argument** (a computed
number, a count under a cap, a classification enum, or a multi-constraint product choice)
to a WRITE without re-checking it against the policy at the moment of the write. So the
fixes cluster into a few cross-cutting mechanisms, applied per issue below.

---

## Fix levers (what each layer can do)

| Layer | Mechanism | Strength | Weakness |
|---|---|---|---|
| **Prompt** | Append a mandatory pre-mutation "re-derive + confirm" protocol to the agent instruction (generic). | Cheap, no code, addresses all four facets. | Advisory — a strong model may still skip it; fragile across wording (seen in I1 work). |
| **Harness / gate** | SABER-style aux-verifier (`--use-aux-verifier`): a PreToolUse gate that re-reads policy and BLOCKS a WRITE discoverable call with feedback. Enhanced here to also check computed numbers, count/caps, and classification enums. | Deterministic interception; model-agnostic; gives corrective feedback. | Only gates `call_discoverable_agent_tool` WRITEs — **misses user-tool writes** (e.g. `apply_for_credit_card` in task_003); adds latency + a second model. |
| **Retrieval** | Force the relevant policy section (rate table, dispute-type definitions, provisional-cap rule) into context at decision time; or have the gate inject it. | Removes "never saw the rule" failures. | These failures are mostly mis-*application*, not mis-retrieval, so retrieval alone is a partial fix. |
| **Forced user confirmation** | Require the agent to state the exact action + key values and get user agreement before the write (realised through the tau2 simulated user). | Catches wrong product/category the user can veto. | User-sim may rubber-stamp; doesn't catch silent arithmetic errors the user can't check. |
| **Benchmark-side** | (From I1 work) relax hash on free-text/audit rows. | — | **Not applicable here** — these are genuine wrong values, not grader artifacts. |

---

## Per-issue fixes

### task_003 — wrong card selection (recommends Gold/premium vs gold's *Silver Rewards Card*)
Customer stated constraints (travel, no FX fees, purchase protection, $100k limit) map to a
specific card; the agent anchors on a higher tier.
- **Primary (prompt + user-confirm):** enumerate eligible cards, score each against *every*
  stated constraint, pick the policy-designated fit, and confirm the named card + the reason
  it meets each constraint with the customer before the application is submitted.
- **Retrieval:** ensure the full card-comparison/eligibility table is retrieved before
  recommending (not just the premium card's doc the agent anchored on).
- **Harness caveat:** `apply_for_credit_card` is a **user** tool, so the aux-verifier gate
  does **not** intercept it — the only leverage here is the agent's recommendation. This
  makes 003 the hardest for the gate-based fix and a good test of the prompt/user-confirm path.

### task_039 — provisional-credit cap miscount (gold: 3 of 8 eligible; agent 2 or 4)
- **Primary (gate, enhanced):** the aux-verifier counts how many disputes carry
  `eligible_for_provisional_credit=true` across this + prior calls, subtracts any consumed by
  `get_user_dispute_history`, and BLOCKS a filing that exceeds the cap or flags the wrong items.
- **Prompt:** force an explicit "count eligible, subtract prior, select top-N" derivation
  before filing.
- **Pre-check dependency:** require `get_user_dispute_history_7291` before filing (a prior
  dispute consumes a slot) — already a gate rule pattern; the count is the new check.

### task_086 — fraud misclassification (gold: `card_present_fraud`/`pin_purchase`; agent got category right but `transaction_type=signature_purchase`)
- **Primary (gate, enhanced):** classification check — map the transaction's facts (PIN
  entered, card physically present, in-person) to the policy enum and BLOCK a mismatched
  `transaction_type`/`dispute_category`.
- **Prompt:** require restating the concrete facts → enum mapping before filing.
- **Retrieval:** surface the dispute-type definition table at filing time.

### task_095 — APY over-stack (gold: `$98`/`6.85%`; agent `6.875%`, over-credits $100/$112.5)
- **Primary (gate, enhanced):** numeric check — re-derive the APY from the policy's rate
  components, reject an extra/stacked bonus the policy doesn't list, and BLOCK if the
  credited `amount`/`expected_apy` don't match the derivation. Deterministic arithmetic, so
  the most gate-tractable.
- **Prompt:** force step-by-step recomputation showing which bonuses the policy permits.

---

## What is being tested empirically (sonnet agent, 1 trial/task, parallel)

Three conditions, identical except the fix, on the **sonnet** agent (per request), strict DB
scoring, user-sim + judge `opus-4-8/high`, retrieval `alltools`:

- **A — baseline:** sonnet, no fix. Establishes the sonnet reference (the documented numbers
  were opus-4.7, so we need a same-model baseline to attribute any change to the fix).
- **B — prompt-fix:** + `policy_fixes/fix_premutation_revalidation.txt` (generic re-derive +
  user-confirm protocol). Tests the prompt/user-confirm layer; the only lever for task_003.
- **C — aux-verifier (enhanced):** + `--use-aux-verifier` with the value-correctness checks
  added to the gate (numbers / count-caps / classification). Tests the harness layer;
  expected to help 039/086/095 but **not** 003 (user-tool write, ungated).

Run dirs: `data/simulations/fix_{base,prompt,aux}_task_{003,039,086,095}/`.

## Results (sonnet agent, 1 trial/task, strict DB scoring)

All 12 runs in `data/simulations/fix_{base,prompt,aux}_task_*/`. `r=` is strict reward.

| Task | A — baseline (sonnet) | B — prompt-fix | C — aux-verifier (enhanced) |
|---|---|---|---|
| **003** card select | Platinum Rewards (wrong) · r0 | Gold Rewards (wrong) · r0 | Gold Rewards (wrong) · r0 |
| **039** prov-cap | 8 disputes, **4** eligible (over-cap) · r0 | 8 disputes, **4** eligible (over-cap) · r0 | **no disputes filed** (incomplete) · r0 |
| **086** fraud class | `signature_purchase` (wrong) · r0 | `signature_purchase` (wrong) · r0 | `signature_purchase` (wrong) · r0 |
| **095** APY/amount | amount **110.06** (wrong), apy 6.85 · r0 | **amount 98.0, apy 6.85 → r1.0 ✅ PASS** (`db_match=True`) | amount **89** (wrong), apy 6.85 · r0 |

**One verified fix: prompt-fix resolves task_095** — strict DB pass (`reward=1.0,
db_match=True`). The mandatory "re-derive the number from scratch before the write" step made
sonnet credit the correct `$98.00` where baseline credited `$110.06`. The
deterministic-arithmetic issue is the one the prompt layer fixes cleanly.

### The prompt is domain-generic, and the 095 fix survives genericity (2/5 trials)

The first version of `fix_premutation_revalidation.txt` leaked banking nouns (APY, disputes,
provisional credit, PIN, card/account). It was rewritten to state the principle generically —
"records", "computed/counted/classified values", "category/type/reason/status enums",
"options/requirements" — so the same harness augmentation applies to retail/airline/telecom
unchanged. Re-validated on task_095 across **5 trials** (sonnet):

| trial | credited amount | strict result |
|---|---|---|
| t0, t2 | **$98.00** | ✅ PASS (`db_match=True`) |
| orig, t1, t3 | $107.43 / $81.55 / $91.82 | ✗ |

**Pass rate 2/5 (40%).** Genericity did **not** break the fix — the generic prompt still
drives the correct `$98.00` computation and a strict pass. The result is **stochastic**: when
sonnet does the arithmetic correctly it lands exactly on the gold value and passes; otherwise
it drifts to a nearby wrong amount (the APY itself, 6.85, was correct in every trial — the
unstable step is the derived dollar amount). The earlier banking-specific prompt's single pass
was one draw from this same noisy distribution; there is no evidence the domain-specific
wording helped. For per-trial reliability this prompt would need pairing with a value-checking
gate (see recommendation 2) or best-of-N sampling.

### Reading the rest

- **task_003 (card selection) — unmoved by all three.** Baseline picked Platinum; both fixes
  picked Gold; gold is Silver Rewards. The prompt's "enumerate vs all constraints + confirm"
  step nudged the tier down (Platinum→Gold) but not to the right card. The aux-verifier
  **cannot** help here — `apply_for_credit_card` is a user tool, so the gate never sees it
  (0 blocks on 003, as predicted). Leverage for 003 is retrieval (surface the full
  card-comparison table) + the recommendation-side prompt, not the gate.

- **task_039 (provisional cap) — not fixed; aux regressed it.** Baseline/prompt both filed 8
  disputes with 4 provisional-eligible (the documented over-cap). Under the aux-verifier the
  agent never reached a successful dispute filing (1 pre-check block fired on an unrelated
  `order_replacement_credit_card`; the episode ended with no disputes written) — a
  completeness regression, not a fix. The cap-count check did not produce a corrective block.

- **task_086 (fraud classification) — unmoved.** `signature_purchase` (vs gold `pin_purchase`)
  in all three. The aux-verifier's classification check did not block it.

- **The enhanced aux-verifier produced essentially no value-correctness blocks** (003/086/095:
  zero; 039: one pre-check block). The gate *did* run on the WRITE calls (they are all
  `ToolType.WRITE`) but **approved the wrong values**. Two reasons, both fixable but beyond a
  prompt tweak: (1) the verifier only receives a 6000-char policy *excerpt*, which generally
  does **not** contain the specific rate table / cap rule / dispute-type definitions it would
  need to re-derive; (2) the verifier defaults to APPROVE on any uncertainty (by design, to
  avoid false blocks). So a value-checking gate needs **retrieval wired into the gate** (feed
  it the governing policy section for the proposed tool) and a compute-or-block posture —
  not just instructions to check.

## Recommendation (per layer, evidence-based)

1. **Ship the prompt re-derivation protocol** — it is cheap, generic, and produced a real
   strict pass (095). Best for computed-number errors.
2. **For 039/086, the gate is the right shape but under-powered as built.** Make it effective
   by (a) retrieving and injecting the *specific* policy section for the proposed WRITE into
   the verifier prompt (rate table / provisional-cap rule / dispute-type definitions), and
   (b) requiring the verifier to show the derivation and BLOCK on mismatch rather than
   default-approve. Tune to avoid the 039-style over-block (scope pre-check rules tightly).
3. **For 003, add a retrieval + recommendation fix** (full card-comparison table in context;
   confirm the named card against each constraint). The gate can't reach a user-tool write.
4. **These are not grader artifacts** — unlike several I1/INCOMPLETE cases, every failure here
   is a genuine wrong value; no scorer relaxation recovers them, only better reasoning/gating.

*Caveat: 1 trial/task on sonnet (weaker than the documented opus-4.7). Single-trial results
carry sampling noise — the 095 pass is verified (db_match=True) but the negative results
(003/039/086) would benefit from more trials before declaring a fix ineffective. Directionally:
the prompt layer fixes arithmetic; the gate needs retrieval to fix counts/classes; selection
(003) needs retrieval + recommendation-side help.*
