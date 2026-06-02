"""AGEINT figures package."""

from __future__ import annotations

from ._01_part import FigureKind, FigureSpec
from ._02_part import (
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
