#!/usr/bin/env python3
"""Build AGEINT data, variables, and the resolved semantic manuscript."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from _paths import ensure_project_paths  # noqa: E402

ensure_project_paths(PROJECT_ROOT)

from build_pipeline import run_build  # noqa: E402
from template_resolver import ensure_template_repo_on_path  # noqa: E402

ensure_template_repo_on_path(PROJECT_ROOT)

try:
    from infrastructure.core.logging.utils import get_logger
except ImportError:
    import logging

    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)

logger = get_logger(__name__)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--regenerate-source-template-library",
        "--regenerate-source-templates",
        action="store_true",
        dest="regenerate_source_template_library",
        help="Rewrite manuscript/templates/*.md from the built-in neutral template library.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    logger.info("Starting AGEINT curriculum build")
    result = run_build(
        PROJECT_ROOT,
        regenerate_source_template_library=args.regenerate_source_template_library,
    )
    stats = result.curriculum.stats
    summary = (
        "Built AGEINT curriculum: "
        f"{stats['parts']} parts, {stats['chapters']} modules, "
        f"{stats['appendices']} appendices, {stats['patterns']} AGEINT patterns, "
        f"{stats['references']} references; "
        f"rewrote {result.written_source_templates} neutral source templates; "
        f"rendered figures {result.figure_registry_path}; "
        f"rendered {result.output_manuscript}"
    )
    print(summary)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
