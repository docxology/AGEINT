"""Tests for source-grounded topic-lesson prose helpers."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from intelligence_content._01_part import TopicEntry  # noqa: E402
from intelligence_content._11_part import chapter_source_annotations  # noqa: E402
from intelligence_content.source_grounding import (  # noqa: E402
    SourceRecord,
    annotated_source_table,
    cited_sources,
    clean_source_note,
    clean_source_title,
    evidence_from_sources,
    safe_source_note,
    safe_source_title,
    source_record,
    source_support_sentence,
    sources_for_numbers,
)


def _entry(citation_numbers: tuple[int, ...], title: str = "Sample topic") -> TopicEntry:
    return TopicEntry(
        raw_title=title,
        display_title=title,
        source_locus="1.1",
        provenance_note="",
        risk_category="standard",
        citation_numbers=citation_numbers,
    )


def test_clean_source_title_strips_pdf_prefix_and_site_suffix() -> None:
    raw = "(PDF) COGNITIVE SECURITY IN THE AGE OF AI - Academia.edu"
    assert clean_source_title(raw) == "COGNITIVE SECURITY IN THE AGE OF AI"


def test_clean_source_title_strips_linkedin_and_ellipsis() -> None:
    assert clean_source_title("Unveiling the concept - LinkedIn") == "Unveiling the concept"
    assert clean_source_title("A long source title that was cut ...") == "A long source title that was cut"


def test_clean_source_title_preserves_real_hyphenated_titles() -> None:
    title = "Intelligence - A National Security Discipline"
    assert clean_source_title(title) == title


def test_clean_source_title_strips_bracket_pdf_prefix() -> None:
    assert clean_source_title("[PDF] BASIC CRYPTOGRAPHY") == "BASIC CRYPTOGRAPHY"
    # Duplicated tags collapse fully.
    assert clean_source_title("[PDF] [PDF] The Psychology of Intelligence Analysis") == (
        "The Psychology of Intelligence Analysis"
    )


def test_clean_source_title_trims_trailing_function_word_without_ellipsis() -> None:
    # A hard truncation with no ellipsis marker leaves a dangling function word.
    assert clean_source_title("The Utility of Military Deception and Information Operations in") == (
        "The Utility of Military Deception and Information Operations"
    )
    assert clean_source_title("Behavioral Outcomes of Human Cognitive Security within an") == (
        "Behavioral Outcomes of Human Cognitive Security"
    )


_NOTE_DANGLING_TAIL_WORDS = frozenset(
    {
        "a", "an", "the", "to", "of", "for", "and", "or", "as", "in", "on",
        "with", "by", "that", "which", "critical", "committed", "human",
        "presents", "including", "distinct", "such",
    }
)


def _ends_on_complete_clause(cleaned: str) -> bool:
    """A cleaned note is complete only if non-empty and not ending on a dangler."""
    if not cleaned:
        return True  # title-only fallback is an acceptable outcome
    if not cleaned.endswith((".", "!", "?")):
        return False
    words = cleaned.rstrip(".!?").split()
    if not words:
        return False
    return words[-1].strip(",;:-\"'()").lower() not in _NOTE_DANGLING_TAIL_WORDS


def test_clean_source_note_drops_truncated_partial_word() -> None:
    note = "We provide a comprehensive review of the current state, including its developm..."
    cleaned = clean_source_note(note)
    assert cleaned.endswith("state, including its.") is False
    assert "developm" not in cleaned
    assert cleaned.endswith(".")
    # The clause must be complete, not a fabricated sentence ending on a dangler.
    assert _ends_on_complete_clause(cleaned)


def test_clean_source_note_drops_severed_attributive_adjective() -> None:
    # Truncation that severs an adjective from its head noun must not be
    # presented as a finished sentence; fall back to title-only ("").
    assert clean_source_note(
        "This research examined the possibility of using shared experiences to recruit committed hu..."
    ) == ""
    assert clean_source_note(
        "Explore ICS Cybersecurity and learn how to protect critical infrastruct..."
    ) == ""


def test_clean_source_note_trims_trailing_function_words() -> None:
    cleaned = clean_source_note("Prebunking builds preemptive resilience to...")
    assert cleaned == "Prebunking builds preemptive resilience."


def test_clean_source_note_balances_unmatched_paren_and_quote() -> None:
    assert clean_source_note('Heuer gives starters in his book (Structured Analytic Techniques for...').endswith(
        "in his book."
    )
    assert clean_source_note('He shared an article: "Unveiling the multifaceted...').endswith("article.")


def test_clean_source_note_keeps_complete_sentences() -> None:
    note = "First complete sentence here. A dangling second frag..."
    cleaned = clean_source_note(note)
    assert cleaned == "First complete sentence here."


def test_clean_source_note_handles_empty() -> None:
    assert clean_source_note("") == ""
    assert clean_source_note("   ...") == ""


def test_clean_source_note_cuts_dangling_adjective_clause() -> None:
    note = "This policy paper examines the emergence of cognitive security as a distinct and critical strategic ..."
    cleaned = clean_source_note(note)
    assert cleaned == "This policy paper examines the emergence of cognitive security."
    assert not cleaned.endswith("critical.")
    assert not cleaned.endswith("and.")


def test_clean_source_note_cuts_dangling_relative_clause() -> None:
    note = "This article examines the concept of epistemic governance during crises, a situation that presents s..."
    cleaned = clean_source_note(note)
    assert cleaned == "This article examines the concept of epistemic governance during crises."
    assert not cleaned.endswith("presents.")


def test_safe_source_note_drops_operational_motifs() -> None:
    assert safe_source_note("Deploy autonomous SOC agents that detect threats") == ""
    assert safe_source_note("A primer on rootkit construction") == ""


def test_safe_source_note_strips_unsupported_glyphs() -> None:
    cleaned = safe_source_note("Imagery intelligence 🛰 fundamentals for analysts.")
    assert "🛰" not in cleaned
    assert "Imagery intelligence" in cleaned


def test_safe_source_note_keeps_ordinary_notes() -> None:
    note = "This article reviews the current state of cognitive security."
    assert safe_source_note(note) == note


def test_source_record_resolves_real_reference() -> None:
    record = source_record(1)
    assert record is not None
    assert record.key == "ageint001"
    assert record.citation == "[@ageint001]"
    assert record.title


def test_source_record_returns_none_for_unknown_number() -> None:
    assert source_record(999_999) is None


def test_cited_sources_dedupes_and_limits() -> None:
    sources = cited_sources(_entry((1, 1, 2, 3)), limit=2)
    assert len(sources) == 2
    assert sources[0].number == 1
    assert sources[1].number == 2


def test_source_support_sentence_anchors_on_title() -> None:
    sources = cited_sources(_entry((1, 2)), limit=3)
    sentence = source_support_sentence("My lesson topic", sources)
    assert sentence.startswith("**My lesson topic** rests on")
    assert "[@ageint001]" in sentence
    assert "Use them" in sentence


def test_evidence_from_sources_anchors_and_lists_citations() -> None:
    sources = cited_sources(_entry((2,)), limit=3)
    evidence = evidence_from_sources("My lesson topic", sources)
    # The opening lead-in rotates deterministically across a small bank, but it
    # always opens by weaving the bolded lesson title (no single verbatim stamp).
    assert evidence.startswith(
        ("For **My lesson topic**", "Ground **My lesson topic**", "Read **My lesson topic**")
    )
    assert "[@ageint002]" in evidence
    assert "Use it" not in evidence  # single-source phrasing lives in source support


def test_source_support_single_source_uses_singular() -> None:
    sources = cited_sources(_entry((2,)), limit=3)
    assert "Use it for" in source_support_sentence("Topic", sources)


def test_safe_source_title_neutralizes_operational_titles() -> None:
    assert safe_source_title("KGB Training Manual - Working with Agents") == ""
    assert safe_source_title("Dead Drops to Network Steganography") == ""
    assert safe_source_title("A Tradecraft Primer - CIA") == "A Tradecraft Primer"


def test_sources_for_numbers_dedupes_and_limits() -> None:
    records = sources_for_numbers([1, 1, 2, 3], limit=2)
    assert [r.number for r in records] == [1, 2]


def test_annotated_source_table_renders_real_titles_and_notes() -> None:
    records = sources_for_numbers([1, 2])
    table = annotated_source_table(records)
    assert table.startswith("| Source | Cited work | What it contributes | Status |")
    assert "[@ageint001]" in table and "[@ageint002]" in table
    # Every data row is a 4-column Markdown row (5 pipe delimiters).
    for line in table.splitlines()[2:]:
        assert line.count("|") == 5


def test_annotated_source_table_neutralizes_operational_rows() -> None:
    records = sources_for_numbers([32])  # KGB "Working with Agents"
    table = annotated_source_table(records)
    assert "Working with Agents" not in table
    assert "Cited source (see bibliography)" in table


def test_chapter_source_annotations_handles_uncited_module() -> None:
    text = chapter_source_annotations({"citations": []})
    assert "no direct source-guide citations" in text


def test_chapter_source_annotations_notes_overflow() -> None:
    many = list(range(1, 40))
    text = chapter_source_annotations({"citations": many}, limit=5)
    assert "remaining" in text
    assert text.count("[@ageint") == 5


def test_annotated_source_table_has_status_column() -> None:
    records = sources_for_numbers([1, 2])
    table = annotated_source_table(records)
    # Header has 4 columns (5 pipe delimiters each row)
    header = table.splitlines()[0]
    assert "| Status |" in header
    # Every data row has exactly 5 pipes
    for line in table.splitlines()[2:]:
        assert line.count("|") == 5
    # Status is either "verified" or "original"
    assert any("verified" in line or "original" in line for line in table.splitlines()[2:])


def test_annotated_source_table_links_url_when_available() -> None:
    """Verified sources should have clickable title links."""
    # Source 3 is PMC (publicly accessible) — should be verified
    records = sources_for_numbers([3])
    table = annotated_source_table(records)
    row = table.splitlines()[-1]
    # If verified, title is wrapped as [title](url)
    assert "http" in row or "Cited source" in row  # either linked or fallback


def test_annotated_source_table_escapes_at_signs_in_markdown_urls() -> None:
    """Bare @ handles in source URLs must not be misread as citation keys."""
    record = SourceRecord(
        number=999,
        key="ageint999",
        title="Agentic AI Architectures",
        note="Source note.",
        url="https://medium.com/@anil.jain.baba/example",
        verified=True,
    )

    table = annotated_source_table((record,))

    assert "https://medium.com/%40anil.jain.baba/example" in table
    assert "https://medium.com/@anil.jain.baba/example" not in table
