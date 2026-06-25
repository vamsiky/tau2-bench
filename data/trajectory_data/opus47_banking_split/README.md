# Opus 4.7 `banking_knowledge` — split trajectory files

The original `Claude Opus 4.7_banking_knowledge_trajectories.json` (123 MB, 388 simulations)
split into 10 smaller, self-contained JSON files for easier browsing in an IDE.

Each `part_NN.json` keeps the original top-level shape — `timestamp`, `info`, `tasks`,
`simulations` — plus two helper keys: `_part` (index) and `_tasks` (the task IDs in this part).
Splitting is **by task**, so all 4 trials of a task stay in the same file.

| Part | Tasks | Sims | Failed trials | Size |
|---|---|---:|---:|---:|
| part_00 | task_001–task_012 | 40 | 20 | 4.8 MB |
| part_01 | task_014–task_023 | 40 | 23 | 8.8 MB |
| part_02 | task_024–task_034 | 40 | 23 | 9.2 MB |
| part_03 | task_035–task_045 | 40 | 33 | 8.3 MB |
| part_04 | task_046–task_055 | 40 | 32 | 10.5 MB |
| part_05 | task_056–task_065 | 40 | 35 | 16.0 MB |
| part_06 | task_066–task_075 | 40 | 37 | 14.9 MB |
| part_07 | task_076–task_085 | 40 | 40 | 13.1 MB |
| part_08 | task_086–task_095 | 40 | 28 | 13.8 MB |
| part_09 | task_096–task_102 | 28 | 19 | 6.6 MB |

Total: 388 simulations, 290 failed trials.

## Analysis outputs (in `claudedocs/`)
- `opus47_banking_knowledge_failure_analysis.md` — root-cause summary and recommendations.
- `opus47_banking_failure_evidence_table.md` — one row per failed trial: task, trial, category,
  exact gold vs actual, why it failed, and a narrative up to the failure.
