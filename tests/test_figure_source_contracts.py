"""Source-anchor contracts for AGEINT figure groups."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path

from curriculum import load_curriculum
from figures import FigureKind, build_figure_specs
from intelligence_content import (
    INTELLIGENCE_PROFILES,
    INTELLIGENCE_RESEARCH_ANCHORS,
    expanded_profile_anchor_keys,
    research_source_pack_payload,
)
from manuscript_manifest import build_manuscript_manifest


PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"
LITERATURE_SHARD = PROJECT_ROOT / "data" / "research_anchors" / "intelligence-anchors-305-340.jsonl"
SAT_LITERATURE_SHARD = PROJECT_ROOT / "data" / "research_anchors" / "intelligence-anchors-341-367.jsonl"
CITATION_EXPANSION_SHARDS = (
    PROJECT_ROOT / "data" / "research_anchors" / "intelligence-anchors-368-417.jsonl",
    PROJECT_ROOT / "data" / "research_anchors" / "intelligence-anchors-418-462.jsonl",
)
CITATION_EXPANSION_REPORT = (
    PROJECT_ROOT / "data" / "research_anchors" / "citation-expansion-2026-06-16-report.json"
)
LITERATURE_INTEGRATION_KEYS = {
    "scholarly_dylan_stivang_2025_emerging_tech_intelligence",
    "scholarly_caballero_jenkins_2024_llm_national_security",
    "official_belfer_mcmahon_2024_ai_tradecraft_standards",
    "official_reagan_nsdd_298_opsec",
    "public_council_europe_information_disorder",
    "scholarly_terp_breuer_2022_disarm",
    "scholarly_smith_2022_active_inference_tutorial",
}
SAT_LITERATURE_INTEGRATION_KEYS = {
    "official_cia_cooper_2005_analytic_pathologies",
    "scholarly_janis_1982_groupthink",
    "scholarly_coulthart_2017_core_sat_evaluation",
    "scholarly_chang_2018_restructuring_sats",
    "scholarly_whitesmith_2019_ach_bias",
    "scholarly_karvetski_mandel_2020_ach_coherence",
    "scholarly_dhami_mandel_mellers_tetlock_2015_decision_science",
    "official_national_academies_2011_intelligence_analysis_tomorrow",
    "official_senate_2004_prewar_iraq_assessment",
    "official_iarpa_ace_program",
    "official_iarpa_reason_program",
    "official_foi_2021_structured_analytic_techniques",
    "official_jips_2021_jsat",
    "scholarly_wilcox_mandel_2024_ach_critical_review",
}


def _anchor_rows(path: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def _literature_rows() -> list[dict[str, object]]:
    return _anchor_rows(LITERATURE_SHARD)


def _sat_literature_rows() -> list[dict[str, object]]:
    return _anchor_rows(SAT_LITERATURE_SHARD)


def _citation_expansion_rows() -> list[dict[str, object]]:
    rows: list[dict[str, object]] = []
    for path in CITATION_EXPANSION_SHARDS:
        rows.extend(_anchor_rows(path))
    return rows


def _figure_specs_by_label() -> dict[str, object]:
    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)
    return {spec.label: spec for spec in build_figure_specs(curriculum, manifest)}


def test_literature_integration_shard_is_metadata_complete_unique_and_routed() -> None:
    rows = _literature_rows()
    required_fields = {
        "key",
        "title",
        "author",
        "year",
        "url",
        "note",
        "domain",
        "source_type",
        "checked_as_of",
        "verification_note",
        "citation_role",
        "source_lane",
        "source_tier",
        "refresh_cadence",
        "refresh_trigger",
        "verification_method",
        "claim_scope",
        "stakeholder_role",
        "assurance_use",
        "rights_dimension",
    }
    keys = [str(row["key"]) for row in rows]
    urls = [str(row["url"]) for row in rows]
    routed = {
        key
        for profile in INTELLIGENCE_PROFILES
        for key in expanded_profile_anchor_keys(profile)
    }

    assert len(rows) == 36
    assert len(keys) == len(set(keys))
    assert len(urls) == len(set(urls))
    assert LITERATURE_INTEGRATION_KEYS <= set(keys)
    assert set(keys) <= {anchor.key for anchor in INTELLIGENCE_RESEARCH_ANCHORS}
    assert set(keys) <= routed
    for row in rows:
        assert required_fields <= set(row), row
        assert str(row["checked_as_of"]) == "2026-06-15"
        assert str(row["citation_role"]) == "curriculum_anchor"
        assert str(row["url"]).startswith("https://")
        for field in required_fields:
            assert str(row[field]).strip(), (row["key"], field)


def test_sat_literature_shard_is_verified_deduped_complete_and_routed() -> None:
    rows = _sat_literature_rows()
    required_fields = {
        "key",
        "title",
        "author",
        "year",
        "url",
        "note",
        "domain",
        "source_type",
        "checked_as_of",
        "verification_note",
        "citation_role",
        "source_lane",
        "source_tier",
        "refresh_cadence",
        "refresh_trigger",
        "verification_method",
        "claim_scope",
        "stakeholder_role",
        "assurance_use",
        "rights_dimension",
    }
    keys = [str(row["key"]) for row in rows]
    urls = [str(row["url"]) for row in rows]
    anchors = {anchor.key: anchor for anchor in INTELLIGENCE_RESEARCH_ANCHORS}
    old_urls = {anchor.url for key, anchor in anchors.items() if key not in keys}
    routed = {
        key
        for profile in INTELLIGENCE_PROFILES
        for key in expanded_profile_anchor_keys(profile)
    }

    assert len(rows) == 27
    assert len(INTELLIGENCE_RESEARCH_ANCHORS) == 462
    assert len(keys) == len(set(keys))
    assert len(urls) == len(set(urls))
    assert not (set(urls) & old_urls)
    assert SAT_LITERATURE_INTEGRATION_KEYS <= set(keys)
    assert set(keys) <= anchors.keys()
    assert set(keys) <= routed
    assert "scholarly_heuer_pherson_sats" not in keys
    assert "scholarly_rand_2016_sat_evaluation" not in keys
    assert anchors["scholarly_rand_2016_sat_evaluation"].author == (
        "Stephen J. Artner; Richard S. Girven; James B. Bruce"
    )
    assert anchors["scholarly_ard_2023_sat_pragmatic"].title == (
        "Structured Analytic Techniques: A Pragmatic Approach"
    )
    for row in rows:
        assert required_fields <= set(row), row
        assert str(row["checked_as_of"]) == "2026-06-15"
        assert str(row["citation_role"]) == "curriculum_anchor"
        assert str(row["url"]).startswith("https://")
        assert str(row["claim_scope"]).startswith("Supports bounded")
        for field in required_fields:
            assert str(row[field]).strip(), (row["key"], field)


def test_citation_expansion_import_is_verified_bounded_deduped_and_routed() -> None:
    rows = _citation_expansion_rows()
    report = json.loads(CITATION_EXPANSION_REPORT.read_text(encoding="utf-8"))
    required_fields = {
        "key",
        "title",
        "author",
        "year",
        "url",
        "note",
        "domain",
        "source_type",
        "checked_as_of",
        "verification_note",
        "citation_role",
        "source_lane",
        "source_tier",
        "refresh_cadence",
        "refresh_trigger",
        "verification_method",
        "claim_scope",
        "stakeholder_role",
        "assurance_use",
        "rights_dimension",
        "source_agency",
        "source_pack",
    }
    keys = [str(row["key"]) for row in rows]
    urls = [str(row["url"]) for row in rows]
    anchors = {anchor.key: anchor for anchor in INTELLIGENCE_RESEARCH_ANCHORS}
    old_urls = {anchor.url for key, anchor in anchors.items() if key not in keys}
    routed = {
        key
        for profile in INTELLIGENCE_PROFILES
        for key in expanded_profile_anchor_keys(profile)
    }
    research_pack_keys = {
        key
        for keys_in_pack in research_source_pack_payload(PROJECT_ROOT).values()
        for key in keys_in_pack
    }

    assert report["candidate_heading_count"] == 106
    assert report["structurally_importable_count"] == 102
    assert report["accepted_count"] == 95
    assert report["deferred_count"] == 11
    assert report["new_intelligence_anchor_count_after_import"] == 462
    assert report["new_metadata_row_count_after_import"] == 472
    assert report["accepted_shards"] == [
        "intelligence-anchors-368-417.jsonl",
        "intelligence-anchors-418-462.jsonl",
    ]
    assert {str(item["original_key"]) for item in report["deferred"]} >= {
        "official_nist_sp_800_61r3_new",
        "official_nist_csf_2_0",
        "official_cisa_ics_alert_bb19_339a",
        "scholarly_microsoft_autogen_2024",
        "official_atp_2_22_9_1_pai_osint_2023",
    }
    assert len(rows) == 95
    assert len(keys) == len(set(keys))
    assert len(urls) == len(set(urls))
    assert not (set(urls) & old_urls)
    assert set(keys) <= anchors.keys()
    assert set(keys) <= routed
    assert set(keys) <= research_pack_keys
    assert {
        "professional_hutchins_2011_kill_chain",
        "professional_caltagirone_2013_diamond_model",
        "professional_rand_paul_matthews_firehose_falsehood",
        "professional_eset_win32_industroyer_2017",
        "professional_weng_2023_agent_survey",
    } <= set(keys)
    assert "scholarly_weng_2023_agent_survey" not in keys
    weak_hosts = ("wikipedia.org", "amazon.", "goodreads.", "scribd.", "blogspot.", "weebly.com")
    for row in rows:
        assert required_fields <= set(row), row
        assert str(row["checked_as_of"]) == "2026-06-16"
        assert str(row["citation_role"]) == "curriculum_anchor"
        assert str(row["url"]).startswith("https://")
        assert not any(host in str(row["url"]).lower() for host in weak_hosts), row["url"]
        assert "does not authorize collection tasking" in str(row["claim_scope"])
        assert "live-target procedures" in str(row["claim_scope"])
        for field in required_fields:
            assert str(row[field]).strip(), (row["key"], field)


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
    assert len(INTELLIGENCE_RESEARCH_ANCHORS) == 462
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
        "fig:ageint-si-tradecraft-opsec-cogsec-convergence",
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
