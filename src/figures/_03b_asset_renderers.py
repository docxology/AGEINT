from __future__ import annotations

import io
from pathlib import Path

from curriculum import Curriculum

from ._01_part import FigureSpec
from ._03_part import (
    _download_bytes,
    _draw_bar_chart,
    _draw_concept_plate,
    _draw_text_plate,
    _font,
    _pil_modules,
)


def _render_historical_figure(root: Path, spec: FigureSpec, output: Path | None = None) -> None:
    if output is None:
        output = root / spec.output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    data = _download_bytes(spec.provenance["asset_url"])
    if data is None:
        _draw_text_plate(
            output,
            spec.title,
            "Official historical image could not be refreshed; provenance remains in registry.",
        )
        return
    image_mod, draw_mod, font_mod, ops_mod = _pil_modules()
    try:
        img_context = image_mod.open(io.BytesIO(data))
    except (OSError, ValueError):
        _draw_text_plate(
            output,
            spec.title,
            "Official historical image response was unreadable; provenance remains in registry.",
        )
        return
    with img_context as img:
        canvas = image_mod.new("RGB", (1600, 1000), "#111827")
        fitted = ops_mod.contain(img.convert("RGB"), (1520, 820))
        x = (1600 - fitted.width) // 2
        canvas.paste(fitted, (x, 40))
        draw = draw_mod.Draw(canvas)
        font = _font(font_mod, 34)
        small = _font(font_mod, 24)
        draw.rectangle((0, 870, 1600, 1000), fill="#f8fafc")
        draw.text((42, 890), spec.title, fill="#111827", font=font)
        draw.text((42, 940), "Source: USGS EROS | Usage: Public Domain", fill="#334155", font=small)
        canvas.save(output, format="PNG", optimize=True)


def _render_ai_concept_figure(root: Path, spec: FigureSpec, output: Path | None = None) -> None:
    prompt = spec.provenance["prompt"]
    visual_text = spec.provenance.get("visual_text", "")
    _draw_concept_plate(output or root / spec.output_path, spec.title, prompt, spec.label, visual_text)


def _render_citation_density(output: Path, curriculum: Curriculum, spec: FigureSpec) -> None:
    values = [len(chapter["citations"]) for chapter in curriculum.chapters]
    labels = [str(chapter["number"]) for chapter in curriculum.chapters]
    _draw_bar_chart(output, spec.title, labels, values, "#2563eb")
