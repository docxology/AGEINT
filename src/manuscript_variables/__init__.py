"""AGEINT manuscript_variables package."""

from __future__ import annotations

from _package_loader import merge_part_modules

_PARTS = ["_01_part", "_02_part"]
merge_part_modules(__name__, _PARTS)

from ._01_part import (  # noqa: E402
    SOURCE_QUALITY_ANCHORS,
    appendix_rows,
    citation_spine,
    generate_variables,
    reference_bibtex_files,
)
from ._02_part import save_variables, write_bibtex_files  # noqa: E402

__all__ = [
    "SOURCE_QUALITY_ANCHORS",
    "appendix_rows",
    "citation_spine",
    "generate_variables",
    "save_variables",
    "reference_bibtex_files",
    "write_bibtex_files",
]
