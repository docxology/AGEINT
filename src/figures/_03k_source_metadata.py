from __future__ import annotations

from pathlib import Path

from source_metadata import source_metadata_figure_rows

from ._01_part import FigureSpec
from ._03c_control_matrix import draw_control_matrix


def _render_source_metadata_integrity(output: Path, spec: FigureSpec) -> None:
    project_root = output.resolve().parents[3]
    draw_control_matrix(
        output,
        spec.title,
        source_metadata_figure_rows(project_root),
        ("Surface", "Coverage", "Explicit Field", "Failure Signal"),
        "#ddd6fe",
        "#dcfce7",
    )


__all__ = ["_render_source_metadata_integrity"]
