"""Runtime manuscript-variable generation for the AGEINT curriculum atlas."""

from __future__ import annotations

import re
from typing import Any, Final

from curriculum import Curriculum
from citation_workflow import source_citation_cell, source_citation_spine
from markdown_refs import citation_ref, crossref_slug, figure_ref, part_module_map_figure_label, section_ref
from intelligence_content import INTELLIGENCE_RESEARCH_ANCHORS, safe_curriculum_treatment, safe_pattern_rows, safe_pattern_treatment
from intelligence_content._02_part import SOURCE_QUALITY_RESEARCH_ANCHORS
from intelligence_content.source_grounding import safe_source_note as _sg_safe_note, safe_source_title as _sg_safe_title


SOURCE_QUALITY_ANCHORS: Final[list[dict[str, str]]] = [anchor.as_reference() for anchor in SOURCE_QUALITY_RESEARCH_ANCHORS]


def _slug(value: str) -> str:
    """Return a Pandoc-safe lowercase label slug."""
    slug = re.sub(r"[^a-z0-9]+", "_", value.lower()).strip("_")
    return slug or "item"


def section_label(kind: str, title: str, suffix: str = "") -> str:
    """Stable section label without embedding source-guide chapter numbers."""
    suffix_part = f"_{_slug(suffix)}" if suffix else ""
    return f"sec:{_slug(kind)}_{_slug(title)}{suffix_part}"


def citation_spine(citation_numbers: list[int]) -> str:
    """Return a Pandoc citation spine for source-guide reference numbers."""
    return source_citation_spine(citation_numbers)


def _citation_cell(citation_numbers: list[int]) -> str:
    return source_citation_cell(citation_numbers)


def _append_unique(values: list[Any], value: Any) -> None:
    if value not in values:
        values.append(value)


def section_rows(sections: list[dict[str, Any]], *, safe_patterns: bool = False) -> str:
    """Render source-guide subsection rows for a generated chapter."""
    if not sections:
        return "| Curriculum treatment | Source loci | Citation spine |\n|---|---|---|\n| Module-level synthesis | Module source spine | - |"
    grouped: dict[str, dict[str, list[Any]]] = {}
    active_pattern_number: int | None = None
    for section in sections:
        citations = section.get("citations", [])
        source_locus = str(section.get("number") or "module section")
        title = str(section["title"])
        if safe_patterns:
            title, active_pattern_number = safe_pattern_treatment(title, active_pattern_number)
        title = safe_curriculum_treatment(title)
        bucket = grouped.setdefault(title, {"source_loci": [], "citations": []})
        _append_unique(bucket["source_loci"], source_locus)
        for citation in citations:
            _append_unique(bucket["citations"], citation)

    rows = ["| Curriculum treatment | Source loci | Citation spine |", "|---|---|---|"]
    for title, bucket in grouped.items():
        loci = "; ".join(str(value) for value in bucket["source_loci"])
        cite_text = _citation_cell([int(value) for value in bucket["citations"]])
        rows.append(f"| {title} | {loci} | {cite_text} |")
    return "\n".join(rows)


def part_rows(curriculum: Curriculum) -> str:
    """Render the top-level curriculum map."""
    rows = ["| Curriculum area | Part intro | Modules | Unit map | Runtime source |", "|:--------------------------------------|:----------|--------:|:---------|:----------------|"]
    for part in curriculum.parts:
        title = _curriculum_area_title(str(part["title"]))
        part_intro = section_ref(f"sec:part-{crossref_slug(title)}")
        unit_map = figure_ref(part_module_map_figure_label(part))
        rows.append(f"| {title} | {part_intro} | {len(part['chapters'])} | {unit_map} | parsed source guide |")
    return "\n".join(rows)


def _curriculum_area_title(title: str) -> str:
    """Render source guide part titles in a PDF-friendly curriculum-map cell."""
    if not title.isupper():
        return title
    words = []
    acronyms = {"AGEINT", "HUMINT", "SIGINT", "OSINT", "FININT", "ICS"}
    lowercase = {"and", "of", "the", "to", "in"}
    for raw in title.split():
        stripped = raw.strip("()")
        if stripped in acronyms:
            word = stripped
        else:
            word = raw.lower().capitalize()
            if word.lower() in lowercase:
                word = word.lower()
        if raw.startswith("(") and raw.endswith(")"):
            word = f"({word})"
        words.append(word)
    return " ".join(words)


def appendix_rows(appendix: dict[str, Any]) -> str:
    """Render appendix item rows."""
    grouped: dict[str, dict[str, list[Any]]] = {}
    for item in appendix["items"]:
        citations = item.get("citations", [])
        raw_title = str(item["title"])
        title = safe_curriculum_treatment(raw_title)
        bucket = grouped.setdefault(title, {"source_items": [], "citations": []})
        _append_unique(bucket["source_items"], _blocked_appendix_source_label(raw_title, title))
        for citation in citations:
            _append_unique(bucket["citations"], citation)

    rows = ["| Source item / safe study title | Provenance status | Citation context |", "|---|---|---|"]
    for title, bucket in grouped.items():
        source_items = "; ".join(str(value) for value in bucket["source_items"])
        cite_text = _citation_cell([int(value) for value in bucket["citations"]])
        rows.append(f"| {title} | {source_items} | {cite_text} |")
    return "\n".join(rows)


def _blocked_appendix_source_label(raw_title: str, safe_title: str) -> str:
    """Keep appendix provenance without reprinting unsafe learner-facing wording."""
    if raw_title == safe_title:
        # No risky motif needed transforming, so the "blocked source motif" column
        # carries no signal — say so rather than duplicating the safe-treatment cell.
        return "no blocked motif; source title used verbatim"
    prefix = re.match(r"^\s*([A-Z]\.\d+)", raw_title)
    source_id = prefix.group(1) if prefix else "source item"
    return f"{source_id} retained for audit; operational wording transformed"


def pattern_rows(patterns: list[dict[str, Any]]) -> str:
    """Render AGEINT design-pattern rows."""
    return safe_pattern_rows(patterns)


def _source_quality_references() -> list[dict[str, str]]:
    """Return fresh reference records from the canonical source-quality catalog."""
    return [anchor.copy() for anchor in SOURCE_QUALITY_ANCHORS]


def _all_references(references: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [*references, *_source_quality_references(), *(anchor.as_reference() for anchor in INTELLIGENCE_RESEARCH_ANCHORS)]


def bibliography_rows(references: list[dict[str, Any]]) -> str:
    """Render a bibliography atlas table."""
    rows = ["| Citation key | Title | Role | Lane | Tier | Checked | Refresh | Stakeholder | Assurance use | Rights dimension | Source note |", "|---|---|---|---|---|---|---|---|---|---|---|"]
    for ref in _all_references(references):
        # Route note + title through the same cleaners as the .bib emission so the
        # atlas never shows a truncated fragment, [PDF] tag, or dangling title.
        note = _sg_safe_note(str(ref.get("note") or "")) or "Source-guide bibliography entry."
        note = re.sub(r"https?://\S+", "source URL noted in guide", str(note))
        cleaned_title = _sg_safe_title(str(ref["title"])) or str(ref["title"])
        title = re.sub(r"\bChapter\s+(?:[0-9]+(?:\.[0-9]+)*|[IVXLC]+)\s*:\s*", "Source-guide chapter: ", cleaned_title)
        role = ref.get("citation_role") or "source_guide_reference"
        lane = ref.get("source_lane") or "source_guide_reference"
        tier = ref.get("source_tier") or ref.get("source_type") or "source_guide_reference"
        checked = ref.get("checked_as_of") or "source guide import"
        refresh = ref.get("refresh_cadence") or "source guide lifecycle"
        stakeholder = ref.get("stakeholder_role") or "source guide context"
        assurance = ref.get("assurance_use") or "bibliography traceability"
        rights = ref.get("rights_dimension") or "source guide context"
        rows.append(
            f"| {citation_ref(str(ref['key']))} | {_clean_markdown_table_cell(title)} | {_clean_markdown_table_cell(role)} | "
            f"{_clean_markdown_table_cell(lane)} | {_clean_markdown_table_cell(tier)} | "
            f"{_clean_markdown_table_cell(checked)} | {_clean_markdown_table_cell(refresh)} | "
            f"{_clean_markdown_table_cell(stakeholder)} | {_clean_markdown_table_cell(assurance)} | "
            f"{_clean_markdown_table_cell(rights)} | {_clean_markdown_table_cell(note)} |"
        )
    return "\n".join(rows)


def _clean_markdown_table_cell(value: object) -> str:
    """Keep generated bibliography tables plain-text and PDF-renderable."""
    text = re.sub(r"\s+", " ", str(value)).strip()
    replacements = {"🛰": "satellite", "3️⃣": "3", "\ufe0f": "", "\u20e3": "", "|": "/"}
    for old, new in replacements.items():
        text = text.replace(old, new)
    return text
