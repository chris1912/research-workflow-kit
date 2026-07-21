# HTML 交付检查清单 / HTML Delivery Checklist

Grok annotation: Template created by Grok on 2026-07-20. Markdown and structured artifacts remain authoritative; HTML is the human-readable delivery view.

## When required / 何时必需

Required for **conclusion-bearing** runs that present recommendations, ranked directions, claim-ready synthesis, or submission-facing conclusions. Optional for pure intermediate exploration.

## Required pages / 必需页面

| # | Page role | Suggested filename in user run | Source of truth | Ready? |
| ---: | --- | --- | --- | --- |
| 1 | Entry / navigation page | `index.html` or `START_HERE_RUN.html` | this checklist + run summary |  |
| 2–N | Decision-critical pages (total 3–8 including entry) | e.g. `core_papers_page.html`, `priority_papers_page.html`, claim/risk pages | Markdown/CSV/JSONL artifacts |  |

Minimum decision-critical coverage usually includes:

1. Entry page with route, evidence boundary, and navigation
2. Merged core papers page
3. Priority / full-text status page
4. Optional: risks, claim verification, or direction comparison pages as needed

## Entry-page requirements / 入口页要求

- [ ] UTF-8 encoding declared; no `U+FFFD` replacement characters
- [ ] Visible evidence-boundary statement (claim / extract / inference / uncertainty)
- [ ] Repository- or run-relative links only; no private absolute machine paths in published copies
- [ ] Navigation to every decision-critical page
- [ ] Responsive layout usable on narrow screens
- [ ] Print-friendly styles (or acceptable browser print behavior)
- [ ] States whether secondary discovery ran or fell back to primary-only
- [ ] Links back to authoritative Markdown/structured files where practical

## Local link check / 本地链接检查

| Link text | Target | Exists? | Notes |
| --- | --- | --- | --- |
|  |  | yes \| no |  |

## Content safety / 内容安全

- [ ] No credentials, private run paths, or personal contact data
- [ ] No paywall-bypass instructions
- [ ] Unverified claims marked as uncertainty
- [ ] HTML does not silently override Markdown authority

## Sign-off / 签收

| Role | Name | Date | Result |
| --- | --- | --- | --- |
| Producer |  |  | ready \| blocked |
| Human reviewer |  |  | accepted \| needs fixes |
