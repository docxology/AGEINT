"""Reader-facing quality gates for generated AGEINT manuscript prose."""

from __future__ import annotations

from pathlib import Path
import re

from manuscript_quality.inventory_helpers import (
    chapter_text,
    generated_chapter_files,
    generated_output_files,
    manuscript_dir,
    section_text,
)

LESSON_FIELD_LABELS = (
    "Concept",
    "Why it matters",
    "Evidence to inspect",
    "Student artifact",
    "Misconception check",
    "Transfer task",
)
RENDERED_FORMULA_PHRASES = (
    "The tool found the answer, so the claim is ready",
    "what the example proves, what it does not prove",
    "Each input gets a source descriptor, provenance note, sensitivity class",
    "source descriptor, claim, caveat, uncertainty, blocked-use statement, and named reviewer",
    "A strong answer names what the concept enables, what it cannot prove, and which reviewer should challenge it",
    "anchors the section's source flow, safety gate, or practice artifact",
    "This section documents verified sources",
    "This section turns **",
    "This section records when **",
    "The goal is to make governance",
    "The chapter keeps the local",
    "The answer should identify",
    "inspect fictional records that show how",
    "fictional",
    "Use this module studio plan",
    "After this module, the class writes",
    "cite the evidence field that would support the definition",
    "review review",
    "lens lens",
    "Lens** lens",
    "A short class can complete moves",
    "what learners should do",
    "Start with the unit's guiding question",
    "Each input gets a",
    ", submit a completed **",
    ", submit a blocked-request control card",
    "completed artifact is a",
    "placeholder",
    "boilerplate",
    # Retired fixed-tail boilerplate (deterministic rotations replaced these);
    # each substring is unique to the old stamped form, so it can never silently
    # return. See source_grounding/_source_prose, topic_prompt_routes, and the
    # why_it_matters rotation slot 0.
    "extract the bounded claim it supports",
    "for the topic definition, scope boundary, and refresh check before transfer",
    "source descriptor, bounded claim, caveat, uncertainty note, blocked-use statement",
    "enabled judgment, proof limit, and reviewer responsible for challenge",
    "Use these links to read this module in sequence",
)
PDF_UNSUPPORTED_SOURCE_GLYPHS = ("🛰", "⃣")
TITLE_KEYWORD_STOPWORDS = {
    "about",
    "after",
    "against",
    "agent",
    "agentic",
    "analysis",
    "and",
    "from",
    "into",
    "module",
    "source",
    "that",
    "the",
    "their",
    "through",
    "using",
    "with",
}


def _reader_paragraphs(text: str) -> list[str]:
    paragraphs: list[str] = []
    current: list[str] = []
    in_fence = False
    for line in text.splitlines():
        stripped = line.strip()
        if stripped.startswith("```"):
            in_fence = not in_fence
            continue
        if in_fence:
            continue
        if not stripped:
            if current:
                paragraphs.append(" ".join(current))
                current = []
            continue
        current.append(stripped)
    if current:
        paragraphs.append(" ".join(current))

    prose: list[str] = []
    for paragraph in paragraphs:
        if paragraph.startswith("#"):
            continue
        if paragraph.startswith("![") or paragraph.startswith("{#"):
            continue
        if "|" in paragraph:
            continue
        if "{{" in paragraph or "}}" in paragraph:
            continue
        if len(re.findall(r"[A-Za-z0-9]+", paragraph)) < 18:
            continue
        prose.append(re.sub(r"\s+", " ", paragraph).strip())
    return prose


def _title_keywords(title: str) -> set[str]:
    words = {
        word
        for word in re.findall(r"[a-z0-9]+", title.lower())
        if len(word) >= 4 and word not in TITLE_KEYWORD_STOPWORDS
    }
    return words or set(re.findall(r"[a-z0-9]+", title.lower()))


def _anchors_lesson_title(text: str, title: str) -> bool:
    if title in text:
        return True
    haystack = set(re.findall(r"[a-z0-9]+", text.lower()))
    keywords = _title_keywords(title)
    return len(haystack & keywords) >= min(2, len(keywords))


def _anchors_lesson_title_or_sanitized_module(text: str, title: str) -> bool:
    if _anchors_lesson_title(text, title):
        return True
    if "the module" not in text and "this module" not in text:
        return False
    haystack = set(re.findall(r"[a-z0-9]+", text.lower()))
    return bool(haystack & _title_keywords(title))


def test_generated_reader_prose_does_not_repeat_template_paragraphs(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    paragraph_locations: dict[str, list[str]] = {}
    for path in generated_output_files(output_manuscript):
        rel = path.relative_to(output_manuscript).as_posix()
        for paragraph in _reader_paragraphs(path.read_text(encoding="utf-8")):
            paragraph_locations.setdefault(paragraph, []).append(rel)

    repeated = {
        paragraph: locations
        for paragraph, locations in paragraph_locations.items()
        if len(set(locations)) > 6
    }

    assert repeated == {}


def test_topic_lessons_are_topic_specific_not_template_repeated(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    for path in generated_chapter_files(output_manuscript):
        section = section_text(chapter_text(path), "Topic lessons")
        lesson_titles = re.findall(r"^#{3,4} Lesson \d+: (.+)$", section, flags=re.MULTILINE)
        assert lesson_titles, path
        assert len(lesson_titles) == len(set(lesson_titles)), path
        for title in lesson_titles:
            assert len(title.split()) >= 2, f"{path}: {title}"
        lesson_blocks = re.split(r"^#{3,4} Lesson \d+: .+$", section, flags=re.MULTILINE)[1:]
        for title, block in zip(lesson_titles, lesson_blocks, strict=True):
            for field in LESSON_FIELD_LABELS:
                marker = f"**{field}.**"
                assert marker in block
                field_text = block.split(marker, 1)[1].split("\n", 1)[0]
                assert _anchors_lesson_title_or_sanitized_module(field_text, title), (
                    f"{path}: {title}: {field}"
                )
            concept = block.split("**Concept.**", 1)[1].split("\n", 1)[0]
            bold_anchors = " ".join(re.findall(r"\*\*(.+?)\*\*", concept))
            assert bold_anchors, f"{path}: {title}"
            assert _anchors_lesson_title_or_sanitized_module(bold_anchors, title), f"{path}: {title}"
            assert not re.search(r"Use [A-Z][A-Za-z]+, [A-Z][A-Za-z]+,", concept), path


def test_generated_manuscript_avoids_known_rendered_formulas(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    failures: list[str] = []
    for phrase in RENDERED_FORMULA_PHRASES:
        hits: list[str] = []
        for path in generated_output_files(output_manuscript):
            count = path.read_text(encoding="utf-8").count(phrase)
            if count:
                rel = path.relative_to(output_manuscript).as_posix()
                hits.append(f"{rel} ({count})")
        if hits:
            failures.append(f"{phrase!r}: {', '.join(hits[:6])}")

    assert failures == []


def test_generated_manuscript_avoids_pdf_unsupported_source_glyphs(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    failures: list[str] = []
    for path in generated_output_files(output_manuscript):
        text = path.read_text(encoding="utf-8")
        for glyph in PDF_UNSUPPORTED_SOURCE_GLYPHS:
            if glyph in text:
                rel = path.relative_to(output_manuscript).as_posix()
                failures.append(f"{rel}: {glyph!r}")

    assert failures == []


def test_orientation_gives_reader_use_paths(built_output: Path) -> None:
    orientation_dir = manuscript_dir(built_output) / "orientation"
    text = "\n\n".join(
        path.read_text(encoding="utf-8") for path in sorted(orientation_dir.glob("*.md"))
    )

    assert "## How to use this atlas" in text
    assert "## Reader paths" in text
    assert "Instructor" in text
    assert "Learner" in text
    assert "Assurance reviewer" in text
    assert "## Consolidated glossary and index" in text
    assert "Source lane" in text
    assert "## Capstone model-answer exemplars" in text
    assert "Safe-lab packet" in text


# Max times any single source-support CLOSING sentence or artifact-verification
# sentence may render verbatim across all topic-lesson files. The closing
# sentence is title-woven (near-unique; repeats only when the SAME title recurs,
# capped by the most-repeated title at ~6) and the artifact sentence is anchored
# on topic words. The current measured live max is 20 (the pattern-registry
# artifact sentence, whose anchor collapses to a short shared fragment for that
# category). The cap is set just above that real recurrence so a partial-stamp
# regression past today's level trips, rather than only a catastrophic revert:
# dropping the {title} weave would spike the closing sentence back to ~70, and a
# full boilerplate revert to 500+. (Tightened from 40 → 24 after the 2026-06-09
# RedTeam audit flagged the old cap as ~2x the live max and blind to the
# realistic regression it exists to prevent.)
_MAX_GROUNDING_SENTENCE_REPEAT = 24

# The two de-boilerplated grounding sentence families. The closing source-support
# sentence always terminates its physical line, so it is captured to end-of-line
# (robust to title-internal periods like "(11.5)" or "vs."). The artifact-
# verification sentence is followed by more prose on the same line, so it is
# bounded by its terminal period; its woven anchor words contain no periods.
_SOURCE_SUPPORT_CLOSING_RE = re.compile(r"Use (?:them|it) for .+$", re.MULTILINE)
_ARTIFACT_VERIFICATION_RE = re.compile(r"The artifact must [^.]+\.")


def _topic_lesson_files(output_manuscript: Path) -> list[Path]:
    return sorted(output_manuscript.rglob("01-practice-studio*.md"))


def test_grounding_closing_and_artifact_sentences_are_not_stamped(built_output: Path) -> None:
    """Cap verbatim repetition of the source-support closing and artifact sentences.

    Both are topic-woven now (title for the closing sentence, anchor words for the
    artifact sentence), so neither should recur as one identical stamp. Navigation
    prose, markdown table cells, and arbitrary repeated source NOTES are excluded:
    we count ONLY these two grounding sentence families, and only in topic-lesson
    files (the sole place they render), skipping any line bearing a table pipe.
    """
    from collections import Counter

    output_manuscript = manuscript_dir(built_output)
    counts: Counter[str] = Counter()
    for path in _topic_lesson_files(output_manuscript):
        for line in path.read_text(encoding="utf-8").splitlines():
            if "|" in line:  # skip markdown table rows
                continue
            for match in _SOURCE_SUPPORT_CLOSING_RE.findall(line):
                counts[f"closing::{match.strip()}"] += 1
            for match in _ARTIFACT_VERIFICATION_RE.findall(line):
                counts[f"artifact::{match.strip()}"] += 1

    assert counts, "expected grounding sentences in generated topic lessons"
    over = {
        sentence: total
        for sentence, total in counts.items()
        if total > _MAX_GROUNDING_SENTENCE_REPEAT
    }
    assert over == {}, (
        "grounding sentence repeated verbatim past the de-boilerplating cap: "
        + "; ".join(f"{total}x {sentence[:90]!r}" for sentence, total in sorted(
            over.items(), key=lambda kv: kv[1], reverse=True
        )[:5])
    )
