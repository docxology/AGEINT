"""Structural inventory checks for generated AGEINT manuscript outputs."""

from __future__ import annotations

from pathlib import Path
import re

import pytest

from curriculum import load_curriculum
from manuscript_manifest._heading_titles import chapter_scaffold_titles

# Both packages live only in the sibling docxology/template checkout (see
# src/template_resolver.py, which conftest.py uses to add it to sys.path when
# found nearby). A bare top-level import here would turn "template repo not
# available" into a hard pytest COLLECTION error that aborts the entire run
# for every test file, not just this one's tests — pytest.importorskip
# converts that into a graceful per-module skip instead, matching the
# optional-dependency pattern the rest of this suite already uses for e.g.
# Mermaid/Chrome (`requires_mermaid`). Confirmed live: this repo's own
# standalone GitHub Actions CI has no template checkout on the runner.
infrastructure_rendering = pytest.importorskip("infrastructure.rendering.manuscript_discovery")
manuscript_quality_inventory = pytest.importorskip("manuscript_quality.inventory_helpers")
discover_manuscript_files = infrastructure_rendering.discover_manuscript_files

DATA = manuscript_quality_inventory.DATA
MANUSCRIPT = manuscript_quality_inventory.MANUSCRIPT
REMOVED_REPEATED_MODULE_SECTIONS = manuscript_quality_inventory.REMOVED_REPEATED_MODULE_SECTIONS
RAW_PSEUDO_HEADING_PREFIXES = manuscript_quality_inventory.RAW_PSEUDO_HEADING_PREFIXES
SOURCE_QUALITY_KEYS = manuscript_quality_inventory.SOURCE_QUALITY_KEYS
TEMPLATES = manuscript_quality_inventory.TEMPLATES
chapter_title_from_text = manuscript_quality_inventory.chapter_title_from_text
chapter_text = manuscript_quality_inventory.chapter_text
generated_chapter_files = manuscript_quality_inventory.generated_chapter_files
manuscript_dir = manuscript_quality_inventory.manuscript_dir
required_module_sections_for = manuscript_quality_inventory.required_module_sections_for


RETIRED_TOC_SUFFIXES = (
    "reader task, conceptual primer, outcomes, and vocabulary",
    "topic lessons, safe worked example, and knowledge check",
    "source spine, verified anchors, transfer architecture, and claim limits",
    "synthesis, agent-assistance rules, rights, and assurance gates",
    "capstone artifacts, refresh duties, reviewer challenges, and handoff",
)


def _chapter_title(text: str) -> str:
    return chapter_title_from_text(text)


def test_source_uses_neutral_template_library_without_numbered_modules() -> None:
    payload = load_curriculum(DATA).payload
    template_names = {
        path.name
        for path in TEMPLATES.glob("*.md")
        if path.name not in {"AGENTS.md", "README.md"}
    }

    assert template_names == {
        "abstract.md",
        "appendix.md",
        "bibliography_atlas.md",
        "chapter.md",
        "method_assurance_reference.md",
        "orientation.md",
        "part.md",
        "references.md",
    }
    assert payload["stats"]["chapters"] == 51
    assert not list(MANUSCRIPT.glob("[0-9][0-9]_*.md"))

    chapter_template = (TEMPLATES / "chapter.md").read_text(encoding="utf-8")
    assert "{{SECTION_TITLE}}" in chapter_template
    assert "{{SECTION_BODY}}" in chapter_template
    assert "{{CHAPTER_031_TITLE}}" not in chapter_template
    assert "Foundations of AGEINT" not in chapter_template


def test_generated_output_uses_semantic_paths_without_numbered_modules(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    chapter = (
        output_manuscript
        / "parts"
        / "ageint-agentic-intelligence"
        / "foundations-of-ageint"
        / "00-overview.md"
    )
    assert chapter.is_file()
    assert not list(output_manuscript.rglob("[0-9][0-9]_*.md"))

    text = chapter_text(chapter)
    assert "{{" not in text
    assert "Foundations of AGEINT" in text
    assert "31.1" in text
    assert "[@ageint137]" in text


def test_generated_config_orders_semantic_files(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    ordered = [
        path.relative_to(output_manuscript).as_posix()
        for path in discover_manuscript_files(output_manuscript)
    ]
    assert ordered[:2] == [
        "abstract.md",
        "orientation/00-how-to-use-this-atlas-navigation-path-evidence-checks-and-verifier-handoff-sec-how-to-use-this-atlas.md",
    ]
    assert (
        ordered[2]
        == "orientation/01-synthetic-analytic-tradecraft-thesis-synthetic-fixtures-source-discipline-and-reviewable-claims-sec-synthetic-analytic-tradecraft-thesis.md"
    )
    assert "parts/ageint-agentic-intelligence/unit_intro.md" in ordered
    assert "parts/ageint-agentic-intelligence/foundations-of-ageint/00-overview.md" in ordered
    assert ordered[-1] == "references.md"


def test_bibliography_keys_cover_cited_references_and_source_anchors(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    bib = "\n".join(
        path.read_text(encoding="utf-8") for path in sorted(output_manuscript.glob("*.bib"))
    )
    payload = load_curriculum(DATA).payload
    cited = {
        number
        for part in payload["parts"]
        for chapter in part["chapters"]
        for number in chapter["citations"]
    }
    for number in cited:
        assert f"@misc{{ageint{number:03d}," in bib

    for key in SOURCE_QUALITY_KEYS:
        assert f"@misc{{{key}," in bib


def test_generated_chapter_modules_have_consistent_expansion_sections(built_output: Path) -> None:
    chapter_files = generated_chapter_files(manuscript_dir(built_output))
    assert len(chapter_files) == 51
    for path in chapter_files:
        text = chapter_text(path)
        h2_headings = {
            line.removeprefix("## ").strip()
            for line in text.splitlines()
            if line.startswith("## ") and not line.startswith("### ")
        }
        title = _chapter_title(text)
        assert len(h2_headings) == 3, f"{path.name}: {sorted(h2_headings)}"
        assert any(
            heading.endswith(
                f" frame for {title}: source context, topic focus, and reader task"
            )
            for heading in h2_headings
        ), f"{path.name}: {sorted(h2_headings)}"
        assert any(
            heading.endswith(f" path for {title}: lesson cluster, safe artifact, and review")
            for heading in h2_headings
        ), f"{path.name}: {sorted(h2_headings)}"
        assert (
            f"{title} assurance handoff: evidence, governance, refresh, and capstone"
            in h2_headings
        ), f"{path.name}: {sorted(h2_headings)}"
        for heading in h2_headings:
            assert not any(heading.endswith(suffix) for suffix in RETIRED_TOC_SUFFIXES), (
                path.name,
                heading,
            )
        for scaffold in chapter_scaffold_titles(title).values():
            assert re.search(rf"^### {re.escape(scaffold)}$", text, flags=re.MULTILINE), (
                path.name,
                scaffold,
            )
        required_sections = required_module_sections_for(title)
        missing = {
            section
            for section in required_sections
            if not any(
                line.startswith(("### ", "#### ")) and line.lstrip("#").strip() == section
                for line in text.splitlines()
            )
        }
        assert missing == set(), f"{path.name}: {sorted(missing)}"
        repeated = REMOVED_REPEATED_MODULE_SECTIONS & h2_headings
        assert repeated == set(), f"{path.name}: {sorted(repeated)}"
        generic_h2 = required_sections & h2_headings
        assert generic_h2 == set(), f"{path.name}: generic H2s in PDF TOC: {sorted(generic_h2)}"
        for heading in h2_headings:
            assert not any(prefix in heading for prefix in RAW_PSEUDO_HEADING_PREFIXES), heading


def test_generated_source_lane_titles_are_reader_facing(built_output: Path) -> None:
    body = "\n".join(chapter_text(path) for path in generated_chapter_files(manuscript_dir(built_output)))

    assert "Source-lane evidence, public registers, and claim-ledger studio" in body
    assert "Bounded autonomy, procurement, incident-response, and assurance studio" in body
    assert "Model-card, recoverability, retention, and learner-support evidence package" in body
    assert "AGEINT pattern registry, agent identity, and interface-contract studio" in body
