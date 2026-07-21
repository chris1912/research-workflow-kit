<!--
essential_core_lineage:
  file: core/contracts/generator_evaluator.md
  implementation: first-party-rewrite
  upstream_concepts:
    - generator evaluator separation
    - rebuttal audit
    - claim intent
    - revision safety
    - protected hedges
  upstream_path_hints:
    - skills/research-methods/ars/.../firm_rules
    - revision/rebuttal protocols
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Generator / Evaluator Separation Contract

Grok annotation: Essential Core contract by Grok on 2026-07-20 (E1).
Grok annotation: E3-B revision/rebuttal/coach hardening by Grok on 2026-07-20.

## Roles

| Class | Examples | Obligations |
| --- | --- | --- |
| Generators | draft_writer, argument builder, revision drafting | Emit claim-intent pre-commit before prose; no self-score as final peer review; ledger protected-claim changes |
| Coaches | revision_coach | Roadmap/response skeleton only; no silent full manuscript rewrite |
| Evaluators | peer_reviewer, panel, claim audit, rebuttal-audit | Do not invent supportive citations to “fix” drafts; no generated author response prose as pass |

## Rules

1. Full paper mode plans require writer pre-commit before peer score.
2. `rebuttal-audit` is evaluator-only: coverage/gaps/risk flags; **no** response generation.
3. `revision-coach` may structure reviewer comments into a roadmap but does not
   silently rewrite the manuscript unless user selects `revision` mode.
4. Claim-audit env (`RM_CLAIM_AUDIT` / `ARS_CLAIM_AUDIT`) adds claim-intent gates
   to the plan quality_gates list.
5. `revision` mode must preserve protected claims/hedges unless a change ledger
   row names the delete/replace and author_signoff is true.
6. Silent new DOI/result inserts without new_evidence_gate rows fail closed.
7. False ledger claims (asserted change absent from after-text) fail closed.
8. Recovery checkpoints are required when resuming interrupted revision; restart
   wipe without checkpoint is forbidden.
9. Heuristic strength checks may escalate risk; they never prove semantic
   preservation of rewritten claims.
10. Disclosure AI/funding/COI fields are mandatory and never auto-fabricated;
    human confirmation is required for final packages.

## Behavioral helpers (private, not public gate IDs)

Bound into public gate `generator_evaluator_separation`:

- `evaluate_revision_transition` — before/after + ledger + sign-off + recovery
- `evaluate_rebuttal_consistency` — point_id matrix vs change/evidence pointers

These helpers use structured fixtures. Protocol keyword presence alone is not
sufficient for pass.

## Pre-commit checklist (generators)

- [ ] Claim-intent nodes listed with evidence states
- [ ] No invented results or citations
- [ ] Protected hedges identified when revising
- [ ] Mode matches user request (coach ≠ revision ≠ rebuttal-audit)

## Evaluator-only checklist

- [ ] No generated author rebuttal prose as audit pass
- [ ] Every reviewer point covered or explicitly missing
- [ ] ms_change rows linked to change ledger
- [ ] Tone/overclaim flags recorded without inventing evidence
