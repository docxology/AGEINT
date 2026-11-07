"""Tests for generated heading reference-support auditing."""

from __future__ import annotations

from pathlib import Path

import pytest

from _markdown_split import split_by_line_budget

from manuscript_quality.inventory_helpers import manuscript_dir
from rendered_heading_support import add_heading_support, heading_support_inventory, heading_support_summary, unsupported_heading_rows


def test_heading_navigation_does_not_borrow_another_blocks_citation() -> None:
    rendered = (
        "# Sample {#sec:sample}\n\n"
        "Search reporting follows [@scholarly_rethlefsen_2021_prisma_s].\n\n"
        "## Safety and mastery rules\n\n"
        "| Rule | Required artifact |\n|---|---|\n| Stop | Review record |\n"
    )
    revised = add_heading_support(rendered)
    assert revised.count("[@scholarly_rethlefsen_2021_prisma_s]") == 1
    safety_block = revised.split("## Safety and mastery rules", 1)[1]
    assert "[@sec:sample]" in safety_block
    assert "scholarly_rethlefsen_2021_prisma_s" not in safety_block
    assert add_heading_support(revised) == revised


@pytest.mark.parametrize("section_text", [None, "# Parent without a label\n", "```markdown\n# Parent {#sec:fake}\n```\n"])
def test_heading_without_real_target_is_not_given_an_invented_reference(section_text: str | None) -> None:
    rendered = "## Capstone rubric\n\nAuthor-defined criteria need review.\n"
    revised = add_heading_support(rendered, section_text=section_text)
    assert "[@sec:" not in revised
    assert unsupported_heading_rows_for_text(revised) == ["Capstone rubric"]


def test_local_heading_label_is_navigation_not_evidence(tmp_path: Path) -> None:
    (tmp_path / "sample.md").write_text("# Sample {#sec:sample}\n\n## Rule\n\nThis author-defined rule has no supporting source.\n", encoding="utf-8")
    rows = heading_support_inventory(tmp_path)
    assert rows[0].supported
    assert rows[0].support_refs == ("{#sec:sample}",)
    assert not rows[1].supported


def test_inline_code_and_fenced_examples_do_not_supply_heading_navigation() -> None:
    text = "## Rule\n\n`[@source]`\n\n```text\n[@source]\n{#sec:fake}\n```\n"
    assert unsupported_heading_rows_for_text(text) == ["Rule"]


def test_generated_reader_headings_all_have_navigation(built_output: Path) -> None:
    root = manuscript_dir(built_output)
    summary = heading_support_summary(heading_support_inventory(root))
    assert summary.ok, unsupported_heading_rows(root)


def test_audit_excludes_repository_helpers_but_keeps_reader_backmatter(tmp_path: Path) -> None:
    (tmp_path / "chapter.md").write_text("# Chapter {#sec:chapter}\n", encoding="utf-8")
    (tmp_path / "references.md").write_text("# References\n", encoding="utf-8")
    nested = tmp_path / "parts"
    nested.mkdir()
    for name in ["README.md", "AGENTS.md"]:
        (nested / name).write_text("# Repository instructions without reader navigation\n", encoding="utf-8")
    rows = heading_support_inventory(tmp_path)
    assert [(row.path, row.supported) for row in rows] == [("chapter.md", True), ("references.md", False)]


def test_fragment_navigation_uses_only_the_actual_source_section_target(tmp_path: Path) -> None:
    source = "# Overview {#sec:overview .unnumbered}\n\nSource discussion [@scholarly_example].\n"
    fragment = "### Continued overview\n\n#### Practice rule\n\nAuthor-defined criteria.\n"
    revised = add_heading_support(fragment, section_text=source)
    (tmp_path / "fragment.md").write_text(revised, encoding="utf-8")
    rows = heading_support_inventory(tmp_path)
    assert [(row.title, row.support_refs) for row in rows] == [("Continued overview", ("[@sec:overview]",)), ("Practice rule", ("[@sec:overview]",))]
    assert "scholarly_example" not in revised
    assert "{#sec:" not in revised


def test_line_budget_keeps_trailing_heading_with_following_content() -> None:
    source = "# Overview {#sec:overview}\n\none\ntwo\nthree\nfour\n#### Boundary lesson\n\nFirst supporting paragraph.\n" + "\n".join(f"Following paragraph {index}." for index in range(15))
    fragments = split_by_line_budget("chapter.md", source, max_lines=12)
    lesson = next(text for _, text in fragments if "#### Boundary lesson" in text)
    assert "First supporting paragraph." in lesson
    assert all(len(text.splitlines()) <= 12 for _, text in fragments)
    assert [line for _, text in fragments for line in text.splitlines() if line.strip()] == [line for line in source.splitlines() if line.strip()]


def unsupported_heading_rows_for_text(text: str) -> list[str]:
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        path = root / "sample.md"
        path.write_text(text, encoding="utf-8")
        return [row.title for row in unsupported_heading_rows(root)]
