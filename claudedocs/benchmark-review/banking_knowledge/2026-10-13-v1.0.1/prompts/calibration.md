# Severity calibration for recurring cases

The severity definitions in `review.md` decide every verdict. Reviewers working in
parallel applied them differently to a few recurring situations, which made verdicts on
identical evidence diverge. Apply the readings below so that the same defect gets the
same severity in every task and every run. Each one follows from the definitions; when a
task has a reason to differ, state it.

- **Cosmetic document defects** (a credit score printed as a dollar amount, an empty
  procedure step, an unrendered `[[placeholder]]`, an arithmetic slip in a worked
  example): a note, not an issue, when the correct answer does not depend on the
  corrupted text. `Minor` when the corrupted value is the deciding fact for that task.
- **Two document-supported readings that lead to different graded states**, where the
  gold follows one of them: `Major`. It becomes `Blocker` only when the gold follows no
  reading the documents support, or when the information or tool needed to reach it does
  not exist.
- **Ties without a documented tie-breaker** that lead to different graded states:
  `Blocker`, since a correct agent fails at random.
- **Rules the grader cannot see** (ACTION grading ignores order and count; transfers
  write nothing to the DB): `Minor`. Correct work still passes; the task just tests less
  than it claims.
- **Customer choices the script never states but the gold records** (shipping speed, card
  design, a refund type): `Minor` when the documents give a clear default that matches
  the gold, `Major` when there is no default or the default differs from the gold.
- **Gold values that depend on data dated after the fixed clock**: `Major`.
- **A required document missing from `required_documents`** while the agent can still
  retrieve it in the default retrieval configuration: `Minor`.
- **Author notes that contradict the data**: a note, since the agent never sees them,
  unless the gold was built from the wrong note, in which case judge the gold itself.
