<!--
essential_core_lineage:
  file: core/templates/rebuttal_audit.md
  implementation: first-party-rewrite
  upstream_concepts:
    - rebuttal audit
    - evaluator-only coverage matrix
  upstream_path_hints:
    - ars rebuttal-audit command
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Rebuttal Audit (evaluator-only)

Grok annotation: Essential Core E3-B designated rebuttal template by Grok on 2026-07-20.

**parity: partial** — Designated surface for rebuttal-audit mode. Protocol prose
elsewhere cannot rescue hollow fields here. Evaluator-only: **no** generated
author rebuttal prose as a pass product.

## Scope

- Manuscript / revision id:
- Review round:
- Auditor role (evaluator only):
- Change ledger pointer:
- Evidence pointer set:

### evaluator_only

This template is evaluator-only. Record coverage, gaps, response_kind
consistency, tone/overclaim flags, and unresolved blocks. Do not ship
generated_response_prose as a successful audit artifact. Author letter drafting
belongs outside this mode.

### point_coverage_matrix

Every reviewer point_id must appear exactly once. Coverage ∈
{covered, partial, missing}. Duplicate point rows hide gaps and fail. Partial
requires a non-empty gap note/pointer. Missing blocks audit-clean.

| point_id | reviewer_text_summary | coverage | gap_note | risk_flags |
| --- | --- | --- | --- | --- |
|  |  | covered / partial / missing |  |  |

### change_or_evidence_or_rationale

Map each point to exactly one response_kind:

- `ms_change` — must link to a change_ledger row listing this point_id
- `evidence` — must provide a non-empty evidence pointer
- `no_change_rationale` — must provide a non-empty rationale pointer/text

Claimed manuscript changes absent from the ledger fail
(`asserted_change_absent`). Empty evidence or empty no-change rationale fails.

| point_id | response_kind | pointer_or_rationale | change_id (if ms_change) |
| --- | --- | --- | --- |
|  | ms_change / evidence / no_change_rationale |  |  |

### tone_overclaim_flags

Flag adversarial tone, dismissiveness, unsupported superiority claims, and
overclaim relative to evidence. Flags escalate review; they do not invent
missing evidence. Record none explicitly when clean after human skim.

| point_id | tone_flag | overclaim_flag | notes |
| --- | --- | --- | --- |
|  | none / mild / severe | none / mild / severe |  |

### unresolved_escalation

Any coverage=missing, partial without gap note, asserted change absent from
ledger, empty evidence/rationale, duplicate point_id, or non-empty
generated_response_prose blocks audit-clean. List unresolved point_ids and the
blocking error class. Do not mark clean while unresolved remains.

| unresolved_point_id | block_reason | required_human_action |
| --- | --- | --- |
|  |  |  |

## Human gates

- [ ] All reviewer points inventoried with stable ids
- [ ] No generated author response prose treated as audit pass
- [ ] ms_change rows linked to change ledger
- [ ] Unresolved list empty before clean pass language
- [ ] Human reviewed tone/overclaim flags
