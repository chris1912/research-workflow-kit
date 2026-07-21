## Summary / 摘要

<!-- What changed and why? / 变更内容与原因 -->

## Scope check / 范围检查

- [ ] Change stays within first-party contracts, skills, adapters, tests, or docs.
      / 变更限于一级契约、技能、适配器、测试或文档。
- [ ] No new required backend, credential, or paywall-bypass instruction.
      / 未新增必需后端、凭据或付费墙绕过说明。
- [ ] Dual-route / merged-core / priority full-text / HTML gate policy preserved when touched.
      / 若触及相关路径，已保持双路线、合并核心、优先全文与 HTML 门禁策略。

## Validation / 验证

- [ ] `python -m pytest`
- [ ] `python -m compileall -q src tests scripts`
- [ ] `python scripts/verify_publish_tree.py`
- [ ] `git diff --check` (when Git is available)
- [ ] Documentation links and HTML local links checked when docs or HTML changed
      / 文档或 HTML 变更时已检查链接与本地相对链接

## Provenance and safety / 出处与安全

- [ ] Third-party sources and licenses recorded in `docs/THIRD_PARTY_MANIFEST.json` when needed.
      / 如有需要，已在 `docs/THIRD_PARTY_MANIFEST.json` 记录第三方来源与许可。
- [ ] No credentials, private manuscripts, personal/health data, unpublished results, binaries, or runtime environments included.
      / 未包含凭据、未发表手稿、个人/健康数据、未公开结果、二进制或运行时环境。
- [ ] Scientific claims and citations remain subject to human review.
      / 科学主张与引文仍须人工审阅。
