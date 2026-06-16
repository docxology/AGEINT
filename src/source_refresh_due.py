"""Source-refresh due-date audit helpers for AGEINT."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import UTC, date, datetime
import json
from pathlib import Path
from typing import Any

try:
    from .source_metadata import collect_source_metadata
except ImportError:  # pragma: no cover - direct script imports
    from source_metadata import collect_source_metadata  # type: ignore[no-redef]


CADENCE_DAYS: dict[str, int] = {
    "monthly": 31,
    "quarterly": 92,
    "semiannual": 183,
    "annual": 365,
    "biennial": 730,
}
DUE_SOON_DAYS = 30


@dataclass(frozen=True)
class SourceRefreshDueRow:
    """One source-anchor row with computed refresh due-date status."""

    path: str
    line: int
    key: str
    row_class: str
    source_lane: str
    source_tier: str
    refresh_cadence: str
    checked_as_of: str
    due_date: str
    days_since_check: int | None
    days_until_due: int | None
    bucket: str
    flags: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "line": self.line,
            "key": self.key,
            "row_class": self.row_class,
            "source_lane": self.source_lane,
            "source_tier": self.source_tier,
            "refresh_cadence": self.refresh_cadence,
            "checked_as_of": self.checked_as_of,
            "due_date": self.due_date,
            "days_since_check": self.days_since_check,
            "days_until_due": self.days_until_due,
            "bucket": self.bucket,
            "flags": list(self.flags),
        }


@dataclass(frozen=True)
class SourceRefreshDueReport:
    """Source-refresh due-date readiness report."""

    payload: dict[str, Any]

    @property
    def ok(self) -> bool:
        return bool(self.payload["ok"])


def collect_source_refresh_due(project_root: Path, *, as_of: date | None = None) -> SourceRefreshDueReport:
    """Collect refresh-due buckets for all curated and support source anchors."""

    root = Path(project_root)
    as_of_date = as_of or datetime.now(UTC).date()
    metadata = collect_source_metadata(root).payload
    rows = [_row_from_metadata(row, as_of_date) for row in metadata["rows"]]
    issue_rows = [row for row in rows if _is_blocking(row)]
    payload = {
        "project": "AGEINT",
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "as_of": as_of_date.isoformat(),
        "ok": not issue_rows and bool(rows),
        "summary": _summary(rows),
        "issue_row_count": len(issue_rows),
        "issue_rows": [row.as_dict() for row in issue_rows],
        "rows": [row.as_dict() for row in rows],
    }
    return SourceRefreshDueReport(payload)


def write_source_refresh_due(project_root: Path) -> tuple[Path, Path, SourceRefreshDueReport]:
    """Write JSON and Markdown source-refresh due reports under ``output/reports``."""

    root = Path(project_root)
    report = collect_source_refresh_due(root)
    reports_dir = root / "output" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_path = reports_dir / "source_refresh_due.json"
    md_path = reports_dir / "source_refresh_due.md"
    json_path.write_text(json.dumps(report.payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_source_refresh_due_markdown(report), encoding="utf-8")
    return json_path, md_path, report


def render_source_refresh_due_markdown(report: SourceRefreshDueReport) -> str:
    """Render a compact Markdown version of the source-refresh due report."""

    payload = report.payload
    summary = payload["summary"]
    lines = [
        "# AGEINT Source Refresh Due-Date Readiness",
        "",
        "| Measure | Value |",
        "|---|---:|",
        f"| OK | {str(payload['ok']).lower()} |",
        f"| Generated at | {payload['generated_at']} |",
        f"| As of | {payload['as_of']} |",
        f"| Rows | {summary['row_count']} |",
        f"| Current | {summary['bucket_counts'].get('current', 0)} |",
        f"| Due soon | {summary['bucket_counts'].get('due_soon', 0)} |",
        f"| Due | {summary['bucket_counts'].get('due', 0)} |",
        f"| Stale | {summary['bucket_counts'].get('stale', 0)} |",
        f"| Unknown | {summary['bucket_counts'].get('unknown', 0)} |",
        f"| Blocking rows | {payload['issue_row_count']} |",
        "",
        "## Refresh Cadence",
        "",
        "| Cadence | Rows |",
        "|---|---:|",
    ]
    for cadence, count in summary["cadence_counts"].items():
        lines.append(f"| {cadence or 'missing'} | {count} |")
    lines.extend(["", "## Due-Date Buckets", "", "| Bucket | Rows |", "|---|---:|"])
    for bucket, count in summary["bucket_counts"].items():
        lines.append(f"| {bucket} | {count} |")
    lines.extend(
        [
            "",
            "## Blocking Rows",
            "",
            "| Path | Line | Key | Cadence | Checked as of | Bucket | Flags |",
            "|---|---:|---|---|---|---|---|",
        ]
    )
    if payload["issue_rows"]:
        for row in payload["issue_rows"]:
            lines.append(
                f"| {_cell(row['path'])} | {row['line']} | {_cell(row['key'])} | "
                f"{_cell(row['refresh_cadence'])} | {_cell(row['checked_as_of'])} | "
                f"{_cell(row['bucket'])} | {_cell(', '.join(row['flags']))} |"
            )
    else:
        lines.append("| None | 0 | - | - | - | - | - |")
    return "\n".join(lines) + "\n"


def source_refresh_due_figure_rows(project_root: Path) -> tuple[tuple[str, tuple[str, str, str]], ...]:
    """Return compact source-refresh due rows for a registry-backed visual."""

    report = collect_source_refresh_due(project_root).payload
    summary = report["summary"]
    buckets = summary["bucket_counts"]
    cadences = summary["cadence_counts"]
    return (
        (
            "Refresh status",
            (
                f"{buckets.get('current', 0)} current",
                f"{buckets.get('due_soon', 0)} due soon",
                f"{buckets.get('due', 0) + buckets.get('stale', 0)} due/stale",
            ),
        ),
        (
            "Cadence coverage",
            (
                f"{len(cadences)} cadence classes",
                f"{cadences.get('annual', 0)} annual",
                f"{cadences.get('semiannual', 0)} semiannual",
            ),
        ),
        (
            "Metadata readiness",
            (
                f"{summary['row_count']} source rows",
                f"{summary['missing_checked_as_of_count']} missing dates",
                f"{summary['unknown_cadence_count']} unknown cadences",
            ),
        ),
        (
            "Release preflight",
            (
                "source_refresh_due_ok",
                "due/stale fails",
                "dates are not auto-updated",
            ),
        ),
    )


def _row_from_metadata(row: dict[str, Any], as_of: date) -> SourceRefreshDueRow:
    cadence = str(row.get("refresh_cadence") or "")
    checked_raw = str(row.get("checked_as_of") or "")
    flags: list[str] = []
    checked = _parse_date(checked_raw)
    cadence_days = CADENCE_DAYS.get(cadence)
    due_date = ""
    days_since_check: int | None = None
    days_until_due: int | None = None
    bucket = "unknown"
    if checked is None:
        flags.append("missing_or_invalid_checked_as_of")
    if cadence_days is None:
        flags.append("unknown_refresh_cadence")
    if checked is not None and cadence_days is not None:
        days_since_check = (as_of - checked).days
        due = date.fromordinal(checked.toordinal() + cadence_days)
        due_date = due.isoformat()
        days_until_due = (due - as_of).days
        if days_since_check < 0:
            bucket = "unknown"
            flags.append("future_checked_as_of")
        elif days_since_check >= cadence_days * 2:
            bucket = "stale"
            flags.append("refresh_stale")
        elif days_since_check >= cadence_days:
            bucket = "due"
            flags.append("refresh_due")
        elif days_until_due <= DUE_SOON_DAYS:
            bucket = "due_soon"
        else:
            bucket = "current"
    return SourceRefreshDueRow(
        path=str(row.get("path") or ""),
        line=int(row.get("line") or 0),
        key=str(row.get("key") or ""),
        row_class=str(row.get("row_class") or ""),
        source_lane=str(row.get("source_lane") or ""),
        source_tier=str(row.get("source_tier") or ""),
        refresh_cadence=cadence,
        checked_as_of=checked_raw,
        due_date=due_date,
        days_since_check=days_since_check,
        days_until_due=days_until_due,
        bucket=bucket,
        flags=tuple(flags),
    )


def _summary(rows: list[SourceRefreshDueRow]) -> dict[str, Any]:
    flags = Counter(flag for row in rows for flag in row.flags)
    return {
        "row_count": len(rows),
        "bucket_counts": dict(sorted(Counter(row.bucket for row in rows).items())),
        "cadence_counts": dict(sorted(Counter(row.refresh_cadence for row in rows).items())),
        "source_lane_due_counts": dict(
            sorted(Counter(row.source_lane for row in rows if row.bucket in {"due", "stale"}).items())
        ),
        "missing_checked_as_of_count": flags.get("missing_or_invalid_checked_as_of", 0),
        "unknown_cadence_count": flags.get("unknown_refresh_cadence", 0),
        "due_or_stale_count": sum(1 for row in rows if row.bucket in {"due", "stale"}),
        "due_soon_count": sum(1 for row in rows if row.bucket == "due_soon"),
        "flag_counts": dict(sorted(flags.items())),
    }


def _is_blocking(row: SourceRefreshDueRow) -> bool:
    return bool(row.flags) and row.bucket != "due_soon"


def _parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _cell(value: object) -> str:
    return " ".join(str(value).split()).replace("|", "/")


__all__ = [
    "CADENCE_DAYS",
    "DUE_SOON_DAYS",
    "SourceRefreshDueReport",
    "SourceRefreshDueRow",
    "collect_source_refresh_due",
    "render_source_refresh_due_markdown",
    "source_refresh_due_figure_rows",
    "write_source_refresh_due",
]
