"""Tests for composable citation workflow helpers."""

from __future__ import annotations

from pathlib import Path

from citation_workflow import (
    source_citation_cell,
    source_citation_spine,
    source_citation_spine_inline,
    source_key,
    source_section_citation_inventory,
)
from curriculum import load_curriculum

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"


def test_source_keys_and_citation_spines_are_stable() -> None:
    assert source_key(1) == "ageint001"
    assert source_key(312) == "ageint312"
    assert source_citation_spine([137, 137, 155], limit=2) == "[@ageint137]; [@ageint155]."
    assert source_citation_spine_inline([137, 137, 155], limit=2) == "[@ageint137]; [@ageint155]"
    assert source_citation_cell([137, 137, 155]) == "[@ageint137]; [@ageint155]"
    assert source_citation_cell([]) == "-"
    assert source_citation_spine([], fallback="No source.") == "No source."
    assert source_citation_spine_inline([], fallback="No source") == "No source"


def test_source_section_inventory_paths_match_curriculum_shards() -> None:
    curriculum = load_curriculum(DATA)
    rows = source_section_citation_inventory(curriculum)
    unique_paths = {row.path for row in rows}

    assert unique_paths
    for relative_path in unique_paths:
        assert (PROJECT_ROOT / relative_path).is_file(), relative_path

