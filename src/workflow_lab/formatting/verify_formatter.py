#!/usr/bin/env python
"""Run an offline smoke test for the local Markdown-to-Word formatter."""

from __future__ import annotations

import sys
import tempfile
from pathlib import Path

FORMATTER_DIR = Path(__file__).resolve().parent
sys.path.insert(0, str(FORMATTER_DIR))

from formatter import MarkdownToWordConverter


def run_verification() -> int:
    """Compile the sanitized sample into a temporary Word document offline."""
    input_md = FORMATTER_DIR / "sample_draft.md"
    if not input_md.exists():
        print(f"Error: sample draft was not found: {input_md}")
        return 1

    with tempfile.TemporaryDirectory(prefix="workflow-lab-format-") as temp_dir:
        output_docx = Path(temp_dir) / "sample_output.docx"
        print("=== GB/T 7714-2015 Formatter Offline Verification ===")
        print(f"Input Markdown: {input_md}")
        print(f"Temporary Word document: {output_docx}")
        try:
            converter = MarkdownToWordConverter(output_docx)
            converter.convert_file(input_md, refine_citations=False)
        except Exception as exc:
            print(f"[FAILURE] Conversion failed: {exc}")
            return 1
        if not output_docx.exists() or output_docx.stat().st_size <= 0:
            print("[FAILURE] Formatter produced an empty document.")
            return 1
        print(f"[SUCCESS] Offline document compiled ({output_docx.stat().st_size} bytes).")
        return 0


if __name__ == "__main__":
    raise SystemExit(run_verification())
