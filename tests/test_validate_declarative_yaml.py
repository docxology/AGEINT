"""Smoke tests for declarative YAML validation script."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "scripts" / "validate_declarative_yaml.py"


def test_validate_declarative_yaml_script_exits_zero() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    assert result.returncode == 0, result.stderr or result.stdout
    assert "Declarative YAML validation passed." in result.stdout
