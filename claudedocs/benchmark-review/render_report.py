"""Render a benchmark-review run into review.md and review.html.

The reviewers write judgments only (``findings/<task_id>.json``, optional
``verification/*.json`` and ``synthesis.json``). Everything copied from the benchmark
itself - customer instructions, required documents, gold actions - is read here from
the benchmark's git ref, so the report always shows the exact task text that was
reviewed. Optional ``pinpoint/<task_id>.json`` files give each verdict's exact step,
values, and document text, and ``inputs/gold_outputs.json`` holds each gold step's
output (both written with ``replay.py``).

Usage:
    python claudedocs/benchmark-review/render_report.py \
        claudedocs/benchmark-review/<domain>/<date>-<version>
"""

from __future__ import annotations

import argparse
import html
import json
import subprocess
from collections import Counter
from pathlib import Path

SEVERITIES = ["Blocker", "Major", "Minor", "None"]
HERE = Path(__file__).resolve().parent


class GitTree:
    """Read files from a git ref without checking it out."""

    def __init__(self, repo: Path, ref: str):
        self.repo, self.ref = repo, ref
        self.commit = self._git("rev-parse", f"{ref}^{{commit}}").strip()

    def _git(self, *args: str) -> str:
        return subprocess.run(
            ["git", "-C", str(self.repo), *args],
            check=True,
            capture_output=True,
            text=True,
        ).stdout

    def ls(self, path: str) -> list[str]:
        return self._git("ls-tree", "-r", "--name-only", self.ref, path).split()

    def read_json(self, path: str):
        return json.loads(self._git("show", f"{self.ref}:{path}"))


def load_run(run_dir: Path, allow_partial: bool = False) -> dict:
    meta = json.loads((run_dir / "run.json").read_text())
    repo = Path(
        subprocess.run(
            ["git", "-C", str(run_dir), "rev-parse", "--show-toplevel"],
            check=True,
            capture_output=True,
            text=True,
        ).stdout.strip()
    )
    tree = GitTree(repo, meta["benchmark_ref"])
    domain = meta["domain"]
    base = f"data/tau2/domains/{domain}"

    tasks = {}
    for path in tree.ls(f"{base}/tasks"):
        task = tree.read_json(path)
        tasks[task["id"]] = task

    pinpoints = {}
    for path in sorted((run_dir / "pinpoint").glob("*.json")):
        p = json.loads(path.read_text())
        pinpoints[p["task_id"]] = p
    cited = {
        r["source"]
        for p in pinpoints.values()
        for point in p.get("points", [])
        for r in point.get("refs", [])
        if r.get("source", "").startswith("doc_")
    }
    outputs_path = run_dir / "inputs" / "gold_outputs.json"
    gold_outputs = json.loads(outputs_path.read_text()) if outputs_path.exists() else {}

    doc_ids = sorted(
        {d for t in tasks.values() for d in t.get("required_documents") or []} | cited
    )
    documents = {}
    for doc_id in doc_ids:
        try:
            doc = tree.read_json(f"{base}/documents/{doc_id}.json")
            documents[doc_id] = {
                "title": doc.get("title", doc_id),
                "content": doc["content"],
            }
        except subprocess.CalledProcessError:
            documents[doc_id] = {"title": doc_id, "content": None}

    findings = {}
    for path in sorted((run_dir / "findings").glob("*.json")):
        f = json.loads(path.read_text())
        if not meta.get("prior_run"):
            f.pop("prior_status", None)
            f.pop("prior_note", None)
        findings[f["task_id"]] = f
    missing = sorted(set(tasks) - set(findings))
    if missing and not allow_partial:
        raise SystemExit(f"findings missing for {len(missing)} tasks: {missing}")
    tasks = {tid: t for tid, t in tasks.items() if tid in findings}

    verdicts, verification = (
        {},
        {"fact_checks": [], "calibration_notes": [], "methodology_notes": []},
    )
    for path in (
        sorted((run_dir / "verification").glob("*.json"))
        if (run_dir / "verification").exists()
        else []
    ):
        v = json.loads(path.read_text())
        verdicts.update(v.get("task_verdicts", {}))
        verification["fact_checks"] += v.get("fact_checks", [])
        verification["calibration_notes"] += v.get("calibration_notes", [])
        if v.get("methodology_note"):
            verification["methodology_notes"].append(v["methodology_note"])

    prior_path = run_dir / "inputs" / "prior_findings.json"
    prior = (
        json.loads(prior_path.read_text())
        if meta.get("prior_run") and prior_path.exists()
        else {"tasks": {}}
    )
    synthesis_path = run_dir / "synthesis.json"
    synthesis = (
        json.loads(synthesis_path.read_text()) if synthesis_path.exists() else {}
    )

    # Optional cross-run reconciliation: {"file": <path relative to run_dir>,
    # "side": <key prefix, e.g. "upstream">}. It settles disagreements between
    # independent runs and takes precedence over reviewer and verifier severities.
    reconciled = {}
    rec_cfg = meta.get("reconciliation")
    if rec_cfg:
        rec = json.loads((run_dir / rec_cfg["file"]).read_text())
        side = rec_cfg["side"]
        for tid, r in rec.get("tasks", {}).items():
            reconciled[tid] = {
                "severity": r[f"{side}_severity"],
                "before": r.get(f"prior_{side}"),
                "cause": r.get("difference_cause"),
                "why_runs_differed": r.get("why_runs_differed"),
                "reason": r.get("reason", ""),
                "evidence": r.get("evidence", []),
            }

    return {
        "meta": {**meta, "benchmark_commit": tree.commit},
        "tasks": tasks,
        "documents": documents,
        "findings": findings,
        "verdicts": verdicts,
        "verification": verification,
        "prior": prior,
        "synthesis": synthesis,
        "reconciled": reconciled,
        "pinpoints": pinpoints,
        "gold_outputs": gold_outputs,
    }


def final_severity(run: dict, task_id: str) -> str:
    """Reconciled severity, else the verifier's, else the reviewer's."""
    r = run["reconciled"].get(task_id)
    if r and r.get("severity") in SEVERITIES:
        return r["severity"]
    v = run["verdicts"].get(task_id)
    if v and v.get("verified_severity") in SEVERITIES:
        return v["verified_severity"]
    return run["findings"][task_id]["severity"]


def build_rows(run: dict) -> list[dict]:
    rows = []
    for task_id in sorted(run["tasks"]):
        f = run["findings"][task_id]
        p = run["prior"]["tasks"].get(task_id, {})
        v = run["verdicts"].get(task_id, {})
        rows.append(
            {
                "task_id": task_id,
                "severity": final_severity(run, task_id),
                "review_severity": f["severity"],
                "verdict": v.get("verdict", "Not sampled"),
                "verified_severity": v.get("verified_severity", "-"),
                "reconciled": task_id in run["reconciled"],
                "prior_severity": p.get("severity", "-"),
                "prior_status": f.get("prior_status", "-"),
                "headline": f.get("headline", ""),
                "reason": run["pinpoints"].get(task_id, {}).get("reason")
                or f.get("headline", ""),
                "ratings": f.get("ratings", {}),
                "classes": sorted({i.get("class", "") for i in f.get("issues", [])}),
                "reward_basis": run["tasks"][task_id]["evaluation_criteria"].get(
                    "reward_basis"
                )
                or [],
            }
        )
    return rows


# ---------------------------------------------------------------- markdown


def md_cell(text) -> str:
    return str(text).replace("|", "\\|").replace("\n", " ")


def md_call(c: dict | None) -> str:
    if not c:
        return "-"
    if c.get("call") == "(no call)":
        return "no tool call"
    if not c.get("args") and not c.get("output"):
        return f"skips `{md_cell(c.get('call', ''))}`"
    args = ", ".join(f"{k}={json.dumps(v)}" for k, v in (c.get("args") or {}).items())
    return f"`{md_cell(c.get('call', ''))}({md_cell(args)})`"


def md_pinpoint(p: dict) -> list[str]:
    out = [f"**Why:** {p['reason']}", ""]
    for n, pt in enumerate(p.get("points", []), 1):
        step = (
            f"gold step #{pt['step']}" if pt.get("step") is not None else "no gold step"
        )
        out += [
            f"**{n}. {pt['title']}** ({pt['severity']} · {pt['kind']} · {step})",
            "",
            *([f"*{pt['issue_note']}*", ""] if pt.get("issue_note") else []),
            "| | Call | Output |",
            "|---|---|---|",
            f"| Gold | {md_call(pt.get('gold'))} | {md_cell((pt.get('gold') or {}).get('output', '-'))} |",
        ]
        alt = pt.get("doc_faithful")
        if alt:
            note = f" ({alt['note']})" if alt.get("note") else ""
            out.append(
                f"| Alternative path | {md_call(alt)}{md_cell(note)} | {md_cell(alt.get('output', '-'))} |"
            )
        out.append("")
        for r in pt.get("refs", []):
            out.append(f'- **{r["source"]}:** "{" ".join(r["quote"].split())}"')
        out.append(f"- **Where it differs:** {pt['conflict']}")
        sc = pt.get("scorer")
        if sc:
            out.append(
                f"- **Scorer:** `{sc.get('field', '-')}` → DB upstream {sc['upstream']}, "
                f"verified {sc['verified']}"
                + (
                    f", actions {sc['action']}"
                    if sc.get("action") in ("PASS", "FAIL")
                    else ""
                )
            )
        out.append("")
    if p.get("discrepancy"):
        out += [f"*Replay note:* {p['discrepancy']}", ""]
    return out


def render_md(run: dict, rows: list[dict]) -> str:
    m, syn = run["meta"], run["synthesis"]
    counts = Counter(r["severity"] for r in rows)
    prior_counts = Counter(r["prior_severity"] for r in rows)
    has_prior = bool(m.get("prior_run"))
    out = [
        f"# `{m['domain']}` benchmark correctness review — {m['benchmark_version']}",
        "",
        f"**Benchmark:** `{m['benchmark_ref']}` (`{m['benchmark_commit'][:10]}`) · "
        f"**Run date:** {m['run_date']} · **Reviewer:** {m.get('reviewer', '-')} · "
        f"**Effort:** {m.get('effort', '-')}"
        + (f" · **Prior review:** {m['prior_run']}" if has_prior else ""),
        "",
        "The interactive version (`review.html`) shows each task's customer instructions, "
        "required documents, gold trajectory, and findings side by side.",
        "",
        "## Summary",
        "",
        "| Severity | Now | Prior |" if has_prior else "| Severity | Tasks |",
        "|---|---|---|" if has_prior else "|---|---|",
    ]
    for s in SEVERITIES:
        prior_cell = f" {prior_counts.get(s, 0)} |" if has_prior else ""
        out.append(f"| {s} | {counts.get(s, 0)} |{prior_cell}")
    if syn.get("summary"):
        out += ["", syn["summary"]]
    if syn.get("systemic_issues"):
        out += ["", "## Systemic issues", ""]
        for i, s in enumerate(syn["systemic_issues"], 1):
            out.append(
                f"{i}. **{s['title']}** ({', '.join(s.get('tasks', []))}). {s['description']}"
            )
    changed = [
        r
        for r in rows
        if r["prior_status"] in ("resolved", "changed", "new")
        or r["severity"] != r["prior_severity"]
    ]
    if has_prior:
        out += [
            "",
            "## Changes since the prior review",
            "",
            "| Task | Prior | Now | Status | Why |",
            "|---|---|---|---|---|",
        ]
        for r in changed:
            out.append(
                f"| {r['task_id']} | {r['prior_severity']} | {r['severity']} | {r['prior_status']} | {md_cell(r['reason'])} |"
            )
    prior_head = " Prior |" if has_prior else ""
    out += [
        "",
        "## All tasks",
        "",
        f"| Task | Final | Reviewer | Verifier | Reconciled |{prior_head} Instr. | Docs det. | Cx | Ordering | Gold ok | Why |",
        "|---" * (12 if has_prior else 11) + "|",
    ]
    for r in rows:
        g = r["ratings"]
        prior_cell = f" {r['prior_severity']} |" if has_prior else ""
        out.append(
            f"| {r['task_id']} | {r['severity']} | {r['review_severity']} | "
            f"{r['verdict']} ({r['verified_severity']}) | {'yes' if r['reconciled'] else '-'} |{prior_cell} "
            f"{g.get('instructions_sufficient', '-')} | {g.get('docs_deterministic', '-')} | "
            f"{g.get('reasoning_complexity', '-')} | {g.get('ordering_dependency', '-')} | "
            f"{g.get('gold_consistent', '-')} | {md_cell(r['reason'])} |"
        )
    shown = ("Blocker", "Major", "Minor") if run["pinpoints"] else ("Blocker", "Major")
    out += ["", f"## Findings ({', '.join(shown)})", ""]
    if run["pinpoints"]:
        out += [
            "Each finding shows the gold step where the task breaks, the path an agent "
            "that follows the documents takes there instead (both replayed on the "
            "benchmark snapshot), the exact text that disagrees with the gold, and what "
            "the scorer compares. For a Minor issue where the gold is right but easy to "
            "miss, the alternative is the plausible misreading. Full write-ups are in "
            "`findings/` and `verification/`.",
            "",
        ]
    for r in rows:
        if r["severity"] not in shown:
            continue
        f = run["findings"][r["task_id"]]
        v = run["verdicts"].get(r["task_id"])
        out += [f"### {r['task_id']} — {r['severity']}", ""]
        if r["task_id"] in run["pinpoints"]:
            out += md_pinpoint(run["pinpoints"][r["task_id"]])
            continue
        out += [f"**{f['headline']}**", ""]
        for i in f.get("issues", []):
            out.append(
                f"- **{i.get('class')} ({i.get('severity')})** — {i.get('summary')}"
            )
            for e in i.get("evidence", []):
                out.append(f"  - `{e}`" if len(e) < 160 else f"  - {e}")
            if i.get("why_it_matters"):
                out.append(f"  - *Why it matters:* {i['why_it_matters']}")
            if i.get("suggested_fix"):
                out.append(f"  - *Fix:* {i['suggested_fix']}")
        if v:
            out += [
                "",
                f"*Verifier: {v.get('verdict')} ({v.get('review_severity')} → {v.get('verified_severity')}).* {v.get('note', '')}",
            ]
        rec = run["reconciled"].get(r["task_id"])
        if rec:
            out += [
                "",
                f"*Reconciled across runs: {rec.get('before')} → {rec['severity']} ({rec.get('why_runs_differed')}).* {rec['reason']}",
            ]
        out.append("")
    return "\n".join(out) + "\n"


# ---------------------------------------------------------------- html


def render_html(run: dict, rows: list[dict]) -> str:
    payload = {
        "meta": run["meta"],
        "rows": rows,
        "tasks": {
            tid: {
                "instructions": t["user_scenario"].get("instructions"),
                "persona": t["user_scenario"].get("persona"),
                "purpose": (t.get("description") or {}).get("purpose"),
                "notes": (t.get("description") or {}).get("notes"),
                "required_documents": t.get("required_documents") or [],
                "actions": t["evaluation_criteria"].get("actions") or [],
                "communicate_info": t["evaluation_criteria"].get("communicate_info")
                or [],
                "nl_assertions": t["evaluation_criteria"].get("nl_assertions") or [],
                "reward_basis": t["evaluation_criteria"].get("reward_basis") or [],
                "initial_state": t.get("initial_state"),
                "outputs": run["gold_outputs"].get(tid, []),
            }
            for tid, t in run["tasks"].items()
        },
        "documents": run["documents"],
        "findings": run["findings"],
        "verdicts": run["verdicts"],
        "verification": run["verification"],
        "reconciled": run["reconciled"],
        "prior": run["prior"]["tasks"],
        "synthesis": run["synthesis"],
        "pinpoints": run["pinpoints"],
    }
    data = json.dumps(payload, ensure_ascii=False).replace("</", "<\\/")
    template = (HERE / "report_template.html").read_text()
    title = run["meta"].get("title") or (
        f"{run['meta']['domain']} review {run['meta']['benchmark_version']}"
    )
    return template.replace("{{TITLE}}", html.escape(title)).replace("{{DATA}}", data)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("run_dir", type=Path)
    parser.add_argument(
        "--allow-partial",
        action="store_true",
        help="render only the tasks that have findings so far (preview)",
    )
    args = parser.parse_args()
    run = load_run(args.run_dir, allow_partial=args.allow_partial)
    rows = build_rows(run)
    (args.run_dir / "review.md").write_text(render_md(run, rows))
    (args.run_dir / "review.html").write_text(render_html(run, rows))
    counts = Counter(r["severity"] for r in rows)
    print(
        f"rendered {len(rows)} tasks: "
        + ", ".join(f"{s}={counts.get(s, 0)}" for s in SEVERITIES)
    )


if __name__ == "__main__":
    main()
