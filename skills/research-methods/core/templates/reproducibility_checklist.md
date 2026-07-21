<!--
essential_core_lineage:
  file: core/templates/reproducibility_checklist.md
  implementation: first-party-rewrite
  upstream_concepts:
    - reproducibility checklist
  upstream_path_hints:
    - Stage-D reproducibility_checklist.md
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Experiment and Reproducibility Checklist

Grok annotation: Essential Core template by Grok on 2026-07-20.
**parity: partial** — Stage-D content preserved where applicable; deeper fields reserved for E4.

**Stage-D successor** of `templates/reproducibility_checklist.md`.
Planning artifact only. Do not invent data, statistics, or completed registrations.

## 1. Study and experiment intent

- Research question / estimand:
- Design type:
- Units, sample frame, and inclusion rules:
- Interventions / exposures / conditions:
- Outcomes and measurement timing:

## 2. Materials and environment

- Data sources and access path (lawful only):
- Code / notebook locations:
- Software and package versions:
- Hardware or runtime notes:
- Random seeds / stochastic controls:
- Sensitive-data handling:

## 3. Analysis and statistical-interpretation plan

- Primary analysis:
- Secondary / sensitivity analyses:
- Model family and assumptions:
- Multiplicity handling:
- Missing-data plan:
- Effect measure and uncertainty reporting plan:
- What result would falsify the preferred interpretation:
- Explicit non-claims (what will not be over-interpreted):

## 4. Reproducibility artifacts

| Artifact | Planned path or ID | Status | Notes |
| --- | --- | --- | --- |
| Protocol / preregistration note |  | planned / done / n/a | |
| Raw or controlled data access |  |  | |
| Analysis code |  |  | |
| Environment lock / container note |  |  | |
| Intermediate outputs |  |  | |
| Final tables/figures with provenance |  |  | |

## 5. Evidence states

- Confirmed extracts or prior results:
- Inferences requiring caution:
- Items marked **uncertainty**:
- External dependencies not yet available:

## 6. Human gates

- [ ] No invented p-values, effect sizes, CIs, or power results
- [ ] Execution requires explicit approval when mode is run
