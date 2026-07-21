# NOTICE — Research Methods Essential Core

Grok annotation: Added by Grok on 2026-07-20 for Essential Core E0 packaging.
Grok annotation: E3-D parity honesty note updated by Grok on 2026-07-21.

## Implementation status

This package is a **first-party rewrite** of research-method contracts and
runtime surfaces for the Research Workflow Kit. It is **not** a restore of the
previously vendored Academic Research Skills trees under `ars/` or `codex/`.

Packaging mode: `essential_core` (see `manifest.json`).

## Conceptual lineage

Behavioral contracts (modes, reviewer independence, passport stages, integrity
verdicts, PRISMA/RoB/GRADE field requirements) are conceptually distilled from
the Academic Research Skills project and its Codex-oriented distribution:

| Source | URL | License |
| --- | --- | --- |
| academic-research-skills | https://github.com/Imbad0202/academic-research-skills | CC BY-NC-4.0 |
| academic-research-skills-codex | https://github.com/Imbad0202/academic-research-skills-codex | CC BY-NC-4.0 |

Local license text retained for provenance:

- `docs/licenses/academic-research-skills-license.txt`

## What is and is not bundled

- **Bundled:** first-party Essential Core files under `skills/research-methods/`
  listed in the accepted plan flat list (65 paths).
- **Not bundled:** full upstream ARS documentation, eval gold, CI, multi-locale
  READMEs, JSON Schema forest, or Claude plugin marketplace lifecycle.
- **Not claimed:** full ARS behavioral parity. E2–E3 protocol bodies are
  `parity: partial` only; E4–E5 remain `parity: not_started` until depth and
  quality gates for those stages pass. Partial depth is not multi-process
  orchestration and not a required external suite/runtime.

## Copy policy

Do not wholesale-copy upstream agent bodies or design docs into this pack.
Rewrite in first-party voice. Record conceptual anchors in `LINEAGE_INDEX.md`
and per-file lineage headers. Commercial-use implications of any CC BY-NC
derived material remain a user legal decision; this notice is attribution
mechanics, not legal advice.

## Optional external suite

Users may install the full upstream suite outside this repository. This kit
does not auto-install, submodule, or silently download it.
