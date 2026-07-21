# LINEAGE_INDEX

Grok annotation: Essential Core lineage index by Grok on 2026-07-20 (E0/E1).
Grok annotation: E3-D protocol body parity labels reconciled by Grok on 2026-07-21.

Conceptual anchors only. No wholesale upstream prose. See `NOTICE.md`.

| Essential Core path | Kind | Upstream concept anchors | Upstream path hints (HEAD) | Decision |
| --- | --- | --- | --- | --- |
| `SKILL.md` | entry | public methods entry | skills/research-methods/SKILL.md | rewrite |
| `manifest.json` | manifest | packaging mode | skills/research-methods/manifest.json | rewrite |
| `MODE_REGISTRY.md` | registry | 27 modes + aliases | ars modes / codex manifest | rewrite |
| `COMPATIBILITY.md` | compat | supported/partial/external | codex/compatibility-matrix.md | rewrite |
| `NOTICE.md` | provenance | CC BY-NC attribution | docs/licenses/... | first-party |
| `LINEAGE_INDEX.md` | provenance | file-level lineage map | n/a | first-party |
| `agents/openai.yaml` | meta | skill UI metadata | agents/openai.yaml | rewrite |
| `core/contracts/evidence_states.md` | contract | evidence_states | ars/codex contracts | rewrite |
| `core/contracts/mode_routing.md` | contract | mode_routing | ars/codex contracts | rewrite |
| `core/contracts/passport_state.md` | contract | passport_state | ars/codex contracts | rewrite |
| `core/contracts/reviewer_independence.md` | contract | reviewer_independence | ars/codex contracts | rewrite |
| `core/contracts/evidence_verdict.md` | contract | evidence_verdict | ars/codex contracts | rewrite |
| `core/contracts/quality_gates.md` | contract | quality_gates | ars/codex contracts | rewrite |
| `core/contracts/generator_evaluator.md` | contract | generator_evaluator | ars/codex contracts | rewrite |
| `core/protocols/research_question.md` | protocol | research_question | ars/.../research_question.md | rewrite; body `parity: partial` (E2); no wholesale copy |
| `core/protocols/deep_research.md` | protocol | deep_research | ars/.../deep_research.md | rewrite; body `parity: partial` (E2); no wholesale copy |
| `core/protocols/systematic_review.md` | protocol | systematic_review | ars/.../systematic_review.md | rewrite; body `parity: partial` (E2); no wholesale copy |
| `core/protocols/manuscript_review.md` | protocol | manuscript_review | ars/.../manuscript_review.md | rewrite; body `parity: partial` (E3-C); no wholesale copy |
| `core/protocols/citation_integrity.md` | protocol | citation_integrity | ars/.../citation_integrity.md | rewrite; body `parity: partial` (E3-A); no wholesale copy |
| `core/protocols/academic_pipeline.md` | protocol | academic_pipeline | ars/.../academic_pipeline.md | rewrite (body not_started until E4) |
| `core/protocols/experiment.md` | protocol | experiment | ars/.../experiment.md | rewrite (body not_started until E4) |
| `core/protocols/academic_paper.md` | protocol | academic_paper | ars/.../academic_paper.md | rewrite; body `parity: partial` (E3-B); no wholesale copy |
| `core/protocols/optional_runtime.md` | protocol | optional_runtime | ars/.../optional_runtime.md | rewrite (body not_started until E4) |
| `core/teams/deep_research_roles.md` | role_card | merged agent roles | ars agent prompts | merge/rewrite |
| `core/teams/academic_paper_roles.md` | role_card | merged agent roles | ars agent prompts | merge/rewrite |
| `core/teams/reviewer_panel_roles.md` | role_card | merged agent roles | ars agent prompts | merge/rewrite |
| `core/teams/pipeline_roles.md` | role_card | merged agent roles | ars agent prompts | merge/rewrite |
| `core/teams/experiment_roles.md` | role_card | merged agent roles | ars agent prompts | merge/rewrite |
| `core/templates/research_question_brief.md` | template | research_question_brief | ars templates / Stage-D | rewrite |
| `core/templates/prisma_protocol.md` | template | prisma_protocol | ars templates / Stage-D | rewrite |
| `core/templates/prisma_report_skeleton.md` | template | prisma_report_skeleton | ars templates / Stage-D | rewrite |
| `core/templates/literature_matrix.md` | template | literature_matrix | ars templates / Stage-D | rewrite |
| `core/templates/evidence_assessment.md` | template | evidence_assessment | ars templates / Stage-D | rewrite |
| `core/templates/manuscript_review_full.md` | template | manuscript_review_full | ars templates / Stage-D | rewrite |
| `core/templates/editorial_decision.md` | template | editorial_decision | ars templates / Stage-D | rewrite |
| `core/templates/revision_roadmap.md` | template | revision_roadmap | ars templates / Stage-D | rewrite |
| `core/templates/citation_integrity_audit.md` | template | citation_integrity_audit | ars templates / Stage-D | rewrite |
| `core/templates/claim_verification_report.md` | template | claim_verification_report | ars templates / Stage-D | rewrite |
| `core/templates/pipeline_status.md` | template | pipeline_status | ars templates / Stage-D | rewrite |
| `core/templates/material_passport.md` | template | material_passport | ars templates / Stage-D | rewrite |
| `core/templates/study_protocol.md` | template | study_protocol | ars templates / Stage-D | rewrite |
| `core/templates/code_experiment_plan.md` | template | code_experiment_plan | ars templates / Stage-D | rewrite |
| `core/templates/reproducibility_checklist.md` | template | reproducibility_checklist | ars templates / Stage-D | rewrite |
| `core/templates/statistical_validation.md` | template | statistical_validation | ars templates / Stage-D | rewrite |
| `core/templates/rebuttal_audit.md` | template | rebuttal_audit | ars templates / Stage-D | rewrite |
| `core/templates/disclosure_statement.md` | template | disclosure_statement | ars templates / Stage-D | rewrite |
| `core/templates/argument_map.md` | template | argument_map | ars templates / Stage-D | rewrite |
| `runtime/full-runtime-manifest.json` | runtime | alias + env manifest | codex/full-runtime-manifest.json | rewrite |
| `runtime/compatibility-matrix.md` | runtime | runtime support matrix | codex/compatibility-matrix.md | rewrite |
| `runtime/agents/deep-research-team.md` | runtime_agent | Codex team prompt | codex/agents/deep-research-team.md | rewrite |
| `runtime/agents/academic-paper-team.md` | runtime_agent | Codex team prompt | codex/agents/academic-paper-team.md | rewrite |
| `runtime/agents/academic-pipeline-orchestrator.md` | runtime_agent | Codex team prompt | codex/agents/academic-pipeline-orchestrator.md | rewrite |
| `runtime/agents/experiment-team.md` | runtime_agent | Codex team prompt | codex/agents/experiment-team.md | rewrite |
| `runtime/agents/paper-reviewer-panel.md` | runtime_agent | Codex team prompt | codex/agents/paper-reviewer-panel.md | rewrite |
| `runtime/scripts/essential_full_runtime.py` | script | deterministic planner | codex/scripts/ars_codex_full_runtime.py | rewrite |
| `runtime/scripts/essential_hook.py` | script | read-only hook wrapper | codex/scripts/ars_codex_hook.py | rewrite |
| `runtime/scripts/essential_quality_gates.py` | script | quality gate runner | codex/scripts/ars_codex_quality_gates.py | rewrite |
| `runtime/hooks/hooks.json` | hooks | hook config | codex/hooks/hooks.json | rewrite |
| `runtime/hooks/README.md` | hooks | hook boundaries | codex/hooks/README.md | rewrite |
| `runtime/tests/*` | test_support | routing/hook/gates/independence tests + fixtures | codex/tests/* | rewrite |
