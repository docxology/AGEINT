"""Tests for AGEINT guide parsing and curriculum accessors."""

from __future__ import annotations

from pathlib import Path

from _curriculum_shards import source_support_numbers_for_section
from curriculum import build_curriculum, load_curriculum, parse_curriculum_guide, resolve_curriculum_payload, write_curriculum_shards
from published_counts_gate import recompute_source_counts

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT_ROOT / "SIST-Guide-TOC-and-Bibliography-v2.md"
DATA = PROJECT_ROOT / "data" / "curriculum"
MINIMAL_GUIDE = """
### PART I: FOUNDATIONS OF INTELLIGENCE TRADECRAFT
**Chapter 1 — The Nature of Intelligence**
- 1.1 Defining Intelligence[^1]

## CODE SNIPPETS
### Appendix A — Python OSINT Library
- Source verification helper[^1]

## References
1. [Reference One](https://example.com/ref-one) - fixture
"""


def test_parse_curriculum_guide_counts_source_shape() -> None:
    payload = load_curriculum(DATA).payload
    assert payload["stats"]["parts"] == 16
    assert payload["stats"]["chapters"] == 51
    assert payload["stats"]["appendices"] == 9
    assert payload["stats"]["patterns"] == 20
    assert payload["stats"]["references"] >= 296


def test_guide_build_publishes_independently_recomputed_source_counts(tmp_path: Path) -> None:
    guide = tmp_path / "guide.md"
    guide.write_text(MINIMAL_GUIDE, encoding="utf-8")
    shards = tmp_path / "curriculum"
    curriculum = build_curriculum(guide, shards)

    assert curriculum.stats == {"parts": 1, "chapters": 1, "appendices": 1, "patterns": 0, "references": 1, "authored_teaching_note_count": 0}
    assert curriculum.stats == recompute_source_counts(shards)



def test_authored_teaching_note_count_recomputed_from_nonblank_shards(tmp_path: Path) -> None:
    payload = parse_curriculum_guide(MINIMAL_GUIDE)
    chapter = payload["parts"][0]["chapters"][0]
    chapter["sections"][0]["teaching_note"] = "An authored explanation."
    chapter["sections"].extend(
        {"number": f"1.{number}", "title": f"Section {number}", "citations": [1], **fields}
        for number, fields in enumerate(
            [{"teaching_note": " \n\t"}, {}, {"teaching_note": 17}], start=2
        )
    )
    payload["parts"].append(
        {"number": 2, "roman": "II", "title": "Second part", "chapters": [
            {"number": 2, "title": "Second chapter", "sections": [
                {"number": "2.1", "title": "Another explanation", "citations": [1], "teaching_note": "Another authored note."}
            ]}
        ]}
    )
    payload["stats"]["authored_teaching_note_count"] = 999
    write_curriculum_shards(payload, tmp_path)

    curriculum = load_curriculum(tmp_path)

    assert curriculum.stats["authored_teaching_note_count"] == 2

def test_ageint_part_preserves_chapter_and_pattern_registry_shape() -> None:
    curriculum = load_curriculum(DATA)
    ageint_part = next(part for part in curriculum.parts if part["number"] == 11)
    assert [chapter["number"] for chapter in ageint_part["chapters"]] == [31, 32, 33, 34, 35, 36]
    assert len(curriculum.patterns) == 20


def test_chapter_citation_keys_are_stable() -> None:
    curriculum = load_curriculum(DATA)
    citations = curriculum.citations_for_chapter(33)
    assert "ageint155" in citations
    assert all(key.startswith("ageint") and len(key) == 9 for key in citations)


def test_build_curriculum_round_trips_to_json(tmp_path: Path) -> None:
    output = tmp_path / "curriculum.json"
    curriculum = build_curriculum(SOURCE, output)
    assert output.exists()
    reloaded = load_curriculum(output)
    assert reloaded.stats == curriculum.stats


def test_all_chapter_shards_declare_profile_and_lens() -> None:
    curriculum = load_curriculum(DATA)
    for part in curriculum.parts:
        for chapter in part["chapters"]:
            assert chapter.get("content_profile"), chapter["title"]
            assert chapter.get("practice_lens"), chapter["title"]


def test_resolve_curriculum_payload_uses_sharded_data_when_guide_missing() -> None:
    payload = resolve_curriculum_payload(PROJECT_ROOT / "missing-guide.md")
    assert payload["stats"]["chapters"] == 51


def test_source_routing_requires_topic_terms_not_substrings_or_context_alone() -> None:
    expansion = {"keyword_routes": [{"keywords": ["ot"], "citations": [2]}, {"keywords": ["cti"], "citations": [3]}]}
    part = {"title": "OT and CTI"}
    for title in ("Photographs and publication history", "Historical comparison"):
        selected = source_support_numbers_for_section(expansion, part, {}, {"title": title}, {1, 2, 3}, part_default=[1])
        assert selected == [1]


def test_source_routing_recognizes_whole_terms_and_hyphenated_phrases() -> None:
    expansion = {"keyword_routes": [{"keywords": ["ot"], "citations": [2]}, {"keywords": ["open source"], "citations": [3]}]}
    assert source_support_numbers_for_section(expansion, {}, {}, {"title": "OT architecture"}, {1, 2, 3}, part_default=[1]) == [2]
    assert source_support_numbers_for_section(expansion, {}, {}, {"title": "Open-source records"}, {1, 2, 3}, part_default=[1]) == [3]
