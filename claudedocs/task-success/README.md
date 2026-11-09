# Improving task success (banking_knowledge)

Analyses and experiments aimed at raising agent success on `banking_knowledge`. For
whether the tasks themselves are sound, see [`../benchmark-review/`](../benchmark-review/README.md).

| Folder | Contents |
|---|---|
| [`failure-analysis/`](failure-analysis/) | Where Claude Opus 4.7 fails: the failure taxonomy ([analysis](failure-analysis/opus47_banking_knowledge_failure_analysis.md)), every failed trial with its gold-vs-actual diff ([evidence table](failure-analysis/opus47_banking_failure_evidence_table.md)), and a check of the scorer's internal consistency ([verifier inconsistencies](failure-analysis/opus47_verifier_inconsistencies.md)). |
| [`policy-reasoning/`](policy-reasoning/) | The POLICY_REASONING failure class: reproduction, candidate fixes, the deterministic-path experiment, the A1–A4 MISSING_WRITE / PRODUCT_SELECTION fixes and the 52-task run with them. Prompt fragments used in those runs are in `a1a4_fixes/` and `policy_fixes/`. |
| [`i1-fixes/`](i1-fixes/) | Prompt-only fix iterations for the I1 task set ([validation](i1-fixes/i1_fix_validation.md)); the fix prompts themselves are in `i1_fixes/`. Commands: [`../i1_run_runbook.md`](../i1_run_runbook.md). |
| [`hindsight/`](hindsight/) | Hindsight-backed retrieval: [implementation and validation](hindsight/hindsight_retrieval_validation.md), and a [step-by-step trajectory analysis](hindsight/hindsight_i1_trajectory_analysis.md) of the I1 runs. |
| [`zero-hallucination/`](zero-hallucination/) | The zero-hallucination RAG variant: [pipeline validation](zero-hallucination/zero_hallucination_rag_validation.md) and [full-episode runs](zero-hallucination/zero_hallucination_full_trajectory_runs.md); the scripts and policy used are in `scripts/`. |
| [`design/`](design/) | Design notes: [multi-hop decision tasks](design/multihop_decision_task_architecture.md) and the [deep-research workflow canvas](design/deep-research-workflow-canvas.html). |
| [`policy-register/`](policy-register/) | `RhoBank_Policy_Register.md`, the synthesized policy register. The `policy_register` retrieval variant loads it at runtime, so it must stay at this path. |
