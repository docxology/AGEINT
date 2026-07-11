"""Source-anchor metadata audit helpers for AGEINT."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
import json
from typing import Any


SOURCE_METADATA_BASELINE: dict[str, int] = {
    "legacy_intelligence_blank_rows": 109,
    "source_quality_blank_rows": 10,
    "total_blank_rows_closed": 119,
}


@dataclass(frozen=True)
class SourceMetadataRow:
    """One source-anchor row with the fields that drive lane/tier audits."""

    path: str
    line: int
    key: str
    row_class: str
    domain: str
    source_type: str
    source_lane: str
    source_tier: str
    refresh_cadence: str
    checked_as_of: str
    flags: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "line": self.line,
            "key": self.key,
            "row_class": self.row_class,
            "domain": self.domain,
            "source_type": self.source_type,
            "source_lane": self.source_lane,
            "source_tier": self.source_tier,
            "refresh_cadence": self.refresh_cadence,
            "checked_as_of": self.checked_as_of,
            "flags": list(self.flags),
        }


@dataclass(frozen=True)
class SourceMetadataReport:
    """One source-anchor metadata snapshot."""

    payload: dict[str, Any]

    @property
    def ok(self) -> bool:
        return bool(self.payload["ok"])


def collect_source_metadata(project_root: Path) -> SourceMetadataReport:
    """Collect lane/tier metadata coverage for curated and support anchors."""
    root = Path(project_root)
    rows = _load_rows(root / "data" / "research_anchors")
    issue_rows = [row for row in rows if row.flags]
    summary = _summary(rows)
    payload = {
        "project": "AGEINT",
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "ok": not issue_rows and bool(rows),
        "baseline_closed": SOURCE_METADATA_BASELINE,
        "summary": summary,
        "issue_row_count": len(issue_rows),
        "issue_rows": [row.as_dict() for row in issue_rows],
        "rows": [row.as_dict() for row in rows],
    }
    return SourceMetadataReport(payload)


def write_source_metadata(project_root: Path) -> tuple[Path, Path, SourceMetadataReport]:
    """Write JSON and Markdown source-metadata reports under ``output/reports``."""
    root = Path(project_root)
    report = collect_source_metadata(root)
    reports_dir = root / "output" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_path = reports_dir / "source_metadata.json"
    md_path = reports_dir / "source_metadata.md"
    json_path.write_text(json.dumps(report.payload, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_source_metadata_markdown(report), encoding="utf-8")
    return json_path, md_path, report


def render_source_metadata_markdown(report: SourceMetadataReport) -> str:
    """Render a compact Markdown version of the source-metadata report."""
    payload = report.payload
    summary = payload["summary"]
    baseline = payload["baseline_closed"]
    lines = [
        "# AGEINT Source Metadata",
        "",
        "| Measure | Value |",
        "|---|---:|",
        f"| OK | {str(payload['ok']).lower()} |",
        f"| Generated at | {payload['generated_at']} |",
        f"| Metadata records | {summary['metadata_records']} |",
        f"| Intelligence anchors | {summary['intelligence_anchor_count']} |",
        f"| Source-quality support anchors | {summary['source_quality_anchor_count']} |",
        f"| Blank source lanes | {summary['blank_source_lane_count']} |",
        f"| Blank source tiers | {summary['blank_source_tier_count']} |",
        f"| Fallback-dependent rows | {summary['fallback_dependent_row_count']} |",
        f"| Source-quality semantic issues | {summary['source_quality_semantic_issue_count']} |",
        "",
        "## Baseline Closed",
        "",
        "| Baseline | Rows |",
        "|---|---:|",
        f"| Legacy intelligence blank rows | {baseline['legacy_intelligence_blank_rows']} |",
        f"| Source-quality blank rows | {baseline['source_quality_blank_rows']} |",
        f"| Total blank rows closed | {baseline['total_blank_rows_closed']} |",
        "",
        "## Lane Distribution",
        "",
        "| Lane | Rows |",
        "|---|---:|",
    ]
    for lane, count in summary["source_lane_distribution"].items():
        lines.append(f"| {lane} | {count} |")
    lines.extend(["", "## Tier Distribution", "", "| Tier | Rows |", "|---|---:|"])
    for tier, count in summary["source_tier_distribution"].items():
        lines.append(f"| {tier} | {count} |")
    lines.extend(["", "## Issue Rows", "", "| Path | Line | Key | Flags |", "|---|---:|---|---|"])
    if payload["issue_rows"]:
        for row in payload["issue_rows"]:
            lines.append(f"| {row['path']} | {row['line']} | {row['key']} | {', '.join(row['flags'])} |")
    else:
        lines.append("| None | 0 | - | - |")
    return "\n".join(lines) + "\n"


def source_metadata_figure_rows(project_root: Path) -> tuple[tuple[str, tuple[str, str, str]], ...]:
    """Return compact source-metadata rows for a registry-backed visual."""
    report = collect_source_metadata(project_root).payload
    summary = report["summary"]
    baseline = report["baseline_closed"]
    return (
        (
            "Intelligence anchors",
            (
                f"{summary['intelligence_anchor_count']} rows",
                f"{baseline['legacy_intelligence_blank_rows']} legacy blanks closed",
                f"{summary['blank_source_lane_count']} blank lanes",
            ),
        ),
        (
            "Source-quality anchors",
            (
                f"{summary['source_quality_anchor_count']} rows",
                "source_quality_spine",
                "source_quality_anchor",
            ),
        ),
        (
            "Metadata explicitness",
            (
                f"{summary['metadata_records']} records",
                f"{summary['fallback_dependent_row_count']} fallback rows",
                f"{summary['blank_source_tier_count']} blank tiers",
            ),
        ),
        (
            "Refresh cadence",
            (
                f"{len(summary['refresh_cadence_distribution'])} cadence classes",
                "checked_as_of retained",
                "refresh triggers preserved",
            ),
        ),
        (
            "Evidence manifest",
            (
                "source_metadata_ok",
                "blank row fails",
                "support semantics fail",
            ),
        ),
    )


def _load_rows(data_dir: Path) -> list[SourceMetadataRow]:
    rows: list[SourceMetadataRow] = []
    for path in sorted(data_dir.glob("*.jsonl")):
        if path.name != "source-quality-anchors.jsonl" and not path.name.startswith("intelligence-anchors-"):
            continue
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            payload = json.loads(line)
            rows.append(_row_from_payload(data_dir.parent.parent, path, line_number, payload))
    return rows


def _row_from_payload(project_root: Path, path: Path, line_number: int, payload: dict[str, Any]) -> SourceMetadataRow:
    row_class = "source_quality" if path.name == "source-quality-anchors.jsonl" else "intelligence"
    source_lane = str(payload.get("source_lane") or "")
    source_tier = str(payload.get("source_tier") or "")
    flags: list[str] = []
    if not source_lane:
        flags.append("blank_source_lane")
    if not source_tier:
        flags.append("blank_source_tier")
    if row_class == "source_quality" and source_lane != "source_quality_spine":
        flags.append("source_quality_lane_mismatch")
    if row_class == "source_quality" and source_tier != "source_quality_anchor":
        flags.append("source_quality_tier_mismatch")
    return SourceMetadataRow(
        path=path.relative_to(project_root).as_posix(),
        line=line_number,
        key=str(payload.get("key") or "<missing>"),
        row_class=row_class,
        domain=str(payload.get("domain") or ""),
        source_type=str(payload.get("source_type") or ""),
        source_lane=source_lane,
        source_tier=source_tier,
        refresh_cadence=str(payload.get("refresh_cadence") or ""),
        checked_as_of=str(payload.get("checked_as_of") or ""),
        flags=tuple(flags),
    )


def _summary(rows: list[SourceMetadataRow]) -> dict[str, Any]:
    blank_lane = [row for row in rows if "blank_source_lane" in row.flags]
    blank_tier = [row for row in rows if "blank_source_tier" in row.flags]
    fallback_rows = sorted({(row.path, row.line, row.key) for row in (*blank_lane, *blank_tier)})
    source_quality_issues = [
        row
        for row in rows
        if "source_quality_lane_mismatch" in row.flags or "source_quality_tier_mismatch" in row.flags
    ]
    return {
        "metadata_records": len(rows),
        "intelligence_anchor_count": sum(1 for row in rows if row.row_class == "intelligence"),
        "source_quality_anchor_count": sum(1 for row in rows if row.row_class == "source_quality"),
        "blank_source_lane_count": len(blank_lane),
        "blank_source_tier_count": len(blank_tier),
        "fallback_dependent_row_count": len(fallback_rows),
        "source_quality_semantic_issue_count": len(source_quality_issues),
        "source_lane_distribution": dict(sorted(Counter(row.source_lane for row in rows).items())),
        "source_tier_distribution": dict(sorted(Counter(row.source_tier for row in rows).items())),
        "refresh_cadence_distribution": dict(sorted(Counter(row.refresh_cadence for row in rows).items())),
        "checked_as_of_distribution": dict(sorted(Counter(row.checked_as_of for row in rows).items())),
    }


__all__ = [
    "SOURCE_METADATA_BASELINE",
    "SourceMetadataReport",
    "SourceMetadataRow",
    "collect_source_metadata",
    "render_source_metadata_markdown",
    "source_metadata_figure_rows",
    "write_source_metadata",
]
