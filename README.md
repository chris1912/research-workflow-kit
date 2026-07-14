# Research Workflow Kit

Codex annotation: Created by Codex on 2026-07-15.

[![Quality](https://github.com/chris1912/research-workflow-kit/actions/workflows/quality.yml/badge.svg)](https://github.com/chris1912/research-workflow-kit/actions/workflows/quality.yml)

Research Workflow Kit is a small, provenance-aware orchestration layer for a
research workflow that moves from a research question to evidence-backed
writing and final style checks.

## Start here

Open [`docs/START_HERE.html`](docs/START_HERE.html) for the visual route guide.
The architecture map is [`docs/ARCHITECTURE_ROADMAP.html`](docs/ARCHITECTURE_ROADMAP.html).

The default route is:

```text
question -> discovery -> parsing -> evidence QA -> literature map
-> synthesis -> long-form draft -> academic edit -> prose lint -> package
```

## What is included

- `src/workflow_lab/`: first-party adapters and the dependency-free CLI.
- `skills/`: neutral-named router, proposal, research-method, writing, editing,
  and prose-lint skills.
- `src/workflow_lab/config/vale/`: project-specific Vale rules and profiles.
- `docs/`: installation, workflow, architecture, provenance, and license notes.
- `examples/`: only sanitized, dependency-free examples.

Large research engines and their virtual environments are intentionally not
vendored. Install them separately using [`docs/DEPENDENCIES.md`](docs/DEPENDENCIES.md)
and configure command paths through environment variables.

## Install the first-party layer

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[test]"
python -m workflow_lab --help
python -m pytest
```

## Provenance and licenses

The first-party layer is MIT licensed. Selected skills and rules remain under
their original licenses, and all source commits are recorded in
[`docs/THIRD_PARTY_MANIFEST.json`](docs/THIRD_PARTY_MANIFEST.json) and
[`docs/THIRD_PARTY_NOTICES.md`](docs/THIRD_PARTY_NOTICES.md).

The kit does not provide scientific evidence, guarantee citation correctness,
or replace expert review. External APIs, models, and document parsers can
require credentials, network access, or additional license review.
