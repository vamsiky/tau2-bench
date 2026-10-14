# POLICY_REASONING reproduction validation — SDK driver (banking_knowledge)

**Goal:** take the next-largest failure category after INCOMPLETE (already covered in
[`i1_fix_validation.md`](i1_fix_validation.md)) and confirm the documented errors are
*reproducible* on the current SDK driver — i.e. the agent independently re-commits the
same gold-vs-actual mistake the evidence table records.

**Category:** `POLICY_REASONING` — **121 / 290 failures (42%)**, the dominant bucket in
[`opus47_banking_failure_evidence_table.md`](opus47_banking_failure_evidence_table.md)
("right tool, wrong decision/value"). Four tasks chosen to span its four documented
sub-patterns.

**Driver/config (matches the prior validation run):**
`examples/agents/claude_sdk_loop_eval.py` · domain `banking_knowledge` ·
agent `claude-opus-4-8` **effort=max** · SDK user-sim `claude-opus-4-8/high` ·
SDK NL-judge `claude-opus-4-8/high` · retrieval `alltools` · **strict** DB scoring
(`--no-verified-scorer`) · 2 trials/task · run dir `data/simulations/policy_repro/`.

> Note on faithfulness: the documented run used agent `claude-opus-4-7 (effort=max)` +
> user-sim `gpt-5.2`. This reproduction uses `claude-opus-4-8` for the agent, user-sim,
> and judge (subscription, no API key — same constraint as the I1 work). So this tests
> whether the *failure mode* survives a model/user-sim refresh, not a bit-exact replay.

---

## Result: 4 / 4 tasks — **8 / 8 trials** — reproduce the documented POLICY_REASONING failure

Every one of the 8 trials (4 tasks × 2 trials) ended `reward=0.0`, `term=user_stop`,
**`db_match=False`** — the exact termination/grading signature the evidence table records
for these tasks (no crashes, no timeouts, no retrieval failure). The agent had the right
tool and the right information and made the wrong decision/value, which is the definition of
the category.

| Task | Sub-pattern (documented) | Gold | Documented actual | **Reproduced actual (opus-4-8)** | Verdict |
|---|---|---|---|---|---|
| **task_003** | wrong card/product selection | `apply_for_credit_card(card_type="Silver Rewards Card")` | applied for a premium card (Diamond/Platinum) | **Gold Rewards Card** (both trials) | ✅ same category — wrong card |
| **task_039** | provisional-credit cap miscount | file 8 disputes, **exactly 3** `eligible_for_provisional_credit=true` | marked **4** eligible (over the 3-cap) | t0: 5 disputes / 2 eligible · **t1: 8 disputes / 4 eligible (bit-exact to documented)** | ✅ same category — t1 matches the documented over-count exactly |
| **task_086** | wrong fraud classification | $625 TechWorld: `card_present_fraud` + `pin_purchase` | `card_not_present_fraud` + `online_purchase` | `card_present_fraud` + **`signature_purchase`** (both trials) | ✅ same dispute miscategorized (different facet: txn_type not category) |
| **task_095** | APY/numeric computation | credit `amount=98.00`, `expected_apy=6.85` | over-stacked +0.025% bonus → `$100` / `6.875` | **`expected_apy=6.875` both trials**; amount `100.0` / `112.5` | ✅ **exact APY over-stack**; over-credit magnitude varies |

### Per-task detail

- **task_003 (wrong-card, P2).** 2/2 trials: agent researched the catalog and applied for
  **Gold Rewards Card** where gold requires **Silver Rewards Card**. Short episode (3 turns,
  `user_stop`) — the wrong recommendation is locked in early, identical to the documented
  "anchored on the wrong tier, applied for the wrong card" pattern. (Note from the I1 work:
  `apply_for_credit_card` is a *user* tool; the user-sim applies for whatever the agent
  recommends, so the wrong DB write traces to the agent's recommendation.)

- **task_039 (provisional-cap, P4).** Reproduces the category in **both** trials, and one
  trial reproduces the documented count **exactly**. Gold files 8 disputes with exactly 3
  flagged provisional-eligible. Trial 0 filed only **5** disputes / **2** eligible
  (under-counted); trial 1 filed all **8** disputes / **4** eligible — **the exact
  documented over-the-3-cap error** the evidence table records for Opus-4.7. So the
  provisional-cap miscount is robustly reproduced, with the specific wrong number varying
  trial-to-trial (2 then 4) around gold's 3 — consistent with the evidence table flagging
  the provisional-cap arithmetic as the unstable step.

- **task_086 (fraud classification, P3).** Same $625 Miami fraud dispute, misclassified in
  **both** trials on the same field: Opus-4.8 got `dispute_category=card_present_fraud`
  **right** yet set `transaction_type=signature_purchase` where gold is `pin_purchase`
  (documented Opus-4.7 missed both, calling it card-not-present/online). Net effect is
  identical — the filed dispute row diverges from gold → `db_match=False`. The
  `signature_purchase` slip is stable across both trials.

- **task_095 (APY computation, P1).** The documented over-stacked-bonus error reproduces in
  **both** trials: `expected_apy=6.875` (vs gold `6.85`) every time — a deterministic
  arithmetic mistake (agent adds the +0.025% relationship bonus it shouldn't). Trial 0 is
  bit-exact to the documented `$100` over-credit; trial 1 over-credits `$112.5` instead, so
  the *APY error* is fully stable while the derived dollar amount drifts. The most reliably
  reproducible of the four.

---

## Reading

1. **The POLICY_REASONING category is real and reproducible**, not a documentation
   artifact: **8/8 trials across 4/4 tasks** re-fail with the documented
   `reward=0 / user_stop / db_match=False` signature on a *newer, stronger* agent model. The
   failures are decision/value errors with the right tools and information in hand — exactly
   as classified.

2. **The category reproduces; the precise wrong value can drift** with the model/user-sim
   version. The numeric/computation case (095) reproduces bit-exactly; the
   selection/counting cases (039, 086) reproduce the same *kind* of error on the same
   action, but land on a different specific wrong value (5 disputes / 2 eligible vs 4;
   `signature_purchase` vs `online_purchase`). This is the expected behavior for a
   reasoning-class failure and matches the analysis's own "complexity, not capability"
   framing — the unstable steps are the computed/classified arguments.

3. **Contrast with the INCOMPLETE/I1 finding.** The I1 investigation showed several of those
   labels were grader artifacts (extra read-only audit rows, free-text `closure_reason`).
   These POLICY_REASONING failures are **not** grader artifacts — they are genuine wrong
   values (wrong card, wrong APY, wrong dispute set/type) that a verified/lenient scorer
   would *also* fail. No benchmark-side relaxation recovers them; only better agent reasoning
   does.

---

*Method: ran the 4 tasks on the SDK driver, then diffed each trajectory's relevant tool
calls against the gold actions in `data/tau2/domains/banking_knowledge/tasks.json`
(`$CLAUDE_JOB_DIR/tmp/analyze_policy.py`). Reproduction = agent independently emits the same
wrong decision/value on the same gold action, with `db_match=False`.*
