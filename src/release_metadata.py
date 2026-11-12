"""Read-only release metadata alignment and version-derived task prerequisites.

These checks establish local source consistency, never the existence of a tag,
SDK release, DOI, or permission to publish.
"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import tomllib
from typing import Any

import yaml

STABLE_VERSION_RE = re.compile(r"(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)\.(?:0|[1-9][0-9]*)")
TEMPLATE_PLATFORM_VERSION = "5.2.0"


@dataclass(frozen=True)
class ReleaseMetadataReport:
    """Source-owned metadata evidence, independent of artifact acceptance."""

    payload: dict[str, Any]

    @property
    def ok(self) -> bool:
        return self.payload["ok"] is True


def _stable_version(value: object) -> bool:
    return isinstance(value, str) and STABLE_VERSION_RE.fullmatch(value) is not None


def _read_mapping(root: Path, relative: str, issues: list[str]) -> dict[str, Any]:
    try:
        text = (root / relative).read_text(encoding="utf-8")
        payload = tomllib.loads(text) if relative.endswith(".toml") else yaml.safe_load(text)
    except (OSError, UnicodeError, ValueError, yaml.YAMLError):
        issues.append(f"{relative}: missing or invalid source metadata")
        return {}
    if not isinstance(payload, dict):
        issues.append(f"{relative}: expected a mapping")
        return {}
    return payload


def _field(payload: dict[str, Any], *keys: str) -> str | None:
    value: Any = payload
    for key in keys:
        if not isinstance(value, dict):
            return None
        value = value.get(key)
    return value if isinstance(value, str) else None


def collect_release_metadata(project_root: Path, *, expected_tag: str | None = None) -> ReleaseMetadataReport:
    """Compare source versions and SDK binding; do not contact any registry."""
    root = Path(project_root)
    issues: list[str] = []
    package = _read_mapping(root, "pyproject.toml", issues)
    citation = _read_mapping(root, "CITATION.cff", issues)
    manuscript = _read_mapping(root, "docs/manuscript/config.yaml", issues)
    versions = {
        "package": _field(package, "project", "version"),
        "citation": _field(citation, "version"),
        "paper": _field(manuscript, "paper", "version"),
        "book": _field(manuscript, "book", "edition"),
    }
    version = versions["package"]
    valid = _stable_version(version)
    tag = f"v{version}" if valid else None
    platform_version = _field(package, "tool", "template", "platform_version")
    checks = {
        "canonical_version_valid": valid,
        "versions_match": valid and all(isinstance(value, str) and value == version for value in versions.values()),
        "template_platform_version_ok": platform_version == TEMPLATE_PLATFORM_VERSION,
        "expected_tag_matches": valid and (expected_tag is None or expected_tag == tag),
    }
    if not checks["canonical_version_valid"]:
        issues.append("pyproject.toml: project.version must be a stable X.Y.Z string")
    for name, value in versions.items():
        if not valid or not isinstance(value, str) or value != version:
            issues.append(f"{name}: release version is missing, invalid, or differs from project.version")
    if not checks["template_platform_version_ok"]:
        issues.append(f"pyproject.toml: tool.template.platform_version must be {TEMPLATE_PLATFORM_VERSION}")
    if not checks["expected_tag_matches"]:
        issues.append("expected tag must be exactly v followed by the canonical stable X.Y.Z version")
    return ReleaseMetadataReport({
        "project": "AGEINT", "schema_version": "1.0", "ok": not issues and all(checks.values()),
        "version": version if valid else None, "tag": tag, "expected_tag": expected_tag,
        "template_platform_version": platform_version, "versions": versions,
        "checks": checks, "issue_count": len(issues), "issues": issues,
    })


def collect_release_task_status(project_root: Path, *, version: str | None) -> dict[str, Any]:
    """Require the current version's milestone and only its declared done deps.

    A done milestone is re-checkable evidence of an existing artifact, not
    authorization for another publication. No historical task IDs are implied.
    """
    issues: list[str] = []
    milestone_id = "ageint-release-" + version.replace(".", "-") if _stable_version(version) else None
    if milestone_id is None:
        issues.append("current release version is unknown or invalid")
    payload = _read_mapping(Path(project_root), "tasks.yaml", issues)
    tasks = payload.get("tasks")
    by_id: dict[str, dict[str, Any]] = {}
    board_valid = isinstance(tasks, list) and bool(tasks)
    if not board_valid:
        issues.append("tasks.yaml: tasks must be a nonempty list")
    else:
        for row in tasks:
            task_id = row.get("id") if isinstance(row, dict) else None
            if not isinstance(task_id, str) or not task_id or task_id in by_id:
                board_valid = False
                issues.append("tasks.yaml: task IDs must be unique nonempty strings")
                continue
            by_id[task_id] = row
    milestone = by_id.get(milestone_id, {})
    status = _field(milestone, "status") or "missing"
    deps = milestone.get("deps")
    deps_valid = (
        isinstance(deps, list) and bool(deps)
        and all(isinstance(dep, str) and bool(dep) and dep != milestone_id for dep in deps)
        and len(set(deps)) == len(deps)
    )
    milestone_valid = board_valid and milestone_id is not None and milestone.get("milestone") is True and deps_valid
    milestone_ready = milestone_valid and status in ("todo", "in_progress", "done")
    if not milestone_ready:
        issues.append("current-version release milestone must exist with milestone: true, a ready status, and explicit nonempty unique deps")
    required = {dep: _field(by_id.get(dep, {}), "status") or "missing" for dep in deps} if deps_valid else {}
    prerequisites_done = bool(milestone_valid and required and all(value == "done" for value in required.values()))
    if not prerequisites_done:
        issues.append("every declared release dependency must exist and have status done")
    return {
        "version": version if _stable_version(version) else None,
        "release_milestone_id": milestone_id, "release_milestone_status": status,
        "required_done_tasks": required, "prerequisites_done": prerequisites_done,
        "release_milestone_ready": bool(milestone_ready), "issue_count": len(issues), "issues": issues,
    }


def render_release_metadata_markdown(report: ReleaseMetadataReport) -> str:
    """Render metadata failures without implying artifact acceptance."""
    payload = report.payload
    lines = ["# AGEINT Release Metadata", "", f"OK: {str(report.ok).lower()}",
             f"Version: {payload['version']}", f"Tag: {payload['tag']}", "",
             "| Check | Pass |", "|---|---:|"]
    lines.extend(f"| {name} | {str(passed).lower()} |" for name, passed in payload["checks"].items())
    if payload["issues"]:
        lines.extend(["", "## Issues", "", *(f"- {issue}" for issue in payload["issues"])])
    lines.extend(["", "Metadata alignment is not artifact acceptance or publication authorization."])
    return "\n".join(lines) + "\n"


__all__ = ["ReleaseMetadataReport", "collect_release_metadata", "collect_release_task_status", "render_release_metadata_markdown"]
