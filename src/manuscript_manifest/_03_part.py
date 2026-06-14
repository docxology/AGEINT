from __future__ import annotations

from typing import Any

from curriculum import PATTERN_REGISTRY_CHAPTER_NUMBER
from intelligence_content import (
    anchor_references,
    chapter_key_terms,
    chapter_knowledge_check,
    chapter_learning_outcomes,
    chapter_practice_lens,
    chapter_practice_sequence,
    chapter_research_brief,
    chapter_source_annotations,
    chapter_textbook_primer,
    chapter_topic_lessons,
    chapter_worked_example,
    practice_lens_for_titles,
    profile_triangulation_anchors,
    profile_for_titles,
    safe_topic_entries,
    subsection_practice_rows,
)
from citation_workflow import source_citation_spine

from ._01_part import (
    _chapter_source_context,
    _chapter_source_context_inline,
    _chapter_topic_context,
    _claim_evidence_ledger,
    _failure_mode_drill,
    _instructor_artifact,
    _review_checklist,
    _safe_practice_lab,
    _source_canon,
)
from ._02_part import (
    _capstone_deliverable,
    _instructor_facilitation_notes,
    _refresh_triggers,
    _runtime_section_map,
    _safe_substitution_patterns,
)
from ._heading_titles import chapter_landmark_titles




def _module_architecture(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    title = chapter["title"]
    profile = profile_for_titles(str(part["title"]), title, chapter=chapter)
    source_context = _chapter_source_context(chapter)
    topic_context = _chapter_topic_context(chapter, part)
    from _data_loaders import module_architecture

    architecture = module_architecture(profile.identifier)
    inputs, transforms, outputs, failures = architecture
    return "\n".join(
        [
            "#### Lineage and source tradition",
            "",
            (
                f"This sits in the **{profile.title}** lineage: "
                f"{profile.conceptual_focus}. {source_context}"
            ),
            "",
            "#### Working model",
            "",
            (
                "The work is modeled as inputs, constraints, transforms, outputs, "
                f"feedback, and oversight for {topic_context}, with provenance and reviewability throughout."
            ),
            "",
            "#### Knowledge architecture: inputs, transforms, outputs",
            "",
            f"- **Inputs:** {inputs}. {source_context}",
            f"- **Transforms:** {transforms}.",
            f"- **Outputs:** {outputs}.",
            f"- **Failure modes:** {failures}.",
            "",
            "#### Transfer contracts",
            "",
            f"- **Authority contract:** define why the work is being practiced, who reviews it, and which actions are excluded for {topic_context}.",
            f"- **Evidence contract:** keep the **{profile.title}** source descriptors, transformations, claims, uncertainty, and confidence separable.",
            "- **Tool contract:** bind any agent assistance to explicit tools, permissions, budgets, logging, and rollback conditions.",
            f"- **Output contract:** render the chapter artifact as {outputs} that another reviewer can audit.",
            "",
            "#### Profile emphasis and local focus",
            "",
            (
                f"The matched profile emphasizes {profile.conceptual_focus}. "
                f"The method stack is {profile.method_stack}; the local topic cluster is {topic_context}."
            ),
        ]
    )


def _governance_rights_assurance(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    title = chapter["title"]
    profile = profile_for_titles(str(part["title"]), title, chapter=chapter)
    lens = practice_lens_for_titles(str(part["title"]), title, chapter=chapter)
    source_context = _chapter_source_context(chapter)
    topic_context = _chapter_topic_context(chapter, part)
    return f"""#### Governance card

| Gate | Coursebook check | Evidence retained |
|---|---|---|
| Authority | The exercise has a lawful, educational, or defensive purpose and named reviewer. | scope card, excluded-action list, and reviewer initials |
| Evidence | Claims in this module remain tied to guide citations or verified anchors starting with {source_context} | claim ledger, source descriptors, caveats, and confidence language |
| Rights and access | Privacy, accessibility, learner support, and affected-group impacts are considered before reuse. | rights note, accommodation path, and unresolved-risk owner |
| Agent control | Any agent assistance stays bounded to retrieval, comparison, drafting, simulation, critique, or audit. | tool allowlist, prompt/output record, stop condition, and rollback note |
| Assurance | The artifact is challenged against **{profile.title}** failure modes and the **{lens.title}** safety check. | failure-mode note, remediation item, retest result, and refresh trigger |

#### Evidence package handoff

Detailed model/data cards, transparency notices, retention
rows, release gates, risk exceptions, incident drills, procurement checks, and
learner-support workflows live in the generated appendices and source-support docs.
The local **{lens.title}** evidence gate stays compact enough to apply during
reading, practice, and revision for {topic_context}.

{_current_source_assurance(chapter, part, profile, lens)}
"""


def _table_cell(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def _current_source_assurance(
    chapter: dict[str, Any],
    part: dict[str, Any],
    profile: Any,
    lens: Any,
) -> str:
    """Render a chapter-specific source assurance crosswalk."""
    source_context = _chapter_source_context(chapter)
    topic_context = _chapter_topic_context(chapter, part)
    rows = [
        "#### Current-source assurance",
        "",
        (
            "The source assurance check ties the current verified "
            "anchor set to the local chapter artifact instead of relying on "
            f"discovery summaries, here covering {topic_context}. {source_context}"
        ),
        "",
        "| Assurance question | Direct source evidence | Chapter artifact |",
        "|---|---|---|",
    ]
    for anchor in anchor_references(profile.anchor_keys)[:4]:
        lane = anchor.source_lane or anchor.domain
        use = anchor.assurance_use or anchor.note
        rows.append(
            f"| What does the module inherit from `{anchor.key}` for {topic_context}? | "
            f"{_table_cell(anchor.title)}; lane `{_table_cell(lane)}`; "
            f"checked {anchor.checked_as_of}. | "
            f"{_table_cell(lens.evidence_artifact)}; {_table_cell(use)} |"
        )
    rows.append(
        "| How is Perplexity handled here? | Discovery and second-opinion "
        "notes are not citable authority unless converted into direct official, "
        "standards-body, public-domain, or scholarly anchors. | Claim ledger records "
        "the direct URL, checked date, source lane, refresh trigger, and reviewer. |"
    )
    return "\n".join(rows)


def _domain_practice_studio(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    title = chapter["title"]
    lens = practice_lens_for_titles(str(part["title"]), title, chapter=chapter)
    topic_context = _chapter_topic_context(chapter, part)
    return f"""The studio converts reading into a reviewable artifact for {topic_context}. Start with
the lens question: **{lens.planning_question}**

### Studio moves

- Build a glossary card for each module source section.
- Create a concept map that links the module to prior curriculum areas and later AGEINT or cognitive-security material.
- Write a concise analytic note that states assumptions, evidence, confidence, alternatives, and oversight constraints.
- Pair each agent-assisted step with a human review decision, a stop condition, and a retained evidence artifact.

**Practice rail:** use public, benign, owned-lab, or synthetic material; preserve provenance and uncertainty notes.

### Safe practice lab

{_safe_practice_lab(chapter)}

### Failure modes

{_failure_mode_drill(chapter)}

### Safe substitution patterns

{_safe_substitution_patterns(chapter)}

### Instructor artifact

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
    topic_context = _chapter_topic_context(chapter, part)
    topic_rubric = ""
    if topic_rows:
        topic_rubric = f"""
| Topic | Evidence of mastery |
|---|---|
{topic_rows}
"""
    return f"""#### Capstone pathway

{_capstone_deliverable(chapter, part)}

#### Instructor facilitation notes

{_instructor_facilitation_notes(chapter, part)}

#### Assessment rubric
{topic_rubric}
The general competency and mastery rubric is the canonical
five-row rubric in the shared method-and-assurance reference
([@sec:method-assurance-reference]), covering conceptual command, analytic
rigor, agentic design, governance and rights, and safety posture. Score the
artifact for {topic_context} against that rubric together with the
topic-specific evidence rows above so conceptual command, uncertainty
handling, oversight design, rights evidence, and non-operational posture stay
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
intervention [@scholarly_systems_security_agentic_computing];
[@official_unu_macau_agentic_ai_boundaries].

The PolicyCompliance service-level indicator makes the 99-percent threshold concrete. Over a
review window of $N_{\\text{total}}$ governed actions with $N_{\\text{violations}}$ policy
violations, define

$$\\mathrm{PolicyCompliance}_{\\mathrm{SLI}} =
\\frac{N_{\\text{total}} - N_{\\text{violations}}}{N_{\\text{total}}} \\;\\ge\\; 0.99,$$

so the breaker's CLOSED state is exactly the region where this indicator clears its target. The
complementary error budget is the count of violations the window can absorb before the indicator
drops below target,

$$\\text{ErrorBudget} = (1 - 0.99)\\,N_{\\text{total}} = 0.01\\,N_{\\text{total}},
\\qquad \\text{breaker} \\to \\text{OPEN when } N_{\\text{violations}} > \\text{ErrorBudget}.$$

The budget burns down as violations accrue and is restored when a fresh window opens, which is the
quantity the safety-error-budget figure tracks. Have students compute the SLI on a synthetic action
log, set $N_{\\text{total}}$ for one window, and identify the exact violation count that trips the
breaker [@scholarly_systems_security_agentic_computing].
"""


def _chapter_body(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    title = chapter["title"]
    source_spine = source_citation_spine(chapter["citations"])
    source_context = _chapter_source_context(chapter)
    source_context_inline = _chapter_source_context_inline(chapter)
    topic_context = _chapter_topic_context(chapter, part)
    safe_patterns = chapter["number"] == PATTERN_REGISTRY_CHAPTER_NUMBER
    synthesis_block = _security_synthesis_block() if chapter["number"] == 34 else ""
    headings = chapter_landmark_titles(title)
    safety_boundary = (
        "Keep all practice authorized, synthetic, defensive, logged, "
        f"reversible, and non-operational while working from {source_context_inline} and {topic_context}. Do not convert it into "
        "live targeting, evasion, exploitation, covert collection, "
        "manipulation, or unsafe cyber-physical action."
    )
    if safe_patterns:
        safety_boundary = (
            "Raw design-pattern motifs are transformed into authorized tabletop, "
            "audit, provenance, control-coverage, and governance exercises. The "
            "module preserves source identity in the pattern registry while "
            f"rewriting methods, applications, and architecture artifacts for {topic_context} into "
            "non-operational curriculum treatments."
        )
    profile = profile_for_titles(str(part["title"]), title, chapter=chapter)
    lens = practice_lens_for_titles(str(part["title"]), title, chapter=chapter)
    return f"""This module teaches the **{profile.title}** lane through a bounded, source-backed coursebook chapter. {source_context}

## {headings["orientation"]}

### Textbook primer

{chapter_textbook_primer(chapter, part)}

### Learning outcomes

{chapter_learning_outcomes(chapter, part)}

### Core vocabulary

{chapter_key_terms(chapter, part)}

## {headings["practice"]}

### Topic lessons

{chapter_topic_lessons(chapter, part)}

### Worked safe example

{chapter_worked_example(chapter, part)}

### Practice sequence

{chapter_practice_sequence(chapter, part)}

### Knowledge check

{chapter_knowledge_check(chapter, part)}

## {headings["evidence"]}

### Module architecture and transfer contract

{_module_architecture(chapter, part)}

### Evidence canon and source spine

Guide citations preserve the inherited bibliography, verified anchors supply
lane constraints, and the **{profile.title}** profile tells reviewers what
evidence is strong enough for the module artifact built around {topic_context}.

#### Guide source spine

Primary guide citations: {source_spine}

#### Verified source canon

{_source_canon(chapter, part, source_spine)}

#### Intelligence practice lens

{chapter_practice_lens(chapter, part)}

#### Runtime-to-reader map

{_runtime_section_map(chapter, part)}

#### Reusable subsection contract

{subsection_practice_rows(chapter, part)}

#### Annotated source ledger

Each source cited by this **{profile.title}** module is paired below with its
real title and a one-line note on what it contributes to {topic_context}.

{chapter_source_annotations(chapter)}

## {headings["governance"]}

### Source-backed analytic synthesis

{profile_triangulation_anchors(str(part["title"]), title, chapter=chapter, surface="governance-boundary section")}

{chapter_research_brief(chapter, part)}

{synthesis_block}
#### Evidence standard and citation floor

Official
guidance supplies governance, safety, and legal constraints for the **{profile.title}**
lane; scholarly or policy-scholarship sources supply explanatory frames; source-guide
citations preserve the inherited AGEINT bibliography. Perplexity-assisted discovery
is allowed during maintenance, but the manuscript citation itself must resolve to a
direct source URL in `references-*.bib`. Local checks start with {source_context}

### Agentic translation: assist, approve, block

AGEINT translation is bounded by the **{profile.title}** lane.
Agents may organize sources, retrieve context, compare alternatives, draft
checklists, summarize evidence, simulate benign scenarios, and audit reasoning.
They do not initiate unauthorized collection, exploitation, covert targeting,
manipulation, or cyber-physical action; examples stay tied to {topic_context}.

#### Permitted defensive utility

The defensive utility is curriculum design, tabletop preparation,
risk assessment, governance review, source evaluation, and resilience planning.
Work products fit the current unit's education, policy review, lab
exercises, and authorized defensive analysis for {topic_context}.

#### Excluded operational boundary

{safety_boundary}

### Governance, rights, and assurance

Governance is practiced as a gate on the **{profile.title}**
lane. Learners use the **{lens.title}** to decide who authorized the exercise,
which evidence is sufficient, what rights and access issues remain, and when an
agent-assisted artifact must stop for human review while using {topic_context}.

{_governance_rights_assurance(chapter, part)}

## {headings["assessment"]}

### Assessment artifacts and capstone pathway

{_assessment_and_capstone_pathway(chapter, part)}

### Refresh, safety, and source maps

Source changes, unsafe wording, inaccessible artifacts, rights triggers, tool
incidents, and instructor debrief findings each produce a visible owner, action,
and retest condition before the module is reused against {source_context_inline} and {topic_context}.

#### Refresh triggers

{_refresh_triggers(chapter, part)}

#### Claim and evidence ledger

{_claim_evidence_ledger(chapter, part)}

### Reviewer challenge checklist

{_review_checklist(chapter, part)}
"""
