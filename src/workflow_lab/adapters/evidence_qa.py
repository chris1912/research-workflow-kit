"""Adapter for evidence-grounded local corpus question answering."""

from pathlib import Path

from ..contracts import AdapterResult, failure_result
from ..process import run_stage


def ask(
    question: str,
    *,
    corpus: Path | None = None,
    cwd: Path | None = None,
) -> AdapterResult:
    """Ask the configured corpus backend without changing claim wording."""
    if not question.strip():
        return failure_result("invalid-input", "A non-empty question is required.")
    if corpus is not None and not Path(corpus).exists():
        return failure_result("invalid-input", f"Corpus path does not exist: {corpus}")
    arguments = ["ask", question]
    if corpus:
        arguments.extend(["--corpus", str(corpus)])
    return run_stage("WORKFLOW_LAB_EVIDENCE_CMD", "pqa", arguments, cwd=cwd)
