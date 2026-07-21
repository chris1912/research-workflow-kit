# Research Workflow Kit / 研究工作流工具包

Grok annotation: Bilingual public README prepared by Grok on 2026-07-20 for
pre-publish review (Stage A+B/D lightweight kit).
Codex annotation: Created by Codex on 2026-07-15.

[![Quality](https://github.com/chris1912/research-workflow-kit/actions/workflows/quality.yml/badge.svg)](https://github.com/chris1912/research-workflow-kit/actions/workflows/quality.yml)

## Summary / 摘要

**English.** Research Workflow Kit is a small, provenance-aware orchestration
layer that routes a research question through literature discovery, evidence
handling, long-form drafting, academic editing, and prose checks. The published
tree stays compact after Essential Core packaging (about 210 existing
publish-candidate files; keep under 220 without written justification). The
methods pack is fixed at 65 files for this stage (soft ceiling 100). Optional
backends are never required.

**中文。** Research Workflow Kit 是一套轻量、可追溯的研究编排层：从研究问题出发，
经文献发现、证据处理、长文起草、学术润色与文风检查完成路由。Essential Core 打包后
公开树体约 210 个现有发布候选文件（无书面说明时保持 &lt;220）；方法包本阶段精确 65
文件（软上限 100）。可选后端均非必需依赖。

## Start here / 入口

- Lightweight project entry / 轻量项目入口: [`SCIENTIFIC_WORKFLOW_START_HERE.html`](SCIENTIFIC_WORKFLOW_START_HERE.html)
- Detailed teaching manual / 详细教学手册: [`docs/START_HERE.html`](docs/START_HERE.html)
- Architecture map / 架构图: [`docs/ARCHITECTURE_ROADMAP.html`](docs/ARCHITECTURE_ROADMAP.html)

Default route / 默认路径:

```text
question -> search strategy -> optional dual-route preflight
-> primary discovery (+ optional blind secondary)
-> MERGED_CORE_PAPERS -> priority OA-first full text
-> parsing -> evidence QA -> literature map
-> synthesis -> long-form draft -> academic edit -> prose lint
-> HTML delivery (conclusion-bearing) -> package
```

## Features / 功能

**English**

- Neutral public skills for routing, proposal deep research, methods entry,
  long-form writing, academic editing, and prose lint.
- Project-level `$scientific-workflow-lab-lite` router with an explicit specialist
  hand-off contract; hosts that support project-local skills may invoke it
  directly.
- Explicit evidence states: claim / extract / inference / uncertainty.
- Optional dual-route literature discovery with provider-neutral `secondary_*`
  fields; primary route completes when secondary is unset.
- `MERGED_CORE_PAPERS.md` as the sole post-convergence authority;
  `core_papers.md` remains a pre-merge or single-route compatibility template.
- Priority 3–8 lawful OA-first full-text contracts, acquisition log, deep-read
  report, and manual-action queue (no paywall bypass).
- Final HTML delivery checklist and page shells for conclusion-bearing runs;
  Markdown and structured artifacts remain authoritative.
- First-party `skills/research-methods` Essential Core (`essential_core`) with
  contracts, templates, and opt-in offline runtime; E2–E3 protocol depth is
  `parity: partial` (RQ/deep/SR + paper/integrity/review); E4 pipeline/experiment
  remains `parity: not_started`. Partial depth is not full ARS parity. Full
  Academic Research Skills suite is optional external.
- Dependency-free first-party CLI and adapters that fail explicitly when optional
  backends are missing.

**中文**

- 中立公开技能：路由、开题深研、方法入口、长文写作、学术编辑、文风检查。
- 项目级 `$scientific-workflow-lab-lite` 总路由：先判断阶段，再交给对应专业技能；支持项目级技能的宿主可直接调用，不影响完整版 `scientific-workflow-lab`。
- 明确证据状态：主张 / 摘录 / 推断 / 不确定。
- 可选双路线文献发现（提供商中立的 `secondary_*` 字段）；次路线未配置时主路线仍可完成。
- 收敛后以 `MERGED_CORE_PAPERS.md` 为唯一下游权威；`core_papers.md` 仅作合并前或单路线兼容模板。
- 优先 3–8 篇合法 OA 优先全文契约、获取日志、深读报告与人工队列（不描述付费墙绕过）。
- 结论性交付的 HTML 清单与页面壳；Markdown / 结构化产物仍为权威源。
- 一级 `skills/research-methods` Essential Core（`essential_core`）含合约、模板与可选离线 runtime；E2–E3 协议深度为 `parity: partial`（研究问题/深研/系统评价 + 论文/完整性/评审）；E4 管线/实验仍为 `parity: not_started`；部分深度不等于完整 ARS 对等；完整 Academic Research Skills 套件为可选外部材料。
- 无强制依赖的一级 CLI 与适配器；可选后端缺失时显式失败。

## Requirements / 环境要求

**English**

- Python 3.10 or newer.
- Optional local backends (discovery, document parse, evidence QA, literature
  map, research synthesis, prose lint) configured only via environment variables.
- No cloud API, model, or third-party research engine is required to install or
  exercise the first-party layer.

**中文**

- Python 3.10 或更高版本。
- 可选本地后端（发现、文档解析、证据问答、文献图谱、研究综合、文风检查）仅通过环境变量配置。
- 安装与运行一级层时，不要求云 API、模型或第三方研究引擎。

## Installation / 安装

**English.** Create a virtual environment, install the editable package with test
extras, and confirm the CLI. Large engines are not vendored; install them
separately if needed (see [`docs/DEPENDENCIES.md`](docs/DEPENDENCIES.md)).

**中文。** 创建虚拟环境，以可编辑方式安装包（含测试可选依赖），并确认 CLI。
大型引擎不内嵌；需要时另行安装（见 [`docs/DEPENDENCIES.md`](docs/DEPENDENCIES.md)）。

```powershell
python -m venv .venv
.\.venv\Scripts\python -m pip install -e ".[test]"
python -m workflow_lab --help
```

## Usage / 使用

**English**

1. Open [`SCIENTIFIC_WORKFLOW_START_HERE.html`](SCIENTIFIC_WORKFLOW_START_HERE.html) before routing a task; use [`docs/START_HERE.html`](docs/START_HERE.html) for the detailed teaching manual (skills, prompts, artifacts, gates).
2. Invoke `$scientific-workflow-lab-lite` when the stage is unclear, then follow the
   selected specialist contract under `skills/` for proposal research, methods,
   long-form writing, academic editing, or prose lint.
3. Record optional secondary discovery fallbacks in `literature_route_status.json`.
4. After dual-route convergence, treat `MERGED_CORE_PAPERS.md` as the sole
   downstream authority.
5. For priority full text, select 3–8 papers, attempt lawful OA-first acquisition,
   deep-read readable text, and open the manual queue on failure.
6. For conclusion-bearing runs, complete the HTML delivery checklist.

**中文**

1. 路由任务前先打开 [`SCIENTIFIC_WORKFLOW_START_HERE.html`](SCIENTIFIC_WORKFLOW_START_HERE.html)，需要细节时再打开 [`docs/START_HERE.html`](docs/START_HERE.html) 详细教学手册（技能、示例请求、产物与门禁）。
2. 阶段不明时调用 `$scientific-workflow-lab-lite` 总路由，再按它选择的 `skills/` 专业契约执行开题研究、方法入口、长文写作、学术编辑与文风检查；它与完整版 `scientific-workflow-lab` 分开。
3. 将可选次路线回退原因记入 `literature_route_status.json`。
4. 双路线收敛后，以 `MERGED_CORE_PAPERS.md` 为唯一下游权威。
5. 优先全文：选 3–8 篇，合法 OA 优先获取，可读文本深读，失败则进入人工队列。
6. 结论性运行须完成 HTML 交付清单。

Minimal CLI smoke check / 最小 CLI 冒烟检查:

```powershell
python -m workflow_lab --help
```

## Verification / 验证

**English.** Run the first-party tests and publish-tree scan before claiming a
change is ready. CI runs the same checks via `.github/workflows/quality.yml`.

**中文。** 在声称变更就绪前运行一级测试与发布树扫描。CI 通过
`.github/workflows/quality.yml` 执行相同检查。

```powershell
python -m compileall -q src tests scripts
python -m pytest
python scripts/verify_publish_tree.py
```

## Limitations / 限制

**English**

- This kit does not supply scientific evidence, guarantee citation correctness,
  or replace expert review.
- Optional secondary discovery, parsers, and models may need credentials,
  network access, or separate license review.
- The Essential Core methods pack does not bundle the full Academic Research Skills suite;
  install that suite outside this repository under upstream terms if required.
- Generated Word/PDF outputs, virtual environments, and personal research runs
  are intentionally excluded from the public tree.

**中文**

- 本工具包不提供科学证据，不保证引文正确，也不能替代专家审阅。
- 可选次路线发现、解析器与模型可能需要凭据、网络或单独许可审查。
- Essential Core 方法核心包不内嵌完整 Academic Research Skills 套件；如需请在本仓库外按上游条款安装。
- 生成的 Word/PDF、虚拟环境与个人研究运行产物有意排除在公开树外。

## Security / 安全

**English.** Never commit API keys, private manuscripts, personal or health data,
unpublished results, or local model caches. Configure credentials only through
the local environment. Report security issues privately through GitHub Security
Advisories for `chris1912/research-workflow-kit` rather than public issues. See
[`SECURITY.md`](SECURITY.md).

**中文。** 切勿提交 API 密钥、未发表手稿、个人或健康数据、未公开结果或本地模型缓存。
凭据仅通过本地环境配置。安全问题请通过 GitHub Security Advisories
（仓库 `chris1912/research-workflow-kit`）私下报告，勿在公开 issue 中披露。
详见 [`SECURITY.md`](SECURITY.md)。

## What is included / 包含内容

- `src/workflow_lab/`: first-party adapters and dependency-free CLI.
- `skills/scientific-workflow-lab-lite/`: project-level lite router and host metadata.
- `skills/`: specialist routers and contracts for proposal, research-methods,
  writing, editing, and prose-lint.
- `skills/proposal-research/templates/`: route status, merged core, priority full
  text, and HTML delivery contracts.
- `src/workflow_lab/config/vale/`: project Vale rules and profiles.
- `docs/`: installation, workflow, architecture, provenance, and license notes.
- `examples/`: sanitized, dependency-free examples only.

`skills/research-methods` is first-party packaging mode `essential_core`
(contracts, mode registry, templates, dual agent surfaces, opt-in runtime).
E2–E3 protocol bodies are operational at `parity: partial` (research question,
deep research, systematic review, academic paper, citation integrity, manuscript
review). E4 bodies (`academic_pipeline`, `experiment`, `optional_runtime`) remain
`parity: not_started`. Partial depth is not full ARS behavioral parity, not real
multi-process orchestration, and not a required external suite. See
[`skills/research-methods/SKILL.md`](skills/research-methods/SKILL.md),
[`skills/research-methods/NOTICE.md`](skills/research-methods/NOTICE.md), and
[`docs/DEPENDENCIES.md`](docs/DEPENDENCIES.md).

## Provenance and licenses / 出处与许可证

The first-party layer is MIT licensed. Selected skills and rules remain under
their original licenses; source commits are recorded in
[`docs/THIRD_PARTY_MANIFEST.json`](docs/THIRD_PARTY_MANIFEST.json) and
[`docs/THIRD_PARTY_NOTICES.md`](docs/THIRD_PARTY_NOTICES.md).

一级层采用 MIT 许可。部分技能与规则保留原许可；来源提交记录见上述出处文件。

## License / 许可证

MIT. See [`LICENSE`](LICENSE).
