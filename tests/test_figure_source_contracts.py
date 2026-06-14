"""Source-anchor contracts for AGEINT figure groups."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from curriculum import load_curriculum
from figures import FigureKind, build_figure_specs
from intelligence_content import INTELLIGENCE_RESEARCH_ANCHORS
from manuscript_manifest import build_manuscript_manifest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"


def _figure_specs_by_label() -> dict[str, object]:
    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)
    return {spec.label: spec for spec in build_figure_specs(curriculum, manifest)}


def test_internet_backed_visuals_have_current_source_anchor_contracts() -> None:
    anchors = {anchor.key: anchor for anchor in INTELLIGENCE_RESEARCH_ANCHORS}
    required = {
        "official_nist_ai_800_2_automated_benchmark_evaluations",
        "official_oecd_agentic_ai_landscape",
        "official_nsa_mcp_security_design_considerations",
        "scholarly_roozenbeek_2022_psychological_inoculation",
    }
    assert required <= anchors.keys()
    for key in required:
        anchor = anchors[key]
        assert date.fromisoformat(anchor.checked_as_of) >= date(2026, 6, 11)
        assert anchor.source_lane
        assert anchor.source_tier
        assert anchor.assurance_use
        assert anchor.rights_dimension

    specs = _figure_specs_by_label()
    assert specs["fig:ageint-source-freshness-coverage"].kind == FigureKind.PYTHON
    assert (
        specs["fig:ageint-source-freshness-coverage"].provenance["renderer_id"]
        == "source_freshness_coverage"
    )
    analytic_boundary = specs["fig:ageint-analytic-source-quality-boundary"]
    assert analytic_boundary.kind == FigureKind.PYTHON
    assert analytic_boundary.provenance["renderer_id"] == "analytic_source_quality_boundary"
    accessibility_contract = specs["fig:ageint-visual-accessibility-contract"]
    assert accessibility_contract.kind == FigureKind.PYTHON
    assert accessibility_contract.provenance["renderer_id"] == "visual_accessibility_contract"
    assert "W3C WAI complex-image guidance" in accessibility_contract.caption
    assert "USWDS data-visualization guidance" in accessibility_contract.caption
    assert "color" in accessibility_contract.long_description.lower()


def test_analytic_tradecraft_source_refresh_has_boundary_contracts() -> None:
    anchors = {anchor.key: anchor for anchor in INTELLIGENCE_RESEARCH_ANCHORS}
    required = {
        "official_cia_sherman_kent_profession",
        "official_cia_kent_analyst_policymaker_relations",
        "scholarly_wohlstetter_1962_pearl_harbor_warning_decision",
        "official_cia_grabo_warning_intelligence_handbook",
        "official_irtpa_2004_analytic_integrity",
        "official_911_commission_report",
        "official_robb_silberman_wmd_report",
        "official_nato_alternative_analysis_handbook",
        "scholarly_rand_2016_sat_evaluation",
        "scholarly_marcoci_2019_tradecraft_reliability",
        "scholarly_barnes_mandel_2014_forecast_accuracy",
        "scholarly_ard_2023_sat_pragmatic",
        "scholarly_stromer_galley_2020_flexible_sat",
        "scholarly_betts_1978_intelligence_failure",
        "scholarly_jervis_2022_postmortems_fail",
        "scholarly_wirtz_2023_intelligence_failures_inevitable",
    }
    assert len(INTELLIGENCE_RESEARCH_ANCHORS) == 248
    assert required <= anchors.keys()

    weak_hosts = ("wikipedia.org", "amazon.", "goodreads.", "scribd.", "blogspot.")
    for key in required:
        anchor = anchors[key]
        assert date.fromisoformat(anchor.checked_as_of) >= date(2026, 6, 11)
        assert anchor.url.startswith("https://")
        assert not any(host in anchor.url for host in weak_hosts), anchor.url
        assert anchor.source_lane in {
            "analytic_tradecraft_evidence",
            "warning_intelligence",
            "intelligence_failure_postmortem",
            "sat_evaluation_evidence",
            "forecasting_calibration_evidence",
        }
        assert anchor.source_tier
        assert anchor.verification_method
        assert anchor.claim_scope
        assert anchor.assurance_use
        assert anchor.rights_dimension

    specs = _figure_specs_by_label()
    tradecraft_labels = {
        "fig:ageint-analytic-tradecraft-evidence-ladder",
        "fig:ageint-analytic-source-quality-boundary",
        "fig:ageint-first-principles-tradecraft-decomposition",
        "fig:ageint-redteam-tradecraft-negative-control-loop",
        "fig:ageint-icd203-probability-confidence-boundary",
        "fig:ageint-sat-evidence-boundary",
        "fig:ageint-warning-failure-feedback-loop",
    }
    assert tradecraft_labels <= specs.keys()
    for label in tradecraft_labels:
        spec = specs[label]
        assert spec.kind in {FigureKind.MERMAID, FigureKind.PYTHON}
        assert "Source-backed" in spec.caption
        assert any(
            token in spec.caption.lower()
            for token in (
                "overclaim",
                "separat",
                "single technique",
                "universal debiasing",
                "evidence lane",
                "false-certification",
            )
        )
