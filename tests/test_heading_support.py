"""Tests for generated heading reference-support auditing."""

from __future__ import annotations

from pathlib import Path

from manuscript_quality.inventory_helpers import manuscript_dir
from rendered_heading_support import add_heading_support, heading_support_inventory, heading_support_summary, render_heading_support_markdown, unsupported_heading_rows


def test_heading_navigation_does_not_borrow_another_blocks_citation(tmp_path: Path) -> None:
    rendered = (
        "# Sample {#sec:sample}\n\n"
        "Search reporting follows [@scholarly_rethlefsen_2021_prisma_s].\n\n"
        "## Safety and mastery rules\n\n"
        "| Rule | Required artifact |\n|---|---|\n| Stop | Review record |\n"
    )
    revised = add_heading_support(rendered, "parts/unit/chapter/overview.md")
    assert revised.count("[@scholarly_rethlefsen_2021_prisma_s]") == 1
    safety_block = revised.split("## Safety and mastery rules", 1)[1]
    assert "[@sec:sample]" in safety_block
    assert "scholarly_rethlefsen_2021_prisma_s" not in safety_block
    assert "Evidence anchor" not in revised
    assert "navigation" in safety_block.lower()
    assert add_heading_support(revised, "parts/unit/chapter/overview.md") == revised


def test_heading_without_real_target_is_not_given_an_invented_reference() -> None:
    rendered = "## Capstone rubric\n\nAuthor-defined criteria need review.\n"
    revised = add_heading_support(rendered, "parts/unit/chapter/rubric.md")
    assert "[@sec:" not in revised
    assert unsupported_heading_rows_for_text(revised) == ["Capstone rubric"]


def test_local_heading_label_is_navigation_not_evidence(tmp_path: Path) -> None:
    (tmp_path / "sample.md").write_text(
        "# Sample {#sec:sample}\n\n## Rule\n\n"
        "This author-defined rule has no supporting source.\n",
        encoding="utf-8",
    )
    rows = heading_support_inventory(tmp_path)
    assert rows[0].supported
    assert rows[0].support_refs == ("{#sec:sample}",)
    assert not rows[1].supported
    report = render_heading_support_markdown(tmp_path)
    assert "not evidence" in report.lower()


def test_inline_code_and_fenced_examples_do_not_supply_heading_navigation() -> None:
    text = "## Rule\n\n`[@source]`\n\n```text\n[@source]\n{#sec:fake}\n```\n"
    assert unsupported_heading_rows_for_text(text) == ["Rule"]


def test_generated_heading_inventory_accounts_for_all_rows(built_output: Path) -> None:
    rows = heading_support_inventory(manuscript_dir(built_output))
    summary = heading_support_summary(rows)
    assert summary.heading_count > 0
    assert summary.heading_count == summary.supported_heading_count + summary.unsupported_heading_count
    assert summary.unsupported_heading_count == len(unsupported_heading_rows(manuscript_dir(built_output)))


def unsupported_heading_rows_for_text(text: str) -> list[str]:
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        path = root / "sample.md"
        path.write_text(text, encoding="utf-8")
        return [row.title for row in unsupported_heading_rows(root)]
