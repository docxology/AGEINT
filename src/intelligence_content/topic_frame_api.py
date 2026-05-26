"""Stable frame API for topic lesson field resolution."""

from __future__ import annotations

from ._12_topic_frames import (
    artifact_prompt_for_entry,
    concept_frame_for_entry,
    evidence_prompt_for_entry,
)
from .topic_rotation_templates import misconception_for_entry, why_it_matters_for_entry

__all__ = [
    "artifact_prompt_for_entry",
    "concept_frame_for_entry",
    "evidence_prompt_for_entry",
    "misconception_for_entry",
    "why_it_matters_for_entry",
]
