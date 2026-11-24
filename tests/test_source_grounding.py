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
    safe_source_note,
    safe_source_title,
    source_record,
    sources_for_numbers,
)


def _entry(citation_numbers: tuple[int, ...], title: str = "Sample topic") -> TopicEntry:
    return TopicEntry(raw_title=title, display_title=title, source_locus="1.1", provenance_note="", risk_category="standard", citation_numbers=citation_numbers)


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
    assert clean_source_title("[PDF] [PDF] The Psychology of Intelligence Analysis") == ("The Psychology of Intelligence Analysis")


def test_clean_source_title_trims_trailing_function_word_without_ellipsis() -> None:
    # A hard truncation with no ellipsis marker leaves a dangling function word.
    assert clean_source_title("The Utility of Military Deception and Information Operations in") == ("The Utility of Military Deception and Information Operations")
    assert clean_source_title("Behavioral Outcomes of Human Cognitive Security within an") == ("Behavioral Outcomes of Human Cognitive Security")


def test_clean_source_note_keeps_complete_sentences() -> None:
    note = "First complete sentence here. A dangling second frag..."
    cleaned = clean_source_note(note)
    assert cleaned == "First complete sentence here."


def test_clean_source_note_handles_empty() -> None:
    assert clean_source_note("") == ""
    assert clean_source_note("   ...") == ""


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


def test_safe_source_note_preserves_bounded_fictional_evidence_not_import_scaffolds() -> None:
    note = "The study tested 🛰 fictional headlines. Recognition is not observed sharing."
    assert safe_source_note(note) == "The study tested fictional headlines. Recognition is not observed sharing."
    assert safe_source_note("Inspect fictional records before the source guide import.") == ""


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


def test_truncated_notes_do_not_manufacture_complete_claims() -> None:
    assert clean_source_note("This study demonstrates a reliable method for...") == ""
    assert clean_source_note("A complete scoped statement. A truncated continuation...") == "A complete scoped statement."
    assert clean_source_note("Studies in Intelligence, Vol. 70, No. 1 introduces...") == ""
    assert clean_source_note("An institution in the U.S. reports...") == ""


def test_overlong_annotation_does_not_become_a_fabricated_sentence() -> None:
    assert safe_source_note("A purported conclusion " + "with qualifications " * 40 + "under a narrow model.") == ""


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
    assert "[@ageint001]" in table and "[@ageint002]" in table
    # Every data row is a 4-column Markdown row (5 pipe delimiters).
    for line in table.splitlines()[2:]:
        assert line.count("|") == 5


def test_annotated_source_table_neutralizes_operational_rows() -> None:
    records = sources_for_numbers([32])  # KGB "Working with Agents"
    table = annotated_source_table(records)
    assert "Working with Agents" not in table


def test_chapter_source_annotations_notes_overflow() -> None:
    many = list(range(1, 40))
    text = chapter_source_annotations({"citations": many}, limit=5)
    assert text.count("[@ageint") == 5


def test_annotated_source_table_escapes_at_signs_in_markdown_urls() -> None:
    """Bare @ handles in source URLs must not be misread as citation keys."""
    record = SourceRecord(number=999, key="ageint999", title="Agentic AI Architectures", note="Source note.", url="https://medium.com/@anil.jain.baba/example", verified=True)

    table = annotated_source_table((record,))

    assert "https://medium.com/%40anil.jain.baba/example" in table
    assert "https://medium.com/@anil.jain.baba/example" not in table
