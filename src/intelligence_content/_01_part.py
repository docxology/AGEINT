from __future__ import annotations

"""Research-backed AGEINT content profiles and source anchors."""


from dataclasses import dataclass
import re
from typing import Any, Final

try:  # Support package and script-level imports.
    from .markdown_refs import citation_ref_list
except ImportError:  # pragma: no cover - exercised by thin CLI wrappers
    from markdown_refs import citation_ref_list  # type: ignore[no-redef]


@dataclass(frozen=True)
class ResearchAnchor:
    """A directly citable official or scholarly source used by AGEINT."""

    key: str
    title: str
    author: str
    year: str
    url: str
    note: str
    domain: str
    source_type: str
    checked_as_of: str = "2026-05-21"
    verification_note: str = (
        "Direct source URL verified against an official, standards, public-domain, "
        "or scholarly source for AGEINT curriculum use."
    )
    citation_role: str = "curriculum_anchor"
    source_lane: str = ""
    source_tier: str = ""
    refresh_cadence: str = "annual"
    refresh_trigger: str = "source URL, policy status, standard version, or legal text materially changes"
    verification_method: str = "direct_source_url_review"
    claim_scope: str = "curriculum grounding and source-backed synthesis"
    stakeholder_role: str = ""
    assurance_use: str = ""
    rights_dimension: str = ""

    def as_reference(self) -> dict[str, str]:
        """Return a manuscript-variable compatible reference dictionary."""
        return {
            "key": self.key,
            "title": self.title,
            "author": self.author,
            "year": self.year,
            "url": self.url,
            "note": self.note,
            "domain": self.domain,
            "source_type": self.source_type,
            "checked_as_of": self.checked_as_of,
            "verification_note": self.verification_note,
            "citation_role": self.citation_role,
            "source_lane": self.source_lane or self.domain,
            "source_tier": self.source_tier or self.source_type,
            "refresh_cadence": self.refresh_cadence,
            "refresh_trigger": self.refresh_trigger,
            "verification_method": self.verification_method,
            "claim_scope": self.claim_scope,
            "stakeholder_role": self.stakeholder_role,
            "assurance_use": self.assurance_use,
            "rights_dimension": self.rights_dimension,
        }


@dataclass(frozen=True)
class IntelligenceProfile:
    """Reusable content profile matched to generated parts and chapters."""

    identifier: str
    title: str
    match_terms: tuple[str, ...]
    anchor_keys: tuple[str, ...]
    conceptual_focus: str
    method_stack: str
    composability_contract: str
    failure_modes: str
    safety_boundary: str


@dataclass(frozen=True)
class PracticeLens:
    """Composable practice lens used at part, chapter, and subsection levels."""

    identifier: str
    title: str
    match_terms: tuple[str, ...]
    planning_question: str
    evidence_artifact: str
    validation_rule: str
    handoff_contract: str
    safety_check: str


@dataclass(frozen=True)
class SafePatternProfile:
    """Safety-transformed treatment for a source-guide AGEINT pattern."""

    key: str
    safe_name: str
    methods: str
    application: str
    safety_boundary: str


@dataclass(frozen=True)
class CoursebookProfile:
    """Profile-specific coursebook language for generated chapter teaching blocks."""

    identifier: str
    disciplinary_frame: str
    key_distinction: str
    vocabulary: tuple[tuple[str, str], ...]
    worked_scenario: str
    worked_input: str
    worked_process: str
    worked_output: str
    practice_focus: str
    review_question: str


@dataclass(frozen=True)
class TopicEntry:
    """A source-guide topic with safe learner-facing treatment metadata."""

    raw_title: str
    display_title: str
    source_locus: str
    provenance_note: str
    risk_category: str
    citation_numbers: tuple[int, ...] = ()
