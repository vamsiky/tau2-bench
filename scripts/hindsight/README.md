# Hindsight retrieval for banking_knowledge

Stores the whole banking_knowledge corpus in a [Hindsight](https://hindsight.vectorize.io)
bank and answers `KB_search` at runtime via Hindsight `recall`, as an alternative to the
local BM25 / embedding retrieval pipelines.

## Components

| Piece | Location |
|---|---|
| Pipeline (duck-typed `RetrievalPipeline`) | `src/tau2/domains/banking_knowledge/hindsight_pipeline.py` |
| Retrieval variants `hindsight`, `hindsight_grep` | `src/tau2/domains/banking_knowledge/retrieval.py` |
| Prompt | `data/tau2/domains/banking_knowledge/prompts/hindsight.md` |
| Ingest CLI | `scripts/hindsight/ingest.py` |

The variants index the **71-doc consolidated `register_corpus`** (same lossless corpus as
`register_search`), not the 698 raw fragments — far cheaper to push through Hindsight's
LLM-backed fact extraction.

## 1. Run the Hindsight server (podman)

```bash
export OPENAI_API_KEY=$(grep '^OPENAI_API_KEY=' .env | cut -d= -f2-)
podman run -d --name hindsight --restart unless-stopped \
  -p 8888:8888 -p 9999:9999 \
  -e OPENSSL_armcap=0 \
  -e HINDSIGHT_API_LLM_API_KEY="$OPENAI_API_KEY" \
  -e HINDSIGHT_API_LLM_MAX_CONCURRENT=5 \
  -v hindsight-data:/home/hindsight/.pg0 \
  ghcr.io/vectorize-io/hindsight:latest
```

- API: http://localhost:8888 · Control plane / UI: http://localhost:9999
- Fact extraction / answer generation use **OpenAI gpt-4o-mini** via `HINDSIGHT_API_LLM_API_KEY`.

> **`HINDSIGHT_API_LLM_MAX_CONCURRENT=5` keeps ingestion under the OpenAI TPM cap.** The
> default (32) launches up to 32 concurrent gpt-4o-mini calls — at ~4k tokens each that
> blows a 200k tokens-per-minute org limit and triggers a 429 storm (slow retries, some
> dropped extraction ops). A global cap of 5 bounds retain **and** consolidation together
> and essentially eliminates the 429s; ingestion just runs slower. `recall` uses a separate
> pool (`HINDSIGHT_API_RECALL_MAX_CONCURRENT`, default 32) so runtime `KB_search` stays fast.
> Other knobs if you need finer control: `HINDSIGHT_API_CONSOLIDATION_LLM_MAX_CONCURRENT`,
> `HINDSIGHT_API_WORKER_MAX_SLOTS` (default 10), `HINDSIGHT_API_ENABLE_AUTO_CONSOLIDATION`
> (set `false` to skip the background fact-merging pass entirely).

> **`OPENSSL_armcap=0` is required on Apple Silicon + podman.** Without it the bundled
> `cryptography`/OpenSSL native code hits a SIGILL (`Illegal instruction (core dumped)`)
> on the Virtualization.framework VM and `hindsight-api` crash-loops. Setting
> `OPENSSL_armcap=0` disables OpenSSL's ARM CPU-feature probing and the API boots.

Override the endpoint with `HINDSIGHT_API_URL` (default `http://localhost:8888`) and auth
with `HINDSIGHT_API_KEY` if the server is configured with one.

## 2. Ingest the corpus (one-time)

```bash
uv run python scripts/hindsight/ingest.py --check        # status
uv run python scripts/hindsight/ingest.py --variant hindsight   # ingest (~14 min, 71 docs)
uv run python scripts/hindsight/ingest.py --force        # re-ingest from scratch
```

Ingestion is idempotent: a sentinel at `~/.cache/tau2_hindsight/<bank>.json` records the
corpus fingerprint, so trials and the evaluator's env rebuilds never re-ingest. The bank
itself persists in the `hindsight-data` volume across container restarts.

## 3. Run an evaluation with the variant

The driver's `--retrieval-config` selects the variant (banking_knowledge only):

```bash
uv run python examples/agents/claude_sdk_loop_eval.py \
  --domain banking_knowledge --task-ids task_064 --num-trials 1 \
  --agent-model claude-opus-4-8 --sdk-nl-judge \
  --retrieval-config hindsight \
  --save-to hindsight_smoke --log-level INFO
```

If the server is down when the agent calls `KB_search`, the tool errors for that call only
(connect + ingest are lazy — env construction never touches Hindsight).
