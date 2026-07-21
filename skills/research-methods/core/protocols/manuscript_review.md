<!--
essential_core_lineage:
  file: core/protocols/manuscript_review.md
  implementation: first-party-rewrite
  upstream_concepts:
    - paper reviewer modes
    - re-review residual trajectory
    - calibration gold labels
    - four blind independents
    - minority disposition
  upstream_path_hints:
    - ars/.../academic-paper-reviewer
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Manuscript Review Protocol

Grok annotation: Essential Core E3-C manuscript-review vertical slice by Grok on 2026-07-20.

**parity: partial** — E3-C manuscript-review vertical slice is operational offline for
six mode-scoped contracts, four blind independent perspectives, synthesis and
minority barriers, reviewer-identity provenance, re-review trajectory,
calibration-gold honesty, and designated templates. Multi-process reviewer
isolation remains an honest non-claim: deterministic stage validators provide
partial parity only. Not full ARS multi-agent runtime or process-isolation
parity. Academic-paper drafting depth remains outside this protocol (E3-B).

## Intent

Provide mode-isolated instructions for full, re-review, quick,
methodology-focus, guided, and calibration. Each mode owns its inputs,
outputs, stop conditions, offline fallback, and human gates. Four independent
reports stay blind until durable methodology, domain, interdisciplinary, and
devil's-advocate artifacts exist; synthesis runs afterward only. Decision
letters stay labeled simulated unless a real venue/editor process and human
authority are supplied. Never fabricate reviewer names, prestige, gold labels,
or peer-review scores as real.

## Runtime binding

Workflow: `academic-paper-reviewer`. Registry tokens use hyphens
(`methodology-focus`, `re-review`); mode-scoped field IDs use underscores
(`methodology_focus`, `re_review`). Contracts: `reviewer_independence.md`,
`evidence_states.md`. Designated templates: `manuscript_review_full.md`,
`editorial_decision.md`, plus residual tracking on `revision_roadmap.md`.
Private helpers live in `essential_quality_gates.py` and wire into public gates
`reviewer_independence` and `content_depth` only. Existing A20
`early_visibility`, `premature_synthesis`, and `missing_disposition` validators
remain binding.

## Mode token map

| Registry token | Field slug |
| --- | --- |
| full | full |
| re-review | re_review |
| quick | quick |
| methodology-focus | methodology_focus |
| guided | guided |
| calibration | calibration |

---

## Mode: full

### full_mode_inputs

Require the manuscript package (title, version, body or sections), genre,
optional venue class, shared rubric, and evidence-badge inventory. Reject empty
“review this paper” without a manuscript pointer. Shared inputs only: no peer
independent drafts may be supplied to any independent role before all four
complete.

### full_mode_outputs

Emit four durable independent reports (methodology, domain, interdisciplinary,
devil's advocate), then editorial synthesis, a simulated decision letter, and a
revision roadmap with concern IDs. Each minority/independent finding must carry
disposition retained|downgraded|rejected plus non-empty rationale. Do not emit
real-venue acceptance as fact without human authority.

### full_stop_conditions

Stop synthesis if any independent artifact is missing. Stop if early peer
visibility is detected. Stop if a minority/DA finding lacks disposition and
rationale. Stop and refuse when the user asks for fabricated reviewer names or
prestige personas presented as actual peers.

### full_offline_fallback

Without domain literature backends, complete structural and methods checks from
the manuscript alone; mark external novelty claims as uncertainty/missing.
Never invent peer reports or gold labels offline to simulate a full panel.

### full_human_gates

Require human sign-off before treating a decision letter as venue-real, before
naming any real-person reviewer, and before promoting simulated scores as
official peer review. Record who confirmed and when.

### full_independent_methodology

Methodology independent consumes only the shared manuscript package and rubric.
Check design, sampling, analysis plan, statistics reporting honesty, and
reproducibility cues. Write a durable methodology report with concern IDs
before any synthesis prose. Do not read peer independents.

### full_independent_domain

Domain independent consumes only the shared manuscript package and rubric.
Check related work fairness, theory fit, contribution framing, and domain
assumptions. Write a durable domain report with concern IDs before synthesis.
Do not read peer independents.

### full_independent_interdisciplinary

Interdisciplinary independent consumes only the shared package and rubric.
Probe cross-field assumptions, measurement transfer, and alternative framings.
Write a durable interdisciplinary report with concern IDs before synthesis.
Do not read peer independents.

### full_independent_devils_advocate

Devil's-advocate independent challenges the core argument, outcome switching
risks, and unsupported primary claims. Minority findings must not be erased by
later majority vote. Write a durable DA report with concern IDs before
synthesis. Do not read peer independents.

### full_synthesis_barrier

Editorial synthesis starts only after all four durable independent outputs
exist. Synthesis may severity-rank concerns but must not rewrite independent
history. Premature synthesis fails closed (`premature_synthesis`). Inline
single-agent mode still writes four separate artifacts in order first.

### full_minority_disposition

Every independent concern, including DA minority findings, ends with
disposition retained|downgraded|rejected plus a non-empty rationale. Rejected
items require severity. Missing disposition fails closed
(`missing_disposition`). Erasing minority findings is forbidden.

### full_decision_letter_simulated

Decision class uses accept / minor / major / reject / revise-resubmit and must
be labeled **simulated** unless a real venue/editor process and human authority
are both supplied. Blocking vs non-blocking issues map to concern IDs. No
fabricated editor names or journal prestige.

### full_revision_roadmap

Map each retained or partially retained issue to severity, planned change, and
evidence pointer placeholders for residual re-review. Issue IDs must stay
stable for later trajectory scoring. Do not claim all issues fixed at full
mode exit.

---

## Mode: re-review

### re_review_mode_inputs

Require the prior residual issue checklist with non-empty unique prior issue
IDs, the revised manuscript or evidence pointers, and prior dispositions.
Reject re-review that lacks prior issue IDs or invents a clean slate.

### re_review_mode_outputs

Emit current residual rows that cover prior issues exactly, with trajectory
open | partially_addressed | addressed | new. Addressed rows need a
manuscript/evidence pointer. New rows are additive only and never masquerade
as prior closure. Include honest remaining open set.

### re_review_stop_conditions

Stop if prior issue IDs are empty, duplicate, missing from current rows, or
orphaned without trajectory=new. Stop on blanket “all fixed” without per-issue
addressed pointers. Stop if addressed rows lack evidence pointers.

### re_review_offline_fallback

Score residual trajectory from supplied manuscript excerpts only. Mark
unverifiable closures as open or partially_addressed with uncertainty. Never
fabricate closure evidence offline.

### re_review_human_gates

Human confirms addressed closures that affect conclusion-bearing claims and
any waived residual. Model confidence never substitutes for pointer-backed
closure.

### re_review_prior_issues

Prior issue IDs must be non-empty and unique. Current residual rows must cover
those prior IDs exactly once each. Empty or duplicate prior IDs fail closed.

### re_review_trajectory

Trajectory vocabulary is exactly open | partially_addressed | addressed | new.
Addressed requires a non-empty manuscript or evidence pointer. New rows cannot
reuse a prior issue ID as fake closure. Open and partially_addressed remain
honest residuals.

### re_review_no_blanket_all_fixed

Forbid blanket all-fixed claims. Every prior issue needs its own trajectory
row; claiming global closure without per-issue addressed pointers fails. Silent
disappearance of residuals is not allowed.

### re_review_evidence_pointers

Addressed and partially_addressed rows should cite manuscript locations or
evidence badges. Addressed without pointer fails. Pointers may be section,
figure, table, or extract locators—not prestige language.

---

## Mode: quick

### quick_mode_inputs

Require manuscript snapshot, decision use (desk triage vs coaching), and
explicit quick-scope statement. Do not accept a request that secretly expects
four full independent reports under the quick label.

### quick_mode_outputs

Emit a short EIC-style triage note: major risks, missing sections, and whether
full panel review is recommended. Label the output as quick-scope only. Do not
emit four independent durable reports as if completed.

### quick_stop_conditions

Stop if the user requires full-panel independence under quick mode. Stop if
outputs claim full independent completion, synthesis readiness, or venue-real
decision letters. Escalate to full mode instead of faking depth.

### quick_offline_fallback

Produce structural triage from the manuscript alone. Mark domain novelty and
stats adequacy as uncertainty when evidence is thin. Never invent panel scores.

### quick_human_gates

Human confirms that quick triage is sufficient for the decision use, or
upgrades to full/methodology-focus. Quick outputs are not submission-ready
peer review.

### quick_scope_limit

Quick mode is desk triage / EIC skim depth only. Cap claims to high-level
blocking risks and missing-method flags. Do not silently expand into full
four-perspective review without mode change.

### quick_no_full_panel_claim

Quick mode must never claim full-panel completion, four blind independents,
or synthesis-after-panel readiness. If full-panel language appears, fail and
redirect to full mode. Honesty beats faux completeness.

---

## Mode: methodology-focus

### methodology_focus_mode_inputs

Require manuscript methods/results sections, analysis claims, and any
statistical reporting blocks. Domain narrative without methods is insufficient
for this mode alone.

### methodology_focus_mode_outputs

Emit a methodology-mandatory independent report covering design, sampling,
analysis, stats reporting standards, and reproducibility cues, plus optional
light domain notes labeled non-panel. Do not claim four-blind full panel
unless upgraded to full.

### methodology_focus_stop_conditions

Stop if methods sections are missing/blocked and the user demands definitive
stats adequacy. Stop if outputs invent completed domain/interdisciplinary/DA
independents. Escalate missing data honestly.

### methodology_focus_offline_fallback

Review methods prose offline without inventing code or data audits. Mark
unverifiable analysis claims as uncertainty. Prefer checklists over fabricated
re-analysis.

### methodology_focus_human_gates

Human confirms any high-severity methods fail that would drive reject-class
language. Stats judgment remains advisory without raw data access.

### methodology_focus_mandatory_methods

Methodology checks are mandatory: design clarity, eligibility, sample size
honesty, outcome definitions, analysis plan vs reported analyses, and missing
method steps. Empty methods praise fails this mode.

### methodology_focus_stats_checks

Apply statistical reporting standards checks (effect sizes, uncertainty,
multiplicity honesty, selective reporting risk) without inventing re-computed
p-values. Flag silent switching and unsupported significance language.

---

## Mode: guided

### guided_mode_inputs

Require manuscript pointer, user goals for the review dialogue, and current
checkpoint state (open questions, provisional concerns). Guided mode is a
conversation scaffold, not a one-shot dump.

### guided_mode_outputs

Emit multi-turn dialogue checkpoints: clarifying questions, provisional
concern candidates, and human confirmations before freezing issue IDs. Preserve
checkpoint history. Final freeze may hand off to full or re-review.

### guided_stop_conditions

Stop one-shot “here is your full review” dumps that skip dialogue checkpoints.
Stop if the user freezes issues without confirming provisional concern text.
Do not claim full-panel independence from a single guided turn.

### guided_offline_fallback

Run Socratic issue dialogue offline from the manuscript alone. Leave external
novelty and unreproducible stats as open questions. Never invent peer consensus
in guided chat.

### guided_human_gates

Human confirms each checkpoint before concern IDs freeze, and before any
upgrade to full synthesis. Dialogue history is part of the audit trail.

### guided_dialogue_checkpoints

Preserve dialogue/checkpoint behavior: question → user answer → provisional
concern → confirmation → next checkpoint. Checkpoint IDs and open questions
must remain visible. Skipping checkpoints to dump a final review fails.

### guided_no_oneshot_dump

Guided mode forbids replacing dialogue with a single exhaustive review dump.
If outputs read as one-shot full review without checkpoints, fail and restore
dialogue structure. Depth comes from iterative confirmation, not monologue.

---

## Mode: calibration

### calibration_mode_inputs

Require human-supplied gold labels with non-empty item IDs and labels, plus
prediction rows that reference those IDs. Accepted gold set size is 5–20 items
with exact one-to-one prediction mapping. Missing, empty, fewer than 5, or more
than 20 gold rows fail closed. Do not invent gold labels when the user forgets
them.

### calibration_mode_outputs

Emit session-only calibration comparison: matched prediction IDs, agreement
notes, and disagreement rationales. Label results as non-persistent session
calibration. Do not claim a durable calibrated reviewer model.

### calibration_stop_conditions

Stop on missing_calibration_gold, empty gold, inadequate_gold_set (<5),
excessive_gold_set (>20), mismatched prediction IDs, or fabricated labels.
Stop if outputs claim persistent multi-session calibration storage. Exit
honesty over faux accuracy metrics.

### calibration_offline_fallback

Compare predictions to supplied gold offline only. If gold is absent, error
with missing_calibration_gold and stop—do not synthesize substitute labels.
No network leaderboard or external gold harvest.

### calibration_human_gates

Gold labels are human-owned. Human confirms any relabeling. Model-generated
pseudo-gold is forbidden even when confidence is high.

### calibration_gold_required

Calibration requires human-supplied gold labels (accepted range 5–20) and
matching prediction IDs. Missing gold, empty gold lists, underpowered sets
(<5), oversized sets (>20), or predictions without gold counterparts fail.
Helper errors: missing_calibration_gold, empty_gold, inadequate_gold_set,
excessive_gold_set, mismatched_prediction_ids.

### calibration_session_only

Keep calibration session-only. Do not claim persistent calibration profiles,
cross-run memory, or durable scoring models. Session comparison artifacts may
be saved by the human; the protocol does not persist them.

### calibration_no_fabricated_labels

Never fabricate gold labels, invent agreement scores from missing gold, or
backfill labels from model self-grades. Fabricated labels fail closed. Honesty
beats fake calibration curves.

---

## Shared hard rules (all modes)

### reviewer_identity_honesty

Anonymous or simulated role labels (methodology, domain, interdisciplinary,
devil's advocate, EIC) are allowed and must be labeled simulated/anonymous.
Named real-person reviewers require non-empty identity source and human
confirmation. Invented or assumed sources fail. No fabricated prestige.

### multi_process_non_claim

Multi-process reviewer isolation is **not** claimed. Deterministic stage
validators cover A20 visibility, premature synthesis, and minority disposition
semantics only. Process-level isolation remains partial parity.

## Human gates (package)

- [ ] No invented reviewer IDs, prestige, or gold labels
- [ ] Independent sections complete before synthesis (full mode)
- [ ] Minority/DA dispositions with rationale recorded
- [ ] Decision letter labeled simulated unless real venue + human authority
- [ ] Re-review trajectories pointer-backed; no blanket all-fixed
- [ ] Calibration gold human-supplied and session-only
- [ ] Quick never claims full panel; guided preserves dialogue checkpoints
