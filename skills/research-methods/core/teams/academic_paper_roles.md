<!--
essential_core_lineage:
  file: core/teams/academic_paper_roles.md
  implementation: first-party-rewrite
  upstream_concepts:
    - academic paper role card
    - agent roles merge
  upstream_path_hints:
    - skills/research-methods/ars/.../academic_paper
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Academic Paper Role Card

Grok annotation: Essential Core internal role card by Grok on 2026-07-20 (E1).
Grok annotation: E3-B mode-scoped role obligations by Grok on 2026-07-20.

This is an **internal** role card (not a Codex runtime prompt). Codex invocation lives under `runtime/agents/`.

## Purpose

Generators emit claim-intent pre-commit. Peer reviewer here is evaluator-only; full multi-perspective panel uses reviewer_panel_roles. Eleven paper modes bind here via `core/protocols/academic_paper.md` (`parity: partial`).

## Roles

### intake

Collect mode token, audience/venue, constraints, and known evidence gaps.
Refuse to invent missing funding/COI/AI facts for disclosure. Route vague topics
toward plan or research-question refinement before full drafting.

### literature_strategist

Own lit-review mode handoffs to E2 discovery/SR surfaces. Build paper-format
synthesis only from supplied or lawfully retrieved sources. Never claim full
PRISMA completion from paper lit-review alone.

### structure_architect

Own plan and outline-only modes. Negotiate chapters, evidence-map placeholders,
and argument-map edges. Do not smuggle full draft body as “outline complete.”

### argument_builder

Maintain claim-intent nodes, support_status slots, dependencies, and
counterpoints in `argument_map.md`. Pre-commit before full-mode prose for
high-stakes claims.

### draft_writer

Generator for full and revision modes. Emit claim-intent pre-commit; preserve
protected hedges unless ledgered with author_signoff; never invent results.
Revision must write change/commitment ledgers and recovery checkpoints.

### citation_compliance

Own citation-check mode. Bind inventory rows to citation_integrity contracts.
DOI/token/similarity never promote to VERIFIED without locator/extract and
approved assessment source.

### abstract_bilingual

Own abstract-only mode. Fill bilingual fields honestly; mark missing languages
`missing`. Preserve protected hedges from source claims.

### peer_reviewer_evaluator

Evaluator-only. Own rebuttal-audit coverage matrix, tone/overclaim flags, and
unresolved blocks. Do not generate author response prose as a pass artifact.

### formatter_partial

Own format-convert mode. Checklist + engine honesty; never fake PDF/DOCX
success when tooling is unset.

### revision_coach

Roadmap-only coach. Structure issues into `revision_roadmap.md` without full
manuscript rewrite. Hand off mutation work to revision mode.

## Mode ↔ primary role map

| Mode | Primary role | Generator / Evaluator |
| --- | --- | --- |
| full | draft_writer + argument_builder | generator |
| plan | structure_architect + intake | generator |
| outline-only | structure_architect | generator |
| revision | draft_writer | generator (ledgered) |
| revision-coach | revision_coach | coach |
| abstract-only | abstract_bilingual | generator |
| lit-review | literature_strategist | generator + E2 handoff |
| format-convert | formatter_partial | generator (checklist) |
| citation-check | citation_compliance | evaluator-leaning |
| disclosure | intake + citation_compliance | generator + human confirm |
| rebuttal-audit | peer_reviewer_evaluator | evaluator-only |

## Shared hard rules

- Separate claim / extract / inference / uncertainty / missing / blocked / human-confirmed
- No fabricated citations, statistics, or reviewer identities
- Prefer offline honesty when backends are unset
- Human gates for design, integrity sign-off, disclosure confirmation, and submission-ready text
- Protected claims/hedges require ledger + author_signoff to change
- Rebuttal-audit never ships generated response prose as pass
