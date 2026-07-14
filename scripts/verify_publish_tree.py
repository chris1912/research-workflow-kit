"""Check that a publish candidate contains no local-only artifacts.

Codex annotation: Created by Codex on 2026-07-15.
"""

from pathlib import Path
import re
import sys


DENY_NAMES = {".git", ".venv", "node_modules", "__pycache__", ".pytest_cache"}
DENY_SUFFIXES = {".pyc", ".pyo", ".exe", ".zip", ".docx", ".pdf", ".pptx"}
PRIVATE_MARKERS = ("D:\\AIAgent\\", "C:\\Users\\")
SECRET_ASSIGNMENT = re.compile(
    r"(?i)\b(?:OPENAI_API_KEY|TAVILY_API_KEY)\s*=\s*['\"]?"
    r"(?!<|sk-your|your[-_])[A-Za-z0-9_./:+=-]+"
)


def iter_files(root: Path) -> list[Path]:
    """Return regular files below a candidate root in stable order."""
    return sorted(path for path in root.rglob("*") if path.is_file())


def scan_tree(root: Path) -> list[str]:
    """Collect deny-list, secret, and absolute-path findings."""
    findings: list[str] = []
    for path in iter_files(root):
        relative = path.relative_to(root)
        if any(part in DENY_NAMES for part in relative.parts):
            findings.append(f"forbidden directory: {relative}")
        if path.suffix.lower() in DENY_SUFFIXES:
            findings.append(f"forbidden file type: {relative}")
        if path.suffix.lower() in {".md", ".html", ".json", ".jsonl", ".toml", ".yml", ".yaml", ".py", ".ps1"}:
            text = path.read_text(encoding="utf-8", errors="ignore")
            if relative.as_posix() == "scripts/verify_publish_tree.py":
                text_for_secret_scan = ""
            else:
                text_for_secret_scan = text
            if SECRET_ASSIGNMENT.search(text_for_secret_scan):
                findings.append(f"credential assignment: {relative}")
            for marker in PRIVATE_MARKERS:
                if marker in text and "THIRD_PARTY" not in path.name:
                    findings.append(f"private marker {marker}: {relative}")
    return findings


def main() -> int:
    """Run the publish-tree scan and return a process exit code."""
    root = Path(__file__).resolve().parents[1]
    findings = scan_tree(root)
    if findings:
        for finding in findings:
            print(finding, file=sys.stderr)
        return 1
    print(f"publish tree clean: {root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
