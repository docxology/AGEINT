"""Appendix body rendering for AGEINT generated manuscript sections."""

from __future__ import annotations

import re
from typing import Any

try:
    from ..intelligence_content import (
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
    title = str(appendix["title"])
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
            f"## {title} workbook scope: purpose, safety envelope, and reuse decision",
            "",
            f"### {title} operating purpose",
            (
                "The current appendix supports a reusable methods workbook. Each source item is "
                "treated as a reviewable classroom artifact rather than an operational instruction; "
                f"examples begin with {topic_context}."
            ),
            "",
            f"### {title} allowed-input boundary",
            (
                "Allowed inputs for the current appendix are public official or scholarly sources, "
                "standards text, instructor-provided excerpts, synthetic datasets, owned-lab logs, "
                f"toy examples, and generated rubrics that expose their provenance for {topic_context}."
            ),
            "",
            f"### {title} excluded-action boundary",
            (
                "Excluded actions for the current appendix are unauthorized collection, private-data "
                "processing, credential use, contact with real targets, live system interaction, "
                f"exploit execution, deception, unsafe cyber-physical action, or external deployment while handling {topic_context}."
            ),
            "",
            f"### {title} expected artifact package",
            (
                "Expected appendix artifacts are a purpose statement, allowed-inputs card, "
                "excluded-actions card, source-lane map, provenance record, claim ledger, "
                f"safe-substitution note, output schema, review rubric, and capstone handoff memo for {topic_context}."
            ),
            "",
            _safe_artifact_schema(title),
            "",
            _io_contract(title),
            "",
            _failure_cases(title),
            "",
            _evidence_package_schemas(title),
            "",
            _rubric_scoring_bands(title),
            "",
            _refresh_evidence(title),
            "",
            _validation_rubric(title),
            "",
            f"### {title} debrief protocol and reuse decision",
            (
                "Debrief by naming what the artifact can support, what it does not establish, what source "
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
    if letter == "D":
        return (
            "\n\n## MCP and AutoGen source boundary\n\n"
            "This appendix separates protocol claims, framework-pattern claims, and security "
            "claims before learners build any classroom artifact. MCP interoperability language "
            "is grounded in the version-pinned official specification; tool-consent, confused-"
            "deputy, token-handling, and least-privilege language is grounded in the official "
            "MCP security guidance and NSA security-design guidance. STIX/TAXII examples are "
            "treated as standards-governed data-exchange examples, not as permission to connect "
            "to external systems [@official_model_context_protocol_specification]; "
            "[@official_model_context_protocol_security_best_practices]; "
            "[@official_nsa_mcp_security_design_considerations]; "
            "[@official_oasis_stix_21]; [@official_oasis_taxii_21].\n\n"
            "AutoGen and multi-agent framework rows remain a safe-substitution exercise: the "
            "learner may compare orchestration patterns, sandbox policies, denied-action logs, "
            "and reviewer evidence, but may not run external code, contact live services, or "
            "treat framework names as assurance evidence. When the source guide supplies only "
            "framework or security context, this appendix records the limitation and routes "
            "normative claims back to the official protocol, standards, and security anchors "
            "rather than laundering them through an agent-generated summary [@ageint147]; "
            "[@ageint153]; [@ageint155]; [@ageint299]; [@ageint309]; [@ageint310]."
        )
    if letter == "E":
        return (
            "\n\n## Cryptographic standards boundary\n\n"
            "This appendix treats cryptography as an assurance and governance subject. "
            "Confidentiality, hashing, digital signatures, and key management are grounded in "
            "NIST standards and lifecycle guidance; classroom work may inspect properties, "
            "terminology, and review evidence, but it must not become operational secrecy, "
            "covert communications, evasion, or live key-management instruction "
            "[@official_nist_fips_197_aes]; [@official_nist_fips_180_4_shs]; "
            "[@official_nist_fips_186_5_dss]; "
            "[@official_nist_sp_800_57pt1r5_key_management].\n\n"
            "The source-guide material on dead drops and steganography is retained only as "
            "historical or detection-literacy context. A learner-facing artifact should map "
            "claim type to evidence type: standards for cryptographic properties, scholarly "
            "or official sources for evaluation claims, and explicit blocked-use notes for "
            "anything that could drift toward covert channels or uncontrolled deployment "
            "[@ageint027]; [@ageint028]; [@fig:appendix-crypto-assurance-methods]."
        )
    if letter == "G":
        return (
            "\n\n## Cognitive degradation as a staged cascade\n\n"
            "The Cloud Security Alliance Cognitive Degradation Resilience model treats an attack on an "
            "agent network not as a single breach but as a six-stage slide that stays below conventional "
            "alerting thresholds, illustrated for this appendix in [@fig:ageint-cdr-degradation-cascade]. "
            "Stage one is trigger injection, where adversarial inputs win a foothold in agent reasoning; "
            "stage two is resource starvation, in which context windows and compute are deliberately "
            "consumed to degrade decision quality; stage three is behavioral drift, where outputs deviate "
            "from policy without tripping alerts; stage four is memory entrenchment, where corrupted "
            "beliefs solidify in agent memory stores; stage five is functional override, where adversary "
            "objectives supersede the legitimate task; and stage six is systemic collapse, where "
            "coordinated agent behavior serves adversarial ends. The decisive observation is that the "
            "intervention window opens early -- between resource starvation and behavioral drift -- "
            "because once beliefs entrench in memory, remediation cost rises sharply "
            "[@official_csa_cdr_framework].\n\n"
            "Each stage is paired in the QSAF-BC control set with a named, testable countermeasure rather "
            "than a single catch-all monitor: starvation detection (BC-001) and token-overload limits (BC-002) "
            "defend the early stages, an entropy-drift monitor (BC-006) and a memory-integrity check "
            "(BC-007) defend the middle, and override resistance (BC-005) defends the late stages. Treat "
            "this cascade as a classroom tabletop: map a synthetic incident onto the six stages, identify "
            "which control would have fired first, and record the evidence a reviewer would need to "
            "confirm the agent recovered [@official_csa_securing_autonomous_ai_agents]; "
            "[@scholarly_agentic_ai_security_survey].\n\n"
            "## The decoherence-degradation isomorphism\n\n"
            "The same dynamic appears one scale up. The CCDCOE reconception of cognitive warfare "
            "describes how an adversary degrades a human organization by attacking systemic invariants "
            "-- shared trust, identity, and epistemic standards -- driving it through initiation, "
            "uncertainty amplification, polarization, hardened competing frameworks, narrative capture, "
            "and a final state where the institution functions formally but can no longer coordinate. As "
            "[@fig:ageint-cognitive-decoherence-cdr-isomorphism] makes explicit, those six "
            "human-organization phases map one-to-one onto the CDR degradation stages in an agent "
            "network, phase for phase from initiation to collapse "
            "[@scholarly_ccdcoe_cognitive_warfare_reconception]. The pedagogical payoff is that a single "
            "defensive vocabulary -- early detection, drift monitoring, integrity of stored belief -- "
            "transfers across both the human and the machine layer, which is why this appendix teaches "
            "them together rather than as separate disciplines."
        )
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


def _safe_artifact_schema(title: str) -> str:
    return "\n".join(
        [
            f"### {title} safe artifact schema",
            "| Field | Required evidence | Reject condition |",
            "|---|---|---|",
            "| Purpose | lawful educational, governance, research, or defensive purpose | vague operational objective or missing authority |",
            "| Inputs | public, official, scholarly, synthetic, owned-lab, or instructor-provided material | private data, live target data, credentialed access, or unclear provenance |",
            "| Transform | summary, comparison, rubric scoring, tabletop simulation, or audit review | collection expansion, external action, or unsafe system interaction |",
            "| Output | memo, matrix, checklist, ledger, rubric, or debrief packet | deployable procedure, target package, or automated action plan |",
            "| Reviewer | human reviewer, approval gate, revision note, and refresh owner | anonymous ownership or no escalation path |",
        ]
    )


def _io_contract(title: str) -> str:
    return "\n".join(
        [
            f"### {title} input/output contract",
            "| Contract term | Input rule | Output rule |",
            "|---|---|---|",
            "| Source identity | retain `ageintNNN`, title, URL, and checked status | cite with Pandoc keys and avoid pasted raw URLs in prose |",
            "| Accessibility | include plain-language labels, table headers, and figure alternatives | reject inaccessible figures, unlabeled tables, or single-modality evidence |",
            "| Rights | identify affected groups, safeguards, and residual risk | preserve privacy, equality, access, contestability, and redress notes |",
            "| Tooling | use allowlisted tools, visible prompts, logs, and stop conditions | keep outputs non-operational, reversible, and human-reviewed |",
            "| Refresh | record source, policy, standard, incident, or assessment trigger | assign an owner and date for revalidation |",
        ]
    )


def _failure_cases(title: str) -> str:
    return "\n".join(
        [
            f"### {title} failure cases and required responses",
            "| Failure case | Signal | Required response |",
            "|---|---|---|",
            "| Source laundering | claim cites an agent summary instead of a verified source | rebuild the claim ledger from direct sources |",
            "| Boundary drift | exercise starts asking for live targets, private data, or external action | stop, substitute synthetic inputs, and document the block |",
            "| Accessibility gap | learner cannot inspect, navigate, or complete the artifact | remediate and retest before reuse |",
            "| Rights gap | affected group, safeguard, or redress path is missing | run HRIA/DPIA worksheet and escalate unresolved risk |",
            "| Vendor opacity | tool owner, data use, logs, or exit path is unknown | replace tool or pause until procurement evidence exists |",
        ]
    )


def _evidence_package_schemas(title: str) -> str:
    return "\n\n".join(
        [
            f"### {title} evidence package schemas",
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


def _rubric_scoring_bands(title: str) -> str:
    return "\n".join(
        [
            f"### {title} rubric scoring bands",
            "| Band | Evidence standard | Disposition |",
            "|---|---|---|",
            "| 4 - ready | source identity, accessibility, rights, safety, and reviewer evidence are complete | may be reused after normal refresh review |",
            "| 3 - revise | one evidence field is incomplete but risk is bounded and remediable | revise before reuse |",
            "| 2 - hold | multiple evidence fields are incomplete or ownership is unclear | hold for instructor and assurance review |",
            "| 1 - reject | unsafe action, private data, inaccessible artifact, or unverified claim appears | reject and rebuild from safe inputs |",
        ]
    )


def _refresh_evidence(title: str) -> str:
    return "\n".join(
        [
            f"### {title} refresh evidence",
            "| Evidence item | Refresh trigger | Retained support |",
            "|---|---|---|",
            "| Source lane | official source, standard, or legal text changes | checked-as-of date and source note |",
            "| Safety treatment | operational wording or unsafe motif appears | safe-substitution decision and blocked context |",
            "| Accessibility | WCAG, UDL, or institutional accessibility duty changes | defect log, retest result, and owner |",
            "| Rights | privacy, human-rights, public transparency, or education guidance changes | HRIA/DPIA revision note |",
            "| Vendor/tool | contract, data-use, incident, or model capability changes | procurement packet and incident review |",
        ]
    )


def _validation_rubric(title: str) -> str:
    return "\n".join(
        [
            f"### {title} validation rubric",
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
