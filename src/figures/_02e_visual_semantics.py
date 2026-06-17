from __future__ import annotations

from dataclasses import replace

from ._01_part import FigureKind, FigureSpec


QUANTITATIVE_RENDERERS = frozenset(
    {
        "citation_density",
        "source_freshness_coverage",
        "analytic_source_quality_boundary",
        "reference_coverage",
        "visual_quality_audit_dashboard",
        "source_metadata_integrity",
        "source_refresh_due_dashboard",
        "agency_source_coverage_dashboard",
    }
)


def _with_visual_semantics(spec: FigureSpec) -> FigureSpec:
    """Fill semantic figure fields from kind and renderer defaults."""

    renderer_id = spec.provenance.get("renderer_id", "")
    if renderer_id == "claim_calibration_and_visual_semantics":
        return spec
    if spec.kind is FigureKind.PYTHON and renderer_id in QUANTITATIVE_RENDERERS:
        return replace(
            spec,
            semantic_role="descriptive_audit_chart",
            evidence_role="local artifact telemetry and verifier coverage summary",
            quantitative=True,
            unit="count",
            denominator="current generated AGEINT source, manuscript, figure, or report set",
            counting_rule=f"Renderer `{renderer_id}` counts local AGEINT records declared in its caption and provenance.",
            interpretation_limit=(
                "Counts describe local artifact coverage and verifier status; they are not "
                "measured learning outcomes, operational performance, source-quality scores, "
                "or statistical evidence of real-world analytic effect."
            ),
        )
    if spec.kind is FigureKind.HISTORICAL:
        return replace(
            spec,
            semantic_role="historical_source_example",
            evidence_role="public-domain provenance example and reader context",
            interpretation_limit=(
                "The image is a historical context example, not a measured capability score, "
                "current collection product, operational cue, or empirical validation result."
            ),
        )
    if spec.kind is FigureKind.AI_GENERATED:
        return replace(
            spec,
            semantic_role="synthetic_concept_plate",
            evidence_role="safe visual metaphor for a bounded curriculum concept",
            interpretation_limit=(
                "The plate is synthetic and illustrative, not a measured capability score, "
                "real event depiction, empirical result, or operational instruction."
            ),
        )
    if spec.kind is FigureKind.MERMAID:
        return replace(
            spec,
            semantic_role="conceptual_relationship_diagram",
            evidence_role="reader navigation, source relationship, or governance boundary map",
            interpretation_limit=(
                "Node position, color, and arrows are explanatory, not a measured capability "
                "score, statistical weight, source-quality ranking, or operational sequence."
            ),
        )
    return spec


__all__ = ["_with_visual_semantics"]
