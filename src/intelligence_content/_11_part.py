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
    "_10_part",
    "_12_topic_frames",
)


def chapter_topic_lessons(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render source-guide topics as concrete, safe coursebook lessons."""
    title = str(chapter["title"])
    part_title = str(part["title"])
    profile = profile_for_titles(part_title, title, chapter=chapter)
    lens = practice_lens_for_titles(part_title, title, chapter=chapter)
    coursebook = _coursebook_profile_for_titles(part_title, title)
    entries = _safe_topic_entries(chapter, part)
    distinct_openers = tuple(dict.fromkeys(entry.display_title for entry in entries[:3]))
    lessons = [lesson_intro_paragraph(title, coursebook, lens, distinct_openers)]
    for index, entry in enumerate(entries, 1):
        concept = _reader_facing_concept(
            entry,
            _topic_concept_frame(entry, coursebook, profile),
        )
        evidence_prompt = _for_topic(entry, _topic_evidence_prompt(entry, lens, coursebook))
        artifact_prompt = _for_topic(entry, _topic_student_artifact(entry, lens, coursebook))
        transfer_task = _for_topic(
            entry,
            _topic_transfer_task(entry, coursebook, lesson_index=index, chapter_title=title),
        )
        lessons.extend(
            [
                f"### Lesson {index}: {entry.display_title}",
                f"**Concept.** {concept}",
                (
                    f"**Why it matters.** "
                    f"{why_it_matters_for_entry(entry, profile, coursebook, lesson_index=index)}"
                ),
                f"**Evidence to inspect.** {evidence_prompt}",
                f"**Student artifact.** {artifact_prompt}",
                (
                    f"**Misconception check.** Correct the misconception "
                    f"for **{entry.display_title}**: "
                    f"{_topic_misconception(entry, coursebook, lesson_index=index, chapter_title=title)}."
                ),
                f"**Transfer task.** {transfer_task}",
            ]
        )
    return "\n\n".join(lessons)


def chapter_worked_example(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Render a synthetic worked example for a generated chapter."""
    title = str(chapter["title"])
    part_title = str(part["title"])
    lens = practice_lens_for_titles(part_title, title, chapter=chapter)
    coursebook = _coursebook_profile_for_titles(part_title, title)
    entries = _safe_topic_entries(chapter, part)
    anchor_topic = entries[0].display_title if entries else title
    source_context = _chapter_ref_context(chapter)
    return "\n\n".join(
        [
            f"Worked example for this module: {coursebook.worked_scenario}. The source path begins with {source_context}",
            (
                f"**Frame.** The classroom question centers on **{anchor_topic}**. "
                f"Excluded actions stay explicit, and the **{lens.title}** planning "
                f"question is: {lens.planning_question}"
            ),
            (
                f"**Inputs.** For this module's **{anchor_topic}** scenario, use {coursebook.worked_input}. Each input gets a "
                f"documented intake note for the {lens.title}: provenance, sensitivity, "
                "fit-to-purpose, and the reason the fixture is enough for this bounded exercise."
            ),
            (
                f"**Analysis.** For **{anchor_topic}** in this module, students "
                f"{coursebook.worked_process}. Pause whenever an inference about "
                f"{anchor_topic} appears without evidence, confidence outruns support, "
                "or an agent output is treated as judgment."
            ),
            (
                f"**Filled artifact.** Purpose = **{anchor_topic}** classroom scenario; "
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
                f"**Debrief.** After this module, the class writes a three-line reuse note: "
                f"the defensible claim about **{anchor_topic}**, the assumption most likely "
                "to fail, and the review condition that would stop reuse."
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
    entries = _safe_topic_entries(chapter, part)[:3]
    first_topics = ", ".join(entry.display_title for entry in entries)
    misconception = _topic_misconception(entries[0], coursebook)
    topic_context = _topic_context(chapter, part)
    source_context = _chapter_ref_context(chapter)
    practice_rows = "\n".join(
        [
            "| Move | Learner action | Output | Check |",
            "|---|---|---|---|",
            f"| 1. Distinguish | Compare {first_topics}; name what each topic can and cannot prove. | Glossary-and-contrast card. | Terms match the **{_table_cell(profile.title)}** lane. |",
            f"| 2. Frame | Answer the lens question: {lens.planning_question} | Scope card. | Authority, excluded actions, data boundary, and reviewer are explicit. |",
            f"| 3. Evidence | Fill the artifact fields for {entries[0].display_title}: {lens.evidence_artifact}. | Evidence packet. | Sources, caveats, confidence, and uncertainty stay separable. |",
            f"| 4. Challenge | Test the misconception {misconception}. | Failure-mode note. | The artifact applies the key distinction: {coursebook.key_distinction}. |",
            "| 5. Handoff | Prepare the artifact for another reviewer. | Handoff memo. | Inputs, transformations, reviewer, refresh trigger, and residual risk are visible. |",
        ]
    )
    return "\n\n".join(
        [
            (
                f"Use this module studio plan with the **{lens.title}** "
                "lens. A short class can complete moves 1-3; a full seminar "
                f"should complete all moves and submit the handoff memo for {topic_context}."
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
    entries = _safe_topic_entries(chapter, part)
    topic = entries[0]
    second_topic = entries[1] if len(entries) > 1 else entries[0]
    return "\n".join(
        [
            f"1. Define **{topic.display_title}** and cite the evidence field that would support the definition.",
            f"2. Contrast **{topic.display_title}** with **{second_topic.display_title}** using the **{lens.title}** artifact fields.",
            f"3. Identify one failure mode from the **{profile.title}** lane and the evidence that would reveal it.",
            f"4. Answer the coursebook review question: {coursebook.review_question}",
            f"5. Correct this misconception: {_topic_misconception(topic, coursebook)}.",
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
    entries = _safe_topic_entries(chapter, part)
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
