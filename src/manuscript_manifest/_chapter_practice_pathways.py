"""Pathway assessment and synthesis block generators for manuscript chapters."""

from __future__ import annotations

from typing import Any

from intelligence_content import practice_lens_for_titles, safe_topic_entries
from prose_policy import source_identifier_text

from ._01_part import _chapter_topic_context
from ._02_part import _capstone_deliverable, _instructor_facilitation_notes
from ._heading_titles import chapter_detail_titles


def _topic_assessment_rows(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Cover every topic, grouping pattern aspects under their preserved identity."""
    title = str(chapter["title"])
    lens = practice_lens_for_titles(str(part["title"]), title, chapter=chapter)
    topics: list[str] = []
    seen_topics: set[str] = set()
    for entry in safe_topic_entries(chapter, part):
        is_pattern = entry.risk_category == "ageint_pattern_registry"
        topic_key = entry.source_locus if is_pattern else entry.display_title.strip().lower()
        if topic_key in seen_topics:
            continue
        seen_topics.add(topic_key)
        topic_title = entry.display_title
        if is_pattern:
            topic_title = topic_title.split(" (source identity preserved", 1)[0]
        topics.append(topic_title)
    if not topics:
        return ""
    operations = (
        f"**Source warrant:** reconstruct a consequential claim from an exact source locator; separate observation from inference and apply this check: {lens.validation_rule}.",
        "**Competing explanation:** compare two accounts of the same evidence; identify a discriminating observation and a claim neither account can yet support.",
        f"**Revision and transfer:** revise or defend the judgment after the withheld evidence arrives; identify what cannot transfer to another benign case. Apply the boundary: {lens.safety_check}.",
    )
    group_size = (len(topics) + len(operations) - 1) // len(operations)
    rows = []
    for operation, start in zip(operations, range(0, len(topics), group_size)):
        topic_labels = "; ".join(f"**{source_identifier_text(topic)}**" for topic in topics[start : start + group_size])
        rows.append(f"| {topic_labels} | {operation} |")
    return "\n".join(rows)


def _assessment_and_capstone_pathway(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    topic_rows = _topic_assessment_rows(chapter, part)
    title = str(chapter["title"])
    topic_context = _chapter_topic_context(chapter, part)
    details = chapter_detail_titles(title)
    topic_rubric = ""
    if topic_rows:
        topic_rubric = f"""
| Topics or pattern identities (complete coverage) | Evidence of mastery |
|---|---|
{topic_rows}
"""
    return f"""#### {details["capstone_pathway"]}

{_capstone_deliverable(chapter, part)}

#### {details["facilitation"]}

{_instructor_facilitation_notes(chapter, part)}

#### {details["rubric"]}
{topic_rubric}
The groups cover every listed topic, not just the opening topics. For pattern
registries, each identity includes its methods, defensive application, and
architecture aspects in one reviewable artifact. The row identifies a focused
reasoning operation; the studio's source trace, competing explanation, and
withheld-evidence revision remain required for every topic or pattern in
{topic_context}. For the transfer challenge, compare the final listed topic or
pattern with the first: explain which claim, permission, or evidence assumption
fails to carry over after the instructor's new evidence. For a single-topic
module, change the benign case instead. A justified abstention or refusal to
transfer can demonstrate mastery; an unsupported confident answer cannot.
Use the canonical five-row rubric in the shared method-and-assurance reference
([@sec:method-assurance-reference]) for conceptual command, analytic rigor,
agentic design, governance and rights, and safety posture.
"""


def _security_synthesis_block() -> str:
    return """#### Threat-model framework: MAESTRO seven layers

The CSA MAESTRO model gives a concrete map of where an agentic
system can be attacked, shown in [@fig:ageint-maestro-seven-layer]. It stacks seven layers of
the agent lifecycle: foundation models (L1: adversarial examples, model stealing, backdoors),
data operations (L2: poisoning, RAG-pipeline compromise), agent frameworks (L3: supply chain and
input validation), deployment and infrastructure (L4: container escape, lateral movement),
evaluation and observability (L5: metric manipulation, detection evasion), and the agent ecosystem
(L7: impersonation, marketplace and goal manipulation). The layer that carries the sharpest
lesson is L6, Security and Compliance, which is drawn cross-cutting every other layer rather than
stacked among them: the security agents you deploy to watch the system are themselves an attack
surface, so a mature design must monitor the monitors [@official_csa_maestro_threat_modeling];
[@official_owasp_agentic_ai_threats_mitigations].

#### Governance control: SRE circuit breaker

Knowing where attacks land is not the same as bounding their blast radius. The
author-defined SRE circuit-breaker teaching pattern, depicted in
[@fig:ageint-sre-circuit-breaker], borrows reliability vocabulary for a synthetic
governance tabletop, not a validated agent-safety threshold. In CLOSED the agent
operates only within explicit human-approved permissions. An illustrative
reliability budget may cover non-safety failures such as unavailable service or
tool timeouts; its limits must be declared for that exercise, not generalized
into a universal compliance percentage.

Authorization violations, private-data disclosure, and unsafe-action attempts
or execution are zero-tolerance breaches: immediately pause the affected agent
workflow, move to OPEN, preserve the record, and escalate to the accountable human.
Successful routine actions cannot offset these breaches in an averaged SLI.
Human review must establish containment and validate remediation before approving
limited restoration in HALF_OPEN, with restricted permissions and explicit stop
conditions. Any recurrence returns the workflow to OPEN. Returning to CLOSED
requires a separate, recorded human approval; a clean record or elapsed recovery
period never authorizes more autonomy automatically. Rehearse these transitions
with synthetic incident records, not live actions
[@scholarly_systems_security_agentic_computing].
"""
