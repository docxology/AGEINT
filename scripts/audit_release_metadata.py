#!/usr/bin/env python3
"""Check AGEINT source release metadata without writing or publishing."""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from _paths import ensure_project_paths  # noqa: E402

ensure_project_paths(PROJECT_ROOT)

from release_metadata import collect_release_metadata, render_release_metadata_markdown  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--format", choices=("json", "markdown"), default="markdown", help="Output format.")
    parser.add_argument("--expected-tag", help="Require exactly vX.Y.Z for the canonical package version.")
    args = parser.parse_args(argv)
    report = collect_release_metadata(PROJECT_ROOT, expected_tag=args.expected_tag)
    if args.format == "json":
        print(json.dumps(report.payload, indent=2, sort_keys=True))
    else:
        print(render_release_metadata_markdown(report), end="")
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
