"""Manuscript manifest datatypes and slug helpers."""

from __future__ import annotations

from dataclasses import dataclass
import json
import re
from typing import Any


@dataclass(frozen=True)
class ManuscriptSection:
    """A generated manuscript section with semantic output path and context."""

    kind: str
    title: str
    relative_path: str
    template_name: str
    context: dict[str, str]
    order: int
    section_label: str = ""
    parent_label: str = ""
    previous_label: str = ""
    next_label: str = ""
    figure_labels: tuple[str, ...] = ()
    chapter_number: int | None = None
    appendix_letter: str | None = None


@dataclass(frozen=True)
class ManuscriptManifest:
    """Ordered AGEINT manuscript manifest."""

    sections: list[ManuscriptSection]
    units: list[dict[str, Any]]
    appendix_files: list[str]

    @property
    def chapter_sections(self) -> list[ManuscriptSection]:
        return [section for section in self.sections if section.kind == "chapter"]

    @property
    def part_sections(self) -> list[ManuscriptSection]:
        return [section for section in self.sections if section.kind == "part"]

    @property
    def appendix_sections(self) -> list[ManuscriptSection]:
        return [section for section in self.sections if section.kind == "appendix"]

    def section_for_chapter(self, number: int) -> ManuscriptSection:
        for section in self.chapter_sections:
            if section.chapter_number == number:
                return section
        raise KeyError(f"No chapter section {number}")

    def section_for_appendix(self, letter: str) -> ManuscriptSection:
        normalized = letter.upper()
        for section in self.appendix_sections:
            if section.appendix_letter == normalized:
                return section
        raise KeyError(f"No appendix section {letter}")

    def config_yaml(self) -> str:
        """Return YAML ordering understood by infrastructure manuscript discovery."""
        return ordering_config_yaml(["abstract.md", "orientation.md"], self.units, self.appendix_files)


def ordering_config_yaml(
    front_matter_files: list[str],
    units: list[dict[str, Any]],
    appendix_files: list[str],
) -> str:
    """Return YAML ordering understood by infrastructure manuscript discovery."""
    lines = [
        "front_matter:",
        "  include_front_matter: true",
        f"  files: {_flow_file_entries(front_matter_files)}",
    ]
    lines.append("units:")
    for unit in units:
        lines.extend(
            [
                f"  - id: {unit['id']}",
                f"    directory: {unit['directory']}",
                "    chapters:",
            ]
        )
        for chapter_file in unit["chapters"]:
            lines.append(f"      - file: {chapter_file}")

    lines.extend(
        [
            "appendices:",
            "  include_reference: true",
            f"  reference: {_flow_file_entries(appendix_files)}",
        ]
    )
    return "\n".join(lines) + "\n"


def _flow_file_entries(file_names: list[str]) -> str:
    """Return compact YAML file-entry list for long generated ordering surfaces."""
    return "[" + ", ".join(f'{{file: {json.dumps(file_name)}}}' for file_name in file_names) + "]"


class SlugRegistry:
    """Track unique slugs per namespace for stable section labels."""

    def __init__(self) -> None:
        self._seen: dict[str, set[str]] = {}

    def unique(self, namespace: str, value: str) -> str:
        base = slugify(value)
        seen = self._seen.setdefault(namespace, set())
        if base not in seen:
            seen.add(base)
            return base
        suffix = 2
        while f"{base}-{suffix}" in seen:
            suffix += 1
        resolved = f"{base}-{suffix}"
        seen.add(resolved)
        return resolved


def slugify(value: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or "section"


def section_label(kind: str, slug: str) -> str:
    return f"sec:{kind}-{slug}"


# Back-compat aliases for merged part modules.
_SlugRegistry = SlugRegistry
_slug = slugify
_label = section_label
_ordering_config_yaml = ordering_config_yaml

__all__ = [
    "ManuscriptManifest",
    "ManuscriptSection",
    "SlugRegistry",
    "_flow_file_entries",
    "ordering_config_yaml",
    "section_label",
    "slugify",
]
