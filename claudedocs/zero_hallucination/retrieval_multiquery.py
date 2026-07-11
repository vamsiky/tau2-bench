"""Multi-query union retrieval probe — mirrors how the agent searches across
turns (several targeted KB_search queries), which is the realistic setting the
single-query probe understated. Measures union recall of required_documents for
ZH vs its BM25 and dense components. Deterministic; no SDK episode needed.

Queries per task are the actual short, targeted queries the sonnet agent issued
during real episodes (pulled from trajectories) plus the obvious topic queries an
agent would form from the scenario — not hand-tuned to the required set.
"""

import json
from pathlib import Path

from tau2.domains.banking_knowledge.environment import get_knowledge_base
from tau2.domains.banking_knowledge.retrieval import (
    create_bm25_retrieval_pipeline,
    create_embedding_retrieval_pipeline,
    DEFAULT_DENSE_EMBEDDING_MODEL_OPENAI,
)
from tau2.domains.banking_knowledge.zero_hallucination_pipeline import (
    ZeroHallucinationPipeline,
)

TASKS_DIR = Path("data/tau2/domains/banking_knowledge/tasks")
TOP_K = 8

# Realistic per-turn agent queries (topic-driven, not tuned to required doc ids).
QUERIES = {
    "task_043": [
        "close Platinum Rewards Card account closure procedure",
        "credit card annual fee waiver retention offer",
        "outstanding balance must be paid before closing credit card",
        "check dispute history before closing account eligibility",
        "pending replacement card orders before closing account",
        "credit card account closure eligibility requirements",
    ],
    "task_047": [
        "downgrade Platinum Rewards Card to lower fee card",
        "credit card annual fee retention statement credit offer",
        "Business Platinum Rewards Card rewards rate benefits",
        "close business credit card Silver Zoom Card",
        "apply statement credit retention tool procedure",
    ],
    "task_053": [
        "credit limit increase eligibility while dispute pending",
        "file a dispute for a credit card transaction",
        "credit card account logistics limit increase",
        "approve credit limit increase before dispute order",
    ],
}


def union_recall(pipes, queries, required, k):
    got = set()
    for q in queries:
        for doc_id, _ in pipes.retrieve(q, top_k=k):
            got.add(doc_id)
    hit = set(required) & got
    return len(hit), len(required), got


def main():
    kb = get_knowledge_base()
    bm25 = create_bm25_retrieval_pipeline(kb, top_k=50)
    dense = create_embedding_retrieval_pipeline(
        kb, "openai", {"model": DEFAULT_DENSE_EMBEDDING_MODEL_OPENAI}, top_k=50
    )
    # ZH configs to compare: gate-prune (min_score=4) vs gate-reorder-only
    # (min_score=1: reranker reorders but drops nothing), at two top_k widths.
    zh_prune = ZeroHallucinationPipeline(
        bm25, dense, candidates=50, rerank_top_n=20, top_k=TOP_K,
        rerank_min_score=4, abstain=True, abstain_min_top_score=2,
    )
    zh_reorder8 = ZeroHallucinationPipeline(
        bm25, dense, candidates=50, rerank_top_n=20, top_k=TOP_K,
        rerank_min_score=1, abstain=True, abstain_min_top_score=1,
    )
    zh_reorder10 = ZeroHallucinationPipeline(
        bm25, dense, candidates=50, rerank_top_n=20, top_k=10,
        rerank_min_score=1, abstain=True, abstain_min_top_score=1,
    )

    print(f"Multi-query UNION recall of required_documents\n")
    hdr = f"{'task':<10} {'#q':>3} {'bm25@8':>7} {'dense@8':>8} {'ZHprune@8':>10} {'ZHreord@8':>10} {'ZHreord@10':>11} {'req':>5}"
    print(hdr)
    tot = {"bm": 0, "de": 0, "zp": 0, "zr8": 0, "zr10": 0, "r": 0}
    for tid, queries in QUERIES.items():
        req = json.loads((TASKS_DIR / f"{tid}.json").read_text())["required_documents"]
        bh, n, _ = union_recall(bm25, queries, req, TOP_K)
        dh, _, _ = union_recall(dense, queries, req, TOP_K)
        zp, _, _ = union_recall(zh_prune, queries, req, TOP_K)
        zr8, _, _ = union_recall(zh_reorder8, queries, req, TOP_K)
        zr10, _, _ = union_recall(zh_reorder10, queries, req, 10)
        print(f"{tid:<10} {len(queries):>3} {bh:>7} {dh:>8} {zp:>10} {zr8:>10} {zr10:>11} {n:>5}")
        tot["bm"] += bh; tot["de"] += dh; tot["zp"] += zp
        tot["zr8"] += zr8; tot["zr10"] += zr10; tot["r"] += n
    print(f"{'TOTAL':<10} {'':>3} {tot['bm']:>7} {tot['de']:>8} {tot['zp']:>10} "
          f"{tot['zr8']:>10} {tot['zr10']:>11} {tot['r']:>5}")


if __name__ == "__main__":
    main()
