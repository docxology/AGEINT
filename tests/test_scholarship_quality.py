"""Tests for the AGEINT scholarship-quality verifier."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from intelligence_content import INTELLIGENCE_RESEARCH_ANCHORS
from scholarship_quality import (
    ANALYSIS_VALIDATION_CONTRACT_REQUIREMENTS,
    ANALYSIS_VALIDATION_LANE_REQUIREMENTS,
    SAT_METHOD_CONTRACT_REQUIREMENTS,
    ScholarshipQualityRow,
    _analysis_validation_family_coverage,
    citation_source_family,
    collect_scholarship_quality,
    render_scholarship_quality_markdown,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _write_overview(root: Path, text: str) -> None:
    path = root / "parts" / "unit" / "chapter" / "02-overview.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_scholarship_quality_current_generated_output_passes(built_output: Path) -> None:
    report = collect_scholarship_quality(built_output / "manuscript")
    summary = report.payload["summary"]

    assert report.ok is True
    assert summary["generated_markdown_files"] >= 330
    assert summary["claim_bearing_files"] >= 250
    assert summary["uncited_claim_bearing_files"] == 0
    assert summary["thin_claim_bearing_files"] == 0
    assert (
        summary["single_source_family_claim_bearing_files"]
        == report.payload["warning_row_count"]
    )
    if report.payload["warning_rows"]:
        assert report.payload["warning_rows"][0]["flags"] == [
            "single_source_family_claim_bearing"
        ]
    assert summary["source_family_mentions"]["source_guide"] > 0
    assert summary["source_family_mentions"]["official"] > 0
    assert summary["source_family_mentions"]["scholarly"] > 0
    assert summary["source_family_mentions"]["standard"] > 0
    assert report.payload["sat_method_contract"]["ok"] is True
    assert report.payload["sat_method_contract"]["checked"] is True
    assert report.payload["analysis_validation_contract"]["ok"] is True
    assert report.payload["analysis_validation_contract"]["checked"] is True
    assert report.payload["analysis_validation_lane_contract"]["ok"] is True
    assert report.payload["analysis_validation_lane_contract"]["checked"] is True
    assert report.payload["analysis_validation_family_coverage"]["ok"] is True
    assert report.payload["analysis_validation_family_coverage"]["checked"] is True
    assert report.payload["analysis_validation_family_coverage"]["missing_families"] == []

    markdown = render_scholarship_quality_markdown(report)
    assert "Source-Family Mentions" in markdown
    assert "Single-family claim-bearing files" in markdown
    assert "Synthetic Analytic Tradecraft Method Contract" in markdown
    assert "Analysis Validation Contract" in markdown
    assert "Analysis Validation Lane Contract" in markdown
    assert "Analysis Validation Family Coverage" in markdown


def test_scholarship_quality_flags_thin_claim_bearing_negative_control(tmp_path: Path) -> None:
    _write_overview(tmp_path, "# Thin overview\n\nA claim-bearing sentence [@ageint001].\n")

    report = collect_scholarship_quality(tmp_path)

    assert report.ok is False
    assert report.payload["summary"]["thin_claim_bearing_files"] == 1
    assert report.payload["hard_fail_rows"][0]["flags"] == ["thin_claim_bearing"]


def test_scholarship_quality_warns_for_single_family_without_failing(tmp_path: Path) -> None:
    _write_overview(
        tmp_path,
        "# Single-family overview\n\n"
        "A supported sentence [@official_nist_ai_rmf]; [@official_nist_ai_600_1].\n",
    )

    report = collect_scholarship_quality(tmp_path)

    assert report.ok is True
    assert report.payload["summary"]["thin_claim_bearing_files"] == 0
    assert report.payload["summary"]["single_source_family_claim_bearing_files"] == 1
    assert report.payload["warning_rows"][0]["flags"] == ["single_source_family_claim_bearing"]


def test_scholarship_quality_flags_broken_sat_method_contract(tmp_path: Path) -> None:
    (tmp_path / "abstract.md").write_text("# Abstract\n\nSynthetic framing without method figure.\n", encoding="utf-8")
    (tmp_path / "orientation.md").write_text(
        "# Orientation\n\n"
        "## Synthetic Analytic Tradecraft thesis: synthetic fixtures, source discipline, "
        "and reviewable claims {#sec:synthetic-analytic-tradecraft-thesis}\n",
        encoding="utf-8",
    )

    report = collect_scholarship_quality(tmp_path)

    assert report.ok is False
    assert report.payload["sat_method_contract"]["checked"] is True
    missing = {(row["path"], row["term"]) for row in report.payload["sat_method_contract"]["missing"]}
    assert ("abstract", "[@fig:ageint-synthetic-tradecraft-method-contract]") in missing
    assert ("orientation", "source-family triangulation") in missing
    assert len(missing) >= len(SAT_METHOD_CONTRACT_REQUIREMENTS) - 1


def test_scholarship_quality_flags_broken_analysis_validation_contract(tmp_path: Path) -> None:
    (tmp_path / "abstract.md").write_text(
        "# Abstract\n\nSynthetic Analytic Tradecraft is synthetic in its fixtures, not in its standards "
        "[@fig:ageint-synthetic-tradecraft-method-contract].\n",
        encoding="utf-8",
    )
    (tmp_path / "orientation.md").write_text(
        "# Orientation\n\n"
        "## Synthetic Analytic Tradecraft thesis: synthetic fixtures, source discipline, "
        "and reviewable claims {#sec:synthetic-analytic-tradecraft-thesis}\n\n"
        "source-family triangulation and negative-control testing "
        "[@fig:ageint-synthetic-tradecraft-method-contract].\n",
        encoding="utf-8",
    )

    report = collect_scholarship_quality(tmp_path)

    assert report.ok is False
    assert report.payload["analysis_validation_contract"]["checked"] is True
    missing = {(row["path"], row["term"]) for row in report.payload["analysis_validation_contract"]["missing"]}
    assert ("abstract", "[@fig:ageint-analysis-validation-matrix]") in missing
    assert ("orientation", "{#sec:analysis-validation-protocol}") in missing
    assert len(missing) == len(ANALYSIS_VALIDATION_CONTRACT_REQUIREMENTS)


def test_scholarship_quality_flags_incomplete_analysis_validation_lanes(tmp_path: Path) -> None:
    (tmp_path / "abstract.md").write_text(
        "# Abstract\n\nSynthetic Analytic Tradecraft is synthetic in its fixtures, not in its standards "
        "[@fig:ageint-synthetic-tradecraft-method-contract]. The matrix "
        "[@fig:ageint-analysis-validation-matrix] exists.\n",
        encoding="utf-8",
    )
    (tmp_path / "orientation.md").write_text(
        "# Orientation\n\n"
        "## Synthetic Analytic Tradecraft thesis: synthetic fixtures, source discipline, "
        "and reviewable claims {#sec:synthetic-analytic-tradecraft-thesis}\n\n"
        "source-family triangulation and negative-control testing "
        "[@fig:ageint-synthetic-tradecraft-method-contract].\n\n"
        "## Analysis validation protocol: claim classes, evidence packets, and failure "
        "modes {#sec:analysis-validation-protocol}\n\n"
        "The analysis validation matrix [@fig:ageint-analysis-validation-matrix] has a table.\n\n"
        "| Claim class | Validation question | Required evidence | Failure mode |\n"
        "|---|---|---|---|\n"
        "| Design guidance | Is the claim framed as proposed guidance rather than measured performance? | "
        "source-family support, caveat, and bounded conclusion | "
        "architecture prose is promoted into empirical proof |\n",
        encoding="utf-8",
    )

    report = collect_scholarship_quality(tmp_path)

    assert report.ok is False
    assert report.payload["analysis_validation_contract"]["ok"] is True
    assert report.payload["analysis_validation_lane_contract"]["checked"] is True
    missing = {(row["path"], row["term"]) for row in report.payload["analysis_validation_lane_contract"]["missing"]}
    assert ("orientation", "Artifact readiness claim") in missing
    assert ("orientation", "stale output or Markdown-file links certify as ready") in missing
    assert len(missing) >= len(ANALYSIS_VALIDATION_LANE_REQUIREMENTS) - 4


def test_analysis_validation_family_coverage_flags_unmapped_claim_family() -> None:
    row = ScholarshipQualityRow(
        path="parts/example/new-section.md",
        family="new-claim-family",
        citation_count=2,
        unique_citation_count=2,
        citation_keys=("ageint001", "official_nist_ai_rmf"),
        source_families=("source_guide", "official"),
        flags=(),
    )
    original = set(__import__("scholarship_quality").CLAIM_BEARING_FAMILIES)
    patched = frozenset(original | {"new-claim-family"})
    module = __import__("scholarship_quality")
    previous = module.CLAIM_BEARING_FAMILIES
    try:
        module.CLAIM_BEARING_FAMILIES = patched
        coverage = _analysis_validation_family_coverage([row])
    finally:
        module.CLAIM_BEARING_FAMILIES = previous

    assert coverage["ok"] is False
    assert coverage["missing_families"] == ["new-claim-family"]


def test_citation_source_family_classifies_existing_anchor_keys() -> None:
    anchor_map = {anchor.key: anchor for anchor in INTELLIGENCE_RESEARCH_ANCHORS}

    assert citation_source_family("ageint001", anchor_map) == "source_guide"
    assert citation_source_family("official_nist_fips_197_aes", anchor_map) == "standard"
    assert citation_source_family("official_nist_ai_rmf", anchor_map) == "official"
    assert citation_source_family("scholarly_rethlefsen_2021_prisma_s", anchor_map) == "scholarly"


def test_audit_scholarship_quality_script_writes_json_contract(built_output: Path) -> None:
    assert (built_output / "manuscript").is_dir()
    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "audit_scholarship_quality.py"),
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
    assert payload["summary"]["thin_claim_bearing_files"] == 0
    assert payload["analysis_validation_lane_contract"]["ok"] is True
    assert payload["analysis_validation_family_coverage"]["ok"] is True
    assert (PROJECT_ROOT / "output" / "reports" / "scholarship_quality.json").is_file()
    assert (PROJECT_ROOT / "output" / "reports" / "scholarship_quality.md").is_file()
