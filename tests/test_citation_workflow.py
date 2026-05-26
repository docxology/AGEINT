"""Tests for composable citation workflow helpers."""

from __future__ import annotations

from pathlib import Path

from citation_workflow import (
    generated_markdown_citation_inventory,
    render_citation_workflow_markdown,
    source_citation_cell,
    source_citation_coverage_summary,
    source_citation_spine,
    source_key,
    source_section_citation_inventory,
)
from curriculum import load_curriculum
from manuscript_quality.inventory_helpers import manuscript_dir

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"


def test_source_keys_and_citation_spines_are_stable() -> None:
    assert source_key(1) == "ageint001"
    assert source_key(312) == "ageint312"
    assert source_citation_spine([137, 137, 155], limit=2) == "[@ageint137]; [@ageint155]."
    assert source_citation_cell([137, 137, 155]) == "[@ageint137]; [@ageint155]"
    assert source_citation_cell([]) == "-"
    assert source_citation_spine([], fallback="No source.") == "No source."


def test_source_section_inventory_paths_match_curriculum_shards() -> None:
    curriculum = load_curriculum(DATA)
    rows = source_section_citation_inventory(curriculum)
    unique_paths = {row.path for row in rows}

    assert unique_paths
    for relative_path in unique_paths:
        assert (PROJECT_ROOT / relative_path).is_file(), relative_path


def test_source_section_inventory_matches_current_curriculum() -> None:
    curriculum = load_curriculum(DATA)
    rows = source_section_citation_inventory(curriculum)
    summary = source_citation_coverage_summary(curriculum)

    assert len(rows) == 723
    assert summary.section_count == 723
    assert summary.citation_occurrences == 1484
    assert summary.zero_citation_sections == 0
    assert summary.unique_citation_keys == 301
    assert dict(summary.citation_count_distribution) == {1: 273, 2: 142, 3: 305, 4: 3}


def test_rendered_workflow_markdown_names_authoring_surfaces() -> None:
    curriculum = load_curriculum(DATA)
    rendered = render_citation_workflow_markdown(curriculum)

    assert "`data/curriculum/`" in rendered
    assert "`data/research_anchors/`" in rendered
    assert "`src/intelligence_content/`" in rendered
    assert "never hand-edit `output/manuscript/`" in rendered
    assert "| Source sections | 723 |" in rendered


def test_generated_markdown_inventory_reports_topic_lesson_citations(built_output: Path) -> None:
    rows = generated_markdown_citation_inventory(manuscript_dir(built_output))
    topic_rows = [row for row in rows if row.family == "topic-lessons"]

    assert topic_rows
    assert sum(row.citation_count for row in topic_rows) > 0
