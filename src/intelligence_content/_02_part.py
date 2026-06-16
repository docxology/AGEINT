from __future__ import annotations

from pathlib import Path
from typing import Final

from _jsonl import read_jsonl

from ._01_part import ResearchAnchor


def _project_root() -> Path:
    return Path(__file__).resolve().parents[2]


def _load_intelligence_research_anchors() -> tuple[ResearchAnchor, ...]:
    data_dir = _project_root() / "data" / "research_anchors"
    rows: list[dict] = []
    for path in sorted(data_dir.glob("intelligence-anchors-*.jsonl")):
        rows.extend(read_jsonl(path))
    return tuple(ResearchAnchor(**row) for row in rows)


INTELLIGENCE_RESEARCH_ANCHORS: Final[tuple[ResearchAnchor, ...]] = _load_intelligence_research_anchors()
