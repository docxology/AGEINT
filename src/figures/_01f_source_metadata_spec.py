"""Registry rows for source-metadata integrity visuals."""

from __future__ import annotations

SOURCE_METADATA_VISUALS: tuple[dict[str, str], ...] = (
    {
        "slug": "ageint-source-metadata-integrity",
        "title": "AGEINT Source Metadata Integrity",
        "caption": (
            "The source metadata integrity figure makes the anchor-lane hardening "
            "contract visible to reviewers. It separates curated intelligence anchors, "
            "source-quality support anchors, explicit lane and tier fields, refresh "
            "cadence evidence, and the artifact-evidence manifest so source rows cannot "
            "silently fall back to broad domain or source-type semantics while the "
            "rendered PDF still appears locally ready."
        ),
        "alt_text": (
            "Control matrix showing AGEINT source metadata coverage across intelligence "
            "anchors, source-quality support anchors, explicit source lanes, explicit "
            "source tiers, refresh cadence fields, and artifact-evidence failure checks."
        ),
        "renderer": "source_metadata_integrity",
        "source_section": "orientation.md",
    },
)


__all__ = ["SOURCE_METADATA_VISUALS"]
