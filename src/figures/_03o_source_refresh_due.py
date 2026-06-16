from __future__ import annotations

from pathlib import Path

from source_refresh_due import source_refresh_due_figure_rows

from ._01_part import FigureSpec
from ._03c_control_matrix import draw_evidence_dashboard


def _render_source_refresh_due_dashboard(output: Path, spec: FigureSpec) -> None:
    project_root = output.resolve().parents[3]
    draw_evidence_dashboard(
        output,
        spec.title,
        source_refresh_due_figure_rows(project_root),
        ("Surface", "Status", "Coverage", "Failure Signal"),
        "#bae6fd",
        "#dcfce7",
        subtitle="Refresh readiness is counted from checked_as_of dates and cadence metadata before source-backed prose is treated as current.",
        denominator="472 source rows with checked_as_of dates, refresh cadence classes, and refresh triggers.",
        failure_path="Due, stale, missing-date, or unknown-cadence rows block source_refresh_due_ok",
        reviewer_action="Refresh the source URL and date before reusing affected claims in generated manuscript sections.",
        footer="Source: AGEINT source refresh audit | Date telemetry only; not an empirical source-performance claim.",
    )


__all__ = ["_render_source_refresh_due_dashboard"]
