"""AGEINT manuscript_variables package."""

from __future__ import annotations

from ._01_part import (
    SOURCE_QUALITY_ANCHORS,
    appendix_rows,
    citation_spine,
)
from ._02_part import generate_variables, reference_bibtex_files, save_variables, write_bibtex_files

__all__ = [
    "SOURCE_QUALITY_ANCHORS",
    "appendix_rows",
    "citation_spine",
    "generate_variables",
    "save_variables",
    "reference_bibtex_files",
    "write_bibtex_files",
]
