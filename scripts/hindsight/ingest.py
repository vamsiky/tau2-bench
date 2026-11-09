#!/usr/bin/env python
"""One-time ingestion of the banking_knowledge corpus into a Hindsight bank.

Stores the whole banking domain knowledge in a Hindsight bank so the
``hindsight`` retrieval variant can answer ``KB_search`` via ``recall`` at
runtime. Ingestion is idempotent: a sentinel records the ingested corpus
fingerprint, so re-running is a no-op unless the corpus changed or ``--force``
is passed.

Usage:
    uv run python scripts/hindsight/ingest.py                 # default 'hindsight' variant
    uv run python scripts/hindsight/ingest.py --variant hindsight --force
    uv run python scripts/hindsight/ingest.py --check         # report status only

Requires a running Hindsight server (see scripts/hindsight/README.md).
"""

import argparse
import logging
import sys

from tau2.domains.banking_knowledge.environment import get_knowledge_base
from tau2.domains.banking_knowledge.hindsight_pipeline import HindsightPipeline
from tau2.domains.banking_knowledge.retrieval import resolve_variant


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--variant", default="hindsight", help="retrieval variant name")
    parser.add_argument(
        "--force", action="store_true", help="re-ingest even if fingerprint matches"
    )
    parser.add_argument(
        "--check", action="store_true", help="report ingestion status and exit"
    )
    parser.add_argument("--log-level", default="INFO")
    args = parser.parse_args()

    logging.basicConfig(
        level=args.log_level, format="%(asctime)s %(levelname)s %(message)s"
    )

    variant = resolve_variant(args.variant)
    if variant.kb_search is None or variant.kb_search.type != "hindsight":
        print(f"Variant {args.variant!r} is not a Hindsight variant.", file=sys.stderr)
        return 2

    kb = get_knowledge_base(getattr(variant, "corpus_dir", None))
    pipeline = HindsightPipeline(
        knowledge_base=kb,
        bank_id=variant.kb_search.bank_id or "tau2-banking-knowledge",
        top_k=variant.kb_search.top_k,
        budget=variant.kb_search.budget,
        include_chunks=variant.kb_search.include_chunks,
    )

    fp = pipeline._sentinel_path()
    from tau2.domains.banking_knowledge.hindsight_pipeline import _corpus_fingerprint

    fingerprint = _corpus_fingerprint(pipeline._documents)
    already = pipeline._already_ingested(fingerprint)
    print(
        f"bank={pipeline.bank_id} base_url={pipeline.base_url} "
        f"docs={len(pipeline._documents)} sentinel={fp} ingested={already}"
    )
    if args.check:
        return 0

    if args.force and fp.exists():
        fp.unlink()
        print("Sentinel cleared (--force); will re-ingest.")

    pipeline.ensure_ingested()
    print("Ingestion complete." if not (already and not args.force) else "Up to date.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
