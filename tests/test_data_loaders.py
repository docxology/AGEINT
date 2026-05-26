"""Tests for declarative YAML loaders in ``src/_data_loaders.py``."""

from __future__ import annotations

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
    assert payload["topic_rules"]
    assert payload["chapter_context_rules"]


def test_topic_prompt_routes_payload_has_required_sections() -> None:
    payload = topic_prompt_routes_payload()
    for key in (
        "evidence_category_prompts",
        "evidence_keyword_routes",
        "artifact_keyword_routes",
        "artifact_risk_category_prompts",
    ):
        assert isinstance(payload[key], list)
        assert payload[key]


def test_topic_prompt_route_loaders_return_non_empty() -> None:
    assert evidence_category_prompts()
    assert evidence_keyword_routes()
    assert artifact_keyword_routes()
    assert artifact_risk_category_prompts()


def test_topic_rotation_templates_payload_has_required_sections() -> None:
    payload = topic_rotation_templates_payload()
    for key in (
        "why_it_matters_templates",
        "risk_why_failure_hints",
        "misconception_fallbacks",
        "misconception_risk_templates",
    ):
        assert isinstance(payload[key], list)
        assert payload[key]


def test_topic_rotation_template_loaders_return_non_empty() -> None:
    assert why_it_matters_templates()
    assert risk_why_failure_hints()
    assert misconception_fallbacks()
    assert misconception_risk_templates()


def test_coursebook_profiles_loader_returns_fourteen_profiles() -> None:
    from _data_loaders import coursebook_profiles_as_dataclasses

    profiles = coursebook_profiles_as_dataclasses()
    assert len(profiles) == 14
    sample = profiles["analytic_tradecraft"]
    assert sample.identifier == "analytic_tradecraft"
    assert sample.vocabulary


def test_safety_artifact_table_loader_returns_rows() -> None:
    from _data_loaders import safety_artifact_table

    rows = safety_artifact_table("SAFE_SUBSTITUTION_PATTERNS")
    assert rows
    assert "motif" in rows[0]
