"""Tests for the AGEINT build orchestrator."""

from __future__ import annotations

import json
from pathlib import Path
import shutil

import pytest

import template_resolver
from _data_loaders import validate_declarative_tables
from build_pipeline import generated_output_is_stale, run_build
from citation_workflow import SOURCE_CITATION_COVERAGE_PATH, source_citation_coverage_summary
from orchestration_contracts import output_build_sentinels, source_freshness_roots

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"

# Build integrations use temporary project fixtures and require the shared SDK
# for manuscript injection. Standalone compatibility skips do not establish
# full native or release acceptance.
requires_template_repo = pytest.mark.skipif(template_resolver.resolve_template_repo(PROJECT_ROOT) is None, reason="sibling docxology/template repo not resolvable in this checkout")
REQUIRED_OUTPUT_DOC_DIRS = {
    Path("output"),
    Path("output/data"),
    Path("output/figures"),
    Path("output/manuscript"),
    Path("output/manuscript/appendices"),
    Path("output/manuscript/parts"),
    Path("output/pdf"),
    Path("output/reports"),
    Path("output/slides"),
    Path("output/web"),
}


def _minimal_project(tmp_path: Path) -> Path:
    project = tmp_path / "AGEINT"
    templates = project / "docs" / "manuscript" / "templates"
    templates.mkdir(parents=True)
    data_dir = project / "data"
    data_dir.mkdir()
    shutil.copytree(DATA, data_dir / DATA.name)
    (templates / "chapter.md").write_text("# {{SECTION_TITLE}}\n\n{{VISUAL_SYNTHESIS}}\n\nTEMPLATE SENTINEL\n\n{{SECTION_BODY}}\n", encoding="utf-8")
    _write_minimal_source_config(project)
    return project


def _write_minimal_source_config(project: Path) -> None:
    config = project / "docs" / "manuscript" / "config.yaml"
    config.parent.mkdir(parents=True, exist_ok=True)
    config.write_text('paper:\n  title: "Fixture project"\nbook:\n  title: "Fixture project"\n  license: "CC BY 4.0"\n  code_license: "Apache-2.0"\n', encoding="utf-8")


def _force_mermaid_placeholders(monkeypatch) -> None:
    monkeypatch.setenv("PATH", "")


@requires_template_repo
def test_default_build_preserves_neutral_template_library(tmp_path: Path, monkeypatch) -> None:
    _force_mermaid_placeholders(monkeypatch)
    project = _minimal_project(tmp_path)
    template_file = project / "docs" / "manuscript" / "templates" / "chapter.md"

    result = run_build(project, regenerate_source_template_library=False, allow_placeholder_figures=True)

    assert result.written_source_templates == 0
    assert "TEMPLATE SENTINEL" in template_file.read_text(encoding="utf-8")
    for relative in REQUIRED_OUTPUT_DOC_DIRS:
        assert (project / relative / "README.md").is_file(), relative
        assert (project / relative / "AGENTS.md").is_file(), relative
    assert (project / "output" / "data" / "curriculum_outline.json").is_file()
    assert (project / "output" / "data" / "curriculum" / "metadata.json").is_file()
    assert (project / "output" / "data" / "manuscript_variables.json").is_file()
    assert (project / "output" / "manuscript" / "parts" / "ageint-agentic-intelligence" / "foundations-of-ageint" / "00-overview.md").is_file()
    coverage = json.loads((project / SOURCE_CITATION_COVERAGE_PATH).read_text(encoding="utf-8"))
    summary = source_citation_coverage_summary(result.curriculum)
    assert coverage["summary"]["section_count"] == summary.section_count
    assert coverage["summary"]["citation_occurrences"] == summary.citation_occurrences
    appendix = project / "output" / "manuscript" / "appendices" / "bibliography-atlas" / "05-bind-the-claim-not-merely-the-citation-01.md"
    text = appendix.read_text(encoding="utf-8")
    for label, binding in coverage["claim_bindings"].items():
        field = binding["field"].removeprefix("$.summary.")
        assert f"| {label} | {coverage['summary'][field]} |" in text
        assert f"`{binding['path']}`" in text
        assert f"`{binding['field']}`" in text
    assert not (project / "output" / "reports" / "current_artifact_evidence.json").exists()


@pytest.mark.parametrize("existing_output", [False, True])
def test_missing_source_config_fails_the_build(tmp_path: Path, existing_output: bool) -> None:
    """Source validation must fail before figure work or any source/output writes."""
    project = tmp_path / "AGEINT"
    templates = project / "docs" / "manuscript" / "templates"
    templates.mkdir(parents=True)
    (templates / "chapter.md").write_text("# Keep this template\n", encoding="utf-8")
    if existing_output:
        figures = project / "output" / "figures"
        figures.mkdir(parents=True)
        (figures / "keep.png").write_bytes(b"existing figure")
    before = {path.relative_to(project): path.read_bytes() if path.is_file() else None for path in project.rglob("*")}
    missing_config = project / "docs" / "manuscript" / "config.yaml"

    with pytest.raises(FileNotFoundError) as error:
        run_build(project, regenerate_source_template_library=True, allow_placeholder_figures=False)

    assert missing_config.as_posix() in str(error.value)
    assert {path.relative_to(project): path.read_bytes() if path.is_file() else None for path in project.rglob("*")} == before
    if not existing_output:
        assert not (project / "output").exists()


def test_source_validation_rechecks_selected_project_config(tmp_path: Path) -> None:
    """Cached table loaders must not mask removal in a different project root."""
    _write_minimal_source_config(tmp_path)
    validate_declarative_tables(tmp_path)
    missing_config = tmp_path / "docs" / "manuscript" / "config.yaml"
    missing_config.unlink()

    with pytest.raises(FileNotFoundError) as error:
        validate_declarative_tables(tmp_path)

    assert missing_config.as_posix() in str(error.value)


@requires_template_repo
def test_build_freshness_uses_registered_stage_contracts(tmp_path: Path, monkeypatch) -> None:
    _force_mermaid_placeholders(monkeypatch)
    project = _minimal_project(tmp_path)

    assert Path("data") in source_freshness_roots()
    assert Path("figures/figure_registry.json") in output_build_sentinels()
    result = run_build(project, allow_placeholder_figures=True)

    assert result.figure_registry_path.is_file()
    assert generated_output_is_stale(project, project / "output") is False


@requires_template_repo
def test_explicit_regeneration_rewrites_only_template_library(tmp_path: Path, monkeypatch) -> None:
    _force_mermaid_placeholders(monkeypatch)
    project = _minimal_project(tmp_path)
    template_file = project / "docs" / "manuscript" / "templates" / "chapter.md"

    result = run_build(project, regenerate_source_template_library=True, allow_placeholder_figures=True)

    assert result.written_source_templates == 8
    rewritten = template_file.read_text(encoding="utf-8")
    assert "TEMPLATE SENTINEL" not in rewritten
    assert "{{SECTION_TITLE}}" in rewritten
    assert "{{CHAPTER_031_TITLE}}" not in rewritten
