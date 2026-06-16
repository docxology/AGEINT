"""Contract-registry tests for AGEINT orchestration and extension seams."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

import pytest

from audit_contracts import audit_contracts, publication_readiness_audit_check_ids
from figures.mermaid_contracts import mermaid_type_contracts, validate_mermaid_source_contract
from intelligence_content import INTELLIGENCE_RESEARCH_ANCHORS
from intelligence_content.source_packs import (
    source_pack_contract_report,
    source_pack_registry,
)
from orchestration_audit import collect_orchestration_contract, render_orchestration_contract_markdown
from orchestration_contracts import (
    output_build_sentinels,
    pipeline_stage_contracts,
    source_freshness_roots,
    validate_pipeline_stage_contracts,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_pipeline_stage_registry_is_complete_acyclic_and_derives_freshness_contracts() -> None:
    validate_pipeline_stage_contracts()
    stages = pipeline_stage_contracts()
    stage_ids = {stage.stage_id for stage in stages}

    assert {
        "source_validation",
        "curriculum_build",
        "variables_and_bibliography",
        "figures",
        "manuscript_render",
        "evidence_transit",
        "artifact_reports",
    } <= stage_ids
    assert Path("data") in source_freshness_roots()
    assert Path("src") in source_freshness_roots()
    assert Path("figures/figure_registry.json") in output_build_sentinels()
    assert Path("reports/current_artifact_evidence.json") not in output_build_sentinels()
    assert all(stage.strict_gate for stage in stages)
    assert all(stage.failure_mode for stage in stages)


def test_audit_registry_declares_report_paths_negative_controls_and_readiness_gates() -> None:
    contracts = audit_contracts()
    check_ids = {contract.check_id for contract in contracts}

    assert {
        "reference_quality_ok",
        "scholarship_quality_ok",
        "source_metadata_ok",
        "source_refresh_due_ok",
        "agency_source_coverage_ok",
        "claim_calibration_ok",
        "figure_quality_ok",
        "pdf_quality_ok",
        "rendered_references_resolve",
        "stale_output_scans_clean",
    } <= check_ids
    for contract in contracts:
        assert contract.report_paths
        assert contract.negative_control
        assert contract.purpose
    assert "reference_quality_ok" in publication_readiness_audit_check_ids()
    assert "agency_source_coverage_ok" in publication_readiness_audit_check_ids()


def test_source_pack_registry_validates_known_keys_and_source_class_errors(tmp_path: Path) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "agency_source_packs.yaml").write_text(
        "packs:\n  agency_pack:\n    - official_known\n",
        encoding="utf-8",
    )
    (data_dir / "research_source_packs.yaml").write_text(
        "packs:\n  research_pack:\n    - scholarly_missing\nprofile_routes:\n  analytic_tradecraft:\n    - research_pack\n",
        encoding="utf-8",
    )

    report = source_pack_contract_report(tmp_path, known_source_keys={"official_known"})

    assert report["issue_count"] == 1
    assert report["issues"][0]["source_class"] == "research"
    assert report["issues"][0]["issue"] == "unknown_source_key"

    (data_dir / "research_source_packs.yaml").write_text(
        "packs:\n  research_pack:\n    - scholarly_known\n    - scholarly_known\n",
        encoding="utf-8",
    )
    with pytest.raises(ValueError, match="research source packs entry research_pack has duplicate"):
        source_pack_registry("research", tmp_path)


def test_current_source_pack_registry_routes_known_anchor_keys() -> None:
    known_keys = {anchor.key for anchor in INTELLIGENCE_RESEARCH_ANCHORS}
    report = source_pack_contract_report(PROJECT_ROOT, known_source_keys=known_keys)

    assert report["issue_count"] == 0
    by_class = {registry["source_class"]: registry for registry in report["registries"]}
    assert by_class["agency"]["pack_count"] >= 1
    assert by_class["research"]["profile_route_count"] >= 1
    assert all(not Path(registry["path"]).is_absolute() for registry in report["registries"])


def test_mermaid_type_contracts_cover_supported_types_and_fail_bad_sources() -> None:
    types = {contract.diagram_type for contract in mermaid_type_contracts()}

    assert {
        "flowchart",
        "stateDiagram-v2",
        "sequenceDiagram",
        "journey",
        "timeline",
        "quadrantChart",
    } <= types
    validate_mermaid_source_contract(
        "sequenceDiagram",
        "sequenceDiagram\n    A->>B: check\n",
        "reader detail with enough words to explain the exchange, evidence handoff, and reviewer boundary",
    )
    with pytest.raises(ValueError, match="must start"):
        validate_mermaid_source_contract("timeline", "flowchart TB\n    A-->B\n", "timeline reader detail with enough words")
    with pytest.raises(ValueError, match="reader_detail"):
        validate_mermaid_source_contract("journey", "journey\n    title Review\n", "thin")


def test_orchestration_contract_report_and_cli_expose_all_contract_families() -> None:
    payload = collect_orchestration_contract(PROJECT_ROOT)
    markdown = render_orchestration_contract_markdown(payload)
    payload_text = json.dumps(payload, sort_keys=True)

    assert payload["pipeline"]["stage_count"] >= 8
    assert payload["audits"]["contract_count"] >= 10
    assert payload["source_packs"]["registry_count"] == 2
    assert payload["mermaid"]["diagram_type_count"] >= 6
    assert PROJECT_ROOT.as_posix() not in payload_text
    assert PROJECT_ROOT.as_posix() not in markdown
    assert "AGEINT Contract Map" in markdown
    assert "Pipeline Contract" in markdown
    assert "Audit Contracts" in markdown
    assert "Source-Pack Contracts" in markdown
    assert "Mermaid Diagram Types" in markdown

    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "audit_orchestration_contract.py"),
            "--format",
            "json",
        ],
        cwd=PROJECT_ROOT,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    cli_payload = json.loads(result.stdout)
    assert cli_payload["ok"] is True
    assert cli_payload["audits"]["contract_count"] == payload["audits"]["contract_count"]
    assert PROJECT_ROOT.as_posix() not in result.stdout
