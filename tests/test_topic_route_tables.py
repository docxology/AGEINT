"""Tests for the canonical topic route tables in ``src/topic_route_tables.py``.

The thin ``scripts/generate_topic_*_yaml.py`` orchestrators emit these tables to
the committed declarative files under ``data/``; these tests fail if the
canonical tables drift from what the runtime loader reads.
"""

from __future__ import annotations

from pathlib import Path

import yaml

from topic_route_tables import (
    topic_prompt_routes_payload,
    topic_rotation_templates_payload,
    write_topic_prompt_routes_yaml,
    write_topic_rotation_templates_yaml,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_topic_prompt_routes_payload_matches_committed_yaml() -> None:
    committed = yaml.safe_load((PROJECT_ROOT / "data" / "topic_prompt_routes.yaml").read_text(encoding="utf-8"))
    assert committed == topic_prompt_routes_payload()


def test_topic_rotation_templates_payload_matches_committed_yaml() -> None:
    committed = yaml.safe_load((PROJECT_ROOT / "data" / "topic_rotation_templates.yaml").read_text(encoding="utf-8"))
    assert committed == topic_rotation_templates_payload()


def test_write_helpers_are_idempotent(tmp_path: Path) -> None:
    first = write_topic_prompt_routes_yaml(tmp_path)
    second = write_topic_rotation_templates_yaml(tmp_path)
    assert first == tmp_path / "data" / "topic_prompt_routes.yaml"
    assert second == tmp_path / "data" / "topic_rotation_templates.yaml"
    assert first.read_text(encoding="utf-8") == write_topic_prompt_routes_yaml(tmp_path).read_text(encoding="utf-8")
    assert second.read_text(encoding="utf-8") == write_topic_rotation_templates_yaml(tmp_path).read_text(encoding="utf-8")
    assert yaml.safe_load(first.read_text(encoding="utf-8")) == topic_prompt_routes_payload()
    assert yaml.safe_load(second.read_text(encoding="utf-8")) == topic_rotation_templates_payload()
