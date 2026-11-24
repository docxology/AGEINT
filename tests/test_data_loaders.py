"""Tests for declarative YAML loaders in ``src/_data_loaders.py``."""

from __future__ import annotations

from pathlib import Path

import pytest

import _data_loaders as data_loaders

from _data_loaders import (
    artifact_keyword_routes,
    artifact_risk_category_prompts,
    category_concept_frames,
    concept_keyword_routes,
    domain_concept_routes,
    evidence_category_prompts,
    evidence_keyword_routes,
    merged_concept_keyword_routes,
    misconception_fallbacks,
    misconception_risk_templates,
    module_architecture,
    risk_why_failure_hints,
    topic_prompt_routes_payload,
    topic_rotation_templates_payload,
    topic_risk_routes_payload,
    why_it_matters_templates,
)


def test_concept_route_loaders_return_non_empty_tuples() -> None:
    assert concept_keyword_routes()
    assert domain_concept_routes()
    assert merged_concept_keyword_routes()


def test_concept_routes_without_optional_supplement_preserve_primary_routes(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    data_dir = tmp_path / "data"
    data_dir.mkdir()
    (data_dir / "concept_routes.yaml").write_text(
        "concept_keyword_routes:\n  - keywords: [primary]\n    frame: primary_frame\n"
        "concept_keyword_routes_b:\n  - keywords: [secondary]\n    frame: secondary_frame\n"
        "domain_concept_routes:\n  - keywords: [domain]\n    frame: domain_frame\n",
        encoding="utf-8",
    )
    cached_loaders = (data_loaders._load_concept_routes_yaml, data_loaders._yaml_routes, data_loaders.merged_concept_keyword_routes)
    for loader in cached_loaders:
        loader.cache_clear()
    try:
        with monkeypatch.context() as patch:
            patch.setattr(data_loaders, "_PROJECT_ROOT", tmp_path)

            assert data_loaders.merged_concept_keyword_routes() == (
                (("primary",), "primary_frame"),
                (("secondary",), "secondary_frame"),
                (("domain",), "domain_frame"),
            )
    finally:
        for loader in cached_loaders:
            loader.cache_clear()


def test_category_concept_frames_maps_categories() -> None:
    frames = category_concept_frames()
    assert frames
    assert all(isinstance(key, str) and isinstance(value, str) for key, value in frames.items())


def test_module_architecture_returns_four_fields() -> None:
    inputs, transforms, outputs, failures = module_architecture("agentic_ai_governance")
    assert inputs
    assert transforms
    assert outputs
    assert failures


def test_module_architecture_falls_back_to_default_profile() -> None:
    inputs, transforms, outputs, failures = module_architecture("unknown_profile_slug")
    assert all((inputs, transforms, outputs, failures))


def test_topic_risk_routes_payload_has_rule_lists() -> None:
    payload = topic_risk_routes_payload()
    assert len(payload["topic_rules"]) >= 30
    assert len(payload["chapter_context_rules"]) >= 8


def test_transfer_task_keyword_routes_loaded() -> None:
    from _data_loaders import transfer_task_keyword_routes

    routes = transfer_task_keyword_routes()
    assert routes
    assert any("active inference" in keywords for keywords, _ in routes)


def test_topic_prompt_routes_payload_has_required_sections() -> None:
    payload = topic_prompt_routes_payload()
    for key in ("evidence_category_prompts", "evidence_keyword_routes", "artifact_keyword_routes", "artifact_risk_category_prompts"):
        assert isinstance(payload[key], list)
        assert payload[key]


def test_topic_prompt_route_loaders_return_non_empty() -> None:
    assert evidence_category_prompts()
    assert evidence_keyword_routes()
    assert artifact_keyword_routes()
    assert artifact_risk_category_prompts()


def test_topic_rotation_templates_payload_has_required_sections() -> None:
    payload = topic_rotation_templates_payload()
    for key in ("why_it_matters_templates", "risk_why_failure_hints", "misconception_fallbacks", "misconception_risk_templates", "misconception_keyword_routes", "transfer_task_keyword_routes"):
        assert isinstance(payload[key], list)
        assert payload[key]


def test_topic_rotation_template_loaders_return_non_empty() -> None:
    assert why_it_matters_templates()
    assert risk_why_failure_hints()
    assert misconception_fallbacks()
    assert misconception_risk_templates()
    from _data_loaders import misconception_keyword_routes

    assert misconception_keyword_routes()


def test_safety_artifact_table_names_match_yaml() -> None:
    from _data_loaders import SAFETY_ARTIFACT_TABLE_NAMES, safety_artifact_tables_payload

    payload = safety_artifact_tables_payload()
    assert set(payload) == set(SAFETY_ARTIFACT_TABLE_NAMES)
    assert len(SAFETY_ARTIFACT_TABLE_NAMES) == 17


def test_safety_artifact_table_loader_returns_rows() -> None:
    from _data_loaders import safety_artifact_table

    rows = safety_artifact_table("SAFE_SUBSTITUTION_PATTERNS")
    assert rows
    assert "motif" in rows[0]
