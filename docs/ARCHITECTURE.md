# Architecture

Codex annotation: Created by Codex on 2026-07-15.

## Layers

1. **Intent layer**: turns a guide or question into a task type, scope, and
   required intermediate artifacts.
2. **Evidence layer**: discovers sources, parses documents, answers questions
   over a local corpus, and produces literature maps.
3. **Synthesis layer**: combines source-backed findings while preserving the
   distinction between evidence, inference, uncertainty, and proposal design.
4. **Writing layer**: drafts long sections, revises paragraphs, keeps terms
   consistent, and prepares reviewer-facing responses.
5. **Quality layer**: runs deterministic prose rules and provenance checks before
   a human reviews the final Markdown or Word/PDF package.

## Data flow

```text
guide.md / question
  -> discovery metadata
  -> parsed Markdown or JSON
  -> evidence cards and corpus answers
  -> field map and counterevidence
  -> draft sections
  -> edited text
  -> lint report and delivery package
```

The first-party adapters in `src/workflow_lab/adapters/` only invoke configured
local commands. They preserve the backend's stdout/stderr and return a stable
status record; they do not fabricate claims or silently switch methods.

## Public aliases

The public skill names are intentionally neutral. The complete mapping to
upstream repositories, licenses, commits, and included paths is maintained in
`docs/THIRD_PARTY_MANIFEST.json`.

