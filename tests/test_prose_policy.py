"""Tests for shared prose transforms."""

from __future__ import annotations

import pytest

from prose_policy import source_identifier_text


def test_source_identifier_text_preserves_markdown_and_quantity_boundaries() -> None:
    text = (
        "EO 12333; ISO/IEC TR 24028:2020; Unit 8200; PLA Unit 61398; section 2.3. "
        "Measured 4.60 and synthetic 0.3125, with 8200 records. "
        "`EO 12333` and ``ISO 19157:2013 `literal` ``. "
        "[Executive Order 12333](https://example.org/EO 12333/(nested/(section 2.3))) "
        "https://example.org/ISO/19157:2013 and xEO 12333 and EO 12333x."
    )
    expected = (
        "`EO 12333`; `ISO/IEC TR 24028:2020`; `Unit 8200`; PLA `Unit 61398`; `section 2.3`. "
        "Measured 4.60 and synthetic 0.3125, with 8200 records. "
        "`EO 12333` and ``ISO 19157:2013 `literal` ``. "
        "[`Executive Order 12333`](https://example.org/EO 12333/(nested/(section 2.3))) "
        "https://example.org/ISO/19157:2013 and xEO 12333 and EO 12333x."
    )
    assert source_identifier_text(text) == expected
    assert source_identifier_text(expected) == expected
    literal_block = "~~~text\nEO 12333 and section 2.3\n~~~"
    assert source_identifier_text(literal_block) == literal_block


@pytest.mark.parametrize(
    ("opening", "body", "closing"),
    [
        ("```text", "EO 12333 and ISO 19157:2013", "````"),
        ("````text", "EO 12333\n```\nsection 5.10", "`````"),
        ("  ```text", "EO 12333 and section 5.10", "   ````"),
        ("~~~text", "EO 12333 and section 5.10", "~~~~"),
    ],
)
def test_source_identifier_text_preserves_fenced_examples(opening: str, body: str, closing: str) -> None:
    example = f"{opening}\n{body}\n{closing}"
    assert source_identifier_text(f"EO 12333\n{example}\nUnit 8200") == f"`EO 12333`\n{example}\n`Unit 8200`"


@pytest.mark.parametrize("opening", ["```text", "~~~text"])
def test_source_identifier_text_preserves_unclosed_fenced_examples(opening: str) -> None:
    example = f"{opening}\nEO 12333 and section 5.10\n"
    assert source_identifier_text(f"Unit 8200\n{example}") == f"`Unit 8200`\n{example}"


def test_source_identifier_text_marks_designations_not_entire_annotations() -> None:
    text = (
        "Historical EO 12333 at 46 FR 59941; PPD-28 is distinct. "
        "Intelligence Community Directive 504: data management; ISA/IEC 62443 series; "
        "Regulation (EU) 2024/1689: scope. ISO 19157:2013 is not an efficacy result."
    )
    assert source_identifier_text(text) == (
        "Historical `EO 12333` at `46 FR 59941`; `PPD-28` is distinct. "
        "`Intelligence Community Directive 504`: data management; `ISA/IEC 62443` series; "
        "`Regulation (EU) 2024/1689`: scope. `ISO 19157:2013` is not an efficacy result."
    )
