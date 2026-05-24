#!/usr/bin/env python3
"""Thin orchestrator: refresh AGEINT manuscript variables and output manuscript."""

from __future__ import annotations

from pathlib import Path
import sys

_PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(_PROJECT_ROOT / "src"))

from _paths import ensure_project_paths  # noqa: E402

ensure_project_paths(_PROJECT_ROOT)

from build_pipeline import run_build  # noqa: E402
from template_resolver import ensure_template_repo_on_path  # noqa: E402

ensure_template_repo_on_path(_PROJECT_ROOT)

try:
    from infrastructure.core.logging.utils import get_logger
except ImportError:
    import logging

    def get_logger(name: str) -> logging.Logger:
        return logging.getLogger(name)

logger = get_logger(__name__)


def main() -> int:
    logger.info("Refreshing AGEINT manuscript variables via full build")
    result = run_build(_PROJECT_ROOT, regenerate_source_template_library=False)
    logger.info("Wrote variables to %s", result.variables_path)
    print(str(result.variables_path))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
