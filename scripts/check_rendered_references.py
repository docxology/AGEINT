#!/usr/bin/env python3
"""Audit rendered AGEINT text for hard-coded section references."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from _paths import ensure_project_paths  # noqa: E402

ensure_project_paths(PROJECT_ROOT)

from rendered_reference_audit import audit_rendered_references  # noqa: E402


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "output_root",
        nargs="?",
        default=str(PROJECT_ROOT / "output"),
        help="Rendered output root to scan; defaults to AGEINT/output.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    output_root = Path(args.output_root).resolve()
    violations = audit_rendered_references(output_root)
    if violations:
        for violation in violations:
            print(violation.format(PROJECT_ROOT), file=sys.stderr)
        print(f"Rendered reference audit failed: {len(violations)} violation(s).", file=sys.stderr)
        return 1
    print(f"Rendered reference audit passed: {output_root}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
