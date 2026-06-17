"""Tests for the generated AGEINT visual-quality audit artifact."""

from __future__ import annotations

import json
from pathlib import Path

from analysis_validation import (
    ANALYSIS_VALIDATION_LANES,
    analysis_validation_family_rows,
    analysis_validation_matrix_rows,
)
from curriculum import load_curriculum
from figures import FigureKind, load_figure_registry, render_figures
from manuscript_manifest import build_manuscript_manifest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"


def test_visual_quality_audit_matches_rendered_registry() -> None:
    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)
    registry_path = render_figures(
        PROJECT_ROOT,
        curriculum,
        manifest,
        allow_placeholder_figures=True,
    )
    registry = load_figure_registry(registry_path)
    audit_path = PROJECT_ROOT / registry["quality_audit_path"]
    audit = json.loads(audit_path.read_text(encoding="utf-8"))

    assert audit["project"] == "AGEINT"
    assert audit["schema_version"] == "1.0"
    assert audit["registry_schema"] == registry["schema_version"] == "1.5"
    assert audit["figure_count"] == registry["figure_count"] >= 170
    assert audit["pass"] is True
    assert registry["quality_summary"] == audit["summary"]
    assert audit["summary"]["kind_counts"] == {
        FigureKind.AI_GENERATED.value: 6,
        FigureKind.HISTORICAL.value: 4,
        FigureKind.MERMAID.value: 115,
        FigureKind.PYTHON.value: 52,
    }
    for check, count in audit["summary"]["check_counts"].items():
        assert count == audit["figure_count"], check
    assert audit["summary"]["min_caption_words"] >= 40
    assert audit["summary"]["min_alt_text_words"] >= 24
    assert audit["summary"]["min_long_description_words"] >= 70
    assert audit["summary"]["max_aspect_ratio"] <= 1.1
    assert audit["summary"]["quantitative_figures"] > 0
    assert audit["summary"]["conceptual_figures"] > 0
    assert audit["summary"]["missing_visual_semantics"] == 0


def test_visual_quality_dashboard_is_registry_backed() -> None:
    registry = load_figure_registry(PROJECT_ROOT / "output/figures/figure_registry.json")
    dashboard = next(
        entry
        for entry in registry["figures"]
        if entry["label"] == "fig:ageint-visual-quality-audit-dashboard"
    )
    assert dashboard["kind"] == FigureKind.PYTHON.value
    assert dashboard["provenance"]["renderer_id"] == "visual_quality_audit_dashboard"
    assert "visual_quality_audit.json" in dashboard["caption"]
    assert (PROJECT_ROOT / dashboard["output_path"]).is_file()


def test_artifact_evidence_control_loop_is_registry_backed() -> None:
    registry = load_figure_registry(PROJECT_ROOT / "output/figures/figure_registry.json")
    figure = next(
        entry
        for entry in registry["figures"]
        if entry["label"] == "fig:ageint-artifact-evidence-control-loop"
    )
    assert figure["kind"] == FigureKind.PYTHON.value
    assert figure["provenance"]["renderer_id"] == "artifact_evidence_control_loop"
    assert "current evidence reports" in figure["caption"]
    assert (PROJECT_ROOT / figure["output_path"]).is_file()


def test_scholarship_triangulation_map_is_registry_backed() -> None:
    registry = load_figure_registry(PROJECT_ROOT / "output/figures/figure_registry.json")
    figure = next(
        entry
        for entry in registry["figures"]
        if entry["label"] == "fig:ageint-scholarship-triangulation-map"
    )
    assert figure["kind"] == FigureKind.PYTHON.value
    assert figure["provenance"]["renderer_id"] == "scholarship_triangulation_map"
    assert "scholarship triangulation map" in figure["caption"].lower()
    assert (PROJECT_ROOT / figure["output_path"]).is_file()


def test_synthetic_tradecraft_method_contract_is_registry_backed() -> None:
    registry = load_figure_registry(PROJECT_ROOT / "output/figures/figure_registry.json")
    figure = next(
        entry
        for entry in registry["figures"]
        if entry["label"] == "fig:ageint-synthetic-tradecraft-method-contract"
    )
    assert figure["kind"] == FigureKind.PYTHON.value
    assert figure["provenance"]["renderer_id"] == "synthetic_tradecraft_method_contract"
    assert "method commitments rather than prestige language" in figure["caption"]
    assert (PROJECT_ROOT / figure["output_path"]).is_file()


def test_analysis_validation_matrix_is_registry_backed() -> None:
    registry = load_figure_registry(PROJECT_ROOT / "output/figures/figure_registry.json")
    figure = next(
        entry
        for entry in registry["figures"]
        if entry["label"] == "fig:ageint-analysis-validation-matrix"
    )
    assert figure["kind"] == FigureKind.PYTHON.value
    assert figure["provenance"]["renderer_id"] == "analysis_validation_matrix"
    assert "claims reviewable by class" in figure["caption"]
    assert [row[0] for row in analysis_validation_matrix_rows()] == [
        lane.claim_class for lane in ANALYSIS_VALIDATION_LANES
    ]
    assert "Artifact readiness claim" in {lane.claim_class for lane in ANALYSIS_VALIDATION_LANES}
    assert (PROJECT_ROOT / figure["output_path"]).is_file()


def test_analysis_validation_family_coverage_is_registry_backed() -> None:
    registry = load_figure_registry(PROJECT_ROOT / "output/figures/figure_registry.json")
    figure = next(
        entry
        for entry in registry["figures"]
        if entry["label"] == "fig:ageint-analysis-validation-family-coverage"
    )
    assert figure["kind"] == FigureKind.PYTHON.value
    assert figure["provenance"]["renderer_id"] == "analysis_validation_family_coverage"
    assert "claim-bearing manuscript family" in figure["caption"]
    assert "method-assurance-reference.md" in {row[0] for row in analysis_validation_family_rows()}
    assert (PROJECT_ROOT / figure["output_path"]).is_file()


def test_source_metadata_integrity_is_registry_backed() -> None:
    registry = load_figure_registry(PROJECT_ROOT / "output/figures/figure_registry.json")
    figure = next(
        entry
        for entry in registry["figures"]
        if entry["label"] == "fig:ageint-source-metadata-integrity"
    )
    assert figure["kind"] == FigureKind.PYTHON.value
    assert figure["provenance"]["renderer_id"] == "source_metadata_integrity"
    assert "source metadata integrity figure" in figure["caption"]
    assert "denominator context" in figure["caption"]
    assert "not a quality score" in figure["caption"]
    assert (PROJECT_ROOT / figure["output_path"]).is_file()


def test_source_refresh_due_dashboard_is_registry_backed() -> None:
    registry = load_figure_registry(PROJECT_ROOT / "output/figures/figure_registry.json")
    figure = next(
        entry
        for entry in registry["figures"]
        if entry["label"] == "fig:ageint-source-refresh-due-dashboard"
    )
    assert figure["kind"] == FigureKind.PYTHON.value
    assert figure["provenance"]["renderer_id"] == "source_refresh_due_dashboard"
    assert "source refresh due-date dashboard" in figure["caption"]
    assert "publication-preflight failure path" in figure["caption"]
    assert "not a score or empirical performance claim" in figure["caption"]
    assert figure["quantitative"] is True
    assert (PROJECT_ROOT / figure["output_path"]).is_file()


def test_agency_source_coverage_dashboard_is_registry_backed() -> None:
    registry = load_figure_registry(PROJECT_ROOT / "output/figures/figure_registry.json")
    figure = next(
        entry
        for entry in registry["figures"]
        if entry["label"] == "fig:ageint-agency-source-coverage"
    )
    assert figure["kind"] == FigureKind.PYTHON.value
    assert figure["provenance"]["renderer_id"] == "agency_source_coverage_dashboard"
    assert "agency-source coverage" in figure["caption"]
    assert "56-anchor denominator" in figure["caption"]
    assert "artifact-evidence failure path" in figure["caption"]
    assert figure["quantitative"] is True
    assert (PROJECT_ROOT / figure["output_path"]).is_file()


def test_claim_calibration_visual_is_registry_backed() -> None:
    registry = load_figure_registry(PROJECT_ROOT / "output/figures/figure_registry.json")
    figure = next(
        entry
        for entry in registry["figures"]
        if entry["label"] == "fig:ageint-claim-calibration-and-visual-semantics"
    )
    assert figure["kind"] == FigureKind.PYTHON.value
    assert figure["provenance"]["renderer_id"] == "claim_calibration_and_visual_semantics"
    assert "claim-calibration verifier" in figure["caption"]
    assert "reviewer inputs" in figure["caption"]
    assert "score, benchmark, or empirical performance claim" in figure["caption"]
    assert figure["semantic_role"] == "verifier_control_map"
    assert figure["evidence_role"] == "claim, source-strength, formalism, and visualization audit contract"
    assert figure["quantitative"] is False
    assert "not a measured capability score" in figure["interpretation_limit"]
    assert (PROJECT_ROOT / figure["output_path"]).is_file()


def test_visual_semantics_are_present_in_registry_and_audit() -> None:
    registry = load_figure_registry(PROJECT_ROOT / "output/figures/figure_registry.json")
    audit_path = PROJECT_ROOT / registry["quality_audit_path"]
    audit = json.loads(audit_path.read_text(encoding="utf-8"))

    for entry in registry["figures"]:
        assert entry["semantic_role"]
        assert entry["evidence_role"]
        assert entry["interpretation_limit"]
        if entry["quantitative"]:
            assert entry["unit"] != "not_applicable"
            assert entry["denominator"] != "not_applicable"
            assert entry["counting_rule"] != "not_applicable"
        else:
            assert "not a measured" in entry["interpretation_limit"].lower()
    assert all(row["checks"]["visual_semantics_present"] for row in audit["figures"])
