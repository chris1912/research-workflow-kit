<!--
essential_core_lineage:
  file: core/contracts/reviewer_independence.md
  implementation: first-party-rewrite
  upstream_concepts:
    - reviewer independence
    - minority retention
    - calibration
    - re-review trajectory
    - reviewer identity honesty
  upstream_path_hints:
    - skills/research-methods/ars/.../reviewer panel protocols
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Reviewer Independence Contract

Grok annotation: Essential Core contract by Grok on 2026-07-20 (E1).
Grok annotation: E3-C re-review, identity, calibration, and minority rationale by Grok on 2026-07-20.

Applies to `academic-paper-reviewer` modes `full` and `methodology-focus`, and
pipeline Stage `3`. Protocol body: `core/protocols/manuscript_review.md`
(`parity: partial`, E3-C). Validator coverage is partial parity; multi-process
isolation remains an honest non-claim.

## Separate input artifacts

Each independent reviewer consumes only the shared manuscript package and rubric.
They must not see other reviewers' drafts before all independents complete.

| Artifact | Producer | Consumers |
| --- | --- | --- |
| review/independent/methodology.md | Methodology | Synthesis after all independents |
| review/independent/domain.md | Domain | Synthesis after all independents |
| review/independent/interdisciplinary.md | Perspective | Synthesis after all independents |
| review/independent/devils_advocate.md | Devil's Advocate | Synthesis after all independents |
| review/synthesis/editorial.md | Editorial synthesizer | Decision + roadmap |
| review/synthesis/decision_letter.md | Editorial | Human |
| review/synthesis/revision_roadmap.md | Editorial | Human / revision modes |

## Fixed section order

1. Independent Reviewer: Methodology
2. Independent Reviewer: Domain
3. Independent Reviewer: Interdisciplinary
4. Independent Reviewer: Devil's Advocate
5. Editorial Synthesis
6. Decision Letter
7. Revision Roadmap

Gate `reviewer_independence` fails if synthesis appears before all four
independent headings/artifacts, or if order differs from the fixture oracle.

## Visibility barrier

| Phase | Allowed visibility |
| --- | --- |
| Independent drafting | Own role + manuscript only |
| After own section complete | Still no peer independents until all complete |
| Synthesis | All four independent artifacts |
| Decision / roadmap | Synthesis + independents |

Inline single-agent mode must still write four separate artifacts in order
before synthesis prose.

### Stage validator (A20)

```text
validate_reviewer_stage_state(state) -> { ok, error, message }
```

Deterministic failures (in-memory; no multi-process claim):

| error | Condition |
| --- | --- |
| `early_visibility` | A reviewer sees peer independent drafts before all four complete (A20) |
| `premature_synthesis` | Synthesis starts before all four independents complete |
| `missing_disposition` | Synthesis lacks a disposition for an independent source, including DA |
| `missing_rationale` | Disposition present without non-empty rationale at synthesis |

Multi-process orchestration / process isolation remains **partial**. Gate
detail must distinguish validator coverage from process isolation. Do not
advertise full process isolation.

## Minority retention

Synthesis may severity-rank but must not erase minority/DA findings by majority
vote. Each independent concern ends with disposition
`retained|downgraded|rejected`, a non-empty rationale, and justification;
`rejected` requires severity.

## Reviewer identity provenance

```text
evaluate_reviewer_identity(payload) -> { ok, error, detail }
```

| identity_kind | Rule |
| --- | --- |
| anonymous / simulated_role | Allowed; must be labeled simulated or anonymous |
| named_real | Requires non-empty `identity_source` and `human_confirmation=true` |

Invented or assumed sources fail. Fabricated real-person names or prestige
personas presented as actual peers fail closed.

## Re-review

```text
evaluate_rereview_consistency(payload) -> { ok, error, detail }
```

Start from residual issue checklist mapped to prior `concern_id` / issue IDs.
Prior issue IDs must be non-empty and unique. Current rows cover prior issues
exactly. Score trajectory required:
`open | partially_addressed | addressed | new`.

| Rule | Failure |
| --- | --- |
| Empty or duplicate prior IDs | fail closed |
| Missing prior coverage / orphan non-new rows | fail closed |
| `addressed` without manuscript/evidence pointer | fail closed |
| `new` row masquerading as prior closure | fail closed |
| Blanket all-fixed without per-issue addressed pointers | fail closed |

No silent “all fixed” without evidence pointers.

## Calibration

```text
evaluate_calibration_gold(payload) -> { ok, error, detail }
```

Requires user-supplied gold labels with non-empty item IDs. Accepted gold set
size is **5–20** items with exact one-to-one prediction mapping. Predictions
must match gold IDs. Missing or empty gold → `error: missing_calibration_gold`
(or empty_gold). Fewer than 5 → `inadequate_gold_set`; more than 20 →
`excessive_gold_set`. Fabricated labels and persistent calibration claims fail.
Invalid sets emit no metrics. Session-only only; never invent ground truth.

## Decision letter honesty

Decision letters are **simulated** unless a real venue/editor process and human
authority are both supplied. No fabricated editor or reviewer prestige.

## Mode honesty bounds

| Mode | Bound |
| --- | --- |
| quick | Must not claim full-panel completion |
| guided | Must preserve dialogue/checkpoint behavior; no one-shot dump |
| methodology-focus | Methodology mandatory; not silent full panel |
| full | Four blinds then synthesis; minority rationale required |
| re-review | Trajectory + pointers; no blanket all-fixed |
| calibration | Gold required; session-only |

## Private helpers (not public gate IDs)

Wired into existing `reviewer_independence` and `content_depth` only:

- `evaluate_reviewer_identity`
- `evaluate_rereview_consistency`
- `evaluate_calibration_gold`
- `evaluate_all_reviewer_modes_text`
- `evaluate_manuscript_review_template_text`
- `evaluate_editorial_decision_template_text`
