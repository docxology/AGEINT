"""Profile-synthesized topic lesson frames and lesson field helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._12_concept_routes import CONCEPT_KEYWORD_ROUTES, _first_matching_frame, _match_keywords

if TYPE_CHECKING:
    from ._01_part import CoursebookProfile, PracticeLens, TopicEntry
    from ._04b_part import IntelligenceProfile


from ._07_safe_titles import _topic_anchor_words, is_generic_display_title

from _data_loaders import category_concept_frames

CATEGORY_CONCEPT_FRAMES: dict[str, str] = category_concept_frames()


def _analytic_subcategory(raw_lower: str) -> str | None:
    if _match_keywords(
        raw_lower,
        (
            "competing hypotheses",
            "ach",
            "key assumptions",
            "devil's advocacy",
            "devils advocacy",
            "red team analysis",
            "structured analytic",
        ),
    ):
        return "analytic_tradecraft_sats"
    if _match_keywords(
        raw_lower,
        ("icd 203", "nine tradecraft", "analytic tradecraft standard", "analytic confidence"),
    ):
        return "analytic_tradecraft_standards"
    if _match_keywords(raw_lower, ("bias", "heuristic", "cognitive trap", "mirror imaging")):
        return "analytic_tradecraft_bias"
    return None


def _cognitive_subcategory(raw_lower: str) -> str | None:
    if _match_keywords(raw_lower, ("epistemic", "knowledge integrity", "malign influence")):
        return "cognitive_resilience_epistemic"
    if _match_keywords(raw_lower, ("prebunking", "inoculation", "debunking")):
        return "cognitive_resilience_inoculation"
    if _match_keywords(
        raw_lower,
        ("neuro", "resaid", "neurips", "brain", "cognitive mechanism"),
    ):
        return "cognitive_resilience_neuro"
    return None


def _category_frame_key(entry: TopicEntry) -> str:
    raw = f"{entry.display_title} {entry.raw_title}".lower()
    if entry.risk_category == "analytic_tradecraft":
        sub = _analytic_subcategory(raw)
        if sub:
            return sub
    if entry.risk_category == "cognitive_resilience":
        sub = _cognitive_subcategory(raw)
        if sub:
            return sub
    if entry.risk_category == "ageint_pattern_registry":
        if _match_keywords(raw, ("pattern", "archetype", "registry")):
            return "ageint_pattern_registry"
    return entry.risk_category


def synthesized_concept_frame(
    entry: TopicEntry,
    coursebook: CoursebookProfile,
    profile: IntelligenceProfile,
) -> str:
    """Profile-backed concept prose when no keyword or category route matches."""
    anchor_source = (
        entry.raw_title
        if is_generic_display_title(entry.display_title)
        else entry.display_title
    )
    anchor = _topic_anchor_words(anchor_source, limit=3)
    return (
        f"**{entry.display_title}** applies {anchor} within {profile.title}: "
        f"learners use {coursebook.key_distinction} and {coursebook.practice_focus} "
        "evidence before any judgment moves forward."
    )


def concept_frame_for_entry(
    entry: TopicEntry,
    coursebook: CoursebookProfile,
    profile: IntelligenceProfile,
) -> str:
    raw = f"{entry.display_title} {entry.raw_title}".lower()
    frame = _first_matching_frame(raw, CONCEPT_KEYWORD_ROUTES)
    if frame:
        return frame
    category_key = _category_frame_key(entry)
    category_frame = CATEGORY_CONCEPT_FRAMES.get(category_key)
    if category_frame:
        return category_frame
    return synthesized_concept_frame(entry, coursebook, profile)


def synthesized_evidence_prompt(entry: TopicEntry, lens: PracticeLens, coursebook: CoursebookProfile) -> str:
    anchor = _topic_anchor_words(entry.display_title, limit=2)
    focus = coursebook.practice_focus.removesuffix(" review")
    return (
        f"The evidence packet for **{entry.display_title}** uses source descriptors, "
        f"{focus} records, provenance gaps, and a documented judgment-change condition for {anchor}."
    )


# Deferred import: breaks cycle with topic_prompt_routes importing _12_concept_routes.
from .topic_prompt_routes import (
    artifact_prompt_for_entry as _artifact_prompt_from_routes,
    evidence_prompt_for_entry as _evidence_prompt_from_routes,
)


def evidence_prompt_for_entry(
    entry: TopicEntry,
    lens: PracticeLens,
    coursebook: CoursebookProfile,
) -> str:
    return _evidence_prompt_from_routes(
        entry,
        lens,
        coursebook,
        synthesized_evidence_prompt=synthesized_evidence_prompt,
    )


def artifact_prompt_for_entry(entry: TopicEntry, lens: PracticeLens, coursebook: CoursebookProfile) -> str:
    return _artifact_prompt_from_routes(entry, lens, coursebook)


def lesson_intro_paragraph(
    chapter_title: str,
    coursebook: CoursebookProfile,
    lens: PracticeLens,
    topic_titles: tuple[str, ...],
) -> str:
    opener = topic_titles[0] if topic_titles else chapter_title
    topic_path = ", ".join(f"**{title}**" for title in topic_titles[:3]) if topic_titles else f"**{opener}**"
    return (
        f"**{chapter_title}** builds {coursebook.disciplinary_frame}. "
        f"The sequence opens with {topic_path} and applies the **{lens.title}** "
        "practice frame through concept, evidence, artifact, misconception, and transfer tasks."
    )
