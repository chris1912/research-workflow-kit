# 检索策略与关键词扩展表 / Search Strategy

Grok annotation: Updated by Grok on 2026-07-20 for dual-route briefs and converge criteria.
Codex annotation: Template originally created by Codex on 2026-07-06.

## 检索目标 / Objectives

- 当前阶段 / Stage：
- 主候选方向 / Primary direction：
- 需要验证的关键问题 / Key questions：
- 截止日期 / Cutoff date：

## Dual-route brief / 双路由摘要

Optional secondary discovery accelerates coverage only. The primary route must finish when secondary provider, CLI, auth, discovery, model, quota, network, or task is unavailable.

| Field | Value |
| --- | --- |
| primary_route | available |
| secondary_provider | null \| grok \| other |
| planned_mode | primary_only \| primary_secondary_parallel |
| blind_independent_discovery | yes \| no |
| status_artifact | literature_route_status.json |
| merged_authority | MERGED_CORE_PAPERS.md |

## 检索轮次 / Rounds

| 轮次 | 目的 | 工具/来源 | 预期产物 |
| --- | --- | --- | --- |
| 1 | 指南关键词宽检索 | discovery adapter / Web context / research_synthesis adapter | 候选文献池 |
| 2 | 可选第二路由独立宽检索 | independent secondary agent/engine if available | secondary pool only |
| 3 | 候选方向扩展检索 | discovery adapter / literature_map adapter | 方向比较证据 |
| 4 | 归一化、去重、对照遗漏、再筛选 | agent procedure | MERGED_CORE_PAPERS.md |
| 5 | 被选方向反向核验检索 | discovery adapter / evidence_qa adapter | 反证与风险 |

## 关键词扩展 / Keyword expansion

| 类型 | 中文词 | 英文词 | 用途 | 备注 |
| --- | --- | --- | --- | --- |
| 指南原词 |  |  |  |  |
| 同义词 |  |  |  |  |
| 上位概念 |  |  |  |  |
| 邻近方向 |  |  |  |  |
| 跨学科扩展 |  |  |  |  |
| 排除词 |  |  |  |  |

## 推荐查询 / Queries

| 查询编号 | 查询语句 | 来源 | 目标数量 | 备注 |
| --- | --- | --- | ---: | --- |
| Q1 |  |  |  |  |

## 收敛规则 / Convergence criteria

| Gate | Soft target | Hard rule |
| --- | --- | --- |
| Candidate pool (guide-first) | 80–120 | Record actual count; justify shortfalls |
| Candidate pool (clear direction) | 50–80 | Record actual count; justify shortfalls |
| Core papers after re-screen | ≥20 when evidence density allows | Write finals only to MERGED_CORE_PAPERS.md |
| Evidence cards | ≥60 target | Separate claim / extract / inference / uncertainty |
| Priority full text | 3–8 OA-first attempts | Log every attempt; never paywall bypass |

Additional rules:

- 候选文献池目标：
- 核心文献筛选标准：
- 何时扩展关键词：
- 何时停止检索：
- secondary missing → set `selected_mode=primary_only` and continue

## 来源分布检查 / Source coverage

记录不同数据库、期刊/会议、年份、学派、国家/地区或应用场景的覆盖情况。Note primary-only versus dual-route coverage differences after merge.
