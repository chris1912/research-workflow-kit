"""Adapter for deterministic prose linting with local Vale installation."""

import os
from pathlib import Path

from ..contracts import AdapterResult, failure_result
from ..process import run_stage


def lint(
    input_path: Path,
    *,
    profile: str = "general",
    cwd: Path | None = None,
) -> AdapterResult:
    """Lint a human-facing draft with the selected local rule profile."""
    source = Path(input_path)
    if not source.is_file():
        return failure_result("invalid-input", f"Input draft does not exist: {source}")
    config = os.getenv("WORKFLOW_LAB_VALE_CONFIG", "").strip()
    if not config:
        config_name = "vale-grant.ini" if profile == "grant" else "vale.ini"
        config = str(Path(__file__).parents[1] / "config" / "vale" / config_name)
    return run_stage(
        "WORKFLOW_LAB_PROSE_LINT_CMD",
        "vale",
        [str(source), "--config", config],
        cwd=cwd,
    )

