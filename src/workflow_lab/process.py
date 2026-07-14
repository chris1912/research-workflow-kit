"""Process helpers for optional local research tools.

Codex annotation: Created by Codex on 2026-07-15.
"""

import os
import shlex
import subprocess
from pathlib import Path
from typing import Sequence

from .contracts import AdapterResult, failure_result


def command_from_env(env_name: str, default: str | None) -> tuple[str, ...]:
    """Resolve a command from an environment variable or a safe executable default."""
    raw = os.getenv(env_name, "").strip()
    if raw:
        return tuple(shlex.split(raw, posix=os.name != "nt"))
    if default:
        return (default,)
    return ()


def run_command(
    command: Sequence[str],
    *,
    cwd: Path | None = None,
    timeout_seconds: float = 120.0,
) -> AdapterResult:
    """Run an optional backend and preserve stdout, stderr, and exit status.

    The helper deliberately avoids shell expansion and never reads credential files.
    A missing executable, timeout, or non-zero exit is represented as a structured
    result so callers can show an actionable message instead of silently falling
    back to a different scientific method.
    """
    normalized = tuple(str(part) for part in command)
    if not normalized:
        return failure_result("missing", "No backend command was configured.")
    try:
        completed = subprocess.run(
            normalized,
            cwd=str(cwd) if cwd else None,
            capture_output=True,
            text=True,
            check=False,
            timeout=timeout_seconds,
        )
    except FileNotFoundError:
        return failure_result(
            "missing",
            f"Backend executable was not found: {normalized[0]}",
            normalized,
        )
    except subprocess.TimeoutExpired as exc:
        return AdapterResult(
            status="timeout",
            command=normalized,
            stdout=exc.stdout or "",
            stderr=exc.stderr or "",
            warnings=(f"Backend exceeded {timeout_seconds} seconds.",),
        )
    status = "ok" if completed.returncode == 0 else "failed"
    return AdapterResult(
        status=status,
        command=normalized,
        stdout=completed.stdout,
        stderr=completed.stderr,
        returncode=completed.returncode,
    )


def run_stage(
    env_name: str,
    default: str | None,
    arguments: Sequence[str],
    *,
    cwd: Path | None = None,
    timeout_seconds: float = 120.0,
) -> AdapterResult:
    """Resolve one stage command and run it with explicit arguments."""
    executable = command_from_env(env_name, default)
    if not executable:
        return failure_result(
            "missing",
            f"Configure {env_name} before using this workflow stage.",
        )
    return run_command(
        (*executable, *(str(argument) for argument in arguments)),
        cwd=cwd,
        timeout_seconds=timeout_seconds,
    )

