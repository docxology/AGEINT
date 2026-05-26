#!/usr/bin/env python3
"""One-shot generator for data/topic_rotation_templates.yaml from canonical tables."""

from __future__ import annotations

from pathlib import Path

import yaml

WHY_IT_MATTERS_TEMPLATES: tuple[str, ...] = (
    (
        "Analysts use **{topic}** to {distinction}. A defensible treatment names the "
        "enabled judgment, proof limit, and reviewer responsible for challenge."
    ),
    (
        "**{topic}** matters in the **{profile}** lane because {practice_focus} "
        "evidence must stay separate from judgment; {failure_hint} is a common failure."
    ),
    (
        "**{topic}** connects classroom vocabulary to {profile} practice: learners "
        "document evidence, caveats, and reviewer ownership rather than repeating labels."
    ),
    (
        "Without explicit treatment of **{topic}**, {failure_hint} undermines "
        "{practice_focus} review; the lesson builds the habit to {distinction}."
    ),
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
    "that {topic} proves intent without reviewing alternative explanations",
    "that {topic} replaces human review whenever evidence looks plausible",
)

MISCONCEPTION_RISK_TEMPLATES: tuple[str, ...] = (
    (
        "that a safe curriculum label for **{display_title}** in "
        "**{chapter_anchor}** authorizes the original operational source motif"
    ),
    (
        "that **{chapter_anchor}** classroom framing for **{display_title}** "
        "removes the need for provenance and reviewer sign-off"
    ),
    (
        "that completing the **{display_title}** artifact in "
        "**{chapter_anchor}** proves real-world authorization"
    ),
)

MISCONCEPTION_KEYWORD_ROUTES: tuple[tuple[tuple[str, ...], str], ...] = (
    (("mice",), "that a motivation taxonomy is a recruitment checklist"),
    (("att&ck",), "that a defensive taxonomy is an instruction sequence"),
    (("kill chain",), "that a defensive taxonomy is an instruction sequence"),
    (
        ("fisa", "executive order"),
        "that a legal source grants authority without scope and oversight",
    ),
    (
        ("beneficial ownership",),
        "that ownership evidence removes uncertainty about control or intent",
    ),
    (
        ("geoint", "imagery"),
        "that a visible feature is enough for a confident geospatial claim",
    ),
    (
        ("ach", "competing hypotheses"),
        "that listing one favored hypothesis is enough without testing alternatives",
    ),
)


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    payload = {
        "why_it_matters_templates": list(WHY_IT_MATTERS_TEMPLATES),
        "risk_why_failure_hints": [
            {"category": category, "hint": hint}
            for category, hint in RISK_WHY_FAILURE_HINTS.items()
        ],
        "misconception_fallbacks": list(MISCONCEPTION_FALLBACKS),
        "misconception_risk_templates": list(MISCONCEPTION_RISK_TEMPLATES),
        "misconception_keyword_routes": [
            {"keywords": list(keywords), "misconception": misconception}
            for keywords, misconception in MISCONCEPTION_KEYWORD_ROUTES
        ],
    }
    out = root / "data" / "topic_rotation_templates.yaml"
    out.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
