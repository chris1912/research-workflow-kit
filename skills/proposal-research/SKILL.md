---
name: proposal-research
description: Build an evidence-backed grant or research proposal from a question, funder guidance, literature pool, and explicit review gates.
---

# Proposal Research

Grok annotation: Contract upgrade implemented by Grok on 2026-07-20 (Stage A dual-route, merged-core, priority full text, HTML delivery).
Grok annotation: Stage D research-methods thin-router handoff wording by Grok on 2026-07-20.
Codex annotation: Public alias prepared by Codex on 2026-07-15.

Read [`docs/START_HERE.html`](../../docs/START_HERE.html) first and announce the selected route. Work in a user-supplied run directory or a sanitized copy under `examples/minimal/`; never require real application files in the repository.

## Workflow

1. Parse the research question, population, intervention or exposure, comparator, outcome, and funder constraints. Decompose the guide and, when underspecified, score three candidate directions.
2. Write `search_strategy.md` with keyword expansion, dual-route brief, and converge criteria.
3. Run dual-route preflight into `literature_route_status.json`:
   - `primary_route` is always required for discovery work.
   - `secondary_provider` may be `null`, `grok`, or another independent provider.
   - Secondary discovery is optional acceleration only.
   - If secondary skill, CLI, auth, discovery, model, quota, network, or task is unavailable, set `selected_mode` to `primary_only` or `primary_only_after_secondary_failure`, record `fallback_reason`, and **continue**.
4. Discover candidate literature through the primary `discovery` path (adapter or equivalent user tools). Keep an optional secondary route **blind and independent** until both pools are frozen. Record DOI, source URL, date, and retrieval status in `candidate_literature_pool.csv`.
5. Normalize DOI/title/year, deduplicate, compare omissions, re-screen the union, and write the sole downstream authority to `MERGED_CORE_PAPERS.md`. Use `core_papers.md` only as a pre-merge or single-route compatibility snapshot and state the authority transition.
6. Select 3–8 priority papers in `priority_papers.md`. Attempt lawful OA-first acquisition, log every attempt in `fulltext_acquisition.csv`, deep-read readable full text with `deep_read_report.md`, and open `FULLTEXT_MANUAL_ACTION_REQUIRED.md` when access is unavailable. Never describe paywall bypass.
7. Parse supplied documents with `document_parse` and keep page or section provenance.
8. Build evidence cards with `evidence_qa` (or manual cards); separate **claim**, **extract**, **inference**, and **uncertainty**. Soft target: ≥60 cards when evidence density allows.
9. Use `literature_map` for trends and field structure, then use `research_synthesis` for a multi-source narrative. Keep counterevidence in `risks_and_counterevidence.md` and claim checks in `claim_verification.md`.
10. Draft with `longform-writing`, refine with `academic-editing`, and run `prose-lint` before export.
11. For conclusion-bearing runs, complete `html_delivery_checklist.md` and deliver a readable UTF-8 HTML entry page plus 3–8 decision-critical pages (shells: `core_papers_page.html`, `priority_papers_page.html`). Markdown/structured artifacts remain authoritative.

## Soft and hard gates

| Gate | Type | Expectation |
| --- | --- | --- |
| Guide decomposition / candidate directions | soft | 3 directions when the guide is underspecified |
| Broad search then converge | soft | guide-first 80–120 candidates; clearer direction 50–80 |
| Core papers | soft | ≥20 after re-screen when density allows |
| Evidence cards | soft | ≥60 with explicit epistemic fields |
| Dual-route fallback | hard | primary completes when secondary is unavailable |
| Blind merge protocol | hard | no early cross-reading of the other route's pool |
| Merged-core authority | hard | after convergence, only `MERGED_CORE_PAPERS.md` feeds downstream |
| Priority full text | hard | 3–8 OA-first attempts logged; manual queue on failure |
| Citation integrity | hard | do not invent citations, statistics, reviewers, or results |
| HTML delivery | hard for conclusions | entry page + 3–8 pages, local links, evidence boundary, UTF-8 |
| Human confirmation | hard | required before final claims, design commitments, or submission packaging |

## Evidence states

Use visible badges rather than prose implication alone:

- **claim**: source-backed assertion ready for careful use after check
- **extract**: quotation or tightly bound paraphrase with locator
- **inference**: interpretation beyond the extract
- **uncertainty**: conflict, missing access, weak support, or unverified item

## Required vs optional stages

**Required for a full deep-research proposal run:** guide/question parse, search strategy, primary discovery, merged or primary-final core list, evidence cards, risks/claim checks, draft, uncertainty log, and human review gate.

**Optional accelerators:** secondary discovery provider, external adapters (`discovery`, `document_parse`, `evidence_qa`, `literature_map`, `research_synthesis`), priority full-text acquisition when OA exists, HTML delivery for non-conclusion exploration, Word/PDF packaging.

The skill remains useful when every optional adapter and secondary provider is unset: produce templates, explicit `missing`/fallback status, metadata-level evidence, and manual next steps.

## Deliverables

Return at least:

- question/guide brief and `guide_decomposition.md` / `candidate_directions.md` as needed
- `search_strategy.md`, `literature_route_status.json`, candidate pool
- `core_papers.md` (compatibility) and `MERGED_CORE_PAPERS.md` (authority after converge)
- `priority_papers.md`, `fulltext_acquisition.csv`, manual queue and deep-read reports when full text is in scope
- evidence cards, field map, claim verification, risks, concept cards, final reference draft
- HTML checklist and pages for conclusion-bearing work
- style-check report when drafting completes

Link phase summaries to [`docs/START_HERE.html`](../../docs/START_HERE.html). Route systematic-review, integrity, peer-review, and reproducibility planning through `skills/research-methods` (thin first-party router and local templates). Do not vendor or auto-install the optional external methods suite from this skill.
