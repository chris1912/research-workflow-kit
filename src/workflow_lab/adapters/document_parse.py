"""Adapter for PDF, DOCX, and image parsing backends."""

from pathlib import Path

from ..contracts import AdapterResult, failure_result
from ..process import run_stage


def parse(
    input_path: Path,
    *,
    output_dir: Path | None = None,
    cwd: Path | None = None,
) -> AdapterResult:
    """Parse one document through the configured document backend."""
    source = Path(input_path)
    if not source.is_file():
        return failure_result("invalid-input", f"Input document does not exist: {source}")
    arguments = ["-p", str(source)]
    if output_dir:
        arguments.extend(["-o", str(output_dir)])
    return run_stage("WORKFLOW_LAB_DOCUMENT_CMD", "mineru", arguments, cwd=cwd)

