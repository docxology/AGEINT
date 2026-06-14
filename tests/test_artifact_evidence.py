"""Tests for the current AGEINT artifact-evidence manifest."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from artifact_evidence import collect_artifact_evidence, render_artifact_evidence_markdown

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
        "stale_output_scans_clean",
        "pdf_quality_ok",
        "figure_quality_ok",
        "citation_source_sections_covered",
        "scholarship_quality_ok",
        "source_metadata_ok",
        "claim_calibration_ok",
    }
    assert payload["citations"]["source_sections"] >= 700
    assert payload["citations"]["source_zero_citation_sections"] == 0
    assert payload["scholarship_quality"]["summary"]["thin_claim_bearing_files"] == 0
    assert payload["scholarship_quality"]["sat_method_contract"]["ok"] is True
    assert payload["scholarship_quality"]["analysis_validation_contract"]["ok"] is True
    assert payload["scholarship_quality"]["analysis_validation_lane_contract"]["ok"] is True
    assert payload["scholarship_quality"]["analysis_validation_family_coverage"]["ok"] is True
    assert payload["scholarship_quality"]["summary"]["source_family_mentions"]["source_guide"] > 0
    assert payload["source_metadata"]["summary"]["metadata_records"] == 258
    assert payload["source_metadata"]["summary"]["intelligence_anchor_count"] == 248
    assert payload["source_metadata"]["summary"]["source_quality_anchor_count"] == 10
    assert payload["source_metadata"]["summary"]["fallback_dependent_row_count"] == 0
    assert payload["source_metadata"]["summary"]["blank_source_lane_count"] == 0
    assert payload["source_metadata"]["summary"]["blank_source_tier_count"] == 0
    assert payload["claim_calibration"]["summary"]["hard_fail_rows"] == 0
    assert payload["claim_calibration"]["summary"]["candidate_rows"] > 0
    assert payload["figures"]["figure_count"] >= 160
    assert payload["pdf"]["link_audit"]["bad_target_count"] == 0
    assert payload["rendered_references"]["violation_count"] == 0
    assert payload["generated_output_scan"]["hit_count"] == 0

    markdown = render_artifact_evidence_markdown(evidence)
    assert "False-Certification Control" in markdown
    assert "Generated citation occurrences" in markdown
    assert "Thin claim-bearing files" in markdown
    assert "Source metadata explicit" in markdown
    assert "Claim calibration pass" in markdown


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
    assert payload["checks"]["claim_calibration_ok"] is True
    assert payload["scholarship_quality"]["sat_method_contract"]["checked"] is True
    assert payload["scholarship_quality"]["analysis_validation_contract"]["checked"] is True
    assert payload["scholarship_quality"]["analysis_validation_lane_contract"]["checked"] is True
    assert payload["scholarship_quality"]["analysis_validation_family_coverage"]["checked"] is True
    assert (PROJECT_ROOT / "output" / "reports" / "current_artifact_evidence.json").is_file()
    assert (PROJECT_ROOT / "output" / "reports" / "current_artifact_evidence.md").is_file()
    assert (PROJECT_ROOT / "output" / "reports" / "scholarship_quality.json").is_file()
    assert (PROJECT_ROOT / "output" / "reports" / "source_metadata.json").is_file()
    assert (PROJECT_ROOT / "output" / "reports" / "claim_calibration.json").is_file()
