"""Three-tier concept frames: safe identity/subject, category, then synthesis.

The raw source title is provenance, never a competing instructional subject.
"""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._12_concept_routes import CONCEPT_KEYWORD_ROUTES, _first_matching_frame, _match_keywords

if TYPE_CHECKING:
    from ._01_part import CoursebookProfile, PracticeLens, TopicEntry, IntelligenceProfile


from _data_loaders import category_concept_frames

CATEGORY_CONCEPT_FRAMES: dict[str, str] = category_concept_frames()


def _analytic_subcategory(raw_lower: str) -> str | None:
    if _match_keywords(raw_lower, ("competing hypotheses", "ach", "key assumptions", "devil's advocacy", "devils advocacy", "red team analysis", "structured analytic")):
        return "analytic_tradecraft_sats"
    if _match_keywords(raw_lower, ("icd 203", "nine tradecraft", "analytic tradecraft standard", "analytic confidence")):
        return "analytic_tradecraft_standards"
    if _match_keywords(raw_lower, ("bias", "heuristic", "cognitive trap", "mirror imaging")):
        return "analytic_tradecraft_bias"
    return None


def _cognitive_subcategory(raw_lower: str) -> str | None:
    if _match_keywords(raw_lower, ("epistemic", "knowledge integrity", "malign influence")):
        return "cognitive_resilience_epistemic"
    if _match_keywords(raw_lower, ("prebunking", "inoculation", "debunking")):
        return "cognitive_resilience_inoculation"
    if _match_keywords(raw_lower, ("neuro", "resaid", "neurips", "brain", "cognitive mechanism")):
        return "cognitive_resilience_neuro"
    return None


def _category_frame_key(entry: TopicEntry) -> str:
    raw = entry.display_title.lower()
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


def synthesized_concept_frame(entry: TopicEntry, coursebook: CoursebookProfile, profile: IntelligenceProfile) -> str:
    """Provide honest profile framing, not a definition made from title words."""
    distinction = coursebook.key_distinction.rstrip(".")
    return (
        f"**{entry.display_title}** is taught in the **{profile.title}** lane. "
        f"The analytic distinction is to {distinction}. "
        "Apply it to the supplied evidence; a topic label alone establishes "
        "neither a mechanism nor a conclusion."
    )


def concept_frame_for_entry(entry: TopicEntry, coursebook: CoursebookProfile, profile: IntelligenceProfile) -> str:
    from .topic_prompt_routes import pattern_profile_for_entry

    pattern = pattern_profile_for_entry(entry)
    if pattern:
        return (
            f"**{pattern.safe_name}** uses {pattern.methods}. "
            f"Its classroom application is {pattern.application}; it {pattern.safety_boundary}."
        )
    # Tier A follows the instructional subject, never a competing source title.
    frame = _first_matching_frame(entry.display_title.lower(), CONCEPT_KEYWORD_ROUTES)
    if frame:
        return frame
    category_key = _category_frame_key(entry)
    category_frame = CATEGORY_CONCEPT_FRAMES.get(category_key)
    if category_frame:
        return category_frame
    return synthesized_concept_frame(entry, coursebook, profile)


def synthesized_evidence_prompt(entry: TopicEntry, lens: PracticeLens, coursebook: CoursebookProfile) -> str:
    return (
        f"For **{entry.display_title}**, inspect records relevant to {coursebook.practice_focus}, "
        "their versions, original sources, and dependency links. "
        f"Apply the **{lens.title}** check; record missing evidence and what would change the judgment."
    )


# Deferred import: breaks cycle with topic_prompt_routes importing _12_concept_routes.
from .topic_prompt_routes import (  # noqa: E402 - deferred to break route/frame import cycle
    artifact_prompt_for_entry as _artifact_prompt_from_routes,
    evidence_prompt_for_entry as _evidence_prompt_from_routes,
)


def evidence_prompt_for_entry(entry: TopicEntry, lens: PracticeLens, coursebook: CoursebookProfile) -> str:
    return _evidence_prompt_from_routes(entry, lens, coursebook, synthesized_evidence_prompt=synthesized_evidence_prompt)


def artifact_prompt_for_entry(entry: TopicEntry, lens: PracticeLens, coursebook: CoursebookProfile) -> str:
    return _artifact_prompt_from_routes(entry, lens, coursebook)


def lesson_intro_paragraph(chapter_title: str, coursebook: CoursebookProfile, lens: PracticeLens, topic_titles: tuple[str, ...]) -> str:
    opener = topic_titles[0] if topic_titles else chapter_title
    topic_path = ", ".join(f"**{title}**" for title in topic_titles[:3]) if topic_titles else f"**{opener}**"
    return (
        f"**{chapter_title}** builds {coursebook.disciplinary_frame}. "
        f"The sequence opens with {topic_path} and applies the **{lens.title}** "
        "practice frame through concept, evidence, artifact, misconception, and transfer tasks."
    )
