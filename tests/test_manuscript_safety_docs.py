"""Safety, documentation, and runtime-variable checks for generated AGEINT outputs."""

from __future__ import annotations

from datetime import date
from pathlib import Path

from intelligence_content import INTELLIGENCE_PROFILES, INTELLIGENCE_RESEARCH_ANCHORS, expanded_profile_anchor_keys

from manuscript_quality.inventory_helpers import (
    PROJECT_ROOT,
    REQUIRED_REFRESHED_ANCHOR_KEYS,
    REQUIRED_SOURCE_LANES,
    SOURCE_QUALITY_KEYS,
    TOKEN_RE,
    generated_output_files,
    manuscript_dir,
)


def test_generated_output_contains_no_unresolved_tokens(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    for path in generated_output_files(output_manuscript):
        text = path.read_text(encoding="utf-8")
        assert not TOKEN_RE.search(text), path


def test_research_anchors_include_verification_metadata() -> None:
    assert len(INTELLIGENCE_RESEARCH_ANCHORS) == 462
    assert REQUIRED_REFRESHED_ANCHOR_KEYS <= {anchor.key for anchor in INTELLIGENCE_RESEARCH_ANCHORS}
    assert REQUIRED_SOURCE_LANES <= {anchor.source_lane or anchor.domain for anchor in INTELLIGENCE_RESEARCH_ANCHORS}
    anchor_keys = SOURCE_QUALITY_KEYS
    for profile in INTELLIGENCE_PROFILES:
        assert set(expanded_profile_anchor_keys(profile)) <= anchor_keys, profile.identifier
    for anchor in INTELLIGENCE_RESEARCH_ANCHORS:
        checked = date.fromisoformat(anchor.checked_as_of)
        assert date(2026, 5, 21) <= checked <= max(date.today(), date(2026, 6, 16))
        assert anchor.verification_note
        assert anchor.citation_role == "curriculum_anchor"
        assert anchor.source_lane or anchor.domain
        assert anchor.source_tier or anchor.source_type
        assert anchor.refresh_cadence
        assert anchor.refresh_trigger
        assert anchor.verification_method
        assert anchor.claim_scope
        assert anchor.url.startswith("https://")
        if anchor.source_lane in {
            "accessibility_digital_inclusion",
            "procurement_vendor_governance",
            "agent_incident_response",
            "ai_red_team_assurance",
            "public_sector_transparency",
            "rights_impact_privacy",
            "model_card_reporting",
            "dataset_documentation",
            "algorithmic_transparency_reporting",
            "records_retention_auditability",
            "secure_release_change_control",
            "risk_exception_governance",
            "learner_support_accommodations",
            "assurance_evaluation_evidence",
            "procurement_performance_monitoring",
        }:
            assert anchor.stakeholder_role
            assert anchor.assurance_use
            assert anchor.rights_dimension


def test_meaningful_folders_have_readme_and_agent_notes() -> None:
    required = [
        PROJECT_ROOT / "data",
        PROJECT_ROOT / "docs",
        PROJECT_ROOT / "docs" / "manuscript",
        PROJECT_ROOT / "docs" / "manuscript" / "templates",
        PROJECT_ROOT / "output",
        PROJECT_ROOT / "output" / "data",
        PROJECT_ROOT / "output" / "figures",
        PROJECT_ROOT / "output" / "manuscript",
        PROJECT_ROOT / "output" / "manuscript" / "appendices",
        PROJECT_ROOT / "output" / "manuscript" / "parts",
        PROJECT_ROOT / "output" / "pdf",
        PROJECT_ROOT / "output" / "reports",
        PROJECT_ROOT / "output" / "slides",
        PROJECT_ROOT / "output" / "web",
        PROJECT_ROOT / "scripts",
        PROJECT_ROOT / "src",
        PROJECT_ROOT / "tests",
    ]
    for folder in required:
        assert (folder / "README.md").is_file(), folder
        assert (folder / "AGENTS.md").is_file(), folder

