"""Verification gate: published counts must match a fresh source re-count."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from published_counts_gate import compare_counts, recompute_figure_count, recompute_source_counts, verify_published_counts

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_recompute_source_counts_matches_published_stats() -> None:
    """Re-counting data/curriculum shards yields the published stats."""

    recomputed = recompute_source_counts(PROJECT_ROOT / "data" / "curriculum")
    outline = json.loads((PROJECT_ROOT / "output" / "data" / "curriculum_outline.json").read_text(encoding="utf-8"))
    assert recomputed == outline["stats"]


def test_recompute_figure_count_matches_registry_self_count() -> None:
    registry_path = PROJECT_ROOT / "output" / "figures" / "figure_registry.json"
    count = recompute_figure_count(registry_path)
    payload = json.loads(registry_path.read_text(encoding="utf-8"))
    assert count == len(payload["figures"])
    assert count == payload["figure_count"]


def test_verify_published_counts_passes_on_real_repo_data() -> None:
    report = verify_published_counts(PROJECT_ROOT, figure_count=recompute_figure_count(PROJECT_ROOT / "output" / "figures" / "figure_registry.json"))
    assert report["figures"] == report["published_stats"].get("figures", report["figures"])
    assert report["recomputed"]["references"] > 0


def test_verify_published_counts_accepts_build_time_stats() -> None:
    recomputed = recompute_source_counts(PROJECT_ROOT / "data" / "curriculum")
    report = verify_published_counts(PROJECT_ROOT, curriculum_stats=recomputed)
    assert report["recomputed"] == recomputed


def test_compare_counts_flags_every_drift_axis() -> None:
    recomputed = {"parts": 16, "chapters": 51, "appendices": 9, "patterns": 20, "references": 312}
    published = {"parts": 15, "chapters": 51, "appendices": "9", "patterns": 20, "references": 311}
    mismatches = compare_counts(recomputed, published, figure_count_recomputed=177, figure_count_published=176)
    assert any("parts" in row for row in mismatches)
    assert any("references" in row for row in mismatches)
    assert any("appendices" in row and "non-integer" in row for row in mismatches)
    assert any("figures" in row for row in mismatches)


def test_verify_published_counts_raises_on_drift(tmp_path: Path) -> None:
    recomputed = recompute_source_counts(PROJECT_ROOT / "data" / "curriculum")
    drifted = dict(recomputed)
    drifted["chapters"] += 1
    with pytest.raises(ValueError, match="chapters"):
        verify_published_counts(PROJECT_ROOT, curriculum_stats=drifted)
    with pytest.raises(ValueError, match="figures"):
        verify_published_counts(PROJECT_ROOT, curriculum_stats=recomputed, figure_count=recomputed["parts"])
