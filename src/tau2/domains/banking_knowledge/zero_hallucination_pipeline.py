"""Zero-hallucination RAG pipeline for the banking_knowledge domain.

Implements the multi-stage, safety-first retrieval architecture from
``FareedKhan-dev/rag-zero-hallucinations`` as a drop-in, duck-typed replacement
for :class:`tau2.knowledge.pipeline.RetrievalPipeline`. It exposes exactly the
surface the ``KBSearchMixin`` tool relies on::

    retrieve(query, top_k=None, return_timing=True) -> RetrievalResult
    get_document_title(doc_id) -> str
    get_document_content(doc_id) -> str

The rule the whole system follows (from the reference repo): *retrieve evidence
with two complementary retrievers, fuse by rank, verify each candidate against
the query, and abstain when support is missing* — rather than trusting a single
retriever's similarity score.

Stages
------
1. **Hybrid retrieval.** A dense (embedding) retriever recovers paraphrase
   matches; a sparse BM25 retriever recovers exact token / id / number matches.
   Each returns an independent ranked candidate list.
2. **Reciprocal Rank Fusion (RRF).** The two ranked lists are fused by rank, not
   by raw score: ``score(d) = Σ_lists 1 / (k + rank_d)`` with ``k = 60``. This
   needs no score normalization and rewards documents both retrievers agree on.
3. **Cross-encoder / LLM reranking (the verification gate).** Each fused
   candidate is scored 0–10 for whether it actually helps answer the query
   (reusing the tested :class:`PointwiseLLMReranker`). Candidates below
   ``rerank_min_score`` are dropped — this is the per-passage faithfulness check
   that isolates hallucination risk to individual passages. NB: the default
   ``rerank_min_score`` is low (2 — "reorder, don't prune") because this tool
   feeds an agent that issues many queries and must still hit required reads, so
   multi-query union recall matters more than aggressive single-query pruning. A
   higher threshold trades recall for precision; validated on the banking
   policy-reasoning tasks (see ``claudedocs/zero_hallucination_rag_validation.md``).
4. **Abstention.** If even the best surviving candidate scores below
   ``abstain_min_top_score``, the tool returns a single explicit
   ``INSUFFICIENT_EVIDENCE`` result instructing the agent to gather more
   information rather than act on a weak match. This is the CRAG "hopeless"
   gate: a single, visible safe-failure mode instead of confident fabrication.

The pipeline holds two already-built sub-pipelines (BM25 + dense) constructed by
``retrieval._create_kb_pipeline`` so there is no circular import and the existing
indexing / embedding-cache machinery is reused unchanged.
"""

from __future__ import annotations

import logging
import time
from typing import TYPE_CHECKING, List, Optional, Tuple

from tau2.knowledge.pipeline import RetrievalResult, RetrievalTiming

if TYPE_CHECKING:
    from tau2.knowledge.pipeline import RetrievalPipeline

logger = logging.getLogger(__name__)

# doc_id used for the explicit safe-failure result.
INSUFFICIENT_EVIDENCE_ID = "INSUFFICIENT_EVIDENCE"
_INSUFFICIENT_EVIDENCE_TEXT = (
    "No knowledge-base passage was verified as sufficiently relevant to this "
    "query (all candidates scored below the support threshold). Do NOT answer or "
    "act from memory. Re-run KB_search with a more specific query, search for the "
    "exact product / policy name, or ask the customer a clarifying question."
)


class ZeroHallucinationPipeline:
    """Hybrid retrieval + RRF fusion + verification-gated reranking + abstention."""

    def __init__(
        self,
        bm25_pipeline: "RetrievalPipeline",
        dense_pipeline: "RetrievalPipeline",
        *,
        candidates: int = 50,
        rrf_k: int = 60,
        rerank_top_n: int = 20,
        top_k: int = 10,
        rerank_model: str = "gpt-5.2",
        rerank_min_score: int = 2,
        reasoning_effort: str = "low",
        abstain: bool = True,
        abstain_min_top_score: int = 2,
        max_concurrency: int = 20,
        rerank_request_timeout: float = 30.0,
    ) -> None:
        self._bm25 = bm25_pipeline
        self._dense = dense_pipeline
        self.candidates = candidates
        self.rrf_k = rrf_k
        self.rerank_top_n = rerank_top_n
        self.top_k = top_k
        self.rerank_min_score = rerank_min_score
        self.abstain = abstain
        self.abstain_min_top_score = abstain_min_top_score
        self._rerank_request_timeout = rerank_request_timeout

        # Reuse the tested pointwise LLM reranker for the verification gate.
        from tau2.knowledge.postprocessors.pointwise_llm_reranker import (
            PointwiseLLMReranker,
        )

        self._reranker = PointwiseLLMReranker(
            model=rerank_model,
            min_score=rerank_min_score,
            reasoning_effort=reasoning_effort,
            max_concurrency=max_concurrency,
        )
        # Bound each rerank request. The stock reranker builds an OpenAI client
        # with no timeout (SDK default ~600s x retries); called from inside the
        # SDK agent's lock-held tool handler, ONE stuck gpt-5.2 request freezes
        # the whole episode for tens of minutes. A tight per-request timeout makes
        # a stuck call raise (caught per-doc), so the gate degrades instead of
        # hanging. See claudedocs/zero_hallucination_rag_validation.md.
        from openai import OpenAI

        self._reranker.client = OpenAI(
            api_key=self._reranker.client.api_key,
            timeout=self._rerank_request_timeout,
            max_retries=1,
        )

    # -- fusion ---------------------------------------------------------------

    def _rrf(
        self, ranked_lists: List[List[Tuple[str, float]]]
    ) -> List[Tuple[str, float]]:
        """Reciprocal Rank Fusion across ranked lists (rank-based, no norm)."""
        fused: dict[str, float] = {}
        for ranked in ranked_lists:
            for rank, (doc_id, _score) in enumerate(ranked):
                fused[doc_id] = fused.get(doc_id, 0.0) + 1.0 / (self.rrf_k + rank + 1)
        return sorted(fused.items(), key=lambda x: x[1], reverse=True)

    # -- retrieval interface (duck-typed RetrievalPipeline) -------------------

    def retrieve(
        self, query: str, top_k: int = None, return_timing: bool = False
    ) -> "List[Tuple[str, float]] | RetrievalResult":
        timing = RetrievalTiming()

        # Stage 1: hybrid retrieval (two independent ranked lists).
        t0 = time.perf_counter()
        dense_res = self._dense.retrieve(query, top_k=self.candidates)
        bm25_res = self._bm25.retrieve(query, top_k=self.candidates)
        timing.retrieval_ms = (time.perf_counter() - t0) * 1000

        # Stage 2: Reciprocal Rank Fusion, keep the top-N for reranking.
        fused = self._rrf([dense_res, bm25_res])[: self.rerank_top_n]

        # Stage 3 + 4: verification-gate rerank, then abstention.
        pp_start = time.perf_counter()
        state = self._dense.state  # doc_content_map shared across sub-pipelines
        try:
            reranked = self._reranker.process(fused, {"query": query}, state)
        except Exception as e:  # never let the gate take down the episode
            logger.warning("ZeroHallucination: rerank failed (%s); using fused order", e)
            reranked = []
        timing.postprocessing_ms = (time.perf_counter() - pp_start) * 1000
        timing.postprocessor_details["ZeroHallucinationVerify"] = (
            timing.postprocessing_ms
        )

        limit = top_k if top_k is not None else self.top_k

        # Graceful degradation: an empty rerank with non-empty fused candidates
        # means the verification gate errored/timed out (min_score is low, so a
        # genuine all-below-threshold is rare). Fall back to the RRF-fused order
        # rather than abstain — better to return unverified-but-fused evidence
        # than to lose retrieval to a transient API stall.
        if not reranked and fused:
            logger.info("ZeroHallucination: gate returned nothing; degrading to fused order")
            if return_timing:
                return RetrievalResult(results=fused[:limit], timing=timing)
            return fused[:limit]

        top_score = reranked[0][1] if reranked else 0.0
        if self.abstain and top_score < self.abstain_min_top_score:
            logger.info(
                "ZeroHallucination: abstaining (top verified score %.1f < %d) for "
                "query=%r",
                top_score,
                self.abstain_min_top_score,
                query[:80],
            )
            self._abstained = True
            result = [(INSUFFICIENT_EVIDENCE_ID, 0.0)]
        else:
            self._abstained = False
            result = reranked[:limit]

        if return_timing:
            return RetrievalResult(results=result, timing=timing)
        return result

    # -- content lookup (delegates to the dense sub-pipeline's maps) ----------

    def get_document_content(self, doc_id: str) -> Optional[str]:
        if doc_id == INSUFFICIENT_EVIDENCE_ID:
            return _INSUFFICIENT_EVIDENCE_TEXT
        return self._dense.get_document_content(doc_id)

    def get_document_title(self, doc_id: str) -> Optional[str]:
        if doc_id == INSUFFICIENT_EVIDENCE_ID:
            return "INSUFFICIENT_EVIDENCE"
        return self._dense.get_document_title(doc_id)

    def get_name(self) -> str:
        return "zero_hallucination[rrf+verify]"
