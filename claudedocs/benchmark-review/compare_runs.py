"""Compare benchmark-review runs of the same benchmark version task by task.

Measures agreement at each stage (reviewer, verifier, and reconciled when a
reconciliation file is given) against a same-scorer repeat that measures run-to-run
judgment noise.

Usage:
    python claudedocs/benchmark-review/compare_runs.py \
        claudedocs/benchmark-review/<domain>/comparison-<date>-<version>.json

The spec names the runs to compare, an optional same-scorer repeat used as the noise
baseline, and an optional reconciliation file. Without one, each run's verified
severity is final and every differing task shows both runs' reasoning. Output is
written next to the spec as .md and .html.
"""

from __future__ import annotations

import argparse
import html
import json
from collections import Counter
from pathlib import Path

SEVERITIES = ["Blocker", "Major", "Minor", "None"]
STAGES = [
    ("reviewer", "Reviewers"),
    ("verified", "After verification"),
    ("reconciled", "After reconciliation"),
]


def load_run(run_dir: Path) -> dict:
    findings = {
        json.loads(p.read_text())["task_id"]: json.loads(p.read_text())
        for p in sorted((run_dir / "findings").glob("*.json"))
    }
    verdicts = {}
    vdir = run_dir / "verification"
    if vdir.exists():
        for p in sorted(vdir.glob("*.json")):
            verdicts.update(json.loads(p.read_text()).get("task_verdicts", {}))
    meta = json.loads((run_dir / "run.json").read_text())
    return {"findings": findings, "verdicts": verdicts, "meta": meta}


def reviewer(run: dict, t: str) -> str:
    return run["findings"][t]["severity"]


def verified(run: dict, t: str) -> str:
    v = run["verdicts"].get(t, {}).get("verified_severity")
    return v if v in SEVERITIES else reviewer(run, t)


def explanation(run: dict, t: str) -> str:
    """The verifier's note where it changed the severity, else the reviewer's headline."""
    v = run["verdicts"].get(t, {})
    if v.get("verified_severity") in SEVERITIES and v["verified_severity"] != reviewer(
        run, t
    ):
        return v.get("note", "")
    return run["findings"][t].get("headline", "")


def agreement(a: dict[str, str], b: dict[str, str]) -> tuple[int, list[str]]:
    diff = sorted(t for t in a if a[t] != b.get(t))
    return len(a) - len(diff), diff


def build(spec_path: Path) -> dict:
    spec = json.loads(spec_path.read_text())
    base = spec_path.parent
    runs = {r["label"]: load_run(base / r["dir"]) for r in spec["runs"]}
    a_label, b_label = [r["label"] for r in spec["runs"]]
    a_side, b_side = [r["side"] for r in spec["runs"]]
    A, B = runs[a_label], runs[b_label]
    rec_data = (
        json.loads((base / spec["reconciliation"]).read_text())
        if spec.get("reconciliation")
        else {}
    )
    rec = rec_data.get("tasks", {})
    baseline = (
        load_run(base / spec["noise_baseline"]["dir"])
        if spec.get("noise_baseline")
        else None
    )
    prior = json.loads(
        (base / spec["runs"][0]["dir"] / "inputs" / "prior_findings.json").read_text()
    )["tasks"]

    tasks = sorted(A["findings"])
    stage = {
        "reviewer": (
            {t: reviewer(A, t) for t in tasks},
            {t: reviewer(B, t) for t in tasks},
        ),
        "verified": (
            {t: verified(A, t) for t in tasks},
            {t: verified(B, t) for t in tasks},
        ),
    }
    final_a = {
        t: rec[t][f"{a_side}_severity"] if t in rec else stage["verified"][0][t]
        for t in tasks
    }
    final_b = {
        t: rec[t][f"{b_side}_severity"] if t in rec else stage["verified"][1][t]
        for t in tasks
    }
    if spec.get("reconciliation"):
        stage["reconciled"] = (final_a, final_b)

    rows = []
    for t in tasks:
        r = rec.get(t, {})
        rows.append(
            {
                "task": t,
                "prior": prior.get(t, {}).get("severity", "-"),
                "baseline": reviewer(baseline, t)
                if baseline and t in baseline["findings"]
                else "-",
                "a_rev": stage["reviewer"][0][t],
                "a_ver": stage["verified"][0][t],
                "b_rev": stage["reviewer"][1][t],
                "b_ver": stage["verified"][1][t],
                "a_fin": final_a[t],
                "b_fin": final_b[t],
                "cause": r.get("difference_cause", "")
                if final_a[t] != final_b[t]
                else "",
                "why": r.get("why_runs_differed", ""),
                "reason": r.get("reason", ""),
                "a_why": explanation(A, t),
                "b_why": explanation(B, t),
            }
        )

    summary = {
        "labels": [a_label, b_label],
        "n": len(tasks),
        "stages": {k: agreement(*v) for k, v in stage.items()},
        "counts": {
            a_label: Counter(final_a.values()),
            b_label: Counter(final_b.values()),
        },
        "why": Counter(r["why_runs_differed"] for r in rec.values()),
    }
    if baseline:
        same = {t: reviewer(baseline, t) for t in tasks if t in baseline["findings"]}
        summary["noise"] = agreement(same, stage["reviewer"][0])
        summary["noise_label"] = spec["noise_baseline"]["label"]
    return {
        "spec": spec,
        "rows": rows,
        "summary": summary,
        "notes": rec_data.get("notes", spec.get("notes", [])),
    }


def render_md(c: dict) -> str:
    s, (a, b) = c["summary"], c["summary"]["labels"]
    n = s["n"]
    reconciled = "reconciled" in s["stages"]
    out = [
        f"# {c['spec']['title']}",
        "",
        c["spec"].get("intro", ""),
        "",
        "## Agreement by stage",
        "",
        "| Stage | Tasks with the same severity | Differences |",
        "|---|---|---|",
    ]
    if "noise" in s:
        same, diff = s["noise"]
        out.append(
            f"| Noise baseline: {s['noise_label']} vs {a} reviewers (same scorer) | {same}/{len(diff) + same} | {len(diff)} |"
        )
    for k, label in STAGES:
        if k in s["stages"]:
            same, diff = s["stages"][k]
            out.append(f"| {label}: {a} vs {b} | {same}/{n} | {len(diff)} |")
    final = "reconciled" if reconciled else "verified"
    same, diff = s["stages"][final]
    differing = [r for r in c["rows"] if r["task"] in diff]
    if reconciled:
        out += ["", "## What remains after reconciliation", ""]
        out += [
            f"- **{r['task']}**: {a} {r['a_fin']}, {b} {r['b_fin']}. {r['reason']}"
            for r in differing
        ]
    else:
        out += ["", f"## Tasks that differ after verification ({len(diff)})", ""]
        out += [
            f"- **{r['task']}**: {a} {r['a_fin']}, {b} {r['b_fin']}.\n"
            f"  - {a}: {r['a_why']}\n  - {b}: {r['b_why']}"
            for r in differing
        ]
    out += [
        "",
        "## Final severity counts",
        "",
        f"| Severity | {a} | {b} |",
        "|---|---|---|",
    ]
    out += [
        f"| {sv} | {s['counts'][a].get(sv, 0)} | {s['counts'][b].get(sv, 0)} |"
        for sv in SEVERITIES
    ]
    out += ["", "## Every task", ""]
    if reconciled:
        out += [
            f"| Task | v1.0.0 | Repeat | {a} reviewer | {a} verified | {b} reviewer | {b} verified | {a} final | {b} final | Why runs differed |",
            "|---|---|---|---|---|---|---|---|---|---|",
        ]
        out += [
            f"| {r['task']} | {r['prior']} | {r['baseline']} | {r['a_rev']} | {r['a_ver']} | {r['b_rev']} | {r['b_ver']} | {r['a_fin']} | {r['b_fin']} | {r['why'] or '-'} |"
            for r in c["rows"]
        ]
    else:
        out += [
            f"| Task | v1.0.0 | Repeat | {a} reviewer | {a} verified | {b} reviewer | {b} verified |",
            "|---|---|---|---|---|---|---|",
        ]
        out += [
            f"| {r['task']} | {r['prior']} | {r['baseline']} | {r['a_rev']} | {r['a_ver']} | {r['b_rev']} | {r['b_ver']} |"
            for r in c["rows"]
        ]
    if c["notes"]:
        out += ["", "## Notes", ""] + [f"- {x}" for x in c["notes"]]
    return "\n".join(out) + "\n"


CSS = """
:root{--bg:#f7f8fa;--surface:#fff;--surface-2:#f1f3f6;--border:#dde1e7;--text:#1c2330;--muted:#5d6878;--accent:#2f6fde;
--b:#c62f3d;--bs:#fbe7e9;--ma:#c76a12;--mas:#fdf0e1;--mi:#8a7400;--mis:#faf5d9;--no:#23864f;--nos:#e3f5ea;--hl:#fff7d6;color-scheme:light}
@media (prefers-color-scheme:dark){:root:not([data-theme="light"]){--bg:#0f1218;--surface:#161b23;--surface-2:#1d232d;--border:#2a323e;--text:#e6eaf0;--muted:#a0aab8;--accent:#6ea2ff;
--b:#ff7380;--bs:#3a1b20;--ma:#ffaa5c;--mas:#3a2a17;--mi:#e6cd55;--mis:#353015;--no:#5fd393;--nos:#173325;--hl:#2e2a14;color-scheme:dark}}
:root[data-theme="dark"]{--bg:#0f1218;--surface:#161b23;--surface-2:#1d232d;--border:#2a323e;--text:#e6eaf0;--muted:#a0aab8;--accent:#6ea2ff;
--b:#ff7380;--bs:#3a1b20;--ma:#ffaa5c;--mas:#3a2a17;--mi:#e6cd55;--mis:#353015;--no:#5fd393;--nos:#173325;--hl:#2e2a14;color-scheme:dark}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--text);font:14px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Inter,sans-serif}
main{max-width:1400px;margin:0 auto;padding:16px}section{background:var(--surface);border:1px solid var(--border);border-radius:10px;padding:16px;margin-bottom:16px}
h1{font-size:19px;margin:0 0 6px}h2{font-size:16px;margin:0 0 10px}.muted{color:var(--muted)}
.tscroll{max-height:min(70vh,780px);overflow:auto;border:1px solid var(--border);border-radius:8px}
table{border-collapse:separate;border-spacing:0;width:max-content;min-width:100%}
th,td{padding:5px 9px;border-bottom:1px solid var(--border);text-align:left;vertical-align:top;background:var(--surface)}
thead th{position:sticky;top:0;z-index:2;background:var(--surface-2);font-size:12.5px;color:var(--muted);white-space:nowrap}
th:first-child,td:first-child{position:sticky;left:0;z-index:1;border-right:1px solid var(--border);font-family:ui-monospace,Menlo,monospace}
thead th:first-child{z-index:3}tr.diff td{background:var(--hl)}td.wrap{max-width:520px;min-width:260px}
.sev{display:inline-block;border-radius:5px;padding:0 7px;font-size:12px;font-weight:600}
.Blocker{color:var(--b);background:var(--bs)}.Major{color:var(--ma);background:var(--mas)}.Minor{color:var(--mi);background:var(--mis)}.None{color:var(--no);background:var(--nos)}
tr[hidden]{display:none}
label{display:inline-flex;gap:6px;align-items:center;margin-bottom:10px}
"""


def render_html(c: dict) -> str:
    s, (a, b) = c["summary"], c["summary"]["labels"]
    e = html.escape
    reconciled = "reconciled" in s["stages"]

    def sev(x: str) -> str:
        return f'<span class="sev {e(x)}">{e(x)}</span>' if x in SEVERITIES else e(x)

    stages = []
    if "noise" in s:
        same, diff = s["noise"]
        stages.append(
            (
                f"Noise baseline: {s['noise_label']} vs {a} reviewers (same scorer)",
                f"{same}/{same + len(diff)}",
                len(diff),
            )
        )
    for k, label in STAGES:
        if k in s["stages"]:
            same, diff = s["stages"][k]
            stages.append((f"{label}: {a} vs {b}", f"{same}/{s['n']}", len(diff)))
    stage_rows = "".join(
        f"<tr><td>{e(name)}</td><td>{e(x)}</td><td>{d}</td></tr>"
        for name, x, d in stages
    )
    remaining = s["stages"]["reconciled" if reconciled else "verified"][1]
    differing = [r for r in c["rows"] if r["task"] in remaining]
    if reconciled:
        rem_title = f"What remains after reconciliation ({len(remaining)})"
        rem_head = f"<th>Task</th><th>{e(a)}</th><th>{e(b)}</th><th>Why</th>"
        rem = "".join(
            f"<tr><td>{e(r['task'])}</td><td>{sev(r['a_fin'])}</td><td>{sev(r['b_fin'])}</td><td class='wrap'>{e(r['reason'])}</td></tr>"
            for r in differing
        )
    else:
        rem_title = f"Tasks that differ after verification ({len(remaining)})"
        rem_head = f"<th>Task</th><th>{e(a)}</th><th>{e(b)}</th><th>{e(a)} reasoning</th><th>{e(b)} reasoning</th>"
        rem = "".join(
            f"<tr><td>{e(r['task'])}</td><td>{sev(r['a_fin'])}</td><td>{sev(r['b_fin'])}</td><td class='wrap'>{e(r['a_why'])}</td><td class='wrap'>{e(r['b_why'])}</td></tr>"
            for r in differing
        )
    counts = "".join(
        f"<tr><td>{sev(x)}</td><td>{s['counts'][a].get(x, 0)}</td><td>{s['counts'][b].get(x, 0)}</td></tr>"
        for x in SEVERITIES
    )
    head = f"<th>Task</th><th>v1.0.0</th><th>Repeat</th><th>{e(a)} reviewer</th><th>{e(a)} verified</th><th>{e(b)} reviewer</th><th>{e(b)} verified</th>"
    if reconciled:
        head += f"<th>{e(a)} final</th><th>{e(b)} final</th><th>Why runs differed</th><th>Reconciliation reason</th>"

    def row(r: dict) -> str:
        cells = (
            f"<td>{e(r['task'])}</td><td>{sev(r['prior'])}</td><td>{sev(r['baseline'])}</td>"
            f"<td>{sev(r['a_rev'])}</td><td>{sev(r['a_ver'])}</td><td>{sev(r['b_rev'])}</td><td>{sev(r['b_ver'])}</td>"
        )
        if reconciled:
            cells += (
                f"<td>{sev(r['a_fin'])}</td><td>{sev(r['b_fin'])}</td>"
                f"<td>{e(r['why'] or '-')}</td><td class='wrap'>{e(r['reason'])}</td>"
            )
        differs = r["a_ver"] != r["b_ver"] or r["a_fin"] != r["b_fin"]
        return f"<tr class='{'diff' if differs else ''}'>{cells}</tr>"

    body = "".join(row(r) for r in c["rows"])
    notes = "".join(f"<li>{e(x)}</li>" for x in c["notes"])
    return f"""<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>{e(c["spec"].get("page_title", "Review run comparison"))}</title><style>{CSS}</style></head><body><main>
<section><h1>{e(c["spec"]["title"])}</h1><p class="muted">{e(c["spec"].get("intro", ""))}</p></section>
<section><h2>Agreement by stage</h2><div class="tscroll"><table><thead><tr><th>Stage</th><th>Same severity</th><th>Differences</th></tr></thead><tbody>{stage_rows}</tbody></table></div></section>
<section><h2>{e(rem_title)}</h2><div class="tscroll"><table><thead><tr>{rem_head}</tr></thead><tbody>{rem}</tbody></table></div></section>
<section><h2>Final severity counts</h2><div class="tscroll"><table><thead><tr><th>Severity</th><th>{e(a)}</th><th>{e(b)}</th></tr></thead><tbody>{counts}</tbody></table></div></section>
<section><h2>Every task</h2><label><input type="checkbox" id="only"> Show only tasks where the runs differ</label>
<div class="tscroll"><table id="all"><thead><tr>{head}</tr></thead><tbody>{body}</tbody></table></div></section>
{f"<section><h2>Notes</h2><ul>{notes}</ul></section>" if notes else ""}
</main><script>
document.getElementById('only').onchange = e => document.querySelectorAll('#all tbody tr').forEach(tr => tr.hidden = e.target.checked && !tr.classList.contains('diff'));
</script></body></html>
"""


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("spec", type=Path)
    args = parser.parse_args()
    c = build(args.spec)
    args.spec.with_suffix(".md").write_text(render_md(c))
    args.spec.with_suffix(".html").write_text(render_html(c))
    for k, (same, diff) in c["summary"]["stages"].items():
        print(f"{k:>10}: {same}/{c['summary']['n']} agree, {len(diff)} differ")
    if "noise" in c["summary"]:
        same, diff = c["summary"]["noise"]
        print(f"     noise: {same}/{same + len(diff)} agree, {len(diff)} differ")


if __name__ == "__main__":
    main()
