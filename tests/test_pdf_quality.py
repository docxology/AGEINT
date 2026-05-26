"""Tests for rendered PDF quality auditing."""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
import time
from pathlib import Path

import pytest
from reportlab.pdfgen import canvas

from pdf_quality import (
    PdfPhraseHit,
    PdfQualityReport,
    audit_pdf_quality,
    extract_pdf_text,
    pdf_metadata,
    render_pdf_quality_markdown,
    report_json,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]

pytestmark = pytest.mark.skipif(
    not shutil.which("pdftotext") or not shutil.which("pdfinfo"),
    reason="pdftotext and pdfinfo required for PDF quality tests",
)


def _write_pdf(path: Path, pages: list[str]) -> None:
    pdf = canvas.Canvas(str(path))
    for index, text in enumerate(pages):
        pdf.drawString(72, 720, text)
        if index < len(pages) - 1:
            pdf.showPage()
    pdf.save()


def test_pdf_quality_script_reports_clean_rendered_pdf() -> None:
    pdf = PROJECT_ROOT / "output" / "pdf" / "AGEINT_combined.pdf"
    if not pdf.is_file():
        pytest.skip("Rendered combined PDF not present")
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
    assert report.stale_pdf is True
    assert report.page_count == 0


def test_audit_pdf_quality_flags_banned_phrase_on_page(tmp_path: Path) -> None:
    pdf_path = tmp_path / "flagged.pdf"
    _write_pdf(
        pdf_path,
        [
            "Chapter overview with curriculum-safe prose.",
            "This page still contains a TODO marker for reviewers.",
        ],
    )

    report = audit_pdf_quality(pdf_path, banned_phrases=("TODO",))

    assert report.exists is True
    assert report.ok is False
    assert report.page_count >= 2
    assert report.text_character_count > 0
    assert report.flagged_pages == (2,)
    assert report.banned_phrase_hits
    assert report.banned_phrase_hits[0].phrase == "TODO"
    assert report.banned_phrase_hits[0].page == 2


def test_audit_pdf_quality_clean_pdf_is_ok(tmp_path: Path) -> None:
    pdf_path = tmp_path / "clean.pdf"
    _write_pdf(pdf_path, ["Curriculum-safe analyst workbook content."])

    report = audit_pdf_quality(pdf_path)

    assert report.ok is True
    assert report.banned_phrase_hits == ()
    assert report.flagged_pages == ()
    assert report.stale_pdf is False


def test_audit_pdf_quality_detects_stale_pdf_from_manuscript_dir(tmp_path: Path) -> None:
    manuscript_dir = tmp_path / "manuscript"
    manuscript_dir.mkdir()
    source = manuscript_dir / "01_introduction.md"
    source.write_text("# Introduction\n\nFresh manuscript prose.\n", encoding="utf-8")

    pdf_path = tmp_path / "stale.pdf"
    _write_pdf(pdf_path, ["Rendered before the manuscript edit."])
    stale_mtime = time.time() - 3600
    import os

    os.utime(pdf_path, (stale_mtime, stale_mtime))

    report = audit_pdf_quality(pdf_path, manuscript_dir=manuscript_dir)

    assert report.stale_pdf is True
    assert report.ok is False


def test_audit_pdf_quality_uses_combined_manuscript_mtime(tmp_path: Path) -> None:
    pdf_dir = tmp_path / "pdf"
    pdf_dir.mkdir()
    combined = pdf_dir / "_combined_manuscript.md"
    combined.write_text("# Combined\n\nNewer source.\n", encoding="utf-8")

    pdf_path = pdf_dir / "combined.pdf"
    _write_pdf(pdf_path, ["Older render output."])
    stale_mtime = time.time() - 7200
    import os

    os.utime(pdf_path, (stale_mtime, stale_mtime))

    report = audit_pdf_quality(pdf_path)

    assert report.stale_pdf is True
    assert report.newest_manuscript_mtime > report.pdf_mtime


def test_render_pdf_quality_markdown_includes_hits(tmp_path: Path) -> None:
    report = PdfQualityReport(
        pdf_path=str(tmp_path / "sample.pdf"),
        exists=True,
        page_count=2,
        text_character_count=120,
        creation_date="D:20260101000000",
        pdf_mtime=1.0,
        newest_manuscript_mtime=0.5,
        stale_pdf=False,
        banned_phrase_hits=(
            PdfPhraseHit(phrase="TODO", page=2, count=1),
        ),
        flagged_pages=(2,),
    )

    markdown = render_pdf_quality_markdown(report)

    assert "Banned Phrase Hits" in markdown
    assert "TODO" in markdown
    assert "| OK | false |" in markdown


def test_render_pdf_quality_markdown_without_hits() -> None:
    report = PdfQualityReport(
        pdf_path="sample.pdf",
        exists=True,
        page_count=1,
        text_character_count=50,
        creation_date="",
        pdf_mtime=1.0,
        newest_manuscript_mtime=0.0,
        stale_pdf=False,
        banned_phrase_hits=(),
        flagged_pages=(),
    )

    markdown = render_pdf_quality_markdown(report)

    assert "Banned Phrase Hits" not in markdown
    assert "| OK | true |" in markdown


def test_report_json_round_trip() -> None:
    report = PdfQualityReport(
        pdf_path="sample.pdf",
        exists=True,
        page_count=3,
        text_character_count=90,
        creation_date="D:20260101000000",
        pdf_mtime=10.0,
        newest_manuscript_mtime=5.0,
        stale_pdf=False,
        banned_phrase_hits=(),
        flagged_pages=(),
    )

    payload = json.loads(report_json(report))

    assert payload["ok"] is True
    assert payload["page_count"] == 3
    assert payload["banned_phrase_hits"] == []


def test_extract_pdf_text_and_metadata(tmp_path: Path) -> None:
    pdf_path = tmp_path / "meta.pdf"
    _write_pdf(pdf_path, ["Metadata extraction check."])

    text = extract_pdf_text(pdf_path)
    metadata = pdf_metadata(pdf_path)

    assert "Metadata extraction check" in text
    assert metadata.get("Pages", "1") == "1" or metadata.get("Pages")
