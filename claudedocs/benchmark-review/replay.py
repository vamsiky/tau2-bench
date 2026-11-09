"""Replay banking_knowledge gold trajectories on a benchmark snapshot.

Runs against a checkout of the reviewed benchmark tag (not this branch), given as
BENCH_DIR. Used to produce the exact step outputs and DB differences in a run's
``pinpoint/*.json`` files and ``inputs/gold_outputs.json``.

    BENCH_DIR=<worktree of the tag> uv run python claudedocs/benchmark-review/replay.py gold task_026
    ... replay.py alt task_026 edits.json      # or "-" to read edits from stdin
    ... replay.py dump-gold <run_dir>          # writes <run_dir>/inputs/gold_outputs.json
    ... replay.py check <run_dir> [task ...]   # validates pinpoint files (prompts/pinpoint.md)

Edits are a JSON list applied to the gold steps (indices are the original gold numbering):
    {"op": "replace", "step": 10, "inner": {...}}   new inner args of a discoverable call
    {"op": "replace", "step": 3, "args": {...}}     new top-level args
    {"op": "drop", "step": 7}
    {"op": "insert_before", "step": 4, "call": CALL}
    {"op": "append", "call": CALL}
CALL is {"name", "requestor", "args"}, or {"tool", "inner"} for a discoverable agent
tool, which expands to unlock + call_discoverable_agent_tool.

"upstream" is the exact agent-DB and user-DB match; "verified" applies the rules of
``_verified_db_match`` in src/tau2/evaluator/evaluator_env.py (copied here because the
snapshot's code predates it).
"""

import copy
import json
import os
import re
import sys

BENCH = os.environ["BENCH_DIR"]
os.environ["TAU2_DATA_DIR"] = BENCH + "/data"
sys.path.insert(0, BENCH + "/src")

from loguru import logger  # noqa: E402

logger.remove()

from tau2.domains.banking_knowledge.environment import (  # noqa: E402
    get_environment,
    get_tasks,
)
from tau2.runner.build import _derive_read_log_allowlist  # noqa: E402

FREE_TEXT = {"accounts": {"closure_reason"}}
INPUT_ERROR_RE = re.compile(
    r"^Error: (?:Missing required parameter|Invalid |Unexpected parameter|"
    r".*(?: is required| are required|must be (?:a number|numbers|an integer|"
    r"positive|a positive|a whole number|exactly \d+ digits)|PIN cannot be"
    r"| not found\.))"
)

_TASKS = {}


def task(tid):
    if not _TASKS:
        _TASKS.update({t.id: t for t in get_tasks()})
    return _TASKS[tid]


def gold_steps(tid):
    return [
        {"name": a.name, "requestor": a.requestor, "args": dict(a.arguments)}
        for a in task(tid).evaluation_criteria.actions
    ]


def run(tid, steps):
    t = task(tid)
    env = get_environment(
        retrieval_variant="bm25", read_log_allowlist=_derive_read_log_allowlist(t)
    )
    init = t.initial_state
    env.set_state(
        initialization_data=init.initialization_data if init else None,
        initialization_actions=init.initialization_actions if init else None,
        message_history=(init.message_history or []) if init else [],
    )
    outs = []
    for s in steps:
        try:
            out = env.make_tool_call(
                tool_name=s["name"], requestor=s["requestor"], **s["args"]
            )
        except Exception as e:  # rejected before the tool runs
            out = f"<EXCEPTION {type(e).__name__}: {e}>"
        outs.append(out if isinstance(out, str) else json.dumps(out, default=str))
    return env, outs


def show_step(label, s, out, limit=1500):
    args = dict(s["args"])
    if s["name"] == "call_discoverable_agent_tool":
        try:
            args["arguments"] = json.loads(args["arguments"])
        except (KeyError, TypeError, json.JSONDecodeError):
            pass
    o = out if len(out) <= limit else out[:limit] + f" …[{len(out)} chars]"
    return f"{label} [{s['requestor']}] {s['name']} {json.dumps(args)}\n   -> {o}"


def expand(call):
    if "tool" in call:
        return [
            {
                "name": "unlock_discoverable_agent_tool",
                "requestor": "assistant",
                "args": {"agent_tool_name": call["tool"]},
            },
            {
                "name": "call_discoverable_agent_tool",
                "requestor": "assistant",
                "args": {
                    "agent_tool_name": call["tool"],
                    "arguments": json.dumps(call["inner"]),
                },
            },
        ]
    return [
        {
            "name": call["name"],
            "requestor": call.get("requestor", "assistant"),
            "args": call.get("args", {}),
        }
    ]


def apply_edits(gold, edits):
    """Return [(step, tag)]; tag is "#i" for an unchanged gold step."""
    slots = [[(copy.deepcopy(s), f"#{i}")] for i, s in enumerate(gold)]
    tail = []
    for e in edits:
        if e["op"] == "append":
            tail += [(s, "+new") for s in expand(e["call"])]
            continue
        i = e["step"]
        if e["op"] == "drop":
            slots[i] = []
        elif e["op"] == "replace":
            st = copy.deepcopy(gold[i])
            if "inner" in e:
                st["args"]["arguments"] = json.dumps(e["inner"])
            if "args" in e:
                st["args"] = e["args"]
            if "name" in e:
                st["name"] = e["name"]
            slots[i] = [(st, f"#{i} CHANGED")]
        elif e["op"] == "insert_before":
            slots[i] = [(s, f"+new before #{i}") for s in expand(e["call"])] + slots[i]
        else:
            raise SystemExit(f"unknown op {e['op']}")
    return [x for sl in slots for x in sl] + tail


def table_diff(g, p, max_rows=8):
    lines = []
    for table in sorted(set(g) | set(p)):
        gt = (g.get(table) or {}).get("data", {})
        pt = (p.get(table) or {}).get("data", {})
        if gt == pt:
            continue
        n = 0
        for k in sorted(set(gt) | set(pt)):
            a, b = gt.get(k), pt.get(k)
            if a == b:
                continue
            n += 1
            if n > max_rows:
                lines.append(f"{table}: … more rows differ")
                break
            if a is None:
                lines.append(
                    f"{table}[{k}]: EXTRA row in agent DB: {json.dumps(b, default=str)[:400]}"
                )
            elif b is None:
                lines.append(
                    f"{table}[{k}]: MISSING row (gold has): {json.dumps(a, default=str)[:400]}"
                )
            else:
                for f in sorted(set(a) | set(b)):
                    if a.get(f) != b.get(f):
                        lines.append(
                            f"{table}[{k}].{f}: gold={json.dumps(a.get(f), default=str)[:200]}"
                            f" agent={json.dumps(b.get(f), default=str)[:200]}"
                        )
    return lines


def strip(db):
    db = copy.deepcopy(db)
    for table, fields in FREE_TEXT.items():
        for rec in ((db.get(table) or {}).get("data") or {}).values():
            for f in fields:
                rec.pop(f, None)
    return db


def tool_names(db):
    rows = ((db.get("agent_discoverable_tools") or {}).get("data") or {}).values()
    return {r.get("tool_name") for r in rows}


def verified(g, p, input_rejected):
    g, p = strip(g), strip(p)
    reasons = []
    if tool_names(g) - tool_names(p):
        reasons.append(
            f"missing required discoverable calls: {sorted(tool_names(g) - tool_names(p))}"
        )
    extra = tool_names(p) - tool_names(g) - input_rejected
    if extra:
        reasons.append(f"extra discoverable calls: {sorted(extra)}")
    for t in sorted(set(g) | set(p)):
        if t != "agent_discoverable_tools" and g.get(t) != p.get(t):
            reasons.append(f"table '{t}' differs")
    return not reasons, reasons


KINDS = {
    "gold_value_wrong",
    "gold_call_missing",
    "gold_call_extra",
    "ambiguous_choice",
    "info_unavailable",
    "instruction_conflict",
    "nl_grading",
    "other",
}


def check(run_dir, ids):
    """Schema, step ranges, and verbatim document/instruction quotes."""
    docs = BENCH + "/data/tau2/domains/banking_knowledge/documents"
    ids = ids or sorted(f[:-5] for f in os.listdir(f"{run_dir}/pinpoint"))
    bad = 0
    for tid in ids:
        d = json.load(open(f"{run_dir}/pinpoint/{tid}.json"))
        n_issues = len(json.load(open(f"{run_dir}/findings/{tid}.json"))["issues"])
        t = task(tid)
        n_steps = len(t.evaluation_criteria.actions)
        errs = []
        if d.get("task_id") != tid:
            errs.append("task_id")
        if not d.get("reason") or len(d["reason"].split()) > 35:
            errs.append("reason missing or > 35 words")
        if not d.get("points"):
            errs.append("no points")
        for k, p in enumerate(d.get("points", [])):
            w = f"points[{k}]"
            if not 1 <= p.get("issue", 0) <= n_issues:
                errs.append(f"{w}.issue out of range")
            if p.get("kind") not in KINDS:
                errs.append(f"{w}.kind {p.get('kind')}")
            st = p.get("step")
            if st is not None and not (isinstance(st, int) and 0 <= st < n_steps):
                errs.append(f"{w}.step {st} not in 0..{n_steps - 1}")
            if len((p.get("conflict") or "").split()) > 45:
                errs.append(f"{w}.conflict > 45 words")
            for r in p.get("refs", []):
                src, q = r.get("source", ""), r.get("quote", "")
                if src.startswith("doc_"):
                    path = f"{docs}/{src}.json"
                    if not os.path.exists(path):
                        errs.append(f"{w} unknown doc {src}")
                    elif q not in json.load(open(path))["content"]:
                        errs.append(f"{w} quote not verbatim in {src}: {q[:60]!r}")
                elif src == "instructions" and q not in str(
                    t.user_scenario.instructions
                ):
                    errs.append(f"{w} quote not verbatim in instructions: {q[:60]!r}")
            sc = p.get("scorer")
            verdicts = (
                {sc.get("upstream"), sc.get("verified"), sc.get("action", "n/a")}
                if sc
                else set()
            )
            if not verdicts <= {"PASS", "FAIL", "n/a"}:
                errs.append(f"{w}.scorer verdicts must be PASS/FAIL/n/a")
            basis = [
                str(getattr(b, "value", b))
                for b in t.evaluation_criteria.reward_basis or []
            ]
            if sc and "ACTION" in basis and sc.get("action") not in ("PASS", "FAIL"):
                errs.append(f"{w}.scorer.action required (task graded on ACTION)")
        print(tid, "OK" if not errs else "ERRORS: " + "; ".join(errs))
        bad += bool(errs)
    return bad


def main():
    mode = sys.argv[1]
    if mode == "check":
        sys.exit(1 if check(sys.argv[2], sys.argv[3:]) else 0)
    if mode == "dump-gold":
        run_dir = sys.argv[2]
        task("task_001")
        out = {tid: run(tid, gold_steps(tid))[1] for tid in sorted(_TASKS)}
        with open(f"{run_dir}/inputs/gold_outputs.json", "w") as f:
            json.dump(out, f, indent=1, ensure_ascii=False)
        print(f"wrote gold outputs for {len(out)} tasks")
        return
    tid = sys.argv[2]
    gold = gold_steps(tid)
    genv, gouts = run(tid, gold)
    if mode == "gold":
        for i, (s, o) in enumerate(zip(gold, gouts)):
            print(show_step(f"#{i}", s, o, limit=int(os.environ.get("PP_LIMIT", 1500))))
        return
    src = sys.stdin.read() if sys.argv[3] == "-" else open(sys.argv[3]).read()
    tagged = apply_edits(gold, json.loads(src))
    steps = [s for s, _ in tagged]
    aenv, aouts = run(tid, steps)
    print("== changed / new steps (output in the alternative run)")
    for (s, tag), o in zip(tagged, aouts):
        if tag.startswith("#") and "CHANGED" not in tag:
            if o == gouts[int(tag[1:])]:
                continue
            tag += " (same call, output differs from gold)"
        print(show_step(tag, s, o))
    gdb, adb = genv.tools.db.model_dump(), aenv.tools.db.model_dump()
    print("== DB fields that differ (gold vs agent)")
    for line in table_diff(gdb, adb) or ["(none)"]:
        print("  " + line)
    outcomes = {}
    for s, o in zip(steps, aouts):
        if s["name"] == "call_discoverable_agent_tool":
            n = s["args"].get("agent_tool_name")
            outcomes[n] = outcomes.get(n, True) and bool(INPUT_ERROR_RE.match(o))
    up = (
        genv.get_db_hash() == aenv.get_db_hash()
        and genv.get_user_db_hash() == aenv.get_user_db_hash()
    )
    ok, reasons = verified(gdb, adb, {n for n, r in outcomes.items() if r})
    print(f"== upstream exact match: {'PASS' if up else 'FAIL'}")
    print(f"== verified scorer: {'PASS' if ok else 'FAIL'} {reasons}")
    # ACTION grading: every gold action must match some call (name + compared args).
    from tau2.data_model.message import ToolCall

    calls = [
        ToolCall(
            id=str(i), name=s["name"], arguments=s["args"], requestor=s["requestor"]
        )
        for i, s in enumerate(steps)
    ]
    missing = [
        f"#{i} {a.name}"
        for i, a in enumerate(task(tid).evaluation_criteria.actions)
        if not any(a.compare_with_tool_call(c) for c in calls)
    ]
    basis = [
        str(getattr(b, "value", b))
        for b in task(tid).evaluation_criteria.reward_basis or []
    ]
    print(
        f"== action check: {'PASS' if not missing else 'FAIL missing ' + str(missing)}"
        f"  (this task is graded on {basis})"
    )


if __name__ == "__main__":
    main()
