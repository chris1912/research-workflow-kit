# Dependencies

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

The exact upstream URLs, commits, licenses, and bundled paths are recorded in
`THIRD_PARTY_MANIFEST.json`. Do not treat this table as a license grant.

