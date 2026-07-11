"""PDF text extraction and quality audit helpers for AGEINT."""

from __future__ import annotations

from dataclasses import dataclass, field
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
)
SUPPORT_DOC_NAMES = {"AGENTS.md", "README.md"}

# A fresh git checkout (as opposed to a real edit-then-rebuild cycle) writes
# every tracked file at roughly the same instant, in whatever order git's
# tree-walk visits them — not the logical source-before-output order a real
# build produces. Confirmed live: a genuinely fresh `git clone` of this repo
# showed the manuscript's newest mtime just 21ms after the PDF's mtime,
# tripping a strict `<` comparison as "stale" even though nothing was
# actually rebuilt. A real edit-then-rebuild gap is seconds to minutes;
# checkout-ordering noise is milliseconds. This tolerance absorbs the noise
# without masking genuine staleness.
STALE_PDF_TOLERANCE_SECONDS = 30.0


@dataclass(frozen=True)
class PdfPhraseHit:
    """A banned phrase occurrence in extracted PDF text."""

    phrase: str
    page: int
    count: int


@dataclass(frozen=True)
class PdfLinkIssue:
    """A PDF annotation target that should not appear in reader output."""

    page: int
    issue: str
    target: str


@dataclass(frozen=True)
class PdfLinkAudit:
    """Structured annotation audit for rendered PDF links."""

    available: bool = True
    uri_links: int = 0
    file_actions: int = 0
    bad_targets: tuple[PdfLinkIssue, ...] = ()
    skipped_reason: str = ""

    @property
    def bad_target_count(self) -> int:
        return len(self.bad_targets)

    @property
    def ok(self) -> bool:
        return self.available and self.file_actions == 0 and not self.bad_targets

    def as_dict(self) -> dict[str, Any]:
        return {
            "available": self.available,
            "uri_links": self.uri_links,
            "file_actions": self.file_actions,
            "bad_target_count": self.bad_target_count,
            "bad_targets": [
                {
                    "page": issue.page,
                    "issue": issue.issue,
                    "target": issue.target,
                }
                for issue in self.bad_targets
            ],
            "skipped_reason": self.skipped_reason,
            "ok": self.ok,
        }


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
    link_audit: PdfLinkAudit = field(default_factory=PdfLinkAudit)

    @property
    def ok(self) -> bool:
        return (
            self.exists
            and self.page_count > 0
            and self.text_character_count > 0
            and not self.stale_pdf
            and not self.banned_phrase_hits
            and self.link_audit.ok
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
            "link_audit": self.link_audit.as_dict(),
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
            link_audit=PdfLinkAudit(available=pdf_path.is_file()),
        )

    metadata = pdf_metadata(pdf_path)
    text = extract_pdf_text(pdf_path)
    pages = _split_pages(text)
    hits = _phrase_hits(pages, banned_phrases)
    link_audit = audit_pdf_links(pdf_path)
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
        stale_pdf=bool(
            newest_manuscript_mtime
            and pdf_mtime < newest_manuscript_mtime - STALE_PDF_TOLERANCE_SECONDS
        ),
        banned_phrase_hits=tuple(hits),
        flagged_pages=flagged_pages,
        link_audit=link_audit,
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
        f"| URI links | {report.link_audit.uri_links} |",
        f"| File actions | {report.link_audit.file_actions} |",
        f"| Bad link targets | {report.link_audit.bad_target_count} |",
        f"| OK | {str(report.ok).lower()} |",
    ]
    if report.banned_phrase_hits:
        lines.extend(["", "## Banned Phrase Hits", "", "| Phrase | Page | Count |", "|---|---:|---:|"])
        for hit in report.banned_phrase_hits:
            lines.append(f"| {_table_cell(hit.phrase)} | {hit.page} | {hit.count} |")
    if report.link_audit.bad_targets:
        lines.extend(["", "## Bad Link Targets", "", "| Page | Issue | Target |", "|---:|---|---|"])
        for issue in report.link_audit.bad_targets:
            lines.append(
                f"| {issue.page} | {_table_cell(issue.issue)} | {_table_cell(issue.target)} |"
            )
    return "\n".join(lines)


def report_json(report: PdfQualityReport) -> str:
    """Return the report as stable JSON."""
    return json.dumps(report.as_dict(), indent=2, sort_keys=True)


def audit_pdf_links(pdf_path: Path) -> PdfLinkAudit:
    """Audit PDF annotations for Markdown-file links and file/launch actions."""
    try:
        from pypdf import PdfReader
    except ImportError:  # pragma: no cover - dependency is present in test/runtime env.
        return PdfLinkAudit(available=False, skipped_reason="pypdf is not installed")

    uri_links = 0
    file_actions = 0
    issues: list[PdfLinkIssue] = []
    try:
        reader = PdfReader(str(pdf_path))
    except Exception as exc:  # pragma: no cover - corrupt PDFs fail earlier via pdfinfo.
        return PdfLinkAudit(
            available=False,
            skipped_reason=f"pypdf could not read PDF annotations: {exc}",
        )

    for page_number, page in enumerate(reader.pages, 1):
        annotations = page.get("/Annots") or []
        for annotation_ref in annotations:
            annotation = annotation_ref.get_object()
            action = annotation.get("/A") or {}
            uri = action.get("/URI")
            if uri:
                uri_links += 1
                target = str(uri)
                if _forbidden_pdf_target(target):
                    issues.append(PdfLinkIssue(page_number, "forbidden_uri_target", target))
            if action.get("/S") == "/Launch" or action.get("/F"):
                file_actions += 1
                issues.append(PdfLinkIssue(page_number, "file_or_launch_action", str(action)))
    return PdfLinkAudit(
        available=True,
        uri_links=uri_links,
        file_actions=file_actions,
        bad_targets=tuple(issues),
    )


def _split_pages(text: str) -> list[str]:
    pages = text.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    return pages or [text]


def _phrase_hits(pages: list[str], banned_phrases: tuple[str, ...]) -> list[PdfPhraseHit]:
    hits: list[PdfPhraseHit] = []
    for page_number, page_text in enumerate(pages, 1):
        for phrase in banned_phrases:
            pattern = _phrase_pattern(phrase)
            count = len(re.findall(pattern, page_text, flags=re.IGNORECASE))
            if count:
                hits.append(PdfPhraseHit(phrase=phrase, page=page_number, count=count))
    return hits


def _phrase_pattern(phrase: str) -> str:
    escaped = re.escape(phrase)
    if re.fullmatch(r"[A-Za-z0-9_]+", phrase):
        return rf"\b{escaped}\b"
    return escaped


def _page_count(metadata: dict[str, str], fallback: int) -> int:
    raw = metadata.get("Pages", "")
    return int(raw) if raw.isdigit() else fallback


def _forbidden_pdf_target(target: str) -> bool:
    lowered = target.lower()
    return lowered.startswith("file:") or ".md" in lowered or ".markdown" in lowered


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
    from markdown_cell import plain_table_cell

    return plain_table_cell(value)


__all__ = [
    "DEFAULT_BANNED_PHRASES",
    "PdfLinkAudit",
    "PdfLinkIssue",
    "PdfPhraseHit",
    "PdfQualityReport",
    "audit_pdf_links",
    "audit_pdf_quality",
    "extract_pdf_text",
    "pdf_metadata",
    "render_pdf_quality_markdown",
    "report_json",
]
