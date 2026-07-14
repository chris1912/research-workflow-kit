---
name: workflow-router
description: Route scientific research tasks from question and literature discovery through parsing, evidence review, synthesis, drafting, editing, and style checks.
---

# Workflow Router

Codex annotation: Public entrypoint prepared by Codex on 2026-07-15.

## First Action

Read `docs/START_HERE.html` before choosing a route. Tell the user which stage is selected, which optional backend is needed, and what evidence boundary applies.

## Route By Task

- Proposal or research direction: `proposal-research`, then `research-methods` when protocol or integrity gates are needed.
- Proposal revision or reviewer response: `proposal-iteration`.
- Paper discovery and metadata: the `discovery` adapter with a locally installed paper-search command.
- PDF, DOCX, image, or scan parsing: the `document_parse` adapter with a locally installed document parser.
- Corpus questions and evidence cards: the `evidence_qa` adapter with a locally installed corpus QA tool.
- Bibliometrics and field maps: the `literature_map` adapter with a locally installed analysis tool.
- Broad multi-source synthesis: the `research_synthesis` adapter with a locally installed research tool.
- Long-form structure and drafting: `longform-writing`.
- Paragraph-level academic refinement: `academic-editing`.
- Deterministic prose checks: `prose-lint` and the Vale configuration under `src/workflow_lab/config/vale/`.

## Evidence Rules

Treat search results as candidates until metadata, source provenance, and claim support are checked. Keep scientific content unchanged inside adapters. Require human confirmation for decisions that affect study design, claims, citations, or submission-ready text.

## Optional Backends

Adapters call commands supplied by environment variables such as `WORKFLOW_LAB_DISCOVERY_CMD`. Missing dependencies return an explicit error; they never silently downgrade to an unrelated tool. See `docs/DEPENDENCIES.md` and `docs/INSTALL.md`.

## Output Habit

For every phase summary, route choice, check result, risk note, or next-step suggestion, include the repository-relative manual link `docs/START_HERE.html`.
