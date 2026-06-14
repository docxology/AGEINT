from __future__ import annotations

from pathlib import Path

from ._01_part import FigureSpec
from ._03c_control_matrix import draw_control_matrix


def _render_artifact_evidence_control_loop(output: Path, spec: FigureSpec) -> None:
    rows = [
        ("Source inputs", ("curriculum shards", "templates and src", "source freshness", "negative control")),
        ("Manuscript", ("semantic files", "section labels", "reference audit", "stale scan")),
        ("Citation spine", ("source sections", "Pandoc keys", "zero uncovered", "inventory JSON")),
        ("Figure registry", ("PNG metadata", "reader text", "quality audit", "source binding")),
        ("Rendered PDF", ("page count", "URI links", "no file actions", "stale check")),
        ("Evidence report", ("single manifest", "current counts", "validator status", "release blocker")),
    ]
    draw_control_matrix(
        output,
        spec.title,
        rows,
        ("Artifact", "Evidence", "Verifier", "Failure signal"),
        "#bae6fd",
        "#dcfce7",
    )


__all__ = ["_render_artifact_evidence_control_loop"]
