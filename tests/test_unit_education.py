"""Tests for unit-specific educational content profiles."""

from __future__ import annotations

from pathlib import Path

from _slug import slug_for_path
from curriculum import load_curriculum
from manuscript_quality.inventory_helpers import manuscript_dir
from unit_education import unit_profile_for_part, unit_profile_for_number, unit_specific_terms

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"


def test_all_curriculum_units_have_education_profiles() -> None:
    curriculum = load_curriculum(DATA)

    assert len(curriculum.parts) == 16
    for part in curriculum.parts:
        profile = unit_profile_for_part(part)
        assert profile.number == part["number"]
        assert profile.concept
        assert profile.practice_artifact
        assert profile.evidence_artifacts
        assert profile.anchor_numbers


def test_unit_profiles_render_in_unit_introductions(built_output: Path) -> None:
    curriculum = load_curriculum(DATA)
    root = manuscript_dir(built_output)

    for part in curriculum.parts:
        profile = unit_profile_for_part(part)
        intro = root / "parts" / slug_for_path(part["title"]) / "unit_intro.md"
        text = intro.read_text(encoding="utf-8")
        assert "### Discipline spine" in text
        assert "### Source-use contract" in text
        assert profile.concept in text
        assert profile.practice_artifact in text
        assert profile.safety_boundary in text


def test_topic_lessons_include_unit_specific_terms(built_output: Path) -> None:
    curriculum = load_curriculum(DATA)
    root = manuscript_dir(built_output)

    for part in curriculum.parts:
        profile = unit_profile_for_number(part["number"])
        terms = unit_specific_terms(profile)
        assert terms
        for chapter in part["chapters"]:
            lesson_path = (
                root
                / "parts"
                / slug_for_path(part["title"])
                / slug_for_path(chapter["title"])
                / "01-practice-studio.md"
            )
            paths = sorted(lesson_path.parent.glob("01-practice-studio*.md"))
            assert paths, lesson_path.parent
            text = "\n".join(path.read_text(encoding="utf-8") for path in paths).lower()
            assert any(term in text for term in terms), lesson_path.parent
