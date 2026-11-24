"""Safe-identity evidence/artifact checks, then display-subject YAML routes.

Registry checks specialize the existing safe profiles; category and synthesized
fallbacks remain available without consulting transformed-away source wording.
"""

from __future__ import annotations

import re
from collections.abc import Callable
from typing import TYPE_CHECKING

from _data_loaders import artifact_keyword_routes, artifact_risk_category_prompts, evidence_category_prompts, evidence_keyword_routes
from ._07_safe_titles import distinguishing_phrase
from ._12_concept_routes import _first_matching_frame, _match_keywords
from ._03_part import SAFE_PATTERN_PROFILES

if TYPE_CHECKING:
    from ._01_part import CoursebookProfile, PracticeLens, SafePatternProfile, TopicEntry

# These checks follow registry identity, not keywords in the source-title ledger.
# Each tuple names evidence to inspect, the artifact's discriminating fields, and
# the misconception to challenge. They are classroom designs, not efficacy claims.
_PATTERN_CHECKS = {
    1: ("source passages, assumptions, and a self-critique against the same packet", "claim, passage, assumption, alternative, and confidence", "that a reasoner's self-critique supplies independent evidence"),
    2: ("original answer, review rubric, feedback, and revised answer", "rubric finding, revision, source support, and unresolved error", "that reflection makes an unsupported answer independently verified"),
    3: ("retrieval requests, connector allowlist, returned passages, and refusals", "tool schema, allowed request, source passage, and blocked scope change", "that an available retrieval tool grants permission to use it"),
    4: ("milestones, dependencies, approval decisions, and rollback notes", "plan step, prerequisite, approval owner, and rollback condition", "that a planner's proposed task authorizes its execution"),
    5: ("source-origin families, duplicate passages, and contradictory source claims", "source comparison, originating evidence family, duplicate, contradiction, and unresolved claim", "that agreeing source summaries from one origin are independent corroboration"),
    6: ("role assignments, evidence returned by each role, and reviewer dissent", "role, granted scope, source passage, dissent, and final human disposition", "that assigning different roles makes their evidence independent"),
    7: ("competing hypotheses, diagnostic evidence, and the judge's stated rubric", "hypothesis, supporting and disconfirming evidence, dissent, and rubric decision", "that winning a debate establishes factual truth"),
    8: ("corpus version, retrieval hits, quoted snippets, and citation checks", "query, retrieved passage, supported claim, injection flag, and abstention", "that a retrieved citation necessarily supports the generated answer"),
    9: ("claim revisions, source versions, retention rules, and contamination checks", "claim ledger, superseded version, dependency, retention decision, and correction", "that remembered claim text remains valid after its source changes"),
    10: ("routing decisions, tool permissions, budgets, and deny logs", "request, policy decision, remaining budget, revocation, and human owner", "that a routing interface can grant itself additional permissions"),
    11: ("toy asset-health records, synthetic event times, thresholds, and reviewed false alarms", "asset-health threshold rationale, false alarm, missing observation, and escalation decision", "that a toy asset-health alert proves a real incident or permits surveillance"),
    12: ("high-level scenario cards, control mappings, and mitigation evidence gaps", "control objective, scenario, coverage gap, and bounded mitigation question", "that a control-coverage critique establishes exploitability"),
    13: ("clearly synthetic identity artifacts, provenance labels, and consistency errors", "fiction label, artifact origin, inconsistency, and uncertainty", "that a consistent fictional identity is an authenticated real identity"),
    14: ("source metadata, corroborating records, authenticity labels, and alternatives", "reliability claim, provenance check, alternative explanation, and uncertainty", "that a reliability warning proves deception or identifies its author"),
    15: ("interrupt records, proposed actions, approval versions, and reviewer decisions", "exact action, scope, artifact version, authorized reviewer, and expiry", "that model confidence substitutes for human authorization"),
    16: ("fabricated alerts, published ATT&CK descriptions, and triage rationales", "alert, taxonomy mapping, severity rationale, uncertainty, and no-response boundary", "that an ATT&CK label confirms an incident or authorizes response"),
    17: ("sample SBOMs, dependency graphs, public advisories, and integrity evidence", "component version, advisory match, provenance gap, and uncertainty", "that a dependency match alone proves exploitability or maintainer intent"),
    18: ("provided imagery metadata, synthetic changes, and image-quality caveats", "GEOINT quality flag, observation time, resolution, and alternative interpretation", "that an image feature alone supports a confident location or attribution claim"),
    19: ("opt-in media-literacy materials, transparent labels, and learning-measurement limits", "media-literacy objective, consent, technique label, correction, and measurement limit", "that a media-literacy lesson's completion proves resistance to manipulation"),
    20: ("delegation scopes, child results, aggregation decisions, and recovery records", "parent and child task, inherited scope, evidence dependency, failure, and next owner", "that hierarchical delegation permits a child to expand its parent's authority"),
}


def pattern_profile_for_entry(entry: TopicEntry) -> SafePatternProfile | None:
    """Resolve only explicit registry identity; raw titles are provenance."""
    if entry.risk_category != "ageint_pattern_registry":
        return None
    match = re.fullmatch(r"Pattern (\d+)", entry.source_locus)
    return SAFE_PATTERN_PROFILES.get(int(match.group(1))) if match else None


def instructional_focus(entry: TopicEntry) -> tuple[str, str, str] | None:
    """Return aligned evidence/artifact/misconception for an explicit subject."""
    pattern = pattern_profile_for_entry(entry)
    if pattern:
        number = int(entry.source_locus.split()[-1])
        evidence, artifact, misconception = _PATTERN_CHECKS[number]
        return (
            f"Evidence packet for **{pattern.safe_name}**: {evidence}.",
            f"Build a **{pattern.safe_name}** card with {artifact}; keep the exercise within its registry boundary.",
            misconception,
        )
    title = entry.display_title.lower()
    if _match_keywords(title, ("institutional architecture", "soviet and russian institutions", "british intelligence", "israeli institutions", "chinese institutions")):
        return (
            "Evidence packet: dated public institutional descriptions, historical versus current mandates, oversight records, and gaps in the institutional comparison.",
            "Build an institutional role matrix with institution, date, collection/analysis/coordination role, oversight, and unknown or unsupported relationship.",
            "that institutional lineage or a similar name establishes an unchanged current mandate or chain of command",
        )
    if _match_keywords(title, ("mcp", "model context protocol")):
        return (
            "Evidence packet: MCP host/client/server boundaries, versioned tool schemas, consent decisions, and untrusted tool or source text.",
            "Build an MCP permission-boundary card with host, client, server, tool request, consent owner, and deny decision; protocol capability is not authorization.",
            "that MCP tool registration, a schema, or server-provided text grants execution authority",
        )
    if _match_keywords(title, ("cognitive controller", "reasoning agents", "controller stack")):
        return (
            "Evidence packet: software-controller inputs, proposed plans, tool requests, source-grounded outputs, and stop decisions.",
            "Build a reasoning-controller trace separating model proposal, application state, permission gate, tool result, and human decision.",
            "that a software reasoning controller is a human brain or that plausible reasoning authorizes its proposed action",
        )
    if _match_keywords(title, ("perception modules", "multimodal ingestion")):
        return (
            "Evidence packet: supplied text, image, and audio descriptors, ingestion transforms, missing modalities, and provenance gaps.",
            "Build an ingestion map with modality, original record, transform, information loss, and unsupported inference.",
            "that ingesting multiple modalities establishes their authenticity or gives a software system human perception",
        )
    if entry.risk_category == "evidence_change_memory":
        return (
            "Evidence packet: claim IDs, source revisions, dependencies, retention rules, and contamination checks; no person or asset tracking.",
            "Build a claim-change ledger linking original and revised passages, affected claims, retirement decisions, and reviewer corrections.",
            "that stored claim memory is independent evidence or remains valid after its source has changed",
        )
    if _match_keywords(title, ("rascls",)):
        return (
            "Evidence packet: historical RASCLS definitions, source context, alternative explanations, and limits on person-level inference.",
            "Build a RASCLS versus MICE vocabulary comparison with historical context, consent boundary, and unsupported motive inference.",
            "that RASCLS labels predict an individual's motives or authorize persuasion or contact",
        )
    return None

# Deterministic per-risk-category verification clause for the artifact fallback.
# Each clause names the six required artifact elements (source descriptor, bounded
# claim, caveat, uncertainty note, blocked-use boundary, accountable reviewer) but
# reframes and reorders them in the category's own risk vocabulary and threads in
# the topic anchor ({a}). This replaces a single verbatim sentence that was stamped
# onto hundreds of lessons; the lens-derived artifact-name prefix is unchanged.
_DEFAULT_ARTIFACT_VERIFICATION = "name the source descriptor, the bounded claim about {a}, the supporting caveat, the uncertainty note, the blocked-use boundary, and the accountable reviewer"
_ARTIFACT_VERIFICATION_BY_RISK: dict[str, str] = {
    "standard": ("name the source descriptor, the bounded claim about {a}, the caveat that limits it, the uncertainty note, the out-of-scope-use boundary, and the reviewer accountable for challenge"),
    "agentic_cyber_misuse": ("label the tool permission, the bounded claim about {a}, the deny rule that blocks the unsafe path, the residual uncertainty, and the reviewer who signs the disposition"),
    "cognitive_resilience": (
        "record the narrative provenance, the bounded claim about {a}, the audience-harm caveat, the uncertainty note, the transparent-use boundary, and the reviewer accountable for correction"
    ),
    "historical_humint_source_protection": (
        "cite the declassified source descriptor, the bounded lesson about {a}, the redaction caveat, the attribution uncertainty, the protected-detail boundary, and the reviewer who clears release"
    ),
    "analytic_tradecraft": (
        "separate the source descriptor, the bounded judgment about {a}, the analytic caveat, the confidence note, the excluded-inference boundary, and the reviewer who logs dissent"
    ),
    "operator_decision_hygiene": (
        "note the workload descriptor, the bounded claim about {a}, the fatigue caveat, the uncertainty margin, the do-not-escalate boundary, and the reviewer who owns the handoff"
    ),
    "gray_zone_governance": (
        "name the indicator descriptor, the bounded claim about {a}, the attribution caveat, the threshold uncertainty, the non-attribution boundary, and the reviewer who approves the policy read"
    ),
    "sigint_authority": (
        "state the authority descriptor, the bounded claim about {a}, the minimization caveat, the uncertainty note, the collection boundary, and the reviewer accountable for the authorization"
    ),
    "cyber_taxonomy": ("map the indicator descriptor, the bounded claim about {a}, the taxonomy caveat, the confidence note, the no-action boundary, and the reviewer who validates the labeling"),
    "geoint_data_quality": (
        "list the imagery descriptor, the bounded claim about {a}, the resolution caveat, the uncertainty note, the sensitive-site boundary, and the reviewer who checks the interpretation"
    ),
    "counterintelligence_vetting": (
        "record the vetting descriptor, the bounded claim about {a}, the bias caveat, the uncertainty note, the unproven-allegation boundary, and the reviewer who adjudicates"
    ),
    "humint_recruitment_risk": (
        "note the motivation descriptor, the bounded claim about {a}, the consent caveat, the uncertainty note, the no-contact boundary, and the reviewer who owns escalation duties"
    ),
    "humint_handling_history": (
        "cite the historical descriptor, the bounded lesson about {a}, the handling caveat, the uncertainty note, the protected-tradecraft boundary, and the reviewer who clears the account"
    ),
    "operational_tradecraft_governance": (
        "name the governance descriptor, the bounded claim about {a}, the compartmentation caveat, the uncertainty note, the non-authorization boundary, and the reviewer who signs oversight"
    ),
    "osint_tool_governance": (
        "record the tool-and-terms descriptor, the bounded claim about {a}, the "
        "minimization caveat, the reproducibility uncertainty, the identity-exposure "
        "boundary, and the reviewer who approves the use"
    ),
    "ics_safety": ("list the asset descriptor, the bounded claim about {a}, the safety caveat, the uncertainty note, the no-live-actuation boundary, and the reviewer who owns the safety case"),
    "critical_infrastructure_sharing": (
        "state the handling descriptor, the bounded claim about {a}, the anonymization caveat, the confidence note, the consumer-duty boundary, and the reviewer who clears sharing"
    ),
    "non_state_actor_governance": (
        "name the actor descriptor, the bounded claim about {a}, the attribution caveat, the uncertainty note, the non-targeting boundary, and the reviewer who approves the assessment"
    ),
    "software_supply_chain_social_trust": (
        "record the provenance descriptor, the bounded claim about {a}, the maintainer-trust caveat, the attribution uncertainty, the escalation boundary, and the reviewer who signs the disposition"
    ),
    "financial_due_diligence": (
        "note the typology descriptor, the bounded claim about {a}, the intent caveat, the uncertainty threshold, the no-accusation boundary, and the reviewer who owns escalation"
    ),
    "evidence_change_memory": (
        "record the source descriptor, the bounded claim about {a}, the revision caveat, the uncertainty note, the superseded-claim boundary, and the reviewer who logs the change"
    ),
    "identity_provenance": (
        "state the identity descriptor, the bounded claim about {a}, the linkage caveat, the uncertainty note, the no-deanonymization boundary, and the reviewer who clears the record"
    ),
    "ics_evasion_coverage": (
        "list the coverage descriptor, the bounded claim about {a}, the detection-gap caveat, the uncertainty note, the no-evasion boundary, and the reviewer who owns the control review"
    ),
    "ics_collection_detection": (
        "list the observation descriptor, the bounded claim about {a}, the detection caveat, the uncertainty note, the approved-point boundary, and the reviewer who validates coverage"
    ),
    "ageint_pattern_registry": (
        "name the pattern descriptor, the bounded claim about {a}, the safe-substitution caveat, the uncertainty note, the no-deployment boundary, and the reviewer accountable for challenge"
    ),
}


def evidence_prompt_for_entry(
    entry: TopicEntry, lens: PracticeLens, coursebook: CoursebookProfile, *, synthesized_evidence_prompt: Callable[[TopicEntry, PracticeLens, CoursebookProfile], str]
) -> str:
    """Resolve evidence prompt from YAML routes with synthesized fallback."""
    focus = instructional_focus(entry)
    if focus:
        return focus[0]
    # Transformed source wording remains in the provenance ledger, not routing.
    routed = _first_matching_frame(entry.display_title.lower(), evidence_keyword_routes())
    if routed:
        return routed
    category_prompts = evidence_category_prompts()
    category = category_prompts.get(entry.risk_category)
    if category:
        return category
    return synthesized_evidence_prompt(entry, lens, coursebook)


def artifact_prompt_for_entry(entry: TopicEntry, lens: PracticeLens, coursebook: CoursebookProfile) -> str:
    """Resolve artifact prompt from YAML routes with default template fallback."""
    focus = instructional_focus(entry)
    if focus:
        return focus[1]
    routed = _first_matching_frame(entry.display_title.lower(), artifact_keyword_routes())
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
    anchor_phrase = distinguishing_phrase(entry.display_title) or "this topic"
    anchor = f"**{anchor_phrase}**" if anchor_phrase != "this topic" else anchor_phrase
    verification = _ARTIFACT_VERIFICATION_BY_RISK.get(entry.risk_category, _DEFAULT_ARTIFACT_VERIFICATION).format(a=anchor)
    return f"Build a **{lens.evidence_artifact}** for this {coursebook.practice_focus} topic. The artifact must {verification}."


__all__ = ["artifact_prompt_for_entry", "evidence_prompt_for_entry"]
