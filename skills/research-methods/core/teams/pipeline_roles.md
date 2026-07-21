<!--
essential_core_lineage:
  file: core/teams/pipeline_roles.md
  implementation: first-party-rewrite
  upstream_concepts:
    - pipeline role card
    - agent roles merge
  upstream_path_hints:
    - skills/research-methods/ars/.../pipeline
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Pipeline Role Card

Grok annotation: Essential Core internal role card by Grok on 2026-07-20 (E1).

This is an **internal** role card (not a Codex runtime prompt). Codex invocation lives under `runtime/agents/`.

## Purpose

Orchestrator enforces legal stage transitions. State tracker owns passport checkpoints. Integrity verification can block Stage 3 on MATERIAL or AUDIT_FAILED.

## Roles

- **pipeline_orchestrator**: first-party obligation slot; see protocol for stage depth.
- **state_tracker**: first-party obligation slot; see protocol for stage depth.
- **integrity_verification**: first-party obligation slot; see protocol for stage depth.
- **claim_ref_alignment_audit**: first-party obligation slot; see protocol for stage depth.
- **collaboration_depth_advisory**: first-party obligation slot; see protocol for stage depth.

## Shared hard rules

- Separate claim / extract / inference / uncertainty / missing / blocked / human-confirmed
- No fabricated citations, statistics, or reviewer identities
- Prefer offline honesty when backends are unset
- Human gates for design, integrity sign-off, and submission-ready text
