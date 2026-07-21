# Architecture

Grok annotation: Updated by Grok on 2026-07-20 for dual-route evidence layer and HTML delivery layer.
Grok annotation: Stage D thin research-methods packaging noted by Grok on 2026-07-20.
Grok annotation: Essential Core E0+E1 packaging noted by Grok on 2026-07-20.
Grok annotation: E3-D current-state parity wording updated by Grok on 2026-07-21.
Codex annotation: Created by Codex on 2026-07-15.

## Layers

1. **Intent layer**: turns a guide or question into a task type, scope, and
   required intermediate artifacts.
2. **Evidence layer**: discovers sources (primary always; optional secondary),
   merges core literature, parses documents, answers questions over a local
   corpus, and produces literature maps.
3. **Synthesis layer**: combines source-backed findings while preserving the
   distinction between evidence, inference, uncertainty, and proposal design.
4. **Writing layer**: drafts long sections, revises paragraphs, keeps terms
   consistent, and prepares reviewer-facing responses.
5. **Delivery layer**: keeps Markdown/structured artifacts authoritative and
   adds human-readable HTML packages for conclusion-bearing runs.
6. **Quality layer**: runs deterministic prose rules and provenance checks before
   a human reviews the final Markdown, HTML, or optional Word/PDF package.

## Data flow

```text
guide.md / question
  -> search strategy + literature_route_status.json
  -> primary discovery metadata (+ optional blind secondary pool)
  -> normalize / dedupe / re-screen
  -> MERGED_CORE_PAPERS.md (authority) + compatibility core_papers.md
  -> priority 3-8 OA-first full text log + deep reads or manual queue
  -> parsed Markdown or JSON
  -> evidence cards and corpus answers
  -> field map and counterevidence
  -> draft sections
  -> edited text
  -> HTML entry + 3-8 decision pages when conclusions are delivered
  -> lint report and delivery package
```

### Evidence-layer dual-route box

| Role | Behavior |
| --- | --- |
| Primary | Required for discovery-bearing work; must complete |
| Secondary | Optional; `secondary_provider` may be `null`, `grok`, or other |
| Merge | Blind pools first; then DOI/title/year normalize, dedupe, omission compare, re-screen |
| Authority | `MERGED_CORE_PAPERS.md` only after convergence |
| Fallback | Missing secondary capability → `primary_only` with reason |

### Delivery-layer HTML vs Markdown

| Artifact class | Authority | Role |
| --- | --- | --- |
| Markdown / CSV / JSON / JSONL | Source of truth | Machine- and human-auditable run record |
| HTML shells and run pages | Delivery view | Readable navigation for collaborators; must not silently override Markdown |
| Word / PDF | Optional export | External packaging only |

## First-party adapters

The first-party adapters in `src/workflow_lab/adapters/` only invoke configured
local commands. They preserve the backend's stdout/stderr and return a stable
status record; they do not fabricate claims or silently switch methods. Dual-route
status and HTML delivery in this upgrade are contract/template concerns and do
not require new runtime backends.

## Public aliases

The public skill names are intentionally neutral. The complete mapping to
upstream repositories, licenses, commits, and included paths is maintained in
`docs/THIRD_PARTY_MANIFEST.json`.

## Methods pack packaging

`skills/research-methods` is first-party packaging mode `essential_core`: mode
registry, seven contracts, protocol/template surfaces, dual agent cards, and an
opt-in offline runtime under `runtime/`. E2–E3 protocol bodies are operational at
`parity: partial` (RQ/deep/SR + paper/integrity/manuscript review). E4 bodies
(`academic_pipeline`, `experiment`, `optional_runtime`) remain
`parity: not_started`. Partial depth is not full ARS behavioral parity and not
real multi-process orchestration. The full Academic Research Skills suite remains
optional external material: not vendored under `ars/` or `codex/`, not a required
runtime, and not auto-installed by this kit. Retained license texts under
`docs/licenses/` and provenance rows in the third-party manifest record conceptual
lineage only.
