<!--
essential_core_lineage:
  file: core/contracts/evidence_states.md
  implementation: first-party-rewrite
  upstream_concepts:
    - evidence badges
    - evidence states
  upstream_path_hints:
    - skills/research-methods/ars/.../evidence state guidance
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Evidence States Contract

Grok annotation: Essential Core contract by Grok on 2026-07-20 (E1).

## Required vocabulary (seven states)

| State | Meaning | Allowed use |
| --- | --- | --- |
| `claim` | Source-backed assertion after check | After verification |
| `extract` | Quotation / tightly bound paraphrase + locator | Always with locator |
| `inference` | Interpretation beyond the extract | Separate from extract |
| `uncertainty` | Conflict, weak support, incomplete check | Prefer over silent omission |
| `missing` | Needed item not present | Offline / adapter unset |
| `blocked` | Cannot proceed without human/backend | Hard stop until resolved |
| `human-confirmed` | Human signed off | Only after explicit confirm |

Stage-D four-badge set (`claim`, `extract`, `inference`, `uncertainty`) is a
**subset**. Essential Core must implement all seven.

## Rules

1. Never invent extracts or citations to convert `missing` into `claim`.
2. `human-confirmed` requires a recorded human override or sign-off reference.
3. Optional backend absence → `missing` or `blocked`, not fabricated results.
4. Templates and protocols must only use these seven labels for evidence badges.
