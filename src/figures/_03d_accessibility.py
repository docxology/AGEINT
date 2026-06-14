from __future__ import annotations

from pathlib import Path

from ._01_part import FigureSpec
from ._03c_control_matrix import draw_control_matrix


def _render_visual_accessibility_contract(output: Path, spec: FigureSpec) -> None:
    rows = [
        ("Short alt text", ("identify type", "purpose in context", "alt_text", "24-word gate")),
        (
            "Long description",
            ("equivalent content", "relationships and limits", "long_description", "70-word gate"),
        ),
        ("Caption", ("reader task", "source and boundary", "caption", "40-word gate")),
        ("Color-safe labels", ("not color alone", "contrast and symbols", "visible text", "PNG readability")),
        ("Provenance", ("official guidance", "source section", "registry row", "hash and path")),
        ("PNG metadata", ("portable evidence", "alt/caption carried", "text chunks", "Pillow audit")),
        ("Rendered audit", ("PDF and web", "no Markdown targets", "validators", "link scan")),
    ]
    draw_control_matrix(
        output,
        spec.title,
        rows,
        ("Guidance", "Reader value", "Registry field", "Verifier"),
        "#bfdbfe",
        "#dcfce7",
    )


__all__ = ["_render_visual_accessibility_contract"]
