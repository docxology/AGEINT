"""US IC agency-source expansion and coverage contracts."""

from __future__ import annotations

from datetime import date
from pathlib import Path
import json
import subprocess
import sys

from agency_source_coverage import (
    collect_agency_source_coverage,
    render_agency_source_coverage_markdown,
)
from intelligence_content import (
    INTELLIGENCE_PROFILES,
    INTELLIGENCE_RESEARCH_ANCHORS,
    agency_source_pack_keys,
    expanded_profile_anchor_keys,
)
from manuscript_quality.inventory_helpers import SOURCE_QUALITY_KEYS

PROJECT_ROOT = Path(__file__).resolve().parents[1]
NEW_SHARD = PROJECT_ROOT / "data" / "research_anchors" / "intelligence-anchors-249-304.jsonl"


def _new_rows() -> list[dict[str, object]]:
    return [
        json.loads(line)
        for line in NEW_SHARD.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def test_us_ic_source_expansion_shard_count_and_minimums() -> None:
    rows = _new_rows()
    agencies = [str(row["source_agency"]) for row in rows]

    assert len(rows) == 56
    assert len(INTELLIGENCE_RESEARCH_ANCHORS) == 462
    assert agencies.count("CIA") >= 25
    assert agencies.count("DIA") >= 3
    assert sum(agency in {"ODNI", "Intelligence.gov"} for agency in agencies) >= 20


def test_new_official_us_ic_anchors_are_metadata_complete_and_unique() -> None:
    rows = _new_rows()
    keys = [str(row["key"]) for row in rows]
    urls = [str(row["url"]) for row in rows]
    required = {
        "key",
        "title",
        "author",
        "year",
        "url",
        "note",
        "domain",
        "source_type",
        "checked_as_of",
        "verification_note",
        "citation_role",
        "source_lane",
        "source_tier",
        "refresh_cadence",
        "refresh_trigger",
        "verification_method",
        "claim_scope",
        "stakeholder_role",
        "assurance_use",
        "rights_dimension",
        "source_agency",
        "source_pack",
    }

    assert len(keys) == len(set(keys))
    assert len(urls) == len(set(urls))
    for row in rows:
        assert required <= set(row), row
        assert str(row["key"]).startswith("official_")
        assert str(row["source_type"]) == "official_primary"
        assert str(row["source_tier"]) == "official_primary"
        assert str(row["citation_role"]) == "curriculum_anchor"
        assert str(row["url"]).startswith("https://")
        assert date.fromisoformat(str(row["checked_as_of"])) >= date(2026, 6, 14)
        for field in required:
            assert str(row[field]).strip(), (row["key"], field)


def test_agency_source_packs_are_deterministic_deduped_and_profile_routable() -> None:
    analytic = agency_source_pack_keys("cia_analytic_uncertainty")
    assert analytic == tuple(dict.fromkeys(analytic))
    assert "official_cia_words_estimative_probability" in analytic
    assert "official_cia_limits_of_prediction" in analytic

    all_anchor_keys = {anchor.key for anchor in INTELLIGENCE_RESEARCH_ANCHORS} | SOURCE_QUALITY_KEYS
    for profile in INTELLIGENCE_PROFILES:
        expanded = expanded_profile_anchor_keys(profile)
        assert expanded == tuple(dict.fromkeys(expanded)), profile.identifier
        assert set(expanded) <= all_anchor_keys, profile.identifier
    routed = {
        key
        for profile in INTELLIGENCE_PROFILES
        for key in expanded_profile_anchor_keys(profile)
    }
    assert {str(row["key"]) for row in _new_rows()} & routed


def test_agency_source_coverage_current_report_and_markdown() -> None:
    report = collect_agency_source_coverage(PROJECT_ROOT)
    payload = report.payload

    assert report.ok is True
    assert payload["summary"]["new_official_us_ic_anchor_count"] == 56
    assert payload["summary"]["curated_intelligence_anchor_count"] == 462
    assert payload["summary"]["missing_required_metadata_count"] == 0
    assert payload["summary"]["unrouted_new_anchor_count"] == 0
    assert payload["summary"]["agency_counts"]["CIA"] >= 25
    assert payload["summary"]["agency_counts"]["DIA"] >= 3
    assert payload["summary"]["source_pack_counts"]["cia_analytic_uncertainty"] >= 1
    assert "agency_source_coverage_ok" in render_agency_source_coverage_markdown(report)


def test_agency_source_coverage_fails_missing_source_pack_negative_control(tmp_path: Path) -> None:
    data_dir = tmp_path / "data" / "research_anchors"
    data_dir.mkdir(parents=True)
    row = {
        "key": "official_fixture_us_ic",
        "title": "Fixture",
        "author": "Fixture Agency",
        "year": "2026",
        "url": "https://example.com/source",
        "note": "Fixture source.",
        "domain": "analytic_tradecraft",
        "source_type": "official_primary",
        "checked_as_of": "2026-06-14",
        "verification_note": "Fixture verified.",
        "citation_role": "curriculum_anchor",
        "source_lane": "analytic_tradecraft_evidence",
        "source_tier": "official_primary",
        "refresh_cadence": "annual",
        "refresh_trigger": "fixture changes",
        "verification_method": "fixture_review",
        "claim_scope": "fixture claim scope",
        "stakeholder_role": "fixture stakeholder",
        "assurance_use": "fixture assurance",
        "rights_dimension": "fixture rights",
        "source_agency": "CIA",
        "source_pack": "",
    }
    (data_dir / "intelligence-anchors-249-304.jsonl").write_text(
        json.dumps(row) + "\n",
        encoding="utf-8",
    )
    (tmp_path / "data" / "agency_source_packs.yaml").write_text(
        "packs:\n  fixture_pack:\n    - official_fixture_us_ic\n",
        encoding="utf-8",
    )

    report = collect_agency_source_coverage(tmp_path)

    assert report.ok is False
    assert report.payload["summary"]["missing_required_metadata_count"] == 1
    assert "missing_source_pack" in report.payload["issue_rows"][0]["flags"]


def test_audit_agency_source_coverage_script_writes_json_contract() -> None:
    result = subprocess.run(
        [
            sys.executable,
            str(PROJECT_ROOT / "scripts" / "audit_agency_source_coverage.py"),
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
    assert payload["summary"]["new_official_us_ic_anchor_count"] == 56
    assert (PROJECT_ROOT / "output" / "reports" / "agency_source_coverage.json").is_file()
    assert (PROJECT_ROOT / "output" / "reports" / "agency_source_coverage.md").is_file()
