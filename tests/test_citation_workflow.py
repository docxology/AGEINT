"""Tests for composable citation workflow helpers."""

from __future__ import annotations

from copy import deepcopy
import hashlib
import json
from pathlib import Path

import pytest

from citation_workflow import (
    SOURCE_CITATION_COVERAGE_PATH,
    render_citation_workflow_markdown,
    source_citation_cell,
    source_citation_spine,
    source_citation_spine_inline,
    source_key,
    source_section_citation_inventory,
    write_source_citation_coverage,
)
from build_pipeline import source_content_digest
from curriculum import load_curriculum, write_compact_curriculum_payload, write_curriculum_shards

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"


def test_source_keys_and_citation_spines_are_stable() -> None:
    assert source_key(1) == "ageint001"
    assert source_key(312) == "ageint312"
    assert source_citation_spine([137, 137, 155], limit=2) == "[@ageint137]; [@ageint155]."
    assert source_citation_spine_inline([137, 137, 155], limit=2) == "[@ageint137]; [@ageint155]"
    assert source_citation_cell([137, 137, 155]) == "[@ageint137]; [@ageint155]"
    assert source_citation_cell([]) == "-"
    assert source_citation_spine([], fallback="No source.") == "No source."
    assert source_citation_spine_inline([], fallback="No source") == "No source"


def test_source_section_inventory_paths_match_curriculum_shards() -> None:
    curriculum = load_curriculum(DATA)
    rows = source_section_citation_inventory(curriculum)
    unique_paths = {row.path for row in rows}

    assert unique_paths
    for relative_path in unique_paths:
        assert (PROJECT_ROOT / relative_path).is_file(), relative_path


@pytest.mark.parametrize("edit", ["citation", "section"])
def test_current_coverage_evidence_tracks_native_source_counts(tmp_path: Path, edit: str) -> None:
    payload = deepcopy(load_curriculum(DATA).payload)
    source = tmp_path / "data" / "curriculum"
    mirror = tmp_path / "output" / "data" / "curriculum_outline.json"

    def generate() -> tuple[dict, bytes]:
        write_curriculum_shards(payload, source)
        curriculum = load_curriculum(source)
        write_compact_curriculum_payload(curriculum.payload, mirror)
        path = write_source_citation_coverage(curriculum, tmp_path, source_digest=source_content_digest(tmp_path))
        report = json.loads(path.read_text(encoding="utf-8"))
        markdown = render_citation_workflow_markdown(curriculum)
        for label, binding in report["claim_bindings"].items():
            field = binding["field"].removeprefix("$.summary.")
            value = report["summary"][field]
            assert type(value) is int
            assert f"| {label} | {value} |" in markdown
            assert f"`{binding['path']}`" in markdown
            assert f"`{binding['field']}`" in markdown
        assert report["source_digest"] == source_content_digest(tmp_path)
        assert report["input"]["sha256"] == hashlib.sha256(mirror.read_bytes()).hexdigest()
        assert path == tmp_path / SOURCE_CITATION_COVERAGE_PATH
        assert not (tmp_path / "output" / "reports").exists()
        return report, path.read_bytes()

    before, before_bytes = generate()
    assert generate()[1] == before_bytes
    chapter = next(chapter for part in payload["parts"] for chapter in part["chapters"] if any(section.get("citations") for section in chapter["sections"]))
    section = next(section for section in chapter["sections"] if section.get("citations"))
    if edit == "citation":
        section["citations"].append(section["citations"][0])
        section_delta, citation_delta = 0, 1
    else:
        added = deepcopy(section)
        added["number"] = "coverage-regression"
        chapter["sections"].append(added)
        section_delta, citation_delta = 1, len(added["citations"])
    after, after_bytes = generate()
    assert after["summary"]["section_count"] == before["summary"]["section_count"] + section_delta
    assert after["summary"]["citation_occurrences"] == before["summary"]["citation_occurrences"] + citation_delta
    assert after["summary"]["unique_citation_keys"] == before["summary"]["unique_citation_keys"]
    assert after["source_digest"] != before["source_digest"]
    assert after["input"]["sha256"] != before["input"]["sha256"]
    assert after_bytes != before_bytes
    assert generate()[1] == after_bytes


def test_generated_identity_tables_preserve_real_evidence_validation(built_output: Path) -> None:
    evidence = pytest.importorskip("infrastructure.validation.evidence_registry")
    manuscript = built_output / "manuscript"
    registry = evidence.build_project_evidence_registry(PROJECT_ROOT)
    fragments = sorted(manuscript.rglob("02-evidence-contract.md")) + sorted(manuscript.rglob("04-assessment-route.md"))
    errors = []
    for fragment in fragments:
        report = evidence.validate_text_against_registry(fragment.read_text(encoding="utf-8"), registry)
        errors.extend((fragment.relative_to(manuscript).as_posix(), issue.line_number, issue.kind, issue.value) for issue in report.errors)
    assert errors == []
    negative = evidence.validate_text_against_registry("Source locator `1.101`.\n\n| Metric | Value |\n|---|---|\n| Observed | 1.101 |\n", evidence.VerifiedEvidenceRegistry())
    assert [issue.value for issue in negative.errors] == ["1.101"]
