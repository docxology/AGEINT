from __future__ import annotations

# GENERIC_DISPLAY_TITLE_MARKERS and is_generic_display_title re-exported via _07_part merge.

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

def source_refresh_rows(limit: int | None = None) -> str:
    """Render source-refresh ledger rows for verified anchors."""
    rows = ["| Anchor | Lane | Tier | Checked | Cadence | Refresh trigger |", "|---|---|---|---|---|---|"]
    anchors = INTELLIGENCE_RESEARCH_ANCHORS if limit is None else INTELLIGENCE_RESEARCH_ANCHORS[:limit]
    for anchor in anchors:
        rows.append(
            f"| `@{anchor.key}` | {anchor.source_lane or anchor.domain} | "
            f"{anchor.source_tier or anchor.source_type} | {anchor.checked_as_of} | "
            f"{anchor.refresh_cadence} | {anchor.refresh_trigger} |"
        )
    return "\n".join(rows)

def safe_substitution_rows() -> str:
    """Render risky source motif to safe curriculum substitute rows."""
    rows = [
        "| Source motif | Unsafe source motif | Safe curriculum substitute | Blocked context |",
        "|---|---|---|---|",
    ]
    for item in SAFE_SUBSTITUTION_PATTERNS:
        rows.append(
            f"| {item['motif']} | {item['source_risk']} | "
            f"{item['substitute']} | {item['blocked_context']} |"
        )
    return "\n".join(rows)

def capstone_scaffold_rows() -> str:
    """Render reusable capstone workflow rows."""
    rows = ["| Phase | Artifact | Review gate |", "|---|---|---|"]
    for item in CAPSTONE_SCAFFOLDS:
        rows.append(f"| {item['phase']} | {item['artifact']} | {item['review_gate']} |")
    return "\n".join(rows)

def accessibility_review_rows() -> str:
    """Render accessibility and UDL review rows."""
    rows = ["| Step | Artifact | Review question |", "|---|---|---|"]
    for item in ACCESSIBILITY_REVIEW_STEPS:
        rows.append(f"| {item['step']} | {item['artifact']} | {item['review_question']} |")
    return "\n".join(rows)

def procurement_oversight_rows() -> str:
    """Render procurement and vendor oversight rows."""
    rows = ["| Step | Artifact | Review question |", "|---|---|---|"]
    for item in PROCUREMENT_OVERSIGHT_STEPS:
        rows.append(f"| {item['step']} | {item['artifact']} | {item['review_question']} |")
    return "\n".join(rows)

def hria_dpia_worksheet_rows() -> str:
    """Render HRIA and DPIA worksheet rows."""
    rows = ["| Dimension | Prompt | Evidence |", "|---|---|---|"]
    for item in HRIA_DPIA_WORKSHEET:
        rows.append(f"| {item['dimension']} | {item['prompt']} | {item['evidence']} |")
    return "\n".join(rows)

def data_lineage_registry_rows() -> str:
    """Render data lineage registry rows."""
    rows = ["| Object | Lineage field | Quality gate |", "|---|---|---|"]
    for item in DATA_LINEAGE_REGISTRY:
        rows.append(f"| {item['object']} | {item['lineage_field']} | {item['quality_gate']} |")
    return "\n".join(rows)

def assessment_integrity_rows() -> str:
    """Render assessment-integrity protocol rows."""
    rows = ["| Control | Student evidence | Instructor check |", "|---|---|---|"]
    for item in ASSESSMENT_INTEGRITY_PROTOCOL:
        rows.append(f"| {item['control']} | {item['student_evidence']} | {item['instructor_check']} |")
    return "\n".join(rows)

def agent_incident_response_rows() -> str:
    """Render agent incident response drill rows."""
    rows = ["| Phase | Drill action | Artifact |", "|---|---|---|"]
    for item in AGENT_INCIDENT_RESPONSE_DRILL:
        rows.append(f"| {item['phase']} | {item['drill_action']} | {item['artifact']} |")
    return "\n".join(rows)

def role_competency_rows() -> str:
    """Render role-based competency map rows."""
    rows = ["| Role | Competency | Evidence |", "|---|---|---|"]
    for item in ROLE_BASED_COMPETENCY_MAP:
        rows.append(f"| {item['role']} | {item['competency']} | {item['evidence']} |")
    return "\n".join(rows)

def adversarial_assurance_rows() -> str:
    """Render adversarial assurance cycle rows."""
    rows = ["| Stage | Challenge question | Artifact |", "|---|---|---|"]
    for item in ADVERSARIAL_ASSURANCE_CYCLE:
        rows.append(f"| {item['stage']} | {item['question']} | {item['artifact']} |")
    return "\n".join(rows)

def model_dataset_card_rows() -> str:
    """Render model-card and dataset-card documentation rows."""
    rows = ["| Field | Model card evidence | Dataset card evidence | Review gate |", "|---|---|---|---|"]
    for item in MODEL_DATASET_CARD:
        rows.append(
            f"| {item['field']} | {item['model_card']} | "
            f"{item['dataset_card']} | {item['review_gate']} |"
        )
    return "\n".join(rows)

def transparency_notice_rows() -> str:
    """Render transparency notice workflow rows."""
    rows = ["| Step | Artifact | Review gate |", "|---|---|---|"]
    for item in TRANSPARENCY_NOTICE_WORKFLOW:
        rows.append(f"| {item['step']} | {item['artifact']} | {item['review_gate']} |")
    return "\n".join(rows)

def retention_audit_rows() -> str:
    """Render records-retention and audit-trail rows."""
    rows = ["| Record | Retained fields | Audit question |", "|---|---|---|"]
    for item in RETENTION_AUDIT_TRAIL:
        rows.append(f"| {item['record']} | {item['retained_fields']} | {item['audit_question']} |")
    return "\n".join(rows)

def release_change_control_rows() -> str:
    """Render release and change-control gate rows."""
    rows = ["| Gate | Release evidence | Block condition |", "|---|---|---|"]
    for item in RELEASE_CHANGE_CONTROL_GATE:
        rows.append(f"| {item['gate']} | {item['release_evidence']} | {item['block_condition']} |")
    return "\n".join(rows)

def risk_exception_rows() -> str:
    """Render risk exception memo rows."""
    rows = ["| Field | Minimum content | Approval rule |", "|---|---|---|"]
    for item in RISK_EXCEPTION_MEMO:
        rows.append(f"| {item['field']} | {item['minimum_content']} | {item['approval_rule']} |")
    return "\n".join(rows)

def learner_support_rows() -> str:
    """Render learner support and accommodation plan rows."""
    rows = ["| Need | Support | Evidence |", "|---|---|---|"]
    for item in LEARNER_SUPPORT_PLAN:
        rows.append(f"| {item['need']} | {item['support']} | {item['evidence']} |")
    return "\n".join(rows)

def question_bank_rows() -> str:
    """Render instructor question-bank rows."""
    rows = ["| Question type | Prompt | Evidence |", "|---|---|---|"]
    for item in INSTRUCTOR_QUESTION_BANK:
        rows.append(f"| {item['question_type']} | {item['prompt']} | {item['evidence']} |")
    return "\n".join(rows)

def remediation_backlog_rows() -> str:
    """Render remediation backlog rows."""
    rows = ["| Backlog item | Trigger | Closure evidence |", "|---|---|---|"]
    for item in REMEDIATION_BACKLOG:
        rows.append(f"| {item['item']} | {item['trigger']} | {item['closure_evidence']} |")
    return "\n".join(rows)

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
            f"| `@{anchor.key}` | {anchor.domain} | {anchor.source_lane or anchor.domain} | "
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
    """Return prose summary of the added research spine."""
    domains = ", ".join(sorted({anchor.domain for anchor in INTELLIGENCE_RESEARCH_ANCHORS}))
    lanes = ", ".join(sorted({anchor.source_lane or anchor.domain for anchor in INTELLIGENCE_RESEARCH_ANCHORS}))
    return (
        f"Additional research hydration adds {len(INTELLIGENCE_RESEARCH_ANCHORS)} "
        f"directly citable official or scholarly anchors across domains {domains}. "
        f"Source lanes include {lanes}. "
        "Perplexity is used only for discovery and second-opinion synthesis; "
        "the manuscript cites the verified source URLs directly."
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
        f"Unit source path begins with {source_context}"
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
    return "; ".join(topics)

def chapter_practice_lens(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render a chapter-level practice lens."""
    title = str(chapter["title"])
    lens = practice_lens_for_titles(str(part["title"]), title)
    source_context = _chapter_ref_context(chapter)
    topic_context = _topic_context(chapter, part)
    return "\n".join(
        [
            f"**Practice lens for this module:** {lens.title}. Source context: {source_context}",
            "",
            f"**Planning question for this module:** {lens.planning_question} Apply it to {topic_context}.",
            "",
            f"**Evidence artifact for this module:** {lens.evidence_artifact}. Source context: {source_context}",
            "",
            f"**Validation rule for this module:** {lens.validation_rule}. Topic focus: {topic_context}.",
            "",
            f"**Handoff contract for this module:** {lens.handoff_contract}. Source context: {source_context}",
            "",
            f"**Safety check for this module:** {lens.safety_check}. Topic focus: {topic_context}.",
        ]
    )

def chapter_research_brief(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render chapter-level research synthesis."""
    title = str(chapter["title"])
    profile = profile_for_titles(str(part["title"]), title)
    distinct = list(dict.fromkeys(e.display_title for e in safe_topic_entries(chapter, part)))[:3]
    source_context = _chapter_ref_context(chapter)
    topic_context = "; ".join(distinct[:2]) if distinct else "the local topic cluster"
    topic_line = (
        "**Curriculum topic spine for this module:** "
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
            f"| `@{anchor.key}` | {anchor.note} Checked as of "
            f"{anchor.checked_as_of}; role: {anchor.citation_role}. |"
        )
    return "\n".join(
        [
            f"**Research lane for this module:** {profile.title}. Source context: {source_context}",
            "",
            topic_line.rstrip(),
            f"**Verified anchor cluster for this module:** {citation_cluster(profile.anchor_keys, limit=7)} Topic focus: {topic_context}.",
            "",
            f"**Conceptual depth for this module:** {profile.conceptual_focus}. Apply it to {topic_context}.",
            "",
            f"**Method stack for this module:** {profile.method_stack}. Source context: {source_context}",
            "",
            f"**Composability contract for this module:** {profile.composability_contract}. Topic focus: {topic_context}.",
            "",
            f"**Known failure modes for this module:** {profile.failure_modes}. Source context: {source_context}",
            "",
            f"**Defensive boundary for this module:** {profile.safety_boundary}. Topic focus: {topic_context}.",
            "",
            *anchor_rows,
        ]
    ).replace("\n\n\n", "\n\n")

def _table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()

def _coursebook_profile_for_titles(part_title: str, section_title: str = "") -> CoursebookProfile:
    profile = profile_for_titles(part_title, section_title)
    return COURSEBOOK_PROFILES[profile.identifier]

try:
    from intelligence_content.topic_entries import safe_topic_entries
except ImportError:  # pragma: no cover - merged namespace
    from .topic_entries import safe_topic_entries  # type: ignore[no-redef]
