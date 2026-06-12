from __future__ import annotations

from importlib import import_module
from pathlib import Path
import textwrap
from typing import Any, Sequence

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


def draw_control_matrix(
    output: Path,
    title: str,
    rows: Sequence[tuple[str, Sequence[str]]],
    cols: Sequence[str],
    primary_fill: str,
    secondary_fill: str,
) -> None:
    image_mod, draw_mod, font_mod = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (1400, 1400), CANVAS_BG)
    draw = draw_mod.Draw(canvas)
    header_font = _font(font_mod, 22)
    row_font = _font(font_mod, 21)
    cell_font = _font(font_mod, 18)
    draw_title_band(
        draw,
        font_mod,
        _font,
        title,
        subtitle="Audit table; cells are review prompts, not measured capability claims.",
        width=1400,
        height=132,
        accent=primary_fill,
    )
    left = 270
    top = 225
    right = 1340
    bottom = 1280
    row_h = (bottom - top) // len(rows)
    cell_w = (right - left) // len(cols)
    for col_index, col in enumerate(cols):
        x = left + col_index * cell_w
        draw.text((x + 12, top - 42), col, fill=INK, font=header_font)
    for row_index, (row_label, cells) in enumerate(rows):
        y = top + row_index * row_h
        draw.rounded_rectangle((58, y + 8, left - 22, y + row_h - 10), radius=8, fill="#e2e8f0", outline=GRID)
        for line_index, line in enumerate(textwrap.wrap(row_label, width=18)[:3]):
            draw.text((76, y + 24 + line_index * 26), line, fill="#1e293b", font=row_font)
        for col_index, cell in enumerate(cells):
            x = left + col_index * cell_w
            fill = primary_fill if (row_index + col_index) % 2 == 0 else secondary_fill
            draw.rounded_rectangle(
                (x + 6, y + 8, x + cell_w - 8, y + row_h - 10),
                radius=8,
                fill=fill,
                outline=MUTED,
                width=2,
            )
            for line_index, line in enumerate(textwrap.wrap(cell, width=17)[:4]):
                draw.text((x + 20, y + 30 + line_index * 24), line, fill=INK, font=cell_font)
    draw_footer(draw, font_mod, _font, "Source: AGEINT figure renderer | Matrix is a qualitative audit surface.", width=1400, y=1320)
    canvas.save(output, format="PNG", optimize=True)


def draw_matrix(output: Path, title: str, rows: Sequence[str], cols: Sequence[str]) -> None:
    image_mod, draw_mod, font_mod = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (1600, 1200), CANVAS_BG)
    draw = draw_mod.Draw(canvas)
    draw_title_band(
        draw,
        font_mod,
        _font,
        title,
        subtitle="Qualitative matrix; shaded cells mark designed review coverage.",
        width=1600,
        height=126,
        accent=PALETTE[0],
    )
    x0, y0 = 430, 190
    right = 1510
    cell_w = max(118, (right - x0) // max(1, len(cols)))
    cell_h = max(50, min(74, (900 - y0) // max(1, len(rows))))
    for col_index, col in enumerate(cols):
        x = x0 + col_index * cell_w
        draw_centered_text(draw, (x, y0 - 62, x + cell_w - 8, y0 - 8), col, _font(font_mod, 20), width=14, max_lines=2)
    for row_index, row in enumerate(rows):
        y = y0 + row_index * cell_h
        draw_wrapped_text(draw, (60, y + 11), row, _font(font_mod, 19), fill=MUTED, width=32, max_lines=2, line_height=22)
        for col_index, _ in enumerate(cols):
            x = x0 + col_index * cell_w
            shade = SOFT_PALETTE[(row_index + col_index) % len(SOFT_PALETTE)]
            outline = PALETTE[col_index % len(PALETTE)]
            draw.rounded_rectangle((x, y, x + cell_w - 8, y + cell_h - 8), radius=7, fill=shade, outline=outline, width=2)
    draw_footer(draw, font_mod, _font, "Source: AGEINT renderer | Matrix entries are review surfaces, not scores.", width=1600, y=1110)
    canvas.save(output, format="PNG", optimize=True)


def _pil_modules() -> tuple[Any, Any, Any]:
    return (
        import_module("PIL.Image"),
        import_module("PIL.ImageDraw"),
        import_module("PIL.ImageFont"),
    )


def _font(font_mod: Any, size: int) -> Any:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).is_file():
            return font_mod.truetype(candidate, size)
    return font_mod.load_default()
