<!--
essential_core_lineage:
  file: core/protocols/citation_integrity.md
  implementation: first-party-rewrite
  upstream_concepts:
    - claim verification
    - integrity review Mode1/Mode2 phases A-E
    - temporal verification
    - contamination signals
    - plagiarism boundaries
    - AI research failure modes
  upstream_path_hints:
    - ars/.../claim_verification_protocol
    - integrity_review_protocol
    - plagiarism_detection_protocol
    - claim-faithfulness-and-contaminated-source-spec
    - temporal-verification-spec
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Citation Integrity Protocol

Grok annotation: Essential Core E3-A citation integrity depth by Grok on 2026-07-20.

**parity: partial** — E3-A citation integrity vertical slice is operational offline.
Not full ARS multi-agent, network DOI lookup, or deterministic gold-corpus parity.
A DOI, citation token, or string similarity may only downgrade, escalate, or mark
unverified; never promote a record to `VERIFIED`.

## Intent

Provide high-density, offline-honest instructions for citation identity, locator
or extract discipline, claim-source fidelity, temporal/version family checks,
correction/retraction/predatory risk, contamination advisory, plagiarism
boundaries, access states, Mode1/Mode2 scope, verdict vocabulary, escalation,
and human gates. Use with designated templates
`citation_integrity_audit.md` and `claim_verification_report.md`.

## Runtime binding

Citation-check mode under academic-paper workflow binds here. Contracts:
`evidence_verdict.md` (claim verdicts), `evidence_states.md` (evidence badges).
Private record helpers live in `essential_quality_gates.py` and wire into
existing public gates `claim_verdict_vocab` and `content_depth` only.
Do not invent bibliographic data, quotes, page numbers, or DOI strings.

---

## Field contracts (protocol surface)

### citation_identity

Record durable bibliographic identity for every citation row: title, authors or
corporate author, year, venue, and at least one durable identifier when
available (DOI, PMID, arXiv id, ISBN, or stable archival URL). Require internal
consistency checks among title, authors, year, and identifier tokens. Missing
title and missing identifier together is incomplete identity; mark the row
`unverified` or escalate. Never invent a DOI, PMID, title fragment, or author
list to complete a sparse string. Secondary citations must be labeled secondary
and must not be presented as primary identity without the primary source.

### locator_or_quote

Every claim-support path needs a locator (page, section, figure/table, paragraph)
or a short supporting extract/quote bound to that locator. Bare DOI, bare
citation token, or title-author similarity is never enough for `VERIFIED`.
When the full text is unavailable, record access honestly and use
`UNVERIFIABLE_ACCESS` rather than fabricating locators or extracts. Prefer short
extracts over long paste; keep extracts attributable and non-fabricated.

### claim_source_fidelity

Bind each atomic claim to supporting citation IDs and a claim-source verdict from
the fixed enum: `VERIFIED`, `MINOR_DISTORTION`, `MAJOR_DISTORTION`,
`UNVERIFIABLE`, `UNVERIFIABLE_ACCESS`. Require an explicit `support_status` among
`supported`, `partial`, `contradicted`, `unsupported`, `unknown`. `VERIFIED`
requires `support_status=supported`, a non-empty locator or extract, coherent
access and risk state, and a traceable `assessment_source` such as
`human_confirmed` or `verified_adapter`. Heuristic string similarity, DOI match
alone, or model confidence scores may only downgrade, escalate, or leave the
row unverified—never promote to `VERIFIED`.

### temporal_version_check

Check version family: preprint versus published version, version-of-record
updates, corrigendum dates, and superseded replacements. When the claim depends
on a specific version, record the version identifier or date and surface
mismatches as `version_mismatch` risk rather than silently swapping identities.
Do not auto-reconcile preprint and published numbers when they conflict; keep
both with an explicit note and lower claim strength until a human chooses.

### correction_retraction_predatory_risk

Screen for retraction, expression of concern, correction/erratum, and predatory
or unreliable venue signals when lawful metadata or human notes are available.
Risk flags include `retracted`, `corrected`, `expression_of_concern`,
`version_mismatch`, and `predatory`. A retracted source must not be marked clean
`VERIFIED`. A corrected source may support a claim only when the correction is
acknowledged in identity notes and the claim still holds after correction.
When offline metadata is unknown, mark risk `unknown` and do not invent a clean
bill of health.

### contamination_signals

Treat contamination as an advisory layer when offline status is unknown: AI
generated citations, circular self-cite loops, secondary-only chains, poisoned
or mirrored pages, and sources that appear only as model-recalled strings.
Record `contamination_advisory` when any signal is present or unverifiable
offline. Contamination alone does not prove fabrication, but it blocks silent
`VERIFIED` promotion and requires human review or a verified adapter result
before strong claims proceed.

### plagiarism_boundary

Apply offline-honest originality classes for text under review relative to
sources: `ORIGINAL`, `COMMON_KNOWLEDGE`, `PARAPHRASE`, `CLOSE_MATCH`,
`VERBATIM`. Require locator-backed comparison when a close or verbatim match is
asserted. Self-plagiarism and recycled methods text need disclosure notes, not
silent reuse. Do not claim automated plagiarism detector parity; without tools,
classify only what the human-supplied corpus supports and mark the rest
`unknown` / `unverified`.

### access_state

Use exactly one access state per citation/claim row: `verified`, `unverified`,
`unresolvable`, or `access_blocked`. `verified` means identity and supporting
text were confirmed through an allowed source (OA, licensed, or human-supplied).
`access_blocked` or `unresolvable` cannot coexist with verdict `VERIFIED`.
Never describe paywall bypass, credential sharing, or shadow-library retrieval.
Blocked access routes to manual queue and `UNVERIFIABLE_ACCESS`.

### integrity_mode

Choose Mode1 or Mode2 before scoring:

- **Mode1 (sampling):** inventory all citations; deep-check a risk-weighted
  sample of high-stakes claims (numbers, causal statements, novel mechanisms).
  Document sample rule and residual unchecked set as `unverified`.
- **Mode2 (full-scope):** deep-check every claim-support path in scope before
  clean pass language is allowed.

Phases A–E (conceptual): A inventory, B identity/locator, C claim fidelity,
D temporal/risk/contamination, E escalation and human gates. Offline operation
must still execute these phases without inventing lookup results.

### escalation

Map outcomes to `PASS`, `PASS_WITH_NOTES`, or `FAIL`:

- `PASS` — no `MAJOR_DISTORTION`, no retracted-as-clean, no fabricated identity,
  and all high-stakes claims either `VERIFIED`/`MINOR_DISTORTION` or explicitly
  out of sample with residual notes allowed only in Mode1.
- `PASS_WITH_NOTES` — residual `UNVERIFIABLE_ACCESS`, contamination advisories,
  unknown predatory risk offline, or minor distortions requiring author rewrite.
- `FAIL` — fabricated citations, `MAJOR_DISTORTION` on strict modes, retracted
  sources marked clean, access-blocked rows marked `VERIFIED`, or missing
  mandatory human gates on conclusion-bearing audits.

Escalate to human stop on fabrication requests, integrity violations, or
attempts to bypass access controls.

---

## Offline fallback

When Crossref, publisher, or detector adapters are unset: continue with
human-supplied PDFs, bibliographies, and prior matrices; mark unresolved
lookups `unverified`, `unresolvable`, or `access_blocked`; never invent DOI
resolution, retraction status, or similarity scores. Method steps remain
executable; only external confirmation is marked missing.

## Human gates

- [ ] No invented studies, DOIs, titles, page numbers, or quotations
- [ ] `VERIFIED` only with locator or extract, `support_status=supported`,
      coherent access/risk state, and `human_confirmed` or `verified_adapter`
- [ ] Strict modes fail on `MAJOR_DISTORTION` or bare `UNVERIFIABLE` for
      in-scope high-stakes claims
- [ ] `UNVERIFIABLE_ACCESS` and contamination advisories stay visible notes
- [ ] Human sign-off required for conclusion-bearing integrity outcomes
