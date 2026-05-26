"""Appendix body rendering for AGEINT generated manuscript sections."""

from __future__ import annotations

import re
from typing import Any

try:
    from ..intelligence_content import (
        accessibility_review_rows,
        adversarial_assurance_rows,
        assessment_integrity_rows,
        capstone_scaffold_rows,
        data_lineage_registry_rows,
        hria_dpia_worksheet_rows,
        learner_support_rows,
        model_dataset_card_rows,
        question_bank_rows,
        release_change_control_rows,
        remediation_backlog_rows,
        retention_audit_rows,
        risk_exception_rows,
        safe_substitution_rows,
        source_lane_rows,
        transparency_notice_rows,
    )
except ImportError:  # pragma: no cover - exercised by script-level imports
    from intelligence_content import (  # type: ignore[no-redef]
        accessibility_review_rows,
        adversarial_assurance_rows,
        assessment_integrity_rows,
        capstone_scaffold_rows,
        data_lineage_registry_rows,
        hria_dpia_worksheet_rows,
        learner_support_rows,
        model_dataset_card_rows,
        question_bank_rows,
        release_change_control_rows,
        remediation_backlog_rows,
        retention_audit_rows,
        risk_exception_rows,
        safe_substitution_rows,
        source_lane_rows,
        transparency_notice_rows,
    )


def appendix_body(appendix: dict[str, Any]) -> str:
    """Return the generated methods-workbook body for an appendix."""

    letter = appendix["letter"]
    topic_context = _appendix_topic_context(appendix)
    specialized = _specialized_appendix_body(letter)
    return "\n".join(
        [
            (
                "The current appendix is an evidence workbook for reusable classroom methods. "
                "It is educational and non-operational: examples remain synthetic, defensive, "
                "lawful, and bounded to owned labs, public sources, or tabletop exercises. "
                f"Source-item focus: {topic_context}."
            ),
            "",
            "## Purpose",
            (
                "The current appendix supports a reusable methods workbook. Each source item is "
                "treated as a reviewable classroom artifact rather than an operational instruction; "
                f"examples begin with {topic_context}."
            ),
            "",
            "## Allowed inputs",
            (
                "Allowed inputs for the current appendix are public official or scholarly sources, "
                "standards text, instructor-provided excerpts, synthetic datasets, owned-lab logs, "
                f"toy examples, and generated rubrics that expose their provenance for {topic_context}."
            ),
            "",
            "## Excluded actions",
            (
                "Excluded actions for the current appendix are unauthorized collection, private-data "
                "processing, credential use, contact with real targets, live system interaction, "
                f"exploit execution, deception, unsafe cyber-physical action, or external deployment while handling {topic_context}."
            ),
            "",
            "## Expected artifacts",
            (
                "Expected appendix artifacts are a purpose statement, allowed-inputs card, "
                "excluded-actions card, source-lane map, provenance record, claim ledger, "
                f"safe-substitution note, output schema, review rubric, and capstone handoff memo for {topic_context}."
            ),
            "",
            _safe_artifact_schema(),
            "",
            _io_contract(),
            "",
            _failure_cases(),
            "",
            _evidence_package_schemas(),
            "",
            _rubric_scoring_bands(),
            "",
            _refresh_evidence(),
            "",
            _validation_rubric(),
            "",
            "## Debrief protocol",
            (
                "Debrief by naming what the artifact proves, what it does not prove, what source "
                "changed, what risk was avoided by safe substitution, what human approval is still "
                f"required, and when the appendix should be refreshed for {topic_context}."
            ),
            "",
            specialized.strip(),
        ]
    ).strip()


def _appendix_topic_context(appendix: dict[str, Any], *, limit: int = 2) -> str:
    titles = [
        re.sub(r"^[A-Z]\.\d+\s+", "", str(item.get("title", "")).strip())
        for item in appendix.get("items", [])[:limit]
    ]
    titles = [title for title in titles if title]
    return "; ".join(titles) if titles else "the appendix source-item set"


def _specialized_appendix_body(letter: str) -> str:
    if letter == "H":
        return (
            "\n\n## Source verification workflow\n\n"
            "The source-verification and claim-ledger workbook preserves `ageint001` through "
            "`ageint231`, appends new references after the locked range, and records lane, tier, "
            "checked date, verification method, claim scope, refresh cadence, and refresh trigger "
            "for every curated anchor.\n\n"
            f"{source_lane_rows()}\n\n"
            "## Source refresh evidence\n\n"
            f"{data_lineage_registry_rows()}\n\n"
            "## HRIA/DPIA evidence bridge\n\n"
            f"{hria_dpia_worksheet_rows()}"
        )
    if letter == "I":
        return (
            "\n\n## Instructor capstone workflow\n\n"
            "The instructor capstone, rubric, and red-team review pack binds each student artifact "
            "to source verification, safe substitution, rights review, assurance, and debrief evidence.\n\n"
            f"{capstone_scaffold_rows()}\n\n"
            "## Safe artifact rows\n\n"
            f"{safe_substitution_rows()}\n\n"
            "## Assessment lifecycle evidence\n\n"
            f"{assessment_integrity_rows()}\n\n"
            "## Adversarial review evidence\n\n"
            f"{adversarial_assurance_rows()}"
        )
    return ""


def _safe_artifact_schema() -> str:
    return "\n".join(
        [
            "## Safe artifact schema",
            "| Field | Required evidence | Reject condition |",
            "|---|---|---|",
            "| Purpose | lawful educational, governance, research, or defensive purpose | vague operational objective or missing authority |",
            "| Inputs | public, official, scholarly, synthetic, owned-lab, or instructor-provided material | private data, live target data, credentialed access, or unclear provenance |",
            "| Transform | summary, comparison, rubric scoring, tabletop simulation, or audit review | collection expansion, external action, or unsafe system interaction |",
            "| Output | memo, matrix, checklist, ledger, rubric, or debrief packet | deployable procedure, target package, or automated action plan |",
            "| Reviewer | human reviewer, approval gate, revision note, and refresh owner | anonymous ownership or no escalation path |",
        ]
    )


def _io_contract() -> str:
    return "\n".join(
        [
            "## Input/output contract",
            "| Contract term | Input rule | Output rule |",
            "|---|---|---|",
            "| Source identity | retain `ageintNNN`, title, URL, and checked status | cite with Pandoc keys and avoid pasted raw URLs in prose |",
            "| Accessibility | include plain-language labels, table headers, and figure alternatives | reject inaccessible figures, unlabeled tables, or single-modality evidence |",
            "| Rights | identify affected groups, safeguards, and residual risk | preserve privacy, equality, access, contestability, and redress notes |",
            "| Tooling | use allowlisted tools, visible prompts, logs, and stop conditions | keep outputs non-operational, reversible, and human-reviewed |",
            "| Refresh | record source, policy, standard, incident, or assessment trigger | assign an owner and date for revalidation |",
        ]
    )


def _failure_cases() -> str:
    return "\n".join(
        [
            "## Failure cases",
            "| Failure case | Signal | Required response |",
            "|---|---|---|",
            "| Source laundering | claim cites an agent summary instead of a verified source | rebuild the claim ledger from direct sources |",
            "| Boundary drift | exercise starts asking for live targets, private data, or external action | stop, substitute synthetic inputs, and document the block |",
            "| Accessibility gap | learner cannot inspect, navigate, or complete the artifact | remediate and retest before reuse |",
            "| Rights gap | affected group, safeguard, or redress path is missing | run HRIA/DPIA worksheet and escalate unresolved risk |",
            "| Vendor opacity | tool owner, data use, logs, or exit path is unknown | replace tool or pause until procurement evidence exists |",
        ]
    )


def _evidence_package_schemas() -> str:
    return "\n\n".join(
        [
            "## Evidence package schemas",
            "Model and dataset card:",
            model_dataset_card_rows(),
            "Transparency notice:",
            transparency_notice_rows(),
            "Records retention and audit trail:",
            retention_audit_rows(),
            "Release and change-control gate:",
            release_change_control_rows(),
            "Risk exception memo:",
            risk_exception_rows(),
            "Learner support and accommodation plan:",
            learner_support_rows(),
            "Instructor question bank:",
            question_bank_rows(),
            "Remediation backlog:",
            remediation_backlog_rows(),
        ]
    )


def _rubric_scoring_bands() -> str:
    return "\n".join(
        [
            "## Rubric scoring bands",
            "| Band | Evidence standard | Disposition |",
            "|---|---|---|",
            "| 4 - ready | source identity, accessibility, rights, safety, and reviewer evidence are complete | may be reused after normal refresh review |",
            "| 3 - revise | one evidence field is incomplete but risk is bounded and remediable | revise before reuse |",
            "| 2 - hold | multiple evidence fields are incomplete or ownership is unclear | hold for instructor and assurance review |",
            "| 1 - reject | unsafe action, private data, inaccessible artifact, or unverified claim appears | reject and rebuild from safe inputs |",
        ]
    )


def _refresh_evidence() -> str:
    return "\n".join(
        [
            "## Refresh evidence",
            "| Evidence item | Refresh trigger | Retained proof |",
            "|---|---|---|",
            "| Source lane | official source, standard, or legal text changes | checked-as-of date and source note |",
            "| Safety treatment | operational wording or unsafe motif appears | safe-substitution decision and blocked context |",
            "| Accessibility | WCAG, UDL, or institutional accessibility duty changes | defect log, retest result, and owner |",
            "| Rights | privacy, human-rights, public transparency, or education guidance changes | HRIA/DPIA revision note |",
            "| Vendor/tool | contract, data-use, incident, or model capability changes | procurement packet and incident review |",
        ]
    )


def _validation_rubric() -> str:
    return "\n".join(
        [
            "## Validation rubric",
            "| Criterion | Passing evidence |",
            "|---|---|",
            "| Source identity | existing `ageintNNN` keys remain stable or new references are append-only |",
            "| Verification | official, standards, public-domain, or scholarly URL is checked directly |",
            "| Safety | method is converted into tabletop, audit, governance, or synthetic-data treatment |",
            "| Reproducibility | another reviewer can rebuild the artifact from retained inputs |",
            "| Rights review | privacy, IP, human-rights, workforce, and education impacts are considered where relevant |",
        ]
    )


__all__ = ["appendix_body"]
