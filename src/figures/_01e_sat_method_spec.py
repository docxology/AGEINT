"""Registry rows for Synthetic Analytic Tradecraft and validation visuals."""

from __future__ import annotations

SAT_METHOD_VISUALS: tuple[dict[str, str], ...] = (
    {
        "slug": "ageint-graphical-abstract",
        "title": "AGEINT Synthetic Tradecraft System Atlas",
        "caption": (
            "The Synthetic Tradecraft System Atlas replaces the former graphical "
            "abstract with a governed-system view of AGEINT. It shows the source "
            "spine as the evidence floor; intelligence disciplines as collection "
            "and context lanes; Synthetic Analytic Tradecraft as the central "
            "claim-making contract; bounded agentic assistance as a limited "
            "support layer; and verification, safety, and human-review gates as "
            "the outer assurance ring. The figure is a curriculum architecture "
            "map, not a claim that AGEINT has measured operational performance."
        ),
        "alt_text": (
            "Square system atlas for AGEINT. A dark source spine anchors locked "
            "reference keys and verified sources at the bottom. Discipline lanes "
            "for HUMINT, SIGINT, OSINT, GEOINT, FININT, cyber, cognitive security, "
            "and governance feed a central Synthetic Analytic Tradecraft core. "
            "Above it, bounded agentic assistance can retrieve, reason, structure, "
            "and hand off, but cannot approve external action. Around the system, "
            "verification and safety gates check citations, figures, metadata, "
            "PDF links, rights, and human review before any product is trusted."
        ),
        "renderer": "graphical_abstract_atlas",
        "source_section": "orientation.md",
        "canvas_size": "2400",
    },
    {
        "slug": "ageint-synthetic-tradecraft-method-contract",
        "title": "Synthetic Analytic Tradecraft Method Contract",
        "caption": (
            "The method-contract figure makes AGEINT's Synthetic Analytic Tradecraft "
            "claim falsifiable. It links source-family triangulation, synthetic "
            "fixtures, analytic field separation, negative-control testing, reviewer "
            "challenge, and artifact-evidence reports so early manuscript claims remain "
            "method commitments rather than prestige language."
        ),
        "alt_text": (
            "Control matrix connecting source families, synthetic fixtures, analytic "
            "claim fields, negative controls, reviewer challenge, and artifact evidence "
            "for AGEINT Synthetic Analytic Tradecraft."
        ),
        "renderer": "synthetic_tradecraft_method_contract",
        "source_section": "orientation.md",
    },
    {
        "slug": "ageint-analysis-validation-matrix",
        "title": "AGEINT Analysis Validation Matrix",
        "caption": (
            "The analysis-validation matrix makes the manuscript's scholarship and "
            "assurance claims reviewable by class. It separates design guidance, "
            "empirical or evaluation claims, governance claims, figure/readability "
            "claims, rendered-artifact readiness claims, and reviewer disposition "
            "claims so each one has a required evidence packet, validation question, "
            "failure condition, and remediation path."
        ),
        "alt_text": (
            "Matrix connecting AGEINT claim classes to evidence packets, validation "
            "questions, failure conditions, and reviewer dispositions for manuscript "
            "analysis validation."
        ),
        "renderer": "analysis_validation_matrix",
        "source_section": "orientation.md",
    },
    {
        "slug": "ageint-analysis-validation-family-coverage",
        "title": "AGEINT Analysis Validation Family Coverage",
        "caption": (
            "The analysis-validation family-coverage figure closes the gap between "
            "method prose and generated manuscript structure. It maps each "
            "claim-bearing manuscript family to a canonical analysis-validation "
            "lane, the evidence signal that should be present, and the failure "
            "signal that should block local readiness if a family becomes "
            "claim-bearing without a review class."
        ),
        "alt_text": (
            "Matrix mapping AGEINT claim-bearing manuscript families to analysis "
            "validation lanes, evidence signals, and failure signals."
        ),
        "renderer": "analysis_validation_family_coverage",
        "source_section": "orientation.md",
    },
)


__all__ = ["SAT_METHOD_VISUALS"]
