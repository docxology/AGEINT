from __future__ import annotations

from pathlib import Path

from source_metadata import source_metadata_figure_rows

from ._01_part import FigureSpec
from ._03c_control_matrix import draw_evidence_dashboard


def _render_source_metadata_integrity(output: Path, spec: FigureSpec) -> None:
    project_root = output.resolve().parents[3]
    draw_evidence_dashboard(
        output,
        spec.title,
        source_metadata_figure_rows(project_root),
        ("Surface", "Coverage", "Explicit Field", "Failure Signal"),
        "#ddd6fe",
        "#dcfce7",
        subtitle="Source metadata integrity is checked against local anchor rows before generated prose can reuse an anchor as support.",
        denominator="472 metadata rows: 462 intelligence anchors plus 10 source-quality support anchors.",
        failure_path="Blank source_lane/source_tier rows, fallback semantics, or support-anchor mismatches fail source_metadata_ok",
        reviewer_action="Compare lane, tier, checked_as_of, cadence, and trigger fields before trusting manuscript claims.",
        footer="Source: AGEINT source metadata audit | Local telemetry only; not a source quality score.",
    )


__all__ = ["_render_source_metadata_integrity"]
