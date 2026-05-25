from __future__ import annotations

def _import_prior_parts(*module_names: str) -> None:
    import importlib

    for module_name in module_names:
        mod = importlib.import_module(f".{module_name}", __package__)
        globals().update({k: v for k, v in vars(mod).items() if not k.startswith("__")})


_import_prior_parts(
    "_01_part",
    "_02_part",
    "_03_part",
    "_04_part",
    "_04b_part",
    "_05_part",
    "_06_part",
    "_07_part",
    "_08_part",
    "_09_part",
    "_12_topic_frames",
)


def _topic_concept_frame(
    entry: TopicEntry,
    coursebook: CoursebookProfile,
    profile: IntelligenceProfile,
) -> str:
    return concept_frame_for_entry(entry, coursebook, profile)


def _topic_evidence_prompt(
    entry: TopicEntry,
    lens: PracticeLens,
    coursebook: CoursebookProfile,
) -> str:
    return evidence_prompt_for_entry(entry, lens, coursebook)


def _topic_student_artifact(
    entry: TopicEntry,
    lens: PracticeLens,
    coursebook: CoursebookProfile,
) -> str:
    return artifact_prompt_for_entry(entry, lens, coursebook)


def _topic_transfer_task(
    entry: TopicEntry,
    coursebook: CoursebookProfile,
    *,
    lesson_index: int = 1,
    chapter_title: str = "",
) -> str:
    raw = entry.raw_title.lower()
    if "active inference" in raw or "free energy" in raw or "predictive" in raw:
        return (
            "Transfer the idea to a non-AI chapter by naming the assumed model, the "
            "surprising observation, and the review point before any decision follows."
        )
    if entry.risk_category not in {"standard", "ageint_pattern_registry"}:
        templates = (
            (
                f"Transfer **{entry.display_title}** from this module to a "
                f"second motif by preserving {coursebook.practice_focus}, replacing "
                "action with audit, and naming the blocked use."
            ),
            (
                f"Apply this module's safe boundary for **{entry.display_title}** "
                f"to another artifact while keeping {coursebook.practice_focus} and "
                "reviewer ownership explicit."
            ),
            (
                f"Reuse the **{entry.display_title}** audit pattern from this module "
                "on a different fictional record set with a new reviewer and blocked-use note."
            ),
        )
        return templates[(lesson_index - 1) % len(templates)]
    return (
        f"Transfer **{entry.display_title}** to a second module by preserving "
        f"{coursebook.practice_focus}, changing the source evidence, and naming a new reviewer."
    )


def _topic_misconception(
    entry: TopicEntry,
    coursebook: CoursebookProfile,
    *,
    lesson_index: int = 1,
    chapter_title: str = "",
) -> str:
    return misconception_for_entry(
        entry,
        coursebook,
        lesson_index=lesson_index,
        chapter_title=chapter_title,
    )


def chapter_textbook_primer(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render concrete coursebook primer prose for a generated chapter."""
    title = str(chapter["title"])
    part_title = str(part["title"])
    profile = profile_for_titles(part_title, title, chapter=chapter)
    lens = practice_lens_for_titles(part_title, title, chapter=chapter)
    coursebook = _coursebook_profile_for_titles(part_title, title)
    entries = _safe_topic_entries(chapter, part)
    topics = [entry.display_title for entry in entries[:3]]
    topic_sentence = "; ".join(topics)
    anchors = citation_cluster(profile.anchor_keys, limit=3)
    source_context = _chapter_ref_context(chapter)
    topic_context = _topic_context(chapter, part)
    return "\n\n".join(
        [
            (
                f"This module teaches {coursebook.disciplinary_frame}. "
                f"The chapter uses **{lens.title}** to connect definitions, "
                f"evidence tests, practice artifacts, and review gates for {topic_context}."
            ),
            (
                f"The central distinction is to {coursebook.key_distinction}. "
                f"Core topics include {topic_sentence}. Each topic covers meaning, "
                "evidentiary support, common misconceptions, and safety boundaries."
            ),
            (
                f"In this module, verified anchors such as {anchors} ground definitions, examples, "
                f"uncertainty language, and artifact requirements. Source context: {source_context}"
            ),
            (
                f"Learners working on this module move from vocabulary and the **{lens.title}** "
                f"distinction through topic lessons on {topics[0] if topics else title} with "
                "evidence and misconception checks, then "
                f"assemble a **{lens.evidence_artifact}** with safety and rights gates."
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
    topics = [entry.display_title for entry in _safe_topic_entries(chapter, part)[:2]]
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
    topic_terms = _safe_topic_entries(chapter, part)
    seen_topic_defs: set[str] = set()
    for entry in topic_terms:
        label = entry.display_title[:48]
        if label and any(label.lower() in row.lower() for row in rows):
            continue
        anchor = _topic_anchor_words(entry.display_title, limit=3)
        definition = f"Topic focus: {anchor}."
        if definition in seen_topic_defs:
            continue
        seen_topic_defs.add(definition)
        rows.append(f"| {_table_cell(label)} | {_table_cell(definition)} |")
        if len(seen_topic_defs) >= 2:
            break
    return "\n".join(rows)


def _reader_facing_concept(entry: TopicEntry, frame: str) -> str:
    """Anchor reusable concept frames to the concrete source topic."""
    text = frame.strip()
    if f"**{entry.display_title}**" in text:
        return text

    replacements = {
        "Analyze ": "analyzes ",
        "Applies ": "applies ",
        "Connect ": "connects ",
        "Define ": "defines ",
        "Distinguish ": "distinguishes ",
        "Evaluate ": "evaluates ",
        "Explain how ": "shows how ",
        "Focus on ": "focuses on ",
        "Frame ": "frames ",
        "Map ": "maps ",
        "Read ": "reads ",
        "Shows ": "shows ",
        "Study ": "studies ",
        "Translate ": "translates ",
        "Treat ": "treats ",
        "Use ": "uses ",
    }
    for prefix, replacement in replacements.items():
        if text.startswith(prefix):
            text = replacement + text[len(prefix) :]
            break
    return f"**{entry.display_title}** {text}"


def _lower_first_word(text: str) -> str:
    stripped = text.strip()
    return stripped[:1].lower() + stripped[1:] if stripped else stripped


def _for_topic(entry: TopicEntry, text: str) -> str:
    """Prefix repeated lesson prose with the concrete source topic."""
    if entry.display_title in text or f"**{entry.display_title}**" in text:
        return text
    return f"For **{entry.display_title}**, {_lower_first_word(text)}"
