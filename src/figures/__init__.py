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
from ._03l_cover_art import COVER_OUTPUT_PATH, render_cover_art
from ._03q_frontmatter_transit import FRONTMATTER_OUTPUT_PATH, render_evidence_transit_map

__all__ = [
    "FigureKind",
    "FigureSpec",
    "COVER_OUTPUT_PATH",
    "FRONTMATTER_OUTPUT_PATH",
    "build_figure_specs",
    "render_figures",
    "render_cover_art",
    "render_evidence_transit_map",
    "load_figure_registry",
    "figures_for_section",
    "figure_markdown",
]
