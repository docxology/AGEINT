"""Smoke tests for thin AGEINT script entrypoints."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from citation_workflow import source_citation_coverage_summary
from curriculum import load_curriculum

PROJECT_ROOT = Path(__file__).resolve().parents[1]
DATA = PROJECT_ROOT / "data" / "curriculum"


def test_setup_hook_writes_output_docs() -> None:
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "setup_hook.py")],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode == 0
    assert (PROJECT_ROOT / "output" / "README.md").is_file()


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


def test_audit_pdf_quality_script_reports_json_contract() -> None:
    pdf = PROJECT_ROOT / "output" / "pdf" / "AGEINT_combined.pdf"
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
