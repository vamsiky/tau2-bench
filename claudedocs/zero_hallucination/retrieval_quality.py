"""Iteration-0 retrieval-quality probe for the zero_hallucination pipeline.

For each A1-A4 policy-reasoning task, query the pipeline with the task's natural
user text and measure recall of the task's required_documents in the returned
set. Compares zero_hallucination (hybrid+RRF+verify) against its BM25 and dense
components to isolate the effect of fusion + the verification gate.
"""

import json
import sys
from pathlib import Path

from tau2.domains.banking_knowledge.environment import get_knowledge_base
from tau2.domains.banking_knowledge.retrieval import (
    create_bm25_retrieval_pipeline,
    create_embedding_retrieval_pipeline,
    DEFAULT_DENSE_EMBEDDING_MODEL_OPENAI,
)
from tau2.domains.banking_knowledge.zero_hallucination_pipeline import (
    ZeroHallucinationPipeline,
    INSUFFICIENT_EVIDENCE_ID,
)

TASKS_DIR = Path("data/tau2/domains/banking_knowledge/tasks")
TASK_IDS = ["task_043", "task_047", "task_053", "task_063", "task_064", "task_092"]
TOP_K = 10


def task_query(task: dict) -> str:
    """Natural query = the situation + goal sections (what drives the agent's search).

    Drops the verification-info and conversation-flow boilerplate, which is noise
    for retrieval and matches how an agent actually forms KB queries.
    """
    us = task.get("user_scenario", {})
    instr = us.get("instructions", "") or ""
    situation = ""
    for marker in ("**Your situation:**", "**Your goal:**"):
        idx = instr.find(marker)
        if idx != -1:
            end = instr.find("**Information you know", idx)
            end = end if end != -1 else instr.find("## Conversation Flow", idx)
            end = end if end != -1 else idx + 400
            situation += " " + instr[idx:end]
    if not situation.strip():
        situation = instr[:600]
    return " ".join(situation.split())[:800]


def recall(retrieved_ids, required):
    req = set(required)
    hit = req & set(retrieved_ids)
    return len(hit), len(req), sorted(req - hit)


def main():
    kb = get_knowledge_base()
    print(f"KB documents: {len(kb.documents)}")

    # Build components once (shared candidate pool of 50).
    bm25 = create_bm25_retrieval_pipeline(kb, top_k=50)
    dense = create_embedding_retrieval_pipeline(
        kb, "openai", {"model": DEFAULT_DENSE_EMBEDDING_MODEL_OPENAI}, top_k=50
    )
    zh = ZeroHallucinationPipeline(
        bm25, dense, candidates=50, rerank_top_n=20, top_k=TOP_K,
        rerank_min_score=4, abstain=True, abstain_min_top_score=2,
    )

    summary = []
    for tid in TASK_IDS:
        task = json.loads((TASKS_DIR / f"{tid}.json").read_text())
        required = task.get("required_documents", [])
        q = task_query(task)

        bm25_ids = [d for d, _ in bm25.retrieve(q, top_k=TOP_K)]
        dense_ids = [d for d, _ in dense.retrieve(q, top_k=TOP_K)]
        zh_res = zh.retrieve(q, top_k=TOP_K)
        zh_ids = [d for d, _ in zh_res]
        abstained = zh_ids == [INSUFFICIENT_EVIDENCE_ID]

        bh, bn, _ = recall(bm25_ids, required)
        dh, dn, _ = recall(dense_ids, required)
        zh_hit, zn, zmiss = recall(zh_ids, required)

        print(f"\n=== {tid} (required={zn} docs) ===")
        print(f"  bm25   recall@{TOP_K}: {bh}/{bn}")
        print(f"  dense  recall@{TOP_K}: {dh}/{dn}")
        print(f"  ZH     recall@{TOP_K}: {zh_hit}/{zn}"
              f"{'  [ABSTAINED]' if abstained else ''}")
        if not abstained:
            print(f"  ZH returned {len(zh_ids)} verified docs; missed: {zmiss[:4]}"
                  f"{'...' if len(zmiss) > 4 else ''}")
        summary.append((tid, bh, dh, zh_hit, zn, abstained))

    print("\n\n=== SUMMARY (recall@%d of required_documents) ===" % TOP_K)
    print(f"{'task':<10} {'bm25':>6} {'dense':>6} {'ZH':>6} {'req':>5} {'abstain':>8}")
    tb = td = tz = tr = 0
    for tid, bh, dh, zh_hit, zn, ab in summary:
        print(f"{tid:<10} {bh:>6} {dh:>6} {zh_hit:>6} {zn:>5} {str(ab):>8}")
        tb += bh; td += dh; tz += zh_hit; tr += zn
    print(f"{'TOTAL':<10} {tb:>6} {td:>6} {tz:>6} {tr:>5}")


if __name__ == "__main__":
    sys.exit(main())
