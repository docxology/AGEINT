from __future__ import annotations

from typing import Any

from ._06_part import expanded_profile_anchor_keys, practice_lens_for_titles, profile_for_titles
from ._07_safe_titles import _topic_anchor_words
from ._09_part import (
    _chapter_ref_context,
    _coursebook_profile_for_titles,
    _table_cell,
    _topic_context,
    citation_cluster,
)
from .topic_entries import safe_topic_entries


def chapter_textbook_primer(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render concrete coursebook primer prose for a generated chapter."""
    title = str(chapter["title"])
    part_title = str(part["title"])
    profile = profile_for_titles(part_title, title, chapter=chapter)
    lens = practice_lens_for_titles(part_title, title, chapter=chapter)
    coursebook = _coursebook_profile_for_titles(part_title, title)
    entries = safe_topic_entries(chapter, part)
    topics = [entry.display_title for entry in entries[:3]]
    topic_sentence = f"**{'; '.join(topics)}**" if topics else "the local topic cluster"
    first_topic = f"**{topics[0]}**" if topics else "the local topic cluster"
    anchors = citation_cluster(expanded_profile_anchor_keys(profile), limit=3)
    source_context = _chapter_ref_context(chapter)
    topic_context = _topic_context(chapter, part)
    return "\n\n".join(
        [
            (
                f"This chapter teaches {coursebook.disciplinary_frame}. "
                f"The chapter uses **{lens.title}** to connect definitions, "
                f"evidence tests, practice artifacts, and review gates for {topic_context}."
            ),
            (
                f"The central distinction is to {coursebook.key_distinction}. "
                f"Core topics include {topic_sentence}. Each topic covers meaning, "
                "evidentiary support, common misconceptions, and safety boundaries."
            ),
            (
                f"Governance requirements use verified official, standards, "
                f"public-domain, or scholarly anchors such as {anchors} "
                "Technical, theoretical, or empirical statements require direct "
                "domain sources and are limited to what those sources establish. "
                f"{source_context}"
            ),
            (
                f"Learners move from vocabulary and the **{lens.title}** "
                f"distinction through topic lessons on {first_topic} with "
                "evidence and misconception checks, then "
                f"assemble {_indefinite_article(lens.evidence_artifact)} "
                f"**{lens.evidence_artifact}** with safety and rights gates."
            ),
        ]
    )


def _indefinite_article(phrase: str) -> str:
    first = phrase.strip()[:1].lower()
    return "an" if first in {"a", "e", "i", "o", "u"} else "a"


def chapter_learning_outcomes(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render chapter-specific learning outcomes."""
    title = str(chapter["title"])
    part_title = str(part["title"])
    profile = profile_for_titles(part_title, title, chapter=chapter)
    lens = practice_lens_for_titles(part_title, title, chapter=chapter)
    coursebook = _coursebook_profile_for_titles(part_title, title)
    topics = [entry.display_title for entry in safe_topic_entries(chapter, part)[:2]]
    topic_clause = " and ".join(topics) if len(topics) == 2 else topics[0]
    return "\n".join(
        [
            (
                f"- Connect **{topic_clause}** to **{profile.title}** by naming "
                "shared vocabulary, evidence burden, and audience-facing caveats."
            ),
            (
                f"- Build {_indefinite_article(lens.evidence_artifact)} "
                f"**{lens.evidence_artifact}** that keeps observation, "
                "inference, uncertainty, source quality, reviewer decision, and "
                "refresh trigger separate."
            ),
            (
                f"- Apply the key distinction: {coursebook.key_distinction}; "
                "show where an apparently useful shortcut would cross that line."
            ),
            (
                f"- Diagnose failure modes such as {profile.failure_modes}, then "
                "write one recovery move for each failure mode that preserves the "
                "learning objective."
            ),
            f"- Teach the defensive boundary back to a peer: {profile.safety_boundary}.",
        ]
    )


def chapter_key_terms(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render a profile-aware vocabulary table for a generated chapter."""
    title = str(chapter["title"])
    part_title = str(part["title"])
    coursebook = _coursebook_profile_for_titles(part_title, title)
    rows = ["| Term | Working definition |", "|---|---|"]
    for term, definition in coursebook.vocabulary:
        rows.append(f"| {_table_cell(term)} | {_table_cell(definition)} |")
    topic_terms = safe_topic_entries(chapter, part)
    seen_topic_defs: set[str] = set()
    for entry in topic_terms:
        label = entry.display_title
        if len(label) > 48:
            label = label[:48].rsplit(" ", 1)[0] + "…"
        if label and any(label.lower() in row.lower() for row in rows):
            continue
        anchor = _topic_anchor_words(entry.display_title, limit=3)
        definition = f"Key terms: {anchor}."
        if definition in seen_topic_defs:
            continue
        seen_topic_defs.add(definition)
        rows.append(f"| {_table_cell(label)} | {_table_cell(definition)} |")
        if len(seen_topic_defs) >= 2:
            break
    return "\n".join(rows)
