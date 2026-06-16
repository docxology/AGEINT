"""Publication-readiness preflight for AGEINT local release decisions."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
import re
import subprocess
from typing import Any

import yaml

try:
    from .audit_contracts import publication_readiness_audit_check_ids
    from .artifact_evidence import collect_artifact_evidence
    from .source_refresh_due import collect_source_refresh_due
except ImportError:  # pragma: no cover - direct script imports
    from audit_contracts import publication_readiness_audit_check_ids  # type: ignore[no-redef]
    from artifact_evidence import collect_artifact_evidence  # type: ignore[no-redef]
    from source_refresh_due import collect_source_refresh_due  # type: ignore[no-redef]


PRIVATE_TOKEN_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("absolute_user_path", re.compile(r"/Users/")),
    ("codex_private_path", re.compile(r"\.codex")),
    ("agents_private_path", re.compile(r"\.agents")),
    ("claude_private_path", re.compile(r"\.claude")),
    ("private_projects_env", re.compile(r"TEMPLATE_PRIVATE_PROJECTS_ROOT|\.private_projects_root")),
    ("working_lifecycle_path", re.compile(r"projects/working")),
)
LOCAL_PATH_RE = re.compile(r"/Users/[^\s`'\"),;]+")
MARKDOWN_FILE_LINK_RE = re.compile(r"\]\([^)]*\.m(?:d|arkdown)(?:[#)\s]|$)", re.IGNORECASE)
FILE_URI_LINK_RE = re.compile(r"(\]\(\s*file:|href=[\"']file:)", re.IGNORECASE)
REQUIRED_DONE_TASKS = ("ageint-25", "ageint-26", "ageint-31")


@dataclass(frozen=True)
class ReleaseSurfaceIssue:
    """One publication-surface leak or link issue."""

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
class PublicationReadinessReport:
    """Publication-readiness preflight report."""

    payload: dict[str, Any]

    @property
    def ok(self) -> bool:
        return bool(self.payload["ok"])


def collect_publication_readiness(
    project_root: Path,
    *,
    template_root: Path | None = None,
    run_parent_guard: bool = True,
) -> PublicationReadinessReport:
    """Collect local publication-readiness evidence without publishing anything."""

    root = Path(project_root)
    artifact_evidence = collect_artifact_evidence(root).payload
    artifact_checks = artifact_evidence.get("checks", {}) if isinstance(artifact_evidence, dict) else {}
    source_refresh_due = collect_source_refresh_due(root).payload
    manifest_status = artifact_manifest_status(root)
    release_surface = scan_release_surfaces(root)
    source_license = collect_source_license_posture(root)
    task_status = collect_task_status(root)
    parent_guard = run_parent_confidentiality_guard(root, template_root=template_root) if run_parent_guard else {
        "checked": False,
        "ok": True,
        "stdout": "not run in this invocation",
        "stderr": "",
        "returncode": 0,
    }
    parent_guard = _sanitize_parent_guard(parent_guard)
    artifact_audit_checks = {
        check_id: bool(artifact_checks.get(check_id))
        for check_id in publication_readiness_audit_check_ids()
    }
    checks = {
        "artifact_evidence_ok": bool(artifact_evidence.get("ok")),
        **artifact_audit_checks,
        "source_refresh_due_ok": bool(source_refresh_due.get("ok")),
        "artifact_manifest_ok": manifest_status["ok"],
        "release_surface_scan_ok": not release_surface,
        "source_license_posture_ok": source_license["ok"],
        "task_prerequisites_done": task_status["prerequisites_done"],
        "release_milestone_still_todo": task_status["release_milestone_still_todo"],
        "parent_confidentiality_guard_ok": bool(parent_guard["ok"]),
    }
    payload = {
        "project": "AGEINT",
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "ok": all(checks.values()),
        "checks": checks,
        "artifact_evidence": {
            "report_paths": [
                "output/reports/current_artifact_evidence.json",
                "output/reports/current_artifact_evidence.md",
            ],
            "summary": {
                "generated_markdown_files": artifact_evidence["citations"]["generated_markdown_files"],
                "generated_markdown_citation_occurrences": artifact_evidence["citations"][
                    "generated_markdown_citation_occurrences"
                ],
                "figures": artifact_evidence["figures"]["figure_count"],
                "pdf_pages": artifact_evidence["pdf"]["page_count"],
                "pdf_stale": artifact_evidence["pdf"]["stale_pdf"],
                "bad_pdf_link_targets": artifact_evidence["pdf"]["link_audit"]["bad_target_count"],
                "claim_hard_fail_rows": artifact_evidence["claim_calibration"]["summary"]["hard_fail_rows"],
                "scholarship_hard_fail_rows": len(artifact_evidence["scholarship_quality"]["hard_fail_rows"]),
                "agency_source_coverage_ok": bool(
                    artifact_checks.get("agency_source_coverage_ok", True)
                ),
                "new_official_us_ic_anchors": artifact_evidence.get("agency_source_coverage", {})
                .get("summary", {})
                .get("new_official_us_ic_anchor_count", 0),
                "agency_source_unrouted_rows": artifact_evidence.get("agency_source_coverage", {})
                .get("summary", {})
                .get("unrouted_new_anchor_count", 0),
                "agency_source_missing_metadata": artifact_evidence.get("agency_source_coverage", {})
                .get("summary", {})
                .get("missing_required_metadata_count", 0),
                "reference_quality_issues": artifact_evidence.get("reference_quality", {})
                .get("summary", {})
                .get("issue_count", 0),
                "generic_detail_heading_issues": artifact_evidence.get("reference_quality", {})
                .get("summary", {})
                .get("generic_heading_issues", 0),
                "citation_context_issues": artifact_evidence.get("reference_quality", {})
                .get("summary", {})
                .get("citation_context_issues", 0),
            },
        },
        "source_refresh_due": {
            "report_paths": [
                "output/reports/source_refresh_due.json",
                "output/reports/source_refresh_due.md",
            ],
            "summary": source_refresh_due["summary"],
            "issue_row_count": source_refresh_due["issue_row_count"],
        },
        "artifact_manifest": manifest_status,
        "release_surface_scan": {
            "issue_count": len(release_surface),
            "issues": [issue.as_dict() for issue in release_surface],
        },
        "source_license_posture": source_license,
        "task_status": task_status,
        "parent_confidentiality_guard": parent_guard,
        "release_decision": (
            "Ready for an explicit local release decision only when this report is ok. "
            "This report does not publish, push, archive, promote, or create a public record."
        ),
    }
    return PublicationReadinessReport(payload)


def write_publication_readiness(
    project_root: Path,
    *,
    run_parent_guard: bool = True,
) -> tuple[Path, Path, PublicationReadinessReport]:
    """Write JSON and Markdown publication-readiness reports under ``output/reports``."""

    root = Path(project_root)
    reports_dir = root / "output" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_path = reports_dir / "publication_readiness.json"
    md_path = reports_dir / "publication_readiness.md"
    for stale_path in (json_path, md_path):
        stale_path.unlink(missing_ok=True)
    report = collect_publication_readiness(root, run_parent_guard=run_parent_guard)
    json_path.write_text(json.dumps(report.payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_publication_readiness_markdown(report), encoding="utf-8")
    return json_path, md_path, report


def render_publication_readiness_markdown(report: PublicationReadinessReport) -> str:
    """Render a compact Markdown publication-readiness report."""

    payload = report.payload
    checks = payload["checks"]
    artifact = payload["artifact_evidence"]["summary"]
    refresh = payload["source_refresh_due"]["summary"]
    lines = [
        "# AGEINT Publication Readiness",
        "",
        "| Measure | Value |",
        "|---|---:|",
        f"| OK | {str(payload['ok']).lower()} |",
        f"| Generated at | {payload['generated_at']} |",
        f"| Generated Markdown files | {artifact['generated_markdown_files']} |",
        f"| Generated citation occurrences | {artifact['generated_markdown_citation_occurrences']} |",
        f"| Registered figures | {artifact['figures']} |",
        f"| PDF pages | {artifact['pdf_pages']} |",
        f"| Bad PDF link targets | {artifact['bad_pdf_link_targets']} |",
        f"| Claim hard-fail rows | {artifact['claim_hard_fail_rows']} |",
        f"| Scholarship hard-fail rows | {artifact['scholarship_hard_fail_rows']} |",
        f"| New official US IC anchors | {artifact['new_official_us_ic_anchors']} |",
        f"| Agency-source unrouted rows | {artifact['agency_source_unrouted_rows']} |",
        f"| Agency-source missing metadata | {artifact['agency_source_missing_metadata']} |",
        f"| Reference-quality issues | {artifact['reference_quality_issues']} |",
        f"| Generic detail-heading issues | {artifact['generic_detail_heading_issues']} |",
        f"| Citation-context issues | {artifact['citation_context_issues']} |",
        f"| Source refresh due/stale rows | {refresh['due_or_stale_count']} |",
        f"| Release-surface issues | {payload['release_surface_scan']['issue_count']} |",
        f"| Artifact-manifest issues | {payload['artifact_manifest']['issue_count']} |",
        "",
        "## Checks",
        "",
        "| Check | Pass |",
        "|---|---:|",
    ]
    for name, passed in checks.items():
        lines.append(f"| {name.replace('_', ' ')} | {str(passed).lower()} |")
    lines.extend(
        [
            "",
            "## Blocking Issues",
            "",
            "| Surface | Count |",
            "|---|---:|",
            f"| Release surface scan | {payload['release_surface_scan']['issue_count']} |",
            f"| Source/license posture | {payload['source_license_posture']['issue_count']} |",
            f"| Artifact manifest | {payload['artifact_manifest']['issue_count']} |",
            "",
            "## Release Decision",
            "",
            payload["release_decision"],
        ]
    )
    return "\n".join(lines) + "\n"


def scan_release_surfaces(project_root: Path) -> tuple[ReleaseSurfaceIssue, ...]:
    """Scan public-release input surfaces for private paths and PDF-bound Markdown links."""

    root = Path(project_root)
    issues: list[ReleaseSurfaceIssue] = []
    for path in _release_text_paths(root):
        text = path.read_text(encoding="utf-8", errors="ignore")
        relative = path.relative_to(root).as_posix()
        for line_number, line in enumerate(text.splitlines(), 1):
            for issue_name, pattern in PRIVATE_TOKEN_PATTERNS:
                if pattern.search(line):
                    issues.append(_issue(relative, line_number, issue_name, line))
            if _is_pdf_bound_text(path, root) and MARKDOWN_FILE_LINK_RE.search(line):
                issues.append(_issue(relative, line_number, "markdown_file_link", line))
            if FILE_URI_LINK_RE.search(line):
                issues.append(_issue(relative, line_number, "file_uri_link", line))
    return tuple(issues)


def collect_source_license_posture(project_root: Path) -> dict[str, Any]:
    """Check source, license, and figure provenance posture for release inputs."""

    root = Path(project_root)
    issues: list[dict[str, str]] = []
    config = _load_yaml(root / "manuscript" / "config.yaml")
    book = config.get("book", {}) if isinstance(config, dict) else {}
    metadata = config.get("metadata", {}) if isinstance(config, dict) else {}
    if not book.get("license") and not metadata.get("license"):
        issues.append({"surface": "manuscript/config.yaml", "issue": "missing_publication_license"})
    if not book.get("code_license"):
        issues.append({"surface": "manuscript/config.yaml", "issue": "missing_code_license"})

    registry_path = root / "output" / "figures" / "figure_registry.json"
    registry = _load_json(registry_path)
    figures = registry.get("figures", []) if isinstance(registry, dict) else []
    if not figures:
        issues.append({"surface": "output/figures/figure_registry.json", "issue": "missing_figure_registry"})
    for row in figures:
        if not isinstance(row, dict):
            continue
        label = str(row.get("label") or "<unknown>")
        provenance = row.get("provenance") if isinstance(row.get("provenance"), dict) else {}
        provenance_text = json.dumps(provenance, sort_keys=True)
        if not provenance:
            issues.append({"surface": label, "issue": "missing_figure_provenance"})
        if "/Users/" in provenance_text or ".codex" in provenance_text or ".agents" in provenance_text:
            issues.append({"surface": label, "issue": "private_path_in_figure_provenance"})
        if row.get("kind") == "historical" and provenance.get("usage") != "Public Domain":
            issues.append({"surface": label, "issue": "historical_asset_not_public_domain"})
        if row.get("kind") == "ai_generated" and "synthetic" not in str(provenance.get("safety", "")).lower():
            issues.append({"surface": label, "issue": "synthetic_asset_missing_safety_provenance"})

    source_metadata = _load_json(root / "output" / "reports" / "source_metadata.json")
    metadata_summary = source_metadata.get("summary", {}) if isinstance(source_metadata, dict) else {}
    if metadata_summary.get("blank_source_lane_count") != 0 or metadata_summary.get("blank_source_tier_count") != 0:
        issues.append({"surface": "output/reports/source_metadata.json", "issue": "source_metadata_not_explicit"})
    return {
        "ok": not issues,
        "issue_count": len(issues),
        "issues": issues,
        "license": {
            "book": book.get("license", ""),
            "code": book.get("code_license", ""),
            "metadata": metadata.get("license", ""),
        },
        "figure_count": len(figures),
    }


def artifact_manifest_status(project_root: Path) -> dict[str, Any]:
    path = Path(project_root) / "output" / "reports" / "artifact_manifest.json"
    if not path.is_file():
        return {
            "ok": False,
            "path": "output/reports/artifact_manifest.json",
            "issue_count": 1,
            "issues": ["missing artifact manifest"],
        }
    payload = _load_json(path)
    issues = [str(issue) for issue in payload.get("issues", [])] if isinstance(payload, dict) else ["invalid manifest"]
    return {
        "ok": not issues,
        "path": "output/reports/artifact_manifest.json",
        "issue_count": len(issues),
        "issues": issues,
    }


def collect_task_status(project_root: Path) -> dict[str, Any]:
    payload = _load_yaml(Path(project_root) / "tasks.yaml")
    tasks = payload.get("tasks", []) if isinstance(payload, dict) else []
    by_id = {str(row.get("id")): row for row in tasks if isinstance(row, dict)}
    required = {
        task_id: str(by_id.get(task_id, {}).get("status", "missing"))
        for task_id in REQUIRED_DONE_TASKS
    }
    milestone_status = str(by_id.get("ageint-m1", {}).get("status", "missing"))
    return {
        "required_done_tasks": required,
        "prerequisites_done": all(status == "done" for status in required.values()),
        "ageint_27_status": str(by_id.get("ageint-27", {}).get("status", "missing")),
        "ageint_m1_status": milestone_status,
        "release_milestone_still_todo": milestone_status == "todo",
    }


def run_parent_confidentiality_guard(
    project_root: Path,
    *,
    template_root: Path | None = None,
) -> dict[str, Any]:
    template = template_root or _default_template_root(project_root)
    if not template or not template.is_dir():
        return {
            "checked": False,
            "ok": False,
            "stdout": "",
            "stderr": "template repo not found",
            "returncode": 1,
        }
    result = subprocess.run(
        ["uv", "run", "python", "scripts/check_tracked_projects.py"],
        cwd=template,
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )
    return {
        "checked": True,
        "ok": result.returncode == 0,
        "stdout": _clean_output(result.stdout),
        "stderr": _clean_output(result.stderr),
        "returncode": result.returncode,
    }


def _release_text_paths(root: Path) -> tuple[Path, ...]:
    paths: list[Path] = []
    roots = [
        root / "output" / "manuscript",
        root / "output" / "web",
        root / "output" / "pdf",
    ]
    for base in roots:
        if base.is_dir():
            paths.extend(
                path
                for path in base.rglob("*")
                if path.is_file() and path.suffix.lower() in {".md", ".tex", ".html", ".yaml", ".yml", ".bib"}
            )
    reports_dir = root / "output" / "reports"
    if reports_dir.is_dir():
        paths.extend(
            path
            for path in reports_dir.rglob("*")
            if path.is_file() and path.suffix.lower() in {".json", ".jsonl", ".md", ".txt", ".html"}
        )
    explicit = [
        root / "output" / "figures" / "figure_registry.json",
        root / "output" / "figures" / "visual_quality_audit.json",
        root / "output" / "figures" / "cover" / "ageint-cover-synthesis.json",
    ]
    paths.extend(path for path in explicit if path.is_file())
    return tuple(sorted(set(paths)))


def _is_pdf_bound_text(path: Path, root: Path) -> bool:
    try:
        rel = path.relative_to(root).as_posix()
    except ValueError:
        rel = path.as_posix()
    return rel.startswith("output/manuscript/") or rel.startswith("output/pdf/")


def _issue(path: str, line: int, issue: str, text: str) -> ReleaseSurfaceIssue:
    return ReleaseSurfaceIssue(path=path, line=line, issue=issue, snippet=" ".join(text.split())[:220])


def _load_json(path: Path) -> dict[str, Any]:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _load_yaml(path: Path) -> dict[str, Any]:
    try:
        payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    except OSError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _default_template_root(project_root: Path) -> Path | None:
    docs_root = Path(project_root).resolve().parents[2]
    candidate = docs_root / "template"
    return candidate if candidate.is_dir() else None


def _clean_output(value: str) -> str:
    return LOCAL_PATH_RE.sub("<local-path>", " ".join(value.split()))[:500]


def _sanitize_parent_guard(parent_guard: dict[str, Any]) -> dict[str, Any]:
    sanitized = dict(parent_guard)
    sanitized["stdout"] = _clean_output(str(sanitized.get("stdout", "")))
    sanitized["stderr"] = _clean_output(str(sanitized.get("stderr", "")))
    return sanitized


__all__ = [
    "MARKDOWN_FILE_LINK_RE",
    "PRIVATE_TOKEN_PATTERNS",
    "PublicationReadinessReport",
    "ReleaseSurfaceIssue",
    "artifact_manifest_status",
    "collect_publication_readiness",
    "collect_source_license_posture",
    "collect_task_status",
    "render_publication_readiness_markdown",
    "run_parent_confidentiality_guard",
    "scan_release_surfaces",
    "write_publication_readiness",
]
