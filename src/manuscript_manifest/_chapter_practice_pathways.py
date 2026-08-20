"""Practice studio, pathway assessment, and synthesis block generators for manuscript chapters.

Extracted from _03_part.py so both modules remain comfortably under the 500-line cap.
"""

from __future__ import annotations

from typing import Any

from intelligence_content import (
    practice_lens_for_titles,
    safe_topic_entries,
)

from ._01_part import (
    _chapter_topic_context,
    _failure_mode_drill,
    _instructor_artifact,
    _safe_practice_lab,
)
from ._02_part import (
    _capstone_deliverable,
    _instructor_facilitation_notes,
    _safe_substitution_patterns,
)
from ._heading_titles import chapter_detail_titles


def _domain_practice_studio(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    title = chapter["title"]
    lens = practice_lens_for_titles(str(part["title"]), title, chapter=chapter)
    topic_context = _chapter_topic_context(chapter, part)
    return f"""The studio converts reading into a reviewable artifact for {topic_context}. Start with
the lens question: **{lens.planning_question}**

### {title} studio moves: glossary, concept map, analytic note, and agent review

- Build a glossary card for each module source section.
- Create a concept map that links the module to prior curriculum areas and later AGEINT or cognitive-security material.
- Write a concise analytic note that states assumptions, evidence, confidence, alternatives, and oversight constraints.
- Pair each agent-assisted step with a human review decision, a stop condition, and a retained evidence artifact.

**Practice rail:** use public, benign, owned-lab, or synthetic material; preserve provenance and uncertainty notes.

### {title} safe practice lab: accountable inputs and retained safety gates

{_safe_practice_lab(chapter)}

### {title} failure modes: source drift, unsafe transfer, and weak evidence

{_failure_mode_drill(chapter)}

### {title} safe substitution patterns: defensive artifacts for risky motifs

{_safe_substitution_patterns(chapter)}

### {title} instructor artifact: review packet and facilitation evidence

{_instructor_artifact(chapter)}
"""


def _topic_assessment_rows(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Topic-specific assessment rows tied to the chapter practice lens artifact."""
    title = str(chapter["title"])
    lens = practice_lens_for_titles(str(part["title"]), title, chapter=chapter)
    rows: list[str] = []
    seen_topics: set[str] = set()
    for entry in safe_topic_entries(chapter, part):
        topic_key = entry.display_title.strip().lower()
        if topic_key in seen_topics:
            continue
        seen_topics.add(topic_key)
        rows.append(
            f"| **{entry.display_title}** | Completed **{lens.evidence_artifact}** "
            "with source descriptor, caveat, uncertainty, blocked-use note, and "
            "named reviewer for this topic. |"
        )
        if len(rows) >= 3:
            break
    return "\n".join(rows)


def _assessment_and_capstone_pathway(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    topic_rows = _topic_assessment_rows(chapter, part)
    title = str(chapter["title"])
    topic_context = _chapter_topic_context(chapter, part)
    details = chapter_detail_titles(title)
    topic_rubric = ""
    if topic_rows:
        topic_rubric = f"""
| Topic | Evidence of mastery |
|---|---|
{topic_rows}
"""
    return f"""#### {details["capstone_pathway"]}

{_capstone_deliverable(chapter, part)}

#### {details["facilitation"]}

{_instructor_facilitation_notes(chapter, part)}

#### {details["rubric"]}
{topic_rubric}
The general competency and mastery rubric is the canonical
five-row rubric in the shared method-and-assurance reference
([@sec:method-assurance-reference]), covering conceptual command, analytic
rigor, agentic design, governance and rights, and safety posture. Score the
artifact for {topic_context} against that rubric together with the
topic-specific evidence rows above so conceptual command, uncertainty
handling, oversight design, rights evidence, and evidence-bounded posture stay
visible.
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
SRE circuit-breaker teaching pattern, depicted in [@fig:ageint-sre-circuit-breaker],
adapts reliability vocabulary into an author-defined governance exercise for
agents with three states. In CLOSED the agent operates normally, its autonomy
earned by a clean safety record; when the safety error budget is exhausted --
for this curriculum, when the PolicyCompliance service-level indicator falls
below 99 percent -- the breaker trips to OPEN and a human takes over; after a
recovery period plus validation it moves to HALF_OPEN with limited capability,
returning to CLOSED only if the clean record holds and snapping back to OPEN on
any new violation. Activation triggers include policy-bypass attempts,
LLM-provider errors, tool-timeout cascades, trust-score degradation, and
reasoning loops or deadlocks. Teach this as a defensive governance exercise:
define the PolicyCompliance SLI for a synthetic agent, set its error budget, and
rehearse the OPEN-state human takeover as a tabletop rather than a live
breaker [@scholarly_systems_security_agentic_computing].
"""
