"""Adapter for broad research synthesis backends."""

from pathlib import Path

from ..contracts import AdapterResult, failure_result
from ..process import run_stage


def synthesize(prompt: str, *, cwd: Path | None = None) -> AdapterResult:
    """Run a configured synthesis backend with one explicit prompt."""
    if not prompt.strip():
        return failure_result("invalid-input", "A non-empty synthesis prompt is required.")
    return run_stage(
        "WORKFLOW_LAB_SYNTHESIS_CMD",
        None,
        [prompt],
        cwd=cwd,
    )
