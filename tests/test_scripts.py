"""Smoke tests for thin AGEINT script entrypoints."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_setup_hook_writes_output_docs() -> None:
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "setup_hook.py")],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert (PROJECT_ROOT / "output" / "README.md").is_file()


def test_generate_figures_script_runs() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "generate_figures.py"),
            "--allow-placeholder-figures",
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Rendered" in result.stdout


def test_z_generate_manuscript_variables_prints_path() -> None:
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "z_generate_manuscript_variables.py")],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0
    assert result.stdout.strip().endswith("manuscript_variables.json")
