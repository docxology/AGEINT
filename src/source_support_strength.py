"""Source-support strength classification for AGEINT citation keys."""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
from urllib.parse import urlparse
from typing import Any

try:
    from ._jsonl import read_jsonl
except ImportError:  # pragma: no cover - direct script imports
    from _jsonl import read_jsonl  # type: ignore[no-redef]


PRIMARY_STRENGTHS = frozenset(
    {
        "official_primary",
        "standard_primary",
        "scholarly_primary",
        "law_policy_primary",
        "public_domain_primary",
        "source_quality_anchor",
        "source_guide_primary",
    }
)
WEAK_STRENGTHS = frozenset(
    {
        "practitioner_or_vendor_context",
        "social_or_video_context",
        "mirror_or_copy_context",
        "source_guide_context",
        "unknown",
    }
)

OFFICIAL_DOMAINS = (
    ".gov",
    ".mil",
    "dni.gov",
    "odni.gov",
    "cia.gov",
    "cisa.gov",
    "nist.gov",
    "nsa.gov",
    "usgs.gov",
    "oecd.org",
    "europa.eu",
    "international.gc.ca",
    "canada.ca",
    "ico.org.uk",
)
STANDARD_DOMAINS = (
    "iso.org",
    "iec.ch",
    "ieee.org",
    "oasis-open.org",
    "w3.org",
    "rfc-editor.org",
    "ietf.org",
    "mitre.org",
)
SCHOLARLY_DOMAINS = (
    "doi.org",
    "arxiv.org",
    "pmc.ncbi.nlm.nih.gov",
    "ncbi.nlm.nih.gov",
    "journals.sagepub.com",
    "tandfonline.com",
    "cambridge.org",
    "springer.com",
    "sciencedirect.com",
    "science.org",
    "nature.com",
    "jstor.org",
)
PRACTITIONER_VENDOR_DOMAINS = (
    "linkedin.com",
    "medium.com",
    "aws.amazon.com",
    "protectai.com",
    "bandwidth.com",
    "gravitee.io",
    "bitdefender.com",
    "redteams.ai",
    "mitsloan.mit.edu",
    "paloaltonetworks.com",
    "claroty.com",
    "simbian.ai",
    "dynatrace.com",
)
SOCIAL_VIDEO_DOMAINS = (
    "youtube.com",
    "youtu.be",
    "reddit.com",
    "x.com",
    "twitter.com",
)
MIRROR_COPY_DOMAINS = (
    "scribd.com",
    "wikipedia.org",
    "researchgate.net",
    "academia.edu",
    "slideshare.net",
)


@dataclass(frozen=True)
class SourceSupportProfile:
    """Support-strength profile for one citation key."""

    key: str
    strength: str
    family: str
    primary_support: bool
    weak_context: bool
    source_title: str = ""
    source_url: str = ""
    source_tier: str = ""
    note: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "key": self.key,
            "strength": self.strength,
            "family": self.family,
            "primary_support": self.primary_support,
            "weak_context": self.weak_context,
            "source_title": self.source_title,
            "source_url": self.source_url,
            "source_tier": self.source_tier,
            "note": self.note,
        }


def source_support_strength(key: str, project_root: Path) -> SourceSupportProfile:
    """Return a support-strength profile for a Pandoc citation key."""

    root = Path(project_root)
    clean_key = key.strip().lstrip("@")
    if clean_key.startswith("ageint") and clean_key[6:].isdigit():
        row = _source_guide_index(root).get(clean_key)
        if row is None:
            return _unknown(clean_key)
        return _profile_from_source_guide_row(clean_key, row)
    anchor = _curated_anchor_index(root).get(clean_key)
    if anchor is not None:
        return _profile_from_anchor(clean_key, anchor)
    return _profile_from_key(clean_key)


def support_profiles_for_keys(keys: list[str] | tuple[str, ...], project_root: Path) -> list[SourceSupportProfile]:
    """Return support profiles in key order, preserving unknowns."""

    return [source_support_strength(key, project_root) for key in keys]


def support_family_for_key(key: str, project_root: Path) -> str:
    """Return a coarse source family derived from support strength."""

    return source_support_strength(key, project_root).family


def has_primary_support(keys: list[str] | tuple[str, ...], project_root: Path) -> bool:
    """True when at least one key supplies primary support."""

    return any(profile.primary_support for profile in support_profiles_for_keys(keys, project_root))


@lru_cache(maxsize=8)
def _source_guide_index(project_root: Path) -> dict[str, dict[str, Any]]:
    references = Path(project_root) / "data" / "curriculum" / "references"
    rows: dict[str, dict[str, Any]] = {}
    if not references.is_dir():
        return rows
    for shard in sorted(references.glob("source-guide-*.jsonl")):
        for row in read_jsonl(shard):
            key = str(row.get("key") or f"ageint{int(row['number']):03d}")
            rows[key] = dict(row)
    return rows


@lru_cache(maxsize=8)
def _curated_anchor_index(project_root: Path) -> dict[str, dict[str, Any]]:
    anchors = Path(project_root) / "data" / "research_anchors"
    rows: dict[str, dict[str, Any]] = {}
    if not anchors.is_dir():
        return rows
    for shard in sorted(anchors.glob("*.jsonl")):
        for row in read_jsonl(shard):
            rows[str(row["key"])] = dict(row)
    return rows


def _profile_from_source_guide_row(key: str, row: dict[str, Any]) -> SourceSupportProfile:
    url = str(row.get("url", ""))
    title = str(row.get("title", ""))
    note_verified = bool(row.get("note_verified", False))
    host = _host(url)
    if _matches(host, SOCIAL_VIDEO_DOMAINS):
        strength = "social_or_video_context"
        family = "source_guide_social_video"
    elif _matches(host, MIRROR_COPY_DOMAINS):
        strength = "mirror_or_copy_context"
        family = "source_guide_mirror_copy"
    elif _matches(host, PRACTITIONER_VENDOR_DOMAINS):
        strength = "practitioner_or_vendor_context"
        family = "practitioner_vendor"
    elif _matches(host, STANDARD_DOMAINS):
        strength = "standard_primary"
        family = "standard"
    elif _matches(host, OFFICIAL_DOMAINS):
        strength = "source_guide_primary"
        family = "official"
    elif _matches(host, SCHOLARLY_DOMAINS):
        strength = "scholarly_primary" if note_verified else "source_guide_context"
        family = "scholarly" if note_verified else "source_guide"
    elif note_verified:
        strength = "source_guide_primary"
        family = "source_guide"
    else:
        strength = "source_guide_context"
        family = "source_guide"
    return _profile(
        key,
        strength,
        family,
        source_title=title,
        source_url=url,
        source_tier="source_guide",
    )


def _profile_from_anchor(key: str, row: dict[str, Any]) -> SourceSupportProfile:
    text = " ".join(
        str(row.get(field, ""))
        for field in ("source_tier", "source_type", "source_lane", "domain", "citation_role", "key")
    ).lower()
    if "source_quality_anchor" in text:
        strength = "source_quality_anchor"
        family = "source_quality"
    elif "standard" in text or "fips" in text or "sp_800" in text:
        strength = "standard_primary"
        family = "standard"
    elif "scholarly" in text or key.startswith("scholarly_"):
        strength = "scholarly_primary"
        family = "scholarly"
    elif any(token in text for token in ("statutory", "regulatory", "law", "policy")):
        strength = "law_policy_primary"
        family = "law_policy"
    elif any(token in text for token in ("public_domain", "historical")):
        strength = "public_domain_primary"
        family = "public_domain"
    elif "official" in text or key.startswith("official_"):
        strength = "official_primary"
        family = "official"
    elif any(token in text for token in ("vendor", "practitioner")):
        strength = "practitioner_or_vendor_context"
        family = "practitioner_vendor"
    else:
        strength = "curated_context"
        family = "curated_anchor"
    return _profile(
        key,
        strength,
        family,
        source_title=str(row.get("title", "")),
        source_url=str(row.get("url", "")),
        source_tier=str(row.get("source_tier") or row.get("source_type") or ""),
    )


def _profile_from_key(key: str) -> SourceSupportProfile:
    lowered = key.lower()
    if lowered.startswith("official_"):
        return _profile(key, "official_primary", "official")
    if lowered.startswith("scholarly_"):
        return _profile(key, "scholarly_primary", "scholarly")
    if lowered.startswith("standard_"):
        return _profile(key, "standard_primary", "standard")
    return _unknown(key)


def _profile(
    key: str,
    strength: str,
    family: str,
    *,
    source_title: str = "",
    source_url: str = "",
    source_tier: str = "",
) -> SourceSupportProfile:
    primary = strength in PRIMARY_STRENGTHS
    weak = strength in WEAK_STRENGTHS or not primary and strength != "curated_context"
    return SourceSupportProfile(
        key=key,
        strength=strength,
        family=family,
        primary_support=primary,
        weak_context=weak,
        source_title=source_title,
        source_url=source_url,
        source_tier=source_tier,
        note=_support_note(strength),
    )


def _unknown(key: str) -> SourceSupportProfile:
    return _profile(key, "unknown", "unknown")


def _support_note(strength: str) -> str:
    if strength in PRIMARY_STRENGTHS:
        return "direct support lane for bounded AGEINT claims"
    if strength == "curated_context":
        return "curated contextual support; use direct anchors for strong claims"
    return "context only; do not use alone for empirical, performance, governance, or safety claims"


def _host(url: str) -> str:
    parsed = urlparse(url if "://" in url else f"https://{url}")
    return parsed.netloc.lower().removeprefix("www.")


def _matches(host: str, domains: tuple[str, ...]) -> bool:
    return any(host == domain or host.endswith(domain) for domain in domains)


__all__ = [
    "PRIMARY_STRENGTHS",
    "SourceSupportProfile",
    "WEAK_STRENGTHS",
    "has_primary_support",
    "source_support_strength",
    "support_family_for_key",
    "support_profiles_for_keys",
]
