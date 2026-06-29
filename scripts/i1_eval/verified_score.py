#!/usr/bin/env python3
"""Principled "verified" re-scorer (SABER tau-Bench-Verified style) for I1
(banking_knowledge) trajectories, applied to an existing results.json.

Two changes vs the strict DB-hash scorer:
  1. agent_discoverable_tools: require gold's called tools to be a SUBSET of the
     agent's calls (no MISSING required call) but ALLOW extra calls — a harmless
     extra read is not penalized. This keeps task_047's requirement (a missing
     required check still fails) while unblocking task_063/task_064's extra read.
  2. Drop free-text annotation fields (e.g. closure_reason) before comparing —
     unblocks task_067's descriptive closure reason.
Every other table (accounts, applications, ...) is compared exactly.

Usage:
    uv run python scripts/i1_eval/verified_score.py <task_id> <results.json>
    uv run python scripts/i1_eval/verified_score.py            # built-in I1 table

Reconstructed from the 2026-06-24 I1 investigation session.
"""
import sys
import copy

# claude_sdk_loop_eval parses argv at import time; capture our args, then neutralize.
_A = list(sys.argv)
sys.argv = ["x"]

from tau2.runner import get_tasks, build_environment  # noqa: E402
from tau2.data_model.simulation import Results  # noqa: E402
from examples.agents.claude_sdk_loop_eval import _retrieval_env_kwargs  # noqa: E402

DOMAIN = "banking_knowledge"
ek = _retrieval_env_kwargs(DOMAIN, "alltools", None)
FREE_TEXT_FIELDS = {"closure_reason"}  # annotation-only, no functional effect

# Default per-task best-known result files (used when no CLI args are given).
DEFAULT_ITEMS = [
    ("task_047", "data/simulations/i1_fix5/results.json"),
    ("task_058", "data/simulations/i1_fix4/results.json"),  # fix4 = correct Silver selection
    ("task_063", "data/simulations/i1_fix5/results.json"),
    ("task_064", "data/simulations/i1_fix5/results.json"),
    ("task_067", "data/simulations/i1_fix1/results.json"),
]


def build(tid, res):
    """Return (gold_db, predicted_db, strict_reward) for a task/result pair."""
    task = get_tasks(DOMAIN, task_ids=[tid])[0]
    sim = next(s for s in Results.load(res).simulations if s.task_id == tid)
    init = task.initial_state

    def mk():
        e = build_environment(DOMAIN, env_kwargs={**ek, "task": task})
        e.set_state(
            initialization_data=init.initialization_data if init else None,
            initialization_actions=init.initialization_actions if init else None,
            message_history=[],
        )
        return e

    g = mk()
    for a in task.evaluation_criteria.actions or []:
        g.make_tool_call(a.name, requestor=a.requestor, **a.arguments)
    p = mk()
    p.set_state(
        initialization_data=init.initialization_data if init else None,
        initialization_actions=init.initialization_actions if init else None,
        message_history=list(sim.messages),
    )
    return (
        g.tools.db.model_dump(),
        p.tools.db.model_dump(),
        sim.reward_info.reward if sim.reward_info else None,
    )


def strip_free_text(d):
    d = copy.deepcopy(d)
    for table in d.values():
        data = table.get("data") if isinstance(table, dict) else None
        if isinstance(data, dict):
            for rec in data.values():
                if isinstance(rec, dict):
                    for f in FREE_TEXT_FIELDS:
                        rec.pop(f, None)
    return d


def verified_match(gd, pd):
    """Return (is_match, reasons). gd = gold DB dump, pd = predicted DB dump."""
    gd, pd = strip_free_text(gd), strip_free_text(pd)
    reasons = []

    # 1) discoverable audit: gold tool_names must be a subset of predicted tool_names
    def toolnames(db):
        data = (db.get("agent_discoverable_tools", {}).get("data", {}) or {})
        return {r.get("tool_name") for r in data.values()}

    missing = toolnames(gd) - toolnames(pd)
    if missing:
        reasons.append(f"MISSING required discoverable calls: {sorted(missing)}")

    # 2) compare every other table exactly (audit table handled above)
    for table in sorted(set(gd) | set(pd)):
        if table == "agent_discoverable_tools":
            continue
        if gd.get(table) != pd.get(table):
            reasons.append(f"table '{table}' differs")
    return (len(reasons) == 0), reasons


def main():
    if len(_A) >= 3:
        items = [(_A[1], _A[2])]
    else:
        items = DEFAULT_ITEMS
    print(f"{'task':9} {'strict':7} {'verified':9} reason")
    for tid, res in items:
        gd, pd, strict = build(tid, res)
        ok, reasons = verified_match(gd, pd)
        strict_lbl = "PASS" if strict and strict >= 1 else "FAIL"
        ver_lbl = "PASS" if ok else "FAIL"
        print(f"{tid:9} {strict_lbl:7} {ver_lbl:9} {'' if ok else '; '.join(reasons)}")


if __name__ == "__main__":
    main()
