"""Generated chapter fragment quality gates (all six module sections)."""

from __future__ import annotations

import json
import re
from pathlib import Path

from manuscript_quality.inventory_helpers import (
    REQUIRED_MODULE_SECTIONS,
    chapter_text,
    generated_chapter_files,
    manuscript_dir,
    section_text,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"

COLLAPSED_COGSEC_BASE = "Cognitive-security resilience lesson using sample materials and transparent labels"
GOVERNANCE_BOUNDED_GENERIC = (
    "Governance-bounded intelligence topic review using instructor-provided sample records"
)
DIRECT_ANCHOR_RE = re.compile(r"\[@(?:official|scholarly)_")

MIN_SECTION_CHARS = {
    "Textbook primer": 120,
    "Learning outcomes": 80,
    "Core vocabulary": 40,
    "Topic lessons": 200,
    "Worked safe example": 80,
    "Module architecture and transfer contract": 60,
    "Evidence canon and source spine": 40,
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
        overview_path = path.parent / "00-overview.md"
        if not overview_path.exists():
            continue
        overview = chapter_text(overview_path)
        primer = section_text(overview, "Textbook primer")
        if COLLAPSED_COGSEC_BASE in primer:
            failures.append(f"{_chapter_slug(path)}: collapsed_cogsec_in_primer")
        if primer.count(GOVERNANCE_BOUNDED_GENERIC) > 1:
            failures.append(f"{_chapter_slug(path)}: generic_titles_in_primer")
        topic_section = section_text(chapter_text(path), "Topic lessons")
        headers = re.findall(r"^#{3,4} Lesson \d+: (.+)$", topic_section, flags=re.MULTILINE)
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
        practice_path = path.parent / "01-practice-studio.md"
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
        arch_path = path.parent / "02-evidence-contract.md"
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


def test_topic_lessons_include_educational_cross_links(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    failures: list[str] = []
    for path in generated_chapter_files(output_manuscript):
        section = section_text(chapter_text(path), "Topic lessons")
        if "**Cross-links.**" not in section:
            failures.append(f"{_chapter_slug(path)}: missing lesson cross-links")
        if "[@fig:part-" not in section:
            failures.append(f"{_chapter_slug(path)}: missing unit module map figure ref")
        if "[@sec:curriculum_orientation]" not in section:
            failures.append(f"{_chapter_slug(path)}: missing curriculum atlas section ref")
    assert failures == []


def test_topic_lessons_include_source_support_lines(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    failures: list[str] = []
    for path in generated_chapter_files(output_manuscript):
        section = section_text(chapter_text(path), "Topic lessons")
        lesson_count = len(re.findall(r"^#{3,4} Lesson \d+:", section, flags=re.MULTILINE))
        source_support_count = section.count("**Source support.**")
        if lesson_count != source_support_count:
            failures.append(f"{_chapter_slug(path)}: {source_support_count}/{lesson_count}")
    assert failures == []


def test_claim_bearing_fragments_include_profile_triangulation_anchors(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    fragment_names = (
        "01-practice-studio",
        "02-evidence-contract",
        "03-governance-boundary",
        "04-assessment-route",
    )
    failures: list[str] = []
    for path in generated_chapter_files(output_manuscript):
        for fragment_name in fragment_names:
            fragment_paths = sorted(path.parent.glob(f"{fragment_name}*.md"))
            if not fragment_paths:
                failures.append(f"{_chapter_slug(path)}: missing {fragment_name}")
                continue
            text = "\n\n".join(fragment.read_text(encoding="utf-8") for fragment in fragment_paths)
            if "**Triangulation anchors.**" not in text:
                failures.append(f"{_chapter_slug(path)}: missing anchors in {fragment_name}")
            if not DIRECT_ANCHOR_RE.search(text):
                failures.append(f"{_chapter_slug(path)}: missing direct citation in {fragment_name}")
    assert failures == []
