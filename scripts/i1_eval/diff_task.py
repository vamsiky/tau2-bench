#!/usr/bin/env python3
"""Diff a task's GOLD final DB against the AGENT's predicted final DB (faithful
`set_state` replay of the recorded trajectory). Useful for seeing exactly which
table/field caused a strict-scorer FAIL.

Usage:
    uv run python scripts/i1_eval/diff_task.py <task_id> <results.json>
    uv run python scripts/i1_eval/diff_task.py            # task_064 / i1_fix3 defaults

Legend in output: `+AGENT` = present only in agent DB, `-GOLD` = present only in
gold DB, `~` = differing value.

Reconstructed from the 2026-06-24 I1 investigation session.
"""
import sys

_A = list(sys.argv)
sys.argv = ["x"]

from tau2.runner import get_tasks, build_environment  # noqa: E402
from tau2.data_model.simulation import Results  # noqa: E402
from examples.agents.claude_sdk_loop_eval import _retrieval_env_kwargs  # noqa: E402

DOMAIN = "banking_knowledge"
ek = _retrieval_env_kwargs(DOMAIN, "alltools", None)

TID = _A[1] if len(_A) > 1 else "task_064"
RES = _A[2] if len(_A) > 2 else "data/simulations/i1_fix3/results.json"

task = get_tasks(DOMAIN, task_ids=[TID])[0]
sim = next(s for s in Results.load(RES).simulations if s.task_id == TID)
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
gd, pd = g.tools.db.model_dump(), p.tools.db.model_dump()


def walk(a, b, path=""):
    if isinstance(a, dict) and isinstance(b, dict):
        for k in sorted(set(a) | set(b)):
            if k not in a:
                print(f"  +AGENT {path}/{k} = {repr(b[k])[:110]}")
            elif k not in b:
                print(f"  -GOLD  {path}/{k} = {repr(a[k])[:110]}")
            else:
                walk(a[k], b[k], f"{path}/{k}")
    elif isinstance(a, list) and isinstance(b, list):
        if len(a) != len(b):
            print(f"  ~len {path}: gold={len(a)} agent={len(b)}")
        for i in range(min(len(a), len(b))):
            walk(a[i], b[i], f"{path}[{i}]")
    elif a != b:
        print(f"  ~ {path}: gold={repr(a)[:80]} | agent={repr(b)[:80]}")


print(f"==== {TID} DB diff (gold vs agent) ====")
for t in sorted(set(gd) | set(pd)):
    if gd.get(t) != pd.get(t):
        print(f"## {t}")
        walk(gd.get(t), pd.get(t), "")
