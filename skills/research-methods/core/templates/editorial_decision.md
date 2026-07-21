<!--
essential_core_lineage:
  file: core/templates/editorial_decision.md
  implementation: first-party-rewrite
  upstream_concepts:
    - editorial decision
    - simulated decision letter
    - minority retention
  upstream_path_hints:
    - ars editorial synthesizer
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Editorial Decision Letter

Grok annotation: Essential Core E3-C designated editorial decision template by Grok on 2026-07-20.

**parity: partial** — Designated surface for simulated decision letters after
full-panel synthesis. Protocol prose cannot rescue hollow fields here. Not a
real venue/editor process unless human authority is recorded.

### decision_class

Record the decision class using exactly one of: accept, minor, major, reject,
revise-resubmit. Tie the class to blocking issue severity. Do not invent
journal-specific acceptance language as if an official editor signed.

- Decision class:
- Linked blocking concern IDs:
- Summary rationale:

### simulated_disclaimer

Label the letter **simulated** unless both a real venue/editor process and
human authority are supplied. Simulated outputs must never be presented as
official peer-review acceptance. Keep the disclaimer visible in the letter
header or first paragraph.

- Simulated (true/false):
- Disclaimer text:
- Real venue process supplied (true/false):

### blocking_issues

List blocking issues with concern IDs, severity, and required change. Blocking
items prevent accept-class language. Prefer residual IDs stable for re-review
trajectory scoring.

| concern_id | severity | required_change | evidence_pointer |
| --- | --- | --- | --- |
|  |  |  |  |

### non_blocking_suggestions

List non-blocking suggestions that improve clarity or completeness without
driving reject/major alone. Keep concern IDs when available. Do not promote
non-blocking items to fake blocking prestige.

| concern_id | suggestion | optional_evidence |
| --- | --- | --- |
|  |  |  |

### minority_concerns_retained

Retain minority and devil's-advocate concerns with disposition
retained|downgraded|rejected and non-empty rationale. Majority vote must not
erase DA findings. Rejected rows require severity.

| concern_id | source_reviewer | disposition | rationale |
| --- | --- | --- | --- |
|  |  | retained / downgraded / rejected |  |

### human_authority_gate

Human authority is mandatory before treating any letter as venue-real. Record
signer, timestamp, venue process pointer, and authority scope. Model tone never
substitutes for human authority. Without authority, keep simulated=true.

- Signer:
- Timestamp:
- Venue process pointer:
- Authority scope:
- human_authority (true/false):

## Human gates

- [ ] Simulated disclaimer present unless real venue + human authority
- [ ] Blocking vs non-blocking mapped to concern IDs
- [ ] Minority/DA concerns retained with rationale
- [ ] No fabricated editor or reviewer prestige names
