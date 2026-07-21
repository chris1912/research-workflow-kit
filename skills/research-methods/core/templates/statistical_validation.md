<!--
essential_core_lineage:
  file: core/templates/statistical_validation.md
  implementation: first-party-rewrite
  upstream_concepts:
    - statistical fallacies
  upstream_path_hints:
    - ars statistical_interpretation_guide
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
-->

# Statistical Validation (11 fallacies reserved)

Grok annotation: Essential Core template by Grok on 2026-07-20.
**parity: partial** — Stage-D content preserved where applicable; deeper fields reserved for E4.

**parity: not_started** for full instructional bodies on all 11 checks (E4).

Reserved check IDs:

| Check ID | Fallacy |
| --- | --- |
| sf01_p_equals_truth | p as probability hypothesis true |
| sf02_non_sig_equals_absent | non-significance = no effect |
| sf03_sig_equals_important | significance = importance |
| sf04_multiple_comparisons | multiplicity fishing |
| sf05_base_rate_neglect | base-rate neglect |
| sf06_stopping_optional | optional stopping |
| sf07_pseudoreplication | non-independent units |
| sf08_underpowered_claim | underpowered strong claims |
| sf09_ci_misread | CI misinterpretation |
| sf10_causal_from_assoc | causal from association |
| sf11_garden_of_forking | undisclosed analysis flexibility |

Each check needs instructional body + `pass|fail|na` slot before gate `stats_fallacies_11` can pass.
