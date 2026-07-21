# Contributing / 贡献指南

Grok annotation: Bilingual contributing guide prepared by Grok on 2026-07-20.
Codex annotation: Created by Codex on 2026-07-15.

## Scope / 范围

**English.** Keep changes focused on the workflow contract, first-party skills,
adapters, tests, or public documentation. Do not modify vendored third-party
source in place. When copying or adapting a skill, rule, or fragment, update
provenance records under `docs/`.

**中文。** 变更应聚焦工作流契约、一级技能、适配器、测试或公开文档。勿就地修改
第三方源码。复制或改编技能、规则或片段时，须更新 `docs/` 下的出处记录。

## Project policy / 项目策略

- Preserve citation safety, uncertainty labels, and clear boundaries among
  evidence, inference, and style. / 保持引文安全、不确定标注，以及证据、推断与文风的清晰边界。
- Do not add required backends, credentials, personal research artifacts, or
  paywall-bypass instructions. / 勿添加必需后端、凭据、个人研究产物或付费墙绕过说明。
- After dual-route convergence, keep `MERGED_CORE_PAPERS.md` as the sole
  downstream authority. / 双路线收敛后保持 `MERGED_CORE_PAPERS.md` 为唯一下游权威。
- Route systematic-review, integrity, and peer-review protocol work through
  `skills/research-methods` (thin offline router). / 系统综述、完整性与同行评议协议任务走轻量离线路由 `skills/research-methods`。
- Prefer repository-relative links in tracked files. / 受控文件优先使用仓库相对链接。

## Local checks / 本地检查

```powershell
python -m compileall -q src tests scripts
python -m pytest
python scripts/verify_publish_tree.py
git diff --check
```

## Pull requests / 拉取请求

Use the repository PR template. Summarize the contract impact, list the checks
you ran, and confirm that no credentials, private manuscripts, personal/health
data, or unpublished results are included.

请使用仓库 PR 模板：说明契约影响、列出已运行检查，并确认未包含凭据、未发表手稿、
个人/健康数据或未公开结果。

## Issues / 议题

Use the issue templates. For security concerns, follow [`SECURITY.md`](SECURITY.md)
and do not open a public issue with sensitive material.

使用议题模板。安全问题请遵循 [`SECURITY.md`](SECURITY.md)，勿在公开议题中粘贴敏感材料。
