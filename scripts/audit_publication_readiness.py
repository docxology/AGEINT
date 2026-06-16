#!/usr/bin/env python3
"""Write and report AGEINT publication-readiness preflight evidence."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from _paths import ensure_project_paths  # noqa: E402

ensure_project_paths(PROJECT_ROOT)

from publication_readiness import (  # noqa: E402
    collect_publication_readiness,
    render_publication_readiness_markdown,
    write_publication_readiness,
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
        help="Write output/reports/publication_readiness.{json,md}.",
    )
    parser.add_argument(
        "--skip-parent-guard",
        action="store_true",
        help="Do not run the parent template tracked-project confidentiality guard.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.write:
        json_path, md_path, report = write_publication_readiness(
            PROJECT_ROOT,
            run_parent_guard=not args.skip_parent_guard,
        )
    else:
        json_path = md_path = None
        report = collect_publication_readiness(
            PROJECT_ROOT,
            run_parent_guard=not args.skip_parent_guard,
        )
    if args.format == "json":
        import json

        print(json.dumps(report.payload, indent=2, sort_keys=True))
    else:
        print(render_publication_readiness_markdown(report), end="")
    if args.write and json_path and md_path:
        print(
            f"Wrote {json_path.relative_to(PROJECT_ROOT)} and {md_path.relative_to(PROJECT_ROOT)}",
            file=sys.stderr,
        )
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
