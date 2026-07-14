"""Tests for first-party adapter contracts."""

from pathlib import Path
import sys

from workflow_lab.adapters.document_parse import parse
from workflow_lab.adapters.evidence_qa import ask
from workflow_lab.adapters.literature_map import analyze
from workflow_lab.adapters.research_synthesis import synthesize
from workflow_lab.process import run_command


def test_run_command_preserves_success_output() -> None:
    result = run_command((sys.executable, "-c", "print('ok')"))
    assert result.status == "ok"
    assert result.stdout.strip() == "ok"


def test_document_parser_rejects_missing_input(tmp_path: Path) -> None:
    result = parse(tmp_path / "missing.pdf")
    assert result.status == "invalid-input"
    assert "does not exist" in result.stderr


def test_literature_backend_requires_explicit_command(tmp_path: Path, monkeypatch) -> None:
    monkeypatch.delenv("WORKFLOW_LAB_LITERATURE_CMD", raising=False)
    metadata = tmp_path / "metadata.json"
    metadata.write_text("{}", encoding="utf-8")
    result = analyze(metadata)
    assert result.status == "missing"


def test_path_and_prompt_validation_is_explicit(tmp_path: Path) -> None:
    assert analyze(tmp_path / "missing.json").status == "invalid-input"
    assert ask("", corpus=tmp_path).status == "invalid-input"
    assert ask("question", corpus=tmp_path / "missing").status == "invalid-input"
    assert synthesize(" ").status == "invalid-input"


def test_run_command_reports_timeout() -> None:
    result = run_command((sys.executable, "-c", "import time; time.sleep(0.2)"), timeout_seconds=0.01)
    assert result.status == "timeout"
