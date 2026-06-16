#!/usr/bin/env python3
"""Write and report AGEINT source-refresh due-date readiness."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from _paths import ensure_project_paths  # noqa: E402

ensure_project_paths(PROJECT_ROOT)

from source_refresh_due import (  # noqa: E402
    collect_source_refresh_due,
    render_source_refresh_due_markdown,
    write_source_refresh_due,
)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format.",
    )
    parser.add_argument(
        "--write",
        action="store_true",
        help="Write output/reports/source_refresh_due.{json,md}.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.write:
        json_path, md_path, report = write_source_refresh_due(PROJECT_ROOT)
    else:
        json_path = md_path = None
        report = collect_source_refresh_due(PROJECT_ROOT)
    if args.format == "json":
        import json

        print(json.dumps(report.payload, indent=2, sort_keys=True))
    else:
        print(render_source_refresh_due_markdown(report), end="")
    if args.write and json_path and md_path:
        print(
            f"Wrote {json_path.relative_to(PROJECT_ROOT)} and {md_path.relative_to(PROJECT_ROOT)}",
            file=sys.stderr,
        )
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
