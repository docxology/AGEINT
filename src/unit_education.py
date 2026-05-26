"""Data-backed unit-specific educational content for AGEINT renderers."""

from __future__ import annotations

from dataclasses import dataclass
import re
from typing import Any

from _data_loaders import unit_education_profiles


@dataclass(frozen=True)
class UnitEducationProfile:
    """A unit-level teaching spine loaded from ``data/unit_education_profiles.yaml``."""

    number: int
    unit_key: str
    concept: str
    discipline_spine: str
    source_use_contract: str
    practice_artifact: str
    safety_boundary: str
    learning_spine: str
    evidence_artifacts: tuple[str, ...]
    anchor_numbers: tuple[int, ...]


def unit_profile_for_number(number: int) -> UnitEducationProfile:
    """Return the educational profile for a part number."""
    raw = unit_education_profiles()[int(number)]
    return UnitEducationProfile(
        number=int(number),
        unit_key=str(raw["unit_key"]),
        concept=str(raw["concept"]),
        discipline_spine=str(raw["discipline_spine"]),
        source_use_contract=str(raw["source_use_contract"]),
        practice_artifact=str(raw["practice_artifact"]),
        safety_boundary=str(raw["safety_boundary"]),
        learning_spine=str(raw["learning_spine"]),
        evidence_artifacts=tuple(str(item) for item in raw.get("evidence_artifacts", ())),
        anchor_numbers=tuple(int(item) for item in raw.get("anchor_numbers", ())),
    )


def unit_profile_for_part(part: dict[str, Any]) -> UnitEducationProfile:
    """Return the educational profile for a curriculum part dictionary."""
    return unit_profile_for_number(int(part["number"]))


def render_unit_profile_markdown(part: dict[str, Any]) -> str:
    """Render reader-facing unit education sections for a unit introduction."""
    profile = unit_profile_for_part(part)
    artifact_list = "; ".join(profile.evidence_artifacts)
    return "\n\n".join(
        [
            "### Discipline spine",
            (
                f"This unit teaches **{profile.concept}**. "
                f"{profile.discipline_spine}"
            ),
            "### Source-use contract",
            profile.source_use_contract,
            "### Practice artifact",
            (
                f"The recurring practice artifact is a **{profile.practice_artifact}**. "
                f"It draws on {artifact_list} and keeps the unit's learning spine explicit: "
                f"{profile.learning_spine}"
            ),
            "### Safety boundary",
            profile.safety_boundary,
        ]
    )


def unit_lesson_evidence_line(profile: UnitEducationProfile, topic_title: str) -> str:
    """Return a compact unit-specific evidence sentence for a topic lesson."""
    artifacts = ", ".join(profile.evidence_artifacts[:3])
    return (
        f"For **{topic_title}**, the unit-specific evidence focus is {artifacts}; "
        f"it supports {profile.concept} without crossing the unit safety boundary."
    )


def unit_lesson_artifact_line(profile: UnitEducationProfile, topic_title: str) -> str:
    """Return a compact unit-specific artifact sentence for a topic lesson."""
    return (
        f"Shape **{topic_title}** work as a **{profile.practice_artifact}** that "
        "names evidence, uncertainty, reviewer, and stop condition."
    )


def unit_specific_terms(profile: UnitEducationProfile) -> set[str]:
    """Return normalized terms expected to appear in rendered unit-specific lessons."""
    terms = {profile.concept, profile.practice_artifact, *profile.evidence_artifacts}
    return {
        token
        for value in terms
        for token in re.findall(r"[a-z0-9][a-z0-9-]{3,}", value.lower())
    }


__all__ = [
    "UnitEducationProfile",
    "render_unit_profile_markdown",
    "unit_lesson_artifact_line",
    "unit_lesson_evidence_line",
    "unit_profile_for_number",
    "unit_profile_for_part",
    "unit_specific_terms",
]
