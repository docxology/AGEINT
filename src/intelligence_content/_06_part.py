from __future__ import annotations

import re
from typing import Any

from _data_loaders import coursebook_profiles_as_dataclasses

from ._01_part import (
    IntelligenceProfile,
    PracticeLens,
    ResearchAnchor,
    SafePatternProfile,
)
from ._03_part import ALL_PROFILE_ANCHORS_BY_KEY, SAFE_PATTERN_PROFILES
from ._04b_part import INTELLIGENCE_PROFILES
from ._05_part import PRACTICE_LENSES


COURSEBOOK_PROFILES = coursebook_profiles_as_dataclasses()

def _normalized_lookup_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _profile_by_identifier(identifier: str) -> IntelligenceProfile:
    for profile in INTELLIGENCE_PROFILES:
        if profile.identifier == identifier:
            return profile
    raise KeyError(identifier)


def _lens_by_identifier(identifier: str) -> PracticeLens:
    for lens in PRACTICE_LENSES:
        if lens.identifier == identifier:
            return lens
    raise KeyError(identifier)


def _match_score(terms: tuple[str, ...], haystack: str) -> int:
    score = 0
    for term in terms:
        escaped = re.escape(term.lower())
        if re.search(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", haystack):
            score += 4 if " " in term or "-" in term else 2
    return score


def profile_for_titles(
    part_title: str,
    section_title: str = "",
    chapter: dict[str, object] | None = None,
) -> IntelligenceProfile:
    """Return the best content profile for a part or chapter title."""
    if chapter and chapter.get("content_profile"):
        return _profile_by_identifier(str(chapter["content_profile"]))

    haystack = f"{section_title} {part_title}".lower()
    best = INTELLIGENCE_PROFILES[0]
    best_score = -1
    for profile in INTELLIGENCE_PROFILES:
        score = _match_score(profile.match_terms, haystack)
        if score > best_score:
            best = profile
            best_score = score
    return best


def practice_lens_for_titles(
    part_title: str,
    section_title: str = "",
    chapter: dict[str, object] | None = None,
) -> PracticeLens:
    """Return the best reusable practice lens for a part, chapter, or subsection."""
    if chapter and chapter.get("practice_lens"):
        return _lens_by_identifier(str(chapter["practice_lens"]))

    part_key = _normalized_lookup_key(part_title)
    section_key = _normalized_lookup_key(section_title)
    if (
        any(term in part_key for term in ("industrial", "ics", "operational technology"))
        and any(term in section_key for term in ("incident", "attack", "att ck", "threat"))
    ):
        return _lens_by_identifier("cyber_physical_readiness")

    haystack = f"{section_title} {part_title}".lower()
    best = PRACTICE_LENSES[0]
    best_score = -1
    for lens in PRACTICE_LENSES:
        score = _match_score(lens.match_terms, haystack)
        if score > best_score:
            best = lens
            best_score = score
    return best


def anchor_references(keys: tuple[str, ...]) -> list[ResearchAnchor]:
    """Resolve anchor keys while preserving order and failing on typos."""
    missing = [key for key in keys if key not in ALL_PROFILE_ANCHORS_BY_KEY]
    if missing:
        missing_keys = ", ".join(missing)
        raise KeyError(f"Unknown AGEINT research anchor keys: {missing_keys}")
    return [ALL_PROFILE_ANCHORS_BY_KEY[key] for key in keys]


def _safe_pattern_profile(number: int | None) -> SafePatternProfile:
    if number is None:
        return SafePatternProfile(
            key="source_subsection",
            safe_name="Source-Guide Safety Treatment",
            methods="source description, safety translation, and instructor review",
            application="authorized curriculum-only exercise with public or synthetic material",
            safety_boundary="keeps source material educational, defensive, and non-operational",
        )
    return SAFE_PATTERN_PROFILES[number]


def safe_pattern_rows(patterns: list[dict[str, Any]]) -> str:
    """Render identity-preserving but safety-transformed AGEINT pattern rows."""
    rows = [
        "| Source identity | Safe curriculum treatment | Methods | Defensive application | Safety boundary |",
        "|---|---|---|---|---|",
    ]
    for pattern in patterns:
        number = int(pattern["number"])
        profile = _safe_pattern_profile(number)
        rows.append(
            "| "
            f"Pattern {number}: {pattern['name']} (source identity only) | "
            f"{profile.safe_name} | {profile.methods} | {profile.application} | "
            f"{profile.safety_boundary} |"
        )
    return "\n".join(rows)


def safe_pattern_treatment(
    section_title: str,
    active_pattern_number: int | None = None,
) -> tuple[str, int | None]:
    """Return a safe treatment for a raw pattern subsection title."""
    pattern_match = re.match(r"Pattern\s+(\d+):\s+(.+?)(?:\s+[-\u2014]|$)", section_title)
    if pattern_match:
        number = int(pattern_match.group(1))
        profile = _safe_pattern_profile(number)
        return (
            f"Pattern {number}: {profile.safe_name} "
            f"(source identity preserved in pattern registry) - {profile.safety_boundary}",
            number,
        )

    profile = _safe_pattern_profile(active_pattern_number)
    if section_title.startswith("Methods:"):
        return f"Safe methods: {profile.methods}", active_pattern_number
    if section_title.startswith("Application:"):
        return f"Safe defensive application: {profile.application}", active_pattern_number
    if section_title.startswith("Code Archetype:"):
        return (
            "Safe architecture artifact: diagram an allowlisted, logged, "
            f"revocable workflow for {profile.safe_name}",
            active_pattern_number,
        )
    return section_title, active_pattern_number
