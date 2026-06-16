"""US Intelligence Community agency-source coverage audit for AGEINT."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
from typing import Any

try:
    from intelligence_content import INTELLIGENCE_PROFILES, expanded_profile_anchor_keys
    from intelligence_content.source_packs import agency_source_pack_payload
except ImportError:  # pragma: no cover - package import variants
    from .intelligence_content import INTELLIGENCE_PROFILES, expanded_profile_anchor_keys
    from .intelligence_content.source_packs import agency_source_pack_payload

NEW_SHARD_NAME = "intelligence-anchors-249-304.jsonl"
EXPECTED_NEW_US_IC_ANCHORS = 56
REQUIRED_NEW_METADATA: tuple[str, ...] = (
    "source_agency",
    "source_pack",
    "source_lane",
    "source_tier",
    "checked_as_of",
    "claim_scope",
    "assurance_use",
    "rights_dimension",
)
MINIMUM_AGENCY_COUNTS: dict[str, int] = {
    "CIA": 25,
    "DIA": 3,
}
MINIMUM_ODNI_INTELGOV = 20


@dataclass(frozen=True)
class AgencySourceCoverageRow:
    """One agency-source row with audit flags."""

    path: str
    line: int
    key: str
    source_agency: str
    source_pack: str
    source_lane: str
    source_tier: str
    routed_profiles: tuple[str, ...]
    flags: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "line": self.line,
            "key": self.key,
            "source_agency": self.source_agency,
            "source_pack": self.source_pack,
            "source_lane": self.source_lane,
            "source_tier": self.source_tier,
            "routed_profiles": list(self.routed_profiles),
            "flags": list(self.flags),
        }


@dataclass(frozen=True)
class AgencySourceCoverageReport:
    """Agency-source coverage audit snapshot."""

    payload: dict[str, Any]

    @property
    def ok(self) -> bool:
        return bool(self.payload["ok"])


def collect_agency_source_coverage(project_root: Path) -> AgencySourceCoverageReport:
    """Collect coverage for the official US IC source-expansion tranche."""

    root = Path(project_root)
    raw_rows = _load_anchor_rows(root)
    new_rows = [row for row in raw_rows if row["path"].endswith(NEW_SHARD_NAME)]
    packs = agency_source_pack_payload(root)
    key_to_profiles = _profile_routes(root)
    existing_rows = [row for row in raw_rows if not row["path"].endswith(NEW_SHARD_NAME)]
    duplicate_keys = sorted(_new_duplicate_values(new_rows, existing_rows, "key"))
    duplicate_urls = sorted(_new_duplicate_values(new_rows, existing_rows, "url"))
    rows = [
        _coverage_row(row, packs, key_to_profiles, duplicate_keys, duplicate_urls)
        for row in new_rows
    ]
    row_issues = [row for row in rows if row.flags]
    global_issues = _global_issues(rows, new_rows, duplicate_keys, duplicate_urls)
    payload = {
        "project": "AGEINT",
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "ok": bool(new_rows) and not row_issues and not global_issues,
        "expected_new_us_ic_anchors": EXPECTED_NEW_US_IC_ANCHORS,
        "required_new_metadata": list(REQUIRED_NEW_METADATA),
        "summary": _summary(raw_rows, rows),
        "minimums": {
            "cia_new_minimum": MINIMUM_AGENCY_COUNTS["CIA"],
            "dia_new_minimum": MINIMUM_AGENCY_COUNTS["DIA"],
            "odni_or_intelligence_gov_new_minimum": MINIMUM_ODNI_INTELGOV,
        },
        "global_issue_count": len(global_issues),
        "global_issues": global_issues,
        "issue_row_count": len(row_issues),
        "issue_rows": [row.as_dict() for row in row_issues],
        "rows": [row.as_dict() for row in rows],
    }
    return AgencySourceCoverageReport(payload)


def write_agency_source_coverage(project_root: Path) -> tuple[Path, Path, AgencySourceCoverageReport]:
    """Write JSON and Markdown reports under ``output/reports``."""

    root = Path(project_root)
    report = collect_agency_source_coverage(root)
    reports = root / "output" / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    json_path = reports / "agency_source_coverage.json"
    md_path = reports / "agency_source_coverage.md"
    json_path.write_text(json.dumps(report.payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_agency_source_coverage_markdown(report), encoding="utf-8")
    return json_path, md_path, report


def render_agency_source_coverage_markdown(report: AgencySourceCoverageReport) -> str:
    """Render the agency-source coverage audit as Markdown."""

    payload = report.payload
    summary = payload["summary"]
    lines = [
        "# AGEINT Agency Source Coverage",
        "",
        "| Measure | Value |",
        "|---|---:|",
        f"| OK | {str(payload['ok']).lower()} |",
        f"| agency_source_coverage_ok | {str(payload['ok']).lower()} |",
        f"| Generated at | {payload['generated_at']} |",
        f"| Curated intelligence anchors | {summary['curated_intelligence_anchor_count']} |",
        f"| New official US IC anchors | {summary['new_official_us_ic_anchor_count']} |",
        f"| Missing required metadata | {summary['missing_required_metadata_count']} |",
        f"| Unrouted new anchors | {summary['unrouted_new_anchor_count']} |",
        f"| Duplicate new/source keys | {summary['duplicate_key_count']} |",
        f"| Duplicate new/source URLs | {summary['duplicate_url_count']} |",
        "",
        "## Agency Counts",
        "",
        "| Agency | Rows |",
        "|---|---:|",
    ]
    for agency, count in summary["agency_counts"].items():
        lines.append(f"| {agency} | {count} |")
    lines.extend(["", "## Source Pack Counts", "", "| Source pack | Rows |", "|---|---:|"])
    for pack, count in summary["source_pack_counts"].items():
        lines.append(f"| {pack} | {count} |")
    lines.extend(["", "## Issue Rows", "", "| Path | Line | Key | Flags |", "|---|---:|---|---|"])
    if payload["issue_rows"]:
        for row in payload["issue_rows"]:
            lines.append(f"| {row['path']} | {row['line']} | {row['key']} | {', '.join(row['flags'])} |")
    else:
        lines.append("| None | 0 | - | - |")
    if payload["global_issues"]:
        lines.extend(["", "## Global Issues", "", "| Issue | Detail |", "|---|---|"])
        for issue in payload["global_issues"]:
            lines.append(f"| {issue['issue']} | {issue['detail']} |")
    return "\n".join(lines) + "\n"


def agency_source_coverage_figure_rows(project_root: Path) -> tuple[tuple[str, tuple[str, str, str]], ...]:
    """Return compact rows for the agency-source coverage dashboard."""

    report = collect_agency_source_coverage(project_root).payload
    summary = report["summary"]
    agencies = summary["agency_counts"]
    packs = summary["source_pack_counts"]
    return (
        (
            "US IC source tranche",
            (
                f"{summary['new_official_us_ic_anchor_count']} new anchors",
                f"{agencies.get('CIA', 0)} CIA",
                f"{agencies.get('DIA', 0)} DIA",
            ),
        ),
        (
            "ODNI and public IC",
            (
                f"{agencies.get('ODNI', 0)} ODNI",
                f"{agencies.get('Intelligence.gov', 0)} Intelligence.gov",
                f"{summary['odni_or_intelgov_count']} ODNI/Intel.gov",
            ),
        ),
        (
            "Pack routing",
            (
                f"{len(packs)} source packs",
                f"{summary['profile_routed_new_anchor_count']} routed",
                f"{summary['unrouted_new_anchor_count']} unrouted",
            ),
        ),
        (
            "Evidence manifest",
            (
                "agency_source_coverage_ok",
                "missing pack fails",
                "counts are coverage telemetry",
            ),
        ),
    )


def _load_anchor_rows(root: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    data_dir = root / "data" / "research_anchors"
    for path in sorted(data_dir.glob("intelligence-anchors-*.jsonl")):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if not line.strip():
                continue
            row = json.loads(line)
            row["path"] = path.relative_to(root).as_posix()
            row["line"] = line_number
            rows.append(row)
    return rows


def _coverage_row(
    row: dict[str, Any],
    packs: dict[str, tuple[str, ...]],
    key_to_profiles: dict[str, tuple[str, ...]],
    duplicate_keys: list[str],
    duplicate_urls: list[str],
) -> AgencySourceCoverageRow:
    key = str(row.get("key") or "")
    source_agency = str(row.get("source_agency") or "")
    source_pack = str(row.get("source_pack") or "")
    flags: list[str] = []
    for field in REQUIRED_NEW_METADATA:
        if not str(row.get(field) or "").strip():
            flags.append(f"missing_{field}")
    if source_pack and key not in packs.get(source_pack, ()):
        flags.append("source_pack_missing_key")
    if not str(row.get("url") or "").startswith("https://"):
        flags.append("non_https_url")
    if str(row.get("source_type") or "") != "official_primary":
        flags.append("not_official_primary")
    if str(row.get("source_tier") or "") != "official_primary":
        flags.append("not_official_primary_tier")
    if key in duplicate_keys:
        flags.append("duplicate_key")
    if str(row.get("url") or "") in duplicate_urls:
        flags.append("duplicate_url")
    routed_profiles = key_to_profiles.get(key, ())
    if not routed_profiles:
        flags.append("unrouted_new_anchor")
    return AgencySourceCoverageRow(
        path=str(row.get("path") or ""),
        line=int(row.get("line") or 0),
        key=key,
        source_agency=source_agency,
        source_pack=source_pack,
        source_lane=str(row.get("source_lane") or ""),
        source_tier=str(row.get("source_tier") or ""),
        routed_profiles=routed_profiles,
        flags=tuple(flags),
    )


def _profile_routes(root: Path) -> dict[str, tuple[str, ...]]:
    route_map: dict[str, list[str]] = {}
    for profile in INTELLIGENCE_PROFILES:
        try:
            keys = expanded_profile_anchor_keys(profile, root)
        except KeyError:
            keys = profile.anchor_keys
        for key in keys:
            route_map.setdefault(key, []).append(profile.identifier)
    return {key: tuple(values) for key, values in route_map.items()}


def _summary(raw_rows: list[dict[str, Any]], rows: list[AgencySourceCoverageRow]) -> dict[str, Any]:
    agency_counts = Counter(row.source_agency for row in rows)
    source_pack_counts = Counter(row.source_pack for row in rows)
    flags = Counter(flag for row in rows for flag in row.flags)
    odni_or_intelgov = agency_counts.get("ODNI", 0) + agency_counts.get("Intelligence.gov", 0)
    return {
        "curated_intelligence_anchor_count": len(raw_rows),
        "new_official_us_ic_anchor_count": len(rows),
        "agency_counts": dict(sorted(agency_counts.items())),
        "source_pack_counts": dict(sorted(source_pack_counts.items())),
        "source_lane_counts": dict(sorted(Counter(row.source_lane for row in rows).items())),
        "source_tier_counts": dict(sorted(Counter(row.source_tier for row in rows).items())),
        "odni_or_intelgov_count": odni_or_intelgov,
        "profile_routed_new_anchor_count": sum(1 for row in rows if row.routed_profiles),
        "unrouted_new_anchor_count": flags.get("unrouted_new_anchor", 0),
        "missing_required_metadata_count": sum(
            count for flag, count in flags.items() if flag.startswith("missing_")
        ),
        "duplicate_key_count": flags.get("duplicate_key", 0),
        "duplicate_url_count": flags.get("duplicate_url", 0),
        "flag_counts": dict(sorted(flags.items())),
    }


def _global_issues(
    rows: list[AgencySourceCoverageRow],
    new_rows: list[dict[str, Any]],
    duplicate_keys: list[str],
    duplicate_urls: list[str],
) -> list[dict[str, str]]:
    issues: list[dict[str, str]] = []
    if len(new_rows) != EXPECTED_NEW_US_IC_ANCHORS:
        issues.append(
            {
                "issue": "new_shard_count_mismatch",
                "detail": f"expected {EXPECTED_NEW_US_IC_ANCHORS}; found {len(new_rows)}",
            }
        )
    agencies = Counter(row.source_agency for row in rows)
    for agency, minimum in MINIMUM_AGENCY_COUNTS.items():
        if agencies.get(agency, 0) < minimum:
            issues.append(
                {
                    "issue": "agency_minimum_not_met",
                    "detail": f"{agency} expected at least {minimum}; found {agencies.get(agency, 0)}",
                }
            )
    odni_or_intelgov = agencies.get("ODNI", 0) + agencies.get("Intelligence.gov", 0)
    if odni_or_intelgov < MINIMUM_ODNI_INTELGOV:
        issues.append(
            {
                "issue": "odni_intelgov_minimum_not_met",
                "detail": f"expected at least {MINIMUM_ODNI_INTELGOV}; found {odni_or_intelgov}",
            }
        )
    if duplicate_keys:
        issues.append({"issue": "duplicate_keys", "detail": ", ".join(duplicate_keys[:10])})
    if duplicate_urls:
        issues.append({"issue": "duplicate_urls", "detail": ", ".join(duplicate_urls[:10])})
    return issues


def _new_duplicate_values(
    new_rows: list[dict[str, Any]],
    existing_rows: list[dict[str, Any]],
    field: str,
) -> set[str]:
    new_values = [str(row.get(field) or "") for row in new_rows if row.get(field)]
    existing_values = {str(row.get(field) or "") for row in existing_rows if row.get(field)}
    return _duplicates(new_values) | {value for value in new_values if value in existing_values}


def _duplicates(values: list[str]) -> set[str]:
    counts = Counter(values)
    return {value for value, count in counts.items() if count > 1}


__all__ = [
    "AgencySourceCoverageReport",
    "AgencySourceCoverageRow",
    "agency_source_coverage_figure_rows",
    "collect_agency_source_coverage",
    "render_agency_source_coverage_markdown",
    "write_agency_source_coverage",
]
