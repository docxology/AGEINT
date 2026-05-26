"""Canonical slug helpers for curriculum shards and inventory paths."""

from __future__ import annotations

import re
from typing import Any, Mapping


def slug_for_path(value: str, *, default: str = "item") -> str:
    """Return a filesystem-safe slug derived from *value*."""
    slug = re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-")
    return slug or default


def numbered_dir_name(number: int, title: str, *, default: str = "item") -> str:
    """Return a numbered shard directory name such as ``03-open-source-intelligence``."""
    return f"{number:02d}-{slug_for_path(title, default=default)}"


def curriculum_part_dir_name(part: Mapping[str, Any]) -> str:
    """Return the on-disk part directory name under ``data/curriculum/parts/``."""
    return numbered_dir_name(int(part["number"]), str(part["title"]))


def curriculum_chapter_dir_name(chapter: Mapping[str, Any]) -> str:
    """Return the on-disk chapter directory name under a part's ``chapters/`` tree."""
    return numbered_dir_name(int(chapter["number"]), str(chapter["title"]))


def curriculum_sections_jsonl_path(part: Mapping[str, Any], chapter: Mapping[str, Any]) -> str:
    """Return the repo-relative path to a chapter's ``sections.jsonl`` shard."""
    part_dir = curriculum_part_dir_name(part)
    chapter_dir = curriculum_chapter_dir_name(chapter)
    return f"data/curriculum/parts/{part_dir}/chapters/{chapter_dir}/sections.jsonl"
