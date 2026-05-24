"""Tests for AGEINT generated figure and section cross-reference integrity."""

from __future__ import annotations

import json
from pathlib import Path
import re

from _inventory_helpers import manuscript_dir

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DOCS = PROJECT_ROOT / "docs"
MANUSCRIPT = PROJECT_ROOT / "manuscript"
TOKEN_RE = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}")
FIGURE_DEF_RE = re.compile(r"!\[[^\]]+\]\((?P<path>[^)]+)\)\{#(?P<label>fig:[a-z0-9-]+)\}")
FIGURE_REF_RE = re.compile(r"\[@(?P<label>fig:[a-z0-9-]+)\]")
SECTION_LABEL_RE = re.compile(r"\{#(?P<label>sec:[a-zA-Z0-9_-]+)\}")
SECTION_REF_RE = re.compile(r"\[@(?P<label>sec:[a-zA-Z0-9_-]+)\]")
EQUATION_LABEL_RE = re.compile(r"\{#(?P<label>eq:[a-zA-Z0-9_-]+)\}")
EQUATION_REF_RE = re.compile(r"\[@(?P<label>eq:[a-zA-Z0-9_-]+)\]")
TABLE_LABEL_RE = re.compile(r"\{#(?P<label>tbl:[a-zA-Z0-9_-]+)\}")
TABLE_REF_RE = re.compile(r"\[@(?P<label>tbl:[a-zA-Z0-9_-]+)\]")
CITATION_REF_RE = re.compile(r"\[@(?P<label>(?!fig:|sec:|eq:|tbl:)[A-Za-z][A-Za-z0-9_-]*)\]")
BIB_ENTRY_RE = re.compile(r"^@\w+\{(?P<label>[^,]+),", re.MULTILINE)
HARD_CODED_NUMBER_RE = re.compile(
    r"\b(?:Figure|Fig\.|Section|Sec\.|Equation|Eq\.|Formalism|Chapter)\s+"
    r"(?:[0-9]+(?:\.[0-9]+)*|[IVXLC]+)\b|\bAppendix\s+[A-Z]\b"
)
RAW_LATEX_REF_RE = re.compile(r"\\(?:ref|autoref|cref|Cref|eqref)\{")
FORMALISM_REF_RE = re.compile(r"\b[Ff]ormalisms?\b")


def _markdown_files(output_manuscript: Path) -> list[Path]:
    return sorted(
        path
        for path in output_manuscript.rglob("*.md")
        if path.name not in {"AGENTS.md", "README.md"}
    )


def _reference_scan_files(output_manuscript: Path) -> list[Path]:
    generated = [
        path
        for path in _markdown_files(output_manuscript)
        if "bibliography-atlas" not in path.parts and path.name != "references.md"
    ]
    templates = sorted(
        path
        for path in MANUSCRIPT.rglob("*.md")
        if path.name not in {"AGENTS.md", "README.md"}
    )
    docs = sorted(path for path in DOCS.rglob("*.md") if path.name not in {"AGENTS.md", "README.md"})
    return generated + templates + docs + [PROJECT_ROOT / "README.md", PROJECT_ROOT / "AGENTS.md"]


def _all_output_text(output_manuscript: Path) -> str:
    return "\n\n".join(path.read_text(encoding="utf-8") for path in _markdown_files(output_manuscript))


def _all_bibtex_text(output_manuscript: Path) -> str:
    return "\n\n".join(
        path.read_text(encoding="utf-8") for path in sorted(output_manuscript.glob("*.bib"))
    )


def _generated_crossref_prose_text(output_manuscript: Path) -> str:
    return "\n\n".join(
        path.read_text(encoding="utf-8")
        for path in _markdown_files(output_manuscript)
        if "bibliography-atlas" not in path.parts and path.name != "references.md"
    )


def test_generated_figures_and_references_resolve_through_registry(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    figure_registry = built_output / "figures" / "figure_registry.json"
    text = _all_output_text(output_manuscript)
    registry = json.loads(figure_registry.read_text(encoding="utf-8"))
    registered = {entry["label"] for entry in registry["figures"]}
    definitions = {match.group("label") for match in FIGURE_DEF_RE.finditer(text)}
    references = {match.group("label") for match in FIGURE_REF_RE.finditer(text)}

    assert registered == definitions
    assert references <= definitions
    assert {"fig:ageint-curriculum-map", "fig:ageint-safety-boundary-loop"} <= references


def test_generated_section_references_resolve_without_raw_latex_or_hard_numbers(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    text = _all_output_text(output_manuscript)
    section_labels = {match.group("label") for match in SECTION_LABEL_RE.finditer(text)}
    section_refs = {match.group("label") for match in SECTION_REF_RE.finditer(text)}

    assert section_refs
    assert section_refs <= section_labels
    assert not RAW_LATEX_REF_RE.search(text)
    assert not HARD_CODED_NUMBER_RE.search(_generated_crossref_prose_text(output_manuscript))


def test_generated_equation_table_and_citation_references_resolve(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    text = _all_output_text(output_manuscript)
    bib = _all_bibtex_text(output_manuscript)

    equation_labels = {match.group("label") for match in EQUATION_LABEL_RE.finditer(text)}
    equation_refs = {match.group("label") for match in EQUATION_REF_RE.finditer(text)}
    table_labels = {match.group("label") for match in TABLE_LABEL_RE.finditer(text)}
    table_refs = {match.group("label") for match in TABLE_REF_RE.finditer(text)}
    citation_labels = {match.group("label") for match in CITATION_REF_RE.finditer(text)}
    bib_labels = {match.group("label") for match in BIB_ENTRY_RE.finditer(bib)}

    assert equation_refs <= equation_labels
    assert table_refs <= table_labels
    assert citation_labels
    assert citation_labels <= bib_labels


def test_generated_cross_links_are_label_backed_not_title_prose(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    violations: list[str] = []
    for path in sorted((output_manuscript / "parts").glob("*/*/00-overview.md")):
        if not path.is_file():
            continue
        text = "\n\n".join(
            fragment.read_text(encoding="utf-8")
            for fragment in sorted(path.parent.glob("*.md"))
        )
        cross_links = text.split("## Cross-links", 1)[1].split("\n## ", 1)[0]
        if "[@sec:" not in cross_links or "adjacent AGEINT architecture" in cross_links:
            rel = path.relative_to(PROJECT_ROOT).as_posix()
            violations.append(f"{rel}: {cross_links.strip()}")

    assert violations == []


def test_source_docs_explain_label_backed_reference_syntax() -> None:
    syntax = (MANUSCRIPT / "SYNTAX.md").read_text(encoding="utf-8")
    agents = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")

    assert "[@sec:curriculum_orientation]" in syntax
    assert "[@fig:ageint-curriculum-map]" in syntax
    assert "[@ageint137]" in syntax
    assert "Pandoc-crossref labels" in agents
    assert "label-backed" in readme


def test_manuscript_docs_and_templates_do_not_hard_code_numbered_references(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    violations: list[str] = []
    for path in _reference_scan_files(output_manuscript):
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
            if HARD_CODED_NUMBER_RE.search(line) or RAW_LATEX_REF_RE.search(line) or FORMALISM_REF_RE.search(line):
                rel = path.relative_to(PROJECT_ROOT).as_posix()
                violations.append(f"{rel}:{line_number}: {line.strip()}")

    assert violations == []


def _fragment_paths_for_source_section(output_manuscript: Path, source_section: str) -> list[Path]:
    path = Path(source_section)
    if source_section == "orientation.md":
        return sorted((output_manuscript / "orientation").glob("*.md"))
    if source_section == "bibliography-atlas.md":
        atlas_dir = output_manuscript / "appendices" / "bibliography-atlas"
        if atlas_dir.is_dir():
            return sorted(atlas_dir.glob("*.md"))
    if path.parts[:1] == ("parts",) and path.suffix == ".md" and len(path.parts) == 3:
        chapter_dir = output_manuscript / path.parent / path.stem
        if chapter_dir.is_dir():
            return sorted(chapter_dir.glob("*.md"))
    direct = output_manuscript / source_section
    if direct.is_file():
        return [direct]
    appendix = output_manuscript / "appendices" / source_section
    if appendix.is_file():
        return [appendix]
    return []


def test_overview_fragments_define_local_figures_when_assigned(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    figure_registry = built_output / "figures" / "figure_registry.json"
    registry = json.loads(figure_registry.read_text(encoding="utf-8"))
    by_section: dict[str, list[str]] = {}
    for entry in registry["figures"]:
        by_section.setdefault(entry["source_section"], []).append(entry["label"])

    violations: list[str] = []
    for source_section, labels in sorted(by_section.items()):
        fragments = _fragment_paths_for_source_section(output_manuscript, source_section)
        if not fragments:
            violations.append(f"{source_section}: no output fragments")
            continue
        combined = "\n\n".join(fragment.read_text(encoding="utf-8") for fragment in fragments)
        for label in labels:
            if f"{{#{label}}}" not in combined:
                violations.append(f"{source_section}: missing definition for {label}")
        if "## Figures and course links" in combined and not FIGURE_REF_RE.search(combined):
            violations.append(f"{source_section}: figures block without [@fig:…] references")
    assert violations == []


def test_every_generated_manuscript_file_has_resolved_tokens_and_figure_links(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    for path in _markdown_files(output_manuscript):
        text = path.read_text(encoding="utf-8")
        assert not TOKEN_RE.search(text), path
        if path.name in {"references.md", "preamble.md"}:
            continue
        if "## Figures and course links" in text:
            assert list(FIGURE_REF_RE.finditer(text)), path
