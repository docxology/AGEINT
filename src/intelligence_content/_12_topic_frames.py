"""Profile-synthesized topic lesson frames and lesson field helpers."""

from __future__ import annotations

from typing import TYPE_CHECKING

from ._12_concept_routes import CONCEPT_KEYWORD_ROUTES, _first_matching_frame, _match_keywords

if TYPE_CHECKING:
    from ._01_part import CoursebookProfile, PracticeLens, TopicEntry
    from ._04b_part import IntelligenceProfile


def _import_prior_parts(*module_names: str) -> None:
    import importlib

    for module_name in module_names:
        mod = importlib.import_module(f".{module_name}", __package__)
        globals().update({k: v for k, v in vars(mod).items() if not k.startswith("__")})


_import_prior_parts("_01_part", "_04b_part", "_07_safe_titles", "_09_part")

CATEGORY_CONCEPT_FRAMES: dict[str, str] = {
    "agentic_cyber_misuse": (
        "Treat the topic as a misuse-case control problem: identify the agent permission, "
        "prompt path, tool boundary, and blocked outcome."
    ),
    "historical_humint_source_protection": (
        "Study the declassified record for institutional lessons about source protection, "
        "oversight, and the danger of translating historical methods into current practice."
    ),
    "ics_evasion_coverage": (
        "Use the tactic family as a defensive coverage question: which monitoring, logging, "
        "and operator-review controls would reveal evasion in a tabletop scenario?"
    ),
    "ics_collection_detection": (
        "Use the tactic family as a detection-design question over synthetic process tags, "
        "not as guidance for observing or changing a real process."
    ),
    "software_supply_chain_social_trust": (
        "Analyze how trust, maintainer contact, and package provenance become supply-chain "
        "assurance evidence without contacting or profiling real maintainers."
    ),
    "osint_tool_governance": (
        "Evaluate the tool class by provenance, legality, rate limits, identity exposure, "
        "and reproducibility before any public-source claim is reused."
    ),
    "humint_recruitment_risk": (
        "Read the concept as recruitment-risk literacy: identify pressure, consent, "
        "source-protection duties, and the line that blocks contact activity."
    ),
    "humint_handling_history": (
        "Use the historical motif to discuss source-protection ethics, documentation, "
        "and oversight without recreating handling procedures."
    ),
    "sigint_authority": (
        "Connect the technical term to authority, minimization, communications-security "
        "risk, and public doctrine rather than interception mechanics."
    ),
    "cyber_taxonomy": (
        "Use the taxonomy label to organize fabricated defensive observations, confidence, "
        "and control implications without describing adversary execution."
    ),
    "ics_safety": (
        "Translate the technique family into safety, availability, operator decision, "
        "and recovery-evidence questions for a tabletop."
    ),
    "cognitive_resilience": (
        "Focus on transparent resilience education: provenance, audience harm, attribution "
        "caution, and non-manipulative response options."
    ),
    "gray_zone_governance": (
        "Identify ambiguous-threshold activity through indicators, attribution caution, "
        "and policy review—not through prescribed response actions."
    ),
    "non_state_actor_governance": (
        "Study organizational and funding indicators with open-source evidence, "
        "minimization, and explicit uncertainty."
    ),
    "financial_due_diligence": (
        "Structure financial-pattern review as typology-driven due diligence with "
        "escalation thresholds, not proof of wrongdoing."
    ),
    "counterintelligence_vetting": (
        "Connect vetting and insider-threat review to access control, anomaly signals, "
        "and accountable escalation."
    ),
    "operator_decision_hygiene": (
        "Manage workload and bias through prioritization, explicit handoffs, and "
        "review checkpoints—not unsustainable pace."
    ),
    "geoint_data_quality": (
        "Audit imagery and map products for resolution, accuracy, temporal fitness, "
        "and uncertainty before any geospatial claim."
    ),
    "geoint_uncertainty": (
        "Treat geolocation and attribution claims as uncertainty problems with "
        "synthetic records and explicit caveats."
    ),
    "agentic_tool_isolation": (
        "Review sandbox policy, tool isolation, and deny-by-default rules using "
        "toy fixtures only."
    ),
    "ageint_pattern_registry": (
        "Use the pattern name as safe architectural vocabulary: allowlisted tools, "
        "logging, human approval, and blocked external action."
    ),
    "analytic_tradecraft": (
        "Apply structured analytic methods with explicit alternatives, evidence "
        "tables, and calibrated confidence—not rhetorical certainty."
    ),
    "analytic_tradecraft_sats": (
        "Use structured analytic techniques to keep alternatives, disconfirming "
        "evidence, and confidence visible before convergence."
    ),
    "analytic_tradecraft_standards": (
        "Apply ICD 203 tradecraft standards to sourcing, uncertainty, alternatives, "
        "and argumentation—not rhetorical certainty."
    ),
    "analytic_tradecraft_bias": (
        "Connect cognitive bias literacy to review checkpoints, dissent channels, "
        "and explicit uncertainty language."
    ),
    "operational_tradecraft_governance": (
        "Treat operational tradecraft as governance: OPSEC, compartmentation, cover "
        "discipline, and oversight—not contact or evasion activity."
    ),
    "cognitive_resilience_epistemic": (
        "Protect knowledge production with provenance, dissent channels, and "
        "transparent correction—not narrative control."
    ),
    "cognitive_resilience_inoculation": (
        "Build audience resilience with transparent labels, source checks, and "
        "non-manipulative corrections."
    ),
    "cognitive_resilience_neuro": (
        "Connect neurocognitive claims to analytic bias literacy and review "
        "compensation—not operational timing advice."
    ),
    "critical_infrastructure_sharing": (
        "Evaluate ISAC and sector sharing by handling rules, anonymization, "
        "confidence, and consumer responsibilities."
    ),
}


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
    return (
        f"Inspect fictional records that show how {anchor} appears in "
        f"{coursebook.practice_focus} review—mark provenance, gaps, and "
        f"what would change the judgment."
    )


EVIDENCE_CATEGORY_PROMPTS: dict[str, str] = {
    "agentic_cyber_misuse": (
        "Inspect fictional prompts, tool-call logs, blocked-action records, and the policy that denies the unsafe request."
    ),
    "historical_humint_source_protection": (
        "Inspect release metadata, redaction caveats, institutional setting, and the governance lesson that can be defended from the record."
    ),
    "ics_evasion_coverage": (
        "Inspect synthetic alert records, expected operator observations, control coverage, and recovery notes."
    ),
    "ics_collection_detection": (
        "Inspect synthetic tag histories, approved observation points, operator annotations, and detection gaps."
    ),
    "software_supply_chain_social_trust": (
        "Inspect package provenance, maintainer-trust signals, build-integrity evidence, and uncertainty about attribution."
    ),
    "osint_tool_governance": (
        "Inspect terms of use, source provenance, reproducibility notes, minimization decisions, and identity-exposure risks."
    ),
    "humint_recruitment_risk": (
        "Inspect fictional source notes for pressure, consent, escalation duties, and excluded contact actions."
    ),
    "cyber_taxonomy": (
        "Inspect fabricated alerts, published taxonomy labels, confidence language, and control implications."
    ),
    "cognitive_resilience": (
        "Inspect narrative provenance, audience-harm notes, attribution evidence, and transparent education options."
    ),
    "gray_zone_governance": (
        "Inspect ambiguous-threshold indicators, attribution caveats, and policy review fields in a fictional scenario."
    ),
    "financial_due_diligence": (
        "Inspect transaction typology notes, source quality, escalation thresholds, and uncertainty fields."
    ),
    "analytic_tradecraft": (
        "Inspect hypothesis tables, evidence matrices, confidence language, and reviewer dissent fields."
    ),
    "operational_tradecraft_governance": (
        "Inspect fictional OPSEC worksheets, compartmentation registers, and "
        "cover-review notes with explicit oversight fields."
    ),
    "cognitive_resilience_epistemic": (
        "Inspect provenance chains, dissent channels, and correction options "
        "for epistemic-security tabletop review."
    ),
    "cognitive_resilience_inoculation": (
        "Inspect inoculation lesson plans with transparent labels, source checks, "
        "and non-manipulative correction options."
    ),
    "critical_infrastructure_sharing": (
        "Inspect fictional ISAC packets for handling rules, anonymization, confidence, and consumer duties."
    ),
}


ARTIFACT_KEYWORD_ROUTES: tuple[tuple[tuple[str, ...], str], ...] = (
    (("free energy", "predictive processing"), (
        "Submit a prediction-error concept card linking surprise, model assumption, and reviewer checkpoint."
    )),
    (("computational model", "active inference as computational"), (
        "Submit a toy agent-model card with beliefs, actions, observations, and a human approval gate."
    )),
    (("shared protentions", "multi-agent active inference"), (
        "Submit a shared-expectation register showing aligned expectations, dissent, and review ownership."
    )),
    (("social organization", "intelligence communit"), (
        "Submit an institutional feedback-loop map with incentives, review points, and oversight hooks."
    )),
    (("verses", "multi-scale active inference"), (
        "Submit an architecture-claim card separating research claims, implementation assumptions, and governance limits."
    )),
    (("cognitive security through the active inference",), (
        "Submit a fictional narrative-risk map with provenance, audience harm, and transparent response options."
    )),
    (("deception detection", "surprise minimization", "threat modeling"), (
        "Submit a threat-model review card with assumptions, disconfirming evidence, and confidence language."
    )),
    (("tu delft", "applications of active inference and fep"), (
        "Submit a research question, method, evidence base, and classroom boundary statement for the thesis topic."
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
            "Inspect a hypothesis table with evidence for and against each alternative "
            "before assigning confidence."
        )
    if "mice" in raw or "recruitment" in raw:
        return (
            "Inspect fictional source notes for pressure indicators, consent language, "
            "validation steps, and excluded contact actions."
        )
    category = EVIDENCE_CATEGORY_PROMPTS.get(entry.risk_category)
    if category:
        if "fictional materials and transparent labels" in entry.display_title.lower():
            anchor = _topic_anchor_words(entry.raw_title, limit=2)
            return (
                f"Inspect fictional records for {anchor}: narrative provenance, "
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
            "Submit a blocked-request control card with tool permission, unsafe outcome, "
            "deny rule, log evidence, and reviewer disposition."
        )
    if entry.risk_category == "software_supply_chain_social_trust":
        return (
            "Submit a maintainer-trust evidence card with provenance, communication-risk "
            "signal, uncertainty, and escalation boundary."
        )
    return (
        f"Submit a completed **{lens.evidence_artifact}** for this {coursebook.practice_focus} "
        f"topic. The artifact must name the source descriptor, bounded claim, caveat, "
        "uncertainty note, blocked-use statement, and accountable reviewer."
    )


WHY_IT_MATTERS_TEMPLATES: tuple[str, ...] = (
    (
        "Analysts use **{topic}** to {distinction}. The answer should identify the "
        "enabled judgment, the proof limit, and the reviewer responsible for challenge."
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
) -> str:
    failure_hint = RISK_WHY_FAILURE_HINTS.get(
        entry.risk_category,
        profile.failure_modes.split(",")[0].strip() if profile.failure_modes else "overconfidence",
    )
    template_index = lesson_index % len(WHY_IT_MATTERS_TEMPLATES)
    if entry.risk_category in RISK_WHY_FAILURE_HINTS:
        template_index = (lesson_index + len(entry.risk_category)) % len(WHY_IT_MATTERS_TEMPLATES)
    template = WHY_IT_MATTERS_TEMPLATES[template_index]
    return template.format(
        topic=entry.display_title,
        distinction=coursebook.key_distinction,
        profile=profile.title,
        practice_focus=coursebook.practice_focus,
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
        "lens through concept, evidence, artifact, misconception, and transfer tasks."
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
        return templates[(lesson_index - 1) % len(templates)]
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
    template = MISCONCEPTION_FALLBACKS[(lesson_index - 1) % len(MISCONCEPTION_FALLBACKS)]
    return template.format(topic=entry.display_title, focus=coursebook.key_distinction)
