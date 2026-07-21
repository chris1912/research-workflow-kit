# Compatibility

Grok annotation: Essential Core compatibility matrix authored by Grok on 2026-07-20.
Grok annotation: E3-D packaging consistency closeout by Grok on 2026-07-21.

## Packaging

| Field | Value |
| --- | --- |
| packaging_mode | essential_core |
| stage | E0+E1 runtime + E2 method depth (RQ/deep/SR) + E3 paper/integrity/review partial |
| full ARS tree | not bundled; optional external |
| behavioral parity claim | **not claimed** for full ARS; E2–E3 protocol depth is `parity: partial` only; E4–E5 remain pending |

## Parity labels

| Label | Meaning |
| --- | --- |
| supported | Implemented and testable at current stage |
| partial | Scaffold present; depth incomplete |
| not_started | Reserved for later stage; do not advertise complete |
| external | Hand off to adjacent skill/adapter |
| unsupported | Explicitly out of Essential Core residual list |

## Mode parity (E3-D snapshot)

| Area | Parity | Notes |
| --- | --- | --- |
| Mode routing + aliases | supported | planner + MODE_REGISTRY + 68-alias manifest |
| Seven evidence states | supported | contract + gates |
| Passport transition hooks | partial | schema/transition + append-only reset-ledger transition validator executable at E1; full pipeline stage depth E4 |
| Reviewer independence contract | partial | fixture order + A20/synthesis/minority + identity/re-review/calibration validators; multi-process isolation remains partial (not real multi-process orchestration) |
| Hook announce safety | supported | read-only |
| Quality gate runner | supported | E2 method gates + E3 integrity/paper/review gates executable; `stats_fallacies_11` remains E4 not_started |
| RQ / deep research / SR protocol depth | partial | E2 depth + semantic gates; not full ARS multi-agent parity |
| Manuscript review / integrity / paper modes depth | partial | E3-A/B/C operational offline; not full ARS multi-process or editorial authority |
| Pipeline + experiment + optional_runtime depth | not_started | E4 |
| Dual-route literature discovery | external | proposal-research |
| Figure codegen | external | longform-writing when present |
| Full ARS eval gold / CI | unsupported | residual |

## Stage-D template successors

| Stage-D path | Essential Core successor | Parity |
| --- | --- | --- |
| templates/review_protocol.md | core/templates/prisma_protocol.md | partial (E2 PRISMA/RoB/GRADE fields present; not full ARS) |
| templates/manuscript_review.md | core/templates/manuscript_review_full.md | partial (E3-C manuscript-review depth; not multi-process isolation or real editorial authority) |
| templates/citation_integrity_check.md | core/templates/citation_integrity_audit.md | partial (E3-A citation integrity depth; offline-honest, no network verification claim) |
| templates/reproducibility_checklist.md | core/templates/reproducibility_checklist.md | partial (E4 fallacy depth pending) |

## Env flag aliases (one release)

| Canonical | Alias |
| --- | --- |
| RM_FULL_RUNTIME | ARS_CODEX_FULL_RUNTIME |
| RM_AGENT_TEAM | ARS_CODEX_AGENT_TEAM |
| RM_HOOKS | ARS_CODEX_HOOKS |
| RM_PASSPORT_RESET | ARS_PASSPORT_RESET |
| RM_CLAIM_AUDIT | ARS_CLAIM_AUDIT |

## Dual agent surface

Internal role cards (`core/teams/*`) and Codex runtime prompts (`runtime/agents/*`)
are **distinct** files and must not be double-counted.
