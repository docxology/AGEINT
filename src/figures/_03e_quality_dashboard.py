from __future__ import annotations

from pathlib import Path

from ._01_part import FigureSpec
from ._03c_control_matrix import draw_control_matrix


def _render_visual_quality_audit_dashboard(output: Path, spec: FigureSpec) -> None:
    rows = [
        ("Readable PNG", ("signature", "Pillow opens", "width and height", "asset audit")),
        ("Stable layout", ("square canvas", "ratio <= 1.1", "normalized PNG", "layout audit")),
        ("Reader text", ("caption", "short alt text", "long description", "word gates")),
        ("Metadata parity", ("PNG chunks", "registry values", "provenance JSON", "metadata audit")),
        ("Source binding", ("source section", "section label", "figure label", "crossref audit")),
        ("Color safety", ("not color alone", "contrast cues", "visible labels", "visual inspection")),
        ("Rendered links", ("PDF and web", "no .md targets", "no file URIs", "annotation scan")),
    ]
    draw_control_matrix(
        output,
        spec.title,
        rows,
        ("Gate", "Reader value", "Artifact field", "Verifier"),
        "#c7d2fe",
        "#fef3c7",
    )


__all__ = ["_render_visual_quality_audit_dashboard"]
