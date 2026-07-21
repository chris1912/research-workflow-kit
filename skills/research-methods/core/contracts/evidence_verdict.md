<!--
essential_core_lineage:
  file: core/contracts/evidence_verdict.md
  implementation: first-party-rewrite
  upstream_concepts:
    - claim-source verdicts
    - audit verdicts
    - temporal integrity
    - contamination and retraction risk recording
  upstream_path_hints:
    - skills/research-methods/ars/.../claim_verification_protocol
    - temporal-verification-spec
    - claim-faithfulness-and-contaminated-source-spec
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Evidence Verdict Contract

Grok annotation: Essential Core contract by Grok on 2026-07-20 (E1).
Grok annotation: E3-A temporal/risk/contamination recording shapes by Grok on 2026-07-20.

## Claim-source verdicts (integrity)

| Verdict | Meaning |
| --- | --- |
| `VERIFIED` | Claim aligns with extract + locator; support is coherent |
| `MINOR_DISTORTION` | Small wording drift; substance holds |
| `MAJOR_DISTORTION` | Material misrepresentation |
| `UNVERIFIABLE` | Cannot confirm with available sources |
| `UNVERIFIABLE_ACCESS` | Source identity known but access blocked |

Strict modes: zero `MAJOR_DISTORTION` and zero bare `UNVERIFIABLE` on in-scope
high-stakes claims. `UNVERIFIABLE_ACCESS` → pass-with-notes / `uncertainty`,
not silent pass. Never describe paywall bypass.

### VERIFIED promotion rules (normative)

`VERIFIED` is allowed only when **all** of the following hold:

1. Non-empty `locator_or_quote` and/or `extract` bound to the claim
2. `support_status` is `supported` (not partial, contradicted, unsupported, or unknown)
3. `access_state` is coherent (not `unresolvable` or `access_blocked`)
4. Risk flags do not include clean-blocking states (`retracted`, unacknowledged
   `corrected`, `version_mismatch` without reconciliation note)
5. Traceable `assessment_source` is `human_confirmed` or `verified_adapter`

A correct DOI token, citation-string similarity score, or model confidence
value **must not** promote a row to `VERIFIED`. Those signals may only
downgrade, escalate, or keep the row unverified / human-review.

## Support status vocabulary

| Status | Use |
| --- | --- |
| `supported` | Extract/locator substantiates the claim |
| `partial` | Partial support; residual gap |
| `contradicted` | Source conflicts with the claim |
| `unsupported` | Source does not speak to the claim |
| `unknown` | Not yet assessed |

## Access states

`verified | unverified | unresolvable | access_blocked`

Access-blocked or unresolvable rows cannot carry `VERIFIED`.

## Risk and temporal recording shape

```json
{
  "citation_id": "C1",
  "identity": {
    "title": "...",
    "authors": "...",
    "year": "2020",
    "venue": "...",
    "doi_or_id": "10.1000/example",
    "correction_note": null
  },
  "locator_or_quote": "p.12 §Results",
  "extract": "short attributable extract",
  "claim_text": "atomic claim",
  "support_status": "supported",
  "access_state": "verified",
  "risk_flags": [],
  "contamination_advisory": false,
  "assessment_source": "human_confirmed",
  "verdict": "VERIFIED",
  "evidence_state": "extract",
  "temporal": {
    "version_label": "published",
    "version_family_note": "preprint vs VoR checked",
    "mismatch": false
  },
  "notes": "aligns with extract"
}
```

### Risk flags (non-exhaustive)

`retracted`, `corrected`, `expression_of_concern`, `version_mismatch`,
`predatory`, `contamination_advisory`

Retracted + `VERIFIED` is always invalid. Corrected + `VERIFIED` requires an
identity-level correction acknowledgment. Version mismatch + `VERIFIED` is
invalid until reconciled with an explicit note and human gate.

## Audit / orchestrator verdicts

`PASS | MINOR | MATERIAL | AUDIT_FAILED`

Integrity audits advance to clean conclusion language only on `PASS` or `MINOR`
(`PASS_WITH_NOTES`). `MATERIAL` / `AUDIT_FAILED` block silent success.

## Plagiarism boundary classes (offline-honest)

`ORIGINAL | COMMON_KNOWLEDGE | PARAPHRASE | CLOSE_MATCH | VERBATIM`

Classes are advisory without a detector runtime; require locator-backed
comparison for close/verbatim assertions.
