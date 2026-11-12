"""Tests for canonical safety contract invariants."""

from __future__ import annotations

from safety_contract import text_is_operational


def test_text_is_operational_blocks_phrase_and_regex_motifs() -> None:
    assert text_is_operational("Uses shodan for infrastructure tracking")
    assert text_is_operational("Automated weaponization playbook")
    assert not text_is_operational("Tabletop audit of synthetic records")
