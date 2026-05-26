"""Tests for AGEINT guide parsing and curriculum accessors."""

from __future__ import annotations

from pathlib import Path

from curriculum import build_curriculum, load_curriculum, parse_curriculum_guide, resolve_curriculum_payload

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT_ROOT / "SIST-Guide-TOC-and-Bibliography-v2.md"
DATA = PROJECT_ROOT / "data" / "curriculum"
V2_AGEINT_DEPTH_CHAPTERS = {31, 32, 33, 34, 35, 36}
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


def test_parse_curriculum_guide_handles_minimal_fixture() -> None:
    payload = parse_curriculum_guide(MINIMAL_GUIDE)

    assert payload["stats"]["parts"] == 1
    assert payload["stats"]["chapters"] == 1
    assert payload["stats"]["appendices"] == 1
    assert payload["references"][0]["key"] == "ageint001"


def test_ageint_part_is_dense_and_named() -> None:
    curriculum = load_curriculum(DATA)
    ageint_part = next(part for part in curriculum.parts if part["number"] == 11)
    assert ageint_part["title"] == "AGEINT — AGENTIC INTELLIGENCE"
    assert [chapter["number"] for chapter in ageint_part["chapters"]] == [31, 32, 33, 34, 35, 36]
    assert len(curriculum.patterns) == 20
    assert curriculum.patterns[0]["name"] == "The Solo Reasoner"
    assert curriculum.patterns[-1]["name"] == "The Hierarchical Command"


def test_all_chapters_have_v2_source_lane_bullets() -> None:
    payload = load_curriculum(DATA).payload
    for part in payload["parts"]:
        for chapter in part["chapters"]:
            titles = [section["title"] for section in chapter["sections"]]
            assert any(title.startswith("V2 source-lane extension:") for title in titles), chapter["title"]
            assert any(title.startswith("Deep expansion:") for title in titles), chapter["title"]
            assert any(title.startswith("Evidence-package expansion:") for title in titles), chapter["title"]
            if chapter["number"] in V2_AGEINT_DEPTH_CHAPTERS:
                assert any(title.startswith("V2 AGEINT-depth extension:") for title in titles), chapter["title"]


def test_chapter_citation_keys_are_stable() -> None:
    curriculum = load_curriculum(DATA)
    citations = curriculum.citations_for_chapter(33)
    assert "ageint155" in citations
    assert all(key.startswith("ageint") and len(key) == 9 for key in citations)


def test_curriculum_accessors_expose_stable_surfaces() -> None:
    curriculum = load_curriculum(DATA)

    assert curriculum.part(11)["title"] == "AGEINT — AGENTIC INTELLIGENCE"
    assert curriculum.appendix("A")["title"] == "Python OSINT Library"
    assert curriculum.appendix("H")["title"] == "Source Verification and Claim Ledger Workbook"
    assert curriculum.appendix("I")["title"] == "Instructor Capstone, Rubric, and Red-Team Review Pack"
    assert "Model Context Protocol" in curriculum.reference("ageint155")["title"]
    assert curriculum.reference(140)["url"].startswith("https://www.oecd.org")
    assert curriculum.reference("ageint232")["title"] == "European AI Office"
    assert curriculum.reference("ageint285")["title"] == "NIST AI Resource Center"
    assert curriculum.reference("ageint296")["title"] == (
        "Artificial Intelligence Risk Management Framework: Generative Artificial Intelligence Profile"
    )
    assert "ageint140" in curriculum.citation_keys()


def test_build_curriculum_round_trips_to_json(tmp_path: Path) -> None:
    output = tmp_path / "curriculum.json"
    curriculum = build_curriculum(SOURCE, output)
    assert output.exists()
    reloaded = load_curriculum(output)
    assert reloaded.stats == curriculum.stats
    assert reloaded.chapter(31)["title"] == "Foundations of AGEINT"


def test_all_chapter_shards_declare_profile_and_lens() -> None:
    curriculum = load_curriculum(DATA)
    for part in curriculum.parts:
        for chapter in part["chapters"]:
            assert chapter.get("content_profile"), chapter["title"]
            assert chapter.get("practice_lens"), chapter["title"]


def test_resolve_curriculum_payload_uses_sharded_data_when_guide_missing() -> None:
    payload = resolve_curriculum_payload(PROJECT_ROOT / "missing-guide.md")
    assert payload["stats"]["chapters"] == 51
