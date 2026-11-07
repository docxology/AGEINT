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


def test_recompute_source_counts_counts_only_authored_nonblank_notes(tmp_path: Path) -> None:
    chapters = tmp_path / "parts" / "one" / "chapters"
    split = chapters / "split"
    split.mkdir(parents=True)
    (chapters.parent / "part.json").write_text('{"number": 1}', encoding="utf-8")
    (chapters / "flat.json").write_text(json.dumps({"sections": [{"teaching_note": "one"}, {"teaching_note": " \n "}, {"teaching_note": None}]}), encoding="utf-8")
    (split / "chapter.json").write_text('{"sections": [{"teaching_note": "ignored inline residue"}]}', encoding="utf-8")
    rows = [{"teaching_note": "two"}, {"teaching_note": 3}, {"teaching_note": ""}, {"teaching_note": "three"}]
    sections = split / "sections.jsonl"
    sections.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
    (tmp_path / "patterns.json").write_text("[]", encoding="utf-8")
    (tmp_path / "stats.json").write_text('{"authored_teaching_note_count": 999}', encoding="utf-8")

    expected = {"parts": 1, "chapters": 2, "appendices": 0, "patterns": 0, "references": 0, "authored_teaching_note_count": 3}
    assert recompute_source_counts(tmp_path) == expected
    rows[0]["teaching_note"] = "\t "
    sections.write_text("\n".join(json.dumps(row) for row in rows) + "\n", encoding="utf-8")
    assert recompute_source_counts(tmp_path) == {**expected, "authored_teaching_note_count": 2}


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
    recomputed = {"parts": 16, "chapters": 51, "appendices": 9, "patterns": 20, "references": 312, "authored_teaching_note_count": 564}
    published = {"parts": 15, "chapters": 51, "appendices": "9", "patterns": 20, "references": 311, "authored_teaching_note_count": 563}
    mismatches = compare_counts(recomputed, published, figure_count_recomputed=177, figure_count_published=176)
    assert any("parts" in row for row in mismatches)
    assert any("references" in row for row in mismatches)
    assert any("appendices" in row and "non-integer" in row for row in mismatches)
    assert any("figures" in row for row in mismatches)
    assert any("authored_teaching_note_count" in row for row in mismatches)


@pytest.mark.parametrize("invalid_count", [True, False, 1.0, "1", None])
def test_compare_counts_rejects_noninteger_published_note_counts(invalid_count: object) -> None:
    recomputed = {"parts": 1, "chapters": 1, "appendices": 1, "patterns": 1, "references": 1, "authored_teaching_note_count": 1}
    published = {**recomputed, "authored_teaching_note_count": invalid_count}
    mismatches = compare_counts(recomputed, published, figure_count_recomputed=1, figure_count_published=1)
    assert len(mismatches) == 1
    assert "authored_teaching_note_count" in mismatches[0] and "non-integer" in mismatches[0]


def test_verify_published_counts_raises_on_drift(tmp_path: Path) -> None:
    recomputed = recompute_source_counts(PROJECT_ROOT / "data" / "curriculum")
    drifted = dict(recomputed)
    drifted["chapters"] += 1
    with pytest.raises(ValueError, match="chapters"):
        verify_published_counts(PROJECT_ROOT, curriculum_stats=drifted)
    with pytest.raises(ValueError, match="figures"):
        verify_published_counts(PROJECT_ROOT, curriculum_stats=recomputed, figure_count=recomputed["parts"])
