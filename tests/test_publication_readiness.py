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
    render_publication_readiness_markdown,
    scan_release_surfaces,
)
from release_metadata import collect_release_task_status

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def _green_artifact_checks() -> dict[str, bool]:
    return {check_id: True for check_id in publication_readiness_audit_check_ids()}


def _write_release_metadata(root: Path) -> None:
    _write(root / "pyproject.toml", '[project]\nversion = "0.2.0"\n[tool.template]\nplatform_version = "5.1.0"\n')
    _write(root / "CITATION.cff", 'version: "0.2.0"\n')
    _write(root / "docs" / "manuscript" / "config.yaml", yaml.safe_dump({
        "paper": {"version": "0.2.0"},
        "book": {"edition": "0.2.0", "license": "CC BY 4.0", "code_license": "Apache-2.0"},
    }))


@pytest.fixture
def native_guard_template(tmp_path: Path) -> Path:
    """Run fixture guard programs through the prepared Python subprocess boundary."""
    template = tmp_path / "template"
    _write(template / "pyproject.toml", '[project]\nname = "guard-fixture"\nversion = "0.0.0"\n')
    _write(template / "infrastructure" / "validation" / "cli.py", "")
    (template / "infrastructure" / "rendering").mkdir()
    _write(
        template / "scripts" / "audit" / "check_tracked_all.py",
        "import json\nfrom pathlib import Path\n"
        "print(json.dumps({'cwd': str(Path.cwd()), 'script': str(Path(__file__).resolve())}))\n",
    )
    return template


def test_publication_readiness_current_outputs_are_informational_without_parent_guard() -> None:
    if not (PROJECT_ROOT / "output" / "pdf" / "AGEINT_combined.pdf").is_file():
        pytest.skip("Rendered combined PDF not present")
    if not (PROJECT_ROOT / "output" / "reports" / "artifact_manifest.json").is_file():
        pytest.skip("Artifact manifest not present")

    report = collect_publication_readiness(PROJECT_ROOT, run_parent_guard=False)
    payload = report.payload

    assert payload["project"] == "AGEINT"
    assert payload["schema_version"] == "2.0"
    assert report.ok is False
    assert payload["checks"]["parent_confidentiality_guard_ok"] is False
    assert payload["parent_confidentiality_guard"]["status"] == "skipped"
    assert set(payload["checks"]) >= {
        "artifact_evidence_ok",
        "agency_source_coverage_ok",
        "reference_quality_ok",
        "source_refresh_due_ok",
        "artifact_manifest_ok",
        "release_surface_scan_ok",
        "source_license_posture_ok",
        "task_prerequisites_done",
        "release_milestone_ready",
        "release_metadata_ok",
        "parent_confidentiality_guard_ok",
    }
    assert payload["source_refresh_due"]["summary"]["due_or_stale_count"] == 0
    assert payload["artifact_evidence"]["summary"]["reference_quality_issues"] == 0
    assert payload["release_surface_scan"]["issue_count"] == 0
    assert payload["source_license_posture"]["ok"] is True
    assert payload["task_status"]["release_milestone_id"] == "ageint-release-" + payload["release_metadata"]["version"].replace(".", "-")
    assert "does not publish" in payload["release_decision"]

    markdown = render_publication_readiness_markdown(report)
    assert "Publication Readiness" in markdown
    assert "Release Decision" in markdown


def test_release_surface_scan_flags_private_paths_and_markdown_links(tmp_path: Path) -> None:
    _write(tmp_path / "output" / "manuscript" / "chapter.md", "# Chapter\n\nSee [local](notes.md) and /Users/4d/private-note.\n")
    _write(tmp_path / "output" / "reports" / "current_artifact_evidence.json", '{"pdf": {"pdf_path": "/Users/4d/private/AGEINT_combined.pdf"}}\n')
    _write(tmp_path / "output" / "reports" / "output_statistics.txt", "Output Directory: projects/working/AGEINT/output\n")

    issues = scan_release_surfaces(tmp_path)
    issue_names = {issue.issue for issue in issues}

    assert "markdown_file_link" in issue_names
    assert "absolute_user_path" in issue_names
    assert "working_lifecycle_path" in issue_names


def test_source_license_posture_flags_private_figure_provenance(tmp_path: Path) -> None:
    _write(tmp_path / "docs" / "manuscript" / "config.yaml", yaml.safe_dump({"book": {"license": "CC BY 4.0", "code_license": "Apache-2.0"}, "metadata": {"license": "CC-BY-4.0"}}))
    _write(tmp_path / "output" / "figures" / "figure_registry.json", json.dumps({"schema_version": "1.5", "figures": [{"label": "fig:fixture", "kind": "mermaid", "provenance": {"source": "/Users/4d/Downloads/private.md"}}]}))
    _write(tmp_path / "output" / "reports" / "source_metadata.json", json.dumps({"schema_version": "1.0", "summary": {"blank_source_lane_count": 0, "blank_source_tier_count": 0}}))

    posture = collect_source_license_posture(tmp_path)

    assert posture["ok"] is False
    assert posture["issues"][0]["issue"] == "private_path_in_figure_provenance"


def test_release_tasks_require_current_milestone_declared_prerequisites(tmp_path: Path) -> None:
    _write(
        tmp_path / "tasks.yaml",
        yaml.safe_dump({"tasks": [
            {"id": "new-render", "status": "done"}, {"id": "new-acceptance", "status": "todo"},
            {"id": "ageint-release-0-2-0", "milestone": True, "deps": ["new-render", "new-acceptance"], "status": "todo"},
        ]}),
    )

    status = collect_release_task_status(tmp_path, version="0.2.0")

    assert status["prerequisites_done"] is False
    assert status["required_done_tasks"]["new-acceptance"] == "todo"
    assert status["release_milestone_ready"] is True


def test_artifact_manifest_status_fails_on_missing_declared_output_issue(tmp_path: Path) -> None:
    _write(tmp_path / "output" / "reports" / "artifact_manifest.json", json.dumps({"entries": [], "issues": ["missing declared output: projects/AGEINT/output"]}))

    status = artifact_manifest_status(tmp_path)

    assert status["ok"] is False
    assert status["issue_count"] == 1


def test_publication_readiness_requires_parent_guard_even_with_green_local_evidence(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, native_guard_template: Path,
) -> None:
    class DummyReport:
        def __init__(self, payload: dict[str, object]) -> None:
            self.payload = payload

    artifact_payload = {
        "ok": True,
        "citations": {"generated_markdown_files": 3, "generated_markdown_citation_occurrences": 12},
        "figures": {"figure_count": 2},
        "pdf": {"page_count": 9, "stale_pdf": False, "link_audit": {"bad_target_count": 0}},
        "claim_calibration": {"summary": {"hard_fail_rows": 0}},
        "scholarship_quality": {"hard_fail_rows": []},
        "checks": _green_artifact_checks(),
        "reference_quality": {"summary": {"issue_count": 0, "generic_heading_issues": 0, "citation_context_issues": 0}},
    }
    refresh_payload = {"ok": True, "summary": {"due_or_stale_count": 0}, "issue_row_count": 0}
    monkeypatch.setattr(publication_readiness_module, "collect_artifact_evidence", lambda _root: DummyReport(artifact_payload))
    monkeypatch.setattr(publication_readiness_module, "collect_source_refresh_due", lambda _root: DummyReport(refresh_payload))

    _write(
        tmp_path / "tasks.yaml",
        yaml.safe_dump({"tasks": [
            {"id": "render", "status": "done"},
            {"id": "ageint-release-0-2-0", "milestone": True, "deps": ["render"], "status": "todo"},
        ]}),
    )
    _write_release_metadata(tmp_path)
    _write(tmp_path / "output" / "figures" / "figure_registry.json", json.dumps({"schema_version": "1.5", "figures": [{"label": "fig:fixture", "kind": "mermaid", "provenance": {"source": "fixture"}}]}))
    _write(tmp_path / "output" / "reports" / "source_metadata.json", json.dumps({"schema_version": "1.0", "summary": {"blank_source_lane_count": 0, "blank_source_tier_count": 0}}))
    _write(tmp_path / "output" / "reports" / "artifact_manifest.json", json.dumps({"issues": []}))
    _write(tmp_path / "output" / "manuscript" / "fixture.md", "# Fixture\n\nClean text.\n")

    report = collect_publication_readiness(tmp_path, run_parent_guard=False)
    payload = report.payload

    assert report.ok is False
    assert payload["parent_confidentiality_guard"]["checked"] is False
    assert payload["parent_confidentiality_guard"]["ok"] is False
    assert payload["parent_confidentiality_guard"]["status"] == "skipped"
    assert payload["parent_confidentiality_guard"]["returncode"] is None
    assert payload["checks"]["parent_confidentiality_guard_ok"] is False
    assert all(passed for name, passed in payload["checks"].items() if name != "parent_confidentiality_guard_ok")
    assert payload["checks"]["artifact_manifest_ok"] is True
    assert payload["checks"]["task_prerequisites_done"] is True
    assert payload["release_surface_scan"]["issue_count"] == 0

    json_path, md_path, written = publication_readiness_module.write_publication_readiness(tmp_path, run_parent_guard=False)
    assert written.ok is False
    assert json_path.is_file()
    assert md_path.read_text(encoding="utf-8").startswith("# AGEINT Publication Readiness")

    unavailable = collect_publication_readiness(tmp_path, template_root=tmp_path / "missing-template")
    assert unavailable.ok is False
    assert unavailable.payload["checks"]["parent_confidentiality_guard_ok"] is False
    assert unavailable.payload["parent_confidentiality_guard"]["status"] == "unavailable"

    checked = collect_publication_readiness(tmp_path, template_root=native_guard_template)
    assert checked.ok is True
    assert checked.payload["checks"]["parent_confidentiality_guard_ok"] is True
    assert checked.payload["parent_confidentiality_guard"]["status"] == "passed"

    citation = tmp_path / "CITATION.cff"
    citation.write_text('version: "0.1.0"\n', encoding="utf-8")
    mismatched = collect_publication_readiness(tmp_path, template_root=native_guard_template)
    assert mismatched.ok is False
    assert mismatched.payload["checks"]["release_metadata_ok"] is False
    assert mismatched.payload["checks"]["parent_confidentiality_guard_ok"] is True
    citation.write_text('version: "0.2.0"\n', encoding="utf-8")

    _write(native_guard_template / "scripts" / "audit" / "check_tracked_all.py", "raise SystemExit(7)\n")
    failed = collect_publication_readiness(tmp_path, template_root=native_guard_template)
    assert failed.ok is False
    assert failed.payload["checks"]["parent_confidentiality_guard_ok"] is False
    assert failed.payload["parent_confidentiality_guard"]["status"] == "failed"


def test_publication_readiness_writer_removes_stale_self_report_before_scan(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch, native_guard_template: Path,
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
                "citations": {"generated_markdown_files": 1, "generated_markdown_citation_occurrences": 1},
                "figures": {"figure_count": 1},
                "pdf": {"page_count": 1, "stale_pdf": False, "link_audit": {"bad_target_count": 0}},
                "claim_calibration": {"summary": {"hard_fail_rows": 0}},
                "scholarship_quality": {"hard_fail_rows": []},
                "checks": _green_artifact_checks(),
                "reference_quality": {"summary": {"issue_count": 0, "generic_heading_issues": 0, "citation_context_issues": 0}},
            }
        ),
    )
    monkeypatch.setattr(publication_readiness_module, "collect_source_refresh_due", lambda _root: DummyReport({"ok": True, "summary": {"due_or_stale_count": 0}, "issue_row_count": 0}))
    _write(
        native_guard_template / "scripts" / "audit" / "check_tracked_all.py",
        'import sys\nprint("ok")\nprint("warning: /Users/4d/private/env", file=sys.stderr)\n',
    )
    _write(
        tmp_path / "tasks.yaml",
        yaml.safe_dump({"tasks": [
            {"id": "render", "status": "done"},
            {"id": "ageint-release-0-2-0", "milestone": True, "deps": ["render"], "status": "done"},
        ]}),
    )
    _write_release_metadata(tmp_path)
    _write(tmp_path / "output" / "figures" / "figure_registry.json", json.dumps({"schema_version": "1.5", "figures": [{"label": "fig:fixture", "provenance": {"source": "fixture"}}]}))
    _write(tmp_path / "output" / "reports" / "source_metadata.json", json.dumps({"schema_version": "1.0", "summary": {"blank_source_lane_count": 0, "blank_source_tier_count": 0}}))
    _write(tmp_path / "output" / "reports" / "artifact_manifest.json", json.dumps({"issues": []}))
    _write(tmp_path / "output" / "manuscript" / "fixture.md", "# Fixture\n\nClean text.\n")
    _write(tmp_path / "output" / "reports" / "publication_readiness.json", '{"stale": "/Users/4d/private/previous-run"}\n')

    json_path, _md_path, report = publication_readiness_module.write_publication_readiness(tmp_path, template_root=native_guard_template)

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
    result = publication_readiness_module.run_parent_confidentiality_guard(tmp_path, template_root=tmp_path / "missing-template")

    assert result["checked"] is False
    assert result["ok"] is False
    assert result["status"] == "unavailable"
    assert result["returncode"] is None


def test_parent_guard_uses_shared_sibling_resolution(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    for name in ("AGEINT_TEMPLATE_REPO", "DOCXOLOGY_TEMPLATE_REPO", "DOCXOLOGY_TEMPLATE_ROOT", "TEMPLATE_REPO_ROOT"):
        monkeypatch.delenv(name, raising=False)
    project = tmp_path / "Public" / "AGEINT"
    project.mkdir(parents=True)
    template = project.parent / "template"
    _write(template / "infrastructure" / "validation" / "cli.py", "")
    (template / "infrastructure" / "rendering").mkdir()

    assert publication_readiness_module.resolve_template_repo(project) == template.resolve()




@pytest.mark.parametrize("exit_code", [0, 13])
def test_parent_guard_executes_current_script_in_template_cwd(native_guard_template: Path, exit_code: int) -> None:
    script = native_guard_template / "scripts" / "audit" / "check_tracked_all.py"
    script.write_text(script.read_text(encoding="utf-8") + f"raise SystemExit({exit_code})\n", encoding="utf-8")
    # A stale command must not silently pass by invoking an obsolete entry point.
    _write(native_guard_template / "scripts" / "check_tracked_projects.py", "raise SystemExit(97)\n")

    result = publication_readiness_module.run_parent_confidentiality_guard(PROJECT_ROOT, template_root=native_guard_template)

    assert result["checked"] is True
    assert result["ok"] is (exit_code == 0)
    assert result["status"] == ("passed" if exit_code == 0 else "failed")
    assert result["returncode"] == exit_code
    evidence = json.loads(result["stdout"])
    assert evidence["cwd"] == publication_readiness_module._clean_output(str(native_guard_template.resolve()))
    assert evidence["script"] == publication_readiness_module._clean_output(str(script.resolve()))


def test_parent_guard_rejects_missing_current_script(tmp_path: Path) -> None:
    _write(tmp_path / "scripts" / "check_tracked_projects.py", "raise SystemExit(0)\n")
    result = publication_readiness_module.run_parent_confidentiality_guard(PROJECT_ROOT, template_root=tmp_path)
    assert result["status"] == "unavailable"
    assert result["checked"] is False
    assert result["ok"] is False
    assert result["returncode"] is None


def test_parent_guard_needs_no_uv_or_dependency_sync(native_guard_template: Path, monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    empty_path = tmp_path / "empty-bin"
    empty_path.mkdir()
    monkeypatch.setenv("PATH", str(empty_path))
    result = publication_readiness_module.run_parent_confidentiality_guard(PROJECT_ROOT, template_root=native_guard_template)
    assert result["status"] == "passed"
    assert result["checked"] is True
    assert result["ok"] is True
    assert result["returncode"] == 0


def test_parent_guard_reports_real_subprocess_timeout(native_guard_template: Path) -> None:
    _write(native_guard_template / "scripts" / "audit" / "check_tracked_all.py", "import time\ntime.sleep(2)\n")
    result = publication_readiness_module.run_parent_confidentiality_guard(
        PROJECT_ROOT, template_root=native_guard_template, timeout=0.1,
    )
    assert result["status"] == "timeout"
    assert result["checked"] is False
    assert result["ok"] is False
    assert result["returncode"] is None


def test_parent_guard_matches_current_template_native_command() -> None:
    template = publication_readiness_module.resolve_template_repo(PROJECT_ROOT)
    if template is None:
        pytest.skip("Native template guard requires the sibling checkout")
    command = [sys.executable, "scripts/audit/check_tracked_all.py"]
    expected = subprocess.run(command, cwd=template, check=False, capture_output=True, text=True, timeout=180)
    actual = publication_readiness_module.run_parent_confidentiality_guard(PROJECT_ROOT)
    assert actual["checked"] is True
    assert actual["returncode"] == expected.returncode
    assert actual["ok"] is (expected.returncode == 0)
    assert actual["status"] == ("passed" if expected.returncode == 0 else "failed")
    assert actual["stdout"] == publication_readiness_module._clean_output(expected.stdout)


def test_readiness_cli_rejects_skipped_parent_guard() -> None:
    if not (PROJECT_ROOT / "output" / "pdf" / "AGEINT_combined.pdf").is_file():
        pytest.skip("Rendered combined PDF not present")

    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "audit_publication_readiness.py"),
            "--format",
            "json",
            "--skip-parent-guard",
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=900,
    )
    assert result.returncode == 1, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["ok"] is False
    assert payload["checks"]["parent_confidentiality_guard_ok"] is False
    assert payload["parent_confidentiality_guard"]["status"] == "skipped"
