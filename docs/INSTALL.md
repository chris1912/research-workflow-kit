# Installation

Codex annotation: Created by Codex on 2026-07-15.

## First-party layer

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[test]"
python -m workflow_lab --help
```

The first-party layer has no mandatory network or model dependency.

## Optional backends

Install only the stages you need, following `docs/DEPENDENCIES.md`. Then copy
`.env.example` to a local environment file outside version control or set the
variables in the shell. The adapters accept executable names or complete
commands through `WORKFLOW_LAB_*_CMD` variables.

## Verification

```powershell
python -m compileall src tests
python -m pytest
python scripts/verify_publish_tree.py
```

