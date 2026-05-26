"""Reader-voice helpers for generated topic-lesson prose."""

from __future__ import annotations

from typing import TYPE_CHECKING

from unit_education import UnitEducationProfile, unit_lesson_artifact_line, unit_lesson_evidence_line

if TYPE_CHECKING:
    from ._01_part import TopicEntry


def lower_first_word(text: str) -> str:
    stripped = text.strip()
    return stripped[:1].lower() + stripped[1:] if stripped else stripped


def for_topic(entry: TopicEntry, text: str) -> str:
    if entry.display_title in text or f"**{entry.display_title}**" in text:
        return text
    return f"For **{entry.display_title}**, {lower_first_word(text)}"


def reader_facing_concept(entry: TopicEntry, frame: str) -> str:
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


def evidence_packet_sentence(
    entry: TopicEntry,
    text: str,
    *,
    unit_profile: UnitEducationProfile | None = None,
) -> str:
    rendered = for_topic(entry, text)
    rendered = rendered.replace(", evidence packet:", ", the evidence packet contains", 1)
    if unit_profile is not None:
        rendered = f"{rendered} {unit_lesson_evidence_line(unit_profile, entry.display_title)}"
    return rendered


def student_artifact_sentence(
    entry: TopicEntry,
    text: str,
    *,
    unit_profile: UnitEducationProfile | None = None,
) -> str:
    rendered = for_topic(entry, text)
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


__all__ = [
    "evidence_packet_sentence",
    "for_topic",
    "lower_first_word",
    "reader_facing_concept",
    "student_artifact_sentence",
]
