<!--
essential_core_lineage:
  file: core/templates/disclosure_statement.md
  implementation: first-party-rewrite
  upstream_concepts:
    - disclosure
    - CRediT
    - AI assistance disclosure
  upstream_path_hints:
    - ars disclosure mode
    - policy anchor disclosure
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Disclosure Statement

Grok annotation: Essential Core E3-B designated disclosure template by Grok on 2026-07-20.

**parity: partial** — Designated surface for disclosure mode. Protocol prose
elsewhere cannot rescue hollow fields here. AI assistance, funding, and COI are
**mandatory** fields—never optional and never auto-fabricated.

## Scope

- Manuscript id:
- Corresponding author:
- Venue / policy selector:
- Draft vs final:

### credit_authorship

CRediT (or explicit equivalent) authorship contributions. Record each author
against roles such as conceptualization, methodology, formal analysis,
investigation, writing – original draft, writing – review & editing,
supervision, and funding acquisition. Missing roles stay missing; do not invent
contributions. If CRediT is not used, state the alternative taxonomy explicitly.

| author | credit_roles | notes |
| --- | --- | --- |
|  |  |  |

### funding

Funding disclosure is mandatory. List grantors, grant ids, and roles. If there
is no funding, record explicit none only after human confirmation. Do not mark
funding optional, and do not auto-fabricate a clean funding statement.

- Funding text:
- Status: funded / none_confirmed / unknown_pending_human

### conflicts

Competing interests / conflicts of interest (COI) are mandatory. Describe
financial and non-financial interests. Explicit none requires human
confirmation. Do not optionalize COI and do not auto-fabricate a clean bill of
health.

- COI text:
- Status: interests_present / none_confirmed / unknown_pending_human

### data_code_availability

State data and code availability with access path, license, or honest
restriction reason. Missing repositories remain missing/blocked. Do not invent
URLs, DOIs, or “available on request” placeholders without author instruction.

- Data availability:
- Code availability:
- Restrictions / blocked reasons:

### ai_assistance

AI assistance disclosure is mandatory for writing, analysis, coding, figure
generation, or literature tooling that materially contributed. Name tools and
roles when known; mark unknown details missing. Never treat AI disclosure as
optional and never auto-fabricate tool lists or “no AI used” without human
confirmation.

- AI tools and roles:
- Status: disclosed / none_confirmed / unknown_pending_human

### policy_anchor_or_venue

Record venue or policy anchor selector. If venue rules are unknown, state
uncertainty and do not invent journal-specific disclosure rules. Policy text
remains human-confirmed before finalization.

- Venue / policy:
- Known?: yes / no / unknown
- Uncertainty notes:

### human_confirmation

Mandatory human confirmation of the full disclosure package. Automation may
draft fields but must not self-confirm. Final packages require human_confirmation
true with signer and timestamp. Auto-complete of AI/funding/COI is forbidden.

- human_confirmation (true/false):
- Signer:
- Timestamp:
- Confirmation scope:

## Human gates

- [ ] CRediT/authorship reviewed
- [ ] Funding mandatory field completed honestly
- [ ] COI mandatory field completed honestly
- [ ] Data/code availability honest
- [ ] AI assistance mandatory field completed honestly
- [ ] Venue/policy uncertainty recorded when unknown
- [ ] Human confirmation recorded (no auto-confirm)
