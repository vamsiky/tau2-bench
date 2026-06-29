#!/usr/bin/env python3
"""Best-of-N re-scorer for I1 (banking_knowledge): across all trials of a run,
report whether ANY trial passes under the strict reward and under the verified
scorer (scripts/i1_eval/verified_score.py).

Usage:
    uv run python scripts/i1_eval/bestof.py
    uv run python scripts/i1_eval/bestof.py "data/simulations/i1_g3i3_{task}/results.json"

The single optional arg is a results-path template containing `{task}`; it
defaults to the iteration-3 (fix4, best-of-2) parallel layout.

Reconstructed from the 2026-06-24 I1 investigation session.
"""
import os
import sys

_A = list(sys.argv)
sys.argv = ["x"]

# Same-dir import: this script's directory is sys.path[0] under `python <path>`.
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from tau2.runner import get_tasks, build_environment  # noqa: E402
from tau2.data_model.simulation import Results  # noqa: E402
from examples.agents.claude_sdk_loop_eval import _retrieval_env_kwargs  # noqa: E402
from verified_score import verified_match  # noqa: E402

DOMAIN = "banking_knowledge"
ek = _retrieval_env_kwargs(DOMAIN, "alltools", None)
I1_TASKS = ["task_047", "task_058", "task_063", "task_064", "task_067"]
PATTERN = _A[1] if len(_A) > 1 else "data/simulations/i1_g3i3_{task}/results.json"


def score_sim(task, sim, init):
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
    ok, reasons = verified_match(g.tools.db.model_dump(), p.tools.db.model_dump())
    return ok, reasons, (sim.reward_info.reward if sim.reward_info else 0)


def main():
    print(f"{'task':9} {'strict(best)':12} {'verified(best)':14} note")
    for t in I1_TASKS:
        task = get_tasks(DOMAIN, task_ids=[t])[0]
        init = task.initial_state
        sims = Results.load(PATTERN.format(task=t)).simulations
        best_v = False
        best_s = 0
        note = ""
        for s in sims:
            ok, reasons, r = score_sim(task, s, init)
            best_s = max(best_s, 1 if r and r >= 1 else 0)
            if ok:
                best_v = True
            elif not best_v:
                note = "; ".join(reasons)[:70]
        strict_lbl = "PASS" if best_s else "FAIL"
        ver_lbl = "PASS" if best_v else "FAIL"
        print(f"{t:9} {strict_lbl:12} {ver_lbl:14} {note if not best_v else ''}")


if __name__ == "__main__":
    main()
