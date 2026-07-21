<!--
essential_core_lineage:
  file: core/templates/argument_map.md
  implementation: first-party-rewrite
  upstream_concepts:
    - argument map
    - claim intent pre-commit
  upstream_path_hints:
    - ars argument builder
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Argument Map

Grok annotation: Essential Core E3-B argument map depth by Grok on 2026-07-20.

**parity: partial** — Supports plan, outline-only, and full paper modes for
claim-intent pre-commit. Not a substitute for citation integrity or revision
ledgers. Do not invent supportive nodes.

## Purpose

Capture atomic claims, extracts, and inferences with dependencies and support
status before (or while) drafting. Generators emit claim-intent here as
pre-commit; evaluators do not invent missing support.

### claim_intent_nodes

List each atomic claim node with a stable node_id, claim text, intended
evidence state (claim/extract/inference/uncertainty/missing/blocked/
human-confirmed), and whether the node is conclusion-bearing. Claim-intent is
required before full-mode prose for high-stakes results.

| node_id | claim_text | node_type | evidence_state | conclusion_bearing |
| --- | --- | --- | --- | --- |
|  |  | claim / extract / inference |  | yes/no |

### support_status_slots

For each claim node, record support_status
(supported/partial/contradicted/unsupported/unknown), linked citation ids or
evidence pointers, and locator needs. Unknown stays unknown offline; do not
promote to supported without extract or human confirmation.

| node_id | support_status | evidence_pointers | locator_needed |
| --- | --- | --- | --- |
|  |  |  | yes/no |

### dependency_edges

Record depends-on edges between nodes so outline and full modes can order
sections without smuggling unsupported conclusions upstream. Cycles and missing
dependencies are risks, not silent fixes.

| from_node | to_node | dependency_kind | notes |
| --- | --- | --- | --- |
|  |  | premise / definition / method |  |

### counterpoint_slots

Capture counterpoints, alternative explanations, and boundary conditions for
high-stakes claims. Empty counterpoint slots on conclusion-bearing causal
claims should be flagged for human review rather than filled with invented
objections.

| node_id | counterpoint | disposition | notes |
| --- | --- | --- | --- |
|  |  | open / addressed / waived |  |

## Node table (working surface)

| Node | Type (claim/extract/inference) | Depends on | Support status | Counterpoints |
| --- | --- | --- | --- | --- |
|  |  |  |  |  |

## Human gates

- [ ] Claim-intent pre-commit complete for full mode
- [ ] No invented evidence pointers
- [ ] Conclusion-bearing nodes have honest support_status
- [ ] Counterpoints reviewed for high-stakes claims
