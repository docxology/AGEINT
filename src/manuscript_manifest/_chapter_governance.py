"""Specific governance, audit, and quality assurance section renderers.

Extracted from _02_part.py so both modules remain comfortably under the 500-line limit.
"""

from __future__ import annotations

from typing import Any

from intelligence_content import (
    accessibility_review_rows,
    adversarial_assurance_rows,
    agent_incident_response_rows,
    assessment_integrity_rows,
    data_lineage_registry_rows,
    hria_dpia_worksheet_rows,
    learner_support_rows,
    model_dataset_card_rows,
    procurement_oversight_rows,
    question_bank_rows,
    release_change_control_rows,
    remediation_backlog_rows,
    retention_audit_rows,
    risk_exception_rows,
    role_competency_rows,
    transparency_notice_rows,
)

from ._01_part import _chapter_source_context


def _accessibility_udl_review(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Review for accessibility and Universal Design for Learning before reuse. {source_context}",
            "",
            accessibility_review_rows(),
            "",
            ("Minimum gate: no learner-facing artifact should depend on a single modality, unstated accommodation, inaccessible figure, unlabeled table, or hidden tool assumption."),
        ]
    )


def _procurement_vendor_oversight(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Treat any tool, dataset, platform, or service as a governed vendor input. {source_context}",
            "",
            procurement_oversight_rows(),
            "",
            ("Minimum gate: a classroom tool must be revocable, auditable, accessible, privacy-reviewed, and replaceable with a synthetic or instructor-provided substitute."),
        ]
    )


def _hria_dpia_worksheet(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Use this HRIA/DPIA worksheet when the work touches people, public services, education, or data reuse. {source_context}",
            "",
            hria_dpia_worksheet_rows(),
            "",
            ("Minimum gate: if a scenario cannot identify affected groups, safeguards, review owner, and residual risk, it stays at the discussion stage."),
        ]
    )


def _data_lineage_registry(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"The data lineage registry keeps claims, examples, prompts, and outputs traceable. {source_context}",
            "",
            data_lineage_registry_rows(),
            "",
            ("Minimum gate: every retained artifact names source identity, transformation, reviewer, sensitivity status, retention rule, and refresh owner."),
        ]
    )


def _assessment_integrity_protocol(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Assessment integrity depends on visible, bounded, and reviewable AI assistance. {source_context}",
            "",
            assessment_integrity_rows(),
            "",
            ("Minimum gate: learners may use agents only when tool use is declared, evidence is retained, independent reasoning is visible, and grading criteria remain human-reviewed."),
        ]
    )


def _agent_incident_response_drill(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Run an agent incident response drill using synthetic tickets and bounded logs. {source_context}",
            "",
            agent_incident_response_rows(),
            "",
            ("Minimum gate: the drill rehearses pause, revoke, preserve, review, recover, and debrief actions without touching live services or private data."),
        ]
    )


def _role_based_competency_map(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"The role-based competency map clarifies who must prove which skill. {source_context}",
            "",
            role_competency_rows(),
            "",
            ("Minimum gate: no artifact is accepted unless learner, instructor, source steward, assurance reviewer, and rights/procurement responsibilities are separable."),
        ]
    )


def _adversarial_assurance_cycle(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Use the adversarial assurance cycle to stress-test the work before classroom reuse. {source_context}",
            "",
            adversarial_assurance_rows(),
            "",
            ("Minimum gate: every challenge produces an owner, a remediation path, a retest result, and a source or safety refresh trigger."),
        ]
    )


def _model_dataset_documentation_card(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Use a model and dataset documentation card whenever the work relies on a model, dataset, example corpus, or synthetic fixture. {source_context}",
            "",
            model_dataset_card_rows(),
            "",
            (
                "Minimum gate: model and data claims must name intended use, excluded use, "
                "affected stakeholders, provenance, collection process, license or authority, "
                "composition limits, evaluation context, subgroup caveats, failure modes, "
                "lifecycle owner, rollback path, and refresh trigger."
            ),
        ]
    )


def _transparency_communication_notice(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"The transparency notice converts internal evidence into a plain-language accountability record. {source_context}",
            "",
            transparency_notice_rows(),
            "",
            ("Minimum gate: a learner, reviewer, or affected public audience can see purpose, authority, data summary, safeguards, human review, contact point, and publication limits."),
        ]
    )


def _records_retention_audit_trail(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"The records-retention and audit trail preserves enough evidence to review without retaining unnecessary sensitive material. {source_context}",
            "",
            retention_audit_rows(),
            "",
            ("Minimum gate: prompts, sources, decisions, exceptions, incidents, outputs, and remediation records have owners, retention rules, and deletion or refresh conditions."),
        ]
    )


def _release_change_control_gate(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Before an artifact is reused, pass it through a release and change-control gate. {source_context}",
            "",
            release_change_control_rows(),
            "",
            ("Minimum gate: scope, rights, security, version, rollback, monitoring, incident threshold, and post-release review are all visible."),
        ]
    )


def _risk_exception_acceptance_memo(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"If a gate cannot be satisfied, use a risk exception memo instead of silently lowering the standard. {source_context}",
            "",
            risk_exception_rows(),
            "",
            ("Minimum gate: exceptions are narrow, time-bound, evidence-backed, rights-reviewed, and closed by retest rather than left as permanent workarounds."),
        ]
    )


def _learner_support_accommodation_plan(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"The learner support and accommodation plan keeps access, cognitive load, and assessment fairness explicit. {source_context}",
            "",
            learner_support_rows(),
            "",
            ("Minimum gate: each learner-facing artifact has an access path, alternative means, allowed-tool statement, feedback path, and remediation owner."),
        ]
    )


def _instructor_question_bank(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"Use these instructor question prompts to deepen the work during facilitation and review. {source_context}",
            "",
            question_bank_rows(),
            "",
            ("Minimum gate: every question must produce a revision, retained evidence, or an explicit decision that no change is required."),
        ]
    )


def _remediation_backlog(chapter: dict[str, Any]) -> str:
    source_context = _chapter_source_context(chapter)
    return "\n".join(
        [
            f"The remediation backlog turns review findings into accountable follow-through. {source_context}",
            "",
            remediation_backlog_rows(),
            "",
            ("Minimum gate: backlog items have a trigger, owner, due date, closure evidence, and retest result before the artifact is reused."),
        ]
    )
