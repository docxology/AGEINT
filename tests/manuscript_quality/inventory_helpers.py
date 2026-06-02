"""Shared constants and helpers for generated manuscript inventory tests."""

from __future__ import annotations

import re
from pathlib import Path

from intelligence_content import INTELLIGENCE_RESEARCH_ANCHORS
from manuscript_variables import SOURCE_QUALITY_ANCHORS
from safety_contract import BLOCKED_OPERATIONAL_PHRASES, DIRECT_TASK_MOTIF_RE

PROJECT_ROOT = Path(__file__).resolve().parents[2]
MANUSCRIPT = PROJECT_ROOT / "manuscript"
TEMPLATES = MANUSCRIPT / "templates"
OUTPUT_MANUSCRIPT = PROJECT_ROOT / "output" / "manuscript"


def manuscript_dir(output_root: Path) -> Path:
    """Return the generated manuscript tree under an output root."""
    return output_root / "manuscript"


def _resolve_manuscript(output_manuscript: Path | None) -> Path:
    return output_manuscript if output_manuscript is not None else OUTPUT_MANUSCRIPT


DATA = PROJECT_ROOT / "data" / "curriculum"
TOKEN_RE = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}")
REQUIRED_MODULE_SECTIONS = {
    "Textbook primer",
    "Learning outcomes",
    "Core vocabulary",
    "Topic lessons",
    "Worked safe example",
    "Practice sequence",
    "Knowledge check",
    "Module architecture",
    "Evidence and source canon",
    "Research-backed synthesis",
    "Agentic translation boundary",
    "Governance, rights, and assurance",
    "Assessment artifacts and capstone pathway",
    "Refresh, safety, and source maps",
    "Review checklist",
    "Cross-links",
}
RAW_PSEUDO_HEADING_PREFIXES = {
    "V2 source-lane extension:",
    "Deep expansion:",
    "Evidence-package expansion:",
    "V2 AGEINT-depth extension:",
}
REMOVED_REPEATED_MODULE_SECTIONS = {
    "Accessibility and UDL review",
    "Procurement and vendor oversight",
    "HRIA and DPIA worksheet",
    "Data lineage registry",
    "Assessment integrity protocol",
    "Agent incident response drill",
    "Role-based competency map",
    "Adversarial assurance cycle",
    "Model and dataset documentation card",
    "Transparency and communication notice",
    "Records retention and audit trail",
    "Release and change-control gate",
    "Risk exception and acceptance memo",
    "Learner support and accommodation plan",
    "Instructor question bank",
    "Remediation backlog",
}
REMOVED_META_PHRASES = {
    "converts the source-guide outline into",
    "an AGEINT curriculum unit with atlas",
    "playbook affordances",
    "Students should leave with",
    "Explain the role of",
    "This module is part of",
    "Generated section context",
    "Visual references for this generated section",
    "Source-guide topic translated",
    "Treat source locus",
    "Runtime subsection",
}
REMOVED_FILLER_PHRASES = {
    "Source-guide topic translated into a safe classroom concept",
    "The classroom move is to define the concept",
    "reviewable artifact instead of a loose idea",
    "Learners use those sources",
    "Generated section context",
    "Visual references for this generated section",
    "safe classroom concept for evidence review",
}
REMOVED_GENERATED_SCAFFOLD_PHRASES = {
    "as a coursebook concept",
    "fields fields",
    "generic",
    "placeholder",
    "scaffold",
    "scaffolding",
    "scaffolds",
    "reusable methods scaffold",
    "Capstone scaffold",
    "Primary visual reference:",
    "then restate the idea",
    "reviewer who has not read the source guide",
    "- Explain **",
    "**Concept.** Explain how",
    "The teaching task is",
    "Each lesson card teaches",
    "runtime subsection",
    "runtime-derived subsection",
    "source-guide subsection",
    "Which wording, scaffold",
}
REMOVED_GENERIC_CONCEPT_PHRASES = {
    "defensible claim whose meaning",
    "treats each source topic through",
    "parsed AGEINT source spine",
    "study sequence has three passes",
}
SOURCE_QUALITY_KEYS = {anchor["key"] for anchor in SOURCE_QUALITY_ANCHORS} | {
    anchor.key for anchor in INTELLIGENCE_RESEARCH_ANCHORS
}
REQUIRED_REFRESHED_ANCHOR_KEYS = {
    "official_nsf_ai_agent_ecosystems",
    "official_cdc_agentic_research_public_health",
    "official_nist_ai_rmf_playbook",
    "official_iso_iec_42001_ai_management",
    "official_oasis_stix_21",
    "official_oasis_taxii_21",
    "official_cisa_cross_sector_cpg",
    "official_cisa_kev_catalog",
    "official_nga_geoint_ai",
    "official_iso_19157_data_quality",
    "official_nist_privacy_framework",
    "official_fincen_boi",
    "official_ofac_compliance_commitments",
    "official_fatf_virtual_assets_guidance",
    "official_nist_sp_1800_10_ics_integrity",
    "official_wipo_ai_ip_policy",
    "official_w3c_wcag_22",
    "official_cast_udl_guidelines_30",
    "official_doj_ada_title_ii_web_rule",
    "official_edpb_dpia_faq",
    "official_oecd_public_procurement_recommendation",
    "official_open_contracting_data_standard",
    "official_nist_sp_800_61r3_incident_response",
    "official_enisa_ai_cybersecurity_challenges",
    "official_nist_ai_security_resilience",
    "official_oecd_open_government_recommendation",
    "official_w3c_vc_data_integrity",
    "scholarly_model_cards_model_reporting",
    "scholarly_datasheets_for_datasets",
    "official_uk_algorithmic_transparency_hub",
    "official_uk_algorithmic_transparency_guidance",
    "official_nist_sp_800_218a_ai_ssdf",
    "official_us_access_board_revised_508_standards",
    "official_nist_aria_pilot_evaluation_report",
    "official_nara_ai_use_case_inventory",
    "official_omb_m_25_21_federal_ai_governance",
    "official_omb_m_25_22_federal_ai_acquisition",
    "official_nist_ai_600_1_generative_ai_profile",
    "official_cisa_ai_red_teaming_tev",
    "official_cisa_ai_data_security_best_practices",
    "official_nist_ai_rmf_critical_infrastructure_profile_concept",
    "official_oecd_governing_with_ai_public_sector",
    "official_nara_2025_ai_compliance_plan",
    "official_canada_agentic_ai_guide",
    "official_canada_algorithmic_impact_assessment",
    "official_canada_ai_register",
    "official_canada_ai_strategy_2025_2027",
    "official_oecd_ai_risks_incidents",
    "official_oecd_ai_incident_reporting_framework",
    "official_un_global_digital_compact",
    "official_nist_dioptra",
    "official_cisa_deploying_ai_systems_securely",
    "official_cisa_secure_by_demand_ot_procurement",
    "official_cisa_ot_asset_inventory_guidance",
    "official_cisa_ot_definitive_architecture",
}
# Re-export for manuscript-safety tests (canonical set lives in src/safety_contract.py).
BLOCKED_OPERATIONAL_PATTERN_PHRASES = BLOCKED_OPERATIONAL_PHRASES
DIRECT_STUDENT_TASK_MOTIFS = DIRECT_TASK_MOTIF_RE
REQUIRED_SOURCE_LANES = {
    "ai_conformity_compliance",
    "education_assessment",
    "public_sector_agentic_ai",
    "cross_border_data_spaces",
    "human_rights_governance",
    "agent_interoperability_standards",
    "workforce_governance",
    "model_data_provenance",
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
}
REQUIRED_V2_DOCS = {
    "accessibility_rights_review.md",
    "adversarial_assurance.md",
    "agent_incident_response.md",
    "data_lineage_registry.md",
    "evidence_package_map.md",
    "instructor_guide.md",
    "learner_support_assessment.md",
    "procurement_vendor_governance.md",
    "records_retention_audit.md",
    "release_change_control.md",
    "safety_audit.md",
    "source_identity_stability.md",
    "source_lane_map.md",
    "source_refresh_ledger.md",
    "transparency_notice_workflow.md",
    "v2_expansion_map.md",
}


def generated_output_files(output_manuscript: Path | None = None) -> list[Path]:
    root = _resolve_manuscript(output_manuscript)
    return sorted(
        path
        for path in root.rglob("*.md")
        if path.name not in {"AGENTS.md", "README.md"}
    )


def generated_chapter_files(output_manuscript: Path | None = None) -> list[Path]:
    root = _resolve_manuscript(output_manuscript)
    return [
        path
        for path in sorted((root / "parts").glob("*/*/00-overview.md"))
    ]


def chapter_text(path: Path) -> str:
    return "\n\n".join(
        fragment.read_text(encoding="utf-8")
        for fragment in sorted(path.parent.glob("*.md"))
    )


def chapter_relative(path: Path, output_manuscript: Path | None = None) -> str:
    root = _resolve_manuscript(output_manuscript)
    return path.parent.relative_to(root / "parts").as_posix()


def section_text(text: str, heading: str) -> str:
    marker = f"## {heading}"
    assert marker in text
    return text.split(marker, 1)[1].split("\n## ", 1)[0]


def markdown_table_rows(section: str) -> list[list[str]]:
    rows: list[list[str]] = []
    for line in section.splitlines():
        if not line.startswith("| ") or line.startswith("|---"):
            continue
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if cells and cells[0] in {"Term", "Course topic", "Source topic", "Move", "Step"}:
            continue
        rows.append(cells)
    return rows
