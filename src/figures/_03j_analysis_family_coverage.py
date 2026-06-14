from __future__ import annotations

from pathlib import Path

from analysis_validation import analysis_validation_family_figure_rows

from ._01_part import FigureSpec
from ._03c_control_matrix import draw_control_matrix


def _render_analysis_validation_family_coverage(output: Path, spec: FigureSpec) -> None:
    draw_control_matrix(
        output,
        spec.title,
        analysis_validation_family_figure_rows(),
        ("Claim lane", "Evidence signal", "Failure signal"),
        "#fef9c3",
        "#dcfce7",
    )


__all__ = ["_render_analysis_validation_family_coverage"]
