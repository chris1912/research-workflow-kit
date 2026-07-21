"""Reviewer independence fixture + stage validator semantics for Essential Core.

Grok annotation: Added by Grok on 2026-07-20 for E1.
Grok annotation: V2-3 A20 / synthesis / minority negatives by Grok on 2026-07-20
(revision 2).
Grok annotation: E3-C rationale + identity/re-review/calibration wiring by Grok on 2026-07-20.
"""

from __future__ import annotations

import importlib.util
from pathlib import Path

METHODS_ROOT = Path(__file__).resolve().parents[2]
FIXTURE = (
    METHODS_ROOT
    / "runtime"
    / "tests"
    / "fixtures"
    / "reviewer_full_independent_sections.md"
)
GATES = METHODS_ROOT / "runtime" / "scripts" / "essential_quality_gates.py"


def load_gates_module():
    spec = importlib.util.spec_from_file_location("essential_quality_gates_rev2", GATES)
    if spec is None or spec.loader is None:
        raise RuntimeError("unable to load quality gates module")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def test_fixture_section_order_and_minority_disposition() -> None:
    text = FIXTURE.read_text(encoding="utf-8")
    order = [
        "Independent Reviewer: Methodology",
        "Independent Reviewer: Domain",
        "Independent Reviewer: Interdisciplinary",
        "Independent Reviewer: Devil's Advocate",
        "Editorial Synthesis",
        "Decision Letter",
        "Revision Roadmap",
    ]
    positions = [text.find(h) for h in order]
    assert all(p >= 0 for p in positions), positions
    assert positions == sorted(positions)
    assert "disposition" in text.lower()
    assert "retained" in text.lower() or "rejected" in text.lower()
    # Synthesis must not precede independents (already ordered)
    assert positions[4] > positions[3]
    # Minority retention: DA concern disposition recorded
    assert "DA-01" in text
    assert "devils_advocate" in text.lower() or "devil" in text.lower()
    # Pre-synthesis barrier: independent headings appear once before synthesis
    independent_blob = text[: positions[4]]
    for heading in order[:4]:
        assert independent_blob.count(heading) == 1
    return None


def test_reviewer_stage_positive_and_a20_negatives() -> None:
    """Negative cases must fail; allowing them would break A20 / synthesis / minority."""
    mod = load_gates_module()
    ids = list(mod.INDEPENDENT_REVIEWER_IDS)

    good = mod.validate_reviewer_stage_state(
        {
            "independents_complete": ids,
            "visibility": {rid: [] for rid in ids},
            "synthesis_started": True,
            "dispositions": [
                {
                    "concern_id": "M-01",
                    "source": "methodology",
                    "disposition": "retained",
                    "rationale": "incomplete sample justification",
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
                    "rationale": "multi-site validity secondary",
                },
                {
                    "concern_id": "DA-01",
                    "source": "devils_advocate",
                    "disposition": "retained",
                    "rationale": "outcome switching risk remains",
                },
            ],
        }
    )
    assert good["ok"] is True, good

    early = mod.validate_reviewer_stage_state(
        {
            "independents_complete": ["methodology"],
            "visibility": {"domain": ["methodology"], "methodology": []},
            "synthesis_started": False,
            "dispositions": [],
        }
    )
    assert early["ok"] is False
    assert early["error"] == "early_visibility"

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

    missing_da = mod.validate_reviewer_stage_state(
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
                    "rationale": "measurement transfer unclear",
                },
            ],
        }
    )
    assert missing_da["ok"] is False
    assert missing_da["error"] == "missing_disposition"

    missing_rationale = mod.validate_reviewer_stage_state(
        {
            "independents_complete": ids,
            "visibility": {rid: [] for rid in ids},
            "synthesis_started": True,
            "dispositions": [
                {
                    "concern_id": "M-01",
                    "source": "methodology",
                    "disposition": "retained",
                },
                {
                    "concern_id": "D-01",
                    "source": "domain",
                    "disposition": "retained",
                    "rationale": "domain gap",
                },
                {
                    "concern_id": "I-01",
                    "source": "interdisciplinary",
                    "disposition": "retained",
                    "rationale": "transfer gap",
                },
                {
                    "concern_id": "DA-01",
                    "source": "devils_advocate",
                    "disposition": "retained",
                    "rationale": "minority risk",
                },
            ],
        }
    )
    assert missing_rationale["ok"] is False
    assert missing_rationale["error"] == "missing_rationale"
    return None


def test_e3c_identity_calibration_rereview_helpers_fail_closed() -> None:
    """E3-C direct-helper adversarial cases for identity, calibration, re-review."""
    mod = load_gates_module()

    # Display name alone is not identity.
    name_only = mod.evaluate_reviewer_identity({"display_name": "Famous Scholar"})
    assert name_only["ok"] is False
    assert name_only["error"] == "missing_identity_kind"

    unlabeled = mod.evaluate_reviewer_identity(
        {
            "identity_kind": "simulated_role",
            "display_name": "Famous Scholar",
        }
    )
    assert unlabeled["ok"] is False
    assert unlabeled["error"] == "unlabeled_simulated"

    self_asserted = mod.evaluate_reviewer_identity(
        {
            "identity_kind": "named_real_person",
            "display_name": "Ada",
            "identity_source": "self-asserted",
            "human_confirmation": True,
        }
    )
    assert self_asserted["ok"] is False
    assert self_asserted["error"] == "forbidden_identity_source"

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

    # Single/two-row gold is inadequate; invalid sets emit no metrics.
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

    gold_five = [
        {"item_id": f"C{i}", "label": "major" if i % 2 else "minor"}
        for i in range(1, 6)
    ]
    orphan_preds = [dict(row) for row in gold_five]
    orphan_preds.append({"item_id": "C9", "label": "major"})
    orphan_pred = mod.evaluate_calibration_gold(
        {
            "gold_labels": gold_five,
            "predictions": orphan_preds,
            "session_only": True,
        }
    )
    assert orphan_pred["ok"] is False
    assert orphan_pred["error"] == "mismatched_prediction_ids"
    assert orphan_pred.get("metrics") is None

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

    new_cannot_offset = mod.evaluate_rereview_consistency(
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
    assert new_cannot_offset["ok"] is False
    assert new_cannot_offset["error"] == "missing_prior_coverage"

    dialogue_oneshot = mod.evaluate_guided_dialogue(
        {
            "oneshot_dump": True,
            "turns": [
                {
                    "checkpoint_id": "G1",
                    "question": "dump?",
                    "response": "entire review as dialogue",
                },
                {
                    "checkpoint_id": "G2",
                    "question": "more?",
                    "response": "still dump",
                },
            ],
        }
    )
    assert dialogue_oneshot["ok"] is False
    assert dialogue_oneshot["error"] == "oneshot_dump"
    return None
