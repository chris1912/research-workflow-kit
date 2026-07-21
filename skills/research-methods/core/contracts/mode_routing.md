<!--
essential_core_lineage:
  file: core/contracts/mode_routing.md
  implementation: first-party-rewrite
  upstream_concepts:
    - mode routing
    - command aliases
    - socratic override
  upstream_path_hints:
    - skills/research-methods/codex/scripts/ars_codex_full_runtime.py
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Mode Routing Contract

Grok annotation: Essential Core contract by Grok on 2026-07-20 (E1).

## Inputs

- user text
- optional alias (`ars-*` / `rm-*`)
- env flags (`RM_*` / `ARS_*`)
- optional prior passport stage

## Alias semantics

| Property | Rule |
| --- | --- |
| Nature | Compatibility routing inputs, not shell-installed binaries |
| Canonical | Prefer `rm-*`; accept `ars-*` as one-release synonyms |
| Resolution | Map known alias → workflow, mode, gates, protocol paths |
| Unsupported | Known pattern `ars-*`/`rm-*` but not in table → `error=unsupported_alias`, exit **2** |
| Free text | Never treated as unsupported_alias |

## Deterministic precedence (highest first)

1. Explicit command alias — lock route if known; fail if unknown `ars-*`/`rm-*`.
2. Explicit mode token in message (`mode:systematic-review`).
3. Vague paper-topic + unclear RQ → force `deep-research` / `socratic`.
4. Keyword heuristics per `MODE_REGISTRY.md`.
5. Ambiguity → one clarifying question; default highest-oversight safe mode (`plan` or `socratic`).

## Success JSON

```json
{
  "ok": true,
  "workflow": "deep-research",
  "mode": "socratic",
  "command_alias": null,
  "route_reason": "paper_topic_scoping_override",
  "agent_template": "runtime/agents/deep-research-team.md",
  "role_card": "core/teams/deep_research_roles.md",
  "protocol_paths": ["core/protocols/research_question.md", "core/protocols/deep_research.md"],
  "template_paths": ["core/templates/research_question_brief.md"],
  "quality_gates": ["vague_topic_socratic", "evidence_state_vocab"],
  "runtime": {
    "full_runtime": false,
    "agent_team": false,
    "hooks": false,
    "degraded": null,
    "missing_backends": []
  },
  "passport": {"resume": false, "reset_boundary": false, "checkpoint_hash": null},
  "error": null
}
```

## Error JSON

```json
{
  "ok": false,
  "error": "unsupported_alias",
  "message": "human-readable",
  "supported_aliases": ["ars-plan", "rm-plan"],
  "workflow": null,
  "mode": null
}
```

Exit codes: 0 success; 1 semantic failure; 2 usage/unsupported alias; 3 state/schema; 4 I/O; 5 internal.
