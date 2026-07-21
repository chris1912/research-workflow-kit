# Workflow

Grok annotation: Updated by Grok on 2026-07-20 for hard/soft gates, merged-core authority, priority full text, and HTML delivery.
Grok annotation: Essential Core E1 research-methods route noted by Grok on 2026-07-20.
Grok annotation: E3-D current-state parity wording updated by Grok on 2026-07-21.
Codex annotation: Created by Codex on 2026-07-15.

## Research and proposal route

1. Read the guide and record scope, endpoints, population, methods, and hard
   constraints.
2. Produce three candidate directions when the guide is underspecified, then
   score fit, question clarity, gap, feasibility, and writability.
3. Write the search strategy, including an optional dual-route brief. Secondary
   discovery is acceleration only; primary must finish when secondary provider,
   CLI, auth, discovery, model, quota, network, or task is unavailable.
4. Search broadly before converging on core papers. Soft targets: about 80–120
   candidates for guide-first runs, 50–80 when the direction is already clear.
   Keep metadata separate from full text and record source quality.
5. If a secondary route is available, keep discovery blind and independent,
   then normalize DOI/title/year, deduplicate, compare omissions, re-screen the
   union, and record the outcome in `literature_route_status.json`.
6. After convergence, treat `MERGED_CORE_PAPERS.md` as the sole downstream
   authority. `core_papers.md` is only a pre-merge or single-route compatibility
   template and must state the authority transition.
7. Select 3–8 priority papers, attempt lawful OA-first acquisition, log every
   attempt, deep-read readable full text, and open a manual-action queue when
   access is unavailable. Never describe paywall bypass.
8. Parse difficult documents before semantic question answering. Keep raw
   source files outside the public repository and store only sanitized outputs.
9. Build evidence cards with claim, extract, inference/uncertainty, source, and
   limitation fields before drafting. Soft target: ≥60 cards when density allows.
10. Use field maps and counterevidence to identify gaps without turning trends
    into causal claims.
11. Draft one section at a time, then run paragraph-level editing without
    strengthening claims beyond the evidence.
12. For conclusion-bearing work, complete the HTML delivery checklist: UTF-8
    entry page, 3–8 decision-critical pages, responsive/print-friendly
    navigation, evidence-boundary text, and local-link checks. Markdown and
    structured artifacts remain authoritative.
13. Run prose linting and citation/provenance checks before producing a final
    reference draft or optional Word/PDF package.

## Hard and soft gates

| Gate | Type | Rule |
| --- | --- | --- |
| Primary route completion | hard | Continues even when every optional adapter/secondary is unset |
| Secondary fallback | hard | Record `primary_only` / failure reason; do not block |
| Blind merge protocol | hard | No early cross-reading of the other route's pool |
| Merged-core authority | hard | Downstream uses only `MERGED_CORE_PAPERS.md` after converge |
| Priority full text | hard | 3–8 OA-first attempts logged; manual queue on failure |
| No invented evidence | hard | No fabricated citations, statistics, reviewers, or results |
| HTML for conclusions | hard for conclusion-bearing runs | Entry + 3–8 pages, local links, evidence boundary, UTF-8 |
| Human confirmation | hard | Before final claims, design commitments, submission packaging |
| Candidate pool size | soft | 80–120 guide-first; 50–80 clear direction |
| Core paper count | soft | ≥20 after re-screen when evidence density allows |
| Evidence cards | soft | ≥60 with explicit epistemic fields |

## Writing route

Use `longform-writing` for structure, `academic-editing` for conservative
paragraph revision, and `prose-lint` for deterministic style findings. A lint
finding is a review prompt, not an instruction to change scientific meaning.

## Methods and integrity route

Keep systematic-review, citation-integrity, peer-review, and reproducibility
planning tasks on the `research-methods` entry. That entry is first-party
Essential Core packaging (`essential_core`): contracts, mode registry, templates
under `skills/research-methods/core/templates/`, dual agent surfaces, and an
opt-in offline runtime under `skills/research-methods/runtime/`. E2–E3 protocol
bodies are operational at `parity: partial`; E4 pipeline/experiment/optional_runtime
bodies remain `parity: not_started` and must not be advertised as complete ARS
parity. Partial depth is not real multi-process orchestration. The full Academic
Research Skills suite is optional external material and is not required for the
local route. Do not vendor or auto-install that suite from the proposal
deep-research path.

## Failure boundaries

- Missing optional executables produce `missing` results with an installation
  hint.
- A timeout or non-zero backend exit is surfaced to the caller.
- Unverified or conflicting evidence stays marked as uncertainty.
- Credentials are read only from the process environment and never written to
  workflow artifacts.
- Secondary discovery failure never cancels a completable primary route.
