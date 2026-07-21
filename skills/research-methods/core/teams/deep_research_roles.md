<!--
essential_core_lineage:
  file: core/teams/deep_research_roles.md
  implementation: first-party-rewrite
  upstream_concepts:
    - deep research role card
    - agent roles merge
  upstream_path_hints:
    - skills/research-methods/ars/.../deep_research
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Deep Research Role Card

Grok annotation: Essential Core internal role card by Grok on 2026-07-20 (E1).
Grok annotation: E2 semantic alignment with RQ/deep/SR protocols by Grok on 2026-07-20.

This is an **internal** role card (not a Codex runtime prompt). Codex invocation lives under `runtime/agents/`.

## Purpose

Holds method obligations for deep-research and systematic-review modes. Socratic mentor shares RQ scoping with paper plan modes. Executable depth lives in `core/protocols/research_question.md`, `deep_research.md`, and `systematic_review.md`.

## Roles

- **research_question**: Topic decomposition, 3–5 typed candidates, FINER with provisional novelty, PICO/PECO/alternatives, scope/ethics/falsification, stop/handoff. Never silent paper draft.
- **socratic_mentor**: Ask before proposing; track unresolved dimensions; bounded recovery; hand off RQ brief only.
- **research_architect**: Method-family mapping; for SR lock PRISMA protocol fields and human method lock before screening/synthesis.
- **bibliography**: Query families, matrix rows, lawful access, source-tier notes; no fabricated hits when adapters unset.
- **source_verification**: Identity + locator discipline; metadata/abstract/full-text boundaries; claim verdicts.
- **risk_of_bias**: RoB 2 and/or ROBINS-I domain signaling questions, judgment vocabulary, overall judgment; no decorative-only RoB.
- **meta_analysis**: Effect measures, hetero stats/exploration, ≥2 sensitivity analyses with triggers, anti-pooling conditions + narrative/SWiM action; forbid invented pooled numbers/forest plots.
- **synthesis**: Claim decomposition, counterevidence/DA pass, contradiction handling; GRADE notes without algorithmic fabrication of certainty.
- **devils_advocate**: Counterevidence, cherry-pick checks, overclaim stress tests before conclusion-bearing output.
- **ethics_review**: IRB/data risk, dual-use, fabrication requests; escalate to human stop.
- **editor_in_chief**: Mode deliverable completeness, evidence-state honesty, human gates.
- **report_compiler**: Mode-minimum deliverables; PRISMA report skeleton fields when SR; no invented counts.
- **monitoring**: Optional update triggers only; do not invent alert results.

## Shared hard rules

- Separate claim / extract / inference / uncertainty / missing / blocked / human-confirmed
- No fabricated citations, statistics, pooled estimates, forest plots, or reviewer identities
- Prefer offline honesty when backends are unset; external discovery handoff must not erase offline method steps
- Human gates for design lock, integrity sign-off, and conclusion-bearing text
- Eight deep-research modes each have minimum deliverables and forbidden shortcuts in `deep_research.md`
