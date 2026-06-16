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


def _first_cell(rows: Sequence[tuple[str, Sequence[str]]], fallback: str) -> str:
    if not rows:
        return fallback
    cells = list(rows[0][1])
    return cells[0] if cells else fallback


def draw_evidence_dashboard(
    output: Path,
    title: str,
    rows: Sequence[tuple[str, Sequence[str]]],
    cols: Sequence[str],
    primary_fill: str,
    secondary_fill: str,
    *,
    subtitle: str,
    denominator: str,
    failure_path: str,
    reviewer_action: str,
    footer: str,
) -> None:
    image_mod, draw_mod, font_mod = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    width = height = 1400
    canvas = image_mod.new("RGB", (width, height), CANVAS_BG)
    draw = draw_mod.Draw(canvas)
    heading_font = _font(font_mod, 22)
    label_font = _font(font_mod, 21)
    body_font = _font(font_mod, 20)
    small_font = _font(font_mod, 16)
    draw_title_band(
        draw,
        font_mod,
        _font,
        title,
        subtitle="Dashboard: compare denominator, evidence rows, failure path, and reviewer action.",
        width=width,
        height=132,
        accent=primary_fill,
    )
    draw_wrapped_text(
        draw,
        (58, 146),
        subtitle,
        _font(font_mod, 20),
        fill=MUTED,
        width=108,
        max_lines=2,
        line_height=26,
    )

    card_top = 210
    card_height = 166
    card_gap = 18
    card_width = (width - 116 - 3 * card_gap) / 4
    cards = [
        ("Denominator", denominator),
        ("Visible status", _first_cell(rows, "local artifact rows")),
        ("Fail-closed path", failure_path),
        ("Reviewer action", reviewer_action),
    ]
    for index, (card_title, card_body) in enumerate(cards):
        x0 = 58 + index * (card_width + card_gap)
        x1 = x0 + card_width
        fill = "#fff7ed" if index == 2 else "#ffffff"
        outline = "#f59e0b" if index == 2 else GRID
        draw.rounded_rectangle((x0, card_top, x1, card_top + card_height), radius=18, fill=fill, outline=outline, width=3)
        draw.text((x0 + 18, card_top + 16), card_title, fill=INK, font=heading_font)
        draw_wrapped_text(
            draw,
            (x0 + 18, card_top + 54),
            card_body,
            small_font,
            fill=MUTED,
            width=max(16, int((card_width - 36) / 10)),
            max_lines=5,
            line_height=21,
        )

    lane_top = 438
    lane_bottom = 1138
    lane_count = max(1, len(rows))
    lane_gap = 14
    lane_height = (lane_bottom - lane_top - lane_gap * (lane_count - 1)) / lane_count
    label_width = 232
    grid_left = 58 + label_width + 22
    grid_right = width - 58
    first_cells = list(rows[0][1]) if rows else []
    display_cols = tuple(cols[1:]) if first_cells and len(first_cells) == len(cols) - 1 else tuple(cols)
    label_heading = cols[0] if first_cells and len(first_cells) == len(cols) - 1 else "Control lane"
    col_count = max(1, len(display_cols))
    col_gap = 10
    col_width = (grid_right - grid_left - col_gap * (col_count - 1)) / col_count

    draw_wrapped_text(
        draw,
        (96, lane_top - 44),
        label_heading,
        label_font,
        fill=INK,
        width=15,
        max_lines=2,
        line_height=23,
    )
    for col_index, col in enumerate(display_cols):
        x = grid_left + col_index * (col_width + col_gap)
        draw_wrapped_text(
            draw,
            (x + 8, lane_top - 44),
            col,
            label_font,
            fill=INK,
            width=22,
            max_lines=2,
            line_height=23,
        )

    for row_index, (row_label, cells) in enumerate(rows):
        y0 = lane_top + row_index * (lane_height + lane_gap)
        y1 = y0 + lane_height
        lane_fill = "#ffffff" if row_index % 2 == 0 else "#f8fafc"
        draw.rounded_rectangle((58, y0, width - 58, y1), radius=18, fill=lane_fill, outline=GRID, width=2)
        draw.rounded_rectangle((78, y0 + 20, 58 + label_width, y1 - 20), radius=15, fill=primary_fill, outline="#94a3b8", width=2)
        draw_wrapped_text(draw, (96, y0 + 38), row_label, label_font, fill=INK, width=15, max_lines=4, line_height=25)
        cell_values = list(cells)
        for col_index in range(col_count):
            x0 = grid_left + col_index * (col_width + col_gap)
            x1 = x0 + col_width
            cell_text = cell_values[col_index] if col_index < len(cell_values) else ""
            cell_fill = secondary_fill if col_index == 0 else "#ffffff"
            draw.rounded_rectangle(
                (x0, y0 + 20, x1, y1 - 20),
                radius=15,
                fill=cell_fill,
                outline="#cbd5e1",
                width=2,
            )
            draw_wrapped_text(
                draw,
                (x0 + 18, y0 + 38),
                cell_text,
                body_font,
                fill=INK,
                width=max(13, int((col_width - 36) / 10)),
                max_lines=4,
                line_height=25,
            )

    strip_top = 1174
    strip_bottom = 1298
    draw.rounded_rectangle((58, strip_top, width - 58, strip_bottom), radius=18, fill="#fef2f2", outline="#fecaca", width=3)
    draw.text((86, strip_top + 18), "Stop or revise condition", fill="#991b1b", font=heading_font)
    draw_wrapped_text(
        draw,
        (86, strip_top + 54),
        f"{failure_path}. This is local verifier telemetry; it is not a score, benchmark, or empirical performance claim.",
        body_font,
        fill="#7f1d1d",
        width=115,
        max_lines=3,
        line_height=24,
    )
    draw_footer(draw, font_mod, _font, footer, width=width, y=1320)
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
