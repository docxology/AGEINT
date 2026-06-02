"""Tests for canonical safety contract invariants."""

from __future__ import annotations

from manuscript_quality.inventory_helpers import (
    BLOCKED_OPERATIONAL_PATTERN_PHRASES,
    DIRECT_STUDENT_TASK_MOTIFS,
)
from safety_contract import (
    BLOCKED_OPERATIONAL_PHRASES,
    DIRECT_TASK_MOTIF_RE,
    text_is_operational,
)


def test_inventory_helpers_reexport_matches_safety_contract() -> None:
    assert BLOCKED_OPERATIONAL_PATTERN_PHRASES == BLOCKED_OPERATIONAL_PHRASES
    assert DIRECT_STUDENT_TASK_MOTIFS.pattern == DIRECT_TASK_MOTIF_RE.pattern


def test_text_is_operational_blocks_phrase_and_regex_motifs() -> None:
    assert text_is_operational("Uses shodan for infrastructure tracking")
    assert text_is_operational("Automated weaponization playbook")
    assert not text_is_operational("Tabletop audit of synthetic records")
