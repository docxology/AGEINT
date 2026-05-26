#!/usr/bin/env python3
"""One-shot generator for data/topic_prompt_routes.yaml from canonical prompt tables."""

from __future__ import annotations

from pathlib import Path

import yaml

EVIDENCE_CATEGORY_PROMPTS: dict[str, str] = {
    "agentic_cyber_misuse": (
        "Evidence packet: sample prompt records, tool-call logs, blocked-action records, and the policy that denies the unsafe request."
    ),
    "historical_humint_source_protection": (
        "Evidence packet: release metadata, redaction caveats, institutional setting, and the governance lesson that can be defended from the record."
    ),
    "ics_evasion_coverage": (
        "Evidence packet: synthetic alert records, expected operator observations, control coverage, and recovery notes."
    ),
    "ics_collection_detection": (
        "Evidence packet: synthetic tag histories, approved observation points, operator annotations, and detection gaps."
    ),
    "software_supply_chain_social_trust": (
        "Evidence packet: package provenance, maintainer-trust signals, build-integrity evidence, and uncertainty about attribution."
    ),
    "osint_tool_governance": (
        "Evidence packet: terms of use, source provenance, reproducibility notes, minimization decisions, and identity-exposure risks."
    ),
    "humint_recruitment_risk": (
        "Evidence packet: sample source notes for pressure, consent, escalation duties, and excluded contact actions."
    ),
    "cyber_taxonomy": (
        "Evidence packet: fabricated alerts, published taxonomy labels, confidence language, and control implications."
    ),
    "cognitive_resilience": (
        "Evidence packet: narrative provenance, audience-harm notes, attribution evidence, and transparent education options."
    ),
    "gray_zone_governance": (
        "Evidence packet: ambiguous-threshold indicators, attribution caveats, and policy review fields in a sample scenario."
    ),
    "financial_due_diligence": (
        "Evidence packet: transaction typology notes, source quality, escalation thresholds, and uncertainty fields."
    ),
    "analytic_tradecraft": (
        "Evidence packet: hypothesis tables, evidence matrices, confidence language, and reviewer dissent fields."
    ),
    "operational_tradecraft_governance": (
        "Evidence packet: sample OPSEC worksheets, compartmentation registers, and "
        "cover-review notes with explicit oversight fields."
    ),
    "cognitive_resilience_epistemic": (
        "Evidence packet: provenance chains, dissent channels, and correction options "
        "for epistemic-security tabletop review."
    ),
    "cognitive_resilience_inoculation": (
        "Evidence packet: inoculation lesson plans with transparent labels, source checks, "
        "and non-manipulative correction options."
    ),
    "critical_infrastructure_sharing": (
        "Evidence packet: sample ISAC packets for handling rules, anonymization, confidence, and consumer duties."
    ),
}

EVIDENCE_KEYWORD_ROUTES: tuple[tuple[tuple[str, ...], str], ...] = (
    (("ach", "competing hypotheses"), (
        "Evidence packet: hypothesis table with evidence for and against each alternative "
        "before confidence is assigned."
    )),
    (("mice", "recruitment"), (
        "Evidence packet: sample source notes for pressure indicators, consent language, "
        "validation steps, and excluded contact actions."
    )),
)

ARTIFACT_KEYWORD_ROUTES: tuple[tuple[tuple[str, ...], str], ...] = (
    (("free energy", "predictive processing"), (
        "Build a prediction-error concept card linking surprise, model assumption, and reviewer checkpoint."
    )),
    (("computational model", "active inference as computational"), (
        "Build a toy agent-model card with beliefs, actions, observations, and a human approval gate."
    )),
    (("shared protentions", "multi-agent active inference"), (
        "Build a shared-expectation register showing aligned expectations, dissent, and review ownership."
    )),
    (("social organization", "intelligence communit"), (
        "Build an institutional feedback-loop map with incentives, review points, and oversight hooks."
    )),
    (("verses", "multi-scale active inference"), (
        "Build an architecture-claim card separating research claims, implementation assumptions, and governance limits."
    )),
    (("cognitive security through the active inference",), (
        "Build a sample narrative-risk map with provenance, audience harm, and transparent response options."
    )),
    (("deception detection", "surprise minimization", "threat modeling"), (
        "Build a threat-model review card with assumptions, disconfirming evidence, and confidence language."
    )),
    (("tu delft", "applications of active inference and fep"), (
        "Build a research question, method, evidence base, and classroom boundary statement for the thesis topic."
    )),
)

ARTIFACT_RISK_CATEGORY_PROMPTS: dict[str, str] = {
    "agentic_cyber_misuse": (
        "Build a blocked-request control card with tool permission, unsafe outcome, "
        "deny rule, log evidence, and reviewer disposition."
    ),
    "software_supply_chain_social_trust": (
        "Build a maintainer-trust evidence card with provenance, communication-risk "
        "signal, uncertainty, and escalation boundary."
    ),
}


def _category_rows(mapping: dict[str, str]) -> list[dict[str, str]]:
    return [{"category": category, "prompt": prompt} for category, prompt in mapping.items()]


def _keyword_rows(routes: tuple[tuple[tuple[str, ...], str], ...]) -> list[dict[str, object]]:
    return [{"keywords": list(keywords), "prompt": prompt} for keywords, prompt in routes]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    payload = {
        "evidence_category_prompts": _category_rows(EVIDENCE_CATEGORY_PROMPTS),
        "evidence_keyword_routes": _keyword_rows(EVIDENCE_KEYWORD_ROUTES),
        "artifact_keyword_routes": _keyword_rows(ARTIFACT_KEYWORD_ROUTES),
        "artifact_risk_category_prompts": _category_rows(ARTIFACT_RISK_CATEGORY_PROMPTS),
    }
    out = root / "data" / "topic_prompt_routes.yaml"
    out.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
