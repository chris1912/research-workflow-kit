---
name: scientific-workflow-lab-lite
description: Use whenever a user asks about Research Workflow Kit Lite, the lightweight scientific workflow, research-question refinement, literature discovery, proposal research, systematic review planning, manuscript review, evidence-backed academic writing, or is unsure which public-kit skill to use. This project-level router selects the lite kit's specialist skills, preserves evidence boundaries, and requires readable HTML delivery for conclusion-bearing work.
---

# Scientific Workflow Lab — Public Lite Router

Codex annotation: Project-level public router added by Codex on 2026-07-22.

This is the callable entry point for the lightweight `research-workflow-kit`.
It routes the seven specialist skills in this repository; it is not a copy of
the private/full `scientific-workflow-lab` and does not install the full
Academic Research Skills suite.
If both the full lab and this kit are loaded, use the repository-local contract
for tasks explicitly scoped to this public kit.

## First action

1. Read [`SCIENTIFIC_WORKFLOW_START_HERE.html`](../../SCIENTIFIC_WORKFLOW_START_HERE.html).
2. Read [`docs/START_HERE.html`](../../docs/START_HERE.html) when the task has
   more than one stage or the correct specialist is unclear.
3. Tell the user the selected stage, specialist skill, required and optional
   steps, evidence boundary, expected artifacts, and the next human-confirmation
   point before doing substantial work.

When a host supports project-local skills, invoke this router as
`$scientific-workflow-lab-lite`. If the host does not discover repository skills,
open this file explicitly or use the equivalent specialist contract under
`skills/`.

## Route by task

| User need | Start with | Then hand off to |
| --- | --- | --- |
| Unsure where to begin or task spans stages | this router | `workflow-router` |
| Grant, proposal, or research-direction deep research | `proposal-research` | `research-methods` for methods/integrity gates; writing stack for drafting |
| Existing proposal or manuscript needs controlled revision | `proposal-iteration` | `academic-editing` → `prose-lint` |
| Research-question refinement, systematic review, integrity, peer review | `research-methods` | `proposal-research` for proposal literature/HTML work |
| Long-form paper, thesis, or review structure and drafting | `longform-writing` | `academic-editing` → `prose-lint` |
| Existing text, terminology, translation, or reviewer response | `academic-editing` | `prose-lint` when a human-facing draft is ready |
| Deterministic style review | `prose-lint` | Human review; lint is not evidence validation |

Use the contracts at:

- [`skills/workflow-router/SKILL.md`](../workflow-router/SKILL.md)
- [`skills/proposal-research/SKILL.md`](../proposal-research/SKILL.md)
- [`skills/proposal-iteration/SKILL.md`](../proposal-iteration/SKILL.md)
- [`skills/research-methods/SKILL.md`](../research-methods/SKILL.md)
- [`skills/longform-writing/SKILL.md`](../longform-writing/SKILL.md)
- [`skills/academic-editing/SKILL.md`](../academic-editing/SKILL.md)
- [`skills/prose-lint/SKILL.md`](../prose-lint/SKILL.md)

## Default research route

For a new proposal or research direction, use this order unless the user
explicitly narrows the task:

1. Define the question, scope, population/intervention or exposure/comparator/
   outcome, constraints, and desired deliverable.
2. Write a search strategy and complete the primary literature route.
3. Treat a secondary provider (including Grok) as optional independent coverage;
   never block the primary route when it is unavailable.
4. Normalize and re-screen the union; after convergence, use only
   `MERGED_CORE_PAPERS.md` downstream.
5. Select 3–8 priority papers, attempt lawful OA-first full-text retrieval, log
   attempts, deep-read readable text, and open a manual queue on failure.
6. Build evidence cards, claim checks, risks/counterevidence, and synthesis.
7. Draft with `longform-writing`, refine with `academic-editing`, and run
   `prose-lint` when available.
8. For conclusion-bearing work, complete the HTML delivery gate and obtain
   human confirmation before treating claims or design decisions as final.

## Evidence and integrity boundary

Use explicit states such as `claim`, `extract`, `inference`, `uncertainty`,
`missing`, `blocked`, and `human-confirmed`. Never invent papers, DOIs,
quotations, data, statistics, experiments, reviewer identities, or citation
support. Metadata or an abstract cannot be presented as full-text method or
performance evidence. Keep Markdown/JSON/CSV as the authoritative source;
HTML is the readable navigation and delivery layer.

`skills/research-methods` is first-party `essential_core`: E2 research-question,
deep-research, and systematic-review depth plus E3 paper/integrity/review depth
are `parity: partial`; E4 pipeline/experiment/optional-runtime bodies are
`parity: not_started`. Partial depth is not full ARS behavioral parity, real
multi-process orchestration, or editorial authority. The upstream suite is
optional external material and must not be silently installed or advertised as
bundled.

## Optional backends and fallback

Adapters are configured through the environment variables documented in
[`docs/DEPENDENCIES.md`](../../docs/DEPENDENCIES.md). Missing discovery,
document parsing, evidence QA, literature-map, synthesis, Vale, network,
authentication, model, or quota dependencies must produce an explicit
`missing`/`blocked`/fallback record, never a silent substitution. Keep personal
research runs, credentials, caches, virtual environments, and generated binary
files outside the tracked repository.

For methods-only offline checks, the opt-in commands are:

```powershell
python skills/research-methods/runtime/scripts/essential_full_runtime.py plan --text "..." --json
python skills/research-methods/runtime/scripts/essential_quality_gates.py list --json
```

## Conclusion delivery gate

When the run reaches a conclusion, proposal reference draft, research-direction
decision, systematic-review conclusion, or comparable final result, deliver:

- one UTF-8 HTML entry page;
- 3–8 decision-critical standalone pages with responsive/print navigation;
- visible evidence-boundary and remaining-risk text;
- links to authoritative Markdown/structured artifacts and working local-link
  checks;
- `html/core_papers.html` and `html/priority_papers_deep_read.html` when those
  stages were performed.

Do not apply this gate to an intermediate search, single-paper read, corpus
parse, or paragraph-level edit unless the user asks for HTML. If the user
explicitly requests machine-only output, follow that request and record the
exception.

## User-facing output habit

Every phase summary should state: selected route and specialist, tools/backends
used, evidence boundary, artifacts created, checks run, unresolved risks, and
the next human decision. Link the project manual as
[`docs/START_HERE.html`](../../docs/START_HERE.html).

### Copy-ready requests

```text
请使用 $scientific-workflow-lab-lite。我的目标是：[目标]，已有材料：[路径或粘贴内容]。先读取项目手册，判断阶段并选择 specialist skill，列出必做/可选步骤、证据边界和预计产物；不要直接编造结论。

请使用 $scientific-workflow-lab-lite 路由一个开题深研任务：[指南/主题]。先完成 primary route；次路线只有在能独立审计时才启用；收敛后以 MERGED_CORE_PAPERS.md 为下游唯一权威。

请使用 $scientific-workflow-lab-lite 处理现有论文草稿：[文件]。先判断是 research-methods、proposal-iteration、longform-writing 还是 academic-editing，并在修改前给出诊断与人工确认点。
```
