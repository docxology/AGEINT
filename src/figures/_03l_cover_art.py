from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from curriculum import Curriculum

from ._04_part import _font, _pil_modules, _validate_png_asset
from ._05_visual_style import INK, MUTED, PALETTE, SOFT_PALETTE, draw_wrapped_text

COVER_OUTPUT_PATH = Path("output/figures/cover/ageint-cover-synthesis.png")
COVER_CANVAS_SIZE = 2400
COVER_MIN_FONT_SIZE = 24

COVER_DOMAIN_LABELS = (
    "HUMINT",
    "SIGINT",
    "OSINT",
    "GEOINT/IMINT",
    "FININT",
    "CYBINT/CTI",
    "TECHINT/MASINT",
    "CI",
    "COGSEC",
    "ALL-SOURCE FUSION",
)

COVER_BOUNDARY_TERMS = (
    "DEFENSIVE",
    "EDUCATIONAL",
    "ACCOUNTABLE",
    "SYNTHETIC",
    "EVIDENCE-BOUNDED",
)

COVER_FOREGROUND_REGIONS: tuple[tuple[str, tuple[int, int, int, int]], ...] = (
    ("header", (140, 95, 2260, 260)),
    ("boundary_key", (270, 300, 2130, 390)),
    ("agentic_layer", (410, 430, 1990, 660)),
    ("domain_humint", (235, 780, 585, 858)),
    ("domain_sigint", (235, 910, 585, 988)),
    ("domain_geoint_imint", (235, 1040, 585, 1118)),
    ("domain_techint_masint", (235, 1170, 585, 1248)),
    ("domain_cogsec", (235, 1300, 585, 1378)),
    ("tradecraft_core", (670, 820, 1730, 1420)),
    ("domain_osint", (1815, 780, 2165, 858)),
    ("domain_finint", (1815, 910, 2165, 988)),
    ("domain_cybint_cti", (1815, 1040, 2165, 1118)),
    ("domain_ci", (1815, 1170, 2165, 1248)),
    ("domain_all_source", (1815, 1300, 2165, 1378)),
    ("verification_citations", (260, 1485, 610, 1620)),
    ("verification_figures_pdf", (715, 1485, 1065, 1620)),
    ("verification_metadata", (1170, 1485, 1520, 1620)),
    ("verification_quality", (1625, 1485, 1975, 1620)),
    ("source_floor", (190, 1715, 2210, 2075)),
    ("footer", (220, 2165, 2180, 2305)),
)

_REGION_BOXES = dict(COVER_FOREGROUND_REGIONS)

_DOMAIN_NODE_SPECS: tuple[tuple[str, str, str], ...] = (
    ("HUMINT", "domain_humint", PALETTE[0]),
    ("SIGINT", "domain_sigint", PALETTE[1]),
    ("GEOINT/IMINT", "domain_geoint_imint", PALETTE[2]),
    ("TECHINT/MASINT", "domain_techint_masint", PALETTE[3]),
    ("COGSEC", "domain_cogsec", PALETTE[5]),
    ("OSINT", "domain_osint", PALETTE[0]),
    ("FININT", "domain_finint", PALETTE[1]),
    ("CYBINT/CTI", "domain_cybint_cti", PALETTE[4]),
    ("CI", "domain_ci", PALETTE[2]),
    ("ALL-SOURCE FUSION", "domain_all_source", PALETTE[6]),
)


def render_cover_art(project_root: Path, curriculum: Curriculum) -> Path:
    """Render the non-numbered AGEINT cover image and metadata sidecar."""

    root = Path(project_root)
    output = root / COVER_OUTPUT_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    pnginfo_mod = __import__("PIL.PngImagePlugin", fromlist=["PngInfo"])

    canvas = image_mod.new("RGB", (COVER_CANVAS_SIZE, COVER_CANVAS_SIZE), "#f7fafc")
    draw = draw_mod.Draw(canvas)

    _draw_background_grid(draw, COVER_CANVAS_SIZE)
    _draw_system_rings(draw)
    _draw_domain_paths(draw)
    _draw_header(draw, font_mod)
    _draw_boundary_key(draw, font_mod)
    _draw_agentic_layer(draw, font_mod)
    _draw_domain_nodes(draw, font_mod)
    _draw_tradecraft_core(draw, font_mod, curriculum)
    _draw_verification_strip(draw, font_mod)
    _draw_source_foundation(draw, font_mod, curriculum)
    _draw_cover_footer(draw, font_mod, curriculum)

    png_info = pnginfo_mod.PngInfo()
    metadata = _cover_metadata(curriculum)
    layout_regions = json.dumps(metadata["layout_regions"], sort_keys=True)
    for key, value in {
        "AGEINT.Kind": metadata["kind"],
        "AGEINT.Title": metadata["title"],
        "AGEINT.OutputPath": metadata["output_path"],
        "AGEINT.NonNumbered": str(metadata["non_numbered"]).lower(),
        "AGEINT.Description": metadata["description"],
        "AGEINT.DomainLabels": "|".join(COVER_DOMAIN_LABELS),
        "AGEINT.BoundaryTerms": "|".join(COVER_BOUNDARY_TERMS),
        "AGEINT.LayoutRegions": layout_regions,
        "AGEINT.MinimumFontSize": str(COVER_MIN_FONT_SIZE),
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


def _cover_metadata(curriculum: Curriculum) -> dict[str, Any]:
    return {
        "kind": "cover_art",
        "non_numbered": True,
        "title": "AGEINT Cover Synthesis",
        "output_path": COVER_OUTPUT_PATH.as_posix(),
        "description": (
            "Deterministic non-numbered cover image for the AGEINT PDF title page. "
            "The visual is a conceptual domain map and evidence-lens atlas for source spine, Synthetic "
            "Analytic Tradecraft, bounded agentic assistance, verification, and "
            "safety constraints; it is not a performance or completeness claim."
        ),
        "domain_labels": list(COVER_DOMAIN_LABELS),
        "boundary_terms": list(COVER_BOUNDARY_TERMS),
        "minimum_font_size": COVER_MIN_FONT_SIZE,
        "layout_regions": [
            {"name": name, "box": list(box)} for name, box in COVER_FOREGROUND_REGIONS
        ],
        "provenance": {
            "renderer": "python_pillow",
            "source": "data/curriculum/",
            "parts": str(curriculum.stats["parts"]),
            "modules": str(curriculum.stats["chapters"]),
            "appendices": str(curriculum.stats["appendices"]),
            "references": str(curriculum.stats["references"]),
            "domain_labels": "|".join(COVER_DOMAIN_LABELS),
        },
    }


def _cover_font(font_mod: Any, size: int) -> Any:
    if size < COVER_MIN_FONT_SIZE:
        raise ValueError(f"Cover text below {COVER_MIN_FONT_SIZE} pt: {size}")
    return _font(font_mod, size)


def _box(name: str) -> tuple[int, int, int, int]:
    return _REGION_BOXES[name]


def _draw_background_grid(draw: Any, size: int) -> None:
    for offset in range(0, size + 1, 120):
        color = "#edf4fb" if offset % 240 else "#dbe8f4"
        draw.line((offset, 0, offset, size), fill=color, width=1)
        draw.line((0, offset, size, offset), fill=color, width=1)
    draw.rectangle((52, 52, size - 52, size - 52), outline="#a8b7ca", width=4)
    draw.rectangle((78, 78, size - 78, size - 78), outline="#d3deea", width=2)


def _draw_header(draw: Any, font_mod: Any) -> None:
    x0, y0, x1, y1 = _box("header")
    draw.rounded_rectangle((x0, y0, x1, y1), radius=42, fill="#0f172a", outline="#334155", width=5)
    draw.text((x0 + 58, y0 + 30), "AGEINT", fill="#f8fafc", font=_cover_font(font_mod, 70))
    draw.text(
        (x0 + 360, y0 + 36),
        "Synthetic Analytic Tradecraft Atlas",
        fill="#dbeafe",
        font=_cover_font(font_mod, 50),
    )
    draw.text(
        (x0 + 63, y0 + 104),
        "source-governed curriculum, accountable agent support, and evidence-bounded claim packets",
        fill="#cbd5e1",
        font=_cover_font(font_mod, 28),
    )


def _draw_boundary_key(draw: Any, font_mod: Any) -> None:
    x0, y0, x1, y1 = _box("boundary_key")
    draw.rounded_rectangle((x0, y0, x1, y1), radius=30, fill="#ffffff", outline="#0f766e", width=4)
    draw.text((x0 + 36, y0 + 26), "BOUNDARY KEY", fill="#0f766e", font=_cover_font(font_mod, 27))
    chip_styles = {
        "DEFENSIVE": ("#dbeafe", "#2563eb"),
        "EDUCATIONAL": ("#ccfbf1", "#0f766e"),
        "ACCOUNTABLE": ("#fef3c7", "#b45309"),
        "SYNTHETIC": ("#ede9fe", "#7c3aed"),
        "EVIDENCE-BOUNDED": ("#ffe4e6", "#be123c"),
    }
    chip_x = x0 + 270
    for label in COVER_BOUNDARY_TERMS:
        fill, outline = chip_styles[label]
        width = 240 if len(label) < 13 else 330
        draw.rounded_rectangle((chip_x, y0 + 20, chip_x + width, y1 - 20), radius=22, fill=fill, outline=outline, width=3)
        bbox = draw.textbbox((0, 0), label, font=_cover_font(font_mod, 24))
        draw.text(
            (chip_x + (width - (bbox[2] - bbox[0])) / 2, y0 + 34),
            label,
            fill=outline,
            font=_cover_font(font_mod, 24),
        )
        chip_x += width + 28


def _draw_agentic_layer(draw: Any, font_mod: Any) -> None:
    x0, y0, x1, y1 = _box("agentic_layer")
    draw.rounded_rectangle((x0, y0, x1, y1), radius=44, fill="#ffffff", outline="#7c3aed", width=6)
    draw.text((x0 + 56, y0 + 32), "BOUNDED AGENTIC ASSISTANCE", fill="#4c1d95", font=_cover_font(font_mod, 38))
    draw.text(
        (x0 + 56, y0 + 87),
        "retrieve -> compare -> constrain tools -> preserve memory -> hand off for review",
        fill=MUTED,
        font=_cover_font(font_mod, 26),
    )
    steps = (
        ("PERCEIVE", "retrieve and structure"),
        ("REASON", "compare hypotheses"),
        ("TOOLS", "allowlisted only"),
        ("MEMORY", "governed recall"),
        ("HANDOFF", "human review"),
    )
    for index, (title, body) in enumerate(steps):
        sx0 = x0 + 74 + index * 285
        sy0 = y0 + 135
        draw.rounded_rectangle((sx0, sy0, sx0 + 250, sy0 + 68), radius=20, fill="#f5f3ff", outline="#a78bfa", width=3)
        draw.text((sx0 + 18, sy0 + 12), title, fill="#5b21b6", font=_cover_font(font_mod, 24))
        draw.text((sx0 + 18, sy0 + 38), body, fill=INK, font=_cover_font(font_mod, 24))


def _draw_system_rings(draw: Any) -> None:
    center = (1200, 1080)
    rings = (
        (705, "#2563eb"),
        (545, "#0f766e"),
        (385, "#b45309"),
        (245, "#7c3aed"),
    )
    for radius, outline in rings:
        box = (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius)
        draw.ellipse(box, outline=outline, width=5)


def _draw_domain_paths(draw: Any) -> None:
    center = (1200, 1080)
    for _, region_name, color in _DOMAIN_NODE_SPECS:
        x0, y0, x1, y1 = _box(region_name)
        node_center = ((x0 + x1) // 2, (y0 + y1) // 2)
        draw.line((*node_center, *center), fill=color, width=3)
        draw.line((*node_center, *center), fill="#ffffff", width=1)


def _draw_domain_nodes(draw: Any, font_mod: Any) -> None:
    for label, region_name, color in _DOMAIN_NODE_SPECS:
        _draw_domain_node(draw, font_mod, _box(region_name), label, color)


def _draw_domain_node(
    draw: Any,
    font_mod: Any,
    box: tuple[int, int, int, int],
    label: str,
    color: str,
) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle((x0, y0, x1, y1), radius=30, fill="#ffffff", outline=color, width=5)
    label_text = label.replace("ALL-SOURCE FUSION", "ALL-SOURCE\nFUSION")
    lines = label_text.split("\n")
    font = _cover_font(font_mod, 30 if len(label) <= 12 else 27)
    line_height = 33
    y = y0 + ((y1 - y0) - len(lines) * line_height) / 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        draw.text((x0 + ((x1 - x0) - (bbox[2] - bbox[0])) / 2, y), line, fill=color, font=font)
        y += line_height


def _draw_tradecraft_core(draw: Any, font_mod: Any, curriculum: Curriculum) -> None:
    x0, y0, x1, y1 = _box("tradecraft_core")
    draw.rounded_rectangle((x0, y0, x1, y1), radius=52, fill="#ffffff", outline="#0f172a", width=7)
    draw.ellipse((x0 + 88, y0 + 42, x1 - 88, y0 + 282), fill="#f8fafc", outline="#94a3b8", width=4)
    draw.text((x0 + 305, y0 + 72), "EVIDENCE LENS", fill="#334155", font=_cover_font(font_mod, 34))
    draw.text((x0 + 178, y0 + 123), "SYNTHETIC ANALYTIC", fill=INK, font=_cover_font(font_mod, 51))
    draw.text((x0 + 305, y0 + 188), "TRADECRAFT", fill=INK, font=_cover_font(font_mod, 64))
    draw.line((x0 + 110, y0 + 286, x1 - 110, y0 + 286), fill="#cbd5e1", width=5)
    draw_wrapped_text(
        draw,
        (x0 + 118, y0 + 298),
        (
            "Synthetic records become reviewable claim packets after "
            "source trace, caveat, and reviewer handoff."
        ),
        _cover_font(font_mod, 31),
        fill=MUTED,
        width=52,
        max_lines=2,
        line_height=39,
    )
    fields = (
        "observation",
        "inference",
        "assumption",
        "likelihood",
        "confidence",
        "dissent",
    )
    for index, field in enumerate(fields):
        row = index // 3
        col = index % 3
        fx0 = x0 + 110 + col * 300
        fy0 = y0 + 424 + row * 58
        color = SOFT_PALETTE[index % len(SOFT_PALETTE)]
        draw.rounded_rectangle((fx0, fy0, fx0 + 250, fy0 + 42), radius=18, fill=color, outline="#94a3b8", width=2)
        draw.text((fx0 + 18, fy0 + 7), field, fill=INK, font=_cover_font(font_mod, 24))
    draw.rounded_rectangle((x0 + 110, y1 - 64, x1 - 110, y1 - 16), radius=20, fill="#ecfeff", outline="#0f766e", width=2)
    draw.text(
        (x0 + 145, y1 - 52),
        "decision boundary: claim, caveat, reviewer, refresh",
        fill="#334155",
        font=_cover_font(font_mod, 26),
    )
    _ = curriculum


def _draw_verification_strip(draw: Any, font_mod: Any) -> None:
    cards = (
        ("verification_citations", "CITATIONS", "Pandoc keys resolve"),
        ("verification_figures_pdf", "FIGURES + PDF", "caption, alt, links"),
        ("verification_metadata", "METADATA", "lane and tier explicit"),
        ("verification_quality", "QUALITY GATES", "stale and boilerplate scans"),
    )
    for index, (region_name, title, body) in enumerate(cards):
        x0, y0, x1, y1 = _box(region_name)
        color = PALETTE[index % len(PALETTE)]
        draw.rounded_rectangle((x0, y0, x1, y1), radius=28, fill="#ffffff", outline=color, width=4)
        draw.text((x0 + 26, y0 + 22), title, fill=color, font=_cover_font(font_mod, 28))
        draw_wrapped_text(
            draw,
            (x0 + 26, y0 + 65),
            body,
            _cover_font(font_mod, 25),
            fill=MUTED,
            width=25,
            max_lines=2,
            line_height=31,
        )


def _draw_source_foundation(draw: Any, font_mod: Any, curriculum: Curriculum) -> None:
    x0, y0, x1, y1 = _box("source_floor")
    draw.rounded_rectangle((x0, y0, x1, y1), radius=40, fill="#0f172a", outline="#1e293b", width=5)
    draw.text((x0 + 60, y0 + 42), "SOURCE SPINE AND EVIDENCE FLOOR", fill="#f8fafc", font=_cover_font(font_mod, 42))
    subtitle = (
        f"{curriculum.stats['parts']} parts | {curriculum.stats['chapters']} modules | "
        f"{curriculum.stats['appendices']} appendices | {curriculum.stats['references']} parsed guide references"
    )
    draw.text((x0 + 60, y0 + 102), subtitle, fill="#cbd5e1", font=_cover_font(font_mod, 30))
    tiles = (
        ("LOCKED KEYS", "ageint001-312 identities remain append-only"),
        ("DIRECT ANCHORS", "official, standards, public-domain, scholarly checks"),
        ("CLAIM LEDGER", "source keys, caveats, alternatives, confidence, owner"),
        ("REFRESH DUTY", "dated review, triggers, negative controls"),
    )
    tile_w = 445
    for index, (title, body) in enumerate(tiles):
        tx0 = x0 + 60 + index * 482
        ty0 = y0 + 175
        draw.rounded_rectangle((tx0, ty0, tx0 + tile_w, ty0 + 112), radius=22, fill="#1e293b", outline="#475569", width=3)
        draw.text((tx0 + 24, ty0 + 18), title, fill="#bfdbfe", font=_cover_font(font_mod, 24))
        draw_wrapped_text(
            draw,
            (tx0 + 24, ty0 + 54),
            body,
            _cover_font(font_mod, 24),
            fill="#e2e8f0",
            width=32,
            max_lines=2,
            line_height=29,
        )


def _draw_cover_footer(draw: Any, font_mod: Any, curriculum: Curriculum) -> None:
    x0, y0, _, _ = _box("footer")
    text = (
        "A rebuildable local atlas: source shards, neutral templates, figure renderers, "
        "citation inventories, validation reports, and PDF audits must agree before the artifact is trusted."
    )
    draw_wrapped_text(
        draw,
        (x0, y0),
        text,
        _cover_font(font_mod, 29),
        fill="#334155",
        width=115,
        max_lines=2,
        line_height=36,
    )
    draw.text(
        (x0, y0 + 86),
        (
            f"Generated from data/curriculum/ with {curriculum.stats['chapters']} modules "
            f"and {curriculum.stats['references']} parsed references."
        ),
        fill="#64748b",
        font=_cover_font(font_mod, 25),
    )


__all__ = [
    "COVER_BOUNDARY_TERMS",
    "COVER_DOMAIN_LABELS",
    "COVER_FOREGROUND_REGIONS",
    "COVER_MIN_FONT_SIZE",
    "COVER_OUTPUT_PATH",
    "render_cover_art",
]
