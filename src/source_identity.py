"""Source-guide identity lock helpers for AGEINT references."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from _jsonl import read_jsonl as _read_jsonl

try:  # Support package imports and direct script imports.
    from .curriculum import load_curriculum, parse_curriculum_guide
except ImportError:  # pragma: no cover - exercised by tests/scripts using src on sys.path
    from curriculum import load_curriculum, parse_curriculum_guide  # type: ignore[no-redef]


LOCK_SCHEMA_VERSION = "1.0"


def _source_payload(source_path: Path) -> dict[str, Any]:
    from curriculum import resolve_curriculum_payload

    if source_path.exists():
        if source_path.suffix == ".json":
            return json.loads(source_path.read_text(encoding="utf-8"))
        if source_path.is_dir():
            return load_curriculum(source_path).payload
        return parse_curriculum_guide(source_path.read_text(encoding="utf-8"))
    return resolve_curriculum_payload(source_path)


def build_source_identity_lock(
    guide_path: Path,
    *,
    max_reference: int = 231,
) -> dict[str, Any]:
    """Build a stable identity lock for existing source-guide references."""
    payload = _source_payload(guide_path)
    locked_by_number: dict[int, dict[str, Any]] = {}
    for reference in payload["references"]:
        number = int(reference["number"])
        if number > max_reference or number in locked_by_number:
            continue
        locked_by_number[number] = {
            "number": number,
            "key": reference["key"],
            "title": reference["title"],
            "url": reference["url"],
        }
    locked = [locked_by_number[number] for number in sorted(locked_by_number)]
    return {
        "schema_version": LOCK_SCHEMA_VERSION,
        "source": guide_path.name,
        "max_reference": max_reference,
        "locked_reference_count": len(locked),
        "references": locked,
    }


def write_source_identity_lock_shards(lock: dict[str, Any], directory: Path) -> Path:
    """Write source identity lock shards under ``directory``."""
    directory.mkdir(parents=True, exist_ok=True)
    metadata = {key: lock[key] for key in ("schema_version", "source", "max_reference", "locked_reference_count")}
    (directory / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    lock_dir = directory / "lock"
    lock_dir.mkdir(exist_ok=True)
    references = lock["references"]
    for start in range(1, len(references) + 1, 75):
        end = min(start + 74, len(references))
        chunk = [entry for entry in references if start <= int(entry["number"]) <= end]
        text = "".join(json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n" for entry in chunk)
        (lock_dir / f"source-identity-{start:03d}-{end:03d}.jsonl").write_text(text, encoding="utf-8")
    return directory


def load_source_identity_lock(lock_path: Path) -> dict[str, Any]:
    """Load a source identity lock from JSON or sharded source-identity directory."""
    if lock_path.is_dir():
        metadata = json.loads((lock_path / "metadata.json").read_text(encoding="utf-8"))
        references = [
            row
            for path in sorted((lock_path / "lock").glob("*.jsonl"))
            for row in _read_jsonl(path)
        ]
        return {**metadata, "references": references}
    if lock_path.is_file():
        return json.loads(lock_path.read_text(encoding="utf-8"))
    if lock_path.name == "source_identity_lock.json":
        shard_dir = lock_path.parent / "source_identity"
        if shard_dir.is_dir():
            return load_source_identity_lock(shard_dir)
    raise FileNotFoundError(f"No source identity lock found: {lock_path}")


def source_identity_mismatches(
    guide_path: Path,
    lock_path: Path,
) -> list[str]:
    """Return human-readable mismatches between the current guide and lock."""
    lock = load_source_identity_lock(lock_path)
    current = build_source_identity_lock(
        guide_path,
        max_reference=int(lock["max_reference"]),
    )
    expected = {entry["number"]: entry for entry in lock["references"]}
    actual = {entry["number"]: entry for entry in current["references"]}
    mismatches: list[str] = []
    for number, expected_entry in expected.items():
        actual_entry = actual.get(number)
        if actual_entry is None:
            mismatches.append(f"missing ageint{number:03d}")
            continue
        for field in ("key", "title", "url"):
            if actual_entry[field] != expected_entry[field]:
                mismatches.append(
                    f"ageint{number:03d} {field}: "
                    f"{actual_entry[field]!r} != {expected_entry[field]!r}"
                )
    return mismatches
