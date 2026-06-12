from __future__ import annotations

from typing import Any, Final

from markdown_refs import citation_ref, citation_ref_list

from ._01_part import CoursebookProfile, ResearchAnchor
from ._02_part import INTELLIGENCE_RESEARCH_ANCHORS
from ._05_part import PRACTICE_LENSES
from ._06_part import (
    COURSEBOOK_PROFILES,
    anchor_references,
    practice_lens_for_titles,
    profile_for_titles,
)
from ._08_part import (
    ACCESSIBILITY_REVIEW_STEPS,
    ADVERSARIAL_ASSURANCE_CYCLE,
    AGENT_INCIDENT_RESPONSE_DRILL,
    ASSESSMENT_INTEGRITY_PROTOCOL,
    CAPSTONE_SCAFFOLDS,
    DATA_LINEAGE_REGISTRY,
    HRIA_DPIA_WORKSHEET,
    INSTRUCTOR_QUESTION_BANK,
    LEARNER_SUPPORT_PLAN,
    MODEL_DATASET_CARD,
    PROCUREMENT_OVERSIGHT_STEPS,
    RELEASE_CHANGE_CONTROL_GATE,
    RETENTION_AUDIT_TRAIL,
    RISK_EXCEPTION_MEMO,
    ROLE_BASED_COMPETENCY_MAP,
    SAFE_SUBSTITUTION_PATTERNS,
    TRANSPARENCY_NOTICE_WORKFLOW,
)
from .topic_entries import safe_topic_entries
from .topic_lesson_voice import compact_topic_cluster
from .markdown_table import render_dict_table, table_cell

# GENERIC_DISPLAY_TITLE_MARKERS and is_generic_display_title live in _07_safe_titles.

REMEDIATION_BACKLOG: Final[tuple[dict[str, str], ...]] = (
    {
        "item": "Unverified claim",
        "trigger": "claim lacks a guide citation or directly verified anchor",
        "closure_evidence": "verified source, removed claim, or explicit source-guide context note",
    },
    {
        "item": "Unsafe phrasing",
        "trigger": "wording implies live targeting, external action, exploitation, manipulation, or unsafe control",
        "closure_evidence": "safe substitute, blocked context, and reviewer sign-off",
    },
    {
        "item": "Accessibility defect",
        "trigger": "artifact cannot be inspected through an expected assistive or alternative workflow",
        "closure_evidence": "defect fix, alternative means, and retest result",
    },
    {
        "item": "Assurance gap",
        "trigger": "evaluation, release, exception, incident, or vendor evidence is incomplete",
        "closure_evidence": "owner, due date, retest, and accepted disposition",
    },
)

def source_lane_inventory() -> dict[str, list[ResearchAnchor]]:
    """Group curated anchors by source lane."""
    lanes: dict[str, list[ResearchAnchor]] = {}
    for anchor in INTELLIGENCE_RESEARCH_ANCHORS:
        lane = anchor.source_lane or anchor.domain
        lanes.setdefault(lane, []).append(anchor)
    return lanes

def source_lane_rows() -> str:
    """Render source-lane coverage for generated manuscript surfaces."""
    lanes = source_lane_inventory()
    rows = ["| Source lane | Anchor count | Refresh cadence | Claim scope |", "|---|---:|---|---|"]
    for lane in sorted(lanes):
        anchors = lanes[lane]
        cadences = ", ".join(sorted({anchor.refresh_cadence for anchor in anchors}))
        scopes = sorted({anchor.claim_scope for anchor in anchors})
        scope = scopes[0] if len(scopes) == 1 else f"{len(scopes)} scoped claim families"
        rows.append(f"| {lane} | {len(anchors)} | {cadences} | {scope} |")
    return "\n".join(rows)

def _verification_note_for_table(anchor: ResearchAnchor) -> str:
    """Return a compact, reader-facing verification note for a source anchor."""
    note = anchor.verification_note.strip()
    if not note:
        return "direct source review recorded"
    if len(note) <= 320:
        return note
    return note[:317].rstrip() + "..."


def source_refresh_rows(limit: int | None = None) -> str:
    """Render source-refresh ledger rows for verified anchors."""
    rows = [
        "| Anchor | Source | Lane | Tier | Checked | Cadence | Refresh trigger | Verification note |",
        "|---|---|---|---|---|---|---|---|",
    ]
    anchors = INTELLIGENCE_RESEARCH_ANCHORS if limit is None else INTELLIGENCE_RESEARCH_ANCHORS[:limit]
    for anchor in anchors:
        source = f"[{table_cell(anchor.title)}]({anchor.url})" if anchor.url else table_cell(anchor.title)
        rows.append(
            f"| {citation_ref(anchor.key)} | {source} | {table_cell(anchor.source_lane or anchor.domain)} | "
            f"{table_cell(anchor.source_tier or anchor.source_type)} | {anchor.checked_as_of} | "
            f"{table_cell(anchor.refresh_cadence)} | {table_cell(anchor.refresh_trigger)} | "
            f"{table_cell(_verification_note_for_table(anchor))} |"
        )
    return "\n".join(rows)


def current_source_update_rows(cutoff: str = "2026-06-06") -> str:
    """Render the current-source additions and refreshes from the latest audit pass."""
    rows = [
        "| Anchor | Source | Lane | Contribution to the manuscript | Verification caveat |",
        "|---|---|---|---|---|",
    ]
    updates = [
        anchor
        for anchor in INTELLIGENCE_RESEARCH_ANCHORS
        if anchor.checked_as_of >= cutoff or cutoff in anchor.verification_note
    ]
    for anchor in updates:
        source = f"[{table_cell(anchor.title)}]({anchor.url})" if anchor.url else table_cell(anchor.title)
        caveat = _verification_note_for_table(anchor)
        if anchor.source_tier == "official_draft" and "draft status" not in caveat.lower():
            caveat = f"Draft status retained. {caveat}"
        rows.append(
            f"| {citation_ref(anchor.key)} | {source} | {table_cell(anchor.source_lane or anchor.domain)} | "
            f"{table_cell(anchor.claim_scope)} | {table_cell(caveat)} |"
        )
    return "\n".join(rows)

def safe_substitution_rows() -> str:
    """Render risky source motif to safe curriculum substitute rows."""
    return render_dict_table(
        ("Source motif", "Unsafe source motif", "Safe curriculum substitute", "Blocked context"),
        SAFE_SUBSTITUTION_PATTERNS,
        ("motif", "source_risk", "substitute", "blocked_context"),
    )


def capstone_scaffold_rows() -> str:
    """Render reusable capstone workflow rows."""
    return render_dict_table(
        ("Phase", "Artifact", "Review gate"),
        CAPSTONE_SCAFFOLDS,
        ("phase", "artifact", "review_gate"),
    )


def accessibility_review_rows() -> str:
    """Render accessibility and UDL review rows."""
    return render_dict_table(
        ("Step", "Artifact", "Review question"),
        ACCESSIBILITY_REVIEW_STEPS,
        ("step", "artifact", "review_question"),
    )


def procurement_oversight_rows() -> str:
    """Render procurement and vendor oversight rows."""
    return render_dict_table(
        ("Step", "Artifact", "Review question"),
        PROCUREMENT_OVERSIGHT_STEPS,
        ("step", "artifact", "review_question"),
    )


def hria_dpia_worksheet_rows() -> str:
    """Render HRIA and DPIA worksheet rows."""
    return render_dict_table(
        ("Dimension", "Prompt", "Evidence"),
        HRIA_DPIA_WORKSHEET,
        ("dimension", "prompt", "evidence"),
    )


def data_lineage_registry_rows() -> str:
    """Render data lineage registry rows."""
    return render_dict_table(
        ("Object", "Lineage field", "Quality gate"),
        DATA_LINEAGE_REGISTRY,
        ("object", "lineage_field", "quality_gate"),
    )


def assessment_integrity_rows() -> str:
    """Render assessment-integrity protocol rows."""
    return render_dict_table(
        ("Control", "Student evidence", "Instructor check"),
        ASSESSMENT_INTEGRITY_PROTOCOL,
        ("control", "student_evidence", "instructor_check"),
    )


def agent_incident_response_rows() -> str:
    """Render agent incident response drill rows."""
    return render_dict_table(
        ("Phase", "Drill action", "Artifact"),
        AGENT_INCIDENT_RESPONSE_DRILL,
        ("phase", "drill_action", "artifact"),
    )


def role_competency_rows() -> str:
    """Render role-based competency map rows."""
    return render_dict_table(
        ("Role", "Competency", "Evidence"),
        ROLE_BASED_COMPETENCY_MAP,
        ("role", "competency", "evidence"),
    )


def adversarial_assurance_rows() -> str:
    """Render adversarial assurance cycle rows."""
    return render_dict_table(
        ("Stage", "Challenge question", "Artifact"),
        ADVERSARIAL_ASSURANCE_CYCLE,
        ("stage", "question", "artifact"),
    )


def model_dataset_card_rows() -> str:
    """Render model-card and dataset-card documentation rows."""
    return render_dict_table(
        ("Field", "Model card evidence", "Dataset card evidence", "Review gate"),
        MODEL_DATASET_CARD,
        ("field", "model_card", "dataset_card", "review_gate"),
    )


def transparency_notice_rows() -> str:
    """Render transparency notice workflow rows."""
    return render_dict_table(
        ("Step", "Artifact", "Review gate"),
        TRANSPARENCY_NOTICE_WORKFLOW,
        ("step", "artifact", "review_gate"),
    )


def retention_audit_rows() -> str:
    """Render records-retention and audit-trail rows."""
    return render_dict_table(
        ("Record", "Retained fields", "Audit question"),
        RETENTION_AUDIT_TRAIL,
        ("record", "retained_fields", "audit_question"),
    )


def release_change_control_rows() -> str:
    """Render release and change-control gate rows."""
    return render_dict_table(
        ("Gate", "Release evidence", "Block condition"),
        RELEASE_CHANGE_CONTROL_GATE,
        ("gate", "release_evidence", "block_condition"),
    )


def risk_exception_rows() -> str:
    """Render risk exception memo rows."""
    return render_dict_table(
        ("Field", "Minimum content", "Approval rule"),
        RISK_EXCEPTION_MEMO,
        ("field", "minimum_content", "approval_rule"),
    )


def learner_support_rows() -> str:
    """Render learner support and accommodation plan rows."""
    return render_dict_table(
        ("Need", "Support", "Evidence"),
        LEARNER_SUPPORT_PLAN,
        ("need", "support", "evidence"),
    )


def question_bank_rows() -> str:
    """Render instructor question-bank rows."""
    return render_dict_table(
        ("Question type", "Prompt", "Evidence"),
        INSTRUCTOR_QUESTION_BANK,
        ("question_type", "prompt", "evidence"),
    )


def remediation_backlog_rows() -> str:
    """Render remediation backlog rows."""
    return render_dict_table(
        ("Backlog item", "Trigger", "Closure evidence"),
        REMEDIATION_BACKLOG,
        ("item", "trigger", "closure_evidence"),
    )

def citation_cluster(keys: tuple[str, ...], limit: int = 4) -> str:
    """Return a compact Pandoc citation cluster for a profile."""
    return citation_ref_list(keys[:limit]) + "."

def research_anchor_rows() -> str:
    """Render a compact table of curated research anchors."""
    rows = [

        "| Anchor | Domain | Lane | Tier | Checked | Refresh | Curriculum use |",
        "|---|---|---|---|---|---|---|",
    ]
    for anchor in INTELLIGENCE_RESEARCH_ANCHORS:
        rows.append(
            f"| {citation_ref(anchor.key)} | {anchor.domain} | {anchor.source_lane or anchor.domain} | "
            f"{anchor.source_tier or anchor.source_type} | {anchor.checked_as_of} | "
            f"{anchor.refresh_cadence} | {anchor.note} |"
        )
    return "\n".join(rows)

def practice_lens_rows() -> str:
    """Render a compact table of reusable intelligence practice lenses."""
    rows = [
        "| Practice lens | Evidence artifact | Validation rule | Safety check |",
        "|---|---|---|---|",
    ]
    for lens in PRACTICE_LENSES:
        rows.append(
            f"| {lens.title} | {lens.evidence_artifact} | "
            f"{lens.validation_rule} | {lens.safety_check} |"
        )
    return "\n".join(rows)

def research_spine_summary() -> str:
    """Return prose summary of the added research spine.

    The abstract carries counts and representative examples rather than the full
    machine-readable slug lists; the complete domain and source-lane maps are
    generated separately for the curriculum orientation.
    """
    domain_count = len({anchor.domain for anchor in INTELLIGENCE_RESEARCH_ANCHORS})
    lane_count = len({anchor.source_lane or anchor.domain for anchor in INTELLIGENCE_RESEARCH_ANCHORS})
    return (
        f"The research layer adds {len(INTELLIGENCE_RESEARCH_ANCHORS)} directly "
        f"citable official or scholarly anchors spanning {domain_count} domains — "
        "including agentic AI governance, cyber threat intelligence, legal "
        "oversight, cognitive influence security, and OSINT/GEOINT — across "
        f"{lane_count} curated source lanes. The full domain and source-lane maps "
        "appear in the curriculum orientation. Perplexity is used only for "
        "discovery and second-opinion synthesis; the manuscript cites the verified "
        "source URLs directly."
    )

def part_research_brief(part: dict[str, Any]) -> str:
    """Render a short part-level research brief."""
    profile = profile_for_titles(str(part["title"]))
    lens = practice_lens_for_titles(str(part["title"]))
    source_context = _source_ref_context(_part_citation_numbers(part))
    return (
        f"**Research lane:** {profile.title}. "
        f"Core anchors: {citation_cluster(profile.anchor_keys, limit=3)} "
        f"Conceptual focus: {profile.conceptual_focus}. "
        f"Composability contract: {profile.composability_contract}. "
        f"**Practice lens:** {lens.title}; {lens.planning_question} "
        f"{source_context}"
    )

def _part_citation_numbers(part: dict[str, Any], *, limit: int = 2) -> list[int]:
    citations: list[int] = []
    for chapter in part.get("chapters", []):
        for number in chapter.get("citations", []):
            if number not in citations:
                citations.append(number)
            if len(citations) >= limit:
                return citations
    return citations

def _source_ref_context(citation_numbers: list[int], *, limit: int = 2) -> str:
    selected = list(citation_numbers[:limit])
    if not selected:
        return "the surrounding verified source spine"
    return citation_ref_list(f"ageint{number:03d}" for number in selected) + "."

def _chapter_ref_context(chapter: dict[str, Any]) -> str:
    return _source_ref_context(list(chapter.get("citations", [])))

def _topic_context(chapter: dict[str, Any], part: dict[str, Any], *, limit: int = 2) -> str:
    topics = [entry.display_title for entry in safe_topic_entries(chapter, part)[:limit]]
    if not topics:
        return "the local topic cluster"
    return f"**{compact_topic_cluster(topics)}**"

def chapter_practice_lens(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render a chapter-level practice lens."""
    title = str(chapter["title"])
    lens = practice_lens_for_titles(str(part["title"]), title)
    source_context = _chapter_ref_context(chapter)
    topic_context = _topic_context(chapter, part)
    return "\n".join(
        [
            f"Practice lens: **{lens.title}** for {topic_context}. {source_context}",
            "",
            f"**Planning question:** {lens.planning_question}",
            "",
            f"**Evidence artifact:** {lens.evidence_artifact}.",
            "",
            f"**Validation rule:** {lens.validation_rule}. Applied to {topic_context}.",
            "",
            f"**Handoff contract:** {lens.handoff_contract}.",
            "",
            f"**Safety check:** {lens.safety_check}.",
        ]
    )

def chapter_research_brief(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render chapter-level research synthesis."""
    title = str(chapter["title"])
    profile = profile_for_titles(str(part["title"]), title)
    distinct = list(dict.fromkeys(e.display_title for e in safe_topic_entries(chapter, part)))[:3]
    source_context = _chapter_ref_context(chapter)
    topic_context = f"**{'; '.join(distinct[:2])}**" if distinct else "the local topic cluster"
    topic_line = (
        "**Curriculum topic spine:** "
        f"{', '.join(f'**{topic}**' for topic in distinct)}.\n\n"
        if distinct
        else ""
    )
    anchor_rows = [
        "| Anchor | Why it matters here |",
        "|---|---|",
    ]
    for anchor in anchor_references(profile.anchor_keys)[:7]:
        anchor_rows.append(
            f"| {citation_ref(anchor.key)} | {anchor.note} Checked as of "
            f"{anchor.checked_as_of}; role: {anchor.citation_role}. |"
        )
    return "\n".join(
        [
            f"Research lane: **{profile.title}** for {topic_context}. {source_context}",
            "",
            topic_line.rstrip(),
            f"**Verified anchor cluster:** {citation_cluster(profile.anchor_keys, limit=7)}",
            "",
            f"**Conceptual depth:** {profile.conceptual_focus}.",
            "",
            f"**Method stack:** {profile.method_stack}.",
            "",
            f"**Composability contract:** {profile.composability_contract}.",
            "",
            f"**Known failure modes:** {profile.failure_modes}.",
            "",
            f"**Defensive boundary:** {profile.safety_boundary}. Applied to {topic_context}.",
            "",
            *anchor_rows,
        ]
    ).replace("\n\n\n", "\n\n")

def _table_cell(value: str) -> str:
    return table_cell(value)

def _coursebook_profile_for_titles(part_title: str, section_title: str = "") -> CoursebookProfile:
    profile = profile_for_titles(part_title, section_title)
    return COURSEBOOK_PROFILES[profile.identifier]
