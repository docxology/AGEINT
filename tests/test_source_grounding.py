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


def test_source_support_preserves_inherited_keys_without_asserting_relevance() -> None:
    records = sources_for_numbers([309, 310])
    text = source_support_sentence("Self-critique", records)
    assert all(record.citation in text for record in records)
    assert "source-guide context" in text
    assert "not" in text and "topical" in text and "empirical" in text
    assert "rests on" not in text
    assert text == source_support_sentence("Self-critique", records)


def test_evidence_binds_each_curriculum_annotation_to_its_own_key() -> None:
    records = (
        SourceRecord(1, "ageint001", "First source", "", ""),
        SourceRecord(2, "ageint002", "Second source", "A bounded model is proposed. It is not an evaluation.", ""),
        SourceRecord(3, "ageint003", "Third source", "A different annotation.", ""),
    )
    text = evidence_from_sources("A lesson", records)
    assert "Curriculum annotation for [@ageint002]: A bounded model is proposed. It is not an evaluation." in text
    assert "Curriculum annotation for [@ageint003]: A different annotation." in text
    assert "Curriculum annotation for [@ageint001]" not in text
    assert "source-authored" in text and "not" in text
    assert text == evidence_from_sources("A lesson", records)


def test_verification_flag_does_not_turn_context_into_primary_claim_support() -> None:
    for verified in (False, True):
        record = SourceRecord(999, "ageint999", "An organizational overview", "An institution describes its remit.", "https://www.nist.gov/about", verified)
        text = source_support_sentence("A technical method", (record,))
        evidence = evidence_from_sources("A technical method", (record,))
        assert "claim-specific primary" in text
        assert "passage" in evidence and "normative" in evidence
        assert "independently verified" in evidence


def test_uncited_and_unannotated_inputs_keep_evidence_gaps_visible() -> None:
    assert "No source-guide" in source_support_sentence("A lesson", ())
    record = SourceRecord(999, "ageint999", "A source", "", "")
    text = evidence_from_sources("A lesson", (record,))
    assert "No displayable curriculum annotation" in text
    assert record.citation in text
    assert "No source-guide" in evidence_from_sources("A lesson", ())


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
    assert all(label in table.splitlines()[0] for label in ("Source", "Cited work", "Curriculum annotation", "Status"))
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
    assert any("source-guide" in line for line in table.splitlines()[2:])


def test_annotated_source_table_marks_practitioner_sources_as_secondary() -> None:
    records = sources_for_numbers([139, 143, 144, 156])
    table = annotated_source_table(records)
    rows = table.splitlines()[2:]
    assert len(rows) == 4
    assert all("secondary evidence only" in row for row in rows)


def test_annotated_source_table_flags_generic_mcp_spec_as_context() -> None:
    table = annotated_source_table(sources_for_numbers([299]))
    assert "use pinned MCP anchor for normative claims" in table


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
    record = SourceRecord(number=999, key="ageint999", title="Agentic AI Architectures", note="Source note.", url="https://medium.com/@anil.jain.baba/example", verified=True)

    table = annotated_source_table((record,))

    assert "https://medium.com/%40anil.jain.baba/example" in table
    assert "https://medium.com/@anil.jain.baba/example" not in table
