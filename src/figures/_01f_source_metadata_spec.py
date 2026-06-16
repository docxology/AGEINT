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
            "cadence evidence, denominator context, reviewer action, and the artifact-"
            "evidence manifest failure path so source rows cannot silently fall back to "
            "broad domain or source-type semantics while the rendered PDF still appears "
            "locally ready. Read it as local metadata telemetry, not a quality score for "
            "the cited sources."
        ),
        "alt_text": (
            "Dashboard showing AGEINT source metadata coverage across the local anchor "
            "denominator, explicit source lanes and tiers, refresh cadence fields, "
            "reviewer action cues, and fail-closed artifact-evidence checks."
        ),
        "renderer": "source_metadata_integrity",
        "source_section": "orientation.md",
    },
    {
        "slug": "ageint-source-refresh-due-dashboard",
        "title": "AGEINT Source Refresh Due-Date Dashboard",
        "caption": (
            "The source refresh due-date dashboard turns checked_as_of dates and "
            "refresh cadence metadata into a release-readiness control. It separates "
            "the 472-row local source denominator, current anchors, due-soon rows, due "
            "or stale rows, cadence coverage, missing metadata, reviewer refresh "
            "actions, and the publication-preflight failure path so source dates cannot "
            "silently age past their review window while citation, link, figure, and "
            "PDF validators remain green. The visual is not a score or empirical "
            "performance claim."
        ),
        "alt_text": (
            "Dashboard showing AGEINT source anchors by refresh status, cadence "
            "coverage, missing checked dates, unknown cadences, the local row "
            "denominator, reviewer action cues, and the release preflight gate that "
            "fails due or stale rows."
        ),
        "renderer": "source_refresh_due_dashboard",
        "source_section": "bibliography-atlas.md",
    },
    {
        "slug": "ageint-agency-source-coverage",
        "title": "AGEINT Agency-Source Coverage and Pack Routing",
        "caption": (
            "The agency-source coverage figure summarizes the official US Intelligence "
            "Community source expansion as agency-source coverage telemetry, not an "
            "endorsement or source-quality score. It shows the 56-anchor denominator "
            "for the new official US IC tranche, the CIA, DIA, ODNI, Intelligence.gov, "
            "NSA, NGA, FBI, and NRO agency distribution, deterministic source-pack "
            "routing into profiles, reviewer routing actions, and the artifact-evidence "
            "failure path that blocks a new agency anchor when source_agency, source_pack, "
            "source_lane, source_tier, checked_as_of, claim_scope, assurance_use, or "
            "rights_dimension metadata is missing."
        ),
        "alt_text": (
            "Agency-source coverage dashboard for AGEINT showing the new official US "
            "Intelligence Community anchors, agency distribution, source-pack routing, "
            "metadata completeness, profile routing, reviewer action cues, denominator "
            "context, and the agency_source_coverage_ok gate used by artifact evidence "
            "and publication readiness."
        ),
        "renderer": "agency_source_coverage_dashboard",
        "source_section": "bibliography-atlas.md",
    },
)


__all__ = ["SOURCE_METADATA_VISUALS"]
