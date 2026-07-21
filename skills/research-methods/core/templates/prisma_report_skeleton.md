<!--
essential_core_lineage:
  file: core/templates/prisma_report_skeleton.md
  implementation: first-party-rewrite
  upstream_concepts:
    - PRISMA report
  upstream_path_hints:
    - ars prisma report templates
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# PRISMA Report Skeleton

Grok annotation: Essential Core E2 template depth by Grok on 2026-07-20.
**parity: partial** — E2 report instructional sections. Fill only from real protocol execution logs; never invent counts, pooled estimates, or forest plots.

Use with `core/protocols/systematic_review.md` and a completed `prisma_protocol.md`.

## report_title_abstract

Title must identify the work as a systematic review and/or meta-analysis. Structured abstract slots: background/objectives; eligibility; information sources and date last searched; risk-of-bias methods; synthesis methods; results summary **without invented numbers**; limitations; registration number if real; funding note. Leave numeric slots blank or `missing` when unknown.

## report_methods_eligibility

Report inclusion/exclusion criteria with PICOS/PECOS elements, time/language/publication-status limits, and any protocol deviations with dates and human acknowledgment. Do not silently rewrite eligibility after seeing results.

## report_methods_search

Describe all information sources, present at least one reproducible strategy (or repository pointer), and state last search dates. If external discovery adapters were unset, say so and mark unsearched planned sources `missing`/`blocked` rather than fabricating hits.

## report_methods_selection

State number of reviewers, independence, conflict resolution, and any automation. Explain how full-text exclusion reasons were categorized for flow accounting. Dual screening is the default path unless a human-approved alternative was locked in the protocol.

## report_methods_data

List data items extracted, dual-extraction or audit policy, missing-data handling, and rules against unjustified imputation of critical variances. Require citation identity and locators for extracted effect estimates.

## report_methods_rob

Name RoB 2 and/or ROBINS-I (or justified alternative), level of assessment (study vs result), and how domain judgments informed synthesis, sensitivity analyses, and GRADE. Point to domain tables rather than inventing traffic-light summaries without assessments.

## report_methods_synthesis

State effect measures, meta-analysis vs narrative/SWiM decision rules, heterogeneity plan, sensitivity analyses, anti-pooling conditions, and reporting-bias methods actually applied. If pooling was forbidden, say narrative/SWiM was mandatory and that invented pooled numbers/forest plots are forbidden.

## report_results_selection_flow

Provide PRISMA-style flow accounting: records identified, duplicates removed, records screened, full-text assessed, excluded with reasons, studies included in qualitative synthesis, studies included in quantitative synthesis (may be zero). Use only logged counts; zeros are valid; never fabricate.

## report_results_study_chars

Present study characteristics (design, population, interventions/exposures, outcomes, follow-up, funding) with citations. Each key factual cell should be traceable to a locator. Mark unavailable fields `missing` instead of guessing.

## report_results_rob

Report domain-level judgments per study/result using protocol vocabulary (RoB 2: low|some_concerns|high|no_information; ROBINS-I: low|moderate|serious|critical|no_information). Summarize distribution without implying a numeric average risk score.

## report_results_synthesis

If a legitimate meta-analysis was computed from real extracted data, report estimates, CIs, and heterogeneity metrics available. If anti-pooling triggered or data insufficient, present structured narrative/SWiM findings only—**no invented pooled means or forest plots**, and no silent numeric pooling.

## report_discussion_certainty

Interpret findings against decision use, integrate GRADE certainty per critical outcome, discuss limitations of the evidence and of the review process, and avoid causal overclaim from association-only bodies. Separate known, missing, blocked, and uncertainty.

## report_funding_competing

Declare funding sources, funder roles in design/analysis/reporting, and competing interests of authors/reviewers. If unknown, record `missing` rather than inventing a clean disclosure.

## Human gates

- [ ] Flow counts trace to screening logs
- [ ] No fabricated pooled estimates or forest plots
- [ ] Certainty statements match GRADE notes
- [ ] Human sign-off before treating report as conclusion-bearing
