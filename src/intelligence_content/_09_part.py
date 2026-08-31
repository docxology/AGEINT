from __future__ import annotations

from typing import Any

from markdown_refs import citation_ref, citation_ref_list

from ._01_part import CoursebookProfile, ResearchAnchor
from ._02_part import INTELLIGENCE_RESEARCH_ANCHORS
from ._05_part import PRACTICE_LENSES
from ._06_part import COURSEBOOK_PROFILES, anchor_references, expanded_profile_anchor_keys, practice_lens_for_titles, profile_for_titles
from .topic_entries import safe_topic_entries
from .topic_lesson_voice import compact_topic_cluster
from .markdown_table import table_cell


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
    rows = ["| Anchor | Source | Lane | Tier | Checked | Cadence | Refresh trigger | Verification note |", "|---|---|---|---|---|---|---|---|"]
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
    rows = ["| Anchor | Source | Lane | Contribution to the manuscript | Verification caveat |", "|---|---|---|---|---|"]
    updates = [anchor for anchor in INTELLIGENCE_RESEARCH_ANCHORS if anchor.checked_as_of >= cutoff or cutoff in anchor.verification_note]
    for anchor in updates:
        source = f"[{table_cell(anchor.title)}]({anchor.url})" if anchor.url else table_cell(anchor.title)
        caveat = _verification_note_for_table(anchor)
        if anchor.source_tier == "official_draft" and "draft status" not in caveat.lower():
            caveat = f"Draft status retained. {caveat}"
        rows.append(f"| {citation_ref(anchor.key)} | {source} | {table_cell(anchor.source_lane or anchor.domain)} | {table_cell(anchor.claim_scope)} | {table_cell(caveat)} |")
    return "\n".join(rows)


def citation_cluster(keys: tuple[str, ...], limit: int = 4) -> str:
    """Return a compact Pandoc citation cluster for a profile."""
    return citation_ref_list(keys[:limit]) + "."


def profile_triangulation_anchors(part_title: str, section_title: str = "", *, chapter: dict[str, object] | None = None, limit: int = 4, surface: str = "section") -> str:
    """Return a profile-specific triangulation sentence for claim-bearing sections."""
    profile = profile_for_titles(part_title, section_title, chapter=chapter)
    anchors = citation_cluster(expanded_profile_anchor_keys(profile), limit=limit)
    module_number = str(chapter.get("number", "")).strip() if chapter else ""
    local_scope = f"module {module_number}" if module_number else "this module"
    return (
        f"**Triangulation anchors.** In {local_scope}'s {surface}, directly "
        f"verified anchors for the **{profile.title}** lane include {anchors} Use "
        "them to test source-guide claims, method boundaries, governance constraints, "
        "and safety gates without replacing the module's `ageintNNN` provenance."
    )


def research_anchor_rows() -> str:
    """Render a compact table of curated research anchors."""
    rows = ["| Anchor | Domain | Lane | Tier | Checked | Refresh | Curriculum use |", "|---|---|---|---|---|---|---|"]
    for anchor in INTELLIGENCE_RESEARCH_ANCHORS:
        rows.append(
            f"| {citation_ref(anchor.key)} | {anchor.domain} | {anchor.source_lane or anchor.domain} | "
            f"{anchor.source_tier or anchor.source_type} | {anchor.checked_as_of} | "
            f"{anchor.refresh_cadence} | {anchor.note} |"
        )
    return "\n".join(rows)


def practice_lens_rows() -> str:
    """Render a compact table of reusable intelligence practice lenses."""
    rows = ["| Practice lens | Evidence artifact | Validation rule | Safety check |", "|---|---|---|---|"]
    for lens in PRACTICE_LENSES:
        rows.append(f"| {lens.title} | {lens.evidence_artifact} | {lens.validation_rule} | {lens.safety_check} |")
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
        f"Core anchors: {citation_cluster(expanded_profile_anchor_keys(profile), limit=3)} "
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
    topic_line = f"**Curriculum topic spine:** {', '.join(f'**{topic}**' for topic in distinct)}.\n\n" if distinct else ""
    anchor_rows = ["| Anchor | Why it matters here |", "|---|---|"]
    for anchor in anchor_references(expanded_profile_anchor_keys(profile))[:7]:
        anchor_rows.append(f"| {citation_ref(anchor.key)} | {anchor.note} Checked as of {anchor.checked_as_of}; role: {anchor.citation_role}. |")
    return "\n".join(
        [
            f"Research lane: **{profile.title}** for {topic_context}. {source_context}",
            "",
            topic_line.rstrip(),
            f"**Verified anchor cluster:** {citation_cluster(expanded_profile_anchor_keys(profile), limit=7)}",
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
