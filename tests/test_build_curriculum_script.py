"""Tests for the AGEINT build orchestrator."""

from __future__ import annotations

from pathlib import Path
import shutil
import subprocess
import sys

import pytest

import template_resolver
from build_pipeline import generated_output_is_stale, run_build
from figures import _02b_mermaid as mermaid_rendering
from orchestration_contracts import output_build_sentinels, source_freshness_roots

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT_ROOT / "scripts" / "build_curriculum.py"
DATA = PROJECT_ROOT / "data" / "curriculum"

# Every test decorated with @requires_template_repo below calls run_build()
# (directly, via a tmp_path project, or via a subprocess against this repo's
# actual PROJECT_ROOT) — render_manuscript() unconditionally calls
# substitute_manuscript_text(), which needs the sibling docxology/template
# repo's `infrastructure` package (src/manuscript_injection.py) regardless of
# project size or whether the copy is tmp_path-isolated. One test
# (test_build_curriculum_script_smoke) is worse than "just fails": it runs
# scripts/build_curriculum.py with cwd=PROJECT_ROOT — the REAL project root,
# not a tmp_path copy — so an unguarded crash partway through rendering
# leaves output/manuscript/ emptied for the rest of the pytest session,
# cascading into ~45 unrelated failures in every other test that reads
# generated manuscript content. Confirmed live, twice, in a genuinely
# isolated checkout with no template sibling (matching GitHub Actions
# exactly): first pass only guarded the two PROJECT_ROOT-touching tests and
# still surfaced 3 more tmp_path-based failures from this same file: all
# call run_build() too, just non-destructively. Skip the whole class rather
# than whack-a-mole discovering each one via another isolated run.
requires_template_repo = pytest.mark.skipif(
    template_resolver.resolve_template_repo(PROJECT_ROOT) is None,
    reason="sibling docxology/template repo not resolvable in this checkout",
)
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
    templates = project / "manuscript" / "templates"
    templates.mkdir(parents=True)
    data_dir = project / "data"
    data_dir.mkdir()
    shutil.copytree(DATA, data_dir / DATA.name)
    (templates / "chapter.md").write_text(
        "# {{SECTION_TITLE}}\n\n{{VISUAL_SYNTHESIS}}\n\nTEMPLATE SENTINEL\n\n{{SECTION_BODY}}\n",
        encoding="utf-8",
    )
    return project


def _force_mermaid_placeholders(monkeypatch) -> None:
    monkeypatch.setattr(mermaid_rendering.shutil, "which", lambda _name: None)


@requires_template_repo
def test_default_build_preserves_neutral_template_library(tmp_path: Path, monkeypatch) -> None:
    _force_mermaid_placeholders(monkeypatch)
    project = _minimal_project(tmp_path)
    template_file = project / "manuscript" / "templates" / "chapter.md"

    result = run_build(
        project,
        regenerate_source_template_library=False,
        allow_placeholder_figures=True,
    )

    assert result.written_source_templates == 0
    assert "TEMPLATE SENTINEL" in template_file.read_text(encoding="utf-8")
    for relative in REQUIRED_OUTPUT_DOC_DIRS:
        assert (project / relative / "README.md").is_file(), relative
        assert (project / relative / "AGENTS.md").is_file(), relative
    assert (project / "output" / "data" / "curriculum_outline.json").is_file()
    assert (project / "output" / "data" / "curriculum" / "metadata.json").is_file()
    assert (project / "output" / "data" / "manuscript_variables.json").is_file()
    assert (
        project
        / "output"
        / "manuscript"
        / "parts"
        / "ageint-agentic-intelligence"
        / "foundations-of-ageint"
        / "00-overview.md"
    ).is_file()
    foundations = (
        project
        / "output"
        / "manuscript"
        / "parts"
        / "ageint-agentic-intelligence"
        / "foundations-of-ageint"
        / "01-practice-studio.md"
    ).read_text(encoding="utf-8")
    assert "#### Lesson 1:" in foundations
    worked = (
        project
        / "output"
        / "manuscript"
        / "parts"
        / "ageint-agentic-intelligence"
        / "foundations-of-ageint"
        / "01-practice-studio.md"
    ).read_text(encoding="utf-8")
    assert "**Filled artifact.**" in worked
    assert (
        "#### Foundations of AGEINT answer quality rubric: source evidence, uncertainty, and safe transfer"
        in worked
    )
    assert "uses [@fig:" in (
        project
        / "output"
        / "manuscript"
        / "parts"
        / "ageint-agentic-intelligence"
        / "foundations-of-ageint"
        / "00-overview.md"
    ).read_text(encoding="utf-8")
    assert "Generated section context" not in foundations


@requires_template_repo
def test_build_script_resolves_template_repo_without_manual_pythonpath() -> None:
    repo = template_resolver.ensure_template_repo_on_path(PROJECT_ROOT)

    assert repo is not None
    assert (repo / "infrastructure" / "validation" / "cli" / "__init__.py").is_file()
    assert str(repo) in sys.path


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
    template_file = project / "manuscript" / "templates" / "chapter.md"

    result = run_build(
        project,
        regenerate_source_template_library=True,
        allow_placeholder_figures=True,
    )

    assert result.written_source_templates == 8
    rewritten = template_file.read_text(encoding="utf-8")
    assert "TEMPLATE SENTINEL" not in rewritten
    assert "{{SECTION_TITLE}}" in rewritten
    assert "{{CHAPTER_031_TITLE}}" not in rewritten


@requires_template_repo
def test_build_curriculum_script_smoke() -> None:
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        # Real Mermaid rendering (mmdc + headless Chrome) for ~24 figures takes
        # well over the original 120s smoke budget; allow a realistic ceiling.
        timeout=600,
    )
    assert result.returncode == 0
    combined = f"{result.stdout}\n{result.stderr}"
    assert "parts" in combined.lower()
    assert "modules" in combined.lower() or "chapters" in combined.lower()
