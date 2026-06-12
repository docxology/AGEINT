from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import re
from typing import Sequence

from curriculum import Curriculum

from ._01_part import FigureKind, FigureSpec
from ._02b_mermaid import mermaid_source

MIN_READER_CAPTION_WORDS = 40
MIN_ALT_TEXT_WORDS = 24


def _with_informative_reader_text(spec: FigureSpec, curriculum: Curriculum) -> FigureSpec:
    """Expand terse captions and alt text using source-owned figure metadata."""

    caption = _expand_caption(spec, curriculum)
    alt_text = _expand_alt_text(spec, curriculum)
    if caption == spec.caption and alt_text == spec.alt_text:
        return spec
    return replace(spec, caption=caption, alt_text=alt_text)


def _expand_caption(spec: FigureSpec, curriculum: Curriculum) -> str:
    if _word_count(spec.caption) >= MIN_READER_CAPTION_WORDS:
        return spec.caption
    detail = _figure_detail(spec, curriculum, limit=4)
    context = _source_context(spec.source_section)
    variants = (
        (
            "It is anchored to {context}; use it to inspect {detail} while preserving "
            "the distinction between curriculum structure, evidence boundary, and authorized practice."
        ),
        (
            "In {context}, it lets readers compare {detail} so the visual functions as "
            "a traceable course aid rather than an unscoped assertion."
        ),
        (
            "Its reader value is to make {detail} visible at a glance, with {context} "
            "as the source section and defensive review as the boundary."
        ),
        (
            "The captioned view belongs to {context} and should be read as a map of "
            "{detail}, not as a capability score or live-task instruction."
        ),
    )
    suffix = variants[_stable_variant(spec.label)].format(context=context, detail=detail)
    return f"{_terminal(spec.caption)} {suffix}"


def _expand_alt_text(spec: FigureSpec, curriculum: Curriculum) -> str:
    if _word_count(spec.alt_text) >= MIN_ALT_TEXT_WORDS:
        return spec.alt_text
    detail = _figure_detail(spec, curriculum, limit=5)
    context = _source_context(spec.source_section)
    return (
        f"{_terminal(spec.alt_text)} Labeled content highlights {detail}, "
        f"with the visual tied back to {context}."
    )


def _figure_detail(spec: FigureSpec, curriculum: Curriculum, *, limit: int) -> str:
    if spec.label == "fig:ageint-curriculum-map":
        return (
            f"{len(curriculum.parts)} part nodes, source-backed module counts, and the reading "
            "path from tradecraft foundations through oversight frameworks"
        )
    if spec.label.startswith("fig:part-") and spec.label.endswith("-module-map"):
        for part in curriculum.parts:
            if spec.title == f"{part['title']} Module Map":
                chapters = [str(chapter["title"]) for chapter in part["chapters"]]
                if chapters:
                    return (
                        f"{len(chapters)} module nodes from {chapters[0]} through {chapters[-1]}, "
                        "plus the unit's ordered source-backed route"
                    )
    if spec.kind is FigureKind.MERMAID:
        labels = _mermaid_labels(mermaid_source(curriculum, spec), limit=limit)
        if labels:
            return _join_items(labels)
    if spec.kind is FigureKind.AI_GENERATED:
        visual_text = spec.provenance.get("visual_text", "")
        labels = [item.strip() for item in visual_text.split("|") if item.strip()]
        if labels:
            return _join_items(labels[:limit])
    if spec.kind is FigureKind.HISTORICAL:
        agency = spec.provenance.get("source_agency", "the source agency")
        date = spec.provenance.get("date", "the documented collection date")
        return (
            f"{agency} provenance, {date} collection context, public-domain status, "
            "and analytic reuse boundary"
        )
    if spec.kind is FigureKind.PYTHON:
        return _python_visual_detail(spec.provenance.get("renderer_id", "figure"))
    return _detail_from_text(f"{spec.alt_text} {spec.caption}", limit=limit)


def _mermaid_labels(source: str, *, limit: int) -> list[str]:
    labels: list[str] = []
    for raw in re.findall(r'\["([^"\n]+)"\]', source):
        label = _clean_label(raw)
        if label and label not in labels:
            labels.append(label)
        if len(labels) >= limit:
            break
    return labels


def _clean_label(raw: str) -> str:
    label = re.sub(r"<br\s*/?>", " ", raw)
    label = re.sub(r"</?b>", "", label)
    label = re.sub(r"\s+", " ", label).strip()
    return label.strip(" .;:")


def _detail_from_text(text: str, *, limit: int) -> str:
    cleaned = re.sub(r"\b(?:diagram|showing|matrix|loop|chart|conceptual)\b", "", text, flags=re.I)
    phrases = [
        phrase.strip(" .;:")
        for phrase in re.split(r",|;|\band\b", cleaned)
        if len(phrase.split()) >= 2
    ]
    deduped: list[str] = []
    for phrase in phrases:
        if phrase and phrase not in deduped:
            deduped.append(phrase)
        if len(deduped) >= limit:
            break
    return _join_items(deduped) if deduped else _generic_detail()


def _source_context(source_section: str) -> str:
    if source_section == "orientation.md":
        return "the curriculum orientation"
    if source_section == "bibliography-atlas.md":
        return "the bibliography atlas"
    if source_section.startswith("appendices/"):
        appendix = Path(source_section).stem.replace("-", " ")
        return f"the {appendix} appendix"
    if source_section.startswith("parts/"):
        parts: list[str] = []
        for part in Path(source_section).parts[1:]:
            stem = Path(part).stem
            if stem in {"00-overview", "unit_intro"}:
                continue
            parts.append(stem.replace("-", " "))
        label = " / ".join(parts[:2]) or "unit"
        return f"the {label} section"
    return source_section.removesuffix(".md").replace("-", " ")


def _python_visual_detail(renderer_id: str) -> str:
    label = renderer_id.replace("_", " ")
    if any(token in renderer_id for token in ("loop", "flow", "lifecycle", "cycle", "workflow")):
        return f"{label} steps, decision gates, owner handoffs, refresh triggers, and closure evidence"
    if any(
        token in renderer_id
        for token in ("matrix", "map", "card", "registry", "audit", "memo", "bank", "backlog")
    ):
        return f"{label} fields, row and column obligations, source records, reviewer decisions, and closure evidence"
    if any(token in renderer_id for token in ("coverage", "density", "spine", "boundary", "taxonomy")):
        return f"{label} categories, denominators, evidence lanes, limitations, and reviewer-use cautions"
    return f"{label} labels, source records, review gates, refresh cues, and reader-use boundaries"


def _join_items(items: Sequence[str]) -> str:
    if not items:
        return _generic_detail()
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + f", and {items[-1]}"


def _generic_detail() -> str:
    return "the labeled controls, evidence objects, review gates, and closure cues"


def _terminal(text: str) -> str:
    stripped = text.strip()
    if stripped.endswith((".", "!", "?")):
        return stripped
    return f"{stripped}."


def _word_count(text: str) -> int:
    return len([word for word in text.replace("/", " ").split() if word.strip()])


def _stable_variant(value: str) -> int:
    return sum(ord(char) for char in value) % 4


__all__ = [
    "MIN_ALT_TEXT_WORDS",
    "MIN_READER_CAPTION_WORDS",
    "_with_informative_reader_text",
]
