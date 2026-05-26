"""AGEINT figures package."""

from __future__ import annotations

from _package_loader import merge_part_modules

_PARTS = ["_01_part", "_03_part", "_02b_mermaid", "_02_part", "_04_part"]
merge_part_modules(__name__, _PARTS)

from ._01_part import (  # noqa: E402
    FigureKind,
    FigureSpec,
    build_figure_specs,
    figure_markdown,
    figures_for_section,
    load_figure_registry,
    render_figures,
)

__all__ = [
    "FigureKind",
    "FigureSpec",
    "build_figure_specs",
    "render_figures",
    "load_figure_registry",
    "figures_for_section",
    "figure_markdown",
]
