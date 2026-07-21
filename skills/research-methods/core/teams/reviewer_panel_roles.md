<!--
essential_core_lineage:
  file: core/teams/reviewer_panel_roles.md
  implementation: first-party-rewrite
  upstream_concepts:
    - reviewer panel role card
    - agent roles merge
    - four blind independents
  upstream_path_hints:
    - skills/research-methods/ars/.../reviewer_panel
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Reviewer Panel Role Card

Grok annotation: Essential Core internal role card by Grok on 2026-07-20 (E1).
Grok annotation: E3-C independent obligations + identity honesty by Grok on 2026-07-20.

This is an **internal** role card (not a Codex runtime prompt). Codex invocation
lives under `runtime/agents/`. Protocol: `core/protocols/manuscript_review.md`
(`parity: partial`, E3-C). Contract: `core/contracts/reviewer_independence.md`.

## Purpose

Independent reviewers write separate durable artifacts before synthesis.
Editorial synthesizer runs only after all independents complete. Minority DA
findings must retain disposition records with rationale. Reviewer identities
are anonymous/simulated unless named real person + source + human confirmation.

## Roles

- **field_analyst**: scopes manuscript package, rubric, and mode selection;
  blocks full-panel claims under quick; opens guided checkpoints when dialogue
  is required.
- **eic**: quick-mode desk triage only; recommends full panel when risks exceed
  skim depth; never fabricates four independent reports.
- **methodology_reviewer**: writes `review/independent/methodology.md` from
  shared package only; methods, stats reporting, reproducibility cues; no peer
  visibility before all independents complete.
- **domain_reviewer**: writes `review/independent/domain.md` from shared
  package only; related work fairness, theory, contribution; no peer drafts.
- **perspective_reviewer**: writes `review/independent/interdisciplinary.md`
  from shared package only; cross-field assumptions and measurement transfer;
  no peer drafts.
- **devils_advocate_reviewer**: writes `review/independent/devils_advocate.md`
  challenging core claims and outcome risks; minority findings must survive
  synthesis with disposition + rationale.
- **editorial_synthesizer**: runs only after four durable independents exist;
  severity-ranks without erasing minorities; emits simulated decision letter
  and revision roadmap; re-review residual scoring when in re-review mode.

## Mode obligations

| Mode | Primary roles | Hard bound |
| --- | --- | --- |
| full | four independents + synthesizer | blinds until four complete |
| re-review | synthesizer + residual tracker | trajectory + pointers |
| quick | eic | no full-panel claim |
| methodology-focus | methodology_reviewer | methods mandatory |
| guided | field_analyst + dialogue | checkpoints, no one-shot dump |
| calibration | field_analyst | human gold only (5–20); session-only |

## Shared hard rules

- Separate claim / extract / inference / uncertainty / missing / blocked / human-confirmed
- No fabricated citations, statistics, reviewer identities, or prestige
- Named real reviewers need identity_source + human confirmation
- Prefer offline honesty when backends are unset
- Human gates for venue-real decisions, identity, gold labels, and addressed closures
- Multi-process isolation is not claimed; validators only
