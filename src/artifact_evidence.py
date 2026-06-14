"""Current AGEINT artifact-evidence manifest helpers."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
import json
import re
from typing import Any

from build_pipeline import generated_output_is_stale
from claim_calibration import collect_claim_calibration, write_claim_calibration
from citation_workflow import (
    generated_markdown_citation_inventory,
    source_citation_coverage_summary,
)
from curriculum import load_curriculum
from pdf_quality import audit_pdf_quality
from rendered_reference_audit import audit_rendered_references
from scholarship_quality import collect_scholarship_quality, write_scholarship_quality
from source_metadata import collect_source_metadata, write_source_metadata

STALE_OUTPUT_PATTERNS: tuple[str, ...] = (
    r"Evidence link.*scholarly_heuer_psychology_intelligence_analysis",
    r"Section 80; \[Jr\., 2007\]",
    r"\| Chapter \| Section \| Source title \| Citation count \| Citation keys \|",
    r"\]\([^)]*\.md\)",
    r"\]\([^)]*\.markdown\)",
)


@dataclass(frozen=True)
class ArtifactEvidence:
    """One evidence snapshot for the generated AGEINT artifact set."""

    payload: dict[str, Any]

    @property
    def ok(self) -> bool:
        return bool(self.payload["ok"])


def collect_artifact_evidence(project_root: Path) -> ArtifactEvidence:
    """Collect current generated-output evidence without mutating outputs."""
    root = Path(project_root)
    output = root / "output"
    manuscript = output / "manuscript"
    pdf = output / "pdf" / "AGEINT_combined.pdf"
    curriculum = load_curriculum(root / "data" / "curriculum")
    source_summary = source_citation_coverage_summary(curriculum)
    generated_rows = generated_markdown_citation_inventory(manuscript)
    figure_registry = _load_json(output / "figures" / "figure_registry.json")
    visual_audit = _load_json(output / "figures" / "visual_quality_audit.json")
    pdf_report = audit_pdf_quality(pdf, manuscript_dir=manuscript)
    rendered_reference_violations = audit_rendered_references(output)
    scan_hits = _scan_generated_text(root)
    figure_summary = _figure_summary(figure_registry, visual_audit)
    citation_counts = _citation_counts(source_summary, generated_rows)
    scholarship_report = collect_scholarship_quality(manuscript)
    source_metadata_report = collect_source_metadata(root)
    claim_calibration_report = collect_claim_calibration(manuscript, project_root=root)
    checks = {
        "generated_output_fresh": not generated_output_is_stale(root, output),
        "rendered_references_resolve": not rendered_reference_violations,
        "stale_output_scans_clean": not scan_hits,
        "pdf_quality_ok": pdf_report.ok,
        "figure_quality_ok": figure_summary["quality_pass"] is True,
        "citation_source_sections_covered": source_summary.zero_citation_sections == 0,
        "scholarship_quality_ok": scholarship_report.ok,
        "source_metadata_ok": source_metadata_report.ok,
        "claim_calibration_ok": claim_calibration_report.ok,
    }
    payload = {
        "project": "AGEINT",
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "ok": all(checks.values()),
        "checks": checks,
        "curriculum": {
            "parts": curriculum.stats["parts"],
            "chapters": curriculum.stats["chapters"],
            "appendices": curriculum.stats["appendices"],
            "patterns": curriculum.stats["patterns"],
            "references": curriculum.stats["references"],
        },
        "citations": citation_counts,
        "scholarship_quality": {
            "report_paths": [
                "output/reports/scholarship_quality.json",
                "output/reports/scholarship_quality.md",
            ],
            "summary": scholarship_report.payload["summary"],
            "sat_method_contract": scholarship_report.payload["sat_method_contract"],
            "analysis_validation_contract": scholarship_report.payload["analysis_validation_contract"],
            "analysis_validation_lane_contract": scholarship_report.payload[
                "analysis_validation_lane_contract"
            ],
            "analysis_validation_family_coverage": scholarship_report.payload[
                "analysis_validation_family_coverage"
            ],
            "hard_fail_rows": scholarship_report.payload["hard_fail_rows"],
            "warning_row_count": scholarship_report.payload["warning_row_count"],
        },
        "source_metadata": {
            "report_paths": [
                "output/reports/source_metadata.json",
                "output/reports/source_metadata.md",
            ],
            "baseline_closed": source_metadata_report.payload["baseline_closed"],
            "summary": source_metadata_report.payload["summary"],
            "issue_row_count": source_metadata_report.payload["issue_row_count"],
            "issue_rows": source_metadata_report.payload["issue_rows"],
        },
        "claim_calibration": {
            "report_paths": [
                "output/reports/claim_calibration.json",
                "output/reports/claim_calibration.md",
            ],
            "summary": claim_calibration_report.payload["summary"],
            "thresholds": claim_calibration_report.payload["thresholds"],
            "hard_fail_rows": claim_calibration_report.payload["hard_fail_rows"],
            "warning_row_count": claim_calibration_report.payload["warning_row_count"],
        },
        "figures": figure_summary,
        "pdf": pdf_report.as_dict(),
        "rendered_references": {
            "violation_count": len(rendered_reference_violations),
            "violations": [violation.format(root) for violation in rendered_reference_violations],
        },
        "generated_output_scan": {
            "pattern_count": len(STALE_OUTPUT_PATTERNS),
            "hit_count": len(scan_hits),
            "hits": scan_hits,
        },
        "false_certification_control": {
            "scenario": (
                "A reviewer trusts a copied PDF, citation count, or current-evidence note "
                "without proving that rendered references, PDF annotations, figure metadata, "
                "and generated citation counts came from the same rebuilt artifact set."
            ),
            "negative_control": (
                "Add a generated Markdown link to a local .md file, restore the old "
                "source-section coverage table header, or make the PDF older than the "
                "combined manuscript; collapse a claim-bearing generated section to a "
                "single citation key; or remove the Synthetic Analytic Tradecraft method "
                "figure reference, analysis-validation matrix reference, or analysis "
                "validation protocol from the abstract or orientation; or remove one "
                "analysis-validation claim class such as Artifact readiness claim from "
                "the orientation protocol; introduce a new claim-bearing manuscript "
                "family without adding it to the analysis-validation family coverage "
                "map; or add one curated source-anchor row with an empty source_lane "
                "or source_tier; or add an unsupported measured-performance, p-value, "
                "or proof-language claim whose only citation is a weak source-guide "
                "context row. This evidence manifest must fail."
            ),
        },
    }
    return ArtifactEvidence(payload)


def write_artifact_evidence(project_root: Path) -> tuple[Path, Path, ArtifactEvidence]:
    """Write JSON and Markdown evidence reports under ``output/reports``."""
    root = Path(project_root)
    write_scholarship_quality(root)
    write_source_metadata(root)
    write_claim_calibration(root)
    evidence = collect_artifact_evidence(root)
    reports = root / "output" / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    json_path = reports / "current_artifact_evidence.json"
    md_path = reports / "current_artifact_evidence.md"
    json_path.write_text(json.dumps(evidence.payload, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_artifact_evidence_markdown(evidence), encoding="utf-8")
    return json_path, md_path, evidence


def render_artifact_evidence_markdown(evidence: ArtifactEvidence) -> str:
    """Render the evidence snapshot as a compact Markdown report."""
    payload = evidence.payload
    checks = payload["checks"]
    citations = payload["citations"]
    scholarship = payload["scholarship_quality"]["summary"]
    source_metadata = payload["source_metadata"]["summary"]
    claim_calibration = payload["claim_calibration"]["summary"]
    figures = payload["figures"]
    pdf = payload["pdf"]
    link_audit = pdf["link_audit"]
    lines = [
        "# AGEINT Current Artifact Evidence",
        "",
        "| Measure | Value |",
        "|---|---:|",
        f"| OK | {str(payload['ok']).lower()} |",
        f"| Generated at | {payload['generated_at']} |",
        f"| Generated Markdown files | {citations['generated_markdown_files']} |",
        f"| Generated citation occurrences | {citations['generated_markdown_citation_occurrences']} |",
        f"| Thin claim-bearing files | {scholarship['thin_claim_bearing_files']} |",
        f"| Single-family claim-bearing files | {scholarship['single_source_family_claim_bearing_files']} |",
        f"| SAT method contract | {str(payload['scholarship_quality']['sat_method_contract']['ok']).lower()} |",
        f"| Analysis validation contract | {str(payload['scholarship_quality']['analysis_validation_contract']['ok']).lower()} |",
        f"| Analysis validation lane contract | {str(payload['scholarship_quality']['analysis_validation_lane_contract']['ok']).lower()} |",
        f"| Analysis validation family coverage | {str(payload['scholarship_quality']['analysis_validation_family_coverage']['ok']).lower()} |",
        f"| Source metadata explicit | {str(checks['source_metadata_ok']).lower()} |",
        f"| Source metadata rows | {source_metadata['metadata_records']} |",
        f"| Source metadata fallback rows | {source_metadata['fallback_dependent_row_count']} |",
        f"| Blank source lanes | {source_metadata['blank_source_lane_count']} |",
        f"| Blank source tiers | {source_metadata['blank_source_tier_count']} |",
        f"| Claim calibration pass | {str(checks['claim_calibration_ok']).lower()} |",
        f"| Claim-calibration candidate rows | {claim_calibration['candidate_rows']} |",
        f"| Claim-calibration hard fails | {claim_calibration['hard_fail_rows']} |",
        f"| Claim-calibration review warnings | {claim_calibration['warning_rows']} |",
        f"| Source sections | {citations['source_sections']} |",
        f"| Zero-citation source sections | {citations['source_zero_citation_sections']} |",
        f"| Registered figures | {figures['figure_count']} |",
        f"| Figure quality pass | {str(figures['quality_pass']).lower()} |",
        f"| PDF pages | {pdf['page_count']} |",
        f"| PDF URI links | {link_audit['uri_links']} |",
        f"| Bad PDF link targets | {link_audit['bad_target_count']} |",
        "",
        "## Checks",
        "",
        "| Check | Pass |",
        "|---|---:|",
    ]
    for name, passed in checks.items():
        lines.append(f"| {name.replace('_', ' ')} | {str(passed).lower()} |")
    lines.extend(
        [
            "",
            "## False-Certification Control",
            "",
            f"**Scenario.** {payload['false_certification_control']['scenario']}",
            "",
            f"**Negative control.** {payload['false_certification_control']['negative_control']}",
        ]
    )
    return "\n".join(lines) + "\n"


def _citation_counts(source_summary: Any, generated_rows: list[Any]) -> dict[str, Any]:
    generated_by_family = Counter()
    for row in generated_rows:
        generated_by_family[row.family] += row.citation_count
    return {
        "source_sections": source_summary.section_count,
        "source_citation_occurrences": source_summary.citation_occurrences,
        "source_unique_citation_keys": source_summary.unique_citation_keys,
        "source_zero_citation_sections": source_summary.zero_citation_sections,
        "source_distribution": dict(source_summary.citation_count_distribution),
        "generated_markdown_files": len(generated_rows),
        "generated_markdown_citation_occurrences": sum(row.citation_count for row in generated_rows),
        "generated_by_family": dict(sorted(generated_by_family.items())),
    }


def _figure_summary(registry: dict[str, Any], visual_audit: dict[str, Any]) -> dict[str, Any]:
    rows = registry.get("figures", [])
    kind_counts = Counter(str(row.get("kind", "")) for row in rows)
    return {
        "schema_version": registry.get("schema_version", ""),
        "figure_count": registry.get("figure_count", len(rows)),
        "kind_counts": dict(sorted(kind_counts.items())),
        "quality_audit_path": registry.get("quality_audit_path", ""),
        "quality_pass": visual_audit.get("pass") if visual_audit else False,
        "quality_summary": visual_audit.get("summary", {}),
    }


def _scan_generated_text(project_root: Path) -> list[dict[str, Any]]:
    roots = [
        project_root / "output" / "manuscript",
        project_root / "output" / "pdf" / "_combined_manuscript.md",
        project_root / "output" / "pdf" / "_combined_manuscript.tex",
    ]
    hits: list[dict[str, Any]] = []
    for path in _iter_text_paths(roots):
        text = path.read_text(encoding="utf-8", errors="ignore")
        for pattern in STALE_OUTPUT_PATTERNS:
            for match in re.finditer(pattern, text):
                line_number = text.count("\n", 0, match.start()) + 1
                hits.append(
                    {
                        "path": path.relative_to(project_root).as_posix(),
                        "line": line_number,
                        "pattern": pattern,
                        "match": match.group(0)[:180],
                    }
                )
    return hits


def _iter_text_paths(roots: list[Path]) -> list[Path]:
    paths: list[Path] = []
    for root in roots:
        if root.is_file():
            paths.append(root)
        elif root.is_dir():
            paths.extend(path for path in root.rglob("*.md") if path.is_file())
    return sorted(paths)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


__all__ = [
    "ArtifactEvidence",
    "STALE_OUTPUT_PATTERNS",
    "collect_artifact_evidence",
    "render_artifact_evidence_markdown",
    "write_artifact_evidence",
]
