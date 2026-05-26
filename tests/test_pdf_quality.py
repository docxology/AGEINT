"""Tests for rendered PDF quality auditing."""

from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

from pdf_quality import audit_pdf_quality

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_pdf_quality_script_reports_clean_rendered_pdf() -> None:
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
    assert payload["page_count"] > 0
    assert payload["text_character_count"] > 0
    assert payload["stale_pdf"] is False
    assert payload["flagged_pages"] == []
    assert payload["banned_phrase_hits"] == []


def test_pdf_quality_reports_missing_pdf_as_not_ok(tmp_path: Path) -> None:
    report = audit_pdf_quality(
        tmp_path / "missing.pdf",
        manuscript_dir=PROJECT_ROOT / "output" / "manuscript",
    )

    assert report.exists is False
    assert report.ok is False
