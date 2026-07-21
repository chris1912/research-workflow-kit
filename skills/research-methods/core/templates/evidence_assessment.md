<!--
essential_core_lineage:
  file: core/templates/evidence_assessment.md
  implementation: first-party-rewrite
  upstream_concepts:
    - evidence assessment
    - claim verification
  upstream_path_hints:
    - ars synthesis / verification
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Evidence Assessment

Grok annotation: Essential Core E2 template depth by Grok on 2026-07-20.
**parity: partial** — E2 claim/evidence assessment for deep research and SR handoff.

Use after claim decomposition. Do not invent sources to complete a verdict. Lawful access only.

## Claim under assessment

- Claim ID / text (atomic):
- Context (paper section, user question, protocol outcome):
- Why this claim is decision-critical:

## Source and locator

- Primary source identity (DOI/PMID/arXiv/stable URL):
- Secondary source (if used only as lead):
- Locator (page/section/figure/table/paragraph):
- Access path: OA / licensed / human-supplied / failed
- Boundary used: metadata / abstract / full-text

## Extract vs inference

- Direct extract (quote or close paraphrase with locator):
- Inference drawn (if any) — must not be labeled as extract:
- Source tier (I–VII) and primary/secondary role:

## Verdict and states

- Verdict: VERIFIED / MINOR_DISTORTION / MAJOR_DISTORTION / UNVERIFIABLE / UNVERIFIABLE_ACCESS
- Evidence state: claim / extract / inference / uncertainty / missing / blocked / human-confirmed
- Distortion notes (what was overclaimed or omitted):

## Counterevidence and contradictions

- Counterevidence sought? yes / no / blocked
- Disconfirming sources or alternative explanations:
- Residual contradiction handling:

## Certainty handoff (if SR/GRADE applies)

- Related critical outcome:
- Notes for grade_risk_of_bias / inconsistency / indirectness / imprecision / publication_bias:
- Do not algorithmically fabricate certainty ratings here

## Human gates

- [ ] Locator present before VERIFIED
- [ ] Access failures not silently treated as absence of effect
- [ ] Human confirmation required for conclusion-bearing use
