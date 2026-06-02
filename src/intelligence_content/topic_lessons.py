"""Unified resolver for generated topic-lesson field prose."""

from __future__ import annotations

from dataclasses import dataclass
from typing import TYPE_CHECKING

from _data_loaders import transfer_task_keyword_routes
from unit_education import UnitEducationProfile
from ._12_concept_routes import _match_keywords
from .topic_frame_api import (
    artifact_prompt_for_entry,
    concept_frame_for_entry,
    evidence_prompt_for_entry,
    misconception_for_entry,
    why_it_matters_for_entry,
)
from .topic_lesson_voice import (
    evidence_packet_sentence,
    for_topic,
    reader_facing_concept,
    student_artifact_sentence,
)
from .topic_rotation import template_index

if TYPE_CHECKING:
    from ._01_part import CoursebookProfile, PracticeLens, TopicEntry
    from ._04b_part import IntelligenceProfile


@dataclass(frozen=True)
class TopicLessonFields:
    """Resolved reader-facing strings for one topic lesson."""

    concept: str
    why_it_matters: str
    evidence_prompt: str
    artifact_prompt: str
    misconception: str
    transfer_task: str


def transfer_task_for_entry(
    entry: TopicEntry,
    coursebook: CoursebookProfile,
    *,
    lesson_index: int = 1,
    chapter_title: str = "",
) -> str:
    raw = entry.raw_title.lower()
    for keywords, template in transfer_task_keyword_routes():
        if _match_keywords(raw, keywords):
            return template
    if entry.risk_category not in {"standard", "ageint_pattern_registry"}:
        templates = (
            (
                f"Transfer **{entry.display_title}** from this module to a "
                f"second motif by preserving {coursebook.practice_focus}, replacing "
                "action with audit, and naming the blocked use."
            ),
            (
                f"Apply this module's safe boundary for **{entry.display_title}** "
                f"to another artifact while keeping {coursebook.practice_focus} and "
                "reviewer ownership explicit."
            ),
            (
                f"Reuse the **{entry.display_title}** audit pattern from this module "
                "on a different sample record set with a new reviewer and blocked-use note."
            ),
        )
        slot = template_index(
            entry.display_title,
            chapter_title,
            str(lesson_index),
            entry.risk_category,
            count=len(templates),
        )
        return templates[slot]
    return (
        f"Transfer **{entry.display_title}** to a second module by preserving "
        f"{coursebook.practice_focus}, changing the source evidence, and naming a new reviewer."
    )


def resolve_topic_lesson_fields(
    entry: TopicEntry,
    *,
    coursebook: CoursebookProfile,
    profile: IntelligenceProfile,
    lens: PracticeLens,
    lesson_index: int,
    chapter_title: str,
    unit_profile: UnitEducationProfile | None = None,
) -> TopicLessonFields:
    """Resolve all topic-lesson fields in canonical routing order."""
    concept = reader_facing_concept(
        entry,
        concept_frame_for_entry(entry, coursebook, profile),
    )
    why_it_matters = why_it_matters_for_entry(
        entry,
        profile,
        coursebook,
        lesson_index=lesson_index,
        chapter_title=chapter_title,
    )
    evidence_prompt = evidence_packet_sentence(
        entry,
        evidence_prompt_for_entry(entry, lens, coursebook),
        unit_profile=unit_profile,
    )
    artifact_prompt = student_artifact_sentence(
        entry,
        artifact_prompt_for_entry(entry, lens, coursebook),
        unit_profile=unit_profile,
    )
    misconception = misconception_for_entry(
        entry,
        coursebook,
        lesson_index=lesson_index,
        chapter_title=chapter_title,
    )
    transfer_task = for_topic(
        entry,
        transfer_task_for_entry(
            entry,
            coursebook,
            lesson_index=lesson_index,
            chapter_title=chapter_title,
        ),
    )
    return TopicLessonFields(
        concept=concept,
        why_it_matters=why_it_matters,
        evidence_prompt=evidence_prompt,
        artifact_prompt=artifact_prompt,
        misconception=misconception,
        transfer_task=transfer_task,
    )


def resolve_topic_misconception(
    entry: TopicEntry,
    *,
    coursebook: CoursebookProfile,
    profile: IntelligenceProfile,
    lens: PracticeLens,
    lesson_index: int,
    chapter_title: str,
    unit_profile: UnitEducationProfile | None = None,
) -> str:
    """Return the misconception string aligned with topic-lesson routing."""
    del profile, lens, unit_profile
    return misconception_for_entry(
        entry,
        coursebook,
        lesson_index=lesson_index,
        chapter_title=chapter_title,
    )


__all__ = [
    "TopicLessonFields",
    "resolve_topic_lesson_fields",
    "resolve_topic_misconception",
    "template_index",
    "transfer_task_for_entry",
]
