#!/usr/bin/env python3
"""Count AGEINT source-section and generated manuscript citations."""

from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from _paths import ensure_project_paths  # noqa: E402

ensure_project_paths(PROJECT_ROOT)

from citation_workflow import (  # noqa: E402
    generated_markdown_citation_inventory,
    render_citation_workflow_markdown,
    source_citation_coverage_summary,
)
from curriculum import load_curriculum  # noqa: E402


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--format",
        choices=("markdown", "json"),
        default="markdown",
        help="Output format for citation counts.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    curriculum = load_curriculum(PROJECT_ROOT / "data" / "curriculum")
    summary = source_citation_coverage_summary(curriculum)
    generated_rows = generated_markdown_citation_inventory(PROJECT_ROOT / "output" / "manuscript")
    generated_by_family = Counter()
    for row in generated_rows:
        generated_by_family[row.family] += row.citation_count

    if args.format == "json":
        print(
            json.dumps(
                {
                    "source_sections": summary.section_count,
                    "source_citation_occurrences": summary.citation_occurrences,
                    "source_unique_citation_keys": summary.unique_citation_keys,
                    "source_zero_citation_sections": summary.zero_citation_sections,
                    "source_distribution": dict(summary.citation_count_distribution),
                    "generated_markdown_files": len(generated_rows),
                    "generated_markdown_citation_occurrences": sum(
                        row.citation_count for row in generated_rows
                    ),
                    "generated_by_family": dict(sorted(generated_by_family.items())),
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 0

    print(render_citation_workflow_markdown(curriculum))
    print("\n## Generated Markdown Citation Counts\n")
    print("| Section family | Citation occurrences |")
    print("|---|---:|")
    for family, count in sorted(generated_by_family.items()):
        print(f"| {family} | {count} |")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
