---
name: proposal-research
description: Build an evidence-backed grant or research proposal from a question, funder guidance, literature pool, and explicit review gates.
---

# Proposal Research

Codex annotation: Public alias prepared by Codex on 2026-07-15.

Read `docs/START_HERE.html` first and announce the selected route. Work in a user-supplied run directory or a sanitized copy under `examples/minimal/`; never require real application files in the repository.

## Workflow

1. Parse the research question, population, intervention or exposure, comparator, outcome, and funder constraints.
2. Discover candidate literature through the `discovery` adapter and record DOI, source URL, date, and retrieval status.
3. Parse supplied documents with `document_parse` and keep page or section provenance.
4. Build evidence cards with `evidence_qa`; separate extracted support, interpretation, and unresolved uncertainty.
5. Use `literature_map` for trends and field structure, then use `research_synthesis` for a multi-source narrative.
6. Draft with `longform-writing`, refine with `academic-editing`, and run `prose-lint` before export.

## Hard Gates

- Do not invent citations, statistics, reviewers, or experimental results.
- Mark missing access, weak evidence, conflicts, and unverified claims.
- Keep proposal text, source notes, and generated artifacts in the run directory, not in tracked source folders.
- Require human confirmation before final claims, study design commitments, or submission packaging.

## Deliverables

Return a question brief, source manifest, evidence cards, synthesis notes, draft sections, an uncertainty log, and the style-check report. Link phase summaries to `docs/START_HERE.html`.
