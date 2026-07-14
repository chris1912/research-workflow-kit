# Workflow

Codex annotation: Created by Codex on 2026-07-15.

## Research and proposal route

1. Read the guide and record scope, endpoints, population, methods, and hard
   constraints.
2. Produce three candidate directions when the guide is underspecified, then
   score fit, question clarity, gap, feasibility, and writability.
3. Search broadly before converging on core papers; keep metadata separate from
   full text and record source quality.
4. Parse difficult documents before semantic question answering. Keep raw
   source files outside the public repository and store only sanitized outputs.
5. Build evidence cards with claim, extract, source, epistemic status, and
   limitation fields before drafting.
6. Use field maps and counterevidence to identify gaps without turning trends
   into causal claims.
7. Draft one section at a time, then run paragraph-level editing without
   strengthening claims beyond the evidence.
8. Run prose linting and citation/provenance checks before producing a final
   reference draft or Word/PDF package.

## Writing route

Use `longform-writing` for structure, `academic-editing` for conservative
paragraph revision, and `prose-lint` for deterministic style findings. A lint
finding is a review prompt, not an instruction to change scientific meaning.

## Failure boundaries

- Missing optional executables produce `missing` results with an installation
  hint.
- A timeout or non-zero backend exit is surfaced to the caller.
- Unverified or conflicting evidence stays marked as uncertain.
- Credentials are read only from the process environment and never written to
  workflow artifacts.

