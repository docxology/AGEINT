"""Tests for AGEINT source metadata coverage."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from source_metadata import (
    SOURCE_METADATA_BASELINE,
    collect_source_metadata,
    render_source_metadata_markdown,
    source_metadata_figure_rows,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_source_metadata_current_rows_are_explicit() -> None:
    report = collect_source_metadata(PROJECT_ROOT)
    summary = report.payload["summary"]

    assert report.ok is True
    assert summary["metadata_records"] == 472
    assert summary["intelligence_anchor_count"] == 462
    assert summary["source_quality_anchor_count"] == 10
    assert summary["blank_source_lane_count"] == 0
    assert summary["blank_source_tier_count"] == 0
    assert summary["fallback_dependent_row_count"] == 0
    assert summary["source_quality_semantic_issue_count"] == 0
    assert report.payload["baseline_closed"] == SOURCE_METADATA_BASELINE
    assert SOURCE_METADATA_BASELINE["total_blank_rows_closed"] == 119

    markdown = render_source_metadata_markdown(report)
    assert "Total blank rows closed" in markdown
    assert "Source-quality support anchors" in markdown
    assert "Fallback-dependent rows" in markdown


def test_source_metadata_flags_blank_lane_or_tier_negative_control(tmp_path: Path) -> None:
    data_dir = tmp_path / "data" / "research_anchors"
    data_dir.mkdir(parents=True)
    row = {
        "key": "official_fixture",
        "title": "Fixture",
        "author": "Fixture",
        "year": "2026",
        "url": "https://example.com",
        "note": "Fixture.",
        "domain": "analytic_tradecraft",
        "source_type": "official_primary",
        "checked_as_of": "2026-06-13",
        "citation_role": "curriculum_anchor",
        "source_lane": "",
        "source_tier": "",
        "refresh_cadence": "annual",
    }
    (data_dir / "intelligence-anchors-001-050.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")

    report = collect_source_metadata(tmp_path)

    assert report.ok is False
    assert report.payload["summary"]["blank_source_lane_count"] == 1
    assert report.payload["summary"]["blank_source_tier_count"] == 1
    assert report.payload["summary"]["fallback_dependent_row_count"] == 1
    assert report.payload["issue_rows"][0]["flags"] == ["blank_source_lane", "blank_source_tier"]


def test_source_metadata_flags_source_quality_semantic_mismatch(tmp_path: Path) -> None:
    data_dir = tmp_path / "data" / "research_anchors"
    data_dir.mkdir(parents=True)
    row = {
        "key": "official_support_fixture",
        "title": "Fixture",
        "author": "Fixture",
        "year": "2026",
        "url": "https://example.com",
        "note": "Fixture.",
        "checked_as_of": "2026-06-13",
        "citation_role": "source_quality_anchor",
        "source_lane": "analytic_tradecraft",
        "source_tier": "official_primary",
        "refresh_cadence": "annual",
    }
    (data_dir / "source-quality-anchors.jsonl").write_text(json.dumps(row) + "\n", encoding="utf-8")

    report = collect_source_metadata(tmp_path)

    assert report.ok is False
    assert report.payload["summary"]["source_quality_semantic_issue_count"] == 1
    assert report.payload["issue_rows"][0]["flags"] == [
        "source_quality_lane_mismatch",
        "source_quality_tier_mismatch",
    ]


def test_source_metadata_figure_rows_expose_manifest_gate() -> None:
    rows = source_metadata_figure_rows(PROJECT_ROOT)
    flat = " ".join(cell for _, cells in rows for cell in cells)

    assert "source_metadata_ok" in flat
    assert "119 legacy blanks closed" not in flat
    assert "109 legacy blanks closed" in flat
    assert "10 rows" in flat


def test_audit_source_metadata_script_writes_json_contract() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "audit_source_metadata.py"),
            "--format",
            "json",
            "--write",
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["summary"]["fallback_dependent_row_count"] == 0
    assert payload["summary"]["source_quality_anchor_count"] == 10
    assert payload["summary"]["intelligence_anchor_count"] == 462
    assert (PROJECT_ROOT / "output" / "reports" / "source_metadata.json").is_file()
    assert (PROJECT_ROOT / "output" / "reports" / "source_metadata.md").is_file()
