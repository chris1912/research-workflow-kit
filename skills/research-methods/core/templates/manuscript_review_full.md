<!--
essential_core_lineage:
  file: core/templates/manuscript_review_full.md
  implementation: first-party-rewrite
  upstream_concepts:
    - manuscript review
    - four blind independents
    - minority disposition
  upstream_path_hints:
    - Stage-D manuscript_review.md
    - ars academic-paper-reviewer templates
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Manuscript Review Full Template

Grok annotation: Essential Core E3-C designated full-panel review template by Grok on 2026-07-20.

**parity: partial** — Designated surface for full manuscript-review mode.
Protocol prose in `manuscript_review.md` cannot rescue hollow fields here. Not
multi-process isolation parity. Simulated review only.

**Stage-D successor** of `templates/manuscript_review.md`. Do not invent
reviewer identities or editorial decisions presented as real.

## 1. Manuscript snapshot

- Working title:
- Genre: empirical / review / methods / theory / other
- Target audience or venue class (optional):
- Version / date:
- Reviewer identity kind: anonymous / simulated_role / named_real
- Identity source (required if named_real):
- Human confirmation for named identity (true/false):

## 2. Structure map

| Section | Present? | Purpose of section | Main claim or contribution | Support status |
| --- | --- | --- | --- | --- |
| Title / abstract |  |  |  | |
| Introduction |  |  |  | |
| Methods |  |  |  | |
| Results |  |  |  | |
| Discussion |  |  |  | |
| Limitations |  |  |  | |
| References |  |  |  | |

## 3. Claim support checklist

- Primary contribution statement:
- Direct supporting extracts (with locators):
- Inferences beyond extracts:
- Counterevidence or alternative explanations:
- Items marked **uncertainty**:

### independent_methodology

Methodology independent report scaffold. Consume only the shared manuscript
package and rubric. Record design, sampling, analysis honesty, stats reporting
risks, and reproducibility cues with concern IDs. Do not read peer independent
drafts before all four complete. Leave durable methodology findings here.

| concern_id | finding | evidence_state | severity |
| --- | --- | --- | --- |
|  |  |  |  |

### independent_domain

Domain independent report scaffold. Consume only the shared package and rubric.
Record related-work fairness, theory fit, contribution framing, and domain
assumptions with concern IDs. Blind until all independents complete.

| concern_id | finding | evidence_state | severity |
| --- | --- | --- | --- |
|  |  |  |  |

### independent_interdisciplinary

Interdisciplinary independent report scaffold. Probe cross-field assumptions,
measurement transfer, and alternative framings. Shared package only; no peer
draft visibility before completion of all four independents.

| concern_id | finding | evidence_state | severity |
| --- | --- | --- | --- |
|  |  |  |  |

### independent_devils_advocate

Devil's-advocate independent report scaffold. Challenge core argument strength,
outcome switching, and unsupported primary claims. Minority findings must not
be erased later. Shared package only until all independents complete.

| concern_id | finding | evidence_state | severity | minority_note |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

### synthesis_barrier

Editorial synthesis is allowed only after methodology, domain,
interdisciplinary, and devil's-advocate durable sections exist. Premature
synthesis fails. Severity ranking is allowed; rewriting independent history is
not. Record that all four independents completed before this section.

- Independents complete (true/false):
- Synthesis started after barrier (true/false):
- Barrier notes:

### minority_disposition

Every independent concern, including DA minority findings, needs disposition
retained|downgraded|rejected plus non-empty rationale. Rejected requires
severity. Do not erase minorities by majority vote.

| concern_id | source_reviewer | disposition | rationale | severity |
| --- | --- | --- | --- | --- |
|  | methodology / domain / interdisciplinary / devils_advocate | retained / downgraded / rejected |  |  |

### decision_letter

Decision class accept / minor / major / reject / revise-resubmit must be labeled
**simulated** unless real venue process and human authority are both supplied.
Map blocking and non-blocking issues to concern IDs. No fabricated editor names.

- Decision class (simulated unless real authority):
- Simulated disclaimer present (true/false):
- Blocking issues:
- Non-blocking suggestions:
- Human authority recorded (true/false):

### revision_roadmap

Map residual issues to severity, planned change, and evidence pointer
placeholders for re-review. Issue IDs stay stable. Trajectory vocabulary for
later re-review: open | partially_addressed | addressed | new. No blanket
all-fixed claim at full-mode exit.

| Issue ID | Source reviewer | Severity | Disposition | Planned change | Evidence pointer | Trajectory |
| --- | --- | --- | --- | --- | --- | --- |
|  |  |  |  |  |  | open |

## 4. Simulated peer-review questions

1. Clarity of research question:
2. Methods adequacy and transparency:
3. Result-claim alignment:
4. Related work coverage and fairness:
5. Limitations and generalizability:
6. Presentation and reproducibility cues:

## 5. Independent sections (order required)

1. Independent Reviewer: Methodology
2. Independent Reviewer: Domain
3. Independent Reviewer: Interdisciplinary
4. Independent Reviewer: Devil's Advocate
5. Editorial Synthesis
6. Decision Letter
7. Revision Roadmap

## 6. Human gates

- [ ] No invented reviewer IDs or fake scores presented as real
- [ ] Independent sections complete before synthesis
- [ ] Minority/DA dispositions with rationale recorded
- [ ] Decision letter labeled simulated unless real venue + human authority
- [ ] Multi-process isolation not claimed
- [ ] Evidence badge recorded for claim/extract/inference/uncertainty/missing/blocked/human-confirmed rows
