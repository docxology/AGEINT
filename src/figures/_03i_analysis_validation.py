from __future__ import annotations

from pathlib import Path

from analysis_validation import analysis_validation_matrix_rows

from ._01_part import FigureSpec
from ._03c_control_matrix import draw_control_matrix


def _render_analysis_validation_matrix(output: Path, spec: FigureSpec) -> None:
    draw_control_matrix(
        output,
        spec.title,
        analysis_validation_matrix_rows(),
        ("Claim class", "Evidence packet", "Validation question", "Failure condition"),
        "#e0f2fe",
        "#fee2e2",
    )


__all__ = ["_render_analysis_validation_matrix"]
