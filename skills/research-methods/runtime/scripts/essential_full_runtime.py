#!/usr/bin/env python3
"""Essential Core deterministic planner / full runtime entry.

Grok annotation: First-party rewrite by Grok on 2026-07-20 (E1).
Grok annotation: Alias matrix + ambiguity/reproducibility fixes by Grok on 2026-07-20 (E0/E1 revision 1).
Grok annotation: V2-1 ambiguous mode context + V2-2 reset ledger transition by Grok on 2026-07-20 (revision 2).
stdlib only. No network. No secret logging.

essential_core_lineage:
  file: runtime/scripts/essential_full_runtime.py
  implementation: first-party-rewrite
  upstream_concepts:
    - codex full runtime planner
    - mode routing
    - passport validation
  upstream_path_hints:
    - skills/research-methods/codex/scripts/ars_codex_full_runtime.py
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
RUNTIME_DIR = SCRIPT_DIR.parent
METHODS_ROOT = RUNTIME_DIR.parent
MANIFEST_PATH = RUNTIME_DIR / "full-runtime-manifest.json"

EXIT_OK = 0
EXIT_FAIL = 1
EXIT_USAGE = 2
EXIT_STATE = 3
EXIT_IO = 4
EXIT_INTERNAL = 5

SUPPORTED_SCHEMA = "essential_passport_v1"

LEGAL_TRANSITIONS = {
    (None, "1"),
    ("1", "2"),
    ("2", "2.5"),
    ("2.5", "3"),
    ("2.5", "2"),
    ("3", "4"),
    ("3", "3p"),
    ("3p", "4"),
    ("4", "4.5"),
    ("4", "3p"),
    ("4p", "4.5"),
    ("4p", "3p"),
    ("4.5", "5"),
    ("4.5", "4"),
    ("5", "FULL"),
}

WORKFLOW_PATHS = {
    "deep-research": {
        "agent_template": "runtime/agents/deep-research-team.md",
        "role_card": "core/teams/deep_research_roles.md",
        "protocol_paths": [
            "core/protocols/deep_research.md",
            "core/protocols/research_question.md",
        ],
        "template_paths": [
            "core/templates/research_question_brief.md",
            "core/templates/evidence_assessment.md",
            "core/templates/literature_matrix.md",
        ],
        "quality_gates": ["evidence_state_vocab", "vague_topic_socratic"],
    },
    "academic-paper": {
        "agent_template": "runtime/agents/academic-paper-team.md",
        "role_card": "core/teams/academic_paper_roles.md",
        "protocol_paths": ["core/protocols/academic_paper.md"],
        "template_paths": [
            "core/templates/argument_map.md",
            "core/templates/revision_roadmap.md",
            "core/templates/disclosure_statement.md",
            "core/templates/rebuttal_audit.md",
        ],
        "quality_gates": ["generator_evaluator_separation", "mode_registry_coverage"],
    },
    "academic-paper-reviewer": {
        "agent_template": "runtime/agents/paper-reviewer-panel.md",
        "role_card": "core/teams/reviewer_panel_roles.md",
        "protocol_paths": ["core/protocols/manuscript_review.md"],
        "template_paths": [
            "core/templates/manuscript_review_full.md",
            "core/templates/editorial_decision.md",
            "core/templates/revision_roadmap.md",
        ],
        "quality_gates": ["reviewer_independence"],
    },
    "academic-pipeline": {
        "agent_template": "runtime/agents/academic-pipeline-orchestrator.md",
        "role_card": "core/teams/pipeline_roles.md",
        "protocol_paths": ["core/protocols/academic_pipeline.md"],
        "template_paths": [
            "core/templates/pipeline_status.md",
            "core/templates/material_passport.md",
        ],
        "quality_gates": ["passport_reset_contract"],
    },
    "experiment": {
        "agent_template": "runtime/agents/experiment-team.md",
        "role_card": "core/teams/experiment_roles.md",
        "protocol_paths": ["core/protocols/experiment.md"],
        "template_paths": [
            "core/templates/study_protocol.md",
            "core/templates/code_experiment_plan.md",
            "core/templates/reproducibility_checklist.md",
            "core/templates/statistical_validation.md",
        ],
        "quality_gates": ["optional_runtime_honesty", "stats_fallacies_11"],
    },
}

MODE_OVERRIDES = {
    "systematic-review": {
        "protocol_paths": [
            "core/protocols/systematic_review.md",
            "core/protocols/deep_research.md",
        ],
        "template_paths": [
            "core/templates/prisma_protocol.md",
            "core/templates/prisma_report_skeleton.md",
            "core/templates/literature_matrix.md",
        ],
        "quality_gates": [
            "prisma_fields",
            "rob2_fields",
            "grade_fields",
            "anti_pooling_fields",
        ],
    },
    "socratic": {
        "protocol_paths": [
            "core/protocols/research_question.md",
            "core/protocols/deep_research.md",
        ],
        "template_paths": ["core/templates/research_question_brief.md"],
        "quality_gates": ["vague_topic_socratic", "evidence_state_vocab"],
    },
    "citation-check": {
        "protocol_paths": [
            "core/protocols/citation_integrity.md",
            "core/protocols/academic_paper.md",
        ],
        "template_paths": [
            "core/templates/citation_integrity_audit.md",
            "core/templates/claim_verification_report.md",
        ],
        "quality_gates": ["claim_verdict_vocab"],
    },
    "lit-review": {
        "protocol_paths": [
            "core/protocols/deep_research.md",
            "core/protocols/academic_paper.md",
        ],
        "template_paths": ["core/templates/literature_matrix.md"],
        "quality_gates": ["evidence_state_vocab"],
    },
    "fact-check": {
        "protocol_paths": [
            "core/protocols/deep_research.md",
            "core/protocols/citation_integrity.md",
        ],
        "template_paths": [
            "core/templates/claim_verification_report.md",
            "core/templates/evidence_assessment.md",
        ],
        "quality_gates": ["claim_verdict_vocab"],
    },
    "rebuttal-audit": {
        "protocol_paths": ["core/protocols/academic_paper.md"],
        "template_paths": ["core/templates/rebuttal_audit.md"],
        "quality_gates": ["generator_evaluator_separation"],
    },
}


def _truthy(value: str | None) -> bool:
    if value is None:
        return False
    return value.strip().lower() in {"1", "true", "yes", "on"}


def env_flag(canonical: str, alias: str) -> bool:
    """Return True if either canonical or alias env flag is truthy.

    Canonical wins if both are set and conflict.
    """
    can_raw = os.environ.get(canonical)
    alias_raw = os.environ.get(alias)
    can_set = can_raw is not None and can_raw != ""
    alias_set = alias_raw is not None and alias_raw != ""
    if can_set and alias_set:
        return _truthy(can_raw)
    if can_set:
        return _truthy(can_raw)
    if alias_set:
        return _truthy(alias_raw)
    return False


def load_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.is_file():
        raise FileNotFoundError(str(MANIFEST_PATH))
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def list_supported_aliases(manifest: dict[str, Any]) -> list[str]:
    aliases = manifest.get("aliases") or {}
    return sorted(str(k) for k in aliases.keys())


def runtime_block() -> dict[str, Any]:
    full_runtime = env_flag("RM_FULL_RUNTIME", "ARS_CODEX_FULL_RUNTIME")
    agent_team = env_flag("RM_AGENT_TEAM", "ARS_CODEX_AGENT_TEAM")
    hooks = env_flag("RM_HOOKS", "ARS_CODEX_HOOKS")
    missing: list[str] = []
    # Honesty: discovery/fulltext backends are optional and not present by default.
    for name, var in (
        ("proposal-research", "WORKFLOW_LAB_DISCOVERY_CMD"),
        ("document-parser", "WORKFLOW_LAB_DOCUMENT_CMD"),
        ("evidence-qa", "WORKFLOW_LAB_EVIDENCE_CMD"),
        ("openalex", "OPENALEX_API_KEY"),
    ):
        if not os.environ.get(var):
            missing.append(name)
    degraded = "missing_backend" if missing else None
    return {
        "full_runtime": full_runtime,
        "agent_team": agent_team,
        "hooks": hooks,
        "degraded": degraded,
        "missing_backends": missing,
        "honesty": "continue_offline" if missing else "backends_optional",
    }


def emit(obj: dict[str, Any], as_json: bool) -> None:
    if as_json:
        sys.stdout.write(json.dumps(obj, ensure_ascii=False, indent=2) + "\n")
    else:
        sys.stdout.write(json.dumps(obj, ensure_ascii=False) + "\n")


def error_plan(
    error: str,
    message: str,
    supported: list[str] | None = None,
) -> dict[str, Any]:
    return {
        "ok": False,
        "error": error,
        "message": message,
        "supported_aliases": supported or [],
        "workflow": None,
        "mode": None,
    }


def success_plan(
    workflow: str,
    mode: str,
    route_reason: str,
    command_alias: str | None,
    passport_info: dict[str, Any] | None = None,
) -> dict[str, Any]:
    base = dict(WORKFLOW_PATHS[workflow])
    if mode in MODE_OVERRIDES:
        override = MODE_OVERRIDES[mode]
        for key in ("protocol_paths", "template_paths", "quality_gates"):
            if key in override:
                base[key] = list(override[key])
    if mode == "systematic-review":
        # systematic-review is a deep-research mode
        pass
    gates = list(base["quality_gates"])
    if env_flag("RM_CLAIM_AUDIT", "ARS_CLAIM_AUDIT"):
        if "generator_evaluator_separation" not in gates:
            gates.append("generator_evaluator_separation")
        gates.append("claim_verdict_vocab")
    rt = runtime_block()
    if not rt["agent_team"]:
        # attach template paths still; degraded inline note
        if rt.get("degraded") is None:
            rt["degraded"] = "inline_agent"
    return {
        "ok": True,
        "workflow": workflow,
        "mode": mode,
        "command_alias": command_alias,
        "route_reason": route_reason,
        "agent_template": base["agent_template"],
        "role_card": base["role_card"],
        "protocol_paths": list(base["protocol_paths"]),
        "template_paths": list(base["template_paths"]),
        "quality_gates": gates,
        "runtime": rt,
        "passport": passport_info
        or {"resume": False, "reset_boundary": False, "checkpoint_hash": None},
        "error": None,
    }


def looks_like_alias(token: str) -> bool:
    return bool(re.fullmatch(r"(ars|rm)-[a-z0-9-]+", token.strip().lower()))


def extract_explicit_mode(text: str) -> str | None:
    match = re.search(r"mode\s*[:=]\s*([a-z0-9-]+)", text, flags=re.I)
    if match:
        return match.group(1).lower()
    return None


def is_vague_paper_topic(text: str) -> bool:
    lowered = text.lower().strip()
    if not lowered:
        return False
    paper_signals = (
        "write a paper",
        "write paper",
        "want to write a paper",
        "paper about",
        "paper on",
        "draft a paper",
        "i want to write",
    )
    if not any(sig in lowered for sig in paper_signals):
        return False
    # Clear RQ signals reduce vagueness
    rq_signals = (
        "research question",
        "pico",
        "peco",
        "hypothesis",
        "we ask whether",
        "does ",
        "what is the effect",
        "among ",
    )
    if any(sig in lowered for sig in rq_signals):
        return False
    # Very short topic after "about/on" counts as vague
    return True


def heuristic_route(text: str) -> tuple[str, str, str]:
    lowered = text.lower()
    # Order matters: more specific signals (reproducibility/validate) before generic experiment.
    rules: list[tuple[tuple[str, ...], str, str]] = [
        (("systematic review", "meta-analysis", "prisma"), "deep-research", "systematic-review"),
        (("peer review", "reviewer panel", "manuscript review"), "academic-paper-reviewer", "full"),
        (("passport", "pipeline", "resume stage"), "academic-pipeline", "pipeline"),
        (
            (
                "reproducibility",
                "reproduce",
                "statistical interpretation",
                "validate experiment",
                "validate reproducibility",
            ),
            "experiment",
            "validate",
        ),
        (("experiment", "preregistration", "study protocol"), "experiment", "plan"),
        (("rebuttal audit", "rebuttal-audit"), "academic-paper", "rebuttal-audit"),
        (("disclosure",), "academic-paper", "disclosure"),
        (("revision coach", "revision-coach"), "academic-paper", "revision-coach"),
        (("fact check", "fact-check", "claim verification"), "deep-research", "fact-check"),
        (("three-way", "why/how/what", "ars-3w"), "deep-research", "three-way-scan"),
        (("outline",), "academic-paper", "outline-only"),
        (("abstract",), "academic-paper", "abstract-only"),
        (("citation check", "citation-check"), "academic-paper", "citation-check"),
        (("lit review", "literature review"), "deep-research", "lit-review"),
        (("socratic",), "deep-research", "socratic"),
        (("write a paper", "draft paper", "paper plan"), "academic-paper", "plan"),
    ]
    for signals, workflow, mode in rules:
        if any(sig in lowered for sig in signals):
            return workflow, mode, "heuristic"
    return "deep-research", "socratic", "heuristic"


# Modes that appear under more than one workflow. Explicit mode alone is ambiguous.
# Candidate workflows come from full-runtime-manifest.json mode rows.
AMBIGUOUS_MODE_CANDIDATES: dict[str, tuple[str, ...]] = {
    "full": ("deep-research", "academic-paper", "academic-paper-reviewer"),
    "quick": ("deep-research", "academic-paper-reviewer"),
    "lit-review": ("deep-research", "academic-paper"),
    "plan": ("academic-paper", "experiment"),
}

# Bare tokens (no useful context) use documented safe defaults. For full/quick the
# default may replace the mode so bare mode:full never silent-drafts.
AMBIGUOUS_BARE_DEFAULTS: dict[str, tuple[str, str, str]] = {
    "full": ("deep-research", "socratic", "ambiguous_mode_default"),
    "quick": ("deep-research", "socratic", "ambiguous_mode_default"),
    "lit-review": ("deep-research", "lit-review", "ambiguous_mode_default"),
    "plan": ("academic-paper", "plan", "ambiguous_mode_default"),
}

# Back-compat alias used by older tests/docs.
AMBIGUOUS_MODES = AMBIGUOUS_BARE_DEFAULTS

RESET_LEDGER_REQUIRED_FIELDS = (
    "reset_id",
    "timestamp",
    "from_stage",
    "to_stage",
    "from_checkpoint_hash",
    "reason",
    "actor",
    "env_flags_observed",
)
RESET_LEDGER_ACTORS = frozenset({"human", "agent"})


def resolve_alias(alias: str, manifest: dict[str, Any]) -> tuple[str, str] | None:
    aliases = manifest.get("aliases") or {}
    entry = aliases.get(alias)
    if not isinstance(entry, dict):
        # try case-insensitive
        for key, value in aliases.items():
            if str(key).lower() == alias.lower() and isinstance(value, dict):
                entry = value
                break
    if not isinstance(entry, dict):
        return None
    workflow = str(entry.get("workflow", ""))
    mode = str(entry.get("mode", ""))
    if workflow not in WORKFLOW_PATHS:
        return None
    return workflow, mode


def mode_to_workflow(mode: str) -> str | None:
    """Map unambiguous mode ids to a workflow. Ambiguous modes return None."""
    if mode in AMBIGUOUS_MODE_CANDIDATES:
        return None
    mapping = {
        "review": "deep-research",
        "three-way-scan": "deep-research",
        "fact-check": "deep-research",
        "socratic": "deep-research",
        "systematic-review": "deep-research",
        "outline-only": "academic-paper",
        "revision": "academic-paper",
        "revision-coach": "academic-paper",
        "abstract-only": "academic-paper",
        "format-convert": "academic-paper",
        "citation-check": "academic-paper",
        "disclosure": "academic-paper",
        "rebuttal-audit": "academic-paper",
        "re-review": "academic-paper-reviewer",
        "methodology-focus": "academic-paper-reviewer",
        "guided": "academic-paper-reviewer",
        "calibration": "academic-paper-reviewer",
        "pipeline": "academic-pipeline",
        "resume_from_passport": "academic-pipeline",
        "mark-read": "academic-pipeline",
        "unmark-read": "academic-pipeline",
        "cache-invalidate": "academic-pipeline",
        "run": "experiment",
        "manage": "experiment",
        "validate": "experiment",
        "study-protocol": "experiment",
        "code-experiment": "experiment",
        "statistical-interpretation": "experiment",
        "reproducibility": "experiment",
    }
    return mapping.get(mode)


def pick_workflow_from_context(text: str, candidates: tuple[str, ...] | list[str]) -> str | None:
    """Pick a workflow among candidates using free-text context only.

    Does not select a mode. Returns None when no candidate signal matches.
    """
    if not candidates:
        return None
    lowered = text.lower()
    candidate_set = set(candidates)
    # Ordered from specific to broad so peer-review wins over bare "paper".
    signal_rules: list[tuple[tuple[str, ...], str]] = [
        (
            ("peer review", "reviewer panel", "manuscript review", "reviewer"),
            "academic-paper-reviewer",
        ),
        (
            (
                "experiment",
                "preregistration",
                "study protocol",
                "reproducibility",
                "statistical interpretation",
            ),
            "experiment",
        ),
        (("passport", "pipeline", "resume stage"), "academic-pipeline"),
        (
            ("systematic review", "meta-analysis", "prisma", "deep research"),
            "deep-research",
        ),
        (
            (
                "academic paper",
                "write a paper",
                "draft paper",
                "paper plan",
                "outline",
                "manuscript",
            ),
            "academic-paper",
        ),
        (("paper",), "academic-paper"),
        (("research", "literature"), "deep-research"),
    ]
    for signals, workflow in signal_rules:
        if workflow not in candidate_set:
            continue
        if any(sig in lowered for sig in signals):
            return workflow
    return None


def resolve_ambiguous_explicit_mode(mode: str, text: str) -> tuple[str, str, str]:
    """Disambiguate duplicated modes by workflow context; keep requested mode.

    Bare tokens with no useful remainder use documented safe defaults (which may
    replace full/quick with socratic so bare mode:full never silent-drafts).
    When context selects a candidate workflow, the explicit mode is retained.
    """
    candidates = AMBIGUOUS_MODE_CANDIDATES.get(mode)
    if not candidates:
        bare = AMBIGUOUS_BARE_DEFAULTS.get(mode)
        if bare is None:
            return "deep-research", "socratic", "ambiguous_mode_default"
        return bare

    remainder = re.sub(r"mode\s*[:=]\s*[a-z0-9-]+", "", text, flags=re.I).strip()
    if not remainder or not re.search(r"[a-z]{3,}", remainder, flags=re.I):
        return AMBIGUOUS_BARE_DEFAULTS[mode]

    workflow = pick_workflow_from_context(remainder, candidates)
    if workflow is None:
        return AMBIGUOUS_BARE_DEFAULTS[mode]
    # Keep the explicitly requested mode; context only chose the workflow.
    return workflow, mode, "explicit_mode_disambiguated"


def checkpoint_hash(
    passport_id: str,
    stage_id: str,
    global_state: str,
    artifact_paths: list[str],
    integrity_summary: str,
    updated_at_iso: str,
) -> str:
    payload = "|".join(
        [
            passport_id,
            stage_id,
            global_state,
            ",".join(sorted(artifact_paths)),
            integrity_summary,
            updated_at_iso,
        ]
    )
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def _ledger_entry_snapshot(entry: Any) -> Any:
    """Return a JSON-stable deep copy snapshot for equality without mutation."""
    return json.loads(json.dumps(entry, sort_keys=True))


def validate_reset_ledger_entry(entry: Any) -> dict[str, Any]:
    """Validate one reset-ledger entry for required fields and actor enum."""
    if not isinstance(entry, dict):
        return {
            "ok": False,
            "error": "invalid_reset_entry",
            "message": "reset ledger entry must be an object",
        }
    missing = [f for f in RESET_LEDGER_REQUIRED_FIELDS if f not in entry]
    if missing:
        return {
            "ok": False,
            "error": "invalid_reset_entry",
            "message": f"missing required fields: {missing}",
        }
    actor = entry.get("actor")
    if actor not in RESET_LEDGER_ACTORS:
        return {
            "ok": False,
            "error": "invalid_reset_actor",
            "message": f"actor must be one of {sorted(RESET_LEDGER_ACTORS)}, got {actor!r}",
        }
    flags = entry.get("env_flags_observed")
    if not isinstance(flags, list):
        return {
            "ok": False,
            "error": "invalid_reset_entry",
            "message": "env_flags_observed must be a list",
        }
    for field in ("reset_id", "timestamp", "from_stage", "to_stage", "from_checkpoint_hash", "reason"):
        if entry.get(field) in (None, ""):
            return {
                "ok": False,
                "error": "invalid_reset_entry",
                "message": f"{field} must be non-empty",
            }
    return {"ok": True, "error": None, "message": "ok"}


def validate_reset_ledger_transition(
    previous_ledger: Any,
    new_ledger: Any,
) -> dict[str, Any]:
    """Validate append-only reset-ledger transition against a previous ledger.

    Accepts exactly one valid append. Rejects deletion, reordering, mutation of
    historical rows, multiple appends, missing required fields, and invalid
    actors. Does not mutate either input.
    """
    if not isinstance(previous_ledger, list):
        return {
            "ok": False,
            "error": "invalid_reset_ledger",
            "message": "previous_ledger must be a list",
        }
    if not isinstance(new_ledger, list):
        return {
            "ok": False,
            "error": "invalid_reset_ledger",
            "message": "new_ledger must be a list",
        }

    prev_snap = [_ledger_entry_snapshot(e) for e in previous_ledger]
    new_snap = [_ledger_entry_snapshot(e) for e in new_ledger]

    if len(new_snap) < len(prev_snap):
        return {
            "ok": False,
            "error": "reset_ledger_delete",
            "message": "reset_ledger must not delete historical entries",
        }
    if len(new_snap) == len(prev_snap):
        if new_snap != prev_snap:
            return {
                "ok": False,
                "error": "reset_ledger_mutation",
                "message": "reset_ledger historical entries must not be mutated or reordered",
            }
        return {
            "ok": False,
            "error": "reset_ledger_no_append",
            "message": "reset transition requires exactly one new ledger entry",
        }
    if len(new_snap) > len(prev_snap) + 1:
        return {
            "ok": False,
            "error": "reset_ledger_multi_append",
            "message": "reset_ledger may append at most one entry per transition",
        }

    # Exactly one append: historical prefix must match previous order and content.
    if new_snap[: len(prev_snap)] != prev_snap:
        # Distinguish reorder/mutation of history from an insert-not-at-end.
        if sorted(
            json.dumps(e, sort_keys=True) for e in new_snap[: len(prev_snap)]
        ) == sorted(json.dumps(e, sort_keys=True) for e in prev_snap):
            return {
                "ok": False,
                "error": "reset_ledger_reorder",
                "message": "reset_ledger historical entries must not be reordered",
            }
        return {
            "ok": False,
            "error": "reset_ledger_mutation",
            "message": "reset_ledger historical entries must not be mutated",
        }

    entry_check = validate_reset_ledger_entry(new_ledger[-1])
    if not entry_check["ok"]:
        return entry_check

    return {
        "ok": True,
        "error": None,
        "message": "append-only reset ledger transition ok",
    }


def validate_passport_obj(
    passport: dict[str, Any],
    from_stage: str | None = None,
    to_stage: str | None = None,
    previous_reset_ledger: list[Any] | None = None,
) -> dict[str, Any]:
    schema = passport.get("schema_id")
    if schema != SUPPORTED_SCHEMA:
        return {
            "ok": False,
            "error": "unknown_schema",
            "checkpoint_hash_expected": None,
            "message": f"schema_id must be {SUPPORTED_SCHEMA}",
        }

    # Always enforce resume checkpoint match when a hash is presented.
    resume = passport.get("resume") or {}
    last = passport.get("last_checkpoint") or {}
    if isinstance(resume, dict) and resume.get("checkpoint_hash"):
        expected = last.get("hash")
        if expected and resume.get("checkpoint_hash") != expected:
            return {
                "ok": False,
                "error": "missing_checkpoint",
                "checkpoint_hash_expected": expected,
                "message": "checkpoint hash mismatch",
            }
        if resume.get("checkpoint_hash") and not expected:
            return {
                "ok": False,
                "error": "missing_checkpoint",
                "checkpoint_hash_expected": None,
                "message": "resume checkpoint hash present but last_checkpoint.hash missing",
            }

    # Reset requires flag + append-only ledger list, independent of transition args.
    if passport.get("reset_requested"):
        if not env_flag("RM_PASSPORT_RESET", "ARS_PASSPORT_RESET"):
            return {
                "ok": False,
                "error": "reset_requires_flag",
                "checkpoint_hash_expected": None,
                "message": "RM_PASSPORT_RESET or ARS_PASSPORT_RESET required",
            }
        ledger = passport.get("reset_ledger")
        if not isinstance(ledger, list):
            return {
                "ok": False,
                "error": "reset_requires_flag",
                "checkpoint_hash_expected": None,
                "message": "reset_ledger must be a list",
            }
        if previous_reset_ledger is not None:
            ledger_result = validate_reset_ledger_transition(previous_reset_ledger, ledger)
            if not ledger_result["ok"]:
                return {
                    "ok": False,
                    "error": ledger_result.get("error") or "invalid_reset_ledger",
                    "checkpoint_hash_expected": None,
                    "message": ledger_result.get("message") or "reset ledger transition failed",
                }
        else:
            # Without a previous ledger, still validate any present entries.
            for entry in ledger:
                entry_check = validate_reset_ledger_entry(entry)
                if not entry_check["ok"]:
                    return {
                        "ok": False,
                        "error": entry_check.get("error") or "invalid_reset_entry",
                        "checkpoint_hash_expected": None,
                        "message": entry_check.get("message") or "invalid reset entry",
                    }

    if from_stage is None and to_stage is None:
        return {"ok": True, "error": None, "checkpoint_hash_expected": None, "message": "schema_ok"}

    fr = from_stage if from_stage not in (None, "null", "") else None
    to = to_stage
    if (fr, to) not in LEGAL_TRANSITIONS and not (fr == to and fr is not None):
        if not (fr == to and fr is not None):
            return {
                "ok": False,
                "error": "illegal_transition",
                "checkpoint_hash_expected": None,
                "message": f"illegal transition {fr!r} -> {to!r}",
            }
    return {"ok": True, "error": None, "checkpoint_hash_expected": None, "message": "ok"}


def plan_from_inputs(
    text: str,
    alias: str | None,
    passport_path: str | None,
    manifest: dict[str, Any],
) -> tuple[dict[str, Any], int]:
    supported = list_supported_aliases(manifest)
    passport_info = {"resume": False, "reset_boundary": False, "checkpoint_hash": None}
    if passport_path:
        path = Path(passport_path)
        if not path.is_file():
            return error_plan("missing_input", f"passport not found: {passport_path}", supported), EXIT_IO
        try:
            passport = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            return error_plan("invalid_json", f"passport JSON invalid: {exc}", supported), EXIT_USAGE
        if not isinstance(passport, dict):
            return error_plan("invalid_json", "passport must be an object", supported), EXIT_USAGE
        result = validate_passport_obj(passport)
        if not result["ok"]:
            code = EXIT_STATE if result["error"] in {"unknown_schema", "illegal_transition", "missing_checkpoint", "reset_requires_flag"} else EXIT_USAGE
            return error_plan(str(result["error"]), str(result.get("message") or result["error"]), supported), code
        passport_info = {
            "resume": True,
            "reset_boundary": bool(passport.get("reset_requested")),
            "checkpoint_hash": (passport.get("last_checkpoint") or {}).get("hash"),
        }

    alias_token = (alias or "").strip()
    if not alias_token:
        # detect leading alias-like token in text
        first = (text.strip().split() or [""])[0]
        if looks_like_alias(first):
            alias_token = first.lower()
            text = text.strip()[len(first) :].strip()

    if alias_token:
        normalized = alias_token.lower()
        if looks_like_alias(normalized):
            resolved = resolve_alias(normalized, manifest)
            if resolved is None:
                return (
                    error_plan(
                        "unsupported_alias",
                        f"unsupported alias: {normalized}",
                        supported,
                    ),
                    EXIT_USAGE,
                )
            workflow, mode = resolved
            plan = success_plan(workflow, mode, "alias", normalized, passport_info)
            return plan, EXIT_OK
        # non-pattern alias strings fall through as free text contribution
        text = f"{alias_token} {text}".strip()

    explicit = extract_explicit_mode(text)
    if explicit:
        if explicit in AMBIGUOUS_MODE_CANDIDATES:
            # Context disambiguates workflow only; keep requested mode when resolved.
            # Bare tokens use documented safe defaults (may replace full/quick).
            workflow, mode, reason = resolve_ambiguous_explicit_mode(explicit, text)
            plan = success_plan(workflow, mode, reason, None, passport_info)
            return plan, EXIT_OK
        workflow = mode_to_workflow(explicit)
        if workflow is None:
            workflow, mode, _ = heuristic_route(text)
            plan = success_plan(workflow, mode, "explicit_mode", None, passport_info)
            return plan, EXIT_OK
        mode = explicit
        if explicit in {"study-protocol"}:
            mode = "plan"
        elif explicit in {"code-experiment"}:
            mode = "run"
        elif explicit in {"statistical-interpretation", "reproducibility"}:
            mode = "validate"
        plan = success_plan(workflow, mode, "explicit_mode", None, passport_info)
        return plan, EXIT_OK

    if is_vague_paper_topic(text):
        plan = success_plan(
            "deep-research",
            "socratic",
            "paper_topic_scoping_override",
            None,
            passport_info,
        )
        return plan, EXIT_OK

    if passport_info.get("resume"):
        plan = success_plan(
            "academic-pipeline",
            "resume_from_passport",
            "resume",
            None,
            passport_info,
        )
        return plan, EXIT_OK

    workflow, mode, reason = heuristic_route(text)
    plan = success_plan(workflow, mode, reason, None, passport_info)
    return plan, EXIT_OK


def cmd_list_aliases(as_json: bool) -> int:
    try:
        manifest = load_manifest()
    except FileNotFoundError as exc:
        emit(error_plan("missing_input", str(exc)), as_json)
        return EXIT_IO
    aliases = list_supported_aliases(manifest)
    emit({"ok": True, "supported_aliases": aliases, "count": len(aliases)}, as_json)
    return EXIT_OK


def cmd_plan(args: argparse.Namespace) -> int:
    try:
        manifest = load_manifest()
    except FileNotFoundError as exc:
        emit(error_plan("missing_input", str(exc)), True if args.json else args.json)
        return EXIT_IO

    text = args.text or ""
    alias = args.alias
    passport_path = args.passport
    if args.request:
        req_path = Path(args.request)
        if not req_path.is_file():
            emit(error_plan("missing_input", f"request not found: {args.request}"), args.json)
            return EXIT_IO
        try:
            req = json.loads(req_path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            emit(error_plan("invalid_json", str(exc)), args.json)
            return EXIT_USAGE
        if not isinstance(req, dict):
            emit(error_plan("invalid_json", "request must be an object"), args.json)
            return EXIT_USAGE
        text = str(req.get("text") or text)
        alias = req.get("alias", alias)
        passport_path = req.get("passport_path", passport_path)

    if not text and not alias and not passport_path:
        emit(error_plan("missing_input", "provide --text and/or --alias"), args.json)
        return EXIT_USAGE

    plan, code = plan_from_inputs(text, alias, passport_path, manifest)
    emit(plan, args.json)
    return code


def cmd_validate_passport(args: argparse.Namespace) -> int:
    path = Path(args.passport)
    if not path.is_file():
        emit(error_plan("missing_input", f"passport not found: {args.passport}"), args.json)
        return EXIT_IO
    try:
        passport = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        emit(error_plan("invalid_json", str(exc)), args.json)
        return EXIT_USAGE
    if not isinstance(passport, dict):
        emit(error_plan("invalid_json", "passport must be an object"), args.json)
        return EXIT_USAGE
    result = validate_passport_obj(
        passport,
        from_stage=args.from_stage,
        to_stage=args.to_stage,
    )
    emit(
        {
            "ok": bool(result["ok"]),
            "error": result.get("error"),
            "message": result.get("message"),
            "checkpoint_hash_expected": result.get("checkpoint_hash_expected"),
            "supported_aliases": [],
            "workflow": None,
            "mode": None,
        },
        args.json,
    )
    if result["ok"]:
        return EXIT_OK
    if result.get("error") in {
        "unknown_schema",
        "illegal_transition",
        "missing_checkpoint",
        "reset_requires_flag",
    }:
        return EXIT_STATE
    return EXIT_USAGE


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Essential Core full runtime planner")
    sub = parser.add_subparsers(dest="command", required=True)

    p_list = sub.add_parser("list-aliases", help="List supported ars-*/rm-* aliases")
    p_list.add_argument("--json", action="store_true")

    p_plan = sub.add_parser("plan", help="Emit deterministic route plan")
    p_plan.add_argument("--text", default="")
    p_plan.add_argument("--alias", default=None)
    p_plan.add_argument("--passport", default=None)
    p_plan.add_argument("--request", default=None)
    p_plan.add_argument("--json", action="store_true")

    p_val = sub.add_parser("validate-passport", help="Validate passport schema/transition")
    p_val.add_argument("--passport", required=True)
    p_val.add_argument("--from-stage", default=None)
    p_val.add_argument("--to-stage", default=None)
    p_val.add_argument("--json", action="store_true")

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    try:
        args = parser.parse_args(argv)
        if args.command == "list-aliases":
            return cmd_list_aliases(args.json)
        if args.command == "plan":
            return cmd_plan(args)
        if args.command == "validate-passport":
            return cmd_validate_passport(args)
        return EXIT_USAGE
    except BrokenPipeError:
        return EXIT_OK
    except Exception as exc:  # noqa: BLE001 — top-level CLI guard
        emit(
            {
                "ok": False,
                "error": "internal_error",
                "message": str(exc),
                "supported_aliases": [],
                "workflow": None,
                "mode": None,
            },
            True,
        )
        return EXIT_INTERNAL


if __name__ == "__main__":
    raise SystemExit(main())
