# Mode Registry

Grok annotation: Essential Core mode registry authored by Grok on 2026-07-20 (E0/E1).

Canonical workflows and modes for the Essential Core planner. Aliases are
compatibility **routing inputs**, not OS-installed binaries.

## Workflows

| workflow_id | role_card | runtime_agent | primary_protocol |
| --- | --- | --- | --- |
| deep-research | core/teams/deep_research_roles.md | runtime/agents/deep-research-team.md | core/protocols/deep_research.md |
| academic-paper | core/teams/academic_paper_roles.md | runtime/agents/academic-paper-team.md | core/protocols/academic_paper.md |
| academic-paper-reviewer | core/teams/reviewer_panel_roles.md | runtime/agents/paper-reviewer-panel.md | core/protocols/manuscript_review.md |
| academic-pipeline | core/teams/pipeline_roles.md | runtime/agents/academic-pipeline-orchestrator.md | core/protocols/academic_pipeline.md |
| experiment | core/teams/experiment_roles.md | runtime/agents/experiment-team.md | core/protocols/experiment.md |

## Modes (27 + experiment label aliases)

### deep-research (8)

| mode | aliases | quality_gates | notes |
| --- | --- | --- | --- |
| full | rm-full-research, ars-full-research | evidence_state_vocab | multi-agent deep research |
| quick | rm-quick-research, ars-quick-research | evidence_state_vocab | shallow pass |
| review | rm-review-sources, ars-review-sources | claim_verdict_vocab | source-text critique |
| lit-review | rm-lit-review, ars-lit-review | evidence_state_vocab | literature matrix; discovery may hand off |
| three-way-scan | rm-3w, ars-3w | evidence_state_vocab | WHY/HOW/WHAT shortlist |
| fact-check | rm-fact-check, ars-fact-check | claim_verdict_vocab | claim separation |
| socratic | rm-socratic, ars-socratic | vague_topic_socratic | vague-topic override target |
| systematic-review | rm-systematic-review, ars-systematic-review | prisma_fields,rob2_fields,grade_fields | depth E2 |

### academic-paper (11)

| mode | aliases | quality_gates | notes |
| --- | --- | --- | --- |
| full | rm-full, ars-full | generator_evaluator_separation | full draft path |
| plan | rm-plan, ars-plan | generator_evaluator_separation | structure/plan only |
| outline-only | rm-outline, ars-outline | mode_registry_coverage | outline |
| revision | rm-revision, ars-revision | generator_evaluator_separation | revision mode |
| revision-coach | rm-revision-coach, ars-revision-coach | generator_evaluator_separation | roadmap coach |
| abstract-only | rm-abstract, ars-abstract | mode_registry_coverage | bilingual abstract fields |
| lit-review | rm-paper-lit-review, ars-paper-lit-review | evidence_state_vocab | paper-format lit review |
| format-convert | rm-format-convert, ars-format-convert | optional_runtime_honesty | checklist; engines external |
| citation-check | rm-citation-check, ars-citation-check | claim_verdict_vocab | citation compliance |
| disclosure | rm-disclosure, ars-disclosure | mode_registry_coverage | disclosure statement |
| rebuttal-audit | rm-rebuttal-audit, ars-rebuttal-audit | generator_evaluator_separation | evaluator-only |

### academic-paper-reviewer (6)

| mode | aliases | quality_gates | notes |
| --- | --- | --- | --- |
| full | rm-reviewer, ars-reviewer | reviewer_independence | four independents then synthesis |
| re-review | rm-re-review, ars-re-review | reviewer_independence | residual scoring |
| quick | rm-reviewer-quick, ars-reviewer-quick | mode_registry_coverage | EIC quick |
| methodology-focus | rm-methodology-focus, ars-methodology-focus | reviewer_independence | methodology mandatory |
| guided | rm-guided-review, ars-guided-review | mode_registry_coverage | Socratic issue dialogue |
| calibration | rm-calibration, ars-calibration | claim_verdict_vocab | requires gold labels |

### academic-pipeline (1 + ops)

| mode | aliases | quality_gates | notes |
| --- | --- | --- | --- |
| pipeline | rm-pipeline, ars-pipeline | passport_reset_contract | 10-stage machine |
| resume_from_passport | rm-resume, ars-resume | passport_reset_contract | checkpoint resume |
| mark-read | rm-mark-read, ars-mark-read | mode_registry_coverage | operational |
| unmark-read | rm-unmark-read, ars-unmark-read | mode_registry_coverage | operational |
| cache-invalidate | rm-cache-invalidate, ars-cache-invalidate | mode_registry_coverage | operational |

### experiment (4 canonical + Codex labels)

| mode | aliases / labels | quality_gates | notes |
| --- | --- | --- | --- |
| plan | rm-experiment-plan, ars-experiment-plan, study-protocol | stats_fallacies_11 | study protocol |
| run | rm-experiment-run, ars-experiment-run, code-experiment | optional_runtime_honesty | execution boundary |
| manage | rm-experiment-manage, ars-experiment-manage | mode_registry_coverage | study management |
| validate | rm-experiment-validate, ars-experiment-validate, statistical-interpretation, reproducibility | stats_fallacies_11 | stats + repro |

## Count model (exact)

| Metric | Value | Explanation |
| --- | ---: | --- |
| workflows | 5 | deep-research, academic-paper, academic-paper-reviewer, academic-pipeline, experiment |
| mode/operation rows | 34 | 8 + 11 + 6 + 5 + 4 |
| legacy ARS mode families | 27 | 8 + 11 + 6 + 1 pipeline family + 1 experiment family |
| prefixed aliases (`ars-*` / `rm-*`) | 68 | 34 rows × 2 prefixes |

Compatibility labels `study-protocol`, `code-experiment`,
`statistical-interpretation`, and `reproducibility` are **not** prefixed aliases
and are not counted in the 68.

Machine-readable source of truth for planner routing:
`runtime/full-runtime-manifest.json` (`modes`, `aliases`, `count_model`).
This Markdown registry must agree with that manifest.

## Supported command aliases (complete = 68)

Every alias listed in the mode tables above (both `ars-*` and `rm-*`) is
supported by the planner. Minimum historical Codex set remains included:
`ars-plan`, `ars-outline`, `ars-abstract`, `ars-lit-review`, `ars-3w`,
`ars-citation-check`, `ars-disclosure`, `ars-format-convert`,
`ars-revision-coach`, `ars-revision`, `ars-rebuttal-audit`, `ars-full`,
`ars-reviewer`, `ars-mark-read`, `ars-unmark-read`, `ars-cache-invalidate`,
plus all other table aliases such as `ars-systematic-review` and
`rm-experiment-validate`.

Unsupported tokens matching `ars-*` or `rm-*` that are not in the supported
table must return planner error `unsupported_alias` with exit code **2**.

## Keyword heuristics (lowest precedence after alias and explicit mode)

| signals | workflow | mode |
| --- | --- | --- |
| systematic review, meta-analysis, PRISMA | deep-research | systematic-review |
| peer review, reviewer panel, manuscript review | academic-paper-reviewer | full |
| pipeline, passport, resume stage | academic-pipeline | pipeline |
| reproducibility, statistical interpretation, validate experiment | experiment | validate |
| experiment, preregistration, study protocol | experiment | plan |
| rebuttal audit | academic-paper | rebuttal-audit |
| disclosure statement | academic-paper | disclosure |
| revision coach | academic-paper | revision-coach |
| fact check, claim verification | deep-research | fact-check |
| three-way, WHY HOW WHAT | deep-research | three-way-scan |
| write a paper / outline | academic-paper | plan |
| vague paper topic without RQ | deep-research | socratic |
| bare ambiguous mode tokens (`full`, `quick`, `plan`, `lit-review`) | safe default | socratic or plan (`route_reason=ambiguous_mode_default`) |

## Vague paper-topic override

If free text matches a paper-writing intent without a clear research question
(PICO/FINER elements missing), force `workflow=deep-research`, `mode=socratic`,
`route_reason=paper_topic_scoping_override`. Never silent full draft.
