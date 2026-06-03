from __future__ import annotations

import re
from dataclasses import dataclass
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
from ._06_part import practice_lens_for_titles, profile_for_titles
from ._09_part import (
    _chapter_ref_context,
    _coursebook_profile_for_titles,
    _table_cell,
    _topic_context,
)
from ._12_topic_frames import lesson_intro_paragraph
from .source_grounding import (
    SourceRecord,
    annotated_source_table,
    cited_sources,
    evidence_from_sources,
    source_support_sentence,
    sources_for_numbers,
)
from .topic_entries import safe_topic_entries
from .topic_formalisms import lesson_formalism_field
from .topic_lesson_voice import compact_topic, short_title, topic_reference
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
    ]
    for index, entry in enumerate(entries, 1):
        fields = resolve_topic_lesson_fields(
            entry,
            coursebook=coursebook,
            profile=profile,
            lens=lens,
            lesson_index=index,
            chapter_title=title,
            unit_profile=unit_profile,
        )
        sources = cited_sources(entry, limit=3)
        evidence = (
            evidence_from_sources(entry.display_title, sources)
            if sources
            else fields.evidence_prompt
        )
        # ``forbidden`` blocks short forms that collide with a chapter/part title,
        # which the downstream section-title sanitiser would collapse to "the
        # module" and strip of every keyword the anchor gate needs.
        forbidden = {title.casefold(), part_title.casefold()}
        body_fields = [
            f"**Why it matters.** {fields.why_it_matters}",
            f"**Source support.** {_topic_source_support(entry, chapter, sources)}",
            f"**Evidence to inspect.** {evidence}",
            f"**Student artifact.** {fields.artifact_prompt}",
            f"**Misconception check.** {_misconception_line(entry.display_title, fields.misconception, forbidden=forbidden)}",
            f"**Transfer task.** {fields.transfer_task}",
        ]
        # The header and Concept keep the full bold title (Concept anchors the
        # title-keyword check). Every later field uses a short or anaphoric
        # reference so a single lesson never restates the bold title ~9 times.
        anchor = AnchorState()
        body_fields = [
            _anaphorize_field(entry.display_title, field, anchor=anchor, forbidden=forbidden)
            for field in body_fields
        ]
        formalism = lesson_formalism_field(entry.display_title)
        if formalism:
            body_fields.append(formalism)
        lessons.extend(
            [
                f"### Lesson {index}: {entry.display_title}",
                f"**Concept.** {fields.concept}",
                *body_fields,
            ]
        )
    return "\n\n".join(lessons)


@dataclass
class AnchorState:
    """Tracks how many title references a lesson body has already emitted."""

    slot: int = 0


# Articles and possessives that may already precede a title token; when present
# we emit a bare noun so we never produce "the this topic".
_LEADING_DETERMINERS = ("the", "a", "an", "this", "that", "its", "their", "each")

# Bare nouns used after a determiner (e.g. "the topic artifact"). These carry no
# title keyword, so they are only used on the SECOND+ occurrence within a single
# field, after that field already anchored the title keywords via short form.
_BARE_NOUNS = ("topic", "lesson topic", "subject")

# Standalone anaphora used after a determiner is absent and the field already
# carries title keywords from an earlier short-form mention.
_STANDALONE = ("this topic", "the same topic", "this subject")


def _anaphorize_field(
    display_title: str,
    field: str,
    *,
    anchor: AnchorState,
    forbidden: frozenset[str] | set[str] = frozenset(),
) -> str:
    """Replace repeated bold full titles in one body field with shorter references.

    The first title occurrence WITHIN a field becomes the bolded short form so
    the field keeps the lesson's title keywords (required by the reader-quality
    anchor gate) while shedding the long colon tail. Any further occurrences in
    the same field — the source of the field-to-field "stutter" — collapse to a
    grammar-aware anaphor. This runs after frame resolution so it covers every
    title-injection site uniformly, and it stops the generator restating the
    full bold title ~9 times per lesson.
    """
    token = f"**{display_title}**"
    if token not in field:
        return field
    parts = field.split(token)
    rebuilt = parts[0]
    compact = short_title(display_title)
    # The anchor gate requires each field to keep the lesson's title keywords. If
    # the short form drops them, or collides with a chapter/part title that the
    # section-title sanitiser would collapse to "the module", fall back to the
    # full title for the field's first mention so the field still anchors.
    if not _keeps_title_keywords(compact, display_title) or compact.casefold() in forbidden:
        compact = display_title
    field_has_anchor = False
    for tail in parts[1:]:
        if not field_has_anchor:
            # First mention in this field: keep title keywords via short form.
            field_has_anchor = True
            anchor.slot += 1
            rebuilt += f"**{compact}**" + tail
            continue
        rebuilt += _anaphor(rebuilt, anchor) + tail
    return rebuilt


_TITLE_KEYWORD_STOPWORDS = {
    "about", "after", "against", "agent", "agentic", "analysis", "and",
    "from", "into", "module", "source", "that", "the", "their", "through",
    "using", "with",
}


def _title_keywords(title: str) -> set[str]:
    """Title keywords used by the reader-quality anchor gate (mirrors the test)."""
    words = {
        word
        for word in re.findall(r"[a-z0-9]+", title.lower())
        if len(word) >= 4 and word not in _TITLE_KEYWORD_STOPWORDS
    }
    return words or set(re.findall(r"[a-z0-9]+", title.lower()))


def _keeps_title_keywords(candidate: str, title: str) -> bool:
    """True when ``candidate`` retains enough title keywords to anchor a field."""
    keywords = _title_keywords(title)
    haystack = set(re.findall(r"[a-z0-9]+", candidate.lower()))
    return len(haystack & keywords) >= min(2, len(keywords))


def _misconception_line(
    display_title: str,
    misconception: str,
    *,
    forbidden: frozenset[str] | set[str] = frozenset(),
) -> str:
    """Render the misconception sentence, anchoring the topic only once.

    Risk-category templates already name the topic; keyword-routed and fallback
    templates do not, so a short-form prefix supplies the title keywords the
    field-anchor gate needs without producing the old double-title stutter.
    """
    text = misconception.strip().rstrip(".")
    inner_anchored = (
        f"**{display_title}**" in text
        or display_title in text
        or _keeps_title_keywords(text, display_title)
    )
    if inner_anchored:
        return f"Correct the misconception {text}."
    compact = short_title(display_title)
    if not _keeps_title_keywords(compact, display_title) or compact.casefold() in forbidden:
        compact = display_title
    return f"Correct the misconception about **{compact}**: {text}."


def _anaphor(before: str, anchor: AnchorState) -> str:
    """Choose a grammatical anaphor for a repeated title within one field."""
    anchor.slot += 1
    trimmed = before.rstrip()
    last_word = trimmed.rsplit(" ", 1)[-1].lower() if trimmed else ""
    if last_word in _LEADING_DETERMINERS:
        return _BARE_NOUNS[anchor.slot % len(_BARE_NOUNS)]
    reference = _STANDALONE[anchor.slot % len(_STANDALONE)]
    at_sentence_start = (not trimmed) or trimmed[-1] in ".!?:*"
    if at_sentence_start:
        return reference[0].upper() + reference[1:]
    return reference


def chapter_source_annotations(chapter: dict[str, Any], limit: int = 30) -> str:
    """Render a module's real annotated source list from its cited works."""
    records = sources_for_numbers(chapter.get("citations", []), limit=limit)
    if not records:
        return (
            "This module carries no direct source-guide citations; it inherits the "
            "surrounding part bibliography, and the gap stays visible in the claim ledger."
        )
    table = annotated_source_table(records)
    total = len(set(int(number) for number in chapter.get("citations", [])))
    if total > len(records):
        remaining = total - len(records)
        table = (
            f"{table}\n\nThe remaining {remaining} cited source(s) "
            "appear in the bibliography appendix with the same verification metadata."
        )
    return table


def _topic_source_support(
    entry: TopicEntry,
    chapter: dict[str, Any],
    sources: tuple[SourceRecord, ...] = (),
) -> str:
    """Render direct topic citations or an honest module-spine fallback."""

    if sources:
        return source_support_sentence(entry.display_title, sources)
    if entry.citation_numbers:
        return (
            f"Source-guide row {entry.source_locus} cites "
            f"{source_citation_spine(entry.citation_numbers)} Use it for the topic definition, "
            "scope boundary, and refresh check before transfer."
        )
    if chapter.get("citations"):
        return (
            "This row has no direct citation; the module source spine is "
            f"{source_citation_spine(chapter['citations'])} It supplies context, and the "
            "gap remains visible in the claim ledger."
        )
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
            (
                f"**Unit discipline spine.** Discipline: **{unit_profile.concept}**. "
                f"Learners use a **{unit_profile.practice_artifact}** and keep this boundary visible: "
                f"{unit_profile.safety_boundary}"
            ),
            (
                f"**Frame.** The classroom question centers on **{anchor_topic}**. "
                f"Excluded actions stay explicit, and the **{lens.title}** planning "
                f"question is: {lens.planning_question}"
            ),
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
                f"\"{lens.title} confirms it\" is not enough. The revision ties the claim to "
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
    misconception = resolve_topic_misconception(
        entries[0],
        coursebook=coursebook,
        profile=profile,
        lens=lens,
        lesson_index=1,
        chapter_title=title,
        unit_profile=unit_profile,
    )
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
            (
                f"The studio sequence uses the **{lens.title}** "
                "practice lens. Moves 1-3 form the compressed path; the full seminar "
                f"path adds challenge, handoff, and a review memo for {topic_context}."
            ),
            practice_rows,
            "### Instructor notes",
            (
                "Ask learners to verbalize the difference between "
                "a source, an inference, and a decision. Require a revision whenever "
                f"a claim cannot be traced to a source descriptor or a human review point. Keep the focus on {topic_context}. {source_context}"
            ),
            "### Extension",
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
            "### Answer quality rubric",
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
        return (
            "| Lesson topic | Practice lens | Evidence artifact | Safety check |\n"
            "|---|---|---|---|\n"
            f"| {entries[0].display_title} | {lens.title} | {lens.evidence_artifact} | "
            f"{lens.safety_check} |"
        )

    rows = [
        "| Lesson topic | Practice lens | Evidence artifact | Safety check |",
        "|---|---|---|---|",
    ]
    for entry in entries:
        lens = practice_lens_for_titles(str(part["title"]), entry.display_title)
        rows.append(
            f"| {entry.display_title} | {lens.title} | {lens.evidence_artifact} | "
            f"{lens.safety_check} |"
        )
    return "\n".join(rows)


def profile_inventory_rows() -> str:
    """Render the available intelligence profile taxonomy."""
    rows = [
        "| Profile | Anchor count | Core contract |",
        "|---|---:|---|",
    ]
    for profile in INTELLIGENCE_PROFILES:
        rows.append(
            f"| {profile.title} | {len(profile.anchor_keys)} | "
            f"{profile.composability_contract} |"
        )
    return "\n".join(rows)
