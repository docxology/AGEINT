#!/usr/bin/env python3
"""Audit generated AGEINT Markdown heading reference support."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from _paths import ensure_project_paths  # noqa: E402

ensure_project_paths(PROJECT_ROOT)

from rendered_heading_support import (  # noqa: E402
    heading_support_inventory,
    heading_support_json,
    heading_support_summary,
    render_heading_support_markdown,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manuscript-dir",
        type=Path,
        default=PROJECT_ROOT / "output" / "manuscript",
        help="Generated manuscript directory to audit.",
    )
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.format == "json":
        print(heading_support_json(args.manuscript_dir))
    else:
        print(render_heading_support_markdown(args.manuscript_dir))
    summary = heading_support_summary(heading_support_inventory(args.manuscript_dir))
    return 0 if summary.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
