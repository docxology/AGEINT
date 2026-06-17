from __future__ import annotations

import math
from pathlib import Path
from typing import Any

from ._01_part import FigureSpec
from ._04_part import _font, _pil_modules
from ._05_visual_style import INK, MUTED, PALETTE, SOFT_PALETTE, draw_wrapped_text


CANVAS = 2400


def _render_reader_route_compass(output: Path, spec: FigureSpec) -> None:
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (CANVAS, CANVAS), "#f8fafc")
    draw = draw_mod.Draw(canvas)

    _draw_grid(draw)
    _draw_header(draw, font_mod, spec.title, "Opening navigation: choose the reader path, retain the evidence handoff")
    center = (1200, 1125)
    _draw_compass_core(draw, font_mod, center)
    routes = [
        ("INSTRUCTOR", "sequence, rubric, facilitation", "retain: rubric row + excluded actions", 1200, 455, "#2563eb"),
        ("LEARNER", "primer, studio, capstone packet", "retain: claim ledger + uncertainty note", 1925, 1125, "#0f766e"),
        ("REVIEWER", "source lane, caveat, verifier", "retain: source key + challenge result", 1200, 1795, "#b45309"),
        ("MAINTAINER", "source edit, rebuild, audit", "retain: changed file + validation result", 475, 1125, "#7c3aed"),
    ]
    for title, task, evidence, x, y, color in routes:
        _draw_route_card(draw, font_mod, center, (x, y), title, task, evidence, color)
    _draw_ring_labels(draw, font_mod)
    _draw_footer(
        draw,
        font_mod,
        "Use as a navigation aid only: the compass routes reader duties and evidence handoffs, not learning outcomes or analytic performance.",
    )
    canvas.save(output, format="PNG", compress_level=3)


def _render_synthetic_tradecraft_workbench(output: Path, spec: FigureSpec) -> None:
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (CANVAS, CANVAS), "#f8fafc")
    draw = draw_mod.Draw(canvas)

    _draw_grid(draw)
    _draw_header(draw, font_mod, spec.title, "Synthetic fixture to evidence packet to reviewer gate")
    stages = [
        ("1", "Synthetic fixture", "toy records, public examples, owned-lab logs", "#2563eb"),
        ("2", "Source context", "key, provenance, tier, checked date", "#0f766e"),
        ("3", "Analytic fields", "observation, inference, assumption, confidence", "#b45309"),
        ("4", "Evidence packet", "claim, caveat, alternatives, refresh trigger", "#7c3aed"),
        ("5", "Reviewer gate", "challenge, revise, approve, or halt", "#be123c"),
    ]
    for index, (number, title, body, color) in enumerate(stages):
        x0 = 190 + index * 415
        _draw_workbench_stage(draw, font_mod, (x0, 665, x0 + 335, 1180), number, title, body, color)
        if index < len(stages) - 1:
            _arrow(draw, (x0 + 350, 925), (x0 + 405, 925), "#64748b", width=8)
    _draw_workbench_belts(draw, font_mod)
    _draw_packet_drawer(draw, font_mod)
    _draw_footer(
        draw,
        font_mod,
        "Reader limit: the workbench assembles review-bounded classroom artifacts; it is not field-capability proof or an autonomous action claim.",
    )
    canvas.save(output, format="PNG", compress_level=3)


def _render_source_constellation_map(output: Path, spec: FigureSpec) -> None:
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (CANVAS, CANVAS), "#08111f")
    draw = draw_mod.Draw(canvas)

    _draw_stars(draw)
    _draw_dark_header(draw, font_mod, spec.title, "Evidence families and lane routes for the opening atlas")
    families = [
        ("OFFICIAL", "policy, doctrine, public guidance", 515, 690, "#60a5fa"),
        ("STANDARDS", "risk, safety, accessibility, records", 1575, 690, "#2dd4bf"),
        ("SCHOLARLY", "evaluation, theory, methods, limits", 1780, 1415, "#fbbf24"),
        ("PUBLIC", "declassified, statutory, historical", 1040, 1810, "#f472b6"),
        ("PROFESSIONAL", "practice notes, postmortems, tools", 345, 1415, "#a78bfa"),
    ]
    center = (1200, 1160)
    draw.ellipse((985, 945, 1415, 1375), fill="#f8fafc", outline="#93c5fd", width=7)
    draw.text((1062, 1050), "AGEINT", fill=INK, font=_font(font_mod, 56))
    draw.text((1047, 1118), "source spine", fill="#334155", font=_font(font_mod, 30))
    draw_wrapped_text(
        draw,
        (1040, 1180),
        "claim class -> source lane -> caveat -> refresh duty",
        _font(font_mod, 25),
        fill=MUTED,
        width=26,
        max_lines=2,
        line_height=31,
    )
    for index, (title, body, x, y, color) in enumerate(families):
        _draw_constellation_family(draw, font_mod, center, (x, y), title, body, color, index)
    _draw_source_lanes(draw, font_mod)
    _draw_footer_dark(
        draw,
        font_mod,
        "Interpretation boundary: route density shows reader obligations and source families, not source quality rankings or evidence strength scores.",
    )
    canvas.save(output, format="PNG", compress_level=3)


def _render_assurance_cockpit(output: Path, spec: FigureSpec) -> None:
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (CANVAS, CANVAS), "#0f172a")
    draw = draw_mod.Draw(canvas)

    _draw_cockpit_background(draw)
    _draw_dark_header(draw, font_mod, spec.title, "Local readiness telemetry with publication boundaries kept visible")
    tiles = [
        ("BUILD\nFRESHNESS", "same-source rebuild", "ready when outputs match source", "#22c55e"),
        ("REFERENCE\nQUALITY", "citations and links", "blocked by unresolved or stale refs", "#38bdf8"),
        ("SOURCE\nMETADATA", "lane, tier, refresh", "blocked by blank evidence rows", "#f59e0b"),
        ("FIGURE\nQUALITY", "caption, alt, PNG", "blocked by unreadable or thin assets", "#a78bfa"),
    ]
    for index, (title, subtitle, body, color) in enumerate(tiles):
        x0 = 250 + (index % 2) * 645
        y0 = 535 + (index // 2) * 410
        _draw_status_tile(draw, font_mod, (x0, y0, x0 + 560, y0 + 300), title, subtitle, body, color)
    _draw_readiness_stack(draw, font_mod)
    _draw_boundary_console(draw, font_mod)
    _draw_footer_dark(
        draw,
        font_mod,
        "Cockpit statuses are schematic reader-orientation indicators; authoritative states live in generated audits.",
    )
    canvas.save(output, format="PNG", compress_level=3)


def _draw_header(draw: Any, font_mod: Any, title: str, subtitle: str) -> None:
    draw.rounded_rectangle((105, 105, 2295, 280), radius=42, fill="#ffffff", outline="#cbd5e1", width=4)
    draw.rectangle((105, 105, 147, 280), fill="#0f766e")
    draw.text((190, 145), title.upper(), fill=INK, font=_font(font_mod, 50))
    draw.text((193, 215), subtitle, fill=MUTED, font=_font(font_mod, 27))


def _draw_dark_header(draw: Any, font_mod: Any, title: str, subtitle: str) -> None:
    draw.rounded_rectangle((105, 105, 2295, 280), radius=42, fill="#111827", outline="#334155", width=4)
    draw.rectangle((105, 105, 147, 280), fill="#38bdf8")
    draw.text((190, 145), title.upper(), fill="#f8fafc", font=_font(font_mod, 50))
    draw.text((193, 215), subtitle, fill="#cbd5e1", font=_font(font_mod, 27))


def _draw_grid(draw: Any) -> None:
    for offset in range(0, CANVAS + 1, 120):
        color = "#edf2f7" if offset % 240 else "#e2e8f0"
        draw.line((offset, 0, offset, CANVAS), fill=color, width=2)
        draw.line((0, offset, CANVAS, offset), fill=color, width=2)
    draw.rounded_rectangle((70, 70, 2330, 2330), radius=54, outline="#cbd5e1", width=4)


def _draw_stars(draw: Any) -> None:
    for index in range(130):
        x = (index * 137 + 83) % 2300 + 50
        y = (index * 211 + 157) % 2100 + 260
        r = 2 + index % 4
        color = "#dbeafe" if index % 3 else "#f8fafc"
        draw.ellipse((x - r, y - r, x + r, y + r), fill=color)


def _draw_compass_core(draw: Any, font_mod: Any, center: tuple[int, int]) -> None:
    cx, cy = center
    for radius, color, width in ((540, "#dbeafe", 12), (390, "#ccfbf1", 10), (235, "#fef3c7", 9)):
        draw.ellipse((cx - radius, cy - radius, cx + radius, cy + radius), outline=color, width=width)
    points = [(cx, cy - 360), (cx + 105, cy - 105), (cx + 360, cy), (cx + 105, cy + 105),
              (cx, cy + 360), (cx - 105, cy + 105), (cx - 360, cy), (cx - 105, cy - 105)]
    draw.polygon(points, fill="#ffffff", outline="#0f172a")
    draw.ellipse((cx - 205, cy - 205, cx + 205, cy + 205), fill="#0f172a", outline="#1e293b", width=6)
    draw.text((cx - 108, cy - 68), "START", fill="#f8fafc", font=_font(font_mod, 54))
    draw.text((cx - 142, cy + 4), "route by role", fill="#cbd5e1", font=_font(font_mod, 29))


def _draw_route_card(
    draw: Any,
    font_mod: Any,
    center: tuple[int, int],
    xy: tuple[int, int],
    title: str,
    task: str,
    evidence: str,
    color: str,
) -> None:
    x, y = xy
    card = (x - 285, y - 145, x + 285, y + 145)
    cx, cy = center
    dx = x - cx
    dy = y - cy
    distance = max(math.hypot(dx, dy), 1)
    arrow_start = (int(cx + dx / distance * 225), int(cy + dy / distance * 225))
    _arrow(draw, arrow_start, (x, y), color, width=7)
    draw.rounded_rectangle(card, radius=36, fill="#ffffff", outline=color, width=6)
    draw.text((card[0] + 38, card[1] + 31), title, fill=color, font=_font(font_mod, 32))
    draw_wrapped_text(draw, (card[0] + 38, card[1] + 78), task, _font(font_mod, 24), fill=INK, width=31, max_lines=2)
    draw.line((card[0] + 38, card[1] + 148, card[2] - 38, card[1] + 148), fill="#e2e8f0", width=3)
    draw_wrapped_text(draw, (card[0] + 38, card[1] + 168), evidence, _font(font_mod, 22), fill=MUTED, width=34, max_lines=2)


def _draw_ring_labels(draw: Any, font_mod: Any) -> None:
    labels = [
        ("source lane", 1065, 705, "#2563eb"),
        ("safety gate", 1325, 875, "#0f766e"),
        ("claim packet", 1065, 1490, "#b45309"),
        ("rebuild proof", 700, 875, "#7c3aed"),
    ]
    for text, x, y, color in labels:
        draw.rounded_rectangle((x, y, x + 270, y + 58), radius=24, fill="#f8fafc", outline=color, width=3)
        draw.text((x + 23, y + 17), text.upper(), fill=color, font=_font(font_mod, 20))


def _draw_workbench_stage(
    draw: Any,
    font_mod: Any,
    box: tuple[int, int, int, int],
    number: str,
    title: str,
    body: str,
    color: str,
) -> None:
    draw.rounded_rectangle(box, radius=36, fill="#ffffff", outline=color, width=6)
    draw.ellipse((box[0] + 30, box[1] + 28, box[0] + 100, box[1] + 98), fill=color)
    draw.text((box[0] + 53, box[1] + 42), number, fill="#ffffff", font=_font(font_mod, 32))
    draw_wrapped_text(draw, (box[0] + 34, box[1] + 130), title, _font(font_mod, 35), fill=INK, width=15, max_lines=2, line_height=40)
    draw_wrapped_text(draw, (box[0] + 34, box[1] + 255), body, _font(font_mod, 25), fill=MUTED, width=22, max_lines=4, line_height=31)
    draw.rounded_rectangle((box[0] + 36, box[3] - 95, box[2] - 36, box[3] - 35), radius=20, fill=SOFT_PALETTE[int(number) % len(SOFT_PALETTE)], outline="#cbd5e1", width=2)
    draw.text((box[0] + 60, box[3] - 78), "trace retained", fill="#334155", font=_font(font_mod, 22))


def _draw_workbench_belts(draw: Any, font_mod: Any) -> None:
    draw.rounded_rectangle((160, 1275, 2240, 1510), radius=44, fill="#0f172a", outline="#334155", width=5)
    draw.text((230, 1318), "REVIEW BELT", fill="#f8fafc", font=_font(font_mod, 36))
    belt_items = [
        "source key",
        "caveat",
        "alternative",
        "negative control",
        "rights limit",
        "refresh owner",
    ]
    for index, item in enumerate(belt_items):
        x0 = 545 + index * 255
        draw.rounded_rectangle((x0, 1330, x0 + 205, 1448), radius=22, fill="#1e293b", outline="#475569", width=3)
        draw_wrapped_text(draw, (x0 + 22, 1360), item, _font(font_mod, 23), fill="#e2e8f0", width=15, max_lines=2)


def _draw_packet_drawer(draw: Any, font_mod: Any) -> None:
    draw.rounded_rectangle((250, 1650, 2150, 2045), radius=44, fill="#ffffff", outline="#94a3b8", width=5)
    draw.text((330, 1692), "PACKET DRAWER: what survives the exercise", fill=INK, font=_font(font_mod, 38))
    rows = [
        ("claim", "one bounded statement"),
        ("evidence", "source keys and artifacts"),
        ("uncertainty", "assumptions and confidence basis"),
        ("challenge", "reviewer question and disposition"),
        ("refresh", "trigger, owner, and retest path"),
    ]
    for index, (label, body) in enumerate(rows):
        x0 = 330 + index * 350
        draw.rounded_rectangle((x0, 1790, x0 + 285, 1940), radius=28, fill=SOFT_PALETTE[index % len(SOFT_PALETTE)], outline="#cbd5e1", width=3)
        draw.text((x0 + 25, 1820), label.upper(), fill=INK, font=_font(font_mod, 23))
        draw_wrapped_text(draw, (x0 + 25, 1865), body, _font(font_mod, 20), fill=MUTED, width=21, max_lines=2)


def _draw_constellation_family(
    draw: Any,
    font_mod: Any,
    center: tuple[int, int],
    xy: tuple[int, int],
    title: str,
    body: str,
    color: str,
    index: int,
) -> None:
    x, y = xy
    _arrow(draw, center, (x, y), color, width=5)
    draw.ellipse((x - 172, y - 172, x + 172, y + 172), fill="#111827", outline=color, width=6)
    draw.text((x - 118, y - 58), title, fill=color, font=_font(font_mod, 32))
    draw_wrapped_text(draw, (x - 120, y - 8), body, _font(font_mod, 23), fill="#e2e8f0", width=22, max_lines=3, line_height=29)
    for satellite in range(5):
        angle = (satellite * 72 + index * 17) * math.pi / 180
        sx = x + int(math.cos(angle) * 225)
        sy = y + int(math.sin(angle) * 225)
        draw.ellipse((sx - 18, sy - 18, sx + 18, sy + 18), fill=color)
        draw.line((x + int(math.cos(angle) * 175), y + int(math.sin(angle) * 175), sx, sy), fill=color, width=2)


def _draw_source_lanes(draw: Any, font_mod: Any) -> None:
    lanes = [
        ("governance", 245, 2055, "#60a5fa"),
        ("technical", 625, 2055, "#2dd4bf"),
        ("historical", 1005, 2055, "#fbbf24"),
        ("evaluation", 1385, 2055, "#f472b6"),
        ("assurance", 1765, 2055, "#a78bfa"),
    ]
    for title, x, y, color in lanes:
        draw.rounded_rectangle((x, y, x + 320, y + 96), radius=24, fill="#111827", outline=color, width=3)
        draw.text((x + 32, y + 30), title.upper(), fill=color, font=_font(font_mod, 24))


def _draw_cockpit_background(draw: Any) -> None:
    for offset in range(0, CANVAS + 1, 120):
        color = "#1e293b" if offset % 240 else "#334155"
        draw.line((offset, 0, offset, CANVAS), fill=color, width=1)
        draw.line((0, offset, CANVAS, offset), fill=color, width=1)
    draw.rounded_rectangle((70, 70, 2330, 2330), radius=54, outline="#334155", width=4)
    draw.rounded_rectangle((160, 400, 2240, 2080), radius=62, fill="#111827", outline="#475569", width=5)


def _draw_status_tile(
    draw: Any,
    font_mod: Any,
    box: tuple[int, int, int, int],
    title: str,
    subtitle: str,
    body: str,
    color: str,
) -> None:
    x0, y0, x1, y1 = box
    draw.rounded_rectangle(box, radius=38, fill="#0f172a", outline=color, width=5)
    draw.rounded_rectangle((x0 + 30, y0 + 30, x0 + 168, y0 + 78), radius=18, fill="#111827", outline=color, width=3)
    draw.text((x0 + 58, y0 + 43), "AUDIT", fill=color, font=_font(font_mod, 20))
    for index, line in enumerate(title.splitlines()):
        draw.text((x0 + 35, y0 + 105 + index * 41), line, fill="#f8fafc", font=_font(font_mod, 34))
    draw.text((x0 + 35, y0 + 194), subtitle, fill="#cbd5e1", font=_font(font_mod, 24))
    draw.line((x0 + 35, y0 + 235, x1 - 35, y0 + 235), fill="#334155", width=3)
    draw_wrapped_text(
        draw,
        (x0 + 35, y0 + 252),
        body,
        _font(font_mod, 22),
        fill="#dbeafe",
        width=36,
        max_lines=2,
        line_height=26,
    )


def _draw_gauge(
    draw: Any,
    font_mod: Any,
    center: tuple[int, int],
    title: str,
    subtitle: str,
    value: float,
    color: str,
) -> None:
    cx, cy = center
    box = (cx - 235, cy - 235, cx + 235, cy + 235)
    draw.ellipse(box, fill="#0f172a", outline="#334155", width=10)
    for step in range(0, 11):
        angle = math.radians(210 + step * 12)
        x0 = cx + math.cos(angle) * 168
        y0 = cy + math.sin(angle) * 168
        x1 = cx + math.cos(angle) * 200
        y1 = cy + math.sin(angle) * 200
        draw.line((x0, y0, x1, y1), fill="#64748b", width=4)
    for step in range(0, int(value * 10) + 1):
        angle = math.radians(210 + step * 12)
        x = cx + math.cos(angle) * 198
        y = cy + math.sin(angle) * 198
        draw.ellipse((x - 11, y - 11, x + 11, y + 11), fill=color)
    needle_angle = math.radians(210 + value * 120)
    draw.line((cx, cy, cx + math.cos(needle_angle) * 155, cy + math.sin(needle_angle) * 155), fill=color, width=9)
    draw.ellipse((cx - 18, cy - 18, cx + 18, cy + 18), fill="#f8fafc")
    for index, line in enumerate(title.splitlines()):
        bbox = draw.textbbox((0, 0), line, font=_font(font_mod, 29))
        draw.text((cx - (bbox[2] - bbox[0]) / 2, cy + 62 + index * 34), line, fill="#f8fafc", font=_font(font_mod, 29))
    bbox = draw.textbbox((0, 0), subtitle, font=_font(font_mod, 22))
    draw.text((cx - (bbox[2] - bbox[0]) / 2, cy + 146), subtitle, fill="#cbd5e1", font=_font(font_mod, 22))


def _draw_readiness_stack(draw: Any, font_mod: Any) -> None:
    box = (1555, 525, 2115, 1600)
    draw.rounded_rectangle(box, radius=42, fill="#0f172a", outline="#475569", width=4)
    draw.text((1620, 570), "READINESS STACK", fill="#f8fafc", font=_font(font_mod, 34))
    rows = [
        ("artifact evidence", "current JSON + Markdown"),
        ("source refresh", "no stale checked-as-of rows"),
        ("figure audit", "metadata parity and readable PNGs"),
        ("publication", "local preflight, not a release"),
        ("template validators", "markdown and prerender"),
    ]
    for index, (label, body) in enumerate(rows):
        y = 660 + index * 165
        color = PALETTE[index % len(PALETTE)]
        draw.rounded_rectangle((1625, y, 2045, y + 112), radius=24, fill="#111827", outline=color, width=3)
        draw.text((1650, y + 22), label.upper(), fill=color, font=_font(font_mod, 20))
        draw_wrapped_text(draw, (1650, y + 54), body, _font(font_mod, 19), fill="#dbeafe", width=28, max_lines=2)


def _draw_boundary_console(draw: Any, font_mod: Any) -> None:
    box = (280, 1725, 2120, 2025)
    draw.rounded_rectangle(box, radius=40, fill="#020617", outline="#64748b", width=4)
    draw.text((340, 1770), "PUBLICATION BOUNDARY CONSOLE", fill="#f8fafc", font=_font(font_mod, 34))
    messages = [
        ("READY", "local artifacts agree"),
        ("WARN", "review caveat before reuse"),
        ("BLOCK", "publication, push, or release still requires explicit action"),
    ]
    for index, (status, body) in enumerate(messages):
        x0 = 345 + index * 580
        color = ("#22c55e", "#f59e0b", "#ef4444")[index]
        draw.rounded_rectangle((x0, 1850, x0 + 490, 1955), radius=24, fill="#111827", outline=color, width=4)
        draw.text((x0 + 24, 1878), status, fill=color, font=_font(font_mod, 27))
        draw_wrapped_text(draw, (x0 + 145, 1875), body, _font(font_mod, 21), fill="#e2e8f0", width=25, max_lines=2)


def _draw_footer(draw: Any, font_mod: Any, text: str) -> None:
    draw.rounded_rectangle((140, 2185, 2260, 2288), radius=28, fill="#eef2f7", outline="#cbd5e1", width=2)
    draw_wrapped_text(draw, (205, 2212), text, _font(font_mod, 24), fill="#334155", width=118, max_lines=2, line_height=29)


def _draw_footer_dark(draw: Any, font_mod: Any, text: str) -> None:
    draw.rounded_rectangle((140, 2185, 2260, 2288), radius=28, fill="#111827", outline="#334155", width=2)
    draw_wrapped_text(draw, (205, 2212), text, _font(font_mod, 24), fill="#cbd5e1", width=118, max_lines=2, line_height=29)


def _arrow(
    draw: Any,
    start: tuple[int, int],
    end: tuple[int, int],
    color: str,
    *,
    width: int = 5,
) -> None:
    sx, sy = start
    ex, ey = end
    draw.line((sx, sy, ex, ey), fill=color, width=width)
    angle = math.atan2(ey - sy, ex - sx)
    size = 24
    points = [
        (ex, ey),
        (ex - math.cos(angle - math.pi / 7) * size, ey - math.sin(angle - math.pi / 7) * size),
        (ex - math.cos(angle + math.pi / 7) * size, ey - math.sin(angle + math.pi / 7) * size),
    ]
    draw.polygon(points, fill=color)


__all__ = [
    "_render_assurance_cockpit",
    "_render_reader_route_compass",
    "_render_source_constellation_map",
    "_render_synthetic_tradecraft_workbench",
]
