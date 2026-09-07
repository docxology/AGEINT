"""Renderers for safety and artifact tables loaded from declarative YAML.

Extracted from _09_part.py so both modules remain comfortably under the 500-line cap.
"""

from __future__ import annotations

from typing import Final

from ._08_part import (
    ACCESSIBILITY_REVIEW_STEPS,
    ADVERSARIAL_ASSURANCE_CYCLE,
    AGENT_INCIDENT_RESPONSE_DRILL,
    ASSESSMENT_INTEGRITY_PROTOCOL,
    CAPSTONE_SCAFFOLDS,
    DATA_LINEAGE_REGISTRY,
    HRIA_DPIA_WORKSHEET,
    INSTRUCTOR_QUESTION_BANK,
    LEARNER_SUPPORT_PLAN,
    MODEL_DATASET_CARD,
    PROCUREMENT_OVERSIGHT_STEPS,
    RELEASE_CHANGE_CONTROL_GATE,
    RETENTION_AUDIT_TRAIL,
    RISK_EXCEPTION_MEMO,
    ROLE_BASED_COMPETENCY_MAP,
    SAFE_SUBSTITUTION_PATTERNS,
    TRANSPARENCY_NOTICE_WORKFLOW,
)
from .markdown_table import render_dict_table


REMEDIATION_BACKLOG: Final[tuple[dict[str, str], ...]] = (
    {"item": "Unverified claim", "trigger": "claim lacks a guide citation or directly verified anchor", "closure_evidence": "verified source, removed claim, or explicit source-guide context note"},
    {
        "item": "Unsafe phrasing",
        "trigger": "wording implies live targeting, external action, exploitation, manipulation, or unsafe control",
        "closure_evidence": "safe substitute, blocked context, and reviewer sign-off",
    },
    {
        "item": "Accessibility defect",
        "trigger": "artifact cannot be inspected through an expected assistive or alternative workflow",
        "closure_evidence": "defect fix, alternative means, and retest result",
    },
    {"item": "Assurance gap", "trigger": "evaluation, release, exception, incident, or vendor evidence is incomplete", "closure_evidence": "owner, due date, retest, and accepted disposition"},
)


def safe_substitution_rows() -> str:
    """Render risky source motif to safe curriculum substitute rows."""
    return render_dict_table(
        ("Source motif", "Unsafe source motif", "Safe curriculum substitute", "Blocked context"), SAFE_SUBSTITUTION_PATTERNS, ("motif", "source_risk", "substitute", "blocked_context")
    )


def capstone_scaffold_rows() -> str:
    """Render reusable capstone workflow rows."""
    return render_dict_table(("Phase", "Artifact", "Review gate"), CAPSTONE_SCAFFOLDS, ("phase", "artifact", "review_gate"))


def accessibility_review_rows() -> str:
    """Render accessibility and UDL review rows."""
    return render_dict_table(("Step", "Artifact", "Review question"), ACCESSIBILITY_REVIEW_STEPS, ("step", "artifact", "review_question"))


def procurement_oversight_rows() -> str:
    """Render procurement and vendor oversight rows."""
    return render_dict_table(("Step", "Artifact", "Review question"), PROCUREMENT_OVERSIGHT_STEPS, ("step", "artifact", "review_question"))


def hria_dpia_worksheet_rows() -> str:
    """Render HRIA and DPIA worksheet rows."""
    return render_dict_table(("Dimension", "Prompt", "Evidence"), HRIA_DPIA_WORKSHEET, ("dimension", "prompt", "evidence"))


def data_lineage_registry_rows() -> str:
    """Render data lineage registry rows."""
    return render_dict_table(("Object", "Lineage field", "Quality gate"), DATA_LINEAGE_REGISTRY, ("object", "lineage_field", "quality_gate"))


def assessment_integrity_rows() -> str:
    """Render assessment integrity rows."""
    return render_dict_table(("Control", "Student evidence", "Instructor check"), ASSESSMENT_INTEGRITY_PROTOCOL, ("control", "student_evidence", "instructor_check"))


def agent_incident_response_rows() -> str:
    """Render agent incident response drill rows."""
    return render_dict_table(("Phase", "Drill action", "Artifact"), AGENT_INCIDENT_RESPONSE_DRILL, ("phase", "drill_action", "artifact"))


def role_competency_rows() -> str:
    """Render role-based competency rows."""
    return render_dict_table(("Role", "Competency", "Evidence"), ROLE_BASED_COMPETENCY_MAP, ("role", "competency", "evidence"))


def adversarial_assurance_rows() -> str:
    """Render adversarial assurance cycle rows."""
    return render_dict_table(("Stage", "Challenge question", "Artifact"), ADVERSARIAL_ASSURANCE_CYCLE, ("stage", "question", "artifact"))


def model_dataset_card_rows() -> str:
    """Render model and dataset documentation card rows."""
    return render_dict_table(("Field", "Model card evidence", "Dataset card evidence", "Review gate"), MODEL_DATASET_CARD, ("field", "model_card", "dataset_card", "review_gate"))


def transparency_notice_rows() -> str:
    """Render transparency and public notice rows."""
    return render_dict_table(("Step", "Artifact", "Review gate"), TRANSPARENCY_NOTICE_WORKFLOW, ("step", "artifact", "review_gate"))


def retention_audit_rows() -> str:
    """Render records retention and audit trail rows."""
    return render_dict_table(("Record", "Retained fields", "Audit requirement"), RETENTION_AUDIT_TRAIL, ("record", "retained_fields", "audit_question"))


def release_change_control_rows() -> str:
    """Render release and change-control gate rows."""
    return render_dict_table(("Gate", "Release evidence", "Block condition"), RELEASE_CHANGE_CONTROL_GATE, ("gate", "release_evidence", "block_condition"))


def risk_exception_rows() -> str:
    """Render risk-exception memo rows."""
    return render_dict_table(("Field", "Minimum content", "Approval rule"), RISK_EXCEPTION_MEMO, ("field", "minimum_content", "approval_rule"))


def learner_support_rows() -> str:
    """Render learner support plan rows."""
    return render_dict_table(("Need", "Support", "Evidence"), LEARNER_SUPPORT_PLAN, ("need", "support", "evidence"))


def question_bank_rows() -> str:
    """Render instructor question bank rows."""
    return render_dict_table(("Question type", "Prompt", "Evidence"), INSTRUCTOR_QUESTION_BANK, ("question_type", "prompt", "evidence"))


def remediation_backlog_rows() -> str:
    """Render remediation backlog rows."""
    return render_dict_table(("Backlog item", "Trigger", "Closure evidence"), REMEDIATION_BACKLOG, ("item", "trigger", "closure_evidence"))
