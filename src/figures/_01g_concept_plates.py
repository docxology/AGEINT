"""Data-backed deterministic concept-plate specs."""

from __future__ import annotations

import json
from pathlib import Path

_CONCEPT_PLATES_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "figures" / "concept_plates.jsonl"
)


def _load_concept_plates() -> tuple[dict[str, str], ...]:
    if not _CONCEPT_PLATES_PATH.is_file():
        return ()
    rows: list[dict[str, str]] = []
    for line in _CONCEPT_PLATES_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(dict(json.loads(line)))
    return tuple(rows)


AI_CONCEPTUAL_PLATES: tuple[dict[str, str], ...] = _load_concept_plates()
