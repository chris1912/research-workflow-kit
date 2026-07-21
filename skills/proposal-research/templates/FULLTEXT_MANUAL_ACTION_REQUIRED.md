# 全文人工处理队列 / Full-Text Manual Action Required

Grok annotation: Template created by Grok on 2026-07-20. Never describe or request paywall bypass.

## Purpose / 用途

Queue every priority paper whose lawful open-access or institutional acquisition failed. The research run continues with metadata-level evidence for queued items; do not invent full-text extracts.

## Queue / 队列

| Queue ID | Merged ID | Title | DOI / URL | Failure reason | Lawful next step | Owner | Due | Status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Q001 |  |  |  | paywalled \| not_found \| network \| rights_unclear \| parse_failed | library request \| author manuscript request \| substitute paper \| proceed metadata-only | human |  | open \| done \| dropped |

## Rules / 规则

1. Log the failed attempt in `fulltext_acquisition.csv` before opening a queue row.
2. Prefer substituting an equally relevant OA paper when the claim can still be supported.
3. If the claim depends on inaccessible full text, mark the related evidence card as `uncertainty`.
4. Keep all stored paths local to the user run directory; never commit PDFs or private downloads to the public repository.
5. Forbidden: piracy sites, credential sharing, or any paywall circumvention language.

## Closure checklist / 关闭检查

- [ ] Every priority paper is either deep-read, substituted, or explicitly metadata-only.
- [ ] Downstream draft sections cite only evidence states that match access reality.
- [ ] HTML delivery pages surface manual-queue items that remain open.
