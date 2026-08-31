"""Schema-version gate: generated artifacts fail their readers on a schema bump."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from schema_gate import (
    EXPECTED_SCHEMA_VERSIONS,
    SchemaVersionError,
    expected_schema_version,
    load_json_with_schema,
    require_schema_version,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT_ROOT = PROJECT_ROOT / "output"


def test_expected_map_covers_registry_and_quality_audit() -> None:
    assert EXPECTED_SCHEMA_VERSIONS["figures/figure_registry.json"] == "1.5"
    assert EXPECTED_SCHEMA_VERSIONS["figures/visual_quality_audit.json"] == "1.0"
    assert EXPECTED_SCHEMA_VERSIONS["reports/source_metadata.json"] == "1.0"


def test_committed_registry_loads_through_the_gate() -> None:
    payload = load_json_with_schema(
        OUTPUT_ROOT / "figures" / "figure_registry.json", output_root=OUTPUT_ROOT
    )
    assert payload["schema_version"] == "1.5"
    assert payload["figure_count"] == len(payload["figures"])


def test_missing_schema_version_is_rejected(tmp_path: Path) -> None:
    artifact = tmp_path / "figures" / "figure_registry.json"
    artifact.parent.mkdir()
    artifact.write_text(json.dumps({"figures": []}), encoding="utf-8")
    with pytest.raises(SchemaVersionError, match="schema_version"):
        load_json_with_schema(artifact, output_root=tmp_path)


def test_bumped_schema_version_is_rejected(tmp_path: Path) -> None:
    artifact = tmp_path / "figures" / "visual_quality_audit.json"
    artifact.parent.mkdir()
    artifact.write_text(json.dumps({"schema_version": "2.0"}), encoding="utf-8")
    with pytest.raises(SchemaVersionError, match="bump the consumer"):
        load_json_with_schema(artifact, output_root=tmp_path)


def test_non_object_payload_is_rejected(tmp_path: Path) -> None:
    artifact = tmp_path / "figures" / "figure_registry.json"
    artifact.parent.mkdir()
    artifact.write_text("[]", encoding="utf-8")
    with pytest.raises(SchemaVersionError, match="JSON object"):
        load_json_with_schema(artifact, output_root=tmp_path)


def test_require_schema_version_accepts_matching_value() -> None:
    require_schema_version({"schema_version": "1.0"}, "1.0", artifact="x.json")


def test_paths_outside_output_root_are_ungated(tmp_path: Path) -> None:
    outsider = tmp_path / "elsewhere" / "figure_registry.json"
    outsider.parent.mkdir()
    outsider.write_text("[]", encoding="utf-8")
    assert expected_schema_version(outsider, output_root=tmp_path) is None
    assert load_json_with_schema(outsider, output_root=tmp_path) == []
