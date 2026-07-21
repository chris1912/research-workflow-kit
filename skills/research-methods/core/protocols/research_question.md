<!--
essential_core_lineage:
  file: core/protocols/research_question.md
  implementation: first-party-rewrite
  upstream_concepts:
    - research question agent
    - FINER
    - Socratic mentor
    - PICO/PECO
    - failure recovery
  upstream_path_hints:
    - ars/.../research_question_agent
    - socratic_mode_protocol
    - failure_paths
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Research Question Protocol

Grok annotation: Essential Core E2 method depth by Grok on 2026-07-20.

**parity: partial** — E2 research-question refinement depth implemented. Not full ARS behavioral parity. Do not invent studies, effect sizes, or novelty claims before evidence search.

## Intent

Transform vague topics into decision-relevant, researchable questions using topic decomposition, multi-type candidates, FINER scoring with human judgment, PICO/PECO (and context alternatives), scope boundaries, Socratic clarification, falsification, and honest evidence states. Never silently draft a paper from a vague topic.

## Runtime binding

Mode family: `deep-research` / `socratic` and RQ handoff from paper-topic overrides. See `MODE_REGISTRY.md` and `core/contracts/mode_routing.md`. Fill `core/templates/research_question_brief.md` as the operational brief.

## Evidence and claim states

Every open dimension must carry one of: `known` | `missing` | `blocked` | `uncertainty` (plus the full seven-state vocabulary when extracts exist). Do not coerce unknowns into fake knowns.

## 1. Topic decomposition

1. Restate the user's topic in neutral language without adding claims.
2. Extract domains, entities, relationships, outcomes, and decision use.
3. Identify whether the need is descriptive, comparative, associational, causal, or evaluative (or mixed).
4. List prior assumptions the user already made; mark each `known` / `missing` / `blocked` / `uncertainty`.
5. Stop if the user only needs a bibliography or manuscript critique—route to the matching mode instead of forcing an RQ rewrite.

## 2. Candidate questions (3–5)

Generate **3–5** candidate primary questions spanning applicable types:

| Type | When to include | Example shape (illustrative only) |
| --- | --- | --- |
| Descriptive | prevalence, status, mapping | What is the distribution of X in population Y during T? |
| Comparative | A vs B on outcome | How do A and B differ on outcome O under setting S? |
| Associational | correlation / co-occurrence | Is exposure E associated with outcome O after adjusting for C? |
| Causal | intervention/effect estimand | What is the effect of intervention I vs comparator C on O in P? |
| Evaluative | program/policy judgment | To what extent does program G achieve criterion K for stakeholders S? |

Rules:

- Each candidate must be specific enough to imply a method family.
- Do not invent a preferred answer or “expected significant result.”
- If the topic is purely qualitative experience-focused, prefer SPIDER-shaped candidates over forced causal PICO.
- Record why each candidate was proposed in one line.

## 3. FINER scoring (with failure behavior)

Score each candidate on Feasible, Interesting, Novel, Ethical, Relevant (1–5) with **written justification per criterion**.

| Criterion | Score 1 (weak) | Score 5 (strong) |
| --- | --- | --- |
| Feasible | No accessible data/methods/time | Clear data path, methods, and timeline |
| Interesting | Trivial or already closed | Addresses a real tension or decision need |
| Novel | Pure duplicate of settled work | New angle, population, method, or evidence need |
| Ethical | Serious unresolved risk | Risks manageable with oversight/consent plan |
| Relevant | No user for the answer | Directly informs practice, policy, or theory |

**Thresholds and failure:**

- Prefer average ≥ 3.0 and no criterion below 2.
- If all candidates fail threshold: do not force a winner; return a recovery plan (narrow population, change estimand, switch method family, or gather feasibility data).
- **Novelty:** do not assign a high novelty score as if literature were already searched. Before evidence search, novelty is a **provisional human judgment** marked `uncertainty` unless the human already confirms the gap. Never invent a “novelty score from the literature” offline.
- FINER is decision support, not an automatic pass; **human judgment** selects or revises the winner.

## 4. Structure frames: PICO / PECO and alternatives

Lock the winning question into a structure frame:

- **PICO** (intervention): Population, Intervention, Comparator, Outcome.
- **PECO** (exposure): Population, Exposure, Comparator, Outcome.
- **PICOT** when time horizon is decision-critical.
- **SPIDER** for qualitative/mixed experience questions: Sample, Phenomenon of Interest, Design, Evaluation, Research type.
- Other frames only when justified (e.g., policy PESTLE is not a substitute for outcome operationalization).

For each element record:

1. Operational definition (measurable or codeable).
2. Estimand / relationship type (effect, association, description, evaluation).
3. Population, setting, and time window.
4. Primary vs secondary outcomes; avoid kitchen-sink outcomes.
5. State `known` / `missing` / `blocked` / `uncertainty` per element.

## 5. Scope, assumptions, feasibility, ethics, falsification

### In-scope / out-of-scope

Write explicit inclusion and exclusion boundaries for populations, interventions/exposures, outcomes, designs, languages, and time. Out-of-scope needs a one-line rationale (not “later maybe”).

### Assumptions

List load-bearing assumptions (e.g., outcome ascertainment, access to records). Mark each with an evidence state.

### Feasibility and data access

State data sources, access permissions, sample size realism, timeline, skills, and compute. If access is closed, mark `blocked` and propose lawful alternatives—never paywall bypass or invented datasets.

### Ethics / IRB / data risk

Flag human participants, animals, sensitive personal data, dual-use, and consent needs. If IRB/ethics review is required or unknown, mark `blocked` or `uncertainty` and do not proceed to participant contact plans.

### Falsification

State what evidence would weaken or overturn the leading hypothesis or expected pattern. If nothing could falsify it, the question is not researchable—revise.

### Subquestions

Decompose into **2–3** subquestions that map to analysis or report sections. Each must be answerable with a method step, not rhetorical.

### Method-family mapping

Map primary + subquestions to method families (e.g., systematic review, observational study, RCT secondary analysis, qualitative interview study, simulation). Mapping is a plan, not a fabricated protocol result.

## 6. Socratic branch

Activate when the user is vague, wants guidance, or paper-topic override routes here.

Rules:

1. **Ask before proposing** a locked primary question. First turns clarify decision use, population, outcome, and constraints.
2. Track **unresolved dimensions** in a living list (population, exposure/intervention, comparator, outcome, time, setting, ethics, data access, success criterion).
3. **Bounded failure/recovery:** after a small fixed number of clarification rounds (default 3–5), if critical dimensions remain unresolved, stop proposing polish and issue a recovery package: unresolved list, 2–3 provisional candidates, what human must decide, and next mode options. Do not loop forever.
4. **Never silently draft a paper**, bibliography, or results section under this protocol. Deliverable is the RQ brief + open states only.
5. Prefer questions that make disagreements resolvable with evidence over questions that only invite opinion.

## 7. Stop / handoff criteria

**Stop (RQ complete enough to hand off)** when all are true:

- Primary question + 2–3 subquestions written.
- FINER table with justifications and human selection recorded (or explicit provisional selection marked `uncertainty`).
- Structure frame filled with operational outcomes and estimand.
- In/out scope, assumptions, feasibility, ethics, falsification present.
- Critical unknowns labeled `missing` / `blocked` / `uncertainty` (not hidden).

**Handoff targets:**

| Next need | Mode / protocol |
| --- | --- |
| Guided exploration continues | `deep-research` / `socratic` or `quick` |
| Broad evidence map | `deep-research` / `full` or `lit-review` |
| PRISMA-style review | `deep-research` / `systematic-review` → `systematic_review.md` |
| Paper drafting | only after RQ lock + human confirm → academic-paper modes |
| Experiment plan | experiment protocol (E4 depth separate) |

**Hard stops (do not hand off as “ready”):**

- User still has no decision use and refuses clarification.
- Ethics/IRB `blocked` without human disposition.
- Request is to fabricate significance, novelty, or citations.

## 8. Human gates

- [ ] Human confirms or revises the selected primary question
- [ ] Novelty remains provisional until evidence search unless human confirms known gap
- [ ] Ethics/data risks reviewed by a human when participants or sensitive data are involved
- [ ] No invented studies, effect sizes, citations, or reviewer identities
- [ ] Known / missing / blocked / uncertainty recorded honestly

## 9. Forbidden shortcuts

- Turning a vague topic into a full draft without RQ lock
- Fake FINER novelty from unsearched literature
- Collapsing all candidates into one without scoring or human choice
- Silent omission of ethics or data-access blockers
- Claiming ARS full parity or external discovery results without adapters
