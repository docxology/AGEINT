"""Reader-facing quality checks for generated AGEINT chapter content."""

from __future__ import annotations

from pathlib import Path

from manuscript_quality.inventory_helpers import (
    DIRECT_STUDENT_TASK_MOTIFS,
    GENERIC_DETAIL_SECTION_KEYS,
    GENERIC_TEACHING_SECTION_KEYS,
    REMOVED_FILLER_PHRASES,
    REMOVED_GENERATED_SCAFFOLD_PHRASES,
    REMOVED_META_PHRASES,
    RETIRED_GENERIC_HEADING_LABELS,
    PROJECT_ROOT,
    chapter_title_from_text,
    chapter_text,
    generated_chapter_files,
    generated_output_files,
    manuscript_dir,
    markdown_table_rows,
    required_module_sections_for,
    section_text,
)
from manuscript_manifest._heading_titles import chapter_detail_titles, chapter_teaching_titles


def test_generated_manuscript_has_no_scaffold_or_author_instruction_prose(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    violations: list[str] = []
    for path in generated_output_files(output_manuscript):
        text = path.read_text(encoding="utf-8")
        for phrase in REMOVED_GENERATED_SCAFFOLD_PHRASES:
            haystack = text.lower() if phrase.islower() else text
            needle = phrase.lower() if phrase.islower() else phrase
            if needle in haystack:
                rel = path.relative_to(PROJECT_ROOT).as_posix()
                violations.append(f"{rel}: {phrase}")

    assert violations == []


def test_generated_chapters_are_coursebook_not_meta_scaffold(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    for path in generated_chapter_files(output_manuscript):
        text = chapter_text(path)
        details = chapter_detail_titles(chapter_title_from_text(text))
        for phrase in REMOVED_META_PHRASES:
            assert phrase not in text, f"{path.name}: {phrase}"
        teaching_body = text.split(f"### {details['evidence']}", 1)[0]
        for phrase in REMOVED_FILLER_PHRASES:
            assert phrase not in teaching_body, f"{path.name}: {phrase}"
        teaching = chapter_teaching_titles(chapter_title_from_text(text))
        assert f"### {teaching['lessons']}" in text
        assert f"### {teaching['example']}" in text
        assert f"### {teaching['check']}" in text
        before_runtime_map = text.split(f"#### {details['runtime_map']}", 1)[0]
        assert f"### {teaching['lessons']}" in before_runtime_map
        assert f"### {teaching['sequence']}" in before_runtime_map
        assert "#### Lesson 1:" in before_runtime_map
        assert "**Misconception check.**" in before_runtime_map
        assert "**Filled artifact.**" in before_runtime_map
        assert (
            f"#### {chapter_title_from_text(text)} answer quality rubric: source evidence, uncertainty, and safe transfer"
            in before_runtime_map
        )
        assert before_runtime_map.count("|") < 220, path


def test_coursebook_sections_precede_runtime_maps_in_fixed_order(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    for path in generated_chapter_files(output_manuscript):
        text = chapter_text(path)
        title = chapter_title_from_text(text)
        teaching = chapter_teaching_titles(title)
        details = chapter_detail_titles(title)
        resolved_order = [
            f"### {teaching['primer']}",
            f"### {teaching['outcomes']}",
            f"### {teaching['vocabulary']}",
            f"### {teaching['lessons']}",
            f"### {teaching['example']}",
            f"### {teaching['sequence']}",
            f"### {teaching['check']}",
            f"### {details['architecture']}",
            f"### {details['evidence']}",
            f"#### {details['runtime_map']}",
            f"#### {details['subsection_contract']}",
        ]
        positions = [text.index(heading) for heading in resolved_order]
        assert positions == sorted(positions), path


def test_major_module_sections_have_reader_facing_introductions(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    for path in generated_chapter_files(output_manuscript):
        text = chapter_text(path)
        details = chapter_detail_titles(chapter_title_from_text(text))
        intro_sections = {
            details["evidence"],
            details["governance"],
            details["refresh"],
            details["links"],
        }
        for heading in intro_sections:
            section = section_text(text, heading)
            first_nonblank = next(
                (line.strip() for line in section.splitlines() if line.strip()), ""
            )
            assert first_nonblank
            assert not first_nonblank.startswith("### "), f"{path}: {heading}"
            intro = section.split("\n### ", 1)[0]
            assert len(intro.split()) >= 16, f"{path}: {heading}"


def test_generated_detail_headings_are_chapter_specific_not_generic(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    generic_headings = {
        "Module architecture and transfer contract",
        "Evidence canon and source spine",
        "Source-backed analytic synthesis",
        "Agentic translation: assist, approve, block",
        "Governance, rights, and assurance",
        "Assessment artifacts and capstone pathway",
        "Refresh, safety, and source maps",
        "Reviewer challenge checklist",
        "Learning-path cross-links",
        "Cross-links",
    } | set(GENERIC_TEACHING_SECTION_KEYS) | set(GENERIC_DETAIL_SECTION_KEYS) | RETIRED_GENERIC_HEADING_LABELS
    for path in generated_chapter_files(output_manuscript):
        text = chapter_text(path)
        title = chapter_title_from_text(text)
        assert required_module_sections_for(title)
        for heading in generic_headings:
            assert not any(
                line.lstrip("#").strip() == heading
                for line in text.splitlines()
                if line.startswith("###")
            ), f"{path}: {heading}"


def test_core_vocabulary_definitions_are_curated_not_source_heading_fillers(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    for path in generated_chapter_files(output_manuscript):
        rows = markdown_table_rows(section_text(chapter_text(path), "Core vocabulary"))
        assert len(rows) >= 5, path
        definitions = [row[1] for row in rows if len(row) >= 2]
        assert len(definitions) == len(set(definitions)), path
        for definition in definitions:
            assert "Source-guide topic" not in definition
            assert "classroom concept" not in definition


def test_unsafe_source_motifs_do_not_become_direct_student_tasks(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    for path in generated_chapter_files(output_manuscript):
        text = chapter_text(path)
        teaching_sections = "\n".join(
            [
                section_text(text, "Core vocabulary"),
                section_text(text, "Topic lessons"),
                section_text(text, "Practice sequence"),
                section_text(text, "Knowledge check"),
            ]
        )
        matches = [
            match.group(0) for match in DIRECT_STUDENT_TASK_MOTIFS.finditer(teaching_sections)
        ]
        assert matches == [], f"{path}: {matches}"


def test_coursebook_topic_lessons_cover_representative_int_domains(built_output: Path) -> None:
    output_manuscript = manuscript_dir(built_output)
    expected = {
        "human-intelligence-humint/agent-recruitment": "MICE Framework",
        "signals-intelligence-sigint/sigint-fundamentals": "communications-security",
        "open-source-intelligence-osint/osint-foundations": "IC OSINT Strategy",
        "open-source-intelligence-osint/geoint-and-imagery-intelligence": "GEOINT and Imagery Intelligence",
        "imagery-and-financial-intelligence/financial-intelligence-finint": "beneficial ownership",
        "counterintelligence/counterintelligence-fundamentals": "source-integrity",
        "technical-intelligence-and-cyber-operations/cyber-intelligence-fundamentals": "defensive taxonomy",
        "industrial-and-cyber-physical-intelligence/industrial-control-systems-ics-and-operational-technology": "SCADA, DCS, PLC",
        "cognitive-security/cognitive-security-operations": "narrative-risk map",
        "epistemic-rigor-and-analytic-tradecraft/structured-analytic-techniques-sats": "competing hypotheses",
        "ageint-agentic-intelligence/foundations-of-ageint": "agent run card",
        "legal-ethical-and-oversight-frameworks/legal-authorities-and-constraints": "Executive Order 12333",
        "productivity-intelligence-and-cognitive-performance/the-intelligent-operator-as-cognitive-athlete": "NASA-TLX",
        "ageint-agentic-intelligence/ageint-design-patterns-and-archetypes": "pattern",
        "gray-zone-hybrid-warfare-and-non-state-actors/gray-zone-warfare": "hybrid",
        "psychological-operations-and-influence/psyop-and-miso-doctrine": "MISO",
    }
    for relative, phrase in expected.items():
        path = output_manuscript / "parts" / relative / "00-overview.md"
        text = chapter_text(path)
        details = chapter_detail_titles(chapter_title_from_text(text))
        textbook_body = text.split(f"#### {details['runtime_map']}", 1)[0]
        assert phrase in textbook_body, f"{relative}: {phrase}"
