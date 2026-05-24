"""Tests for shard-backed content profile and practice lens routing."""

from __future__ import annotations

import re
from pathlib import Path

from curriculum import load_curriculum
from intelligence_content import practice_lens_for_titles, profile_for_titles

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"

FORMER_PROFILE_OVERRIDES = {
    "cyber intelligence fundamentals": "cyber_threat_intelligence",
    "advanced persistent threats apts": "cyber_threat_intelligence",
    "supply chain intelligence attacks": "cyber_threat_intelligence",
    "electronic and emanations intelligence": "collection_management",
    "modern sigint and cryptography": "collection_management",
    "industrial control systems ics and operational technology": "ics_ot_defense",
    "mitre att ck for ics": "ics_ot_defense",
    "historical ics cyber incidents intelligence analysis": "ics_ot_defense",
    "threat intelligence sharing for critical infrastructure": "ics_ot_defense",
    "ageint applied to ics and cyber physical intelligence": "ics_ot_defense",
}

FORMER_LENS_OVERRIDES = {
    "cyber intelligence fundamentals": "defensive_cyber_intelligence",
    "advanced persistent threats apts": "defensive_cyber_intelligence",
    "supply chain intelligence attacks": "software_supply_chain_assurance",
    "ageint security and adversarial considerations": "defensive_cyber_intelligence",
    "ageint python code library": "agentic_tool_governance",
    "mitre att ck for ics": "cyber_physical_readiness",
    "historical ics cyber incidents intelligence analysis": "cyber_physical_readiness",
    "threat intelligence sharing for critical infrastructure": "cyber_physical_readiness",
    "ageint applied to ics and cyber physical intelligence": "cyber_physical_readiness",
}


def _normalized_lookup_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def test_chapter_shards_match_former_profile_and_lens_overrides() -> None:
    curriculum = load_curriculum(DATA)
    for chapter in curriculum.chapters:
        key = _normalized_lookup_key(str(chapter["title"]))
        if key in FORMER_PROFILE_OVERRIDES:
            assert chapter["content_profile"] == FORMER_PROFILE_OVERRIDES[key], chapter["title"]
        if key in FORMER_LENS_OVERRIDES:
            assert chapter["practice_lens"] == FORMER_LENS_OVERRIDES[key], chapter["title"]


def test_profile_for_titles_prefers_shard_content_profile() -> None:
    chapter = {
        "content_profile": "legal_oversight",
        "title": "Cyber Intelligence Fundamentals",
    }
    profile = profile_for_titles(
        "TECHNICAL INTELLIGENCE AND CYBER OPERATIONS",
        "Cyber Intelligence Fundamentals",
        chapter=chapter,
    )
    assert profile.identifier == "legal_oversight"


def test_practice_lens_for_titles_prefers_shard_practice_lens() -> None:
    chapter = {
        "practice_lens": "oversight_and_rights",
        "title": "Cyber Intelligence Fundamentals",
    }
    lens = practice_lens_for_titles(
        "TECHNICAL INTELLIGENCE AND CYBER OPERATIONS",
        "Cyber Intelligence Fundamentals",
        chapter=chapter,
    )
    assert lens.identifier == "oversight_and_rights"
