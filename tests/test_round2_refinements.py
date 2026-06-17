"""Round-2 refinement regressions.

Guards the round-2 changes: the shared Markdown table-cell module, the flowchart
visual-type announcement fix, appendix column de-duplication, and the
mid-chapter wayfinding back-links.
"""

from __future__ import annotations

from pathlib import Path

from figures import load_figure_registry
from manuscript_variables._01_part import _blocked_appendix_source_label
from markdown_cell import escape_table_cell, plain_table_cell

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = PROJECT_ROOT / "output" / "manuscript"


def test_table_cell_policies_are_distinct_and_correct() -> None:
    # escape policy: keep the pipe (backslash-escaped), collapse only newlines.
    assert escape_table_cell("a | b\nc") == "a \\| b c"
    assert escape_table_cell("  x  ") == "x"
    # plain policy: collapse all whitespace, replace the pipe with a slash.
    assert plain_table_cell("a | b\nc\t d") == "a / b c d"
    assert plain_table_cell("  x  ") == "x"


def test_appendix_blocked_label_does_not_duplicate_safe_treatment() -> None:
    # No transform needed -> the blocked-motif cell must NOT reprint the title.
    same = _blocked_appendix_source_label("E.1 AES Overview", "E.1 AES Overview")
    assert same != "E.1 AES Overview"
    assert "verbatim" in same
    # A real transform still names the retained source id for audit.
    transformed = _blocked_appendix_source_label(
        "E.2 raw operational title", "E.2 safe treatment"
    )
    assert "E.2" in transformed


def test_module_map_figures_announced_as_process_flow_not_matrix() -> None:
    registry = load_figure_registry(PROJECT_ROOT / "output/figures/figure_registry.json")
    module_maps = [
        fig
        for fig in registry["figures"]
        if fig["label"].startswith("fig:part-") and fig["label"].endswith("-module-map")
    ]
    assert module_maps, "expected part module-map figures in the registry"
    for fig in module_maps:
        # Flowcharts must not be announced to screen readers as matrices.
        assert "matrix-style figure" not in fig["long_description"], fig["label"]
        assert "process-flow figure" in fig["long_description"], fig["label"]


def test_mid_chapter_fragments_link_back_to_orientation() -> None:
    fragments = sorted(MANUSCRIPT.glob("parts/*/*/02-evidence-contract*.md")) + sorted(
        MANUSCRIPT.glob("parts/*/*/03-governance-boundary*.md")
    )
    assert fragments, "expected evidence-contract and governance-boundary fragments"
    for path in fragments:
        text = path.read_text(encoding="utf-8")
        assert "sec:curriculum_orientation" in text, path.as_posix()
