"""Canonical claim-class lanes for AGEINT analysis validation."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class AnalysisValidationLane:
    """One claim class that must remain visible in prose, audit, and figures."""

    claim_class: str
    validation_question: str
    required_evidence: str
    failure_mode: str
    matrix_evidence: str
    matrix_question: str
    matrix_failure: str


@dataclass(frozen=True)
class AnalysisValidationFamilyLane:
    """One generated manuscript family mapped to its review lane."""

    manuscript_family: str
    claim_class: str
    evidence_signal: str
    failure_signal: str


ANALYSIS_VALIDATION_LANES: tuple[AnalysisValidationLane, ...] = (
    AnalysisValidationLane(
        claim_class="Design guidance",
        validation_question="Is the claim framed as proposed guidance rather than measured performance?",
        required_evidence="source-family support, caveat, and bounded conclusion",
        failure_mode="architecture prose is promoted into empirical proof",
        matrix_evidence="source family, caveat, bounded conclusion",
        matrix_question="guidance or measured performance?",
        matrix_failure="architecture prose becomes proof",
    ),
    AnalysisValidationLane(
        claim_class="Empirical or evaluation claim",
        validation_question="Does a cited study, metric, benchmark, or evaluation source directly support the claim?",
        required_evidence="method source, limitation note, and refresh trigger",
        failure_mode="measured language appears without direct evaluation evidence",
        matrix_evidence="study, metric, limitation, refresh trigger",
        matrix_question="direct evaluation support?",
        matrix_failure="measured language without evidence",
    ),
    AnalysisValidationLane(
        claim_class="Governance or rights claim",
        validation_question="Which law, standard, public guidance, or rights-impact source constrains the advice?",
        required_evidence="source lane, affected group, owner, residual risk",
        failure_mode="compliance language appears as unsupported assurance",
        matrix_evidence="law, standard, owner, residual risk",
        matrix_question="which constraint governs?",
        matrix_failure="unsupported compliance assurance",
    ),
    AnalysisValidationLane(
        claim_class="Figure or visualization claim",
        validation_question="Does the visual carry readable text, alt text, provenance, and an inspectable source section?",
        required_evidence="registry row, PNG metadata, caption, long description",
        failure_mode="a figure works only as decoration or inaccessible evidence",
        matrix_evidence="registry, caption, alt text, PNG metadata",
        matrix_question="readable and inspectable?",
        matrix_failure="decorative or inaccessible visual",
    ),
    AnalysisValidationLane(
        claim_class="Artifact readiness claim",
        validation_question="Are manuscript, citations, figures, references, and PDF links from the same rebuild?",
        required_evidence="artifact-evidence manifest, rendered-reference audit, PDF audit",
        failure_mode="stale output or Markdown-file links certify as ready",
        matrix_evidence="fresh build, reference audit, PDF audit",
        matrix_question="same rebuilt artifact set?",
        matrix_failure="stale output certifies as ready",
    ),
    AnalysisValidationLane(
        claim_class="Reviewer disposition",
        validation_question="What would make this row pass, warn, fail, or reopen?",
        required_evidence="negative control, closure evidence, task owner",
        failure_mode="a green check hides the decision rule",
        matrix_evidence="negative control, owner, closure evidence",
        matrix_question="pass, warn, fail, or reopen?",
        matrix_failure="green check hides decision rule",
    ),
)

ANALYSIS_VALIDATION_FAMILY_LANES: tuple[AnalysisValidationFamilyLane, ...] = (
    AnalysisValidationFamilyLane(
        manuscript_family="overview",
        claim_class="Design guidance",
        evidence_signal="chapter primer, scope caveat, source-family support",
        failure_signal="orientation guidance reads as measured performance",
    ),
    AnalysisValidationFamilyLane(
        manuscript_family="part unit intros",
        claim_class="Design guidance",
        evidence_signal="unit profile, chapter roster, bounded reuse language",
        failure_signal="part-level framing becomes unsupported generalization",
    ),
    AnalysisValidationFamilyLane(
        manuscript_family="practice-studio",
        claim_class="Design guidance",
        evidence_signal="topic-specific lessons, safe example, source spines, safe substitutions",
        failure_signal="practice studio prose becomes generic or operational",
    ),
    AnalysisValidationFamilyLane(
        manuscript_family="evidence-contract",
        claim_class="Empirical or evaluation claim",
        evidence_signal="source annotations, transfer architecture, method limits, current anchor metadata",
        failure_signal="evidence contract implies unsupported empirical proof",
    ),
    AnalysisValidationFamilyLane(
        manuscript_family="governance-boundary",
        claim_class="Governance or rights claim",
        evidence_signal="synthesis, agent boundary, policy lane, owner, residual-risk and refresh duty",
        failure_signal="governance boundary becomes assurance without authority",
    ),
    AnalysisValidationFamilyLane(
        manuscript_family="assessment-route",
        claim_class="Reviewer disposition",
        evidence_signal="rubric row, pass/warn/fail criteria, negative control",
        failure_signal="review outcome lacks decision rule",
    ),
    AnalysisValidationFamilyLane(
        manuscript_family="method-assurance-reference.md",
        claim_class="Artifact readiness claim",
        evidence_signal="render, reference, PDF, figure, and report gates",
        failure_signal="method claim survives without fresh artifact evidence",
    ),
)


def analysis_validation_matrix_rows() -> tuple[tuple[str, tuple[str, str, str]], ...]:
    """Return compact rows for the rendered validation matrix."""
    return tuple(
        (
            lane.claim_class,
            (lane.matrix_evidence, lane.matrix_question, lane.matrix_failure),
        )
        for lane in ANALYSIS_VALIDATION_LANES
    )


def analysis_validation_family_rows() -> tuple[tuple[str, tuple[str, str, str]], ...]:
    """Return compact rows for the manuscript-family coverage visual."""
    return tuple(
        (
            row.manuscript_family,
            (row.claim_class, row.evidence_signal, row.failure_signal),
        )
        for row in ANALYSIS_VALIDATION_FAMILY_LANES
    )


def analysis_validation_family_figure_rows() -> tuple[tuple[str, tuple[str, str, str]], ...]:
    """Return display rows that preserve lane meaning while fitting figure cells."""
    display_cells = {
        "overview": ("Design guidance", "chapter primer; scope caveat; source mix", "guidance becomes performance claim"),
        "part unit intros": ("Design guidance", "unit profile; chapter roster; bounded reuse", "part framing overgeneralizes"),
        "practice-studio": ("Design guidance", "topic lessons; safe examples; source spines", "studio becomes generic or operational"),
        "evidence-contract": (
            "Empirical or evaluation claim",
            "source notes; method limits; anchor metadata",
            "summary implies unsupported proof",
        ),
        "governance-boundary": (
            "Governance or rights claim",
            "policy lane; owner; risk refresh",
            "governance prose becomes assurance",
        ),
        "assessment-route": ("Reviewer disposition", "rubric row; criteria; negative control", "review lacks decision rule"),
        "method-assurance-reference.md": (
            "Artifact readiness claim",
            "render; refs; PDF; artifact gates",
            "method claim lacks fresh artifact evidence",
        ),
    }
    return tuple((row.manuscript_family, display_cells[row.manuscript_family]) for row in ANALYSIS_VALIDATION_FAMILY_LANES)


def analysis_validation_family_lane_map() -> dict[str, AnalysisValidationFamilyLane]:
    """Return manuscript family to analysis-validation lane metadata."""
    return {row.manuscript_family: row for row in ANALYSIS_VALIDATION_FAMILY_LANES}


def analysis_validation_contract_terms() -> tuple[str, ...]:
    """Return all lane terms the scholarship audit must find in orientation prose."""
    terms: list[str] = []
    for lane in ANALYSIS_VALIDATION_LANES:
        terms.extend(
            [
                lane.claim_class,
                lane.validation_question,
                lane.required_evidence,
                lane.failure_mode,
            ]
        )
    return tuple(terms)


__all__ = [
    "ANALYSIS_VALIDATION_FAMILY_LANES",
    "ANALYSIS_VALIDATION_LANES",
    "AnalysisValidationFamilyLane",
    "AnalysisValidationLane",
    "analysis_validation_contract_terms",
    "analysis_validation_family_figure_rows",
    "analysis_validation_family_lane_map",
    "analysis_validation_family_rows",
    "analysis_validation_matrix_rows",
]
