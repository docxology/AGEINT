"""Behavioral contracts for safe title routing, identifiers and input errors."""

from __future__ import annotations

from pathlib import Path

import pytest

import curriculum
import intelligence_content as ic
from manuscript_manifest.types import SlugRegistry
import manuscript_variables._01_part as mv1
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
        ("Analysis of Competing Hypotheses (ACH)", "Epistemic Rigor", "Structured Analytic Techniques (SATs)", "Analysis of Competing Hypotheses"),
        ("ICD 203 Analytic Standards: The Nine Tradecraft Standards", "Epistemic Rigor", "Structured Analytic Techniques (SATs)", "ICD 203"),
        ("The Science Behind Getting Things Done (GTD): Cognitive Foundations", "Productivity Intelligence", "The Intelligent Operator as Cognitive Athlete", "Getting Things Done"),
        ("NASA-TLX and Analyst Workload Monitoring", "Productivity Intelligence", "The Intelligent Operator as Cognitive Athlete", "NASA-TLX"),
    ]

    for title, part, chapter, expected in cases:
        assert expected in ic.safe_curriculum_treatment(title, part, chapter)


def test_slug_registry_disambiguates_duplicate_titles() -> None:
    registry = SlugRegistry()
    assert registry.unique("chapter", "Same Title") == "same-title"
    assert registry.unique("chapter", "Same Title") == "same-title-2"


def test_section_labels_normalize_identifier_segments() -> None:
    assert mv1.section_label("Chapter", "A/B", "C") == "sec:chapter_a_b_c"


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
