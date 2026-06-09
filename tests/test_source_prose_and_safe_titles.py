"""Direct unit tests for the Turn-7 de-boilerplating and safe-title modules.

The reader-quality suite exercises these modules only incidentally, through
built-corpus snapshots. These tests pin their behaviour directly so a
regression in determinism, rotation spread, citation-noise handling, or the
high-risk title rewrite trips a focused unit failure rather than a diffuse
corpus-snapshot drift. (Added 2026-06-09 after a RedTeam audit flagged the
modules as covered only obliquely.)
"""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from intelligence_content import _source_prose as prose  # noqa: E402
from intelligence_content import _07_safe_titles as safe_titles  # noqa: E402


# --- _source_prose.stable_index -------------------------------------------------

def test_stable_index_is_deterministic_across_calls() -> None:
    assert prose.stable_index("Social Engineering", 4) == prose.stable_index("Social Engineering", 4)


def test_stable_index_pins_fixed_ordinal_digest() -> None:
    # Pinned literals lock the algorithm to the salt-free polynomial digest. If
    # someone swaps in Python's per-process salted hash(), these break (and the
    # build stops being reproducible), which is exactly the regression to catch.
    assert prose.stable_index("Social Engineering", 4) == 1
    assert prose.stable_index("the-nature-of-intelligence", 4) == 3


def test_stable_index_stays_in_range_and_handles_degenerate_modulo() -> None:
    for seed in ("a", "topic|3|use", "Counterintelligence Fundamentals"):
        for modulo in (2, 3, 4, 7):
            assert 0 <= prose.stable_index(seed, modulo) < modulo
    assert prose.stable_index("anything", 1) == 0
    assert prose.stable_index("anything", 0) == 0


def test_stable_index_spreads_across_all_buckets() -> None:
    # A degenerate index (e.g. always 0) would re-stamp one variant; confirm the
    # digest actually distributes distinct seeds across every bucket.
    seeds = [f"lesson-title-{n}" for n in range(64)]
    buckets = {prose.stable_index(seed, 4) for seed in seeds}
    assert buckets == {0, 1, 2, 3}


# --- _source_prose rotation banks ----------------------------------------------

def test_rotation_banks_have_distinct_variants() -> None:
    for bank in (prose.NOTE_INTROS, prose.USE_CLAUSES, prose.EVIDENCE_CLOSERS, prose.EVIDENCE_LEADS):
        assert len(bank) >= 4
        assert len(set(bank)) == len(bank)  # no duplicate variant re-stamps


def test_title_woven_banks_carry_title_placeholder() -> None:
    for bank in (prose.USE_CLAUSES, prose.EVIDENCE_CLOSERS, prose.EVIDENCE_LEADS):
        assert all("{title}" in variant for variant in bank)


def test_lead_clause_surfaces_one_sentence_deterministically() -> None:
    note = "First sentence here. Second sentence follows. Third one closes."
    first = prose.lead_clause(note, seed="alpha")
    assert first == prose.lead_clause(note, seed="alpha")
    assert first.count(".") == 1 and first.endswith(".")
    # An empty note yields no clause (so the caller drops the detail entirely).
    assert prose.lead_clause("") == ""


def test_note_carrier_picks_most_specific_note() -> None:
    notes = ["short", "the longest and most descriptive note of the set", "mid one"]
    assert prose.note_carrier(notes) == "the longest and most descriptive note of the set"


# --- _07_safe_titles.distinguishing_phrase -------------------------------------

def test_distinguishing_phrase_returns_empty_for_citation_noise() -> None:
    # The empty return is the case the artifact-prompt caller must guard (T7-01):
    # a bare year or a "Case Study: <year>" carries no distinguishing topic words.
    assert safe_titles.distinguishing_phrase("2021") == ""
    assert safe_titles.distinguishing_phrase("Case Study: 2019") == ""


def test_distinguishing_phrase_prefers_topic_specific_tail_after_generic_head() -> None:
    assert (
        safe_titles.distinguishing_phrase("Historical Foundations: Soviet Active Measures")
        == "Soviet Active Measures"
    )


def test_distinguishing_phrase_strips_parenthetical_and_keeps_contiguous_phrase() -> None:
    assert safe_titles.distinguishing_phrase("MICE Framework (11.5)") == "MICE Framework"


# --- _07_safe_titles high-risk rewrite -----------------------------------------

def test_is_generic_display_title_flags_category_fallbacks_only() -> None:
    assert safe_titles.is_generic_display_title(
        "AI-enabled recruitment-risk ethics and source-protection case study"
    )
    assert not safe_titles.is_generic_display_title("The Intelligence Cycle")


def test_safe_curriculum_treatment_rewrites_operational_title_to_educational() -> None:
    # The safety property: an operational-sounding source title is rewritten to a
    # bounded, educational label before it can become a lesson header.
    rewritten = safe_titles.safe_curriculum_treatment(
        "Dead Drops: Physical and Digital Methods",
        "Human Intelligence",
        "Tradecraft History",
    )
    assert rewritten == "Historical clandestine-communications ethics review"
    assert "dead drop" not in rewritten.lower()
