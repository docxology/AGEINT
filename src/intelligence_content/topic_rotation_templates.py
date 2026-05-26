"""YAML-driven why-it-matters and misconception rotation for topic lessons."""

from __future__ import annotations

from typing import TYPE_CHECKING

try:
    from _data_loaders import (
        misconception_fallbacks,
        misconception_risk_templates,
        risk_why_failure_hints,
        why_it_matters_templates,
    )
except ImportError:  # pragma: no cover - package import
    from .._data_loaders import (  # type: ignore[no-redef]
        misconception_fallbacks,
        misconception_risk_templates,
        risk_why_failure_hints,
        why_it_matters_templates,
    )

if TYPE_CHECKING:
    from ._01_part import CoursebookProfile, TopicEntry
    from ._04b_part import IntelligenceProfile

try:
    from intelligence_content._12_concept_routes import _match_keywords
except ImportError:  # pragma: no cover - merged namespace
    from ._12_concept_routes import _match_keywords  # type: ignore[no-redef]

try:
    from .topic_rotation import template_index
except ImportError:  # pragma: no cover - merged namespace
    from intelligence_content.topic_rotation import template_index  # type: ignore[no-redef]


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
    chapter_slot = template_index(
        chapter_title,
        entry.risk_category,
        count=len(templates),
    )
    template_index_value = (chapter_slot + lesson_index - 1) % len(templates)
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
    """Resolve misconception text from YAML templates and keyword branches."""
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
    raw = f"{entry.display_title} {entry.raw_title}".lower()
    if _match_keywords(raw, ("mice",)):
        return "that a motivation taxonomy is a recruitment checklist"
    if _match_keywords(raw, ("att&ck",)) or "kill chain" in raw:
        return "that a defensive taxonomy is an instruction sequence"
    if "fisa" in raw or "executive order" in raw:
        return "that a legal source grants authority without scope and oversight"
    if "beneficial ownership" in raw:
        return "that ownership evidence removes uncertainty about control or intent"
    if "geoint" in raw or "imagery" in raw:
        return "that a visible feature is enough for a confident geospatial claim"
    if _match_keywords(raw, ("ach",)) or "competing hypotheses" in raw:
        return "that listing one favored hypothesis is enough without testing alternatives"
    fallbacks = misconception_fallbacks()
    chapter_base = template_index(chapter_title, count=len(fallbacks))
    template_slot = (chapter_base + lesson_index - 1) % len(fallbacks)
    template = fallbacks[template_slot]
    return template.format(topic=entry.display_title, focus=coursebook.key_distinction)


__all__ = ["misconception_for_entry", "why_it_matters_for_entry"]
