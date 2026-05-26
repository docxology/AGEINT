"""Shard loading and payload normalization for AGEINT curriculum data."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from _data_loaders import source_support_expansion
from _jsonl import read_jsonl


def dedupe_references(references: list[dict[str, Any]]) -> list[dict[str, Any]]:
    """Keep one row per citation key; later shard rows win when files overlap."""

    by_key: dict[str, dict[str, Any]] = {}
    for reference in references:
        key = str(reference.get("key") or "")
        if key:
            by_key[key] = reference
    return sorted(by_key.values(), key=lambda ref: int(ref.get("number") or 0))


def load_curriculum_shards_payload(directory: Path) -> dict[str, Any]:
    """Compose a curriculum payload from the sharded data directory."""
    metadata_path = directory / "metadata.json"
    stats_path = directory / "stats.json"
    if not metadata_path.is_file() or not stats_path.is_file():
        raise FileNotFoundError(f"No sharded AGEINT curriculum found in {directory}")

    parts: list[dict[str, Any]] = []
    for part_path in sorted((directory / "parts").glob("*/part.json")):
        part = json.loads(part_path.read_text(encoding="utf-8"))
        chapters = []
        for path in sorted((part_path.parent / "chapters").iterdir()):
            if path.is_dir():
                chapter = json.loads((path / "chapter.json").read_text(encoding="utf-8"))
                chapter["sections"] = read_jsonl(path / "sections.jsonl")
                chapters.append(chapter)
            elif path.suffix == ".json":
                chapters.append(json.loads(path.read_text(encoding="utf-8")))
        part.pop("chapter_files", None)
        part["chapters"] = chapters
        parts.append(part)

    appendices = [
        json.loads(path.read_text(encoding="utf-8"))
        for path in sorted((directory / "appendices").glob("*.json"))
    ]
    references = dedupe_references(
        [
            row
            for path in sorted((directory / "references").glob("*.jsonl"))
            for row in read_jsonl(path)
        ]
    )
    payload = {
        **json.loads(metadata_path.read_text(encoding="utf-8")),
        "parts": parts,
        "appendices": appendices,
        "patterns": json.loads((directory / "patterns.json").read_text(encoding="utf-8")),
        "references": references,
        "stats": json.loads(stats_path.read_text(encoding="utf-8")),
    }
    return finalize_curriculum_payload(payload)


def finalize_curriculum_payload(payload: dict[str, Any]) -> dict[str, Any]:
    """Normalize derived counts and hydrate data-backed citation support."""

    hydrate_source_support(payload)
    payload["stats"] = {
        **payload.get("stats", {}),
        "parts": len(payload.get("parts", [])),
        "chapters": sum(len(part.get("chapters", [])) for part in payload.get("parts", [])),
        "appendices": len(payload.get("appendices", [])),
        "patterns": len(payload.get("patterns", [])),
        "references": len(payload.get("references", [])),
    }
    return payload


def hydrate_source_support(payload: dict[str, Any]) -> None:
    """Attach configured source support to uncited source sections."""

    reference_numbers = {
        int(reference["number"])
        for reference in payload.get("references", [])
        if isinstance(reference.get("number"), int)
    }
    if not reference_numbers:
        return
    expansion = source_support_expansion()
    for part in payload.get("parts", []):
        part_default = filtered_citation_numbers(
            expansion.get("part_defaults", {}).get(int(part.get("number", 0)), ()),
            reference_numbers,
        )
        for chapter in part.get("chapters", []):
            chapter_citations = unique_ints(chapter.get("citations", []))
            for section in chapter.get("sections", []):
                section_citations = unique_ints(section.get("citations", []))
                if not section_citations:
                    section_citations = source_support_numbers_for_section(
                        expansion,
                        part,
                        chapter,
                        section,
                        reference_numbers,
                        part_default=part_default,
                    )
                    section["citations"] = section_citations
                for number in section_citations:
                    if number not in chapter_citations:
                        chapter_citations.append(number)
            chapter["citations"] = chapter_citations


def source_support_numbers_for_section(
    expansion: dict[str, Any],
    part: dict[str, Any],
    chapter: dict[str, Any],
    section: dict[str, Any],
    reference_numbers: set[int],
    *,
    part_default: list[int],
) -> list[int]:
    haystack = " ".join(
        str(value)
        for value in (
            part.get("title", ""),
            chapter.get("title", ""),
            section.get("number", ""),
            section.get("title", ""),
            section.get("raw", ""),
        )
    ).lower()
    for row in expansion.get("keyword_routes", []):
        keywords = tuple(str(keyword).lower() for keyword in row.get("keywords", ()))
        if any(keyword in haystack for keyword in keywords):
            routed = filtered_citation_numbers(row.get("citations", ()), reference_numbers)
            if routed:
                return routed
    if part_default:
        return part_default
    return filtered_citation_numbers(expansion.get("default_citations", ()), reference_numbers)


def filtered_citation_numbers(numbers: Any, reference_numbers: set[int]) -> list[int]:
    return [number for number in unique_ints(numbers or []) if number in reference_numbers]


def unique_ints(numbers: Any) -> list[int]:
    selected: list[int] = []
    for number in numbers or []:
        resolved = int(number)
        if resolved not in selected:
            selected.append(resolved)
    return selected
