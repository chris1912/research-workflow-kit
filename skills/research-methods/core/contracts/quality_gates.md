<!--
essential_core_lineage:
  file: core/contracts/quality_gates.md
  implementation: first-party-rewrite
  upstream_concepts:
    - quality gates
    - semantic field minimums
    - content depth
    - private E3 evaluators
  upstream_path_hints:
    - skills/research-methods/codex/scripts/ars_codex_quality_gates.py
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Quality Gates Contract

Grok annotation: Essential Core contract by Grok on 2026-07-20 (E1).
Grok annotation: E3-A private citation evaluators bound to existing gates by Grok on 2026-07-20.
Grok annotation: E3-B paper mode + revision/rebuttal helpers bound by Grok on 2026-07-20.
Grok annotation: E3-C manuscript-review helpers bound by Grok on 2026-07-20.

Runner: `runtime/scripts/essential_quality_gates.py` (stdlib only).

## CLI

```text
python essential_quality_gates.py list [--json]
python essential_quality_gates.py gate --id <gate_id> [--json]
python essential_quality_gates.py all [--json]
```

## Frozen public gate ID set (21)

Do not add, rename, or remove public gate IDs without explicit approval.

```text
alias_coverage
anti_pooling_fields
claim_verdict_vocab
content_depth
effect_hetero_sensitivity
evidence_state_vocab
file_lineage_headers
generator_evaluator_separation
grade_fields
hook_safety
mode_registry_coverage
optional_runtime_honesty
passport_reset_contract
prisma_fields
reviewer_independence
rob2_fields
robins_i_fields
single_root_skill
stats_fallacies_11
upstream_provenance
vague_topic_socratic
```

## Gate catalog

### E1 packaging / routing / safety (must be executable now)

| Gate ID | Kind |
| --- | --- |
| single_root_skill | packaging |
| alias_coverage | routing |
| vague_topic_socratic | routing |
| mode_registry_coverage | routing |
| reviewer_independence | agent-team fixture + E3-C identity/re-review/calibration |
| passport_reset_contract | passport samples |
| evidence_state_vocab | integrity |
| claim_verdict_vocab | integrity + E3-A citation behavioral fixtures |
| hook_safety | hooks |
| optional_runtime_honesty | runtime |
| generator_evaluator_separation | paper + E3-B revision/rebuttal fixtures |
| upstream_provenance | provenance |
| file_lineage_headers | provenance |
| content_depth | depth + E3-A citation + E3-B paper + E3-C review modes/templates |

### E2+ semantic gates

| Gate ID | Stage |
| --- | --- |
| prisma_fields | E2 |
| rob2_fields | E2 |
| robins_i_fields | E2 |
| grade_fields | E2 |
| effect_hetero_sensitivity | E2 |
| anti_pooling_fields | E2 |
| stats_fallacies_11 | E4 (`not_started` until experiment depth) |

E1 runners must **not** report E2 semantic gates as pass while protocol bodies
are `parity: not_started`. Prefer status `not_started` / fail with honest detail.

## Private E3-A evaluators (not public gate IDs)

These helpers are stdlib-only, deterministic, and called from existing `g_*`
functions or unit tests. They must not appear as new `GATE_FUNCS` keys.

| Private helper | Public gate path | Surfaces / fixtures |
| --- | --- | --- |
| `evaluate_citation_record` | `claim_verdict_vocab` | structured citation/claim rows |
| `evaluate_citation_records` | `claim_verdict_vocab` | multi-row aggregate |
| `evaluate_citation_integrity_protocol_text` | `content_depth`, `claim_verdict_vocab` | `core/protocols/citation_integrity.md` |
| `evaluate_citation_audit_template_text` | `content_depth` | `core/templates/citation_integrity_audit.md` |
| `evaluate_claim_report_template_text` | `content_depth` | `core/templates/claim_verification_report.md` |

### Behavioral hard rules (citation records)

- DOI / citation token / string similarity never promotes to `VERIFIED`
- `VERIFIED` requires locator or extract, coherent access/risk state,
  `support_status=supported`, and `assessment_source` in
  `{human_confirmed, verified_adapter}`
- Retracted, unacknowledged correction, version mismatch, or access-blocked
  rows cannot be clean `VERIFIED`
- Failure details name the `citation_id` or designated surface path

## Private E3-B evaluators (not public gate IDs)

| Private helper | Public gate path | Surfaces / fixtures |
| --- | --- | --- |
| `evaluate_all_paper_modes_text` | `content_depth` | `core/protocols/academic_paper.md` (11 modes) |
| `evaluate_mode_fields_text` | `content_depth` / tests | single mode field set |
| `evaluate_revision_template_text` | `content_depth` | `core/templates/revision_roadmap.md` |
| `evaluate_rebuttal_template_text` | `content_depth` | `core/templates/rebuttal_audit.md` |
| `evaluate_disclosure_template_text` | `content_depth` | `core/templates/disclosure_statement.md` |
| `evaluate_revision_transition` | `generator_evaluator_separation` | structured before/after fixtures |
| `evaluate_rebuttal_consistency` | `generator_evaluator_separation` | structured point matrix fixtures |

### Behavioral hard rules (revision / rebuttal / disclosure)

- Protected claim/hedge deletion or silent strengthening without ledger +
  author_signoff fails (`protected_claim_deleted` /
  `protected_claim_strengthened`)
- Silent new DOI/result without gated new_evidence_rows fails
  (`silent_new_evidence`)
- False ledger claims and missing recovery checkpoints fail closed
- Rebuttal: missing/duplicate point rows, asserted change absent from ledger,
  empty evidence/no-change rationale, and generated_response_prose fail
- Disclosure: optionalizing or auto-fabricating AI/funding/COI fails; human
  confirmation is mandatory
- Designated templates validate independently; protocol duplicates cannot rescue
  hollow revision/rebuttal/disclosure surfaces

### Designated surface isolation

Protocol, audit template, and claim report each carry their own labeled field
bodies. Duplicates in a peer file must not rescue a hollow designated surface.
E3-B adds the same isolation for academic_paper modes and
revision/rebuttal/disclosure templates.
E3-C adds isolation for manuscript_review modes and
manuscript_review_full / editorial_decision templates.

## Private E3-C evaluators (not public gate IDs)

| Private helper | Public gate path | Surfaces / fixtures |
| --- | --- | --- |
| `evaluate_all_reviewer_modes_text` | `content_depth`, `reviewer_independence` | `core/protocols/manuscript_review.md` (6 modes) |
| `evaluate_reviewer_mode_fields_text` | `content_depth` / tests | single reviewer mode field set |
| `evaluate_manuscript_review_template_text` | `content_depth` | `core/templates/manuscript_review_full.md` |
| `evaluate_editorial_decision_template_text` | `content_depth` | `core/templates/editorial_decision.md` |
| `evaluate_reviewer_identity` | `reviewer_independence` | named vs anonymous/simulated identity |
| `evaluate_rereview_consistency` | `reviewer_independence` | residual trajectory rows |
| `evaluate_calibration_gold` | `reviewer_independence` | gold labels vs predictions |
| `evaluate_quick_mode_honesty` | tests / `content_depth` polarity | quick must not claim full panel |
| `evaluate_guided_mode_honesty` | tests / `content_depth` polarity | guided dialogue checkpoints |

### Behavioral hard rules (manuscript review)

- Four independents remain blind until all durable outputs exist; synthesis after
- Every minority finding needs retained|downgraded|rejected plus rationale
- Named real-person reviewers require non-empty source and human confirmation
- Re-review: unique prior IDs, exact coverage, trajectory vocab, addressed pointer,
  no new-as-closure, no blanket all-fixed
- Calibration: human gold required; missing/empty gold fails; session-only;
  no fabricated labels or persistent calibration claim
- Quick cannot claim full-panel completion; guided preserves dialogue checkpoints
- Decision letter labeled simulated unless real venue process + human authority
- Multi-process isolation remains an honest non-claim (validator partial only)
- Designated templates validate independently; protocol cannot rescue hollow
  manuscript_review_full or editorial_decision surfaces

## Exit codes

0 all selected pass; 1 any fail; 2 bad gate id; 4 missing root.
