"""Behavioral tests for curriculum attribution and safe-title helpers."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from intelligence_content import _source_prose as prose  # noqa: E402
from intelligence_content import _07_safe_titles as safe_titles  # noqa: E402


def test_curriculum_annotation_preserves_context_and_key_binding() -> None:
    note = "Studies in Intelligence, Vol. 70, No. 1. This is curriculum commentary. Its antecedent stays visible."
    text = prose.curriculum_annotation("[@ageint025]", note)
    assert text == f"Curriculum annotation for [@ageint025]: {note}"
    assert prose.curriculum_annotation("[@ageint025]", "") == ""
    assert text == prose.curriculum_annotation("[@ageint025]", note)


# --- _07_safe_titles.distinguishing_phrase -------------------------------------


def test_distinguishing_phrase_returns_empty_for_citation_noise() -> None:
    # The empty return is the case the artifact-prompt caller must guard (T7-01):
    # a bare year or a "Case Study: <year>" carries no distinguishing topic words.
    assert safe_titles.distinguishing_phrase("2021") == ""
    assert safe_titles.distinguishing_phrase("Case Study: 2019") == ""


def test_distinguishing_phrase_prefers_topic_specific_tail_after_generic_head() -> None:
    assert safe_titles.distinguishing_phrase("Historical Foundations: Soviet Active Measures") == "Soviet Active Measures"


def test_distinguishing_phrase_strips_parenthetical_and_keeps_contiguous_phrase() -> None:
    assert safe_titles.distinguishing_phrase("MICE Framework (11.5)") == "MICE Framework"


# --- _07_safe_titles high-risk rewrite -----------------------------------------


def test_is_generic_display_title_flags_category_fallbacks_only() -> None:
    assert safe_titles.is_generic_display_title("AI-enabled recruitment-risk ethics and source-protection case study")
    assert not safe_titles.is_generic_display_title("The Intelligence Cycle")


def test_safe_curriculum_treatment_rewrites_operational_title_to_educational() -> None:
    # The safety property: an operational-sounding source title is rewritten to a
    # bounded, educational label before it can become a lesson header.
    rewritten = safe_titles.safe_curriculum_treatment("Dead Drops: Physical and Digital Methods", "Human Intelligence", "Tradecraft History")
    assert rewritten == "Historical clandestine-communications ethics review"
    assert "dead drop" not in rewritten.lower()
