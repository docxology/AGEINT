"""Tests for AGEINT publication-readiness preflight."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest
import yaml

from audit_contracts import publication_readiness_audit_check_ids
import publication_readiness as publication_readiness_module
from publication_readiness import (
    artifact_manifest_status,
    collect_publication_readiness,
    collect_source_license_posture,
    collect_task_status,
    render_publication_readiness_markdown,
    scan_release_surfaces,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _green_artifact_checks() -> dict[str, bool]:
    return {check_id: True for check_id in publication_readiness_audit_check_ids()}


def test_publication_readiness_current_outputs_are_green_when_release_inputs_are_clean() -> None:
    if not (PROJECT_ROOT / "output" / "pdf" / "AGEINT_combined.pdf").is_file():
        pytest.skip("Rendered combined PDF not present")
    if not (PROJECT_ROOT / "output" / "reports" / "artifact_manifest.json").is_file():
        pytest.skip("Artifact manifest not present")

    report = collect_publication_readiness(PROJECT_ROOT, run_parent_guard=False)
    payload = report.payload

    assert payload["project"] == "AGEINT"
    assert set(payload["checks"]) >= {
        "artifact_evidence_ok",
        "agency_source_coverage_ok",
        "reference_quality_ok",
        "source_refresh_due_ok",
        "artifact_manifest_ok",
        "release_surface_scan_ok",
        "source_license_posture_ok",
        "task_prerequisites_done",
        "release_milestone_still_todo",
        "parent_confidentiality_guard_ok",
    }
    assert payload["source_refresh_due"]["summary"]["due_or_stale_count"] == 0
    assert payload["artifact_evidence"]["summary"]["reference_quality_issues"] == 0
    assert payload["release_surface_scan"]["issue_count"] == 0
    assert payload["source_license_posture"]["ok"] is True
    assert payload["task_status"]["ageint_m1_status"] == "todo"
    assert "does not publish" in payload["release_decision"]

    markdown = render_publication_readiness_markdown(report)
    assert "Publication Readiness" in markdown
    assert "Release Decision" in markdown


def test_release_surface_scan_flags_private_paths_and_markdown_links(tmp_path: Path) -> None:
    _write(
        tmp_path / "output" / "manuscript" / "chapter.md",
        "# Chapter\n\nSee [local](notes.md) and /Users/4d/private-note.\n",
    )
    _write(
        tmp_path / "output" / "reports" / "current_artifact_evidence.json",
        '{"pdf": {"pdf_path": "/Users/4d/private/AGEINT_combined.pdf"}}\n',
    )
    _write(
        tmp_path / "output" / "reports" / "output_statistics.txt",
        "Output Directory: projects/working/AGEINT/output\n",
    )

    issues = scan_release_surfaces(tmp_path)
    issue_names = {issue.issue for issue in issues}

    assert "markdown_file_link" in issue_names
    assert "absolute_user_path" in issue_names
    assert "working_lifecycle_path" in issue_names


def test_source_license_posture_flags_private_figure_provenance(tmp_path: Path) -> None:
    _write(
        tmp_path / "manuscript" / "config.yaml",
        yaml.safe_dump(
            {
                "book": {"license": "CC BY 4.0", "code_license": "Apache-2.0"},
                "metadata": {"license": "CC-BY-4.0"},
            }
        ),
    )
    _write(
        tmp_path / "output" / "figures" / "figure_registry.json",
        json.dumps(
            {
                "figures": [
                    {
                        "label": "fig:fixture",
                        "kind": "mermaid",
                        "provenance": {"source": "/Users/4d/Downloads/private.md"},
                    }
                ]
            }
        ),
    )
    _write(
        tmp_path / "output" / "reports" / "source_metadata.json",
        json.dumps({"summary": {"blank_source_lane_count": 0, "blank_source_tier_count": 0}}),
    )

    posture = collect_source_license_posture(tmp_path)

    assert posture["ok"] is False
    assert posture["issues"][0]["issue"] == "private_path_in_figure_provenance"


def test_task_status_requires_preflight_prerequisites_but_keeps_release_milestone_open(tmp_path: Path) -> None:
    _write(
        tmp_path / "tasks.yaml",
        yaml.safe_dump(
            {
                "tasks": [
                    {"id": "ageint-25", "status": "done"},
                    {"id": "ageint-26", "status": "todo"},
                    {"id": "ageint-31", "status": "done"},
                    {"id": "ageint-m1", "status": "todo"},
                ]
            }
        ),
    )

    status = collect_task_status(tmp_path)

    assert status["prerequisites_done"] is False
    assert status["required_done_tasks"]["ageint-26"] == "todo"
    assert status["release_milestone_still_todo"] is True


def test_artifact_manifest_status_fails_on_missing_declared_output_issue(tmp_path: Path) -> None:
    _write(
        tmp_path / "output" / "reports" / "artifact_manifest.json",
        json.dumps({"entries": [], "issues": ["missing declared output: projects/AGEINT/output"]}),
    )

    status = artifact_manifest_status(tmp_path)

    assert status["ok"] is False
    assert status["issue_count"] == 1


def test_publication_readiness_collects_green_fixture_without_pdf(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class DummyReport:
        def __init__(self, payload: dict[str, object]) -> None:
            self.payload = payload

    artifact_payload = {
        "ok": True,
        "citations": {
            "generated_markdown_files": 3,
            "generated_markdown_citation_occurrences": 12,
        },
        "figures": {"figure_count": 2},
        "pdf": {
            "page_count": 9,
            "stale_pdf": False,
            "link_audit": {"bad_target_count": 0},
        },
        "claim_calibration": {"summary": {"hard_fail_rows": 0}},
        "scholarship_quality": {"hard_fail_rows": []},
        "checks": _green_artifact_checks(),
        "reference_quality": {
            "summary": {
                "issue_count": 0,
                "generic_heading_issues": 0,
                "citation_context_issues": 0,
            }
        },
    }
    refresh_payload = {
        "ok": True,
        "summary": {"due_or_stale_count": 0},
        "issue_row_count": 0,
    }
    monkeypatch.setattr(
        publication_readiness_module,
        "collect_artifact_evidence",
        lambda _root: DummyReport(artifact_payload),
    )
    monkeypatch.setattr(
        publication_readiness_module,
        "collect_source_refresh_due",
        lambda _root: DummyReport(refresh_payload),
    )

    _write(
        tmp_path / "tasks.yaml",
        yaml.safe_dump(
            {
                "tasks": [
                    {"id": "ageint-25", "status": "done"},
                    {"id": "ageint-26", "status": "done"},
                    {"id": "ageint-31", "status": "done"},
                    {"id": "ageint-m1", "status": "todo"},
                ]
            }
        ),
    )
    _write(
        tmp_path / "manuscript" / "config.yaml",
        yaml.safe_dump({"book": {"license": "CC BY 4.0", "code_license": "Apache-2.0"}}),
    )
    _write(
        tmp_path / "output" / "figures" / "figure_registry.json",
        json.dumps({"figures": [{"label": "fig:fixture", "kind": "mermaid", "provenance": {"source": "fixture"}}]}),
    )
    _write(
        tmp_path / "output" / "reports" / "source_metadata.json",
        json.dumps({"summary": {"blank_source_lane_count": 0, "blank_source_tier_count": 0}}),
    )
    _write(tmp_path / "output" / "reports" / "artifact_manifest.json", json.dumps({"issues": []}))
    _write(tmp_path / "output" / "manuscript" / "fixture.md", "# Fixture\n\nClean text.\n")

    report = collect_publication_readiness(tmp_path, run_parent_guard=False)
    payload = report.payload

    assert report.ok is True
    assert payload["checks"]["artifact_manifest_ok"] is True
    assert payload["checks"]["task_prerequisites_done"] is True
    assert payload["release_surface_scan"]["issue_count"] == 0

    json_path, md_path, written = publication_readiness_module.write_publication_readiness(
        tmp_path,
        run_parent_guard=False,
    )
    assert written.ok is True
    assert json_path.is_file()
    assert md_path.read_text(encoding="utf-8").startswith("# AGEINT Publication Readiness")


def test_publication_readiness_writer_removes_stale_self_report_before_scan(
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class DummyReport:
        def __init__(self, payload: dict[str, object]) -> None:
            self.payload = payload

    monkeypatch.setattr(
        publication_readiness_module,
        "collect_artifact_evidence",
        lambda _root: DummyReport(
            {
                "ok": True,
                "citations": {
                    "generated_markdown_files": 1,
                    "generated_markdown_citation_occurrences": 1,
                },
                "figures": {"figure_count": 1},
                "pdf": {
                    "page_count": 1,
                    "stale_pdf": False,
                    "link_audit": {"bad_target_count": 0},
                },
                "claim_calibration": {"summary": {"hard_fail_rows": 0}},
                "scholarship_quality": {"hard_fail_rows": []},
                "checks": _green_artifact_checks(),
                "reference_quality": {
                    "summary": {
                        "issue_count": 0,
                        "generic_heading_issues": 0,
                        "citation_context_issues": 0,
                    }
                },
            }
        ),
    )
    monkeypatch.setattr(
        publication_readiness_module,
        "collect_source_refresh_due",
        lambda _root: DummyReport(
            {
                "ok": True,
                "summary": {"due_or_stale_count": 0},
                "issue_row_count": 0,
            }
        ),
    )
    monkeypatch.setattr(
        publication_readiness_module,
        "run_parent_confidentiality_guard",
        lambda *_args, **_kwargs: {
            "checked": True,
            "ok": True,
            "stdout": "ok",
            "stderr": "warning: /Users/4d/private/env",
            "returncode": 0,
        },
    )
    _write(
        tmp_path / "tasks.yaml",
        yaml.safe_dump(
            {
                "tasks": [
                    {"id": "ageint-25", "status": "done"},
                    {"id": "ageint-26", "status": "done"},
                    {"id": "ageint-31", "status": "done"},
                    {"id": "ageint-m1", "status": "todo"},
                ]
            }
        ),
    )
    _write(
        tmp_path / "manuscript" / "config.yaml",
        yaml.safe_dump({"book": {"license": "CC BY 4.0", "code_license": "Apache-2.0"}}),
    )
    _write(
        tmp_path / "output" / "figures" / "figure_registry.json",
        json.dumps({"figures": [{"label": "fig:fixture", "provenance": {"source": "fixture"}}]}),
    )
    _write(
        tmp_path / "output" / "reports" / "source_metadata.json",
        json.dumps({"summary": {"blank_source_lane_count": 0, "blank_source_tier_count": 0}}),
    )
    _write(tmp_path / "output" / "reports" / "artifact_manifest.json", json.dumps({"issues": []}))
    _write(tmp_path / "output" / "manuscript" / "fixture.md", "# Fixture\n\nClean text.\n")
    _write(
        tmp_path / "output" / "reports" / "publication_readiness.json",
        '{"stale": "/Users/4d/private/previous-run"}\n',
    )

    json_path, _md_path, report = publication_readiness_module.write_publication_readiness(tmp_path)

    payload = json.loads(json_path.read_text(encoding="utf-8"))
    assert report.ok is True
    assert payload["release_surface_scan"]["issue_count"] == 0
    assert "/Users/" not in json_path.read_text(encoding="utf-8")
    assert "<local-path>" in payload["parent_confidentiality_guard"]["stderr"]


def test_clean_output_sanitizes_local_paths() -> None:
    text = publication_readiness_module._clean_output(  # noqa: SLF001 - regression for report sanitizer
        "warning: VIRTUAL_ENV=/Users/4d/Documents/GitHub/projects/working/AGEINT/.venv"
    )

    assert "/Users/" not in text
    assert "<local-path>" in text


def test_parent_confidentiality_guard_reports_missing_template(tmp_path: Path) -> None:
    result = publication_readiness_module.run_parent_confidentiality_guard(
        tmp_path,
        template_root=tmp_path / "missing-template",
    )

    assert result["checked"] is False
    assert result["ok"] is False
    assert result["returncode"] == 1


def test_audit_publication_readiness_script_writes_json_contract() -> None:
    if not (PROJECT_ROOT / "output" / "pdf" / "AGEINT_combined.pdf").is_file():
        pytest.skip("Rendered combined PDF not present")

    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "audit_publication_readiness.py"),
            "--format",
            "json",
            "--write",
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=240,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["checks"]["release_surface_scan_ok"] is True
    assert payload["checks"]["source_license_posture_ok"] is True
    assert payload["checks"]["reference_quality_ok"] is True
    assert (PROJECT_ROOT / "output" / "reports" / "publication_readiness.json").is_file()
    assert (PROJECT_ROOT / "output" / "reports" / "publication_readiness.md").is_file()
