"""Hindsight-backed retrieval pipeline for the banking_knowledge domain.

`HindsightPipeline` is a drop-in, duck-typed replacement for
:class:`tau2.knowledge.pipeline.RetrievalPipeline`. It exposes exactly the
surface the ``KBSearchMixin`` tool relies on:

* ``retrieve(query, top_k=None, return_timing=True) -> RetrievalResult``
* ``get_document_title(doc_id) -> str``
* ``get_document_content(doc_id) -> str``

Instead of indexing documents into a local BM25/embedding index, it stores the
whole knowledge base in a Hindsight *bank* (https://hindsight.vectorize.io) via
``retain`` and answers ``KB_search`` queries with ``recall``.

Two design choices keep this safe inside the tau2 eval loop:

1. **Lazy connect + lazy ingest.** ``__init__`` is cheap and never touches the
   Hindsight server. The client is created and the corpus ingested only on the
   first ``retrieve`` call. The evaluator rebuilds gold/predicted environments
   that never call ``KB_search`` — those never reach Hindsight at all.
2. **Sentinel-guarded ingestion.** Ingestion runs once per (bank, corpus-hash).
   A local sentinel records the ingested corpus fingerprint, so repeated trials
   and process restarts reuse the already-populated, persisted bank rather than
   re-running Hindsight's (LLM-backed, costly) fact extraction.

Hindsight ``recall`` returns extracted *facts* plus their source *chunks*. To
preserve the verbatim procedural detail the banking tasks depend on, the search
result surfaces the source chunk text alongside the synthesized fact.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import time
from pathlib import Path
from typing import TYPE_CHECKING, Any, List, Optional, Tuple

from tau2.knowledge.pipeline import RetrievalResult, RetrievalTiming

if TYPE_CHECKING:
    from tau2.domains.banking_knowledge.data_model import KnowledgeBase

logger = logging.getLogger(__name__)

DEFAULT_BASE_URL = "http://localhost:8888"
SENTINEL_DIR = Path.home() / ".cache" / "tau2_hindsight"


def _corpus_fingerprint(documents: List[dict]) -> str:
    """Stable hash of the corpus (ids + content) for ingestion idempotency."""
    h = hashlib.sha256()
    for doc in sorted(documents, key=lambda d: d["id"]):
        h.update(doc["id"].encode())
        h.update(b"\x00")
        h.update(doc["content"].encode())
        h.update(b"\x00")
    return h.hexdigest()


class HindsightPipeline:
    """Retrieval pipeline backed by a Hindsight knowledge bank."""

    def __init__(
        self,
        knowledge_base: "KnowledgeBase",
        bank_id: str,
        *,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        top_k: int = 10,
        budget: str = "mid",
        include_chunks: bool = True,
        max_tokens: int = 4096,
        timeout: float = 300.0,
        drain_timeout: float = 3600.0,
    ) -> None:
        self.bank_id = bank_id
        self.base_url = base_url or os.getenv("HINDSIGHT_API_URL", DEFAULT_BASE_URL)
        self.api_key = api_key or os.getenv("HINDSIGHT_API_KEY")
        self.top_k = top_k
        self.budget = budget
        self.include_chunks = include_chunks
        self.max_tokens = max_tokens
        self.timeout = timeout
        self.drain_timeout = drain_timeout

        # Materialize the corpus once (cheap, in-memory) for lazy ingestion.
        self._documents = [
            {"id": doc.id, "title": doc.title, "content": doc.content}
            for doc in knowledge_base.get_all_documents()
        ]

        self._client = None
        self._ingested = False
        # Per-query maps populated by retrieve() so the KB_search formatter can
        # look up the title/content of each returned synthetic doc id.
        self._content_map: dict[str, str] = {}
        self._title_map: dict[str, str] = {}

    # -- connection / ingestion ------------------------------------------------

    def _get_client(self):
        if self._client is None:
            from hindsight_client import Hindsight

            kwargs: dict[str, Any] = {"base_url": self.base_url, "timeout": self.timeout}
            if self.api_key:
                kwargs["api_key"] = self.api_key
            self._client = Hindsight(**kwargs)
        return self._client

    def _sentinel_path(self) -> Path:
        safe = self.bank_id.replace("/", "_")
        return SENTINEL_DIR / f"{safe}.json"

    def _already_ingested(self, fingerprint: str) -> bool:
        path = self._sentinel_path()
        if not path.exists():
            return False
        try:
            data = json.loads(path.read_text())
        except (OSError, json.JSONDecodeError):
            return False
        return data.get("fingerprint") == fingerprint

    def _mark_ingested(self, fingerprint: str) -> None:
        path = self._sentinel_path()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(
                {
                    "bank_id": self.bank_id,
                    "fingerprint": fingerprint,
                    "n_documents": len(self._documents),
                    "base_url": self.base_url,
                }
            )
        )

    def ensure_ingested(self) -> None:
        """Create the bank and ingest the corpus once (idempotent)."""
        if self._ingested:
            return
        fingerprint = _corpus_fingerprint(self._documents)
        if self._already_ingested(fingerprint):
            self._ingested = True
            logger.info(
                "Hindsight bank %r already populated (%d docs, fingerprint match); "
                "skipping ingestion.",
                self.bank_id,
                len(self._documents),
            )
            return

        client = self._get_client()
        # Rebuild from a clean slate so a prior partial run can't leave duplicate
        # facts. Safe: when the sentinel is absent we are (re)building anyway.
        try:
            client.delete_bank(self.bank_id)
            logger.info("Dropped existing bank %r for a clean rebuild.", self.bank_id)
        except Exception as e:
            logger.debug("delete_bank(%r) non-fatal: %s", self.bank_id, e)
        self._ensure_bank(client)

        logger.info(
            "Queueing %d documents into Hindsight bank %r (async; LLM-backed fact "
            "extraction runs server-side)...",
            len(self._documents),
            self.bank_id,
        )
        t0 = time.perf_counter()
        failures: list[str] = []
        for i, doc in enumerate(self._documents, 1):
            try:
                client.retain(
                    bank_id=self.bank_id,
                    content=doc["content"],
                    context=doc["title"],
                    document_id=doc["id"],
                    metadata={"title": doc["title"], "doc_id": doc["id"]},
                    retain_async=True,
                )
            except Exception as e:
                failures.append(doc["id"])
                logger.warning("  retain failed for %s: %s", doc["id"], repr(e)[:160])
            if i % 10 == 0 or i == len(self._documents):
                logger.info("  queued %d/%d docs", i, len(self._documents))
        logger.info(
            "Queued in %.1fs (%d failures). Waiting for server-side processing to "
            "drain...",
            time.perf_counter() - t0,
            len(failures),
        )
        self._wait_for_drain(client)
        logger.info(
            "Hindsight ingestion complete in %.1fs total.", time.perf_counter() - t0
        )
        if failures:
            logger.warning("Documents that failed to queue: %s", failures)
        self._mark_ingested(fingerprint)
        self._ingested = True

    def _pending_op_count(self, client) -> int:
        """Number of not-yet-finished retain/consolidation ops for the bank.

        Uses the operations REST endpoint directly: the SDK's ``operations``
        sub-API is async-only (returns un-awaited coroutines), whereas this poll
        runs in the synchronous ingest path. The response's ``total`` field is
        the authoritative count for the requested status.
        """
        import urllib.error
        import urllib.parse
        import urllib.request

        base = self.base_url.rstrip("/")
        bank = urllib.parse.quote(self.bank_id, safe="")
        total = 0
        for status in ("pending", "processing"):
            url = f"{base}/v1/default/banks/{bank}/operations?status={status}&limit=1"
            req = urllib.request.Request(url)
            if self.api_key:
                req.add_header("Authorization", f"Bearer {self.api_key}")
            try:
                with urllib.request.urlopen(req, timeout=30) as resp:
                    data = json.loads(resp.read().decode())
                total += int(data.get("total", 0))
            except (urllib.error.URLError, ValueError, OSError) as e:
                logger.debug("operations poll (%s) failed: %s", status, e)
        return total

    def _wait_for_drain(self, client) -> None:
        deadline = time.perf_counter() + self.drain_timeout
        idle_polls = 0
        while time.perf_counter() < deadline:
            pending = self._pending_op_count(client)
            if pending == 0:
                idle_polls += 1
                # Require two consecutive empty polls: consolidation ops can be
                # enqueued slightly after their parent retain finishes.
                if idle_polls >= 2:
                    return
            else:
                idle_polls = 0
                logger.info("  draining: %d op(s) pending/processing...", pending)
            time.sleep(10)
        logger.warning(
            "Drain wait hit %.0fs timeout; proceeding (bank may still be "
            "consolidating in the background).",
            self.drain_timeout,
        )

    def _ensure_bank(self, client) -> None:
        try:
            client.create_bank(
                bank_id=self.bank_id,
                name=f"tau2 banking_knowledge ({self.bank_id})",
                mission=(
                    "You hold RhoBank's customer-service policy knowledge base. "
                    "Answer retrieval queries with the precise, verbatim policy "
                    "text relevant to the query."
                ),
            )
        except Exception as e:  # bank likely already exists — non-fatal
            logger.debug("create_bank(%r) non-fatal error: %s", self.bank_id, e)

    # -- retrieval interface (duck-typed RetrievalPipeline) --------------------

    def retrieve(
        self, query: str, top_k: int = None, return_timing: bool = False
    ) -> "List[Tuple[str, float]] | RetrievalResult":
        self.ensure_ingested()
        client = self._get_client()
        timing = RetrievalTiming()

        t0 = time.perf_counter()
        resp = client.recall(
            bank_id=self.bank_id,
            query=query,
            budget=self.budget,
            max_tokens=self.max_tokens,
            include_chunks=self.include_chunks,
        )
        timing.retrieval_ms = (time.perf_counter() - t0) * 1000

        self._content_map = {}
        self._title_map = {}
        results: List[Tuple[str, float]] = []

        recall_results = getattr(resp, "results", None) or []
        limit = top_k if top_k is not None else self.top_k
        for i, r in enumerate(recall_results):
            if limit is not None and i >= limit:
                break
            doc_id = f"hs_{i}"
            # Hindsight may or may not expose a numeric score; fall back to a
            # rank-descending score so ordering is preserved.
            score = getattr(r, "score", None)
            score = float(score) if score is not None else max(0.0, 1.0 - i * 0.01)

            fact_text = getattr(r, "text", "") or ""
            fact_type = getattr(r, "type", "memory")
            chunks = getattr(r, "chunks", None) or []
            chunk_texts = [getattr(c, "text", "") for c in chunks if getattr(c, "text", "")]

            content = fact_text
            if chunk_texts:
                content = content + "\n\nSource:\n" + "\n---\n".join(chunk_texts)

            self._content_map[doc_id] = content.strip()
            self._title_map[doc_id] = f"[{fact_type}] {fact_text[:80]}".strip()
            results.append((doc_id, score))

        if return_timing:
            return RetrievalResult(results=results, timing=timing)
        return results

    def get_document_content(self, doc_id: str) -> Optional[str]:
        return self._content_map.get(doc_id)

    def get_document_title(self, doc_id: str) -> Optional[str]:
        return self._title_map.get(doc_id)

    def get_name(self) -> str:
        return f"hindsight[{self.bank_id}]"
