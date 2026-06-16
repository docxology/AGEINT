from __future__ import annotations

from pathlib import Path

from agency_source_coverage import agency_source_coverage_figure_rows

from ._01_part import FigureSpec
from ._03c_control_matrix import draw_evidence_dashboard


def _render_agency_source_coverage_dashboard(output: Path, spec: FigureSpec) -> None:
    project_root = output.resolve().parents[3]
    draw_evidence_dashboard(
        output,
        spec.title,
        agency_source_coverage_figure_rows(project_root),
        ("Surface", "Coverage", "Routing", "Failure Signal"),
        "#bfdbfe",
        "#dcfce7",
        subtitle="Agency coverage is a routing audit for official-source anchors, not a claim that every agency or discipline is covered equally.",
        denominator="56 official US IC anchors routed through 10 source packs and profile lanes.",
        failure_path="Missing source_agency/source_pack metadata or unrouted source-pack keys fail agency_source_coverage_ok",
        reviewer_action="Verify agency label, source pack, profile route, and rights metadata before relying on a coverage claim.",
        footer="Source: AGEINT agency source coverage audit | Coverage telemetry only; not an authority ranking.",
    )


__all__ = ["_render_agency_source_coverage_dashboard"]
