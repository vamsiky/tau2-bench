# Benchmark correctness reviews

A review asks, task by task, whether a domain's tasks are well-posed and
deterministically solvable from what the agent is given: the customer instructions,
the knowledge base, and the tools. It reviews the benchmark, not an agent.

## Layout

```
benchmark-review/
├── prompts/review.md          current review prompt (one findings JSON per task)
├── prompts/verification.md    current independent-verification prompt
├── prompts/calibration.md     agreed severities for recurring borderline cases
├── prompts/scorers/*.md       optional scorer variants (e.g. verified.md)
├── render_report.py           findings JSON + benchmark data -> review.md / review.html
├── report_template.html       page template used by the renderer
├── compare_runs.py            task-by-task comparison of two runs of one version
└── <domain>/<run date>-<benchmark version>[-<variant>]/
    ├── run.json               domain, benchmark version and git ref, run date, reviewer, prior run
    ├── prompts/               copy of the prompts exactly as this run used them
    ├── inputs/                prior verdicts, change notes, verification scope
    ├── findings/<task>.json   one reviewer verdict per task
    ├── verification/<v>.json  independent verifier verdicts
    ├── synthesis.json         summary and systemic issues
    ├── review.html            interactive report (open in a browser)
    └── review.md              the same report as Markdown
```

Runs of the same version that differ in one setting (a scorer variant) sit side by side
with a suffix, and share a `reconciliation-<date>-<version>.json` and a
`comparison-<date>-<version>.{json,md,html}` in the domain folder.

The folder name says when the review ran and which benchmark version it reviewed, for
example `banking_knowledge/2026-10-13-v1.0.1`. The benchmark version is the upstream
release tag (`git tag`), and `run.json` records the exact commit.

| Run | Benchmark | Notes |
|---|---|---|
| [`banking_knowledge/2026-06-25-v1.0.0`](banking_knowledge/2026-06-25-v1.0.0/review.html) | v1.0.0 | First review. Graded against a locally modified scorer, not upstream grading. |
| [`banking_knowledge/2026-10-13-v1.0.1`](banking_knowledge/2026-10-13-v1.0.1/review.html) | v1.0.1 | Upstream scoring. Compared task by task with the v1.0.0 review. |
| [`banking_knowledge/2026-10-13-v1.0.1-verified-scorer`](banking_knowledge/2026-10-13-v1.0.1-verified-scorer/review.html) | v1.0.1 | Same as above under the first version of this branch's verified scorer (any extra discoverable call allowed, `closure_reason` ignored everywhere). The scorer was tightened afterwards; see `prompts/scorers/verified.md`. Its frozen `prompts/` copy describes the version this run used. |
| [`banking_knowledge/2026-10-13-v1.0.1-draft-1`](banking_knowledge/2026-10-13-v1.0.1-draft-1/) | v1.0.1 | Superseded, unverified first attempt with upstream scoring; kept as a same-scorer repeat to measure run-to-run noise. |
| [`banking_knowledge/comparison-2026-10-13-v1.0.1.html`](banking_knowledge/comparison-2026-10-13-v1.0.1.html) | v1.0.1 | Upstream vs verified scorer, agreement at each stage, and what the scorer alone changes. |

## Reading a report

Open `review.html`. The **Task explorer** shows one task per screen in three columns:
the customer instructions and required documents (full text, expandable), the gold
trajectory (every expected tool call with its arguments, with the steps an issue
refers to highlighted), and the findings (ratings, issues with evidence and fixes, the
verifier's verdict, and the comparison with the prior review). Filter by severity or
prior status, deep-link with `review.html#task_074`, and use the arrow keys to step
through tasks. Tables scroll inside a box no taller than the window, so the horizontal
scrollbar is always on screen.

## Running a review

1. **Snapshot the benchmark version.** Reviewers must read the released benchmark,
   not this branch, which carries local changes to tools and evaluators:
   `git worktree add --detach <scratch>/bench-<tag> <tag>`.
2. **Create the run folder** `<domain>/<YYYY-MM-DD>-<tag>/` with `run.json` (see the
   existing runs), copy `prompts/` into it, and put the prior run's verdicts and the
   change notes since that run in `inputs/` when comparing with an earlier review.
3. **Review.** Give `prompts/review.md` to reviewer agents with a run brief that fills
   in `{domain}`, `{benchmark_version}`, `{snapshot_root}`, `{run_dir}`,
   `{prior_findings}`, `{scorer_variant}` (or none), and a batch of task ids.
   Contiguous batches of about 12 tasks keep related tasks (shared documents) with the
   same reviewer. Use claude-opus-5-5 at effort `high`, set on each agent rather than in
   the prompt, and give every agent its own scratch folder: parallel agents sharing one
   overwrote each other's scripts during the 2026-10-13 runs.
4. **Verify.** In fresh sessions, give `prompts/verification.md` to verifier agents.
   Cover every Blocker and Major, every severity change from the prior run, and a
   seeded random sample of None/Minor tasks to look for missed defects; record the
   scope in `inputs/verification_scope.json`.
5. **Reconcile (when comparing runs).** Independent runs disagree on borderline calls
   even with the same scorer (the draft-1 repeat measures how much). An adjudicator
   reads both runs' evidence and writes `reconciliation-<date>-<version>.json`, giving
   each disputed task one severity per run; runs may keep different severities only
   where the scorer causes the difference. Point each run's `run.json` at it with
   `"reconciliation": {"file": ..., "side": ...}`. The reports keep the reviewer and
   verifier verdicts visible next to the reconciled one.
6. **Synthesize.** Write `synthesis.json` (`summary`, and `systemic_issues` as
   `{title, description, tasks}`) after reading the findings and verification.
7. **Render.**
   ```bash
   uv run python claudedocs/benchmark-review/render_report.py \
       claudedocs/benchmark-review/<domain>/<run>
   ```
   The renderer reads task text, documents, and gold actions from the benchmark's git
   tag (`benchmark_ref` in `run.json`), so the report always shows the exact task that
   was reviewed. The reported severity is the reconciled one, else the verifier's, else
   the reviewer's. `--allow-partial` renders before every task has findings. Compare two
   runs with `compare_runs.py <domain>/comparison-<date>-<version>.json`.
