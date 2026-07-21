"""Behavioral tests for Essential Core quality gates.

Grok annotation: Added by Grok on 2026-07-20 for E1.
Grok annotation: content_depth mutation tests and structured coverage by Grok
on 2026-07-20 (E0/E1 revision 1).
Grok annotation: V2-2/V2-3 reset-ledger + reviewer-stage negatives by Grok on
2026-07-20 (revision 2).
Grok annotation: E2-R1–R5 adversarial negatives by Grok on 2026-07-20
(e2-review-revision-2).
Grok annotation: E3-A citation integrity adversarial tests by Grok on 2026-07-20.
Grok annotation: E3-B paper modes/revision/rebuttal/disclosure tests by Grok on 2026-07-20.
Grok annotation: E3-B revision-1 false-pass closure tests by Grok on 2026-07-20.
Grok annotation: E3-B revision-2 ledger add/move/annotate + unique change_id by Grok on 2026-07-20.
Grok annotation: E3-C manuscript-review modes/identity/re-review/calibration tests by Grok on 2026-07-20.
"""

from __future__ import annotations

import importlib.util
import json
import re
import subprocess
import sys
from pathlib import Path
from typing import Any

METHODS_ROOT = Path(__file__).resolve().parents[2]
GATES = METHODS_ROOT / "runtime" / "scripts" / "essential_quality_gates.py"
REPO_ROOT = METHODS_ROOT.parents[1]


def run_gates(args: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        [sys.executable, str(GATES), *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        check=False,
    )


def load_gates_module() -> Any:
    """Load essential_quality_gates as a module for direct helper tests."""
    spec = importlib.util.spec_from_file_location("essential_quality_gates_test", GATES)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load quality gates module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def _read_surface(rel: str) -> str:
    """Read one methods-pack surface relative to METHODS_ROOT."""
    return (METHODS_ROOT / rel).read_text(encoding="utf-8")


def _hollow_field(text: str, field_id: str, replacement_body: str) -> str:
    """Replace every labeled heading body for field_id with replacement_body."""
    pattern = (
        rf"(?m)^(#{{1,6}}\s+`?{re.escape(field_id)}`?[^\n]*\n)"
        rf"([\s\S]*?)(?=^#{{1,6}}\s|\Z)"
    )
    return re.sub(
        pattern,
        lambda m: m.group(1) + replacement_body + "\n\n",
        text,
    )


def _replace_local_cue(text: str, field_id: str, old_cue: str, new_cue: str) -> str:
    """Swap domain label cues only inside the field's local heading+body block."""
    mod = load_gates_module()
    match = mod.extract_labeled_field_match(text, field_id)
    if match is None:
        raise RuntimeError(f"missing labeled block for {field_id}")
    full = match.group(0)
    if old_cue.lower() not in full.lower():
        raise RuntimeError(f"{field_id} does not contain local cue {old_cue!r}")
    # Replace every local occurrence so residual local cues cannot keep the field green.
    patched = re.sub(re.escape(old_cue), new_cue, full, flags=re.I)
    # Match was computed on lineage-stripped text; replace by content in original.
    if full not in text:
        raise RuntimeError(f"could not locate {field_id} block in original surface text")
    return text.replace(full, patched, 1)


def test_list_includes_e1_and_e2_gates() -> None:
    result = run_gates(["list", "--json"])
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["ok"] is True
    gates = set(data["gates"])
    assert "alias_coverage" in gates
    assert "hook_safety" in gates
    assert "prisma_fields" in gates
    assert "stats_fallacies_11" in gates
    assert "mode_registry_coverage" in gates
    assert "content_depth" in gates


def test_e1_gate_alias_coverage_passes() -> None:
    result = run_gates(["gate", "--id", "alias_coverage", "--json"])
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["ok"] is True


def test_mode_registry_coverage_passes_structured() -> None:
    result = run_gates(["gate", "--id", "mode_registry_coverage", "--json"])
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["ok"] is True
    detail = data["results"][0]["detail"]
    assert "mode_operation_rows=34" in detail
    assert "prefixed_aliases=68" in detail


def test_content_depth_passes_on_repo() -> None:
    result = run_gates(["gate", "--id", "content_depth", "--json"])
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["ok"] is True


def test_content_depth_negative_mutations() -> None:
    """Empty, heading-only, and too-short bodies must fail content_depth helper."""
    mod = load_gates_module()
    empty_ok, empty_reason = mod.evaluate_content_depth_text("", kind="contract")
    assert empty_ok is False
    assert "empty" in empty_reason

    heading_only = "# Title\n\n## One\n\n## Two\n\n## Three\n"
    ho_ok, ho_reason = mod.evaluate_content_depth_text(heading_only, kind="contract")
    assert ho_ok is False
    assert "heading-only" in ho_reason or "prose" in ho_reason or "short" in ho_reason

    too_short = "# Title\n\n## A\n\nx\n\n## B\n\ny\n\n## C\n\nz\n"
    ts_ok, ts_reason = mod.evaluate_content_depth_text(too_short, kind="contract")
    assert ts_ok is False
    assert ts_reason

    good = (
        "# Contract\n\n"
        "## Scope\n\n"
        "This contract defines executable obligations for agents with enough "
        "instructional detail to act without inventing the method or inventing "
        "missing evidence states when optional backends are unavailable.\n\n"
        "## Rules\n\n"
        "Agents must validate inputs, refuse unknown schemas, and record evidence "
        "states honestly when backends are missing. Passport resume requires a "
        "matching checkpoint hash before any stage transition is accepted.\n\n"
        "## Failures\n\n"
        "Empty stubs, heading-only sections, and silent full drafts are forbidden "
        "by this gate and must fail automated checks. Unsupported aliases must "
        "exit with code 2 rather than falling through to heuristic draft modes.\n"
    )
    good_ok, good_reason = mod.evaluate_content_depth_text(good, kind="contract")
    assert good_ok is True, good_reason


def test_e2_method_gates_pass() -> None:
    """E2 PRISMA/RoB/GRADE/effect/anti-pooling gates must pass on real bodies."""
    for gate_id in (
        "prisma_fields",
        "rob2_fields",
        "robins_i_fields",
        "grade_fields",
        "effect_hetero_sensitivity",
        "anti_pooling_fields",
    ):
        result = run_gates(["gate", "--id", gate_id, "--json"])
        assert result.returncode == 0, f"{gate_id}: {result.stdout}"
        data = json.loads(result.stdout)
        assert data["ok"] is True, gate_id


def test_e4_stats_fallacies_still_not_started() -> None:
    result = run_gates(["gate", "--id", "stats_fallacies_11", "--json"])
    assert result.returncode == 1
    data = json.loads(result.stdout)
    assert data["ok"] is False
    assert data["results"][0]["status"] == "not_started"
    assert "not_started" in data["results"][0]["detail"]


def test_e2_semantic_gate_mutations() -> None:
    """Damaged copies must fail the intended gate family independently."""
    mod = load_gates_module()
    base = (
        _read_surface("core/protocols/systematic_review.md")
        + "\n\n"
        + _read_surface("core/templates/prisma_protocol.md")
        + "\n\n"
        + _read_surface("core/templates/prisma_report_skeleton.md")
    )
    ok, _ = mod.evaluate_prisma_fields_text(base)
    assert ok is True

    # Index-only field IDs must not pass
    index_only = (
        "# Index\n\n"
        "`prisma_title_registration`, `eligibility_pico`, `information_sources`, "
        "`search_strategy`, `selection_process`, `data_items`, `risk_of_bias_plan`, "
        "`effect_measures`, `synthesis_methods`, `heterogeneity_plan`, "
        "`sensitivity_plan`, `anti_pooling`, `reporting_bias`, `certainty_grade`\n"
    )
    idx_ok, idx_detail = mod.evaluate_prisma_fields_text(index_only)
    assert idx_ok is False
    assert "missing" in idx_detail or "field failures" in idx_detail

    # Hollow one PRISMA protocol field across all copies
    hollow_prisma = _hollow_field(base, "prisma_title_registration", "x\n")
    p_ok, _ = mod.evaluate_prisma_fields_text(hollow_prisma)
    assert p_ok is False

    # Remove RoB signaling question from every rob2_d1 copy
    hollow_rob = _hollow_field(
        base,
        "rob2_d1",
        "Domain label randomization process only; judgment low some_concerns high no_information without any probe.\n",
    )
    r_ok, r_detail = mod.evaluate_rob2_fields_text(hollow_rob)
    assert r_ok is False
    assert "rob2_d1" in r_detail or "signaling" in r_detail

    # Remove one GRADE downgrade domain body everywhere
    hollow_grade = _hollow_field(base, "grade_imprecision", "short\n")
    g_ok, g_detail = mod.evaluate_grade_fields_text(hollow_grade)
    assert g_ok is False
    assert "grade_imprecision" in g_detail or "field failures" in g_detail

    # Leave only one sensitivity analysis
    one_sens = _hollow_field(
        base,
        "sensitivity_analyses",
        "1. Risk-of-bias restricted analysis — trigger: high RoB studies present.\n",
    )
    s_ok, s_detail = mod.evaluate_effect_hetero_sensitivity_text(one_sens)
    assert s_ok is False
    assert "sensitivity" in s_detail.lower() or "count" in s_detail.lower()

    # Fewer than three anti-pooling conditions
    few_cond = _hollow_field(
        base,
        "anti_pooling_conditions",
        "1. Only one vague condition about diversity without enough siblings.\n",
    )
    c_ok, c_detail = mod.evaluate_anti_pooling_fields_text(few_cond)
    assert c_ok is False
    assert "condition" in c_detail.lower() or "anti-pooling" in c_detail.lower()

    # Replace narrative action with silent pooling endorsement
    silent = _hollow_field(
        base,
        "anti_pooling_action",
        "When conditions trigger, continue with silent pooling of whatever numbers "
        "are handy and skip narrative synthesis entirely for speed.\n",
    )
    a_ok, a_detail = mod.evaluate_anti_pooling_fields_text(silent)
    assert a_ok is False
    assert (
        "narrative" in a_detail.lower()
        or "silent" in a_detail.lower()
        or "forbid" in a_detail.lower()
        or "swim" in a_detail.lower()
    )

    # ROBINS-I domain hollow
    hollow_robins = _hollow_field(
        base,
        "robins_d1",
        "Confounding placeholder without probe or judgment vocabulary.\n",
    )
    ri_ok, _ = mod.evaluate_robins_i_fields_text(hollow_robins)
    assert ri_ok is False


def test_e2_r1_file_specific_protocol_hollow() -> None:
    """E2-R1: hollow one PRISMA protocol surface; duplicates cannot rescue it."""
    mod = load_gates_module()
    sr = _read_surface("core/protocols/systematic_review.md")
    protocol = _read_surface("core/templates/prisma_protocol.md")
    report = _read_surface("core/templates/prisma_report_skeleton.md")

    ok, detail = mod.evaluate_prisma_fields_surfaces(
        systematic_review=sr,
        prisma_protocol=protocol,
        prisma_report=report,
    )
    assert ok is True, detail

    hollow_protocol = _hollow_field(protocol, "prisma_title_registration", "x\n")
    fail_ok, fail_detail = mod.evaluate_prisma_fields_surfaces(
        systematic_review=sr,
        prisma_protocol=hollow_protocol,
        prisma_report=report,
    )
    assert fail_ok is False
    assert "prisma_protocol" in fail_detail or "prisma_title_registration" in fail_detail
    assert "field failures" in fail_detail or "body" in fail_detail or "missing" in fail_detail


def test_e2_r1_file_specific_report_hollow() -> None:
    """E2-R1: hollow only prisma_report_skeleton while report fields remain elsewhere."""
    mod = load_gates_module()
    sr = _read_surface("core/protocols/systematic_review.md")
    protocol = _read_surface("core/templates/prisma_protocol.md")
    report = _read_surface("core/templates/prisma_report_skeleton.md")

    # Report fields still present in systematic_review.md (elsewhere).
    elsewhere_ok, _, _ = mod.evaluate_required_fields(sr, mod.PRISMA_REPORT_FIELDS)
    assert elsewhere_ok is True

    hollow_report = _hollow_field(report, "report_title_abstract", "x\n")
    fail_ok, fail_detail = mod.evaluate_prisma_fields_surfaces(
        systematic_review=sr,
        prisma_protocol=protocol,
        prisma_report=hollow_report,
    )
    assert fail_ok is False
    assert "prisma_report_skeleton" in fail_detail or "report_title_abstract" in fail_detail


def test_e2_r2_wrong_local_domain_labels() -> None:
    """E2-R2: wrong local RoB/ROBINS labels fail even when correct cues exist elsewhere."""
    mod = load_gates_module()
    surface = _read_surface("core/templates/prisma_protocol.md")

    # Correct cue remains elsewhere in the same surface (other domains / prose).
    assert "randomization" in surface.lower()
    assert "confounding" in surface.lower()

    rob_wrong = _replace_local_cue(surface, "rob2_d1", "randomization", "confounding")
    # Keep the correct RoB 2 cue elsewhere so global substring search would pass.
    rob_wrong = rob_wrong + "\n\nElsewhere residual cue: randomization process notes.\n"
    r_ok, r_detail = mod.evaluate_rob2_fields_text(rob_wrong)
    assert r_ok is False
    assert "rob2_d1" in r_detail
    assert "local domain label" in r_detail or "randomization" in r_detail

    robins_wrong = _replace_local_cue(
        surface, "robins_d1", "confounding", "randomization"
    )
    robins_wrong = (
        robins_wrong + "\n\nElsewhere residual cue: confounding control notes.\n"
    )
    ri_ok, ri_detail = mod.evaluate_robins_i_fields_text(robins_wrong)
    assert ri_ok is False
    assert "robins_d1" in ri_detail
    assert "local domain label" in ri_detail or "confounding" in ri_detail


def test_e2_r3_grade_fabrication_endorsement() -> None:
    """E2-R3: endorsement such as fabricate certainty freely must fail polarity."""
    mod = load_gates_module()
    surface = _read_surface("core/templates/prisma_protocol.md")
    damaged = _hollow_field(
        surface,
        "grade_certainty",
        "high | moderate | low | very low rationale; fabricate certainty freely "
        "when evidence is thin and human confirmation can wait.\n",
    )
    g_ok, g_detail = mod.evaluate_grade_fields_text(damaged)
    assert g_ok is False
    assert "fabricat" in g_detail.lower() or "polarity" in g_detail.lower()

    anti_ok, anti_detail = mod.evaluate_anti_fabrication_certainty(
        "high moderate low very low; fabricate certainty freely for speed."
    )
    assert anti_ok is False
    assert "polarity" in anti_detail.lower() or "endors" in anti_detail.lower()


def test_e2_r4_anti_pooling_optional_allowed() -> None:
    """E2-R4: SWiM optional + invented pooled numbers allowed must fail action."""
    mod = load_gates_module()
    filler = (
        " Continue the methods note with enough instructional prose so body length "
        "clears the minimum non-whitespace threshold for field evaluation."
    )
    body = "SWiM is optional; invented pooled numbers are allowed." + filler
    a_ok, a_detail = mod.evaluate_anti_pooling_action(body)
    assert a_ok is False
    assert (
        "optional" in a_detail.lower()
        or "polarity" in a_detail.lower()
        or "invent" in a_detail.lower()
        or "allowed" in a_detail.lower()
        or "narrative" in a_detail.lower()
        or "swim" in a_detail.lower()
    )

    surface = _read_surface("core/templates/prisma_protocol.md")
    damaged = _hollow_field(surface, "anti_pooling_action", body + "\n")
    f_ok, f_detail = mod.evaluate_anti_pooling_fields_text(damaged)
    assert f_ok is False
    assert "anti_pooling" in f_detail.lower() or "optional" in f_detail.lower() or "polarity" in f_detail.lower()


def test_e2_r5_hetero_exploration_missing_discipline() -> None:
    """E2-R5: subgroup/meta-regression without pre-spec/multiplicity cautions fails."""
    mod = load_gates_module()
    weak = (
        "Plan subgroup analyses and meta-regression for clinical modifiers without "
        "stating any protocol-level constraints beyond listing the keywords above."
    )
    e_ok, e_detail = mod.evaluate_hetero_exploration_body(weak)
    assert e_ok is False
    assert (
        "pre-spec" in e_detail.lower()
        or "multiplicit" in e_detail.lower()
        or "data-driven" in e_detail.lower()
        or "discipline" in e_detail.lower()
        or "caution" in e_detail.lower()
    )

    surface = _read_surface("core/templates/prisma_protocol.md")
    damaged = _hollow_field(surface, "hetero_exploration", weak + "\n")
    f_ok, f_detail = mod.evaluate_effect_hetero_sensitivity_text(damaged)
    assert f_ok is False
    assert (
        "hetero_exploration" in f_detail
        or "pre-spec" in f_detail.lower()
        or "multiplicit" in f_detail.lower()
        or "discipline" in f_detail.lower()
    )


def test_hook_safety_gate_passes() -> None:
    result = run_gates(["gate", "--id", "hook_safety", "--json"])
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["ok"] is True


def test_passport_reset_contract_behavioral() -> None:
    result = run_gates(["gate", "--id", "passport_reset_contract", "--json"])
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["ok"] is True
    detail = data["results"][0]["detail"]
    assert "illegal_transition" in detail or "behavioral" in detail
    assert "append-only" in detail


def test_reset_ledger_transition_positives_and_negatives() -> None:
    """Append-only ledger: one valid append ok; delete/reorder/mutate/multi fail."""
    planner_path = METHODS_ROOT / "runtime" / "scripts" / "essential_full_runtime.py"
    spec = importlib.util.spec_from_file_location("planner_reset_test", planner_path)
    assert spec is not None and spec.loader is not None
    planner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(planner)

    e1 = {
        "reset_id": "r1",
        "timestamp": "2026-07-20T00:00:00Z",
        "from_stage": "3",
        "to_stage": "1",
        "from_checkpoint_hash": "x",
        "reason": "first",
        "actor": "human",
        "env_flags_observed": ["RM_PASSPORT_RESET=1"],
    }
    e2 = {
        "reset_id": "r2",
        "timestamp": "2026-07-20T01:00:00Z",
        "from_stage": "4",
        "to_stage": "1",
        "from_checkpoint_hash": "y",
        "reason": "second",
        "actor": "agent",
        "env_flags_observed": ["RM_PASSPORT_RESET=1"],
    }
    prev: list = []
    new = [dict(e1)]
    ok = planner.validate_reset_ledger_transition(prev, new)
    assert ok["ok"] is True
    assert prev == []
    assert new == [e1]

    assert planner.validate_reset_ledger_transition([dict(e1)], [dict(e1), dict(e2)])["ok"] is True

    deleted = planner.validate_reset_ledger_transition([dict(e1), dict(e2)], [dict(e1)])
    assert deleted["ok"] is False
    assert deleted["error"] == "reset_ledger_delete"

    mutated = dict(e1)
    mutated["reason"] = "tampered"
    mut = planner.validate_reset_ledger_transition([dict(e1)], [mutated, dict(e2)])
    assert mut["ok"] is False
    assert mut["error"] == "reset_ledger_mutation"

    reordered = planner.validate_reset_ledger_transition(
        [dict(e1), dict(e2)],
        [dict(e2), dict(e1)],
    )
    assert reordered["ok"] is False

    multi = planner.validate_reset_ledger_transition([], [dict(e1), dict(e2)])
    assert multi["ok"] is False
    assert multi["error"] == "reset_ledger_multi_append"

    bad_actor = dict(e1)
    bad_actor["actor"] = "robot"
    actor = planner.validate_reset_ledger_transition([], [bad_actor])
    assert actor["ok"] is False
    assert actor["error"] == "invalid_reset_actor"

    missing = dict(e1)
    del missing["from_checkpoint_hash"]
    miss = planner.validate_reset_ledger_transition([], [missing])
    assert miss["ok"] is False
    assert miss["error"] == "invalid_reset_entry"


def test_file_lineage_includes_runtime_scripts() -> None:
    result = run_gates(["gate", "--id", "file_lineage_headers", "--json"])
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["ok"] is True
    assert "scripts" in data["results"][0]["detail"]


# ---------------------------------------------------------------------------
# E3-A citation integrity vertical slice
# ---------------------------------------------------------------------------

FROZEN_PUBLIC_GATE_IDS = (
    "alias_coverage",
    "anti_pooling_fields",
    "claim_verdict_vocab",
    "content_depth",
    "effect_hetero_sensitivity",
    "evidence_state_vocab",
    "file_lineage_headers",
    "generator_evaluator_separation",
    "grade_fields",
    "hook_safety",
    "mode_registry_coverage",
    "optional_runtime_honesty",
    "passport_reset_contract",
    "prisma_fields",
    "reviewer_independence",
    "rob2_fields",
    "robins_i_fields",
    "single_root_skill",
    "stats_fallacies_11",
    "upstream_provenance",
    "vague_topic_socratic",
)


def _base_citation_record(**overrides: Any) -> dict[str, Any]:
    """Build a coherent VERIFIED citation row; callers override failing fields."""
    record: dict[str, Any] = {
        "citation_id": "C-BASE",
        "identity": {
            "title": "Coherent Study of Survival Outcomes",
            "authors": "A Researcher",
            "year": "2021",
            "venue": "Example Journal",
            "doi_or_id": "10.1000/coherent",
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
    for key, value in overrides.items():
        if key == "identity" and isinstance(value, dict):
            merged = dict(record["identity"])
            merged.update(value)
            record["identity"] = merged
        else:
            record[key] = value
    return record


def test_e3_public_gate_id_snapshot_unchanged() -> None:
    """E3-R13: public gate ID set remains exactly the frozen 21 IDs."""
    mod = load_gates_module()
    assert sorted(mod.GATE_FUNCS.keys()) == sorted(FROZEN_PUBLIC_GATE_IDS)
    result = run_gates(["list", "--json"])
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert sorted(data["gates"]) == sorted(FROZEN_PUBLIC_GATE_IDS)
    assert len(data["gates"]) == 21
    return None


def test_e3a_doi_only_verified_fails() -> None:
    """E3-R1: DOI present + VERIFIED but locator/extract missing fails."""
    mod = load_gates_module()
    record = _base_citation_record(
        citation_id="C-DOI-ONLY",
        locator_or_quote="",
        extract="",
    )
    result = mod.evaluate_citation_record(record)
    assert result["ok"] is False
    assert result["error"] in {
        "doi_alone_insufficient",
        "verified_without_extract",
        "verified_missing_locator_or_extract",
    }
    assert "C-DOI-ONLY" in result["detail"]
    return None


def test_e3a_contradicted_claim_cannot_be_verified() -> None:
    """Wrong/contradicted claim support cannot pass VERIFIED."""
    mod = load_gates_module()
    contradicted = _base_citation_record(
        citation_id="C-CONTRA",
        support_status="contradicted",
        force_mismatch=True,
    )
    result = mod.evaluate_citation_record(contradicted)
    assert result["ok"] is False
    assert result["error"] in {
        "major_distortion_required",
        "verified_support_not_supported",
    }

    wrong_verdict = _base_citation_record(
        citation_id="C-MISMATCH",
        force_mismatch=True,
        support_status="supported",
    )
    result2 = mod.evaluate_citation_record(wrong_verdict)
    assert result2["ok"] is False
    assert result2["error"] == "major_distortion_required"
    return None


def test_e3a_risk_and_access_block_clean_verified() -> None:
    """Retracted/EOC/predatory/corrected/version/access-blocked clean VERIFIED fails."""
    mod = load_gates_module()

    retracted = _base_citation_record(
        citation_id="C-RETRACT",
        risk_flags=["retracted"],
    )
    r1 = mod.evaluate_citation_record(retracted)
    assert r1["ok"] is False
    assert r1["error"] == "retracted_marked_clean"

    eoc = _base_citation_record(
        citation_id="C-EOC",
        risk_flags=["expression_of_concern"],
    )
    r_eoc = mod.evaluate_citation_record(eoc)
    assert r_eoc["ok"] is False
    assert r_eoc["error"] == "expression_of_concern_clean"

    predatory = _base_citation_record(
        citation_id="C-PRED",
        risk_flags=["predatory"],
    )
    r_pred = mod.evaluate_citation_record(predatory)
    assert r_pred["ok"] is False
    assert r_pred["error"] == "predatory_unresolved"

    corrected = _base_citation_record(
        citation_id="C-CORRECT",
        risk_flags=["corrected"],
        identity={"correction_note": ""},
        notes="",
    )
    r2 = mod.evaluate_citation_record(corrected)
    assert r2["ok"] is False
    assert r2["error"] == "correction_ignored"

    version = _base_citation_record(
        citation_id="C-VERSION",
        risk_flags=["version_mismatch"],
    )
    r3 = mod.evaluate_citation_record(version)
    assert r3["ok"] is False
    assert r3["error"] == "version_mismatch_clean"

    blocked = _base_citation_record(
        citation_id="C-BLOCKED-VERIFIED",
        access_state="access_blocked",
    )
    r4 = mod.evaluate_citation_record(blocked)
    assert r4["ok"] is False
    assert r4["error"] == "verdict_access_incoherent"
    return None


def test_e3a_access_state_coherence_fails() -> None:
    """Missing/unverified access under VERIFIED and UVA/access pairing fail closed."""
    mod = load_gates_module()

    missing_access = _base_citation_record(
        citation_id="C-NO-ACCESS",
        access_state="",
    )
    r1 = mod.evaluate_citation_record(missing_access)
    assert r1["ok"] is False
    assert r1["error"] == "unknown_access_state"

    unverified = _base_citation_record(
        citation_id="C-UNVER-ACCESS",
        access_state="unverified",
    )
    r2 = mod.evaluate_citation_record(unverified)
    assert r2["ok"] is False
    assert r2["error"] == "verdict_access_incoherent"

    unknown_access = _base_citation_record(
        citation_id="C-BAD-ACCESS",
        access_state="maybe_open",
    )
    r3 = mod.evaluate_citation_record(unknown_access)
    assert r3["ok"] is False
    assert r3["error"] == "unknown_access_state"

    uva_verified_access = _base_citation_record(
        citation_id="C-UVA-VERIFIED-ACCESS",
        access_state="verified",
        locator_or_quote="",
        extract="",
        support_status="unknown",
        assessment_source="none",
        verdict="UNVERIFIABLE_ACCESS",
    )
    r4 = mod.evaluate_citation_record(uva_verified_access)
    assert r4["ok"] is False
    assert r4["error"] == "verdict_access_incoherent"

    unverifiable_blocked = _base_citation_record(
        citation_id="C-UNV-BLOCKED",
        access_state="access_blocked",
        locator_or_quote="",
        extract="",
        support_status="unknown",
        assessment_source="none",
        verdict="UNVERIFIABLE",
    )
    r5 = mod.evaluate_citation_record(unverifiable_blocked)
    assert r5["ok"] is False
    assert r5["error"] == "verdict_access_incoherent"
    return None


def test_e3a_empty_records_and_required_fields_fail() -> None:
    """Empty aggregate and missing citation_id/claim_text/unknown risk fail closed."""
    mod = load_gates_module()

    empty = mod.evaluate_citation_records([])
    assert empty["ok"] is False
    assert empty["error"] == "empty_records"

    no_id = _base_citation_record(citation_id="")
    r1 = mod.evaluate_citation_record(no_id)
    assert r1["ok"] is False
    assert r1["error"] == "missing_citation_id"

    no_claim = _base_citation_record(citation_id="C-NO-CLAIM", claim_text="")
    r2 = mod.evaluate_citation_record(no_claim)
    assert r2["ok"] is False
    assert r2["error"] == "missing_claim_text"

    unknown_risk = _base_citation_record(
        citation_id="C-BAD-RISK",
        risk_flags=["totally_made_up_risk"],
    )
    r3 = mod.evaluate_citation_record(unknown_risk)
    assert r3["ok"] is False
    assert r3["error"] == "unknown_risk_flag"

    unknown_support = _base_citation_record(
        citation_id="C-BAD-SUPPORT",
        support_status="kinda_ok",
        verdict="UNVERIFIABLE",
        access_state="unverified",
        locator_or_quote="",
        extract="",
        assessment_source="none",
    )
    r4 = mod.evaluate_citation_record(unknown_support)
    assert r4["ok"] is False
    assert r4["error"] == "unknown_support_status"
    return None


def test_e3a_unknown_verdict_and_missing_identity_fail() -> None:
    """Unknown verdict or missing identity fails."""
    mod = load_gates_module()
    unknown = _base_citation_record(citation_id="C-UNK", verdict="TOTALLY_FINE")
    r1 = mod.evaluate_citation_record(unknown)
    assert r1["ok"] is False
    assert r1["error"] == "unknown_verdict"

    missing = _base_citation_record(
        citation_id="C-NOID",
        identity={"title": "", "doi_or_id": "", "authors": "X", "year": "2020"},
    )
    r2 = mod.evaluate_citation_record(missing)
    assert r2["ok"] is False
    assert r2["error"] == "missing_identity"
    return None


def test_e3a_coherent_verified_and_honest_inaccessible_pass() -> None:
    """Coherent VERIFIED, corrected-with-note, and honest access failures pass."""
    mod = load_gates_module()
    good = _base_citation_record(citation_id="C-GOOD")
    r1 = mod.evaluate_citation_record(good)
    assert r1["ok"] is True, r1

    corrected_ok = _base_citation_record(
        citation_id="C-CORRECT-OK",
        risk_flags=["corrected"],
        identity={"correction_note": "Erratum 2022-03 acknowledged; claim uses VoR."},
    )
    r_corr = mod.evaluate_citation_record(corrected_ok)
    assert r_corr["ok"] is True, r_corr

    inaccessible = _base_citation_record(
        citation_id="C-ACCESS",
        locator_or_quote="",
        extract="",
        access_state="access_blocked",
        support_status="unknown",
        assessment_source="none",
        verdict="UNVERIFIABLE_ACCESS",
    )
    r2 = mod.evaluate_citation_record(inaccessible)
    assert r2["ok"] is True, r2

    unresolvable = _base_citation_record(
        citation_id="C-UNRESOLVABLE",
        locator_or_quote="",
        extract="",
        access_state="unresolvable",
        support_status="unknown",
        assessment_source="none",
        verdict="UNVERIFIABLE_ACCESS",
    )
    r3 = mod.evaluate_citation_record(unresolvable)
    assert r3["ok"] is True, r3

    agg = mod.evaluate_citation_records([good, corrected_ok, inaccessible, unresolvable])
    assert agg["ok"] is True, agg
    return None


def test_e3a_similarity_or_doi_never_promotes_verified() -> None:
    """DOI/token/similarity signals cannot promote without assessment_source."""
    mod = load_gates_module()
    heuristic = _base_citation_record(
        citation_id="C-HEURISTIC",
        assessment_source="heuristic_only",
        similarity_score=0.99,
    )
    result = mod.evaluate_citation_record(heuristic)
    assert result["ok"] is False
    assert result["error"] == "verified_missing_assessment_source"
    return None


def test_e3a_surface_isolation_hollow_protocol_audit_report() -> None:
    """Hollow only protocol, only audit, or only claim report each fails alone."""
    mod = load_gates_module()
    protocol = _read_surface("core/protocols/citation_integrity.md")
    audit = _read_surface("core/templates/citation_integrity_audit.md")
    report = _read_surface("core/templates/claim_verification_report.md")

    ok_p, detail_p = mod.evaluate_citation_integrity_protocol_text(protocol)
    assert ok_p is True, detail_p
    ok_a, detail_a = mod.evaluate_citation_audit_template_text(audit)
    assert ok_a is True, detail_a
    ok_r, detail_r = mod.evaluate_claim_report_template_text(report)
    assert ok_r is True, detail_r

    # Hollow only protocol; audit+report remain complete (duplicates elsewhere).
    hollow_protocol = _hollow_field(protocol, "locator_or_quote", "x\n")
    # Keep a keyword-complete but hollow duplicate elsewhere so global search would pass.
    hollow_protocol = hollow_protocol + (
        "\n\nElsewhere residual: locator_or_quote page section extract discipline.\n"
    )
    p_fail, p_detail = mod.evaluate_citation_integrity_protocol_text(hollow_protocol)
    assert p_fail is False
    assert "locator_or_quote" in p_detail
    # Peer surfaces still pass independently.
    assert mod.evaluate_citation_audit_template_text(audit)[0] is True
    assert mod.evaluate_claim_report_template_text(report)[0] is True

    hollow_audit = _hollow_field(audit, "claim_source_fidelity", "x\n")
    hollow_audit = hollow_audit + (
        "\n\nElsewhere residual: claim_source_fidelity VERIFIED support_status.\n"
    )
    a_fail, a_detail = mod.evaluate_citation_audit_template_text(hollow_audit)
    assert a_fail is False
    assert "claim_source_fidelity" in a_detail
    assert mod.evaluate_citation_integrity_protocol_text(protocol)[0] is True

    hollow_report = _hollow_field(report, "escalation", "x\n")
    hollow_report = hollow_report + (
        "\n\nElsewhere residual: escalation PASS PASS_WITH_NOTES FAIL criteria.\n"
    )
    r_fail, r_detail = mod.evaluate_claim_report_template_text(hollow_report)
    assert r_fail is False
    assert "escalation" in r_detail
    assert mod.evaluate_citation_audit_template_text(audit)[0] is True
    return None


def test_e3a_keyword_complete_hollow_bodies_fail() -> None:
    """Keyword-complete short/hollow bodies fail field and depth checks."""
    mod = load_gates_module()
    hollow = (
        "# Citation Integrity Protocol\n\n"
        "**parity: partial**\n\n"
        "### citation_identity\n\nx\n\n"
        "### locator_or_quote\n\nx\n\n"
        "### claim_source_fidelity\n\nx\n\n"
        "### temporal_version_check\n\nx\n\n"
        "### correction_retraction_predatory_risk\n\nx\n\n"
        "### contamination_signals\n\nx\n\n"
        "### plagiarism_boundary\n\nx\n\n"
        "### access_state\n\nx\n\n"
        "### integrity_mode\n\nx\n\n"
        "### escalation\n\nx\n\n"
        "Keywords only: VERIFIED MINOR_DISTORTION MAJOR_DISTORTION "
        "UNVERIFIABLE UNVERIFIABLE_ACCESS Mode1 Mode2 human_confirmed "
        "verified_adapter DOI locator extract retracted corrected.\n"
    )
    ok, detail = mod.evaluate_citation_integrity_protocol_text(hollow)
    assert ok is False
    assert "field failures" in detail or "body" in detail or "missing" in detail

    depth_ok, depth_detail = mod.evaluate_content_depth_text(hollow, kind="protocol")
    assert depth_ok is False
    assert depth_detail
    return None


def test_e3a_claim_verdict_vocab_gate_passes_with_behavior() -> None:
    """Public claim_verdict_vocab gate embeds behavioral fixtures and passes."""
    result = run_gates(["gate", "--id", "claim_verdict_vocab", "--json"])
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["ok"] is True
    detail = data["results"][0]["detail"]
    assert "citation" in detail.lower() or "behavioral" in detail.lower()
    return None


def test_e3a_content_depth_includes_citation_surfaces() -> None:
    """content_depth passes and includes E3-A citation designated surfaces."""
    result = run_gates(["gate", "--id", "content_depth", "--json"])
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["ok"] is True
    detail = data["results"][0]["detail"]
    assert "E3-A" in detail or "citation" in detail.lower()
    return None


def test_e3a_repository_surfaces_field_helpers_pass() -> None:
    """Designated repository surfaces each pass their isolated helper."""
    mod = load_gates_module()
    ok, detail = mod.evaluate_citation_integrity_protocol_text(
        _read_surface("core/protocols/citation_integrity.md")
    )
    assert ok is True, detail
    ok, detail = mod.evaluate_citation_audit_template_text(
        _read_surface("core/templates/citation_integrity_audit.md")
    )
    assert ok is True, detail
    ok, detail = mod.evaluate_claim_report_template_text(
        _read_surface("core/templates/claim_verification_report.md")
    )
    assert ok is True, detail
    return None


# ---------------------------------------------------------------------------
# E3-B paper modes, revision, rebuttal, disclosure
# ---------------------------------------------------------------------------


def _revision_base(**overrides: Any) -> dict[str, Any]:
    """Coherent positive revision payload; callers override failing fields."""
    payload: dict[str, Any] = {
        "before_text": (
            "Treatment may improve survival in subgroup A. "
            "Secondary endpoint X was exploratory."
        ),
        "after_text": (
            "Treatment may improve survival in subgroup A. "
            "Secondary endpoint X was pre-specified as exploratory."
        ),
        "protected_claims": [],
        "protected_hedges": ["Treatment may improve survival in subgroup A."],
        "change_ledger": [
            {
                "change_id": "c1",
                "op": "replace",
                "target": "Secondary endpoint X was exploratory.",
                "summary": "Secondary endpoint X was pre-specified as exploratory.",
            }
        ],
        "new_evidence_rows": [],
        "author_signoff": True,
        "recovery_required": False,
        "recovery_checkpoint": "ckpt-ok",
    }
    payload.update(overrides)
    return payload


def _rebuttal_base(**overrides: Any) -> dict[str, Any]:
    """Coherent positive rebuttal payload."""
    payload: dict[str, Any] = {
        "reviewer_points": [
            {"point_id": "R1", "text": "Clarify sample size."},
            {"point_id": "R2", "text": "Discuss limitation L."},
        ],
        "rebuttal_rows": [
            {
                "point_id": "R1",
                "coverage": "covered",
                "response_kind": "ms_change",
                "pointer": "§Methods sample size",
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
    payload.update(overrides)
    return payload


def test_e3b_all_paper_modes_pass_on_repository() -> None:
    """Repository academic_paper.md validates all 11 modes independently."""
    mod = load_gates_module()
    text = _read_surface("core/protocols/academic_paper.md")
    ok, detail = mod.evaluate_all_paper_modes_text(text)
    assert ok is True, detail
    assert "11" in detail or "modes ok" in detail
    return None


def test_e3b_one_paper_mode_hollow_parametric() -> None:
    """E3-R10: hollow exactly one mode; other 10 complete; detail names slug."""
    mod = load_gates_module()
    base = _read_surface("core/protocols/academic_paper.md")
    # Distinctive field per mode for hollow mutation.
    hollow_field_by_mode = {
        "full": "full_no_invented_results",
        "plan": "plan_chapter_negotiation",
        "outline_only": "outline_evidence_map",
        "revision": "revision_protected_claims",
        "revision_coach": "revision_coach_roadmap_only",
        "abstract_only": "abstract_protected_hedges",
        "lit_review": "lit_review_e2_handoff",
        "format_convert": "format_convert_runtime_honesty",
        "citation_check": "citation_check_bind_integrity",
        "disclosure": "disclosure_human_confirmation",
        "rebuttal_audit": "rebuttal_evaluator_only",
    }
    assert set(hollow_field_by_mode) == set(mod.PAPER_MODES)
    for mode_slug, field_id in hollow_field_by_mode.items():
        mutated = _hollow_field(base, field_id, "x\n")
        # Duplicate generic wording elsewhere must not rescue the hollow mode.
        mutated = mutated + (
            f"\n\nElsewhere residual: {field_id} mode_inputs mode_outputs "
            "stop_conditions offline_fallback human_gates complete wording.\n"
        )
        ok, detail = mod.evaluate_all_paper_modes_text(mutated)
        assert ok is False, f"{mode_slug} should fail when {field_id} hollow"
        assert mode_slug in detail, detail
        assert field_id in detail or "body" in detail or "missing" in detail
    return None


def test_e3b_revision_transition_positives_and_negatives() -> None:
    """Revision ledger truth: replace/delete/add/move/annotate + unique change_id."""
    mod = load_gates_module()

    good = mod.evaluate_revision_transition(_revision_base())
    assert good["ok"] is True, good

    deleted = mod.evaluate_revision_transition(
        _revision_base(
            after_text="Secondary endpoint X was pre-specified as exploratory.",
            change_ledger=[],
        )
    )
    assert deleted["ok"] is False
    assert deleted["error"] in {
        "protected_claim_deleted",
        "protected_claim_strengthened",
    }

    strengthened = mod.evaluate_revision_transition(
        _revision_base(
            after_text=(
                "Treatment does improve survival in subgroup A. "
                "Secondary endpoint X was pre-specified as exploratory."
            ),
            change_ledger=[],
        )
    )
    assert strengthened["ok"] is False
    assert strengthened["error"] in {
        "protected_claim_deleted",
        "protected_claim_strengthened",
    }

    silent_doi = mod.evaluate_revision_transition(
        _revision_base(
            after_text=(
                "Treatment may improve survival in subgroup A. "
                "Secondary endpoint X was pre-specified as exploratory. "
                "See also 10.1000/silent.new.result."
            ),
            new_evidence_rows=[],
        )
    )
    assert silent_doi["ok"] is False
    assert silent_doi["error"] == "silent_new_evidence"

    gated_doi = mod.evaluate_revision_transition(
        _revision_base(
            after_text=(
                "Treatment may improve survival in subgroup A. "
                "Secondary endpoint X was pre-specified as exploratory. "
                "See also 10.1000/gated.result."
            ),
            new_evidence_rows=[
                {
                    "citation_id": "10.1000/gated.result",
                    "claim": "supporting citation added",
                    "evidence_state": "extract",
                    "human_gate": True,
                }
            ],
            author_signoff=True,
        )
    )
    assert gated_doi["ok"] is True, gated_doi

    false_ledger = mod.evaluate_revision_transition(
        _revision_base(
            after_text=(
                "Treatment may improve survival in subgroup A. "
                "Secondary endpoint X was exploratory."
            ),
            change_ledger=[
                {
                    "change_id": "c-false",
                    "op": "replace",
                    "target": "Secondary endpoint X was exploratory.",
                    "summary": "Secondary endpoint X was rewritten completely.",
                }
            ],
        )
    )
    assert false_ledger["ok"] is False
    assert false_ledger["error"] == "false_ledger_claim"

    # Replace: target gone after, but claimed new summary also absent → fail.
    replace_summary_absent = mod.evaluate_revision_transition(
        _revision_base(
            after_text=(
                "Treatment may improve survival in subgroup A. "
                "Secondary endpoint X remains under review."
            ),
            change_ledger=[
                {
                    "change_id": "c-absent-summary",
                    "op": "replace",
                    "target": "Secondary endpoint X was exploratory.",
                    "summary": "Secondary endpoint X was pre-specified as exploratory.",
                }
            ],
        )
    )
    assert replace_summary_absent["ok"] is False
    assert replace_summary_absent["error"] == "false_ledger_claim"

    invalid_op = mod.evaluate_revision_transition(
        _revision_base(
            change_ledger=[
                {
                    "change_id": "c-bad-op",
                    "op": "rewrite",
                    "target": "Secondary endpoint X was exploratory.",
                    "summary": "Secondary endpoint X was pre-specified as exploratory.",
                }
            ],
        )
    )
    assert invalid_op["ok"] is False
    assert invalid_op["error"] == "invalid_ledger_op"

    delete_truth = mod.evaluate_revision_transition(
        _revision_base(
            after_text="Treatment may improve survival in subgroup A.",
            change_ledger=[
                {
                    "change_id": "c-del",
                    "op": "delete",
                    "target": "Secondary endpoint X was exploratory.",
                    "summary": "",
                }
            ],
        )
    )
    assert delete_truth["ok"] is True, delete_truth

    delete_still_present = mod.evaluate_revision_transition(
        _revision_base(
            after_text=(
                "Treatment may improve survival in subgroup A. "
                "Secondary endpoint X was exploratory."
            ),
            change_ledger=[
                {
                    "change_id": "c-del-false",
                    "op": "delete",
                    "target": "Secondary endpoint X was exploratory.",
                    "summary": "",
                }
            ],
        )
    )
    assert delete_still_present["ok"] is False
    assert delete_still_present["error"] == "false_ledger_claim"

    add_missing = mod.evaluate_revision_transition(
        _revision_base(
            change_ledger=[
                {
                    "change_id": "c-add-false",
                    "op": "add",
                    "target": "",
                    "summary": "This sentence never appears after.",
                }
            ],
        )
    )
    assert add_missing["ok"] is False
    assert add_missing["error"] == "false_ledger_claim"

    # Add: summary already present unchanged in before and after → fail.
    add_already = mod.evaluate_revision_transition(
        _revision_base(
            before_text=(
                "Treatment may improve survival in subgroup A. "
                "Secondary endpoint X was exploratory."
            ),
            after_text=(
                "Treatment may improve survival in subgroup A. "
                "Secondary endpoint X was exploratory."
            ),
            change_ledger=[
                {
                    "change_id": "c-add-already",
                    "op": "add",
                    "target": "",
                    "summary": "Secondary endpoint X was exploratory.",
                }
            ],
        )
    )
    assert add_already["ok"] is False
    assert add_already["error"] == "false_ledger_claim"

    # Add positive: summary absent before, present after.
    add_ok = mod.evaluate_revision_transition(
        _revision_base(
            before_text="Treatment may improve survival in subgroup A.",
            after_text=(
                "Treatment may improve survival in subgroup A. "
                "We added a pre-specified sensitivity analysis."
            ),
            protected_hedges=[],
            change_ledger=[
                {
                    "change_id": "c-add-ok",
                    "op": "add",
                    "target": "",
                    "summary": "We added a pre-specified sensitivity analysis.",
                }
            ],
        )
    )
    assert add_ok["ok"] is True, add_ok

    # Move: target never existed before; only unrelated summary after → fail.
    move_absent = mod.evaluate_revision_transition(
        _revision_base(
            before_text="Only before content here.",
            after_text="Only before content here. Unrelated summary appears.",
            protected_hedges=[],
            change_ledger=[
                {
                    "change_id": "c-move-false",
                    "op": "move",
                    "target": "Nonexistent target span.",
                    "summary": "Unrelated summary appears.",
                }
            ],
        )
    )
    assert move_absent["ok"] is False
    assert move_absent["error"] == "false_ledger_claim"

    # Move: target present both sides but first position unchanged → fail closed.
    move_static = mod.evaluate_revision_transition(
        _revision_base(
            before_text="Intro. MOVED_CLAIM_SPAN is here. Outro.",
            after_text="Intro. MOVED_CLAIM_SPAN is here. Outro.",
            protected_hedges=[],
            change_ledger=[
                {
                    "change_id": "c-move-static",
                    "op": "move",
                    "target": "MOVED_CLAIM_SPAN is here.",
                    "summary": "claimed move",
                }
            ],
        )
    )
    assert move_static["ok"] is False
    assert move_static["error"] == "false_ledger_claim"

    # Move positive: non-empty target present before/after; first position differs.
    move_ok = mod.evaluate_revision_transition(
        _revision_base(
            before_text="Intro. MOVED_CLAIM_SPAN is here. Outro.",
            after_text="Intro. Outro. MOVED_CLAIM_SPAN is here.",
            protected_hedges=[],
            change_ledger=[
                {
                    "change_id": "c-move-ok",
                    "op": "move",
                    "target": "MOVED_CLAIM_SPAN is here.",
                    "summary": "Relocated after outro.",
                }
            ],
        )
    )
    assert move_ok["ok"] is True, move_ok

    # Annotate: target exists in neither before nor after → fail.
    annotate_ghost = mod.evaluate_revision_transition(
        _revision_base(
            before_text="Only before content here.",
            after_text="Only after content here.",
            protected_hedges=[],
            change_ledger=[
                {
                    "change_id": "c-ann-false",
                    "op": "annotate",
                    "target": "Ghost target never present.",
                    "summary": "note",
                }
            ],
        )
    )
    assert annotate_ghost["ok"] is False
    assert annotate_ghost["error"] == "false_ledger_claim"

    # Annotate positive: non-empty target present in before or after.
    annotate_ok = mod.evaluate_revision_transition(
        _revision_base(
            before_text=(
                "Treatment may improve survival in subgroup A. "
                "Secondary endpoint X was exploratory."
            ),
            after_text=(
                "Treatment may improve survival in subgroup A. "
                "Secondary endpoint X was exploratory."
            ),
            change_ledger=[
                {
                    "change_id": "c-ann-ok",
                    "op": "annotate",
                    "target": "Secondary endpoint X was exploratory.",
                    "summary": "Editor note retained.",
                }
            ],
        )
    )
    assert annotate_ok["ok"] is True, annotate_ok

    # Unique non-empty change_id required.
    missing_id = mod.evaluate_revision_transition(
        _revision_base(
            change_ledger=[
                {
                    "change_id": "",
                    "op": "replace",
                    "target": "Secondary endpoint X was exploratory.",
                    "summary": "Secondary endpoint X was pre-specified as exploratory.",
                }
            ],
        )
    )
    assert missing_id["ok"] is False
    assert missing_id["error"] == "missing_change_id"

    dup_id = mod.evaluate_revision_transition(
        _revision_base(
            before_text="Alpha sentence. Beta sentence.",
            after_text="Alpha sentence. Beta sentence. Gamma sentence.",
            protected_hedges=[],
            change_ledger=[
                {
                    "change_id": "same-id",
                    "op": "add",
                    "target": "",
                    "summary": "Gamma sentence.",
                },
                {
                    "change_id": "same-id",
                    "op": "annotate",
                    "target": "Alpha sentence.",
                    "summary": "note",
                },
            ],
        )
    )
    assert dup_id["ok"] is False
    assert dup_id["error"] == "duplicate_change_id"

    no_signoff = mod.evaluate_revision_transition(
        _revision_base(
            author_signoff=False,
            new_evidence_rows=[
                {
                    "citation_id": "10.1000/x",
                    "claim": "x",
                    "evidence_state": "extract",
                    "human_gate": True,
                }
            ],
            after_text=(
                "Treatment may improve survival in subgroup A. "
                "Secondary endpoint X was pre-specified as exploratory. "
                "Cite 10.1000/x."
            ),
        )
    )
    assert no_signoff["ok"] is False
    assert no_signoff["error"] == "missing_author_signoff"

    no_recovery = mod.evaluate_revision_transition(
        _revision_base(
            recovery_required=True,
            recovery_checkpoint="",
        )
    )
    assert no_recovery["ok"] is False
    assert no_recovery["error"] == "recovery_checkpoint_missing"
    return None


def test_e3b_rebuttal_consistency_positives_and_negatives() -> None:
    """Rebuttal omits/duplicates/orphans, blank fields, missing coverage, payloads."""
    mod = load_gates_module()

    good = mod.evaluate_rebuttal_consistency(_rebuttal_base())
    assert good["ok"] is True, good

    empty_set = mod.evaluate_rebuttal_consistency(
        {
            "reviewer_points": [],
            "rebuttal_rows": [],
            "change_ledger": [],
            "evidence_pointers": [],
        }
    )
    assert empty_set["ok"] is False
    assert empty_set["error"] == "empty_reviewer_points"

    omit = mod.evaluate_rebuttal_consistency(
        _rebuttal_base(
            rebuttal_rows=[
                {
                    "point_id": "R1",
                    "coverage": "covered",
                    "response_kind": "evidence",
                    "pointer": "Table 2",
                }
            ]
        )
    )
    assert omit["ok"] is False
    assert omit["error"] == "missing_point_row"

    dup = mod.evaluate_rebuttal_consistency(
        _rebuttal_base(
            rebuttal_rows=[
                {
                    "point_id": "R1",
                    "coverage": "covered",
                    "response_kind": "ms_change",
                    "pointer": "§Methods",
                },
                {
                    "point_id": "R1",
                    "coverage": "partial",
                    "response_kind": "evidence",
                    "pointer": "Fig 1",
                },
                {
                    "point_id": "R2",
                    "coverage": "covered",
                    "response_kind": "no_change_rationale",
                    "pointer": "out of scope",
                },
            ]
        )
    )
    assert dup["ok"] is False
    assert dup["error"] == "duplicate_point_row"

    orphan = mod.evaluate_rebuttal_consistency(
        _rebuttal_base(
            rebuttal_rows=[
                {
                    "point_id": "R1",
                    "coverage": "covered",
                    "response_kind": "ms_change",
                    "pointer": "§Methods",
                },
                {
                    "point_id": "R2",
                    "coverage": "covered",
                    "response_kind": "no_change_rationale",
                    "pointer": "out of scope",
                },
                {
                    "point_id": "ORPHAN",
                    "coverage": "covered",
                    "response_kind": "evidence",
                    "pointer": "Table X",
                },
            ]
        )
    )
    assert orphan["ok"] is False
    assert orphan["error"] == "orphan_point_row"

    blank_fields = mod.evaluate_rebuttal_consistency(
        _rebuttal_base(
            rebuttal_rows=[
                {
                    "point_id": "R1",
                    "coverage": "",
                    "response_kind": "",
                    "pointer": "",
                },
                {
                    "point_id": "R2",
                    "coverage": "covered",
                    "response_kind": "no_change_rationale",
                    "pointer": "out of scope",
                },
            ],
            change_ledger=[],
        )
    )
    assert blank_fields["ok"] is False
    assert blank_fields["error"] in {"invalid_coverage", "invalid_response_kind"}

    coverage_missing = mod.evaluate_rebuttal_consistency(
        _rebuttal_base(
            rebuttal_rows=[
                {
                    "point_id": "R1",
                    "coverage": "missing",
                    "response_kind": "evidence",
                    "pointer": "Table 2",
                },
                {
                    "point_id": "R2",
                    "coverage": "covered",
                    "response_kind": "no_change_rationale",
                    "pointer": "out of scope",
                },
            ],
            change_ledger=[],
            audit_marked_clean=False,
        )
    )
    assert coverage_missing["ok"] is False
    assert coverage_missing["error"] == "coverage_missing_unclear"

    partial_no_gap = mod.evaluate_rebuttal_consistency(
        _rebuttal_base(
            rebuttal_rows=[
                {
                    "point_id": "R1",
                    "coverage": "partial",
                    "response_kind": "evidence",
                    "pointer": "",
                },
                {
                    "point_id": "R2",
                    "coverage": "covered",
                    "response_kind": "no_change_rationale",
                    "pointer": "out of scope",
                },
            ],
            change_ledger=[],
            evidence_pointers=[],
        )
    )
    assert partial_no_gap["ok"] is False
    assert partial_no_gap["error"] == "partial_without_gap_note"

    empty_point_text = mod.evaluate_rebuttal_consistency(
        _rebuttal_base(
            reviewer_points=[
                {"point_id": "R1", "text": ""},
                {"point_id": "R2", "text": "Discuss limitation L."},
            ]
        )
    )
    assert empty_point_text["ok"] is False
    assert empty_point_text["error"] == "empty_point_text"

    absent_change = mod.evaluate_rebuttal_consistency(
        _rebuttal_base(
            change_ledger=[],
        )
    )
    assert absent_change["ok"] is False
    assert absent_change["error"] == "asserted_change_absent"

    empty_rationale = mod.evaluate_rebuttal_consistency(
        _rebuttal_base(
            rebuttal_rows=[
                {
                    "point_id": "R1",
                    "coverage": "covered",
                    "response_kind": "ms_change",
                    "pointer": "§Methods",
                },
                {
                    "point_id": "R2",
                    "coverage": "covered",
                    "response_kind": "no_change_rationale",
                    "pointer": "",
                },
            ]
        )
    )
    assert empty_rationale["ok"] is False
    assert empty_rationale["error"] == "empty_no_change_rationale"

    empty_evidence = mod.evaluate_rebuttal_consistency(
        _rebuttal_base(
            rebuttal_rows=[
                {
                    "point_id": "R1",
                    "coverage": "covered",
                    "response_kind": "evidence",
                    "pointer": "",
                },
                {
                    "point_id": "R2",
                    "coverage": "covered",
                    "response_kind": "no_change_rationale",
                    "pointer": "out of scope",
                },
            ],
            change_ledger=[],
            evidence_pointers=[],
        )
    )
    assert empty_evidence["ok"] is False
    assert empty_evidence["error"] == "evidence_pointer_missing"

    prose = mod.evaluate_rebuttal_consistency(
        _rebuttal_base(generated_response_prose="Dear editor, we thank the reviewers...")
    )
    assert prose["ok"] is False
    assert prose["error"] == "evaluator_only_violation"
    return None


def _disclosure_base(**overrides: Any) -> dict[str, Any]:
    """Coherent positive final disclosure record; callers override failing fields."""
    payload: dict[str, Any] = {
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
    payload.update(overrides)
    return payload


def test_e3b_disclosure_record_positives_and_negatives() -> None:
    """Disclosure record: none_confirmed, final/draft, auto-fill, mandatory fields."""
    mod = load_gates_module()

    good = mod.evaluate_disclosure_record(_disclosure_base())
    assert good["ok"] is True, good

    draft_pending = mod.evaluate_disclosure_record(
        _disclosure_base(
            package_state="draft",
            funding={"status": "unknown_pending_human", "details": ""},
            conflicts={"status": "unknown_pending_human", "details": ""},
            ai_assistance={"status": "unknown_pending_human", "details": ""},
            human_confirmation=False,
            signer="",
            timestamp="",
        )
    )
    assert draft_pending["ok"] is True, draft_pending

    final_pending = mod.evaluate_disclosure_record(
        _disclosure_base(
            funding={"status": "unknown_pending_human", "details": ""},
        )
    )
    assert final_pending["ok"] is False
    assert final_pending["error"] == "unknown_pending_blocks_final"

    none_without_human = mod.evaluate_disclosure_record(
        _disclosure_base(
            human_confirmation=False,
            signer="",
            package_state="draft",
            funding={"status": "none_confirmed", "details": ""},
        )
    )
    assert none_without_human["ok"] is False
    assert none_without_human["error"] == "none_confirmed_requires_human"

    funded_no_details = mod.evaluate_disclosure_record(
        _disclosure_base(
            funding={"status": "funded", "details": ""},
        )
    )
    assert funded_no_details["ok"] is False
    assert funded_no_details["error"] == "missing_funding_details"

    interests_no_details = mod.evaluate_disclosure_record(
        _disclosure_base(
            conflicts={"status": "interests_present", "details": ""},
        )
    )
    assert interests_no_details["ok"] is False
    assert interests_no_details["error"] == "missing_coi_details"

    ai_no_details = mod.evaluate_disclosure_record(
        _disclosure_base(
            ai_assistance={"status": "disclosed", "details": ""},
        )
    )
    assert ai_no_details["ok"] is False
    assert ai_no_details["error"] == "missing_ai_details"

    auto_filled = mod.evaluate_disclosure_record(
        _disclosure_base(auto_filled=True)
    )
    assert auto_filled["ok"] is False
    assert auto_filled["error"] == "auto_filled_forbidden"

    self_confirmed = mod.evaluate_disclosure_record(
        _disclosure_base(self_confirmed=True)
    )
    assert self_confirmed["ok"] is False
    assert self_confirmed["error"] == "self_confirmed_forbidden"

    missing_data = mod.evaluate_disclosure_record(
        _disclosure_base(
            data_code_availability={"status": "", "details": "x"},
        )
    )
    assert missing_data["ok"] is False
    assert missing_data["error"] == "invalid_data_code_status"

    missing_policy = mod.evaluate_disclosure_record(
        _disclosure_base(
            policy_anchor_or_venue={"status": "", "details": ""},
        )
    )
    assert missing_policy["ok"] is False
    assert missing_policy["error"] == "invalid_policy_status"

    final_no_signer = mod.evaluate_disclosure_record(
        _disclosure_base(
            signer="",
            funding={"status": "funded", "details": "NIH R01-EX"},
            conflicts={
                "status": "interests_present",
                "details": "Consulting for Co Y",
            },
            ai_assistance={
                "status": "disclosed",
                "details": "Grammar assist only",
            },
        )
    )
    assert final_no_signer["ok"] is False
    assert final_no_signer["error"] == "missing_signer"

    return None


def test_e3b_disclosure_polarity_and_template_isolation() -> None:
    """Disclosure optionalizes/auto-fabricates or lacks human confirmation fails."""
    mod = load_gates_module()
    good = _read_surface("core/templates/disclosure_statement.md")
    ok, detail = mod.evaluate_disclosure_template_text(good)
    assert ok is True, detail

    optionalized = good + (
        "\n\nNote: AI assistance disclosure is optional for short papers.\n"
    )
    ok_opt, detail_opt = mod.evaluate_disclosure_template_text(optionalized)
    assert ok_opt is False
    assert "polarity" in detail_opt or "optional" in detail_opt.lower()

    autofab = (
        "# Disclosure\n\n"
        "### credit_authorship\n\n"
        "Record CRediT roles for each author with honest missing markers for gaps.\n\n"
        "### funding\n\n"
        "Funding may be auto-fabricated when authors forget to provide grant ids.\n\n"
        "### conflicts\n\n"
        "Conflicts of interest statements are mandatory and human-confirmed always.\n\n"
        "### data_code_availability\n\n"
        "Data and code availability must list access paths or honest restrictions.\n\n"
        "### ai_assistance\n\n"
        "AI assistance disclosure is mandatory and never optional for this template.\n\n"
        "### policy_anchor_or_venue\n\n"
        "Venue policy unknown must be recorded as uncertainty without inventing rules.\n\n"
        "### human_confirmation\n\n"
        "Human confirmation is mandatory before finalizing any disclosure package.\n"
    )
    ok_fab, detail_fab = mod.evaluate_disclosure_template_text(autofab)
    assert ok_fab is False

    hollow = _hollow_field(good, "human_confirmation", "x\n")
    hollow = hollow + "\nElsewhere residual: human_confirmation mandatory signer.\n"
    ok_h, detail_h = mod.evaluate_disclosure_template_text(hollow)
    assert ok_h is False
    assert "human_confirmation" in detail_h
    return None


def test_e3b_designated_templates_hollow_while_protocol_complete() -> None:
    """Hollow revision/rebuttal/disclosure templates fail even if protocol complete."""
    mod = load_gates_module()
    protocol = _read_surface("core/protocols/academic_paper.md")
    assert mod.evaluate_all_paper_modes_text(protocol)[0] is True

    revision = _read_surface("core/templates/revision_roadmap.md")
    rebuttal = _read_surface("core/templates/rebuttal_audit.md")
    disclosure = _read_surface("core/templates/disclosure_statement.md")

    assert mod.evaluate_revision_template_text(revision)[0] is True
    assert mod.evaluate_rebuttal_template_text(rebuttal)[0] is True
    assert mod.evaluate_disclosure_template_text(disclosure)[0] is True

    hollow_rev = _hollow_field(revision, "commitment_ledger", "x\n")
    hollow_rev = hollow_rev + (
        "\nElsewhere residual: commitment_ledger concern_id fulfillment_status.\n"
    )
    # Protocol remains complete; designated template must still fail.
    assert mod.evaluate_all_paper_modes_text(protocol)[0] is True
    r_ok, r_detail = mod.evaluate_revision_template_text(hollow_rev)
    assert r_ok is False
    assert "commitment_ledger" in r_detail

    hollow_reb = _hollow_field(rebuttal, "point_coverage_matrix", "x\n")
    hollow_reb = hollow_reb + (
        "\nElsewhere residual: point_coverage_matrix covered partial missing.\n"
    )
    b_ok, b_detail = mod.evaluate_rebuttal_template_text(hollow_reb)
    assert b_ok is False
    assert "point_coverage_matrix" in b_detail

    hollow_dis = _hollow_field(disclosure, "ai_assistance", "x\n")
    hollow_dis = hollow_dis + (
        "\nElsewhere residual: ai_assistance mandatory disclosure human.\n"
    )
    d_ok, d_detail = mod.evaluate_disclosure_template_text(hollow_dis)
    assert d_ok is False
    assert "ai_assistance" in d_detail
    return None


def test_e3b_public_gates_content_depth_and_generator_evaluator() -> None:
    """Public content_depth and generator_evaluator_separation pass with E3-B."""
    depth = run_gates(["gate", "--id", "content_depth", "--json"])
    assert depth.returncode == 0, depth.stdout
    depth_data = json.loads(depth.stdout)
    assert depth_data["ok"] is True
    depth_detail = depth_data["results"][0]["detail"]
    assert "E3-B" in depth_detail or "paper" in depth_detail.lower()

    gen = run_gates(["gate", "--id", "generator_evaluator_separation", "--json"])
    assert gen.returncode == 0, gen.stdout
    gen_data = json.loads(gen.stdout)
    assert gen_data["ok"] is True
    gen_detail = gen_data["results"][0]["detail"]
    assert (
        "revision" in gen_detail.lower()
        or "rebuttal" in gen_detail.lower()
        or "disclosure" in gen_detail.lower()
    )
    return None


def test_e3b_repository_template_helpers_pass() -> None:
    """Designated E3-B repository templates each pass isolated helpers."""
    mod = load_gates_module()
    ok, detail = mod.evaluate_revision_template_text(
        _read_surface("core/templates/revision_roadmap.md")
    )
    assert ok is True, detail
    ok, detail = mod.evaluate_rebuttal_template_text(
        _read_surface("core/templates/rebuttal_audit.md")
    )
    assert ok is True, detail
    ok, detail = mod.evaluate_disclosure_template_text(
        _read_surface("core/templates/disclosure_statement.md")
    )
    assert ok is True, detail
    return None


def _rereview_base(**overrides: Any) -> dict[str, Any]:
    """Minimal coherent re-review payload for E3-C helpers."""
    payload: dict[str, Any] = {
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
    payload.update(overrides)
    return payload


def _calibration_base(**overrides: Any) -> dict[str, Any]:
    """Minimal coherent calibration payload for E3-C helpers (5-row gold set)."""
    gold_labels = [
        {"item_id": f"C{i}", "label": "major" if i % 2 else "minor"}
        for i in range(1, 6)
    ]
    payload: dict[str, Any] = {
        "gold_labels": gold_labels,
        "predictions": [dict(row) for row in gold_labels],
        "session_only": True,
        "fabricated_labels": False,
        "persistent_calibration_claim": False,
    }
    payload.update(overrides)
    return payload


def test_e3c_all_reviewer_modes_pass_on_repository() -> None:
    """Repository manuscript_review.md validates all six modes independently."""
    mod = load_gates_module()
    text = _read_surface("core/protocols/manuscript_review.md")
    ok, detail = mod.evaluate_all_reviewer_modes_text(text)
    assert ok is True, detail
    assert "6" in detail or "modes ok" in detail
    return None


def test_e3c_one_reviewer_mode_hollow_parametric() -> None:
    """Hollow exactly one of six modes while peers stay complete."""
    mod = load_gates_module()
    base = _read_surface("core/protocols/manuscript_review.md")
    hollow_field_by_mode = {
        "full": "full_synthesis_barrier",
        "re_review": "re_review_no_blanket_all_fixed",
        "quick": "quick_no_full_panel_claim",
        "methodology_focus": "methodology_focus_mandatory_methods",
        "guided": "guided_dialogue_checkpoints",
        "calibration": "calibration_gold_required",
    }
    assert set(hollow_field_by_mode) == set(mod.REVIEWER_MODES)
    rescue_body = (
        "This later labeled body intentionally restates mode_inputs, mode_outputs, "
        "stop_conditions, offline_fallback, and human_gates with enough non-ws "
        "instructional text that only first-occurrence isolation can reject it.\n"
    )
    for mode_slug, field_id in hollow_field_by_mode.items():
        mutated = _hollow_field(base, field_id, "x\n")
        # Peer complete wording elsewhere + a later complete labeled field must
        # not rescue the hollow first occurrence for this mode.
        mutated = mutated + (
            f"\n\nElsewhere residual: {field_id} mode_inputs mode_outputs "
            "stop_conditions offline_fallback human_gates complete wording.\n"
            f"\n### {field_id}\n\n{rescue_body}"
        )
        ok, detail = mod.evaluate_all_reviewer_modes_text(mutated)
        assert ok is False, f"{mode_slug} should fail when {field_id} hollow"
        assert mode_slug in detail, detail
        assert field_id in detail or "body" in detail or "missing" in detail
    return None


def test_e3c_stage_synthesis_visibility_minority_negatives() -> None:
    """Synthesis before four reports; peer visibility; minority erased."""
    mod = load_gates_module()
    ids = list(mod.INDEPENDENT_REVIEWER_IDS)

    premature = mod.validate_reviewer_stage_state(
        {
            "independents_complete": ["methodology", "domain"],
            "visibility": {rid: [] for rid in ids},
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
    assert premature["ok"] is False
    assert premature["error"] == "premature_synthesis"

    peer_see = mod.validate_reviewer_stage_state(
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
    assert peer_see["ok"] is False
    assert peer_see["error"] == "early_visibility"

    erased = mod.validate_reviewer_stage_state(
        {
            "independents_complete": ids,
            "visibility": {rid: [] for rid in ids},
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
                    "rationale": "transfer unclear",
                },
            ],
        }
    )
    assert erased["ok"] is False
    assert erased["error"] == "missing_disposition"
    return None


def test_e3c_reviewer_identity_positives_and_negatives() -> None:
    """Named reviewer lacks source/confirm; invented/self/circular source; simulated ok."""
    mod = load_gates_module()

    sim = mod.evaluate_reviewer_identity(
        {
            "identity_kind": "simulated_role",
            "role_label": "methodology",
            "labeled_simulated": True,
        }
    )
    assert sim["ok"] is True, sim

    anon = mod.evaluate_reviewer_identity(
        {
            "identity_kind": "anonymous",
            "label": "anonymous independent",
            "labeled_anonymous": True,
        }
    )
    assert anon["ok"] is True, anon

    named_ok = mod.evaluate_reviewer_identity(
        {
            "identity_kind": "named_real",
            "display_name": "Ada Reviewer",
            "identity_source": "user-supplied CV attachment",
            "human_confirmation": True,
        }
    )
    assert named_ok["ok"] is True, named_ok

    # Legitimate sources must not be rejected by short-token substring false positives.
    for legitimate_source in (
        "Nature staff profile",
        "National university roster",
        "journal masthead",
    ):
        legit = mod.evaluate_reviewer_identity(
            {
                "identity_kind": "named_real",
                "display_name": "Ada Reviewer",
                "identity_source": legitimate_source,
                "human_confirmation": True,
            }
        )
        assert legit["ok"] is True, (legitimate_source, legit)

    # Display name alone never validates identity (no kind).
    name_only = mod.evaluate_reviewer_identity({"display_name": "Ada Reviewer"})
    assert name_only["ok"] is False
    assert name_only["error"] == "missing_identity_kind"

    # Simulated/anonymous without explicit label fail closed even with a name.
    sim_unlabeled = mod.evaluate_reviewer_identity(
        {
            "identity_kind": "simulated_role",
            "display_name": "Famous Scholar",
        }
    )
    assert sim_unlabeled["ok"] is False
    assert sim_unlabeled["error"] == "unlabeled_simulated"

    anon_unlabeled = mod.evaluate_reviewer_identity(
        {
            "identity_kind": "anonymous",
            "display_name": "Dr X",
        }
    )
    assert anon_unlabeled["ok"] is False
    assert anon_unlabeled["error"] == "unlabeled_simulated"

    no_source = mod.evaluate_reviewer_identity(
        {
            "identity_kind": "named_real",
            "display_name": "Dr. Example",
            "identity_source": "",
            "human_confirmation": True,
        }
    )
    assert no_source["ok"] is False
    assert no_source["error"] == "missing_identity_source"

    no_confirm = mod.evaluate_reviewer_identity(
        {
            "identity_kind": "named_real",
            "display_name": "Dr. Example",
            "identity_source": "user roster",
            "human_confirmation": False,
        }
    )
    assert no_confirm["ok"] is False
    assert no_confirm["error"] == "missing_human_confirmation"

    invented = mod.evaluate_reviewer_identity(
        {
            "identity_kind": "named_real",
            "display_name": "Famous Scholar",
            "identity_source": "invented prestige persona",
            "human_confirmation": True,
        }
    )
    assert invented["ok"] is False
    assert invented["error"] == "forbidden_identity_source"

    assumed = mod.evaluate_reviewer_identity(
        {
            "identity_kind": "named_real",
            "display_name": "Assumed Editor",
            "identity_source": "assumed",
            "human_confirmation": True,
        }
    )
    assert assumed["ok"] is False
    assert assumed["error"] == "forbidden_identity_source"

    self_asserted = mod.evaluate_reviewer_identity(
        {
            "identity_kind": "named_real",
            "display_name": "Ada",
            "identity_source": "self-asserted",
            "human_confirmation": True,
        }
    )
    assert self_asserted["ok"] is False
    assert self_asserted["error"] == "forbidden_identity_source"

    circular = mod.evaluate_reviewer_identity(
        {
            "identity_kind": "named_real",
            "display_name": "Ada",
            "identity_source": "circular provenance from display_name Ada",
            "human_confirmation": True,
        }
    )
    assert circular["ok"] is False
    assert circular["error"] == "forbidden_identity_source"

    source_eq_name = mod.evaluate_reviewer_identity(
        {
            "identity_kind": "named_real",
            "display_name": "Ada Reviewer",
            "identity_source": "Ada Reviewer",
            "human_confirmation": True,
        }
    )
    assert source_eq_name["ok"] is False
    assert source_eq_name["error"] == "forbidden_identity_source"

    na_source = mod.evaluate_reviewer_identity(
        {
            "identity_kind": "named_real",
            "display_name": "Ada Reviewer",
            "identity_source": "n/a",
            "human_confirmation": True,
        }
    )
    assert na_source["ok"] is False
    assert na_source["error"] == "forbidden_identity_source"

    # Plan-shaped list interface must also fail closed without source/confirm.
    list_no_source = mod.evaluate_reviewer_identity(
        {
            "reviewer_labels": [
                {
                    "label": "Ada",
                    "kind": "named_real_person",
                    "source": "",
                    "human_confirmed": False,
                }
            ]
        }
    )
    assert list_no_source["ok"] is False
    assert list_no_source["error"] in {
        "missing_identity_source",
        "missing_human_confirmation",
    }
    return None


def test_e3c_rereview_consistency_positives_and_negatives() -> None:
    """Empty/duplicate/missing/orphan IDs, partial residual, new cannot offset, blanket."""
    mod = load_gates_module()

    good = mod.evaluate_rereview_consistency(_rereview_base())
    assert good["ok"] is True, good

    open_ok = mod.evaluate_rereview_consistency(
        {
            "prior_issues": [{"issue_id": "M-01"}],
            "current_rows": [{"issue_id": "M-01", "trajectory": "open"}],
        }
    )
    assert open_ok["ok"] is True, open_ok

    empty_prior = mod.evaluate_rereview_consistency(
        _rereview_base(prior_issues=[], current_rows=[])
    )
    assert empty_prior["ok"] is False
    assert empty_prior["error"] == "empty_prior_issues"

    empty_id = mod.evaluate_rereview_consistency(
        _rereview_base(prior_issues=[{"issue_id": ""}, {"issue_id": "M-01"}])
    )
    assert empty_id["ok"] is False
    assert empty_id["error"] == "empty_issue_id"

    dup = mod.evaluate_rereview_consistency(
        _rereview_base(
            prior_issues=[{"issue_id": "M-01"}, {"issue_id": "M-01"}],
        )
    )
    assert dup["ok"] is False
    assert dup["error"] == "duplicate_prior_issue"

    dup_current = mod.evaluate_rereview_consistency(
        {
            "prior_issues": [{"issue_id": "M-01"}],
            "current_rows": [
                {
                    "issue_id": "M-01",
                    "trajectory": "addressed",
                    "pointer": "ms §3.2",
                },
                {
                    "issue_id": "M-01",
                    "trajectory": "open",
                },
            ],
        }
    )
    assert dup_current["ok"] is False
    assert dup_current["error"] == "duplicate_current_issue"

    missing = mod.evaluate_rereview_consistency(
        _rereview_base(
            current_rows=[
                {
                    "issue_id": "M-01",
                    "trajectory": "addressed",
                    "pointer": "ms §3.2",
                },
            ]
        )
    )
    assert missing["ok"] is False
    assert missing["error"] == "missing_prior_coverage"

    # A new issue cannot satisfy or offset a missing prior issue.
    new_offsets = mod.evaluate_rereview_consistency(
        {
            "prior_issues": [{"issue_id": "M-01"}, {"issue_id": "DA-01"}],
            "current_rows": [
                {
                    "issue_id": "M-01",
                    "trajectory": "addressed",
                    "pointer": "ms §3.2",
                },
                {
                    "issue_id": "N-01",
                    "trajectory": "new",
                    "pointer": "ms §5",
                },
            ],
        }
    )
    assert new_offsets["ok"] is False
    assert new_offsets["error"] == "missing_prior_coverage"

    orphan = mod.evaluate_rereview_consistency(
        _rereview_base(
            current_rows=[
                {
                    "issue_id": "M-01",
                    "trajectory": "addressed",
                    "pointer": "ms §3.2",
                },
                {
                    "issue_id": "DA-01",
                    "trajectory": "open",
                    "pointer": "",
                },
                {
                    "issue_id": "ORPHAN-9",
                    "trajectory": "open",
                    "pointer": "",
                },
            ]
        )
    )
    assert orphan["ok"] is False
    assert orphan["error"] == "orphan_issue_row"

    no_pointer = mod.evaluate_rereview_consistency(
        _rereview_base(
            current_rows=[
                {"issue_id": "M-01", "trajectory": "addressed", "pointer": ""},
                {
                    "issue_id": "DA-01",
                    "trajectory": "open",
                    "pointer": "",
                },
            ]
        )
    )
    assert no_pointer["ok"] is False
    assert no_pointer["error"] == "addressed_without_pointer"

    partial_no_pointer = mod.evaluate_rereview_consistency(
        {
            "prior_issues": [{"issue_id": "M-01"}],
            "current_rows": [
                {
                    "issue_id": "M-01",
                    "trajectory": "partially_addressed",
                    "pointer": "",
                    "residual_gap": "still incomplete",
                }
            ],
        }
    )
    assert partial_no_pointer["ok"] is False
    assert partial_no_pointer["error"] == "addressed_without_pointer"

    partial_no_gap = mod.evaluate_rereview_consistency(
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
    assert partial_no_gap["ok"] is False
    assert partial_no_gap["error"] == "partial_without_residual"

    new_as_close = mod.evaluate_rereview_consistency(
        _rereview_base(
            current_rows=[
                {"issue_id": "M-01", "trajectory": "new", "pointer": "ms §3.2"},
                {
                    "issue_id": "DA-01",
                    "trajectory": "open",
                    "pointer": "",
                },
            ]
        )
    )
    assert new_as_close["ok"] is False
    assert new_as_close["error"] == "new_as_prior_closure"

    # Reach blanket_all_fixed only after rows themselves are trajectory-valid.
    blanket = mod.evaluate_rereview_consistency(
        _rereview_base(
            claim_all_fixed=True,
            current_rows=[
                {
                    "issue_id": "M-01",
                    "trajectory": "addressed",
                    "pointer": "ms §3.2",
                },
                {
                    "issue_id": "DA-01",
                    "trajectory": "open",
                    "pointer": "",
                },
            ],
        )
    )
    assert blanket["ok"] is False
    assert blanket["error"] == "blanket_all_fixed"
    return None


def test_e3c_calibration_gold_positives_and_negatives() -> None:
    """Missing/empty/inadequate/excessive/mismatched gold; no metrics leak."""
    mod = load_gates_module()

    good = mod.evaluate_calibration_gold(_calibration_base())
    assert good["ok"] is True, good
    assert good.get("metrics") is None

    missing = mod.evaluate_calibration_gold(
        {
            "predictions": [{"item_id": "C1", "label": "major"}],
            "session_only": True,
        }
    )
    assert missing["ok"] is False
    assert missing["error"] == "missing_calibration_gold"
    assert missing.get("metrics") is None

    empty = mod.evaluate_calibration_gold(
        _calibration_base(gold_labels=[], predictions=[])
    )
    assert empty["ok"] is False
    assert empty["error"] in {"empty_gold", "missing_calibration_gold"}
    assert empty.get("metrics") is None

    # Protocol minimum: a single gold item is inadequate even if 1:1 mapped.
    inadequate = mod.evaluate_calibration_gold(
        {
            "gold_labels": [{"item_id": "C1", "label": "major"}],
            "predictions": [{"item_id": "C1", "label": "major"}],
            "session_only": True,
        }
    )
    assert inadequate["ok"] is False
    assert inadequate["error"] == "inadequate_gold_set"
    assert inadequate.get("metrics") is None

    # Two-row set is under the accepted 5–20 range and must fail closed.
    two_rows = mod.evaluate_calibration_gold(
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
    assert two_rows["ok"] is False
    assert two_rows["error"] == "inadequate_gold_set"
    assert two_rows.get("metrics") is None

    # Twenty-one rows exceed the accepted maximum.
    oversize_labels = [
        {"item_id": f"C{i}", "label": "major" if i % 2 else "minor"}
        for i in range(1, 22)
    ]
    twenty_one = mod.evaluate_calibration_gold(
        {
            "gold_labels": oversize_labels,
            "predictions": [dict(row) for row in oversize_labels],
            "session_only": True,
        }
    )
    assert twenty_one["ok"] is False
    assert twenty_one["error"] == "excessive_gold_set"
    assert twenty_one.get("metrics") is None

    empty_preds = [dict(row) for row in _calibration_base()["gold_labels"]]
    empty_preds[0] = {"item_id": "C1", "label": ""}
    empty_label = mod.evaluate_calibration_gold(
        _calibration_base(predictions=empty_preds)
    )
    assert empty_label["ok"] is False
    assert empty_label["error"] == "empty_label"
    assert empty_label.get("metrics") is None

    dup_gold_labels = [dict(row) for row in _calibration_base()["gold_labels"]]
    dup_gold_labels[1] = {"item_id": "C1", "label": "minor"}
    dup_gold = mod.evaluate_calibration_gold(
        _calibration_base(gold_labels=dup_gold_labels)
    )
    assert dup_gold["ok"] is False
    assert dup_gold["error"] == "duplicate_gold_id"
    assert dup_gold.get("metrics") is None

    dup_preds = [dict(row) for row in _calibration_base()["gold_labels"]]
    dup_preds[1] = {"item_id": "C1", "label": "minor"}
    dup_pred = mod.evaluate_calibration_gold(
        _calibration_base(predictions=dup_preds)
    )
    assert dup_pred["ok"] is False
    assert dup_pred["error"] == "duplicate_prediction_id"
    assert dup_pred.get("metrics") is None

    mismatched = mod.evaluate_calibration_gold(
        _calibration_base(
            predictions=[{"item_id": "C9", "label": "major"}],
        )
    )
    assert mismatched["ok"] is False
    assert mismatched["error"] == "mismatched_prediction_ids"
    assert mismatched.get("metrics") is None

    orphan_preds = [dict(row) for row in _calibration_base()["gold_labels"]]
    orphan_preds.append({"item_id": "C9", "label": "major"})
    orphan_pred = mod.evaluate_calibration_gold(
        _calibration_base(predictions=orphan_preds)
    )
    assert orphan_pred["ok"] is False
    assert orphan_pred["error"] == "mismatched_prediction_ids"
    assert orphan_pred.get("metrics") is None

    uncovered = mod.evaluate_calibration_gold(
        _calibration_base(
            predictions=[{"item_id": "C1", "label": "major"}],
        )
    )
    assert uncovered["ok"] is False
    assert uncovered["error"] == "mismatched_prediction_ids"
    assert uncovered.get("metrics") is None

    fabricated = mod.evaluate_calibration_gold(
        _calibration_base(fabricated_labels=True)
    )
    assert fabricated["ok"] is False
    assert fabricated["error"] == "fabricated_labels"
    assert fabricated.get("metrics") is None

    persistent = mod.evaluate_calibration_gold(
        _calibration_base(persistent_calibration_claim=True)
    )
    assert persistent["ok"] is False
    assert persistent["error"] == "persistent_calibration_claim"
    assert persistent.get("metrics") is None

    not_session = mod.evaluate_calibration_gold(_calibration_base(session_only=False))
    assert not_session["ok"] is False
    assert not_session["error"] == "persistent_calibration_claim"
    assert not_session.get("metrics") is None
    return None


def test_e3c_quick_and_guided_mode_honesty() -> None:
    """Quick claims full panel; guided becomes one-shot dump or hollow dialogue."""
    mod = load_gates_module()
    protocol = _read_surface("core/protocols/manuscript_review.md")
    assert mod.evaluate_quick_mode_honesty(protocol)[0] is True
    assert mod.evaluate_guided_mode_honesty(protocol)[0] is True

    quick_claim = (
        "# Quick mode\n\n"
        "### quick_mode_outputs\n\n"
        "Quick mode completes full-panel completion with four independent "
        "reports and synthesis readiness for venue decisions immediately.\n"
    )
    q_ok, q_detail = mod.evaluate_quick_mode_honesty(quick_claim)
    assert q_ok is False
    assert "full-panel" in q_detail or "full" in q_detail.lower()

    guided_dump = (
        "# Guided mode\n\n"
        "### guided_mode_outputs\n\n"
        "Deliver a one-shot full review info dump covering every issue without "
        "dialogue checkpoints or human confirmation turns.\n"
    )
    g_ok, g_detail = mod.evaluate_guided_mode_honesty(guided_dump)
    assert g_ok is False
    assert "one-shot" in g_detail or "dump" in g_detail or "checkpoint" in g_detail

    # Keyword dialogue fields without real question-response-checkpoint progression.
    guided_hollow = (
        "# Guided mode\n\n"
        "### guided_mode_outputs\n\n"
        "Preserve dialogue checkpoints and forbid one-shot dumps. checkpoint dialogue "
        "must not be a one-shot dump. guided_no_oneshot_dump must not allow one-shot dump.\n"
        + ("x" * 40)
    )
    gh_ok, gh_detail = mod.evaluate_guided_mode_honesty(guided_hollow)
    assert gh_ok is False
    assert "progression" in gh_detail or "question" in gh_detail

    dialogue_pos = mod.evaluate_guided_dialogue(
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
    assert dialogue_pos["ok"] is True, dialogue_pos

    dialogue_oneshot = mod.evaluate_guided_dialogue(
        {
            "oneshot_dump": True,
            "turns": [
                {
                    "checkpoint_id": "G1",
                    "question": "full review?",
                    "response": "here is entire review dump labeled as dialogue",
                },
                {
                    "checkpoint_id": "G2",
                    "question": "more?",
                    "response": "still one dump",
                },
            ],
        }
    )
    assert dialogue_oneshot["ok"] is False
    assert dialogue_oneshot["error"] == "oneshot_dump"

    dialogue_short = mod.evaluate_guided_dialogue(
        {
            "turns": [
                {
                    "checkpoint_id": "G1",
                    "question": "only one turn",
                    "response": "answer",
                }
            ]
        }
    )
    assert dialogue_short["ok"] is False
    assert dialogue_short["error"] == "missing_progression"
    return None


def test_e3c_designated_templates_hollow_while_protocol_complete() -> None:
    """Hollow manuscript-review and editorial-decision templates fail isolation."""
    mod = load_gates_module()
    protocol = _read_surface("core/protocols/manuscript_review.md")
    assert mod.evaluate_all_reviewer_modes_text(protocol)[0] is True

    review_tpl = _read_surface("core/templates/manuscript_review_full.md")
    decision_tpl = _read_surface("core/templates/editorial_decision.md")
    assert mod.evaluate_manuscript_review_template_text(review_tpl)[0] is True
    assert mod.evaluate_editorial_decision_template_text(decision_tpl)[0] is True

    hollow_review = _hollow_field(review_tpl, "minority_disposition", "x\n")
    # Protocol completeness + later complete labeled field must not rescue.
    hollow_review = (
        hollow_review
        + "\nElsewhere residual: minority_disposition retained rationale complete.\n"
        + "\n### minority_disposition\n\n"
        "Every independent concern ends with disposition retained, downgraded, or "
        "rejected plus a non-empty rationale. Minority DA findings must not be erased "
        "by majority vote or synthesis convenience.\n"
        + "\n"
        + protocol
    )
    assert mod.evaluate_all_reviewer_modes_text(protocol)[0] is True
    r_ok, r_detail = mod.evaluate_manuscript_review_template_text(hollow_review)
    assert r_ok is False
    assert "minority_disposition" in r_detail

    hollow_decision = _hollow_field(decision_tpl, "simulated_disclaimer", "x\n")
    hollow_decision = (
        hollow_decision
        + "\nElsewhere residual: simulated_disclaimer venue authority complete.\n"
        + "\n### simulated_disclaimer\n\n"
        "This decision letter is simulated unless a real venue editor process and "
        "human authority are supplied and confirmed. Simulated disclaimers must remain "
        "visible on every letter surface without exception.\n"
        + "\n"
        + protocol
    )
    d_ok, d_detail = mod.evaluate_editorial_decision_template_text(hollow_decision)
    assert d_ok is False
    assert "simulated_disclaimer" in d_detail
    return None


def test_e3c_public_gates_reviewer_independence_and_content_depth() -> None:
    """Public reviewer_independence and content_depth pass with E3-C."""
    indep = run_gates(["gate", "--id", "reviewer_independence", "--json"])
    assert indep.returncode == 0, indep.stdout
    indep_data = json.loads(indep.stdout)
    assert indep_data["ok"] is True
    indep_detail = indep_data["results"][0]["detail"]
    assert "E3-C" in indep_detail or "identity" in indep_detail.lower()

    depth = run_gates(["gate", "--id", "content_depth", "--json"])
    assert depth.returncode == 0, depth.stdout
    depth_data = json.loads(depth.stdout)
    assert depth_data["ok"] is True
    depth_detail = depth_data["results"][0]["detail"]
    assert "E3-C" in depth_detail or "review" in depth_detail.lower()
    return None


def test_e3c_repository_template_and_coherent_helpers_pass() -> None:
    """Coherent positives for modes, identity, re-review, calibration, templates."""
    mod = load_gates_module()
    ok, detail = mod.evaluate_all_reviewer_modes_text(
        _read_surface("core/protocols/manuscript_review.md")
    )
    assert ok is True, detail

    ok, detail = mod.evaluate_manuscript_review_template_text(
        _read_surface("core/templates/manuscript_review_full.md")
    )
    assert ok is True, detail
    ok, detail = mod.evaluate_editorial_decision_template_text(
        _read_surface("core/templates/editorial_decision.md")
    )
    assert ok is True, detail

    id_ok = mod.evaluate_reviewer_identity(
        {
            "identity_kind": "simulated_role",
            "role_label": "domain",
            "labeled_simulated": True,
        }
    )
    assert id_ok["ok"] is True, id_ok

    rr_ok = mod.evaluate_rereview_consistency(_rereview_base())
    assert rr_ok["ok"] is True, rr_ok

    cal_ok = mod.evaluate_calibration_gold(_calibration_base())
    assert cal_ok["ok"] is True, cal_ok

    # Public gate ID snapshot remains frozen at 21.
    listed = run_gates(["list", "--json"])
    assert listed.returncode == 0
    gates = set(json.loads(listed.stdout)["gates"])
    assert len(gates) == 21
    return None
