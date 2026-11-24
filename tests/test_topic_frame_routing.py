"""Regression tests for token-boundary keyword routing in topic frames."""

from __future__ import annotations

import sys
from pathlib import Path

from dataclasses import replace

import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from intelligence_content.risk_routes import topic_risk_category  # noqa: E402
from intelligence_content._12_concept_routes import (  # noqa: E402
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


def test_opsec_title_routes_to_operational_tradecraft_not_analytic() -> None:
    category = topic_risk_category("Operations Security (OPSEC) Fundamentals", part_title="Foundations of Intelligence Tradecraft", chapter_title="Tradecraft: Core Principles")
    assert category == "operational_tradecraft_governance"


def test_compartmentation_title_routes_to_operational_tradecraft() -> None:
    category = topic_risk_category("Compartmentation and Need-to-Know", part_title="Foundations of Intelligence Tradecraft", chapter_title="Tradecraft: Core Principles")
    assert category == "operational_tradecraft_governance"


def test_epistemic_security_preserves_educational_title_category() -> None:
    category = topic_risk_category("Epistemic Security and Malign Influence", part_title="Cognitive Security", chapter_title="Cognitive Security Foundations and Definitions")
    assert category == "cognitive_resilience"


def test_ach_title_routes_to_analytic_tradecraft_at_topic_level() -> None:
    category = topic_risk_category("Analysis of Competing Hypotheses (ACH)", part_title="Epistemic Rigor and Analytic Tradecraft", chapter_title="Structured Analytic Techniques (SATs)")
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


@pytest.fixture(scope="module")
def curriculum_topics():
    from curriculum import load_curriculum
    from intelligence_content import practice_lens_for_titles, profile_for_titles
    from intelligence_content._09_part import _coursebook_profile_for_titles
    from intelligence_content.topic_entries import safe_topic_entries

    topics = {}
    for part in load_curriculum(PROJECT_ROOT / "data" / "curriculum").parts:
        for chapter in part["chapters"]:
            part_title, chapter_title = str(part["title"]), str(chapter["title"])
            topics[int(chapter["number"])] = (
                safe_topic_entries(chapter, part),
                _coursebook_profile_for_titles(part_title, chapter_title, chapter=chapter),
                profile_for_titles(part_title, chapter_title, chapter=chapter),
                practice_lens_for_titles(part_title, chapter_title, chapter=chapter),
                chapter_title,
            )
    return topics


def _fields_for(entry, context):
    from intelligence_content.topic_lessons import resolve_topic_lesson_fields

    _, coursebook, profile, lens, chapter_title = context
    return resolve_topic_lesson_fields(
        entry, coursebook=coursebook, profile=profile, lens=lens,
        lesson_index=1, chapter_title=chapter_title,
    )


def test_all_pattern_identities_ignore_competing_source_keywords(curriculum_topics):
    context = curriculum_topics[32]
    assert {entry.source_locus for entry in context[0]} == {f"Pattern {n}" for n in range(1, 21)}
    for entry in context[0]:
        colliding = replace(entry, raw_title="SIGINT dark web GEOINT MICE brain reasoning")
        original, changed = _fields_for(entry, context), _fields_for(colliding, context)
        assert original.concept == changed.concept
        assert original.evidence_prompt == changed.evidence_prompt
        assert original.artifact_prompt == changed.artifact_prompt
        assert original.misconception == changed.misconception
        assert original.why_it_matters == changed.why_it_matters
        assert original.transfer_task == changed.transfer_task


@pytest.mark.parametrize(
    ("chapter", "locus"),
    [(33, "33.6.2"), (31, "31.2"), (31, "31.3.1"),
     (31, "31.3.2"), (33, "33.5.1"), (36, "36.5")],
)
def test_explicit_display_subject_survives_raw_title_collisions(curriculum_topics, chapter, locus):
    context = curriculum_topics[chapter]
    entry = next(entry for entry in context[0] if entry.source_locus == locus)
    fields = _fields_for(entry, context)
    colliding = replace(entry, raw_title="MICE GEOINT imagery CIA NSA dark web brain")
    changed = _fields_for(colliding, context)
    assert fields.concept == changed.concept
    assert fields.evidence_prompt == changed.evidence_prompt
    assert fields.artifact_prompt == changed.artifact_prompt
    assert fields.misconception == changed.misconception
    assert fields.why_it_matters == changed.why_it_matters
    assert fields.transfer_task == changed.transfer_task

