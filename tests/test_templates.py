"""Tests for public example artifacts."""

import json
from pathlib import Path


def test_example_evidence_card_is_valid_jsonl() -> None:
    path = Path(__file__).resolve().parents[1] / "examples" / "minimal" / "evidence_card.jsonl"
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    assert len(records) == 1
    assert records[0]["epistemic_status"] == "placeholder"

