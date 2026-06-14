"""Tests for AGEINT tokenized manuscript template generation."""

from __future__ import annotations

from pathlib import Path

import src
from curriculum import load_curriculum
from intelligence_content import (
    INTELLIGENCE_PROFILES,
    anchor_references,
    chapter_knowledge_check,
    chapter_learning_outcomes,
    practice_lens_for_titles,
    practice_lens_rows,
    profile_for_titles,
    research_anchor_rows,
    safe_curriculum_treatment,
    subsection_practice_rows,
)
from manuscript_templates import (
    DEFAULT_TEMPLATES,
    SOURCE_OWNED_TEMPLATE_NAMES,
    TEMPLATE_NAMES,
    template_text,
    write_manuscript_templates,
    write_template_library,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"


def test_package_exports_runtime_helpers() -> None:
    critical = {
        "run_build",
        "run_build_figures",
        "build_curriculum",
        "render_manuscript",
        "render_figures",
        "generate_variables",
        "write_bibtex_files",
    }
    assert critical.issubset(set(src.__all__))
    assert len(src.__all__) <= 50
    assert callable(src.run_build)
    assert callable(src.run_build_figures)
    assert callable(src.render_manuscript)
    assert callable(src.generate_variables)


def test_write_template_library_rewrites_only_neutral_templates(tmp_path: Path) -> None:
    curriculum = load_curriculum(DATA)
    manuscript_dir = tmp_path / "manuscript"
    manuscript_dir.mkdir()
    preserved = manuscript_dir / "README.md"
    stale = manuscript_dir / "43_chapter_031.md"
    preserved.write_text("keep", encoding="utf-8")
    stale.write_text("# Chapter 31 — stale", encoding="utf-8")

    written = write_manuscript_templates(curriculum, manuscript_dir)

    assert preserved.exists()
    assert stale.exists()
    assert len(written) == len(TEMPLATE_NAMES)
    chapter_template = manuscript_dir / "templates" / "chapter.md"
    assert chapter_template.exists()
    text = chapter_template.read_text(encoding="utf-8")
    assert "{{SECTION_TITLE}}" in text
    assert "{{SECTION_BODY}}" in text
    assert "{{CHAPTER_031_TITLE}}" not in text
    assert "Foundations of AGEINT" not in text
    assert "Chapter 31" not in text
    orientation = (manuscript_dir / "templates" / "orientation.md").read_text(encoding="utf-8")
    assert "Synthetic Analytic Tradecraft thesis" in orientation
    assert "{#sec:synthetic-analytic-tradecraft-thesis}" in orientation
    assert {path.name for path in written} == set(TEMPLATE_NAMES)


def test_source_owned_templates_do_not_have_stale_embedded_fallbacks() -> None:
    assert SOURCE_OWNED_TEMPLATE_NAMES == {"abstract.md", "orientation.md"}
    assert set(DEFAULT_TEMPLATES) == set(TEMPLATE_NAMES) - SOURCE_OWNED_TEMPLATE_NAMES
    for name in SOURCE_OWNED_TEMPLATE_NAMES:
        source_text = (PROJECT_ROOT / "manuscript" / "templates" / name).read_text(
            encoding="utf-8"
        )
        assert template_text(name) == source_text


def test_neutral_appendix_template_uses_generic_runtime_tokens(tmp_path: Path) -> None:
    write_template_library(tmp_path)
    appendix = (tmp_path / "appendix.md").read_text(encoding="utf-8")
    assert "{{SECTION_TITLE}}" in appendix
    assert "{{SECTION_ROWS}}" in appendix
    assert "{{APPENDIX_A_TITLE}}" not in appendix
    assert "Python OSINT Library" not in appendix


def test_research_profiles_route_sections_to_domain_content() -> None:
    foundations = profile_for_titles(
        "FOUNDATIONS OF INTELLIGENCE TRADECRAFT",
        "The Nature of Intelligence",
    )
    ageint = profile_for_titles("AGEINT: Agentic Intelligence", "Foundations of AGEINT")
    humint = profile_for_titles("HUMINT", "Agent Recruitment")
    finint = profile_for_titles(
        "IMAGERY AND FINANCIAL INTELLIGENCE",
        "Financial Intelligence (FININT)",
    )
    history = profile_for_titles(
        "HISTORICAL INTELLIGENCE SERVICES",
        "American Intelligence History",
    )
    ci = profile_for_titles("Counterintelligence", "Source Protection")
    cyber = profile_for_titles("Cyber Intelligence", "Supply Chain Intelligence Attacks")
    ics = profile_for_titles(
        "Industrial and Cyber-Physical Intelligence",
        "MITRE ATT&CK for ICS",
    )
    supply_chain = profile_for_titles(
        "TECHNICAL INTELLIGENCE AND CYBER OPERATIONS",
        "Supply Chain Intelligence Attacks",
    )

    assert foundations.identifier == "governed_intelligence_cycle"
    assert ageint.identifier == "agentic_ai_governance"
    assert humint.identifier == "collection_management"
    assert finint.identifier == "financial_economic_security"
    assert history.identifier == "historical_declassified_sources"
    assert ci.identifier == "counterintelligence_source_integrity"
    assert cyber.identifier == "cyber_threat_intelligence"
    assert ics.identifier == "ics_ot_defense"
    assert supply_chain.identifier == "cyber_threat_intelligence"
    assert "official_owasp_llm_top_10" in research_anchor_rows()
    assert "official_odni_icd_204" in research_anchor_rows()
    assert "official_odni_icd_505" in research_anchor_rows()
    assert "official_fincen_advisories" in research_anchor_rows()
    assert "Requirements-to-Evidence Lens" in practice_lens_rows()


def test_research_profile_anchor_keys_resolve_for_chapter_briefs() -> None:
    for profile in INTELLIGENCE_PROFILES:
        anchors = anchor_references(profile.anchor_keys)
        assert [anchor.key for anchor in anchors] == list(profile.anchor_keys)


def test_practice_lenses_route_subsections_to_fractal_contracts() -> None:
    foundations = practice_lens_for_titles(
        "FOUNDATIONS OF INTELLIGENCE TRADECRAFT",
        "Intelligence Community Architectures",
    )
    ageint = practice_lens_for_titles("AGEINT: Agentic Intelligence", "MCP Frameworks")
    finint = practice_lens_for_titles(
        "IMAGERY AND FINANCIAL INTELLIGENCE",
        "Financial Intelligence (FININT)",
    )
    history = practice_lens_for_titles(
        "HISTORICAL INTELLIGENCE SERVICES",
        "Soviet and Russian Intelligence",
    )
    cognitive = practice_lens_for_titles("Cognitive Security", "Prebunking")
    ics = practice_lens_for_titles("Industrial Control Systems", "Incident Response")
    supply_chain = practice_lens_for_titles(
        "TECHNICAL INTELLIGENCE AND CYBER OPERATIONS",
        "Supply Chain Intelligence Attacks",
    )

    assert foundations.identifier == "dissemination_marking_control"
    assert ageint.identifier == "agentic_tool_governance"
    assert finint.identifier == "economic_security_due_diligence"
    assert history.identifier == "historical_case_translation"
    assert cognitive.identifier == "cognitive_resilience"
    assert ics.identifier == "cyber_physical_readiness"
    assert supply_chain.identifier == "software_supply_chain_assurance"


def test_safe_coursebook_helpers_cover_edge_topic_fallbacks() -> None:
    assert "non-sensitive synthetic change examples" in safe_curriculum_treatment(
        "Google Earth Engine"
    )
    assert "no real targets" in safe_curriculum_treatment("persistent target monitoring")
    assert "synthetic GEOINT uncertainty" in safe_curriculum_treatment("facility monitoring")
    assert "fixed inputs" in safe_curriculum_treatment("multi-source data harvesting")
    assert "fabricated alerts" in safe_curriculum_treatment("autonomous SOC")
    assert "defensive tactics" in safe_curriculum_treatment("penetration testing automation")
    assert "sample classroom scenario" in safe_curriculum_treatment(
        "population-scale cognitive security intervention delivery"
    )
    assert "Malware-misuse control review" in safe_curriculum_treatment(
        "Automated Weaponization: Malware Generation"
    )
    assert "Declassified source-protection" in safe_curriculum_treatment(
        "Working with Agents (Declassified Manual)"
    )
    assert "Maintainer-contact" in safe_curriculum_treatment(
        "Sock Puppetry as HUMINT Cover Tradecraft",
        "TECHNICAL INTELLIGENCE AND CYBER OPERATIONS",
        "Supply Chain Intelligence Attacks",
    )

    part = {"title": "AGEINT: Agentic Intelligence"}
    empty_chapter = {"title": "Fallback Coursebook Topic", "sections": []}
    meta_only_chapter = {
        "title": "Meta Only Topic",
        "sections": [{"number": "1.1", "title": "V2 source-lane extension: source lane"}],
    }

    assert "Fallback Coursebook Topic" in chapter_learning_outcomes(empty_chapter, part)
    assert "Meta Only Topic" in chapter_knowledge_check(meta_only_chapter, part)
    fallback_rows = subsection_practice_rows(empty_chapter, part)
    assert "Fallback Coursebook Topic" in fallback_rows
    assert "Source-guide module" not in fallback_rows
