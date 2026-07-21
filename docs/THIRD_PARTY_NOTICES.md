# Third-Party Notices

Grok annotation: Stage D packaging update by Grok on 2026-07-20 for optional-external methods suite.
Grok annotation: Essential Core E0+E1 packaging update by Grok on 2026-07-20.
Codex annotation: Created by Codex on 2026-07-15.

This repository contains a first-party orchestration layer plus selected skills
and rules derived from open-source projects. Public directory aliases are not
claims of authorship. The original project names, URLs, commits, licenses, and
included paths are recorded in `THIRD_PARTY_MANIFEST.json`.

## Bundled skills

- `research-methods` is first-party packaging mode `essential_core` under MIT
  first-party packaging: contracts, mode registry, templates, dual agent
  surfaces, and opt-in offline runtime. It is a first-party rewrite of method
  contracts, not a restore of the former vendored trees. The full Academic
  Research Skills suite is **not bundled** in this tree and is **not** a
  required runtime dependency. Upstream projects historically associated with
  this route are `academic-research-skills` and
  `academic-research-skills-codex` (CC BY-NC 4.0 as stated in their license
  texts). Retained provenance license file:
  `docs/licenses/academic-research-skills-license.txt`. See also
  `skills/research-methods/NOTICE.md` and `LINEAGE_INDEX.md`. Users who want
  the full suite must install it outside this repository under upstream terms;
  this kit does not auto-install or silently download it.
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
first-party templates in this repository are MIT licensed. Bundled writing and
editing skills retain their original licenses and attribution. The former
vendored methods body under `skills/research-methods/ars` and
`skills/research-methods/codex` is no longer present; the stable public route
now ships Essential Core first-party surfaces plus provenance notices.

Do not treat retained license texts as a claim that the full upstream suite is
still shipped in this repository.

The document formatter under `src/workflow_lab/formatting/` was extracted from
the original workspace's local `tools/formatter` utility, then made relative-
path based and stripped of sample output binaries. The Vale profiles under
`src/workflow_lab/config/vale/` were likewise moved from the original local
configuration and contain project-specific rules rather than the Vale runtime.
