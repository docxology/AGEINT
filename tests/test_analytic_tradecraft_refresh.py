"""Regression checks for the analytic-tradecraft source refresh."""

from __future__ import annotations

from pathlib import Path
import re

from manuscript_quality.inventory_helpers import manuscript_dir


def test_analytic_tradecraft_chapters_keep_sat_and_probability_boundaries(
    built_output: Path,
) -> None:
    output_manuscript = manuscript_dir(built_output)
    tradecraft_root = (
        output_manuscript / "parts" / "epistemic-rigor-and-analytic-tradecraft"
    )
    chapter_text_blob = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(tradecraft_root.glob("*/*.md"))
    )
    lower = chapter_text_blob.lower()

    assert "likelihood" in lower
    assert "confidence" in lower
    assert "icd 203" in lower
    assert "structured analytic technique" in lower
    assert "evidence" in lower
    assert "caveat" in lower or "limit" in lower
    assert not re.search(
        r"\bsats?\s+(?:generally\s+|always\s+|reliably\s+|proven\s+to\s+)?"
        r"(?:reduce|eliminate|cure)\s+bias\b",
        lower,
    )


def test_analytic_tradecraft_primary_support_demotes_weak_guide_rows(
    built_output: Path,
) -> None:
    tradecraft_root = (
        manuscript_dir(built_output)
        / "parts"
        / "epistemic-rigor-and-analytic-tradecraft"
    )
    lesson_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(tradecraft_root.glob("*/01-practice-studio.md"))
    )
    assert "curated analytic-tradecraft anchors" in lesson_text
    assert "remain context only" in lesson_text
    for weak_marker in (
        "SpecialEurasia article",
        "Wikipedia biography",
        "hosted on Scribd",
        "Spotter Up",
        "Army University Press",
    ):
        assert weak_marker not in lesson_text


def test_analytic_tradecraft_overviews_surface_new_boundary_figures(
    built_output: Path,
) -> None:
    tradecraft_root = (
        manuscript_dir(built_output)
        / "parts"
        / "epistemic-rigor-and-analytic-tradecraft"
    )
    overview_text = "\n".join(
        path.read_text(encoding="utf-8")
        for path in sorted(tradecraft_root.glob("*/00-overview.md"))
    )
    for label in (
        "fig:ageint-analytic-source-quality-boundary",
        "fig:ageint-first-principles-tradecraft-decomposition",
        "fig:ageint-redteam-tradecraft-negative-control-loop",
    ):
        assert label in overview_text
