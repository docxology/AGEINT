"""Unified resolver for generated topic-lesson field prose."""

from __future__ import annotations

import zlib
from dataclasses import dataclass
from typing import TYPE_CHECKING, Any

try:
    from unit_education import unit_lesson_artifact_line, unit_lesson_evidence_line
except ImportError:  # pragma: no cover - package import
    from ..unit_education import unit_lesson_artifact_line, unit_lesson_evidence_line  # type: ignore[no-redef]

if TYPE_CHECKING:
    from ._01_part import CoursebookProfile, PracticeLens, TopicEntry
    from ._04b_part import IntelligenceProfile


def template_index(*parts: str, count: int) -> int:
    """Return a stable template slot from joined identity parts."""
    if count <= 0:
        raise ValueError("template count must be positive")
    seed = "|".join(parts).encode("utf-8")
    return zlib.adler32(seed) % count


@dataclass(frozen=True)
class TopicLessonFields:
    """Resolved reader-facing strings for one topic lesson."""

    concept: str
    why_it_matters: str
    evidence_prompt: str
    artifact_prompt: str
    misconception: str
    transfer_task: str


def _topic_frame_helpers() -> tuple[Any, ...]:
    try:
        from intelligence_content._12_topic_frames import (
            artifact_prompt_for_entry,
            concept_frame_for_entry,
            evidence_prompt_for_entry,
            misconception_for_entry,
            why_it_matters_for_entry,
        )
    except ImportError:  # pragma: no cover - merged namespace
        from ._12_topic_frames import (  # type: ignore[no-redef]
            artifact_prompt_for_entry,
            concept_frame_for_entry,
            evidence_prompt_for_entry,
            misconception_for_entry,
            why_it_matters_for_entry,
        )
    return (
        artifact_prompt_for_entry,
        concept_frame_for_entry,
        evidence_prompt_for_entry,
        misconception_for_entry,
        why_it_matters_for_entry,
    )


def _lower_first_word(text: str) -> str:
    stripped = text.strip()
    return stripped[:1].lower() + stripped[1:] if stripped else stripped


def _for_topic(entry: TopicEntry, text: str) -> str:
    if entry.display_title in text or f"**{entry.display_title}**" in text:
        return text
    return f"For **{entry.display_title}**, {_lower_first_word(text)}"


def _reader_facing_concept(entry: TopicEntry, frame: str) -> str:
    text = frame.strip()
    if f"**{entry.display_title}**" in text:
        return text
    replacements = {
        "Analyze ": "analyzes ",
        "Applies ": "applies ",
        "Connect ": "connects ",
        "Define ": "defines ",
        "Distinguish ": "distinguishes ",
        "Evaluate ": "evaluates ",
        "Explain how ": "shows how ",
        "Focus on ": "focuses on ",
        "Frame ": "frames ",
        "Map ": "maps ",
        "Read ": "reads ",
        "Shows ": "shows ",
        "Study ": "studies ",
        "Translate ": "translates ",
        "Treat ": "treats ",
        "Use ": "uses ",
    }
    for prefix, replacement in replacements.items():
        if text.startswith(prefix):
            text = replacement + text[len(prefix) :]
            break
    return f"**{entry.display_title}** {text}"


def _evidence_packet_sentence(
    entry: TopicEntry,
    text: str,
    *,
    unit_profile: Any | None = None,
) -> str:
    rendered = _for_topic(entry, text)
    rendered = rendered.replace(", evidence packet:", ", the evidence packet contains", 1)
    if unit_profile is not None:
        rendered = f"{rendered} {unit_lesson_evidence_line(unit_profile, entry.display_title)}"
    return rendered


def _student_artifact_sentence(
    entry: TopicEntry,
    text: str,
    *,
    unit_profile: Any | None = None,
) -> str:
    rendered = _for_topic(entry, text)
    for source, replacement in (
        (", submit a completed **", ", build a **"),
        (", submit an ", ", build an "),
        (", submit a ", ", build a "),
    ):
        rendered = rendered.replace(source, replacement, 1)
    if rendered.startswith("Submit a completed **"):
        rendered = "Build a **" + rendered.removeprefix("Submit a completed **")
    elif rendered.startswith("Submit an "):
        rendered = "Build an " + rendered.removeprefix("Submit an ")
    elif rendered.startswith("Submit a "):
        rendered = "Build a " + rendered.removeprefix("Submit a ")
    if unit_profile is not None:
        rendered = f"{rendered} {unit_lesson_artifact_line(unit_profile, entry.display_title)}"
    return rendered


def transfer_task_for_entry(
    entry: TopicEntry,
    coursebook: CoursebookProfile,
    *,
    lesson_index: int = 1,
    chapter_title: str = "",
) -> str:
    raw = entry.raw_title.lower()
    if "active inference" in raw or "free energy" in raw or "predictive" in raw:
        return (
            "Transfer the idea to a non-AI chapter by naming the assumed model, the "
            "surprising observation, and the review point before any decision follows."
        )
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
    unit_profile: Any | None = None,
) -> TopicLessonFields:
    """Resolve all topic-lesson fields in canonical routing order."""
    (
        artifact_prompt_for_entry,
        concept_frame_for_entry,
        evidence_prompt_for_entry,
        misconception_for_entry,
        why_it_matters_for_entry,
    ) = _topic_frame_helpers()
    concept = _reader_facing_concept(
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
    evidence_prompt = _evidence_packet_sentence(
        entry,
        evidence_prompt_for_entry(entry, lens, coursebook),
        unit_profile=unit_profile,
    )
    artifact_prompt = _student_artifact_sentence(
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
    transfer_task = _for_topic(
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


__all__ = [
    "TopicLessonFields",
    "resolve_topic_lesson_fields",
    "template_index",
    "transfer_task_for_entry",
]
