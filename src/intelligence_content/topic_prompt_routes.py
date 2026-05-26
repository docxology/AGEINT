"""YAML-driven evidence and artifact prompt evaluation for topic lessons."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

try:
    from _data_loaders import (
        artifact_keyword_routes,
        artifact_risk_category_prompts,
        evidence_category_prompts,
        evidence_keyword_routes,
    )
except ImportError:  # pragma: no cover - package import
    from .._data_loaders import (  # type: ignore[no-redef]
        artifact_keyword_routes,
        artifact_risk_category_prompts,
        evidence_category_prompts,
        evidence_keyword_routes,
    )

if TYPE_CHECKING:
    from ._01_part import CoursebookProfile, PracticeLens, TopicEntry

try:
    from intelligence_content._07_safe_titles import _topic_anchor_words
except ImportError:  # pragma: no cover - merged namespace
    from ._07_safe_titles import _topic_anchor_words  # type: ignore[no-redef]

try:
    from intelligence_content._12_concept_routes import _first_matching_frame
except ImportError:  # pragma: no cover - merged namespace
    from ._12_concept_routes import _first_matching_frame  # type: ignore[no-redef]


def evidence_prompt_for_entry(
    entry: TopicEntry,
    lens: PracticeLens,
    coursebook: CoursebookProfile,
    *,
    synthesized_evidence_prompt: Callable[[TopicEntry, PracticeLens, CoursebookProfile], str],
) -> str:
    """Resolve evidence prompt from YAML routes with synthesized fallback."""
    raw = entry.raw_title.lower()
    routed = _first_matching_frame(raw, evidence_keyword_routes())
    if routed:
        return routed
    category_prompts = evidence_category_prompts()
    category = category_prompts.get(entry.risk_category)
    if category:
        if "sample materials and transparent labels" in entry.display_title.lower():
            anchor = _topic_anchor_words(entry.raw_title, limit=2)
            return (
                f"Evidence packet for **{entry.display_title}**: narrative provenance for {anchor}, "
                "audience-harm notes, attribution evidence, and transparent education options."
            )
        return category
    return synthesized_evidence_prompt(entry, lens, coursebook)


def artifact_prompt_for_entry(
    entry: TopicEntry,
    lens: PracticeLens,
    coursebook: CoursebookProfile,
) -> str:
    """Resolve artifact prompt from YAML routes with default template fallback."""
    raw = entry.raw_title.lower()
    routed = _first_matching_frame(raw, artifact_keyword_routes())
    if routed:
        return routed
    risk_prompts = artifact_risk_category_prompts()
    risk_prompt = risk_prompts.get(entry.risk_category)
    if risk_prompt:
        return risk_prompt
    return (
        f"Build a **{lens.evidence_artifact}** for this {coursebook.practice_focus} "
        f"topic. The artifact must name the source descriptor, bounded claim, caveat, "
        "uncertainty note, blocked-use statement, and accountable reviewer."
    )


__all__ = ["artifact_prompt_for_entry", "evidence_prompt_for_entry"]
