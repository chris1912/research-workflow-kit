<!--
essential_core_lineage:
  file: core/templates/revision_roadmap.md
  implementation: first-party-rewrite
  upstream_concepts:
    - revision roadmap
    - commitment ledger
    - protected claims
    - recovery checkpoint
  upstream_path_hints:
    - ars revision coach
    - commitment ledger examples
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Revision Roadmap

Grok annotation: Essential Core E3-B designated revision template by Grok on 2026-07-20.

**parity: partial** — Designated surface for revision and revision-coach modes.
Protocol prose in `academic_paper.md` cannot rescue hollow fields here. Not
deterministic patch-apply parity.

## Scope

- Manuscript / version id:
- Mode: revision / revision-coach
- Before pointer:
- After pointer (revision only):
- Author:

### commitment_ledger

Track reviewer or self-critique commitments with columns: concern_id,
commitment_text, commitment_type, required_evidence_type, and
fulfillment_status (extracted | planned | in_progress | fulfilled |
waived_with_rationale). Waivers require human confirmation. Do not delete
open commitments silently when resuming a version family.

| concern_id | commitment_text | commitment_type | required_evidence_type | fulfillment_status |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### patch_or_change_ledger

Named change units for revision mode. Each row: change_id, op
(add|delete|replace|move|annotate), target span or quote, summary, linked
concern_ids, evidence_state if content is claim-bearing. A row that claims a
replace/delete while the target remains unchanged in after-text is a false
ledger claim. Coach mode may leave ops planned without applying after-text.

| change_id | op | target | summary | concern_ids | evidence_state |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

### protected_claims

List protected claims and hedges that must survive unless a ledgered
delete/replace names them and author_signoff is true. Soft hedges
(may/might/suggests/possibly) must not be silently upgraded to hard claims.
Helpers may escalate risk; they never prove semantic preservation.

| claim_or_hedge | protection_reason | disposition | ledger_change_id |
| --- | --- | --- | --- |
|  |  | retain / ledgered_change |  |

### author_signoff

Mandatory human gate for protected changes and conclusion-bearing new
evidence. Record signer, timestamp, and scope. Model confidence or chat tone
never substitutes for author_signoff=true.

- Signer:
- Timestamp:
- Scope covered:
- author_signoff (true/false):

### revision_recovery

Recovery checkpoint for interrupted or major revisions. Require a non-empty
checkpoint id/note when recovery_required is set. Resume from ledger state; do
not wipe history and pretend a clean restart. Record last good version pointer.

- recovery_required (true/false):
- recovery_checkpoint:
- last_good_version:
- resume_notes:

### version_family_reconciliation

Surface preprint versus published, version-of-record updates, and conflicting
numbers across the version family. Do not auto-swap identities or silently
reconcile conflicting results; keep both with notes until human chooses.

| version_id | kind (preprint/VoR/other) | conflict_note | human_resolution |
| --- | --- | --- | --- |
|  |  |  |  |

### new_evidence_gate

New citations, DOIs, numeric results, or primary-finding language introduced in
after-text must be listed with evidence_state in {claim, extract,
human-confirmed} and human_gate true when conclusion-bearing. Silent inserts
fail the revision transition helper.

| citation_or_result_id | claim | evidence_state | human_gate | notes |
| --- | --- | --- | --- | --- |
|  |  |  | true/false |  |

## Issue tracking (coach + revision)

| Issue ID | Source reviewer | Severity | Disposition | Planned change | Evidence pointer |
| --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  |

Score trajectory (re-review): `open | partially_addressed | addressed | new`.

## Human gates

- [ ] Protected claims reviewed
- [ ] Change ledger honest (no false claims)
- [ ] New evidence gated
- [ ] Author sign-off recorded when required
- [ ] Recovery checkpoint present if resuming
