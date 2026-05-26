"""Tests for AGEINT source-guide identity lock stability."""

from __future__ import annotations

from pathlib import Path
import json

from curriculum import load_curriculum
from source_identity import build_source_identity_lock, source_identity_mismatches

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE = PROJECT_ROOT / "SIST-Guide-TOC-and-Bibliography-v2.md"
LOCK = PROJECT_ROOT / "data" / "source_identity"


def test_locked_source_identities_remain_stable_for_existing_range() -> None:
    lock = build_source_identity_lock(SOURCE, max_reference=231)

    assert LOCK.is_dir()
    assert lock["locked_reference_count"] == 231
    assert lock["references"][0]["key"] == "ageint001"
    assert lock["references"][-1]["key"] == "ageint231"
    assert source_identity_mismatches(SOURCE, LOCK) == []


def test_v2_references_are_append_only_after_locked_range() -> None:
    lock = build_source_identity_lock(SOURCE, max_reference=312)
    keys = [entry["key"] for entry in lock["references"]]

    assert keys[:231] == [f"ageint{number:03d}" for number in range(1, 232)]
    assert keys[231] == "ageint232"
    assert keys[-1] == "ageint312"


def test_locked_source_identity_detects_mutated_title_or_url(tmp_path: Path) -> None:
    payload = load_curriculum(PROJECT_ROOT / "data" / "curriculum").payload
    source = tmp_path / "curriculum_outline.json"
    lock_path = tmp_path / "source_identity_lock.json"
    source.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lock = build_source_identity_lock(source, max_reference=231)
    lock_path.write_text(json.dumps(lock, indent=2), encoding="utf-8")

    payload["references"][0]["title"] = "Mutated Reference Title"
    payload["references"][1]["url"] = "https://example.com/mutated"
    source.write_text(json.dumps(payload, indent=2), encoding="utf-8")

    mismatches = source_identity_mismatches(source, lock_path)
    assert any("ageint001 title" in mismatch for mismatch in mismatches)
    assert any("ageint002 url" in mismatch for mismatch in mismatches)
