"""Small command-line entrypoint for checking the installed workflow kit."""

import argparse
from typing import Sequence


VERSION = "0.1.0"


def build_parser() -> argparse.ArgumentParser:
    """Build the dependency-free command-line parser."""
    parser = argparse.ArgumentParser(prog="workflow-lab")
    parser.add_argument("--version", action="version", version=VERSION)
    parser.add_argument(
        "command",
        nargs="?",
        choices=("check",),
        help="run a dependency-free installation check",
    )
    return parser


def main(argv: Sequence[str] | None = None) -> int:
    """Parse arguments and report the dependency-free installation state."""
    parser = build_parser()
    parser.parse_args(argv)
    print("workflow-lab core is installed; optional backends are configured separately.")
    return 0

