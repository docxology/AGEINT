from __future__ import annotations

try:  # Support package and script-level imports.
    from citation_workflow import source_citation_spine
    from markdown_refs import lesson_educational_crossrefs
    from unit_education import unit_profile_for_part
except ImportError:  # pragma: no cover - exercised by package imports
    from ..citation_workflow import source_citation_spine  # type: ignore[no-redef]
    from ..markdown_refs import lesson_educational_crossrefs  # type: ignore[no-redef]
    from ..unit_education import unit_profile_for_part  # type: ignore[no-redef]

try:
    from intelligence_content.topic_lessons import resolve_topic_lesson_fields, resolve_topic_misconception
except ImportError:  # pragma: no cover - merged part module import
    from .topic_lessons import resolve_topic_lesson_fields, resolve_topic_misconception  # type: ignore[no-redef]


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
        lessons.extend(
            [
                f"### Lesson {index}: {entry.display_title}",
                f"**Concept.** {fields.concept}",
                f"**Why it matters.** {fields.why_it_matters}",
                f"**Source support.** {_topic_source_support(entry, chapter)}",
                f"**Evidence to inspect.** {fields.evidence_prompt}",
                f"**Student artifact.** {fields.artifact_prompt}",
                (
                    f"**Misconception check.** Correct the misconception "
                    f"for **{entry.display_title}**: {fields.misconception}."
                ),
                f"**Transfer task.** {fields.transfer_task}",
            ]
        )
    return "\n\n".join(lessons)


def _topic_source_support(entry: TopicEntry, chapter: dict[str, Any]) -> str:
    """Render direct topic citations or an honest module-spine fallback."""

    if entry.citation_numbers:
        return (
            f"Source-guide row {entry.source_locus} cites "
            f"{source_citation_spine(entry.citation_numbers)} Use it for the topic definition, "
            "scope boundary, and refresh check before transfer."
        )
    if chapter.get("citations"):
        return (
            "This source-topic row has no direct citation; the module source spine is "
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
    return "\n\n".join(
        [
            f"Worked example for this module: {coursebook.worked_scenario}. The source path begins with {source_context}",
            (
                f"**Unit discipline spine.** This module belongs to **{unit_profile.concept}**. "
                f"Learners use a **{unit_profile.practice_artifact}** and keep this boundary visible: "
                f"{unit_profile.safety_boundary}"
            ),
            (
                f"**Frame.** The classroom question centers on **{anchor_topic}**. "
                f"Excluded actions stay explicit, and the **{lens.title}** planning "
                f"question is: {lens.planning_question}"
            ),
            (
                f"**Inputs.** For this module's **{anchor_topic}** scenario, use {coursebook.worked_input}. "
                f"The {lens.title} intake note records provenance, sensitivity, "
                "fit-to-purpose, and why the fixture is enough for this bounded exercise."
            ),
            (
                f"**Analysis.** For **{anchor_topic}** in this module, students "
                f"{coursebook.worked_process}. Pause whenever an inference about "
                f"{anchor_topic} appears without evidence, confidence outruns support, "
                "or an agent output is treated as judgment."
            ),
            (
                f"**Filled artifact.** Purpose = **{anchor_topic}** classroom scenario; "
                f"unit artifact = {unit_profile.practice_artifact}; "
                f"evidence = allowed inputs; method = {coursebook.practice_focus}; "
                f"output = {coursebook.worked_output}; boundary = no external action; "
                "reviewer = instructor or named peer."
            ),
            (
                f"**Flawed answer to revise.** In this module, treating **{anchor_topic}** as "
                f"\"{lens.title} confirms it\" is not enough. The revision ties the claim to "
                f"{coursebook.practice_focus}, adds the missing caveat, states confidence, "
                "and records the reviewer who accepted the bounded judgment."
            ),
            (
                f"**Debrief.** The reuse note for **{anchor_topic}** records the "
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
    first_topics = ", ".join(entry.display_title for entry in entries)
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
            f"| 3. Evidence | Fill the artifact fields for {entries[0].display_title}: {lens.evidence_artifact}. | Evidence packet. | Sources, caveats, confidence, and uncertainty stay separable. |",
            f"| 3a. Unit artifact | Add the {unit_profile.practice_artifact} fields for {entries[0].display_title}. | Unit profile note. | Evidence artifacts include {', '.join(unit_profile.evidence_artifacts[:2])}. |",
            f"| 4. Challenge | Test the misconception {misconception}. | Failure-mode note. | The artifact applies the key distinction: {coursebook.key_distinction}. |",
            "| 5. Handoff | Prepare the artifact for another reviewer. | Handoff memo. | Inputs, transformations, reviewer, refresh trigger, and residual risk are visible. |",
        ]
    )
    return "\n\n".join(
        [
            (
                f"The studio sequence for this module uses the **{lens.title}** "
                "practice lens. Moves 1-3 form the compressed path; the full seminar "
                f"path adds challenge, handoff, and a review memo for {topic_context}."
            ),
            practice_rows,
            "### Instructor notes",
            (
                f"For this module, ask learners to verbalize the difference between "
                "a source, an inference, and a decision. Require a revision whenever "
                f"a claim cannot be traced to a source descriptor or a human review point. Source context: {source_context}; topic focus: {topic_context}."
            ),
            "### Extension",
            (
                f"Have learners swap this module's artifacts and apply the **{lens.title}** "
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
    return "\n".join(
        [
            f"1. Explain how **{topic.display_title}** is defined in this module; name the source descriptor that supports the definition.",
            f"2. Contrast **{topic.display_title}** with **{second_topic.display_title}** using the **{lens.title}** artifact fields.",
            f"3. Identify one failure mode from the **{profile.title}** lane and the evidence that would reveal it.",
            f"4. Answer the coursebook review question: {coursebook.review_question}",
            f"5. Correct this misconception: {resolve_topic_misconception(topic, coursebook=coursebook, profile=profile, lens=lens, lesson_index=1, chapter_title=title)}.",
            "",
            "### Answer quality rubric",
            "",
            "| Level | Evidence in the answer |",
            "|---|---|",
            "| Strong | Uses source evidence, distinguishes observation from judgment, names uncertainty, and states the safe boundary. |",
            "| Adequate | Defines the concept and names a relevant artifact, but leaves one caveat or review owner vague. |",
            "| Revise | Gives a memorized definition without source evidence, uncertainty, or a safe transfer task. |",
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
