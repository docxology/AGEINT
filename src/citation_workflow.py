"""Composable citation workflow and coverage helpers for AGEINT."""

from __future__ import annotations

from collections import Counter
from collections.abc import Iterable
from dataclasses import dataclass
from pathlib import Path
import re

try:
    from ._slug import curriculum_sections_jsonl_path
    from .curriculum import Curriculum
    from .markdown_refs import citation_ref_list
    from .prose_policy import reader_source_title
except ImportError:  # pragma: no cover - exercised by script-level imports
    from _slug import curriculum_sections_jsonl_path  # type: ignore[no-redef]
    from curriculum import Curriculum  # type: ignore[no-redef]
    from markdown_refs import citation_ref_list  # type: ignore[no-redef]
    from prose_policy import reader_source_title  # type: ignore[no-redef]


def _clean_display_title(title: str) -> str:
    """Lazy proxy for ``clean_display_title`` to avoid a circular import.

    ``intelligence_content`` imports this module at package init, so importing
    ``intelligence_content.topic_entries`` at module top-level would cycle. The
    deferred import resolves cleanly at call time.
    """
    try:
        from intelligence_content.topic_entries import clean_display_title
    except ImportError:  # pragma: no cover - script-level fallback
        return title
    return clean_display_title(title)

_PROJECT_ROOT = Path(__file__).resolve().parents[1]


DEFAULT_SOURCE_FALLBACK = (
    "No direct source-guide citation is attached to this item; "
    "use the surrounding part bibliography and source-guide context."
)
SUPPORT_DOC_NAMES = {"AGENTS.md", "README.md", "references.md"}
CITATION_REF_RE = re.compile(r"(?<!`)\[@([^\]]+)\]")
CROSSREF_PREFIXES = ("fig:", "sec:", "eq:", "tbl:")


@dataclass(frozen=True)
class CitationCountRow:
    """Citation coverage for one source section or generated markdown file."""

    scope: str
    path: str
    title: str
    citation_count: int
    unique_citation_count: int
    citation_keys: tuple[str, ...]
    chapter_number: int | None = None
    chapter_title: str = ""
    section_number: str = ""
    family: str = ""


@dataclass(frozen=True)
class CitationCoverageSummary:
    """Aggregate source-section citation coverage."""

    section_count: int
    citation_occurrences: int
    unique_citation_keys: int
    zero_citation_sections: int
    citation_count_distribution: tuple[tuple[int, int], ...]


def source_key(number: int) -> str:
    """Return the stable ``ageintNNN`` key for a source-guide reference."""

    if number < 1:
        raise ValueError(f"Expected positive source reference number, got {number!r}")
    return f"ageint{number:03d}"


def source_citation_spine(
    numbers: Iterable[int],
    *,
    limit: int | None = None,
    fallback: str = DEFAULT_SOURCE_FALLBACK,
) -> str:
    """Return a compact Pandoc citation spine for source-guide numbers."""

    inline = source_citation_spine_inline(numbers, limit=limit, fallback=fallback)
    if inline == fallback:
        return inline
    return inline + "."


def source_citation_spine_inline(
    numbers: Iterable[int],
    *,
    limit: int | None = None,
    fallback: str = DEFAULT_SOURCE_FALLBACK,
) -> str:
    """Return a compact Pandoc citation spine without sentence punctuation."""

    selected = _unique_numbers(numbers)
    if limit is not None:
        selected = selected[:limit]
    if not selected:
        return fallback
    return citation_ref_list(source_key(number) for number in selected)


def source_citation_cell(numbers: Iterable[int]) -> str:
    """Return a Markdown table cell containing source-guide citations."""

    selected = _unique_numbers(numbers)
    if not selected:
        return "-"
    return citation_ref_list(source_key(number) for number in selected)


def source_section_citation_inventory(curriculum: Curriculum) -> list[CitationCountRow]:
    """Return citation rows for every parsed source-guide section."""

    rows: list[CitationCountRow] = []
    for part in curriculum.parts:
        for chapter in part["chapters"]:
            chapter_number = int(chapter["number"])
            chapter_path = curriculum_sections_jsonl_path(part, chapter)
            for section in chapter.get("sections", []):
                citation_numbers = _unique_numbers(section.get("citations", []))
                citation_keys = tuple(source_key(number) for number in citation_numbers)
                section_number = str(section.get("number") or "module section")
                rows.append(
                    CitationCountRow(
                        scope="source-section",
                        path=chapter_path,
                        title=str(section.get("title", "module section")),
                        citation_count=len(section.get("citations", [])),
                        unique_citation_count=len(citation_keys),
                        citation_keys=citation_keys,
                        chapter_number=chapter_number,
                        chapter_title=str(chapter["title"]),
                        section_number=section_number,
                        family="data/curriculum",
                    )
                )
    return rows


def source_citation_coverage_summary(curriculum: Curriculum) -> CitationCoverageSummary:
    """Return aggregate source-section citation coverage."""

    rows = source_section_citation_inventory(curriculum)
    unique_keys = {key for row in rows for key in row.citation_keys}
    distribution = Counter(row.citation_count for row in rows)
    return CitationCoverageSummary(
        section_count=len(rows),
        citation_occurrences=sum(row.citation_count for row in rows),
        unique_citation_keys=len(unique_keys),
        zero_citation_sections=sum(1 for row in rows if row.citation_count == 0),
        citation_count_distribution=tuple(sorted(distribution.items())),
    )


def render_source_section_citation_rows(curriculum: Curriculum) -> str:
    """Render a source-section citation inventory as a Markdown table."""

    rows = [
        "| Section | Module and source section | Citations | Citation links |",
        "|---:|---|---:|---|",
    ]
    for row in source_section_citation_inventory(curriculum):
        source_context = (
            f"{row.chapter_title} - "
            f"{_clean_display_title(reader_source_title(row.title))}"
        )
        rows.append(
            f"| {_table_cell(row.section_number)} | "
            f"{_table_cell(source_context)} | "
            f"{row.citation_count} | "
            f"{_table_cell(citation_ref_list(row.citation_keys) if row.citation_keys else '-')} |"
        )
    return "\n".join(rows)


def _contributor_recipe_markdown(project_root: Path | None = None) -> str:
    root = _PROJECT_ROOT if project_root is None else Path(project_root)
    doc_path = root / "docs" / "citation_workflow.md"
    text = doc_path.read_text(encoding="utf-8")
    recipe = text.split("## Choose The Source Type", 1)[1].split("## Count And Verify Citations", 1)[0].strip()
    return f"{recipe}\n\nnever hand-edit `output/manuscript/` as the source of truth."


def render_citation_workflow_markdown(curriculum: Curriculum) -> str:
    """Render the canonical generated citation workflow and coverage section."""

    summary = source_citation_coverage_summary(curriculum)
    distribution = ", ".join(
        f"{count} citation(s): {sections} section(s)"
        for count, sections in summary.citation_count_distribution
    )
    return "\n\n".join(
        [
            "## Citation workflow and source-section coverage",
            "AGEINT citations are generated from source data, not patched into generated Markdown.",
            "### Contributor recipe",
            _contributor_recipe_markdown(),
            "### Current source-section coverage",
            "\n".join(
                [
                    "| Measure | Count |",
                    "|---|---:|",
                    f"| Source sections | {summary.section_count} |",
                    f"| Citation occurrences | {summary.citation_occurrences} |",
                    f"| Unique source-guide keys | {summary.unique_citation_keys} |",
                    f"| Zero-citation source sections | {summary.zero_citation_sections} |",
                    f"| Distribution | {_table_cell(distribution)} |",
                ]
            ),
            "### Source-section citation rows",
            render_source_section_citation_rows(curriculum),
        ]
    )


def generated_markdown_citation_inventory(manuscript_dir: Path) -> list[CitationCountRow]:
    """Return citation coverage for generated reader-facing Markdown files."""

    root = Path(manuscript_dir)
    rows: list[CitationCountRow] = []
    for path in sorted(root.rglob("*.md")):
        if path.name in SUPPORT_DOC_NAMES:
            continue
        text = path.read_text(encoding="utf-8")
        keys = tuple(_citation_keys(text))
        rows.append(
            CitationCountRow(
                scope="generated-markdown",
                path=path.relative_to(root).as_posix(),
                title=path.stem,
                citation_count=len(keys),
                unique_citation_count=len(set(keys)),
                citation_keys=tuple(dict.fromkeys(keys)),
                family=_generated_family(path.relative_to(root)),
            )
        )
    return rows


def _citation_keys(text: str) -> list[str]:
    keys: list[str] = []
    for match in CITATION_REF_RE.finditer(text):
        for raw in re.split(r"\s*;\s*", match.group(1)):
            key = raw.strip().split()[0].lstrip("@")
            if key and not key.startswith(CROSSREF_PREFIXES):
                keys.append(key)
    return keys


def _generated_family(path: Path) -> str:
    parts = path.parts
    if parts[0] == "parts":
        if path.name == "unit_intro.md":
            return "part unit intros"
        if len(parts) >= 4:
            stem = path.stem
            if stem.startswith("01-practice-studio"):
                return "practice-studio"
            if stem.startswith("02-evidence-contract"):
                return "evidence-contract"
            if stem.startswith("03-governance-boundary"):
                return "governance-boundary"
            if stem.startswith("04-assessment-route"):
                return "assessment-route"
            return stem.split("-", 1)[1] if "-" in stem else stem
        return "part other"
    if parts[0] in {"orientation", "appendices"}:
        return parts[0]
    return path.name


def _unique_numbers(numbers: Iterable[int]) -> list[int]:
    selected: list[int] = []
    for number in numbers:
        resolved = int(number)
        if resolved not in selected:
            selected.append(resolved)
    return selected


def _table_cell(value: object) -> str:
    return re.sub(r"\s+", " ", str(value)).replace("|", "/").strip()


__all__ = [
    "CitationCountRow",
    "CitationCoverageSummary",
    "generated_markdown_citation_inventory",
    "render_citation_workflow_markdown",
    "render_source_section_citation_rows",
    "source_citation_cell",
    "source_citation_coverage_summary",
    "source_citation_spine",
    "source_key",
    "source_section_citation_inventory",
]
