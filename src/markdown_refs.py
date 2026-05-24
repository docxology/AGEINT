"""Validated Pandoc and Pandoc-crossref reference helpers for AGEINT."""

from __future__ import annotations

from collections.abc import Callable, Iterable
import re

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


__all__ = [
    "citation_ref",
    "citation_ref_list",
    "equation_ref",
    "figure_ref",
    "figure_ref_list",
    "section_ref",
    "section_ref_list",
    "table_ref",
]
