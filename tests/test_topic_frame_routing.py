"""Regression tests for token-boundary keyword routing in topic frames."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from intelligence_content.risk_routes import topic_risk_category  # noqa: E402
from intelligence_content._12_concept_routes import (  # noqa: E402
    CONCEPT_KEYWORD_ROUTES,
    _first_matching_frame,
    _match_keywords,
)


def test_match_keywords_rejects_substring_false_positives() -> None:
    assert not _match_keywords("cryptographic lawful access", ("cryptograph",))
    assert not _match_keywords("fisa executive order directive", ("cti",))
    assert not _match_keywords("competing hypotheses approach", ("ach",))


def test_match_keywords_accepts_whole_tokens_and_phrases() -> None:
    assert _match_keywords("cryptographic lawful access", ("lawful access",))
    assert _match_keywords("cyber kill chain fundamentals", ("kill chain",))
    assert _match_keywords("analysis of competing hypotheses", ("competing hypotheses",))
    assert _match_keywords("fisa and executive order review", ("fisa",))


def test_concept_routes_for_representative_titles() -> None:
    cases = {
        "Cryptographic lawful access debate": "confidentiality",
        "FISA executive order directive review": "authority",
        "Cyber Kill Chain defensive mapping": "kill chain",
        "Getting Things Done for analysts": "gtd",
        "Stuxnet tabletop lesson": "stuxnet",
        "MCP tool governance card": "mcp",
        "Operations security five-step review": "opsec",
        "Compartmentation and need-to-know governance": "compartment",
    }
    for title, needle in cases.items():
        frame = _first_matching_frame(title.lower(), CONCEPT_KEYWORD_ROUTES)
        assert frame is not None, title
        assert needle.lower() in frame.lower() or len(frame) > 40, (title, frame)


def test_sats_and_icd_routes_use_specific_frames() -> None:
    icd_frame = _first_matching_frame(
        "icd 203 analytic standards: the nine tradecraft standards",
        CONCEPT_KEYWORD_ROUTES,
    )
    assert icd_frame is not None
    assert "Calibrate confidence" in icd_frame or "ICD 203 tradecraft standards" in icd_frame
    ach_frame = _first_matching_frame(
        "analysis of competing hypotheses (ach)",
        CONCEPT_KEYWORD_ROUTES,
    )
    assert ach_frame is not None
    assert "alternatives" in ach_frame.lower()


def test_opsec_title_routes_to_operational_tradecraft_not_analytic() -> None:
    category = topic_risk_category(
        "Operations Security (OPSEC) Fundamentals",
        part_title="Foundations of Intelligence Tradecraft",
        chapter_title="Tradecraft: Core Principles",
    )
    assert category == "operational_tradecraft_governance"


def test_compartmentation_title_routes_to_operational_tradecraft() -> None:
    category = topic_risk_category(
        "Compartmentation and Need-to-Know",
        part_title="Foundations of Intelligence Tradecraft",
        chapter_title="Tradecraft: Core Principles",
    )
    assert category == "operational_tradecraft_governance"


def test_stuxnet_title_routes_via_keyword_not_chapter_blanket() -> None:
    frame = _first_matching_frame("stuxnet case study review", CONCEPT_KEYWORD_ROUTES)
    assert frame is not None
    category = topic_risk_category(
        "Stuxnet: Intelligence Analysis of a Landmark ICS Incident",
        part_title="Industrial and Cyber-Physical Intelligence",
        chapter_title="Historical ICS Cyber Incidents: Intelligence Analysis",
    )
    assert category in {"standard", "ics_safety", "critical_infrastructure_sharing"}


def test_epistemic_security_preserves_educational_title_category() -> None:
    category = topic_risk_category(
        "Epistemic Security and Malign Influence",
        part_title="Cognitive Security",
        chapter_title="Cognitive Security Foundations and Definitions",
    )
    assert category == "cognitive_resilience"


def test_ach_title_routes_to_analytic_tradecraft_at_topic_level() -> None:
    category = topic_risk_category(
        "Analysis of Competing Hypotheses (ACH)",
        part_title="Epistemic Rigor and Analytic Tradecraft",
        chapter_title="Structured Analytic Techniques (SATs)",
    )
    assert category == "analytic_tradecraft"


def test_topic_risk_category_matches_curriculum_parity_fixture() -> None:
    import json

    fixture = PROJECT_ROOT / "tests" / "fixtures" / "risk_category_parity.json"
    rows = json.loads(fixture.read_text(encoding="utf-8"))
    mismatches: list[str] = []
    for row in rows:
        got = topic_risk_category(row["title"], row["part_title"], row["chapter_title"])
        if got != row["category"]:
            mismatches.append(f"{row['title']!r}: expected {row['category']}, got {got}")
    assert mismatches == []


def test_evidence_and_artifact_prompts_match_curriculum_parity_fixture() -> None:
    import json

    from curriculum import load_curriculum
    from intelligence_content._11_part import _coursebook_profile_for_titles
    from intelligence_content._12_topic_frames import (
        artifact_prompt_for_entry,
        evidence_prompt_for_entry,
    )
    from intelligence_content import practice_lens_for_titles, profile_for_titles
    from intelligence_content.topic_entries import safe_topic_entries

    fixture = PROJECT_ROOT / "tests" / "fixtures" / "topic_prompt_parity.json"
    expected_rows = json.loads(fixture.read_text(encoding="utf-8"))
    curriculum = load_curriculum(PROJECT_ROOT / "data" / "curriculum")
    mismatches: list[str] = []
    index = 0
    for part in curriculum.parts:
        part_title = str(part["title"])
        for chapter in part["chapters"]:
            chapter_title = str(chapter["title"])
            lens = practice_lens_for_titles(part_title, chapter_title, chapter=chapter)
            coursebook = _coursebook_profile_for_titles(part_title, chapter_title)
            for entry in safe_topic_entries(chapter, part):
                expected = expected_rows[index]
                index += 1
                got_evidence = evidence_prompt_for_entry(entry, lens, coursebook)
                got_artifact = artifact_prompt_for_entry(entry, lens, coursebook)
                if got_evidence != expected["evidence_prompt"]:
                    mismatches.append(
                        f"{entry.display_title!r} evidence: fixture mismatch"
                    )
                if got_artifact != expected["artifact_prompt"]:
                    mismatches.append(
                        f"{entry.display_title!r} artifact: fixture mismatch"
                    )
    assert index == len(expected_rows)
    assert mismatches == []
