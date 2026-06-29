# A1–A4 MISSING_WRITE fixes: implementation and validation (sonnet driver)

Implements and tests the four MISSING_WRITE fixes proposed in
[`policy_reasoning_missing_write_product_selection_fixes.md`](policy_reasoning_missing_write_product_selection_fixes.md)
against the `banking_knowledge` domain, with the **Claude Sonnet 4.6** agent driver
(`claude-sonnet-4-6`), user-sim + NL judge `claude-opus-4-8/high`, retrieval `alltools`.

- A1 — authorize the agent to use its own write tools.
- A2 — hand off customer-completed actions (apply / referral).
- A3 — bundle closure-eligibility checks into the retention/closure write (deterministic guard).
- A4 — enforce ordering / procedure selection (sequencing policy + a stored-signal PIN guard).

## TL;DR verdict

| Fix | Mechanism | Verdict on sonnet |
|---|---|---|
| **A3** | Deterministic tool guard | **Validated.** task_043 0.0→1.0; **guard-only run fired the guard and passed**; 4/4 unit checks. |
| **A4 (ordering)** | Policy instruction (env already enforces the constraint) | **Behaviorally validated.** task_053 baseline *denied* the CLI; fixed *approves CLI before dispute*. Full DB pass blocked by an orthogonal user-tool issue outside A1–A4. |
| **A4 (PIN procedure)** | Deterministic tool guard | **Mechanism validated (3/3 unit checks); inert in episode.** task_092 stays 0.0 because its binding signal (Green card) is *computed from transaction velocity, not stored* — deterministically unfixable. |
| **A1 / A2** | Policy instruction | **Do not reproduce on sonnet.** task_045, task_064 pass at baseline; task_063's application *succeeded* at baseline. The opus-4.7 refusals are capability-specific. |

The headline result: **A3 is a real, deterministically-proven win**; the rest is a mix of
behavioral validation, an honest deterministic limitation, and "the issue doesn't occur on a stronger
model."

## The environmental fact that reframes everything

All seven test tasks score on **`reward_basis: ["DB"]`** — reward is purely whether the agent's
terminal DB hash equals the gold-action-replayed DB hash. Crucially, the **set of discoverable tool
calls** (the `agent_discoverable_tools` table) is part of that hashed state. So:

- Missing a required gold **read** (e.g. `get_user_dispute_history_7291`) fails the task even though the
  read changes no business data — because the call-set table diverges from gold.
- The dominant *sonnet* failure is therefore "agent skipped a required discoverable call," not the
  opus-era "agent refused to act." Sonnet pays, closes, and instructs applications fine.

This was confirmed surgically: the **task_043 baseline failed for exactly one reason** — the DB diff
showed *only* the two missing read records:
```
## agent_discoverable_tools
  -GOLD  get_user_dispute_history_7291
  -GOLD  get_pending_replacement_orders_5765
```

## Changes made

### Code — `src/tau2/domains/banking_knowledge/tools.py` (+55 lines)
A3 and A4 implemented as **tool invariants**, using an in-memory call tracker (no DB pollution — a plain
instance attribute is never hashed):

- `__init__`: add `self._discoverable_calls_made: set`.
- `call_discoverable_agent_tool`: mirror every discoverable call into that set.
- `_closure_eligibility_block()`: helper returning an instructive error if
  `get_user_dispute_history_7291` or `get_pending_replacement_orders_5765` haven't been called.
- **A3 guards** (scoped to retention so non-retention paths are untouched):
  `apply_credit_card_account_flag_6147` when `flag_type=="annual_fee_waived"`, and
  `apply_statement_credit_8472` when `reason=="retention_offer"`, call the guard first.
- **A4 PIN guard**: `reset_debit_card_pin_6284` refuses when the card record has
  `fraud_alert_active is True` (→ close + reissue) or `pin_lock_reason=="security_hold"` (→ transfer).

These do not break gold-state computation: gold replays each task's discoverable reads *before* the
gated write (verified by the unit check and by task_043 passing), so the guard is satisfied during gold
replay. The unexercised `close_credit_card_account_7834` was intentionally **not** guarded (no test task
closes a card) to avoid an unvalidated regression; extending the same guard to it is a recommended
follow-up.

### Policy — `claudedocs/a1a4_fixes/`
- `policy_a1a4.txt` — A1 (authorization), A2 (apply/referral handoff), A4 (CLI-before-dispute order +
  PIN procedure), A3 (eligibility reads). Passed via `--agent-extra-instruction-file`.
- `policy_noA3.txt` — same minus the A3 section, used to isolate the deterministic A3 guard.
- `guard_unit_check.py` — direct, deterministic assertions of the A3/A4 guard logic.

## Methodology

Per task: **baseline** (original code, no policy file) vs **fixed** (modified tools + `policy_a1a4.txt`),
sonnet driver, 1 trial (a few tasks re-run for a 2nd trial). Plus two isolation controls:
- **guard-only** (modified tools + `policy_noA3.txt`) — isolates the A3 guard from the A3 prompt.
- **unit checks** — prove the guard logic independent of any LLM episode.

## Results

Reward = strict DB match (1.0 pass / 0.0 fail), verified scorer.

| task | fix targeted | base t1 | base t2 | fixed t1 | fixed t2 | guard-only | note |
|---|---|---|---|---|---|---|---|
| **043** | A3 | 0.0 | — | **1.0** | — | **1.0 (guard fired)** | Clean A3 win; sole baseline cause = 2 missing reads |
| 045 | A1 | 1.0 | — | — | — | — | Passes at baseline (sonnet pays) |
| 047 | A3/retention | 0.0 | 1.0 | 1.0 | 1.0 | — | Baseline **stochastic**; fixed 2/2 (used correct `apply_statement_credit`) |
| **053** | A4 order | 0.0 | — | 0.0 | 0.0 | — | A4 ordering fixed *behaviorally* (deny→approve-first); orthogonal user-tool blocker |
| 063 | A2 | 0.0 | 1.0 | 1.0 | 0.0 | — | Baseline **and** fixed both 1/2 — pure noise, no measurable fix effect |
| 064 | A2 | 1.0 | — | 1.0 | — | — | Passes at baseline (application succeeds) |
| **092** | A4 PIN | 0.0 | — | 0.0 | 0.0 | — | Binding signal (Green) is computed, not stored — unfixable deterministically |

**Guard unit checks: 7/7 PASS** (`uv run python claudedocs/a1a4_fixes/guard_unit_check.py`):
A3 blocks the flag and the retention credit before the reads, passes after, leaves non-retention credits
ungated; A4 blocks PIN reset on fraud-alert and security-hold cards, allows it on normal cards.

## Per-fix findings

### A3 — validated deterministically
task_043's baseline failed solely because sonnet skipped the two eligibility reads. With the guard, the
fixed run passed (1.0). The decisive evidence is the **guard-only** run (A3 prompt removed): the guard
**fired once** (`Closure-eligibility checks incomplete` observed), the agent then called both reads, and
the task **passed** — so the pass is attributable to the deterministic guard, not the prompt. The unit
check confirms the logic in isolation. This is the cleanest result and the strongest evidence in the set.

### A4 ordering — behaviorally validated
The environment *already* enforces "no CLI while a dispute is pending" (`approve_credit_limit_increase`
returns ineligible). So the fix is a **policy** instruction to do the CLI first. Baseline task_053 filed
the dispute first and then **denied** the CLI; with the policy, the agent **submits and approves the CLI
(idx 15) before filing the dispute (idx 23)** and calls all eligibility reads — the exact A4 behavior.
The task still scores 0.0 because of an **orthogonal** failure (`user_discoverable_tool_calls` differs —
the `get_card_last_4_digits` retrieval for the dispute), which is an A1-ARG "fetch authoritative
identifier" issue, not A4. So A4-ordering is validated at the behavioral level even though the full-task
DB doesn't match.

### A4 PIN procedure — mechanism proven, but the hard case is computed
The PIN guard is correct (3/3 unit checks: blocks fraud-alert and security-hold resets, allows normal).
But task_092 stays 0.0 and the guard never fired in the episode: the binding error is the **Green** card,
which gold *closes + reissues* while an almost-identical **Evergreen** card is *PIN-reset* — the two
differ only by transaction velocity (a "scripted-attack" pattern computed from transaction timestamps),
**not** by any stored field. A deterministic guard can route the stored signals (`fraud_alert_active`,
`pin_lock_reason="security_hold"`) but cannot decide Green vs Evergreen without computing over the
transaction stream. This is an honest limit of the stored-signal guard; fully fixing 092 needs a
velocity computation feeding the branch.

### A1 / A2 — do not reproduce on sonnet
The opus-4.7 evidence table recorded A1 (refuse to pay/close) and A2 (fail to instruct apply) failures.
Under sonnet these largely vanish: task_045 and task_064 **pass at baseline**, and task_063's
`apply_for_credit_card` **succeeded at baseline** (its failure was a wrong savings account / extra
transfer, not the handoff). The A1/A2 policy text is harmless insurance but its necessity is not
demonstrable on this model. Validating A1/A2 as flips would require a weaker agent that actually refuses.

## Key learnings / caveats

1. **Single-trial DB reward is stochastic.** task_047 baseline went 0→1 and task_063 went 0→1 across two
   trials; task_063 fixed went 1→0. Per-task reward flips on one trial are unreliable. The robust claims
   here rest on the **guard-only run** and the **unit checks**, which are deterministic, not on noisy
   single rewards.
2. **Sonnet ≠ opus-4.7.** The MISSING_WRITE taxonomy was built on opus-4.7 trajectories; sonnet is
   capable enough that the *refusal* sub-mechanisms (A1/A2) mostly don't occur, while the *omitted-check*
   sub-mechanism (A3) does. Choose the agent model to match the failure you want to test.
3. **DB-only scoring makes required reads load-bearing.** Because the discoverable-call set is hashed,
   "did the agent run the eligibility checks" is graded even though the checks mutate no business data —
   which is exactly why the A3 guard (force the reads) moves the reward.
4. **Deterministic guards only reach stored signals.** Where the gold branch depends on a *computed*
   property (task_092 Green velocity), a tool-invariant cannot decide it; that needs the computation
   wired into the environment/agent, not a field lookup.

## Iterations used

Within the 3-iteration budget: (1) implement guards + policy, run baseline vs fixed; (2) guard-only
isolation + unit checks + 2nd-trial confirmations. No 3rd iteration: the deterministic mechanisms are
proven, and the residual failures are either orthogonal to A1–A4 (053 user-tool) or computed-signal
(092 Green) — neither addressable by these fixes.

## Reproduce

```bash
# Deterministic guard checks (fast, no LLM)
uv run python claudedocs/a1a4_fixes/guard_unit_check.py

# A3 guard, isolated from prompt (expect: guard fires, reward 1.0)
uv run python examples/agents/claude_sdk_loop_eval.py \
  --domain banking_knowledge --task-ids task_043 --num-trials 1 \
  --agent-model claude-sonnet-4-6 --sdk-nl-judge \
  --agent-extra-instruction-file claudedocs/a1a4_fixes/policy_noA3.txt \
  --save-to guardonly_task_043

# Full fixed condition
uv run python examples/agents/claude_sdk_loop_eval.py \
  --domain banking_knowledge --task-ids task_043 task_053 task_092 --num-trials 1 \
  --agent-model claude-sonnet-4-6 --sdk-nl-judge \
  --agent-extra-instruction-file claudedocs/a1a4_fixes/policy_a1a4.txt --save-to fix1

# Score
uv run python scripts/i1_eval/verified_score.py task_043 data/simulations/guardonly_task_043/results.json
```

Run artifacts: `data/simulations/{base_,base2_,fix1_,fix2_,guardonly_}task_*/`.
Code change: `src/tau2/domains/banking_knowledge/tools.py` (+55). Policy/unit files:
`claudedocs/a1a4_fixes/`.
