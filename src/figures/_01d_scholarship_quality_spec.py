"""Registry rows for scholarship-quality audit visuals."""

from __future__ import annotations

SCHOLARSHIP_QUALITY_VISUALS: tuple[dict[str, str], ...] = (
    {
        "slug": "ageint-scholarship-triangulation-map",
        "title": "AGEINT Scholarship Triangulation Map",
        "caption": (
            "The scholarship triangulation map shows how generated AGEINT sections move "
            "from citation presence through source-family classification, thin-support "
            "gates, single-family review warnings, and current artifact-evidence reports."
        ),
        "alt_text": (
            "Control matrix linking claim-bearing generated sections, source-guide "
            "citations, official and standards anchors, scholarly anchors, and hard-fail "
            "or review-warning verifier outcomes."
        ),
        "renderer": "scholarship_triangulation_map",
        "source_section": "orientation.md",
    },
)


__all__ = ["SCHOLARSHIP_QUALITY_VISUALS"]
