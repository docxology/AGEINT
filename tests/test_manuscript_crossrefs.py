"""Tests for AGEINT generated figure and section cross-reference integrity."""

from __future__ import annotations

import json
from pathlib import Path
import re

from manuscript_quality.inventory_helpers import manuscript_dir, section_text
from rendered_reference_audit import TitleRule, audit_rendered_references, sanitize_rendered_section_title_mentions

PROJECT_ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = PROJECT_ROOT / "docs" / "manuscript"
TOKEN_RE = re.compile(r"\{\{[A-Z][A-Z0-9_]*\}\}")
FIGURE_DEF_RE = re.compile(r"!\[[^\]]+\]\((?P<path>[^)]+)\)\{#(?P<label>fig:[a-z0-9-]+)\}")
FIGURE_REF_RE = re.compile(r"\[@(?P<label>fig:[a-z0-9-]+)\]")
MARKDOWN_FILE_LINK_RE = re.compile(r"\[[^\]]+\]\([^)]*\.(?:md|markdown)(?:#[^)]*)?\)", re.IGNORECASE)
HTML_MARKDOWN_FILE_LINK_RE = re.compile(r"href=[\"'][^\"']*\.(?:md|markdown)(?:#[^\"']*)?[\"']", re.IGNORECASE)
SECTION_LABEL_RE = re.compile(r"\{#(?P<label>sec:[a-zA-Z0-9_-]+)(?P<attributes>\s+[^}]*)?\}")
SECTION_REF_RE = re.compile(r"\[@(?P<label>sec:[a-zA-Z0-9_-]+)\]")
EQUATION_LABEL_RE = re.compile(r"\{#(?P<label>eq:[a-zA-Z0-9_-]+)\}")
EQUATION_REF_RE = re.compile(r"\[@(?P<label>eq:[a-zA-Z0-9_-]+)\]")
TABLE_LABEL_RE = re.compile(r"\{#(?P<label>tbl:[a-zA-Z0-9_-]+)\}")
TABLE_REF_RE = re.compile(r"\[@(?P<label>tbl:[a-zA-Z0-9_-]+)\]")
CITATION_REF_RE = re.compile(r"\[@(?P<label>(?!fig:|sec:|eq:|tbl:)[A-Za-z][A-Za-z0-9_-]*)\]")
BIB_ENTRY_RE = re.compile(r"^@\w+\{(?P<label>[^,]+),", re.MULTILINE)
RAW_LATEX_REF_RE = re.compile(r"\\(?:ref|autoref|cref|Cref|eqref)\{")
READER_FACING_CROSSREF_PREFIXES = (
    "figPrefix:\n  - Figure\n  - Figures",
    "secPrefix:\n  - Section\n  - Sections",
    "eqnPrefix:\n  - Equation\n  - Equations",
    "tblPrefix:\n  - Table\n  - Tables",
    "nameInLink: true",
)


def _markdown_files(output_manuscript: Path) -> list[Path]:
    return sorted(path for path in output_manuscript.rglob("*.md") if path.name not in {"AGENTS.md", "README.md"})


def _all_output_text(output_manuscript: Path) -> str:
    return "\n\n".join(path.read_text(encoding="utf-8") for path in _markdown_files(output_manuscript))


def _all_bibtex_text(output_manuscript: Path) -> str:
    return "\n\n".join(path.read_text(encoding="utf-8") for path in sorted(output_manuscript.glob("*.bib")))


def _orientation_text(output_manuscript: Path) -> str:
    return "\n\n".join(path.read_text(encoding="utf-8") for path in sorted((output_manuscript / "orientation").glob("*.md")))


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


def test_generated_section_references_resolve_without_raw_latex(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    text = _all_output_text(output_manuscript)
    section_labels = {match.group("label") for match in SECTION_LABEL_RE.finditer(text)}
    section_refs = {match.group("label") for match in SECTION_REF_RE.finditer(text)}
    unnumbered_labels = {match.group("label") for match in SECTION_LABEL_RE.finditer(text) if ".unnumbered" in (match.group("attributes") or "").split()}

    assert section_refs
    assert section_refs <= section_labels
    assert section_refs.isdisjoint(unnumbered_labels)
    assert not RAW_LATEX_REF_RE.search(text)


def test_generated_reader_outputs_do_not_link_to_markdown_files(built_output: Path) -> None:
    """Reader artifacts should link by labels/citations, not source Markdown paths."""

    output_root = built_output
    violations: list[str] = []
    for path in sorted((output_root / "manuscript").rglob("*.md")):
        text = path.read_text(encoding="utf-8")
        for match in MARKDOWN_FILE_LINK_RE.finditer(text):
            rel = path.relative_to(PROJECT_ROOT).as_posix()
            violations.append(f"{rel}: {match.group(0)}")
    web = output_root / "web"
    if web.is_dir():
        for path in sorted(web.glob("*.html")):
            text = path.read_text(encoding="utf-8")
            for match in HTML_MARKDOWN_FILE_LINK_RE.finditer(text):
                rel = path.relative_to(PROJECT_ROOT).as_posix()
                violations.append(f"{rel}: {match.group(0)}")

    assert violations == []


def test_orientation_navigation_surfaces_are_label_backed(built_output: Path) -> None:
    text = _orientation_text(manuscript_dir(built_output))
    required_labels = {
        "sec:reader-paths",
        "sec:consolidated-glossary-and-index",
        "sec:curriculum-map",
        "sec:research-anchor-atlas",
        "sec:source-lane-map",
        "sec:safe-substitution-matrix",
        "sec:capstone-workflow",
        "sec:orientation-figures-and-course-links",
    }
    required_refs = {
        "sec:curriculum-map",
        "sec:bibliography_atlas",
        "sec:source-lane-map",
        "sec:research-anchor-atlas",
        "sec:safe-substitution-matrix",
        "sec:capstone-workflow",
        "sec:orientation-figures-and-course-links",
        "sec:source-refresh-ledger",
        "fig:ageint-curriculum-map",
    }

    for label in required_labels:
        assert f"{{#{label}}}" in text
    for label in required_refs:
        assert f"[@{label}]" in text


def test_curriculum_map_links_each_part_and_unit_map(built_output: Path) -> None:
    [curriculum_map_path] = sorted((manuscript_dir(built_output) / "orientation").glob("*curriculum-map*.md"))
    curriculum_map = curriculum_map_path.read_text(encoding="utf-8")
    part_refs = set(re.findall(r"\[@(sec:part-[a-z0-9-]+)\]", curriculum_map))
    map_refs = set(re.findall(r"\[@(fig:part-[a-z0-9-]+-module-map)\]", curriculum_map))

    assert "| Curriculum area | Part intro | Modules | Unit map | Runtime source |" in curriculum_map
    assert len(part_refs) == 16
    assert len(map_refs) == 16
    assert "| Counterintelligence |" in curriculum_map
    assert "| COUNTERINTELLIGENCE |" not in curriculum_map
    assert not re.search(r"^\| [^|]+ \| [0-9]+ \| parsed source guide \|$", curriculum_map, flags=re.MULTILINE)


def test_reference_key_tables_use_pandoc_citations_not_literal_keys(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    text = _all_output_text(output_manuscript)

    assert "[@official_cia_tradecraft_primer]" in text
    assert "[@scholarly_rethlefsen_2021_prisma_s]" in text
    assert "[@ageint001]" in text
    assert not re.search(r"`@(?:official|scholarly)_[A-Za-z0-9_-]+`", text)
    assert not re.search(r"`@ageint\d{3}`", text)


def test_rendered_reference_audit_allows_only_structural_title_mentions(built_output: Path) -> None:
    violations = audit_rendered_references(built_output)

    assert [violation.format(PROJECT_ROOT) for violation in violations] == []


def test_sanitizer_preserves_domain_names_and_bibliographic_titles() -> None:
    rules = [
        TitleRule("Agent Recruitment", "the module", "chapter", "sec:recruitment"),
        TitleRule("MITRE ATT&CK for ICS", "the module", "chapter", "sec:ics"),
        TitleRule("Social Engineering", "the module", "chapter", "sec:social"),
    ]
    text = "\n".join(
        [
            "Clandestine Agent Recruitment is the source's title.",
            "MITRE ATT&CK for ICS Navigator Layer is a technical artifact.",
            'See "Social Engineering" by the cited author.',
            "The bibliography names **Social Engineering**.",
            "Social Engineering is also a domain term.",
            "See MITRE ATT&CK for ICS Navigator Layer for the artifact.",
        ]
    )
    assert sanitize_rendered_section_title_mentions(text, rules) == text


def test_sanitizer_normalizes_only_navigation_with_label_targets() -> None:
    rule = [TitleRule("Social Engineering", "the module", "chapter", "sec:social")]
    assert sanitize_rendered_section_title_mentions("See Social Engineering for the exercise.", rule) == "See [@sec:social] for the exercise."
    assert sanitize_rendered_section_title_mentions("See **Social Engineering** for the exercise.", rule) == "See [@sec:social] for the exercise."
    unlabelled = [TitleRule("Social Engineering", "the module", "chapter")]
    text = "See Social Engineering for the exercise."
    assert sanitize_rendered_section_title_mentions(text, unlabelled) == text
    assert sanitize_rendered_section_title_mentions("See [@sec:missing].", rule) == "See [@sec:missing]."


def test_reference_audit_distinguishes_domain_terms_from_navigation(tmp_path: Path) -> None:
    manuscript = tmp_path / "manuscript"
    manuscript.mkdir()
    (manuscript / "chapter.md").write_text(
        "# Agent Recruitment {#sec:recruitment}\n"
        "Clandestine Agent Recruitment is a bibliographic title.\n"
        'The source is titled "Agent Recruitment".\n'
        "See Agent Recruitment for the next exercise.\n"
        "See **Agent Recruitment** for the next exercise.\n"
        "See [@sec:recruitment] for valid navigation.\n",
        encoding="utf-8",
    )
    violations = audit_rendered_references(tmp_path)
    assert [(v.reason, v.line_number) for v in violations] == [("unlabelled section navigation", 4), ("unlabelled section navigation", 5)]


def test_reference_audit_rejects_bad_section_refs_even_in_tables(tmp_path: Path) -> None:
    manuscript = tmp_path / "manuscript"
    manuscript.mkdir()
    (manuscript / "chapter.md").write_text(
        "# Topic {#sec:topic}\nSee [@sec:topic; @sec:topic].\n| Missing | [@sec:missing] |\nSee [@sec:bad label].\n```text\n{#sec:fake}\n```\nSee [@sec:fake].\n", encoding="utf-8"
    )
    assert {(v.reason, v.line_number) for v in audit_rendered_references(tmp_path)} == {("unresolved section reference", 3), ("malformed section reference", 4), ("unresolved section reference", 8)}


def test_reference_quality_keeps_markdown_file_link_gate(tmp_path: Path) -> None:
    from reference_quality import collect_reference_quality

    manuscript = tmp_path / "output" / "manuscript"
    manuscript.mkdir(parents=True)
    (manuscript / "chapter.md").write_text("# Topic {#sec:topic}\nSee [the source](missing.md#topic).\n", encoding="utf-8")
    report = collect_reference_quality(tmp_path)
    assert not report.ok
    assert any(row["issue"] == "markdown_file_link" for row in report.payload["issue_rows"])


def test_rendered_reference_audit_allows_pandoc_resolved_html_crossrefs(tmp_path: Path) -> None:
    web = tmp_path / "web"
    web.mkdir()
    (web / "index.html").write_text("<p>Visual guide for the section Figure&nbsp;1.</p>\n<p>Navigation links: Section&nbsp;2, Section&nbsp;3.</p>\n", encoding="utf-8")

    assert audit_rendered_references(tmp_path) == []


def test_rendered_reference_audit_rejects_visible_crossref_placeholders(tmp_path: Path) -> None:
    web = tmp_path / "web"
    web.mkdir()
    (web / "index.html").write_text(
        '<h1 class="unnumbered" id="sec:references">References</h1>\n<p>¿Dónde está el origen?</p>\n<table><tr><td>Section <strong>¿sec:references?</strong></td></tr></table>\n', encoding="utf-8"
    )
    pdf = tmp_path / "pdf"
    pdf.mkdir()
    (pdf / "_combined_manuscript.tex").write_text(r"\section{A formalism \textbf{¿eq:missing?}}" + "\n", encoding="utf-8")

    assert {(violation.path.relative_to(tmp_path).as_posix(), violation.reason, violation.title) for violation in audit_rendered_references(tmp_path)} == {
        ("web/index.html", "unresolved rendered cross-reference", "¿sec:references?"),
        ("pdf/_combined_manuscript.tex", "unresolved rendered cross-reference", "¿eq:missing?"),
    }


def test_rendered_reference_audit_preserves_rendered_authored_emphasis(tmp_path: Path) -> None:
    manuscript = tmp_path / "manuscript"
    manuscript.mkdir()
    (manuscript / "chapter.md").write_text("# Social Engineering\n", encoding="utf-8")
    web = tmp_path / "web"
    web.mkdir()
    (web / "index.html").write_text("<p><strong>History of Social Engineering</strong> teaches defensive recognition.</p>\n", encoding="utf-8")
    pdf = tmp_path / "pdf"
    pdf.mkdir()
    (pdf / "_combined_manuscript.tex").write_text("\\textbf{AI Automation of Social Engineering at\nScale} stays defensive.\n", encoding="utf-8")

    assert audit_rendered_references(tmp_path) == []


def test_rendered_reference_audit_allows_wrapped_tex_section_titles(tmp_path: Path) -> None:
    title = "Governed Intelligence Cycle and Dissemination Architecture frame for The Nature of Intelligence: source context, topic focus, and reader task"
    manuscript = tmp_path / "manuscript"
    manuscript.mkdir()
    (manuscript / "chapter.md").write_text(f"# {title}\n", encoding="utf-8")
    pdf = tmp_path / "pdf"
    pdf.mkdir()
    (pdf / "_combined_manuscript.tex").write_text(
        "\\subsection{Governed Intelligence Cycle and Dissemination Architecture\n"
        "frame for The Nature of Intelligence: source context, topic focus, and\n"
        "reader\n"
        "task}\\label{fixture-heading}\n"
        f"See {title} for the next exercise.\n",
        encoding="utf-8",
    )
    violations = audit_rendered_references(tmp_path)

    assert [(v.reason, v.line_number) for v in violations] == [("unlabelled section navigation", 5)]


def test_rendered_reference_audit_flags_unresolved_citation_key(tmp_path: Path) -> None:
    manuscript = tmp_path / "manuscript"
    parts = manuscript / "parts" / "unit" / "chapter"
    parts.mkdir(parents=True)
    (manuscript / "references-source-guide-001-050.bib").write_text("@misc{ageint001,\n  title = {Real entry},\n}\n", encoding="utf-8")
    (parts / "01-practice-studio.md").write_text(
        "Topic rests on [@ageint001] and [@ageint999].\nCross-refs [@sec:foo] and [@fig:bar] are fine.\nA URL like medium.com/@anil.jain.baba is not a citation.\n", encoding="utf-8"
    )

    violations = audit_rendered_references(tmp_path)
    reasons = {(v.reason, v.title) for v in violations}
    assert ("unresolved citation key", "@ageint999") in reasons
    # Defined key, crossref namespaces, and the bare @user in a URL must not flag.
    assert ("unresolved citation key", "@ageint001") not in reasons
    assert not any(v.reason == "unresolved citation key" and "anil" in v.title for v in violations)
    assert not any(v.reason == "unresolved citation key" and v.title.startswith("@sec") for v in violations)


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
        text = "\n\n".join(fragment.read_text(encoding="utf-8") for fragment in sorted(path.parent.glob("*.md")))
        from manuscript_manifest._heading_titles import chapter_detail_titles
        from manuscript_quality.inventory_helpers import chapter_title_from_text

        cross_links = section_text(text, chapter_detail_titles(chapter_title_from_text(text))["links"])
        if "[@sec:" not in cross_links or "adjacent AGEINT architecture" in cross_links:
            rel = path.relative_to(PROJECT_ROOT).as_posix()
            violations.append(f"{rel}: {cross_links.strip()}")

    assert violations == []


def test_source_docs_explain_label_backed_reference_syntax() -> None:
    syntax = (MANUSCRIPT / "SYNTAX.md").read_text(encoding="utf-8")
    agents = (PROJECT_ROOT / "AGENTS.md").read_text(encoding="utf-8")
    readme = (PROJECT_ROOT / "README.md").read_text(encoding="utf-8")
    citation_workflow = (PROJECT_ROOT / "docs" / "citation_workflow.md").read_text(encoding="utf-8")

    assert "[@sec:curriculum_orientation]" in syntax
    assert "[@fig:ageint-curriculum-map]" in syntax
    assert "[@ageint137]" in syntax
    assert "../docs/citation_workflow.md" in syntax
    assert "docs/citation_workflow.md" in agents
    assert "docs/citation_workflow.md" in readme
    assert "never hand-edit" in citation_workflow
    assert "Pandoc-crossref labels" in agents
    assert "label-backed" in readme


def test_pdf_crossref_metadata_uses_reader_facing_prefixes(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    template = (MANUSCRIPT / "templates" / "abstract.md").read_text(encoding="utf-8")
    rendered = (output_manuscript / "abstract.md").read_text(encoding="utf-8")

    for text in (template, rendered):
        assert text.startswith("---\n")
        for prefix in READER_FACING_CROSSREF_PREFIXES:
            assert prefix in text


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
        if "Figures and course links" in combined and not FIGURE_REF_RE.search(combined):
            violations.append(f"{source_section}: figures block without [@fig:…] references")
    assert violations == []


def test_every_generated_manuscript_file_has_resolved_tokens_and_figure_links(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    for path in _markdown_files(output_manuscript):
        text = path.read_text(encoding="utf-8")
        assert not TOKEN_RE.search(text), path
        if path.name in {"references.md", "preamble.md"}:
            continue
        if "Figures and course links" in text:
            assert list(FIGURE_REF_RE.finditer(text)), path
