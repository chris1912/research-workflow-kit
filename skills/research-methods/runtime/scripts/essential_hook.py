#!/usr/bin/env python3
"""Essential Core read-only hook announce wrapper.

Grok annotation: First-party rewrite by Grok on 2026-07-20 (E1).
stdlib only. No network. No secret echo. No mutation.

essential_core_lineage:
  file: runtime/scripts/essential_hook.py
  implementation: first-party-rewrite
  upstream_concepts:
    - codex hook wrapper
    - read-only announce
  upstream_path_hints:
    - skills/research-methods/codex/scripts/ars_codex_hook.py
  copy_policy: no-wholesale-copy
  license_note: see NOTICE.md and docs/licenses/academic-research-skills-license.txt
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from typing import Any

EXIT_OK = 0
EXIT_USAGE = 2
EXIT_INTERNAL = 5

SECRET_PATTERNS = [
    re.compile(r"(?i)api[_-]?key"),
    re.compile(r"(?i)secret"),
    re.compile(r"(?i)token"),
    re.compile(r"(?i)password"),
    re.compile(r"(?i)authorization"),
    re.compile(r"sk-[A-Za-z0-9]{10,}"),
    re.compile(r"(?i)bearer\s+[A-Za-z0-9._\-]+"),
]


def scrub(value: str) -> str:
    cleaned = value
    for pattern in SECRET_PATTERNS:
        cleaned = pattern.sub("[redacted]", cleaned)
    return cleaned


def safe_str(value: Any, max_len: int = 200) -> str:
    if value is None:
        return ""
    text = scrub(str(value))
    if len(text) > max_len:
        return text[:max_len] + "…"
    return text


def parse_stdin_json() -> tuple[dict[str, Any] | None, str | None]:
    raw = sys.stdin.read()
    if not raw.strip():
        return {}, None
    try:
        data = json.loads(raw)
    except json.JSONDecodeError as exc:
        return None, f"malformed JSON: {exc}"
    if not isinstance(data, dict):
        return None, "hook input must be a JSON object"
    return data, None


def announce(event: str, payload: dict[str, Any]) -> dict[str, Any]:
    # Never read or echo process environment secrets.
    workflow = safe_str(payload.get("workflow"))
    mode = safe_str(payload.get("mode"))
    message = safe_str(payload.get("message"), max_len=120)
    return {
        "ok": True,
        "announce": "research-methods essential runtime active",
        "event": safe_str(event or payload.get("event") or "agent-start"),
        "workflow": workflow or None,
        "mode": mode or None,
        "message": message or None,
        "safe": True,
        "boundaries": {
            "network": False,
            "mutate_filesystem": False,
            "echo_secrets": False,
            "read_env_values": False,
        },
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Essential Core read-only hook wrapper")
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("announce", help="Emit a safe announce JSON payload")
    p.add_argument("--event", default=None)
    p.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    if args.command != "announce":
        return EXIT_USAGE

    payload, err = parse_stdin_json()
    if err is not None:
        out = {
            "ok": False,
            "error": "invalid_json",
            "message": err,
            "safe": True,
        }
        sys.stdout.write(json.dumps(out, ensure_ascii=False) + "\n")
        return EXIT_USAGE

    assert payload is not None
    result = announce(args.event or "", payload)
    sys.stdout.write(json.dumps(result, ensure_ascii=False, indent=2 if args.json else None) + "\n")
    return EXIT_OK


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:  # noqa: BLE001
        sys.stdout.write(
            json.dumps(
                {
                    "ok": False,
                    "error": "internal_error",
                    "message": str(exc),
                    "safe": True,
                }
            )
            + "\n"
        )
        raise SystemExit(EXIT_INTERNAL)
