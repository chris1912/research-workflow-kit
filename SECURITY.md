# Security / 安全政策

Grok annotation: Private advisory route and data warnings prepared by Grok on
2026-07-20.
Codex annotation: Created by Codex on 2026-07-15.

## Supported surface / 支持范围

**English.** Security reports apply to the public first-party layer of
`chris1912/research-workflow-kit` on the default branch `main` (adapters, CLI,
skills contracts, templates, and publish-tree checks). Optional third-party
backends remain under their own upstream security processes.

**中文。** 安全报告适用于公开仓库 `chris1912/research-workflow-kit` 默认分支
`main` 上的一级层（适配器、CLI、技能契约、模板与发布树检查）。可选第三方后端遵循其上游安全流程。

## Private reporting / 私下报告

**English.** Report suspected vulnerabilities, credential exposure, or
provenance errors through GitHub Security Advisories for this repository:

https://github.com/chris1912/research-workflow-kit/security/advisories/new

Do not open a public issue or pull request that contains secrets, private
manuscripts, personal or health data, unpublished results, or reproduction steps
that would expose such material.

**中文。** 疑似漏洞、凭据泄露或出处错误，请通过本仓库的 GitHub Security Advisories
私下报告（见上方链接）。请勿在公开议题或拉取请求中包含密钥、未发表手稿、个人或健康数据、
未公开结果，或会暴露上述材料的复现步骤。

## Operational guidance / 操作指引

- Never commit API keys, tokens, cookies, private keys, or `.env` files with
  real values. Use local environment variables only. / 切勿提交真实 API 密钥、令牌、Cookie、私钥或含真实值的 `.env`；仅使用本地环境变量。
- Keep private manuscripts, patient or participant data, and unpublished results
  outside the public tree. / 将未发表手稿、患者或受试者数据与未公开结果置于公开树之外。
- Adapters execute configured local commands without shell expansion; keep
  backend commands trusted and use a dedicated workspace for untrusted
  documents. / 适配器在无 shell 展开的情况下执行已配置的本地命令；后端命令须可信，对不受信任文档使用独立工作区。
- Rotate any credential that may have been exposed before deciding whether
  history cleanup is required. / 对可能已暴露的凭据先轮换，再决定是否需要历史清理。

## GitHub-side protection / GitHub 侧防护

Maintainers should enable GitHub Secret Protection and push protection when
available for this repository. Local audits do not replace GitHub-side
protection. Avoid broad secret-scanning path exclusions.

维护者应在可用时为本仓库启用 GitHub Secret Protection 与 push protection。
本地审核不能替代 GitHub 侧防护。避免宽泛的密钥扫描路径排除。
