from __future__ import annotations

from typing import Any

try:  # Support package and script-level imports.
    from citation_workflow import source_citation_spine
    from markdown_refs import lesson_educational_crossrefs
    from unit_education import unit_profile_for_part
except ImportError:  # pragma: no cover - exercised by package imports
    from ..citation_workflow import source_citation_spine  # type: ignore[no-redef]
    from ..markdown_refs import lesson_educational_crossrefs  # type: ignore[no-redef]
    from ..unit_education import unit_profile_for_part  # type: ignore[no-redef]

from ._04b_part import INTELLIGENCE_PROFILES
from ._01_part import TopicEntry
from ._topic_anaphora import AnchorState, anaphorize_field as _anaphorize_field, keeps_title_keywords as _keeps_title_keywords, misconception_line as _misconception_line
from ._06_part import expanded_profile_anchor_keys, practice_lens_for_titles, profile_for_titles
from ._09_part import _chapter_ref_context, _coursebook_profile_for_titles, _table_cell, _topic_context, citation_cluster, profile_triangulation_anchors
from ._12_topic_frames import lesson_intro_paragraph
from .source_grounding import SourceRecord, annotated_source_table, cited_sources, evidence_from_sources, source_support_sentence, sources_for_numbers
from .tradecraft_source_support import curated_tradecraft_evidence, primary_topic_sources, tradecraft_context_support
from .topic_entries import safe_topic_entries
from .topic_formalisms import lesson_formalism_field
from .topic_lesson_voice import compact_topic
from .topic_lessons import resolve_topic_lesson_fields, resolve_topic_misconception


def chapter_topic_lessons(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render source-guide topics as concrete, safe coursebook lessons."""
    title = str(chapter["title"])
    part_title = str(part["title"])
    profile = profile_for_titles(part_title, title, chapter=chapter)
    lens = practice_lens_for_titles(part_title, title, chapter=chapter)
    coursebook = _coursebook_profile_for_titles(part_title, title)
    unit_profile = unit_profile_for_part(part)
    entries = safe_topic_entries(chapter, part)
    distinct_openers = tuple(dict.fromkeys(entry.display_title for entry in entries[:3]))
    lessons = [
        lesson_intro_paragraph(title, coursebook, lens, distinct_openers),
        lesson_educational_crossrefs(part, chapter),
        profile_triangulation_anchors(part_title, title, chapter=chapter, surface="topic-lessons section"),
    ]
    for index, entry in enumerate(entries, 1):
        fields = resolve_topic_lesson_fields(entry, coursebook=coursebook, profile=profile, lens=lens, lesson_index=index, chapter_title=title, unit_profile=unit_profile)
        sources = cited_sources(entry, limit=3)
        support_sources = primary_topic_sources(entry.risk_category, sources)
        evidence = (
            evidence_from_sources(entry.display_title, support_sources)
            if support_sources
            else curated_tradecraft_evidence(entry.display_title)
            if entry.risk_category == "analytic_tradecraft" and sources
            else fields.evidence_prompt
        )
        # ``forbidden`` blocks short forms that collide with a chapter/part title,
        # which the downstream section-title sanitiser would collapse to "the
        # module" and strip of every keyword the anchor gate needs.
        forbidden = {title.casefold(), part_title.casefold()}
        body_fields = [
            f"**Why it matters.** {fields.why_it_matters}",
            (
                f"**Source support.** {_topic_source_support(entry, chapter, support_sources, original_sources=sources)} "
                f"External triangulation uses {citation_cluster(expanded_profile_anchor_keys(profile), limit=2)}"
            ),
            f"**Evidence to inspect.** {evidence}",
            f"**Student artifact.** {fields.artifact_prompt}",
            f"**Misconception check.** {_misconception_line(entry.display_title, fields.misconception, forbidden=forbidden)}",
            f"**Transfer task.** {fields.transfer_task}",
        ]
        # The header and Concept keep the full bold title (Concept anchors the
        # title-keyword check). Every later field uses a short or anaphoric
        # reference so a single lesson never restates the bold title ~9 times.
        anchor = AnchorState()
        body_fields = [field if field.startswith("**Source support.**") else _anaphorize_field(entry.display_title, field, anchor=anchor, forbidden=forbidden) for field in body_fields]
        formalism = lesson_formalism_field(entry.display_title)
        if formalism:
            body_fields.append(formalism)
        lessons.extend([f"#### Lesson {index}: {entry.display_title}", f"**Concept.** {fields.concept}", *body_fields])
    return "\n\n".join(lessons)


def chapter_source_annotations(chapter: dict[str, Any], limit: int = 30) -> str:
    """Render a module's real annotated source list from its cited works."""
    records = sources_for_numbers(chapter.get("citations", []), limit=limit)
    if not records:
        return "This module carries no direct source-guide citations; it inherits the surrounding part bibliography, and the gap stays visible in the claim ledger."
    table = annotated_source_table(records)
    total = len(set(int(number) for number in chapter.get("citations", [])))
    if total > len(records):
        remaining = total - len(records)
        table = f"{table}\n\nThe remaining {remaining} cited source(s) appear in the bibliography appendix with the same verification metadata."
    return table


def _topic_source_support(entry: TopicEntry, chapter: dict[str, Any], sources: tuple[SourceRecord, ...] = (), *, original_sources: tuple[SourceRecord, ...] = ()) -> str:
    """Render direct topic citations or an honest module-spine fallback."""

    if sources:
        return source_support_sentence(entry.display_title, sources)
    if entry.risk_category == "analytic_tradecraft" and original_sources:
        return tradecraft_context_support(entry.display_title, source_citation_spine(entry.citation_numbers))
    if entry.citation_numbers:
        return f"Source-guide row {entry.source_locus} cites {source_citation_spine(entry.citation_numbers)} Use it for the topic definition, scope boundary, and refresh check before transfer."
    if chapter.get("citations"):
        return f"This row has no direct citation; the module source spine is {source_citation_spine(chapter['citations'])} It supplies context, and the gap remains visible in the claim ledger."
    return source_citation_spine([])


def chapter_worked_example(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render a synthetic worked example for a generated chapter."""
    title = str(chapter["title"])
    part_title = str(part["title"])
    lens = practice_lens_for_titles(part_title, title, chapter=chapter)
    coursebook = _coursebook_profile_for_titles(part_title, title)
    unit_profile = unit_profile_for_part(part)
    entries = safe_topic_entries(chapter, part)
    anchor_topic = entries[0].display_title if entries else title
    source_context = _chapter_ref_context(chapter)
    # The Frame field carries the full title once (keyword anchor); every later
    # field uses the keyword-preserving compact form so the 200-char title is not
    # restated bolded eight times per chapter.
    short_anchor = compact_topic(anchor_topic)
    if not _keeps_title_keywords(short_anchor, anchor_topic):
        short_anchor = anchor_topic
    return "\n\n".join(
        [
            f"Worked example: {coursebook.worked_scenario}. {source_context}",
            profile_triangulation_anchors(part_title, title, chapter=chapter, surface="worked-example section"),
            (f"**Unit discipline spine.** Discipline: **{unit_profile.concept}**. Learners use a **{unit_profile.practice_artifact}** and keep this boundary visible: {unit_profile.safety_boundary}"),
            (f"**Frame.** The classroom question centers on **{anchor_topic}**. Excluded actions stay explicit, and the **{lens.title}** planning question is: {lens.planning_question}"),
            (
                f"**Inputs.** For the **{short_anchor}** scenario, use {coursebook.worked_input}. "
                f"The {lens.title} intake note records provenance, sensitivity, "
                "fit-to-purpose, and why the fixture is enough for this bounded exercise."
            ),
            (
                f"**Analysis.** For **{short_anchor}**, students "
                f"{coursebook.worked_process}. Pause whenever an inference about "
                f"{short_anchor} appears without evidence, confidence outruns support, "
                "or an agent output is treated as judgment."
            ),
            (
                f"**Filled artifact.** Purpose = **{short_anchor}** classroom scenario; "
                f"unit artifact = {unit_profile.practice_artifact}; "
                f"evidence = allowed inputs; method = {coursebook.practice_focus}; "
                f"output = {coursebook.worked_output}; boundary = no external action; "
                "reviewer = instructor or named peer."
            ),
            (
                f"**Flawed answer to revise.** Treating **{short_anchor}** as "
                f'"{lens.title} confirms it" is not enough. The revision ties the claim to '
                f"{coursebook.practice_focus}, adds the missing caveat, states confidence, "
                "and records the reviewer who accepted the bounded judgment."
            ),
            (
                f"**Debrief.** The reuse note for **{short_anchor}** records the "
                "defensible claim, the assumption most likely to fail, the evidence "
                "that would change confidence, and the review condition for stopping reuse."
            ),
        ]
    )


def chapter_practice_sequence(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render a bounded practice sequence for a generated chapter."""
    title = str(chapter["title"])
    part_title = str(part["title"])
    profile = profile_for_titles(part_title, title, chapter=chapter)
    lens = practice_lens_for_titles(part_title, title, chapter=chapter)
    coursebook = _coursebook_profile_for_titles(part_title, title)
    unit_profile = unit_profile_for_part(part)
    entries = safe_topic_entries(chapter, part)[:3]
    first_topics = ", ".join(compact_topic(entry.display_title) for entry in entries)
    first_entry_topic = compact_topic(entries[0].display_title)
    if not _keeps_title_keywords(first_entry_topic, entries[0].display_title):
        first_entry_topic = entries[0].display_title
    misconception = resolve_topic_misconception(entries[0], coursebook=coursebook, profile=profile, lens=lens, lesson_index=1, chapter_title=title, unit_profile=unit_profile)
    topic_context = _topic_context(chapter, part)
    source_context = _chapter_ref_context(chapter)
    practice_rows = "\n".join(
        [
            "| Move | Learner action | Output | Check |",
            "|---|---|---|---|",
            f"| 1. Distinguish | Compare {first_topics}; name what each topic can and cannot prove. | Glossary-and-contrast card. | Terms match the **{_table_cell(profile.title)}** lane. |",
            f"| 2. Frame | Answer the lens question: {lens.planning_question} | Scope card. | Authority, excluded actions, data boundary, and reviewer are explicit. |",
            f"| 3. Evidence | Fill the artifact fields for {first_entry_topic}: {lens.evidence_artifact}. | Evidence packet. | Sources, caveats, confidence, and uncertainty stay separable. |",
            f"| 3a. Unit artifact | Add the {unit_profile.practice_artifact} fields for {first_entry_topic}. | Unit profile note. | Evidence artifacts include {', '.join(unit_profile.evidence_artifacts[:2])}. |",
            f"| 4. Challenge | Test the misconception {misconception}. | Failure-mode note. | The artifact applies the key distinction: {coursebook.key_distinction}. |",
            "| 5. Handoff | Prepare the artifact for another reviewer. | Handoff memo. | Inputs, transformations, reviewer, refresh trigger, and residual risk are visible. |",
        ]
    )
    return "\n\n".join(
        [
            (f"The studio sequence uses the **{lens.title}** practice lens. Moves 1-3 form the compressed path; the full seminar path adds challenge, handoff, and a review memo for {topic_context}."),
            profile_triangulation_anchors(part_title, title, chapter=chapter, surface="practice-sequence section"),
            practice_rows,
            f"#### {title} instructor notes: source reasoning, review points, and studio focus",
            (
                "Ask learners to verbalize the difference between "
                "a source, an inference, and a decision. Require a revision whenever "
                f"a claim cannot be traced to a source descriptor or a human review point. Keep the focus on {topic_context}. {source_context}"
            ),
            f"#### {title} extension exercise: peer validation and refresh trigger review",
            (
                f"Have learners swap artifacts and apply the **{lens.title}** "
                "validation rule to someone else's work. The receiving learner "
                "must identify one strength, one missing caveat, and one refresh "
                f"trigger for {topic_context}."
            ),
        ]
    )


def chapter_knowledge_check(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render chapter-specific knowledge-check prompts."""
    title = str(chapter["title"])
    part_title = str(part["title"])
    profile = profile_for_titles(part_title, title, chapter=chapter)
    lens = practice_lens_for_titles(part_title, title, chapter=chapter)
    coursebook = _coursebook_profile_for_titles(part_title, title)
    entries = safe_topic_entries(chapter, part)
    topic = entries[0]
    second_topic = entries[1] if len(entries) > 1 else entries[0]
    # Q1 carries the full title once (keyword anchor); later mentions use the
    # keyword-preserving compact form to avoid restating the 200-char title.
    short_topic = compact_topic(topic.display_title)
    if not _keeps_title_keywords(short_topic, topic.display_title):
        short_topic = topic.display_title
    short_second = compact_topic(second_topic.display_title)
    if not _keeps_title_keywords(short_second, second_topic.display_title):
        short_second = second_topic.display_title
    return "\n".join(
        [
            f"1. Explain how **{topic.display_title}** is defined here; name the source descriptor that supports the definition.",
            f"2. Contrast **{short_topic}** with **{short_second}** using the **{lens.title}** artifact fields.",
            f"3. Identify one failure mode from the **{profile.title}** lane and the evidence that would reveal it.",
            f"4. Answer the coursebook review question: {coursebook.review_question}",
            f"5. Correct this misconception: {resolve_topic_misconception(topic, coursebook=coursebook, profile=profile, lens=lens, lesson_index=1, chapter_title=title)}.",
            "",
            f"#### {title} answer quality rubric: source evidence, uncertainty, and safe transfer",
            "",
            "Judge answers with the canonical mastery evidence "
            "standard in the shared method-and-assurance reference "
            "([@sec:method-assurance-reference]): a strong answer uses source "
            "evidence, distinguishes observation from judgment, names uncertainty, "
            "and states the safe boundary, while a revise-level answer gives a "
            f"memorized definition of **{short_topic}** without source "
            "evidence, uncertainty, or a safe transfer task.",
        ]
    )


def subsection_practice_rows(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render subsection-level practice lenses from runtime source-guide sections."""
    entries = safe_topic_entries(chapter, part)
    if not chapter.get("sections"):
        lens = practice_lens_for_titles(str(part["title"]), str(chapter["title"]), chapter=chapter)
        return f"| Lesson topic | Practice lens | Evidence artifact | Safety check |\n|---|---|---|---|\n| {entries[0].display_title} | {lens.title} | {lens.evidence_artifact} | {lens.safety_check} |"

    rows = ["| Lesson topic | Practice lens | Evidence artifact | Safety check |", "|---|---|---|---|"]
    for entry in entries:
        lens = practice_lens_for_titles(str(part["title"]), entry.display_title)
        rows.append(f"| {entry.display_title} | {lens.title} | {lens.evidence_artifact} | {lens.safety_check} |")
    return "\n".join(rows)


def profile_inventory_rows() -> str:
    """Render the available intelligence profile taxonomy."""
    rows = ["| Profile | Anchor count | Core contract |", "|---|---:|---|"]
    for profile in INTELLIGENCE_PROFILES:
        rows.append(f"| {profile.title} | {len(expanded_profile_anchor_keys(profile))} | {profile.composability_contract} |")
    return "\n".join(rows)
