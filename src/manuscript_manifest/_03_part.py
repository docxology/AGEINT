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
    expanded_profile_anchor_keys,
    practice_lens_for_titles,
    profile_triangulation_anchors,
    profile_for_titles,
    subsection_practice_rows,
)
from citation_workflow import source_citation_spine
from ._chapter_practice_pathways import (
    _assessment_and_capstone_pathway,
    _security_synthesis_block,
)

from ._01_part import (
    _chapter_source_context,
    _chapter_source_context_inline,
    _chapter_topic_context,
    _claim_evidence_ledger,
    _review_checklist,
    _source_canon,
)
from ._02_part import (
    _refresh_triggers,
    _runtime_section_map,
)
from ._heading_titles import (
    chapter_detail_titles,
    chapter_landmark_titles,
    chapter_scaffold_titles,
    chapter_teaching_titles,
)


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
            f"#### {title} lineage and source tradition: profile, concepts, and first anchors",
            "",
            (
                f"This sits in the **{profile.title}** lineage: "
                f"{profile.conceptual_focus}. {source_context}"
            ),
            "",
            f"#### {title} working model: inputs, constraints, transforms, outputs, and oversight",
            "",
            (
                "The work is modeled as inputs, constraints, transforms, outputs, "
                f"feedback, and oversight for {topic_context}, with provenance and reviewability throughout."
            ),
            "",
            f"#### {title} knowledge architecture: inputs, transforms, outputs, and failure checks",
            "",
            f"- **Inputs:** {inputs}. {source_context}",
            f"- **Transforms:** {transforms}.",
            f"- **Outputs:** {outputs}.",
            f"- **Failure modes:** {failures}.",
            "",
            f"#### {title} transfer contracts: authority, evidence, tools, and auditable output",
            "",
            f"- **Authority contract:** define why the work is being practiced, who reviews it, and which actions are excluded for {topic_context}.",
            f"- **Evidence contract:** keep the **{profile.title}** source descriptors, transformations, claims, uncertainty, and confidence separable.",
            "- **Tool contract:** bind any agent assistance to explicit tools, permissions, budgets, logging, and rollback conditions.",
            f"- **Output contract:** render the chapter artifact as {outputs} that another reviewer can audit.",
            "",
            f"#### {title} profile emphasis and local focus: method stack and topic cluster",
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
    details = chapter_detail_titles(title)
    return f"""#### {details["governance_card"]}

| Gate | Coursebook check | Evidence retained |
|---|---|---|
| Authority | The exercise has a lawful, educational, or defensive purpose and named reviewer. | scope card, excluded-action list, and reviewer initials |
| Evidence | Claims in this module remain tied to guide citations or verified anchors starting with {source_context} | claim ledger, source descriptors, caveats, and confidence language |
| Rights and access | Privacy, accessibility, learner support, and affected-group impacts are considered before reuse. | rights note, accommodation path, and unresolved-risk owner |
| Agent control | Any agent assistance stays bounded to retrieval, comparison, drafting, simulation, critique, or audit. | tool allowlist, prompt/output record, stop condition, and rollback note |
| Assurance | The artifact is challenged against **{profile.title}** failure modes and the **{lens.title}** safety check. | failure-mode note, remediation item, retest result, and refresh trigger |

#### {details["evidence_handoff"]}

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
    title = str(chapter["title"])
    source_context = _chapter_source_context(chapter)
    topic_context = _chapter_topic_context(chapter, part)
    details = chapter_detail_titles(title)
    rows = [
        f"#### {details['current_source']}",
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
    for anchor in anchor_references(expanded_profile_anchor_keys(profile))[:4]:
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


def _chapter_body(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    title = chapter["title"]
    source_spine = source_citation_spine(chapter["citations"])
    source_context = _chapter_source_context(chapter)
    source_context_inline = _chapter_source_context_inline(chapter)
    topic_context = _chapter_topic_context(chapter, part)
    safe_patterns = chapter["number"] == PATTERN_REGISTRY_CHAPTER_NUMBER
    synthesis_block = _security_synthesis_block() if chapter["number"] == 34 else ""
    safety_boundary = (
        "Keep all practice accountable, synthetic, defensive, logged, "
        f"reversible, and evidence-bounded while working from {source_context_inline} and {topic_context}. Do not convert it into "
        "live targeting, evasion, exploitation, covert collection, "
        "manipulation, or unsafe cyber-physical action."
    )
    if safe_patterns:
        safety_boundary = (
            "Raw design-pattern motifs are transformed into accountable tabletop, "
            "audit, provenance, control-coverage, and governance exercises. The "
            "module preserves source identity in the pattern registry while "
            f"rewriting methods, applications, and architecture artifacts for {topic_context} into "
            "evidence-bounded curriculum treatments."
        )
    profile = profile_for_titles(str(part["title"]), title, chapter=chapter)
    lens = practice_lens_for_titles(str(part["title"]), title, chapter=chapter)
    headings = chapter_landmark_titles(
        title,
        profile_title=profile.title,
        practice_lens_title=lens.title,
    )
    scaffolds = chapter_scaffold_titles(title)
    details = chapter_detail_titles(title)
    teaching = chapter_teaching_titles(title)
    return f"""This module teaches the **{profile.title}** lane through a bounded, source-backed coursebook chapter. {source_context}

## {headings["frame"]}

### {scaffolds["orientation"]}

### {teaching["primer"]}

{chapter_textbook_primer(chapter, part)}

### {teaching["outcomes"]}

{chapter_learning_outcomes(chapter, part)}

### {teaching["vocabulary"]}

{chapter_key_terms(chapter, part)}

## {headings["path"]}

### {scaffolds["practice"]}

### {teaching["lessons"]}

{chapter_topic_lessons(chapter, part)}

### {teaching["example"]}

{chapter_worked_example(chapter, part)}

### {teaching["sequence"]}

{chapter_practice_sequence(chapter, part)}

### {teaching["check"]}

{chapter_knowledge_check(chapter, part)}

## {headings["assurance"]}

### {scaffolds["evidence"]}

### {details["architecture"]}

{_module_architecture(chapter, part)}

### {details["evidence"]}

Guide citations preserve the inherited bibliography, verified anchors supply
lane constraints, and the **{profile.title}** profile tells reviewers what
evidence is strong enough for the module artifact built around {topic_context}.

#### {details["source_spine"]}

Primary guide citations: {source_spine}

#### {details["verified_canon"]}

{_source_canon(chapter, part, source_spine)}

#### {details["practice_lens"]}

{chapter_practice_lens(chapter, part)}

#### {details["runtime_map"]}

{_runtime_section_map(chapter, part)}

#### {details["subsection_contract"]}

{subsection_practice_rows(chapter, part)}

#### {details["source_ledger"]}

Each source cited by this **{profile.title}** module is paired below with its
real title and a one-line note on what it contributes to {topic_context}.

{chapter_source_annotations(chapter)}

### {scaffolds["governance"]}

### {details["synthesis"]}

{profile_triangulation_anchors(str(part["title"]), title, chapter=chapter, surface="governance-boundary section")}

{chapter_research_brief(chapter, part)}

{synthesis_block}
#### {details["evidence_standard"]}

Official
guidance supplies governance, safety, and legal constraints for the **{profile.title}**
lane; scholarly or policy-scholarship sources supply explanatory frames; source-guide
citations preserve the inherited AGEINT bibliography. Perplexity-assisted discovery
is allowed during maintenance, but the manuscript citation itself must resolve to a
direct source URL in `references-*.bib`. Local checks start with {source_context}

### {details["agentic"]}

AGEINT translation is bounded by the **{profile.title}** lane.
Agents may organize sources, retrieve context, compare alternatives, draft
checklists, summarize evidence, simulate benign scenarios, and audit reasoning.
They do not initiate unauthorized collection, exploitation, covert targeting,
manipulation, or cyber-physical action; examples stay tied to {topic_context}.

#### {details["permitted_utility"]}

The defensive utility is curriculum design, tabletop preparation,
risk assessment, governance review, source evaluation, and resilience planning.
Work products fit the current unit's education, policy review, lab
exercises, and accountable defensive analysis for {topic_context}.

#### {details["excluded_boundary"]}

{safety_boundary}

### {details["governance"]}

Governance is practiced as a gate on the **{profile.title}**
lane. Learners use the **{lens.title}** to decide who is accountable for the exercise,
which evidence is sufficient, what rights and access issues remain, and when an
agent-assisted artifact must stop for human review while using {topic_context}.

{_governance_rights_assurance(chapter, part)}

### {scaffolds["assessment"]}

### {details["assessment"]}

{_assessment_and_capstone_pathway(chapter, part)}

### {details["refresh"]}

Source changes, unsafe wording, inaccessible artifacts, rights triggers, tool
incidents, and instructor debrief findings each produce a visible owner, action,
and retest condition before the module is reused against {source_context_inline} and {topic_context}.

#### {details["refresh_triggers"]}

{_refresh_triggers(chapter, part)}

#### {details["claim_ledger"]}

{_claim_evidence_ledger(chapter, part)}

### {details["review"]}

{_review_checklist(chapter, part)}
"""
