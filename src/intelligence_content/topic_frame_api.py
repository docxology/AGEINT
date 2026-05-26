"""Stable frame API for topic lesson field resolution."""

from __future__ import annotations

try:
    from ._12_topic_frames import (
        artifact_prompt_for_entry,
        concept_frame_for_entry,
        evidence_prompt_for_entry,
        misconception_for_entry,
        why_it_matters_for_entry,
    )
except ImportError:  # pragma: no cover - package import
    from intelligence_content._12_topic_frames import (  # type: ignore[no-redef]
        artifact_prompt_for_entry,
        concept_frame_for_entry,
        evidence_prompt_for_entry,
        misconception_for_entry,
        why_it_matters_for_entry,
    )

__all__ = [
    "artifact_prompt_for_entry",
    "concept_frame_for_entry",
    "evidence_prompt_for_entry",
    "misconception_for_entry",
    "why_it_matters_for_entry",
]
