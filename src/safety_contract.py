"""Canonical safety invariants for non-operational curriculum prose.

Production filtering (``source_grounding``) and manuscript-safety tests import
from this module so blocked phrases and task motifs cannot drift apart.
"""

from __future__ import annotations

import re

# Operational tradecraft motifs that must never be reproduced verbatim in
# reader-facing curriculum prose.
BLOCKED_OPERATIONAL_PHRASES: frozenset[str] = frozenset(
    {
        "multi-source data harvesting",
        "real-time collection",
        "persistent target monitoring",
        "dark web alerting",
        "infrastructure tracking",
        "penetration testing automation",
        "vulnerability discovery",
        "noc legend",
        "sock puppet",
        "autonomous soc",
        "facility monitoring",
        "order-of-battle",
        "population-scale cognitive security intervention delivery",
        "shodan",
        "spiderfoot",
        "google earth engine",
        "recon-ng",
        "long-term asset tracking",
        "pattern-of-life analysis",
        "live target tasking",
        "autonomous response",
        "facility assessment",
        "external deployment",
        "unsafe cyber-physical action",
    }
)

DIRECT_TASK_MOTIF_RE = re.compile(
    r"(?i)(malware generation|phishing automation|spear-phishing automation|"
    r"automated weaponization|rootkit|indicator removal|modify firmware|"
    r"modify controller|project file infection|alarm suppression|block communications|"
    r"dead drops|surveillance detection route|confidential contacts|"
    r"psychological methods and manipulation|working with agents)"
)


def text_is_operational(text: str) -> bool:
    """True when text reproduces a blocked operational tradecraft motif."""
    lowered = text.lower()
    if any(phrase in lowered for phrase in BLOCKED_OPERATIONAL_PHRASES):
        return True
    return bool(DIRECT_TASK_MOTIF_RE.search(text))


__all__ = [
    "BLOCKED_OPERATIONAL_PHRASES",
    "DIRECT_TASK_MOTIF_RE",
    "text_is_operational",
]
