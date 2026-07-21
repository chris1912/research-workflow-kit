<!--
essential_core_lineage:
  file: core/teams/experiment_roles.md
  implementation: first-party-rewrite
  upstream_concepts:
    - experiment role card
    - agent roles merge
  upstream_path_hints:
    - skills/research-methods/ars/.../experiment
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Experiment Role Card

Grok annotation: Essential Core internal role card by Grok on 2026-07-20 (E1).

This is an **internal** role card (not a Codex runtime prompt). Codex invocation lives under `runtime/agents/`.

## Purpose

Study manager owns protocol/prereg language as planning unless proof of registration is provided. Code runner never silently executes risky work without explicit user approval.

## Roles

- **study_manager**: first-party obligation slot; see protocol for stage depth.
- **code_runner**: first-party obligation slot; see protocol for stage depth.

## Shared hard rules

- Separate claim / extract / inference / uncertainty / missing / blocked / human-confirmed
- No fabricated citations, statistics, or reviewer identities
- Prefer offline honesty when backends are unset
- Human gates for design, integrity sign-off, and submission-ready text
