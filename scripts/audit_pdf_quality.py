#!/usr/bin/env python3
"""Audit the rendered AGEINT PDF for stale output and banned phrases."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from _paths import ensure_project_paths  # noqa: E402

ensure_project_paths(PROJECT_ROOT)

from pdf_quality import audit_pdf_quality, render_pdf_quality_markdown, report_json  # noqa: E402


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--pdf",
        type=Path,
        default=PROJECT_ROOT / "output" / "pdf" / "AGEINT_combined.pdf",
        help="Path to the rendered PDF.",
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
    report = audit_pdf_quality(
        args.pdf,
        manuscript_dir=PROJECT_ROOT / "output" / "manuscript",
    )
    if args.format == "json":
        print(report_json(report))
    else:
        print(render_pdf_quality_markdown(report))
    return 0 if report.ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
