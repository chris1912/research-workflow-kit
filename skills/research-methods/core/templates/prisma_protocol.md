<!--
essential_core_lineage:
  file: core/templates/prisma_protocol.md
  implementation: first-party-rewrite
  upstream_concepts:
    - PRISMA protocol planning
  upstream_path_hints:
    - ars prisma templates
    - Stage-D review_protocol.md
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Systematic Review / Meta-Analysis Protocol (PRISMA-oriented)

Grok annotation: Essential Core E2 template depth by Grok on 2026-07-20.
**parity: partial** — E2 PRISMA/RoB/GRADE operational fill-ins. Stage-D successor of `templates/review_protocol.md`.

Use with `core/protocols/systematic_review.md`. Do not invent registration IDs, studies, effect sizes, or pooled estimates. Illustrative method examples only.

## Research question

- Primary question:
- Decision use of the review:
- Structure frame (PICO/PECO/PICOT/other):

## Protocol scope

- Review type: systematic review / meta-analysis / narrative SR without MA / other
- Time window and languages:
- Human method lock date/owner:

## prisma_title_registration

Working title identifying systematic review/meta-analysis; registration intent (PROSPERO/OSF/none+why); protocol version; amendment rule. Registration ID if real—never invent:

## eligibility_pico

Population; Intervention/Exposure; Comparator; Outcomes (primary/secondary); Study designs; inclusion/exclusion lists a second reviewer can apply; unresolved items as missing/blocked:

## Search plan

Operational search fill-ins for Stage-D section compatibility. Use the labeled fields below for E2 semantic depth.

## information_sources

Databases; registers; grey literature policy; citation chasing; planned last-search freeze; offline/adapter limits:

## search_strategy

Concept blocks; draft Boolean/logic; limits; peer-review-of-search intent; primary database reproducible string template:

## selection_process

Dual screening plan for title/abstract and full text; conflict resolution; pilot calibration; exclusion-reason categories for PRISMA flow:

## data_items

Extraction variables; dual extraction or audit sample; missing-data rules (no unjustified variance imputation); locator requirements:

## risk_of_bias_plan

RoB 2 for RCTs and/or ROBINS-I for NRS; assessment level; how judgments feed synthesis/GRADE; training notes:

## effect_measures

Primary effect measure(s) and rationale; mapping for binary/continuous/time-to-event; forbidden conversions:

## synthesis_methods

Meta-analysis eligibility criteria vs narrative/SWiM; multi-arm/overlap handling; model family plan (not forced computation):

## heterogeneity_plan

Clinical vs methodological vs statistical hetero; I²/τ²/prediction interval plan or qualitative alternative:

## sensitivity_plan

Pre-listed sensitivity analyses with triggers (minimum two; see protocol). Execution log:

## anti_pooling

Cross-ref anti_pooling_conditions and anti_pooling_action. Protocol commitment if triggered: narrative/SWiM only; no invented pooled numbers/forest plots:

## reporting_bias

Funnel/small-study only if assumptions hold; else qualitative registry/grey-literature probes; never invent funnel data:

## certainty_grade

GRADE plan per critical outcome; downgrade/upgrade domains; do not algorithmically fabricate certainty; human confirmation for conclusions:

## effect_measure_primary

Primary measure for main outcome (RR/OR/HR/MD/SMD etc.) with decision-use rationale and interpretation boundaries:

## effect_measure_by_outcome_type

Binary → ; Continuous → ; Time-to-event → ; transformation rules and invalid-conversion stops:

## hetero_stats

I² and/or τ² and/or prediction interval plan, or explicit qualitative heterogeneity tables when MA not done:

## hetero_exploration

Pre-specify subgroup analyses and/or meta-regression with scientific rationale; apply multiplicity caution; label data-driven or post hoc exploration as hypothesis-generating, not confirmatory:

## sensitivity_analyses

1. Risk-of-bias restricted analysis — trigger: high/serious RoB studies present.
2. Model or inclusion-decision analysis — trigger: contested model choice or borderline eligibility.
3. Optional additional pre-stated analysis:

## anti_pooling_conditions

1. Incompatible effect measures/scales without justifiable conversion:
2. Clinical diversity too high for one estimand:
3. Single-study or non-independent clusters only / missing variance without justifiable imputation:
4. Other:

## anti_pooling_action

If any condition triggers: mandatory structured narrative/SWiM; forbid invented pooled numbers and forest plots; no silent numeric pooling; state non-pooling reason:

## RoB 2 quick slots (see protocol for signaling questions)

### rob2_d1

Domain label: bias arising from the **randomization** process. Signaling question: was the allocation sequence random and concealed? Judgment slot: low | some_concerns | high | no_information + notes:

### rob2_d2

Domain label: bias due to **deviations** from intended interventions. Signaling question: were deviations from intended interventions unbalanced by arm? Judgment slot: low | some_concerns | high | no_information + notes:

### rob2_d3

Domain label: bias due to **missing** outcome data. Signaling question: were outcome data available for nearly all participants? Judgment slot: low | some_concerns | high | no_information + notes:

### rob2_d4

Domain label: bias in **measurement** of the outcome. Signaling question: was outcome measurement appropriate and comparable across arms? Judgment slot: low | some_concerns | high | no_information + notes:

### rob2_d5

Domain label: bias in **selection of the reported** result. Signaling question: were reported analyses pre-specified versus selectively chosen? Judgment slot: low | some_concerns | high | no_information + notes:

### rob2_overall

Overall RoB 2 judgment using low | some_concerns | high | no_information; do not average domains into a fake score; note synthesis use:

## ROBINS-I quick slots

### robins_d1

Domain label: bias due to **confounding**. Signaling question: is confounding of intervention on outcome adequately controlled? Judgment: low | moderate | serious | critical | no_information:

### robins_d2

Domain label: bias in **selection of participants** into the study. Signaling question: was selection related to intervention and outcome? Judgment: low | moderate | serious | critical | no_information:

### robins_d3

Domain label: bias in **classification** of interventions. Signaling question: was intervention status well defined and assessed without bias? Judgment: low | moderate | serious | critical | no_information:

### robins_d4

Domain label: bias due to **deviations** from intended interventions. Signaling question: were prognostic deviations unbalanced beyond usual practice? Judgment: low | moderate | serious | critical | no_information:

### robins_d5

Domain label: bias due to **missing data**. Signaling question: are outcome/covariate data complete enough for a valid estimate? Judgment: low | moderate | serious | critical | no_information:

### robins_d6

Domain label: bias in **measurement of outcomes**. Signaling question: could outcome measurement differ by intervention group? Judgment: low | moderate | serious | critical | no_information:

### robins_d7

Domain label: bias in **selection of the reported** result. Signaling question: is selective reporting of outcomes or analyses likely? Judgment: low | moderate | serious | critical | no_information:

### robins_overall

Overall ROBINS-I judgment low | moderate | serious | critical | no_information from the most severe domain; note synthesis/GRADE use:

## GRADE per critical outcome

Outcome name:
### grade_risk_of_bias

Downgrade for study-level RoB/ROBINS limitations that could change the estimate; none | serious | very serious:

### grade_inconsistency

Downgrade for unexplained inconsistency of effects across studies after clinical/methodological review:

### grade_indirectness

Downgrade for PICO indirectness or surrogate outcomes poorly linked to the decision endpoint:

### grade_imprecision

Downgrade when intervals or information size allow both meaningful benefit and harm/null at the decision threshold:

### grade_publication_bias

Downgrade when reporting/publication bias assessment suggests missing or selectively unreported evidence:

### grade_upgrade_factors

Large effect / dose-response / residual confounding — only if justified; never upgrade to hide serious RoB:

### grade_certainty

high | moderate | low | very low + rationale; human confirmation status; do not fabricate certainty ratings:

## Evidence states

- Known:
- Missing / not yet searched:
- Blocked:
- Uncertainty / conflicting signals:

## Human gates

- [ ] Protocol criteria reviewed by a human before screening starts
- [ ] Search date freeze approved
- [ ] Synthesis approach locked before pooling attempts
- [ ] No fabricated studies, effect sizes, citations, or pooled estimates
- [ ] Final inclusion list and conclusions require human sign-off

## Next actions

- Immediate next step:
- Blocking dependencies:
