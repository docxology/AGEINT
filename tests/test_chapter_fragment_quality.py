"""Generated chapter fragment quality gates (all six module sections)."""

from __future__ import annotations

import json
import re
from pathlib import Path

from _inventory_helpers import (
    REQUIRED_MODULE_SECTIONS,
    chapter_text,
    generated_chapter_files,
    manuscript_dir,
    section_text,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"

COLLAPSED_COGSEC_BASE = (
    "Cognitive-security resilience lesson using fictional materials and transparent labels"
)
GOVERNANCE_BOUNDED_GENERIC = (
    "Governance-bounded intelligence topic review using instructor-provided fictional records"
)

MIN_SECTION_CHARS = {
    "Textbook primer": 120,
    "Learning outcomes": 80,
    "Core vocabulary": 40,
    "Topic lessons": 200,
    "Worked safe example": 80,
    "Module architecture": 60,
    "Evidence and source canon": 40,
    "Assessment artifacts and capstone pathway": 40,
}


def _chapter_slug(path: Path) -> str:
    return path.parent.name


def _chapter_json_profile(slug: str) -> tuple[str, str]:
    matches = list(DATA.rglob(f"*/{slug}/chapter.json"))
    if not matches:
        return "", ""
    payload = json.loads(matches[0].read_text(encoding="utf-8"))
    return str(payload.get("content_profile", "")), str(payload.get("practice_lens", ""))


def test_overview_primer_references_distinct_topic_titles(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    failures: list[str] = []
    for path in generated_chapter_files(output_manuscript):
        overview_path = path.parent / path.name.replace("01-topic-lessons", "00-overview")
        if not overview_path.exists():
            continue
        overview = chapter_text(overview_path)
        primer = section_text(overview, "Textbook primer")
        if COLLAPSED_COGSEC_BASE in primer:
            failures.append(f"{_chapter_slug(path)}: collapsed_cogsec_in_primer")
        if primer.count(GOVERNANCE_BOUNDED_GENERIC) > 1:
            failures.append(f"{_chapter_slug(path)}: generic_titles_in_primer")
        topic_section = section_text(chapter_text(path), "Topic lessons")
        headers = re.findall(r"^### Lesson \d+: (.+)$", topic_section, flags=re.MULTILINE)
        distinct_headers = {header for header in headers[:3]}
        if len(headers) >= 3 and len(distinct_headers) < 2:
            failures.append(f"{_chapter_slug(path)}: primer_topic_collapse")
    assert failures == []


def test_worked_practice_names_chapter_profile(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    failures: list[str] = []
    for path in generated_chapter_files(output_manuscript):
        slug = _chapter_slug(path)
        profile_id, lens_id = _chapter_json_profile(slug)
        if not profile_id:
            continue
        practice_path = path.parent / path.name.replace("01-topic-lessons", "02-worked-practice")
        if not practice_path.exists():
            continue
        text = chapter_text(practice_path).lower()
        profile_token = profile_id.replace("_", " ")
        if profile_token not in text and profile_id not in text:
            if lens_id.replace("_", " ") not in text:
                failures.append(f"{slug}: missing profile/lens reference in worked practice")
    assert failures == []


def test_architecture_sources_avoids_collapsed_title_echoes(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    failures: list[str] = []
    for path in generated_chapter_files(output_manuscript):
        arch_path = path.parent / path.name.replace("01-topic-lessons", "03-architecture-sources")
        if not arch_path.exists():
            continue
        text = chapter_text(arch_path)
        cogsec_hits = text.count(COLLAPSED_COGSEC_BASE)
        if cogsec_hits > 2:
            failures.append(f"{_chapter_slug(path)}: architecture_cogsec_echo={cogsec_hits}")
        generic_hits = text.count(GOVERNANCE_BOUNDED_GENERIC)
        if generic_hits > 2:
            failures.append(f"{_chapter_slug(path)}: architecture_generic_echo={generic_hits}")
    assert failures == []


def test_required_module_sections_present_with_minimum_length(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    failures: list[str] = []
    for path in generated_chapter_files(output_manuscript):
        text = chapter_text(path)
        slug = _chapter_slug(path)
        for section in REQUIRED_MODULE_SECTIONS:
            if section not in text:
                failures.append(f"{slug}: missing section {section!r}")
                continue
            body = section_text(text, section)
            minimum = MIN_SECTION_CHARS.get(section, 20)
            if len(body.strip()) < minimum and section in MIN_SECTION_CHARS:
                failures.append(f"{slug}: short section {section!r} ({len(body.strip())} chars)")
    assert failures == []
