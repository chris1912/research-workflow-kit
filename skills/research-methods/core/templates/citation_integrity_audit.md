<!--
essential_core_lineage:
  file: core/templates/citation_integrity_audit.md
  implementation: first-party-rewrite
  upstream_concepts:
    - citation integrity audit
    - claim-source inventory
    - risk and access recording
  upstream_path_hints:
    - Stage-D citation_integrity_check.md
    - integrity_review_protocol
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Citation Integrity Audit

Grok annotation: Essential Core template by Grok on 2026-07-20.
Grok annotation: E3-A designated audit fields by Grok on 2026-07-20.

**parity: partial** — E3-A audit surface. Deeper paper revision / disclosure
modes remain outside this template. Do not invent bibliographic data.

**Stage-D successor** of `templates/citation_integrity_check.md`.
This designated surface must pass independently; protocol prose elsewhere
cannot rescue hollow fields here.

## 1. Scope

- Manuscript or run ID:
- Checker:
- Date:
- Integrity mode (Mode1 sampling / Mode2 full-scope):
- Claims or sections under review:

### audit_scope

State manuscript identity, checker, date, Mode1 versus Mode2 selection, and the
claim set or section set under review. Mode1 must document the sampling rule and
the residual unchecked inventory. Mode2 must state that every in-scope
claim-support path will be scored before clean pass language.

## 2. Citation inventory

| ID | Citation string | DOI / ID | Locator (page/section) | Used to support claim | Lookup status | Claim-source fit | Risk flags | Notes |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| C1 |  |  |  |  | unverified / verified / unresolvable / access_blocked | fit / partial / mismatch / unknown | none / retracted / corrected / version_mismatch / predatory / contamination_advisory |  |

### citation_identity

For each inventory row capture title, authors, year, venue, and durable
identifier when available. Flag internal inconsistency among tokens. Missing
both title and identifier is incomplete identity. Never invent DOI, PMID, title,
or author strings to fill blanks.

### locator_or_quote

Require page/section/figure/table/paragraph locator or a short attributable
extract for every claim-support path. Bare DOI or citation token alone is never
sufficient for `VERIFIED`. If full text is unavailable, leave locator empty and
record access honestly instead of fabricating page numbers.

### access_state

Per row use exactly one of: `verified`, `unverified`, `unresolvable`,
`access_blocked`. Access-blocked or unresolvable rows cannot be marked clean
`VERIFIED`. Lawful access only; never describe paywall bypass.

## 3. Claim-to-source audit

For each high-stakes claim:

- Claim text:
- Supporting citation IDs:
- Extract or paraphrase with locator:
- Evidence badge: claim / extract / inference / uncertainty / missing / blocked / human-confirmed
- Support status: supported / partial / contradicted / unsupported / unknown
- Assessment source: human_confirmed / verified_adapter / heuristic_only / none
- Verdict: VERIFIED / MINOR_DISTORTION / MAJOR_DISTORTION / UNVERIFIABLE / UNVERIFIABLE_ACCESS
- Overclaim risk:
- Required rewrite if mismatch:

### claim_source_fidelity

Bind each atomic claim to citation IDs, extract/locator, support status, verdict
enum, and assessment source. `VERIFIED` requires `support_status=supported`,
locator or extract, coherent access/risk state, and `human_confirmed` or
`verified_adapter`. Heuristic similarity may only downgrade or escalate.

### temporal_version_check

Record preprint versus published, version-of-record, corrigendum timing, and any
version_family mismatch. Do not silently swap preprint numbers for published
numbers when they conflict; note both and lower strength until human resolution.

### correction_retraction_predatory_risk

Capture retraction, expression of concern, correction/erratum acknowledgment,
and predatory or unreliable venue signals. Retracted sources must not pass as
clean `VERIFIED`. Corrected sources need an explicit correction note before any
strong support claim.

### contamination_signals

Advisory only when offline unknown: AI-recalled-only strings, circular cite
chains, secondary-only support, mirrored or poisoned pages. Set
`contamination_advisory` and block silent `VERIFIED` promotion until human or
verified adapter confirmation.

## 4. Integrity red flags

- [ ] Fabricated or incomplete citation strings
- [ ] DOI / arXiv / PMID mismatch with title or authors
- [ ] Secondary citation used as if primary
- [ ] Statistics quoted without source locator
- [ ] Self-serving selective citation without counterevidence note
- [ ] Retracted or corrected source used without note
- [ ] Access-blocked source marked VERIFIED

### plagiarism_boundary

Classify questioned spans as ORIGINAL, COMMON_KNOWLEDGE, PARAPHRASE,
CLOSE_MATCH, or VERBATIM relative to the human-supplied corpus. Close or
verbatim assertions need locator-backed comparison. Without a detector runtime,
mark unassessed spans `unknown` rather than inventing a clean originality score.

### integrity_mode

Re-state Mode1 sample rule or Mode2 full-scope commitment and list residual
unchecked rows for Mode1. Phases A inventory, B identity/locator, C fidelity,
D temporal/risk/contamination, E escalation must remain visible offline.

### escalation

Choose PASS, PASS_WITH_NOTES, or FAIL with criteria: FAIL on fabrication,
MAJOR_DISTORTION under strict mode, retracted-as-clean, or access-blocked
VERIFIED; PASS_WITH_NOTES for residual access blocks and contamination
advisories; PASS only when high-stakes in-scope paths are clean or explicitly
out of Mode1 sample with residual notes.

## 5. Uncertainty log

- Items that remain **uncertainty**:
- Access or language barriers:
- Manual library / expert follow-up needed:

## 6. Human gates

- [ ] No fabricated DOIs, titles, page numbers, or quotations
- [ ] VERIFIED only with locator/extract, supported status, coherent access/risk,
      and human_confirmed or verified_adapter assessment source
- [ ] Strict modes fail on MAJOR_DISTORTION or UNVERIFIABLE for in-scope claims
- [ ] Human sign-off recorded for conclusion-bearing audit outcomes
