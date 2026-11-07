"""CLI format/error contracts and source-freshness behavior using real inputs."""

from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path

from reportlab.pdfgen import canvas

from build_pipeline import generated_output_is_stale
from orchestration_contracts import output_build_sentinels

PROJECT_ROOT = Path(__file__).resolve().parents[1]


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
    _write_at(tmp_path / "docs" / "manuscript" / "templates" / "chapter.md", "{{BODY}}\n", 100.0)
    _write_at(tmp_path / "scripts" / "build_curriculum.py", "print('build')\n", 100.0)
    _write_at(tmp_path / "pyproject.toml", "[project]\nname = 'fixture'\n", 100.0)
    for relative in output_build_sentinels():
        _write_at(output / relative, "built\n", 200.0)

    assert generated_output_is_stale(tmp_path, output) is False

    _write_at(tmp_path / "data" / "source_support_expansion.yaml", "default_citations: []\n", 300.0)

    assert generated_output_is_stale(tmp_path, output) is True






def test_audit_pdf_quality_script_reports_json_contract(tmp_path: Path) -> None:
    pdf = tmp_path / "quality-contract.pdf"
    _write_pdf(pdf, "AGEINT rendered quality contract.")
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "audit_pdf_quality.py"), "--pdf", str(pdf), "--format", "json"], cwd=PROJECT_ROOT, check=False, capture_output=True, text=True, timeout=180
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["flagged_pages"] == []
    assert payload["stale_pdf"] is False


def test_audit_heading_support_script_reports_json_contract(tmp_path: Path) -> None:
    document = tmp_path / "navigation.md"
    document.write_text("# Local section {#sec:local}\n\nStructural navigation only.\n", encoding="utf-8")
    command = [sys.executable, str(PROJECT_ROOT / "scripts" / "audit_heading_support.py"), "--manuscript-dir", str(tmp_path), "--format", "json"]
    result = subprocess.run(command, cwd=PROJECT_ROOT, check=False, capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["scope"] == "structural_navigation_not_evidence"
    assert payload["heading_count"] == 1
    assert payload["unsupported_headings"] == []

    document.write_text("## Rule without navigation\n\nAuthor-defined rule.\n", encoding="utf-8")
    result = subprocess.run(command, cwd=PROJECT_ROOT, check=False, capture_output=True, text=True, timeout=120)
    assert result.returncode == 1, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["unsupported_heading_count"] == 1
    assert payload["unsupported_headings"][0]["title"] == "Rule without navigation"


