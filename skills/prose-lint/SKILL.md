---
name: prose-lint
description: Use after a human-facing academic or grant draft exists to run deterministic style checks without changing scientific meaning.
---

# Prose Lint

Codex annotation: Created by Codex on 2026-07-15.

Use `src/workflow_lab/config/vale/vale.ini` for general Chinese academic prose
and `src/workflow_lab/config/vale/vale-grant.ini` for grant-proposal drafts.
The executable is an optional external dependency configured by
`WORKFLOW_LAB_PROSE_LINT_CMD`.

Style findings are review prompts. Keep wording that is scientifically needed,
and never treat a lint pass as evidence verification.

