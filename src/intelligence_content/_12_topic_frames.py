"""Profile-synthesized topic lesson frames and lesson field helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._12_concept_routes import CONCEPT_KEYWORD_ROUTES, _first_matching_frame, _match_keywords

if TYPE_CHECKING:
    from ._01_part import CoursebookProfile, PracticeLens, TopicEntry
    from ._04b_part import IntelligenceProfile


try:
    from .topic_lessons import template_index
except ImportError:  # pragma: no cover - merged namespace
    from intelligence_content.topic_lessons import template_index  # type: ignore[no-redef]

from _data_loaders import category_concept_frames

CATEGORY_CONCEPT_FRAMES: dict[str, str] = category_concept_frames()



def _topic_hook(entry: TopicEntry) -> str:
    anchor = _topic_anchor_words(entry.display_title, limit=2)
    return f"learners connect {anchor} to the chapter practice lens"


def _analytic_subcategory(raw_lower: str) -> str | None:
    if _match_keywords(
        raw_lower,
        (
            "competing hypotheses",
            "ach",
            "key assumptions",
            "devil's advocacy",
            "devils advocacy",
            "red team analysis",
            "structured analytic",
        ),
    ):
        return "analytic_tradecraft_sats"
    if _match_keywords(
        raw_lower,
        ("icd 203", "nine tradecraft", "analytic tradecraft standard", "analytic confidence"),
    ):
        return "analytic_tradecraft_standards"
    if _match_keywords(raw_lower, ("bias", "heuristic", "cognitive trap", "mirror imaging")):
        return "analytic_tradecraft_bias"
    return None


def _cognitive_subcategory(raw_lower: str) -> str | None:
    if _match_keywords(raw_lower, ("epistemic", "knowledge integrity", "malign influence")):
        return "cognitive_resilience_epistemic"
    if _match_keywords(raw_lower, ("prebunking", "inoculation", "debunking")):
        return "cognitive_resilience_inoculation"
    if _match_keywords(
        raw_lower,
        ("neuro", "resaid", "neurips", "brain", "cognitive mechanism"),
    ):
        return "cognitive_resilience_neuro"
    return None


def _category_frame_key(entry: TopicEntry) -> str:
    raw = f"{entry.display_title} {entry.raw_title}".lower()
    if entry.risk_category == "analytic_tradecraft":
        sub = _analytic_subcategory(raw)
        if sub:
            return sub
    if entry.risk_category == "cognitive_resilience":
        sub = _cognitive_subcategory(raw)
        if sub:
            return sub
    if entry.risk_category == "ageint_pattern_registry":
        if _match_keywords(raw, ("pattern", "archetype", "registry")):
            return "ageint_pattern_registry"
    return entry.risk_category


def synthesized_concept_frame(
    entry: TopicEntry,
    coursebook: CoursebookProfile,
    profile: IntelligenceProfile,
) -> str:
    """Profile-backed concept prose when no keyword or category route matches."""
    anchor_source = (
        entry.raw_title
        if is_generic_display_title(entry.display_title)
        else entry.display_title
    )
    anchor = _topic_anchor_words(anchor_source, limit=3)
    return (
        f"**{entry.display_title}** applies {anchor} within {profile.title}: "
        f"learners use {coursebook.key_distinction} and {coursebook.practice_focus} "
        "evidence before any judgment moves forward."
    )


def concept_frame_for_entry(
    entry: TopicEntry,
    coursebook: CoursebookProfile,
    profile: IntelligenceProfile,
) -> str:
    raw = f"{entry.display_title} {entry.raw_title}".lower()
    frame = _first_matching_frame(raw, CONCEPT_KEYWORD_ROUTES)
    if frame:
        return frame
    category_key = _category_frame_key(entry)
    category_frame = CATEGORY_CONCEPT_FRAMES.get(category_key)
    if category_frame:
        return category_frame
    return synthesized_concept_frame(entry, coursebook, profile)


def synthesized_evidence_prompt(entry: TopicEntry, lens: PracticeLens, coursebook: CoursebookProfile) -> str:
    anchor = _topic_anchor_words(entry.display_title, limit=2)
    focus = coursebook.practice_focus.removesuffix(" review")
    return (
        f"The evidence packet for **{entry.display_title}** uses source descriptors, "
        f"{focus} records, provenance gaps, and a documented judgment-change condition for {anchor}."
    )


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


def evidence_prompt_for_entry(
    entry: TopicEntry,
    lens: PracticeLens,
    coursebook: CoursebookProfile,
) -> str:
    raw = entry.raw_title.lower()
    if "ach" in raw or "competing hypotheses" in raw:
        return (
            "Evidence packet: hypothesis table with evidence for and against each alternative "
            "before confidence is assigned."
        )
    if "mice" in raw or "recruitment" in raw:
        return (
            "Evidence packet: sample source notes for pressure indicators, consent language, "
            "validation steps, and excluded contact actions."
        )
    category = EVIDENCE_CATEGORY_PROMPTS.get(entry.risk_category)
    if category:
        if "sample materials and transparent labels" in entry.display_title.lower():
            anchor = _topic_anchor_words(entry.raw_title, limit=2)
            return (
                f"Evidence packet for **{entry.display_title}**: narrative provenance for {anchor}, "
                "audience-harm notes, attribution evidence, and transparent education options."
            )
        return category
    return synthesized_evidence_prompt(entry, lens, coursebook)


def artifact_prompt_for_entry(entry: TopicEntry, lens: PracticeLens, coursebook: CoursebookProfile) -> str:
    raw = entry.raw_title.lower()
    routed = _first_matching_frame(raw, ARTIFACT_KEYWORD_ROUTES)
    if routed:
        return routed
    if entry.risk_category == "agentic_cyber_misuse":
        return (
            "Build a blocked-request control card with tool permission, unsafe outcome, "
            "deny rule, log evidence, and reviewer disposition."
        )
    if entry.risk_category == "software_supply_chain_social_trust":
        return (
            "Build a maintainer-trust evidence card with provenance, communication-risk "
            "signal, uncertainty, and escalation boundary."
        )
    return (
        f"Build a **{lens.evidence_artifact}** for this {coursebook.practice_focus} "
        f"topic. The artifact must name the source descriptor, bounded claim, caveat, "
        "uncertainty note, blocked-use statement, and accountable reviewer."
    )


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


def why_it_matters_for_entry(
    entry: TopicEntry,
    profile: IntelligenceProfile,
    coursebook: CoursebookProfile,
    *,
    lesson_index: int,
    chapter_title: str = "",
) -> str:
    failure_hint = RISK_WHY_FAILURE_HINTS.get(
        entry.risk_category,
        profile.failure_modes.split(",")[0].strip() if profile.failure_modes else "overconfidence",
    )
    chapter_slot = template_index(
        chapter_title,
        entry.risk_category,
        count=len(WHY_IT_MATTERS_TEMPLATES),
    )
    template_index_value = (chapter_slot + lesson_index - 1) % len(WHY_IT_MATTERS_TEMPLATES)
    template = WHY_IT_MATTERS_TEMPLATES[template_index_value]
    practice_focus = coursebook.practice_focus.removesuffix(" review")
    return template.format(
        topic=entry.display_title,
        distinction=coursebook.key_distinction,
        profile=profile.title,
        practice_focus=practice_focus,
        failure_hint=failure_hint,
    )


def lesson_intro_paragraph(
    chapter_title: str,
    coursebook: CoursebookProfile,
    lens: PracticeLens,
    topic_titles: tuple[str, ...],
) -> str:
    opener = topic_titles[0] if topic_titles else chapter_title
    topic_path = ", ".join(f"**{title}**" for title in topic_titles[:3]) if topic_titles else f"**{opener}**"
    return (
        f"**{chapter_title}** builds {coursebook.disciplinary_frame}. "
        f"The sequence opens with {topic_path} and applies the **{lens.title}** "
        "practice frame through concept, evidence, artifact, misconception, and transfer tasks."
    )


MISCONCEPTION_FALLBACKS: tuple[str, ...] = (
    "that {topic} can be used while ignoring the rule to {focus}",
    "that {topic} is optional whenever {focus} feels inconvenient",
    "that {topic} proves intent without reviewing alternative explanations",
    "that {topic} replaces human review whenever evidence looks plausible",
)


def misconception_for_entry(
    entry: TopicEntry,
    coursebook: CoursebookProfile,
    *,
    lesson_index: int = 1,
    chapter_title: str = "",
) -> str:
    if entry.risk_category != "standard" and entry.risk_category != "ageint_pattern_registry":
        chapter_anchor = chapter_title or "this module"
        templates = (
            (
                f"that a safe curriculum label for **{entry.display_title}** in "
                f"**{chapter_anchor}** authorizes the original operational source motif"
            ),
            (
                f"that **{chapter_anchor}** classroom framing for **{entry.display_title}** "
                "removes the need for provenance and reviewer sign-off"
            ),
            (
                f"that completing the **{entry.display_title}** artifact in "
                f"**{chapter_anchor}** proves real-world authorization"
            ),
        )
        slot = template_index(
            entry.display_title,
            chapter_title,
            str(lesson_index),
            entry.risk_category,
            count=len(templates),
        )
        return templates[slot]
    raw = f"{entry.display_title} {entry.raw_title}".lower()
    if _match_keywords(raw, ("mice",)):
        return "that a motivation taxonomy is a recruitment checklist"
    if _match_keywords(raw, ("att&ck",)) or "kill chain" in raw:
        return "that a defensive taxonomy is an instruction sequence"
    if "fisa" in raw or "executive order" in raw:
        return "that a legal source grants authority without scope and oversight"
    if "beneficial ownership" in raw:
        return "that ownership evidence removes uncertainty about control or intent"
    if "geoint" in raw or "imagery" in raw:
        return "that a visible feature is enough for a confident geospatial claim"
    if _match_keywords(raw, ("ach",)) or "competing hypotheses" in raw:
        return "that listing one favored hypothesis is enough without testing alternatives"
    chapter_base = template_index(chapter_title, count=len(MISCONCEPTION_FALLBACKS))
    template_slot = (chapter_base + lesson_index - 1) % len(MISCONCEPTION_FALLBACKS)
    template = MISCONCEPTION_FALLBACKS[template_slot]
    return template.format(topic=entry.display_title, focus=coursebook.key_distinction)
