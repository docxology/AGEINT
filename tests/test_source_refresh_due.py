"""Tests for AGEINT source-refresh due-date readiness."""

from __future__ import annotations

from datetime import date
import json
import subprocess
import sys
from pathlib import Path

from source_refresh_due import (
    collect_source_refresh_due,
    render_source_refresh_due_markdown,
    source_refresh_due_figure_rows,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _write_anchor(path: Path, payload: dict[str, object]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload) + "\n", encoding="utf-8")


def test_source_refresh_due_current_rows_are_not_due() -> None:
    report = collect_source_refresh_due(PROJECT_ROOT, as_of=date(2026, 6, 16))
    summary = report.payload["summary"]

    assert report.ok is True
    assert summary["row_count"] == 472
    assert summary["due_or_stale_count"] == 0
    assert summary["missing_checked_as_of_count"] == 0
    assert summary["unknown_cadence_count"] == 0
    assert report.payload["issue_row_count"] == 0
    assert summary["cadence_counts"]["annual"] > 0
    assert summary["cadence_counts"]["semiannual"] > 0

    markdown = render_source_refresh_due_markdown(report)
    assert "Source Refresh Due-Date Readiness" in markdown
    assert "Blocking rows" in markdown
    assert "None" in markdown


def test_source_refresh_due_flags_stale_anchor_negative_control(tmp_path: Path) -> None:
    _write_anchor(
        tmp_path / "data" / "research_anchors" / "intelligence-anchors-001-050.jsonl",
        {
            "key": "official_fixture",
            "title": "Fixture",
            "author": "Fixture",
            "year": "2026",
            "url": "https://example.com",
            "domain": "analytic_tradecraft",
            "source_type": "official_primary",
            "source_lane": "analytic_tradecraft",
            "source_tier": "official_primary",
            "checked_as_of": "2024-01-01",
            "refresh_cadence": "annual",
            "citation_role": "curriculum_anchor",
        },
    )

    report = collect_source_refresh_due(tmp_path, as_of=date(2026, 6, 14))

    assert report.ok is False
    assert report.payload["summary"]["due_or_stale_count"] == 1
    assert report.payload["issue_rows"][0]["bucket"] == "stale"
    assert "refresh_stale" in report.payload["issue_rows"][0]["flags"]


def test_source_refresh_due_flags_unknown_or_missing_metadata(tmp_path: Path) -> None:
    _write_anchor(
        tmp_path / "data" / "research_anchors" / "intelligence-anchors-001-050.jsonl",
        {
            "key": "official_fixture",
            "title": "Fixture",
            "author": "Fixture",
            "year": "2026",
            "url": "https://example.com",
            "domain": "analytic_tradecraft",
            "source_type": "official_primary",
            "source_lane": "analytic_tradecraft",
            "source_tier": "official_primary",
            "checked_as_of": "",
            "refresh_cadence": "whenever",
            "citation_role": "curriculum_anchor",
        },
    )

    report = collect_source_refresh_due(tmp_path, as_of=date(2026, 6, 14))

    assert report.ok is False
    assert report.payload["summary"]["missing_checked_as_of_count"] == 1
    assert report.payload["summary"]["unknown_cadence_count"] == 1
    assert report.payload["issue_rows"][0]["flags"] == [
        "missing_or_invalid_checked_as_of",
        "unknown_refresh_cadence",
    ]


def test_source_refresh_due_figure_rows_expose_release_preflight_gate() -> None:
    rows = source_refresh_due_figure_rows(PROJECT_ROOT)
    flat = " ".join(cell for _, cells in rows for cell in cells)

    assert "source_refresh_due_ok" in flat
    assert "dates are not auto-updated" in flat
    assert "source rows" in flat


def test_audit_source_refresh_due_script_writes_json_contract() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "audit_source_refresh_due.py"),
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
    assert payload["summary"]["row_count"] == 472
    assert payload["summary"]["due_or_stale_count"] == 0
    assert (PROJECT_ROOT / "output" / "reports" / "source_refresh_due.json").is_file()
    assert (PROJECT_ROOT / "output" / "reports" / "source_refresh_due.md").is_file()
