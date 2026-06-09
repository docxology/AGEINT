"""YAML-driven evidence and artifact prompt evaluation for topic lessons."""

from __future__ import annotations

from collections.abc import Callable
from typing import TYPE_CHECKING

from _data_loaders import (
    artifact_keyword_routes,
    artifact_risk_category_prompts,
    evidence_category_prompts,
    evidence_keyword_routes,
)
from ._07_safe_titles import _topic_anchor_words, distinguishing_phrase
from ._12_concept_routes import _first_matching_frame

if TYPE_CHECKING:
    from ._01_part import CoursebookProfile, PracticeLens, TopicEntry

# Deterministic per-risk-category verification clause for the artifact fallback.
# Each clause names the six required artifact elements (source descriptor, bounded
# claim, caveat, uncertainty note, blocked-use boundary, accountable reviewer) but
# reframes and reorders them in the category's own risk vocabulary and threads in
# the topic anchor ({a}). This replaces a single verbatim sentence that was stamped
# onto hundreds of lessons; the lens-derived artifact-name prefix is unchanged.
_DEFAULT_ARTIFACT_VERIFICATION = (
    "name the source descriptor, the bounded claim about {a}, the supporting caveat, "
    "the uncertainty note, the blocked-use boundary, and the accountable reviewer"
)
_ARTIFACT_VERIFICATION_BY_RISK: dict[str, str] = {
    "standard": (
        "name the source descriptor, the bounded claim about {a}, the caveat that "
        "limits it, the uncertainty note, the out-of-scope-use boundary, and the "
        "reviewer accountable for challenge"
    ),
    "agentic_cyber_misuse": (
        "label the tool permission, the bounded claim about {a}, the deny rule that "
        "blocks the unsafe path, the residual uncertainty, and the reviewer who signs "
        "the disposition"
    ),
    "cognitive_resilience": (
        "record the narrative provenance, the bounded claim about {a}, the audience-harm "
        "caveat, the uncertainty note, the transparent-use boundary, and the reviewer "
        "accountable for correction"
    ),
    "historical_humint_source_protection": (
        "cite the declassified source descriptor, the bounded lesson about {a}, the "
        "redaction caveat, the attribution uncertainty, the protected-detail boundary, "
        "and the reviewer who clears release"
    ),
    "analytic_tradecraft": (
        "separate the source descriptor, the bounded judgment about {a}, the analytic "
        "caveat, the confidence note, the excluded-inference boundary, and the reviewer "
        "who logs dissent"
    ),
    "operator_decision_hygiene": (
        "note the workload descriptor, the bounded claim about {a}, the fatigue caveat, "
        "the uncertainty margin, the do-not-escalate boundary, and the reviewer who owns "
        "the handoff"
    ),
    "gray_zone_governance": (
        "name the indicator descriptor, the bounded claim about {a}, the attribution "
        "caveat, the threshold uncertainty, the non-attribution boundary, and the "
        "reviewer who approves the policy read"
    ),
    "sigint_authority": (
        "state the authority descriptor, the bounded claim about {a}, the minimization "
        "caveat, the uncertainty note, the collection boundary, and the reviewer "
        "accountable for the authorization"
    ),
    "cyber_taxonomy": (
        "map the indicator descriptor, the bounded claim about {a}, the taxonomy caveat, "
        "the confidence note, the no-action boundary, and the reviewer who validates the "
        "labeling"
    ),
    "geoint_data_quality": (
        "list the imagery descriptor, the bounded claim about {a}, the resolution caveat, "
        "the uncertainty note, the sensitive-site boundary, and the reviewer who checks "
        "the interpretation"
    ),
    "counterintelligence_vetting": (
        "record the vetting descriptor, the bounded claim about {a}, the bias caveat, "
        "the uncertainty note, the unproven-allegation boundary, and the reviewer who "
        "adjudicates"
    ),
    "humint_recruitment_risk": (
        "note the motivation descriptor, the bounded claim about {a}, the consent caveat, "
        "the uncertainty note, the no-contact boundary, and the reviewer who owns "
        "escalation duties"
    ),
    "humint_handling_history": (
        "cite the historical descriptor, the bounded lesson about {a}, the handling "
        "caveat, the uncertainty note, the protected-tradecraft boundary, and the "
        "reviewer who clears the account"
    ),
    "operational_tradecraft_governance": (
        "name the governance descriptor, the bounded claim about {a}, the compartmentation "
        "caveat, the uncertainty note, the non-authorization boundary, and the reviewer "
        "who signs oversight"
    ),
    "osint_tool_governance": (
        "record the tool-and-terms descriptor, the bounded claim about {a}, the "
        "minimization caveat, the reproducibility uncertainty, the identity-exposure "
        "boundary, and the reviewer who approves the use"
    ),
    "ics_safety": (
        "list the asset descriptor, the bounded claim about {a}, the safety caveat, "
        "the uncertainty note, the no-live-actuation boundary, and the reviewer who owns "
        "the safety case"
    ),
    "critical_infrastructure_sharing": (
        "state the handling descriptor, the bounded claim about {a}, the anonymization "
        "caveat, the confidence note, the consumer-duty boundary, and the reviewer who "
        "clears sharing"
    ),
    "non_state_actor_governance": (
        "name the actor descriptor, the bounded claim about {a}, the attribution caveat, "
        "the uncertainty note, the non-targeting boundary, and the reviewer who approves "
        "the assessment"
    ),
    "software_supply_chain_social_trust": (
        "record the provenance descriptor, the bounded claim about {a}, the "
        "maintainer-trust caveat, the attribution uncertainty, the escalation boundary, "
        "and the reviewer who signs the disposition"
    ),
    "financial_due_diligence": (
        "note the typology descriptor, the bounded claim about {a}, the intent caveat, "
        "the uncertainty threshold, the no-accusation boundary, and the reviewer who "
        "owns escalation"
    ),
    "evidence_change_memory": (
        "record the source descriptor, the bounded claim about {a}, the revision caveat, "
        "the uncertainty note, the superseded-claim boundary, and the reviewer who logs "
        "the change"
    ),
    "identity_provenance": (
        "state the identity descriptor, the bounded claim about {a}, the linkage caveat, "
        "the uncertainty note, the no-deanonymization boundary, and the reviewer who "
        "clears the record"
    ),
    "ics_evasion_coverage": (
        "list the coverage descriptor, the bounded claim about {a}, the detection-gap "
        "caveat, the uncertainty note, the no-evasion boundary, and the reviewer who owns "
        "the control review"
    ),
    "ics_collection_detection": (
        "list the observation descriptor, the bounded claim about {a}, the detection "
        "caveat, the uncertainty note, the approved-point boundary, and the reviewer who "
        "validates coverage"
    ),
    "ageint_pattern_registry": (
        "name the pattern descriptor, the bounded claim about {a}, the safe-substitution "
        "caveat, the uncertainty note, the no-deployment boundary, and the reviewer "
        "accountable for challenge"
    ),
}


def evidence_prompt_for_entry(
    entry: TopicEntry,
    lens: PracticeLens,
    coursebook: CoursebookProfile,
    *,
    synthesized_evidence_prompt: Callable[[TopicEntry, PracticeLens, CoursebookProfile], str],
) -> str:
    """Resolve evidence prompt from YAML routes with synthesized fallback."""
    raw = entry.raw_title.lower()
    routed = _first_matching_frame(raw, evidence_keyword_routes())
    if routed:
        return routed
    category_prompts = evidence_category_prompts()
    category = category_prompts.get(entry.risk_category)
    if category:
        if "sample materials and transparent labels" in entry.display_title.lower():
            anchor = _topic_anchor_words(entry.raw_title, limit=2)
            return (
                f"Evidence packet for **{entry.display_title}**: narrative provenance for {anchor}, "
                "audience-harm notes, attribution evidence, and transparent education options."
            )
        return category
    return synthesized_evidence_prompt(entry, lens, coursebook)


def artifact_prompt_for_entry(
    entry: TopicEntry,
    lens: PracticeLens,
    coursebook: CoursebookProfile,
) -> str:
    """Resolve artifact prompt from YAML routes with default template fallback."""
    raw = entry.raw_title.lower()
    routed = _first_matching_frame(raw, artifact_keyword_routes())
    if routed:
        return routed
    risk_prompts = artifact_risk_category_prompts()
    risk_prompt = risk_prompts.get(entry.risk_category)
    if risk_prompt:
        return risk_prompt
    # Anchor on the SAFE display_title, never raw_title: raw_title can carry the
    # original operational source motif (e.g. "Evasion: Rootkit, ..."), which must
    # not leak into a student-task sentence.
    # Use a contiguous, readable noun phrase for the prepositional object so the
    # sentence reads "the bounded claim about Intelligence Cycle" rather than the
    # comma-joined keyword fragment "about Cycle, Classic" (which collides with the
    # clause's own commas).
    # distinguishing_phrase can strip a citation-noise title (e.g. "2021",
    # "Case Study: 2019") to "", which would render a dangling object
    # ("the bounded claim about , ..."); fall back to a readable noun phrase.
    anchor = distinguishing_phrase(entry.display_title) or "this topic"
    verification = _ARTIFACT_VERIFICATION_BY_RISK.get(
        entry.risk_category, _DEFAULT_ARTIFACT_VERIFICATION
    ).format(a=anchor)
    return (
        f"Build a **{lens.evidence_artifact}** for this {coursebook.practice_focus} "
        f"topic. The artifact must {verification}."
    )


__all__ = ["artifact_prompt_for_entry", "evidence_prompt_for_entry"]
