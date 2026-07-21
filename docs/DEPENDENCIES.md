# Dependencies

Grok annotation: Stage D optional methods-suite boundary added by Grok on 2026-07-20.
Grok annotation: Essential Core E0+E1 packaging boundary updated by Grok on 2026-07-20.
Grok annotation: E3-D current-state parity wording updated by Grok on 2026-07-21.
Codex annotation: Created by Codex on 2026-07-15.

The public repository contains adapters and skills, not the large upstream
runtime environments. Install optional tools independently and keep their
licenses and credentials separate.

| Workflow stage | Environment variable | Typical executable | Notes |
| --- | --- | --- | --- |
| Discovery | `WORKFLOW_LAB_DISCOVERY_CMD` | `paper-search` | Metadata and open-access retrieval may need API limits or email. |
| Document parsing | `WORKFLOW_LAB_DOCUMENT_CMD` | `mineru` | The parser has its own copyleft license and model downloads. |
| Evidence QA | `WORKFLOW_LAB_EVIDENCE_CMD` | `pqa` | Use only a corpus you are allowed to process. |
| Literature map | `WORKFLOW_LAB_LITERATURE_CMD` | user command | The analysis package may be installed in a separate environment. |
| Research synthesis | `WORKFLOW_LAB_SYNTHESIS_CMD` | user command | Network and model provider credentials are external. |
| Prose lint | `WORKFLOW_LAB_PROSE_LINT_CMD` | `vale` | Use `src/workflow_lab/config/vale/` for the local profiles. |

## Optional research-methods suite (not bundled)

`skills/research-methods` ships first-party packaging mode `essential_core`
(contracts, mode registry, templates, opt-in offline runtime). E2–E3 protocol
bodies are operational at `parity: partial`; E4 pipeline/experiment/optional_runtime
bodies remain `parity: not_started`. Partial depth is not full ARS behavioral
parity. The full Academic Research Skills suite is **optional external** material
and is **not** a required runtime dependency of this kit.

| Item | Guidance |
| --- | --- |
| Local offline path | Use `skills/research-methods/SKILL.md`, `core/`, and `runtime/` |
| Upstream suite | https://github.com/Imbad0202/academic-research-skills |
| Codex-oriented distribution | https://github.com/Imbad0202/academic-research-skills-codex |
| License notes retained here | `docs/licenses/academic-research-skills-license.txt` |
| Install boundary | User-managed checkout outside this repository if desired; no auto-install script, submodule, or silent download from this kit |
| Absence is normal | Essential Core offline path remains supported when the external suite is unset |

The exact upstream URLs, commits, licenses, and packaging modes are recorded in
`THIRD_PARTY_MANIFEST.json`. Do not treat this table as a license grant.

