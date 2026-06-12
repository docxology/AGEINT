from __future__ import annotations

import math
import textwrap
from typing import Any, Sequence

CANVAS_BG = "#f8fafc"
INK = "#0f172a"
MUTED = "#475569"
GRID = "#cbd5e1"
PALETTE = ("#2563eb", "#0f766e", "#b45309", "#7c3aed", "#be123c", "#0369a1", "#4d7c0f")
SOFT_PALETTE = ("#dbeafe", "#ccfbf1", "#fef3c7", "#ede9fe", "#ffe4e6", "#e0f2fe", "#ecfccb")


def wrap_lines(text: str, width: int, max_lines: int | None = None) -> list[str]:
    lines = textwrap.wrap(text, width=width) or [text]
    if max_lines is not None:
        return lines[:max_lines]
    return lines


def draw_title_band(
    draw: Any,
    font_mod: Any,
    font_fn: Any,
    title: str,
    *,
    subtitle: str = "",
    width: int = 1600,
    height: int = 118,
    accent: str = "#2563eb",
) -> None:
    draw.rectangle((0, 0, width, height), fill="#ffffff")
    draw.rectangle((0, 0, 18, height), fill=accent)
    draw.text((52, 24), title, fill=INK, font=font_fn(font_mod, 38))
    if subtitle:
        draw.text((54, 76), subtitle, fill=MUTED, font=font_fn(font_mod, 20))
    draw.line((0, height, width, height), fill=GRID, width=2)


def draw_footer(
    draw: Any,
    font_mod: Any,
    font_fn: Any,
    text: str,
    *,
    width: int = 1600,
    y: int = 930,
) -> None:
    draw.rectangle((0, y, width, y + 70), fill="#eef2f7")
    draw.line((0, y, width, y), fill=GRID, width=2)
    draw.text((50, y + 20), text, fill=MUTED, font=font_fn(font_mod, 20))


def draw_wrapped_text(
    draw: Any,
    xy: tuple[float, float],
    text: str,
    font: Any,
    *,
    fill: str = INK,
    width: int = 28,
    max_lines: int = 3,
    line_height: int = 25,
) -> None:
    x, y = xy
    for index, line in enumerate(wrap_lines(text, width, max_lines)):
        draw.text((x, y + index * line_height), line, fill=fill, font=font)


def draw_centered_text(
    draw: Any,
    box: tuple[float, float, float, float],
    text: str,
    font: Any,
    *,
    fill: str = INK,
    width: int = 20,
    max_lines: int = 3,
    line_height: int = 27,
) -> None:
    x0, y0, x1, y1 = box
    lines = wrap_lines(text, width, max_lines)
    total_h = len(lines) * line_height
    y = y0 + ((y1 - y0) - total_h) / 2
    for line in lines:
        bbox = draw.textbbox((0, 0), line, font=font)
        x = x0 + ((x1 - x0) - (bbox[2] - bbox[0])) / 2
        draw.text((x, y), line, fill=fill, font=font)
        y += line_height


def draw_arrow(
    draw: Any,
    start: tuple[float, float],
    end: tuple[float, float],
    *,
    fill: str = "#334155",
    width: int = 5,
) -> None:
    sx, sy = start
    ex, ey = end
    draw.line((sx, sy, ex, ey), fill=fill, width=width)
    angle = math.atan2(ey - sy, ex - sx)
    size = 18
    points = [
        (ex, ey),
        (ex - math.cos(angle - math.pi / 7) * size, ey - math.sin(angle - math.pi / 7) * size),
        (ex - math.cos(angle + math.pi / 7) * size, ey - math.sin(angle + math.pi / 7) * size),
    ]
    draw.polygon(points, fill=fill)
