from __future__ import annotations

from typing import Any

from curriculum import PATTERN_REGISTRY_CHAPTER_NUMBER
from intelligence_content.topic_entries import clean_display_title
from intelligence_content import practice_lens_for_titles, safe_curriculum_treatment, safe_pattern_treatment

from ._01_part import _chapter_source_context, _chapter_topic_context


def _capstone_deliverable(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    topic_context = _chapter_topic_context(chapter, part)
    return "\n".join(
        [
            "The capstone deliverable is a reviewable packet that "
            "plugs into the broader unit thread. Run it through the canonical "
            "phase, artifact, and review-gate ladder in the shared "
            f"method-and-assurance reference ([@sec:method-assurance-reference]); the local topic "
            f"cluster is {topic_context}.",
            "",
            "Minimum module submission: one-page analytic memo, source-lane map, "
            "claim ledger, safe-lab packet, rubric self-assessment, and debrief "
            "note. The packet must name what is excluded, who may approve reuse, "
            f"and what would trigger a source refresh for {topic_context} and {source_context}",
        ]
    )


def _instructor_facilitation_notes(chapter: dict[str, Any], part: dict[str, Any] | None = None) -> str:
    source_context = _chapter_source_context(chapter)
    topic_context = _chapter_topic_context(chapter, part) if part is not None else "the local topic cluster"
    return "\n".join(
        [
            f"Facilitate as a bounded studio around {topic_context}, not as a lecture-only session.",
            "",
            f"- Start with the authority card and excluded-action list before showing examples from {topic_context} and {source_context}",
            "- Assign one learner to maintain the claim ledger and one learner to challenge source quality.",
            "- Keep agent prompts visible enough for review and separate from final judgment.",
            "- Pause any activity that drifts toward live systems, real people, sensitive data, or external action.",
            "- End with a debrief that separates evidence learned, uncertainty preserved, rights impact, and next refresh owner.",
        ]
    )


def _refresh_triggers(chapter: dict[str, Any], part: dict[str, Any] | None = None) -> str:
    source_context = _chapter_source_context(chapter)
    topic_context = _chapter_topic_context(chapter, part) if part is not None else "the local topic cluster"
    return (
        "Refresh against the canonical trigger-and-action table in "
        "the shared method-and-assurance reference ([@sec:method-assurance-reference]). "
        "When a source-guide reference, official standard, AI or public-sector "
        "policy, interface specification, safety audit, or instructor debrief "
        f"signal appears, take the matching required action before reuse for "
        f"{topic_context}. The local signals begin with {source_context}"
    )


def _reader_section_title(source_title: str, part_title: str = "", chapter_title: str = "") -> str:
    """Normalize source-guide pseudo-headings into reader-facing titles."""
    title = source_title.strip()
    lower = title.lower()
    if lower.startswith("pattern ") or lower.startswith("safe methods:") or lower.startswith("safe defensive") or lower.startswith("safe architecture"):
        return title
    if lower.startswith("v2 source-lane extension:"):
        return "Source-lane evidence, public registers, and claim-ledger studio"
    if lower.startswith("deep expansion:"):
        return "Bounded autonomy, procurement, incident-response, and assurance studio"
    if lower.startswith("evidence-package expansion:"):
        return "Model-card, recoverability, retention, and learner-support evidence package"
    if lower.startswith("v2 ageint-depth extension:"):
        return "AGEINT pattern registry, agent identity, and interface-contract studio"
    # clean_display_title strips bare quantitative vendor-marketing claims so a
    # source headline like "...: 500% Productivity Increase" never stands as the
    # rendered section title (the figures are unsourced and unframed here).
    return clean_display_title(safe_curriculum_treatment(title, part_title, chapter_title))


def _reader_provenance_title(source_title: str) -> str:
    """Keep provenance useful without leaking scaffold wording into prose.

    Bare quantitative marketing claims are stripped here too so the "original:
    ..." provenance trail does not restate an unsourced vendor figure as fact.
    """
    from prose_policy import reader_source_title

    return clean_display_title(reader_source_title(source_title))


def _runtime_section_map(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render source-guide sections as polished runtime/provenance rows."""
    sections = chapter.get("sections", [])
    if not sections:
        lens = practice_lens_for_titles(str(part["title"]), str(chapter["title"]), chapter=chapter)
        return "\n".join(
            [
                "| Rendered title | Source loci | Source provenance | Practice lens | Evidence artifact | Safety check |",
                "|---|---|---|---|---|---|",
                (f"| Module source spine | Module source spine | Parsed chapter title and citation spine | {lens.title} | {lens.evidence_artifact} | {lens.safety_check} |"),
            ]
        )

    rows = ["| Rendered title | Source loci | Source provenance | Practice lens | Evidence artifact | Safety check |", "|---|---|---|---|---|---|"]
    safe_patterns = chapter.get("number") == PATTERN_REGISTRY_CHAPTER_NUMBER
    active_pattern_number: int | None = None
    for section in sections:
        source_title = str(section.get("title", "module section"))
        source_title_for_provenance = _reader_provenance_title(source_title)
        source_number = str(section.get("number", "")).strip()
        working_title = source_title
        provenance = f"{source_number} {source_title_for_provenance}".strip()

        if safe_patterns:
            working_title, active_pattern_number = safe_pattern_treatment(working_title, active_pattern_number)
            provenance = "Source identity preserved in pattern registry with safe classroom treatment"

        rendered_title = _reader_section_title(working_title, str(part["title"]), str(chapter["title"]))
        source_locus = str(section.get("number") or "module section")
        if not safe_patterns and rendered_title != source_title:
            provenance = f"{source_locus} source title transformed into safe curriculum treatment; original: {source_title_for_provenance}"
        lens = practice_lens_for_titles(str(part["title"]), rendered_title, chapter=chapter)
        rows.append(f"| {rendered_title} | {source_locus} | {provenance} | {lens.title} | {lens.evidence_artifact} | {lens.safety_check} |")
    return "\n".join(rows)
