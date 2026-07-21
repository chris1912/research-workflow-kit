# Essential Core Hooks

Grok annotation: Essential Core hooks README by Grok on 2026-07-20 (E1).

## Behavior

Hooks are **read-only announce wrappers**. They call
`runtime/scripts/essential_hook.py announce` and emit a small JSON status.

## Hard boundaries

| Boundary | Rule |
| --- | --- |
| Network | No network I/O |
| Secrets | Do not echo environment secrets, tokens, or API keys |
| Mutation | Do not write files, git state, or process state |
| Dependencies | Python standard library only |

## Enabling

Host may set `RM_HOOKS=1` or `ARS_CODEX_HOOKS=1` to opt into calling hooks.
The wrapper remains read-only whether or not the flag is set.

## Failure modes

Malformed stdin JSON → exit code 2 with `ok: false`.
