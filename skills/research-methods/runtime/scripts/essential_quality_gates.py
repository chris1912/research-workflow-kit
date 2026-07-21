#!/usr/bin/env python3
"""Essential Core quality gate runner.

Grok annotation: First-party rewrite by Grok on 2026-07-20 (E1).
Grok annotation: R1-R4 gate honesty fixes by Grok on 2026-07-20 (E0/E1 revision 1).
Grok annotation: V2-2/V2-3 reset-ledger + reviewer stage validators by Grok on 2026-07-20 (revision 2).
Grok annotation: E2 semantic method gates (PRISMA/RoB/GRADE/effect/anti-pooling) by Grok on 2026-07-20.
Grok annotation: E2 semantic gate adversarial hardening (R1-R5) by Grok on 2026-07-20.
Grok annotation: E3-A citation integrity evaluators + gate wiring by Grok on 2026-07-20.
Grok annotation: E3-B paper modes + revision/rebuttal/disclosure helpers by Grok on 2026-07-20.
Grok annotation: E3-B revision-2 ledger add/move/annotate + unique change_id by Grok on 2026-07-20.
Grok annotation: E3-C manuscript-review modes + identity/re-review/calibration by Grok on 2026-07-20.
Grok annotation: E3-C adversarial fail-closed identity/calibration/re-review/template by Grok on 2026-07-20.
stdlib only. No network.

essential_core_lineage:
  file: runtime/scripts/essential_quality_gates.py
  implementation: first-party-rewrite
  upstream_concepts:
    - codex quality gates
    - content depth
    - mode registry coverage
  upstream_path_hints:
    - skills/research-methods/codex/scripts/ars_codex_quality_gates.py
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
"""

from __future__ import annotations

import argparse
import importlib.util
import json
import re
import sys
from pathlib import Path
from typing import Any, Callable

SCRIPT_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = SCRIPT_DIR.parent
METHODS_ROOT = RUNTIME_DIR.parent
REPO_ROOT = METHODS_ROOT.parent.parent

EXIT_OK = 0
EXIT_FAIL = 1
EXIT_USAGE = 2
EXIT_IO = 4

E2_METHOD_GATES = {
    "prisma_fields",
    "rob2_fields",
    "robins_i_fields",
    "grade_fields",
    "effect_hetero_sensitivity",
    "anti_pooling_fields",
}

E4_SEMANTIC_GATES = {
    "stats_fallacies_11",
}

E2_SEMANTIC_GATES = E2_METHOD_GATES | E4_SEMANTIC_GATES

MIN_FIELD_BODY = 40

PRISMA_PROTOCOL_FIELDS = (
    "prisma_title_registration",
    "eligibility_pico",
    "information_sources",
    "search_strategy",
    "selection_process",
    "data_items",
    "risk_of_bias_plan",
    "effect_measures",
    "synthesis_methods",
    "heterogeneity_plan",
    "sensitivity_plan",
    "anti_pooling",
    "reporting_bias",
    "certainty_grade",
)

PRISMA_REPORT_FIELDS = (
    "report_title_abstract",
    "report_methods_eligibility",
    "report_methods_search",
    "report_methods_selection",
    "report_methods_data",
    "report_methods_rob",
    "report_methods_synthesis",
    "report_results_selection_flow",
    "report_results_study_chars",
    "report_results_rob",
    "report_results_synthesis",
    "report_discussion_certainty",
    "report_funding_competing",
)

ROB2_DOMAINS = {
    "rob2_d1": "randomization",
    "rob2_d2": "deviations",
    "rob2_d3": "missing",
    "rob2_d4": "measurement",
    "rob2_d5": "selection of the reported",
}

ROB2_JUDGMENT_VOCAB = ("low", "some_concerns", "high", "no_information")

ROBINS_DOMAINS = {
    "robins_d1": "confounding",
    "robins_d2": "selection of participants",
    "robins_d3": "classification",
    "robins_d4": "deviations",
    "robins_d5": "missing data",
    "robins_d6": "measurement of outcomes",
    "robins_d7": "selection of the reported",
}

ROBINS_JUDGMENT_VOCAB = (
    "low",
    "moderate",
    "serious",
    "critical",
    "no_information",
)

GRADE_DOWNGRADE_FIELDS = (
    "grade_risk_of_bias",
    "grade_inconsistency",
    "grade_indirectness",
    "grade_imprecision",
    "grade_publication_bias",
)

GRADE_ALL_FIELDS = GRADE_DOWNGRADE_FIELDS + (
    "grade_upgrade_factors",
    "grade_certainty",
)

EFFECT_HETERO_FIELDS = (
    "effect_measure_primary",
    "effect_measure_by_outcome_type",
    "hetero_stats",
    "hetero_exploration",
    "sensitivity_analyses",
)

ANTI_POOLING_FIELDS = (
    "anti_pooling_conditions",
    "anti_pooling_action",
)

CITATION_INTEGRITY_PROTOCOL_FIELDS = (
    "citation_identity",
    "locator_or_quote",
    "claim_source_fidelity",
    "temporal_version_check",
    "correction_retraction_predatory_risk",
    "contamination_signals",
    "plagiarism_boundary",
    "access_state",
    "integrity_mode",
    "escalation",
)

CITATION_AUDIT_TEMPLATE_FIELDS = CITATION_INTEGRITY_PROTOCOL_FIELDS

CLAIM_REPORT_TEMPLATE_FIELDS = CITATION_INTEGRITY_PROTOCOL_FIELDS + (
    "report_scope",
)

CITATION_PROTOCOL_REL = "core/protocols/citation_integrity.md"
CITATION_AUDIT_REL = "core/templates/citation_integrity_audit.md"
CLAIM_REPORT_REL = "core/templates/claim_verification_report.md"

E3_CITATION_SURFACE_RELS = (
    CITATION_PROTOCOL_REL,
    CITATION_AUDIT_REL,
    CLAIM_REPORT_REL,
)

VERIFIED_ASSESSMENT_SOURCES = frozenset({"human_confirmed", "verified_adapter"})
ACCESS_STATES = frozenset(
    {"verified", "unverified", "unresolvable", "access_blocked"}
)
ACCESS_STATES_REQUIRING_UNVERIFIABLE_ACCESS = frozenset(
    {"unresolvable", "access_blocked"}
)
# Backward-compatible alias used by VERIFIED access-block checks.
ACCESS_STATES_BLOCKING_VERIFIED = ACCESS_STATES_REQUIRING_UNVERIFIABLE_ACCESS
SUPPORT_STATUSES = frozenset(
    {"supported", "partial", "contradicted", "unsupported", "unknown"}
)
KNOWN_RISK_FLAGS = frozenset(
    {
        "retracted",
        "corrected",
        "expression_of_concern",
        "version_mismatch",
        "predatory",
        "contamination_advisory",
    }
)

E2_PROTOCOL_NAMES = {
    "research_question.md",
    "deep_research.md",
    "systematic_review.md",
}

E3A_PROTOCOL_NAMES = {
    "citation_integrity.md",
}

E3B_PROTOCOL_NAMES = {
    "academic_paper.md",
}

E3C_PROTOCOL_NAMES = {
    "manuscript_review.md",
}

ACADEMIC_PAPER_PROTOCOL_REL = "core/protocols/academic_paper.md"
REVISION_TEMPLATE_REL = "core/templates/revision_roadmap.md"
REBUTTAL_TEMPLATE_REL = "core/templates/rebuttal_audit.md"
DISCLOSURE_TEMPLATE_REL = "core/templates/disclosure_statement.md"
ARGUMENT_MAP_TEMPLATE_REL = "core/templates/argument_map.md"
MANUSCRIPT_REVIEW_PROTOCOL_REL = "core/protocols/manuscript_review.md"
MANUSCRIPT_REVIEW_TEMPLATE_REL = "core/templates/manuscript_review_full.md"
EDITORIAL_DECISION_TEMPLATE_REL = "core/templates/editorial_decision.md"

E3_PAPER_TEMPLATE_RELS = (
    REVISION_TEMPLATE_REL,
    REBUTTAL_TEMPLATE_REL,
    DISCLOSURE_TEMPLATE_REL,
    ARGUMENT_MAP_TEMPLATE_REL,
)

E3_REVIEW_TEMPLATE_RELS = (
    MANUSCRIPT_REVIEW_TEMPLATE_REL,
    EDITORIAL_DECISION_TEMPLATE_REL,
)

REVIEWER_MODES = (
    "full",
    "re_review",
    "quick",
    "methodology_focus",
    "guided",
    "calibration",
)

REVIEWER_MODE_CORE_FIELDS: dict[str, tuple[str, ...]] = {
    "full": (
        "full_mode_inputs",
        "full_mode_outputs",
        "full_stop_conditions",
        "full_offline_fallback",
        "full_human_gates",
        "full_independent_methodology",
        "full_independent_domain",
        "full_independent_interdisciplinary",
        "full_independent_devils_advocate",
        "full_synthesis_barrier",
        "full_minority_disposition",
        "full_decision_letter_simulated",
        "full_revision_roadmap",
    ),
    "re_review": (
        "re_review_mode_inputs",
        "re_review_mode_outputs",
        "re_review_stop_conditions",
        "re_review_offline_fallback",
        "re_review_human_gates",
        "re_review_prior_issues",
        "re_review_trajectory",
        "re_review_no_blanket_all_fixed",
        "re_review_evidence_pointers",
    ),
    "quick": (
        "quick_mode_inputs",
        "quick_mode_outputs",
        "quick_stop_conditions",
        "quick_offline_fallback",
        "quick_human_gates",
        "quick_scope_limit",
        "quick_no_full_panel_claim",
    ),
    "methodology_focus": (
        "methodology_focus_mode_inputs",
        "methodology_focus_mode_outputs",
        "methodology_focus_stop_conditions",
        "methodology_focus_offline_fallback",
        "methodology_focus_human_gates",
        "methodology_focus_mandatory_methods",
        "methodology_focus_stats_checks",
    ),
    "guided": (
        "guided_mode_inputs",
        "guided_mode_outputs",
        "guided_stop_conditions",
        "guided_offline_fallback",
        "guided_human_gates",
        "guided_dialogue_checkpoints",
        "guided_no_oneshot_dump",
    ),
    "calibration": (
        "calibration_mode_inputs",
        "calibration_mode_outputs",
        "calibration_stop_conditions",
        "calibration_offline_fallback",
        "calibration_human_gates",
        "calibration_gold_required",
        "calibration_session_only",
        "calibration_no_fabricated_labels",
    ),
}

MANUSCRIPT_REVIEW_TEMPLATE_FIELDS = (
    "independent_methodology",
    "independent_domain",
    "independent_interdisciplinary",
    "independent_devils_advocate",
    "synthesis_barrier",
    "minority_disposition",
    "decision_letter",
    "revision_roadmap",
)

EDITORIAL_DECISION_TEMPLATE_FIELDS = (
    "decision_class",
    "simulated_disclaimer",
    "blocking_issues",
    "non_blocking_suggestions",
    "minority_concerns_retained",
    "human_authority_gate",
)

REVIEWER_IDENTITY_KINDS = frozenset(
    {
        "anonymous",
        "anonymous_role",
        "simulated_role",
        "named_real",
        "named_real_person",
        "simulated",
        "role",
    }
)
ANONYMOUS_SIMULATED_KINDS = frozenset(
    {"anonymous", "anonymous_role", "simulated_role", "simulated", "role"}
)
NAMED_REAL_IDENTITY_KINDS = frozenset(
    {"named_real", "named", "real_person", "named_real_person", "named_person"}
)
# Short sentinels: match only as full normalized source or whole tokens.
FORBIDDEN_IDENTITY_EXACT_TOKENS = frozenset(
    {
        "none",
        "n_a",
        "na",
        "tbd",
        "todo",
    }
)
# Phrase tokens: substring detection for forbidden provenance wording.
FORBIDDEN_IDENTITY_PHRASES = frozenset(
    {
        "invented",
        "assumed",
        "fabricated",
        "guessed",
        "made_up",
        "prestige",
        "unknown",
        "self_asserted",
        "selfasserted",
        "self_assert",
        "circular",
        "circular_provenance",
        "model_invented",
        "hallucinated",
        "placeholder",
    }
)
FORBIDDEN_IDENTITY_SOURCES = (
    FORBIDDEN_IDENTITY_EXACT_TOKENS | FORBIDDEN_IDENTITY_PHRASES
)
REREVIEW_TRAJECTORIES = frozenset(
    {"open", "partially_addressed", "addressed", "new"}
)
REREVIEW_NEEDS_POINTER = frozenset({"addressed", "partially_addressed"})
MIN_CALIBRATION_GOLD_ITEMS = 5
MAX_CALIBRATION_GOLD_ITEMS = 20

PAPER_MODES = (
    "full",
    "plan",
    "outline_only",
    "revision",
    "revision_coach",
    "abstract_only",
    "lit_review",
    "format_convert",
    "citation_check",
    "disclosure",
    "rebuttal_audit",
)

PAPER_MODE_CORE_FIELDS: dict[str, tuple[str, ...]] = {
    "full": (
        "full_mode_inputs",
        "full_mode_outputs",
        "full_stop_conditions",
        "full_offline_fallback",
        "full_human_gates",
        "full_claim_intent_precommit",
        "full_no_invented_results",
    ),
    "plan": (
        "plan_mode_inputs",
        "plan_mode_outputs",
        "plan_stop_conditions",
        "plan_offline_fallback",
        "plan_human_gates",
        "plan_chapter_negotiation",
        "plan_insight_capture",
    ),
    "outline_only": (
        "outline_only_mode_inputs",
        "outline_only_mode_outputs",
        "outline_only_stop_conditions",
        "outline_only_offline_fallback",
        "outline_only_human_gates",
        "outline_evidence_map",
        "outline_no_draft_body_claim",
    ),
    "revision": (
        "revision_mode_inputs",
        "revision_mode_outputs",
        "revision_stop_conditions",
        "revision_offline_fallback",
        "revision_human_gates",
        "revision_protected_claims",
        "revision_commitment_ledger",
        "revision_patch_or_change_ledger",
        "revision_no_silent_new_evidence",
        "revision_author_signoff",
        "revision_recovery_checkpoint",
    ),
    "revision_coach": (
        "revision_coach_mode_inputs",
        "revision_coach_mode_outputs",
        "revision_coach_stop_conditions",
        "revision_coach_offline_fallback",
        "revision_coach_human_gates",
        "revision_coach_roadmap_only",
        "revision_coach_forbid_full_rewrite",
    ),
    "abstract_only": (
        "abstract_only_mode_inputs",
        "abstract_only_mode_outputs",
        "abstract_only_stop_conditions",
        "abstract_only_offline_fallback",
        "abstract_only_human_gates",
        "abstract_bilingual_fields",
        "abstract_protected_hedges",
    ),
    "lit_review": (
        "lit_review_mode_inputs",
        "lit_review_mode_outputs",
        "lit_review_stop_conditions",
        "lit_review_offline_fallback",
        "lit_review_human_gates",
        "lit_review_handoffs",
        "lit_review_e2_handoff",
        "lit_review_no_prisma_full_claim",
    ),
    "format_convert": (
        "format_convert_mode_inputs",
        "format_convert_mode_outputs",
        "format_convert_stop_conditions",
        "format_convert_offline_fallback",
        "format_convert_human_gates",
        "format_convert_engine_checklist",
        "format_convert_runtime_honesty",
    ),
    "citation_check": (
        "citation_check_mode_inputs",
        "citation_check_mode_outputs",
        "citation_check_stop_conditions",
        "citation_check_offline_fallback",
        "citation_check_human_gates",
        "citation_check_inventory",
        "citation_check_bind_integrity",
    ),
    "disclosure": (
        "disclosure_mode_inputs",
        "disclosure_mode_outputs",
        "disclosure_stop_conditions",
        "disclosure_offline_fallback",
        "disclosure_human_gates",
        "disclosure_credit",
        "disclosure_funding",
        "disclosure_coi",
        "disclosure_data_code",
        "disclosure_ai",
        "disclosure_policy_or_venue",
        "disclosure_human_confirmation",
    ),
    "rebuttal_audit": (
        "rebuttal_audit_mode_inputs",
        "rebuttal_audit_mode_outputs",
        "rebuttal_audit_stop_conditions",
        "rebuttal_audit_offline_fallback",
        "rebuttal_audit_human_gates",
        "rebuttal_evaluator_only",
        "rebuttal_point_coverage",
        "rebuttal_no_schema11_required",
    ),
}

REVISION_TEMPLATE_FIELDS = (
    "commitment_ledger",
    "patch_or_change_ledger",
    "protected_claims",
    "author_signoff",
    "revision_recovery",
    "version_family_reconciliation",
    "new_evidence_gate",
)

REBUTTAL_TEMPLATE_FIELDS = (
    "evaluator_only",
    "point_coverage_matrix",
    "change_or_evidence_or_rationale",
    "tone_overclaim_flags",
    "unresolved_escalation",
)

DISCLOSURE_TEMPLATE_FIELDS = (
    "credit_authorship",
    "funding",
    "conflicts",
    "data_code_availability",
    "ai_assistance",
    "policy_anchor_or_venue",
    "human_confirmation",
)

REVISION_ALLOWED_OPS = frozenset({"add", "delete", "replace", "move", "annotate"})
REVISION_EVIDENCE_OK = frozenset({"claim", "extract", "human-confirmed", "human_confirmed"})
REBUTTAL_COVERAGE = frozenset({"covered", "partial", "missing"})
REBUTTAL_RESPONSE_KINDS = frozenset({"ms_change", "evidence", "no_change_rationale"})
DISCLOSURE_PACKAGE_STATES = frozenset({"draft", "final"})
DISCLOSURE_FUNDING_STATES = frozenset(
    {"funded", "none_confirmed", "unknown_pending_human"}
)
DISCLOSURE_COI_STATES = frozenset(
    {"interests_present", "none_confirmed", "unknown_pending_human"}
)
DISCLOSURE_AI_STATES = frozenset(
    {"disclosed", "none_confirmed", "unknown_pending_human"}
)
DISCLOSURE_DATA_CODE_STATES = frozenset(
    {
        "available",
        "restricted",
        "blocked",
        "not_applicable",
        "unknown_pending_human",
    }
)
DISCLOSURE_POLICY_STATES = frozenset({"yes", "no", "unknown"})

DOI_FIND_RE = re.compile(r"\b10\.\d{4,9}/[^\s\]>)\"']+", re.I)
RESULT_MARKER_RE = re.compile(
    r"(?:"
    r"\bp\s*[<≥>=]{1,2}\s*0\.\d+"
    r"|\b(?:OR|HR|RR|RRR)\s*=\s*\d+(?:\.\d+)?"
    r"|\bsignificantly\s+(?:increased|decreased|improved|reduced)\b"
    r"|\b(?:effect\s+size|mean\s+difference)\s*=\s*\d+(?:\.\d+)?"
    r")",
    re.I,
)
STRENGTHEN_PAIRS = (
    (re.compile(r"\bmay\b", re.I), re.compile(r"\b(?:does|will|proves?|demonstrates?)\b", re.I)),
    (re.compile(r"\bmight\b", re.I), re.compile(r"\b(?:will|must|proves?)\b", re.I)),
    (re.compile(r"\bsuggests?\b", re.I), re.compile(r"\b(?:proves?|demonstrates?|confirms?)\b", re.I)),
    (re.compile(r"\bpossibly\b", re.I), re.compile(r"\b(?:certainly|definitely|always)\b", re.I)),
    (re.compile(r"\bcould\b", re.I), re.compile(r"\b(?:must|will|does)\b", re.I)),
    (re.compile(r"\bappears?\s+to\b", re.I), re.compile(r"\bis\b", re.I)),
)

EVIDENCE_STATES = {
    "claim",
    "extract",
    "inference",
    "uncertainty",
    "missing",
    "blocked",
    "human-confirmed",
}

CLAIM_VERDICTS = {
    "VERIFIED",
    "MINOR_DISTORTION",
    "MAJOR_DISTORTION",
    "UNVERIFIABLE",
    "UNVERIFIABLE_ACCESS",
}

INDEPENDENT_ARTIFACTS = (
    "review/independent/methodology.md",
    "review/independent/domain.md",
    "review/independent/interdisciplinary.md",
    "review/independent/devils_advocate.md",
)

SYNTHESIS_ARTIFACTS = (
    "review/synthesis/editorial.md",
    "review/synthesis/decision_letter.md",
    "review/synthesis/revision_roadmap.md",
)

SECTION_ORDER = [
    "Independent Reviewer: Methodology",
    "Independent Reviewer: Domain",
    "Independent Reviewer: Interdisciplinary",
    "Independent Reviewer: Devil's Advocate",
    "Editorial Synthesis",
    "Decision Letter",
    "Revision Roadmap",
]

INDEPENDENT_REVIEWER_IDS = (
    "methodology",
    "domain",
    "interdisciplinary",
    "devils_advocate",
)
VALID_DISPOSITIONS = frozenset({"retained", "downgraded", "rejected"})

MIN_PROSE_STRICT = 400
MIN_PROSE_TEMPLATE = 150
MIN_PROSE_NONEMPTY = 40
MAX_THIN_SECTION_RATIO = 0.5
MIN_SECTION_BODY = 40


def read_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def gate_result(gate_id: str, ok: bool, detail: str, status: str | None = None) -> dict[str, Any]:
    return {
        "id": gate_id,
        "ok": ok,
        "detail": detail,
        "status": status or ("pass" if ok else "fail"),
    }


def root_from_args(root: str | None) -> Path:
    if root:
        return Path(root).resolve()
    return METHODS_ROOT.resolve()


def load_manifest(methods_root: Path) -> dict[str, Any]:
    return json.loads(read_text(methods_root / "manifest.json"))


def load_runtime_manifest(methods_root: Path) -> dict[str, Any]:
    return json.loads(read_text(methods_root / "runtime" / "full-runtime-manifest.json"))


def strip_lineage_comments(text: str) -> str:
    return re.sub(r"<!--.*?-->", "", text, flags=re.S)


def prose_body(text: str) -> str:
    body = strip_lineage_comments(text)
    prose = re.sub(r"^#{1,6}\s+.*$", "", body, flags=re.M)
    prose = re.sub(r"\s+", " ", prose).strip()
    return prose


def heading_list(text: str) -> list[str]:
    body = strip_lineage_comments(text)
    return re.findall(r"^#{1,6}\s+.+", body, flags=re.M)


def h23_section_bodies(text: str) -> list[str]:
    body = strip_lineage_comments(text)
    parts = re.split(r"(?=^#{2,3}\s+)", body, flags=re.M)
    sections: list[str] = []
    for part in parts:
        if not re.match(r"^#{2,3}\s+", part):
            continue
        content = re.sub(r"^#{2,3}\s+.*$", "", part, count=1, flags=re.M)
        content = re.sub(r"\s+", " ", content).strip()
        sections.append(content)
    return sections


def load_planner_module() -> Any:
    path = SCRIPT_DIR / "essential_full_runtime.py"
    spec = importlib.util.spec_from_file_location("essential_full_runtime_gate", path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"unable to load planner: {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def g_single_root_skill(methods_root: Path) -> dict[str, Any]:
    skill = methods_root / "SKILL.md"
    if not skill.is_file():
        return gate_result("single_root_skill", False, "SKILL.md missing")
    data = load_manifest(methods_root)
    if data.get("packaging_mode") != "essential_core":
        return gate_result(
            "single_root_skill",
            False,
            f"packaging_mode={data.get('packaging_mode')!r} expected essential_core",
        )
    if (methods_root / "ars").exists() or (methods_root / "codex").exists():
        return gate_result("single_root_skill", False, "ars/ or codex/ unexpectedly present")
    return gate_result("single_root_skill", True, "single SKILL.md and essential_core packaging")


def g_alias_coverage(methods_root: Path) -> dict[str, Any]:
    man = load_runtime_manifest(methods_root)
    aliases = man.get("aliases") or {}
    modes = man.get("modes") or []
    count_model = man.get("count_model") or {}
    expected = int(count_model.get("prefixed_aliases") or 68)
    if len(aliases) != expected:
        return gate_result(
            "alias_coverage",
            False,
            f"alias count {len(aliases)} != expected {expected}",
        )
    # uniqueness already dict; validate each maps to a known mode row
    mode_keys = {(m.get("workflow"), m.get("mode")) for m in modes if isinstance(m, dict)}
    bad: list[str] = []
    for alias, entry in aliases.items():
        if not isinstance(entry, dict):
            bad.append(f"{alias}:not-object")
            continue
        key = (entry.get("workflow"), entry.get("mode"))
        if key not in mode_keys:
            bad.append(f"{alias}:{key}")
    if bad:
        return gate_result("alias_coverage", False, f"unmapped aliases: {bad[:8]}")
    # every mode row must contribute exactly two prefixed aliases
    for mode in modes:
        if not isinstance(mode, dict):
            continue
        row_aliases = mode.get("aliases") or []
        if len(row_aliases) != 2:
            return gate_result(
                "alias_coverage",
                False,
                f"mode {mode.get('workflow')}/{mode.get('mode')} needs 2 aliases, has {len(row_aliases)}",
            )
        for a in row_aliases:
            if a not in aliases:
                return gate_result("alias_coverage", False, f"mode alias missing from map: {a}")
    return gate_result("alias_coverage", True, f"covered {len(aliases)} unique prefixed aliases")


def g_vague_topic_socratic(methods_root: Path) -> dict[str, Any]:
    registry = read_text(methods_root / "MODE_REGISTRY.md")
    planner = read_text(methods_root / "runtime" / "scripts" / "essential_full_runtime.py")
    if "paper_topic_scoping_override" not in planner and "paper_topic_scoping_override" not in registry:
        return gate_result("vague_topic_socratic", False, "override token missing")
    if "socratic" not in registry.lower():
        return gate_result("vague_topic_socratic", False, "socratic mode missing from registry")
    return gate_result("vague_topic_socratic", True, "socratic override documented and coded")


def g_mode_registry_coverage(methods_root: Path) -> dict[str, Any]:
    """Structured exact coverage: identities, aliases, protocol paths, counts."""
    man = load_runtime_manifest(methods_root)
    registry_text = read_text(methods_root / "MODE_REGISTRY.md")
    modes = man.get("modes") or []
    aliases = man.get("aliases") or {}
    count_model = man.get("count_model") or {}
    workflows = man.get("workflows") or []

    expected_rows = int(count_model.get("mode_operation_rows") or 34)
    expected_aliases = int(count_model.get("prefixed_aliases") or 68)
    expected_workflows = int(count_model.get("workflows") or 5)
    breakdown = count_model.get("breakdown") or {}
    legacy = int(count_model.get("legacy_ars_mode_families") or 27)
    legacy_explain = str(count_model.get("legacy_count_explanation") or "")
    alias_explain = str(count_model.get("alias_count_explanation") or "")

    if not legacy_explain or not alias_explain:
        return gate_result(
            "mode_registry_coverage",
            False,
            "count_model missing legacy_count_explanation or alias_count_explanation",
        )
    if len(workflows) != expected_workflows:
        return gate_result(
            "mode_registry_coverage",
            False,
            f"workflows {len(workflows)} != {expected_workflows}",
        )
    if len(modes) != expected_rows:
        return gate_result(
            "mode_registry_coverage",
            False,
            f"mode rows {len(modes)} != {expected_rows}",
        )
    if len(aliases) != expected_aliases:
        return gate_result(
            "mode_registry_coverage",
            False,
            f"aliases {len(aliases)} != {expected_aliases}",
        )

    # breakdown must sum to mode rows
    if breakdown:
        total = sum(int(v) for v in breakdown.values())
        if total != expected_rows:
            return gate_result(
                "mode_registry_coverage",
                False,
                f"breakdown sum {total} != mode_operation_rows {expected_rows}",
            )

    seen_alias: set[str] = set()
    identity_keys: set[tuple[str, str]] = set()
    missing_registry: list[str] = []
    missing_protocol: list[str] = []
    bad_workflow: list[str] = []

    for row in modes:
        if not isinstance(row, dict):
            return gate_result("mode_registry_coverage", False, "non-object mode row")
        workflow = str(row.get("workflow") or "")
        mode = str(row.get("mode") or "")
        if workflow not in workflows:
            bad_workflow.append(f"{workflow}/{mode}")
            continue
        key = (workflow, mode)
        if key in identity_keys:
            return gate_result(
                "mode_registry_coverage",
                False,
                f"duplicate identity {workflow}/{mode}",
            )
        identity_keys.add(key)
        # registry must mention mode id and at least one alias for the row
        if mode not in registry_text:
            missing_registry.append(f"mode:{mode}")
        row_aliases = row.get("aliases") or []
        for alias in row_aliases:
            if alias in seen_alias:
                return gate_result(
                    "mode_registry_coverage",
                    False,
                    f"duplicate alias {alias}",
                )
            seen_alias.add(str(alias))
            mapped = aliases.get(alias)
            if not isinstance(mapped, dict):
                return gate_result(
                    "mode_registry_coverage",
                    False,
                    f"alias {alias} not in aliases map",
                )
            if mapped.get("workflow") != workflow or mapped.get("mode") != mode:
                return gate_result(
                    "mode_registry_coverage",
                    False,
                    f"alias {alias} maps to {mapped} not {workflow}/{mode}",
                )
            if alias not in registry_text:
                missing_registry.append(f"alias:{alias}")
        protocols = row.get("protocol_paths") or []
        if not protocols:
            missing_protocol.append(f"{workflow}/{mode}:none")
        for rel in protocols:
            path = methods_root / str(rel)
            if not path.is_file():
                missing_protocol.append(str(rel))

    if bad_workflow:
        return gate_result(
            "mode_registry_coverage",
            False,
            f"unknown workflows: {bad_workflow[:8]}",
        )
    if missing_protocol:
        return gate_result(
            "mode_registry_coverage",
            False,
            f"missing protocol paths: {missing_protocol[:8]}",
        )
    if missing_registry:
        return gate_result(
            "mode_registry_coverage",
            False,
            f"MODE_REGISTRY.md missing identities/aliases: {missing_registry[:12]}",
        )
    if legacy != 27:
        return gate_result(
            "mode_registry_coverage",
            False,
            f"legacy_ars_mode_families expected 27 got {legacy}",
        )

    detail = (
        f"exact coverage ok: workflows={expected_workflows}, "
        f"mode_operation_rows={expected_rows} ({breakdown}), "
        f"legacy_ars_mode_families={legacy}, prefixed_aliases={expected_aliases}; "
        f"legacy_explain={legacy_explain[:80]}..."
    )
    return gate_result("mode_registry_coverage", True, detail)


def validate_reviewer_stage_state(state: dict[str, Any]) -> dict[str, Any]:
    """Deterministic A20 visibility, synthesis readiness, and minority disposition checks.

    Expected state shape (in-memory; no multi-process claim)::

        {
          "independents_complete": ["methodology", ...],
          "visibility": {"methodology": [], "domain": ["methodology"], ...},
          "synthesis_started": bool,
          "dispositions": [
            {
              "concern_id": "M-01",
              "source": "methodology",
              "disposition": "retained",
              "rationale": "incomplete sample justification",
            },
            ...
          ],
        }

    Multi-process orchestration remains partial; this validator covers barrier
    semantics only. E3-C requires non-empty rationale on each disposition when
    synthesis has started. Retains early_visibility, premature_synthesis, and
    missing_disposition error codes from E1/V2-3.
    """
    required = list(INDEPENDENT_REVIEWER_IDS)
    complete_raw = state.get("independents_complete") or []
    if not isinstance(complete_raw, list):
        return {
            "ok": False,
            "error": "invalid_state",
            "message": "independents_complete must be a list",
        }
    complete = {str(x) for x in complete_raw}
    all_complete = set(required).issubset(complete)

    visibility = state.get("visibility") or {}
    if not isinstance(visibility, dict):
        return {
            "ok": False,
            "error": "invalid_state",
            "message": "visibility must be an object",
        }

    # A20: no reviewer may see peer independent drafts before all independents complete.
    for reviewer_id, peers in visibility.items():
        peer_list = peers if isinstance(peers, list) else []
        peer_ids = [str(p) for p in peer_list if str(p) and str(p) != str(reviewer_id)]
        if peer_ids and not all_complete:
            return {
                "ok": False,
                "error": "early_visibility",
                "message": (
                    f"A20 violation: reviewer {reviewer_id!r} saw peer drafts "
                    f"{peer_ids} before all independents completed"
                ),
            }

    synthesis_started = bool(state.get("synthesis_started"))
    if synthesis_started and not all_complete:
        return {
            "ok": False,
            "error": "premature_synthesis",
            "message": "synthesis started before all four independent artifacts completed",
        }

    dispositions = state.get("dispositions")
    if dispositions is None:
        dispositions = []
    if not isinstance(dispositions, list):
        return {
            "ok": False,
            "error": "invalid_state",
            "message": "dispositions must be a list",
        }

    # When synthesis has started, every independent source needs a disposition,
    # including minority/DA retention, plus non-empty rationale (E3-C).
    if synthesis_started:
        if not dispositions:
            return {
                "ok": False,
                "error": "missing_disposition",
                "message": "synthesis requires minority/independent dispositions",
            }
        sources_with_disp: set[str] = set()
        for item in dispositions:
            if not isinstance(item, dict):
                return {
                    "ok": False,
                    "error": "invalid_disposition",
                    "message": "each disposition must be an object",
                }
            disp = str(item.get("disposition") or "").lower()
            source = str(item.get("source") or "")
            concern = item.get("concern_id")
            rationale = _nonempty_text(
                item.get("rationale") or item.get("reason") or item.get("justification")
            )
            if not concern:
                return {
                    "ok": False,
                    "error": "missing_disposition",
                    "message": "disposition missing concern_id",
                }
            if disp not in VALID_DISPOSITIONS:
                return {
                    "ok": False,
                    "error": "invalid_disposition",
                    "message": f"disposition must be one of {sorted(VALID_DISPOSITIONS)}",
                }
            if not rationale:
                return {
                    "ok": False,
                    "error": "missing_rationale",
                    "message": (
                        f"disposition missing rationale for concern_id={concern!r}"
                    ),
                }
            if source:
                sources_with_disp.add(source)
        if "devils_advocate" not in sources_with_disp:
            return {
                "ok": False,
                "error": "missing_disposition",
                "message": "minority/DA disposition not retained at synthesis",
            }
        missing_sources = [s for s in required if s not in sources_with_disp]
        if missing_sources:
            return {
                "ok": False,
                "error": "missing_disposition",
                "message": f"missing dispositions for sources: {missing_sources}",
            }

    return {
        "ok": True,
        "error": None,
        "message": "reviewer stage visibility/synthesis/disposition ok",
    }


def g_reviewer_independence(methods_root: Path) -> dict[str, Any]:
    """Fixture structure + deterministic stage validator; multi-process remains partial."""
    fixture = methods_root / "runtime" / "tests" / "fixtures" / "reviewer_full_independent_sections.md"
    contract = methods_root / "core" / "contracts" / "reviewer_independence.md"
    if not fixture.is_file() or not contract.is_file():
        return gate_result("reviewer_independence", False, "fixture or contract missing")
    text = read_text(fixture)
    contract_text = read_text(contract)
    positions: list[int] = []
    for heading in SECTION_ORDER:
        idx = text.find(heading)
        if idx < 0:
            return gate_result("reviewer_independence", False, f"missing heading: {heading}")
        positions.append(idx)
    if positions != sorted(positions):
        return gate_result("reviewer_independence", False, "fixture headings out of order")

    for artifact in INDEPENDENT_ARTIFACTS + SYNTHESIS_ARTIFACTS:
        if artifact not in contract_text:
            return gate_result(
                "reviewer_independence",
                False,
                f"contract missing artifact path: {artifact}",
            )
    if "Visibility barrier" not in contract_text and "visibility barrier" not in contract_text.lower():
        return gate_result("reviewer_independence", False, "contract missing visibility barrier")
    if "disposition" not in text.lower():
        return gate_result("reviewer_independence", False, "minority disposition missing on fixture")
    if "devils_advocate" not in text.lower() and "devil" not in text.lower():
        return gate_result("reviewer_independence", False, "DA minority source missing")
    if not re.search(r"DA-0?\d+.*retained|retained.*DA-0?\d+|devils_advocate\s*\|\s*retained", text, re.I):
        if "DA-01" not in text or "retained" not in text.lower():
            return gate_result("reviewer_independence", False, "DA disposition not retained in fixture")
    synth_idx = text.find("Editorial Synthesis")
    independent_blob = text[:synth_idx]
    for heading in SECTION_ORDER[:4]:
        if independent_blob.count(heading) != 1:
            return gate_result(
                "reviewer_independence",
                False,
                f"independence barrier: heading count wrong for {heading}",
            )

    # Positive in-memory stage: all independents done, no early peer visibility,
    # synthesis with full dispositions including DA + rationale (E3-C).
    good_state = {
        "independents_complete": list(INDEPENDENT_REVIEWER_IDS),
        "visibility": {rid: [] for rid in INDEPENDENT_REVIEWER_IDS},
        "synthesis_started": True,
        "dispositions": [
            {
                "concern_id": "M-01",
                "source": "methodology",
                "disposition": "retained",
                "rationale": "incomplete sample size justification",
            },
            {
                "concern_id": "D-01",
                "source": "domain",
                "disposition": "retained",
                "rationale": "missing alternative model class",
            },
            {
                "concern_id": "I-01",
                "source": "interdisciplinary",
                "disposition": "downgraded",
                "rationale": "multi-site validity secondary for this venue",
            },
            {
                "concern_id": "DA-01",
                "source": "devils_advocate",
                "disposition": "retained",
                "rationale": "outcome switching risk remains material",
            },
        ],
    }
    good = validate_reviewer_stage_state(good_state)
    if not good.get("ok"):
        return gate_result(
            "reviewer_independence",
            False,
            f"positive stage validator failed: {good}",
        )

    # Negative: A20 early peer visibility
    early = validate_reviewer_stage_state(
        {
            "independents_complete": ["methodology"],
            "visibility": {
                "domain": ["methodology"],
                "methodology": [],
            },
            "synthesis_started": False,
            "dispositions": [],
        }
    )
    if early.get("ok") or early.get("error") != "early_visibility":
        return gate_result(
            "reviewer_independence",
            False,
            f"A20 early visibility not refused: {early}",
        )

    # Negative: premature synthesis
    premature = validate_reviewer_stage_state(
        {
            "independents_complete": ["methodology", "domain"],
            "visibility": {rid: [] for rid in INDEPENDENT_REVIEWER_IDS},
            "synthesis_started": True,
            "dispositions": [
                {
                    "concern_id": "M-01",
                    "source": "methodology",
                    "disposition": "retained",
                    "rationale": "methods incomplete",
                },
            ],
        }
    )
    if premature.get("ok") or premature.get("error") != "premature_synthesis":
        return gate_result(
            "reviewer_independence",
            False,
            f"premature synthesis not refused: {premature}",
        )

    # Negative: missing DA minority disposition at synthesis
    missing_da = validate_reviewer_stage_state(
        {
            "independents_complete": list(INDEPENDENT_REVIEWER_IDS),
            "visibility": {rid: [] for rid in INDEPENDENT_REVIEWER_IDS},
            "synthesis_started": True,
            "dispositions": [
                {
                    "concern_id": "M-01",
                    "source": "methodology",
                    "disposition": "retained",
                    "rationale": "sample incomplete",
                },
                {
                    "concern_id": "D-01",
                    "source": "domain",
                    "disposition": "retained",
                    "rationale": "related work gap",
                },
                {
                    "concern_id": "I-01",
                    "source": "interdisciplinary",
                    "disposition": "retained",
                    "rationale": "measurement transfer unclear",
                },
            ],
        }
    )
    if missing_da.get("ok") or missing_da.get("error") != "missing_disposition":
        return gate_result(
            "reviewer_independence",
            False,
            f"missing minority disposition not refused: {missing_da}",
        )

    # E3-C: identity / re-review / calibration behavioral fixtures.
    id_pos = evaluate_reviewer_identity(
        {
            "identity_kind": "simulated_role",
            "role_label": "methodology",
            "labeled_simulated": True,
        }
    )
    if not id_pos.get("ok"):
        return gate_result(
            "reviewer_independence",
            False,
            f"identity positive failed: {id_pos}",
        )
    id_neg = evaluate_reviewer_identity(
        {
            "identity_kind": "named_real",
            "display_name": "Dr. Example",
            "identity_source": "",
            "human_confirmation": False,
        }
    )
    if id_neg.get("ok") or id_neg.get("error") not in {
        "missing_identity_source",
        "missing_human_confirmation",
    }:
        return gate_result(
            "reviewer_independence",
            False,
            f"named identity without source/confirm not refused: {id_neg}",
        )
    id_name_only = evaluate_reviewer_identity({"display_name": "Famous Scholar"})
    if id_name_only.get("ok") or id_name_only.get("error") != "missing_identity_kind":
        return gate_result(
            "reviewer_independence",
            False,
            f"display-name-only identity not refused: {id_name_only}",
        )
    id_unlabeled = evaluate_reviewer_identity(
        {
            "identity_kind": "simulated_role",
            "display_name": "Famous Scholar",
        }
    )
    if id_unlabeled.get("ok") or id_unlabeled.get("error") != "unlabeled_simulated":
        return gate_result(
            "reviewer_independence",
            False,
            f"unlabeled simulated identity not refused: {id_unlabeled}",
        )
    id_self = evaluate_reviewer_identity(
        {
            "identity_kind": "named_real",
            "display_name": "Ada",
            "identity_source": "self-asserted",
            "human_confirmation": True,
        }
    )
    if id_self.get("ok") or id_self.get("error") != "forbidden_identity_source":
        return gate_result(
            "reviewer_independence",
            False,
            f"self-asserted identity source not refused: {id_self}",
        )
    # Legitimate provenance must not be rejected by short-token substring false
    # positives (e.g. "na" inside Nature/National/journal).
    for legitimate_source in (
        "Nature staff profile",
        "National university roster",
        "journal masthead",
    ):
        id_legit = evaluate_reviewer_identity(
            {
                "identity_kind": "named_real",
                "display_name": "Ada Reviewer",
                "identity_source": legitimate_source,
                "human_confirmation": True,
            }
        )
        if not id_legit.get("ok"):
            return gate_result(
                "reviewer_independence",
                False,
                f"legitimate identity source refused: {legitimate_source}: {id_legit}",
            )
    id_na = evaluate_reviewer_identity(
        {
            "identity_kind": "named_real",
            "display_name": "Ada Reviewer",
            "identity_source": "n/a",
            "human_confirmation": True,
        }
    )
    if id_na.get("ok") or id_na.get("error") != "forbidden_identity_source":
        return gate_result(
            "reviewer_independence",
            False,
            f"n/a identity source not refused: {id_na}",
        )

    rr_pos = evaluate_rereview_consistency(
        {
            "prior_issues": [
                {"issue_id": "M-01"},
                {"issue_id": "DA-01"},
            ],
            "current_rows": [
                {
                    "issue_id": "M-01",
                    "trajectory": "addressed",
                    "pointer": "ms §3.2 sample size paragraph",
                },
                {
                    "issue_id": "DA-01",
                    "trajectory": "partially_addressed",
                    "pointer": "ms §4 outcome hierarchy note",
                    "residual_gap": "primary outcome hierarchy still incomplete",
                },
                {
                    "issue_id": "N-01",
                    "trajectory": "new",
                    "pointer": "ms §5 new limitation",
                },
            ],
            "claim_all_fixed": False,
        }
    )
    if not rr_pos.get("ok"):
        return gate_result(
            "reviewer_independence",
            False,
            f"re-review positive failed: {rr_pos}",
        )
    rr_neg = evaluate_rereview_consistency(
        {
            "prior_issues": [{"issue_id": "M-01"}, {"issue_id": "DA-01"}],
            "current_rows": [
                {"issue_id": "M-01", "trajectory": "addressed", "pointer": ""},
            ],
            "claim_all_fixed": True,
        }
    )
    if rr_neg.get("ok"):
        return gate_result(
            "reviewer_independence",
            False,
            f"re-review negative not refused: {rr_neg}",
        )
    rr_partial = evaluate_rereview_consistency(
        {
            "prior_issues": [{"issue_id": "M-01"}],
            "current_rows": [
                {
                    "issue_id": "M-01",
                    "trajectory": "partially_addressed",
                    "pointer": "ms §3",
                }
            ],
        }
    )
    if rr_partial.get("ok") or rr_partial.get("error") != "partial_without_residual":
        return gate_result(
            "reviewer_independence",
            False,
            f"partial without residual not refused: {rr_partial}",
        )
    rr_new_offset = evaluate_rereview_consistency(
        {
            "prior_issues": [{"issue_id": "M-01"}, {"issue_id": "DA-01"}],
            "current_rows": [
                {
                    "issue_id": "M-01",
                    "trajectory": "addressed",
                    "pointer": "ms §3",
                },
                {
                    "issue_id": "N-01",
                    "trajectory": "new",
                    "pointer": "ms §5",
                },
            ],
        }
    )
    if (
        rr_new_offset.get("ok")
        or rr_new_offset.get("error") != "missing_prior_coverage"
    ):
        return gate_result(
            "reviewer_independence",
            False,
            f"new issue offsetting prior not refused: {rr_new_offset}",
        )

    cal_pos_labels = [
        {"item_id": f"C{i}", "label": "major" if i % 2 else "minor"}
        for i in range(1, MIN_CALIBRATION_GOLD_ITEMS + 1)
    ]
    cal_pos = evaluate_calibration_gold(
        {
            "gold_labels": cal_pos_labels,
            "predictions": list(cal_pos_labels),
            "session_only": True,
            "fabricated_labels": False,
            "persistent_calibration_claim": False,
        }
    )
    if not cal_pos.get("ok"):
        return gate_result(
            "reviewer_independence",
            False,
            f"calibration positive failed: {cal_pos}",
        )
    cal_neg = evaluate_calibration_gold(
        {
            "gold_labels": [],
            "predictions": [{"item_id": "C1", "label": "major"}],
            "session_only": True,
        }
    )
    if cal_neg.get("ok") or cal_neg.get("error") not in {
        "missing_calibration_gold",
        "empty_gold",
    }:
        return gate_result(
            "reviewer_independence",
            False,
            f"missing calibration gold not refused: {cal_neg}",
        )
    if cal_neg.get("metrics") is not None:
        return gate_result(
            "reviewer_independence",
            False,
            f"invalid calibration leaked metrics: {cal_neg}",
        )
    cal_inadequate = evaluate_calibration_gold(
        {
            "gold_labels": [{"item_id": "C1", "label": "major"}],
            "predictions": [{"item_id": "C1", "label": "major"}],
            "session_only": True,
        }
    )
    if (
        cal_inadequate.get("ok")
        or cal_inadequate.get("error") != "inadequate_gold_set"
        or cal_inadequate.get("metrics") is not None
    ):
        return gate_result(
            "reviewer_independence",
            False,
            f"inadequate calibration gold not refused: {cal_inadequate}",
        )
    # Underpowered two-row set and oversize 21-row set must fail closed.
    cal_two = evaluate_calibration_gold(
        {
            "gold_labels": [
                {"item_id": "C1", "label": "major"},
                {"item_id": "C2", "label": "minor"},
            ],
            "predictions": [
                {"item_id": "C1", "label": "major"},
                {"item_id": "C2", "label": "minor"},
            ],
            "session_only": True,
        }
    )
    if (
        cal_two.get("ok")
        or cal_two.get("error") != "inadequate_gold_set"
        or cal_two.get("metrics") is not None
    ):
        return gate_result(
            "reviewer_independence",
            False,
            f"two-row calibration gold not refused: {cal_two}",
        )
    cal_oversize_labels = [
        {"item_id": f"C{i}", "label": "major" if i % 2 else "minor"}
        for i in range(1, MAX_CALIBRATION_GOLD_ITEMS + 2)
    ]
    cal_oversize = evaluate_calibration_gold(
        {
            "gold_labels": cal_oversize_labels,
            "predictions": list(cal_oversize_labels),
            "session_only": True,
        }
    )
    if (
        cal_oversize.get("ok")
        or cal_oversize.get("error") != "excessive_gold_set"
        or cal_oversize.get("metrics") is not None
    ):
        return gate_result(
            "reviewer_independence",
            False,
            f"21-row calibration gold not refused: {cal_oversize}",
        )

    guided_pos = evaluate_guided_dialogue(
        {
            "turns": [
                {
                    "checkpoint_id": "G1",
                    "question": "What is the primary claim?",
                    "response": "Authors claim X improves Y",
                },
                {
                    "checkpoint_id": "G2",
                    "question": "Is methods detail sufficient?",
                    "response": "Sample size justification missing",
                },
            ]
        }
    )
    if not guided_pos.get("ok"):
        return gate_result(
            "reviewer_independence",
            False,
            f"guided dialogue positive failed: {guided_pos}",
        )
    guided_neg = evaluate_guided_dialogue(
        {
            "oneshot_dump": True,
            "turns": [
                {
                    "checkpoint_id": "G1",
                    "question": "full review?",
                    "response": "here is entire review dump",
                }
            ],
        }
    )
    if guided_neg.get("ok") or guided_neg.get("error") != "oneshot_dump":
        return gate_result(
            "reviewer_independence",
            False,
            f"guided oneshot dump not refused: {guided_neg}",
        )

    protocol_text = _read_methods_surface(methods_root, MANUSCRIPT_REVIEW_PROTOCOL_REL)
    modes_ok, modes_detail = evaluate_all_reviewer_modes_text(protocol_text)
    if not modes_ok:
        return gate_result(
            "reviewer_independence",
            False,
            f"E3-C reviewer modes incomplete: {modes_detail}",
        )

    detail = (
        "fixture order + deterministic reviewer-stage validator "
        "(A20 early_visibility, premature_synthesis, missing_disposition negatives) "
        "+ E3-C identity/re-review/calibration/guided fixtures + six mode fields; "
        "validator coverage only — multi-process execution remains partial"
    )
    return gate_result("reviewer_independence", True, detail, status="pass")


def g_passport_reset_contract(methods_root: Path) -> dict[str, Any]:
    """Execute transition/schema/reset checks via planner validator (not token search)."""
    contract_path = methods_root / "core" / "contracts" / "passport_state.md"
    if not contract_path.is_file():
        return gate_result("passport_reset_contract", False, "passport_state.md missing")
    contract = read_text(contract_path)
    contract_l = contract.lower()
    for token in ("essential_passport_v1", "reset_ledger", "checkpoint_hash", "illegal"):
        if token.lower() not in contract_l and token not in contract:
            return gate_result("passport_reset_contract", False, f"contract missing {token}")
    if "append-only" not in contract_l and "append only" not in contract_l:
        return gate_result("passport_reset_contract", False, "contract missing append-only rule")

    try:
        planner = load_planner_module()
    except Exception as exc:  # noqa: BLE001
        return gate_result("passport_reset_contract", False, f"planner load failed: {exc}")

    # unknown schema
    bad_schema = planner.validate_passport_obj({"schema_id": "nope_v0"})
    if bad_schema.get("ok") or bad_schema.get("error") != "unknown_schema":
        return gate_result(
            "passport_reset_contract",
            False,
            f"unknown schema not refused: {bad_schema}",
        )

    # illegal transition 3 -> 5
    legal_base = {"schema_id": "essential_passport_v1"}
    illegal = planner.validate_passport_obj(legal_base, from_stage="3", to_stage="5")
    if illegal.get("ok") or illegal.get("error") != "illegal_transition":
        return gate_result(
            "passport_reset_contract",
            False,
            f"illegal 3->5 not refused: {illegal}",
        )

    # legal transition 1 -> 2
    legal = planner.validate_passport_obj(legal_base, from_stage="1", to_stage="2")
    if not legal.get("ok"):
        return gate_result(
            "passport_reset_contract",
            False,
            f"legal 1->2 rejected: {legal}",
        )

    # checkpoint mismatch
    mismatched = planner.validate_passport_obj(
        {
            "schema_id": "essential_passport_v1",
            "resume": {"checkpoint_hash": "abc"},
            "last_checkpoint": {"hash": "def"},
        }
    )
    if mismatched.get("ok") or mismatched.get("error") != "missing_checkpoint":
        return gate_result(
            "passport_reset_contract",
            False,
            f"checkpoint mismatch not refused: {mismatched}",
        )

    # reset without flag
    import os

    old_rm = os.environ.pop("RM_PASSPORT_RESET", None)
    old_ars = os.environ.pop("ARS_PASSPORT_RESET", None)
    try:
        reset_no_flag = planner.validate_passport_obj(
            {
                "schema_id": "essential_passport_v1",
                "reset_requested": True,
                "reset_ledger": [],
            }
        )
        if reset_no_flag.get("ok") or reset_no_flag.get("error") != "reset_requires_flag":
            return gate_result(
                "passport_reset_contract",
                False,
                f"reset without flag not refused: {reset_no_flag}",
            )
        os.environ["RM_PASSPORT_RESET"] = "1"

        entry1 = {
            "reset_id": "r1",
            "timestamp": "2026-07-20T00:00:00Z",
            "from_stage": "3",
            "to_stage": "1",
            "from_checkpoint_hash": "x",
            "reason": "test",
            "actor": "human",
            "env_flags_observed": ["RM_PASSPORT_RESET=1"],
        }
        entry2 = {
            "reset_id": "r2",
            "timestamp": "2026-07-20T01:00:00Z",
            "from_stage": "4",
            "to_stage": "1",
            "from_checkpoint_hash": "y",
            "reason": "second",
            "actor": "agent",
            "env_flags_observed": ["RM_PASSPORT_RESET=1"],
        }

        # Positive: exactly one valid append from empty previous
        prev: list[Any] = []
        new_one = [dict(entry1)]
        append_ok = planner.validate_reset_ledger_transition(prev, new_one)
        if not append_ok.get("ok"):
            return gate_result(
                "passport_reset_contract",
                False,
                f"valid single append rejected: {append_ok}",
            )
        # Non-mutation of inputs
        if prev != [] or new_one != [entry1]:
            return gate_result(
                "passport_reset_contract",
                False,
                "validate_reset_ledger_transition mutated inputs",
            )

        # Second valid append
        append2 = planner.validate_reset_ledger_transition([dict(entry1)], [dict(entry1), dict(entry2)])
        if not append2.get("ok"):
            return gate_result(
                "passport_reset_contract",
                False,
                f"second valid append rejected: {append2}",
            )

        # Negative: deletion
        deleted = planner.validate_reset_ledger_transition([dict(entry1), dict(entry2)], [dict(entry1)])
        if deleted.get("ok") or deleted.get("error") != "reset_ledger_delete":
            return gate_result(
                "passport_reset_contract",
                False,
                f"ledger deletion not refused: {deleted}",
            )

        # Negative: mutation of historical entry
        mutated_hist = dict(entry1)
        mutated_hist["reason"] = "tampered"
        mutated = planner.validate_reset_ledger_transition(
            [dict(entry1)],
            [mutated_hist, dict(entry2)],
        )
        if mutated.get("ok") or mutated.get("error") != "reset_ledger_mutation":
            return gate_result(
                "passport_reset_contract",
                False,
                f"ledger mutation not refused: {mutated}",
            )

        # Negative: reorder historical entries
        reordered = planner.validate_reset_ledger_transition(
            [dict(entry1), dict(entry2)],
            [dict(entry2), dict(entry1), dict(entry2)],
        )
        if reordered.get("ok") or reordered.get("error") not in {
            "reset_ledger_reorder",
            "reset_ledger_mutation",
            "reset_ledger_multi_append",
        }:
            # reordering two history + no clean single append should fail
            if reordered.get("ok"):
                return gate_result(
                    "passport_reset_contract",
                    False,
                    f"ledger reorder not refused: {reordered}",
                )

        # Cleaner reorder case: same length with swapped order
        reorder_same_len = planner.validate_reset_ledger_transition(
            [dict(entry1), dict(entry2)],
            [dict(entry2), dict(entry1)],
        )
        if reorder_same_len.get("ok"):
            return gate_result(
                "passport_reset_contract",
                False,
                f"same-length reorder accepted: {reorder_same_len}",
            )

        # Negative: multiple appends
        multi = planner.validate_reset_ledger_transition(
            [],
            [dict(entry1), dict(entry2)],
        )
        if multi.get("ok") or multi.get("error") != "reset_ledger_multi_append":
            return gate_result(
                "passport_reset_contract",
                False,
                f"multi-append not refused: {multi}",
            )

        # Negative: invalid actor
        bad_actor_entry = dict(entry1)
        bad_actor_entry["actor"] = "robot"
        bad_actor = planner.validate_reset_ledger_transition([], [bad_actor_entry])
        if bad_actor.get("ok") or bad_actor.get("error") != "invalid_reset_actor":
            return gate_result(
                "passport_reset_contract",
                False,
                f"invalid actor not refused: {bad_actor}",
            )

        # Negative: missing required field
        missing_field = dict(entry1)
        del missing_field["reason"]
        missing = planner.validate_reset_ledger_transition([], [missing_field])
        if missing.get("ok") or missing.get("error") != "invalid_reset_entry":
            return gate_result(
                "passport_reset_contract",
                False,
                f"missing required field not refused: {missing}",
            )

        # Integrated through validate_passport_obj with previous_reset_ledger
        reset_ok = planner.validate_passport_obj(
            {
                "schema_id": "essential_passport_v1",
                "reset_requested": True,
                "reset_ledger": [dict(entry1)],
            },
            previous_reset_ledger=[],
        )
        if not reset_ok.get("ok"):
            return gate_result(
                "passport_reset_contract",
                False,
                f"reset with flag+append rejected: {reset_ok}",
            )
        reset_bad_ledger = planner.validate_passport_obj(
            {
                "schema_id": "essential_passport_v1",
                "reset_requested": True,
                "reset_ledger": "not-a-list",
            }
        )
        if reset_bad_ledger.get("ok"):
            return gate_result(
                "passport_reset_contract",
                False,
                "non-list reset_ledger accepted",
            )
        reset_multi = planner.validate_passport_obj(
            {
                "schema_id": "essential_passport_v1",
                "reset_requested": True,
                "reset_ledger": [dict(entry1), dict(entry2)],
            },
            previous_reset_ledger=[],
        )
        if reset_multi.get("ok"):
            return gate_result(
                "passport_reset_contract",
                False,
                "passport multi-append accepted",
            )
    finally:
        if old_rm is not None:
            os.environ["RM_PASSPORT_RESET"] = old_rm
        else:
            os.environ.pop("RM_PASSPORT_RESET", None)
        if old_ars is not None:
            os.environ["ARS_PASSPORT_RESET"] = old_ars
        else:
            os.environ.pop("ARS_PASSPORT_RESET", None)

    # checkpoint hash function deterministic
    h1 = planner.checkpoint_hash("p1", "1", "running", ["a.md"], "ok", "t0")
    h2 = planner.checkpoint_hash("p1", "1", "running", ["a.md"], "ok", "t0")
    h3 = planner.checkpoint_hash("p1", "1", "running", ["b.md"], "ok", "t0")
    if h1 != h2 or h1 == h3 or len(h1) != 64:
        return gate_result("passport_reset_contract", False, "checkpoint_hash unstable")

    detail = (
        "behavioral passport checks passed: unknown_schema, illegal_transition, "
        "checkpoint mismatch, reset flag, append-only ledger transition "
        "(delete/reorder/mutation/multi-append/actor/fields), checkpoint_hash; "
        "full pipeline stage machine remains partial until E4"
    )
    return gate_result("passport_reset_contract", True, detail)


def g_evidence_state_vocab(methods_root: Path) -> dict[str, Any]:
    contract = read_text(methods_root / "core" / "contracts" / "evidence_states.md")
    missing = [s for s in EVIDENCE_STATES if s not in contract]
    if missing:
        return gate_result("evidence_state_vocab", False, f"missing states: {missing}")
    return gate_result("evidence_state_vocab", True, "seven evidence states present")


def g_claim_verdict_vocab(methods_root: Path) -> dict[str, Any]:
    """Enum presence plus E3-A citation behavioral fixtures and protocol surface."""
    contract = read_text(methods_root / "core" / "contracts" / "evidence_verdict.md")
    missing = [v for v in CLAIM_VERDICTS if v not in contract]
    if missing:
        return gate_result("claim_verdict_vocab", False, f"missing verdicts: {missing}")

    # Behavioral fixtures embedded so the public gate path is real (E3-A).
    doi_only = {
        "citation_id": "E3A-DOI-ONLY",
        "identity": {
            "title": "Example Study",
            "authors": "A Author",
            "year": "2020",
            "venue": "Example Journal",
            "doi_or_id": "10.1000/example.doi",
        },
        "locator_or_quote": "",
        "extract": "",
        "claim_text": "Treatment improves survival.",
        "access_state": "verified",
        "risk_flags": [],
        "support_status": "supported",
        "assessment_source": "human_confirmed",
        "verdict": "VERIFIED",
    }
    retracted_clean = {
        "citation_id": "E3A-RETRACTED",
        "identity": {
            "title": "Retracted Paper",
            "authors": "B Author",
            "year": "2019",
            "venue": "Example Journal",
            "doi_or_id": "10.1000/retracted",
        },
        "locator_or_quote": "p.4",
        "extract": "authors report improved survival in the treated arm",
        "claim_text": "Treatment improves survival.",
        "access_state": "verified",
        "risk_flags": ["retracted"],
        "support_status": "supported",
        "assessment_source": "human_confirmed",
        "verdict": "VERIFIED",
    }
    good = {
        "citation_id": "E3A-GOOD",
        "identity": {
            "title": "Coherent Study",
            "authors": "C Author",
            "year": "2021",
            "venue": "Example Journal",
            "doi_or_id": "10.1000/good",
        },
        "locator_or_quote": "p.12 §Results",
        "extract": "treated patients had higher overall survival than controls",
        "claim_text": "Treated patients had higher overall survival than controls.",
        "access_state": "verified",
        "risk_flags": [],
        "support_status": "supported",
        "assessment_source": "human_confirmed",
        "verdict": "VERIFIED",
    }
    inaccessible_ok = {
        "citation_id": "E3A-ACCESS-BLOCKED-HONEST",
        "identity": {
            "title": "Paywalled Study",
            "authors": "D Author",
            "year": "2018",
            "venue": "Example Journal",
            "doi_or_id": "10.1000/paywalled",
        },
        "locator_or_quote": "",
        "extract": "",
        "claim_text": "Effect size was large.",
        "access_state": "access_blocked",
        "risk_flags": [],
        "support_status": "unknown",
        "assessment_source": "none",
        "verdict": "UNVERIFIABLE_ACCESS",
    }
    verified_missing_access = {
        "citation_id": "E3A-VERIFIED-NO-ACCESS",
        "identity": {
            "title": "Missing Access Study",
            "authors": "E Author",
            "year": "2022",
            "venue": "Example Journal",
            "doi_or_id": "10.1000/no-access",
        },
        "locator_or_quote": "p.3",
        "extract": "treated patients had higher overall survival than controls",
        "claim_text": "Treated patients had higher overall survival than controls.",
        "access_state": "",
        "risk_flags": [],
        "support_status": "supported",
        "assessment_source": "human_confirmed",
        "verdict": "VERIFIED",
    }
    verified_unverified_access = {
        "citation_id": "E3A-VERIFIED-UNVERIFIED-ACCESS",
        "identity": {
            "title": "Unverified Access Study",
            "authors": "F Author",
            "year": "2022",
            "venue": "Example Journal",
            "doi_or_id": "10.1000/unverified-access",
        },
        "locator_or_quote": "p.5",
        "extract": "treated patients had higher overall survival than controls",
        "claim_text": "Treated patients had higher overall survival than controls.",
        "access_state": "unverified",
        "risk_flags": [],
        "support_status": "supported",
        "assessment_source": "human_confirmed",
        "verdict": "VERIFIED",
    }
    access_verdict_mismatch = {
        "citation_id": "E3A-UVA-VERIFIED-ACCESS",
        "identity": {
            "title": "Access Verdict Mismatch",
            "authors": "G Author",
            "year": "2020",
            "venue": "Example Journal",
            "doi_or_id": "10.1000/uva-mismatch",
        },
        "locator_or_quote": "",
        "extract": "",
        "claim_text": "Effect size was large.",
        "access_state": "verified",
        "risk_flags": [],
        "support_status": "unknown",
        "assessment_source": "none",
        "verdict": "UNVERIFIABLE_ACCESS",
    }
    eoc_clean = {
        "citation_id": "E3A-EOC-CLEAN",
        "identity": {
            "title": "Expression of Concern Paper",
            "authors": "H Author",
            "year": "2017",
            "venue": "Example Journal",
            "doi_or_id": "10.1000/eoc",
        },
        "locator_or_quote": "p.2",
        "extract": "treated patients had higher overall survival than controls",
        "claim_text": "Treated patients had higher overall survival than controls.",
        "access_state": "verified",
        "risk_flags": ["expression_of_concern"],
        "support_status": "supported",
        "assessment_source": "human_confirmed",
        "verdict": "VERIFIED",
    }

    bad_doi = evaluate_citation_record(doi_only)
    if bad_doi.get("ok"):
        return gate_result(
            "claim_verdict_vocab",
            False,
            "citation behavioral: DOI-only VERIFIED fixture unexpectedly passed",
        )
    if bad_doi.get("error") not in {
        "doi_alone_insufficient",
        "verified_without_extract",
        "verified_missing_locator_or_extract",
    }:
        return gate_result(
            "claim_verdict_vocab",
            False,
            f"citation behavioral: DOI-only expected locator/extract fail, got {bad_doi}",
        )

    bad_ret = evaluate_citation_record(retracted_clean)
    if bad_ret.get("ok") or bad_ret.get("error") != "retracted_marked_clean":
        return gate_result(
            "claim_verdict_vocab",
            False,
            f"citation behavioral: retracted-clean fixture failed wrongly: {bad_ret}",
        )

    good_res = evaluate_citation_record(good)
    if not good_res.get("ok"):
        return gate_result(
            "claim_verdict_vocab",
            False,
            f"citation behavioral: coherent VERIFIED fixture failed: {good_res}",
        )

    access_res = evaluate_citation_record(inaccessible_ok)
    if not access_res.get("ok"):
        return gate_result(
            "claim_verdict_vocab",
            False,
            f"citation behavioral: honest access-blocked fixture failed: {access_res}",
        )

    miss_acc = evaluate_citation_record(verified_missing_access)
    if miss_acc.get("ok") or miss_acc.get("error") != "unknown_access_state":
        return gate_result(
            "claim_verdict_vocab",
            False,
            f"citation behavioral: missing access_state fixture: {miss_acc}",
        )

    unver_acc = evaluate_citation_record(verified_unverified_access)
    if unver_acc.get("ok") or unver_acc.get("error") != "verdict_access_incoherent":
        return gate_result(
            "claim_verdict_vocab",
            False,
            f"citation behavioral: VERIFIED+unverified access fixture: {unver_acc}",
        )

    uva_mismatch = evaluate_citation_record(access_verdict_mismatch)
    if uva_mismatch.get("ok") or uva_mismatch.get("error") != "verdict_access_incoherent":
        return gate_result(
            "claim_verdict_vocab",
            False,
            f"citation behavioral: UNVERIFIABLE_ACCESS+verified fixture: {uva_mismatch}",
        )

    eoc_res = evaluate_citation_record(eoc_clean)
    if eoc_res.get("ok") or eoc_res.get("error") != "expression_of_concern_clean":
        return gate_result(
            "claim_verdict_vocab",
            False,
            f"citation behavioral: expression_of_concern clean fixture: {eoc_res}",
        )

    empty_agg = evaluate_citation_records([])
    if empty_agg.get("ok") or empty_agg.get("error") != "empty_records":
        return gate_result(
            "claim_verdict_vocab",
            False,
            f"citation behavioral: empty aggregate fixture: {empty_agg}",
        )

    protocol_text = _read_methods_surface(methods_root, CITATION_PROTOCOL_REL)
    pok, pdetail = evaluate_citation_integrity_protocol_text(protocol_text)
    if not pok:
        return gate_result(
            "claim_verdict_vocab",
            False,
            f"citation protocol surface: {CITATION_PROTOCOL_REL}: {pdetail}",
        )

    return gate_result(
        "claim_verdict_vocab",
        True,
        "claim verdict enum present; citation behavioral/coherence fixtures + protocol surface ok",
    )


def g_hook_safety(methods_root: Path) -> dict[str, Any]:
    hook_py = read_text(methods_root / "runtime" / "scripts" / "essential_hook.py")
    hooks_json = read_text(methods_root / "runtime" / "hooks" / "hooks.json")
    readme = read_text(methods_root / "runtime" / "hooks" / "README.md")
    banned = [
        r"os\.environ\[",
        r"requests\.",
        r"urllib\.request",
        r"subprocess\.",
        r"socket\.",
        r"Path\(.*\)\.write",
    ]
    for pat in banned:
        if re.search(pat, hook_py):
            return gate_result("hook_safety", False, f"unsafe pattern in hook: {pat}")
    if '"network": false' not in hooks_json:
        return gate_result("hook_safety", False, "hooks.json missing network false")
    if "secret" not in readme.lower():
        return gate_result("hook_safety", False, "README missing secret boundary")
    return gate_result("hook_safety", True, "hook is read-only and secret-safe by static rules")


def g_optional_runtime_honesty(methods_root: Path) -> dict[str, Any]:
    optional = methods_root / "core" / "protocols" / "optional_runtime.md"
    planner = read_text(methods_root / "runtime" / "scripts" / "essential_full_runtime.py")
    text = read_text(optional) if optional.is_file() else ""
    if "missing" not in text.lower() and "missing_backends" not in planner:
        return gate_result("optional_runtime_honesty", False, "missing-backend honesty absent")
    if "missing_backends" not in planner:
        return gate_result("optional_runtime_honesty", False, "planner missing_backends absent")
    return gate_result("optional_runtime_honesty", True, "offline honesty markers present")


def g_generator_evaluator_separation(methods_root: Path) -> dict[str, Any]:
    """Contract tokens plus embedded revision/rebuttal behavioral fixtures (E3-B)."""
    contract = read_text(methods_root / "core" / "contracts" / "generator_evaluator.md")
    lower = contract.lower()
    if "rebuttal-audit" not in contract or "pre-commit" not in lower:
        return gate_result(
            "generator_evaluator_separation",
            False,
            "contract missing rebuttal-audit or pre-commit rules",
        )
    if "protected" not in lower or "revision" not in lower:
        return gate_result(
            "generator_evaluator_separation",
            False,
            "contract missing revision/protected-claim rules",
        )

    # Positive revision: ledgered replace of non-protected sentence; hedges kept.
    rev_pos = evaluate_revision_transition(
        {
            "before_text": (
                "Treatment may improve survival in subgroup A. "
                "We also note secondary endpoint X was exploratory."
            ),
            "after_text": (
                "Treatment may improve survival in subgroup A. "
                "We also note secondary endpoint X was pre-specified as exploratory."
            ),
            "protected_claims": [],
            "protected_hedges": ["Treatment may improve survival in subgroup A."],
            "change_ledger": [
                {
                    "change_id": "c1",
                    "op": "replace",
                    "target": "secondary endpoint X was exploratory",
                    "summary": "secondary endpoint X was pre-specified as exploratory",
                }
            ],
            "new_evidence_rows": [],
            "author_signoff": True,
            "recovery_checkpoint": "ckpt-1",
        }
    )
    if not rev_pos.get("ok"):
        return gate_result(
            "generator_evaluator_separation",
            False,
            f"revision/rebuttal behavioral: positive revision failed: {rev_pos}",
        )

    rev_neg = evaluate_revision_transition(
        {
            "before_text": "Treatment may improve survival in subgroup A.",
            "after_text": "Treatment improves survival in subgroup A.",
            "protected_claims": [],
            "protected_hedges": ["Treatment may improve survival in subgroup A."],
            "change_ledger": [],
            "new_evidence_rows": [],
            "author_signoff": True,
            "recovery_checkpoint": "ckpt-1",
        }
    )
    if rev_neg.get("ok"):
        return gate_result(
            "generator_evaluator_separation",
            False,
            "revision/rebuttal behavioral: protected hedge deletion/strengthen should fail",
        )
    if rev_neg.get("error") not in {
        "protected_claim_deleted",
        "protected_claim_strengthened",
    }:
        return gate_result(
            "generator_evaluator_separation",
            False,
            f"revision transition failed: unexpected error {rev_neg.get('error')}",
        )

    # Add/move/annotate ledger truth + unique change_id (E3-B revision-2).
    add_pos = evaluate_revision_transition(
        {
            "before_text": "Treatment may improve survival in subgroup A.",
            "after_text": (
                "Treatment may improve survival in subgroup A. "
                "We added a pre-specified sensitivity analysis."
            ),
            "protected_claims": [],
            "protected_hedges": [],
            "change_ledger": [
                {
                    "change_id": "c-add-1",
                    "op": "add",
                    "target": "",
                    "summary": "We added a pre-specified sensitivity analysis.",
                }
            ],
            "new_evidence_rows": [],
            "author_signoff": True,
            "recovery_checkpoint": "ckpt-1",
        }
    )
    if not add_pos.get("ok"):
        return gate_result(
            "generator_evaluator_separation",
            False,
            f"revision ledger truth: positive add failed: {add_pos}",
        )

    add_already = evaluate_revision_transition(
        {
            "before_text": (
                "Treatment may improve survival in subgroup A. "
                "We added a pre-specified sensitivity analysis."
            ),
            "after_text": (
                "Treatment may improve survival in subgroup A. "
                "We added a pre-specified sensitivity analysis."
            ),
            "protected_claims": [],
            "protected_hedges": [],
            "change_ledger": [
                {
                    "change_id": "c-add-false",
                    "op": "add",
                    "target": "",
                    "summary": "We added a pre-specified sensitivity analysis.",
                }
            ],
            "new_evidence_rows": [],
            "author_signoff": True,
            "recovery_checkpoint": "ckpt-1",
        }
    )
    if add_already.get("ok") or add_already.get("error") != "false_ledger_claim":
        return gate_result(
            "generator_evaluator_separation",
            False,
            (
                "revision ledger truth: add with summary already present "
                f"should fail, got {add_already}"
            ),
        )

    move_pos = evaluate_revision_transition(
        {
            "before_text": (
                "Background note. "
                "MOVED_CLAIM_SPAN is here. "
                "Closing note."
            ),
            "after_text": (
                "Background note. "
                "Closing note. "
                "MOVED_CLAIM_SPAN is here."
            ),
            "protected_claims": [],
            "protected_hedges": [],
            "change_ledger": [
                {
                    "change_id": "c-move-1",
                    "op": "move",
                    "target": "MOVED_CLAIM_SPAN is here.",
                    "summary": "Relocated claim span after closing note.",
                }
            ],
            "new_evidence_rows": [],
            "author_signoff": True,
            "recovery_checkpoint": "ckpt-1",
        }
    )
    if not move_pos.get("ok"):
        return gate_result(
            "generator_evaluator_separation",
            False,
            f"revision ledger truth: positive move failed: {move_pos}",
        )

    move_absent = evaluate_revision_transition(
        {
            "before_text": "Only before content here.",
            "after_text": "Only before content here. Unrelated summary appears.",
            "protected_claims": [],
            "protected_hedges": [],
            "change_ledger": [
                {
                    "change_id": "c-move-false",
                    "op": "move",
                    "target": "Nonexistent target span.",
                    "summary": "Unrelated summary appears.",
                }
            ],
            "new_evidence_rows": [],
            "author_signoff": True,
            "recovery_checkpoint": "ckpt-1",
        }
    )
    if move_absent.get("ok") or move_absent.get("error") != "false_ledger_claim":
        return gate_result(
            "generator_evaluator_separation",
            False,
            (
                "revision ledger truth: move with absent target "
                f"should fail, got {move_absent}"
            ),
        )

    annotate_pos = evaluate_revision_transition(
        {
            "before_text": (
                "Treatment may improve survival in subgroup A. "
                "Secondary endpoint X was exploratory."
            ),
            "after_text": (
                "Treatment may improve survival in subgroup A. "
                "Secondary endpoint X was exploratory."
            ),
            "protected_claims": [],
            "protected_hedges": [],
            "change_ledger": [
                {
                    "change_id": "c-ann-1",
                    "op": "annotate",
                    "target": "Secondary endpoint X was exploratory.",
                    "summary": "Editor note: retain exploratory wording.",
                }
            ],
            "new_evidence_rows": [],
            "author_signoff": True,
            "recovery_checkpoint": "ckpt-1",
        }
    )
    if not annotate_pos.get("ok"):
        return gate_result(
            "generator_evaluator_separation",
            False,
            f"revision ledger truth: positive annotate failed: {annotate_pos}",
        )

    annotate_ghost = evaluate_revision_transition(
        {
            "before_text": "Only before content here.",
            "after_text": "Only after content here.",
            "protected_claims": [],
            "protected_hedges": [],
            "change_ledger": [
                {
                    "change_id": "c-ann-false",
                    "op": "annotate",
                    "target": "Ghost target never present.",
                    "summary": "note",
                }
            ],
            "new_evidence_rows": [],
            "author_signoff": True,
            "recovery_checkpoint": "ckpt-1",
        }
    )
    if (
        annotate_ghost.get("ok")
        or annotate_ghost.get("error") != "false_ledger_claim"
    ):
        return gate_result(
            "generator_evaluator_separation",
            False,
            (
                "revision ledger truth: annotate with missing target "
                f"should fail, got {annotate_ghost}"
            ),
        )

    dup_change_id = evaluate_revision_transition(
        {
            "before_text": "Alpha sentence. Beta sentence.",
            "after_text": (
                "Alpha sentence. Beta sentence. "
                "New gamma sentence."
            ),
            "protected_claims": [],
            "protected_hedges": [],
            "change_ledger": [
                {
                    "change_id": "dup-id",
                    "op": "add",
                    "target": "",
                    "summary": "New gamma sentence.",
                },
                {
                    "change_id": "dup-id",
                    "op": "annotate",
                    "target": "Alpha sentence.",
                    "summary": "note",
                },
            ],
            "new_evidence_rows": [],
            "author_signoff": True,
            "recovery_checkpoint": "ckpt-1",
        }
    )
    if (
        dup_change_id.get("ok")
        or dup_change_id.get("error") != "duplicate_change_id"
    ):
        return gate_result(
            "generator_evaluator_separation",
            False,
            (
                "revision ledger truth: duplicate change_id should fail, "
                f"got {dup_change_id}"
            ),
        )

    reb_pos = evaluate_rebuttal_consistency(
        {
            "reviewer_points": [
                {"point_id": "R1", "text": "Clarify sample size."},
                {"point_id": "R2", "text": "Discuss limitation L."},
            ],
            "rebuttal_rows": [
                {
                    "point_id": "R1",
                    "coverage": "covered",
                    "response_kind": "ms_change",
                    "pointer": "§Methods sample size paragraph",
                },
                {
                    "point_id": "R2",
                    "coverage": "covered",
                    "response_kind": "no_change_rationale",
                    "pointer": "Limitation L is out of scope for this cohort.",
                },
            ],
            "change_ledger": [
                {
                    "change_id": "ch-r1",
                    "point_ids": ["R1"],
                    "summary": "Added sample size justification",
                }
            ],
            "evidence_pointers": [],
        }
    )
    if not reb_pos.get("ok"):
        return gate_result(
            "generator_evaluator_separation",
            False,
            f"revision/rebuttal behavioral: positive rebuttal failed: {reb_pos}",
        )

    reb_missing = evaluate_rebuttal_consistency(
        {
            "reviewer_points": [
                {"point_id": "R1", "text": "Clarify sample size."},
                {"point_id": "R2", "text": "Discuss limitation L."},
            ],
            "rebuttal_rows": [
                {
                    "point_id": "R1",
                    "coverage": "covered",
                    "response_kind": "evidence",
                    "pointer": "Table 2",
                }
            ],
            "change_ledger": [],
            "evidence_pointers": [],
        }
    )
    if reb_missing.get("ok") or reb_missing.get("error") != "missing_point_row":
        return gate_result(
            "generator_evaluator_separation",
            False,
            f"revision/rebuttal behavioral: missing point should fail, got {reb_missing}",
        )

    reb_false = evaluate_rebuttal_consistency(
        {
            "reviewer_points": [{"point_id": "R1", "text": "Clarify sample size."}],
            "rebuttal_rows": [
                {
                    "point_id": "R1",
                    "coverage": "covered",
                    "response_kind": "ms_change",
                    "pointer": "§Methods",
                }
            ],
            "change_ledger": [],
            "evidence_pointers": [],
        }
    )
    if reb_false.get("ok") or reb_false.get("error") != "asserted_change_absent":
        return gate_result(
            "generator_evaluator_separation",
            False,
            f"revision/rebuttal behavioral: false change should fail, got {reb_false}",
        )

    # Disclosure record: coherent final package passes; auto-fill / pending final fail.
    disc_pos = evaluate_disclosure_record(
        {
            "package_state": "final",
            "credit_authorship": {
                "details": "Author A: conceptualization, writing – original draft",
            },
            "funding": {"status": "none_confirmed", "details": ""},
            "conflicts": {"status": "none_confirmed", "details": ""},
            "ai_assistance": {
                "status": "disclosed",
                "details": "Editor model used for grammar only",
            },
            "data_code_availability": {
                "status": "restricted",
                "details": "De-identified data on request under DUA",
            },
            "policy_anchor_or_venue": {
                "status": "yes",
                "details": "Journal X disclosure checklist v2",
            },
            "human_confirmation": True,
            "signer": "Author A",
            "timestamp": "2026-07-20T07:00:00Z",
            "auto_filled": False,
            "self_confirmed": False,
        }
    )
    if not disc_pos.get("ok"):
        return gate_result(
            "generator_evaluator_separation",
            False,
            f"revision/rebuttal/disclosure behavioral: positive disclosure failed: {disc_pos}",
        )

    disc_auto = evaluate_disclosure_record(
        {
            "package_state": "draft",
            "credit_authorship": {"details": "Author A: writing"},
            "funding": {"status": "funded", "details": "Grant X"},
            "conflicts": {"status": "none_confirmed", "details": ""},
            "ai_assistance": {"status": "none_confirmed", "details": ""},
            "data_code_availability": {
                "status": "available",
                "details": "https://example.org/data",
            },
            "policy_anchor_or_venue": {"status": "unknown", "details": ""},
            "human_confirmation": True,
            "signer": "Author A",
            "timestamp": "2026-07-20T07:00:00Z",
            "auto_filled": True,
            "self_confirmed": False,
        }
    )
    if disc_auto.get("ok") or disc_auto.get("error") != "auto_filled_forbidden":
        return gate_result(
            "generator_evaluator_separation",
            False,
            f"disclosure behavioral: auto_filled should fail, got {disc_auto}",
        )

    disc_pending_final = evaluate_disclosure_record(
        {
            "package_state": "final",
            "credit_authorship": {"details": "Author A: writing"},
            "funding": {"status": "unknown_pending_human", "details": ""},
            "conflicts": {"status": "none_confirmed", "details": ""},
            "ai_assistance": {
                "status": "disclosed",
                "details": "Grammar assist",
            },
            "data_code_availability": {
                "status": "blocked",
                "details": "Embargo until publication",
            },
            "policy_anchor_or_venue": {
                "status": "yes",
                "details": "Venue Y",
            },
            "human_confirmation": True,
            "signer": "Author A",
            "timestamp": "2026-07-20T07:00:00Z",
        }
    )
    if (
        disc_pending_final.get("ok")
        or disc_pending_final.get("error") != "unknown_pending_blocks_final"
    ):
        return gate_result(
            "generator_evaluator_separation",
            False,
            (
                "disclosure behavioral: unknown_pending_human must block final, "
                f"got {disc_pending_final}"
            ),
        )

    return gate_result(
        "generator_evaluator_separation",
        True,
        (
            "gen/eval separation contract + revision/rebuttal/disclosure "
            "+ ledger add/move/annotate fixtures ok"
        ),
    )


def g_upstream_provenance(methods_root: Path) -> dict[str, Any]:
    notice = methods_root / "NOTICE.md"
    lineage = methods_root / "LINEAGE_INDEX.md"
    license_path = REPO_ROOT / "docs" / "licenses" / "academic-research-skills-license.txt"
    if not notice.is_file() or not lineage.is_file():
        return gate_result("upstream_provenance", False, "NOTICE or LINEAGE_INDEX missing")
    notice_text = read_text(notice)
    if "CC BY-NC" not in notice_text and "CC BY-NC-4.0" not in notice_text:
        return gate_result("upstream_provenance", False, "NOTICE missing CC BY-NC note")
    if "first-party" not in notice_text.lower() and "first-party" not in read_text(lineage).lower():
        return gate_result("upstream_provenance", False, "first-party rewrite claim missing")
    if not license_path.is_file():
        return gate_result("upstream_provenance", False, "license text missing on disk")
    if "not" not in notice_text.lower():
        return gate_result("upstream_provenance", False, "NOTICE should deny full-tree bundle")
    return gate_result("upstream_provenance", True, "NOTICE + lineage + license present")


def g_file_lineage_headers(methods_root: Path) -> dict[str, Any]:
    missing: list[str] = []
    for folder in ("contracts", "protocols", "teams", "templates"):
        base = methods_root / "core" / folder
        for path in sorted(base.glob("*.md")):
            text = read_text(path)
            if "essential_core_lineage:" not in text:
                missing.append(path.relative_to(methods_root).as_posix())
    agents = methods_root / "runtime" / "agents"
    for path in sorted(agents.glob("*.md")):
        text = read_text(path)
        if "essential_core_lineage:" not in text:
            missing.append(path.relative_to(methods_root).as_posix())
    # Plan requires the three runtime scripts to carry lineage headers too.
    for script_name in (
        "essential_full_runtime.py",
        "essential_hook.py",
        "essential_quality_gates.py",
    ):
        path = methods_root / "runtime" / "scripts" / script_name
        text = read_text(path)
        if "essential_core_lineage:" not in text:
            missing.append(path.relative_to(methods_root).as_posix())
    if missing:
        return gate_result("file_lineage_headers", False, f"missing headers: {missing[:12]}")
    return gate_result(
        "file_lineage_headers",
        True,
        "lineage headers present on core + runtime agents + three runtime scripts",
    )


def _depth_failure_reason(path: Path, text: str, *, kind: str) -> str | None:
    """Return failure reason or None if depth is acceptable."""
    if "parity: not_started" in text and kind == "protocol":
        # E2 protocols must not use this exemption; E3/E4 may remain not_started.
        if path.name in E2_PROTOCOL_NAMES:
            pass
        else:
            return None
    prose = prose_body(text)
    headings = heading_list(text)
    sections = h23_section_bodies(text)

    if len(prose) == 0 and len(headings) >= 1:
        return "heading-only"
    if len(prose) == 0:
        return "empty body"
    if len(headings) >= 1 and len(prose) < MIN_PROSE_NONEMPTY:
        return "heading-only"
    if kind in {"contract", "team", "registry", "skill"}:
        if len(headings) >= 3 and len(prose) < MIN_PROSE_STRICT:
            return f"prose {len(prose)} < {MIN_PROSE_STRICT} with {len(headings)} headings"
        if len(prose) < MIN_PROSE_STRICT and len(headings) < 2:
            return f"insufficient structure/prose ({len(headings)} headings, {len(prose)} prose)"
        if len(prose) < 200:
            return f"prose too short ({len(prose)})"
        if sections:
            thin = sum(1 for s in sections if len(s) < MIN_SECTION_BODY)
            if thin / len(sections) > MAX_THIN_SECTION_RATIO:
                return f"thin sections {thin}/{len(sections)}"
    elif kind == "template":
        if len(prose) < MIN_PROSE_TEMPLATE:
            return f"template prose too short ({len(prose)})"
        if len(headings) >= 3 and len(prose) < 200:
            return f"template heading-heavy with short prose ({len(prose)})"
    elif kind == "protocol":
        if len(prose) < MIN_PROSE_TEMPLATE:
            return f"protocol prose too short ({len(prose)})"
        if sections:
            thin = sum(1 for s in sections if len(s) < MIN_SECTION_BODY)
            if thin / len(sections) > MAX_THIN_SECTION_RATIO:
                return f"thin sections {thin}/{len(sections)}"
    return None


def evaluate_content_depth_text(text: str, *, kind: str) -> tuple[bool, str]:
    """Public helper for mutation tests."""
    reason = _depth_failure_reason(Path("mutated.md"), text, kind=kind)
    if reason is None:
        return True, "ok"
    return False, reason


def g_content_depth(methods_root: Path) -> dict[str, Any]:
    """Reject empty, heading-only, and too-short instructional bodies.

    E2 protocols (RQ/deep/SR), E3-A citation_integrity, E3-B academic_paper, and
    E3-C manuscript_review are never exempt when present. Remaining E4/E5
    protocols marked parity: not_started stay exempt. Designated citation,
    paper, and review surfaces run isolated field helpers.
    """
    failures: list[str] = []
    exempt: list[str] = []

    checks: list[tuple[Path, str]] = []
    for path in sorted((methods_root / "core" / "contracts").glob("*.md")):
        checks.append((path, "contract"))
    for path in sorted((methods_root / "core" / "teams").glob("*.md")):
        checks.append((path, "team"))
    for path in sorted((methods_root / "core" / "templates").glob("*.md")):
        checks.append((path, "template"))
    for path in sorted((methods_root / "core" / "protocols").glob("*.md")):
        checks.append((path, "protocol"))
    checks.append((methods_root / "MODE_REGISTRY.md", "registry"))
    checks.append((methods_root / "SKILL.md", "skill"))

    non_exempt_protocols = (
        E2_PROTOCOL_NAMES
        | E3A_PROTOCOL_NAMES
        | E3B_PROTOCOL_NAMES
        | E3C_PROTOCOL_NAMES
    )

    for path, kind in checks:
        if not path.is_file():
            failures.append(f"{path.name}:missing")
            continue
        text = read_text(path)
        if (
            kind == "protocol"
            and "parity: not_started" in text
            and path.name not in non_exempt_protocols
        ):
            exempt.append(path.name)
            continue
        reason = _depth_failure_reason(path, text, kind=kind)
        if reason is not None:
            failures.append(f"{path.name}:{reason}")

    # E3-A designated citation surfaces: field depth isolation.
    citation_checks = (
        (
            CITATION_PROTOCOL_REL,
            evaluate_citation_integrity_protocol_text,
        ),
        (
            CITATION_AUDIT_REL,
            evaluate_citation_audit_template_text,
        ),
        (
            CLAIM_REPORT_REL,
            evaluate_claim_report_template_text,
        ),
    )
    for rel, evaluator in citation_checks:
        text = _read_methods_surface(methods_root, rel)
        ok, detail = evaluator(text)
        if not ok:
            failures.append(f"{rel}:{detail}")

    # E3-B academic paper modes + designated revision/rebuttal/disclosure templates.
    paper_text = _read_methods_surface(methods_root, ACADEMIC_PAPER_PROTOCOL_REL)
    paper_ok, paper_detail = evaluate_all_paper_modes_text(paper_text)
    if not paper_ok:
        failures.append(f"{ACADEMIC_PAPER_PROTOCOL_REL}:{paper_detail}")

    paper_template_checks = (
        (REVISION_TEMPLATE_REL, evaluate_revision_template_text),
        (REBUTTAL_TEMPLATE_REL, evaluate_rebuttal_template_text),
        (DISCLOSURE_TEMPLATE_REL, evaluate_disclosure_template_text),
    )
    for rel, evaluator in paper_template_checks:
        text = _read_methods_surface(methods_root, rel)
        ok, detail = evaluator(text)
        if not ok:
            failures.append(f"{rel}:{detail}")

    # E3-C manuscript-review modes + designated review templates.
    review_text = _read_methods_surface(methods_root, MANUSCRIPT_REVIEW_PROTOCOL_REL)
    review_ok, review_detail = evaluate_all_reviewer_modes_text(review_text)
    if not review_ok:
        failures.append(f"{MANUSCRIPT_REVIEW_PROTOCOL_REL}:{review_detail}")

    review_template_checks = (
        (MANUSCRIPT_REVIEW_TEMPLATE_REL, evaluate_manuscript_review_template_text),
        (EDITORIAL_DECISION_TEMPLATE_REL, evaluate_editorial_decision_template_text),
    )
    for rel, evaluator in review_template_checks:
        text = _read_methods_surface(methods_root, rel)
        ok, detail = evaluator(text)
        if not ok:
            failures.append(f"{rel}:{detail}")

    if failures:
        return gate_result("content_depth", False, f"depth failures: {failures[:12]}")
    return gate_result(
        "content_depth",
        True,
        f"depth ok including E2 + E3-A citation + E3-B paper + E3-C review surfaces; "
        f"not_started E4/E5 protocols exempt ({len(exempt)}): {', '.join(exempt[:6])}",
    )


def _non_ws_len(text: str) -> int:
    return len(re.sub(r"\s+", "", text or ""))


def _labeled_field_patterns(field_id: str) -> list[str]:
    """Return regex patterns that capture labeled field heading + body."""
    fid = re.escape(field_id)
    return [
        # ### field_id  OR  ### `field_id` Title
        rf"(?m)^(#{{1,6}}\s+`?{fid}`?(?:[ \t]+[^\n]*)?\n)([\s\S]*?)(?=^#{{1,6}}\s|\Z)",
        # **field_id** prompt
        rf"(?m)^(\*\*`?{fid}`?\*\*[ \t]*[:\u2014\u2013\-]?[ \t]*)([^\n]*(?:\n(?!\*\*`?[a-z0-9_]+`?\*\*|#{{1,6}}\s)[^\n]*)*)",
        # `field_id`: instructional body (possibly multi-line until next label/heading)
        rf"(?m)^(`{fid}`[ \t]*[:\u2014\u2013\-][ \t]*)([\s\S]*?)(?=^`[a-z0-9_]+`[ \t]*[:\u2014\u2013\-]|^#{{1,6}}\s|\Z)",
        # field_id: instructional body on its own line label
        rf"(?m)^({fid}[ \t]*[:\u2014\u2013\-][ \t]*)([\s\S]*?)(?=^[a-z0-9_]+[ \t]*[:\u2014\u2013\-]|^#{{1,6}}\s|\Z)",
    ]


def extract_labeled_field_match(text: str, field_id: str) -> re.Match[str] | None:
    """Return the longest labeled-field match (full match includes label/heading)."""
    body = strip_lineage_comments(text)
    # Body capture uses [\s\S] instead of (?s). so heading-line parts stay single-line.
    best: re.Match[str] | None = None
    best_len = -1
    for pattern in _labeled_field_patterns(field_id):
        for match in re.finditer(pattern, body):
            chunk = match.group(2).strip()
            n = _non_ws_len(chunk)
            if n > best_len:
                best = match
                best_len = n
    return best


def extract_first_labeled_field_match(
    text: str, field_id: str
) -> re.Match[str] | None:
    """Return the earliest labeled-field match so later duplicates cannot rescue."""
    body = strip_lineage_comments(text)
    best: re.Match[str] | None = None
    best_start: int | None = None
    for pattern in _labeled_field_patterns(field_id):
        for match in re.finditer(pattern, body):
            start = match.start()
            if best is None or (best_start is not None and start < best_start):
                best = match
                best_start = start
    return best


def field_body_ok_first(
    text: str, field_id: str, *, min_chars: int = MIN_FIELD_BODY
) -> tuple[bool, str]:
    """Check the first labeled occurrence has a real body (no later-field rescue)."""
    match = extract_first_labeled_field_match(text, field_id)
    if match is None:
        return False, f"missing labeled block for {field_id}"
    chunk = match.group(2).strip()
    n = _non_ws_len(chunk)
    if n < min_chars:
        return False, f"{field_id} body non-ws {n} < {min_chars}"
    stripped = re.sub(r"[\W_]+", "", chunk, flags=re.I).lower()
    if stripped in {field_id.replace("_", "").lower(), "todo", "tbd", "placeholder"}:
        return False, f"{field_id} body is placeholder-only"
    return True, f"{field_id} ok ({n})"


def evaluate_required_fields_first(
    text: str,
    field_ids: tuple[str, ...] | list[str],
    *,
    min_chars: int = MIN_FIELD_BODY,
) -> tuple[bool, str, list[str]]:
    """Evaluate required fields using first occurrence only (E3-C isolation)."""
    missing: list[str] = []
    for fid in field_ids:
        ok, reason = field_body_ok_first(text, fid, min_chars=min_chars)
        if not ok:
            missing.append(reason)
    if missing:
        return False, f"field failures: {missing[:8]}", missing
    return True, f"all {len(field_ids)} fields present with body>={min_chars}", []


def extract_labeled_field_body(text: str, field_id: str) -> str | None:
    """Return instructional body after a labeled field block, or None if absent.

    Accepts heading, bold, or labeled ``field_id`` blocks. A field ID that
    appears only inside an index/backtick list without its own labeled block
    does not yield a body. Same-line title suffixes use non-dotall matching so
    instructional paragraphs are not swallowed into the heading line.
    """
    match = extract_labeled_field_match(text, field_id)
    if match is None:
        return None
    return match.group(2).strip()


def extract_labeled_field_block(text: str, field_id: str) -> str | None:
    """Return heading/label line plus body for local cue checks (E2-R2)."""
    match = extract_labeled_field_match(text, field_id)
    if match is None:
        return None
    return (match.group(1) + match.group(2)).strip()


def field_body_ok(text: str, field_id: str, *, min_chars: int = MIN_FIELD_BODY) -> tuple[bool, str]:
    """Check one labeled field has a real instructional body."""
    chunk = extract_labeled_field_body(text, field_id)
    if chunk is None:
        return False, f"missing labeled block for {field_id}"
    n = _non_ws_len(chunk)
    if n < min_chars:
        return False, f"{field_id} body non-ws {n} < {min_chars}"
    # Reject body that is only the field name repeated or pure placeholders
    stripped = re.sub(r"[\W_]+", "", chunk, flags=re.I).lower()
    if stripped in {field_id.replace("_", "").lower(), "todo", "tbd", "placeholder"}:
        return False, f"{field_id} body is placeholder-only"
    return True, f"{field_id} ok ({n})"


def evaluate_required_fields(
    text: str,
    field_ids: tuple[str, ...] | list[str],
    *,
    min_chars: int = MIN_FIELD_BODY,
) -> tuple[bool, str, list[str]]:
    """Evaluate a list of required field IDs against labeled bodies."""
    missing: list[str] = []
    for fid in field_ids:
        ok, reason = field_body_ok(text, fid, min_chars=min_chars)
        if not ok:
            missing.append(reason)
    if missing:
        return False, f"field failures: {missing[:8]}", missing
    return True, f"all {len(field_ids)} fields present with body>={min_chars}", []


def _has_signaling_question(body: str) -> bool:
    if "?" in body:
        return True
    lower = body.lower()
    return "signaling question" in lower or "ask whether" in lower or "probe whether" in lower


def _has_judgment_slot(body: str, vocab: tuple[str, ...]) -> bool:
    lower = body.lower().replace(" ", "_")
    hits = sum(1 for token in vocab if token in lower or token.replace("_", " ") in body.lower())
    if hits >= 2:
        return True
    if "judgment" in body.lower() and ("low" in body.lower() or "risk" in body.lower()):
        return True
    return False


def evaluate_domain_fields(
    text: str,
    domains: dict[str, str],
    overall_id: str,
    vocab: tuple[str, ...],
    *,
    min_chars: int = MIN_FIELD_BODY,
) -> tuple[bool, str]:
    """Domain fields need local label cue, signaling prompt, judgment slot, body depth.

    Domain label cues must appear in the field's own heading-plus-body block
    (E2-R2). Mentions elsewhere in the corpus cannot rescue a wrong local label.
    """
    problems: list[str] = []
    for domain_id, label_cue in domains.items():
        ok, reason = field_body_ok(text, domain_id, min_chars=min_chars)
        if not ok:
            problems.append(reason)
            continue
        body = extract_labeled_field_body(text, domain_id) or ""
        local_block = extract_labeled_field_block(text, domain_id) or body
        if label_cue.lower() not in local_block.lower():
            problems.append(
                f"{domain_id} missing local domain label cue '{label_cue}'"
            )
        if not _has_signaling_question(body):
            problems.append(f"{domain_id} missing signaling question")
        if not _has_judgment_slot(body, vocab):
            problems.append(f"{domain_id} missing judgment slot/vocabulary")
    ok_all, reason_all, _ = evaluate_required_fields(text, (overall_id,), min_chars=min_chars)
    if not ok_all:
        problems.append(reason_all)
    else:
        overall_body = extract_labeled_field_body(text, overall_id) or ""
        if not _has_judgment_slot(overall_body, vocab):
            problems.append(f"{overall_id} missing judgment vocabulary")
    if problems:
        return False, "; ".join(problems[:10])
    return True, f"{len(domains)} domains + {overall_id} ok"


def _count_numbered_or_bulleted_items(body: str) -> int:
    items = re.findall(r"(?m)^\s*(?:[-*]|\d+[.)])\s+\S+", body)
    return len(items)


def evaluate_sensitivity_body(body: str) -> tuple[bool, str]:
    """Require >=2 concrete sensitivity analyses with trigger language."""
    items = _count_numbered_or_bulleted_items(body)
    trigger_hits = len(re.findall(r"trigger", body, flags=re.I))
    if items < 2 and trigger_hits < 2:
        # fall back: split on sentences mentioning analysis
        parts = [p for p in re.split(r"[;\n]", body) if "analys" in p.lower() or "sensitivity" in p.lower()]
        if len(parts) < 2:
            return False, f"sensitivity analyses count <2 (items={items})"
    if trigger_hits < 1 and "when" not in body.lower():
        return False, "sensitivity analyses missing trigger language"
    if items < 2:
        # still require two distinct analysis names/phrases
        named = re.findall(
            r"(leave[- ]one[- ]out|fixed\s+vs\s+random|risk[- ]of[- ]bias|exclude|imputation|model)",
            body,
            flags=re.I,
        )
        if len(set(n.lower() for n in named)) < 2 and items < 2:
            return False, "need >=2 distinct sensitivity analyses"
    return True, "sensitivity ok"


def evaluate_anti_pooling_conditions(body: str) -> tuple[bool, str]:
    """Require >=3 concrete anti-pooling conditions."""
    items = _count_numbered_or_bulleted_items(body)
    if items >= 3:
        return True, f"anti-pooling conditions={items}"
    # semicolon or 'condition' enumerated
    parts = [p.strip() for p in re.split(r"[;\n]", body) if len(p.strip()) > 20]
    if len(parts) >= 3:
        return True, f"anti-pooling conditions parts={len(parts)}"
    return False, f"anti-pooling conditions <3 (items={items})"


def _normalize_gate_text(text: str) -> str:
    """Lowercase and strip light markdown emphasis so polarity checks see prose."""
    lowered = (text or "").lower()
    return re.sub(r"[*_`]+", "", lowered)


def evaluate_anti_pooling_action(body: str) -> tuple[bool, str]:
    """Require mandatory narrative/SWiM and prohibit invented/silent pooling (E2-R4)."""
    lower = _normalize_gate_text(body)
    if _non_ws_len(body) < MIN_FIELD_BODY:
        return False, "anti_pooling_action body too short"

    # Opposite-polarity statements cannot count as compliance.
    opposite_narrative = bool(
        re.search(
            r"(?:"
            r"(?:narrative(?:\s+synthesis)?|swim|structured\s+narrative)"
            r"\s+is\s+optional"
            r"|"
            r"(?:optional|optionally)\s+(?:narrative(?:\s+synthesis)?|swim)"
            r"|"
            r"(?:may|can|might)\s+skip\s+(?:narrative|swim|structured\s+narrative)"
            r"|"
            r"(?:skip|without)\s+(?:narrative|swim)"
            r"|"
            r"narrative(?:\s+synthesis)?\s+(?:not\s+required|unnecessary)"
            r")",
            lower,
        )
    )
    opposite_forbid = bool(
        re.search(
            r"(?:"
            r"(?:invented|fabricated)\s+pooled\s+(?:numbers?|estimates?|means?)"
            r"\s+(?:are\s+)?(?:allowed|optional|permitted|ok|okay|fine)"
            r"|"
            r"(?:allowed|optional|permitted)\s+(?:to\s+)?(?:invent|fabricate|use)"
            r"[^\n.]{0,40}(?:pooled|forest\s+plot|silent\s+pool)"
            r"|"
            r"silent\s+(?:numeric\s+)?pooling\s+(?:is\s+)?(?:allowed|optional|permitted|ok)"
            r"|"
            r"(?:forest\s+plots?|pooled\s+numbers?)\s+(?:are\s+)?(?:allowed|optional)"
            r"\s+(?:even\s+)?(?:without|from\s+invent)"
            r")",
            lower,
        )
    )
    if opposite_narrative:
        return False, "anti_pooling_action narrative/SWiM polarity unsafe (optional/skip)"
    if opposite_forbid:
        return False, "anti_pooling_action allows invented/silent pooling"

    # Affirmative mandatory narrative/SWiM (not mere token presence).
    mandates_narrative = bool(
        re.search(
            r"(?:"
            r"(?:mandatory|required)\s+"
            r"(?:action\s+is\s+)?"
            r"(?:structured\s+)?"
            r"(?:narrative(?:\s+synthesis)?(?:\s*/\s*swim)?|swim|narrative\s*/\s*swim)"
            r"|"
            r"(?:must\s+(?:use|switch\s+to|perform)|use\s+structured)\s+"
            r"(?:narrative|swim)"
            r"|"
            r"(?:structured\s+)?"
            r"(?:narrative(?:\s+synthesis)?(?:\s*/\s*swim)?|swim|narrative\s*/\s*swim)"
            r"\s+(?:is\s+)?(?:mandatory|required)"
            r"|"
            r"mandatory\s+structured\s+narrative"
            r"|"
            r"narrative\s*/\s*swim\s+only"
            r"|"
            r"protocol commitment if triggered:\s*narrative"
            r")",
            lower,
        )
    )

    # Explicit negative prohibition of invented/fabricated/silent pooling or forest plots.
    forbids = bool(
        re.search(
            r"(?:"
            r"(?:forbid(?:den)?|must\s+not|do\s+not|don't|never|no)\s+"
            r"(?:produce\s+)?"
            r"(?:invent(?:ed|ing)?|fabricat\w*|silent)\s+"
            r"(?:pooled\s+)?(?:numbers?|estimates?|means?|numeric\s+pooling|pooling|forest)"
            r"|"
            r"(?:forbid(?:den)?|must\s+not|do\s+not|don't|never)\s+"
            r"(?:invented|fabricated)\s+pooled"
            r"|"
            r"(?:forbid(?:den)?|must\s+not|do\s+not|don't|never|no)\s+"
            r"(?:silent\s+(?:numeric\s+)?pool(?:ing)?|invent(?:ed)?\s+pooled|"
            r"fabricat\w*\s+pooled|forest\s+plots?\s+(?:built|from|without))"
            r"|"
            r"no\s+silent\s+(?:numeric\s+)?pool"
            r"|"
            r"without\s+(?:inventing|fabricating)\s+a\s+pooled"
            r"|"
            r"forbid\s+invented\s+pooled\s+numbers\s+and\s+forest\s+plots"
            r")",
            lower,
        )
    )

    if "silent pooling" in lower and not forbids and not re.search(
        r"(?:forbid|must\s+not|do\s+not|never|no\s+silent)", lower
    ):
        return False, "anti_pooling_action allows silent pooling"
    if not mandates_narrative:
        return False, "anti_pooling_action missing narrative/SWiM requirement"
    if not forbids:
        return False, "anti_pooling_action missing forbid-invented-pooled rule"
    return True, "anti_pooling_action ok"


def _combined_methods_text(methods_root: Path, rels: tuple[str, ...]) -> str:
    parts: list[str] = []
    for rel in rels:
        path = methods_root / rel
        if path.is_file():
            parts.append(read_text(path))
    return "\n\n".join(parts)


SR_TEXT_RELS = (
    "core/protocols/systematic_review.md",
    "core/templates/prisma_protocol.md",
    "core/templates/prisma_report_skeleton.md",
    "core/templates/evidence_assessment.md",
)

SR_PROTOCOL_REL = "core/protocols/systematic_review.md"
PRISMA_PROTOCOL_REL = "core/templates/prisma_protocol.md"
PRISMA_REPORT_REL = "core/templates/prisma_report_skeleton.md"

# Surfaces that intentionally carry full method-field depth for E2 gates.
E2_METHOD_SURFACE_RELS = (
    SR_PROTOCOL_REL,
    PRISMA_PROTOCOL_REL,
)


def _read_methods_surface(methods_root: Path, rel: str) -> str:
    path = methods_root / rel
    if not path.is_file():
        return ""
    return read_text(path)


def evaluate_prisma_fields_text(text: str) -> tuple[bool, str]:
    """Public helper: PRISMA protocol + report labeled fields on one text blob."""
    ok1, detail1, _miss1 = evaluate_required_fields(text, PRISMA_PROTOCOL_FIELDS)
    ok2, detail2, _miss2 = evaluate_required_fields(text, PRISMA_REPORT_FIELDS)
    if ok1 and ok2:
        return True, (
            f"prisma protocol+report fields ok "
            f"({len(PRISMA_PROTOCOL_FIELDS)}+{len(PRISMA_REPORT_FIELDS)})"
        )
    return False, "; ".join(
        [d for d in (detail1 if not ok1 else "", detail2 if not ok2 else "") if d]
    )


def evaluate_prisma_fields_surfaces(
    *,
    systematic_review: str,
    prisma_protocol: str,
    prisma_report: str,
) -> tuple[bool, str]:
    """File-specific PRISMA responsibilities (E2-R1).

    Requires 14 protocol fields independently in the method protocol and in
    ``prisma_protocol.md``, plus 13 report fields independently in
    ``prisma_report_skeleton.md``. Duplicates in another file cannot rescue a
    hollow designated surface.
    """
    problems: list[str] = []
    for label, text in (
        (SR_PROTOCOL_REL, systematic_review),
        (PRISMA_PROTOCOL_REL, prisma_protocol),
    ):
        ok, detail, _ = evaluate_required_fields(text, PRISMA_PROTOCOL_FIELDS)
        if not ok:
            problems.append(f"{label}: {detail}")
    ok_r, detail_r, _ = evaluate_required_fields(prisma_report, PRISMA_REPORT_FIELDS)
    if not ok_r:
        problems.append(f"{PRISMA_REPORT_REL}: {detail_r}")
    if problems:
        return False, "; ".join(problems[:6])
    return True, (
        f"prisma surfaces ok: {len(PRISMA_PROTOCOL_FIELDS)} protocol fields in "
        f"{SR_PROTOCOL_REL} + {PRISMA_PROTOCOL_REL}; "
        f"{len(PRISMA_REPORT_FIELDS)} report fields in {PRISMA_REPORT_REL}"
    )


def evaluate_rob2_fields_text(text: str) -> tuple[bool, str]:
    """Public helper for RoB 2 domain gates."""
    return evaluate_domain_fields(
        text,
        ROB2_DOMAINS,
        "rob2_overall",
        ROB2_JUDGMENT_VOCAB,
    )


def evaluate_robins_i_fields_text(text: str) -> tuple[bool, str]:
    """Public helper for ROBINS-I domain gates."""
    return evaluate_domain_fields(
        text,
        ROBINS_DOMAINS,
        "robins_overall",
        ROBINS_JUDGMENT_VOCAB,
    )


def evaluate_method_fields_on_surfaces(
    evaluator: Callable[[str], tuple[bool, str]],
    surfaces: dict[str, str],
) -> tuple[bool, str]:
    """Run a text helper on each designated surface independently (E2-R1)."""
    problems: list[str] = []
    ok_labels: list[str] = []
    for label, text in surfaces.items():
        ok, detail = evaluator(text)
        if not ok:
            problems.append(f"{label}: {detail}")
        else:
            ok_labels.append(label)
    if problems:
        return False, "; ".join(problems[:8])
    return True, f"ok on surfaces: {', '.join(ok_labels)}"


def evaluate_anti_fabrication_certainty(body: str) -> tuple[bool, str]:
    """Require local negative polarity against fabricating/inventing certainty (E2-R3)."""
    text = body or ""
    lower = _normalize_gate_text(text)
    if _non_ws_len(text) < 8:
        return False, "GRADE missing anti-fabrication certainty rule"

    # Reject endorsement, optionality, or ambiguous positive mentions.
    endorsement = re.search(
        r"(?:"
        r"(?:may|can|should|freely|optionally)\s+(?:algorithmically\s+)?"
        r"(?:fabricat\w*|invent\w*)\s+(?:a\s+)?(?:certainty|grade)"
        r"|"
        r"(?:fabricat\w*|invent\w*)\s+(?:a\s+)?(?:certainty|certainty\s+rating|grade\s+certainty)"
        r"\s+(?:freely|optionally|is\s+allowed|are\s+allowed|is\s+optional|ok|okay)"
        r"|"
        r"(?:fabricating|inventing)\s+certainty\s+(?:is\s+)?(?:allowed|optional|permitted|fine|ok)"
        r"|"
        r"(?:allowed|optional|permitted)\s+to\s+(?:algorithmically\s+)?"
        r"(?:fabricat\w*|invent\w*)\s+(?:a\s+)?certainty"
        r")",
        lower,
    )
    if endorsement:
        return False, "GRADE anti-fabrication polarity unsafe (endorses/optionalizes fabrication)"

    # Explicit negative polarity tied locally to fabricate/invent certainty.
    prohibition = re.search(
        r"(?:"
        r"(?:must\s+not|do\s+not|don't|never|forbid(?:den)?)\s+"
        r"(?:algorithmically\s+)?(?:fabricat\w*|invent\w*)\s+"
        r"(?:a\s+)?(?:certainty|grade(?:\s+certainty)?|certainty\s+rating)"
        r"|"
        r"(?:must\s+not|do\s+not|don't|never|forbid(?:den)?)\s+"
        r"(?:algorithmically\s+)?(?:fabricat\w*|invent\w*)\s+"
        r"(?:a\s+)?(?:certainty\s+)?rating"
        r"|"
        r"(?:no|never)\s+(?:algorithmically\s+)?(?:fabricated?|invented)\s+certainty"
        r"|"
        r"(?:must\s+not|do\s+not|don't|never)\s+invent\s+a\s+certainty"
        r"|"
        r"certainty[^\n.]{0,40}(?:must\s+not|do\s+not|don't|never|forbid)"
        r"[^\n.]{0,40}(?:fabricat|invent)"
        r")",
        lower,
    )
    if prohibition:
        return True, "GRADE anti-fabrication polarity ok"

    # Mere substring "fabricat" / "invent certainty" without prohibition is unsafe.
    if "fabricat" in lower or re.search(r"invent\w*\s+(?:a\s+)?certainty", lower):
        return False, "GRADE anti-fabrication polarity unsafe (mention without prohibition)"
    return False, "GRADE missing anti-fabrication certainty rule"


def evaluate_hetero_exploration_body(body: str) -> tuple[bool, str]:
    """Require subgroup/meta-regression plus pre-spec and multiplicity caution (E2-R5)."""
    lower = _normalize_gate_text(body)
    has_explore = (
        "subgroup" in lower
        or "meta-regression" in lower
        or "meta regression" in lower
        or "metaregression" in lower
    )
    if not has_explore:
        return False, "hetero_exploration missing subgroup/meta-regression rules"
    has_prespec = bool(
        re.search(r"pre[-\s]?specif", lower)
        or "a priori" in lower
        or "apriori" in lower
    )
    if not has_prespec:
        return False, "hetero_exploration missing pre-specification discipline"
    has_caution = bool(
        re.search(
            r"(multiplicit|data[-\s]?driven|fishing|hypothesis[-\s]?generat|"
            r"exploratory|post\s*hoc|post-hoc|not confirmatory|caution)",
            lower,
        )
    )
    if not has_caution:
        return False, "hetero_exploration missing multiplicity/data-driven caution"
    return True, "hetero_exploration ok"


def evaluate_grade_fields_text(text: str) -> tuple[bool, str]:
    """Public helper for GRADE fields."""
    ok, detail, _ = evaluate_required_fields(text, GRADE_ALL_FIELDS)
    if not ok:
        return False, detail
    # Ensure five downgrade domains are each instructional, not index-only
    for fid in GRADE_DOWNGRADE_FIELDS:
        body = extract_labeled_field_body(text, fid) or ""
        if (
            "downgrade" not in body.lower()
            and "certainty" not in body.lower()
            and "bias" not in body.lower()
            and "inconsisten" not in body.lower()
            and "indirect" not in body.lower()
            and "imprecis" not in body.lower()
            and "publication" not in body.lower()
            and "reporting" not in body.lower()
        ):
            if _non_ws_len(body) < MIN_FIELD_BODY:
                return False, f"{fid} lacks instructional downgrade content"
    cert = extract_labeled_field_body(text, "grade_certainty") or ""
    if not any(
        t in cert.lower()
        for t in ("high", "moderate", "low", "very low", "very_low")
    ):
        return False, "grade_certainty missing high/moderate/low/very low vocabulary"
    # Prefer local grade_certainty body; fall back only to other GRADE field bodies
    # (never the whole corpus) so distant fabricate mentions cannot greenwash.
    anti_ok, anti_detail = evaluate_anti_fabrication_certainty(cert)
    if not anti_ok:
        local_grade_bodies = [
            extract_labeled_field_body(text, fid) or ""
            for fid in GRADE_ALL_FIELDS
        ]
        combined_local = "\n".join(local_grade_bodies)
        anti_ok, anti_detail = evaluate_anti_fabrication_certainty(combined_local)
    if not anti_ok:
        return False, anti_detail
    return True, "grade fields ok"


def evaluate_effect_hetero_sensitivity_text(text: str) -> tuple[bool, str]:
    """Public helper for effect/hetero/sensitivity gates."""
    ok, detail, _ = evaluate_required_fields(text, EFFECT_HETERO_FIELDS)
    if not ok:
        return False, detail
    primary = extract_labeled_field_body(text, "effect_measure_primary") or ""
    if not any(
        tok in primary.lower()
        for tok in (
            "rr",
            "or",
            "hr",
            "md",
            "smd",
            "risk ratio",
            "odds",
            "hazard",
            "mean difference",
        )
    ):
        return False, "effect_measure_primary missing effect-measure mapping"
    by_type = extract_labeled_field_body(text, "effect_measure_by_outcome_type") or ""
    missing_types = [
        t for t in ("binary", "continuous") if t not in by_type.lower()
    ]
    if "time" not in by_type.lower():
        missing_types.append("time-to-event")
    if missing_types:
        return False, f"effect_measure_by_outcome_type missing {missing_types}"
    hetero = extract_labeled_field_body(text, "hetero_stats") or ""
    if not any(
        t in hetero.lower()
        for t in ("i2", "i²", "i^2", "tau", "τ", "prediction interval", "qualitative")
    ):
        return False, "hetero_stats missing I2/tau2/PI or qualitative alternative"
    explor = extract_labeled_field_body(text, "hetero_exploration") or ""
    eok, ereason = evaluate_hetero_exploration_body(explor)
    if not eok:
        return False, ereason
    sens = extract_labeled_field_body(text, "sensitivity_analyses") or ""
    sok, sreason = evaluate_sensitivity_body(sens)
    if not sok:
        return False, sreason
    return True, "effect/hetero/sensitivity ok"


def evaluate_anti_pooling_fields_text(text: str) -> tuple[bool, str]:
    """Public helper for anti-pooling conditions + mandatory action."""
    ok, detail, _ = evaluate_required_fields(text, ANTI_POOLING_FIELDS)
    if not ok:
        return False, detail
    cond = extract_labeled_field_body(text, "anti_pooling_conditions") or ""
    cok, creason = evaluate_anti_pooling_conditions(cond)
    if not cok:
        return False, creason
    action = extract_labeled_field_body(text, "anti_pooling_action") or ""
    aok, areason = evaluate_anti_pooling_action(action)
    if not aok:
        return False, areason
    return True, "anti_pooling fields ok"


def _identity_has_title_or_id(identity: Any) -> bool:
    """Return True when identity provides title and/or durable id."""
    if not isinstance(identity, dict):
        return False
    title = str(identity.get("title") or "").strip()
    doi_or_id = str(identity.get("doi_or_id") or "").strip()
    return bool(title or doi_or_id)


def _nonempty_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip()


def _token_set(text: str) -> set[str]:
    return {t for t in re.findall(r"[a-z0-9]+", (text or "").lower()) if len(t) > 2}


def _claim_extract_mismatch(claim_text: str, extract: str, *, force_mismatch: bool) -> bool:
    """Heuristic contradiction detector; may only downgrade, never promote VERIFIED."""
    if force_mismatch:
        return True
    claim_tokens = _token_set(claim_text)
    extract_tokens = _token_set(extract)
    if not claim_tokens or not extract_tokens:
        return False
    # Explicit polarity clash on shared key nouns is rare; use negation cues + low overlap.
    neg_claim = bool(re.search(r"\b(not|no|never|fail|decrease|worsen|inferior)\b", claim_text, re.I))
    neg_extract = bool(
        re.search(r"\b(not|no|never|fail|decrease|worsen|inferior)\b", extract, re.I)
    )
    overlap = len(claim_tokens & extract_tokens) / max(1, len(claim_tokens))
    if overlap < 0.15 and len(claim_tokens) >= 3:
        return True
    if neg_claim != neg_extract and overlap >= 0.3:
        # Opposite polarity language with shared topical tokens.
        pos_claim = bool(
            re.search(r"\b(improve|increase|superior|benefit|effective)\b", claim_text, re.I)
        )
        pos_extract = bool(
            re.search(r"\b(improve|increase|superior|benefit|effective)\b", extract, re.I)
        )
        if pos_claim != pos_extract:
            return True
    return False


def evaluate_citation_record(record: dict) -> dict[str, Any]:
    """Validate one citation/claim row for E3-A integrity consistency.

    A DOI, citation token, or string similarity never promotes to VERIFIED.
    VERIFIED requires access_state=verified, non-empty citation_id/claim_text,
    locator or extract, support_status=supported, safe/resolved risks, and
    assessment_source in {human_confirmed, verified_adapter}.
    access_blocked/unresolvable pairs only with UNVERIFIABLE_ACCESS.
    Unknown access, verdict, support, or risk vocabulary fails closed.
    """
    if not isinstance(record, dict):
        return {
            "ok": False,
            "error": "invalid_record",
            "detail": "citation record must be a dict",
        }

    citation_id = _nonempty_text(record.get("citation_id"))
    identity = record.get("identity")
    locator = _nonempty_text(record.get("locator_or_quote"))
    extract = _nonempty_text(record.get("extract"))
    claim_text = _nonempty_text(record.get("claim_text"))
    access_state = _nonempty_text(record.get("access_state")).lower()
    risk_flags_raw = record.get("risk_flags") or []
    if isinstance(risk_flags_raw, str):
        risk_flags = [risk_flags_raw]
    elif isinstance(risk_flags_raw, (list, tuple, set)):
        risk_flags = [str(x) for x in risk_flags_raw]
    else:
        risk_flags = []
    verdict = _nonempty_text(record.get("verdict"))
    support_status = _nonempty_text(record.get("support_status")).lower()
    assessment_source = _nonempty_text(record.get("assessment_source")).lower()
    force_mismatch = bool(record.get("force_mismatch"))

    if not citation_id:
        return {
            "ok": False,
            "error": "missing_citation_id",
            "detail": "citation record failed: <missing-id>: missing_citation_id",
        }

    if not claim_text:
        return {
            "ok": False,
            "error": "missing_claim_text",
            "detail": f"citation record failed: {citation_id}: missing_claim_text",
        }

    if verdict not in CLAIM_VERDICTS:
        return {
            "ok": False,
            "error": "unknown_verdict",
            "detail": f"citation record failed: {citation_id}: unknown_verdict {verdict!r}",
        }

    if not _identity_has_title_or_id(identity):
        return {
            "ok": False,
            "error": "missing_identity",
            "detail": f"citation record failed: {citation_id}: missing_identity",
        }

    if access_state not in ACCESS_STATES:
        return {
            "ok": False,
            "error": "unknown_access_state",
            "detail": (
                f"citation record failed: {citation_id}: unknown_access_state "
                f"{access_state!r}"
            ),
        }

    risk_flags_l: set[str] = set()
    for raw_flag in risk_flags:
        flag = str(raw_flag).strip().lower()
        if not flag:
            continue
        if flag not in KNOWN_RISK_FLAGS:
            return {
                "ok": False,
                "error": "unknown_risk_flag",
                "detail": (
                    f"citation record failed: {citation_id}: unknown_risk_flag {flag!r}"
                ),
            }
        risk_flags_l.add(flag)

    if support_status and support_status not in SUPPORT_STATUSES:
        return {
            "ok": False,
            "error": "unknown_support_status",
            "detail": (
                f"citation record failed: {citation_id}: unknown_support_status "
                f"{support_status!r}"
            ),
        }

    # access_blocked/unresolvable must pair with UNVERIFIABLE_ACCESS only.
    if access_state in ACCESS_STATES_REQUIRING_UNVERIFIABLE_ACCESS:
        if verdict != "UNVERIFIABLE_ACCESS":
            return {
                "ok": False,
                "error": "verdict_access_incoherent",
                "detail": (
                    f"citation record failed: {citation_id}: verdict_access_incoherent "
                    f"(access_state={access_state}, verdict={verdict})"
                ),
            }
    if verdict == "UNVERIFIABLE_ACCESS":
        if access_state not in ACCESS_STATES_REQUIRING_UNVERIFIABLE_ACCESS:
            return {
                "ok": False,
                "error": "verdict_access_incoherent",
                "detail": (
                    f"citation record failed: {citation_id}: verdict_access_incoherent "
                    f"(UNVERIFIABLE_ACCESS requires access_blocked or unresolvable; "
                    f"got access_state={access_state})"
                ),
            }

    has_locator_or_extract = bool(locator or extract)
    doi_or_id = ""
    if isinstance(identity, dict):
        doi_or_id = _nonempty_text(identity.get("doi_or_id"))

    if verdict == "VERIFIED":
        if access_state != "verified":
            return {
                "ok": False,
                "error": "verdict_access_incoherent",
                "detail": (
                    f"citation record failed: {citation_id}: verdict_access_incoherent "
                    f"(VERIFIED requires access_state=verified; got {access_state})"
                ),
            }
        if not has_locator_or_extract:
            # DOI/id present is never enough; prefer the plan's primary error code
            # when a durable id is present without locator/extract.
            err = "doi_alone_insufficient" if doi_or_id else "verified_without_extract"
            return {
                "ok": False,
                "error": err,
                "detail": (
                    f"citation record failed: {citation_id}: {err} "
                    "(VERIFIED requires locator or extract; DOI alone insufficient)"
                ),
            }
        if "retracted" in risk_flags_l:
            return {
                "ok": False,
                "error": "retracted_marked_clean",
                "detail": f"citation record failed: {citation_id}: retracted_marked_clean",
            }
        if "expression_of_concern" in risk_flags_l:
            return {
                "ok": False,
                "error": "expression_of_concern_clean",
                "detail": (
                    f"citation record failed: {citation_id}: expression_of_concern_clean"
                ),
            }
        if "version_mismatch" in risk_flags_l:
            return {
                "ok": False,
                "error": "version_mismatch_clean",
                "detail": f"citation record failed: {citation_id}: version_mismatch_clean",
            }
        if "predatory" in risk_flags_l:
            return {
                "ok": False,
                "error": "predatory_unresolved",
                "detail": f"citation record failed: {citation_id}: predatory_unresolved",
            }
        if "corrected" in risk_flags_l:
            correction_note = ""
            if isinstance(identity, dict):
                correction_note = _nonempty_text(identity.get("correction_note"))
            notes = _nonempty_text(record.get("notes"))
            if not correction_note and "correction" not in notes.lower():
                return {
                    "ok": False,
                    "error": "correction_ignored",
                    "detail": f"citation record failed: {citation_id}: correction_ignored",
                }
        if support_status != "supported":
            # Contradicted/unsupported/partial/unknown cannot sit under VERIFIED.
            err = (
                "major_distortion_required"
                if support_status in {"contradicted", "unsupported"}
                else "verified_support_not_supported"
            )
            return {
                "ok": False,
                "error": err,
                "detail": (
                    f"citation record failed: {citation_id}: {err} "
                    f"(support_status={support_status or 'missing'})"
                ),
            }
        if assessment_source not in VERIFIED_ASSESSMENT_SOURCES:
            return {
                "ok": False,
                "error": "verified_missing_assessment_source",
                "detail": (
                    f"citation record failed: {citation_id}: "
                    "verified_missing_assessment_source "
                    "(need human_confirmed or verified_adapter; "
                    "DOI/similarity cannot promote)"
                ),
            }

    # Contradiction / forced mismatch cannot sit under VERIFIED/MINOR_DISTORTION.
    if _claim_extract_mismatch(claim_text, extract, force_mismatch=force_mismatch):
        if verdict not in {"MAJOR_DISTORTION", "UNVERIFIABLE", "UNVERIFIABLE_ACCESS"}:
            return {
                "ok": False,
                "error": "major_distortion_required",
                "detail": (
                    f"citation record failed: {citation_id}: major_distortion_required "
                    "(claim/extract mismatch)"
                ),
            }

    return {
        "ok": True,
        "detail": f"citation record ok: {citation_id}",
    }


def evaluate_citation_records(records: list[dict]) -> dict[str, Any]:
    """Aggregate citation rows; ok only if non-empty and every record is ok."""
    if not isinstance(records, list):
        return {
            "ok": False,
            "error": "invalid_records",
            "detail": "citation records must be a list",
        }
    if not records:
        return {
            "ok": False,
            "error": "empty_records",
            "detail": "citation records failed: empty_records",
        }
    for record in records:
        result = evaluate_citation_record(record if isinstance(record, dict) else {})
        if not result.get("ok"):
            cid = ""
            if isinstance(record, dict):
                cid = _nonempty_text(record.get("citation_id"))
            return {
                "ok": False,
                "error": result.get("error", "citation_record_failed"),
                "detail": result.get("detail")
                or f"citation records failed at {cid or '<unknown>'}",
            }
    return {
        "ok": True,
        "detail": f"citation records ok: {len(records)} rows",
    }


def evaluate_citation_integrity_protocol_text(text: str) -> tuple[bool, str]:
    """Protocol-level integrity field bodies on citation_integrity.md only."""
    ok, detail, _ = evaluate_required_fields(text, CITATION_INTEGRITY_PROTOCOL_FIELDS)
    if not ok:
        return False, detail
    # Reject keyword-only hollow bodies: require VERIFIED promotion discipline cues.
    body = strip_lineage_comments(text)
    lower = body.lower()
    if "doi" in lower and "never" not in lower and "insufficient" not in lower:
        # Soft check: protocol must teach DOI insufficiency somewhere.
        if "locator" not in lower:
            return False, "citation protocol missing DOI-insufficiency / locator discipline"
    if "human_confirmed" not in lower and "verified_adapter" not in lower:
        return False, "citation protocol missing assessment_source promotion rules"
    if "mode1" not in lower or "mode2" not in lower:
        return False, "citation protocol missing integrity_mode Mode1/Mode2"
    return True, f"citation integrity protocol fields ok ({len(CITATION_INTEGRITY_PROTOCOL_FIELDS)})"


def evaluate_citation_audit_template_text(text: str) -> tuple[bool, str]:
    """Audit template fields — protocol duplicates cannot pass this helper."""
    ok, detail, _ = evaluate_required_fields(text, CITATION_AUDIT_TEMPLATE_FIELDS)
    if not ok:
        return False, detail
    lower = strip_lineage_comments(text).lower()
    if "inventory" not in lower:
        return False, "citation audit template missing inventory guidance"
    if "human" not in lower:
        return False, "citation audit template missing human gate language"
    return True, f"citation audit template fields ok ({len(CITATION_AUDIT_TEMPLATE_FIELDS)})"


def evaluate_claim_report_template_text(text: str) -> tuple[bool, str]:
    """Claim report template fields — isolated from protocol/audit peers."""
    ok, detail, _ = evaluate_required_fields(text, CLAIM_REPORT_TEMPLATE_FIELDS)
    if not ok:
        return False, detail
    lower = strip_lineage_comments(text).lower()
    if "verdict" not in lower:
        return False, "claim report template missing verdict vocabulary"
    if "mode1" not in lower and "mode2" not in lower and "sampling" not in lower:
        return False, "claim report template missing sampling / mode guidance"
    return True, f"claim report template fields ok ({len(CLAIM_REPORT_TEMPLATE_FIELDS)})"


def _ledger_names_claim(change_ledger: list[dict], claim: str, ops: set[str]) -> bool:
    """Return True when a ledger row with allowed op names the claim in target/summary."""
    for row in change_ledger:
        if not isinstance(row, dict):
            continue
        op = _nonempty_text(row.get("op")).lower()
        if op not in ops:
            continue
        target = _nonempty_text(row.get("target"))
        summary = _nonempty_text(row.get("summary")) or _nonempty_text(
            row.get("replacement")
        )
        if claim in target or claim in summary or (target and target in claim):
            return True
    return False


def _new_evidence_covers_marker(new_evidence_rows: list[dict], marker: str) -> bool:
    """Return True when a gated new-evidence row covers marker with allowed state."""
    for row in new_evidence_rows:
        if not isinstance(row, dict):
            continue
        blob = " ".join(
            [
                _nonempty_text(row.get("citation_id")),
                _nonempty_text(row.get("claim")),
                _nonempty_text(row.get("marker")),
                _nonempty_text(row.get("text")),
            ]
        )
        if marker not in blob and marker.rstrip(".,);]") not in blob:
            continue
        evidence_state = _nonempty_text(row.get("evidence_state")).lower().replace("_", "-")
        if evidence_state not in REVISION_EVIDENCE_OK and evidence_state != "human-confirmed":
            continue
        human_gate = bool(row.get("human_gate"))
        if not human_gate:
            continue
        return True
    return False


def _ledger_row_summary(row: dict) -> str:
    """Non-empty replacement/summary text claimed by a ledger row."""
    return _nonempty_text(row.get("summary")) or _nonempty_text(row.get("replacement"))


def _first_span_index(text: str, span: str) -> int:
    """Return the first deterministic index of span in text, or -1 if absent."""
    if not span:
        return -1
    return text.find(span)


def _validate_change_ledger_row(
    row: dict, before_text: str, after_text: str
) -> dict[str, Any] | None:
    """Return a failure dict when a ledger row is structurally false; else None.

    Replace requires non-empty target/summary, target present before, target
    absent after, and summary present after. Delete requires target present
    before and absent after. Add requires non-empty summary absent before and
    present after. Move requires non-empty target present before and after with
    a differing first deterministic position; ambiguity fails closed. Annotate
    requires non-empty target present in before or after. Operation vocabulary
    is closed.
    """
    op = _nonempty_text(row.get("op")).lower()
    target = _nonempty_text(row.get("target"))
    summary = _ledger_row_summary(row)

    if not op or op not in REVISION_ALLOWED_OPS:
        return {
            "ok": False,
            "error": "invalid_ledger_op",
            "detail": (
                "revision transition failed: invalid_ledger_op "
                f"({op or '<empty>'})"
            ),
        }

    if op == "replace":
        if not target or not summary:
            return {
                "ok": False,
                "error": "false_ledger_claim",
                "detail": (
                    "revision transition failed: false_ledger_claim "
                    "(replace requires non-empty target and summary)"
                ),
            }
        if target not in before_text:
            return {
                "ok": False,
                "error": "false_ledger_claim",
                "detail": (
                    "revision transition failed: false_ledger_claim "
                    "(replace target absent before)"
                ),
            }
        if target in after_text:
            return {
                "ok": False,
                "error": "false_ledger_claim",
                "detail": (
                    "revision transition failed: false_ledger_claim "
                    "(replace target still present after)"
                ),
            }
        if summary not in after_text:
            return {
                "ok": False,
                "error": "false_ledger_claim",
                "detail": (
                    "revision transition failed: false_ledger_claim "
                    "(replace summary absent after)"
                ),
            }
        return None

    if op == "delete":
        if not target:
            return {
                "ok": False,
                "error": "false_ledger_claim",
                "detail": (
                    "revision transition failed: false_ledger_claim "
                    "(delete requires non-empty target)"
                ),
            }
        if target not in before_text:
            return {
                "ok": False,
                "error": "false_ledger_claim",
                "detail": (
                    "revision transition failed: false_ledger_claim "
                    "(delete target absent before)"
                ),
            }
        if target in after_text:
            return {
                "ok": False,
                "error": "false_ledger_claim",
                "detail": (
                    "revision transition failed: false_ledger_claim "
                    "(delete target still present after)"
                ),
            }
        return None

    if op == "add":
        if not summary:
            return {
                "ok": False,
                "error": "false_ledger_claim",
                "detail": (
                    "revision transition failed: false_ledger_claim "
                    "(add requires non-empty summary)"
                ),
            }
        if summary in before_text:
            return {
                "ok": False,
                "error": "false_ledger_claim",
                "detail": (
                    "revision transition failed: false_ledger_claim "
                    "(add summary already present before)"
                ),
            }
        if summary not in after_text:
            return {
                "ok": False,
                "error": "false_ledger_claim",
                "detail": (
                    "revision transition failed: false_ledger_claim "
                    "(add summary absent after)"
                ),
            }
        return None

    if op == "move":
        if not target:
            return {
                "ok": False,
                "error": "false_ledger_claim",
                "detail": (
                    "revision transition failed: false_ledger_claim "
                    "(move requires non-empty target)"
                ),
            }
        before_idx = _first_span_index(before_text, target)
        after_idx = _first_span_index(after_text, target)
        if before_idx < 0:
            return {
                "ok": False,
                "error": "false_ledger_claim",
                "detail": (
                    "revision transition failed: false_ledger_claim "
                    "(move target absent before)"
                ),
            }
        if after_idx < 0:
            return {
                "ok": False,
                "error": "false_ledger_claim",
                "detail": (
                    "revision transition failed: false_ledger_claim "
                    "(move target absent after)"
                ),
            }
        # Fail closed when first deterministic positions do not differ.
        if before_idx == after_idx:
            return {
                "ok": False,
                "error": "false_ledger_claim",
                "detail": (
                    "revision transition failed: false_ledger_claim "
                    "(move first position unchanged; ambiguity fails closed)"
                ),
            }
        return None

    # annotate: referenced manuscript span must exist in before or after.
    if not target:
        return {
            "ok": False,
            "error": "false_ledger_claim",
            "detail": (
                "revision transition failed: false_ledger_claim "
                "(annotate requires non-empty target)"
            ),
        }
    if target not in before_text and target not in after_text:
        return {
            "ok": False,
            "error": "false_ledger_claim",
            "detail": (
                "revision transition failed: false_ledger_claim "
                "(annotate target absent from before and after)"
            ),
        }
    return None


def evaluate_revision_transition(payload: dict) -> dict[str, Any]:
    """Deterministic before/after revision safety checks (E3-B).

    Heuristics may escalate risk but never prove semantic preservation.
    Stable error codes: missing_before_after, invalid_ledger_op,
    missing_change_id, duplicate_change_id, protected_claim_deleted,
    protected_claim_strengthened, silent_new_evidence, false_ledger_claim,
    missing_author_signoff, recovery_checkpoint_missing.
    """
    if not isinstance(payload, dict):
        return {
            "ok": False,
            "error": "invalid_payload",
            "detail": "revision transition failed: payload must be a dict",
        }

    before_text = _nonempty_text(payload.get("before_text"))
    after_text = _nonempty_text(payload.get("after_text"))
    if not before_text or not after_text:
        return {
            "ok": False,
            "error": "missing_before_after",
            "detail": "revision transition failed: missing_before_after",
        }

    protected_claims = [
        str(x).strip()
        for x in (payload.get("protected_claims") or [])
        if str(x).strip()
    ]
    protected_hedges = [
        str(x).strip()
        for x in (payload.get("protected_hedges") or [])
        if str(x).strip()
    ]
    protected = protected_claims + protected_hedges

    change_ledger_raw = payload.get("change_ledger") or []
    if not isinstance(change_ledger_raw, list):
        change_ledger_raw = []
    change_ledger = [r for r in change_ledger_raw if isinstance(r, dict)]

    new_evidence_raw = payload.get("new_evidence_rows") or []
    if not isinstance(new_evidence_raw, list):
        new_evidence_raw = []
    new_evidence_rows = [r for r in new_evidence_raw if isinstance(r, dict)]

    author_signoff = bool(payload.get("author_signoff"))
    recovery_required = bool(
        payload.get("recovery_required")
        or payload.get("require_recovery_checkpoint")
    )
    recovery_checkpoint = _nonempty_text(payload.get("recovery_checkpoint"))

    if recovery_required and not recovery_checkpoint:
        return {
            "ok": False,
            "error": "recovery_checkpoint_missing",
            "detail": "revision transition failed: recovery_checkpoint_missing",
        }

    # Structural ledger honesty: unique change_id, vocabulary, before/after truth.
    seen_change_ids: set[str] = set()
    for row in change_ledger:
        change_id = _nonempty_text(row.get("change_id"))
        if not change_id:
            return {
                "ok": False,
                "error": "missing_change_id",
                "detail": "revision transition failed: missing_change_id",
            }
        if change_id in seen_change_ids:
            return {
                "ok": False,
                "error": "duplicate_change_id",
                "detail": (
                    "revision transition failed: duplicate_change_id "
                    f"({change_id})"
                ),
            }
        seen_change_ids.add(change_id)
        row_fail = _validate_change_ledger_row(row, before_text, after_text)
        if row_fail is not None:
            return row_fail

    # Protected claim/hedge deletion or strengthening.
    for claim in protected:
        if claim not in before_text:
            continue
        if claim in after_text:
            continue
        ledgered = _ledger_names_claim(change_ledger, claim, {"delete", "replace"})
        if ledgered and not author_signoff:
            return {
                "ok": False,
                "error": "missing_author_signoff",
                "detail": "revision transition failed: missing_author_signoff",
            }
        if not ledgered:
            # Strengthening heuristic: soft hedge gone, hard claim language present.
            strengthened = False
            for soft_re, hard_re in STRENGTHEN_PAIRS:
                if soft_re.search(claim) and hard_re.search(after_text):
                    strengthened = True
                    break
            if strengthened:
                return {
                    "ok": False,
                    "error": "protected_claim_strengthened",
                    "detail": (
                        "revision transition failed: protected_claim_strengthened "
                        f"({claim[:80]})"
                    ),
                }
            return {
                "ok": False,
                "error": "protected_claim_deleted",
                "detail": (
                    "revision transition failed: protected_claim_deleted "
                    f"({claim[:80]})"
                ),
            }

    # Silent new evidence: DOI / result markers introduced without gate rows.
    before_dois = {m.group(0).rstrip(".,);]") for m in DOI_FIND_RE.finditer(before_text)}
    after_dois = {m.group(0).rstrip(".,);]") for m in DOI_FIND_RE.finditer(after_text)}
    for doi in sorted(after_dois - before_dois):
        if not _new_evidence_covers_marker(new_evidence_rows, doi):
            return {
                "ok": False,
                "error": "silent_new_evidence",
                "detail": f"revision transition failed: silent_new_evidence ({doi})",
            }

    before_results = {m.group(0) for m in RESULT_MARKER_RE.finditer(before_text)}
    after_results = {m.group(0) for m in RESULT_MARKER_RE.finditer(after_text)}
    for marker in sorted(after_results - before_results):
        if not _new_evidence_covers_marker(new_evidence_rows, marker):
            return {
                "ok": False,
                "error": "silent_new_evidence",
                "detail": (
                    f"revision transition failed: silent_new_evidence ({marker})"
                ),
            }

    # Author sign-off required when protected or new-evidence activity occurred.
    has_protected_edit = False
    for claim in protected:
        if claim in before_text and claim not in after_text:
            has_protected_edit = True
            break
        if _ledger_names_claim(change_ledger, claim, {"delete", "replace"}):
            has_protected_edit = True
            break
    has_new_evidence = bool(new_evidence_rows) or bool(after_dois - before_dois) or bool(
        after_results - before_results
    )
    if (has_protected_edit or has_new_evidence) and not author_signoff:
        return {
            "ok": False,
            "error": "missing_author_signoff",
            "detail": "revision transition failed: missing_author_signoff",
        }

    return {"ok": True, "detail": "revision transition ok"}


def evaluate_rebuttal_consistency(payload: dict) -> dict[str, Any]:
    """Compare reviewer point IDs to rebuttal rows and change/evidence pointers.

    Requires non-empty unique reviewer points and exact reviewer/rebuttal
    point-set equality. Every row needs valid coverage and response_kind.
    coverage=missing is always an unresolved audit failure.

    Stable errors: empty_reviewer_points, empty_point_id, empty_point_text,
    duplicate_reviewer_point, missing_point_row, duplicate_point_row,
    orphan_point_row, invalid_coverage, invalid_response_kind,
    coverage_missing_unclear, asserted_change_absent, empty_no_change_rationale,
    evidence_pointer_missing, evaluator_only_violation, partial_without_gap_note.
    """
    if not isinstance(payload, dict):
        return {
            "ok": False,
            "error": "invalid_payload",
            "detail": "rebuttal consistency failed: payload must be a dict",
        }

    generated = payload.get("generated_response_prose")
    if generated is not None and _nonempty_text(generated):
        return {
            "ok": False,
            "error": "evaluator_only_violation",
            "detail": "rebuttal consistency failed: evaluator_only_violation",
        }

    reviewer_points = payload.get("reviewer_points") or []
    rebuttal_rows = payload.get("rebuttal_rows") or []
    change_ledger = payload.get("change_ledger") or []
    evidence_pointers = payload.get("evidence_pointers") or []
    if not isinstance(reviewer_points, list):
        reviewer_points = []
    if not isinstance(rebuttal_rows, list):
        rebuttal_rows = []
    if not isinstance(change_ledger, list):
        change_ledger = []
    if not isinstance(evidence_pointers, list):
        evidence_pointers = []

    if not reviewer_points:
        return {
            "ok": False,
            "error": "empty_reviewer_points",
            "detail": "rebuttal consistency failed: empty_reviewer_points",
        }

    point_ids: list[str] = []
    seen_reviewer: set[str] = set()
    for point in reviewer_points:
        if not isinstance(point, dict):
            return {
                "ok": False,
                "error": "invalid_reviewer_point",
                "detail": "rebuttal consistency failed: invalid_reviewer_point",
            }
        pid = _nonempty_text(point.get("point_id"))
        text = _nonempty_text(point.get("text"))
        if not pid:
            return {
                "ok": False,
                "error": "empty_point_id",
                "detail": "rebuttal consistency failed: empty_point_id",
            }
        if not text:
            return {
                "ok": False,
                "error": "empty_point_text",
                "detail": f"rebuttal consistency failed: empty_point_text ({pid})",
            }
        if pid in seen_reviewer:
            return {
                "ok": False,
                "error": "duplicate_reviewer_point",
                "detail": (
                    f"rebuttal consistency failed: duplicate_reviewer_point ({pid})"
                ),
            }
        seen_reviewer.add(pid)
        point_ids.append(pid)

    reviewer_set = set(point_ids)
    rows_by_point: dict[str, list[dict]] = {}
    for row in rebuttal_rows:
        if not isinstance(row, dict):
            return {
                "ok": False,
                "error": "invalid_rebuttal_row",
                "detail": "rebuttal consistency failed: invalid_rebuttal_row",
            }
        pid = _nonempty_text(row.get("point_id"))
        if not pid:
            return {
                "ok": False,
                "error": "empty_point_id",
                "detail": "rebuttal consistency failed: empty_point_id (rebuttal row)",
            }
        rows_by_point.setdefault(pid, []).append(row)

    for pid, rows in rows_by_point.items():
        if len(rows) > 1:
            return {
                "ok": False,
                "error": "duplicate_point_row",
                "detail": f"rebuttal consistency failed: duplicate_point_row ({pid})",
            }
        if pid not in reviewer_set:
            return {
                "ok": False,
                "error": "orphan_point_row",
                "detail": f"rebuttal consistency failed: orphan_point_row ({pid})",
            }

    for pid in point_ids:
        rows = rows_by_point.get(pid) or []
        if not rows:
            return {
                "ok": False,
                "error": "missing_point_row",
                "detail": f"rebuttal consistency failed: missing_point_row ({pid})",
            }
        row = rows[0]
        coverage = _nonempty_text(row.get("coverage")).lower()
        response_kind = _nonempty_text(row.get("response_kind")).lower()
        pointer = _nonempty_text(row.get("pointer")) or _nonempty_text(row.get("gap_note"))

        if not coverage or coverage not in REBUTTAL_COVERAGE:
            return {
                "ok": False,
                "error": "invalid_coverage",
                "detail": f"rebuttal consistency failed: invalid_coverage ({pid})",
            }
        if not response_kind or response_kind not in REBUTTAL_RESPONSE_KINDS:
            return {
                "ok": False,
                "error": "invalid_response_kind",
                "detail": f"rebuttal consistency failed: invalid_response_kind ({pid})",
            }

        # Unresolved missing coverage always fails the audit (not only when
        # audit_marked_clean is true).
        if coverage == "missing":
            return {
                "ok": False,
                "error": "coverage_missing_unclear",
                "detail": (
                    f"rebuttal consistency failed: coverage_missing_unclear ({pid})"
                ),
            }

        if coverage == "partial" and not pointer:
            return {
                "ok": False,
                "error": "partial_without_gap_note",
                "detail": (
                    f"rebuttal consistency failed: partial_without_gap_note ({pid})"
                ),
            }

        if response_kind == "ms_change":
            linked = False
            for change in change_ledger:
                if not isinstance(change, dict):
                    continue
                ids = change.get("point_ids") or []
                if isinstance(ids, str):
                    ids = [ids]
                if pid in [str(x) for x in ids]:
                    linked = True
                    break
                if _nonempty_text(change.get("point_id")) == pid:
                    linked = True
                    break
            if not linked:
                return {
                    "ok": False,
                    "error": "asserted_change_absent",
                    "detail": (
                        f"rebuttal consistency failed: asserted_change_absent ({pid})"
                    ),
                }

        if response_kind == "evidence":
            ep = pointer
            if not ep:
                for item in evidence_pointers:
                    if not isinstance(item, dict):
                        continue
                    if _nonempty_text(item.get("point_id")) == pid and _nonempty_text(
                        item.get("pointer")
                    ):
                        ep = _nonempty_text(item.get("pointer"))
                        break
            if not ep:
                return {
                    "ok": False,
                    "error": "evidence_pointer_missing",
                    "detail": (
                        f"rebuttal consistency failed: evidence_pointer_missing ({pid})"
                    ),
                }

        if response_kind == "no_change_rationale" and not pointer:
            return {
                "ok": False,
                "error": "empty_no_change_rationale",
                "detail": (
                    f"rebuttal consistency failed: empty_no_change_rationale ({pid})"
                ),
            }

    return {"ok": True, "detail": f"rebuttal consistency ok: {len(point_ids)} points"}


def _disclosure_section(payload: dict, key: str) -> dict[str, Any]:
    """Return nested disclosure section dict, or empty mapping."""
    value = payload.get(key)
    if isinstance(value, dict):
        return value
    return {}


def _disclosure_details(section: dict[str, Any]) -> str:
    """Join non-empty detail fields from a disclosure section."""
    parts = [
        _nonempty_text(section.get("details")),
        _nonempty_text(section.get("text")),
        _nonempty_text(section.get("roles_text")),
        _nonempty_text(section.get("access_path")),
        _nonempty_text(section.get("restriction_reason")),
        _nonempty_text(section.get("venue")),
        _nonempty_text(section.get("policy")),
    ]
    authors = section.get("authors")
    if isinstance(authors, list):
        parts.extend(_nonempty_text(a) for a in authors)
    elif authors is not None:
        parts.append(_nonempty_text(authors))
    return " ".join(p for p in parts if p).strip()


def evaluate_disclosure_record(payload: dict) -> dict[str, Any]:
    """Fail-closed disclosure package integrity (E3-B record level).

    none_confirmed for funding/COI/AI requires human_confirmation and signer.
    unknown_pending_human is draft-only and blocks final packages.
    funded/interests_present/disclosed require non-empty details.
    data/code and policy/venue states are mandatory. Auto-fill and
    self-confirm flags fail. No field is auto-filled by this helper.
    """
    if not isinstance(payload, dict):
        return {
            "ok": False,
            "error": "invalid_payload",
            "detail": "disclosure record failed: payload must be a dict",
        }

    if bool(payload.get("auto_filled")):
        return {
            "ok": False,
            "error": "auto_filled_forbidden",
            "detail": "disclosure record failed: auto_filled_forbidden",
        }
    if bool(payload.get("self_confirmed")):
        return {
            "ok": False,
            "error": "self_confirmed_forbidden",
            "detail": "disclosure record failed: self_confirmed_forbidden",
        }

    package_state = _nonempty_text(payload.get("package_state")).lower()
    if package_state not in DISCLOSURE_PACKAGE_STATES:
        return {
            "ok": False,
            "error": "invalid_package_state",
            "detail": (
                "disclosure record failed: invalid_package_state "
                f"({package_state or '<empty>'})"
            ),
        }

    human_confirmation = bool(payload.get("human_confirmation"))
    signer = _nonempty_text(payload.get("signer"))
    timestamp = _nonempty_text(payload.get("timestamp"))

    credit = _disclosure_section(payload, "credit_authorship")
    if not _disclosure_details(credit):
        return {
            "ok": False,
            "error": "missing_credit_authorship",
            "detail": "disclosure record failed: missing_credit_authorship",
        }

    funding = _disclosure_section(payload, "funding")
    funding_status = _nonempty_text(funding.get("status")).lower()
    funding_details = _disclosure_details(funding)
    if funding_status not in DISCLOSURE_FUNDING_STATES:
        return {
            "ok": False,
            "error": "invalid_funding_status",
            "detail": (
                "disclosure record failed: invalid_funding_status "
                f"({funding_status or '<empty>'})"
            ),
        }
    if funding_status == "funded" and not funding_details:
        return {
            "ok": False,
            "error": "missing_funding_details",
            "detail": "disclosure record failed: missing_funding_details",
        }
    if funding_status == "none_confirmed" and (
        not human_confirmation or not signer
    ):
        return {
            "ok": False,
            "error": "none_confirmed_requires_human",
            "detail": (
                "disclosure record failed: none_confirmed_requires_human (funding)"
            ),
        }

    conflicts = _disclosure_section(payload, "conflicts")
    coi_status = _nonempty_text(conflicts.get("status")).lower()
    coi_details = _disclosure_details(conflicts)
    if coi_status not in DISCLOSURE_COI_STATES:
        return {
            "ok": False,
            "error": "invalid_coi_status",
            "detail": (
                "disclosure record failed: invalid_coi_status "
                f"({coi_status or '<empty>'})"
            ),
        }
    if coi_status == "interests_present" and not coi_details:
        return {
            "ok": False,
            "error": "missing_coi_details",
            "detail": "disclosure record failed: missing_coi_details",
        }
    if coi_status == "none_confirmed" and (not human_confirmation or not signer):
        return {
            "ok": False,
            "error": "none_confirmed_requires_human",
            "detail": (
                "disclosure record failed: none_confirmed_requires_human (conflicts)"
            ),
        }

    ai_section = _disclosure_section(payload, "ai_assistance")
    ai_status = _nonempty_text(ai_section.get("status")).lower()
    ai_details = _disclosure_details(ai_section)
    if ai_status not in DISCLOSURE_AI_STATES:
        return {
            "ok": False,
            "error": "invalid_ai_status",
            "detail": (
                "disclosure record failed: invalid_ai_status "
                f"({ai_status or '<empty>'})"
            ),
        }
    if ai_status == "disclosed" and not ai_details:
        return {
            "ok": False,
            "error": "missing_ai_details",
            "detail": "disclosure record failed: missing_ai_details",
        }
    if ai_status == "none_confirmed" and (not human_confirmation or not signer):
        return {
            "ok": False,
            "error": "none_confirmed_requires_human",
            "detail": (
                "disclosure record failed: none_confirmed_requires_human "
                "(ai_assistance)"
            ),
        }

    data_code = _disclosure_section(payload, "data_code_availability")
    data_status = _nonempty_text(data_code.get("status")).lower()
    data_details = _disclosure_details(data_code)
    if data_status not in DISCLOSURE_DATA_CODE_STATES:
        return {
            "ok": False,
            "error": "invalid_data_code_status",
            "detail": (
                "disclosure record failed: invalid_data_code_status "
                f"({data_status or '<empty>'})"
            ),
        }
    if data_status in {"available", "restricted", "blocked"} and not data_details:
        return {
            "ok": False,
            "error": "missing_data_code_details",
            "detail": "disclosure record failed: missing_data_code_details",
        }

    policy = _disclosure_section(payload, "policy_anchor_or_venue")
    policy_status = _nonempty_text(policy.get("status")).lower()
    # Accept Known? vocabulary and allow "known" synonym for yes.
    if policy_status == "known":
        policy_status = "yes"
    policy_details = _disclosure_details(policy)
    if policy_status not in DISCLOSURE_POLICY_STATES:
        return {
            "ok": False,
            "error": "invalid_policy_status",
            "detail": (
                "disclosure record failed: invalid_policy_status "
                f"({policy_status or '<empty>'})"
            ),
        }
    if policy_status == "yes" and not policy_details:
        return {
            "ok": False,
            "error": "missing_policy_details",
            "detail": "disclosure record failed: missing_policy_details",
        }

    pending_topics: list[str] = []
    if funding_status == "unknown_pending_human":
        pending_topics.append("funding")
    if coi_status == "unknown_pending_human":
        pending_topics.append("conflicts")
    if ai_status == "unknown_pending_human":
        pending_topics.append("ai_assistance")
    if data_status == "unknown_pending_human":
        pending_topics.append("data_code_availability")
    if package_state == "final" and pending_topics:
        return {
            "ok": False,
            "error": "unknown_pending_blocks_final",
            "detail": (
                "disclosure record failed: unknown_pending_blocks_final "
                f"({','.join(pending_topics)})"
            ),
        }

    if package_state == "final":
        if not human_confirmation:
            return {
                "ok": False,
                "error": "missing_human_confirmation",
                "detail": "disclosure record failed: missing_human_confirmation",
            }
        if not signer:
            return {
                "ok": False,
                "error": "missing_signer",
                "detail": "disclosure record failed: missing_signer",
            }
        if not timestamp:
            return {
                "ok": False,
                "error": "missing_timestamp",
                "detail": "disclosure record failed: missing_timestamp",
            }

    return {
        "ok": True,
        "detail": f"disclosure record ok: package_state={package_state}",
    }


def evaluate_mode_fields_text(
    text: str,
    mode_slug: str,
    field_ids: tuple[str, ...] | list[str] | None = None,
    *,
    min_chars: int = MIN_FIELD_BODY,
) -> tuple[bool, str]:
    """Validate mode-scoped field IDs for one paper mode (Strategy A)."""
    fields = field_ids or PAPER_MODE_CORE_FIELDS.get(mode_slug)
    if not fields:
        return False, f"unknown paper mode slug: {mode_slug}"
    ok, detail, missing = evaluate_required_fields(text, fields, min_chars=min_chars)
    if not ok:
        return False, f"mode isolation: {mode_slug}: {detail}"
    return True, f"mode {mode_slug} ok ({len(fields)} fields)"


def evaluate_all_paper_modes_text(text: str) -> tuple[bool, str]:
    """Independently validate all 11 academic-paper modes; first failure names mode."""
    if not _nonempty_text(text):
        return False, "e3 paper modes: empty protocol text"
    for mode_slug in PAPER_MODES:
        ok, detail = evaluate_mode_fields_text(text, mode_slug)
        if not ok:
            return False, f"e3 paper modes: {detail}"
    return True, f"e3 paper modes ok: {len(PAPER_MODES)} modes"


def evaluate_revision_template_text(text: str) -> tuple[bool, str]:
    """Required template fields on revision_roadmap.md only."""
    ok, detail, _ = evaluate_required_fields(text, REVISION_TEMPLATE_FIELDS)
    if not ok:
        return False, detail
    lower = strip_lineage_comments(text).lower()
    if "author" not in lower or "sign" not in lower:
        return False, "revision template missing author sign-off guidance"
    if "recover" not in lower and "checkpoint" not in lower:
        return False, "revision template missing recovery checkpoint guidance"
    if "protected" not in lower:
        return False, "revision template missing protected claims guidance"
    return True, f"revision template fields ok ({len(REVISION_TEMPLATE_FIELDS)})"


def evaluate_rebuttal_template_text(text: str) -> tuple[bool, str]:
    """Required template fields on rebuttal_audit.md only."""
    ok, detail, _ = evaluate_required_fields(text, REBUTTAL_TEMPLATE_FIELDS)
    if not ok:
        return False, detail
    lower = strip_lineage_comments(text).lower()
    if "evaluator-only" not in lower and "evaluator only" not in lower:
        return False, "rebuttal template missing evaluator-only discipline"
    if "coverage" not in lower:
        return False, "rebuttal template missing coverage matrix guidance"
    if "generated" in lower and "response" in lower:
        # Must forbid generated response prose, not endorse it.
        if not re.search(
            r"(?:no|not|never|forbid|do\s+not).{0,40}generated.{0,20}response",
            lower,
        ) and "no generated" not in lower:
            return False, "rebuttal template must forbid generated response prose"
    return True, f"rebuttal template fields ok ({len(REBUTTAL_TEMPLATE_FIELDS)})"


def evaluate_disclosure_polarity(text: str) -> tuple[bool, str]:
    """Reject optionalizing or auto-fabricating AI/funding/COI declarations.

    Prohibition language near the same topic (never/must not/do not/forbid) is
    allowed; bare endorsement or optionality without prohibition fails.
    """
    lower = strip_lineage_comments(text).lower()
    topics = (
        r"ai\s+assistance",
        r"funding",
        r"conflicts?(?:\s+of\s+interest)?",
        r"coi",
    )
    topic_alt = "|".join(topics)
    # Windowed optionalizing without a nearby prohibition cue.
    for match in re.finditer(
        rf"(?:{topic_alt}).{{0,80}}(?:optional|not\s+required|skippable)"
        rf"|(?:optional|not\s+required|skippable).{{0,80}}(?:{topic_alt})",
        lower,
    ):
        window = lower[max(0, match.start() - 48) : match.end() + 16]
        if not re.search(
            r"(?:must\s+not|do\s+not|don't|never|forbid(?:den)?|not\s+treat|cannot)",
            window,
        ):
            return (
                False,
                "disclosure polarity unsafe (optionalizes/auto-fabricates AI/funding/COI)",
            )

    for match in re.finditer(
        rf"(?:auto[- ]?fabricat\w*|fabricat\w*).{{0,60}}(?:{topic_alt}|disclosure|ai|funding|coi)"
        rf"|(?:{topic_alt}|disclosure).{{0,60}}(?:auto[- ]?fabricat\w*|fabricat\w*)"
        rf"|(?:may|can|should|freely)\s+(?:auto[- ]?)?fabricat\w*",
        lower,
    ):
        window = lower[max(0, match.start() - 48) : match.end() + 16]
        if not re.search(
            r"(?:must\s+not|do\s+not|don't|never|forbid(?:den)?)",
            window,
        ):
            return (
                False,
                "disclosure polarity unsafe (optionalizes/auto-fabricates AI/funding/COI)",
            )

    for topic in ("ai", "funding", "conflict"):
        if topic not in lower and not (topic == "conflict" and "coi" in lower):
            return False, f"disclosure missing mandatory topic language: {topic}"
    if "human" not in lower or "confirm" not in lower:
        return False, "disclosure missing human confirmation language"
    if "fabricat" in lower and not re.search(
        r"(?:must\s+not|do\s+not|don't|never|forbid).{0,40}fabricat",
        lower,
    ):
        return False, "disclosure mentions fabrication without prohibition"
    return True, "disclosure polarity ok"


def evaluate_disclosure_template_text(text: str) -> tuple[bool, str]:
    """Required template fields on disclosure_statement.md only."""
    ok, detail, _ = evaluate_required_fields(text, DISCLOSURE_TEMPLATE_FIELDS)
    if not ok:
        return False, detail
    pol_ok, pol_detail = evaluate_disclosure_polarity(text)
    if not pol_ok:
        return False, pol_detail
    lower = strip_lineage_comments(text).lower()
    if "credit" not in lower and "crédit" not in lower and "authorship" not in lower:
        return False, "disclosure template missing CRediT/authorship guidance"
    if "mandatory" not in lower and "must" not in lower:
        return False, "disclosure template missing mandatory-field language"
    return True, f"disclosure template fields ok ({len(DISCLOSURE_TEMPLATE_FIELDS)})"


def _truthy_flag(value: Any) -> bool:
    """Parse explicit human-confirmation style booleans fail-closed."""
    if value is True:
        return True
    if value is False or value is None:
        return False
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        return value == 1
    text = _nonempty_text(value).lower()
    return text in {"true", "yes", "y", "1", "confirmed"}


def _normalize_identity_kind(kind_raw: str) -> str:
    """Map identity kind aliases onto the closed vocabulary."""
    kind = kind_raw.lower().replace(" ", "_").replace("-", "_")
    if kind in {"anonymous", "anonymous_role"}:
        return "anonymous"
    if kind in {"simulated", "simulated_role", "role"}:
        return "simulated_role"
    if kind in NAMED_REAL_IDENTITY_KINDS:
        return "named_real"
    if "named" in kind or kind.endswith("_real") or kind == "real_person":
        return "named_real"
    return kind


def _identity_explicitly_labeled(payload: dict, kind: str) -> bool:
    """Require explicit anonymous/simulated labeling (display name alone is not enough)."""
    if _truthy_flag(payload.get("labeled_simulated")):
        return True
    if _truthy_flag(payload.get("labeled_anonymous")):
        return True
    if _truthy_flag(payload.get("simulated_label")):
        return True
    label_text = _nonempty_text(
        payload.get("label") or payload.get("role_label")
    ).lower()
    if "simulated" in label_text or "anonymous" in label_text:
        return True
    kind_raw = _nonempty_text(payload.get("identity_kind") or payload.get("kind")).lower()
    if kind == "anonymous" and "anonymous" in kind_raw:
        # Kind token alone is not a label; still need explicit label flag/text.
        return False
    return False


def _normalize_identity_text(value: str) -> str:
    """Normalize identity text for provenance comparison (spaces/hyphen/slash)."""
    text = value.lower().replace(" ", "_").replace("-", "_").replace("/", "_")
    while "__" in text:
        text = text.replace("__", "_")
    return text.strip("_")


def _source_has_exact_token(source_norm: str, token: str) -> bool:
    """True when token is the full source or a whole underscore-delimited unit."""
    if not token:
        return False
    if source_norm == token:
        return True
    # Contiguous whole-token match (handles multi-part tokens like n_a).
    return f"_{token}_" in f"_{source_norm}_"


def _source_is_forbidden(identity_source: str, display_name: str) -> bool:
    """Reject invented/assumed/self-asserted/circular identity provenance.

    Short sentinels (na/n_a/none/tbd/todo) match only as exact normalized values
    or explicit underscore tokens, never as arbitrary substrings. Longer phrase
    tokens keep substring detection for forbidden provenance wording.
    """
    source_norm = _normalize_identity_text(identity_source)
    if not source_norm:
        return False
    if source_norm in FORBIDDEN_IDENTITY_SOURCES:
        return True
    for token in FORBIDDEN_IDENTITY_EXACT_TOKENS:
        if _source_has_exact_token(source_norm, token):
            return True
    for phrase in FORBIDDEN_IDENTITY_PHRASES:
        if phrase in source_norm:
            return True
    name_norm = _normalize_identity_text(display_name)
    if name_norm and source_norm == name_norm:
        return True
    if name_norm and name_norm in source_norm and len(name_norm) >= 4:
        # Source that only restates the display name is circular/self-asserted.
        stripped = source_norm.replace(name_norm, "").strip("_")
        if stripped in {"", "self", "name", "display", "display_name", "reviewer"}:
            return True
    return False


def _evaluate_one_reviewer_identity(payload: dict) -> dict[str, Any]:
    """Validate a single identity payload (flat shape)."""
    kind_raw = _nonempty_text(
        payload.get("identity_kind") or payload.get("kind")
    )
    if not kind_raw:
        return {
            "ok": False,
            "error": "missing_identity_kind",
            "detail": "reviewer identity failed: missing_identity_kind",
        }

    kind = _normalize_identity_kind(kind_raw)
    display_name = _nonempty_text(
        payload.get("display_name")
        or payload.get("name")
        or payload.get("label")
        or payload.get("role_label")
    )
    identity_source = _nonempty_text(
        payload.get("identity_source") or payload.get("source")
    )
    human_confirmation = _truthy_flag(
        payload.get("human_confirmation")
        if "human_confirmation" in payload
        else payload.get("human_confirmed")
    )

    if kind in {"anonymous", "simulated_role"}:
        if not _identity_explicitly_labeled(payload, kind):
            return {
                "ok": False,
                "error": "unlabeled_simulated",
                "detail": (
                    "reviewer identity failed: unlabeled_simulated "
                    "(anonymous/simulated roles must be explicitly labeled; "
                    "display name alone is insufficient)"
                ),
            }
        return {
            "ok": True,
            "error": None,
            "detail": f"reviewer identity ok: {kind}",
        }

    if kind != "named_real" and kind not in REVIEWER_IDENTITY_KINDS:
        return {
            "ok": False,
            "error": "invalid_identity_kind",
            "detail": f"reviewer identity failed: invalid_identity_kind ({kind})",
        }

    if kind == "named_real":
        if not display_name:
            return {
                "ok": False,
                "error": "missing_display_name",
                "detail": "reviewer identity failed: missing_display_name",
            }
        if not identity_source:
            return {
                "ok": False,
                "error": "missing_identity_source",
                "detail": "reviewer identity failed: missing_identity_source",
            }
        if _source_is_forbidden(identity_source, display_name):
            return {
                "ok": False,
                "error": "forbidden_identity_source",
                "detail": (
                    "reviewer identity failed: forbidden_identity_source "
                    f"({identity_source})"
                ),
            }
        if not human_confirmation:
            return {
                "ok": False,
                "error": "missing_human_confirmation",
                "detail": "reviewer identity failed: missing_human_confirmation",
            }
        return {
            "ok": True,
            "error": None,
            "detail": "reviewer identity ok: named_real with source+confirm",
        }

    return {
        "ok": False,
        "error": "invalid_identity_kind",
        "detail": f"reviewer identity failed: invalid_identity_kind ({kind})",
    }


def evaluate_reviewer_identity(payload: dict) -> dict[str, Any]:
    """Validate reviewer-identity provenance for simulated vs named real peers.

    Anonymous and simulated_role identities are allowed only when explicitly
    labeled as such; an arbitrary display name alone never validates identity.
    Named real-person identities require a non-empty, non-circular
    identity_source (not invented/assumed/self-asserted) and explicit human
    confirmation. Accepts flat payloads or reviewer_labels list entries.
    Private helper: not a public gate ID; no multi-process isolation claim.

    Stable errors include invalid_payload, missing_identity_kind,
    missing_identity_source, forbidden_identity_source,
    missing_human_confirmation, missing_display_name, unlabeled_simulated,
    empty_label, and empty_reviewer_labels.
    """
    if not isinstance(payload, dict):
        return {
            "ok": False,
            "error": "invalid_payload",
            "detail": "reviewer identity failed: payload must be a dict",
        }

    labels = payload.get("reviewer_labels")
    if labels is not None:
        if not isinstance(labels, list) or not labels:
            return {
                "ok": False,
                "error": "empty_reviewer_labels",
                "detail": "reviewer identity failed: empty_reviewer_labels",
            }
        for idx, item in enumerate(labels):
            if not isinstance(item, dict):
                return {
                    "ok": False,
                    "error": "invalid_payload",
                    "detail": f"reviewer identity failed: invalid label row {idx}",
                }
            row = {
                "identity_kind": item.get("kind") or item.get("identity_kind"),
                "display_name": item.get("label")
                or item.get("display_name")
                or item.get("name"),
                "label": item.get("label"),
                "role_label": item.get("role_label"),
                "identity_source": item.get("source") or item.get("identity_source"),
                "human_confirmation": item.get("human_confirmed")
                if "human_confirmed" in item
                else item.get("human_confirmation"),
                "labeled_simulated": item.get("labeled_simulated"),
                "labeled_anonymous": item.get("labeled_anonymous"),
            }
            if not _nonempty_text(row.get("display_name") or row.get("label")):
                return {
                    "ok": False,
                    "error": "empty_label",
                    "detail": f"reviewer identity failed: empty_label at index {idx}",
                }
            result = _evaluate_one_reviewer_identity(row)
            if not result.get("ok"):
                return result
        return {
            "ok": True,
            "error": None,
            "detail": f"reviewer identity ok: {len(labels)} labeled entries",
        }

    # Display name alone without kind is never valid.
    if not _nonempty_text(payload.get("identity_kind") or payload.get("kind")):
        if _nonempty_text(
            payload.get("display_name") or payload.get("name") or payload.get("label")
        ):
            return {
                "ok": False,
                "error": "missing_identity_kind",
                "detail": (
                    "reviewer identity failed: missing_identity_kind "
                    "(display name alone is not valid identity)"
                ),
            }
    return _evaluate_one_reviewer_identity(payload)


def _rereview_pointer(row: dict[str, Any]) -> str:
    """Extract manuscript/evidence pointer text from a residual row."""
    return _nonempty_text(
        row.get("pointer")
        or row.get("evidence_pointer")
        or row.get("manuscript_pointer")
    )


def _rereview_residual_gap(row: dict[str, Any]) -> str:
    """Extract residual gap note required for partially_addressed rows."""
    return _nonempty_text(
        row.get("residual_gap")
        or row.get("gap_note")
        or row.get("remaining_gap")
        or row.get("residual")
    )


def evaluate_rereview_consistency(payload: dict) -> dict[str, Any]:
    """Deterministic re-review residual trajectory consistency (E3-C).

    Prior issue IDs must be non-empty and unique. Current rows must cover prior
    issues exactly once each. Trajectory vocabulary is open |
    partially_addressed | addressed | new. addressed and partially_addressed
    require a non-empty manuscript/evidence pointer; partially_addressed also
    requires a non-empty residual gap. New issues are additive only and never
    satisfy missing prior coverage. Orphan non-new IDs fail. Blanket
    claim_all_fixed without every prior issue addressed+pointer fails.

    Stable errors: invalid_payload, empty_prior_issues, empty_issue_id,
    duplicate_prior_issue, missing_prior_coverage, orphan_issue_row,
    invalid_trajectory, addressed_without_pointer, partial_without_residual,
    new_as_prior_closure, blanket_all_fixed, duplicate_current_issue.
    """
    if not isinstance(payload, dict):
        return {
            "ok": False,
            "error": "invalid_payload",
            "detail": "re-review consistency failed: payload must be a dict",
        }

    prior_raw = payload.get("prior_issues") or []
    current_raw = payload.get("current_rows") or []
    if not isinstance(prior_raw, list):
        prior_raw = []
    if not isinstance(current_raw, list):
        current_raw = []

    if not prior_raw:
        return {
            "ok": False,
            "error": "empty_prior_issues",
            "detail": "re-review consistency failed: empty_prior_issues",
        }

    prior_ids: list[str] = []
    seen_prior: set[str] = set()
    for item in prior_raw:
        if isinstance(item, dict):
            iid = _nonempty_text(item.get("issue_id") or item.get("concern_id"))
        else:
            iid = _nonempty_text(item)
        if not iid:
            return {
                "ok": False,
                "error": "empty_issue_id",
                "detail": "re-review consistency failed: empty_issue_id (prior)",
            }
        if iid in seen_prior:
            return {
                "ok": False,
                "error": "duplicate_prior_issue",
                "detail": f"re-review consistency failed: duplicate_prior_issue ({iid})",
            }
        seen_prior.add(iid)
        prior_ids.append(iid)

    prior_set = set(prior_ids)
    current_by_id: dict[str, list[dict[str, Any]]] = {}
    for row in current_raw:
        if not isinstance(row, dict):
            return {
                "ok": False,
                "error": "invalid_current_row",
                "detail": "re-review consistency failed: invalid_current_row",
            }
        iid = _nonempty_text(row.get("issue_id") or row.get("concern_id"))
        if not iid:
            return {
                "ok": False,
                "error": "empty_issue_id",
                "detail": "re-review consistency failed: empty_issue_id (current)",
            }
        current_by_id.setdefault(iid, []).append(row)

    for iid, rows in current_by_id.items():
        if len(rows) > 1:
            return {
                "ok": False,
                "error": "duplicate_current_issue",
                "detail": (
                    f"re-review consistency failed: duplicate_current_issue ({iid})"
                ),
            }

    for iid in prior_ids:
        rows = current_by_id.get(iid) or []
        if not rows:
            return {
                "ok": False,
                "error": "missing_prior_coverage",
                "detail": (
                    f"re-review consistency failed: missing_prior_coverage ({iid})"
                ),
            }
        row = rows[0]
        traj = _nonempty_text(row.get("trajectory")).lower().replace(" ", "_")
        if traj not in REREVIEW_TRAJECTORIES:
            return {
                "ok": False,
                "error": "invalid_trajectory",
                "detail": (
                    f"re-review consistency failed: invalid_trajectory ({iid}={traj})"
                ),
            }
        if traj == "new":
            return {
                "ok": False,
                "error": "new_as_prior_closure",
                "detail": (
                    "re-review consistency failed: new_as_prior_closure "
                    f"({iid} is a prior issue marked new)"
                ),
            }
        pointer = _rereview_pointer(row)
        if traj in REREVIEW_NEEDS_POINTER and not pointer:
            return {
                "ok": False,
                "error": "addressed_without_pointer",
                "detail": (
                    f"re-review consistency failed: addressed_without_pointer ({iid})"
                ),
            }
        if traj == "partially_addressed" and not _rereview_residual_gap(row):
            return {
                "ok": False,
                "error": "partial_without_residual",
                "detail": (
                    "re-review consistency failed: partial_without_residual "
                    f"({iid} needs residual gap)"
                ),
            }

    for iid, rows in current_by_id.items():
        if iid in prior_set:
            continue
        row = rows[0]
        traj = _nonempty_text(row.get("trajectory")).lower().replace(" ", "_")
        if traj != "new":
            return {
                "ok": False,
                "error": "orphan_issue_row",
                "detail": (
                    f"re-review consistency failed: orphan_issue_row ({iid} traj={traj})"
                ),
            }
        if traj not in REREVIEW_TRAJECTORIES:
            return {
                "ok": False,
                "error": "invalid_trajectory",
                "detail": f"re-review consistency failed: invalid_trajectory ({iid})",
            }

    claim_all_fixed = bool(payload.get("claim_all_fixed"))
    if claim_all_fixed:
        for iid in prior_ids:
            row = current_by_id[iid][0]
            traj = _nonempty_text(row.get("trajectory")).lower().replace(" ", "_")
            pointer = _rereview_pointer(row)
            if traj != "addressed" or not pointer:
                return {
                    "ok": False,
                    "error": "blanket_all_fixed",
                    "detail": (
                        "re-review consistency failed: blanket_all_fixed "
                        f"(prior {iid} not addressed with pointer)"
                    ),
                }

    return {
        "ok": True,
        "error": None,
        "detail": (
            f"re-review consistency ok: {len(prior_ids)} prior + "
            f"{sum(1 for i in current_by_id if i not in prior_set)} new"
        ),
    }


def _calibration_fail(error: str, detail: str) -> dict[str, Any]:
    """Fail closed without emitting metrics from an invalid calibration set."""
    return {
        "ok": False,
        "error": error,
        "detail": detail,
        "metrics": None,
    }


def evaluate_calibration_gold(payload: dict) -> dict[str, Any]:
    """Require human-supplied gold labels with matching prediction IDs (E3-C).

    Missing or empty gold fails with missing_calibration_gold or empty_gold.
    Accepted gold range is MIN_CALIBRATION_GOLD_ITEMS–MAX_CALIBRATION_GOLD_ITEMS
    (5–20) non-empty gold rows; fewer than 5 fails inadequate_gold_set and more
    than 20 fails excessive_gold_set. Complete one-to-one prediction mapping is
    required: unique non-empty gold/prediction IDs, non-empty labels, no orphan
    predictions, no uncovered gold IDs. fabricated_labels and persistent
    calibration claims fail. Invalid sets never return agreement metrics.
    Session-only only; never invent ground truth. Private helper — not a public
    gate ID.

    Stable errors: invalid_payload, missing_calibration_gold, empty_gold,
    inadequate_gold_set, excessive_gold_set, empty_item_id, empty_label,
    duplicate_gold_id, duplicate_prediction_id, mismatched_prediction_ids,
    fabricated_labels, persistent_calibration_claim.
    """
    if not isinstance(payload, dict):
        return _calibration_fail(
            "invalid_payload",
            "calibration gold failed: payload must be a dict",
        )

    if bool(payload.get("fabricated_labels")):
        return _calibration_fail(
            "fabricated_labels",
            "calibration gold failed: fabricated_labels",
        )

    if bool(payload.get("persistent_calibration_claim")):
        return _calibration_fail(
            "persistent_calibration_claim",
            "calibration gold failed: persistent_calibration_claim",
        )

    # session_only defaults to required true when key present as false.
    if "session_only" in payload and payload.get("session_only") is False:
        return _calibration_fail(
            "persistent_calibration_claim",
            (
                "calibration gold failed: persistent_calibration_claim "
                "(session_only=false)"
            ),
        )

    if "gold_labels" not in payload or payload.get("gold_labels") is None:
        return _calibration_fail(
            "missing_calibration_gold",
            "calibration gold failed: missing_calibration_gold",
        )

    gold_raw = payload.get("gold_labels")
    predictions_raw = payload.get("predictions") or []
    if not isinstance(gold_raw, list):
        return _calibration_fail(
            "missing_calibration_gold",
            "calibration gold failed: missing_calibration_gold",
        )
    if not isinstance(predictions_raw, list):
        predictions_raw = []

    if not gold_raw:
        return _calibration_fail(
            "empty_gold",
            "calibration gold failed: empty_gold",
        )

    if len(gold_raw) < MIN_CALIBRATION_GOLD_ITEMS:
        return _calibration_fail(
            "inadequate_gold_set",
            (
                "calibration gold failed: inadequate_gold_set "
                f"(need >={MIN_CALIBRATION_GOLD_ITEMS} gold items, got {len(gold_raw)})"
            ),
        )

    if len(gold_raw) > MAX_CALIBRATION_GOLD_ITEMS:
        return _calibration_fail(
            "excessive_gold_set",
            (
                "calibration gold failed: excessive_gold_set "
                f"(need <={MAX_CALIBRATION_GOLD_ITEMS} gold items, got {len(gold_raw)})"
            ),
        )

    gold_ids: list[str] = []
    seen_gold: set[str] = set()
    for item in gold_raw:
        if not isinstance(item, dict):
            return _calibration_fail(
                "invalid_gold_row",
                "calibration gold failed: invalid_gold_row",
            )
        iid = _nonempty_text(item.get("item_id") or item.get("id"))
        label = _nonempty_text(item.get("label") or item.get("gold_label"))
        if not iid:
            return _calibration_fail(
                "empty_item_id",
                "calibration gold failed: empty_item_id (gold)",
            )
        if not label:
            return _calibration_fail(
                "empty_label",
                f"calibration gold failed: empty_label (gold {iid})",
            )
        if iid in seen_gold:
            return _calibration_fail(
                "duplicate_gold_id",
                f"calibration gold failed: duplicate_gold_id ({iid})",
            )
        seen_gold.add(iid)
        gold_ids.append(iid)

    gold_set = set(gold_ids)
    pred_ids: list[str] = []
    seen_pred: set[str] = set()
    for item in predictions_raw:
        if not isinstance(item, dict):
            return _calibration_fail(
                "invalid_prediction_row",
                "calibration gold failed: invalid_prediction_row",
            )
        iid = _nonempty_text(item.get("item_id") or item.get("id"))
        label = _nonempty_text(item.get("label") or item.get("prediction_label"))
        if not iid:
            return _calibration_fail(
                "empty_item_id",
                "calibration gold failed: empty_item_id (prediction)",
            )
        if not label:
            return _calibration_fail(
                "empty_label",
                f"calibration gold failed: empty_label (prediction {iid})",
            )
        if iid in seen_pred:
            return _calibration_fail(
                "duplicate_prediction_id",
                f"calibration gold failed: duplicate_prediction_id ({iid})",
            )
        if iid not in gold_set:
            return _calibration_fail(
                "mismatched_prediction_ids",
                f"calibration gold failed: mismatched_prediction_ids ({iid})",
            )
        seen_pred.add(iid)
        pred_ids.append(iid)

    # Require predictions cover gold when predictions provided; if empty
    # predictions with gold, still fail mismatch for incomplete calibration run.
    if not predictions_raw:
        return _calibration_fail(
            "mismatched_prediction_ids",
            "calibration gold failed: mismatched_prediction_ids (no predictions)",
        )

    missing_preds = [gid for gid in gold_ids if gid not in set(pred_ids)]
    if missing_preds:
        return _calibration_fail(
            "mismatched_prediction_ids",
            (
                "calibration gold failed: mismatched_prediction_ids "
                f"(missing predictions for {missing_preds})"
            ),
        )

    return {
        "ok": True,
        "error": None,
        "detail": f"calibration gold ok: {len(gold_ids)} session-only items",
        "metrics": None,
    }


def evaluate_reviewer_mode_fields_text(
    text: str,
    mode_slug: str,
    field_ids: tuple[str, ...] | list[str] | None = None,
    *,
    min_chars: int = MIN_FIELD_BODY,
) -> tuple[bool, str]:
    """Validate mode-scoped field IDs for one manuscript-review mode (E3-C).

    Uses first labeled occurrence so a later duplicate field body cannot rescue
    a hollow mode-local field.
    """
    fields = field_ids or REVIEWER_MODE_CORE_FIELDS.get(mode_slug)
    if not fields:
        return False, f"unknown reviewer mode slug: {mode_slug}"
    ok, detail, _missing = evaluate_required_fields_first(
        text, fields, min_chars=min_chars
    )
    if not ok:
        return False, f"mode isolation: {mode_slug}: {detail}"
    return True, f"mode {mode_slug} ok ({len(fields)} fields)"


def evaluate_all_reviewer_modes_text(text: str) -> tuple[bool, str]:
    """Independently validate all six manuscript-review modes; first failure names mode.

    Each mode field set is checked in isolation via labeled field bodies so a
    complete peer mode cannot rescue a hollow mode. Used by content_depth and
    reviewer_independence public gates without adding new public gate IDs.
    """
    if not _nonempty_text(text):
        return False, "e3 reviewer modes: empty protocol text"
    for mode_slug in REVIEWER_MODES:
        ok, detail = evaluate_reviewer_mode_fields_text(text, mode_slug)
        if not ok:
            return False, f"e3 reviewer modes: {detail}"
    # Mode honesty polarity on the full protocol text.
    quick_ok, quick_detail = evaluate_quick_mode_honesty(text)
    if not quick_ok:
        return False, f"e3 reviewer modes: {quick_detail}"
    guided_ok, guided_detail = evaluate_guided_mode_honesty(text)
    if not guided_ok:
        return False, f"e3 reviewer modes: {guided_detail}"
    return True, f"e3 reviewer modes ok: {len(REVIEWER_MODES)} modes"


def evaluate_quick_mode_honesty(text: str) -> tuple[bool, str]:
    """Fail if quick mode claims full-panel completion without prohibition.

    Detects endorsement of full-panel completion inside quick-mode surfaces.
    Prohibition language (must not / never / forbid / cannot claim) near the
    claim is allowed. Used for protocol polarity and adversarial dumps.
    """
    lower = strip_lineage_comments(text).lower()
    # If there is no quick-mode content, skip (template-only surfaces).
    if "quick" not in lower:
        return True, "quick honesty skip (no quick surface)"

    # Forbidden endorsement without nearby prohibition.
    patterns = (
        r"quick.{0,80}(?:full[- ]panel|four\s+independent|completed\s+full\s+panel)",
        r"(?:full[- ]panel\s+completion|full\s+panel\s+complete).{0,80}quick",
        r"quick\s+mode\s+(?:completes|completed|provides)\s+full",
    )
    for pattern in patterns:
        for match in re.finditer(pattern, lower):
            window = lower[max(0, match.start() - 60) : match.end() + 40]
            if not re.search(
                r"(?:must\s+not|do\s+not|don't|never|forbid(?:den)?|cannot|no\s+full)",
                window,
            ):
                return False, "quick mode honesty failed: claims full-panel completion"
    # Required prohibition field language on protocol.
    if "quick_no_full_panel_claim" in lower or "never claim full-panel" in lower:
        return True, "quick honesty ok"
    if re.search(
        r"(?:must\s+not|never|forbid).{0,40}full[- ]panel",
        lower,
    ):
        return True, "quick honesty ok"
    # If quick mode fields exist, require anti-claim language.
    if "quick_mode_outputs" in lower or "### quick_" in lower:
        if not re.search(r"(?:full[- ]panel|four\s+independent)", lower):
            return False, "quick mode honesty failed: missing full-panel non-claim"
    return True, "quick honesty ok"


def evaluate_guided_mode_honesty(text: str) -> tuple[bool, str]:
    """Fail if guided mode becomes a one-shot info dump without checkpoints.

    Guided mode must preserve a real question → response → checkpoint
    progression. Endorsing a single exhaustive review dump as guided output
    without prohibition fails. A one-shot information dump merely labeled as
    dialogue also fails. Protocol fields that forbid one-shot dumps and state
    dialogue checkpoints pass when progression language is present.
    """
    lower = strip_lineage_comments(text).lower()
    if "guided" not in lower:
        return True, "guided honesty skip (no guided surface)"

    prohibition = (
        r"(?:must\s+not|do\s+not|don't|never|forbid(?:s|den)?|cannot|"
        r"no\s+one[- ]shot|stop\s+one[- ]shot|skip(?:ping)?\s+dialogue|"
        r"guided_no_oneshot_dump|against\s+one[- ]shot)"
    )

    # One-shot dump endorsement without prohibition.
    for match in re.finditer(
        r"(?:one[- ]shot|oneshot|single[- ]turn).{0,40}(?:full\s+review|info\s*dump|exhaustive)"
        r"|(?:info\s*dump).{0,40}(?:full\s+review|guided)"
        r"|(?:deliver\s+a\s+one[- ]shot)",
        lower,
    ):
        window = lower[max(0, match.start() - 120) : match.end() + 80]
        if not re.search(prohibition, window):
            return False, "guided mode honesty failed: one-shot dump endorsement"

    # Require checkpoint/dialogue language when guided mode fields present.
    if "guided_mode_outputs" in lower or "### guided_" in lower:
        if "checkpoint" not in lower and "dialogue" not in lower:
            return False, "guided mode honesty failed: missing dialogue/checkpoint"
        # Real progression: question + response/answer + checkpoint.
        has_question = bool(
            re.search(r"(?:question|clarifying\s+question|ask)", lower)
        )
        has_response = bool(
            re.search(r"(?:response|answer|user\s+answer|confirmation)", lower)
        )
        has_checkpoint = "checkpoint" in lower
        if not (has_question and has_response and has_checkpoint):
            return False, (
                "guided mode honesty failed: missing question-response-checkpoint "
                "progression"
            )
        if "guided_no_oneshot_dump" not in lower and not re.search(
            r"(?:must\s+not|never|forbid|stop).{0,60}(?:one[- ]shot|oneshot|dump)",
            lower,
        ):
            return False, "guided mode honesty failed: missing one-shot prohibition"
    return True, "guided honesty ok"


def evaluate_guided_dialogue(payload: dict) -> dict[str, Any]:
    """Structured guided-mode progression: question → response → checkpoint.

    Rejects one-shot dumps labeled as dialogue and empty/missing turn chains.
    Private helper for reviewer_independence fixtures and unit tests.
    """
    if not isinstance(payload, dict):
        return {
            "ok": False,
            "error": "invalid_payload",
            "detail": "guided dialogue failed: payload must be a dict",
        }
    if bool(payload.get("oneshot_dump")) or bool(payload.get("one_shot_dump")):
        return {
            "ok": False,
            "error": "oneshot_dump",
            "detail": "guided dialogue failed: oneshot_dump",
        }
    turns = payload.get("turns") or payload.get("checkpoints") or []
    if not isinstance(turns, list) or len(turns) < 2:
        return {
            "ok": False,
            "error": "missing_progression",
            "detail": "guided dialogue failed: missing_progression (need >=2 turns)",
        }
    for idx, turn in enumerate(turns):
        if not isinstance(turn, dict):
            return {
                "ok": False,
                "error": "invalid_turn",
                "detail": f"guided dialogue failed: invalid_turn at {idx}",
            }
        question = _nonempty_text(
            turn.get("question") or turn.get("prompt") or turn.get("ask")
        )
        response = _nonempty_text(
            turn.get("response")
            or turn.get("answer")
            or turn.get("user_answer")
            or turn.get("human_response")
        )
        checkpoint = _nonempty_text(
            turn.get("checkpoint_id")
            or turn.get("checkpoint")
            or turn.get("id")
        )
        if not question:
            return {
                "ok": False,
                "error": "missing_question",
                "detail": f"guided dialogue failed: missing_question at turn {idx}",
            }
        if not response:
            return {
                "ok": False,
                "error": "missing_response",
                "detail": f"guided dialogue failed: missing_response at turn {idx}",
            }
        if not checkpoint:
            return {
                "ok": False,
                "error": "missing_checkpoint",
                "detail": f"guided dialogue failed: missing_checkpoint at turn {idx}",
            }
    return {
        "ok": True,
        "error": None,
        "detail": f"guided dialogue ok: {len(turns)} checkpoints",
    }


def evaluate_manuscript_review_template_text(text: str) -> tuple[bool, str]:
    """Required designated fields on manuscript_review_full.md only.

    Protocol duplicates and later duplicate labeled fields cannot rescue a
    hollow first occurrence. Checks independent section scaffolds, synthesis
    barrier, minority disposition, decision letter, and revision roadmap.
    """
    ok, detail, _ = evaluate_required_fields_first(
        text, MANUSCRIPT_REVIEW_TEMPLATE_FIELDS
    )
    if not ok:
        return False, detail
    lower = strip_lineage_comments(text).lower()
    if "disposition" not in lower:
        return False, "manuscript review template missing disposition guidance"
    if "simulated" not in lower:
        return False, "manuscript review template missing simulated decision guidance"
    if "synthesis" not in lower:
        return False, "manuscript review template missing synthesis barrier guidance"
    return True, (
        f"manuscript review template fields ok "
        f"({len(MANUSCRIPT_REVIEW_TEMPLATE_FIELDS)})"
    )


def evaluate_editorial_decision_template_text(text: str) -> tuple[bool, str]:
    """Required designated fields on editorial_decision.md only.

    Protocol completeness and later duplicate fields cannot rescue hollow
    decision-class, simulated disclaimer, blocking, non-blocking, minority, or
    human-authority first occurrences.
    """
    ok, detail, _ = evaluate_required_fields_first(
        text, EDITORIAL_DECISION_TEMPLATE_FIELDS
    )
    if not ok:
        return False, detail
    lower = strip_lineage_comments(text).lower()
    if "simulated" not in lower:
        return False, "editorial decision template missing simulated disclaimer"
    if "minority" not in lower and "devil" not in lower:
        return False, "editorial decision template missing minority retention"
    if "human" not in lower:
        return False, "editorial decision template missing human authority gate"
    return True, (
        f"editorial decision template fields ok "
        f"({len(EDITORIAL_DECISION_TEMPLATE_FIELDS)})"
    )


def g_prisma_fields(methods_root: Path) -> dict[str, Any]:
    ok, detail = evaluate_prisma_fields_surfaces(
        systematic_review=_read_methods_surface(methods_root, SR_PROTOCOL_REL),
        prisma_protocol=_read_methods_surface(methods_root, PRISMA_PROTOCOL_REL),
        prisma_report=_read_methods_surface(methods_root, PRISMA_REPORT_REL),
    )
    return gate_result("prisma_fields", ok, detail)


def g_rob2_fields(methods_root: Path) -> dict[str, Any]:
    surfaces = {
        rel: _read_methods_surface(methods_root, rel)
        for rel in E2_METHOD_SURFACE_RELS
    }
    ok, detail = evaluate_method_fields_on_surfaces(
        evaluate_rob2_fields_text, surfaces
    )
    return gate_result("rob2_fields", ok, detail)


def g_robins_i_fields(methods_root: Path) -> dict[str, Any]:
    surfaces = {
        rel: _read_methods_surface(methods_root, rel)
        for rel in E2_METHOD_SURFACE_RELS
    }
    ok, detail = evaluate_method_fields_on_surfaces(
        evaluate_robins_i_fields_text, surfaces
    )
    return gate_result("robins_i_fields", ok, detail)


def g_grade_fields(methods_root: Path) -> dict[str, Any]:
    surfaces = {
        rel: _read_methods_surface(methods_root, rel)
        for rel in E2_METHOD_SURFACE_RELS
    }
    ok, detail = evaluate_method_fields_on_surfaces(
        evaluate_grade_fields_text, surfaces
    )
    return gate_result("grade_fields", ok, detail)


def g_effect_hetero_sensitivity(methods_root: Path) -> dict[str, Any]:
    surfaces = {
        rel: _read_methods_surface(methods_root, rel)
        for rel in E2_METHOD_SURFACE_RELS
    }
    ok, detail = evaluate_method_fields_on_surfaces(
        evaluate_effect_hetero_sensitivity_text, surfaces
    )
    return gate_result("effect_hetero_sensitivity", ok, detail)


def g_anti_pooling_fields(methods_root: Path) -> dict[str, Any]:
    surfaces = {
        rel: _read_methods_surface(methods_root, rel)
        for rel in E2_METHOD_SURFACE_RELS
    }
    ok, detail = evaluate_method_fields_on_surfaces(
        evaluate_anti_pooling_fields_text, surfaces
    )
    return gate_result("anti_pooling_fields", ok, detail)


def g_stats_fallacies_11(methods_root: Path) -> dict[str, Any]:
    """E4 gate: honest not_started until experiment/stats depth lands."""
    markers = []
    for rel in (
        "core/templates/statistical_validation.md",
        "core/protocols/experiment.md",
    ):
        path = methods_root / rel
        if path.is_file() and "parity: not_started" in read_text(path):
            markers.append(rel)
    detail = (
        f"E4 semantic gate 'stats_fallacies_11' is not claimed pass while "
        f"experiment/stats bodies are parity: not_started "
        f"({', '.join(markers) or 'markers missing'})"
    )
    return gate_result("stats_fallacies_11", False, detail, status="not_started")


GATE_FUNCS: dict[str, Callable[[Path], dict[str, Any]]] = {
    "single_root_skill": g_single_root_skill,
    "alias_coverage": g_alias_coverage,
    "vague_topic_socratic": g_vague_topic_socratic,
    "mode_registry_coverage": g_mode_registry_coverage,
    "reviewer_independence": g_reviewer_independence,
    "passport_reset_contract": g_passport_reset_contract,
    "evidence_state_vocab": g_evidence_state_vocab,
    "claim_verdict_vocab": g_claim_verdict_vocab,
    "hook_safety": g_hook_safety,
    "optional_runtime_honesty": g_optional_runtime_honesty,
    "generator_evaluator_separation": g_generator_evaluator_separation,
    "upstream_provenance": g_upstream_provenance,
    "file_lineage_headers": g_file_lineage_headers,
    "content_depth": g_content_depth,
    "prisma_fields": g_prisma_fields,
    "rob2_fields": g_rob2_fields,
    "robins_i_fields": g_robins_i_fields,
    "grade_fields": g_grade_fields,
    "effect_hetero_sensitivity": g_effect_hetero_sensitivity,
    "anti_pooling_fields": g_anti_pooling_fields,
    "stats_fallacies_11": g_stats_fallacies_11,
}


def all_gate_ids() -> list[str]:
    return sorted(GATE_FUNCS.keys())


def run_gate(methods_root: Path, gate_id: str) -> dict[str, Any]:
    func = GATE_FUNCS.get(gate_id)
    if func is None:
        return gate_result(gate_id, False, "unknown gate id", status="error")
    return func(methods_root)


def emit(obj: dict[str, Any], as_json: bool) -> None:
    if as_json:
        sys.stdout.write(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")
    else:
        sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Essential Core quality gates")
    common = argparse.ArgumentParser(add_help=False)
    common.add_argument("--root", default=None, help="methods root override")
    common.add_argument("--json", action="store_true")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("list", parents=[common], help="List gate ids")
    p_gate = sub.add_parser("gate", parents=[common], help="Run a single gate")
    p_gate.add_argument("--id", required=True)
    sub.add_parser("all", parents=[common], help="Run all gates")
    args = parser.parse_args(argv)

    methods_root = root_from_args(args.root)
    if not methods_root.is_dir():
        emit({"ok": False, "error": "missing_root", "message": str(methods_root)}, args.json)
        return EXIT_IO

    if args.command == "list":
        ids = all_gate_ids()
        emit(
            {
                "ok": True,
                "gates": ids,
                "e1_executable": sorted(
                    gid for gid in GATE_FUNCS if gid not in E2_SEMANTIC_GATES
                ),
                "e2_method_gates": sorted(E2_METHOD_GATES),
                "e4_semantic_not_started": sorted(E4_SEMANTIC_GATES),
            },
            args.json,
        )
        return EXIT_OK

    if args.command == "gate":
        if args.id not in all_gate_ids():
            emit({"ok": False, "error": "bad_gate_id", "message": args.id}, args.json)
            return EXIT_USAGE
        result = run_gate(methods_root, args.id)
        emit(
            {
                "ok": bool(result["ok"]),
                "failed": [] if result["ok"] else [args.id],
                "passed": [args.id] if result["ok"] else [],
                "results": [result],
            },
            args.json,
        )
        return EXIT_OK if result["ok"] else EXIT_FAIL

    if args.command == "all":
        results = [run_gate(methods_root, gid) for gid in all_gate_ids()]
        passed = [r["id"] for r in results if r["ok"]]
        failed = [r["id"] for r in results if not r["ok"]]
        emit(
            {
                "ok": len(failed) == 0,
                "failed": failed,
                "passed": passed,
                "results": results,
            },
            args.json,
        )
        return EXIT_OK if not failed else EXIT_FAIL

    return EXIT_USAGE


if __name__ == "__main__":
    raise SystemExit(main())
