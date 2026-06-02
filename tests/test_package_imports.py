"""Verify sharded packages import without merge_part_modules seeding."""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _isolated_import(module: str) -> None:
    script = f"""
import importlib
import sys
sys.path.insert(0, {str(PROJECT_ROOT / "src")!r})
for name in list(sys.modules):
    if name == {module.split(".")[0]!r} or name.startswith({module.split(".")[0] + "."!r}):
        del sys.modules[name]
importlib.import_module({module!r})
print("ok")
"""
    result = subprocess.run(
        [sys.executable, "-c", script],
        cwd=PROJECT_ROOT,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr.strip() or result.stdout.strip()


def test_manuscript_manifest_imports_without_merge() -> None:
    _isolated_import("manuscript_manifest")


def test_figures_imports_without_merge() -> None:
    _isolated_import("figures")


def test_manuscript_variables_imports_without_merge() -> None:
    _isolated_import("manuscript_variables")


def test_package_loader_module_removed() -> None:
    for name in list(sys.modules):
        if name == "_package_loader":
            del sys.modules[name]
    with __import__("pytest").raises(ModuleNotFoundError):
        importlib.import_module("_package_loader")
