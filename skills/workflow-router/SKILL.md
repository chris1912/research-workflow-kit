---
name: workflow-router
description: Route scientific research tasks from question and literature discovery through parsing, evidence review, synthesis, drafting, editing, and style checks.
---

# Workflow Router

Grok annotation: Updated by Grok on 2026-07-20 for optional dual-route discovery, evidence badges, and HTML final gate.
Grok annotation: Essential Core E1 research-methods routing note by Grok on 2026-07-20.
Codex annotation: Public entrypoint prepared by Codex on 2026-07-15.

## First Action

Read [`docs/START_HERE.html`](../../docs/START_HERE.html) before choosing a route. Tell the user which stage is selected, which stages are required vs optional, which optional backend is needed, and what evidence boundary applies.

## Route By Task

- Proposal or research direction: `proposal-research`, then `research-methods` when protocol or integrity gates are needed.
- Proposal revision or reviewer response: `proposal-iteration`.
- Paper discovery and metadata: the `discovery` adapter with a locally installed paper-search command.
- Optional secondary literature route: any independent provider configured by the user (`secondary_provider` may be `grok`, another provider, or `null`). Never block the primary route when secondary is unavailable.
- PDF, DOCX, image, or scan parsing: the `document_parse` adapter with a locally installed document parser.
- Corpus questions and evidence cards: the `evidence_qa` adapter with a locally installed corpus QA tool.
- Bibliometrics and field maps: the `literature_map` adapter with a locally installed analysis tool.
- Broad multi-source synthesis: the `research_synthesis` adapter with a locally installed research tool.
- Long-form structure and drafting: `longform-writing`.
- Paragraph-level academic refinement: `academic-editing`.
- Deterministic prose checks: `prose-lint` and the Vale configuration under `src/workflow_lab/config/vale/`.
- Systematic review, integrity, peer-review, or reproducibility planning: `research-methods` Essential Core (`essential_core`) with mode registry, contracts, templates, and opt-in offline runtime; E2 RQ/deep/SR and E3 paper/integrity/review are operational `parity: partial`, while E4 pipeline/experiment/optional_runtime remain `parity: not_started`. Partial depth is not full ARS behavioral parity. The full Academic Research Skills suite is optional external material and must not be auto-installed from this router.

## Evidence Rules

Treat search results as candidates until metadata, source provenance, and claim support are checked. Keep scientific content unchanged inside adapters. Require human confirmation for decisions that affect study design, claims, citations, or submission-ready text.

Use explicit evidence badges in artifacts and summaries:

- **claim**
- **extract**
- **inference**
- **uncertainty**

After literature convergence, treat `MERGED_CORE_PAPERS.md` as the sole downstream authority. `core_papers.md` is a pre-merge or single-route compatibility template.

## Dual-route and fallback

1. Primary discovery must complete.
2. Secondary discovery is optional coverage/acceleration only.
3. Preserve blind independent discovery before merge.
4. Normalize DOI/title/year, deduplicate, compare omissions, re-screen the union, and record the outcome in `literature_route_status.json`.
5. If secondary provider, CLI, auth, discovery, model, quota, network, or task is unavailable, finish in `primary_only` mode with an explicit reason.

## Priority full text

For deep-research runs that need full text, select 3–8 priority papers, attempt lawful OA-first acquisition, log attempts, deep-read readable text, and open a manual-action queue when access fails. Never describe paywall bypass.

## HTML final gate

Markdown and structured files remain authoritative. Conclusion-bearing runs also need a readable UTF-8 HTML entry page plus 3–8 decision-critical pages, responsive/print-friendly navigation, visible evidence-boundary text, and local-link checks. Use `html_delivery_checklist.md` and the public HTML shells under `skills/proposal-research/templates/`.

## Optional Backends

Adapters call commands supplied by environment variables such as `WORKFLOW_LAB_DISCOVERY_CMD`. Missing dependencies return an explicit error; they never silently downgrade to an unrelated tool. See [`docs/DEPENDENCIES.md`](../../docs/DEPENDENCIES.md) and [`docs/INSTALL.md`](../../docs/INSTALL.md). The kit remains useful when every optional adapter is unset.

## Output Habit

For every phase summary, route choice, check result, risk note, or next-step suggestion, include the repository-relative manual link `docs/START_HERE.html`.
