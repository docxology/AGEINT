"""Tests for shared AGEINT path helpers."""

from __future__ import annotations

from pathlib import Path

from _paths import ensure_project_paths, remove_tree


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


def test_remove_tree_deletes_single_file(tmp_path: Path) -> None:
    target = tmp_path / "scratch.txt"
    target.write_text("data", encoding="utf-8")

    remove_tree(target)

    assert not target.exists()


def test_remove_tree_unlinks_symlink_without_following(tmp_path: Path) -> None:
    real = tmp_path / "real_dir"
    real.mkdir()
    (real / "nested").write_text("kept", encoding="utf-8")
    link = tmp_path / "link_dir"
    link.symlink_to(real)

    remove_tree(link)

    assert not link.exists()
    assert real.exists()
    assert (real / "nested").read_text(encoding="utf-8") == "kept"


def test_remove_tree_with_only_files(tmp_path: Path) -> None:
    """Remove a directory tree whose leaves are plain files (common case)."""
    root = tmp_path / "tree"
    (root / "a").mkdir(parents=True)
    (root / "a" / "one.txt").write_text("1", encoding="utf-8")
    (root / "b.txt").write_text("b", encoding="utf-8")

    remove_tree(root)

    assert not root.exists()


def test_ensure_project_paths_adds_root_and_src_then_is_idempotent(tmp_path: Path) -> None:
    import sys

    root = tmp_path / "proj"
    (root / "src").mkdir(parents=True)
    before = list(sys.path)

    result = ensure_project_paths(root)

    assert result == root.resolve()
    new_entries = [p for p in sys.path if p not in before]
    assert str(root.resolve()) in new_entries
    assert str(root.resolve() / "src") in new_entries

    # Second call must not duplicate entries.
    ensure_project_paths(root)
    assert sys.path.count(str(root.resolve() / "src")) == 1

