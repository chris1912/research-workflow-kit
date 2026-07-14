# Public Name Map

Codex annotation: Name map prepared by Codex on 2026-07-15.

The public tree uses neutral names so users can learn the workflow without treating upstream project names as first-party modules. The complete source, commit, license, and modification record is in `docs/THIRD_PARTY_MANIFEST.json`.

| Public name | Source role | Distribution mode |
| --- | --- | --- |
| `workflow-router` | Local workflow router | First-party entrypoint |
| `proposal-research` | Grant and proposal research workflow | First-party entrypoint built from local material |
| `proposal-iteration` | Proposal revision loop | First-party entrypoint built from local material |
| `research-methods` | Structured research design and integrity gates | Bundled third-party methods material behind a first-party entrypoint |
| `longform-writing` | Long-form drafting and section architecture | Bundled skill material behind a first-party entrypoint |
| `academic-editing` | Academic polishing and terminology review | Bundled skill material behind a first-party entrypoint |
| `prose-lint` | Vale style-check workflow | First-party entrypoint for an external executable |

The optional runtime backends are intentionally exposed only through neutral adapters in `src/workflow_lab/adapters/`. Their original names remain in the notices and manifest for attribution and license auditing.
