from __future__ import annotations

from pathlib import Path

from ._01_part import FigureSpec
from ._03c_control_matrix import draw_control_matrix


def _render_scholarship_triangulation_map(output: Path, spec: FigureSpec) -> None:
    rows = [
        ("Claim-bearing sections", ("overview", "topic lessons", "worked practice", "assessment review")),
        ("Citation presence", ("Pandoc keys", "source counts", "uncited gate", "inventory rows")),
        ("Source families", ("source guide", "official / standards", "scholarly", "law / policy")),
        ("Thin support", ("unique keys", "two-key floor", "hard fail", "negative control")),
        ("Triangulation review", ("single-family warning", "anchor metadata", "claim scope", "refresh duty")),
        ("Evidence output", ("JSON report", "Markdown report", "artifact manifest", "release blocker")),
    ]
    draw_control_matrix(
        output,
        spec.title,
        rows,
        ("Section", "Citation Signal", "Verifier", "Disposition"),
        "#c7d2fe",
        "#fef3c7",
    )


__all__ = ["_render_scholarship_triangulation_map"]
