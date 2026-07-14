"""Adapter for bibliometric and literature-map workflows."""

from pathlib import Path

from ..contracts import AdapterResult, failure_result
from ..process import run_stage


def analyze(metadata_path: Path, *, cwd: Path | None = None) -> AdapterResult:
    """Run the configured literature-analysis command over metadata input."""
    source = Path(metadata_path)
    if not source.is_file():
        return failure_result("invalid-input", f"Metadata input does not exist: {source}")
    return run_stage(
        "WORKFLOW_LAB_LITERATURE_CMD",
        None,
        [str(source)],
        cwd=cwd,
    )
