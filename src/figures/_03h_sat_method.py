from __future__ import annotations

from pathlib import Path

from ._01_part import FigureSpec
from ._03c_control_matrix import draw_control_matrix


def _render_synthetic_tradecraft_method_contract(output: Path, spec: FigureSpec) -> None:
    rows = [
        ("Source-family triangulation", ("source guide", "official / standards", "scholarly", "claim fit")),
        ("Synthetic fixture", ("toy records", "declassified context", "owned-lab logs", "no live target")),
        ("Analytic fields", ("observation", "inference", "confidence", "dissent")),
        ("Negative control", ("stale output", "thin support", "broken link", "false pass")),
        ("Reviewer challenge", ("assumption check", "alternative hypothesis", "rights boundary", "refresh duty")),
        ("Evidence artifact", ("JSON report", "PDF audit", "figure registry", "release blocker")),
    ]
    draw_control_matrix(
        output,
        spec.title,
        rows,
        ("Method stage", "Input", "Tradecraft control", "Verifier"),
        "#dbeafe",
        "#f0fdf4",
    )


__all__ = ["_render_synthetic_tradecraft_method_contract"]
