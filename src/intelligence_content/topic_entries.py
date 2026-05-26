"""Pipeline for safe, learner-facing topic entries from curriculum sections."""

from __future__ import annotations

import re
from typing import Any, Final

from curriculum import PATTERN_REGISTRY_CHAPTER_NUMBER

try:
    from intelligence_content._01_part import TopicEntry
    from intelligence_content._06_part import safe_pattern_treatment
    from intelligence_content._07_safe_titles import (
        _topic_anchor_words,
        is_generic_display_title,
        safe_curriculum_treatment,
    )
    from intelligence_content.risk_routes import topic_risk_category
except ImportError:  # pragma: no cover - package import
    from ._01_part import TopicEntry  # type: ignore[no-redef]
    from ._06_part import safe_pattern_treatment  # type: ignore[no-redef]
    from ._07_safe_titles import (  # type: ignore[no-redef]
        _topic_anchor_words,
        is_generic_display_title,
        safe_curriculum_treatment,
    )
    from .risk_routes import topic_risk_category  # type: ignore[no-redef]

META_SOURCE_TOPIC_PREFIXES: Final[tuple[str, ...]] = (
    "v2 source-lane extension:",
    "deep expansion:",
    "evidence-package expansion:",
    "v2 ageint-depth extension:",
)


def is_meta_source_topic(title: str) -> bool:
    lower = title.strip().lower()
    return any(lower.startswith(prefix) for prefix in META_SOURCE_TOPIC_PREFIXES)


def normalize_display_key(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def clean_display_title(title: str) -> str:
    cleaned = re.sub(r":\s*case\s+[\d.]+\s+review\s*$", "", title, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+review\s*$", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip() or title


def load_sections(chapter: dict[str, Any]) -> list[dict[str, Any]]:
    return list(chapter.get("sections", []))


def filter_meta_sections(sections: list[dict[str, Any]]) -> list[dict[str, Any]]:
    filtered: list[dict[str, Any]] = []
    seen_raw_titles: set[str] = set()
    for section in sections:
        raw_title = str(section.get("title", "source-guide topic")).strip()
        if is_meta_source_topic(raw_title):
            continue
        if raw_title in seen_raw_titles:
            continue
        seen_raw_titles.add(raw_title)
        filtered.append(section)
    return filtered


def apply_pattern_registry(
    raw_title: str,
    *,
    safe_patterns: bool,
    active_pattern_number: int | None,
) -> tuple[str, int | None, str, str]:
    working_title = raw_title
    source_locus = ""
    provenance_note = raw_title
    risk_category = "standard"
    if not safe_patterns:
        return working_title, active_pattern_number, source_locus, provenance_note
    working_title, active_pattern_number = safe_pattern_treatment(
        working_title,
        active_pattern_number,
    )
    risk_category = "ageint_pattern_registry"
    source_locus = (
        f"Pattern {active_pattern_number}" if active_pattern_number else "AGEINT pattern registry"
    )
    provenance_note = "Original source identity preserved in AGEINT pattern registry"
    return working_title, active_pattern_number, source_locus, provenance_note


def safe_curriculum_title(
    working_title: str,
    *,
    safe_patterns: bool,
    part_title: str,
    chapter_title: str,
) -> str:
    display_title = (
        working_title
        if safe_patterns
        else safe_curriculum_treatment(working_title, part_title, chapter_title)
    )
    display_title = clean_display_title(display_title)
    if not safe_patterns and is_generic_display_title(display_title):
        shard_fallback = clean_display_title(working_title)
        if shard_fallback and not is_generic_display_title(shard_fallback):
            display_title = shard_fallback
    return display_title


def dedupe_display_title(
    display_title: str,
    *,
    working_title: str,
    raw_title: str,
    source_locus: str,
    seen_display_keys: set[str],
) -> str:
    display_key = normalize_display_key(display_title)
    if display_key in seen_display_keys:
        raw_key = normalize_display_key(clean_display_title(working_title))
        if raw_key != display_key:
            qualifier = source_locus or _topic_anchor_words(raw_title, limit=3)
            display_title = f"{display_title} ({qualifier})"
        else:
            qualifier = _topic_anchor_words(raw_title, limit=4)
            display_title = f"{clean_display_title(working_title)} ({qualifier})"
    seen_display_keys.add(normalize_display_key(display_title))
    return display_title


def safe_topic_entries(chapter: dict[str, Any], part: dict[str, Any]) -> list[TopicEntry]:
    """Return safe, learner-facing source topics with provenance metadata."""
    part_title = str(part["title"])
    chapter_title = str(chapter["title"])
    sections = load_sections(chapter)
    if not sections:
        return [
            TopicEntry(
                raw_title=chapter_title,
                display_title=chapter_title,
                source_locus="chapter",
                provenance_note="Parsed chapter title and citation spine",
                risk_category="standard",
                citation_numbers=tuple(int(number) for number in chapter.get("citations", [])),
            )
        ]

    entries: list[TopicEntry] = []
    seen_display_keys: set[str] = set()
    safe_patterns = chapter.get("number") == PATTERN_REGISTRY_CHAPTER_NUMBER
    active_pattern_number: int | None = None

    for section in filter_meta_sections(sections):
        raw_title = str(section.get("title", "source-guide topic")).strip()
        source_locus = str(section.get("number") or "").strip()
        provenance_note = f"{source_locus} {raw_title}".strip()
        risk_category = topic_risk_category(raw_title, part_title, chapter_title)

        working_title, active_pattern_number, pattern_locus, pattern_note = apply_pattern_registry(
            raw_title,
            safe_patterns=safe_patterns,
            active_pattern_number=active_pattern_number,
        )
        if safe_patterns:
            source_locus = pattern_locus or source_locus
            provenance_note = pattern_note
            risk_category = "ageint_pattern_registry"

        display_title = safe_curriculum_title(
            working_title,
            safe_patterns=safe_patterns,
            part_title=part_title,
            chapter_title=chapter_title,
        )
        display_title = dedupe_display_title(
            display_title,
            working_title=working_title,
            raw_title=raw_title,
            source_locus=source_locus,
            seen_display_keys=seen_display_keys,
        )

        if risk_category not in {"standard", "ageint_pattern_registry"}:
            provenance_note = (
                f"{source_locus or 'chapter outline'} transformed from high-risk source title: "
                f"{raw_title}"
            )
        entries.append(
            TopicEntry(
                raw_title=raw_title,
                display_title=display_title,
                source_locus=source_locus or "chapter outline",
                provenance_note=provenance_note,
                risk_category=risk_category,
                citation_numbers=tuple(int(number) for number in section.get("citations", [])),
            )
        )

    if entries:
        return entries
    return [
        TopicEntry(
            raw_title=chapter_title,
            display_title=chapter_title,
            source_locus="chapter",
            provenance_note="Parsed chapter title and citation spine",
            risk_category="standard",
            citation_numbers=tuple(int(number) for number in chapter.get("citations", [])),
        )
    ]


__all__ = [
    "META_SOURCE_TOPIC_PREFIXES",
    "clean_display_title",
    "dedupe_display_title",
    "filter_meta_sections",
    "is_meta_source_topic",
    "load_sections",
    "normalize_display_key",
    "safe_curriculum_title",
    "safe_topic_entries",
]
