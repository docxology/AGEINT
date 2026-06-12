"""Pytest configuration for AGEINT curriculum tests."""

from __future__ import annotations

import os
from pathlib import Path

os.environ.setdefault("MPLBACKEND", "Agg")

PROJECT_ROOT = Path(__file__).resolve().parents[1]

import sys

sys.path.insert(0, str(PROJECT_ROOT / "src"))
sys.path.insert(0, str(PROJECT_ROOT / "tests"))

from _paths import ensure_project_paths  # noqa: E402

ensure_project_paths(PROJECT_ROOT)

from template_resolver import ensure_template_repo_on_path  # noqa: E402

TEMPLATE_REPO = ensure_template_repo_on_path(PROJECT_ROOT)

import pytest  # noqa: E402

from build_pipeline import generated_output_is_stale, run_build, run_build_figures  # noqa: E402


@pytest.fixture(scope="session")
def built_output() -> Path:
    """Ensure generated output exists for integration tests (cold run may take several minutes)."""
    output = PROJECT_ROOT / "output"
    needs_build = (
        not (output / "manuscript").exists()
        or not (output / "figures" / "figure_registry.json").is_file()
        or generated_output_is_stale(PROJECT_ROOT, output)
    )
    if needs_build:
        run_build(PROJECT_ROOT)
    return output
