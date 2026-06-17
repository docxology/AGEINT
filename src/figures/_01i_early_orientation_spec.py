from __future__ import annotations

EARLY_ORIENTATION_VISUALS: tuple[dict[str, str], ...] = (
    {
        "slug": "ageint-reader-route-compass",
        "title": "AGEINT Reader Route Compass",
        "caption": (
            "Opening navigation compass for the AGEINT orientation. It separates the "
            "instructor, learner, assurance reviewer, and maintainer routes and pairs "
            "each with the evidence trace that should survive the next reading move, so "
            "a reader can choose a path and know what to carry into the following "
            "section. It is navigation support, not a learning-outcome or performance "
            "claim."
        ),
        "alt_text": (
            "Compass-style map of AGEINT reader paths for instructor, learner, "
            "reviewer, and maintainer, with retained evidence attached to each route."
        ),
        "renderer": "reader_route_compass",
        "source_section": "orientation.md",
        "canvas_size": "2400",
        "orientation_slot": "opening_route_compass",
        "semantic_role": "reader_navigation_map",
        "evidence_role": "orientation route selection, reader task framing, and evidence handoff support",
    },
    {
        "slug": "ageint-synthetic-tradecraft-workbench",
        "title": "AGEINT Synthetic Tradecraft Workbench",
        "caption": (
            "Workbench-style assembly line for Synthetic Analytic Tradecraft. It shows "
            "how a synthetic fixture becomes a source description, an analytic field "
            "set, a bounded claim packet, and a reviewer-gate disposition, tracing the "
            "path a classroom exercise takes from raw material to a record another "
            "analyst can challenge. It is a classroom artifact route, not an autonomous "
            "action claim or field-capability proof."
        ),
        "alt_text": (
            "Assembly-line diagram moving from synthetic fixture to source "
            "description, analytic fields, claim packet, and reviewer gate."
        ),
        "renderer": "synthetic_tradecraft_workbench",
        "source_section": "orientation.md",
        "canvas_size": "2400",
        "orientation_slot": "tradecraft_workbench",
        "semantic_role": "synthetic_method_workbench",
        "evidence_role": "synthetic-fixture framing, claim-packet assembly, and reviewer-gate explanation",
    },
    {
        "slug": "ageint-source-constellation-map",
        "title": "AGEINT Source Constellation Map",
        "caption": (
            "Source-family constellation for early orientation. It places the official, "
            "standards, scholarly, public, and professional evidence families around the "
            "AGEINT source spine so a reader can route governance, technical, historical, "
            "evaluation, and assurance claims to the lane whose evidence actually "
            "supports them. Route density shows coverage, not a ranking of source "
            "quality or evidence strength."
        ),
        "alt_text": (
            "Constellation map of AGEINT source families and evidence lanes "
            "surrounding the central source spine."
        ),
        "renderer": "source_constellation_map",
        "source_section": "orientation.md",
        "canvas_size": "2400",
        "orientation_slot": "source_constellation",
        "semantic_role": "source_family_constellation",
        "evidence_role": "source-family orientation, lane selection, and claim-class routing support",
    },
    {
        "slug": "ageint-assurance-cockpit",
        "title": "AGEINT Assurance Cockpit",
        "caption": (
            "Audit-tile orientation cockpit for local readiness. It groups build "
            "freshness, reference quality, source metadata, refresh posture, figure "
            "quality, and the publication-readiness boundary into reader-facing tiles "
            "that route review effort to the right verifier. The tiles are schematic "
            "orientation only; authoritative status — the pass, warn, or block state — "
            "lives in the generated audits, not in this figure."
        ),
        "alt_text": (
            "Cockpit dashboard with audit status tiles for AGEINT build freshness, "
            "reference quality, source metadata, figure quality, readiness stack, "
            "and publication boundary."
        ),
        "renderer": "assurance_cockpit",
        "source_section": "orientation.md",
        "canvas_size": "2400",
        "orientation_slot": "assurance_cockpit",
        "semantic_role": "assurance_readiness_dashboard",
        "evidence_role": "local artifact-readiness orientation, verifier routing, and publication-boundary framing",
    },
)


__all__ = ["EARLY_ORIENTATION_VISUALS"]
