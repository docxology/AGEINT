"""Safety, documentation, and runtime-variable checks for generated AGEINT outputs."""

from __future__ import annotations

import json
from datetime import date
from pathlib import Path
import re

from intelligence_content import INTELLIGENCE_PROFILES, INTELLIGENCE_RESEARCH_ANCHORS
from manuscript_variables import generate_variables

from manuscript_quality.inventory_helpers import (
    BLOCKED_OPERATIONAL_PATTERN_PHRASES,
    PROJECT_ROOT,
    REQUIRED_REFRESHED_ANCHOR_KEYS,
    REQUIRED_SOURCE_LANES,
    REQUIRED_V2_DOCS,
    SOURCE_QUALITY_KEYS,
    TOKEN_RE,
    chapter_text,
    generated_chapter_files,
    generated_output_files,
    manuscript_dir,
    section_text,
)


def test_generated_runtime_item_maps_deduplicate_safe_treatments(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    for path in generated_output_files(output_manuscript):
        text = path.read_text(encoding="utf-8")
        if "## Runtime item map" not in text:
            continue
        table = text.split("## Runtime item map", 1)[1].split("\n## ", 1)[0]
        seen: set[str] = set()
        duplicates: set[str] = set()
        for line in table.splitlines():
            if (
                not line.startswith("| ")
                or line.startswith("| Source item")
                or line.startswith("| Curriculum treatment")
                or line.startswith("| Safe curriculum treatment")
                or line.startswith("|---")
            ):
                continue
            source_item = line.split("|")[1].strip()
            if source_item in seen:
                duplicates.add(source_item)
            seen.add(source_item)
        assert duplicates == set(), f"{path}: {sorted(duplicates)}"


def test_generated_appendix_item_maps_are_safely_transformed(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    risky_patterns = {
        "target tracking",
        "graph scraping",
        "exploit chain",
        "geolocation attribution",
        "autonomous scanning",
        "source handling",
        "audience-targeted influence",
        "persistent target monitoring",
        "multi-source data harvesting",
        "penetration testing automation",
        "vulnerability discovery",
    }
    for path in sorted((output_manuscript / "appendices").glob("*.md")):
        text = path.read_text(encoding="utf-8").lower()
        if "## runtime item map" not in text:
            continue
        table = text.split("## runtime item map", 1)[1].split("\n## ", 1)[0]
        assert "safe curriculum treatment" in table
        assert "blocked source motif, audit-only" in table
        assert "allowed fixture" in table
        assert "rejected action" in table
        assert "required artifact" in table
        for line in table.splitlines():
            if not line.startswith("| ") or line.startswith("| safe curriculum treatment"):
                continue
            first_cell = line.split("|")[1].strip()
            for phrase in risky_patterns:
                assert phrase not in first_cell, f"{path}: {phrase}: {line}"


def test_generated_output_contains_no_unresolved_tokens(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    for path in generated_output_files(output_manuscript):
        text = path.read_text(encoding="utf-8")
        assert not TOKEN_RE.search(text), path


def test_generated_v2_appendices_render_source_and_capstone_workflows(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    appendix_h = output_manuscript / "appendices" / "source-verification-and-claim-ledger-workbook.md"
    appendix_i = output_manuscript / "appendices" / "instructor-capstone-rubric-and-red-team-review-pack.md"

    h_text = appendix_h.read_text(encoding="utf-8")
    i_text = appendix_i.read_text(encoding="utf-8")

    assert "## Source verification workflow" in h_text
    assert "## Safe artifact schema" in h_text
    assert "## Input/output contract" in h_text
    assert "## Failure cases" in h_text
    assert "## Rubric scoring bands" in h_text
    assert "## Refresh evidence" in h_text
    assert "## Source refresh evidence" in h_text
    assert "## HRIA/DPIA evidence bridge" in h_text
    assert "ai_conformity_compliance" in h_text
    assert "accessibility_digital_inclusion" in h_text
    assert "Source identity lock procedure" in h_text
    assert "## Instructor capstone workflow" in i_text
    assert "## Safe artifact rows" in i_text
    assert "## Assessment lifecycle evidence" in i_text
    assert "## Adversarial review evidence" in i_text
    assert "AGEINT patterns" in i_text
    assert "authorized learning question" in i_text


def test_runtime_variables_are_auditable_and_source_backed() -> None:
    variables = generate_variables(PROJECT_ROOT)
    assert variables["CURRICULUM_PART_COUNT"] == "16"
    assert variables["CURRICULUM_CHAPTER_COUNT"] == "51"
    assert variables["CURRICULUM_APPENDIX_COUNT"] == "9"
    assert int(variables["CURRICULUM_REFERENCE_COUNT"]) >= 296
    assert int(variables["INTELLIGENCE_RESEARCH_ANCHOR_COUNT"]) >= 228
    assert int(variables["INTELLIGENCE_PRACTICE_LENS_COUNT"]) >= 12
    assert not any(key.startswith("CHAPTER_") for key in variables)
    assert "Checked as of 2026-05-21" in variables["BIBTEX_REFERENCES"]
    assert r"Citation role: curriculum\_anchor" in variables["BIBTEX_REFERENCES"]
    assert r"Source lane: ai\_conformity\_compliance" in variables["BIBTEX_REFERENCES"]
    assert r"Refresh cadence: quarterly" in variables["BIBTEX_REFERENCES"]
    assert "NIST.AI.100-1" in variables["BIBTEX_REFERENCES"]
    assert r"ATT\&CK" in variables["BIBTEX_REFERENCES"]
    assert "official_oecd_agentic_ai" in variables["BIBLIOGRAPHY_ATLAS_ROWS"]
    assert "official_owasp_llm_top_10" in variables["BIBLIOGRAPHY_ATLAS_ROWS"]
    assert "Careful Adoption of Agentic AI Services" in variables["BIBTEX_REFERENCES"]
    assert "AI Safety Institute Approach to Evaluations" in variables["BIBTEX_REFERENCES"]
    assert "The NIST Cybersecurity Framework" in variables["BIBTEX_REFERENCES"]
    assert "National Intelligence Priorities Framework" in variables["BIBTEX_REFERENCES"]
    assert "Intelligence Community Directive 505" in variables["BIBTEX_REFERENCES"]
    assert "FinCEN Alerts, Advisories" in variables["BIBTEX_REFERENCES"]
    assert "Advancing Artificial Intelligence Agent Ecosystems" in variables["BIBTEX_REFERENCES"]
    assert "STIX Version 2.1" in variables["BIBTEX_REFERENCES"]
    assert "NIST Privacy Framework" in variables["BIBTEX_REFERENCES"]
    assert "European AI Office" in variables["BIBTEX_REFERENCES"]
    assert "Guidance for Generative AI in Education and Research" in variables["BIBTEX_REFERENCES"]
    assert "Common European Data Spaces" in variables["BIBTEX_REFERENCES"]
    assert "Web of Things (WoT) Architecture 1.1" in variables["BIBTEX_REFERENCES"]
    assert "PROV-O: The PROV Ontology" in variables["BIBTEX_REFERENCES"]
    assert "WCAG 2 Overview" in variables["BIBTEX_REFERENCES"]
    assert "CAST Universal Design for Learning Guidelines" in variables["BIBTEX_REFERENCES"]
    assert "Fact Sheet: New Rule on the Accessibility" in variables["BIBTEX_REFERENCES"]
    assert "What is a Data Protection Impact Assessment" in variables["BIBTEX_REFERENCES"]
    assert "Artificial Intelligence Cybersecurity Challenges" in variables["BIBTEX_REFERENCES"]
    assert "Model Cards for Model Reporting" in variables["BIBTEX_REFERENCES"]
    assert "Datasheets for Datasets" in variables["BIBTEX_REFERENCES"]
    assert "Data Cards: Purposeful and Transparent Dataset Documentation" in variables[
        "BIBTEX_REFERENCES"
    ]
    assert "The Free Energy Principle for Action and Perception" in variables["BIBTEX_REFERENCES"]
    assert "PRISMA-S: An Extension to the PRISMA Statement" in variables["BIBTEX_REFERENCES"]
    assert "Compromising Real-World LLM-Integrated Applications" in variables[
        "BIBTEX_REFERENCES"
    ]
    assert "Algorithmic Transparency Recording Standard Hub" in variables["BIBTEX_REFERENCES"]
    assert "Secure Software Development Practices for Generative AI" in variables["BIBTEX_REFERENCES"]
    assert "Revised 508 Standards and 255 Guidelines" in variables["BIBTEX_REFERENCES"]
    assert "Assessing Risks and Impacts of AI" in variables["BIBTEX_REFERENCES"]
    assert "Inventory of NARA Artificial Intelligence" in variables["BIBTEX_REFERENCES"]
    assert "M-25-21" in variables["BIBTEX_REFERENCES"]
    assert "M-25-22" in variables["BIBTEX_REFERENCES"]
    assert "Guide on the Use of Agentic Artificial Intelligence" in variables["BIBTEX_REFERENCES"]
    assert "Towards a common reporting framework for AI incidents" in variables["BIBTEX_REFERENCES"]
    assert "Creating and Maintaining a Definitive View" in variables["BIBTEX_REFERENCES"]
    assert "official_canada_agentic_ai_guide" in variables["BIBLIOGRAPHY_ATLAS_ROWS"]
    assert "official_cisa_ot_definitive_architecture" in variables["BIBLIOGRAPHY_ATLAS_ROWS"]
    assert "Stakeholder role:" in variables["BIBTEX_REFERENCES"]
    assert "Assurance use:" in variables["BIBTEX_REFERENCES"]
    assert "Rights dimension:" in variables["BIBTEX_REFERENCES"]
    assert "official_iso_iec_42001_ai_management" in variables["BIBLIOGRAPHY_ATLAS_ROWS"]
    assert "source_quality_anchor" in variables["BIBLIOGRAPHY_ATLAS_ROWS"]
    assert "ai_conformity_compliance" in variables["INTELLIGENCE_SOURCE_LANE_ROWS"]
    assert "model_data_provenance" in variables["INTELLIGENCE_SOURCE_LANE_ROWS"]
    assert "accessibility_digital_inclusion" in variables["INTELLIGENCE_SOURCE_LANE_ROWS"]
    assert "procurement_vendor_governance" in variables["INTELLIGENCE_SOURCE_LANE_ROWS"]
    assert "agent_incident_response" in variables["INTELLIGENCE_SOURCE_LANE_ROWS"]
    assert "ai_red_team_assurance" in variables["INTELLIGENCE_SOURCE_LANE_ROWS"]
    assert "public_sector_transparency" in variables["INTELLIGENCE_SOURCE_LANE_ROWS"]
    assert "model_card_reporting" in variables["INTELLIGENCE_SOURCE_LANE_ROWS"]
    assert "dataset_documentation" in variables["INTELLIGENCE_SOURCE_LANE_ROWS"]
    assert "algorithmic_transparency_reporting" in variables["INTELLIGENCE_SOURCE_LANE_ROWS"]
    assert "records_retention_auditability" in variables["INTELLIGENCE_SOURCE_LANE_ROWS"]
    assert "secure_release_change_control" in variables["INTELLIGENCE_SOURCE_LANE_ROWS"]
    assert "risk_exception_governance" in variables["INTELLIGENCE_SOURCE_LANE_ROWS"]
    assert "learner_support_accommodations" in variables["INTELLIGENCE_SOURCE_LANE_ROWS"]
    assert "assurance_evaluation_evidence" in variables["INTELLIGENCE_SOURCE_LANE_ROWS"]
    assert "source URL, policy status" in variables["SOURCE_REFRESH_ROWS"]
    assert "| Anchor | Source | Lane | Tier | Checked | Cadence | Refresh trigger | Verification note |" in variables["SOURCE_REFRESH_ROWS"]
    assert "URL refreshed 2026-06-06" in variables["SOURCE_REFRESH_ROWS"]
    assert "manual browser re-verification remains required" in variables["SOURCE_REFRESH_ROWS"]
    assert "| Anchor | Source | Lane | Contribution to the manuscript | Verification caveat |" in variables[
        "CURRENT_SOURCE_UPDATE_ROWS"
    ]
    assert "official_nist_ai_100_4_synthetic_content" in variables["CURRENT_SOURCE_UPDATE_ROWS"]
    assert "official_us_aisi_nist_ai_800_1_misuse_risk" in variables[
        "CURRENT_SOURCE_UPDATE_ROWS"
    ]
    assert "Draft status retained" in variables["CURRENT_SOURCE_UPDATE_ROWS"]
    assert "official_model_context_protocol_security_best_practices" in variables[
        "CURRENT_SOURCE_UPDATE_ROWS"
    ]
    assert "scholarly_data_cards_dataset_documentation" in variables[
        "CURRENT_SOURCE_UPDATE_ROWS"
    ]
    assert "scholarly_buckley_2017_fep_mathematical_review" in variables[
        "BIBLIOGRAPHY_ATLAS_ROWS"
    ]
    assert "scholarly_rethlefsen_2021_prisma_s" in variables["BIBLIOGRAPHY_ATLAS_ROWS"]
    assert "scholarly_greshake_2023_indirect_prompt_injection" in variables[
        "BIBLIOGRAPHY_ATLAS_ROWS"
    ]
    assert "official_agent2agent_protocol_specification" in variables[
        "CURRENT_SOURCE_UPDATE_ROWS"
    ]
    assert "AGEINT patterns" in variables["SAFE_SUBSTITUTION_ROWS"]
    assert "authorized learning question" in variables["CAPSTONE_SCAFFOLD_ROWS"]
    assert "WCAG/UDL needs note" in variables["ACCESSIBILITY_REVIEW_ROWS"]
    assert "procurement rationale" in variables["PROCUREMENT_OVERSIGHT_ROWS"]
    assert "DPIA trigger checklist" in variables["HRIA_DPIA_WORKSHEET_ROWS"]
    assert "claim ledger" in variables["DATA_LINEAGE_REGISTRY_ROWS"]
    assert "tool-use declaration" in variables["ASSESSMENT_INTEGRITY_ROWS"]
    assert "synthetic incident ticket" in variables["AGENT_INCIDENT_RESPONSE_ROWS"]
    assert "Assurance reviewer" in variables["ROLE_COMPETENCY_ROWS"]
    assert "misuse-case card" in variables["ADVERSARIAL_ASSURANCE_ROWS"]
    assert "Intended use" in variables["MODEL_DATASET_CARD_ROWS"]
    assert "Provenance and collection" in variables["MODEL_DATASET_CARD_ROWS"]
    assert "Evaluation and caveats" in variables["MODEL_DATASET_CARD_ROWS"]
    assert "Data Cards purpose statement" in variables["MODEL_DATASET_CARD_ROWS"]
    assert "empirical or performance claims are rejected" in variables[
        "MODEL_DATASET_CARD_ROWS"
    ]
    assert "Public purpose" in variables["TRANSPARENCY_NOTICE_ROWS"]
    assert "Source and prompt register" in variables["RETENTION_AUDIT_ROWS"]
    assert "Scope freeze" in variables["RELEASE_CHANGE_CONTROL_ROWS"]
    assert "Exception requested" in variables["RISK_EXCEPTION_ROWS"]
    assert "Access and modality" in variables["LEARNER_SUPPORT_ROWS"]
    assert "Source challenge" in variables["QUESTION_BANK_ROWS"]
    assert "Unverified claim" in variables["REMEDIATION_BACKLOG_ROWS"]
    assert "Requirements-to-Evidence Lens" in variables["INTELLIGENCE_PRACTICE_LENS_ROWS"]
    assert "Economic-Security Due-Diligence Lens" in variables["INTELLIGENCE_PRACTICE_LENS_ROWS"]
    assert "Software-Supply-Chain Assurance Lens" in variables["INTELLIGENCE_PRACTICE_LENS_ROWS"]
    assert "Active-Inference Boundary Lens" in variables["INTELLIGENCE_PRACTICE_LENS_ROWS"]


def test_research_anchors_include_verification_metadata() -> None:
    assert len(INTELLIGENCE_RESEARCH_ANCHORS) == 248
    assert REQUIRED_REFRESHED_ANCHOR_KEYS <= {anchor.key for anchor in INTELLIGENCE_RESEARCH_ANCHORS}
    assert REQUIRED_SOURCE_LANES <= {
        anchor.source_lane or anchor.domain for anchor in INTELLIGENCE_RESEARCH_ANCHORS
    }
    anchor_keys = SOURCE_QUALITY_KEYS
    for profile in INTELLIGENCE_PROFILES:
        assert set(profile.anchor_keys) <= anchor_keys, profile.identifier
    for anchor in INTELLIGENCE_RESEARCH_ANCHORS:
        checked = date.fromisoformat(anchor.checked_as_of)
        assert date(2026, 5, 21) <= checked <= date.today()
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


def test_reader_docs_match_live_counts_and_perplexity_method() -> None:
    variables = generate_variables(PROJECT_ROOT)
    anchor_count = variables["INTELLIGENCE_RESEARCH_ANCHOR_COUNT"]
    reference_count = variables["CURRICULUM_REFERENCE_COUNT"]
    registry = json.loads((PROJECT_ROOT / "output" / "figures" / "figure_registry.json").read_text())
    figure_count = str(len(registry["figures"]))

    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    agents = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    docs_readme = (PROJECT_ROOT / "docs" / "README.md").read_text(encoding="utf-8")
    output_inventory = (PROJECT_ROOT / "docs" / "output_inventory.md").read_text(encoding="utf-8")
    research = (PROJECT_ROOT / "docs" / "research.md").read_text(encoding="utf-8")
    v2_map = (PROJECT_ROOT / "docs" / "v2_expansion_map.md").read_text(encoding="utf-8")

    assert f"Curated official/scholarly research anchors: {anchor_count}" in readme
    assert f"{anchor_count} research anchors" in agents
    assert f"| Curated research anchors | {anchor_count} |" in docs_readme
    assert f"| Source-guide references | {reference_count} |" in docs_readme
    assert f"Registered figures: {figure_count}" in readme
    assert f"Curated anchors increased to {anchor_count}" in v2_map
    assert f"Registered figures increased to {figure_count}" in v2_map
    assert f"figure metadata ({figure_count} figures" in output_inventory
    assert "current registry has no placeholder plates" in readme
    assert "Perplexity (`llm -m sonar-pro`) timed out" not in research
    assert f"expand the curated anchor set to {anchor_count}" in research
    assert "Vendor/blog results from discovery are not encoded" in research.replace("\n", " ")

def test_generated_chapters_include_current_source_assurance_crosswalk(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    for path in generated_chapter_files(output_manuscript):
        text = chapter_text(path)
        assert "### Current-source assurance crosswalk" in text, path
        crosswalk = section_text(text, "Governance, rights, and assurance")
        assert "Discovery and second-opinion" in crosswalk, path
        assert "Claim ledger records the direct URL" in crosswalk, path
        assert re.search(r"checked 2026-(05|06)-", crosswalk), path


def test_meaningful_folders_have_readme_and_agent_notes() -> None:
    required = [
        PROJECT_ROOT / "data",
        PROJECT_ROOT / "docs",
        PROJECT_ROOT / "manuscript",
        PROJECT_ROOT / "manuscript" / "templates",
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


def test_v2_docs_cover_source_lanes_identity_safety_and_capstone() -> None:
    docs = PROJECT_ROOT / "docs"
    present = {path.name for path in docs.glob("*.md")}
    assert REQUIRED_V2_DOCS <= present

    combined = "\n".join((docs / name).read_text(encoding="utf-8") for name in sorted(REQUIRED_V2_DOCS))
    for phrase in (
        "ageint001",
        "ageint231",
        "ageint285",
        "ageint312",
        "AI conformity/compliance",
        "Public-sector agentic AI",
        "Human-rights governance",
        "Accessibility and digital inclusion",
        "Procurement/vendor governance",
        "Agent incident response",
        "AI red-team assurance",
        "Public-sector transparency",
        "model and dataset cards",
        "Data Cards",
        "transparency notices",
        "records-retention evidence",
        "release gates",
        "risk exceptions",
        "learner support",
        "instructor question bank",
        "remediation backlogs",
        "HRIA/DPIA",
        "safe substitution",
        "authorized learning question",
        "source verification and claim ledgers",
        "instructor capstone/rubric/red-team review",
        "secondary or illustrative evidence",
    ):
        assert phrase in combined


def test_abstract_and_claim_ledger_calibrate_empirical_claims(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    abstract = (output_manuscript / "abstract.md").read_text(encoding="utf-8")
    orientation = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted((output_manuscript / "orientation").glob("*.md"))
    )
    method_ref = (
        output_manuscript / "method-assurance-reference.md"
    ).read_text(encoding="utf-8")
    abstract_normalized = re.sub(r"\s+", " ", abstract)

    assert "curriculum-and-assurance atlas" in abstract_normalized
    assert "does not claim to measure AGEINT performance" in abstract_normalized
    assert (
        "Practitioner, vendor, and blog sources inherited through the source guide"
        in abstract_normalized
    )
    assert "Empirical or evaluated capability claim" in method_ref
    assert "not merely inferred from the AGEINT curriculum architecture" in method_ref
    assert "proposed design guidance and an assurance framework" in orientation


def test_risky_patterns_are_safety_transformed(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    pattern_chapter = (
        output_manuscript
        / "parts"
        / "ageint-agentic-intelligence"
        / "ageint-design-patterns-and-archetypes"
        / "00-overview.md"
    )
    pattern_chapter = chapter_text(pattern_chapter).lower()
    runtime_map = re.split(
        r"^#{2,3} fractal subsection map",
        re.split(r"^#{2,3} runtime section map", pattern_chapter, maxsplit=1, flags=re.M)[1],
        maxsplit=1,
        flags=re.M,
    )[0]
    for phrase in BLOCKED_OPERATIONAL_PATTERN_PHRASES:
        assert phrase not in runtime_map
    assert "monitoring-governance tabletop agent" in runtime_map
    assert "identity-and-provenance fiction audit" in runtime_map
    assert "soc tabletop triage agent" in runtime_map
    assert "geoint data-quality audit agent" in runtime_map
    assert "source identity preserved in pattern registry" in pattern_chapter
    assert "non-operational curriculum treatments" in pattern_chapter


def test_coursebook_practice_sections_safety_transform_unsafe_motifs(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    for path in generated_chapter_files(output_manuscript):
        text = chapter_text(path).lower()
        coursebook = text.split("## evidence and source canon", 1)[0]
        for phrase in BLOCKED_OPERATIONAL_PATTERN_PHRASES:
            assert phrase not in coursebook, f"{path}: {phrase}"


def test_safety_audit_blocks_operational_phrases_outside_source_audit_contexts(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    allowed_contexts = (
        "prohibit",
        "prohibits",
        "excluded",
        "blocked context",
        "unsafe source motif",
        "source motif retained for audit",
        "source_risk",
        "risk was avoided",
        "rather than",
        "does not",
        "do not",
        "no real",
        "no live",
        "tabletop",
        "synthetic",
        "fictional",
        "instructor-provided",
        "toy",
        "opt-in",
        "safe curriculum substitute",
        "safe curriculum treatment",
        "source title transformed",
    )
    blocked = BLOCKED_OPERATIONAL_PATTERN_PHRASES
    for path in generated_output_files(output_manuscript):
        if "bibliography-atlas" in path.parts or path.name == "references.md":
            continue
        for line in path.read_text(encoding="utf-8").lower().splitlines():
            for phrase in blocked:
                if phrase not in line:
                    continue
                assert any(context in line for context in allowed_contexts), f"{path}: {phrase}: {line}"

def test_safety_boundary_is_documented() -> None:
    safety = (PROJECT_ROOT / "docs" / "safety.md").read_text(encoding="utf-8").lower()
    assert "non-operational" in safety
    assert "synthetic" in safety
    assert "unauthorized" in safety
