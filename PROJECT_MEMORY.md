# Project Memory

Codex annotation: Created by Codex on 2026-07-15.

## Project

- Name: `research-workflow-kit`
- Purpose: route evidence-aware research tasks through optional local backends,
  reusable skills, and deterministic writing checks.
- Release shape: first-party adapters and skills only; no virtual environments,
  nested Git repositories, secrets, or personal research runs.

## Decisions

- Public directories use neutral aliases while provenance documents retain the
  original source names and commits.
- Runtime backends are optional and configured through environment variables.
- The first-party layer uses the MIT license.
- The source workspace remains separate from the publish candidate.

## Current route

1. Research question and guide decomposition.
2. Literature discovery and document parsing.
3. Evidence QA and literature mapping.
4. Research synthesis and long-form drafting.
5. Academic editing, prose linting, and final packaging.

## Risks

- External providers may require credentials or network access.
- The research-method skill carries a non-commercial upstream license.
- No copied content from the unlicensed prompt reference library is included.

## Verification

Codex annotation: Verified by Codex on 2026-07-15.

- `python -m pytest`: 6 tests passed.
- `python -m compileall -q src tests scripts`: passed; generated caches were removed.
- Formatter smoke test: passed with a temporary Word output and no tracked binary.
- JSON/JSONL templates: parsed successfully.
- HTML desktop/mobile browser check: both pages loaded without console errors and all relative links resolved.
- Publish-tree scan: no nested Git metadata, junctions, secrets, absolute machine paths, binaries, or generated caches.

## GitHub Publication

Codex annotation: Published by Codex on 2026-07-15.

- repository: `https://github.com/chris1912/research-workflow-kit`
- visibility: public
- default branch: `main`
- latest local commit: `a696325`
- GitHub Actions quality workflow: passing after the repository-metadata scan fix

## Update rule

Update this file when the public tree, route order, provenance policy, or
external dependency contract changes.
