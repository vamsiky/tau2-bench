# Hindsight retrieval for banking_knowledge — implementation + validation

Replaces tau2's local BM25/embedding `KB_search` with a [Hindsight](https://hindsight.vectorize.io)
knowledge bank: the whole banking corpus is stored in a bank via `retain`, and `KB_search`
answers queries at runtime via `recall`. Validated on the I1 task set
(`claudedocs/i1_fix_validation.md`): **task_047, 058, 063, 064, 067**.

## What was built

| Piece | Location |
|---|---|
| `HindsightPipeline` (duck-typed `RetrievalPipeline`) | `src/tau2/domains/banking_knowledge/hindsight_pipeline.py` |
| Variants `hindsight`, `hindsight_grep` | `src/tau2/domains/banking_knowledge/retrieval.py` |
| Prompt | `data/tau2/domains/banking_knowledge/prompts/hindsight.md` |
| Ingest CLI + runbook | `scripts/hindsight/ingest.py`, `scripts/hindsight/README.md` |

`HindsightPipeline` implements exactly the surface `KBSearchMixin` consumes
(`retrieve() -> RetrievalResult`, `get_document_title/content`), so it drops into the
unchanged toolkit. Design:

- **Lazy connect + lazy ingest** — `__init__` never touches the server; the client is
  created and the corpus ingested only on the first `KB_search`. The evaluator's
  gold/predicted env rebuilds (which never call `KB_search`) never reach Hindsight.
- **Sentinel-guarded, idempotent ingestion** (`~/.cache/tau2_hindsight/<bank>.json`,
  corpus-hash keyed) so trials and restarts reuse the persisted bank.
- **`recall(include_chunks=True)`** surfaces the verbatim source chunk alongside the
  synthesized fact, preserving procedural precision.
- Corpus = the **71-doc consolidated `register_corpus`** (same lossless corpus as
  `register_search`), not the 698 raw fragments — far cheaper to push through Hindsight's
  LLM-backed fact extraction.

Bank `tau2-banking-register`: 71 docs → **1685 extracted facts**; recall returns 127–150
relevant facts/query and covers every I1 topic (incl. 047's dispute-history /
pending-replacement pre-checks).

### Operational gotchas found
- **`OPENSSL_armcap=0` is mandatory** running the `ghcr.io/vectorize-io/hindsight:latest`
  image under podman on Apple Silicon. Without it the bundled `cryptography`/OpenSSL native
  code SIGILLs (`Illegal instruction`) on the Virtualization.framework VM and `hindsight-api`
  crash-loops.
- Ingestion must be **async** (`retain_async=True`) + drain-polled via the operations REST
  endpoint. Synchronous `retain` on the 123 KB consolidated doc times the client out at 120 s.
- Fact extraction/consolidation runs on **OpenAI gpt-4o-mini**; the org's 200k TPM cap is the
  ingestion bottleneck (429s → retries). Recall itself is fast (~1 s, no contention).

## Validation — methodology

Same harness for both arms (`examples/agents/claude_sdk_loop_eval.py`, agent
`claude-opus-4-8`, SDK user-sim opus-4-8/high, `--sdk-nl-judge`), **1 trial/task, plain
variant prompt (no fix snippet)**. Baseline = `register_search` (BM25+grep over the
*identical* 71-doc corpus) — a controlled, same-corpus comparison isolating the retrieval
mechanism. Scored both strict (driver) and verified (`scripts/i1_eval/verified_score.py`:
discoverable-audit as superset, free-text annotation fields excluded). 114 Hindsight recall
calls were served across the 5 hindsight trials (baseline served 0 — it is lexical).

## Results

Strict reward: **baseline 0/5, hindsight 1/5**. Verified: **baseline 0/5, hindsight 1/5**.

| task | baseline `register_search` (verified) | `hindsight` (verified) |
|---|---|---|
| 047 | FAIL — missing `apply_statement_credit`, `get_pending_replacement_orders`, `get_user_dispute_history` | FAIL — missing `log_credit_card_closure_reason`, `get_closure_reason_history` |
| 058 | FAIL — **never opened the account** (`open_bank_account` missing) | FAIL — opened, wrong tier (`accounts` table differs only) |
| 063 | FAIL — never opened | FAIL — never opened |
| 064 | FAIL — never opened | **PASS / PASS** |
| 067 | FAIL — missing close+open+apply (`accounts`+`applications` differ) | FAIL — only `credit_card_applications` differs |

### Interpretation (honest)

- **Headline pass rate barely moves** (0/5 → 1/5). This matches the I1 thesis that these
  failures are not primarily retrieval-bound (grader strictness + selection/under-action),
  so a retrieval swap alone was never going to clear the set.
- **But Hindsight visibly changed agent behavior for the better.** Tasks failing on
  *missing required calls* dropped from **5/5 → 2/5**. Residual failures shifted from
  "agent never executed the action" (baseline: never opened accounts on 058/063/064) to
  "executed it slightly wrong" (hindsight: wrong tier on 058, single-table diff on 067) —
  i.e. the agent completed far more of the required procedure. 064 became a clean strict
  pass.
- Concise *extracted facts* (vs. raw doc dumps / lexical hits) appear to help the agent
  follow multi-step procedures to completion. This is a real, if modest, signal in
  Hindsight's favor on the dimension it can affect.

### Caveats
- **Single trial per task** — these tasks are stochastic (the I1 work used best-of-2). The
  per-task verdicts are noisy; the cross-task *pattern* (fewer missing-call failures) is the
  more reliable read.
- The baseline here is `register_search` (same-corpus control), which underperformed the
  documented `alltools` baseline — so this is a clean mechanism A/B, not a claim against the
  strongest prior config.
- Hindsight's fact extraction is lossy by construction; for tasks needing exact verbatim
  policy values, surfacing chunks (done here) matters.

### Recommended next steps
1. Best-of-2 (or 4) per task for both arms to de-noise the headline number.
2. A third arm: `hindsight` + the `fix4` selection prompt (the I1 best selection prompt) —
   tests whether better retrieval *plus* the selection fix compounds.
3. Try `recall(budget="high")` and a `hindsight_grep` arm (recall + lexical grep fallback).
