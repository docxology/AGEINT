"""Topic spine integrity checks for curriculum section parsing."""

from __future__ import annotations

import re

from curriculum import load_curriculum
from intelligence_content._09_part import _safe_topic_entries

PROJECT_ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"

CASE_REVIEW_RE = re.compile(r"case\s+[\d.]+\s+review", re.IGNORECASE)


def test_every_chapter_has_at_least_one_topic_entry() -> None:
    curriculum = load_curriculum(DATA)
    for part in curriculum.parts:
        for chapter in part["chapters"]:
            entries = _safe_topic_entries(chapter, part)
            assert entries, chapter["title"]


def test_chapter_lesson_titles_are_unique() -> None:
    curriculum = load_curriculum(DATA)
    for part in curriculum.parts:
        for chapter in part["chapters"]:
            entries = _safe_topic_entries(chapter, part)
            titles = [entry.display_title for entry in entries]
            assert len(titles) == len(set(titles)), f"{chapter['title']}: {titles}"


def test_display_titles_avoid_case_review_stubs() -> None:
    curriculum = load_curriculum(DATA)
    violations: list[str] = []
    for part in curriculum.parts:
        for chapter in part["chapters"]:
            for entry in _safe_topic_entries(chapter, part):
                if CASE_REVIEW_RE.search(entry.display_title):
                    violations.append(f"{chapter['title']}: {entry.display_title}")
    assert violations == []
