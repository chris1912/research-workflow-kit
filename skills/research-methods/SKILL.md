---
name: research-methods
description: Essential Core methods routing for research questions, systematic review, manuscript review, integrity, pipeline, and experiment planning.
---

# Research Methods (Essential Core)

Grok annotation: Rewritten by Grok on 2026-07-20 as Essential Core E0+E1 packaging.
Grok annotation: E2 method depth (RQ/deep/SR + semantic gates) by Grok on 2026-07-20.
Grok annotation: E3-D packaging/status language reconciled by Grok on 2026-07-21.
Codex annotation: Public entrypoint prepared by Codex on 2026-07-15.

Read [`docs/START_HERE.html`](../../docs/START_HERE.html) first. This skill is the
stable public route for methods, integrity, review, pipeline, and experiment
planning. Packaging mode is **essential_core**: first-party contracts, protocols,
templates, dual agent surfaces, and an opt-in offline runtime under `runtime/`.

The full Academic Research Skills suite remains **optional external material**,
not bundled under `ars/` or `codex/`, and not a required runtime.

## When to use this skill

| Task | Start here | Primary surface |
| --- | --- | --- |
| Research-question refinement | this skill | `core/protocols/research_question.md` |
| Systematic review / meta-analysis protocol | this skill | `core/protocols/systematic_review.md` |
| Deep research / Socratic scoping | this skill | `core/protocols/deep_research.md` |
| Manuscript peer-review simulation | this skill | `core/protocols/manuscript_review.md` |
| Citation and integrity checking | this skill | `core/protocols/citation_integrity.md` |
| Academic paper modes | this skill | `core/protocols/academic_paper.md` |
| Pipeline / passport resume | this skill | `core/protocols/academic_pipeline.md` |
| Experiment / reproducibility | this skill | `core/protocols/experiment.md` |
| Proposal dual-route literature / HTML delivery | `proposal-research` | proposal templates |

## Offline routing contract

1. Read `MODE_REGISTRY.md` and `core/contracts/mode_routing.md`.
2. Prefer explicit `rm-*` / `ars-*` aliases as routing inputs to the planner.
3. Vague paper topics without a clear research question force `deep-research` / `socratic`.
4. E2 RQ/deep/SR and E3 paper/integrity/manuscript-review protocols are operational (`parity: partial`); E4 pipeline/experiment/optional_runtime bodies remain `parity: not_started`—do not advertise complete ARS parity.
5. Use seven evidence states from `core/contracts/evidence_states.md`.
6. Require human confirmation for study design, final claims, integrity sign-off, and submission-ready text.
7. When optional discovery/parser/QA adapters are unset, continue offline with `missing` / `blocked` honesty.

## Runtime (opt-in)

```text
python skills/research-methods/runtime/scripts/essential_full_runtime.py plan --text "..." --json
python skills/research-methods/runtime/scripts/essential_hook.py announce --json
python skills/research-methods/runtime/scripts/essential_quality_gates.py list --json
```

Env flags (canonical | one-release alias): `RM_FULL_RUNTIME` | `ARS_CODEX_FULL_RUNTIME`,
`RM_AGENT_TEAM` | `ARS_CODEX_AGENT_TEAM`, `RM_HOOKS` | `ARS_CODEX_HOOKS`,
`RM_PASSPORT_RESET` | `ARS_PASSPORT_RESET`, `RM_CLAIM_AUDIT` | `ARS_CLAIM_AUDIT`.

## Hard rules

- Do not invent data, citations, reviewer identities, statistics, or results.
- Do not restore or hyperlink as present the removed `ars/` or `codex/` trees.
- Do not claim full ARS behavioral parity; E2/E3 partial protocol depth is not full-suite parity, not real multi-process orchestration, and not real editorial authority.
- Keep repository-relative links in publishable notes.
- Hand proposal dual-route / priority full-text / HTML delivery work to `proposal-research`.

## Provenance

See `NOTICE.md`, `LINEAGE_INDEX.md`, `manifest.json`,
`COMPATIBILITY.md`, `MODE_REGISTRY.md`, and
`docs/licenses/academic-research-skills-license.txt`.

Essential Core baseline: first-party `essential_core` packaging with E1 routing
runtime, E2 RQ/deep/SR method depth, and E3 paper/integrity/review depth as
`parity: partial`; E4 protocol bodies remain `parity: not_started` (see
`COMPATIBILITY.md`).
