"""Tests for the current AGEINT artifact-evidence manifest."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from artifact_evidence import _citation_counts, _figure_summary, _pdf_report_payload, _scan_generated_text, collect_artifact_evidence

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_artifact_evidence_report_contract_for_current_outputs() -> None:
    pdf = PROJECT_ROOT / "output" / "pdf" / "AGEINT_combined.pdf"
    if not pdf.is_file():
        pytest.skip("Rendered combined PDF not present")

    evidence = collect_artifact_evidence(PROJECT_ROOT)
    payload = evidence.payload

    assert payload["project"] == "AGEINT"
    assert payload["schema_version"] == "1.0"
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
    assert payload["source_metadata"]["summary"]["fallback_dependent_row_count"] == 0
    assert payload["source_metadata"]["summary"]["blank_source_lane_count"] == 0
    assert payload["source_metadata"]["summary"]["blank_source_tier_count"] == 0
    assert payload["source_refresh_due"]["summary"]["due_or_stale_count"] == 0
    assert payload["source_refresh_due"]["summary"]["missing_checked_as_of_count"] == 0
    assert payload["source_refresh_due"]["issue_row_count"] == 0
    assert payload["claim_calibration"]["summary"]["hard_fail_rows"] == 0
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
    assert {contract["check_id"] for contract in payload["audit_contracts"]} >= set(payload["checks"])



def test_audit_artifact_evidence_script_reports_json_contract() -> None:
    pdf = PROJECT_ROOT / "output" / "pdf" / "AGEINT_combined.pdf"
    if not pdf.is_file():
        pytest.skip("Rendered combined PDF not present")

    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "audit_artifact_evidence.py"), "--format", "json"], cwd=PROJECT_ROOT, check=False, capture_output=True, text=True, timeout=900
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
        {"schema_version": "1.5", "figure_count": 2, "quality_audit_path": "output/figures/visual_quality_audit.json", "figures": [{"kind": "python"}, {"kind": "mermaid"}]},
        {"pass": True, "summary": {"readable_pngs": 2}},
    )
    assert figures["kind_counts"] == {"mermaid": 1, "python": 1}
    assert figures["quality_pass"] is True

    pdf_payload = _pdf_report_payload({"pdf_path": str(tmp_path / "output" / "pdf" / "AGEINT_combined.pdf")}, tmp_path)
    assert pdf_payload["pdf_path"] == "output/pdf/AGEINT_combined.pdf"

    manuscript = tmp_path / "output" / "manuscript" / "fixture.md"
    manuscript.parent.mkdir(parents=True)
    manuscript.write_text("See [stale](chapter.md).\n", encoding="utf-8")
    hits = _scan_generated_text(tmp_path)
    assert hits[0]["path"] == "output/manuscript/fixture.md"
    assert hits[0]["pattern"] == r"\]\([^)]*\.md\)"
