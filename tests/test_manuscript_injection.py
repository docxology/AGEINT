"""Standalone substitution and real SDK import/execution failure boundaries."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest

SOURCE_DIR = Path(__file__).resolve().parents[1] / "src"


def _substitute_in_child(tmp_path: Path, sdk_body: str | None = None) -> dict[str, object]:
    if sdk_body is not None:
        package = tmp_path / "infrastructure" / "rendering"
        package.mkdir(parents=True)
        (package.parent / "__init__.py").write_text("", encoding="utf-8")
        (package / "__init__.py").write_text("", encoding="utf-8")
        (package / "manuscript_injection.py").write_text(sdk_body, encoding="utf-8")
    script = """import json, sys
sys.path[:0] = sys.argv[1:]
from manuscript_injection import substitute_manuscript_text
try:
    result = substitute_manuscript_text('{{TITLE}} / {{UNKNOWN}} / {{TITLE}}', {'TITLE': 17})
except Exception as error:
    print(json.dumps({'error_type': type(error).__name__, 'name': getattr(error, 'name', None)}))
else:
    print(json.dumps({'result': result}))
"""
    # -I -S excludes inherited SDK paths and site packages in this owned fixture.
    result = subprocess.run([sys.executable, "-I", "-S", "-c", script, str(tmp_path), str(SOURCE_DIR)], cwd=tmp_path, check=True, capture_output=True, text=True, timeout=15)
    return json.loads(result.stdout)


def test_standalone_substitution_preserves_unresolved_tokens(tmp_path: Path) -> None:
    assert _substitute_in_child(tmp_path) == {"result": ["17 / {{UNKNOWN}} / 17", ["UNKNOWN"]]}


@pytest.mark.parametrize("error_type", ["ImportError", "ModuleNotFoundError"])
def test_sdk_body_import_failures_do_not_become_fallback_text(tmp_path: Path, error_type: str) -> None:
    body = f"def substitute_manuscript_text(template, context):\n    raise {error_type}('provider failure')\n"
    assert _substitute_in_child(tmp_path, body) == {"error_type": error_type, "name": None}


def test_sdk_import_failure_does_not_become_fallback_text(tmp_path: Path) -> None:
    assert _substitute_in_child(tmp_path, "raise ImportError('provider import failure')\n") == {"error_type": "ImportError", "name": None}


def test_missing_sdk_dependency_does_not_become_fallback_text(tmp_path: Path) -> None:
    dependency = "ageint_missing_sdk_fixture_dependency"
    assert _substitute_in_child(tmp_path, f"import {dependency}\n") == {"error_type": "ModuleNotFoundError", "name": dependency}
