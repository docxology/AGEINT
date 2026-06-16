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


def test_split_by_line_budget_preserves_multiple_table_headers() -> None:
    measure_table = "\n".join(
        [
            "| Measure | Count |",
            "|---|---:|",
            "| Source sections | 723 |",
            "| Distribution | 1 citation(s): 275 section(s) |",
        ]
    )
    inventory_header = "\n".join(
        [
            "| Section | Module and source section | Citations | Citation links |",
            "|---:|---|---:|---|",
        ]
    )
    inventory_rows = "\n".join(
        f"| {index}.1 | Module {index} - Detailed source-section title with several words | 3 | [@ageint001]; [@ageint002] |"
        for index in range(80)
    )
    text = "\n\n".join(
        [
            "## Add Or Extend A Citation",
            "### Current citation coverage by source section",
            measure_table,
            "### Citation rows by source section",
            f"{inventory_header}\n{inventory_rows}",
        ]
    )

    fragments = split_by_line_budget("appendices/bibliography-atlas/coverage.md", text, max_lines=35)

    assert len(fragments) > 1
    assert all(line_count(body) <= 35 for _, body in fragments)
    for _, body in fragments:
        if "| Section | Module and source section | Citations | Citation links |" in body:
            assert "|---:|---|---:|---|" in body
    assert all(
        "| Distribution | 1 citation(s): 275 section(s) |\n"
        "| Section | Module and source section | Citations | Citation links |" not in body
        for _, body in fragments
    )
