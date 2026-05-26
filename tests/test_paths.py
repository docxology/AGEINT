"""Tests for shared AGEINT path helpers."""

from __future__ import annotations

from pathlib import Path

from _paths import remove_tree


def test_remove_tree_deletes_nested_directory_with_symlink(tmp_path: Path) -> None:
    root = tmp_path / "output" / "manuscript"
    parts = root / "parts" / "02-foundations"
    parts.mkdir(parents=True)
    (parts / "00-overview.md").write_text("# Overview\n", encoding="utf-8")
    (parts / "link").symlink_to(parts / "00-overview.md")
    (root / ".DS_Store").write_bytes(b"")

    remove_tree(root)

    assert not root.exists()


def test_remove_tree_is_idempotent_for_missing_path(tmp_path: Path) -> None:
    remove_tree(tmp_path / "missing")
