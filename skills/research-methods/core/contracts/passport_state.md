<!--
essential_core_lineage:
  file: core/contracts/passport_state.md
  implementation: first-party-rewrite
  upstream_concepts:
    - pipeline state machine
    - passport reset boundary
    - checkpoints
  upstream_path_hints:
    - skills/research-methods/ars/.../pipeline_state_machine.md
    - skills/research-methods/ars/.../passport_as_reset_boundary.md
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Passport / State Contract

Grok annotation: Essential Core contract by Grok on 2026-07-20 (E1).

## Schema

- `schema_id`: `essential_passport_v1` only
- Unknown or missing schema → refuse load/resume; exit **3**; never silent convert

## Stage and global states

Stage states: `pending | in_progress | completed | skipped | blocked`
Global states: `initializing | running | awaiting_confirmation | paused | completed | aborted`

## Legal stages

| Stage ID | Name | Mandatory gates before completed |
| --- | --- | --- |
| `1` | RESEARCH | RQ brief; evidence separation |
| `2` | WRITE | generator pre-commit; claim intent if claim-audit on |
| `2.5` | INTEGRITY | citation/claim/temporal checklist; PASS/MINOR |
| `3` | REVIEW | independent reviewers before synthesis |
| `3p` | RE-REVIEW | residual issues + score trajectory |
| `4` | REVISE | revision roadmap |
| `4p` | REVISE (iter) | roadmap + iteration counter |
| `4.5` | FINAL INTEGRITY | zero blocking issues |
| `5` | FINALIZE | format/disclosure/checklist |
| `FULL` | checkpoint boundary | required stages completed or human-skipped |

## Transition table (legal edges)

| From | Allowed to | Condition |
| --- | --- | --- |
| null | 1 | passport create |
| 1 | 2 | stage 1 completed |
| 2 | 2.5 | stage 2 completed |
| 2.5 | 3 | integrity PASS or MINOR |
| 2.5 | 2 | integrity MATERIAL or AUDIT_FAILED |
| 3 | 4 | independents complete + synthesis done |
| 3 | 3p | re-review requested |
| 3p | 4 | residual checklist recorded |
| 4 / 4p | 4.5 | revision roadmap present |
| 4 / 4p | 3p | major revision loop |
| 4.5 | 5 | final integrity PASS |
| 4.5 | 4 | final integrity fail |
| 5 | FULL | finalize checklist complete |

Illegal examples: `3→5`, `2.5 FAIL→3`, `1→3`.

## Validator contract

```text
validate_transition(passport, from_stage, to_stage, env) ->
  { ok, error, checkpoint_hash_expected }
```

Rules:

1. Unknown schema → refuse.
2. Edge must be in table + conditions.
3. Resume requires matching checkpoint hash.
4. Reset requires `RM_PASSPORT_RESET=1` or `ARS_PASSPORT_RESET=1` and append-only ledger.
5. Skipping mandatory gates requires human override record.

## Checkpoint hash

```text
checkpoint_hash = sha256(
  passport_id | stage_id | global_state | sorted(artifact_paths) |
  integrity_summary | updated_at_iso
) hex digest
```

## Reset ledger (append-only)

Required fields: `reset_id`, `timestamp`, `from_stage`, `to_stage`,
`from_checkpoint_hash`, `reason`, `actor` (`human|agent`), `env_flags_observed`.
Never delete or mutate prior ledger rows.

### Transition validator

```text
validate_reset_ledger_transition(previous_ledger, new_ledger) ->
  { ok, error, message }
```

Rules (non-mutating on either input):

1. Both arguments must be lists.
2. Accept **exactly one** new entry appended after an unchanged historical prefix.
3. Reject deletion (`reset_ledger_delete`), reordering (`reset_ledger_reorder`),
   mutation of prior rows (`reset_ledger_mutation`), and multi-append
   (`reset_ledger_multi_append`).
4. Reject missing required fields (`invalid_reset_entry`) and invalid actors
   (`invalid_reset_actor`).
5. Full pipeline stage-machine depth remains **partial** until E4; this validator
   covers the append-only ledger transition contract only.

## Material passport minimum fields

`schema_id`, `passport_id`, `created_at`, `updated_at`, `stage`, `global_state`,
`artifacts[]`, `claims[]`/`extracts[]`, `integrity_verdicts[]`,
`checkpoints[]`/`last_checkpoint`, `reset_ledger[]`, `human_overrides[]`,
`degradations[]`.
