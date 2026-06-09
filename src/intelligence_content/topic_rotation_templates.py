"""YAML-driven why-it-matters and misconception rotation for topic lessons."""

from __future__ import annotations

from typing import TYPE_CHECKING

from _data_loaders import (
    misconception_category_routes,
    misconception_fallbacks,
    misconception_keyword_routes,
    misconception_risk_templates,
    risk_why_failure_hints,
    why_it_matters_templates,
)
from ._12_concept_routes import _first_matching_frame
from .topic_rotation import template_index

if TYPE_CHECKING:
    from ._01_part import CoursebookProfile, TopicEntry
    from ._04b_part import IntelligenceProfile


def why_it_matters_for_entry(
    entry: TopicEntry,
    profile: IntelligenceProfile,
    coursebook: CoursebookProfile,
    *,
    lesson_index: int,
    chapter_title: str = "",
) -> str:
    """Resolve why-it-matters prose from YAML templates and profile context."""
    templates = why_it_matters_templates()
    failure_hint = risk_why_failure_hints().get(
        entry.risk_category,
        profile.failure_modes.split(",")[0].strip() if profile.failure_modes else "overconfidence",
    )
    # Seed the template choice on a per-topic digest rather than the linear
    # lesson_index. Adding lesson_index linearly made consecutive lessons march
    # through the templates in a predictable A-B-C-D cadence; hashing the topic's
    # identity decorrelates adjacent lessons while staying deterministic.
    template_index_value = template_index(
        entry.display_title,
        entry.raw_title,
        chapter_title,
        entry.risk_category,
        str(lesson_index),
        count=len(templates),
    )
    template = templates[template_index_value]
    practice_focus = coursebook.practice_focus.removesuffix(" review")
    return template.format(
        topic=entry.display_title,
        distinction=coursebook.key_distinction,
        profile=profile.title,
        practice_focus=practice_focus,
        failure_hint=failure_hint,
    )


def misconception_for_entry(
    entry: TopicEntry,
    coursebook: CoursebookProfile,
    *,
    lesson_index: int = 1,
    chapter_title: str = "",
) -> str:
    """Resolve misconception text from YAML templates and keyword branches.

    Precedence matches the other resolvers (route -> category -> fallback):
    content-specific keyword routes (FISA, MICE, ATT&CK, GEOINT, ACH, ...) are
    consulted first so a topic that matches one gets its tailored misconception
    even when it also carries a non-standard risk category; only then do the
    generic per-risk templates and round-robin fallbacks apply.
    """
    raw = f"{entry.display_title} {entry.raw_title}".lower()
    routed = _first_matching_frame(raw, misconception_keyword_routes())
    if routed:
        return routed
    category_route = misconception_category_routes().get(entry.risk_category)
    if category_route:
        return category_route
    if entry.risk_category != "standard" and entry.risk_category != "ageint_pattern_registry":
        chapter_anchor = chapter_title or "this module"
        templates = misconception_risk_templates()
        slot = template_index(
            entry.display_title,
            chapter_title,
            str(lesson_index),
            entry.risk_category,
            count=len(templates),
        )
        return templates[slot].format(
            display_title=entry.display_title,
            chapter_anchor=chapter_anchor,
        )
    fallbacks = misconception_fallbacks()
    chapter_base = template_index(chapter_title, count=len(fallbacks))
    template_slot = (chapter_base + lesson_index - 1) % len(fallbacks)
    template = fallbacks[template_slot]
    return template.format(topic=entry.display_title, focus=coursebook.key_distinction)


__all__ = ["misconception_for_entry", "why_it_matters_for_entry"]
