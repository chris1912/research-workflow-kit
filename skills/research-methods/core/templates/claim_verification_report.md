<!--
essential_core_lineage:
  file: core/templates/claim_verification_report.md
  implementation: first-party-rewrite
  upstream_concepts:
    - claim verification report
    - sampling modes
    - access and pass/fail criteria
  upstream_path_hints:
    - ars claim verification
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Claim Verification Report

Grok annotation: Essential Core template by Grok on 2026-07-20.
Grok annotation: E3-A designated claim report fields by Grok on 2026-07-20.

**parity: partial** — E3-A claim-verification surface. Not full ARS detector
parity. This designated surface must pass independently; protocol or audit
duplicates elsewhere cannot rescue hollow fields here.

## Report header

- Manuscript or run ID:
- Reviewer / checker:
- Date:
- Sampling mode (Mode1 / Mode2):
- Strict mode (yes/no):

### report_scope

Identify the manuscript or run, checker, date, Mode1 sampling versus Mode2
full-scope, and whether strict mode forbids MAJOR_DISTORTION and bare
UNVERIFIABLE on in-scope high-stakes claims. Document residual unchecked claims
for Mode1.

### citation_identity

For each claim row, record supporting citation identity fields (title/authors/
year/venue/DOI-or-id). Incomplete identity (missing both title and durable id)
cannot support VERIFIED. Do not invent identifiers.

### locator_or_quote

Every scored claim needs a locator (page/section/figure/table/paragraph) or a
short extract. DOI-only or citation-token-only rows stay unverified. Fabricated
page numbers are forbidden.

### claim_source_fidelity

| Claim ID | Claim text | Extract + locator | Support status | Assessment source | Verdict | Evidence state | Risk flags | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
|  |  |  | supported / partial / contradicted / unsupported / unknown | human_confirmed / verified_adapter / heuristic_only / none | VERIFIED / MINOR_DISTORTION / MAJOR_DISTORTION / UNVERIFIABLE / UNVERIFIABLE_ACCESS | claim / extract / inference / uncertainty / missing / blocked / human-confirmed |  |  |

`VERIFIED` requires supported status, locator or extract, coherent access and
risk state, and assessment_source of human_confirmed or verified_adapter.
Heuristic similarity may only downgrade, escalate, or leave unknown.

### access_state

Per claim/source row: verified | unverified | unresolvable | access_blocked.
Access-blocked or unresolvable cannot pair with VERIFIED. Use
UNVERIFIABLE_ACCESS when identity is known but text cannot be read lawfully.

### temporal_version_check

Note version family (preprint, accepted manuscript, version of record),
correction dates, and mismatches. Version-mismatched clean VERIFIED is invalid
until reconciled with an explicit human note.

### correction_retraction_predatory_risk

List retracted, corrected, expression-of-concern, and predatory/unreliable venue
flags. Retracted sources never pass clean VERIFIED. Corrected sources need an
acknowledgment note before strong support.

### contamination_signals

Record contamination_advisory when offline status is unknown for AI-recalled
strings, circular citation chains, or secondary-only support used as primary.
Advisory blocks silent VERIFIED promotion.

### plagiarism_boundary

If originality is in scope for adjacent text, classify ORIGINAL /
COMMON_KNOWLEDGE / PARAPHRASE / CLOSE_MATCH / VERBATIM with locator-backed
comparison. Without detectors, mark unassessed material unknown.

### integrity_mode

State Mode1 sample rule or Mode2 full-scope and how residuals are reported.
Phases: inventory → identity/locator → fidelity → temporal/risk → escalation.

### escalation

Summarize PASS / PASS_WITH_NOTES / FAIL with counts by verdict. FAIL on
fabricated identity, MAJOR_DISTORTION under strict mode, retracted-as-clean, or
access-blocked VERIFIED. PASS_WITH_NOTES for residual UNVERIFIABLE_ACCESS and
contamination advisories. Require human sign-off for conclusion-bearing reports.

## Human gates

- [ ] No invented extracts, locators, DOIs, or verdicts
- [ ] VERIFIED promotion rules followed (no DOI-only or similarity promotion)
- [ ] Access blocks and risk flags visible in the table
- [ ] Human confirmation recorded when assessment_source is human_confirmed
