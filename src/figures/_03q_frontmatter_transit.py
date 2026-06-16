from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from agency_source_coverage import collect_agency_source_coverage
from curriculum import Curriculum
from source_metadata import collect_source_metadata
from source_refresh_due import collect_source_refresh_due

from ._04_part import _font, _pil_modules, _validate_png_asset
from ._05_visual_style import INK, MUTED, PALETTE, SOFT_PALETTE, draw_wrapped_text

FRONTMATTER_OUTPUT_PATH = Path("output/figures/frontmatter/ageint-evidence-transit-map.png")


def render_evidence_transit_map(
    project_root: Path,
    curriculum: Curriculum,
    *,
    figure_count: int,
    generated_markdown_files: int,
) -> Path:
    """Render the non-numbered page-two AGEINT evidence transit map."""

    root = Path(project_root)
    output = root / FRONTMATTER_OUTPUT_PATH
    output.parent.mkdir(parents=True, exist_ok=True)

    telemetry = _collect_telemetry(
        root,
        curriculum,
        figure_count=figure_count,
        generated_markdown_files=generated_markdown_files,
    )
    metadata = _frontmatter_metadata(telemetry)

    image_mod, draw_mod, font_mod, _ = _pil_modules()
    pnginfo_mod = __import__("PIL.PngImagePlugin", fromlist=["PngInfo"])

    size = 2200
    canvas = image_mod.new("RGB", (size, size), "#f8fafc")
    draw = draw_mod.Draw(canvas)

    _draw_map_background(draw, size)
    _draw_header(draw, font_mod)
    _draw_column_labels(draw, font_mod)
    _draw_rails(draw)
    _draw_source_reservoirs(draw, font_mod, telemetry)
    _draw_switchyard(draw, font_mod)
    _draw_verifier_gates(draw, font_mod, telemetry)
    _draw_output_artifacts(draw, font_mod, telemetry)
    _draw_boundary_footer(draw, font_mod)

    png_info = pnginfo_mod.PngInfo()
    for key, value in {
        "AGEINT.Kind": metadata["kind"],
        "AGEINT.Title": metadata["title"],
        "AGEINT.OutputPath": metadata["output_path"],
        "AGEINT.NonNumbered": str(metadata["non_numbered"]).lower(),
        "AGEINT.Description": metadata["description"],
        "AGEINT.Provenance": json.dumps(metadata["provenance"], sort_keys=True),
    }.items():
        png_info.add_text(key, value, zip=len(value) > 180)
    canvas.save(output, format="PNG", compress_level=3, pnginfo=png_info)
    _validate_png_asset(output)
    output.with_suffix(".json").write_text(
        json.dumps(metadata, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return output


def _collect_telemetry(
    project_root: Path,
    curriculum: Curriculum,
    *,
    figure_count: int,
    generated_markdown_files: int,
) -> dict[str, Any]:
    source_metadata = collect_source_metadata(project_root).payload
    source_refresh = collect_source_refresh_due(project_root).payload
    agency_coverage = collect_agency_source_coverage(project_root).payload
    metadata_summary = source_metadata["summary"]
    refresh_summary = source_refresh["summary"]
    agency_summary = agency_coverage["summary"]
    return {
        "curriculum": {
            "parts": curriculum.stats["parts"],
            "modules": curriculum.stats["chapters"],
            "appendices": curriculum.stats["appendices"],
            "patterns": curriculum.stats["patterns"],
            "references": curriculum.stats["references"],
        },
        "source_metadata": {
            "records": metadata_summary["metadata_records"],
            "intelligence_anchors": metadata_summary["intelligence_anchor_count"],
            "support_anchors": metadata_summary["source_quality_anchor_count"],
            "blank_lanes": metadata_summary["blank_source_lane_count"],
            "blank_tiers": metadata_summary["blank_source_tier_count"],
            "fallback_rows": metadata_summary["fallback_dependent_row_count"],
        },
        "source_freshness": {
            "as_of": source_refresh["as_of"],
            "rows": refresh_summary["row_count"],
            "due_or_stale": refresh_summary["due_or_stale_count"],
            "due_soon": refresh_summary["due_soon_count"],
            "missing_dates": refresh_summary["missing_checked_as_of_count"],
            "unknown_cadence": refresh_summary["unknown_cadence_count"],
        },
        "agency_source_routing": {
            "new_official_us_ic_anchors": agency_summary["new_official_us_ic_anchor_count"],
            "routed": agency_summary["profile_routed_new_anchor_count"],
            "unrouted": agency_summary["unrouted_new_anchor_count"],
            "missing_metadata": agency_summary["missing_required_metadata_count"],
        },
        "outputs": {
            "registered_figures": figure_count,
            "generated_markdown_files": generated_markdown_files,
        },
    }


def _frontmatter_metadata(telemetry: dict[str, Any]) -> dict[str, Any]:
    return {
        "kind": "front_matter_visual",
        "non_numbered": True,
        "title": "AGEINT Evidence Transit Map",
        "output_path": FRONTMATTER_OUTPUT_PATH.as_posix(),
        "description": (
            "Deterministic non-numbered page-two visual for the AGEINT PDF publishing "
            "information page. The map summarizes artifact telemetry and verification "
            "boundaries without claiming model performance, public release, publication "
            "certification, or learning outcomes."
        ),
        "provenance": {
            "renderer": "python_pillow",
            "source": (
                "data/curriculum/, source metadata, source refresh due, agency source "
                "coverage, generated figure registry, and generated manuscript files"
            ),
            "telemetry": telemetry,
        },
    }


def _draw_map_background(draw: Any, size: int) -> None:
    for offset in range(0, size + 1, 110):
        color = "#e6eef7" if offset % 220 else "#d7e3ef"
        draw.line((offset, 0, offset, size), fill=color, width=2)
        draw.line((0, offset, size, offset), fill=color, width=2)
    draw.rectangle((56, 56, size - 56, size - 56), outline="#94a3b8", width=4)
    draw.rectangle((88, 88, size - 88, size - 88), outline="#d1dbe8", width=2)


def _draw_header(draw: Any, font_mod: Any) -> None:
    draw.rounded_rectangle((150, 135, 2050, 330), radius=44, fill="#0f172a", outline="#334155", width=5)
    draw.text((215, 180), "AGEINT EVIDENCE TRANSIT MAP", fill="#f8fafc", font=_font(font_mod, 58))
    draw.text(
        (218, 255),
        "source reservoirs -> claim packet switchyard -> verifier gates -> output artifacts",
        fill="#cbd5e1",
        font=_font(font_mod, 29),
    )


def _draw_column_labels(draw: Any, font_mod: Any) -> None:
    labels = [
        (235, "SOURCE RESERVOIRS", PALETTE[0]),
        (760, "CLAIM SWITCHYARD", PALETTE[3]),
        (1275, "VERIFIER GATES", PALETTE[1]),
        (1770, "OUTPUT ARTIFACTS", PALETTE[2]),
    ]
    for x, label, color in labels:
        draw.text((x, 390), label, fill=color, font=_font(font_mod, 27))
        draw.line((x, 428, x + 310, 428), fill=color, width=6)


def _draw_rails(draw: Any) -> None:
    rail_specs = [
        ("#2563eb", 545, 1040),
        ("#0f766e", 710, 1180),
        ("#b45309", 875, 1320),
        ("#7c3aed", 1040, 1460),
    ]
    for color, source_y, gate_y in rail_specs:
        _draw_polyline(
            draw,
            (
                (560, source_y),
                (700, source_y),
                (820, 1100),
                (1110, 1100),
                (1240, gate_y),
                (1620, gate_y),
            ),
            color,
        )
    for color, y in (("#2563eb", 1655), ("#0f766e", 1755), ("#b45309", 1855), ("#7c3aed", 1955)):
        _draw_polyline(draw, ((1545, y - 355), (1650, y), (1980, y)), color)


def _draw_source_reservoirs(draw: Any, font_mod: Any, telemetry: dict[str, Any]) -> None:
    curriculum = telemetry["curriculum"]
    metadata = telemetry["source_metadata"]
    freshness = telemetry["source_freshness"]
    agency = telemetry["agency_source_routing"]
    cards = [
        (
            "Curriculum spine",
            f"{curriculum['parts']} parts | {curriculum['modules']} modules",
            f"{curriculum['appendices']} appendices and {curriculum['patterns']} governed patterns",
            PALETTE[0],
            480,
        ),
        (
            "Source anchors",
            f"{metadata['records']} rows | {metadata['intelligence_anchors']} intelligence",
            f"{metadata['support_anchors']} source-quality support anchors",
            PALETTE[1],
            645,
        ),
        (
            "Guide references",
            f"{curriculum['references']} parsed references",
            "source identity lock preserves ageint keys",
            PALETTE[2],
            810,
        ),
        (
            "Agency source packs",
            f"{agency['new_official_us_ic_anchors']} new official US IC anchors",
            f"{agency['routed']} routed profiles | as-of {freshness['as_of']}",
            PALETTE[3],
            975,
        ),
    ]
    for title, value, body, color, y in cards:
        _draw_station_card(draw, font_mod, (170, y, 570, y + 128), title, value, body, color)


def _draw_switchyard(draw: Any, font_mod: Any) -> None:
    box = (735, 550, 1145, 1510)
    draw.rounded_rectangle(box, radius=54, fill="#ffffff", outline="#7c3aed", width=6)
    draw.text((815, 615), "CLAIM", fill="#4c1d95", font=_font(font_mod, 48))
    draw.text((795, 670), "PACKET", fill="#4c1d95", font=_font(font_mod, 48))
    draw.text((770, 725), "SWITCHYARD", fill="#4c1d95", font=_font(font_mod, 38))
    packets = [
        ("source key", "#ede9fe"),
        ("claim scope", "#dbeafe"),
        ("caveat", "#fef3c7"),
        ("reviewer", "#ccfbf1"),
        ("refresh trigger", "#ffe4e6"),
        ("output route", "#e0f2fe"),
    ]
    for index, (label, fill) in enumerate(packets):
        x0 = 790 + (index % 2) * 170
        y0 = 850 + (index // 2) * 142
        draw.rounded_rectangle((x0, y0, x0 + 145, y0 + 92), radius=22, fill=fill, outline="#94a3b8", width=3)
        draw_wrapped_text(
            draw,
            (x0 + 17, y0 + 23),
            label,
            _font(font_mod, 24),
            fill=INK,
            width=11,
            max_lines=2,
            line_height=28,
        )
    draw.rounded_rectangle((780, 1295, 1100, 1415), radius=30, fill="#f8fafc", outline="#7c3aed", width=4)
    draw_wrapped_text(
        draw,
        (812, 1320),
        "Only bounded, cited, reviewable packets can leave the yard.",
        _font(font_mod, 25),
        fill=MUTED,
        width=25,
        max_lines=3,
        line_height=31,
    )


def _draw_verifier_gates(draw: Any, font_mod: Any, telemetry: dict[str, Any]) -> None:
    metadata = telemetry["source_metadata"]
    freshness = telemetry["source_freshness"]
    agency = telemetry["agency_source_routing"]
    outputs = telemetry["outputs"]
    gates = [
        (
            "metadata gate",
            "PASS",
            f"{metadata['blank_lanes']} blank lanes | {metadata['blank_tiers']} blank tiers",
            f"{metadata['fallback_rows']} fallback rows",
            PALETTE[1],
            965,
        ),
        (
            "freshness gate",
            "PASS",
            f"{freshness['due_or_stale']} due/stale | {freshness['due_soon']} due soon",
            f"{freshness['missing_dates']} missing dates | {freshness['unknown_cadence']} unknown cadence",
            PALETTE[0],
            1115,
        ),
        (
            "agency routing",
            "PASS",
            f"{agency['unrouted']} unrouted | {agency['missing_metadata']} missing metadata",
            f"{agency['routed']} profile routes checked",
            PALETTE[3],
            1265,
        ),
        (
            "artifact registry",
            "PASS",
            f"{outputs['registered_figures']} registered figures",
            f"{outputs['generated_markdown_files']} generated manuscript files",
            PALETTE[2],
            1415,
        ),
    ]
    for title, status, value, body, color, y in gates:
        _draw_gate_card(draw, font_mod, (1225, y, 1588, y + 122), title, status, value, body, color)


def _draw_output_artifacts(draw: Any, font_mod: Any, telemetry: dict[str, Any]) -> None:
    outputs = telemetry["outputs"]
    artifacts = [
        (
            "Semantic manuscript",
            f"{outputs['generated_markdown_files']} generated Markdown files",
            "labels, citations, and reader routes",
            PALETTE[0],
            1610,
        ),
        (
            "Figure system",
            f"{outputs['registered_figures']} numbered registry figures",
            "front-matter furniture is non-numbered",
            PALETTE[1],
            1710,
        ),
        (
            "Evidence reports",
            "metadata, refresh, agency routing, quality",
            "fail-closed audits before trust claims",
            PALETTE[3],
            1810,
        ),
        (
            "PDF front matter",
            "cover unchanged | page-two visual added",
            "publishing info carries telemetry caveat",
            PALETTE[2],
            1910,
        ),
    ]
    for title, value, body, color, y in artifacts:
        _draw_terminal_card(draw, font_mod, (1615, y - 62, 2045, y + 60), title, value, body, color)


def _draw_boundary_footer(draw: Any, font_mod: Any) -> None:
    draw.rounded_rectangle((155, 2055, 2045, 2130), radius=28, fill="#fff1f2", outline="#be123c", width=4)
    draw.text(
        (195, 2078),
        "BOUNDARY: artifact telemetry only; no model performance, learning-outcome, public-release, or publication certification claim.",
        fill="#9f1239",
        font=_font(font_mod, 25),
    )


def _draw_station_card(
    draw: Any,
    font_mod: Any,
    box: tuple[int, int, int, int],
    title: str,
    value: str,
    body: str,
    color: str,
) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=26, fill="#ffffff", outline=color, width=5)
    draw.ellipse((x1 - 56, y0 + 36, x1 - 20, y0 + 72), fill=color, outline=color)
    draw.text((x0 + 25, y0 + 18), title.upper(), fill=color, font=_font(font_mod, 23))
    draw_wrapped_text(draw, (x0 + 25, y0 + 53), value, _font(font_mod, 27), fill=INK, width=28, max_lines=1)
    draw_wrapped_text(
        draw,
        (x0 + 25, y0 + 84),
        body,
        _font(font_mod, 18),
        fill=MUTED,
        width=39,
        max_lines=2,
        line_height=22,
    )


def _draw_gate_card(
    draw: Any,
    font_mod: Any,
    box: tuple[int, int, int, int],
    title: str,
    status: str,
    value: str,
    body: str,
    color: str,
) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=24, fill="#ffffff", outline=color, width=5)
    draw.rounded_rectangle((x1 - 95, y0 + 16, x1 - 24, y0 + 50), radius=14, fill="#ecfccb", outline="#4d7c0f", width=2)
    draw.text((x1 - 80, y0 + 23), status, fill="#3f6212", font=_font(font_mod, 17))
    draw.text((x0 + 22, y0 + 17), title.upper(), fill=color, font=_font(font_mod, 21))
    draw_wrapped_text(draw, (x0 + 22, y0 + 50), value, _font(font_mod, 23), fill=INK, width=29, max_lines=1)
    draw_wrapped_text(draw, (x0 + 22, y0 + 82), body, _font(font_mod, 19), fill=MUTED, width=32, max_lines=1)


def _draw_terminal_card(
    draw: Any,
    font_mod: Any,
    box: tuple[int, int, int, int],
    title: str,
    value: str,
    body: str,
    color: str,
) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=24, fill=SOFT_PALETTE[PALETTE.index(color) % len(SOFT_PALETTE)], outline=color, width=4)
    draw.text((x0 + 22, y0 + 15), title.upper(), fill=color, font=_font(font_mod, 20))
    draw_wrapped_text(draw, (x0 + 22, y0 + 45), value, _font(font_mod, 22), fill=INK, width=36, max_lines=1)
    draw_wrapped_text(draw, (x0 + 22, y0 + 75), body, _font(font_mod, 17), fill=MUTED, width=41, max_lines=1)


def _draw_polyline(draw: Any, points: tuple[tuple[int, int], ...], color: str) -> None:
    for start, end in zip(points, points[1:]):
        draw.line((*start, *end), fill=color, width=14)
        draw.line((*start, *end), fill="#ffffff", width=4)
    for x, y in points:
        draw.ellipse((x - 19, y - 19, x + 19, y + 19), fill="#ffffff", outline=color, width=6)


__all__ = ["FRONTMATTER_OUTPUT_PATH", "render_evidence_transit_map"]
