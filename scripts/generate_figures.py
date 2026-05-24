#!/usr/bin/env python3
"""Render AGEINT figure assets and registry."""

from __future__ import annotations

import os
from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from _paths import ensure_project_paths  # noqa: E402

ensure_project_paths(PROJECT_ROOT)

from template_resolver import ensure_template_repo_on_path  # noqa: E402

ensure_template_repo_on_path(PROJECT_ROOT)

try:
    from infrastructure.core.logging.utils import get_logger
except ImportError:
    import logging

    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)

from curriculum import load_curriculum  # noqa: E402
from figures import load_figure_registry, render_figures  # noqa: E402
from manuscript_manifest import build_manuscript_manifest  # noqa: E402

logger = get_logger(__name__)


def main() -> int:
    import argparse

    default_placeholder = os.environ.get("AGEINT_REQUIRE_RENDERED_FIGURES", "") != "1"
    parser = argparse.ArgumentParser(description="Render AGEINT figure assets and registry")
    parser.add_argument(
        "--allow-placeholder-figures",
        action=argparse.BooleanOptionalAction,
        default=default_placeholder,
        help=(
            "Allow deterministic text-plate fallbacks when Mermaid/Chrome is unavailable "
            "(default: on unless AGEINT_REQUIRE_RENDERED_FIGURES=1)"
        ),
    )
    args = parser.parse_args()

    registry_path = PROJECT_ROOT / "output" / "figures" / "figure_registry.json"
    if registry_path.is_file() and not args.allow_placeholder_figures:
        logger.info("Existing figure registry at %s; re-rendering figures", registry_path)

    curriculum = load_curriculum(PROJECT_ROOT / "data" / "curriculum")
    manifest = build_manuscript_manifest(curriculum)
    registry_path = render_figures(
        PROJECT_ROOT,
        curriculum,
        manifest,
        allow_placeholder_figures=args.allow_placeholder_figures,
    )
    registry = load_figure_registry(registry_path)
    message = f"Rendered {registry['figure_count']} AGEINT figures to {registry_path}"
    logger.info(message)
    print(message)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
