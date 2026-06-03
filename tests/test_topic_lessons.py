"""Tests for topic lesson rotation and unified field resolution."""

from __future__ import annotations

import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_ROOT / "src"))

from curriculum import load_curriculum  # noqa: E402
from intelligence_content._11_part import _coursebook_profile_for_titles  # noqa: E402
from intelligence_content.topic_lessons import (  # noqa: E402
    resolve_topic_lesson_fields,
    resolve_topic_misconception,
    template_index,
    transfer_task_for_entry,
)
from intelligence_content import practice_lens_for_titles, profile_for_titles  # noqa: E402
from intelligence_content._11_part import AnchorState, _anaphorize_field  # noqa: E402
from intelligence_content.topic_entries import safe_topic_entries  # noqa: E402
from intelligence_content.topic_lesson_voice import short_title  # noqa: E402

DATA = PROJECT_ROOT / "data" / "curriculum"


def test_template_index_is_stable_for_same_inputs() -> None:
    assert template_index("alpha", "beta", count=5) == template_index("alpha", "beta", count=5)


def test_template_index_varies_with_different_parts() -> None:
    slots = {template_index(f"part-{index}", count=7) for index in range(12)}
    assert len(slots) > 1


def test_transfer_task_for_entry_risk_branch_differs_from_standard() -> None:
    curriculum = load_curriculum(DATA)
    risk_entry = None
    standard_entry = None
    for part in curriculum.parts:
        part_title = str(part["title"])
        for chapter in part["chapters"]:
            coursebook = _coursebook_profile_for_titles(part_title, str(chapter["title"]))
            for entry in safe_topic_entries(chapter, part):
                if entry.risk_category not in {"standard", "ageint_pattern_registry"} and risk_entry is None:
                    risk_entry = (entry, coursebook)
                if entry.risk_category == "standard" and standard_entry is None:
                    standard_entry = (entry, coursebook)
            if risk_entry and standard_entry:
                break
        if risk_entry and standard_entry:
            break
    assert risk_entry is not None
    assert standard_entry is not None
    risk_text = transfer_task_for_entry(
        risk_entry[0],
        risk_entry[1],
        lesson_index=1,
        chapter_title="Test Module",
    )
    standard_text = transfer_task_for_entry(
        standard_entry[0],
        standard_entry[1],
        lesson_index=1,
        chapter_title="Test Module",
    )
    assert "audit" in risk_text.lower() or "blocked" in risk_text.lower()
    assert "second module" in standard_text.lower()


def test_resolve_topic_lesson_fields_smoke_on_curriculum_entry() -> None:
    curriculum = load_curriculum(DATA)
    for part in curriculum.parts:
        part_title = str(part["title"])
        for chapter in part["chapters"]:
            chapter_title = str(chapter["title"])
            profile = profile_for_titles(part_title, chapter_title, chapter=chapter)
            lens = practice_lens_for_titles(part_title, chapter_title, chapter=chapter)
            coursebook = _coursebook_profile_for_titles(part_title, chapter_title)
            entries = safe_topic_entries(chapter, part)
            if not entries:
                continue
            fields = resolve_topic_lesson_fields(
                entries[0],
                coursebook=coursebook,
                profile=profile,
                lens=lens,
                lesson_index=1,
                chapter_title=chapter_title,
            )
            assert fields.concept.strip()
            assert fields.why_it_matters.strip()
            assert fields.evidence_prompt.strip()
            assert fields.artifact_prompt.strip()
            assert fields.misconception.strip()
            assert fields.transfer_task.strip()
            return
    raise AssertionError("curriculum produced no topic entries")


def test_resolve_topic_misconception_matches_lesson_fields() -> None:
    curriculum = load_curriculum(DATA)
    for part in curriculum.parts:
        part_title = str(part["title"])
        for chapter in part["chapters"]:
            chapter_title = str(chapter["title"])
            profile = profile_for_titles(part_title, chapter_title, chapter=chapter)
            lens = practice_lens_for_titles(part_title, chapter_title, chapter=chapter)
            coursebook = _coursebook_profile_for_titles(part_title, chapter_title)
            entries = safe_topic_entries(chapter, part)
            if not entries:
                continue
            entry = entries[0]
            fields = resolve_topic_lesson_fields(
                entry,
                coursebook=coursebook,
                profile=profile,
                lens=lens,
                lesson_index=1,
                chapter_title=chapter_title,
            )
            direct = resolve_topic_misconception(
                entry,
                coursebook=coursebook,
                profile=profile,
                lens=lens,
                lesson_index=1,
                chapter_title=chapter_title,
            )
            assert direct == fields.misconception
            return
    raise AssertionError("curriculum produced no topic entries")


def test_short_title_uses_pre_colon_head() -> None:
    assert (
        short_title("Defining Intelligence: Collection, Analysis, Production, Dissemination")
        == "Defining Intelligence"
    )


def test_short_title_cuts_colon_free_qualifier() -> None:
    assert (
        short_title("AI-Enhanced Micro-Expression Analysis for Source Validation")
        == "AI-Enhanced Micro-Expression Analysis"
    )


def test_short_title_keeps_already_compact_title() -> None:
    assert short_title("Social Engineering") == "Social Engineering"


def test_short_title_rejects_stranded_list_fragment() -> None:
    # Cutting at " and " would strand "APT Definitions, Lifecycle," — keep full.
    assert (
        short_title("APT Definitions, Lifecycle, and Attribution")
        == "APT Definitions, Lifecycle, and Attribution"
    )


def test_anaphorize_field_keeps_first_mention_collapses_rest() -> None:
    title = "Defining Intelligence: Collection, Analysis, Production, Dissemination"
    token = f"**{title}**"
    field = f"For {token}, build the artifact. Shape {token} work as a ledger."
    out = _anaphorize_field(title, field, anchor=AnchorState())
    # First mention becomes the bolded short form; the second collapses to anaphora.
    assert "**Defining Intelligence**" in out
    assert out.count(token) == 0
    assert "this subject" in out or "this topic" in out


def test_anaphorize_field_respects_forbidden_short_form() -> None:
    title = "Social Engineering: The Science of Human Hacking"
    token = f"**{title}**"
    field = f"Without explicit treatment of {token}, the failure mode dominates."
    # "Social Engineering" collides with a chapter title; keep full title to retain
    # keywords the section-title sanitiser would otherwise strip.
    out = _anaphorize_field(
        title, field, anchor=AnchorState(), forbidden={"social engineering"}
    )
    assert token in out
