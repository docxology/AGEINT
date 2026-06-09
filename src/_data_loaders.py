"""Load declarative AGEINT data files from ``data/``."""

from __future__ import annotations

from functools import lru_cache
from pathlib import Path
from typing import Any, Final

import yaml

_PROJECT_ROOT = Path(__file__).resolve().parents[1]


def _load_yaml_mapping(path: Path) -> dict[str, Any]:
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected mapping in {path}")
    return payload


@lru_cache(maxsize=1)
def _load_concept_routes_yaml() -> dict[str, Any]:
    primary = _load_yaml_mapping(_PROJECT_ROOT / "data" / "concept_routes.yaml")
    supplement = _PROJECT_ROOT / "data" / "concept_routes_supplement.yaml"
    if not supplement.is_file():
        return primary
    merged = dict(primary)
    for section, rows in _load_yaml_mapping(supplement).items():
        if section in merged and isinstance(merged[section], list) and isinstance(rows, list):
            merged[section] = [*merged[section], *rows]
        else:
            merged[section] = rows
    return merged


def _yaml_routes(section: str) -> tuple[tuple[tuple[str, ...], str], ...]:
    payload = _load_concept_routes_yaml()
    if section not in payload:
        raise KeyError(f"Missing concept-route section: {section}")
    rows = payload[section]
    return tuple(
        (tuple(str(keyword) for keyword in row["keywords"]), str(row["frame"]))
        for row in rows
    )


def concept_keyword_routes() -> tuple[tuple[tuple[str, ...], str], ...]:
    """Return primary keyword concept routes."""
    return _yaml_routes("concept_keyword_routes")


def concept_keyword_routes_b() -> tuple[tuple[tuple[str, ...], str], ...]:
    """Return supplemental keyword concept routes."""
    return _yaml_routes("concept_keyword_routes_b")


def domain_concept_routes() -> tuple[tuple[tuple[str, ...], str], ...]:
    """Return domain keyword concept routes."""
    return _yaml_routes("domain_concept_routes")


def merged_concept_keyword_routes() -> tuple[tuple[tuple[str, ...], str], ...]:
    """Return all keyword routes in evaluation order."""
    return concept_keyword_routes() + concept_keyword_routes_b() + domain_concept_routes()


def category_concept_frames() -> dict[str, str]:
    """Return category slug to lesson-frame text."""
    rows = _load_concept_routes_yaml()["category_concept_frames"]
    return {str(row["category"]): str(row["frame"]) for row in rows}


@lru_cache(maxsize=1)
def module_architecture(profile_id: str) -> tuple[str, str, str, str]:
    """Return inputs, transforms, outputs, and failures for a chapter profile."""
    path = _PROJECT_ROOT / "data" / "manuscript_architecture.yaml"
    payload = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(payload, dict):
        raise ValueError(f"Expected mapping in {path}")
    profiles = payload.get("profiles", {})
    default = payload.get("default", {})
    row = profiles.get(profile_id, default)
    return (
        str(row["inputs"]),
        str(row["transforms"]),
        str(row["outputs"]),
        str(row["failures"]),
    )


@lru_cache(maxsize=1)
def unit_education_profiles() -> dict[int, dict[str, Any]]:
    """Return unit-specific education profiles keyed by part number."""
    payload = _load_yaml_mapping(_PROJECT_ROOT / "data" / "unit_education_profiles.yaml")
    profiles = payload.get("profiles", {})
    if not isinstance(profiles, dict):
        raise ValueError("Expected mapping under profiles in unit_education_profiles.yaml")
    rendered: dict[int, dict[str, Any]] = {}
    for raw_key, value in profiles.items():
        if not isinstance(value, dict):
            raise ValueError(f"Expected mapping for unit profile {raw_key!r}")
        rendered[int(raw_key)] = value
    return rendered


@lru_cache(maxsize=1)
def source_support_expansion() -> dict[str, Any]:
    """Return data-driven citation routes for uncited source sections."""
    return _load_yaml_mapping(_PROJECT_ROOT / "data" / "source_support_expansion.yaml")


@lru_cache(maxsize=1)
def topic_risk_routes_payload() -> dict[str, Any]:
    """Return ordered topic and chapter risk-category routing rules."""
    payload = _load_yaml_mapping(_PROJECT_ROOT / "data" / "topic_risk_routes.yaml")
    for key in ("topic_rules", "chapter_context_rules"):
        if key not in payload or not isinstance(payload[key], list):
            raise ValueError(f"Expected list {key!r} in topic_risk_routes.yaml")
    return payload


@lru_cache(maxsize=1)
def topic_prompt_routes_payload() -> dict[str, Any]:
    """Return evidence and artifact prompt routing tables."""
    payload = _load_yaml_mapping(_PROJECT_ROOT / "data" / "topic_prompt_routes.yaml")
    for key in (
        "evidence_category_prompts",
        "evidence_keyword_routes",
        "artifact_keyword_routes",
        "artifact_risk_category_prompts",
    ):
        if key not in payload or not isinstance(payload[key], list):
            raise ValueError(f"Expected list {key!r} in topic_prompt_routes.yaml")
    return payload


def _prompt_category_map(section: str) -> dict[str, str]:
    rows = topic_prompt_routes_payload()[section]
    return {str(row["category"]): str(row["prompt"]) for row in rows}


def _prompt_keyword_routes(section: str) -> tuple[tuple[tuple[str, ...], str], ...]:
    rows = topic_prompt_routes_payload()[section]
    return tuple(
        (tuple(str(keyword) for keyword in row["keywords"]), str(row["prompt"]))
        for row in rows
    )


def evidence_category_prompts() -> dict[str, str]:
    """Return risk-category to evidence-prompt text."""
    return _prompt_category_map("evidence_category_prompts")


def evidence_keyword_routes() -> tuple[tuple[tuple[str, ...], str], ...]:
    """Return ordered evidence keyword routes."""
    return _prompt_keyword_routes("evidence_keyword_routes")


def artifact_keyword_routes() -> tuple[tuple[tuple[str, ...], str], ...]:
    """Return ordered artifact keyword routes."""
    return _prompt_keyword_routes("artifact_keyword_routes")


def artifact_risk_category_prompts() -> dict[str, str]:
    """Return risk-category to artifact-prompt text."""
    return _prompt_category_map("artifact_risk_category_prompts")


@lru_cache(maxsize=1)
def topic_rotation_templates_payload() -> dict[str, Any]:
    """Return why-it-matters and misconception rotation tables."""
    payload = _load_yaml_mapping(_PROJECT_ROOT / "data" / "topic_rotation_templates.yaml")
    for key in (
        "why_it_matters_templates",
        "risk_why_failure_hints",
        "misconception_fallbacks",
        "misconception_risk_templates",
        "misconception_keyword_routes",
        "transfer_task_keyword_routes",
    ):
        if key not in payload or not isinstance(payload[key], list):
            raise ValueError(f"Expected list {key!r} in topic_rotation_templates.yaml")
    return payload


def why_it_matters_templates() -> tuple[str, ...]:
    """Return ordered why-it-matters format templates."""
    rows = topic_rotation_templates_payload()["why_it_matters_templates"]
    return tuple(str(row) for row in rows)


def risk_why_failure_hints() -> dict[str, str]:
    """Return risk-category to failure-hint text."""
    rows = topic_rotation_templates_payload()["risk_why_failure_hints"]
    return {str(row["category"]): str(row["hint"]) for row in rows}


def misconception_fallbacks() -> tuple[str, ...]:
    """Return ordered standard misconception fallback templates."""
    rows = topic_rotation_templates_payload()["misconception_fallbacks"]
    return tuple(str(row) for row in rows)


def misconception_risk_templates() -> tuple[str, ...]:
    """Return ordered risk-category misconception templates."""
    rows = topic_rotation_templates_payload()["misconception_risk_templates"]
    return tuple(str(row) for row in rows)


def misconception_keyword_routes() -> tuple[tuple[tuple[str, ...], str], ...]:
    """Return ordered misconception keyword routes."""
    rows = topic_rotation_templates_payload()["misconception_keyword_routes"]
    return tuple(
        (tuple(str(keyword) for keyword in row["keywords"]), str(row["misconception"]))
        for row in rows
    )


def misconception_category_routes() -> dict[str, str]:
    """Return risk-category-specific misconception clauses (risk_category -> clause).

    Consulted after keyword routes and before the generic per-risk templates so a
    topic whose risk category has a tailored misconception gets it instead of one
    of three decoupled fallbacks. Absent key degrades gracefully to ``{}``.
    """
    rows = topic_rotation_templates_payload().get("misconception_category_routes", {})
    return {str(key): str(value) for key, value in rows.items()}


def transfer_task_keyword_routes() -> tuple[tuple[tuple[str, ...], str], ...]:
    """Return ordered transfer-task keyword routes."""
    rows = topic_rotation_templates_payload()["transfer_task_keyword_routes"]
    return tuple(
        (tuple(str(keyword) for keyword in row["keywords"]), str(row["template"]))
        for row in rows
    )


SAFETY_ARTIFACT_TABLE_NAMES: Final[tuple[str, ...]] = (
    "SAFE_SUBSTITUTION_PATTERNS",
    "CAPSTONE_SCAFFOLDS",
    "ACCESSIBILITY_REVIEW_STEPS",
    "PROCUREMENT_OVERSIGHT_STEPS",
    "HRIA_DPIA_WORKSHEET",
    "DATA_LINEAGE_REGISTRY",
    "ASSESSMENT_INTEGRITY_PROTOCOL",
    "AGENT_INCIDENT_RESPONSE_DRILL",
    "ROLE_BASED_COMPETENCY_MAP",
    "ADVERSARIAL_ASSURANCE_CYCLE",
    "MODEL_DATASET_CARD",
    "TRANSPARENCY_NOTICE_WORKFLOW",
    "RETENTION_AUDIT_TRAIL",
    "RELEASE_CHANGE_CONTROL_GATE",
    "RISK_EXCEPTION_MEMO",
    "LEARNER_SUPPORT_PLAN",
    "INSTRUCTOR_QUESTION_BANK",
)


@lru_cache(maxsize=1)
def coursebook_profiles_payload() -> list[dict[str, Any]]:
    """Return normalized coursebook profile rows from authoritative YAML."""
    payload = _load_yaml_mapping(_PROJECT_ROOT / "data" / "coursebook_profiles.yaml")
    profiles = payload.get("profiles", [])
    if not isinstance(profiles, list):
        raise ValueError("Expected list profiles in coursebook_profiles.yaml")
    rendered: list[dict[str, Any]] = []
    for row in profiles:
        if not isinstance(row, dict):
            raise ValueError("Expected mapping for each coursebook profile row")
        identifier = str(row["identifier"])
        vocabulary = tuple(
            (str(item["term"]), str(item["definition"])) for item in row["vocabulary"]
        )
        rendered.append(
            {
                "identifier": identifier,
                "disciplinary_frame": str(row["disciplinary_frame"]),
                "key_distinction": str(row["key_distinction"]),
                "vocabulary": vocabulary,
                "worked_scenario": str(row["worked_scenario"]),
                "worked_input": str(row["worked_input"]),
                "worked_process": str(row["worked_process"]),
                "worked_output": str(row["worked_output"]),
                "practice_focus": str(row["practice_focus"]),
                "review_question": str(row["review_question"]),
            }
        )
    return rendered


def validate_declarative_tables() -> dict[str, int]:
    """Validate authoritative YAML tables and return row counts for reporting."""
    profile_count = len(coursebook_profiles_payload())
    safety_payload = safety_artifact_tables_payload()
    risk_payload = topic_risk_routes_payload()
    counts = {name: len(safety_payload[name]) for name in SAFETY_ARTIFACT_TABLE_NAMES}
    counts["coursebook_profiles"] = profile_count
    counts["topic_risk_rules"] = len(risk_payload["topic_rules"])
    counts["topic_risk_chapter_rules"] = len(risk_payload["chapter_context_rules"])
    return counts


@lru_cache(maxsize=1)
def safety_artifact_tables_payload() -> dict[str, Any]:
    """Return safety and artifact table rows keyed by constant name."""
    payload = _load_yaml_mapping(_PROJECT_ROOT / "data" / "safety_artifact_tables.yaml")
    yaml_keys = set(payload)
    expected_keys = set(SAFETY_ARTIFACT_TABLE_NAMES)
    if yaml_keys != expected_keys:
        missing = expected_keys - yaml_keys
        extra = yaml_keys - expected_keys
        raise ValueError(
            "safety_artifact_tables.yaml key drift: "
            f"missing={sorted(missing)!r}; extra={sorted(extra)!r}"
        )
    return payload


def safety_artifact_table(name: str) -> tuple[dict[str, str], ...]:
    """Return one safety or artifact table as an immutable tuple of row dicts."""
    payload = safety_artifact_tables_payload()
    if name not in payload:
        raise KeyError(f"Unknown safety artifact table: {name}")
    rows = payload[name]
    if not isinstance(rows, list):
        raise ValueError(f"Expected list for safety artifact table {name!r}")
    return tuple(dict(row) for row in rows)
