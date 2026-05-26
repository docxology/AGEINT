"""Tests for generated heading reference-support auditing."""

from __future__ import annotations

from pathlib import Path

from manuscript_quality.inventory_helpers import manuscript_dir
from rendered_heading_support import (
    add_heading_support,
    heading_support_inventory,
    heading_support_summary,
    render_heading_support_markdown,
    unsupported_heading_rows,
)


def test_add_heading_support_adds_contextual_reference_line() -> None:
    rendered = "# Sample Section {#sec:sample-section}\n\n## Purpose\n\nExplain the bounded exercise.\n"
    revised = add_heading_support(rendered, "appendices/sample-section.md")

    assert "**Evidence link.**" in revised
    assert "[@sec:sample-section]" in revised
    assert unsupported_heading_rows_for_text(revised) == []


def test_generated_heading_support_covers_every_heading(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    rows = heading_support_inventory(output_manuscript)
    summary = heading_support_summary(rows)

    assert summary.heading_count > 0
    assert summary.unsupported_heading_count == 0
    assert unsupported_heading_rows(output_manuscript) == []


def test_render_heading_support_markdown_reports_clean_summary(built_output: Path) -> None:
    rendered = render_heading_support_markdown(manuscript_dir(built_output))

    assert "| Unsupported headings | 0 |" in rendered
    assert "| OK | true |" in rendered


def unsupported_heading_rows_for_text(text: str) -> list[str]:
    from tempfile import TemporaryDirectory

    with TemporaryDirectory() as tmp:
        root = Path(tmp)
        path = root / "sample.md"
        path.write_text(text, encoding="utf-8")
        return [row.title for row in unsupported_heading_rows(root)]
