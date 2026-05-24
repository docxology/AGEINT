"""AGEINT manuscript_manifest package."""

from __future__ import annotations

from _package_loader import merge_part_modules

_PARTS = ["_01_part", "_02_part", "_03_part", "_04_part", "_05_part"]
merge_part_modules(__name__, _PARTS)

from ._04_part import build_manuscript_manifest  # noqa: E402
from ._01_part import ManuscriptManifest, ManuscriptSection  # noqa: E402
from ._05_part import render_manuscript  # noqa: E402

__all__ = [
    "ManuscriptManifest",
    "ManuscriptSection",
    "build_manuscript_manifest",
    "render_manuscript",
]
