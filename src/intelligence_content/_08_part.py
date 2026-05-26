from __future__ import annotations

"""Safety and artifact table rows loaded from declarative YAML."""

from typing import Final

from _data_loaders import safety_artifact_table

SAFE_SUBSTITUTION_PATTERNS: Final[tuple[dict[str, str], ...]] = safety_artifact_table(
    "SAFE_SUBSTITUTION_PATTERNS"
)
CAPSTONE_SCAFFOLDS: Final[tuple[dict[str, str], ...]] = safety_artifact_table("CAPSTONE_SCAFFOLDS")
ACCESSIBILITY_REVIEW_STEPS: Final[tuple[dict[str, str], ...]] = safety_artifact_table(
    "ACCESSIBILITY_REVIEW_STEPS"
)
PROCUREMENT_OVERSIGHT_STEPS: Final[tuple[dict[str, str], ...]] = safety_artifact_table(
    "PROCUREMENT_OVERSIGHT_STEPS"
)
HRIA_DPIA_WORKSHEET: Final[tuple[dict[str, str], ...]] = safety_artifact_table("HRIA_DPIA_WORKSHEET")
DATA_LINEAGE_REGISTRY: Final[tuple[dict[str, str], ...]] = safety_artifact_table("DATA_LINEAGE_REGISTRY")
ASSESSMENT_INTEGRITY_PROTOCOL: Final[tuple[dict[str, str], ...]] = safety_artifact_table(
    "ASSESSMENT_INTEGRITY_PROTOCOL"
)
AGENT_INCIDENT_RESPONSE_DRILL: Final[tuple[dict[str, str], ...]] = safety_artifact_table(
    "AGENT_INCIDENT_RESPONSE_DRILL"
)
ROLE_BASED_COMPETENCY_MAP: Final[tuple[dict[str, str], ...]] = safety_artifact_table(
    "ROLE_BASED_COMPETENCY_MAP"
)
ADVERSARIAL_ASSURANCE_CYCLE: Final[tuple[dict[str, str], ...]] = safety_artifact_table(
    "ADVERSARIAL_ASSURANCE_CYCLE"
)
MODEL_DATASET_CARD: Final[tuple[dict[str, str], ...]] = safety_artifact_table("MODEL_DATASET_CARD")
TRANSPARENCY_NOTICE_WORKFLOW: Final[tuple[dict[str, str], ...]] = safety_artifact_table(
    "TRANSPARENCY_NOTICE_WORKFLOW"
)
RETENTION_AUDIT_TRAIL: Final[tuple[dict[str, str], ...]] = safety_artifact_table("RETENTION_AUDIT_TRAIL")
RELEASE_CHANGE_CONTROL_GATE: Final[tuple[dict[str, str], ...]] = safety_artifact_table(
    "RELEASE_CHANGE_CONTROL_GATE"
)
RISK_EXCEPTION_MEMO: Final[tuple[dict[str, str], ...]] = safety_artifact_table("RISK_EXCEPTION_MEMO")
LEARNER_SUPPORT_PLAN: Final[tuple[dict[str, str], ...]] = safety_artifact_table("LEARNER_SUPPORT_PLAN")
INSTRUCTOR_QUESTION_BANK: Final[tuple[dict[str, str], ...]] = safety_artifact_table("INSTRUCTOR_QUESTION_BANK")
