"""Tests for generated reference, title, and citation-context quality audit."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from reference_quality import (
    collect_reference_quality,
    render_reference_quality_markdown,
    write_reference_quality,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def test_reference_quality_current_outputs_are_green(built_output: Path) -> None:
    report = collect_reference_quality(PROJECT_ROOT)
    payload = report.payload

    assert payload["project"] == "AGEINT"
    assert payload["schema_version"] == "1.0"
    assert report.ok is True
    assert payload["summary"]["issue_count"] == 0
    assert payload["summary"]["generic_heading_issues"] == 0
    assert payload["summary"]["citation_context_issues"] == 0
    assert payload["summary"]["markdown_file_link_issues"] == 0
    assert payload["summary"]["raw_literal_citation_issues"] == 0

    markdown = render_reference_quality_markdown(report)
    assert "reference_quality_ok" in markdown
    assert "Citation-context issues" in markdown


def test_reference_quality_flags_reader_quality_negative_controls(tmp_path: Path) -> None:
    _write(
        tmp_path / "output" / "manuscript" / "chapter.md",
        "\n".join(
            [
                "# Chapter {#sec:chapter-fixture}",
                "",
                "### Module architecture and transfer contract",
                "",
                "See [local notes](notes.md).",
                "",
                "**Learning-path links.** Unit module map; module overview; curriculum atlas.",
                "",
                "| Citation links |",
                "|---|",
                "| [@official_fixture] |",
                "",
                "Use `@ageint001` as a raw key.",
            ]
        ),
    )
    _write(
        tmp_path / "output" / "manuscript" / "references-fixture.bib",
        "@misc{official_fixture, title={Fixture}}\n",
    )

    report = collect_reference_quality(tmp_path)
    issue_names = {row["issue"] for row in report.payload["issue_rows"]}

    assert report.ok is False
    assert "markdown_file_link" in issue_names
    assert "generic_detail_heading" in issue_names
    assert "citation_table_row_without_context" in issue_names
    assert "raw_literal_citation_key" in issue_names
    assert any(issue.startswith("incomplete_cross_link:") for issue in issue_names)


def test_reference_quality_allows_contextual_citation_tables_and_linked_crossrefs(tmp_path: Path) -> None:
    _write(
        tmp_path / "output" / "manuscript" / "chapter.md",
        "\n".join(
            [
                "# Chapter {#sec:chapter}",
                "",
                "### Chapter evidence spine: source roles, citation support, and claim limits",
                "",
                "**Learning-path links.** Unit module map [@fig:part-fixture-module-map]; module overview [@sec:chapter-fixture]; curriculum atlas [@sec:curriculum_orientation].",
                "",
                "| Source title | Citation links |",
                "|---|---|",
                "| Official fixture source with lane and role context | [@official_fixture] |",
            ]
        ),
    )
    _write(
        tmp_path / "output" / "manuscript" / "references-fixture.bib",
        "@misc{official_fixture, title={Fixture}}\n",
    )

    report = collect_reference_quality(tmp_path)

    assert report.ok is True
    assert report.payload["summary"]["issue_count"] == 0


def test_reference_quality_writer_and_script_emit_json_contract(built_output: Path) -> None:
    json_path, md_path, report = write_reference_quality(PROJECT_ROOT)

    assert report.ok is True
    assert json_path.is_file()
    assert md_path.is_file()

    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "audit_reference_quality.py"),
            "--format",
            "json",
            "--write",
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=180,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    payload = json.loads(result.stdout)
    assert payload["ok"] is True
    assert payload["summary"]["issue_count"] == 0
