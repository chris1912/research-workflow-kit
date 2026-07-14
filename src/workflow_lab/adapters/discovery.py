"""Adapter for paper discovery backends installed by the user."""

from pathlib import Path
from typing import Sequence

from ..contracts import AdapterResult, failure_result
from ..process import run_stage


def search(
    query: str,
    *,
    sources: Sequence[str] = (),
    cwd: Path | None = None,
) -> AdapterResult:
    """Search configured literature sources and preserve the backend output."""
    if not query.strip():
        return failure_result("invalid-input", "A non-empty discovery query is required.")
    arguments = ["search", query]
    if sources:
        arguments.extend(["-s", ",".join(sources)])
    return run_stage("WORKFLOW_LAB_DISCOVERY_CMD", "paper-search", arguments, cwd=cwd)
