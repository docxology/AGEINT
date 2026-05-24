"""Focused regression coverage for AGEINT coursebook generator branches.

Imports of ``manuscript_manifest._01_part`` and ``manuscript_variables._01_part``
exercise private branch paths intentionally for coverage of part-module edges.
"""

from __future__ import annotations

from pathlib import Path

import pytest

import curriculum
import intelligence_content as ic
import manuscript_manifest._01_part as mm
import manuscript_variables._01_part as mv
import source_identity
import template_resolver

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"


def test_safe_curriculum_treatment_covers_contextual_title_branches() -> None:
    cases = [
        ("XZ Utils Jia Tan maintainer trust", "Supply Chain", "Supply Chain Intelligence Attacks", "XZ Utils"),
        ("Friendly yet aggressive signature", "Supply Chain", "Supply Chain Intelligence Attacks", "Maintainer-pressure"),
        ("Maintainer targeting", "Supply Chain", "Supply Chain Intelligence Attacks", "Maintainer-risk"),
        ("Sock Puppetry as HUMINT Cover Tradecraft", "Supply Chain", "Supply Chain Intelligence Attacks", "Maintainer-contact"),
        ("PythonREPL arbitrary code execution", "", "", "Python REPL sandbox"),
        ("AutoGen Code-Execution Exploit Chain", "", "", "AutoGen sandbox"),
        ("LLM-based autonomous cyberattacks", "", "", "LLM-agent cyber-misuse"),
        ("Multi-agent collaboration in cyberattacks", "", "", "Multi-agent cyber-misuse"),
        ("6G IoT satellite UAV cyberattack capabilities", "", "", "Networked-device cyber-misuse"),
        ("Automated Weaponization: Malware Generation", "", "", "Malware-misuse"),
        ("Spear-phishing automation", "", "", "Phishing-resilience"),
        ("Bulk collection and metadata analysis", "", "", "SIGINT metadata minimization"),
        ("Covert communications", "SIGINT", "Signals Intelligence", "Communications-security history"),
        ("RF spectrum monitoring", "", "", "RF-spectrum governance"),
        ("Steganography", "", "", "Steganography detection-literacy"),
        ("Meeting Structures: overt and covert", "", "", "Historical meeting-structure"),
        ("Dead Drops: physical and digital", "", "", "Historical clandestine-communications"),
        ("Surveillance detection route", "", "", "Historical surveillance-risk"),
        ("Cutouts and intermediaries", "", "", "Historical cutout-and-intermediary"),
        ("Fronts and shell entities", "", "", "Historical front-entity"),
        ("Running agents-in-place tasking", "", "", "Historical agent-tasking"),
        ("Burning, exfiltrating, and terminating agents", "", "", "Historical extraction-and-termination"),
        ("The Lubyanka Files: 29 KGB Training Manuals", "", "", "Declassified training-manual"),
        ("Working-with-Agents Doctrine", "", "", "Declassified source-protection"),
        ("Psychological Methods and Manipulation of Agents", "", "", "Declassified psychological-pressure"),
        ("On Organizing Work with Confidential Contacts", "", "", "Declassified confidential-contact"),
        ("Tasks of a KGB Resident Abroad", "", "", "Declassified residency-management"),
        ("KGB Alpha Team Training Manual", "", "", "Declassified special-unit"),
        ("Eli Cohen: Deep Cover Agent in Syria", "", "", "Declassified cover-identity"),
        ("Operation Wrath of God: Targeted Killing", "", "", "Declassified covert-action"),
        ("Search Engine Tradecraft: Google Dorking and Shodan", "", "", "Search-exposure provenance"),
        ("Social Media OSINT: Scraping and graph analysis", "", "", "Social-source provenance"),
        ("Maltego: Graph-Based OSINT Investigation", "", "", "Graph-analysis provenance"),
        ("Recon-ng: Python-Based Reconnaissance Framework", "", "", "Custom-source integration"),
        ("SpiderFoot: Automated OSINT Collection", "", "", "Automated-source aggregation"),
        ("FOCA, TheHarvester, Sherlock: Targeted Investigation Tools", "", "", "Identity-data minimization"),
        ("Geolocation and IP Attribution", "", "", "IP-geolocation uncertainty"),
        ("Initial Access and Execution", "", "", "Cyber access-and-execution"),
        ("Credential Access and Lateral Movement", "", "", "Cyber credential-and-movement"),
        ("Command & Control and Exfiltration", "", "", "Cyber command, data-loss"),
        ("Domain Fronting and Bulletproof Hosting", "", "", "Cyber infrastructure-abuse"),
        ("Modify Controller and firmware", "", "", "ICS controller-change"),
        ("Project file infection", "", "", "ICS firmware"),
        ("Block communications and alarm suppression", "", "", "ICS alarm"),
        ("Impair process control", "", "", "ICS process-safety"),
        ("Adversarial Cognitive Operations: PSYOP", "", "", "Cognitive influence-analysis"),
        ("AI-assisted cognitive security intervention systems", "", "", "AI-assisted resilience-tool"),
        ("Persistent target monitoring", "", "", "no real targets"),
        ("Multi-source data harvesting", "", "", "fixed inputs"),
        ("Autonomous SOC", "", "", "SOC tabletop"),
        ("Longitudinal target tracking", "", "", "tracks evidence changes"),
        ("Penetration testing automation", "", "", "Control-coverage"),
        ("NOC legend and cover document", "", "", "Identity-and-provenance"),
        ("Population-scale intervention delivery", "", "", "Opt-in media-literacy"),
        (
            "Analysis of Competing Hypotheses (ACH)",
            "Epistemic Rigor",
            "Structured Analytic Techniques (SATs)",
            "Analysis of Competing Hypotheses",
        ),
        (
            "ICD 203 Analytic Standards: The Nine Tradecraft Standards",
            "Epistemic Rigor",
            "Structured Analytic Techniques (SATs)",
            "ICD 203",
        ),
        (
            "The Science Behind Getting Things Done (GTD): Cognitive Foundations",
            "Productivity Intelligence",
            "The Intelligent Operator as Cognitive Athlete",
            "Getting Things Done",
        ),
        (
            "NASA-TLX and Analyst Workload Monitoring",
            "Productivity Intelligence",
            "The Intelligent Operator as Cognitive Athlete",
            "NASA-TLX",
        ),
    ]

    for title, part, chapter, expected in cases:
        assert expected in ic.safe_curriculum_treatment(title, part, chapter)


def test_coursebook_lesson_helpers_cover_domain_specific_frames() -> None:
    part = {"title": "AGEINT: Agentic Intelligence"}
    chapter = {
        "title": "Active Inference and AGEINT",
        "number": 35,
        "sections": [
            {"number": "35.1", "title": "The Free Energy Principle and Predictive Processing"},
            {"number": "35.2", "title": "Active Inference as Computational Model of Intelligence Agent Behavior"},
            {"number": "35.3", "title": "Shared Protentions in Multi-Agent Active Inference"},
            {"number": "35.4", "title": "Active Inference for Social Organization and Intelligence Communities"},
            {"number": "35.5", "title": "VERSES AI Research: Multi-Scale Active Inference Architectures"},
            {"number": "35.6", "title": "Cognitive Security Through the Active Inference Lens"},
            {"number": "35.7", "title": "Applications: Deception Detection, Surprise Minimization, Threat Modeling"},
            {"number": "35.8", "title": "Applications of Active Inference and FEP in Intelligence (TU Delft Thesis)"},
        ],
    }

    lessons = ic.chapter_topic_lessons(chapter, part)

    assert "prediction-error concept card" in lessons
    assert "toy agent-model card" in lessons
    assert "shared-expectation register" in lessons
    assert "institutional feedback-loop map" in lessons
    assert "architecture-claim card" in lessons
    assert "fictional narrative-risk map" in lessons
    assert "threat-model review card" in lessons
    assert "research question, method, evidence base" in lessons

    mixed_part = {"title": "Foundations"}
    mixed_chapter = {
        "title": "Mixed Coursebook Concepts",
        "sections": [
            {"number": "1", "title": "SolarWinds and SBOM assurance"},
            {"number": "2", "title": "CVE-2024-3094 backdoor"},
            {"number": "3", "title": "APT29 attribution"},
            {"number": "4", "title": "UKUSA Five Eyes"},
            {"number": "5", "title": "Cryptographic lawful access"},
            {"number": "6", "title": "COMINT and ELINT"},
            {"number": "7", "title": "MICE and RASCLS"},
            {"number": "8", "title": "Cyber kill chain and ATT&CK"},
            {"number": "9", "title": "FISA executive order directive"},
            {"number": "10", "title": "GEOINT imagery geospatial"},
            {"number": "11", "title": "Beneficial ownership sanctions financial"},
            {"number": "12", "title": "Analysis of Competing Hypotheses"},
        ],
    }

    mixed_lessons = ic.chapter_topic_lessons(mixed_chapter, mixed_part)

    assert "package provenance" in mixed_lessons
    assert "vulnerability record as an assurance case" in mixed_lessons
    assert "APT29 attribution** uses attribution indicators cautiously" in mixed_lessons
    assert "alliance governance" in mixed_lessons
    assert "policy and assurance trade-off" in mixed_lessons
    assert "communications content from electronic signatures" in mixed_lessons
    assert "motivation taxonomy" in mixed_lessons
    assert "defensive vocabulary" in mixed_lessons
    assert "authority, oversight, retention" in mixed_lessons
    assert "quality and uncertainty problem" in mixed_lessons
    assert "due-diligence evidence" in mixed_lessons
    assert "disconfirming evidence" in mixed_lessons


def test_manifest_support_sections_and_visual_fallbacks_have_concrete_content(tmp_path: Path) -> None:
    chapter = {"title": "Branch Coverage Chapter", "citations": [1], "sections": []}
    part = {"title": "Branch Coverage Part"}

    text_blocks = [
        mm._safe_practice_lab(chapter),
        mm._failure_mode_drill(chapter),
        mm._instructor_artifact(chapter),
        mm._authority_accountability_model(chapter, part),
        mm._data_provenance_model(chapter, part),
        mm._evaluation_assurance_protocol(chapter),
        mm._compliance_rights_map(chapter),
        mm._safe_substitution_patterns(chapter),
        mm._capstone_deliverable(chapter, part),
        mm._instructor_facilitation_notes(chapter),
        mm._refresh_triggers(chapter),
        mm._accessibility_udl_review(chapter),
        mm._procurement_vendor_oversight(chapter),
        mm._hria_dpia_worksheet(chapter),
        mm._data_lineage_registry(chapter),
        mm._assessment_integrity_protocol(chapter),
        mm._agent_incident_response_drill(chapter),
        mm._role_based_competency_map(chapter),
        mm._adversarial_assurance_cycle(chapter),
        mm._model_dataset_documentation_card(chapter),
        mm._transparency_communication_notice(chapter),
        mm._records_retention_audit_trail(chapter),
        mm._release_change_control_gate(chapter),
        mm._risk_exception_acceptance_memo(chapter),
        mm._learner_support_accommodation_plan(chapter),
        mm._instructor_question_bank(chapter),
        mm._remediation_backlog(chapter),
        mm._runtime_section_map(chapter, part),
        mm._module_thesis(chapter, part),
        mm._domain_practice_studio(chapter, part),
    ]

    joined = "\n".join(text_blocks)
    assert "Branch Coverage Chapter" in joined
    assert "Module source spine" in joined
    assert "authorized learning question" in joined

    registry = mm._SlugRegistry()
    assert registry.unique("chapter", "Same Title") == "same-title"
    assert registry.unique("chapter", "Same Title") == "same-title-2"

    section = mm.ManuscriptSection(
        kind="chapter",
        title="No Figure Chapter",
        relative_path="parts/example/no-figure.md",
        template_name="chapter.md",
        context={},
        order=1,
        parent_label="sec:part-example",
    )
    manifest = mm.ManuscriptManifest([section], [], [])
    assert "No figure registry" in mm._visual_synthesis(tmp_path, tmp_path, section, manifest, [])


def test_variable_helpers_cover_empty_inputs_safe_appendices_and_reference_fallbacks() -> None:
    assert mv.section_label("Chapter", "A/B", "C") == "sec:chapter_a_b_c"
    assert "No direct source-guide citation" in mv.citation_spine([])
    assert "Module-level synthesis" in mv.section_rows([])

    pattern_rows = mv.section_rows(
        [
            {"number": "32.1", "title": "Pattern 1: Solo Reasoner - test", "citations": [1]},
            {"number": "32.1a", "title": "Methods: bounded source reading", "citations": [2]},
        ],
        safe_patterns=True,
    )
    assert "Focused Analytic Reasoner" in pattern_rows

    appendix = {
        "items": [
            {"title": "A.1 Safe Item", "citations": []},
            {"title": "B.5 Memory-Enabled Agent: Longitudinal Target Tracking", "citations": [1]},
            {"title": "Unsafe motif without prefix: Malware Generation", "citations": []},
        ]
    }
    rows = mv.appendix_rows(appendix)
    assert "A.1 Safe Item" in rows
    assert "operational wording transformed" in rows
    assert "source item retained for audit" in rows

    for title in [
        "OSINT source audit",
        "GEOINT imagery review",
        "HUMINT source-protection review",
        "SOC control-coverage review",
        "ICS tabletop",
        "Cognitive media-literacy",
        "plain title",
    ]:
        assert mv._appendix_allowed_fixture(title)
        assert mv._appendix_rejected_action(title)
        assert mv._appendix_required_artifact(title)

    bib = mv.reference_bibtex(
        [
            {"key": "ageint999", "number": 999, "title": "Numbered", "url": "", "note": ""},
            {"key": "custom123", "title": "Key Digits", "url": "", "note": ""},
            {"key": "custom", "title": "No Digits", "url": "", "note": ""},
        ]
    )
    assert "SIST Guide Reference 999" in bib
    assert "SIST Guide Reference 123" in bib
    assert "SIST Guide Reference}" in bib


def test_curriculum_identity_and_template_error_branches(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    payload = curriculum.load_curriculum(DATA)
    assert payload.reference("001")["key"] == "ageint001"
    assert payload.reference(1)["key"] == "ageint001"
    assert payload.appendix("a")["letter"] == "A"
    with pytest.raises(KeyError):
        payload.part(999)
    with pytest.raises(KeyError):
        payload.chapter(999)
    with pytest.raises(KeyError):
        payload.appendix("z")
    with pytest.raises(KeyError):
        payload.reference("missing")

    missing_source = tmp_path / "missing.md"
    missing_output = tmp_path / "missing.json"
    with pytest.raises(FileNotFoundError):
        curriculum.build_curriculum(missing_source, missing_output)

    lock = source_identity.build_source_identity_lock(DATA, max_reference=2)
    assert lock["locked_reference_count"] == 2
    with pytest.raises(FileNotFoundError):
        source_identity.build_source_identity_lock(tmp_path / "missing.md")

    isolated = tmp_path / "isolated"
    isolated.mkdir()
    monkeypatch.delenv("TEMPLATE_REPO", raising=False)
    monkeypatch.delenv("DOCXOLOGY_TEMPLATE_REPO", raising=False)
    assert template_resolver.resolve_template_repo(isolated) is None
    assert template_resolver.ensure_template_repo_on_path(isolated) is None
