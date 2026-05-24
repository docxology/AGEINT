"""Tests for AGEINT Markdown reference helpers."""

from __future__ import annotations

import pytest

from markdown_refs import (
    citation_ref,
    citation_ref_list,
    equation_ref,
    figure_ref,
    figure_ref_list,
    section_ref,
    section_ref_list,
    table_ref,
)


def test_cross_reference_helpers_render_pandoc_syntax() -> None:
    assert section_ref("sec:curriculum_orientation") == "[@sec:curriculum_orientation]"
    assert figure_ref("fig:ageint-curriculum-map") == "[@fig:ageint-curriculum-map]"
    assert equation_ref("eq:curriculum-map") == "[@eq:curriculum-map]"
    assert table_ref("tbl:source-lanes") == "[@tbl:source-lanes]"
    assert citation_ref("ageint137") == "[@ageint137]"
    assert citation_ref("official_nist_ai_rmf") == "[@official_nist_ai_rmf]"


def test_reference_list_helpers_deduplicate_and_skip_empty_values() -> None:
    assert section_ref_list(
        ["sec:curriculum_orientation", "", "sec:curriculum_orientation", "sec:abstract"]
    ) == "[@sec:curriculum_orientation], [@sec:abstract]"
    assert figure_ref_list(["fig:one", "fig:two"]) == "[@fig:one] [@fig:two]"
    assert citation_ref_list(["ageint137", "ageint137", "official_nist_ai_rmf"]) == (
        "[@ageint137]; [@official_nist_ai_rmf]"
    )


@pytest.mark.parametrize(
    ("helper", "label"),
    [
        (section_ref, "chapter-foundations-of-ageint"),
        (section_ref, "fig:ageint-curriculum-map"),
        (figure_ref, "ageint-curriculum-map"),
        (figure_ref, "sec:curriculum_orientation"),
        (equation_ref, "curriculum-map"),
        (table_ref, "sec:curriculum_orientation"),
        (citation_ref, "@ageint137"),
        (citation_ref, "[@ageint137]"),
        (citation_ref, "fig:ageint-curriculum-map"),
    ],
)
def test_reference_helpers_reject_malformed_labels(helper, label: str) -> None:
    with pytest.raises(ValueError):
        helper(label)
