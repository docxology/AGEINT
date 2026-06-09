"""Tests for AGEINT manuscript variable generation."""

from __future__ import annotations

import json
from pathlib import Path

from build_pipeline import run_build
from curriculum import load_curriculum
from intelligence_content import INTELLIGENCE_RESEARCH_ANCHORS
from manuscript_variables import (
    generate_variables,
    reference_bibtex_files,
    save_variables,
    write_bibtex_files,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_save_variables_writes_sorted_json(tmp_path: Path) -> None:
    target = tmp_path / "variables.json"
    payload = {"B": "two", "A": "one"}

    path = save_variables(payload, target)

    assert path == target
    written = json.loads(target.read_text(encoding="utf-8"))
    assert list(written.keys()) == sorted(payload.keys())


def test_write_bibtex_files_replaces_legacy_combined_bib(tmp_path: Path) -> None:
    target = tmp_path / "manuscript"
    target.mkdir()
    (target / "references.bib").write_text("@misc{legacy}", encoding="utf-8")
    (target / "references-stale.bib").write_text("@misc{stale}", encoding="utf-8")

    write_bibtex_files(
        target,
        {
            "references-source-guide-001-050.bib": "@misc{ageint001, title = {One}}",
        },
    )

    assert not (target / "references.bib").exists()
    assert not (target / "references-stale.bib").exists()
    assert (target / "references-source-guide-001-050.bib").is_file()


def test_reference_bibtex_files_include_research_anchor_shards() -> None:
    curriculum = load_curriculum(PROJECT_ROOT / "data" / "curriculum")
    files = reference_bibtex_files(curriculum.references)

    last_anchor = len(INTELLIGENCE_RESEARCH_ANCHORS)
    last_start = ((last_anchor - 1) // 50) * 50 + 1
    assert any(name.startswith("references-research-anchors-") for name in files)
    assert f"references-research-anchors-{last_start:03d}-{last_anchor:03d}.bib" in files
    assert "references-source-quality.bib" in files


def test_run_build_writes_variables_json(tmp_path: Path) -> None:
    import shutil

    project = tmp_path / "AGEINT"
    shutil.copytree(PROJECT_ROOT / "data", project / "data")
    (project / "manuscript").mkdir()

    result = run_build(project)

    assert result.variables_path.is_file()
    payload = json.loads(result.variables_path.read_text(encoding="utf-8"))
    assert int(payload["CURRICULUM_CHAPTER_COUNT"]) == 51


def test_generate_variables_matches_curriculum_stats() -> None:
    variables = generate_variables(PROJECT_ROOT)

    assert variables["CURRICULUM_PART_COUNT"] == "16"
    assert variables["CURRICULUM_CHAPTER_COUNT"] == "51"
    assert int(variables["INTELLIGENCE_RESEARCH_ANCHOR_COUNT"]) >= 172
    assert "never hand-edit `output/manuscript/`" in variables["CITATION_WORKFLOW_GUIDE"]
    assert "| Source sections | 723 |" in variables["CITATION_WORKFLOW_GUIDE"]
    assert "723 source sections" in variables["SOURCE_CITATION_COVERAGE_SUMMARY"]
    assert "| Chapter | Section | Source title | Citation count | Citation keys |" in variables[
        "SOURCE_SECTION_CITATION_ROWS"
    ]
