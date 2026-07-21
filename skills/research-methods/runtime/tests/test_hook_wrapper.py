"""Behavioral tests for Essential Core hook wrapper safety.

Grok annotation: Added by Grok on 2026-07-20 for E1.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

METHODS_ROOT = Path(__file__).resolve().parents[2]
HOOK = METHODS_ROOT / "runtime" / "scripts" / "essential_hook.py"
REPO_ROOT = METHODS_ROOT.parents[1]


def run_hook(stdin: str, extra_env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["FAKE_API_KEY"] = "sk-this-should-never-appear-in-output-123456"
    env["OPENAI_API_KEY"] = "sk-test-not-for-output"
    if extra_env:
        env.update(extra_env)
    return subprocess.run(
        [sys.executable, str(HOOK), "announce", "--json"],
        cwd=str(REPO_ROOT),
        input=stdin,
        capture_output=True,
        text=True,
        env=env,
        check=False,
    )


def test_announce_ok_and_no_secrets() -> None:
    result = run_hook('{"event":"agent-start","workflow":"academic-paper-reviewer","mode":"full"}')
    assert result.returncode == 0, result.stderr + result.stdout
    data = json.loads(result.stdout)
    assert data["ok"] is True
    assert data["safe"] is True
    assert "research-methods essential runtime active" in data["announce"]
    blob = result.stdout + result.stderr
    assert "sk-this-should-never-appear-in-output-123456" not in blob
    assert "sk-test-not-for-output" not in blob
    assert "FAKE_API_KEY" not in blob


def test_malformed_json_exits_2() -> None:
    result = run_hook("{not-json")
    assert result.returncode == 2
    data = json.loads(result.stdout)
    assert data["ok"] is False
    assert data["error"] == "invalid_json"
