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

    assert "**Section anchor.**" in revised
    assert "[@sec:sample-section]" in revised
    assert unsupported_heading_rows_for_text(revised) == []


def test_add_heading_support_treats_presplit_bibliography_as_structural() -> None:
    rendered = "\n\n".join(
        [
            "# Bibliography Atlas {#sec:bibliography_atlas}",
            "Introductory citation example [@scholarly_heuer_psychology_intelligence_analysis].",
            "## Add Or Extend A Citation",
            "Use source-owned citation workflow steps.",
        ]
    )
    revised = add_heading_support(rendered, "bibliography-atlas.md")

    assert "**Section anchor.** [@sec:bibliography_atlas]." in revised
    anchor_line = next(line for line in revised.splitlines() if line.startswith("**Section anchor.**"))
    assert "scholarly_heuer_psychology_intelligence_analysis" not in anchor_line


def test_add_heading_support_uses_coverage_language_for_source_inventory() -> None:
    rendered = "\n\n".join(
        [
            "## Add Or Extend A Citation",
            "### Current citation coverage by source section",
            "| Measure | Count |",
            "|---|---:|",
            "| Source sections | 723 |",
            "### Citation rows by source section",
            "[@scholarly_heuer_psychology_intelligence_analysis]",
        ]
    )
    revised = add_heading_support(rendered, "appendices/bibliography-atlas/coverage.md")

    assert "**Coverage anchor.** Parent appendix: [@sec:bibliography_atlas]." in revised
    assert "Citation coverage by source section is validated from the generated citation inventory" in revised
    coverage_line = next(line for line in revised.splitlines() if line.startswith("**Coverage anchor.**"))
    assert "scholarly_heuer_psychology_intelligence_analysis" not in coverage_line
    assert "**Evidence link.**" not in revised


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
