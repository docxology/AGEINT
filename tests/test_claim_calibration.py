"""Tests for AGEINT claim-calibration and source-strength gates."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from claim_calibration import collect_claim_calibration, render_claim_calibration_markdown
from source_support_strength import SourceSupportProfile, _profile_from_source_guide_row, source_support_strength, support_profiles_for_keys

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _write_markdown(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_claim_calibration_current_generated_output_passes(built_output: Path) -> None:
    report = collect_claim_calibration(built_output / "manuscript", project_root=PROJECT_ROOT)

    assert report.ok is True
    summary = report.payload["summary"]
    assert summary["candidate_rows"] > 0
    assert summary["hard_fail_rows"] == 0
    assert summary["boundary_allowed_rows"] > 0
    assert "empirical_or_evaluation" in summary["claim_class_counts"]
    assert "artifact_readiness" in summary["claim_class_counts"]

    markdown = render_claim_calibration_markdown(report)
    assert "Claim Calibration" in markdown
    assert "Hard-Fail Rows" in markdown
    assert "Source support distribution" in markdown


def test_claim_calibration_flags_unsupported_performance_claim(tmp_path: Path) -> None:
    _write_markdown(tmp_path / "chapter.md", "# Chapter\n\nAGEINT proves measured performance and statistically significant learning gains.\n")

    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)

    assert report.ok is False
    assert report.payload["summary"]["hard_fail_rows"] == 1
    row = report.payload["hard_fail_rows"][0]
    assert row["claim_class"] == "empirical_or_evaluation"
    assert row["disposition"] == "fail"
    assert "direct official, standards, scholarly, law/policy, or source-quality support" in row["fix_hint"]


def test_claim_calibration_rejects_weak_source_only_statistical_claim(tmp_path: Path) -> None:
    _write_markdown(tmp_path / "chapter.md", "# Chapter\n\nA classroom note reports a p-value and statistically significant capability improvement [@ageint053].\n")

    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)

    assert report.ok is False
    row = report.payload["hard_fail_rows"][0]
    assert row["citation_keys"] == ["ageint053"]
    assert row["source_support_profiles"][0]["strength"] in {"practitioner_or_vendor_context", "social_or_video_context", "mirror_or_copy_context", "source_guide_context"}


def test_claim_calibration_allows_explicit_boundary_language(tmp_path: Path) -> None:
    _write_markdown(tmp_path / "chapter.md", "# Chapter\n\nAGEINT is not a benchmark proving measured performance; it is a design and assurance framework [@official_nist_ai_rmf].\n")

    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)

    assert report.ok is True
    assert report.payload["summary"]["boundary_allowed_rows"] == 1
    assert report.payload["rows"][0]["disposition"] == "boundary_allowed"


def test_claim_calibration_allows_negated_benchmark_metadata_language(tmp_path: Path) -> None:
    _write_markdown(
        tmp_path / "source-lane-map.md",
        "# Source Lane Map\n\n"
        "| Lane | Scope |\n"
        "|---|---|\n"
        "| agentic_ai_security_governance | Agentic AI adoption context, not an AGEINT benchmark. |\n"
        "| current_threat_baseline | Public warning context, not operational targeting or AGEINT benchmark evidence. |\n",
    )

    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)

    assert report.ok is True
    assert report.payload["summary"]["candidate_rows"] == 2
    assert report.payload["summary"]["boundary_allowed_rows"] == 2
    assert {row["disposition"] for row in report.payload["rows"]} == {"boundary_allowed"}


def test_claim_calibration_allows_empirical_requirement_lists(tmp_path: Path) -> None:
    _write_markdown(
        tmp_path / "methods.md",
        "# Methods\n\n"
        "Stronger empirical language requires a direct benchmark, study, field "
        "evaluation, incident dataset, or scholarly empirical source.\n\n"
        "Artifact telemetry is not a learning-outcome estimate, operational-performance "
        "benchmark, or universal safety claim.\n\n"
        "The audit fails unsupported proof-language, measured-performance claims, "
        "p-value or significance language, and decorative formalisms.\n",
    )

    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)

    assert report.ok is True
    assert report.payload["summary"]["candidate_rows"] == 3
    assert report.payload["summary"]["boundary_allowed_rows"] == 3
    assert {row["disposition"] for row in report.payload["rows"]} == {"boundary_allowed"}


def test_claim_calibration_skips_headings_with_performance_terms(tmp_path: Path) -> None:
    _write_markdown(tmp_path / "chapter.md", "# Performance and capability vocabulary\n\nThe body states a bounded design reminder [@official_nist_ai_rmf].\n")

    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)

    assert report.ok is True
    assert report.payload["summary"]["candidate_rows"] == 0


def test_claim_calibration_script_reports_json_contract(built_output: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "audit_claim_calibration.py"), "--format", "json"], cwd=PROJECT_ROOT, check=False, capture_output=True, text=True, timeout=180
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["summary"]["hard_fail_rows"] == 0


def test_source_support_strength_classifies_curated_and_source_guide_keys() -> None:
    official = source_support_strength("official_nist_ai_rmf", PROJECT_ROOT)
    scholarly = source_support_strength("scholarly_rethlefsen_2021_prisma_s", PROJECT_ROOT)
    weak = source_support_strength("ageint053", PROJECT_ROOT)

    assert official.strength in {"official_primary", "standard_primary", "source_quality_anchor"}
    assert official.primary_support is True
    assert scholarly.strength == "scholarly_primary"
    assert scholarly.primary_support is True
    assert weak.primary_support is False
    assert weak.weak_context is True


def test_support_profiles_for_keys_preserves_order_and_unknowns() -> None:
    profiles = support_profiles_for_keys(["ageint053", "official_nist_ai_rmf", "missing_key"], PROJECT_ROOT)

    assert [profile.key for profile in profiles] == ["ageint053", "official_nist_ai_rmf", "missing_key"]
    assert all(isinstance(profile, SourceSupportProfile) for profile in profiles)
    assert profiles[-1].strength == "unknown"
    assert profiles[-1].weak_context is True


def test_unknown_official_looking_key_cannot_validate_a_performance_claim(tmp_path: Path) -> None:
    key = "official_nonexistent_review_fixture"
    _write_markdown(tmp_path / "chapter.md", f"# Challenge\n\nThis proves statistically significant analytic accuracy [@{key}].\n")

    support = source_support_strength(key, PROJECT_ROOT)
    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)

    assert support.strength == "unknown"
    assert support.primary_support is False
    assert report.ok is False
    assert report.payload["hard_fail_rows"][0]["citation_keys"] == [key]


def test_verified_editorial_annotation_does_not_establish_a_primary_source_lane() -> None:
    profile = _profile_from_source_guide_row("ageint999", {"url": "https://example.org/editorial", "title": "Editorial note", "note_verified": True})
    assert profile.primary_support is False
    assert profile.strength == "source_guide_context"


def test_negated_proof_is_not_an_unsupported_positive_claim(tmp_path: Path) -> None:
    _write_markdown(tmp_path / "limits.md", "Neither source agreement nor a valid signature proves factual truth.\n")
    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)
    assert report.ok is True
    assert report.payload["rows"][0]["disposition"] == "boundary_allowed"


def test_boundary_in_one_clause_does_not_hide_a_positive_claim(tmp_path: Path) -> None:
    for text in (
        "This is not a benchmark. The workbook proves statistically significant accuracy.",
        "This is not a benchmark, but it proves measured performance.",
        "This is not only a benchmark; it proves learning gains.",
    ):
        _write_markdown(tmp_path / "mixed.md", text + "\n")
        report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)
        assert report.ok is False
        assert report.payload["rows"][0]["disposition"] == "fail"


def test_reported_bad_answer_does_not_waive_an_endorsed_claim(tmp_path: Path) -> None:
    quoted = "A fictional input record claims 'the policy proves automated accuracy'."
    path = tmp_path / "exercise.md"
    _write_markdown(path, quoted + "\n")
    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)
    assert report.payload["rows"][0]["disposition"] == "review"
    _write_markdown(path, quoted + " The workbook proves learning gains.\n")
    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)
    assert report.ok is False


def test_conditional_observation_does_not_validate_its_consequent(tmp_path: Path) -> None:
    path = tmp_path / "condition.md"
    _write_markdown(path, "If the notice proves incomplete, withhold the accuracy judgment.\n")
    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)
    assert report.payload["rows"][0]["disposition"] == "review"
    _write_markdown(path, "If the notice proves incomplete, this proves measured performance.\n")
    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)
    assert report.ok is False


def test_soft_wrap_preserves_negation_but_not_an_asserted_following_sentence(tmp_path: Path) -> None:
    path = tmp_path / "wrapped.md"
    _write_markdown(path, "Do not\npromote the artifact into proof of autonomous accuracy.\n")
    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)
    assert report.ok is True
    _write_markdown(path, "Do not\npromote the artifact into proof of autonomous accuracy.\nThis proves learning gains.\n")
    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)
    assert report.ok is False


def test_misconception_is_not_endorsed_and_cannot_mask_a_new_assertion(tmp_path: Path) -> None:
    path = tmp_path / "misconception.md"
    prompt = "Correct the misconception about **Theory vs. measurement**: that an indicator proves an incident."
    _write_markdown(path, prompt + "\n")
    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)
    assert report.payload["rows"][0]["disposition"] == "review"
    _write_markdown(path, prompt + " The classroom trial proves measured performance.\n")
    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)
    assert report.ok is False


def test_postverbal_neither_does_not_waive_a_claim_of_no_effect(tmp_path: Path) -> None:
    path = tmp_path / "negation.md"
    _write_markdown(path, "A missing timestamp proves neither age nor falsity.\n")
    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)
    assert report.payload["rows"][0]["disposition"] == "boundary_allowed"
    _write_markdown(path, "The trial proves no effect.\n")
    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)
    assert report.ok is False


def test_stop_instruction_is_not_a_certificate_for_a_stop_device(tmp_path: Path) -> None:
    path = tmp_path / "stop.md"
    _write_markdown(path, "Stop any inference that a vendor badge proves compliance.\n")
    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)
    assert report.payload["rows"][0]["disposition"] == "boundary_allowed"
    _write_markdown(path, "The emergency stop proves measured performance.\n")
    report = collect_claim_calibration(tmp_path, project_root=PROJECT_ROOT)
    assert report.ok is False


def test_primary_lane_uses_hostname_boundaries_not_publisher_suffix_lookalikes() -> None:
    lookalike = _profile_from_source_guide_row("ageint999", {"url": "https://notnature.com/article", "note_verified": True})
    publisher = _profile_from_source_guide_row("ageint998", {"url": "https://www.nature.com/article", "note_verified": True})
    official = _profile_from_source_guide_row("ageint997", {"url": "https://records.example.gov:443/policy", "note_verified": True})
    assert lookalike.primary_support is False
    assert publisher.primary_support is True
    assert official.primary_support is True
