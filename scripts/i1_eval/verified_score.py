#!/usr/bin/env python3
"""Principled "verified" re-scorer (SABER tau-Bench-Verified style) for I1
(banking_knowledge) trajectories, applied to an existing results.json.

Uses the same comparison as the SDK driver's verified scorer
(`_verified_db_match` in src/tau2/evaluator/evaluator_env.py):
  1. agent_discoverable_tools: gold's called tools must be a SUBSET of the agent's
     (a MISSING required call still fails, e.g. task_047). An extra call is allowed
     only if every call to that tool was rejected for bad input.
  2. Bank-account closure_reason (free text with a hidden default) is dropped before
     comparing, which unblocks task_067's descriptive closure reason.
Every other table (accounts, applications, ...) is compared exactly.

Usage:
    uv run python scripts/i1_eval/verified_score.py <task_id> <results.json>
    uv run python scripts/i1_eval/verified_score.py            # built-in I1 table

Reconstructed from the 2026-06-24 I1 investigation session.
"""

import os
import sys

# claude_sdk_loop_eval parses argv at import time; capture our args, then neutralize.
_A = list(sys.argv)
sys.argv = ["x"]

# Repo root, so `examples.*` is importable when run as `python scripts/i1_eval/<x>.py`.
sys.path.insert(
    0, os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
)

from examples.agents.claude_sdk_loop_eval import _retrieval_env_kwargs  # noqa: E402
from tau2.data_model.simulation import Results  # noqa: E402
from tau2.evaluator.evaluator_env import (  # noqa: E402
    _input_rejected_discoverable_tools,
    _verified_db_match,
)
from tau2.runner import build_environment, get_tasks  # noqa: E402
from tau2.runner.build import _derive_read_log_allowlist  # noqa: E402

DOMAIN = "banking_knowledge"
ek = _retrieval_env_kwargs(DOMAIN, "alltools", None)

# Default per-task best-known result files (used when no CLI args are given).
DEFAULT_ITEMS = [
    ("task_047", "data/simulations/i1_fix5/results.json"),
    (
        "task_058",
        "data/simulations/i1_fix4/results.json",
    ),  # fix4 = correct Silver selection
    ("task_063", "data/simulations/i1_fix5/results.json"),
    ("task_064", "data/simulations/i1_fix5/results.json"),
    ("task_067", "data/simulations/i1_fix1/results.json"),
]


def build(tid, res):
    """Return (gold_db, predicted_db, strict_reward, messages) for a task/result pair."""
    task = get_tasks(DOMAIN, task_ids=[tid])[0]
    sim = next(s for s in Results.load(res).simulations if s.task_id == tid)
    init = task.initial_state

    def mk():
        e = build_environment(
            DOMAIN,
            env_kwargs={
                **ek,
                "task": task,
                "read_log_allowlist": _derive_read_log_allowlist(task),
            },
        )
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
        sim.messages,
    )


def verified_match(gd, pd, messages):
    """Return (is_match, reasons). gd = gold DB dump, pd = predicted DB dump."""
    return _verified_db_match(gd, pd, _input_rejected_discoverable_tools(messages))


def main():
    if len(_A) >= 3:
        items = [(_A[1], _A[2])]
    else:
        items = DEFAULT_ITEMS
    print(f"{'task':9} {'strict':7} {'verified':9} reason")
    for tid, res in items:
        gd, pd, strict, messages = build(tid, res)
        ok, reasons = verified_match(gd, pd, messages)
        strict_lbl = "PASS" if strict and strict >= 1 else "FAIL"
        ver_lbl = "PASS" if ok else "FAIL"
        print(f"{tid:9} {strict_lbl:7} {ver_lbl:9} {'' if ok else '; '.join(reasons)}")


if __name__ == "__main__":
    main()
