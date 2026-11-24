"""Tests for content-addressed build freshness.

The point of the stamp is that freshness survives a git checkout, which does not
preserve mtimes. These tests therefore assert the digest ignores mtimes and that
staleness follows content, with the mtime heuristic kept only as the fallback for
un-stamped trees.
"""

from __future__ import annotations

import os
import time
from pathlib import Path

import pytest

from build_pipeline import BUILD_STAMP_PATH, generated_output_is_stale, read_build_stamp, source_content_digest, write_build_stamp
from orchestration_contracts import output_build_sentinels, source_freshness_roots

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _fake_tree(tmp_path: Path) -> tuple[Path, Path]:
    """Build a minimal tree with every source root and output sentinel present."""
    root = tmp_path / "repo"
    output = root / "output"
    for relative in source_freshness_roots():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.suffix:
            path.mkdir(parents=True, exist_ok=True)
            (path / "seed.txt").write_text("seed\n", encoding="utf-8")
        else:
            path.write_text(f"content of {relative}\n", encoding="utf-8")
    for relative in output_build_sentinels():
        path = output / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text("{}\n", encoding="utf-8")
    return root, output


def test_digest_ignores_mtime(tmp_path: Path) -> None:
    root, _ = _fake_tree(tmp_path)
    before = source_content_digest(root)

    future = time.time() + 10_000
    for relative in source_freshness_roots():
        path = root / relative
        if path.is_file():
            os.utime(path, (future, future))

    assert source_content_digest(root) == before


def test_digest_changes_when_content_changes(tmp_path: Path) -> None:
    root, _ = _fake_tree(tmp_path)
    before = source_content_digest(root)

    target = next(root / r for r in source_freshness_roots() if (root / r).is_file())
    target.write_text("edited\n", encoding="utf-8")

    assert source_content_digest(root) != before


def test_digest_is_independent_of_checkout_location(tmp_path: Path) -> None:
    # A fresh clone lives at a different absolute path; the digest must not care.
    root_a, _ = _fake_tree(tmp_path / "a")
    root_b, _ = _fake_tree(tmp_path / "b")
    assert source_content_digest(root_a) == source_content_digest(root_b)


@pytest.mark.parametrize("metadata_directory", ["ageint_curriculum.egg-info", "ageint_curriculum-0.2.0.dist-info"])
def test_packaging_metadata_does_not_change_authored_source_freshness(tmp_path: Path, metadata_directory: str) -> None:
    root, output = _fake_tree(tmp_path)
    module = root / "src" / "reader.py"
    module.write_text("VALUE = 1\n", encoding="utf-8")
    write_build_stamp(root, output)
    original_digest = source_content_digest(root)

    metadata = root / "src" / metadata_directory / "PKG-INFO"
    metadata.parent.mkdir()
    metadata.write_text("Generated package metadata\n", encoding="utf-8")
    assert source_content_digest(root) == original_digest
    assert generated_output_is_stale(root, output) is False
    metadata.write_text("Regenerated package metadata\n", encoding="utf-8")
    assert generated_output_is_stale(root, output) is False

    module.write_text("VALUE = 2\n", encoding="utf-8")
    assert generated_output_is_stale(root, output) is True


def test_stamped_tree_is_fresh_even_when_source_mtimes_are_newer(tmp_path: Path) -> None:
    # This is the checkout case the mtime heuristic gets wrong.
    root, output = _fake_tree(tmp_path)
    write_build_stamp(root, output)

    future = time.time() + 10_000
    for relative in source_freshness_roots():
        path = root / relative
        if path.is_file():
            os.utime(path, (future, future))

    assert generated_output_is_stale(root, output) is False


def test_stamped_tree_is_stale_when_source_content_changes(tmp_path: Path) -> None:
    root, output = _fake_tree(tmp_path)
    write_build_stamp(root, output)

    target = next(root / r for r in source_freshness_roots() if (root / r).is_file())
    target.write_text("edited after the build\n", encoding="utf-8")

    assert generated_output_is_stale(root, output) is True


@pytest.mark.parametrize(
    ("relative", "initial", "changed"),
    [
        ("docs/manuscript/config.yaml", "paper:\n  version: 0.1.0\n", "paper:\n  version: 0.2.0\n"),
        ("docs/manuscript/preamble.md", "Older preamble.\n", "Newer preamble.\n"),
        ("docs/citation_workflow.md", "Old citation recipe.\n", "New citation recipe.\n"),
        ("uv.lock", 'version = 1\n[[package]]\nname = "pillow"\nversion = "13.0.0"\n', 'version = 1\n[[package]]\nname = "pillow"\nversion = "13.0.1"\n'),
    ],
)
def test_publication_input_edits_stale_outputs_without_mtime_changes(tmp_path: Path, relative: str, initial: str, changed: str) -> None:
    root, output = _fake_tree(tmp_path)
    source = root / relative
    source.parent.mkdir(parents=True, exist_ok=True)
    source.write_text(initial, encoding="utf-8")
    write_build_stamp(root, output)
    assert generated_output_is_stale(root, output) is False

    original_stat = source.stat()
    source.write_text(changed, encoding="utf-8")
    os.utime(source, ns=(original_stat.st_atime_ns, original_stat.st_mtime_ns))

    assert generated_output_is_stale(root, output) is True


@pytest.mark.parametrize("sentinel", [output_build_sentinels()[0], Path("data/source_citation_coverage.json")])
def test_missing_sentinel_is_stale_regardless_of_stamp(tmp_path: Path, sentinel: Path) -> None:
    root, output = _fake_tree(tmp_path)
    write_build_stamp(root, output)
    (output / sentinel).unlink()

    assert generated_output_is_stale(root, output) is True


def test_unstamped_tree_falls_back_to_mtimes(tmp_path: Path) -> None:
    root, output = _fake_tree(tmp_path)
    assert read_build_stamp(output) is None

    future = time.time() + 10_000
    for relative in source_freshness_roots():
        path = root / relative
        if path.is_file():
            os.utime(path, (future, future))

    # Legacy behaviour preserved: no stamp, source newer than output -> stale.
    assert generated_output_is_stale(root, output) is True


def test_read_build_stamp_tolerates_a_corrupt_stamp(tmp_path: Path) -> None:
    root, output = _fake_tree(tmp_path)
    write_build_stamp(root, output)
    (output / BUILD_STAMP_PATH).write_text("{not json", encoding="utf-8")

    # Unreadable stamps cannot provide a trusted content digest.
    assert read_build_stamp(output) is None


def test_read_build_stamp_rejects_a_non_mapping_stamp(tmp_path: Path) -> None:
    root, output = _fake_tree(tmp_path)
    write_build_stamp(root, output)
    (output / BUILD_STAMP_PATH).write_text("[1, 2, 3]", encoding="utf-8")

    assert read_build_stamp(output) is None


def test_current_generated_outputs_are_fresh_for_the_current_source() -> None:
    """The consumer must not accept stale or incomplete checked-in outputs."""
    assert generated_output_is_stale(PROJECT_ROOT, PROJECT_ROOT / "output") is False
