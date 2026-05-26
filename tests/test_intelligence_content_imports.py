"""Verify intelligence_content shards import without merge_part_modules seeding."""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

_SHARDS = [
    "_01_part",
    "_02_part",
    "_03_part",
    "_04_part",
    "_04b_part",
    "_05_part",
    "_06_part",
    "_07_risk_categories",
    "_07_safe_titles",
    "_07_part",
    "_08_part",
    "_09_part",
    "_12_concept_routes_domains",
    "_12_concept_routes_b",
    "_12_concept_routes",
    "_12_topic_frames",
    "_10_part",
    "_11_part",
]


def _isolated_import_script(shard: str) -> str:
    return f"""
import importlib
import sys
sys.path.insert(0, {str(PROJECT_ROOT / "src")!r})
for name in list(sys.modules):
    if name == "intelligence_content" or name.startswith("intelligence_content."):
        del sys.modules[name]
importlib.import_module("intelligence_content.{shard}")
print("ok")
"""


def test_intelligence_content_shards_import_in_isolation() -> None:
    failures: list[str] = []
    for shard in _SHARDS:
        result = subprocess.run(
            [sys.executable, "-c", _isolated_import_script(shard)],
            cwd=PROJECT_ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )
        if result.returncode != 0:
            failures.append(f"{shard}: {result.stderr.strip() or result.stdout.strip()}")
    assert failures == []


def test_intelligence_content_package_imports_without_merge() -> None:
    for name in list(sys.modules):
        if name == "intelligence_content" or name.startswith("intelligence_content."):
            del sys.modules[name]
    module = importlib.import_module("intelligence_content")
    assert hasattr(module, "profile_for_titles")
    assert hasattr(module, "safe_curriculum_treatment")
    assert hasattr(module, "safe_pattern_treatment")
