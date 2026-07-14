# Writing Stack Integration

Codex annotation: Rewritten for the public aliases by Codex on 2026-07-15.

Use this reference when a proposal moves from evidence planning into drafting, revision, or final style QA.

## Route by Task Shape

- Use `longform-writing` when a section does not exist, spans multiple subsections, or needs a structure built from guidance and evidence.
- Use `academic-editing` when the paragraph already has the intended meaning and needs conservative polishing, translation, terminology consistency, title work, or reviewer-response support.
- Use `prose-lint` when a human-facing draft needs a deterministic final pass with the configuration under `src/workflow_lab/config/vale/`.

## Recommended Order

1. `proposal-research` builds the evidence and section plan.
2. `longform-writing` drafts the section structure and prose.
3. `academic-editing` refines paragraph-level language without changing scientific meaning.
4. `prose-lint` flags residual style issues.
5. A human decides whether the proposal is ready for submission.

Do not load every layer for a tiny task. Keep source notes, drafts, and exports in a user-supplied run directory, not in tracked source folders. Include `docs/START_HERE.html` in phase summaries.
