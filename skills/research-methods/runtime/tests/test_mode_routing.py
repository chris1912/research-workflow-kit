"""Behavioral tests for Essential Core mode routing planner.

Grok annotation: Added by Grok on 2026-07-20 for E1.
Grok annotation: Exhaustive alias + ambiguity + reproducibility coverage by Grok
on 2026-07-20 (E0/E1 revision 1).
Grok annotation: V2-1 ambiguous mode workflow context retention by Grok on 2026-07-20
(revision 2).
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

METHODS_ROOT = Path(__file__).resolve().parents[2]
PLANNER = METHODS_ROOT / "runtime" / "scripts" / "essential_full_runtime.py"
MANIFEST = METHODS_ROOT / "runtime" / "full-runtime-manifest.json"
REPO_ROOT = METHODS_ROOT.parents[1]


def run_planner(args: list[str], env: dict[str, str] | None = None) -> subprocess.CompletedProcess[str]:
    full_env = os.environ.copy()
    if env:
        full_env.update(env)
    return subprocess.run(
        [sys.executable, str(PLANNER), *args],
        cwd=str(REPO_ROOT),
        capture_output=True,
        text=True,
        env=full_env,
        check=False,
    )


def load_manifest() -> dict:
    return json.loads(MANIFEST.read_text(encoding="utf-8"))


def test_list_aliases_includes_ars_and_rm() -> None:
    result = run_planner(["list-aliases", "--json"])
    assert result.returncode == 0, result.stderr
    data = json.loads(result.stdout)
    assert data["ok"] is True
    aliases = set(data["supported_aliases"])
    assert "ars-plan" in aliases
    assert "rm-plan" in aliases
    assert "ars-reviewer" in aliases
    assert data["count"] == 68
    assert len(aliases) == 68


def test_vague_paper_topic_routes_to_socratic() -> None:
    result = run_planner(
        ["plan", "--text", "I want to write a paper about X", "--json"]
    )
    assert result.returncode == 0, result.stderr + result.stdout
    data = json.loads(result.stdout)
    assert data["ok"] is True
    assert data["workflow"] == "deep-research"
    assert data["mode"] == "socratic"
    assert data["route_reason"] == "paper_topic_scoping_override"


def test_unsupported_alias_exits_2() -> None:
    result = run_planner(
        ["plan", "--alias", "ars-not-a-real-command", "--json"]
    )
    assert result.returncode == 2
    data = json.loads(result.stdout)
    assert data["ok"] is False
    assert data["error"] == "unsupported_alias"
    assert "ars-plan" in data["supported_aliases"]
    assert len(data["supported_aliases"]) == 68


def test_known_alias_plan() -> None:
    result = run_planner(["plan", "--alias", "ars-plan", "--json"])
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["ok"] is True
    assert data["workflow"] == "academic-paper"
    assert data["mode"] == "plan"
    assert data["route_reason"] == "alias"


def test_systematic_review_alias() -> None:
    result = run_planner(["plan", "--alias", "ars-systematic-review", "--json"])
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["ok"] is True
    assert data["workflow"] == "deep-research"
    assert data["mode"] == "systematic-review"


def test_experiment_validate_alias() -> None:
    result = run_planner(["plan", "--alias", "rm-experiment-validate", "--json"])
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["ok"] is True
    assert data["workflow"] == "experiment"
    assert data["mode"] == "validate"


def test_reproducibility_text_routes_to_validate() -> None:
    result = run_planner(
        [
            "plan",
            "--text",
            "please validate reproducibility of this experiment",
            "--json",
        ]
    )
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["ok"] is True
    assert data["workflow"] == "experiment"
    assert data["mode"] == "validate"
    assert data["route_reason"] == "heuristic"


@pytest.mark.parametrize(
    "mode_token,expected_reason",
    [
        ("full", "ambiguous_mode_default"),
        ("quick", "ambiguous_mode_default"),
        ("plan", "ambiguous_mode_default"),
        ("lit-review", "ambiguous_mode_default"),
    ],
)
def test_ambiguous_explicit_modes_use_safe_default(
    mode_token: str, expected_reason: str
) -> None:
    result = run_planner(["plan", "--text", f"mode:{mode_token}", "--json"])
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["ok"] is True
    assert data["route_reason"] == expected_reason
    # Never silent full draft for bare mode:full.
    if mode_token == "full":
        assert data["mode"] == "socratic"
        assert data["workflow"] == "deep-research"


@pytest.mark.parametrize(
    "text,expected_workflow,expected_mode",
    [
        # quick: deep-research | academic-paper-reviewer
        ("mode:quick peer review", "academic-paper-reviewer", "quick"),
        ("mode:quick deep research scan", "deep-research", "quick"),
        # full: deep-research | academic-paper | academic-paper-reviewer
        ("mode:full peer review", "academic-paper-reviewer", "full"),
        ("mode:full academic paper", "academic-paper", "full"),
        ("mode:full systematic review context", "deep-research", "full"),
        # lit-review: deep-research | academic-paper
        ("mode:lit-review academic paper", "academic-paper", "lit-review"),
        ("mode:lit-review deep research matrix", "deep-research", "lit-review"),
        # plan: academic-paper | experiment
        ("mode:plan experiment protocol", "experiment", "plan"),
        ("mode:plan academic paper outline", "academic-paper", "plan"),
    ],
)
def test_ambiguous_mode_context_keeps_requested_mode(
    text: str, expected_workflow: str, expected_mode: str
) -> None:
    """Context disambiguates workflow only; explicit mode is retained."""
    result = run_planner(["plan", "--text", text, "--json"])
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert data["ok"] is True
    assert data["workflow"] == expected_workflow
    assert data["mode"] == expected_mode
    assert data["route_reason"] == "explicit_mode_disambiguated"


def test_missing_backend_honesty_fields() -> None:
    env = {"WORKFLOW_LAB_DISCOVERY_CMD": "", "OPENALEX_API_KEY": ""}
    result = run_planner(
        ["plan", "--text", "mode:outline-only outline a paper with RQ: does A affect B?", "--json"],
        env=env,
    )
    assert result.returncode == 0, result.stdout
    data = json.loads(result.stdout)
    assert "missing_backends" in data["runtime"]
    assert isinstance(data["runtime"]["missing_backends"], list)


def test_every_advertised_alias_routes() -> None:
    man = load_manifest()
    aliases = man.get("aliases") or {}
    assert len(aliases) == 68
    failures: list[str] = []
    for alias, entry in sorted(aliases.items()):
        result = run_planner(["plan", "--alias", alias, "--json"])
        if result.returncode != 0:
            failures.append(f"{alias}: exit {result.returncode} {result.stdout[:120]}")
            continue
        data = json.loads(result.stdout)
        if not data.get("ok"):
            failures.append(f"{alias}: not ok {data.get('error')}")
            continue
        if data.get("workflow") != entry.get("workflow") or data.get("mode") != entry.get("mode"):
            failures.append(
                f"{alias}: got {data.get('workflow')}/{data.get('mode')} "
                f"expected {entry.get('workflow')}/{entry.get('mode')}"
            )
    assert failures == [], "alias routing failures:\n" + "\n".join(failures)


def test_every_mode_row_has_protocol_path() -> None:
    man = load_manifest()
    modes = man.get("modes") or []
    assert len(modes) == 34
    for row in modes:
        protocols = row.get("protocol_paths") or []
        assert protocols, row
        for rel in protocols:
            path = METHODS_ROOT / rel
            assert path.is_file(), rel
