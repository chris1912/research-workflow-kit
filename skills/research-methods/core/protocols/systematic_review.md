<!--
essential_core_lineage:
  file: core/protocols/systematic_review.md
  implementation: first-party-rewrite
  upstream_concepts:
    - systematic review protocol
    - PRISMA
    - RoB2
    - ROBINS-I
    - GRADE
    - heterogeneity
    - anti-pooling
  upstream_path_hints:
    - ars/.../systematic_review_protocol.md
    - systematic_review_toolkit
    - prisma templates
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Systematic Review Protocol

Grok annotation: Essential Core E2 method depth by Grok on 2026-07-20.

**parity: partial** — E2 PRISMA / RoB 2 / ROBINS-I / GRADE / effect / heterogeneity / sensitivity / anti-pooling semantics implemented as executable offline instructions. Not full ARS multi-agent or software meta-analysis parity. Do not invent studies, effect sizes, pooled estimates, or forest plots.

## Intent

Run PRISMA-oriented systematic reviews and optional meta-analyses with human method lock before screening/synthesis, dual screening rules, risk-of-bias domains, GRADE certainty planning, and mandatory anti-pooling narrative/SWiM when pooling is unjustified.

## Runtime binding

Mode: `deep-research` / `systematic-review`. Templates: `prisma_protocol.md`, `prisma_report_skeleton.md`, `literature_matrix.md`, `evidence_assessment.md`. Role support in `deep_research_roles.md` (RoB/meta concepts).

## Hard rules

1. **Human method lock** before screening starts and again before quantitative synthesis.
2. Never invent pooled estimates, forest plots, or study results.
3. Do not algorithmically fabricate GRADE certainty ratings without domain rationale and human review for conclusion-bearing use.
4. Lawful access only; missing full text → document and continue with honest states.
5. Registration/version deviations must be logged; do not silently change eligibility after seeing results.

---

## A. PRISMA protocol planning fields

### prisma_title_registration

Write a working title that identifies the work as a systematic review and/or meta-analysis. Record registration intent (PROSPERO, OSF, or justified non-registration) with ID when available, protocol version, date, and amendment policy. If unregistered, state why and what version control will substitute. Do not invent a registration number.

### eligibility_pico

Define Population, Intervention or Exposure, Comparator, Outcomes, and eligible study designs (PICOS/PECOS). Add time window, language policy, and publication-status rules. List explicit inclusion and exclusion criteria that a second reviewer could apply without guessing. Mark unresolved elements `missing` or `blocked`.

### information_sources

List planned databases and trial/study registers, grey literature policy, citation chasing, expert contact rules, and the planned last-search date freeze. Require at least two bibliographic sources unless a human documents a justified exception. When discovery adapters are unset, keep this plan executable offline and mark unsearched sources `missing`/`blocked` rather than fabricating hit counts.

### search_strategy

Specify concept blocks, Boolean/logic structure, controlled vocabulary vs free text, limits/filters, and peer-review-of-search intent (PRESS-like human review when available). Preserve at least one fully reproducible strategy string template for the primary database. Document translations of concepts across sources without inventing retrieved records.

### selection_process

Require dual independent screening at title/abstract and full text for the default path, with a documented conflict-resolution rule (discussion, third reviewer, or adjudicator). Define pilot calibration on a sample. Single-screen only if human accepts higher error risk and an audit sample is planned. Record reasons for full-text exclusions in categories usable for PRISMA flow.

### data_items

List extraction variables: identity, design, population, interventions/exposures, comparators, outcomes, timepoints, effect estimates, variance, funding, and notes. State missing-data rules (contact authors when lawful/feasible; no unjustified imputation of critical variances). Prefer dual extraction or single extraction plus verification sample. Keep extraction bound to locators.

### risk_of_bias_plan

Pre-specify tools: RoB 2 for randomized trials and ROBINS-I for non-randomized intervention studies (or justified alternative with domain mapping). Assess at study or result level as appropriate. Train reviewers on signaling questions. Use domain judgments to inform synthesis weights, sensitivity analyses, and GRADE risk-of-bias downgrades—not as decorative color only.

### effect_measures

Name planned primary effect measure(s) per outcome type before seeing results (e.g., risk ratio or odds ratio for binary; mean difference or SMD for continuous; hazard ratio for time-to-event). Give rationale tied to decision use and common reporting. State compatible transformations and when conversion is forbidden due to missing data or incommensurable scales.

### synthesis_methods

Define criteria for quantitative meta-analysis versus narrative synthesis / SWiM. Pre-specify model family intent (fixed/random) only as a plan, not a forced computation. Describe how multi-arm trials, overlapping populations, and multiple outcomes will be handled. If pooling criteria fail, switch to structured narrative methods without inventing a pooled number.

### heterogeneity_plan

Distinguish clinical, methodological, and statistical heterogeneity. Plan I² and/or τ² and/or prediction intervals when a meta-analysis is justified; if quantitative heterogeneity metrics are inappropriate, use an explicit qualitative alternative (tabulated design/population/outcome diversity). Do not treat I² thresholds as automatic truth.

### sensitivity_plan

Pre-list sensitivity analyses with triggers (see also `sensitivity_analyses`). Minimum includes risk-of-bias-restricted analysis and at least one model or inclusion decision analysis. Triggers must be written before outcome direction is known. Report all planned sensitivity analyses that were executable; mark blocked ones honestly.

### anti_pooling

State conditions that forbid pooling and the mandatory narrative/SWiM action (see dedicated anti-pooling fields). This field is a protocol commitment: if triggered, do not produce invented pooled estimates or decorative forest plots.

### reporting_bias

Plan assessment of reporting/publication bias: funnel/small-study methods only when study count and assumptions allow; otherwise qualitative probes (registry comparison, selective outcome reporting signals, grey literature yield). Never invent a funnel plot dataset.

### certainty_grade

Plan GRADE (or justified analogue) per critical outcome: start level by design body, consider five downgrade domains and optional upgrades, and produce a certainty summary with rationale. Do not algorithmically fabricate certainty. Human review required for conclusion-bearing certainty claims.

---

## B. Dual screening, extraction, flow, registration

- **Dual screening / conflict resolution:** default two reviewers; conflicts logged; adjudicator path named.
- **Extraction / missing data:** no silent imputation of primary effect variances; document author-contact attempts when used.
- **PRISMA flow accounting:** identification, dedup, screened, full-text assessed, excluded-with-reasons, included in qualitative synthesis, included in quantitative synthesis (n may be zero).
- **Registration/version deviations:** any post-hoc change to eligibility, outcomes, or analysis needs dated justification and human acknowledgment.
- **Human method lock:** checklist sign-off before screening and before synthesis.

---

## C. RoB 2 domains

Judgment vocabulary for each domain and overall: `low | some_concerns | high | no_information`.

### rob2_d1

Domain label: bias arising from the **randomization** process. Signaling question: was the allocation sequence random and adequately concealed, and were baseline imbalances suggestive of a problem? Record sequence generation, concealment, and baseline concerns with locators. Judgment slot: low / some_concerns / high / no_information, plus short rationale.

### rob2_d2

Domain label: bias due to **deviations** from intended interventions. Signaling question: were participants and personnel aware of assignment in a way that could deviate from the intended intervention, and were important deviations unbalanced? Consider ITT vs per-protocol estimands. Judgment slot: low / some_concerns / high / no_information with notes.

### rob2_d3

Domain label: bias due to **missing** outcome data. Signaling question: were outcome data available for all, or nearly all, participants, and could missingness depend on the true value? Document proportions missing by arm and any sensitivity to missingness assumptions. Judgment slot: low / some_concerns / high / no_information.

### rob2_d4

Domain label: bias in **measurement** of the outcome. Signaling question: was the outcome measure appropriate and comparable across arms, and could assessment have been influenced by knowledge of intervention? Prefer blinded outcome assessment when subjective. Judgment slot: low / some_concerns / high / no_information.

### rob2_d5

Domain label: bias in **selection of the reported** result. Signaling question: were the reported outcome analyses pre-specified, and is there evidence of selective reporting from multiple eligible measures or analyses? Compare to registry/protocol when available. Judgment slot: low / some_concerns / high / no_information.

### rob2_overall

Derive overall RoB 2 risk using domain pattern: any high → overall high; else any some_concerns → overall some_concerns; else all low → overall low; use no_information only when domains truly lack basis. Do not average domains into a fake numeric score. Judgment slot vocabulary: low | some_concerns | high | no_information with synthesis implications.

---

## D. ROBINS-I domains

Judgment vocabulary: `low | moderate | serious | critical | no_information` (map carefully; do not silently rename to RoB 2 terms).

### robins_d1

Domain label: bias due to **confounding**. Signaling question: is confounding of the effect of intervention on outcome adequately controlled, including time-varying confounding when relevant? List critical confounders a priori. Judgment slot: low / moderate / serious / critical / no_information.

### robins_d2

Domain label: bias in **selection of participants** into the study. Signaling question: was selection into the study (or into the analysis) related to both intervention and outcome? Consider inception timing and exclusion related to post-intervention events. Judgment slot: low / moderate / serious / critical / no_information.

### robins_d3

Domain label: bias in **classification** of interventions. Signaling question: was intervention status well defined and assessed without bias relative to outcome knowledge? Differential misclassification raises serious concern. Judgment slot: low / moderate / serious / critical / no_information.

### robins_d4

Domain label: bias due to **deviations** from intended interventions. Signaling question: were there deviations from intended intervention beyond usual practice that are unbalanced and prognostic? Align with the chosen estimand (initiation vs adherence). Judgment slot: low / moderate / serious / critical / no_information.

### robins_d5

Domain label: bias due to **missing data**. Signaling question: are outcome and covariate data sufficiently complete, and is missingness likely related to true values? Document missingness mechanisms and any planned sensitivity analyses. Judgment slot: low / moderate / serious / critical / no_information.

### robins_d6

Domain label: bias in **measurement of outcomes**. Signaling question: could outcome measurement differ by intervention group or be influenced by knowledge of intervention? Check instrument validity and differential surveillance. Judgment slot: low / moderate / serious / critical / no_information.

### robins_d7

Domain label: bias in **selection of the reported** result. Signaling question: is there selective reporting of outcomes, time points, or analyses among multiple eligible options? Use protocols/registries when available. Judgment slot: low / moderate / serious / critical / no_information.

### robins_overall

Overall ROBINS-I risk follows the most severe domain judgment (critical/serious dominate). Record overall low / moderate / serious / critical / no_information and how it feeds GRADE and sensitivity inclusion rules. Do not invent domain ratings to force a favorable overall.

---

## E. GRADE certainty

Apply per critical outcome. Start from study design body (trials vs observational), then consider downgrades and limited upgrades. **Do not algorithmically fabricate certainty**; every rating needs domain notes and remains open to human revision.

### grade_risk_of_bias

Downgrade when the body of evidence for the outcome is limited by study-level RoB/ROBINS judgments that could change the estimate. Summarize whether limitations are serious or very serious; link to domain tables. Certainty impact: none / serious / very serious.

### grade_inconsistency

Downgrade for unexplained heterogeneity of effects across studies (direction/magnitude) after considering clinical/methodological diversity. Use hetero plan outputs (I²/τ²/PI or qualitative). Do not ignore conflicting directions to preserve a high rating.

### grade_indirectness

Downgrade when population, intervention, comparator, or outcome differs from the review question (PICO mismatch), or when surrogate outcomes stand in for decision-critical endpoints without strong linkage.

### grade_imprecision

Downgrade when confidence intervals (or study information size) are compatible with both meaningful benefit and harm/null relative to a pre-stated decision threshold. Do not invent CI widths. If quantitative synthesis is absent, judge imprecision narratively from study sizes and estimate instability.

### grade_publication_bias

Downgrade when reporting bias assessment suggests missing studies or selective non-reporting that could distort the synthesized effect. Use the reporting_bias plan; if assessment is infeasible, document `uncertainty` rather than a false clean bill.

### grade_upgrade_factors

Consider upgrades only for observational bodies when appropriate: large effect, dose-response gradient, or residual confounding that would only reduce a demonstrated effect. Upgrades are exceptional and must be justified; never upgrade to offset unexamined serious risk of bias.

### grade_certainty

Summarize final certainty as high / moderate / low / very low for each critical outcome with a one-paragraph rationale tying downgrade/upgrade decisions. Do not invent a certainty rating and do not fabricate certainty to match a desired narrative. Record human confirmation status for conclusion-bearing uses.

---

## F. Effect measures, heterogeneity, sensitivity

### effect_measure_primary

Declare the primary effect measure for the main outcome before results (examples: RR, OR, HR, MD, SMD) with rationale linked to decision use, baseline risk, and how included studies typically report results. State interpretation boundaries (relative vs absolute; standardized units).

### effect_measure_by_outcome_type

Map measures by outcome type: **binary** → RR/OR/RD with preference rule; **continuous** → MD when units shared else SMD with instrument caveats; **time-to-event** → HR with proportional-hazards caution. Note compatible transformations and when conversion is invalid due to missing variance or non-alignable scales.

### hetero_stats

For justified meta-analysis, plan statistical heterogeneity via I² and/or τ² and/or a prediction interval. If meta-analysis is not done, use a qualitative heterogeneity alternative: structured tables of design, population, intervention intensity, and outcome timing. Never compute fake I² from invented study data.

### hetero_exploration

Pre-specify subgroup analyses and/or meta-regression only with scientific rationale and limited multiplicity. Warn that data-driven subgroup fishing is not confirmatory. If exploration was not pre-specified, label findings as hypothesis-generating. Clinical vs methodological vs statistical heterogeneity must be discussed separately.

### sensitivity_analyses

List at least two concrete sensitivity analyses, each with a trigger:

1. **Risk-of-bias restricted analysis** — trigger: one or more studies at high (or serious/critical) risk for the outcome; re-run synthesis excluding them or present side-by-side narrative.
2. **Model or inclusion-decision analysis** — trigger: fixed vs random model choice is contested, or borderline eligibility studies exist; compare conclusions under the alternative pre-stated rule (e.g., leave-one-out of the largest study, or fixed vs random if both were pre-allowed).

Optional additional analyses (still pre-state if used): missing-data assumptions; industry-funded exclusion; alternative effect measures. Report non-execution as `blocked`/`missing`, not as silent success.

---

## G. Anti-pooling semantics

### anti_pooling_conditions

Pooling is forbidden when any of these concrete conditions hold (non-exhaustive minimum three):

1. **Incompatible effect measures or scales** that cannot be lawfully transformed without unjustified assumptions (e.g., mixing non-convertible instruments with missing variances).
2. **Clinical diversity too high** for a single estimand (materially different populations, intervention intensity, co-interventions, or outcome definitions such that an average effect is not decision-meaningful).
3. **Single-study or non-independent clusters only** for the synthesis unit (cannot present a multi-study pooled estimate; overlapping populations double-counted).
4. Additional common triggers: missing variance with no justifiable imputation; extreme statistical heterogeneity with contradictory directions and no pre-specified explanation path.

### anti_pooling_action

When any anti-pooling condition triggers, the mandatory action is **structured narrative synthesis / SWiM** (or equivalent ordered tables by design and risk of bias): describe direction, magnitude ranges as reported, and certainty caveats **without** inventing a pooled mean effect. **Forbid invented pooled numbers and forest plots** built from fabricated or non-poolable data; **no silent numeric pooling**. If software output is unavailable, do not hallucinate forest plot values. State clearly that quantitative synthesis was not performed and why.

---

## H. Report field obligations

Report instructional depth lives with `prisma_report_skeleton.md`. Protocol authors must ensure the report can fill:

### report_title_abstract

Identify the report as a systematic review/meta-analysis; structured abstract covering objectives, sources, eligibility, methods, results summary without invented numbers, limitations, registration.

### report_methods_eligibility

Restate PICOS/PECOS eligibility and deviations from protocol with dates.

### report_methods_search

Full strategies or repository link plan; dates last searched; constraints when adapters missing.

### report_methods_selection

Dual screen process, conflicts, automation tools if any (without inventing tool performance).

### report_methods_data

Extraction items, missing data, assumptions.

### report_methods_rob

Tools, level of assessment, how RoB informs synthesis.

### report_methods_synthesis

Meta-analysis vs narrative criteria, effect measures, hetero/sensitivity/anti-pooling rules actually applied.

### report_results_selection_flow

PRISMA flow counts only from real logs; zeros allowed; never fabricate funnel counts.

### report_results_study_chars

Study-level characteristics table with citations and locators for key facts.

### report_results_rob

Domain judgments per study/result; summary without decorative misrepresentation.

### report_results_synthesis

Pooled results only if legitimately computed from real extracted data; otherwise narrative/SWiM findings and explicit non-pooling.

### report_discussion_certainty

GRADE-linked interpretation, limitations of evidence and process, implications without overclaim.

### report_funding_competing

Funding, roles of funders, competing interests; mark `missing` if unknown rather than inventing clean COI.

---

## Human gates

- [ ] Protocol criteria human-locked before screening
- [ ] Synthesis approach human-locked before quantitative pooling attempts
- [ ] No invented studies, effect sizes, pooled estimates, or forest plots
- [ ] Anti-pooling narrative/SWiM used when conditions trigger
- [ ] GRADE certainty not algorithmically fabricated
- [ ] Registration/version deviations logged
- [ ] Residual known / missing / blocked / uncertainty honest
