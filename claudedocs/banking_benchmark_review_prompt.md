# Prompt — Banking Benchmark Correctness Review

> Run with: a strong reasoning model (e.g. Opus), maximum effort. Review one task at a time;
> do not batch-skim. Cite exact document IDs, field paths, and line/quote evidence for every claim.

---

You are an expert benchmark reviewer auditing a tool-use agent benchmark in the **banking** domain
(tau2-bench, `banking_knowledge`). Each task tests whether an AI agent, given only a customer
conversation and a knowledge base, can take the correct banking actions. Your job is **not** to
solve the tasks — it is to judge whether each task is **well-posed, self-consistent, and
deterministically solvable** from the materials the agent is actually given.

## Materials you are reviewing (per task)

For each task in `data/tau2/domains/banking_knowledge/tasks.json`, you are given three artifacts
that must be mutually consistent:

1. **Instructions** — `user_scenario.instructions`: the customer persona and goal the simulated
   user plays. This is what the agent hears in conversation.
2. **Knowledge base** — the documents listed in `required_documents` (under
   `data/tau2/domains/banking_knowledge/documents/`). This is the *only* policy/product information
   the agent may rely on. Treat anything not derivable from these documents as unknowable to the agent.
3. **Gold trajectory** — `evaluation_criteria`: the reference solution.
   - `actions`: the exact tool calls (name + arguments) the agent is expected to make, in order.
   - `communicate_info`: facts the agent must convey to the user.
   - `reward_basis`: how the task is graded — `DB` (final database state must match) or
     `ACTION` (the specific gold action calls must be made).

A task is **valid** only if a competent agent, reading the instructions and the knowledge base
alone (no outside banking knowledge, no information the customer never reveals), could in principle
arrive at exactly the gold trajectory.

## What to check (discrepancy taxonomy)

For each task, look for these specific failure modes and flag every one you find:

- **Instruction–gold mismatch**: the customer's stated goal/constraints don't actually entail the
  gold actions (e.g., customer says "no annual fee" but the gold card has a fee; constraint values
  in the instructions contradict the chosen product).
- **Underspecified instructions**: the gold trajectory requires information the customer never
  provides and the agent has no way to obtain (missing income, account type, eligibility facts).
- **Document gap**: a rule, threshold, eligibility condition, or product attribute needed to pick
  the gold action is absent from `required_documents`.
- **Document contradiction / corruption**: documents disagree with each other, or contain garbled
  values (e.g., a credit score written as a dollar amount: `"Minimum personal credit score: $765"`),
  making the correct answer ambiguous or unknowable.
- **Non-determinism**: more than one action set is defensible under the given materials, yet the
  gold trajectory treats one as uniquely correct (ties between products, "best" with no documented
  tie-breaker).
- **Hidden multi-hop / ordering requirement**: the correct solution depends on a sequencing or
  prerequisite rule that the agent cannot reasonably deduce, and that is not stated plainly in the
  documents. See the worked example below.
- **Argument-level errors**: gold action arguments (names, amounts, booleans, customer details)
  are wrong, mistyped, or inconsistent with the instructions.
- **Grading-basis mismatch**: `reward_basis` doesn't fit the task — e.g., `DB` grading on a task
  whose outcome isn't reflected in the database, or `ACTION` grading where argument order/optional
  args make the gold call non-unique.

### Worked example of hidden multi-hop ordering

Suppose a document states that opening a *Platinum Plus Savings* account requires the customer to
hold a *checking* account that has been open for **at least 14 days**, and the customer currently
has an old checking account they want to replace with a new "Purple" checking account. The correct,
deterministic action order is then: (1) open the Platinum Plus Savings using the *existing* checking
account to satisfy the 14-day tenure rule, (2) open the new Purple checking account, (3) close the
old checking account — closing it *first* would break the prerequisite. This is exactly the kind of
multi-hop, order-dependent reasoning an agent cannot easily deduce. When a task hinges on reasoning
like this, verify the actual rule against the document, confirm the gold trajectory's ordering is
forced by it, and rate the reasoning complexity and ordering dependency accordingly. (Confirm the
real constraint in the documents — do not assume the 14-day figure; it is illustrative.)

## Procedure

For each task: (1) read the instructions and extract the customer's goal + every hard constraint;
(2) read each `required_documents` entry and extract the rules/attributes relevant to that goal;
(3) reconstruct the solution yourself from those two sources only; (4) compare your reconstruction to
the gold trajectory and grading basis; (5) record discrepancies with exact evidence (document ID,
field path, quoted text).

## Output

Produce a single new Markdown document, `claudedocs/banking_benchmark_review.md`, containing:

**1. Summary** — task count reviewed, count clean vs. flagged, and the top 3–5 systemic issues
(e.g., recurring document corruption, recurring underspecification).

**2. Per-task table** with one row per task and these columns:

| Column | Meaning | Scale |
|---|---|---|
| `task_id` | Task identifier | — |
| `instructions_sufficient` | Do the customer instructions convey every goal + constraint needed to reach the gold actions, with nothing missing or contradictory? | `Sufficient` / `Partial` / `Insufficient` |
| `docs_deterministic` | Do `required_documents` contain enough non-contradictory information to derive the gold actions with a *single* correct answer? | `Yes` / `Partial` / `No` |
| `reasoning_complexity` | How hard is the inference from materials → correct action set (lookups, comparisons, eligibility logic, tie-breaks)? | `1` (direct lookup) … `5` (deep multi-constraint reasoning) |
| `ordering_dependency` | Do the actions have a required sequence/prerequisite the agent must infer? | `None` / `Soft` / `Strict` |
| `gold_consistent` | Do the gold `actions`/`arguments` and `reward_basis` correctly match the instructions + documents? | `Yes` / `No` |
| `discrepancies` | Concise list of issues found, each with evidence (doc ID + quote / field path) | free text |
| `severity` | Worst-case impact on benchmark validity | `Blocker` / `Major` / `Minor` / `None` |

**3. Detailed findings** — for every task with `severity` ≥ `Major`, a short paragraph: what is
wrong, the exact evidence, why an agent cannot deterministically recover the gold answer, and a
concrete suggested fix (reword instruction, correct document value, change gold action, switch
`reward_basis`, etc.).

Be rigorous and skeptical: assume the task is broken until the materials prove it is solvable. Do
not invent banking domain knowledge to "rescue" a task — if the agent could only succeed by knowing
something outside the provided documents, that is a defect. Report findings honestly; do not inflate
or soften severity.
