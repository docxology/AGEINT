"""Tests for shared prose transforms."""

from __future__ import annotations

from prose_policy import reader_source_title


def test_reader_source_title_replaces_scaffold_wording() -> None:
    assert reader_source_title("Capstone scaffold") == "Capstone workflow"
    assert reader_source_title("methods scaffolds") == "methods workflows"
