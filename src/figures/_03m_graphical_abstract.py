from __future__ import annotations

from pathlib import Path
from typing import Any, Sequence

from ._01_part import FigureSpec
from ._04_part import _font, _pil_modules
from ._05_visual_style import INK, MUTED, PALETTE, SOFT_PALETTE, draw_wrapped_text


def _render_graphical_abstract_atlas(output: Path, spec: FigureSpec) -> None:
    """Render the AGEINT graphical abstract as a high-resolution system atlas."""
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (2400, 2400), "#f8fafc")
    draw = draw_mod.Draw(canvas)

    _draw_background(draw)
    _draw_header(draw, font_mod, spec.title)
    _draw_agent_layer(draw, font_mod)
    _draw_discipline_lanes(draw, font_mod)
    _draw_tradecraft_core(draw, font_mod)
    _draw_human_gate(draw, font_mod)
    _draw_verification_ring(draw, font_mod)
    _draw_source_spine(draw, font_mod)
    _draw_flow_arrows(draw)
    _draw_footer(draw, font_mod)

    canvas.save(output, format="PNG", compress_level=3)


def _draw_background(draw: Any) -> None:
    for offset in range(0, 2401, 120):
        color = "#edf2f7" if offset % 240 else "#e2e8f0"
        draw.line((offset, 0, offset, 2400), fill=color, width=2)
        draw.line((0, offset, 2400, offset), fill=color, width=2)
    draw.rounded_rectangle((70, 70, 2330, 2330), radius=54, outline="#94a3b8", width=5)
    draw.rounded_rectangle((105, 105, 2295, 2295), radius=44, outline="#cbd5e1", width=3)
    for radius, color in ((960, "#dbeafe"), (760, "#dcfce7"), (560, "#fef3c7")):
        draw.ellipse(
            (1200 - radius, 1150 - radius, 1200 + radius, 1150 + radius),
            outline=color,
            width=10,
        )


def _draw_header(draw: Any, font_mod: Any, title: str) -> None:
    draw.rounded_rectangle((170, 145, 2230, 275), radius=36, fill="#ffffff", outline="#cbd5e1", width=3)
    draw.rectangle((170, 145, 205, 275), fill="#0f766e")
    draw.text((245, 170), title.upper(), fill=INK, font=_font(font_mod, 48))
    draw.text(
        (248, 226),
        "Evidence-bounded curriculum architecture for Synthetic Analytic Tradecraft; not a capability benchmark",
        fill=MUTED,
        font=_font(font_mod, 27),
    )


def _draw_agent_layer(draw: Any, font_mod: Any) -> None:
    box = (500, 350, 1900, 650)
    draw.rounded_rectangle(box, radius=42, fill="#ffffff", outline="#7c3aed", width=6)
    draw.text((650, 395), "BOUNDED AGENTIC ASSISTANCE", fill="#4c1d95", font=_font(font_mod, 40))
    draw.text((735, 446), "assist, structure, compare, log, and hand off", fill=MUTED, font=_font(font_mod, 26))
    steps = [
        ("retrieve", "direct sources"),
        ("reason", "alternatives"),
        ("tool", "allowlist"),
        ("memory", "governed"),
        ("handoff", "human gate"),
    ]
    for index, (title, body) in enumerate(steps):
        x0 = 600 + index * 245
        y0 = 510
        draw.rounded_rectangle((x0, y0, x0 + 205, y0 + 90), radius=22, fill="#f5f3ff", outline="#a78bfa", width=3)
        draw.text((x0 + 26, y0 + 16), title.upper(), fill="#5b21b6", font=_font(font_mod, 20))
        draw.text((x0 + 26, y0 + 50), body, fill=INK, font=_font(font_mod, 20))


def _draw_discipline_lanes(draw: Any, font_mod: Any) -> None:
    lanes = [
        ((210, 760, 600, 895), "HUMINT", "authority, source handling, consent"),
        ((210, 930, 600, 1065), "SIGINT", "signals, metadata, legal boundary"),
        ((210, 1100, 600, 1235), "OSINT", "public sources, provenance, refresh"),
        ((210, 1270, 600, 1405), "GEOINT / IMINT", "imagery, geospatial uncertainty"),
        ((1800, 760, 2190, 895), "FININT", "financial trails, sanctions, ownership"),
        ((1800, 930, 2190, 1065), "CYBER / TECHINT", "defensive evidence, no exploit drift"),
        ((1800, 1100, 2190, 1235), "COGNITIVE SECURITY", "inoculation, resilience, epistemic care"),
        ((1800, 1270, 2190, 1405), "GOVERNANCE", "rights, records, oversight, assurance"),
    ]
    for index, (box, title, body) in enumerate(lanes):
        color = PALETTE[index % len(PALETTE)]
        draw.rounded_rectangle(box, radius=28, fill="#ffffff", outline=color, width=5)
        draw.text((box[0] + 28, box[1] + 24), title, fill=color, font=_font(font_mod, 26))
        draw_wrapped_text(
            draw,
            (box[0] + 28, box[1] + 65),
            body,
            _font(font_mod, 22),
            fill=MUTED,
            width=27,
            max_lines=2,
            line_height=27,
        )


def _draw_tradecraft_core(draw: Any, font_mod: Any) -> None:
    box = (690, 745, 1710, 1455)
    draw.rounded_rectangle(box, radius=52, fill="#ffffff", outline="#0f172a", width=7)
    draw.text((830, 805), "SYNTHETIC ANALYTIC", fill=INK, font=_font(font_mod, 45))
    draw.text((905, 858), "TRADECRAFT", fill=INK, font=_font(font_mod, 62))
    draw.line((810, 945, 1590, 945), fill="#cbd5e1", width=4)
    draw_wrapped_text(
        draw,
        (805, 985),
        (
            "Evidence-bounded records and public sources become claim packets: "
            "observation, inference, assumption, likelihood, confidence, dissent, "
            "accountability, caveat, owner, and refresh trigger."
        ),
        _font(font_mod, 29),
        fill=MUTED,
        width=52,
        max_lines=4,
        line_height=37,
    )
    fields = [
        "observation",
        "inference",
        "assumption",
        "likelihood",
        "confidence",
        "dissent",
        "accountability",
        "refresh",
    ]
    for index, field in enumerate(fields):
        row = index // 4
        col = index % 4
        x0 = 780 + col * 225
        y0 = 1175 + row * 70
        draw.rounded_rectangle(
            (x0, y0, x0 + 190, y0 + 48),
            radius=18,
            fill=SOFT_PALETTE[index % len(SOFT_PALETTE)],
            outline="#94a3b8",
            width=2,
        )
        draw.text((x0 + 18, y0 + 12), field, fill=INK, font=_font(font_mod, 21))
    draw.rounded_rectangle((815, 1330, 1585, 1386), radius=22, fill="#f8fafc", outline="#64748b", width=3)
    draw.text((865, 1345), "evidence boundary: cite, caveat, review, or halt", fill="#334155", font=_font(font_mod, 24))


def _draw_human_gate(draw: Any, font_mod: Any) -> None:
    gate = (760, 1510, 1640, 1655)
    draw.rounded_rectangle(gate, radius=34, fill="#fff7ed", outline="#b45309", width=6)
    draw.text((845, 1542), "HUMAN REVIEW GATE", fill="#92400e", font=_font(font_mod, 34))
    draw.text(
        (845, 1588),
        "approve for reviewable product, assign revision, or stop and rebuild",
        fill="#78350f",
        font=_font(font_mod, 24),
    )
    _draw_decision_card(draw, font_mod, (250, 1490, 670, 1665), "HALT", "unsafe wording, weak source, broken link, rights gap, or missing owner", "#be123c")
    _draw_decision_card(draw, font_mod, (1755, 1510, 2125, 1655), "PRODUCT", "source-backed memo, matrix, rubric, or evidence packet", "#0f766e")


def _draw_verification_ring(draw: Any, font_mod: Any) -> None:
    checks = [
        ((250, 1695, 610, 1845), "CITATIONS", "Pandoc keys resolve; no raw markdown-file links"),
        ((650, 1695, 1010, 1845), "FIGURES", "caption, alt text, long description, metadata"),
        ((1050, 1695, 1410, 1845), "PDF", "TOC, URI links, annotations, stale-artifact audit"),
        ((1450, 1695, 1810, 1845), "METADATA", "source lane, tier, checked date, refresh trigger"),
        ((1850, 1695, 2210, 1845), "RED TEAM", "negative controls, boilerplate scans, reviewer challenge"),
    ]
    for index, (box, title, body) in enumerate(checks):
        color = PALETTE[(index + 2) % len(PALETTE)]
        draw.rounded_rectangle(box, radius=26, fill="#ffffff", outline=color, width=4)
        draw.text((box[0] + 28, box[1] + 23), title, fill=color, font=_font(font_mod, 23))
        draw_wrapped_text(
            draw,
            (box[0] + 28, box[1] + 60),
            body,
            _font(font_mod, 20),
            fill=MUTED,
            width=27,
            max_lines=3,
            line_height=24,
        )


def _draw_source_spine(draw: Any, font_mod: Any) -> None:
    box = (210, 1905, 2190, 2185)
    draw.rounded_rectangle(box, radius=38, fill="#0f172a", outline="#1e293b", width=5)
    draw.text((275, 1943), "SOURCE SPINE AND EVIDENCE FLOOR", fill="#f8fafc", font=_font(font_mod, 38))
    draw.text(
        (275, 1995),
        "locked source identities, verified anchors, local figure registry, citation inventory, and rebuildable manuscript outputs",
        fill="#cbd5e1",
        font=_font(font_mod, 24),
    )
    tiles = [
        ("identity", "ageint keys remain stable"),
        ("source", "official, standards, public, scholarly"),
        ("packet", "claim, caveat, evidence, owner"),
        ("refresh", "trigger, date, retest, ledger"),
    ]
    for index, (title, body) in enumerate(tiles):
        x0 = 285 + index * 455
        y0 = 2055
        draw.rounded_rectangle((x0, y0, x0 + 390, y0 + 86), radius=20, fill="#1e293b", outline="#475569", width=3)
        draw.text((x0 + 22, y0 + 16), title.upper(), fill="#bfdbfe", font=_font(font_mod, 20))
        draw.text((x0 + 22, y0 + 48), body, fill="#e2e8f0", font=_font(font_mod, 19))


def _draw_flow_arrows(draw: Any) -> None:
    arrows = [
        ((1200, 650), (1200, 745), "#7c3aed"),
        ((1200, 1455), (1200, 1510), "#0f172a"),
        ((1200, 1655), (1200, 1695), "#b45309"),
        ((1200, 1845), (1200, 1905), "#0f766e"),
        ((600, 830), (690, 910), "#2563eb"),
        ((600, 1168), (690, 1100), "#2563eb"),
        ((1800, 830), (1710, 910), "#0f766e"),
        ((1800, 1168), (1710, 1100), "#0f766e"),
        ((1640, 1582), (1755, 1582), "#0f766e"),
        ((760, 1582), (645, 1582), "#be123c"),
    ]
    for start, end, color in arrows:
        _arrow(draw, start, end, color)


def _draw_footer(draw: Any, font_mod: Any) -> None:
    draw.rounded_rectangle((170, 2215, 2230, 2295), radius=26, fill="#eef2f7", outline="#cbd5e1", width=2)
    draw.text(
        (220, 2238),
        "Reader contract: every visible claim must trace to a source, an artifact, a verifier, a review decision, and a refresh path.",
        fill="#334155",
        font=_font(font_mod, 25),
    )


def _draw_decision_card(
    draw: Any,
    font_mod: Any,
    box: tuple[int, int, int, int],
    title: str,
    body: str,
    color: str,
) -> None:
    draw.rounded_rectangle(box, radius=30, fill="#ffffff", outline=color, width=5)
    draw.text((box[0] + 30, box[1] + 28), title, fill=color, font=_font(font_mod, 31))
    draw_wrapped_text(
        draw,
        (box[0] + 30, box[1] + 74),
        body,
        _font(font_mod, 21),
        fill=MUTED,
        width=27,
        max_lines=3,
        line_height=25,
    )


def _arrow(
    draw: Any,
    start: tuple[int, int],
    end: tuple[int, int],
    color: str,
    *,
    width: int = 8,
) -> None:
    sx, sy = start
    ex, ey = end
    draw.line((sx, sy, ex, ey), fill=color, width=width)
    if abs(ex - sx) > abs(ey - sy):
        points: Sequence[tuple[int, int]]
        if ex >= sx:
            points = ((ex, ey), (ex - 24, ey - 15), (ex - 24, ey + 15))
        else:
            points = ((ex, ey), (ex + 24, ey - 15), (ex + 24, ey + 15))
    elif ey >= sy:
        points = ((ex, ey), (ex - 15, ey - 24), (ex + 15, ey - 24))
    else:
        points = ((ex, ey), (ex - 15, ey + 24), (ex + 15, ey + 24))
    draw.polygon(points, fill=color)


__all__ = ["_render_graphical_abstract_atlas"]
