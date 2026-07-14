# Third-Party Notices

Codex annotation: Created by Codex on 2026-07-15.

This repository contains a first-party orchestration layer plus selected skills
and rules derived from open-source projects. Public directory aliases are not
claims of authorship. The original project names, URLs, commits, licenses, and
included paths are recorded in `THIRD_PARTY_MANIFEST.json`.

## Bundled skills

- `research-methods` is materialized from `academic-research-skills-codex` and
  remains under CC BY-NC 4.0. The original license is in
  `docs/licenses/academic-research-skills-license.txt`.
- `academic-editing` is materialized from `academic-writing-assistant` under
  MIT. The original license is in `docs/licenses/academic-writing-assistant-license.txt`.
- `longform-writing` is materialized from `research-writing-skill` under MIT.
  The original license is in `docs/licenses/research-writing-skill-license.txt`.

## External runtimes

The adapters reference `paper-search-mcp`, `MinerU`, `paper-qa`, `litstudy`,
`gpt-researcher`, and Vale without copying their runtime source. Install those
projects separately and follow their own license terms. Their local license
texts are preserved for reference under `docs/licenses/`.

`gpt-researcher` has conflicting license declarations between its repository
license file and package metadata, so this project does not vendor its source.
`MinerU` is treated as AGPL-3.0 based on its license file and is also external.

## Link-only reference

`awesome-ai-research-writing` is referenced as an external prompt library only.
No README or prompt text is copied because no redistributable license was found
in the local checkout.

## First-party changes

The first-party adapters, public aliases, Vale profiles, documentation, and
templates in this repository are MIT licensed. Changes to bundled skills are
limited to materializing the directory, changing public-facing route names,
and adding provenance notes; the original skill rules and attribution remain.

Some retained upstream method notes link to showcase PDFs or fixtures that are
intentionally omitted from this publish tree. Those links are documentation
references only and are not runtime dependencies of `research-methods`.

The document formatter under `src/workflow_lab/formatting/` was extracted from
the original workspace's local `tools/formatter` utility, then made relative-
path based and stripped of sample output binaries. The Vale profiles under
`src/workflow_lab/config/vale/` were likewise moved from the original local
configuration and contain project-specific rules rather than the Vale runtime.
