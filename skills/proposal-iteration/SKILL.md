---
name: proposal-iteration
description: Iteratively improve a proposal or manuscript with structured diagnosis, evidence checks, reviewer simulation, and controlled revision.
---

# Proposal Iteration

Codex annotation: Public alias prepared by Codex on 2026-07-15.

Read `docs/START_HERE.html` and state the stage before editing. Treat the supplied draft as the source of truth and write each revision to a new run directory or versioned output.

## Loop

1. Freeze the input draft and record its version, scope, and known constraints.
2. Diagnose logic, evidence, structure, terminology, compliance, and style separately.
3. Run only the checks relevant to the diagnosed issue; preserve citations and numeric claims unless a source-backed correction is requested.
4. Apply a small revision, record the reason and affected sections, then re-run the relevant checks.
5. Finish with `academic-editing`, `prose-lint`, and a human review of scientific meaning.

## Guardrails

- Never hide uncertainty or turn a suggestion into a fact.
- Never replace a citation without recording the reason and source.
- Keep reviewer comments, change logs, and final exports outside tracked code.
- Stop when requested criteria pass or when the next change would require a scientific decision from the user.

## Deliverables

Provide a diagnosis matrix, revision log, updated draft path, unresolved-risk list, and check results. Include the manual link `docs/START_HERE.html` in each phase summary.
