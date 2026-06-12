from __future__ import annotations

from typing import Protocol


class SourceLike(Protocol):
    url: str
    verified: bool


_PRIMARY_SUPPORT_DOMAINS = (
    "cia.gov",
    "dni.gov",
    "odni.gov",
    "intelligence.gov",
    "nist.gov",
    "cisa.gov",
    "nsa.gov",
    "mitre.org",
    "oecd.org",
    "science.org",
    "pmc.ncbi.nlm.nih.gov",
)

_PRACTITIONER_CONTEXT_DOMAINS = (
    "linkedin.com",
    "medium.com",
    "aws.amazon.com",
    "protectai.com",
    "bandwidth.com",
    "gravitee.io",
    "bitdefender.com",
    "redteams.ai",
    "mitsloan.mit.edu",
)

_NON_PRIMARY_ANALYTIC_CONTEXT_DOMAINS = (
    "specialeurasia.com",
    "spotterup.com",
    "wikipedia.org",
    "scribd.com",
    "armyupress.army.mil",
    "tandfonline.com",
    "oas.org",
    "ialeia.org",
)


def source_evidence_status(record: SourceLike) -> str:
    """Classify inherited source-guide rows by evidence role for readers."""
    url = record.url.lower()
    if any(domain in url for domain in _PRACTITIONER_CONTEXT_DOMAINS):
        prefix = "verified" if record.verified else "original"
        return f"{prefix} practitioner context; secondary evidence only"
    if any(domain in url for domain in _NON_PRIMARY_ANALYTIC_CONTEXT_DOMAINS):
        prefix = "verified" if record.verified else "original"
        return f"{prefix} source-guide context; do not use as primary analytic support"
    if "modelcontextprotocol.io/specification" in url and "/2025-06-18" not in url:
        return "verified source-guide context; use pinned MCP anchor for normative claims"
    return "verified source-guide" if record.verified else "original source-guide"


def source_is_primary_support(record: SourceLike) -> bool:
    """True when a source-guide row is suitable for primary generated claim prose."""
    url = record.url.lower()
    if any(domain in url for domain in _NON_PRIMARY_ANALYTIC_CONTEXT_DOMAINS):
        return False
    if any(domain in url for domain in _PRACTITIONER_CONTEXT_DOMAINS):
        return False
    return any(domain in url for domain in _PRIMARY_SUPPORT_DOMAINS) or record.verified
