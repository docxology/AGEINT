"""Round-trip checks for sharded AGEINT data and split bibliography files."""

from __future__ import annotations

from pathlib import Path
import json
import re

import pytest

from curriculum import load_curriculum
import curriculum as curriculum_module
from intelligence_content import INTELLIGENCE_RESEARCH_ANCHORS
from manuscript_variables import reference_bibtex_files
from source_identity import (
    build_source_identity_lock,
    load_source_identity_lock,
    source_identity_mismatches,
    write_source_identity_lock_shards,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
CURRICULUM = PROJECT_ROOT / "data" / "curriculum"
SOURCE = PROJECT_ROOT / "SIST-Guide-TOC-and-Bibliography-v2.md"
SOURCE_IDENTITY = PROJECT_ROOT / "data" / "source_identity"
RESEARCH_ANCHORS = PROJECT_ROOT / "data" / "research_anchors"
BIB_ENTRY_RE = re.compile(r"^@\w+\{(?P<label>[^,]+),", re.MULTILINE)


def _jsonl_rows(directory: Path) -> list[dict[str, object]]:
    return [
        json.loads(line)
        for path in sorted(directory.glob("*.jsonl"))
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_sharded_curriculum_composes_expected_runtime_payload() -> None:
    curriculum = load_curriculum(CURRICULUM)

    assert curriculum.stats["chapters"] == 51
    assert curriculum.stats["references"] >= 296
    assert curriculum.stats["references"] == len({ref["key"] for ref in curriculum.references})
    assert curriculum.chapter(32)["title"] == "AGEINT Design Patterns and Archetypes"
    assert len(curriculum.chapter(32)["sections"]) >= 80
    assert curriculum.reference("ageint296")["title"].startswith("Artificial Intelligence Risk Management")


def test_keyword_source_support_replaces_only_part_default_citations() -> None:
    curriculum = load_curriculum(CURRICULUM)
    chapter = curriculum.chapter(36)
    citations_by_section = {section["number"]: section["citations"] for section in chapter["sections"]}

    assert citations_by_section["36.1"] == [309, 310, 300]
    assert citations_by_section["36.3"] == [300, 304, 306]
    assert citations_by_section["36.6"] == [308, 311]
    assert citations_by_section["36.7"] == [303, 304, 305]
    assert citations_by_section["36.8"] == [307, 305, 304]
    assert citations_by_section["36.99"] == [242, 243, 246]


def test_source_identity_shards_preserve_locked_reference_keys() -> None:
    lock = load_source_identity_lock(SOURCE_IDENTITY)
    rebuilt = build_source_identity_lock(SOURCE, max_reference=231)

    assert lock["locked_reference_count"] == 231
    assert [row["key"] for row in lock["references"]] == [row["key"] for row in rebuilt["references"]]
    assert lock["references"][0]["key"] == "ageint001"
    assert lock["references"][-1]["key"] == "ageint231"


def test_research_anchor_shards_match_runtime_anchor_keys() -> None:
    rows = _jsonl_rows(RESEARCH_ANCHORS)
    runtime_keys = {anchor.key for anchor in INTELLIGENCE_RESEARCH_ANCHORS}
    shard_keys = {str(row["key"]) for row in rows if str(row.get("citation_role")) == "curriculum_anchor"}

    assert runtime_keys == shard_keys
    assert len(shard_keys) >= 172


def test_split_bibtex_files_cover_runtime_citation_keys(built_output: Path) -> None:
    curriculum = load_curriculum(CURRICULUM)
    expected_files = reference_bibtex_files(curriculum.references)
    output_manuscript = built_output / "manuscript"
    generated_files = {path.name: path.read_text(encoding="utf-8") for path in output_manuscript.glob("*.bib")}
    generated_keys = {
        match.group("label")
        for text in generated_files.values()
        for match in BIB_ENTRY_RE.finditer(text)
    }

    assert set(expected_files) == set(generated_files)
    assert set(curriculum.citation_keys()) <= generated_keys
    assert "official_oecd_agentic_ai" in generated_keys


def test_curriculum_compatibility_loaders_cover_legacy_and_error_paths(tmp_path: Path) -> None:
    guide = tmp_path / "guide.md"
    guide.write_text(
        "\n".join(
            [
                "### PART I: FOUNDATIONS",
                "**Chapter 1 — Test Chapter**",
                "- 1.1 First topic[^1]",
                "- 1.2 First topic repeated[^1]",
                "## CODE SNIPPETS",
                "### Appendix A — Test Appendix",
                "- Review item[^1]",
                "## COMPREHENSIVE STOP",
                "## References",
                "1. [Reference One](https://example.com/one) - note",
            ]
        ),
        encoding="utf-8",
    )
    output_dir = tmp_path / "data" / "curriculum"
    built = curriculum_module.build_curriculum(guide, output_dir)
    assert built.part_titles() == ["FOUNDATIONS"]
    assert built.reference("001")["key"] == "ageint001"
    assert built.reference(1)["key"] == "ageint001"
    with pytest.raises(KeyError):
        built.reference("missing")

    legacy_path = tmp_path / "data" / "curriculum_outline.json"
    assert load_curriculum(legacy_path).stats["chapters"] == 1
    legacy_file = tmp_path / "legacy.json"
    legacy_file.write_text(json.dumps(built.payload), encoding="utf-8")
    assert load_curriculum(legacy_file).stats == built.stats
    with pytest.raises(FileNotFoundError):
        load_curriculum(tmp_path / "missing.json")
    with pytest.raises(FileNotFoundError):
        curriculum_module.build_curriculum(tmp_path / "empty" / "missing-guide.md", tmp_path / "missing-output")


def test_legacy_chapter_file_shard_and_missing_shard_errors(tmp_path: Path) -> None:
    shard = tmp_path / "curriculum"
    (shard / "parts" / "01-test" / "chapters").mkdir(parents=True)
    (shard / "appendices").mkdir()
    (shard / "references").mkdir()
    (shard / "metadata.json").write_text('{"project":"AGEINT","title":"Fixture"}', encoding="utf-8")
    (shard / "stats.json").write_text(
        '{"parts":1,"chapters":1,"appendices":0,"patterns":0,"references":0}',
        encoding="utf-8",
    )
    (shard / "patterns.json").write_text("[]", encoding="utf-8")
    (shard / "parts" / "01-test" / "part.json").write_text(
        '{"number":1,"roman":"I","title":"TEST","source_line":1}',
        encoding="utf-8",
    )
    (shard / "parts" / "01-test" / "chapters" / "01-test.json").write_text(
        '{"number":1,"title":"Legacy","sections":[],"citations":[],"source_line":2}',
        encoding="utf-8",
    )

    assert load_curriculum(shard).chapter(1)["title"] == "Legacy"
    with pytest.raises(FileNotFoundError):
        load_curriculum(tmp_path / "empty")


def test_source_identity_compatibility_and_missing_reference_paths(tmp_path: Path) -> None:
    curriculum_json = tmp_path / "curriculum.json"
    payload = load_curriculum(CURRICULUM).payload
    curriculum_json.write_text(json.dumps(payload), encoding="utf-8")
    lock = build_source_identity_lock(curriculum_json, max_reference=2)
    lock_json = tmp_path / "source_identity_lock.json"
    lock_json.write_text(json.dumps(lock), encoding="utf-8")

    shard_dir = write_source_identity_lock_shards(lock, tmp_path / "source_identity")
    assert load_source_identity_lock(lock_json)["locked_reference_count"] == 2
    assert load_source_identity_lock(shard_dir)["references"][1]["key"] == "ageint002"
    lock_json.unlink()
    assert load_source_identity_lock(lock_json)["references"][0]["key"] == "ageint001"

    mutated = json.loads(curriculum_json.read_text(encoding="utf-8"))
    mutated["references"] = mutated["references"][1:]
    curriculum_json.write_text(json.dumps(mutated), encoding="utf-8")
    mismatches = source_identity_mismatches(curriculum_json, shard_dir)
    assert any("missing ageint001" in mismatch for mismatch in mismatches)
    with pytest.raises(FileNotFoundError):
        load_source_identity_lock(tmp_path / "no-lock.json")
