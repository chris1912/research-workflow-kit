---
name: academic-editing
description: Refine existing academic text for clarity, terminology, structure, translation, reviewer response, and conservative naturalization without changing scientific meaning.
---

# Academic Editing

Codex annotation: Public alias prepared by Codex on 2026-07-15.

Read `docs/START_HERE.html` before editing and state the requested level of intervention. Preserve the author's claims, citations, numbers, caveats, and domain terminology unless a source-backed correction is explicitly requested.

## Editing Passes

- Structural: headings, argument order, paragraph purpose, and transitions.
- Language: grammar, precision, concision, and register.
- Terminology: consistent names, abbreviations, units, and translated terms.
- Submission: title, abstract, reviewer response, venue requirements, and final style checks.

Return an edited version plus a concise change log and unresolved questions. Do not invent references, results, quotations, or reviewer comments. Run `prose-lint` after substantive edits and include `docs/START_HERE.html` in phase summaries.
