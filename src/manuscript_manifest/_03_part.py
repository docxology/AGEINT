from __future__ import annotations

def _import_prior_parts(*module_names: str) -> None:
    import importlib

    for module_name in module_names:
        mod = importlib.import_module(f".{module_name}", __package__)
        globals().update({k: v for k, v in vars(mod).items() if not k.startswith("__")})


_import_prior_parts("_01_part", "_02_part")




def _module_architecture(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    title = chapter["title"]
    profile = profile_for_titles(str(part["title"]), title, chapter=chapter)
    architecture = {
        "governed_intelligence_cycle": (
            "requirements, audience needs, public-source evidence, caveats, and feedback signals",
            "requirement framing, collection scoping, source evaluation, analytic judgment, dissemination, and feedback review",
            "release-neutral brief, audience map, caveat register, and feedback note",
            "unscoped audiences, missing caveats, weak records, and product reuse without feedback",
        ),
        "analytic_tradecraft": (
            "reporting, assumptions, alternatives, confidence language, dissent, and source descriptors",
            "hypothesis generation, evidence sorting, assumption challenge, confidence calibration, and dissent capture",
            "analytic note, hypothesis table, assumption list, and confidence statement",
            "single-hypothesis reasoning, source laundering, confidence inflation, and suppressed dissent",
        ),
        "collection_management": (
            "authorized requirements, source-discipline choices, minimization rules, source-risk notes, and evaluation criteria",
            "priority mapping, source-discipline fit, least-intrusive evidence selection, and feedback review",
            "requirements matrix, collection-limit note, source-quality card, and gap list",
            "recruitment or interception drift, over-collection, weak minimization, and source exposure",
        ),
        "cyber_threat_intelligence": (
            "fabricated alerts, public taxonomy labels, incident context, supplier evidence, and handling rules",
            "indicator normalization, TTP mapping, confidence scoring, sharing review, and control-gap analysis",
            "defensive CTI packet, handling note, control implication, and incident-learning memo",
            "exploit detail leakage, indicator fixation, unvetted sharing, and unsupported attribution",
        ),
        "ics_ot_defense": (
            "synthetic process logs, asset/consequence maps, operator decisions, safety stops, and recovery evidence",
            "asset-consequence mapping, ATT&CK-for-ICS coverage review, operator-decision rehearsal, and after-action learning",
            "cyber-physical tabletop packet, debrief rubric, recovery note, and control-coverage map",
            "IT-first assumptions, unsafe actuation, live-control drift, and missing safety review",
        ),
        "legal_oversight": (
            "legal authorities, policy constraints, affected groups, retention duties, oversight roles, and audit logs",
            "authority mapping, proportionality review, rights-impact assessment, redress planning, and escalation routing",
            "authority-and-impact register, audit trail, redress note, and unresolved-risk owner",
            "authority laundering, missing audit trails, privacy overreach, and governance-as-afterthought",
        ),
    }.get(
        profile.identifier,
        (
            "source materials, domain constraints, learner questions, verified anchors, and artifact requirements",
            "evidence normalization, structured reasoning, source evaluation, governance review, and handoff preparation",
            "annotated map, decision memo, rubric, tabletop packet, or audit artifact",
            "over-automation, misplaced confidence, policy drift, and confusing simulation with deployment",
        ),
    )
    inputs, transforms, outputs, failures = architecture
    return "\n".join(
        [
            "### Historical lineage",
            "",
            (
                f"**{title}** sits in the **{profile.title}** lineage: "
                f"{profile.conceptual_focus}."
            ),
            "",
            "### Conceptual model",
            "",
            (
                f"**{title}** is modeled as inputs, constraints, transforms, outputs, "
                "feedback, and oversight—with provenance and reviewability throughout."
            ),
            "",
            "### Knowledge architecture",
            "",
            f"- **Inputs for {title}:** {inputs}.",
            f"- **Transforms:** {transforms}.",
            f"- **Outputs:** {outputs}.",
            f"- **Failure modes:** {failures}.",
            "",
            "### Composability contracts",
            "",
            f"- **Authority contract:** define why **{title}** is being practiced, who reviews it, and which actions are excluded.",
            f"- **Evidence contract:** keep the **{profile.title}** source descriptors, transformations, claims, uncertainty, and confidence separable.",
            "- **Tool contract:** bind any agent assistance to explicit tools, permissions, budgets, logging, and rollback conditions.",
            f"- **Output contract:** render the chapter artifact as {outputs} that another reviewer can audit.",
            "",
            "### Profile-specific emphasis",
            "",
            (
                f"The **{title}** matched profile emphasizes {profile.conceptual_focus}. "
                f"The method stack is {profile.method_stack}."
            ),
        ]
    )


def _governance_rights_assurance(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    title = chapter["title"]
    profile = profile_for_titles(str(part["title"]), title, chapter=chapter)
    lens = practice_lens_for_titles(str(part["title"]), title, chapter=chapter)
    return f"""### Chapter governance card

| Gate | Coursebook check | Evidence retained |
|---|---|---|
| Authority | The exercise has a lawful, educational, or defensive purpose and named reviewer. | scope card, excluded-action list, and reviewer initials |
| Evidence | Claims in **{title}** remain tied to guide citations or verified anchors. | claim ledger, source descriptors, caveats, and confidence language |
| Rights and access | Privacy, accessibility, learner support, and affected-group impacts are considered before reuse. | rights note, accommodation path, and unresolved-risk owner |
| Agent control | Any agent assistance stays bounded to retrieval, comparison, drafting, simulation, critique, or audit. | tool allowlist, prompt/output record, stop condition, and rollback note |
| Assurance | The artifact is challenged against **{profile.title}** failure modes and the **{lens.title}** safety check. | failure-mode note, remediation item, retest result, and refresh trigger |

### Evidence package pointer

For **{title}**, detailed model/data cards, transparency notices, retention
rows, release gates, risk exceptions, incident drills, procurement checks, and
learner-support workflows live in the generated appendices and source-support docs.
The local **{lens.title}** evidence gate stays compact enough to apply during
reading, practice, and revision.

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
    rows = [
        "### Current-source assurance crosswalk",
        "",
        (
            f"For **{title}**, the source assurance check ties the current verified "
            "anchor set to the local chapter artifact instead of relying on "
            "discovery summaries."
        ),
        "",
        "| Assurance question | Direct source evidence | Chapter artifact |",
        "|---|---|---|",
    ]
    for anchor in anchor_references(profile.anchor_keys)[:4]:
        lane = anchor.source_lane or anchor.domain
        use = anchor.assurance_use or anchor.note
        rows.append(
            f"| What does **{title}** inherit from `{anchor.key}`? | "
            f"{_table_cell(anchor.title)}; lane `{_table_cell(lane)}`; "
            f"checked {anchor.checked_as_of}. | "
            f"{_table_cell(lens.evidence_artifact)}; {_table_cell(use)} |"
        )
    rows.append(
        f"| How is Perplexity handled for **{title}**? | Discovery and second-opinion "
        "notes are not citable authority unless converted into direct official, "
        "standards-body, public-domain, or scholarly anchors. | Claim ledger records "
        "the direct URL, checked date, source lane, refresh trigger, and reviewer. |"
    )
    return "\n".join(rows)


def _domain_practice_studio(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    title = chapter["title"]
    lens = practice_lens_for_titles(str(part["title"]), title, chapter=chapter)
    return f"""The studio converts **{title}** from reading into a reviewable artifact. Start with
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
    for entry in _safe_topic_entries(chapter, part):
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
    topic_rubric = ""
    if topic_rows:
        topic_rubric = f"""
| Topic | Evidence of mastery |
|---|---|
{topic_rows}
"""
    return f"""### Capstone pathway

{_capstone_deliverable(chapter, part)}

### Instructor facilitation notes

{_instructor_facilitation_notes(chapter)}

### Assessment rubric
{topic_rubric}
| Competency | Evidence of mastery |
|---|---|
| Conceptual command | Terms are defined precisely and linked to the source spine. |
| Analytic rigor | Assumptions, uncertainty, alternatives, and confidence are explicit. |
| Agentic design | Human oversight, tool boundaries, logging, and rollback are specified. |
| Governance and rights | Authority, procurement, privacy, accessibility, retention, and redress evidence are visible. |
| Safety posture | Exercises remain authorized, synthetic, defensive, lawful, and non-operational. |
"""


def _chapter_body(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    title = chapter["title"]
    source_spine = citation_spine(chapter["citations"])
    safe_patterns = chapter["number"] == 32
    safety_boundary = (
        f"For **{title}**, keep all practice authorized, synthetic, defensive, logged, "
        "reversible, and non-operational. Do not convert this module into "
        "live targeting, evasion, exploitation, covert collection, "
        "manipulation, or unsafe cyber-physical action."
    )
    if safe_patterns:
        safety_boundary = (
            f"For **{title}**, raw design-pattern motifs are transformed into authorized tabletop, "
            "audit, provenance, control-coverage, and governance exercises. The "
            "module preserves source identity in the pattern registry while "
            "rewriting methods, applications, and architecture artifacts into "
            "non-operational curriculum treatments."
        )
    profile = profile_for_titles(str(part["title"]), title, chapter=chapter)
    lens = practice_lens_for_titles(str(part["title"]), title, chapter=chapter)
    return f"""**{title}** belongs to **{part['title']}** and teaches the **{profile.title}** lane through a bounded, source-backed coursebook chapter.

## Textbook primer

{chapter_textbook_primer(chapter, part)}

## Learning outcomes

{chapter_learning_outcomes(chapter, part)}

## Core vocabulary

{chapter_key_terms(chapter, part)}

## Topic lessons

{chapter_topic_lessons(chapter, part)}

## Worked safe example

{chapter_worked_example(chapter, part)}

## Practice sequence

{chapter_practice_sequence(chapter, part)}

## Knowledge check

{chapter_knowledge_check(chapter, part)}

## Module architecture

{_module_architecture(chapter, part)}

## Evidence and source canon

For **{title}**, the source canon is the audit trail. Guide citations preserve
the inherited bibliography, verified anchors supply lane constraints, and the
**{profile.title}** profile tells reviewers what evidence is strong enough for
the module artifact.

### Source spine

Primary guide citations for this module: {source_spine}

### Source canon

{_source_canon(chapter, part, source_spine)}

### Intelligence practice lens

{chapter_practice_lens(chapter, part)}

### Runtime section map

{_runtime_section_map(chapter, part)}

### Fractal subsection map

{subsection_practice_rows(chapter, part)}

## Research-backed synthesis

{chapter_research_brief(chapter, part)}

### Evidence standard

Each **{title}** source is treated as an anchor, not a decoration. Official
guidance supplies governance, safety, and legal constraints for the **{profile.title}**
lane; scholarly or policy-scholarship sources supply explanatory frames; source-guide
citations preserve the inherited AGEINT bibliography. Perplexity-assisted discovery
is allowed during maintenance, but the manuscript citation itself must resolve to a
direct source URL in `references-*.bib`.

## Agentic translation boundary

AGEINT translation for **{title}** is bounded by the **{profile.title}** lane.
Agents may organize sources, retrieve context, compare alternatives, draft
checklists, summarize evidence, simulate benign scenarios, and audit reasoning.
They do not initiate unauthorized collection, exploitation, covert targeting,
manipulation, or cyber-physical action.

### Defensive utility

The defensive utility of **{title}** is curriculum design, tabletop preparation,
risk assessment, governance review, source evaluation, and resilience planning.
Work products should fit **{part['title']}** education, policy review, lab
exercises, and authorized defensive analysis.

### Safety boundary

{safety_boundary}

## Governance, rights, and assurance

For **{title}**, governance is practiced as a gate on the **{profile.title}**
lane. Learners use the **{lens.title}** to decide who authorized the exercise,
which evidence is sufficient, what rights and access issues remain, and when an
agent-assisted artifact must stop for human review.

{_governance_rights_assurance(chapter, part)}

## Assessment artifacts and capstone pathway

{_assessment_and_capstone_pathway(chapter, part)}

## Refresh, safety, and source maps

Refresh handling for **{title}** is maintenance evidence, not editorial memory.
Source changes, unsafe wording, inaccessible artifacts, rights triggers, tool
incidents, and instructor debrief findings all produce a visible owner, action,
and retest condition before the module is reused.

### Refresh triggers

{_refresh_triggers(chapter)}

### Safety boundary

{safety_boundary}

### Claim and evidence ledger

{_claim_evidence_ledger(chapter, part)}

## Review checklist

{_review_checklist(chapter)}
"""
