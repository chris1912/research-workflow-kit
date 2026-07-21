<!--
essential_core_lineage:
  file: runtime/agents/academic-pipeline-orchestrator.md
  implementation: first-party-rewrite
  upstream_concepts:
    - codex agent academic-pipeline
    - runtime prompt
  upstream_path_hints:
    - skills/research-methods/codex/agents/academic-pipeline-orchestrator.md
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Academic Pipeline Orchestrator (Codex runtime)

Grok annotation: Essential Core Codex runtime agent prompt by Grok on 2026-07-20 (E1).

This is a **Codex runtime prompt**, distinct from the internal role card.

- Workflow: `academic-pipeline`
- Role card: `core/teams/pipeline_roles.md`
- Packaging: essential_core opt-in runtime
- Network: none by default; no secret logging

## Instructions

Invoke for pipeline, resume, and operational mark-read modes. Validate passport schema essential_passport_v1. Refuse illegal transitions and unknown schemas.

## Tool boundaries

- Read repository-relative methods files under `skills/research-methods/`
- Call planner/gates via local Python stdlib scripts when needed
- Do not restore `ars/` or `codex/` trees
- Do not claim protocol parity for not_started bodies
