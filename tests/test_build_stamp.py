"""Tests for content-addressed build freshness.

The point of the stamp is that freshness survives a git checkout, which does not
preserve mtimes. These tests therefore assert the digest ignores mtimes and that
staleness follows content, with the mtime heuristic kept only as the fallback for
un-stamped trees.
"""

from __future__ import annotations

import json
import os
import time
from pathlib import Path

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


def test_missing_sentinel_is_stale_regardless_of_stamp(tmp_path: Path) -> None:
    root, output = _fake_tree(tmp_path)
    write_build_stamp(root, output)
    (output / output_build_sentinels()[0]).unlink()

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


def test_write_build_stamp_records_the_current_digest(tmp_path: Path) -> None:
    root, output = _fake_tree(tmp_path)
    stamp_path = write_build_stamp(root, output)

    assert stamp_path == output / BUILD_STAMP_PATH
    payload = json.loads(stamp_path.read_text(encoding="utf-8"))
    assert payload["schema_version"] == 1
    assert payload["source_digest"] == source_content_digest(root)


def test_read_build_stamp_tolerates_a_corrupt_stamp(tmp_path: Path) -> None:
    root, output = _fake_tree(tmp_path)
    write_build_stamp(root, output)
    (output / BUILD_STAMP_PATH).write_text("{not json", encoding="utf-8")

    # Unreadable stamp must not crash the build; it degrades to the mtime path.
    assert read_build_stamp(output) is None
    assert generated_output_is_stale(root, output) in {True, False}


def test_read_build_stamp_rejects_a_non_mapping_stamp(tmp_path: Path) -> None:
    root, output = _fake_tree(tmp_path)
    write_build_stamp(root, output)
    (output / BUILD_STAMP_PATH).write_text("[1, 2, 3]", encoding="utf-8")

    assert read_build_stamp(output) is None


def test_committed_stamp_matches_committed_source() -> None:
    """Once output/ carries a stamp, it must match the committed source.

    This is the assertion CI ultimately needs: on a fresh clone, where mtimes
    carry no information, the committed tree still reports fresh because its
    stamp matches its source.

    It skips until the first stamped build is committed. Minting a stamp without
    a real rebuild would assert a correspondence that does not hold, and a strict
    rebuild needs chrome-headless-shell for the Mermaid figures (see
    src/figures/AGENTS.md) — without it the build writes placeholder PNGs over
    the published figures. Tracked as the adoption step in TODO.md.
    """
    stamp = read_build_stamp(PROJECT_ROOT / "output")
    if stamp is None:
        import pytest

        pytest.skip("committed output/ has no build stamp yet (see TODO.md Tier 0)")
    assert stamp["source_digest"] == source_content_digest(PROJECT_ROOT)
