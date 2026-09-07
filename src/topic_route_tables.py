"""Canonical topic prompt-route and rotation-template tables for AGEINT.

Authoritative data-as-code tables for the topic-lesson prompt routing. The
thin ``scripts/generate_topic_prompt_routes_yaml.py`` and
``scripts/generate_topic_rotation_templates_yaml.py`` orchestrators emit these
payloads to ``data/topic_prompt_routes.yaml`` and
``data/topic_rotation_templates.yaml``; ``src/_data_loaders.py`` reads those
YAML files at runtime. Regenerate after editing a table here:

    uv run python scripts/generate_topic_prompt_routes_yaml.py
    uv run python scripts/generate_topic_rotation_templates_yaml.py
"""

from __future__ import annotations

from pathlib import Path

import yaml

# --- data/topic_prompt_routes.yaml tables -----------------------------------

EVIDENCE_CATEGORY_PROMPTS: dict[str, str] = {
    "agentic_cyber_misuse": ("Evidence packet: sample prompt records, tool-call logs, blocked-action records, and the policy that denies the unsafe request."),
    "historical_humint_source_protection": ("Evidence packet: release metadata, redaction caveats, institutional setting, and the governance lesson that can be defended from the record."),
    "ics_evasion_coverage": ("Evidence packet: synthetic alert records, expected operator observations, control coverage, and recovery notes."),
    "ics_collection_detection": ("Evidence packet: synthetic tag histories, approved observation points, operator annotations, and detection gaps."),
    "software_supply_chain_social_trust": ("Evidence packet: package provenance, maintainer-trust signals, build-integrity evidence, and uncertainty about attribution."),
    "osint_tool_governance": ("Evidence packet: terms of use, source provenance, reproducibility notes, minimization decisions, and identity-exposure risks."),
    "humint_recruitment_risk": ("Evidence packet: sample source notes for pressure, consent, escalation duties, and excluded contact actions."),
    "cyber_taxonomy": ("Evidence packet: fabricated alerts, published taxonomy labels, confidence language, and control implications."),
    "cognitive_resilience": ("Evidence packet: narrative provenance, audience-harm notes, attribution evidence, and transparent education options."),
    "gray_zone_governance": ("Evidence packet: ambiguous-threshold indicators, attribution caveats, and policy review fields in a sample scenario."),
    "financial_due_diligence": ("Evidence packet: transaction typology notes, source quality, escalation thresholds, and uncertainty fields."),
    "analytic_tradecraft": ("Evidence packet: hypothesis tables, evidence matrices, separated likelihood and confidence language, SAT evidence caveats, and reviewer dissent fields."),
    "operational_tradecraft_governance": ("Evidence packet: sample OPSEC worksheets, compartmentation registers, and cover-review notes with explicit oversight fields."),
    "cognitive_resilience_epistemic": ("Evidence packet: provenance chains, dissent channels, and correction options for epistemic-security tabletop review."),
    "cognitive_resilience_inoculation": (
        "Evidence packet: bounded inoculation lesson plans with transparent labels, source checks, measurement limits, audience-harm notes, and non-manipulative correction options."
    ),
    "critical_infrastructure_sharing": ("Evidence packet: sample ISAC packets for handling rules, anonymization, confidence, and consumer duties."),
    "evidence_change_memory": (
        "Evidence packet: source-change ledger, retention rule, contamination check, and proof that memory tracks claims and sources rather than people, assets, or behavioral patterns."
    ),
}

EVIDENCE_KEYWORD_ROUTES: tuple[tuple[tuple[str, ...], str], ...] = (
    (("ach", "competing hypotheses"), ("Evidence packet: hypothesis table with evidence for and against each alternative before confidence is assigned.")),
    (
        ("icd 203", "confidence language", "analytic confidence", "likelihood"),
        ("Evidence packet: probability term, confidence statement, source-quality basis, assumption register, and reviewer check that likelihood and confidence are not collapsed."),
    ),
    (
        ("warning intelligence", "indications and warning", "indicator register"),
        ("Evidence packet: indicator register, assumption trace, collection gap, decision-uptake note, and postmortem learning field."),
    ),
    (
        ("structured analytic technique", "structured analytic techniques", "sat evidence"),
        ("Evidence packet: technique purpose, diagnosticity claim, empirical support limit, reviewer dissent, and caveat against treating the technique as a universal bias remedy."),
    ),
    (("mice", "recruitment"), ("Evidence packet: sample source notes for pressure indicators, consent language, validation steps, and excluded contact actions.")),
)

ARTIFACT_KEYWORD_ROUTES: tuple[tuple[tuple[str, ...], str], ...] = (
    (("free energy", "predictive processing"), ("Build a prediction-error concept card linking formal source, surprise, model assumption, analogy limit, and reviewer checkpoint.")),
    (("computational model", "active inference as computational"), ("Build a toy agent-model card with beliefs, actions, observations, implementation assumption, and a human approval gate.")),
    (("shared protentions", "multi-agent active inference"), ("Build a shared-expectation register showing aligned expectations, dissent, and review ownership.")),
    (("social organization", "intelligence communit"), ("Build an institutional feedback-loop map with incentives, review points, and oversight hooks.")),
    (("verses", "multi-scale active inference"), ("Build an architecture-claim card separating research claims, implementation assumptions, and governance limits.")),
    (("cognitive security through the active inference",), ("Build a sample narrative-risk map with provenance, audience harm, and transparent response options.")),
    (("deception detection", "surprise minimization", "threat modeling"), ("Build a threat-model review card with assumptions, disconfirming evidence, and confidence language.")),
    (("tu delft", "applications of active inference and fep"), ("Build a research question, method, evidence base, and classroom boundary statement for the thesis topic.")),
    (
        ("external vectordb", "in-context"),
        ("Build an agent-memory boundary card that separates source/change ledgers, external stores, retention rules, and reviewer controls from unsupported cognitive-memory taxonomy claims."),
    ),
    (
        ("persistent memory",),
        (
            "Build a claim-ledger memory card with source descriptor, source-change event, "
            "retention rule, contamination check, and reviewer disposition; do not track "
            "real people, assets, or behavioral patterns."
        ),
    ),
)

ARTIFACT_RISK_CATEGORY_PROMPTS: dict[str, str] = {
    "agentic_cyber_misuse": ("Build a blocked-request control card with tool permission, unsafe outcome, deny rule, log evidence, and reviewer disposition."),
    "software_supply_chain_social_trust": ("Build a maintainer-trust evidence card with provenance, communication-risk signal, uncertainty, and escalation boundary."),
    "evidence_change_memory": (
        "Build a claim-ledger memory card with source descriptor, source-change event, "
        "retention rule, contamination check, and reviewer disposition; it must not "
        "track real people, assets, or behavioral patterns."
    ),
}

# --- data/topic_rotation_templates.yaml tables -------------------------------

WHY_IT_MATTERS_TEMPLATES: tuple[str, ...] = (
    (
        "Analysts use **{topic}** to {distinction}. A defensible treatment names the "
        "judgment it enables for {practice_focus} review, the proof limit that "
        "{failure_hint} would otherwise hide, and the reviewer accountable for challenge."
    ),
    ("**{topic}** matters in the **{profile}** lane because {practice_focus} evidence must stay separate from judgment; {failure_hint} is a common failure."),
    ("**{topic}** connects classroom vocabulary to {profile} practice: learners document evidence, caveats, and reviewer ownership rather than repeating labels."),
    ("Without explicit treatment of **{topic}**, {failure_hint} undermines {practice_focus} review; the lesson builds the habit to {distinction}."),
)

RISK_WHY_FAILURE_HINTS: dict[str, str] = {
    "cognitive_resilience": "treating resilience labels as permission to skip provenance review",
    "humint_recruitment_risk": "confusing motivation literacy with contact authorization",
    "operational_tradecraft_governance": "confusing governance vocabulary with operational authorization",
    "analytic_tradecraft": "collapsing reporting, inference, and judgment into one line",
    "cyber_taxonomy": "treating defensive taxonomy labels as an action sequence",
    "ageint_pattern_registry": "treating pattern names as deployment playbooks",
    "agentic_cyber_misuse": "treating misuse taxonomy as tool permission",
    "financial_due_diligence": "treating typology match as proof of intent",
}

MISCONCEPTION_FALLBACKS: tuple[str, ...] = (
    "that {topic} can be used while ignoring the rule to {focus}",
    "that {topic} is optional whenever {focus} feels inconvenient",
    "that {topic} establishes intent without reviewing alternative explanations",
    "that {topic} replaces human review whenever evidence looks plausible",
)

MISCONCEPTION_RISK_TEMPLATES: tuple[str, ...] = (
    ("that a safe curriculum label for **{display_title}** in **{chapter_anchor}** authorizes the original operational source motif"),
    ("that **{chapter_anchor}** classroom framing for **{display_title}** removes the need for provenance and reviewer sign-off"),
    ("that completing the **{display_title}** artifact in **{chapter_anchor}** establishes real-world authorization without separate approval evidence"),
)

MISCONCEPTION_KEYWORD_ROUTES: tuple[tuple[tuple[str, ...], str], ...] = (
    (("mice",), "that a motivation taxonomy is a recruitment checklist"),
    (("att&ck",), "that a defensive taxonomy is an instruction sequence"),
    (("kill chain",), "that a defensive taxonomy is an instruction sequence"),
    (("fisa", "executive order"), "that a legal source grants authority without scope and oversight"),
    (("beneficial ownership",), "that ownership evidence removes uncertainty about control or intent"),
    (("geoint", "imagery"), "that a visible feature is enough for a confident geospatial claim"),
    (("ach", "competing hypotheses"), "that listing one favored hypothesis is enough without testing alternatives"),
)

# Keyword-routed transfer tasks. Kept in this canonical module so the YAML
# generator emits a COMPLETE payload: the runtime loader
# (_data_loaders.topic_rotation_templates_payload) requires this list, and an
# earlier revision of the generator omitted it, so a regenerate silently
# produced a YAML that failed the loader's contract.
TRANSFER_TASK_KEYWORD_ROUTES: tuple[tuple[tuple[str, ...], str], ...] = (
    (
        ("active inference", "free energy", "predictive"),
        "Transfer the idea to a non-AI chapter by naming the assumed model, the surprising observation, and the review point before any decision follows.",
    ),
)

# Risk-category-specific misconception clauses (risk_category -> clause),
# consulted by _data_loaders.misconception_category_routes() after keyword
# routes and before the generic per-risk templates. Kept canonical here so a
# regenerate cannot silently drop them the way the transfer-task list once was.
MISCONCEPTION_CATEGORY_ROUTES: dict[str, str] = {
    "cognitive_resilience": "that a resilience label on a technique means it has been stress-tested, rather than a habit that still needs evidence, caveats, and reviewer challenge",
    "historical_humint_source_protection": "that a source identity is safe to discuss once the operation is historical, when protection obligations and re-identification risk outlast the case itself",
    "analytic_tradecraft": "that a confident narrative is the same as a tested, source-backed judgment with its alternatives and confidence stated",
    "operator_decision_hygiene": "that feeling certain in the moment substitutes for the checklist, pause, and second-look that decision hygiene exists to enforce",
    "gray_zone_governance": "that activity falling below an obvious threshold is therefore ungoverned, rather than still bound by escalation limits and accountable review",
    "sigint_authority": "that a named collection authority removes the minimization and retention limits on what may be kept",
    "cyber_taxonomy": "that a defensive taxonomy label is an action sequence rather than a vocabulary for describing and detecting behavior",
    "geoint_data_quality": "that a visible feature in imagery is enough for confident attribution without resolution, timing, and provenance caveats",
    "counterintelligence_vetting": "that a clean vetting result certifies present trustworthiness rather than a point-in-time judgment that must be continuously re-examined",
    "humint_recruitment_risk": "that motivation literacy is contact authorization",
    "humint_handling_history": "that a documented handling precedent licenses repeating the approach, rather than a case-bound record whose risks must be re-assessed each time",
    "agentic_cyber_misuse": "that a misuse taxonomy describing what an autonomous agent could do is permission or a recipe to make it do so",
    "operational_tradecraft_governance": "that governance vocabulary about tradecraft confers operational authorization rather than the constraints under which any action must be approved",
    "osint_tool_governance": "that a source being publicly accessible means collecting it is unrestricted, ungoverned, and free of legal, ethical, and scoping limits",
    "ics_safety": "that an industrial control system behaving normally proves it is safe, rather than a state that depends on intact safeguards and monitoring",
    "critical_infrastructure_sharing": "that information being shareable for defense means it carries no sensitivity, attribution, or need-to-know limits on who receives it",
    "non_state_actor_governance": "that lacking a state sponsor places an actor outside the reach of governance, accountability, and applicable rules",
    "software_supply_chain_social_trust": "that a familiar maintainer name or popular package is a substitute for verifying provenance, integrity, and the chain of trust",
    "financial_due_diligence": "that a typology or pattern match is proof of intent rather than a flag requiring corroboration and alternative explanations",
    "evidence_change_memory": "that a current record reflects the original, when undocumented changes to evidence over time can silently rewrite what is remembered",
    "identity_provenance": "that a presented identity is an established one, when provenance requires tracing how that identity was created, verified, and could be forged",
    "ics_evasion_coverage": "that mapping how detection can be evaded in control systems is a how-to, rather than a defensive map of where monitoring coverage must be hardened",
    "ics_collection_detection": "that describing how collection against control systems is detected is an evasion guide, rather than knowledge for strengthening detection",
    "ageint_pattern_registry": "that naming an agent pattern certifies it is safe to deploy without governance gates",
}


def _category_rows(mapping: dict[str, str]) -> list[dict[str, str]]:
    return [{"category": category, "prompt": prompt} for category, prompt in mapping.items()]


def _keyword_rows(routes: tuple[tuple[tuple[str, ...], str], ...]) -> list[dict[str, object]]:
    return [{"keywords": list(keywords), "prompt": prompt} for keywords, prompt in routes]


def topic_prompt_routes_payload() -> dict[str, object]:
    """Return the canonical payload emitted to ``data/topic_prompt_routes.yaml``."""
    return {
        "evidence_category_prompts": _category_rows(EVIDENCE_CATEGORY_PROMPTS),
        "evidence_keyword_routes": _keyword_rows(EVIDENCE_KEYWORD_ROUTES),
        "artifact_keyword_routes": _keyword_rows(ARTIFACT_KEYWORD_ROUTES),
        "artifact_risk_category_prompts": _category_rows(ARTIFACT_RISK_CATEGORY_PROMPTS),
    }


def topic_rotation_templates_payload() -> dict[str, object]:
    """Return the canonical payload emitted to ``data/topic_rotation_templates.yaml``."""
    return {
        "why_it_matters_templates": list(WHY_IT_MATTERS_TEMPLATES),
        "risk_why_failure_hints": [{"category": category, "hint": hint} for category, hint in RISK_WHY_FAILURE_HINTS.items()],
        "misconception_fallbacks": list(MISCONCEPTION_FALLBACKS),
        "misconception_risk_templates": list(MISCONCEPTION_RISK_TEMPLATES),
        "misconception_keyword_routes": [{"keywords": list(keywords), "misconception": misconception} for keywords, misconception in MISCONCEPTION_KEYWORD_ROUTES],
        "transfer_task_keyword_routes": [{"keywords": list(keywords), "template": template} for keywords, template in TRANSFER_TASK_KEYWORD_ROUTES],
        "misconception_category_routes": dict(MISCONCEPTION_CATEGORY_ROUTES),
    }


def write_topic_prompt_routes_yaml(root: Path) -> Path:
    """Emit the canonical prompt-route payload to ``root/data/topic_prompt_routes.yaml``."""
    out = Path(root) / "data" / "topic_prompt_routes.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(topic_prompt_routes_payload(), sort_keys=False, allow_unicode=True), encoding="utf-8")
    return out


def write_topic_rotation_templates_yaml(root: Path) -> Path:
    """Emit the canonical rotation-template payload to ``root/data/topic_rotation_templates.yaml``."""
    out = Path(root) / "data" / "topic_rotation_templates.yaml"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(yaml.safe_dump(topic_rotation_templates_payload(), sort_keys=False, allow_unicode=True), encoding="utf-8")
    return out
