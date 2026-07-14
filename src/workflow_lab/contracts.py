"""Stable result contracts shared by optional workflow backends.

Codex annotation: Created by Codex on 2026-07-15.
"""

from dataclasses import dataclass
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class AdapterResult:
    """Describe one backend invocation without rewriting scientific content."""

    status: str
    command: tuple[str, ...]
    stdout: str = ""
    stderr: str = ""
    returncode: int | None = None
    artifacts: tuple[Path, ...] = ()
    warnings: tuple[str, ...] = ()

    def as_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable view of the invocation result."""
        return {
            "status": self.status,
            "command": list(self.command),
            "stdout": self.stdout,
            "stderr": self.stderr,
            "returncode": self.returncode,
            "artifacts": [str(path) for path in self.artifacts],
            "warnings": list(self.warnings),
        }


def failure_result(
    status: str,
    message: str,
    command: tuple[str, ...] = (),
) -> AdapterResult:
    """Build a deterministic failure result for validation or configuration errors."""
    return AdapterResult(status=status, command=command, stderr=message)

