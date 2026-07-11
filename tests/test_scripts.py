"""Smoke tests for thin AGEINT script entrypoints."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

import pytest
from reportlab.pdfgen import canvas

import template_resolver
from build_pipeline import generated_output_is_stale
from citation_workflow import source_citation_coverage_summary
from curriculum import load_curriculum
from orchestration_contracts import output_build_sentinels

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"

# See the matching guard in test_build_curriculum_script.py for the full
# rationale: this test's subprocess runs scripts/z_generate_manuscript_variables.py
# with cwd=PROJECT_ROOT, which delegates to the real run_build() against this
# repo's actual output/ tree (not a tmp_path copy) — confirmed live to crash
# partway through manuscript rendering and leave output/manuscript/ emptied
# for the rest of the pytest session when the template repo isn't resolvable.
requires_template_repo = pytest.mark.skipif(
    template_resolver.resolve_template_repo(PROJECT_ROOT) is None,
    reason="sibling docxology/template repo not resolvable in this checkout",
)


def _write_pdf(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    pdf = canvas.Canvas(str(path))
    pdf.drawString(72, 720, text)
    pdf.save()


def _write_at(path: Path, text: str, timestamp: float) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")
    os.utime(path, (timestamp, timestamp))


def test_generated_output_staleness_detects_newer_source(tmp_path: Path) -> None:
    output = tmp_path / "output"
    _write_at(tmp_path / "data" / "curriculum" / "sections.jsonl", "{}", 100.0)
    _write_at(tmp_path / "src" / "renderer.py", "VALUE = 1\n", 100.0)
    _write_at(tmp_path / "manuscript" / "templates" / "chapter.md", "{{BODY}}\n", 100.0)
    _write_at(tmp_path / "scripts" / "build_curriculum.py", "print('build')\n", 100.0)
    _write_at(tmp_path / "pyproject.toml", "[project]\nname = 'fixture'\n", 100.0)
    for relative in output_build_sentinels():
        _write_at(output / relative, "built\n", 200.0)

    assert generated_output_is_stale(tmp_path, output) is False

    _write_at(tmp_path / "data" / "source_support_expansion.yaml", "default_citations: []\n", 300.0)

    assert generated_output_is_stale(tmp_path, output) is True


def test_setup_hook_writes_output_docs() -> None:
    # setup_hook.py hardcodes PROJECT_ROOT from its own __file__, so unlike
    # every other subprocess test in this file it cannot be pointed at a
    # tmp_path copy — it always writes into this repo's real output/ tree.
    # write_output_directory_docs() (what it calls) writes a generic stub
    # for EVERY output subdirectory including output/manuscript/, which the
    # real build pipeline overwrites with manuscript-specific content via
    # write_manuscript_output_docs() (src/manuscript_manifest/_05_part.py)
    # as part of a full render_manuscript() pass. Confirmed live (real
    # GitHub Actions run, py3.10 and py3.12): when no full rebuild follows
    # in the same session (true whenever the sibling template repo isn't
    # resolvable — CI's own `test` job never rebuilds before running
    # pytest), the generic stub this test writes persists and causes
    # test_audit_heading_support_script_reports_json_contract, which runs
    # later in this same file, to see stale content and fail — a bug this
    # test's own side effect causes, not a real content-quality issue.
    # Restore the manuscript-specific docs immediately after asserting,
    # matching what a full build always does.
    from output_docs import write_manuscript_output_docs
    from rendered_heading_support import ensure_heading_support_in_tree

    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "setup_hook.py")],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    try:
        assert result.returncode == 0
        assert (PROJECT_ROOT / "output" / "README.md").is_file()
    finally:
        # Mirror the exact restoration order render_manuscript() uses
        # (src/manuscript_manifest/_05_part.py:311-312): write_manuscript_output_docs()
        # alone leaves doc-stub headings without the citation-anchor lines that
        # ensure_heading_support_in_tree() injects, which trips the heading-support
        # audit for the rest of the pytest session.
        manuscript_dir = PROJECT_ROOT / "output" / "manuscript"
        write_manuscript_output_docs(manuscript_dir)
        ensure_heading_support_in_tree(manuscript_dir)


def test_generate_figures_script_runs() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "generate_figures.py"),
            "--allow-placeholder-figures",
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert "Rendered" in result.stdout


@requires_template_repo
def test_z_generate_manuscript_variables_prints_path() -> None:
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "z_generate_manuscript_variables.py")],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        # This script delegates to the full run_build() (template-compat contract),
        # which re-renders all 64 figures (24 Mermaid/Chrome subprocesses, ~185s).
        # Corpus growth pushed the full build to ~150-190s, past the 120s used by
        # the lighter script tests; 300s gives headroom without masking a real hang.
        timeout=300,
    )
    assert result.returncode == 0
    assert result.stdout.strip().endswith("manuscript_variables.json")


def test_check_rendered_references_script_passes(built_output: Path) -> None:
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "check_rendered_references.py"), str(built_output)],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    assert "Rendered reference audit passed" in result.stdout


def test_count_citations_script_reports_source_counts() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "count_citations.py"),
            "--format",
            "json",
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    payload = json.loads(result.stdout)
    summary = source_citation_coverage_summary(load_curriculum(DATA))
    assert payload["source_sections"] == summary.section_count
    assert payload["source_citation_occurrences"] == summary.citation_occurrences
    assert payload["source_zero_citation_sections"] == summary.zero_citation_sections


def test_audit_pdf_quality_script_reports_json_contract(tmp_path: Path) -> None:
    pdf = tmp_path / "quality-contract.pdf"
    _write_pdf(pdf, "AGEINT rendered quality contract.")
    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "audit_pdf_quality.py"),
            "--pdf",
            str(pdf),
            "--format",
            "json",
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["flagged_pages"] == []
    assert payload["stale_pdf"] is False


def test_audit_heading_support_script_reports_json_contract() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "audit_heading_support.py"),
            "--format",
            "json",
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["heading_count"] > 0
    assert payload["unsupported_heading_count"] == 0
    assert payload["unsupported_headings"] == []


def test_audit_orchestration_contract_script_reports_json_contract() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "audit_orchestration_contract.py"),
            "--format",
            "json",
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["pipeline"]["stage_count"] >= 8
    assert payload["audits"]["contract_count"] >= 10
    assert payload["source_packs"]["registry_count"] == 2
