"""Render a benchmark-review run into review.md and review.html.

The reviewers write judgments only (``findings/<task_id>.json``, optional
``verification/*.json`` and ``synthesis.json``). Everything copied from the benchmark
itself - customer instructions, required documents, gold actions - is read here from
the benchmark's git ref, so the report always shows the exact task text that was
reviewed.

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

    doc_ids = sorted(
        {d for t in tasks.values() for d in t.get("required_documents") or []}
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
    prior = json.loads(prior_path.read_text()) if prior_path.exists() else {"tasks": {}}
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


def render_md(run: dict, rows: list[dict]) -> str:
    m, syn = run["meta"], run["synthesis"]
    counts = Counter(r["severity"] for r in rows)
    prior_counts = Counter(r["prior_severity"] for r in rows)
    out = [
        f"# `{m['domain']}` benchmark correctness review — {m['benchmark_version']}",
        "",
        f"**Benchmark:** `{m['benchmark_ref']}` (`{m['benchmark_commit'][:10]}`) · "
        f"**Run date:** {m['run_date']} · **Reviewer:** {m.get('reviewer', '-')} · "
        f"**Effort:** {m.get('effort', '-')} · "
        f"**Prior review:** {m.get('prior_run', '-')}",
        "",
        "The interactive version (`review.html`) shows each task's customer instructions, "
        "required documents, gold trajectory, and findings side by side.",
        "",
        "## Summary",
        "",
        "| Severity | Now | Prior |",
        "|---|---|---|",
    ]
    for s in SEVERITIES:
        out.append(f"| {s} | {counts.get(s, 0)} | {prior_counts.get(s, 0)} |")
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
    out += [
        "",
        "## Changes since the prior review",
        "",
        "| Task | Prior | Now | Status | Headline |",
        "|---|---|---|---|---|",
    ]
    for r in changed:
        out.append(
            f"| {r['task_id']} | {r['prior_severity']} | {r['severity']} | {r['prior_status']} | {md_cell(r['headline'])} |"
        )
    out += [
        "",
        "## All tasks",
        "",
        "| Task | Final | Reviewer | Verifier | Reconciled | Prior | Instr. | Docs det. | Cx | Ordering | Gold ok | Headline |",
        "|---|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for r in rows:
        g = r["ratings"]
        out.append(
            f"| {r['task_id']} | {r['severity']} | {r['review_severity']} | "
            f"{r['verdict']} ({r['verified_severity']}) | {'yes' if r['reconciled'] else '-'} | {r['prior_severity']} | "
            f"{g.get('instructions_sufficient', '-')} | {g.get('docs_deterministic', '-')} | "
            f"{g.get('reasoning_complexity', '-')} | {g.get('ordering_dependency', '-')} | "
            f"{g.get('gold_consistent', '-')} | {md_cell(r['headline'])} |"
        )
    out += ["", "## Findings (Blocker and Major)", ""]
    for r in rows:
        if r["severity"] not in ("Blocker", "Major"):
            continue
        f = run["findings"][r["task_id"]]
        v = run["verdicts"].get(r["task_id"])
        out += [f"### {r['task_id']} — {r['severity']}", "", f"**{f['headline']}**", ""]
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
