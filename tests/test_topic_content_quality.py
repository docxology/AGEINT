"""Anti-fallback and topic-specific content quality gates."""

from __future__ import annotations

import re
from pathlib import Path

from manuscript_quality.inventory_helpers import (
    REMOVED_GENERIC_CONCEPT_PHRASES,
    chapter_text,
    generated_chapter_files,
    manuscript_dir,
    section_text,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

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
    "review",
    "case",
    "lesson",
}

COLLAPSED_COGSEC_BASE = "Cognitive-security resilience lesson using sample materials and transparent labels"
GOVERNANCE_BOUNDED_GENERIC = (
    "Governance-bounded intelligence topic review using instructor-provided sample records"
)
TEAMS_CONFUSE_MARKER = "teams confuse source material"


def _title_keywords(title: str) -> set[str]:
    words = {
        word
        for word in re.findall(r"[a-z0-9]+", title.lower())
        if len(word) >= 4 and word not in TITLE_KEYWORD_STOPWORDS
    }
    return words or set(re.findall(r"[a-z0-9]+", title.lower()))


def _topic_lesson_files(output_manuscript: Path) -> list[Path]:
    return sorted(output_manuscript.rglob("01-practice-studio*.md"))


def test_topic_lessons_contain_no_generic_concept_fallback(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    violations: list[str] = []
    for path in _topic_lesson_files(output_manuscript):
        text = path.read_text(encoding="utf-8")
        for phrase in REMOVED_GENERIC_CONCEPT_PHRASES:
            if phrase.lower() in text.lower():
                rel = path.relative_to(PROJECT_ROOT).as_posix()
                violations.append(f"{rel}: {phrase}")
    assert violations == []


def test_topic_lesson_concepts_anchor_title_keywords(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    chapter_failures: list[str] = []
    for path in generated_chapter_files(output_manuscript):
        section = section_text(chapter_text(path), "Topic lessons")
        lesson_titles = re.findall(r"^#{3,4} Lesson \d+: (.+)$", section, flags=re.MULTILINE)
        lesson_blocks = re.split(r"^#{3,4} Lesson \d+: .+$", section, flags=re.MULTILINE)[1:]
        if not lesson_titles:
            continue
        hits = 0
        for title, block in zip(lesson_titles, lesson_blocks, strict=True):
            concept = block.split("**Concept.**", 1)[1].split("\n", 1)[0]
            keywords = _title_keywords(title)
            haystack = set(re.findall(r"[a-z0-9]+", concept.lower()))
            if haystack & keywords:
                hits += 1
        ratio = hits / len(lesson_titles)
        if ratio < 0.8:
            chapter_failures.append(f"{path.parent.name}: {hits}/{len(lesson_titles)}")
    assert chapter_failures == []


TIER_C_CONCEPT_MARKERS = (
    ("applies the ", "discipline:"),
    ("in the ", "lane:"),
)

GENERIC_MISCONCEPTION_MARKER = "can be used while ignoring the rule to"


def _chapter_topic_lessons_section(path: Path) -> str:
    return section_text(chapter_text(path), "Topic lessons")


def test_tier_c_concept_repetition_capped_per_chapter(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    failures: list[str] = []
    for path in generated_chapter_files(output_manuscript):
        section = _chapter_topic_lessons_section(path)
        lesson_count = len(re.findall(r"^#{3,4} Lesson \d+:", section, flags=re.MULTILINE))
        if lesson_count == 0:
            continue
        tier_c_hits = 0
        for left, right in TIER_C_CONCEPT_MARKERS:
            tier_c_hits = max(
                tier_c_hits,
                sum(
                    1
                    for block in re.split(r"^#{3,4} Lesson \d+:", section, flags=re.MULTILINE)[1:]
                    if left in block.split("**Concept.**", 1)[-1].lower()
                    and right in block.split("**Concept.**", 1)[-1].lower()
                ),
            )
        if tier_c_hits / lesson_count > 0.15:
            failures.append(f"{path.parent.name}: tier_c={tier_c_hits}/{lesson_count}")
    assert failures == []


def test_generic_misconception_repetition_capped_per_chapter(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    failures: list[str] = []
    for path in generated_chapter_files(output_manuscript):
        section = _chapter_topic_lessons_section(path)
        lesson_count = len(re.findall(r"^#{3,4} Lesson \d+:", section, flags=re.MULTILINE))
        if lesson_count == 0:
            continue
        generic_hits = section.lower().count(GENERIC_MISCONCEPTION_MARKER)
        if generic_hits / lesson_count > 0.40:
            failures.append(f"{path.parent.name}: generic={generic_hits}/{lesson_count}")
    assert failures == []


def test_teams_confuse_boilerplate_capped_per_chapter(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    failures: list[str] = []
    for path in generated_chapter_files(output_manuscript):
        section = _chapter_topic_lessons_section(path)
        lesson_count = len(re.findall(r"^#{3,4} Lesson \d+:", section, flags=re.MULTILINE))
        if lesson_count == 0:
            continue
        hits = section.lower().count(TEAMS_CONFUSE_MARKER)
        if hits / lesson_count > 0.20:
            failures.append(f"{path.parent.name}: teams_confuse={hits}/{lesson_count}")
    assert failures == []


def test_collapsed_cogsec_titles_capped_per_chapter(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    failures: list[str] = []
    for path in generated_chapter_files(output_manuscript):
        section = _chapter_topic_lessons_section(path)
        hits = section.count(COLLAPSED_COGSEC_BASE)
        if hits > 1:
            failures.append(f"{path.parent.name}: collapsed_cogsec={hits}")
    assert failures == []


def test_governance_bounded_titles_absent_from_lesson_headers(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    failures: list[str] = []
    for path in generated_chapter_files(output_manuscript):
        section = _chapter_topic_lessons_section(path)
        headers = re.findall(r"^#{3,4} Lesson \d+: (.+)$", section, flags=re.MULTILINE)
        hits = sum(1 for header in headers if GOVERNANCE_BOUNDED_GENERIC in header)
        if hits > 0:
            failures.append(f"{path.parent.name}: governance_bounded_headers={hits}")
    assert failures == []


def test_category_concept_repetition_capped_per_chapter(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    failures: list[str] = []
    for path in generated_chapter_files(output_manuscript):
        section = _chapter_topic_lessons_section(path)
        concepts = [
            block.split("**Concept.**", 1)[1].split("\n", 1)[0].strip()
            for block in re.split(r"^#{3,4} Lesson \d+:", section, flags=re.MULTILINE)[1:]
            if "**Concept.**" in block
        ]
        if not concepts:
            continue
        from collections import Counter

        counts = Counter(concepts)
        max_repeat = max(counts.values())
        if max_repeat / len(concepts) > 0.25:
            failures.append(f"{path.parent.name}: concept_repeat={max_repeat}/{len(concepts)}")
    assert failures == []


SPOT_CHECK_CHAPTER_SLUGS = (
    "the-nature-of-intelligence",
    "agent-recruitment",
    "sigint-fundamentals",
    "osint-foundations",
    "cyber-intelligence-fundamentals",
    "imagery-intelligence-imint",
    "psyop-and-miso-doctrine",
    "counterintelligence-fundamentals",
    "gray-zone-warfare",
    "american-intelligence-history",
    "foundations-of-ageint",
    "cognitive-security-foundations-and-definitions",
    "structured-analytic-techniques-sats",
    "the-intelligent-operator-as-cognitive-athlete",
    "industrial-control-systems-ics-and-operational-technology",
    "ethics-of-intelligence-and-cognitive-security",
)

SPOT_CHECK_REQUIRED_PHRASES = {
    "the-nature-of-intelligence": ("intelligence", "requirement"),
    "agent-recruitment": ("MICE", "recruitment"),
    "sigint-fundamentals": ("SIGINT", "minimization"),
    "osint-foundations": ("open source", "provenance"),
    "cyber-intelligence-fundamentals": ("cyber", "taxonomy"),
    "imagery-intelligence-imint": ("imagery", "geospatial"),
    "psyop-and-miso-doctrine": ("influence", "audience"),
    "counterintelligence-fundamentals": ("vetting", "source"),
    "gray-zone-warfare": ("hybrid", "attribution"),
    "american-intelligence-history": ("oversight", "declassified"),
    "foundations-of-ageint": ("AGEINT", "agent"),
    "cognitive-security-foundations-and-definitions": ("cognitive security", "provenance"),
    "structured-analytic-techniques-sats": (
        "Analysis of Competing Hypotheses",
        "ICD 203",
    ),
    "the-intelligent-operator-as-cognitive-athlete": (
        "Getting Things Done",
        "NASA-TLX",
    ),
    "industrial-control-systems-ics-and-operational-technology": ("ICS", "safety"),
    "ethics-of-intelligence-and-cognitive-security": ("rights", "oversight"),
}


def test_spot_check_chapters_use_domain_titles_not_generic_fallback(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    failures: list[str] = []
    generic = GOVERNANCE_BOUNDED_GENERIC
    for slug in SPOT_CHECK_CHAPTER_SLUGS:
        matches = sorted(output_manuscript.rglob(f"*/{slug}/01-practice-studio*.md"))
        assert matches, f"missing topic lessons for {slug}"
        text = "\n".join(path.read_text(encoding="utf-8") for path in matches)
        if text.count(generic) > 2:
            failures.append(f"{slug}: generic_title={text.count(generic)}")
        if text.count(COLLAPSED_COGSEC_BASE) > 1:
            failures.append(f"{slug}: collapsed_cogsec={text.count(COLLAPSED_COGSEC_BASE)}")
        for phrase in SPOT_CHECK_REQUIRED_PHRASES[slug]:
            if phrase.lower() not in text.lower():
                failures.append(f"{slug}: missing {phrase!r}")
    assert failures == []
