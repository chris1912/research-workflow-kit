<!--
essential_core_lineage:
  file: core/protocols/deep_research.md
  implementation: first-party-rewrite
  upstream_concepts:
    - deep research workflow
    - source quality hierarchy
    - mode selection
    - counterevidence
    - ethics escalation
  upstream_path_hints:
    - ars/deep-research/WORKFLOW.md
    - mode_selection_guide
    - source_quality_hierarchy
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Deep Research Protocol

Grok annotation: Essential Core E2 method depth by Grok on 2026-07-20.

**parity: partial** — E2 deep-research mode behavior implemented offline. Not full ARS multi-agent runtime parity. External discovery handoff must not erase offline method execution.

## Intent

Execute rigorous, mode-specific research workflows with source hierarchy, claim/evidence discipline, counterevidence, ethics escalation, and honest stopping rules. Supports eight modes: `full`, `quick`, `review`, `lit-review`, `three-way-scan`, `fact-check`, `socratic`, `systematic-review`.

## Runtime binding

Planner modes under workflow `deep-research`. Role cards: `core/teams/deep_research_roles.md`. Optional Codex prompt: `runtime/agents/deep-research-team.md`. SR depth lives in `systematic_review.md` when mode is `systematic-review`.

## Shared foundations (all modes)

### Source-quality hierarchy

Prefer higher-tier evidence when the question is causal or estimand-heavy; always state the tier used.

1. Systematic reviews / meta-analyses with transparent methods
2. Individual randomized trials
3. Controlled non-randomized / quasi-experimental studies
4. Cohort / case-control observational studies
5. Systematic qualitative or descriptive syntheses
6. Single descriptive, qualitative, or case studies
7. Expert opinion, commentary, unreferenced web posts

Secondary sources (reviews, news, blogs) may orient search but do not replace primary evidence for claim verification. Mark secondary-only support as weaker and usually `uncertainty` until primary is checked.

### Primary vs secondary role

| Role | Use | Do not |
| --- | --- | --- |
| Primary | Extract claims, effect directions, methods, outcomes | Invent page numbers or quotes |
| Secondary | Map debates, find leads, summarize fields | Cite as if primary data |

### Metadata / abstract / full-text boundaries

- **Metadata only:** title, authors, year, venue, identifiers—ok for inventory; not for strong claims.
- **Abstract only:** may support provisional maps; mark claims `uncertainty` if not full-text confirmed.
- **Full text:** required before strong VERIFIED claims on methods, numbers, or nuanced conclusions.
- Lawful access only: OA, licensed, or human-supplied files. No paywall bypass. Access failure → `UNVERIFIABLE_ACCESS` / `blocked` / manual queue.

### Citation identity and locator discipline

Every extract needs durable identity (DOI, PMID, arXiv id, or stable URL) plus locator (page, section, figure/table, or paragraph). If identity or locator is missing, the claim cannot be VERIFIED.

### Query families

Plan multiple query families before treating search as complete (illustrative families, not fabricated hits):

1. Core concept block (PICO/PECO terms)
2. Synonyms / controlled vocabulary variants
3. Contrast / comparator and null results
4. Method-filtered family (reviews, trials, qualitative)
5. Recent-update family (time-boxed)

When external discovery adapters are unset, continue offline: use human-supplied corpora, prior matrices, and mark unsearched families `missing`/`blocked`. **Do not erase method steps** because a network search failed.

### Evidence matrix and claim decomposition

- Maintain a literature/evidence matrix (`literature_matrix.md`) with design, population, exposure/intervention, outcomes, extract, state.
- Decompose user or draft claims into atomic checkable units; one claim → one verdict path.
- Separate extract vs inference; never launder inference as extract.

### Counterevidence and devil's-advocate pass

Before conclusion-bearing synthesis, run an explicit counterevidence pass:

1. Seek disconfirming studies or alternative explanations.
2. Stress-test cherry-picking, base-rate neglect, and overgeneralization.
3. Record minority findings and why they were retained, downgraded, or rejected.
4. If no counterevidence search was possible, mark `missing` and lower certainty language.

### Contradiction handling

When sources conflict: tabulate the conflict, check population/time/method differences, prefer pre-registered and higher-tier designs when justified, and keep residual conflict as `uncertainty`—do not average away disagreement with invented pooled numbers.

### Ethics and escalation

Escalate to human stop when: participant harm risk, illegal activity, dual-use weaponization, requests to fabricate data/citations, or integrity violations. Ethics agent role may flag; humans dispose.

### Stopping and monitoring

Stop when mode deliverables are met, residual unknowns are labeled, and human gates for conclusion-bearing outputs are listed. Optional monitoring: define update triggers (new trial registry hits, guideline updates) without inventing alert results.

### Uncertainty and human confirmation

Conclusion-bearing outputs require human confirmation. Use evidence states honestly. Never convert `missing` into `known` to finish a draft.

### Forbidden shortcuts (global)

- Invented citations, quotes, effect sizes, or search hit lists
- Full paper draft under `socratic` or pure RQ scoping
- Silent pooling when SR anti-pooling conditions apply
- Claiming external discovery success when adapters are unset
- Skipping counterevidence on conclusion-bearing runs

---

## Mode branches

### Mode: `full`

**Purpose:** End-to-end research report from question through synthesis (not automatic journal submission).

**Minimum path:** RQ lock → method sketch → multi-family search plan → source verification → evidence matrix → claim decomposition → counterevidence/DA → structured synthesis → uncertainty + human gates.

**Minimum deliverables:** refined RQ; source hierarchy notes; evidence matrix; claim table with verdicts/states; counterevidence section; synthesis with boundaries; open `missing`/`blocked` list.

**Forbidden:** fabricating a results section; skipping RQ when topic is vague (route socratic first); pretending PRISMA completeness without systematic-review mode.

### Mode: `quick`

**Purpose:** Time-boxed orientation brief.

**Minimum path:** working question → 1–2 query families → high-tier preference scan → short evidence bullets → explicit limits.

**Minimum deliverables:** ≤ brief length synthesis; key sources with identity; confidence bounds; what a full pass would still need.

**Forbidden:** PRISMA-flow claims; meta-analytic numbers; exhaustive completeness claims.

### Mode: `review`

**Purpose:** Critique an existing manuscript/report the user supplies.

**Minimum path:** structure map → claim support sampling → methods threats → ethics flags → revision priorities. Reuse manuscript-review concepts without claiming E3 full panel independence unless that stage is active.

**Minimum deliverables:** prioritized issues; claim-support gaps; required human decisions; no rewrite-as-author unless asked.

**Forbidden:** inventing peer-reviewer identities; inventing citations to “fix” the draft; full ghostwriting under review mode.

### Mode: `lit-review`

**Purpose:** Structured literature map and thematic synthesis without mandatory meta-analysis.

**Minimum path:** scope → query families → matrix → themes/gaps → uncertainty.

**Minimum deliverables:** matrix; inclusion logic; theme map; gap list; dual-route handoff note if proposal-research HTML discovery is required.

**Forbidden:** fake comprehensive coverage; silent conversion into systematic-review completeness claims.

### Mode: `three-way-scan`

**Purpose:** Shortlist comparison on WHY / HOW / WHAT axes (or equivalent theoretical / methodological / empirical cut).

**Minimum path:** define the three axes → select candidate works with identity → score/compare on axes → recommend reading order.

**Minimum deliverables:** axis definitions; comparison table; limitations of the shortlist; no invented papers.

**Forbidden:** padding shortlist with fabricated titles; claiming systematic exhaustiveness.

### Mode: `fact-check`

**Purpose:** Verify specific claims against sources.

**Minimum path:** claim inventory → locate sources lawfully → extract with locator → verdict per claim → counterevidence check for high-impact claims.

**Minimum deliverables:** claim table with VERIFIED / MINOR_DISTORTION / MAJOR_DISTORTION / UNVERIFIABLE / UNVERIFIABLE_ACCESS; extracts; residual uncertainty.

**Forbidden:** verdict without locator; inventing sources that “would” confirm the claim.

### Mode: `socratic`

**Purpose:** Guided clarification; pairs with `research_question.md`.

**Minimum path:** ask before propose → track unresolved dimensions → bounded recovery → RQ brief only.

**Minimum deliverables:** unresolved dimension list; 3–5 candidates when ready; FINER provisional table; stop/handoff options.

**Forbidden:** silent full report; bibliography inflation to look complete; skipping human choice on the winning question.

### Mode: `systematic-review`

**Purpose:** PRISMA-oriented systematic review / optional meta-analysis method execution.

**Minimum path:** hand off to `systematic_review.md` + PRISMA templates; human method lock before screening/synthesis; RoB/GRADE/effect/hetero/sensitivity/anti-pooling semantics mandatory.

**Minimum deliverables:** protocol fields; flow accounting plan; RoB and GRADE plans; synthesis decision with anti-pooling rules.

**Forbidden:** invented pooled estimates or forest plots; screening without protocol lock; algorithmic fake GRADE certainty.

---

## External discovery handoff

When dual-route literature discovery or HTML delivery is required, hand off to `proposal-research` **without dropping** offline method obligations: still maintain matrix schema, claim states, source hierarchy, and (for SR) protocol fields. Unset adapters ⇒ continue with `missing`/`blocked`, never fabricate hits.

## Human gates

- [ ] Mode selection matches user need (or socratic override documented)
- [ ] Lawful access only; access failures labeled
- [ ] Counterevidence pass done for conclusion-bearing outputs
- [ ] Human confirmation listed for final claims
- [ ] No invented evidence, statistics, or citations
