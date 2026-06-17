"""Tests for the current AGEINT artifact-evidence manifest."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from artifact_evidence import (
    ArtifactEvidence,
    _citation_counts,
    _figure_summary,
    _pdf_report_payload,
    _scan_generated_text,
    collect_artifact_evidence,
    render_artifact_evidence_markdown,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_artifact_evidence_report_contract_for_current_outputs() -> None:
    pdf = PROJECT_ROOT / "output" / "pdf" / "AGEINT_combined.pdf"
    if not pdf.is_file():
        pytest.skip("Rendered combined PDF not present")

    evidence = collect_artifact_evidence(PROJECT_ROOT)
    payload = evidence.payload

    assert payload["project"] == "AGEINT"
    assert payload["schema_version"] == "1.0"
    assert len(payload["audit_contracts"]) >= len(payload["checks"])
    assert set(payload["checks"]) >= {
        "generated_output_fresh",
        "rendered_references_resolve",
        "reference_quality_ok",
        "stale_output_scans_clean",
        "pdf_quality_ok",
        "figure_quality_ok",
        "citation_source_sections_covered",
        "scholarship_quality_ok",
        "source_metadata_ok",
        "source_refresh_due_ok",
        "claim_calibration_ok",
        "agency_source_coverage_ok",
    }
    assert payload["citations"]["source_sections"] >= 700
    assert payload["citations"]["source_zero_citation_sections"] == 0
    assert payload["scholarship_quality"]["summary"]["thin_claim_bearing_files"] == 0
    assert payload["scholarship_quality"]["sat_method_contract"]["ok"] is True
    assert payload["scholarship_quality"]["analysis_validation_contract"]["ok"] is True
    assert payload["scholarship_quality"]["analysis_validation_lane_contract"]["ok"] is True
    assert payload["scholarship_quality"]["analysis_validation_family_coverage"]["ok"] is True
    assert payload["scholarship_quality"]["summary"]["source_family_mentions"]["source_guide"] > 0
    assert payload["source_metadata"]["summary"]["metadata_records"] == 472
    assert payload["source_metadata"]["summary"]["intelligence_anchor_count"] == 462
    assert payload["source_metadata"]["summary"]["source_quality_anchor_count"] == 10
    assert payload["source_metadata"]["summary"]["fallback_dependent_row_count"] == 0
    assert payload["source_metadata"]["summary"]["blank_source_lane_count"] == 0
    assert payload["source_metadata"]["summary"]["blank_source_tier_count"] == 0
    assert payload["source_refresh_due"]["summary"]["row_count"] == 472
    assert payload["source_refresh_due"]["summary"]["due_or_stale_count"] == 0
    assert payload["source_refresh_due"]["summary"]["missing_checked_as_of_count"] == 0
    assert payload["source_refresh_due"]["issue_row_count"] == 0
    assert payload["claim_calibration"]["summary"]["hard_fail_rows"] == 0
    assert payload["agency_source_coverage"]["summary"]["new_official_us_ic_anchor_count"] == 56
    assert payload["agency_source_coverage"]["summary"]["unrouted_new_anchor_count"] == 0
    assert payload["reference_quality"]["summary"]["issue_count"] == 0
    assert payload["reference_quality"]["summary"]["generic_heading_issues"] == 0
    assert payload["reference_quality"]["summary"]["citation_context_issues"] == 0
    assert payload["claim_calibration"]["summary"]["candidate_rows"] > 0
    assert payload["figures"]["figure_count"] >= 160
    assert payload["pdf"]["link_audit"]["bad_target_count"] == 0
    assert payload["pdf"]["pdf_path"] == "output/pdf/AGEINT_combined.pdf"
    assert payload["rendered_references"]["violation_count"] == 0
    assert payload["generated_output_scan"]["hit_count"] == 0
    assert all(contract["negative_control"] for contract in payload["audit_contracts"])
    assert {
        contract["check_id"] for contract in payload["audit_contracts"]
    } >= set(payload["checks"])

    markdown = render_artifact_evidence_markdown(evidence)
    assert "False-Certification Control" in markdown
    assert "Audit Contract Negative Controls" in markdown
    assert "Generated citation occurrences" in markdown
    assert "Thin claim-bearing files" in markdown
    assert "Source metadata explicit" in markdown
    assert "Source refresh due pass" in markdown
    assert "Claim calibration pass" in markdown
    assert "Reference quality pass" in markdown


def test_audit_artifact_evidence_script_writes_json_contract() -> None:
    pdf = PROJECT_ROOT / "output" / "pdf" / "AGEINT_combined.pdf"
    if not pdf.is_file():
        pytest.skip("Rendered combined PDF not present")

    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "audit_artifact_evidence.py"),
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
    assert payload["pdf"]["link_audit"]["ok"] is True
    assert payload["checks"]["scholarship_quality_ok"] is True
    assert payload["checks"]["source_metadata_ok"] is True
    assert payload["checks"]["source_refresh_due_ok"] is True
    assert payload["checks"]["claim_calibration_ok"] is True
    assert payload["checks"]["agency_source_coverage_ok"] is True
    assert payload["checks"]["reference_quality_ok"] is True
    assert payload["scholarship_quality"]["sat_method_contract"]["checked"] is True
    assert payload["scholarship_quality"]["analysis_validation_contract"]["checked"] is True
    assert payload["scholarship_quality"]["analysis_validation_lane_contract"]["checked"] is True
    assert payload["scholarship_quality"]["analysis_validation_family_coverage"]["checked"] is True
    assert (PROJECT_ROOT / "output" / "reports" / "current_artifact_evidence.json").is_file()
    assert (PROJECT_ROOT / "output" / "reports" / "current_artifact_evidence.md").is_file()
    assert (PROJECT_ROOT / "output" / "reports" / "scholarship_quality.json").is_file()
    assert (PROJECT_ROOT / "output" / "reports" / "source_metadata.json").is_file()
    assert (PROJECT_ROOT / "output" / "reports" / "source_refresh_due.json").is_file()
    assert (PROJECT_ROOT / "output" / "reports" / "claim_calibration.json").is_file()
    assert (PROJECT_ROOT / "output" / "reports" / "reference_quality.json").is_file()


def test_artifact_evidence_markdown_renders_preflight_sections_without_pdf() -> None:
    evidence = ArtifactEvidence(
        {
            "ok": True,
            "generated_at": "2026-06-14T00:00:00+00:00",
            "checks": {
                "generated_output_fresh": True,
                "rendered_references_resolve": True,
                "reference_quality_ok": True,
                "stale_output_scans_clean": True,
                "pdf_quality_ok": True,
                "figure_quality_ok": True,
                "citation_source_sections_covered": True,
                "scholarship_quality_ok": True,
                "source_metadata_ok": True,
                "source_refresh_due_ok": True,
                "claim_calibration_ok": True,
                "agency_source_coverage_ok": True,
            },
            "citations": {
                "generated_markdown_files": 3,
                "generated_markdown_citation_occurrences": 8,
                "source_sections": 2,
                "source_zero_citation_sections": 0,
            },
            "scholarship_quality": {
                "summary": {
                    "thin_claim_bearing_files": 0,
                    "single_source_family_claim_bearing_files": 0,
                },
                "sat_method_contract": {"ok": True},
                "analysis_validation_contract": {"ok": True},
                "analysis_validation_lane_contract": {"ok": True},
                "analysis_validation_family_coverage": {"ok": True},
            },
            "source_metadata": {
                "summary": {
                    "metadata_records": 472,
                    "fallback_dependent_row_count": 0,
                    "blank_source_lane_count": 0,
                    "blank_source_tier_count": 0,
                }
            },
            "source_refresh_due": {
                "summary": {
                    "due_or_stale_count": 0,
                    "missing_checked_as_of_count": 0,
                }
            },
            "claim_calibration": {
                "summary": {
                    "candidate_rows": 12,
                    "hard_fail_rows": 0,
                    "warning_rows": 3,
                }
            },
            "agency_source_coverage": {
                "summary": {
                    "new_official_us_ic_anchor_count": 56,
                    "missing_required_metadata_count": 0,
                    "unrouted_new_anchor_count": 0,
                }
            },
            "reference_quality": {
                "summary": {
                    "issue_count": 0,
                    "generic_heading_issues": 0,
                    "citation_context_issues": 0,
                },
                "issue_rows": [],
                "negative_control": "Fixture reference-quality negative control.",
            },
            "figures": {"figure_count": 177, "quality_pass": True},
            "pdf": {"page_count": 10, "link_audit": {"uri_links": 4, "bad_target_count": 0}},
            "false_certification_control": {
                "scenario": "Fixture scenario.",
                "negative_control": "Fixture negative control.",
            },
            "audit_contracts": [
                {
                    "contract_id": "fixture",
                    "check_id": "source_metadata_ok",
                    "negative_control": "Fixture negative control.",
                }
            ],
        }
    )

    markdown = render_artifact_evidence_markdown(evidence)

    assert "False-Certification Control" in markdown
    assert "Source refresh due pass" in markdown
    assert "Claim calibration pass" in markdown


def test_artifact_evidence_helpers_cover_pre_render_fixture_paths(tmp_path: Path) -> None:
    class SourceSummary:
        section_count = 2
        citation_occurrences = 3
        unique_citation_keys = 2
        zero_citation_sections = 0
        citation_count_distribution = {1: 1, 2: 1}

    class GeneratedRow:
        def __init__(self, family: str, citation_count: int) -> None:
            self.family = family
            self.citation_count = citation_count

    counts = _citation_counts(SourceSummary(), [GeneratedRow("abstract", 2), GeneratedRow("abstract", 1)])
    assert counts["generated_by_family"] == {"abstract": 3}
    assert counts["source_zero_citation_sections"] == 0

    figures = _figure_summary(
        {
            "schema_version": "1.5",
            "figure_count": 2,
            "quality_audit_path": "output/figures/visual_quality_audit.json",
            "figures": [{"kind": "python"}, {"kind": "mermaid"}],
        },
        {"pass": True, "summary": {"readable_pngs": 2}},
    )
    assert figures["kind_counts"] == {"mermaid": 1, "python": 1}
    assert figures["quality_pass"] is True

    pdf_payload = _pdf_report_payload(
        {"pdf_path": str(tmp_path / "output" / "pdf" / "AGEINT_combined.pdf")},
        tmp_path,
    )
    assert pdf_payload["pdf_path"] == "output/pdf/AGEINT_combined.pdf"

    manuscript = tmp_path / "output" / "manuscript" / "fixture.md"
    manuscript.parent.mkdir(parents=True)
    manuscript.write_text("See [stale](chapter.md).\n", encoding="utf-8")
    hits = _scan_generated_text(tmp_path)
    assert hits[0]["path"] == "output/manuscript/fixture.md"
    assert hits[0]["pattern"] == r"\]\([^)]*\.md\)"
