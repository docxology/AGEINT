"""Scholarship-quality audit helpers for AGEINT generated manuscripts."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
import json
import re
from typing import Any

try:
    from .analysis_validation import (
        analysis_validation_contract_terms,
        analysis_validation_family_lane_map,
    )
    from .citation_workflow import CitationCountRow, generated_markdown_citation_inventory
    from .intelligence_content import INTELLIGENCE_RESEARCH_ANCHORS
    from .source_support_strength import support_family_for_key
except ImportError:  # pragma: no cover - exercised by script-level imports
    from analysis_validation import (  # type: ignore[no-redef]
        analysis_validation_contract_terms,
        analysis_validation_family_lane_map,
    )
    from citation_workflow import CitationCountRow, generated_markdown_citation_inventory  # type: ignore[no-redef]
    from intelligence_content import INTELLIGENCE_RESEARCH_ANCHORS  # type: ignore[no-redef]
    from source_support_strength import support_family_for_key  # type: ignore[no-redef]


SOURCE_GUIDE_KEY_RE = re.compile(r"^ageint\d{3}$")
PROJECT_ROOT = Path(__file__).resolve().parents[1]
CLAIM_BEARING_FAMILIES = frozenset(
    {
        "assessment-route",
        "evidence-contract",
        "governance-boundary",
        "method-assurance-reference.md",
        "overview",
        "part unit intros",
        "practice-studio",
    }
)
HARD_FAIL_FLAGS = frozenset({"uncited_claim_bearing", "thin_claim_bearing"})
SAT_METHOD_CONTRACT_REQUIREMENTS: tuple[tuple[str, str], ...] = (
    ("abstract", "Synthetic Analytic Tradecraft"),
    ("abstract", "synthetic in its fixtures, not in its standards"),
    ("abstract", "[@fig:ageint-synthetic-tradecraft-method-contract]"),
    ("orientation", "{#sec:synthetic-analytic-tradecraft-thesis}"),
    ("orientation", "source-family triangulation"),
    ("orientation", "negative-control testing"),
    ("orientation", "[@fig:ageint-synthetic-tradecraft-method-contract]"),
)
ANALYSIS_VALIDATION_CONTRACT_REQUIREMENTS: tuple[tuple[str, str], ...] = (
    ("abstract", "[@fig:ageint-analysis-validation-matrix]"),
    ("orientation", "{#sec:analysis-validation-protocol}"),
    ("orientation", "Claim class"),
    ("orientation", "Validation question"),
    ("orientation", "Failure mode"),
    ("orientation", "[@fig:ageint-analysis-validation-matrix]"),
)
ANALYSIS_VALIDATION_LANE_REQUIREMENTS: tuple[tuple[str, str], ...] = tuple(
    ("orientation", term) for term in analysis_validation_contract_terms()
)


@dataclass(frozen=True)
class ScholarshipQualityRow:
    """Citation-family profile for one generated Markdown file."""

    path: str
    family: str
    citation_count: int
    unique_citation_count: int
    citation_keys: tuple[str, ...]
    source_families: tuple[str, ...]
    flags: tuple[str, ...]

    def as_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "family": self.family,
            "citation_count": self.citation_count,
            "unique_citation_count": self.unique_citation_count,
            "citation_keys": list(self.citation_keys),
            "source_families": list(self.source_families),
            "flags": list(self.flags),
        }


@dataclass(frozen=True)
class ScholarshipQualityReport:
    """One scholarship-quality snapshot for generated manuscript files."""

    payload: dict[str, Any]

    @property
    def ok(self) -> bool:
        return bool(self.payload["ok"])


def collect_scholarship_quality(manuscript_dir: Path) -> ScholarshipQualityReport:
    """Collect citation-family and thin-support evidence for generated Markdown."""
    root = Path(manuscript_dir)
    citation_rows = generated_markdown_citation_inventory(root)
    anchor_map = {anchor.key: anchor for anchor in INTELLIGENCE_RESEARCH_ANCHORS}
    rows = [_classify_row(row, anchor_map) for row in citation_rows]
    hard_fail_rows = [row for row in rows if HARD_FAIL_FLAGS.intersection(row.flags)]
    warning_rows = [row for row in rows if "single_source_family_claim_bearing" in row.flags]
    sat_contract = _contract_check(root, SAT_METHOD_CONTRACT_REQUIREMENTS)
    analysis_contract = _contract_check(root, ANALYSIS_VALIDATION_CONTRACT_REQUIREMENTS)
    analysis_lane_contract = _contract_check(root, ANALYSIS_VALIDATION_LANE_REQUIREMENTS)
    analysis_family_coverage = _analysis_validation_family_coverage(rows)
    payload = {
        "project": "AGEINT",
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "ok": (
            not hard_fail_rows
            and sat_contract["ok"]
            and analysis_contract["ok"]
            and analysis_lane_contract["ok"]
            and analysis_family_coverage["ok"]
        ),
        "thresholds": {
            "claim_bearing_min_unique_citations": 2,
            "hard_fail_flags": sorted(HARD_FAIL_FLAGS),
            "single_source_family_is_warning": True,
        },
        "summary": _summary(rows, anchor_map),
        "sat_method_contract": sat_contract,
        "analysis_validation_contract": analysis_contract,
        "analysis_validation_lane_contract": analysis_lane_contract,
        "analysis_validation_family_coverage": analysis_family_coverage,
        "hard_fail_rows": [row.as_dict() for row in hard_fail_rows],
        "warning_row_count": len(warning_rows),
        "warning_rows": [row.as_dict() for row in warning_rows[:40]],
        "rows": [row.as_dict() for row in rows],
    }
    return ScholarshipQualityReport(payload)


def write_scholarship_quality(project_root: Path) -> tuple[Path, Path, ScholarshipQualityReport]:
    """Write JSON and Markdown scholarship-quality reports under ``output/reports``."""
    root = Path(project_root)
    report = collect_scholarship_quality(root / "output" / "manuscript")
    reports_dir = root / "output" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_path = reports_dir / "scholarship_quality.json"
    md_path = reports_dir / "scholarship_quality.md"
    json_path.write_text(json.dumps(report.payload, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_scholarship_quality_markdown(report), encoding="utf-8")
    return json_path, md_path, report


def render_scholarship_quality_markdown(report: ScholarshipQualityReport) -> str:
    """Render a compact Markdown version of the scholarship-quality report."""
    payload = report.payload
    summary = payload["summary"]
    lines = [
        "# AGEINT Scholarship Quality",
        "",
        "| Measure | Value |",
        "|---|---:|",
        f"| OK | {str(payload['ok']).lower()} |",
        f"| Generated at | {payload['generated_at']} |",
        f"| Generated Markdown files | {summary['generated_markdown_files']} |",
        f"| Cited generated files | {summary['cited_files']} |",
        f"| Claim-bearing files | {summary['claim_bearing_files']} |",
        f"| Uncited claim-bearing files | {summary['uncited_claim_bearing_files']} |",
        f"| Thin claim-bearing files | {summary['thin_claim_bearing_files']} |",
        f"| Single-family claim-bearing files | {summary['single_source_family_claim_bearing_files']} |",
        f"| SAT method contract | {str(payload['sat_method_contract']['ok']).lower()} |",
        f"| Analysis validation contract | {str(payload['analysis_validation_contract']['ok']).lower()} |",
        f"| Analysis validation lane contract | {str(payload['analysis_validation_lane_contract']['ok']).lower()} |",
        f"| Analysis validation family coverage | {str(payload['analysis_validation_family_coverage']['ok']).lower()} |",
        "",
        "## Source-Family Mentions",
        "",
        "| Source family | File-key mentions |",
        "|---|---:|",
    ]
    for family, count in summary["source_family_mentions"].items():
        lines.append(f"| {family} | {count} |")
    lines.extend(
        [
            "",
            "## Hard-Fail Rows",
            "",
            "| Path | Family | Citations | Unique | Flags |",
            "|---|---|---:|---:|---|",
        ]
    )
    if payload["hard_fail_rows"]:
        for row in payload["hard_fail_rows"]:
            lines.append(
                f"| {row['path']} | {row['family']} | {row['citation_count']} | "
                f"{row['unique_citation_count']} | {', '.join(row['flags'])} |"
            )
    else:
        lines.append("| None | - | 0 | 0 | - |")
    lines.extend(
        [
            "",
            "## Review Warnings",
            "",
            "Single-family claim-bearing files are review warnings, not automatic failures, "
            "because many coursebook sections intentionally inherit source-guide context. "
            "They identify the next best targets for direct official, standards, or scholarly "
            "triangulation.",
            "",
            "| Path | Family | Source family | Unique citations |",
            "|---|---|---|---:|",
        ]
    )
    if payload["warning_rows"]:
        for row in payload["warning_rows"]:
            lines.append(
                f"| {row['path']} | {row['family']} | "
                f"{', '.join(row['source_families'])} | {row['unique_citation_count']} |"
            )
    else:
        lines.append("| None | - | - | 0 |")
    lines.extend(
        [
            "",
            "## Synthetic Analytic Tradecraft Method Contract",
            "",
            f"Checked: `{str(payload['sat_method_contract']['checked']).lower()}`",
            "",
            f"OK: `{str(payload['sat_method_contract']['ok']).lower()}`",
            "",
            "| Missing path | Missing term |",
            "|---|---|",
        ]
    )
    if payload["sat_method_contract"]["missing"]:
        for row in payload["sat_method_contract"]["missing"]:
            lines.append(f"| {row['path']} | {row['term']} |")
    else:
        lines.append("| None | - |")
    lines.extend(
        [
            "",
            "## Analysis Validation Contract",
            "",
            f"Checked: `{str(payload['analysis_validation_contract']['checked']).lower()}`",
            "",
            f"OK: `{str(payload['analysis_validation_contract']['ok']).lower()}`",
            "",
            "| Missing path | Missing term |",
            "|---|---|",
        ]
    )
    if payload["analysis_validation_contract"]["missing"]:
        for row in payload["analysis_validation_contract"]["missing"]:
            lines.append(f"| {row['path']} | {row['term']} |")
    else:
        lines.append("| None | - |")
    lines.extend(
        [
            "",
            "## Analysis Validation Lane Contract",
            "",
            f"Checked: `{str(payload['analysis_validation_lane_contract']['checked']).lower()}`",
            "",
            f"OK: `{str(payload['analysis_validation_lane_contract']['ok']).lower()}`",
            "",
            "| Missing path | Missing term |",
            "|---|---|",
        ]
    )
    if payload["analysis_validation_lane_contract"]["missing"]:
        for row in payload["analysis_validation_lane_contract"]["missing"]:
            lines.append(f"| {row['path']} | {row['term']} |")
    else:
        lines.append("| None | - |")
    lines.extend(
        [
            "",
            "## Analysis Validation Family Coverage",
            "",
            f"Checked: `{str(payload['analysis_validation_family_coverage']['checked']).lower()}`",
            "",
            f"OK: `{str(payload['analysis_validation_family_coverage']['ok']).lower()}`",
            "",
            "| Manuscript family | Claim class | Evidence signal | Failure signal |",
            "|---|---|---|---|",
        ]
    )
    for row in payload["analysis_validation_family_coverage"]["families"]:
        lines.append(
            f"| {row['family']} | {row['claim_class']} | "
            f"{row['evidence_signal']} | {row['failure_signal']} |"
        )
    if payload["analysis_validation_family_coverage"]["missing_families"]:
        lines.extend(["", "**Missing families:**"])
        for family in payload["analysis_validation_family_coverage"]["missing_families"]:
            lines.append(f"- `{family}`")
    return "\n".join(lines) + "\n"


def citation_source_family(key: str, anchor_map: dict[str, Any] | None = None) -> str:
    """Return a coarse source family for a Pandoc citation key."""
    if SOURCE_GUIDE_KEY_RE.fullmatch(key):
        profile = support_family_for_key(key, PROJECT_ROOT)
        if profile.startswith("source_guide_"):
            return "source_guide"
        return profile
    anchor = (anchor_map or {}).get(key)
    if anchor is not None:
        source_text = " ".join(
            str(value)
            for value in (
                getattr(anchor, "source_tier", ""),
                getattr(anchor, "source_type", ""),
                getattr(anchor, "source_lane", ""),
                getattr(anchor, "domain", ""),
                key,
            )
            if value
        ).lower()
    else:
        source_text = key.lower()
    if "standard" in source_text or "fips" in source_text or "sp_800" in source_text:
        return "standard"
    if "scholarly" in source_text or key.startswith("scholarly_"):
        return "scholarly"
    if any(token in source_text for token in ("statutory", "regulatory", "law", "policy")):
        return "law_policy"
    if "official" in source_text or key.startswith("official_"):
        return "official"
    if any(token in source_text for token in ("public_domain", "historical")):
        return "public_domain"
    if any(token in source_text for token in ("vendor", "practitioner")):
        return "practitioner_vendor"
    return "curated_anchor"


def _classify_row(row: CitationCountRow, anchor_map: dict[str, Any]) -> ScholarshipQualityRow:
    source_families = tuple(
        dict.fromkeys(citation_source_family(key, anchor_map) for key in row.citation_keys)
    )
    flags: list[str] = []
    is_claim_bearing = row.family in CLAIM_BEARING_FAMILIES
    if is_claim_bearing and row.citation_count == 0:
        flags.append("uncited_claim_bearing")
    if is_claim_bearing and 0 < row.unique_citation_count < 2:
        flags.append("thin_claim_bearing")
    if is_claim_bearing and row.unique_citation_count >= 2 and len(source_families) <= 1:
        flags.append("single_source_family_claim_bearing")
    return ScholarshipQualityRow(
        path=row.path,
        family=row.family,
        citation_count=row.citation_count,
        unique_citation_count=row.unique_citation_count,
        citation_keys=row.citation_keys,
        source_families=source_families,
        flags=tuple(flags),
    )


def _summary(rows: list[ScholarshipQualityRow], anchor_map: dict[str, Any]) -> dict[str, Any]:
    family_mentions: Counter[str] = Counter()
    family_file_counts: Counter[str] = Counter()
    for row in rows:
        family_mentions.update(citation_source_family(key, anchor_map) for key in row.citation_keys)
        family_file_counts.update(set(row.source_families))
    claim_rows = [row for row in rows if row.family in CLAIM_BEARING_FAMILIES]
    return {
        "generated_markdown_files": len(rows),
        "cited_files": sum(1 for row in rows if row.citation_count > 0),
        "uncited_files": sum(1 for row in rows if row.citation_count == 0),
        "claim_bearing_files": len(claim_rows),
        "uncited_claim_bearing_files": sum(
            1 for row in claim_rows if "uncited_claim_bearing" in row.flags
        ),
        "thin_claim_bearing_files": sum(
            1 for row in claim_rows if "thin_claim_bearing" in row.flags
        ),
        "single_source_family_claim_bearing_files": sum(
            1 for row in claim_rows if "single_source_family_claim_bearing" in row.flags
        ),
        "source_family_mentions": dict(sorted(family_mentions.items())),
        "source_family_file_counts": dict(sorted(family_file_counts.items())),
        "claim_bearing_family_counts": dict(
            sorted(Counter(row.family for row in claim_rows).items())
        ),
    }


def _analysis_validation_family_coverage(rows: list[ScholarshipQualityRow]) -> dict[str, Any]:
    lane_map = analysis_validation_family_lane_map()
    claim_families = sorted({row.family for row in rows if row.family in CLAIM_BEARING_FAMILIES})
    missing = [family for family in claim_families if family not in lane_map]
    lane_counts = Counter(
        lane_map[family].claim_class for family in claim_families if family in lane_map
    )
    families = []
    for family in claim_families:
        lane = lane_map.get(family)
        families.append(
            {
                "family": family,
                "claim_class": lane.claim_class if lane else "<missing>",
                "evidence_signal": lane.evidence_signal if lane else "<missing>",
                "failure_signal": lane.failure_signal if lane else "<missing>",
            }
        )
    return {
        "checked": bool(claim_families),
        "ok": not missing,
        "family_count": len(claim_families),
        "lane_counts": dict(sorted(lane_counts.items())),
        "missing_families": missing,
        "families": families,
    }


def _contract_check(manuscript_dir: Path, requirements: tuple[tuple[str, str], ...]) -> dict[str, Any]:
    root = Path(manuscript_dir)
    surfaces = {surface for surface, _ in requirements}
    existing_surfaces = {surface for surface in surfaces if _contract_texts(root, surface)}
    if not existing_surfaces:
        return {"checked": False, "ok": True, "missing": []}
    missing: list[dict[str, str]] = []
    for surface, term in requirements:
        texts = _contract_texts(root, surface)
        if not texts:
            missing.append({"path": surface, "term": "<file missing>"})
            continue
        if not any(term in text for _, text in texts):
            missing.append({"path": surface, "term": term})
    return {"checked": True, "ok": not missing, "missing": missing}


def _contract_texts(root: Path, surface: str) -> list[tuple[str, str]]:
    if surface == "abstract":
        paths = [root / "abstract.md"]
    elif surface == "orientation":
        paths = [root / "orientation.md"]
        orientation_dir = root / "orientation"
        if orientation_dir.is_dir():
            paths.extend(sorted(orientation_dir.rglob("*.md")))
    else:
        paths = [root / f"{surface}.md"]
    return [
        (path.relative_to(root).as_posix(), path.read_text(encoding="utf-8"))
        for path in paths
        if path.is_file()
    ]


__all__ = [
    "ANALYSIS_VALIDATION_CONTRACT_REQUIREMENTS",
    "ANALYSIS_VALIDATION_LANE_REQUIREMENTS",
    "CLAIM_BEARING_FAMILIES",
    "HARD_FAIL_FLAGS",
    "SAT_METHOD_CONTRACT_REQUIREMENTS",
    "ScholarshipQualityReport",
    "ScholarshipQualityRow",
    "citation_source_family",
    "collect_scholarship_quality",
    "render_scholarship_quality_markdown",
    "write_scholarship_quality",
    "_analysis_validation_family_coverage",
]
