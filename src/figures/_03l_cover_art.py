from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from curriculum import Curriculum

from ._04_part import _font, _pil_modules, _validate_png_asset
from ._05_visual_style import INK, MUTED, PALETTE, SOFT_PALETTE, draw_wrapped_text

COVER_OUTPUT_PATH = Path("output/figures/cover/ageint-cover-synthesis.png")


def render_cover_art(project_root: Path, curriculum: Curriculum) -> Path:
    """Render the non-numbered AGEINT cover image and metadata sidecar."""

    root = Path(project_root)
    output = root / COVER_OUTPUT_PATH
    output.parent.mkdir(parents=True, exist_ok=True)
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    pnginfo_mod = __import__("PIL.PngImagePlugin", fromlist=["PngInfo"])

    size = 2400
    canvas = image_mod.new("RGB", (size, size), "#f7fafc")
    draw = draw_mod.Draw(canvas)

    _draw_background_grid(draw, size)
    _draw_outer_system_ring(draw, font_mod)
    _draw_source_foundation(draw, font_mod, curriculum)
    _draw_tradecraft_core(draw, font_mod, curriculum)
    _draw_agentic_layer(draw, font_mod)
    _draw_verification_ring(draw, font_mod)
    _draw_safety_ribbon(draw, font_mod)
    _draw_cover_footer(draw, font_mod, curriculum)

    png_info = pnginfo_mod.PngInfo()
    metadata = _cover_metadata(curriculum)
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


def _cover_metadata(curriculum: Curriculum) -> dict[str, Any]:
    return {
        "kind": "cover_art",
        "non_numbered": True,
        "title": "AGEINT Cover Synthesis",
        "output_path": COVER_OUTPUT_PATH.as_posix(),
        "description": (
            "Deterministic non-numbered cover image for the AGEINT PDF title page. "
            "The visual maps source spine, Synthetic Analytic Tradecraft, bounded "
            "agentic assistance, verification, and safety constraints without "
            "claiming measured performance."
        ),
        "provenance": {
            "renderer": "python_pillow",
            "source": "data/curriculum/",
            "parts": str(curriculum.stats["parts"]),
            "modules": str(curriculum.stats["chapters"]),
            "appendices": str(curriculum.stats["appendices"]),
            "references": str(curriculum.stats["references"]),
        },
    }


def _draw_background_grid(draw: Any, size: int) -> None:
    for offset in range(0, size + 1, 120):
        color = "#e8eef6" if offset % 240 else "#dbe5f0"
        draw.line((offset, 0, offset, size), fill=color, width=2)
        draw.line((0, offset, size, offset), fill=color, width=2)
    draw.rectangle((52, 52, size - 52, size - 52), outline="#94a3b8", width=4)
    draw.rectangle((78, 78, size - 78, size - 78), outline="#cbd5e1", width=2)


def _draw_source_foundation(draw: Any, font_mod: Any, curriculum: Curriculum) -> None:
    x0, y0, x1, y1 = 200, 1830, 2200, 2160
    draw.rounded_rectangle((x0, y0, x1, y1), radius=38, fill="#0f172a", outline="#1e293b", width=5)
    draw.text((260, y0 + 42), "SOURCE SPINE AND EVIDENCE FLOOR", fill="#f8fafc", font=_font(font_mod, 42))
    subtitle = (
        f"{curriculum.stats['parts']} parts | {curriculum.stats['chapters']} modules | "
        f"{curriculum.stats['appendices']} appendices | {curriculum.stats['references']} parsed guide references"
    )
    draw.text((260, y0 + 102), subtitle, fill="#cbd5e1", font=_font(font_mod, 28))
    tiles = [
        ("locked keys", "ageint001-312 identities remain append-only"),
        ("direct anchors", "official, standards, public-domain, and scholarly checks"),
        ("claim ledger", "source keys, caveats, alternatives, confidence, owner"),
        ("refresh duty", "dated source review, triggers, and negative controls"),
    ]
    tile_w = 450
    for index, (title, body) in enumerate(tiles):
        tx0 = 260 + index * 470
        ty0 = y0 + 168
        draw.rounded_rectangle((tx0, ty0, tx0 + tile_w, ty0 + 108), radius=20, fill="#1e293b", outline="#475569", width=3)
        draw.text((tx0 + 24, ty0 + 18), title.upper(), fill="#bfdbfe", font=_font(font_mod, 22))
        draw_wrapped_text(draw, (tx0 + 24, ty0 + 52), body, _font(font_mod, 22), fill="#e2e8f0", width=33, max_lines=2, line_height=26)


def _draw_outer_system_ring(draw: Any, font_mod: Any) -> None:
    center = (1200, 1100)
    rings = [
        (900, "#dbeafe", "#2563eb"),
        (730, "#dcfce7", "#0f766e"),
        (565, "#fef3c7", "#b45309"),
        (405, "#ede9fe", "#7c3aed"),
    ]
    for radius, fill, outline in rings:
        box = (center[0] - radius, center[1] - radius, center[0] + radius, center[1] + radius)
        draw.ellipse(box, fill=fill, outline=outline, width=6)
    nodes = [
        (1200, 225, "HUMINT", PALETTE[0]),
        (1735, 430, "SIGINT", PALETTE[1]),
        (2015, 1015, "OSINT\nGEOINT", PALETTE[2]),
        (1740, 1615, "FININT\nCI", PALETTE[3]),
        (675, 1615, "CYBER\nICS", PALETTE[4]),
        (385, 1015, "COGNITIVE\nSECURITY", PALETTE[5]),
        (665, 430, "ALL-SOURCE\nFUSION", PALETTE[6]),
    ]
    for x, y, label, color in nodes:
        _draw_node(draw, font_mod, (x, y), label, color)


def _draw_tradecraft_core(draw: Any, font_mod: Any, curriculum: Curriculum) -> None:
    box = (740, 720, 1660, 1485)
    draw.rounded_rectangle(box, radius=50, fill="#ffffff", outline="#0f172a", width=6)
    draw.text((875, 812), "SYNTHETIC ANALYTIC", fill=INK, font=_font(font_mod, 48))
    draw.text((940, 872), "TRADECRAFT", fill=INK, font=_font(font_mod, 62))
    draw.line((865, 950, 1535, 950), fill="#cbd5e1", width=4)
    draw_wrapped_text(
        draw,
        (858, 990),
        (
            "Synthetic records, public examples, owned-lab logs, and classroom "
            "tabletops become reviewable evidence packets before any claim is trusted."
        ),
        _font(font_mod, 31),
        fill=MUTED,
        width=46,
        max_lines=4,
        line_height=40,
    )
    fields = [
        "observation",
        "inference",
        "assumption",
        "likelihood",
        "confidence",
        "dissent",
    ]
    for index, field in enumerate(fields):
        row = index // 2
        col = index % 2
        x0 = 830 + col * 390
        y0 = 1185 + row * 60
        color = SOFT_PALETTE[index % len(SOFT_PALETTE)]
        draw.rounded_rectangle((x0, y0, x0 + 340, y0 + 42), radius=18, fill=color, outline="#94a3b8", width=2)
        draw.text((x0 + 18, y0 + 9), field, fill=INK, font=_font(font_mod, 22))
    draw.rounded_rectangle((830, 1370, 1570, 1418), radius=20, fill="#f8fafc", outline="#94a3b8", width=2)
    draw.text(
        (858, 1382),
        "decision boundary: claim, caveat, reviewer, refresh",
        fill="#334155",
        font=_font(font_mod, 22),
    )
    draw.text(
        (920, 1432),
        f"Pattern library: {curriculum.stats['patterns']} governed AGEINT patterns",
        fill="#475569",
        font=_font(font_mod, 21),
    )


def _draw_agentic_layer(draw: Any, font_mod: Any) -> None:
    box = (560, 250, 1840, 560)
    draw.rounded_rectangle(box, radius=44, fill="#ffffff", outline="#7c3aed", width=6)
    draw.text((690, 300), "BOUNDED AGENTIC ASSISTANCE", fill="#4c1d95", font=_font(font_mod, 42))
    steps = [
        ("perceive", "retrieve and structure"),
        ("reason", "compare hypotheses"),
        ("use tools", "allowlisted only"),
        ("remember", "governed memory"),
        ("handoff", "human review"),
    ]
    for index, (title, body) in enumerate(steps):
        x0 = 625 + index * 240
        y0 = 380
        draw.rounded_rectangle((x0, y0, x0 + 205, y0 + 105), radius=24, fill="#f5f3ff", outline="#a78bfa", width=3)
        draw.text((x0 + 22, y0 + 17), title.upper(), fill="#5b21b6", font=_font(font_mod, 20))
        draw_wrapped_text(draw, (x0 + 22, y0 + 50), body, _font(font_mod, 19), fill=INK, width=18, max_lines=2, line_height=23)


def _draw_verification_ring(draw: Any, font_mod: Any) -> None:
    items = [
        ("citations", "Pandoc keys resolve"),
        ("figures", "caption, alt text, registry"),
        ("PDF", "links, TOC, no file actions"),
        ("metadata", "lane and tier explicit"),
        ("quality", "boilerplate and stale output scans"),
    ]
    for index, (title, body) in enumerate(items):
        x0 = 360 + index * 340
        y0 = 1500
        draw.rounded_rectangle((x0, y0, x0 + 280, y0 + 150), radius=28, fill="#ffffff", outline="#7c3aed", width=4)
        draw.text((x0 + 28, y0 + 24), title.upper(), fill="#5b21b6", font=_font(font_mod, 22))
        draw_wrapped_text(draw, (x0 + 28, y0 + 63), body, _font(font_mod, 21), fill=MUTED, width=22, max_lines=3, line_height=26)


def _draw_safety_ribbon(draw: Any, font_mod: Any) -> None:
    x0, y0, x1, y1 = 235, 610, 2165, 690
    draw.rounded_rectangle((x0, y0, x1, y1), radius=30, fill="#fff1f2", outline="#be123c", width=4)
    text = "DEFENSIVE | EDUCATIONAL | AUTHORIZED | SYNTHETIC | NON-OPERATIONAL"
    bbox = draw.textbbox((0, 0), text, font=_font(font_mod, 33))
    draw.text((1200 - (bbox[2] - bbox[0]) / 2, y0 + 21), text, fill="#9f1239", font=_font(font_mod, 33))


def _draw_cover_footer(draw: Any, font_mod: Any, curriculum: Curriculum) -> None:
    text = (
        "A rebuildable local atlas: source shards, neutral templates, figure renderers, "
        "citation inventories, validation reports, and PDF audits must agree before the artifact is trusted."
    )
    draw_wrapped_text(draw, (220, 2225), text, _font(font_mod, 27), fill="#334155", width=118, max_lines=2, line_height=34)
    draw.text(
        (220, 2295),
        f"Generated from data/curriculum/ with {curriculum.stats['chapters']} modules and {curriculum.stats['references']} parsed references.",
        fill="#64748b",
        font=_font(font_mod, 22),
    )


def _draw_node(draw: Any, font_mod: Any, center: tuple[int, int], label: str, color: str) -> None:
    x, y = center
    draw.ellipse((x - 124, y - 82, x + 124, y + 82), fill="#ffffff", outline=color, width=6)
    lines = label.split("\n")
    y_start = y - (len(lines) * 25)
    for index, line in enumerate(lines):
        font = _font(font_mod, 26 if len(line) <= 9 else 22)
        bbox = draw.textbbox((0, 0), line, font=font)
        draw.text((x - (bbox[2] - bbox[0]) / 2, y_start + index * 50), line, fill=color, font=font)


__all__ = ["COVER_OUTPUT_PATH", "render_cover_art"]
