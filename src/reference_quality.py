"""Reader-facing reference, heading, and citation-context quality audit."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
import re
from typing import Any, Iterable

try:
    from .rendered_reference_audit import audit_rendered_references
except ImportError:  # pragma: no cover - direct script imports
    from rendered_reference_audit import audit_rendered_references  # type: ignore[no-redef]

MARKDOWN_FILE_LINK_RE = re.compile(r"\]\([^)]*\.m(?:d|arkdown)(?:[#)\s]|$)", re.IGNORECASE)
RAW_LITERAL_CITATION_RE = re.compile(r"`@(?:ageint|official_|scholarly_)[A-Za-z0-9_-]+`")
CITATION_REF_RE = re.compile(r"\[@[^\]]+\]")
CROSS_LINK_LINE_RE = re.compile(r"\*\*(?:Cross-links|Learning-path links)\.\*\*")
GENERIC_DETAIL_HEADING_RE = re.compile(
    r"^#{3,6}\s+("
    r"Textbook primer|"
    r"Learning outcomes|"
    r"Core vocabulary|"
    r"Discipline spine|"
    r"Source-use contract|"
    r"Practice artifact|"
    r"Topic lessons|"
    r"Worked safe example|"
    r"Practice sequence|"
    r"Knowledge check|"
    r"Instructor notes|"
    r"Extension|"
    r"Answer quality rubric|"
    r"Module architecture and transfer contract|"
    r"Evidence canon and source spine|"
    r"Guide source spine|"
    r"Verified source canon|"
    r"Intelligence practice lens|"
    r"Runtime-to-reader map|"
    r"Reusable subsection contract|"
    r"Annotated source ledger|"
    r"Source-backed analytic synthesis|"
    r"Evidence standard and citation floor|"
    r"Agentic translation: assist, approve, block|"
    r"Permitted defensive utility|"
    r"Excluded operational boundary|"
    r"Governance, rights, and assurance|"
    r"Governance card|"
    r"Evidence package handoff|"
    r"Current-source assurance|"
    r"Assessment artifacts and capstone pathway|"
    r"Capstone pathway|"
    r"Instructor facilitation notes|"
    r"Assessment rubric|"
    r"Refresh, safety, and source maps|"
    r"Refresh triggers|"
    r"Claim and evidence ledger|"
    r"Reviewer challenge checklist|"
    r"Learning-path cross-links|"
    r"Cross-links"
    r")\s*$"
)
SUPPORT_NAMES = {"AGENTS.md", "README.md", "references.md"}


@dataclass(frozen=True)
class ReferenceQualityIssue:
    """One reader-facing reference-quality issue."""

    path: str
    line: int
    issue: str
    snippet: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "line": self.line,
            "issue": self.issue,
            "snippet": self.snippet,
        }


@dataclass(frozen=True)
class ReferenceQualityReport:
    """Reference-quality audit snapshot."""

    payload: dict[str, Any]

    @property
    def ok(self) -> bool:
        return bool(self.payload["ok"])


def collect_reference_quality(project_root: Path) -> ReferenceQualityReport:
    """Collect reader-facing reference, heading, and citation-context quality."""

    root = Path(project_root)
    output = root / "output"
    rendered_violations = audit_rendered_references(output)
    issues: list[ReferenceQualityIssue] = []
    for violation in rendered_violations:
        issues.append(
            ReferenceQualityIssue(
                path=_relative(violation.path, root),
                line=violation.line_number,
                issue=f"rendered_reference:{violation.reason.replace(' ', '_')}",
                snippet=violation.line.strip()[:220],
            )
        )
    for path in _pdf_bound_text_paths(root):
        _scan_text_file(path, root, issues)
    summary = {
        "scanned_files": len(_pdf_bound_text_paths(root)),
        "issue_count": len(issues),
        "rendered_reference_issues": sum(
            1 for issue in issues if issue.issue.startswith("rendered_reference:")
        ),
        "markdown_file_link_issues": sum(1 for issue in issues if issue.issue == "markdown_file_link"),
        "raw_literal_citation_issues": sum(1 for issue in issues if issue.issue == "raw_literal_citation_key"),
        "generic_heading_issues": sum(1 for issue in issues if issue.issue == "generic_detail_heading"),
        "cross_link_issues": sum(1 for issue in issues if issue.issue.startswith("incomplete_cross_link")),
        "citation_context_issues": sum(1 for issue in issues if issue.issue == "citation_table_row_without_context"),
    }
    payload = {
        "project": "AGEINT",
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "ok": not issues,
        "summary": summary,
        "issue_rows": [issue.as_dict() for issue in issues],
        "negative_control": (
            "A generated Markdown link to a .md file, an old generic scaffold "
            "heading, a lesson cross-link line without sec/fig refs, or a table "
            "row that contains only citation keys must fail reference_quality_ok."
        ),
    }
    return ReferenceQualityReport(payload)


def write_reference_quality(project_root: Path) -> tuple[Path, Path, ReferenceQualityReport]:
    """Write JSON and Markdown reference-quality reports."""

    root = Path(project_root)
    report = collect_reference_quality(root)
    reports = root / "output" / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    json_path = reports / "reference_quality.json"
    md_path = reports / "reference_quality.md"
    json_path.write_text(json.dumps(report.payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_reference_quality_markdown(report), encoding="utf-8")
    return json_path, md_path, report


def render_reference_quality_markdown(report: ReferenceQualityReport) -> str:
    """Render the reference-quality audit as Markdown."""

    payload = report.payload
    summary = payload["summary"]
    lines = [
        "# AGEINT Reference Quality",
        "",
        "| Measure | Value |",
        "|---|---:|",
        f"| OK | {str(payload['ok']).lower()} |",
        f"| reference_quality_ok | {str(payload['ok']).lower()} |",
        f"| Generated at | {payload['generated_at']} |",
        f"| Scanned files | {summary['scanned_files']} |",
        f"| Issue rows | {summary['issue_count']} |",
        f"| Rendered-reference issues | {summary['rendered_reference_issues']} |",
        f"| Markdown-file link issues | {summary['markdown_file_link_issues']} |",
        f"| Raw literal citation-key issues | {summary['raw_literal_citation_issues']} |",
        f"| Generic detail-heading issues | {summary['generic_heading_issues']} |",
        f"| Cross-link issues | {summary['cross_link_issues']} |",
        f"| Citation-context issues | {summary['citation_context_issues']} |",
        "",
        "## Issue Rows",
        "",
        "| Path | Line | Issue | Snippet |",
        "|---|---:|---|---|",
    ]
    if payload["issue_rows"]:
        for row in payload["issue_rows"][:80]:
            lines.append(
                f"| {_table_cell(row['path'])} | {row['line']} | "
                f"{_table_cell(row['issue'])} | {_table_cell(row['snippet'])} |"
            )
    else:
        lines.append("| None | 0 | - | - |")
    lines.extend(["", "## Negative Control", "", payload["negative_control"]])
    return "\n".join(lines) + "\n"


def _scan_text_file(path: Path, root: Path, issues: list[ReferenceQualityIssue]) -> None:
    text = path.read_text(encoding="utf-8", errors="ignore")
    suffix = path.suffix.lower()
    for line_number, line in enumerate(text.splitlines(), 1):
        if MARKDOWN_FILE_LINK_RE.search(line):
            issues.append(_issue(path, root, line_number, "markdown_file_link", line))
        if RAW_LITERAL_CITATION_RE.search(line):
            issues.append(_issue(path, root, line_number, "raw_literal_citation_key", line))
        if suffix == ".md" and GENERIC_DETAIL_HEADING_RE.match(line.strip()):
            issues.append(_issue(path, root, line_number, "generic_detail_heading", line))
        if CROSS_LINK_LINE_RE.search(line):
            missing = _missing_cross_link_refs(line)
            for item in missing:
                issues.append(_issue(path, root, line_number, f"incomplete_cross_link:{item}", line))
        if suffix == ".md" and _citation_table_row_without_context(line):
            issues.append(_issue(path, root, line_number, "citation_table_row_without_context", line))


def _missing_cross_link_refs(line: str) -> tuple[str, ...]:
    missing: list[str] = []
    if "unit module map" in line.lower() and "[@fig:part-" not in line:
        missing.append("unit_module_map_figure_ref")
    if "module overview" in line.lower() and "[@sec:chapter-" not in line:
        missing.append("module_overview_section_ref")
    if "curriculum atlas" in line.lower() and "[@sec:curriculum_orientation]" not in line:
        missing.append("curriculum_atlas_section_ref")
    return tuple(missing)


def _citation_table_row_without_context(line: str) -> bool:
    stripped = line.strip()
    if not stripped.startswith("|") or not CITATION_REF_RE.search(stripped):
        return False
    cells = [cell.strip() for cell in stripped.strip("|").split("|")]
    if not cells or _is_separator_row(cells):
        return False
    descriptive_cells = [
        cell for cell in cells if _descriptive_cell_text(cell)
    ]
    return not descriptive_cells


def _descriptive_cell_text(cell: str) -> str:
    cleaned = CITATION_REF_RE.sub("", cell)
    cleaned = re.sub(r"[`*_\\[\]():;,.|-]+", " ", cleaned)
    cleaned = " ".join(cleaned.split())
    if len(cleaned) < 12:
        return ""
    return cleaned if re.search(r"[A-Za-z]{4,}", cleaned) else ""


def _is_separator_row(cells: Iterable[str]) -> bool:
    return all(re.fullmatch(r":?-{3,}:?", cell.strip()) for cell in cells if cell.strip())


def _pdf_bound_text_paths(root: Path) -> tuple[Path, ...]:
    paths: list[Path] = []
    manuscript = root / "output" / "manuscript"
    if manuscript.is_dir():
        paths.extend(
            path
            for path in sorted(manuscript.rglob("*.md"))
            if path.name not in SUPPORT_NAMES
        )
    pdf = root / "output" / "pdf"
    for name in ("_combined_manuscript.md", "_combined_manuscript.tex"):
        path = pdf / name
        if path.is_file():
            paths.append(path)
    return tuple(dict.fromkeys(paths))


def _issue(path: Path, root: Path, line: int, issue: str, text: str) -> ReferenceQualityIssue:
    return ReferenceQualityIssue(
        path=_relative(path, root),
        line=line,
        issue=issue,
        snippet=" ".join(text.split())[:220],
    )


def _relative(path: Path, root: Path) -> str:
    try:
        return path.relative_to(root).as_posix()
    except ValueError:
        return path.as_posix()


def _table_cell(value: str) -> str:
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


__all__ = [
    "MARKDOWN_FILE_LINK_RE",
    "RAW_LITERAL_CITATION_RE",
    "ReferenceQualityIssue",
    "ReferenceQualityReport",
    "collect_reference_quality",
    "render_reference_quality_markdown",
    "write_reference_quality",
]
