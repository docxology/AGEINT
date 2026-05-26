"""PDF text extraction and quality audit helpers for AGEINT."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import json
import re
import subprocess
from typing import Any


DEFAULT_BANNED_PHRASES: tuple[str, ...] = (
    "defensible claim whose meaning",
    "treats each source topic through",
    "parsed AGEINT source spine",
    "Use this module studio plan",
    "The answer should",
    "completed artifact is a",
    "fictional",
    "review review",
    "lens lens",
    "Lens lens",
    "placeholder",
    "boilerplate",
    "TODO",
    "TBD",
    "FIXME",
    "lorem ipsum",
    "draft placeholder",
    "ORCID:",
)
SUPPORT_DOC_NAMES = {"AGENTS.md", "README.md"}


@dataclass(frozen=True)
class PdfPhraseHit:
    """A banned phrase occurrence in extracted PDF text."""

    phrase: str
    page: int
    count: int


@dataclass(frozen=True)
class PdfQualityReport:
    """Structured result from auditing a rendered AGEINT PDF."""

    pdf_path: str
    exists: bool
    page_count: int
    text_character_count: int
    creation_date: str
    pdf_mtime: float
    newest_manuscript_mtime: float
    stale_pdf: bool
    banned_phrase_hits: tuple[PdfPhraseHit, ...]
    flagged_pages: tuple[int, ...]

    @property
    def ok(self) -> bool:
        return (
            self.exists
            and self.page_count > 0
            and self.text_character_count > 0
            and not self.stale_pdf
            and not self.banned_phrase_hits
        )

    def as_dict(self) -> dict[str, Any]:
        return {
            "pdf_path": self.pdf_path,
            "exists": self.exists,
            "page_count": self.page_count,
            "text_character_count": self.text_character_count,
            "creation_date": self.creation_date,
            "pdf_mtime": self.pdf_mtime,
            "newest_manuscript_mtime": self.newest_manuscript_mtime,
            "stale_pdf": self.stale_pdf,
            "banned_phrase_hits": [
                {"phrase": hit.phrase, "page": hit.page, "count": hit.count}
                for hit in self.banned_phrase_hits
            ],
            "flagged_pages": list(self.flagged_pages),
            "ok": self.ok,
        }


def extract_pdf_text(pdf_path: Path) -> str:
    """Extract layout-preserving text from a PDF with ``pdftotext``."""
    result = subprocess.run(
        ["pdftotext", "-layout", str(pdf_path), "-"],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def pdf_metadata(pdf_path: Path) -> dict[str, str]:
    """Return parsed ``pdfinfo`` metadata."""
    result = subprocess.run(
        ["pdfinfo", str(pdf_path)],
        check=True,
        capture_output=True,
        text=True,
    )
    metadata: dict[str, str] = {}
    for line in result.stdout.splitlines():
        if ":" not in line:
            continue
        key, value = line.split(":", 1)
        metadata[key.strip()] = value.strip()
    return metadata


def audit_pdf_quality(
    pdf_path: Path,
    *,
    manuscript_dir: Path | None = None,
    banned_phrases: tuple[str, ...] = DEFAULT_BANNED_PHRASES,
) -> PdfQualityReport:
    """Audit a rendered PDF for stale output and reader-facing banned phrases."""
    pdf_path = Path(pdf_path)
    if not pdf_path.is_file():
        return PdfQualityReport(
            pdf_path=str(pdf_path),
            exists=False,
            page_count=0,
            text_character_count=0,
            creation_date="",
            pdf_mtime=0.0,
            newest_manuscript_mtime=_newest_pdf_source_mtime(pdf_path, manuscript_dir),
            stale_pdf=True,
            banned_phrase_hits=(),
            flagged_pages=(),
        )

    metadata = pdf_metadata(pdf_path)
    text = extract_pdf_text(pdf_path)
    pages = _split_pages(text)
    hits = _phrase_hits(pages, banned_phrases)
    newest_manuscript_mtime = _newest_pdf_source_mtime(pdf_path, manuscript_dir)
    pdf_mtime = pdf_path.stat().st_mtime
    flagged_pages = tuple(sorted({hit.page for hit in hits}))
    return PdfQualityReport(
        pdf_path=str(pdf_path),
        exists=True,
        page_count=_page_count(metadata, len(pages)),
        text_character_count=len(text.strip()),
        creation_date=metadata.get("CreationDate", ""),
        pdf_mtime=pdf_mtime,
        newest_manuscript_mtime=newest_manuscript_mtime,
        stale_pdf=bool(newest_manuscript_mtime and pdf_mtime < newest_manuscript_mtime),
        banned_phrase_hits=tuple(hits),
        flagged_pages=flagged_pages,
    )


def render_pdf_quality_markdown(report: PdfQualityReport) -> str:
    """Render a compact Markdown report."""
    lines = [
        "# AGEINT PDF Quality Audit",
        "",
        "| Measure | Value |",
        "|---|---:|",
        f"| PDF exists | {str(report.exists).lower()} |",
        f"| Pages | {report.page_count} |",
        f"| Extracted text characters | {report.text_character_count} |",
        f"| Stale PDF | {str(report.stale_pdf).lower()} |",
        f"| Flagged pages | {', '.join(str(page) for page in report.flagged_pages) or '-' } |",
        f"| OK | {str(report.ok).lower()} |",
    ]
    if report.banned_phrase_hits:
        lines.extend(["", "## Banned Phrase Hits", "", "| Phrase | Page | Count |", "|---|---:|---:|"])
        for hit in report.banned_phrase_hits:
            lines.append(f"| {_table_cell(hit.phrase)} | {hit.page} | {hit.count} |")
    return "\n".join(lines)


def report_json(report: PdfQualityReport) -> str:
    """Return the report as stable JSON."""
    return json.dumps(report.as_dict(), indent=2, sort_keys=True)


def _split_pages(text: str) -> list[str]:
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages or [text]


def _phrase_hits(pages: list[str], banned_phrases: tuple[str, ...]) -> list[PdfPhraseHit]:
    hits: list[PdfPhraseHit] = []
    for page_number, page_text in enumerate(pages, 1):
        for phrase in banned_phrases:
            count = len(re.findall(re.escape(phrase), page_text, flags=re.IGNORECASE))
            if count:
                hits.append(PdfPhraseHit(phrase=phrase, page=page_number, count=count))
    return hits


def _page_count(metadata: dict[str, str], fallback: int) -> int:
    raw = metadata.get("Pages", "")
    return int(raw) if raw.isdigit() else fallback


def _newest_markdown_mtime(manuscript_dir: Path | None) -> float:
    if manuscript_dir is None:
        return 0.0
    root = Path(manuscript_dir)
    if not root.is_dir():
        return 0.0
    mtimes = [
        path.stat().st_mtime
        for path in root.rglob("*.md")
        if path.name not in SUPPORT_DOC_NAMES
    ]
    return max(mtimes) if mtimes else 0.0


def _newest_pdf_source_mtime(pdf_path: Path, manuscript_dir: Path | None) -> float:
    """Return the newest source timestamp that should precede the PDF."""
    combined_sources = [
        pdf_path.parent / "_combined_manuscript.md",
        pdf_path.parent / "_combined_manuscript.tex",
    ]
    mtimes = [path.stat().st_mtime for path in combined_sources if path.is_file()]
    if mtimes:
        return max(mtimes)
    return _newest_markdown_mtime(manuscript_dir)


def _table_cell(value: object) -> str:
    return re.sub(r"\s+", " ", str(value)).replace("|", "/").strip()


__all__ = [
    "DEFAULT_BANNED_PHRASES",
    "PdfPhraseHit",
    "PdfQualityReport",
    "audit_pdf_quality",
    "extract_pdf_text",
    "pdf_metadata",
    "render_pdf_quality_markdown",
    "report_json",
]
