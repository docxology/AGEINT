from __future__ import annotations

def _import_prior_parts(*module_names: str) -> None:
    import importlib

    for module_name in module_names:
        mod = importlib.import_module(f".{module_name}", __package__)
        globals().update({k: v for k, v in vars(mod).items() if not k.startswith("__")})


_import_prior_parts("_01_part", "_02_part", "_03_part", "_04_part", "_04b_part", "_05_part", "_06_part", "_07_part", "_08_part")

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
    return (
        f"**Research lane:** {profile.title}. "
        f"Core anchors: {citation_cluster(profile.anchor_keys, limit=3)} "
        f"Conceptual focus: {profile.conceptual_focus}. "
        f"Composability contract: {profile.composability_contract}. "
        f"**Practice lens:** {lens.title}; {lens.planning_question}"
    )


def chapter_practice_lens(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render a chapter-level practice lens."""
    title = str(chapter["title"])
    lens = practice_lens_for_titles(str(part["title"]), title)
    return "\n".join(
        [
            f"**Practice lens for {title}:** {lens.title}.",
            "",
            f"**Planning question for {title}:** {lens.planning_question}",
            "",
            f"**Evidence artifact for {title}:** {lens.evidence_artifact}.",
            "",
            f"**Validation rule for {title}:** {lens.validation_rule}.",
            "",
            f"**Handoff contract for {title}:** {lens.handoff_contract}.",
            "",
            f"**Safety check for {title}:** {lens.safety_check}.",
        ]
    )


def chapter_research_brief(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render chapter-level research synthesis."""
    title = str(chapter["title"])
    profile = profile_for_titles(str(part["title"]), title)
    distinct = list(dict.fromkeys(e.display_title for e in _safe_topic_entries(chapter, part)))[:3]
    topic_line = (
        f"**Curriculum topic spine for {title}:** "
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
            f"**Research lane for {title}:** {profile.title}.",
            "",
            topic_line.rstrip(),
            f"**Verified anchor cluster for {title}:** {citation_cluster(profile.anchor_keys, limit=7)}",
            "",
            f"**Conceptual depth for {title}:** {profile.conceptual_focus}.",
            "",
            f"**Method stack for {title}:** {profile.method_stack}.",
            "",
            f"**Composability contract for {title}:** {profile.composability_contract}.",
            "",
            f"**Known failure modes for {title}:** {profile.failure_modes}.",
            "",
            f"**Defensive boundary for {title}:** {profile.safety_boundary}.",
            "",
            *anchor_rows,
        ]
    ).replace("\n\n\n", "\n\n")


META_SOURCE_TOPIC_PREFIXES: Final[tuple[str, ...]] = (
    "v2 source-lane extension:",
    "deep expansion:",
    "evidence-package expansion:",
    "v2 ageint-depth extension:",
)


def _table_cell(value: str) -> str:
    return value.replace("|", "\\|").replace("\n", " ").strip()


def _coursebook_profile_for_titles(part_title: str, section_title: str = "") -> CoursebookProfile:
    profile = profile_for_titles(part_title, section_title)
    return COURSEBOOK_PROFILES[profile.identifier]


def _is_meta_source_topic(title: str) -> bool:
    lower = title.strip().lower()
    return any(lower.startswith(prefix) for prefix in META_SOURCE_TOPIC_PREFIXES)


def _normalize_display_key(title: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def _clean_display_title(title: str) -> str:
    cleaned = re.sub(r":\s*case\s+[\d.]+\s+review\s*$", "", title, flags=re.IGNORECASE)
    cleaned = re.sub(r"\s+review\s*$", "", cleaned, flags=re.IGNORECASE)
    return cleaned.strip() or title


def _safe_topic_entries(chapter: dict[str, Any], part: dict[str, Any]) -> list[TopicEntry]:
    """Return safe, learner-facing source topics with provenance metadata."""
    part_title = str(part["title"])
    chapter_title = str(chapter["title"])
    sections = chapter.get("sections", [])
    if not sections:
        return [
            TopicEntry(
                raw_title=chapter_title,
                display_title=chapter_title,
                source_locus="chapter",
                provenance_note="Parsed chapter title and citation spine",
                risk_category="standard",
            )
        ]

    entries: list[TopicEntry] = []
    seen_raw_titles: set[str] = set()
    seen_display_keys: set[str] = set()
    safe_patterns = chapter.get("number") == 32
    active_pattern_number: int | None = None
    for section in sections:
        raw_title = str(section.get("title", "source-guide topic")).strip()
        if _is_meta_source_topic(raw_title):
            continue
        if raw_title in seen_raw_titles:
            continue
        seen_raw_titles.add(raw_title)

        working_title = raw_title
        source_locus = str(section.get("number") or "").strip()
        provenance_note = f"{source_locus} {raw_title}".strip()
        risk_category = _topic_risk_category(raw_title, part_title, chapter_title)
        if safe_patterns:
            working_title, active_pattern_number = safe_pattern_treatment(
                working_title,
                active_pattern_number,
            )
            risk_category = "ageint_pattern_registry"
            source_locus = source_locus or (
                f"Pattern {active_pattern_number}" if active_pattern_number else "AGEINT pattern registry"
            )
            provenance_note = "Original source identity preserved in AGEINT pattern registry"

        display_title = (
            working_title
            if safe_patterns
            else safe_curriculum_treatment(working_title, part_title, chapter_title)
        )
        display_title = _clean_display_title(display_title)
        if not safe_patterns and is_generic_display_title(display_title):
            shard_fallback = _clean_display_title(working_title)
            if shard_fallback and not is_generic_display_title(shard_fallback):
                display_title = shard_fallback
        display_key = _normalize_display_key(display_title)
        if display_key in seen_display_keys:
            raw_key = _normalize_display_key(_clean_display_title(working_title))
            if raw_key != display_key:
                qualifier = source_locus or _topic_anchor_words(raw_title, limit=3)
                display_title = f"{display_title} ({qualifier})"
                display_key = _normalize_display_key(display_title)
            else:
                qualifier = _topic_anchor_words(raw_title, limit=4)
                display_title = f"{_clean_display_title(working_title)} ({qualifier})"
                display_key = _normalize_display_key(display_title)
        seen_display_keys.add(display_key)
        if risk_category != "standard" and risk_category != "ageint_pattern_registry":
            provenance_note = (
                f"{source_locus or 'chapter outline'} transformed from high-risk source title: "
                f"{raw_title}"
            )
        entries.append(
            TopicEntry(
                raw_title=raw_title,
                display_title=display_title,
                source_locus=source_locus or "chapter outline",
                provenance_note=provenance_note,
                risk_category=risk_category,
            )
        )

    if entries:
        return entries
    return [
        TopicEntry(
            raw_title=chapter_title,
            display_title=chapter_title,
            source_locus="chapter",
            provenance_note="Parsed chapter title and citation spine",
            risk_category="standard",
        )
    ]


