"""Source metadata and version-derived release task contracts."""
from __future__ import annotations

import json
from pathlib import Path
import subprocess
import sys

import pytest
import yaml

from release_metadata import collect_release_metadata, collect_release_task_status

PROJECT_ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def release_project(tmp_path: Path) -> Path:
    (tmp_path / "docs" / "manuscript").mkdir(parents=True)
    (tmp_path / "pyproject.toml").write_text(
        '[project]\nname = "ageint"\nversion = "0.2.0"\n'
        '[tool.template]\nplatform_version = "5.1.0"\n', encoding="utf-8",
    )
    (tmp_path / "CITATION.cff").write_text('version: "0.2.0"\n', encoding="utf-8")
    (tmp_path / "docs" / "manuscript" / "config.yaml").write_text(
        yaml.safe_dump({"paper": {"version": "0.2.0"}, "book": {"edition": "0.2.0"}}), encoding="utf-8",
    )
    write_tasks(tmp_path, [{"id": "render", "status": "done"}, {
        "id": "ageint-release-0-2-0", "milestone": True, "status": "todo", "deps": ["render"],
    }])
    return tmp_path


def write_tasks(root: Path, tasks: object) -> None:
    (root / "tasks.yaml").write_text(yaml.safe_dump({"tasks": tasks}), encoding="utf-8")


def test_aligned_metadata_is_read_only(release_project: Path) -> None:
    before = {path: path.read_bytes() for path in release_project.rglob("*") if path.is_file()}
    report = collect_release_metadata(release_project, expected_tag="v0.2.0")
    assert report.ok is True
    assert report.payload["version"] == "0.2.0"
    assert report.payload["tag"] == "v0.2.0"
    assert all(report.payload["checks"].values())
    assert before == {path: path.read_bytes() for path in release_project.rglob("*") if path.is_file()}


@pytest.mark.parametrize("surface", ["package", "cff", "paper", "book"])
def test_every_version_must_match(release_project: Path, surface: str) -> None:
    if surface == "package":
        path = release_project / "pyproject.toml"
        path.write_text(path.read_text().replace('version = "0.2.0"', 'version = "0.3.0"'), encoding="utf-8")
    elif surface == "cff":
        (release_project / "CITATION.cff").write_text('version: "0.1.0"\n', encoding="utf-8")
    else:
        path = release_project / "docs" / "manuscript" / "config.yaml"
        config = yaml.safe_load(path.read_text())
        config["paper" if surface == "paper" else "book"]["version" if surface == "paper" else "edition"] = "0.1.0"
        path.write_text(yaml.safe_dump(config), encoding="utf-8")
    assert collect_release_metadata(release_project).ok is False


@pytest.mark.parametrize("tag", ["v0.1.0", "0.2.0", "AGEINT-v0.2.0", "v0.2.0rc1", "v0.2.0+local", "v00.2.0", "v0.2.0\n", ""])
def test_expected_tag_rejects_foreign_malformed_and_wrong_versions(release_project: Path, tag: str) -> None:
    report = collect_release_metadata(release_project, expected_tag=tag)
    assert report.ok is False
    assert report.payload["checks"]["expected_tag_matches"] is False


@pytest.mark.parametrize("version", ["0.2", "0.2.0rc1", "00.2.0", "", 0.2, None])
def test_canonical_version_requires_stable_semver(release_project: Path, version: object) -> None:
    path = release_project / "pyproject.toml"
    text = path.read_text().replace('version = "0.2.0"', f'version = {json.dumps(version)}')
    path.write_text(text, encoding="utf-8")
    assert collect_release_metadata(release_project).ok is False


@pytest.mark.parametrize("surface", ["pyproject.toml", "CITATION.cff", "docs/manuscript/config.yaml"])
def test_missing_or_malformed_metadata_fails_closed(release_project: Path, surface: str) -> None:
    path = release_project / surface
    path.unlink()
    assert collect_release_metadata(release_project).ok is False
    path.write_text("[not: valid", encoding="utf-8")
    assert collect_release_metadata(release_project).ok is False


def test_sdk_binding_must_match_release_train(release_project: Path) -> None:
    path = release_project / "pyproject.toml"
    path.write_text(path.read_text().replace('"5.1.0"', '"main"'), encoding="utf-8")
    assert collect_release_metadata(release_project).ok is False


@pytest.mark.parametrize("status", ["todo", "in_progress", "done"])
def test_current_milestone_remains_recheckable(release_project: Path, status: str) -> None:
    write_tasks(release_project, [{"id": "render", "status": "done"}, {
        "id": "ageint-release-0-2-0", "milestone": True, "status": status, "deps": ["render"],
    }, {"id": "unrelated", "status": "blocked"}])
    result = collect_release_task_status(release_project, version="0.2.0")
    assert result["release_milestone_ready"] is True
    assert result["prerequisites_done"] is True
    assert result["required_done_tasks"] == {"render": "done"}


@pytest.mark.parametrize("change", [
    {"id": "ageint-m1"}, {"id": "ageint-release-0-1-0"}, {"status": "blocked"},
    {"status": "unknown"}, {"milestone": False}, {"milestone": "true"},
    {"deps": []}, {"deps": None}, {"deps": "render"}, {"deps": ["missing"]},
    {"deps": ["render", "render"]}, {"deps": ["ageint-release-0-2-0"]}, {"deps": [None]},
])
def test_invalid_milestone_cannot_pass(release_project: Path, change: dict[str, object]) -> None:
    milestone = {"id": "ageint-release-0-2-0", "milestone": True, "status": "todo", "deps": ["render"], **change}
    write_tasks(release_project, [{"id": "render", "status": "done"}, milestone])
    result = collect_release_task_status(release_project, version="0.2.0")
    assert not (result["release_milestone_ready"] and result["prerequisites_done"])
    assert result["issues"]


@pytest.mark.parametrize("status", ["todo", "in_progress", "blocked", "missing"])
def test_only_done_declared_dependencies_satisfy_prerequisites(release_project: Path, status: str) -> None:
    write_tasks(release_project, [{"id": "render", "status": status}, {
        "id": "ageint-release-0-2-0", "milestone": True, "status": "done", "deps": ["render"],
    }])
    result = collect_release_task_status(release_project, version="0.2.0")
    assert result["prerequisites_done"] is False
    assert result["required_done_tasks"] == {"render": status}


@pytest.mark.parametrize("tasks", [None, {}, [], [{"id": "x"}, {"id": "x"}], [None]])
def test_unknown_taskboards_fail_closed(release_project: Path, tasks: object) -> None:
    write_tasks(release_project, tasks)
    result = collect_release_task_status(release_project, version="0.2.0")
    assert result["release_milestone_ready"] is False
    assert result["prerequisites_done"] is False


def test_release_task_id_is_derived_from_any_stable_current_version(release_project: Path) -> None:
    write_tasks(release_project, [{"id": "render", "status": "done"}, {
        "id": "ageint-release-1-12-3", "milestone": True, "status": "done", "deps": ["render"],
    }])
    current = collect_release_task_status(release_project, version="1.12.3")
    assert current["release_milestone_id"] == "ageint-release-1-12-3"
    assert current["release_milestone_ready"] is True
    assert current["prerequisites_done"] is True
    assert collect_release_task_status(release_project, version="0.2.0")["release_milestone_ready"] is False


def test_milestone_without_declared_deps_cannot_pass(release_project: Path) -> None:
    write_tasks(release_project, [{"id": "ageint-release-0-2-0", "milestone": True, "status": "done"}])
    result = collect_release_task_status(release_project, version="0.2.0")
    assert result["release_milestone_ready"] is False
    assert result["prerequisites_done"] is False


def test_missing_and_malformed_taskboards_fail_closed(release_project: Path) -> None:
    path = release_project / "tasks.yaml"
    path.unlink()
    assert collect_release_task_status(release_project, version="0.2.0")["prerequisites_done"] is False
    path.write_text("tasks: [invalid", encoding="utf-8")
    assert collect_release_task_status(release_project, version="0.2.0")["release_milestone_ready"] is False


def test_cli_rejects_wrong_tag_without_writing() -> None:
    result = subprocess.run(
        [sys.executable, str(PROJECT_ROOT / "scripts" / "audit_release_metadata.py"),
         "--format", "json", "--expected-tag", "v999.0.0"],
        cwd=PROJECT_ROOT, capture_output=True, text=True, check=False, timeout=30,
    )
    assert result.returncode == 1, result.stderr
    report = json.loads(result.stdout)
    assert report["ok"] is False
    assert report["checks"]["expected_tag_matches"] is False
