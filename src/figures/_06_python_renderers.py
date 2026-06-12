from __future__ import annotations

from collections import Counter
from datetime import date
from pathlib import Path
from typing import Sequence

from curriculum import Curriculum

from ._01_part import FigureSpec
from ._03_part import (
    _render_accessibility_workflow,
    _render_adversarial_assurance_cycle,
    _render_agentic_intelligence_boundary,
    _render_agent_evaluation_loop,
    _render_agent_incident_lifecycle,
    _render_ai_compliance_map,
    _render_ai_incident_reporting_loop,
    _render_assessment_integrity_matrix,
    _render_bounded_autonomy_recoverability,
    _render_capstone_workflow,
    _render_claim_ledger_flow,
    _render_cross_border_data_flow,
    _render_data_lineage_registry,
    _render_hria_dpia_map,
    _render_instructor_assessment_lifecycle,
    _render_instructor_question_bank,
    _render_learner_support_plan,
    _render_model_dataset_card,
    _render_ot_definitive_architecture_record,
    _render_pattern_taxonomy,
    _render_procurement_oversight_loop,
    _render_public_ai_register_lifecycle,
    _render_records_retention_audit,
    _render_reference_coverage,
    _render_release_change_control,
    _render_remediation_backlog,
    _render_risk_exception_memo,
    _render_safe_substitution_matrix,
    _render_safety_boundary_loop,
    _render_section_composability_matrix,
    _render_source_quality_spine,
    _render_source_verification_flow,
    _render_transparency_notice_flow,
)
from ._03b_asset_renderers import _render_citation_density
from ._04_part import _font, _pil_modules
from ._05_visual_style import (
    CANVAS_BG,
    GRID,
    INK,
    MUTED,
    PALETTE,
    SOFT_PALETTE,
    draw_centered_text,
    draw_footer,
    draw_title_band,
    draw_wrapped_text,
)


def render_python_figure(
    root: Path,
    curriculum: Curriculum,
    spec: FigureSpec,
    output: Path | None = None,
) -> None:
    """Dispatch a registry-backed Python visual renderer."""
    renderer_id = spec.provenance["renderer_id"]
    if output is None:
        output = root / spec.output_path
    curriculum_renderers = {
        "citation_density": _render_citation_density,
        "pattern_taxonomy": _render_pattern_taxonomy,
        "section_composability_matrix": _render_section_composability_matrix,
        "reference_coverage": _render_reference_coverage,
    }
    spec_renderers = {
        "source_quality_spine": _render_source_quality_spine,
        "source_freshness_coverage": _render_source_freshness_coverage,
        "analytic_source_quality_boundary": _render_analytic_source_quality_boundary,
        "safety_boundary_loop": _render_safety_boundary_loop,
        "source_verification_flow": _render_source_verification_flow,
        "claim_ledger_flow": _render_claim_ledger_flow,
        "ai_compliance_map": _render_ai_compliance_map,
        "agent_evaluation_loop": _render_agent_evaluation_loop,
        "cross_border_data_flow": _render_cross_border_data_flow,
        "capstone_workflow": _render_capstone_workflow,
        "safe_substitution_matrix": _render_safe_substitution_matrix,
        "instructor_assessment_lifecycle": _render_instructor_assessment_lifecycle,
        "accessibility_workflow": _render_accessibility_workflow,
        "hria_dpia_map": _render_hria_dpia_map,
        "procurement_oversight_loop": _render_procurement_oversight_loop,
        "agent_incident_lifecycle": _render_agent_incident_lifecycle,
        "bounded_autonomy_recoverability": _render_bounded_autonomy_recoverability,
        "public_ai_register_lifecycle": _render_public_ai_register_lifecycle,
        "ai_incident_reporting_loop": _render_ai_incident_reporting_loop,
        "ot_definitive_architecture_record": _render_ot_definitive_architecture_record,
        "data_lineage_registry": _render_data_lineage_registry,
        "assessment_integrity_matrix": _render_assessment_integrity_matrix,
        "adversarial_assurance_cycle": _render_adversarial_assurance_cycle,
        "agentic_intelligence_boundary": _render_agentic_intelligence_boundary,
        "model_dataset_card": _render_model_dataset_card,
        "transparency_notice_flow": _render_transparency_notice_flow,
        "records_retention_audit": _render_records_retention_audit,
        "release_change_control": _render_release_change_control,
        "risk_exception_memo": _render_risk_exception_memo,
        "learner_support_plan": _render_learner_support_plan,
        "instructor_question_bank": _render_instructor_question_bank,
        "remediation_backlog": _render_remediation_backlog,
    }
    if renderer_id in curriculum_renderers:
        curriculum_renderers[renderer_id](output, curriculum, spec)
    elif renderer_id in spec_renderers:
        spec_renderers[renderer_id](output, spec)
    else:
        raise ValueError(f"Unknown AGEINT figure renderer: {renderer_id}")


def _render_source_freshness_coverage(output: Path, spec: FigureSpec) -> None:
    """Render source-anchor freshness and coverage from local JSONL metadata."""
    anchors = _research_anchors()
    checked = [_parse_date(anchor.checked_as_of) for anchor in anchors]
    latest = max((item for item in checked if item is not None), default=date(2026, 6, 11))
    freshness = Counter(_freshness_bucket(item, latest) for item in checked)
    tiers = Counter(anchor.source_tier or anchor.source_type for anchor in anchors)
    lanes = Counter(anchor.source_lane or anchor.domain for anchor in anchors)

    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (1600, 1000), CANVAS_BG)
    draw = draw_mod.Draw(canvas)
    draw_title_band(
        draw,
        font_mod,
        _font,
        spec.title,
        subtitle="Evidence-derived chart from local research-anchor metadata.",
        accent="#0f766e",
    )
    _draw_metric_card(draw, font_mod, (70, 150, 385, 280), "Curated anchors", str(len(anchors)), PALETTE[0])
    _draw_metric_card(draw, font_mod, (430, 150, 745, 280), "Source lanes", str(len(lanes)), PALETTE[1])
    _draw_metric_card(draw, font_mod, (790, 150, 1105, 280), "Evidence tiers", str(len(tiers)), PALETTE[2])
    _draw_metric_card(draw, font_mod, (1150, 150, 1465, 280), "Latest check", latest.isoformat(), PALETTE[3])

    _draw_horizontal_bars(
        draw,
        font_mod,
        (80, 345, 730, 700),
        "Freshness buckets",
        [(label, freshness[label]) for label in ("0-7 days", "8-30 days", "31-90 days", ">90 days", "unknown")],
    )
    _draw_horizontal_bars(
        draw,
        font_mod,
        (840, 345, 1510, 700),
        "Evidence tiers",
        tiers.most_common(6),
    )
    _draw_lane_tiles(draw, font_mod, lanes.most_common(6))
    draw_footer(
        draw,
        font_mod,
        _font,
        f"Source: data/research_anchors/*.jsonl | Baseline date: {latest.isoformat()} | Counts are audit coverage, not source quality scores.",
        y=930,
    )
    canvas.save(output, format="PNG", optimize=True)


def _render_analytic_source_quality_boundary(output: Path, spec: FigureSpec) -> None:
    """Render analytic-tradecraft evidence boundaries from anchor metadata."""
    anchors = [
        anchor
        for anchor in _research_anchors()
        if anchor.domain == "analytic_tradecraft"
        or "analytic" in (anchor.source_lane or "")
        or "forecasting_calibration" in (anchor.source_lane or "")
        or "sat_evaluation" in (anchor.source_lane or "")
        or "intelligence_failure" in (anchor.source_lane or "")
    ]
    lanes = Counter(anchor.source_lane or anchor.domain for anchor in anchors)
    tiers = Counter(anchor.source_tier or anchor.source_type for anchor in anchors)
    verification = Counter(anchor.verification_method for anchor in anchors)
    boundaries = (
        ("Official standards", _count_matching(lanes, ("analytic_tradecraft_evidence", "source_quality"))),
        ("Warning practice", _count_matching(lanes, ("warning_intelligence",))),
        ("Postmortem reports", _count_matching(lanes, ("intelligence_failure_postmortem",))),
        ("SAT evaluation", _count_matching(lanes, ("sat_evaluation_evidence",))),
        ("Forecast calibration", _count_matching(lanes, ("forecasting_calibration_evidence",))),
    )

    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (1600, 1000), CANVAS_BG)
    draw = draw_mod.Draw(canvas)
    draw_title_band(
        draw,
        font_mod,
        _font,
        spec.title,
        subtitle="Evidence-derived chart from curated analytic-tradecraft anchors.",
        accent="#7c3aed",
    )
    _draw_metric_card(draw, font_mod, (70, 150, 385, 280), "Analytic anchors", str(len(anchors)), PALETTE[3])
    _draw_metric_card(draw, font_mod, (430, 150, 745, 280), "Evidence lanes", str(len(lanes)), PALETTE[0])
    _draw_metric_card(draw, font_mod, (790, 150, 1105, 280), "Source tiers", str(len(tiers)), PALETTE[1])
    _draw_metric_card(draw, font_mod, (1150, 150, 1465, 280), "Verification modes", str(len(verification)), PALETTE[2])

    _draw_horizontal_bars(
        draw,
        font_mod,
        (80, 350, 740, 685),
        "Tradecraft evidence lanes",
        lanes.most_common(6),
    )
    _draw_horizontal_bars(
        draw,
        font_mod,
        (850, 350, 1510, 685),
        "Source tiers",
        tiers.most_common(6),
    )
    _draw_boundary_tiles(draw, font_mod, boundaries)
    draw_footer(
        draw,
        font_mod,
        _font,
        "Source: data/research_anchors/*.jsonl | Counts show support coverage and claim-boundary routing, not truth or quality scores.",
        y=930,
    )
    canvas.save(output, format="PNG", optimize=True)


def _count_matching(counter: Counter[str], needles: Sequence[str]) -> int:
    return sum(value for key, value in counter.items() if any(needle in key for needle in needles))


def _draw_boundary_tiles(
    draw: object,
    font_mod: object,
    rows: Sequence[tuple[str, int]],
) -> None:
    draw.text((80, 735), "Primary claim boundary", fill=INK, font=_font(font_mod, 26))
    tile_w = 280
    for index, (label, value) in enumerate(rows):
        x = 80 + index * 300
        box = (x, 785, x + tile_w, 885)
        draw.rounded_rectangle(box, radius=9, fill=SOFT_PALETTE[index % len(SOFT_PALETTE)], outline=GRID, width=2)
        draw_centered_text(draw, (x + 16, 792, x + tile_w - 16, 846), label, _font(font_mod, 18), width=20, max_lines=2)
        draw_centered_text(draw, (x + 20, 850, x + tile_w - 20, 880), str(value), _font(font_mod, 22), width=10, max_lines=1)


def _research_anchors() -> Sequence[object]:
    try:
        from intelligence_content import INTELLIGENCE_RESEARCH_ANCHORS
    except ImportError:  # pragma: no cover - package import variants
        from ..intelligence_content import INTELLIGENCE_RESEARCH_ANCHORS  # type: ignore

    return INTELLIGENCE_RESEARCH_ANCHORS


def _parse_date(value: str) -> date | None:
    try:
        return date.fromisoformat(value)
    except ValueError:
        return None


def _freshness_bucket(value: date | None, latest: date) -> str:
    if value is None:
        return "unknown"
    age = (latest - value).days
    if age <= 7:
        return "0-7 days"
    if age <= 30:
        return "8-30 days"
    if age <= 90:
        return "31-90 days"
    return ">90 days"


def _draw_metric_card(
    draw: object,
    font_mod: object,
    box: tuple[int, int, int, int],
    label: str,
    value: str,
    color: str,
) -> None:
    draw.rounded_rectangle(box, radius=10, fill="#ffffff", outline=color, width=4)
    draw.rectangle((box[0], box[1], box[0] + 16, box[3]), fill=color)
    draw_wrapped_text(draw, (box[0] + 34, box[1] + 24), label, _font(font_mod, 20), fill=MUTED, width=20, max_lines=1)
    draw_wrapped_text(draw, (box[0] + 34, box[1] + 64), value, _font(font_mod, 30), fill=INK, width=18, max_lines=1, line_height=34)


def _draw_horizontal_bars(
    draw: object,
    font_mod: object,
    box: tuple[int, int, int, int],
    title: str,
    rows: Sequence[tuple[str, int]],
) -> None:
    x0, y0, x1, y1 = box
    draw.text((x0, y0 - 42), title, fill=INK, font=_font(font_mod, 26))
    max_value = max((value for _, value in rows), default=1) or 1
    row_h = max(42, (y1 - y0) // max(1, len(rows)))
    for index, (label, value) in enumerate(rows):
        y = y0 + index * row_h
        draw_wrapped_text(draw, (x0, y + 6), _pretty_label(label), _font(font_mod, 18), fill=MUTED, width=23, max_lines=1)
        bar_x = x0 + 210
        bar_w = int((x1 - bar_x - 72) * (value / max_value))
        draw.rounded_rectangle((bar_x, y + 6, x1 - 72, y + row_h - 10), radius=7, fill="#e2e8f0")
        draw.rounded_rectangle((bar_x, y + 6, bar_x + bar_w, y + row_h - 10), radius=7, fill=PALETTE[index % len(PALETTE)])
        draw.text((x1 - 52, y + 9), str(value), fill=INK, font=_font(font_mod, 20))


def _draw_lane_tiles(draw: object, font_mod: object, rows: Sequence[tuple[str, int]]) -> None:
    draw.text((80, 745), "Largest source lanes", fill=INK, font=_font(font_mod, 26))
    tile_w = 235
    for index, (label, value) in enumerate(rows):
        x = 80 + index * 250
        box = (x, 790, x + tile_w, 885)
        draw.rounded_rectangle(box, radius=9, fill=SOFT_PALETTE[index % len(SOFT_PALETTE)], outline=GRID, width=2)
        draw_centered_text(draw, (x + 12, 798, x + tile_w - 12, 850), _pretty_label(label), _font(font_mod, 17), width=20, max_lines=2, line_height=20)
        draw_centered_text(draw, (x + 20, 852, x + tile_w - 20, 880), str(value), _font(font_mod, 22), width=10, max_lines=1)


def _pretty_label(value: str) -> str:
    labels = {
        "analytic_tradecraft": "analytic domain",
        "analytic_tradecraft_evidence": "analytic evidence",
        "intelligence_failure_postmortem": "failure postmortems",
        "sat_evaluation_evidence": "SAT evaluation",
        "forecasting_calibration_evidence": "forecast calibration",
        "official_primary": "official primary",
        "official_report": "official report",
        "scholarly_peer_reviewed": "peer reviewed",
    }
    return labels.get(value, value.replace("_", " ").replace("-", " "))
