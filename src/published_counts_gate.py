"""Build-time verification gate for published AGEINT counts.

Recomputes the parts/chapters/appendices/patterns/references counts directly
from the sharded source data under ``data/curriculum/`` and the figure count
from the figure registry, then compares them to the stats published in the
build mirror artifact ``output/data/curriculum_outline.json`` (or to the
counts carried by the same build). Any disagreement raises ``ValueError`` so
the build fails on drift instead of shipping stale published numbers.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from _jsonl import read_jsonl

CURRICULUM_COUNT_KEYS = ("parts", "chapters", "appendices", "patterns", "references")


def recompute_source_counts(source_dir: Path) -> dict[str, int]:
    """Re-count curriculum units directly from the sharded source directory.

    Independent of :mod:`_curriculum_shards` loading and of any stats file so
    the gate measures the raw files rather than trusting previously written
    numbers.
    """

    parts_dir = source_dir / "parts"
    parts: list[Path] = sorted(parts_dir.glob("*/part.json"))
    chapters = 0
    for part_path in parts:
        chapters_dir = part_path.parent / "chapters"
        if chapters_dir.is_dir():
            chapters += sum(
                1
                for path in chapters_dir.iterdir()
                if (path.is_dir() and (path / "chapter.json").is_file())
                or (path.is_file() and path.suffix == ".json")
            )
    appendices = len(sorted((source_dir / "appendices").glob("*.json")))
    patterns = len(json.loads((source_dir / "patterns.json").read_text(encoding="utf-8")))
    reference_keys: set[str] = set()
    for path in sorted((source_dir / "references").glob("*.jsonl")):
        for row in read_jsonl(path):
            key = str(row.get("key") or "")
            if key:
                reference_keys.add(key)
    return {
        "parts": len(parts),
        "chapters": chapters,
        "appendices": appendices,
        "patterns": patterns,
        "references": len(reference_keys),
    }


def recompute_figure_count(figure_registry_path: Path) -> int:
    """Count registered figures and self-check the registry's own count field."""

    payload = json.loads(figure_registry_path.read_text(encoding="utf-8"))
    figures = payload.get("figures")
    if not isinstance(figures, list):
        raise ValueError(f"figure_registry.json has no figures list: {figure_registry_path}")
    declared = payload.get("figure_count")
    if isinstance(declared, int) and declared != len(figures):
        raise ValueError(
            f"Figure registry self-count drift: figures={len(figures)} figure_count={declared}"
        )
    return len(figures)


def compare_counts(
    recomputed: dict[str, int],
    published: dict[str, Any],
    *,
    figure_count_recomputed: int,
    figure_count_published: Any,
) -> list[str]:
    """Return human-readable drift descriptions between recomputed and published counts."""

    mismatches: list[str] = []
    for key in CURRICULUM_COUNT_KEYS:
        published_value = published.get(key)
        if not isinstance(published_value, int):
            mismatches.append(f"{key}: published stats missing/non-integer ({published_value!r})")
            continue
        if recomputed[key] != published_value:
            mismatches.append(f"{key}: recomputed {recomputed[key]} != published {published_value}")
    if figure_count_published is not None and figure_count_recomputed != figure_count_published:
        mismatches.append(
            f"figures: recomputed {figure_count_recomputed} != published {figure_count_published}"
        )
    return mismatches


def verify_published_counts(
    project_root: Path,
    *,
    curriculum_stats: dict[str, Any] | None = None,
    figure_count: int | None = None,
    figure_registry_path: Path | None = None,
    outline_path: Path | None = None,
    source_dir: Path | None = None,
) -> dict[str, Any]:
    """Verify published counts against counts recomputed from source data.

    Compares the stats in ``output/data/curriculum_outline.json`` (or
    ``curriculum_stats`` from the same build) to a fresh re-count of the
    sharded source data, and compares the figure registry's figure count
    (or ``figure_count`` from the same build) to the registry itself.
    Raises ``ValueError`` listing every mismatch; returns a report dict on
    success.
    """

    root = Path(project_root)
    source = source_dir or root / "data" / "curriculum"
    outline = outline_path or root / "output" / "data" / "curriculum_outline.json"
    if not outline.is_file():
        raise FileNotFoundError(f"Published outline stats not found: {outline}")

    recomputed = recompute_source_counts(source)
    published_stats = (
        dict(curriculum_stats)
        if curriculum_stats is not None
        else json.loads(outline.read_text(encoding="utf-8")).get("stats")
    )
    if not isinstance(published_stats, dict):
        raise ValueError(f"Outline stats missing in {outline}")

    registry = figure_registry_path or root / "output" / "figures" / "figure_registry.json"
    if not registry.is_file():
        raise FileNotFoundError(f"Figure registry not found: {registry}")
    recomputed_figures = recompute_figure_count(registry)
    published_figures = figure_count

    mismatches = compare_counts(
        recomputed,
        published_stats,
        figure_count_recomputed=recomputed_figures,
        figure_count_published=published_figures,
    )
    if mismatches:
        raise ValueError(
            "Published count verification failed: "
            + "; ".join(mismatches)
        )
    return {
        "recomputed": recomputed,
        "published_stats": published_stats,
        "figures": recomputed_figures,
        "outline": outline,
        "registry": registry,
    }
