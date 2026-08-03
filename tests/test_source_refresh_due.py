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
    write_source_refresh_due,
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


def test_source_refresh_due_due_bucket_at_cadence_boundary(tmp_path: Path) -> None:
    """A check exactly one cadence old lands in the ``due`` bucket."""
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
            "checked_as_of": "2025-06-14",
            "refresh_cadence": "annual",
            "citation_role": "curriculum_anchor",
        },
    )

    # checked 2025-06-14, as-of 2026-06-15 => 366 days >= 365 cadence => due.
    report = collect_source_refresh_due(tmp_path, as_of=date(2026, 6, 15))

    row = report.payload["issue_rows"][0]
    assert row["bucket"] == "due"
    assert "refresh_due" in row["flags"]
    assert row["due_date"] == "2026-06-14"


def test_source_refresh_due_future_checked_date_is_unknown(tmp_path: Path) -> None:
    """A checked date in the future is flagged unknown rather than current."""
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
            "checked_as_of": "2027-01-01",
            "refresh_cadence": "annual",
            "citation_role": "curriculum_anchor",
        },
    )

    report = collect_source_refresh_due(tmp_path, as_of=date(2026, 6, 15))

    row = report.payload["rows"][0]
    assert row["bucket"] == "unknown"
    assert "future_checked_as_of" in row["flags"]
    assert row["days_since_check"] is None or row["days_since_check"] < 0


def test_write_source_refresh_due_writes_json_and_markdown(tmp_path: Path) -> None:
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
            "refresh_cadence": "monthly",
            "citation_role": "curriculum_anchor",
        },
    )

    json_path, md_path, report = write_source_refresh_due(tmp_path)

    assert json_path.name == "source_refresh_due.json"
    assert md_path.name == "source_refresh_due.md"
    assert json_path.is_file()
    assert md_path.is_file()
    saved = json.loads(json_path.read_text(encoding="utf-8"))
    assert saved["ok"] == report.ok
    assert saved["summary"]["due_or_stale_count"] >= 1
    # Rendered markdown should include the blocking row table header.
    assert "## Blocking Rows" in md_path.read_text(encoding="utf-8")


def test_render_source_refresh_due_markdown_escapes_pipes_in_cells(tmp_path: Path) -> None:
    """Blocking-row cells with pipes/newlines are flattened so the table stays valid."""
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
            "refresh_cadence": "monthly",
            "citation_role": "curriculum_anchor",
            "path": "data/research_anchors/intelligence-anchors-001-050.jsonl",
        },
    )

    report = collect_source_refresh_due(tmp_path, as_of=date(2026, 6, 15))
    markdown = render_source_refresh_due_markdown(report)

    assert "## Blocking Rows" in markdown
    # Table should contain one real data row (the stale anchor), not "None".
    assert "| None | 0 | - | - | - | - | - |" not in markdown
    # Every blocking-row data row must render exactly 7 cells (8 pipes).
    blocking_lines = markdown.split("## Blocking Rows", 1)[1].splitlines()
    data_rows = [line for line in blocking_lines if line.startswith("|") and "-|-" not in line]
    assert data_rows, "expected at least one data row in the blocking table"
    for line in data_rows:
        assert line.count("|") == 8, line

