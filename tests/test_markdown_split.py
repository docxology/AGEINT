"""Tests for generic Markdown splitting helpers."""

from __future__ import annotations

from _markdown_split import line_count, split_by_line_budget, split_h2_blocks, split_long_table


def test_split_h2_blocks_preserves_lead_and_headings() -> None:
    text = "# Title\n\nIntro\n\n## Alpha\n\nOne\n\n## Beta\n\nTwo"
    lead, blocks = split_h2_blocks(text)
    assert "Intro" in lead
    assert [heading for heading, _ in blocks] == ["Alpha", "Beta"]


def test_split_by_line_budget_keeps_short_text() -> None:
    fragments = split_by_line_budget("parts/01/ch.md", "short\n")
    assert fragments == [("parts/01/ch.md", "short")]


def test_split_long_table_chunks_rows() -> None:
    header = "## Table\n\n| A | B |\n|---|---|"
    rows = "\n".join(f"| {index} | {index} |" for index in range(200))
    text = f"{header}\n{rows}"
    fragments = split_long_table("parts/01/table.md", text, max_lines=40)
    assert len(fragments) > 1
    assert all(line_count(body) <= 40 for _, body in fragments)
