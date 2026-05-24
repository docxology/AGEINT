"""Tests for AGEINT manuscript manifest construction and semantic output paths."""

from __future__ import annotations

from pathlib import Path

import pytest

from curriculum import load_curriculum
from manuscript_manifest import build_manuscript_manifest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"


def test_manifest_builds_ordered_semantic_sections_without_numbered_paths() -> None:
    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)

    assert manifest.sections[0].relative_path == "abstract.md"
    assert manifest.sections[1].relative_path == "orientation.md"
    assert len(manifest.chapter_sections) == 51
    assert len(manifest.part_sections) == 16
    assert len(manifest.appendix_sections) == 9
    assert "appendices:" in manifest.config_yaml()

    foundations = manifest.section_for_chapter(31)
    assert foundations.title == "Foundations of AGEINT"
    assert foundations.relative_path == "parts/ageint-agentic-intelligence/foundations-of-ageint.md"
    assert not Path(foundations.relative_path).name[:2].isdigit()

    appendix_a = manifest.section_for_appendix("a")
    assert appendix_a.appendix_letter == "A"
    assert appendix_a.kind == "appendix"


def test_manifest_lookup_errors_are_explicit() -> None:
    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)

    with pytest.raises(KeyError, match="No chapter section 999"):
        manifest.section_for_chapter(999)

    with pytest.raises(KeyError, match="No appendix section Z"):
        manifest.section_for_appendix("Z")


def test_manifest_uses_deterministic_slug_suffixes_for_collisions() -> None:
    curriculum = load_curriculum(DATA)
    manifest = build_manuscript_manifest(curriculum)
    paths = [section.relative_path for section in manifest.sections]

    assert len(paths) == len(set(paths))
    assert all(" " not in path for path in paths)
    assert all(not Path(path).name.startswith("43_") for path in paths)
