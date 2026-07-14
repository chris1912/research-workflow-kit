# Contributing

Codex annotation: Created by Codex on 2026-07-15.

Keep changes focused on the workflow contract, skills, adapters, or docs. Do
not modify vendored third-party source in place. Add or update provenance
records when copying or adapting a skill, rule, or code fragment.

Run:

```powershell
python -m compileall src tests
python -m pytest
python scripts/verify_publish_tree.py
```

Contributions must preserve citation safety, uncertainty labels, and explicit
boundaries between evidence, inference, and writing style.

