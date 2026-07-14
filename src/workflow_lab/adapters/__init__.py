"""Optional backend adapters exposed by the workflow kit.

Codex annotation: Created by Codex on 2026-07-15.
"""

from .discovery import search
from .document_parse import parse
from .evidence_qa import ask
from .literature_map import analyze
from .prose_lint import lint
from .research_synthesis import synthesize

__all__ = ["analyze", "ask", "lint", "parse", "search", "synthesize"]

