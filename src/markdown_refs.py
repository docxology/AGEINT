"""Validated Pandoc and Pandoc-crossref reference helpers for AGEINT."""

from __future__ import annotations

from collections.abc import Callable, Iterable
import re
from typing import Any, Mapping

_CROSSREF_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*:[A-Za-z0-9][A-Za-z0-9_-]*$")
_CITATION_RE = re.compile(r"^[A-Za-z][A-Za-z0-9_-]*$")
_CROSSREF_PREFIXES = ("fig:", "sec:", "eq:", "tbl:")


def _validate_crossref(label: str, prefix: str) -> str:
    if not label.startswith(prefix) or not _CROSSREF_RE.fullmatch(label):
        raise ValueError(f"Expected {prefix} label, got {label!r}")
    return label


def _validate_citation_key(key: str) -> str:
    if key.startswith("@") or key.startswith(_CROSSREF_PREFIXES) or not _CITATION_RE.fullmatch(key):
        raise ValueError(f"Expected citation key without Pandoc brackets, got {key!r}")
    return key


def _unique_nonempty(values: Iterable[str]) -> list[str]:
    seen: set[str] = set()
    resolved: list[str] = []
    for value in values:
        if not value or value in seen:
            continue
        seen.add(value)
        resolved.append(value)
    return resolved


def _ref_list(
    values: Iterable[str],
    renderer: Callable[[str], str],
    *,
    separator: str,
) -> str:
    return separator.join(renderer(value) for value in _unique_nonempty(values))


def section_ref(label: str) -> str:
    """Return a Pandoc-crossref section reference for a ``sec:`` label."""
    return f"[@{_validate_crossref(label, 'sec:')}]"


def figure_ref(label: str) -> str:
    """Return a Pandoc-crossref figure reference for a ``fig:`` label."""
    return f"[@{_validate_crossref(label, 'fig:')}]"


def equation_ref(label: str) -> str:
    """Return a Pandoc-crossref equation reference for an ``eq:`` label."""
    return f"[@{_validate_crossref(label, 'eq:')}]"


def table_ref(label: str) -> str:
    """Return a Pandoc-crossref table reference for a ``tbl:`` label."""
    return f"[@{_validate_crossref(label, 'tbl:')}]"


def citation_ref(key: str) -> str:
    """Return a Pandoc citation reference for a BibTeX key."""
    return f"[@{_validate_citation_key(key)}]"


def section_ref_list(labels: Iterable[str], *, separator: str = ", ") -> str:
    """Return a deduplicated section-reference list."""
    return _ref_list(labels, section_ref, separator=separator)


def figure_ref_list(labels: Iterable[str], *, separator: str = " ") -> str:
    """Return a deduplicated figure-reference list."""
    return _ref_list(labels, figure_ref, separator=separator)


def citation_ref_list(keys: Iterable[str], *, separator: str = "; ") -> str:
    """Return a deduplicated Pandoc citation-reference list."""
    return _ref_list(keys, citation_ref, separator=separator)


def crossref_slug(value: str) -> str:
    """Return a Pandoc-safe slug aligned with manuscript manifest labels."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "section"


def part_module_map_figure_label(part: Mapping[str, Any]) -> str:
    """Return the registry figure label for a curriculum part module map."""
    return f"fig:part-{crossref_slug(str(part['title']))}-module-map"


def chapter_section_ref(chapter: Mapping[str, Any]) -> str:
    """Return a section reference for a generated chapter overview."""
    return section_ref(f"sec:chapter-{crossref_slug(str(chapter['title']))}")


def lesson_educational_crossrefs(part: Mapping[str, Any], chapter: Mapping[str, Any]) -> str:
    """Return inline cross-links tying topic lessons to unit map and module overview."""
    unit_map = figure_ref(part_module_map_figure_label(part))
    module_overview = chapter_section_ref(chapter)
    atlas = section_ref("sec:curriculum_orientation")
    return (
        f"**Cross-links.** Unit module map {unit_map}; "
        f"module overview {module_overview}; curriculum atlas {atlas}."
    )


__all__ = [
    "citation_ref",
    "citation_ref_list",
    "chapter_section_ref",
    "crossref_slug",
    "equation_ref",
    "figure_ref",
    "figure_ref_list",
    "lesson_educational_crossrefs",
    "part_module_map_figure_label",
    "section_ref",
    "section_ref_list",
    "table_ref",
]
