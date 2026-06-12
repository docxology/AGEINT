"""Structural inventory checks for generated AGEINT manuscript outputs."""

from __future__ import annotations

from pathlib import Path

from infrastructure.rendering.manuscript_discovery import discover_manuscript_files
from curriculum import load_curriculum

from manuscript_quality.inventory_helpers import (
    DATA,
    MANUSCRIPT,
    REMOVED_REPEATED_MODULE_SECTIONS,
    REQUIRED_MODULE_SECTIONS,
    RAW_PSEUDO_HEADING_PREFIXES,
    SOURCE_QUALITY_KEYS,
    TEMPLATES,
    chapter_text,
    generated_chapter_files,
    manuscript_dir,
)


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
        "orientation/00-runtime-inventory-sec-runtime-inventory.md",
    ]
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
        missing = REQUIRED_MODULE_SECTIONS - h2_headings
        assert missing == set(), f"{path.name}: {sorted(missing)}"
        repeated = REMOVED_REPEATED_MODULE_SECTIONS & h2_headings
        assert repeated == set(), f"{path.name}: {sorted(repeated)}"
        for heading in h2_headings:
            assert not any(prefix in heading for prefix in RAW_PSEUDO_HEADING_PREFIXES), heading


def test_generated_source_lane_titles_are_reader_facing(built_output: Path) -> None:
    body = "\n".join(chapter_text(path) for path in generated_chapter_files(manuscript_dir(built_output)))

    assert "Source-lane evidence, public registers, and claim-ledger studio" in body
    assert "Bounded autonomy, procurement, incident-response, and assurance studio" in body
    assert "Model-card, recoverability, retention, and learner-support evidence package" in body
    assert "AGEINT pattern registry, agent identity, and interface-contract studio" in body
