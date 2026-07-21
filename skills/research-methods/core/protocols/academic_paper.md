<!--
essential_core_lineage:
  file: core/protocols/academic_paper.md
  implementation: first-party-rewrite
  upstream_concepts:
    - academic paper pipeline
    - revision coach
    - rebuttal audit
    - disclosure mode
    - protected hedging
    - commitment ledger
  upstream_path_hints:
    - ars/.../academic-paper
    - ars/.../revision_patch_protocol
    - ars/.../disclosure_mode_protocol
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Academic Paper Protocol

Grok annotation: Essential Core E3-B paper modes + revision/rebuttal/disclosure by Grok on 2026-07-20.

**parity: partial** — E3-B academic-paper vertical slice is operational offline for
eleven mode-scoped contracts, revision transition safety, rebuttal audit
consistency, and disclosure integrity. Not full ARS multi-agent runtime,
deterministic patch-apply, or venue-policy matrix parity. Manuscript-review
depth remains outside this protocol (separate E3-C surface).

## Intent

Provide mode-isolated instructions for full, plan, outline-only, revision,
revision-coach, abstract-only, lit-review, format-convert, citation-check,
disclosure, and rebuttal-audit. Each mode owns its inputs, outputs, stop
conditions, offline fallback, human gates, and handoffs where relevant.
Generators emit claim-intent pre-commit; evaluators never invent supportive
citations or peer identities. Heuristics may escalate risk but never prove
semantic preservation of protected claims.

## Runtime binding

Workflow: `academic-paper`. Registry tokens use hyphens (`outline-only`);
mode-scoped field IDs use underscores (`outline_only`). Contracts:
`generator_evaluator.md`, `evidence_states.md`, `evidence_verdict.md`.
Designated templates: `argument_map.md`, `revision_roadmap.md`,
`rebuttal_audit.md`, `disclosure_statement.md`, plus citation templates for
citation-check. Private helpers live in `essential_quality_gates.py` and wire
into public gates `content_depth` and `generator_evaluator_separation` only.

## Mode token map

| Registry token | Field slug |
| --- | --- |
| full | full |
| plan | plan |
| outline-only | outline_only |
| revision | revision |
| revision-coach | revision_coach |
| abstract-only | abstract_only |
| lit-review | lit_review |
| format-convert | format_convert |
| citation-check | citation_check |
| disclosure | disclosure |
| rebuttal-audit | rebuttal_audit |

---

## Mode: full

### full_mode_inputs

Require a research question or claim intent, audience/venue class, evidence
badge inventory (known/missing/blocked/uncertainty), and an argument map
seed. Reject empty “write a paper on X” without Socratic scoping when the
topic is vague. Bind to `argument_map.md` for claim-intent nodes before prose.

### full_mode_outputs

Emit claim-intent pre-commit, sectioned draft or section plan with evidence
states, citation inventory placeholders, and human-gate checklist. Do not
emit peer-review scores from the generator. Mark invented results as forbidden.

### full_stop_conditions

Stop drafting conclusion-bearing results when primary evidence is missing or
blocked. Stop if claim-intent pre-commit is absent. Stop and escalate when the
user asks to fabricate citations, effect sizes, or reviewer identities.

### full_offline_fallback

Without discovery backends, complete plan+outline+argument map only; leave
empirical claims as missing/blocked. Never invent literature or results to
simulate a full manuscript offline.

### full_human_gates

Require human sign-off before treating the draft as submission-ready, before
asserting novelty, and before promoting any claim beyond extract-backed
support. Record who confirmed and when.

### full_claim_intent_precommit

Before body prose, list atomic claims with intended evidence state, support
status target, and dependency nodes. Generators must not self-score the draft
as a final peer review. Claim-intent is a pre-commit contract, not decoration.

### full_no_invented_results

Never invent studies, effect sizes, p-values, confidence intervals, sample
sizes, or “data not shown” results. If a result is required and unavailable,
mark missing/blocked and stop conclusion language.

---

## Mode: plan

### plan_mode_inputs

Collect topic, decision use, constraints (length, venue, timeline), and known
evidence gaps. Prefer FINER-aware question candidates when the topic is vague;
handoff to research-question protocol when refinement is the real need.

### plan_mode_outputs

Produce a chapter/section negotiation plan, insight capture list, risk list,
and evidence-map placeholders. Do not write full draft body prose in plan mode
unless the user explicitly upgrades to full.

### plan_stop_conditions

Stop when chapter order is unresolved by the human, when novelty is asserted
without literature search, or when the plan would require invented methods
results. Prefer open questions over false completeness.

### plan_offline_fallback

Run Socratic plan capture offline without inventing literature. Label every
unsupported method choice as uncertainty. Do not fabricate a literature-backed
novelty claim offline.

### plan_human_gates

Human confirms chapter order, in-scope methods family, and out-of-scope list
before upgrade to full or outline-only. Insight capture requires author review.

### plan_chapter_negotiation

Negotiate section order, depth, and dependency edges with the human. Record
accepted, deferred, and rejected chapter proposals with one-line rationale.
Do not silently drop human-rejected sections.

### plan_insight_capture

Capture non-obvious insights, open risks, and decision criteria as labeled
notes with evidence states. Insights are not results; never promote an insight
to a confirmed finding without support.

---

## Mode: outline-only

### outline_only_mode_inputs

Accept an approved plan or equivalent section list, claim-intent seeds, and
evidence-map placeholders. Reject requests that treat outline-only as a full
draft delivery without mode upgrade.

### outline_only_mode_outputs

Emit hierarchical outline, per-section purpose, evidence-map slots, and
dependency notes. Include argument-map links where claims appear. No full
paragraph draft body unless user upgrades mode.

### outline_only_stop_conditions

Stop if the outline claims completed results, completed PRISMA flows, or
finished peer review. Stop when evidence-map slots are silently filled with
invented sources.

### outline_only_offline_fallback

Produce outline plus empty evidence-map placeholders offline. Mark unknown
source slots as missing. Never fabricate citation strings to fill the map.

### outline_only_human_gates

Human confirms outline scope and that no draft-body claim is being smuggled
as “outline complete.” Author sign-off required before treating outline as the
manuscript skeleton for revision tracking.

### outline_evidence_map

For each outline node, record expected evidence type (claim/extract/inference),
known sources, and missing/blocked gaps. Empty slots stay empty; do not invent
fills. Link high-stakes claims to argument-map nodes.

### outline_no_draft_body_claim

Outline-only must not claim that full Results/Discussion prose is complete.
If paragraph text appears, label it provisional scaffold and refuse
submission-ready language.

---

## Mode: revision

### revision_mode_inputs

Require before-text (or version pointer), reviewer or self-critique issues,
protected claims/hedges list, prior commitment ledger if resuming, and author
intent for each change class. Refuse revision that starts by wiping history.

### revision_mode_outputs

Emit patch-or-change ledger rows, updated commitment ledger fulfillment,
protected-claim disposition, new-evidence gate rows, recovery checkpoint, and
after-text only when changes are ledgered. Bind to `revision_roadmap.md`.

### revision_stop_conditions

Stop on silent deletion or strengthening of protected hedges, silent new DOI
or result inserts, false ledger claims, missing author sign-off, or lost
recovery checkpoint when resuming. Heuristics may flag risk; they never prove
semantic preservation.

### revision_offline_fallback

Operate with human-supplied before/after text and structured ledgers only.
Without apply binaries, still enforce ledger discipline. Do not claim
deterministic patch-apply parity.

### revision_human_gates

Author sign-off is mandatory for protected claim changes and conclusion-bearing
new evidence. Recovery resume requires a non-empty checkpoint. Human confirms
version-family conflicts are not auto-swapped.

### revision_protected_claims

List protected claims and hedges that must survive unless a ledgered
delete/replace names them and author_signoff is true. Soft hedges must not be
silently upgraded to hard claims. Helpers may escalate; they never certify
meaning-preserving rewrites.

### revision_commitment_ledger

Rows: concern_id, commitment_text, commitment_type, required_evidence_type,
fulfillment_status. Lifecycle: extracted → planned → in_progress → fulfilled
or waived_with_rationale. Waivers need human confirmation.

### revision_patch_or_change_ledger

Named change units with op in {add, delete, replace, move, annotate}, target
span, summary, and optional evidence_state. A ledger row that claims a change
absent from after-text is a false ledger claim. No silent untracked edits.

### revision_no_silent_new_evidence

New DOI, citation, numeric result, or primary-finding language in after-text
must appear in new_evidence_rows with evidence_state in {claim, extract,
human-confirmed} and human_gate true for conclusion-bearing inserts.

### revision_author_signoff

Boolean human gate. Any protected change or new-evidence insert without
author_signoff fails closed. Sign-off is not implied by chat tone or model
confidence.

### revision_recovery_checkpoint

When resuming interrupted or major revision, require a non-empty recovery
checkpoint referencing the ledger version. Restart wipe without checkpoint is
forbidden. Record checkpoint id/time/note.

---

## Mode: revision-coach

### revision_coach_mode_inputs

Reviewer comments or issue list, manuscript version pointer, and optional
prior roadmap. Coach mode does not require full before/after patch application.

### revision_coach_mode_outputs

Roadmap skeleton only: issue → severity → disposition options → planned change
slots → evidence pointers. Fill `revision_roadmap.md` structure without
rewriting the manuscript body.

### revision_coach_stop_conditions

Stop if asked to silently rewrite the full manuscript under coach mode.
Stop if coach output is presented as completed revision without mode switch
to `revision`.

### revision_coach_offline_fallback

Structure comments into roadmap rows offline. Do not invent missing reviewer
points or fabricate author commitments. Mark unknown severity as uncertainty.

### revision_coach_human_gates

Author chooses dispositions and upgrades to revision mode before manuscript
mutation. Coach suggestions are non-binding until human accepts them.

### revision_coach_roadmap_only

Outputs are organizational: tables, checklists, and response skeletons. No
full section rewrites, no silent claim upgrades, no generated final rebuttal
letter presented as author-approved.

### revision_coach_forbid_full_rewrite

If the user needs manuscript mutation, hand off to `revision` mode with
protected claims and change ledger. Coach must not claim parity with applied
patches.

---

## Mode: abstract-only

### abstract_only_mode_inputs

Manuscript claims list or section summaries with evidence states, language
targets (e.g., EN/ZH), and protected hedges from the parent draft. Reject
abstract-only when no claim inventory exists.

### abstract_only_mode_outputs

Structured abstract fields (background, methods, results, conclusions) per
language target, with missing-language marked `missing`. Preserve hedges from
source claims; do not harden conclusions.

### abstract_only_stop_conditions

Stop if results numbers are invented, if bilingual fields silently omit a
requested language, or if conclusions exceed supported claims in the source
inventory.

### abstract_only_offline_fallback

Draft abstract fields from supplied claim inventory only. Mark unavailable
numeric results as missing. Never invent effect sizes for abstract polish.

### abstract_only_human_gates

Human confirms bilingual accuracy and that protected hedges remain soft where
source claims were soft. Submission abstract needs author sign-off.

### abstract_bilingual_fields

Provide explicit slots per language. If a language cannot be produced honestly,
mark that language `missing` rather than auto-translating technical claims
without human review.

### abstract_protected_hedges

Carry forward may/might/suggests/possibly language from source claims. Do not
upgrade to proves/demonstrates/will without a ledgered revision of the source
claim and author sign-off.

---

## Mode: lit-review

### lit_review_mode_inputs

Paper-format literature synthesis goal, scope boundaries, and pointers to
primary discovery artifacts when available. Prefer MERGED_CORE_PAPERS authority
after convergence; do not fork a second core list.

### lit_review_mode_outputs

Paper-format synthesis outline or sections with evidence badges, gaps, and
citation inventory placeholders. Not a full PRISMA systematic review claim
unless the user is on systematic-review workflow.

### lit_review_stop_conditions

Stop if the mode claims completed PRISMA/RoB/GRADE execution that was not
performed. Stop on invented citations. Stop when discovery is required but
unavailable without recording offline limits.

### lit_review_offline_fallback

Synthesize only from human-supplied sources offline. Mark unsearched space as
missing. Do not invent a systematic search date or database list.

### lit_review_human_gates

Human confirms scope, inclusion boundaries, and that paper lit-review is not
misbranded as a completed systematic review. Novelty claims need human review.

### lit_review_handoffs

Hand off discovery, screening, RoB, and GRADE depth to E2 `deep_research` /
`systematic_review` protocols and templates. Paper lit-review remains
format-level synthesis plus honest gaps.

### lit_review_e2_handoff

When the user needs PRISMA protocol, dual screening, RoB2/ROBINS-I, GRADE, or
anti-pooling discipline, route to E2 surfaces rather than re-implementing them
here. Record the handoff explicitly.

### lit_review_no_prisma_full_claim

Do not claim full PRISMA systematic-review completion from paper lit-review
mode alone. If PRISMA artifacts exist, cite them; if not, label the product as
narrative or scoping synthesis as appropriate.

---

## Mode: format-convert

### format_convert_mode_inputs

Source manuscript path/format, target format (Markdown/LaTeX/DOCX/PDF/HTML),
style constraints, and engine availability notes. Refuse conversion that
requires inventing missing figures or results.

### format_convert_mode_outputs

Conversion checklist, structure mapping, unresolved engine dependencies, and
honest status for each target artifact. Produce converted text only when the
local engine path is real or the user supplies the target.

### format_convert_stop_conditions

Stop if asked to fabricate a PDF/DOCX binary without an engine. Stop when
citations would be silently altered during conversion. Stop on paywall or
credential-sharing requests.

### format_convert_offline_fallback

Emit checklist and mapping offline. Mark engine-missing targets as blocked.
Never claim a successful PDF build that did not run.

### format_convert_human_gates

Human confirms target venue style and accepts residual formatting debt. Binary
outputs require human verification of visual fidelity.

### format_convert_engine_checklist

Checklist items: source parse, reference style, figure/table paths, equation
handling, cross-references, bibliography engine, and export command. Each item
is done / missing / blocked.

### format_convert_runtime_honesty

If Pandoc/LaTeX/Word tooling is unset, say so. Optional runtime does not
become a fake success. No silent substitution of “looks like PDF” text for a
real build.

---

## Mode: citation-check

### citation_check_mode_inputs

Manuscript citation inventory, claim list, integrity mode (Mode1/Mode2), and
access constraints. Bind to `citation_integrity.md` and designated audit/report
templates.

### citation_check_mode_outputs

Inventory table, claim-source rows with verdicts from the fixed enum, risk
flags, access states, and escalation (PASS / PASS_WITH_NOTES / FAIL). No
network DOI lookup required for offline honesty.

### citation_check_stop_conditions

Stop clean VERIFIED language when locator/extract is missing, access is
blocked, or risk flags forbid clean verified. Stop if Mode2 is claimed without
full-scope checks.

### citation_check_offline_fallback

Inventory + unresolvable honesty offline. DOI tokens never promote to
VERIFIED. Mark network-dependent checks as blocked/unverified.

### citation_check_human_gates

Human confirms high-stakes VERIFIED rows (or verified_adapter path). Integrity
sign-off required before submission claims of clean citation audit.

### citation_check_inventory

Enumerate every citation string with durable id when known, locator needs, and
claims supported. Incomplete identity (no title and no id) stays incomplete.

### citation_check_bind_integrity

Bind each claim-support path to citation_integrity field contracts: identity,
locator_or_quote, claim_source_fidelity, temporal/version, risk, contamination
advisory, plagiarism boundary, access_state, and escalation.

---

## Mode: disclosure

### disclosure_mode_inputs

Author list, CRediT contributions, funding sources, competing interests,
data/code availability, AI assistance facts, and venue/policy selector state.
Refuse auto-complete of unknown legal facts.

### disclosure_mode_outputs

Filled disclosure statement surface with mandatory fields: CRediT, funding,
COI, data/code, AI assistance, policy/venue, and human confirmation. Bind to
`disclosure_statement.md`.

### disclosure_stop_conditions

Stop if AI/funding/COI are marked optional, auto-fabricated, or hollow. Stop
without mandatory human confirmation. Stop when venue rules are invented.

### disclosure_offline_fallback

Use human-supplied facts only. Unknown venue policy → uncertainty, not guessed
rules. Unknown funding/COI → explicit unknown pending author input, never a
fabricated “none” without confirmation.

### disclosure_human_gates

Mandatory human confirmation of the full disclosure package. Auto-generated
statements are drafts until human_confirmation is true.

### disclosure_credit

CRediT (or explicit equivalent) matrix: who did conceptualization, methods,
analysis, writing, supervision, etc. Missing contributions marked missing, not
invented.

### disclosure_funding

Funding statements are mandatory fields. If none, record explicit none only
with human confirmation. Do not optionalize funding disclosure.

### disclosure_coi

Competing interests / conflicts of interest are mandatory. Explicit none requires
human confirmation. Never auto-fabricate a clean COI statement.

### disclosure_data_code

Data and code availability statements with access path or honest restriction
reason. Missing repositories stay missing/blocked, not invented URLs.

### disclosure_ai

AI assistance disclosure is mandatory. Describe tools/roles used for writing,
analysis, or figure generation as known; mark unknown details missing. Never
optionalize or auto-fabricate AI declarations.

### disclosure_policy_or_venue

Record venue/policy selector. If unknown, state uncertainty and do not invent
journal-specific rules. Policy anchors remain human-confirmed.

### disclosure_human_confirmation

Require an explicit human confirmation field before treating disclosure as
final. Draft automation cannot self-confirm.

---

## Mode: rebuttal-audit

### rebuttal_audit_mode_inputs

Reviewer point list with stable point_ids, author rebuttal matrix rows (or
draft pointers), change ledger, and evidence pointers. Evaluator-only: no
generated author response prose as a pass artifact.

### rebuttal_audit_mode_outputs

Coverage matrix (covered/partial/missing), response_kind mapping
(ms_change/evidence/no_change_rationale), tone/overclaim flags, and unresolved
escalation block. Bind to `rebuttal_audit.md`.

### rebuttal_audit_stop_conditions

Stop audit-clean when any point is missing, when ms_change lacks ledger link,
when evidence/no-change rationale is empty, when generated_response_prose is
non-empty as a pass product, or when duplicates hide gaps.

### rebuttal_audit_offline_fallback

Audit coverage from supplied points and rows only. Refuse if the draft matrix
is missing. Do not invent reviewer points or author concessions.

### rebuttal_audit_human_gates

Human reviews unresolved points and tone/overclaim flags before submission of
any response letter. Evaluator does not author the letter.

### rebuttal_evaluator_only

Peer reviewer / audit role is evaluator-only. Do not generate final author
rebuttal prose under this mode. Coverage, gaps, risk flags, and consistency
checks only.

### rebuttal_point_coverage

Every reviewer point_id must appear exactly once in the matrix with coverage in
{covered, partial, missing}. Partial requires a gap note/pointer. Missing
blocks audit-clean.

### rebuttal_no_schema11_required

Point-level audit must not require a full nested commitment schema engine.
Lightweight point_id ↔ change/evidence/rationale consistency is sufficient and
mandatory.

---

## Shared hard rules

1. Generators and evaluators stay separated (`generator_evaluator.md`).
2. Evidence states use the seven-state vocabulary; never coerce missing to known.
3. No fabricated citations, statistics, or named real reviewers without source +
   human confirmation.
4. Protected hedges may be escalated by heuristics; semantic preservation is
   never “proved” by the helper.
5. Manuscript-review panel depth is out of scope for this protocol body.

## Human gates (global)

- [ ] No invented studies, effect sizes, citations, or reviewer identities
- [ ] Record known / missing / blocked honestly
- [ ] Author sign-off for conclusion-bearing revision and disclosure packages
- [ ] Rebuttal-audit remains evaluator-only
