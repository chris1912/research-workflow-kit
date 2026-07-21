# 合并核心文献 / Merged Core Papers

Grok annotation: Template created by Grok on 2026-07-20 for the public research-workflow-kit contract upgrade.

## Authority / 权威说明

**This file is the sole downstream authority after literature convergence.**
收敛完成后，本文件是下游唯一权威文献清单。写作、深读、优先全文、证据卡和 HTML 交付均应引用本表，而不是各自路由的临时核心表。

`core_papers.md` remains a pre-merge or single-route compatibility template. After merge or primary-only finalization, copy or regenerate the authoritative rows here and state the transition in the route-status artifact.

## Route outcome / 路由结果

| Field | Value |
| --- | --- |
| selected_mode | primary_only \| primary_secondary_parallel \| primary_only_after_secondary_failure |
| secondary_provider | null \| grok \| other |
| merge_completed | yes \| no |
| fallback_reason |  |
| primary_core_count |  |
| secondary_core_count |  |
| union_before_rescreen |  |
| merged_core_count |  |

## Convergence protocol / 收敛协议

1. Keep primary and optional secondary discovery **blind and independent** until both pools are frozen.
2. Normalize DOI, title, year, and venue before comparison.
3. Deduplicate the union; record omissions unique to each route.
4. Re-screen the union with explicit inclusion criteria.
5. Write the final rows in this file only after re-screening.

## Merged core table / 合并核心表

| ID | Title | Year | DOI / URL | Venue | Provenance | Evidence level | Why core | Supports claim/section | Counterevidence value | Full-text status | Priority? |
| --- | ---: | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| M001 |  |  |  |  | both \| primary_only \| secondary_only | claim \| extract \| inference \| uncertainty |  |  |  | not_attempted \| oa_acquired \| paywalled_manual \| unavailable | yes \| no |

Provenance values:

- `both`: found by primary and secondary routes
- `primary_only`: only primary route retained after re-screen
- `secondary_only`: only secondary route retained after re-screen

Evidence-level badges must not be implied by prose alone:

- `claim`: source-backed assertion ready for careful use
- `extract`: direct quotation or tightly bound paraphrase
- `inference`: reasoned interpretation beyond the extract
- `uncertainty`: unresolved conflict, missing access, or weak support

## Grouping / 文献分组

| Group | Representative IDs | Main point | Proposal use |
| --- | --- | --- | --- |
| Field importance |  |  |  |
| State of the art |  |  |  |
| Methods |  |  |  |
| Bottlenecks |  |  |  |
| Recent trends |  |  |  |
| Counterevidence and risk |  |  |  |

## Omission comparison / 遗漏对照

| Paper or topic | Present in | Missing from | Action after re-screen |
| --- | --- | --- | --- |
|  | primary \| secondary \| neither |  | keep \| drop \| queue full text |

## Downstream handoff / 下游交接

- Priority selection (3–8): `priority_papers.md`
- Acquisition log: `fulltext_acquisition.csv`
- Manual queue: `FULLTEXT_MANUAL_ACTION_REQUIRED.md`
- Deep-read reports: one `deep_read_report.md` copy per readable priority paper
- HTML shells: `core_papers_page.html` (filled from this file)
