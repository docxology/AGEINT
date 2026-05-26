from __future__ import annotations




COURSEBOOK_PROFILES: Final[dict[str, CoursebookProfile]] = {
    "governed_intelligence_cycle": CoursebookProfile(
        identifier="governed_intelligence_cycle",
        disciplinary_frame=(
            "intelligence as a governed information cycle: requirements become "
            "collection, collection becomes evaluated evidence, evidence becomes "
            "analytic judgment, and judgment becomes a disseminated product with "
            "markings, records, feedback, and oversight"
        ),
        key_distinction="separate intelligence work from ordinary research by naming authority, audience, caveats, and feedback",
        vocabulary=(
            ("Requirement", "the decision need or learning question that justifies evidence collection"),
            ("Dissemination", "the controlled movement of an intelligence product to an authorized audience"),
            ("Marking", "the vocabulary that communicates handling, caveat, and release limits"),
            ("Feedback loop", "the customer or reviewer signal that tests whether the product answered the need"),
            ("Records duty", "the retention, deletion, or refresh obligation attached to an artifact"),
            ("Decision hygiene", "habits that keep requirements, evidence, and reviewer judgment aligned under load"),
            ("Information architecture", "how sources, notes, and products are organized so uncertainty stays visible"),
        ),
        worked_scenario="a synthetic analyst team rebuilds a storm-impact brief after discovering a stale requirement and overloaded reading queue",
        worked_input="public weather bulletins, public infrastructure maps, historical outage summaries, and instructor-provided toy records",
        worked_process="map the requirement, tag each source, separate observation from judgment, assign caveats, and record the dissemination audience",
        worked_output="a one-page release-neutral brief with source descriptors, confidence language, caveats, and a feedback owner",
        practice_focus="cycle mapping and audience-aware product design",
        review_question="Which requirement, source, or workflow step failed first when the team ran out of review time?",
    ),
    "operator_productivity": CoursebookProfile(
        identifier="operator_productivity",
        disciplinary_frame=(
            "intelligence productivity as governed cognitive performance: "
            "external memory, workload limits, flow conditions, and explicit "
            "review handoffs keep judgment reliable under sustained tempo"
        ),
        key_distinction="separate cognitive hygiene from heroics, and workload signals from unreviewed urgency",
        vocabulary=(
            ("External memory", "a trusted capture system that holds tasks and commitments outside working memory"),
            ("NASA-TLX", "a subjective workload instrument for rating mental, temporal, and effort demands"),
            ("Flow precondition", "task clarity, challenge-skill balance, and feedback that enable focused work"),
            ("Decision hygiene", "habits that preserve evidence review, handoffs, and rest boundaries under load"),
            ("Task switching", "context change with measurable recovery cost and explicit re-entry notes"),
        ),
        worked_scenario="a synthetic analyst cell rebuilds a weekly reading queue after workload scores spike during a surge brief",
        worked_input="synthetic task lists, NASA-TLX self-ratings, instructor-provided focus blocks, and a handoff template",
        worked_process="capture open loops, score workload, schedule focus blocks, document handoffs, and assign reviewer checkpoints",
        worked_output="an operator workload card with queue state, TLX scores, focus plan, handoff owner, and rest boundary",
        practice_focus="workload-aware operator decision hygiene",
        review_question="Which workload signal or handoff gap would have prevented the quality drop?",
    ),
    "analytic_tradecraft": CoursebookProfile(
        identifier="analytic_tradecraft",
        disciplinary_frame=(
            "analytic tradecraft as disciplined judgment under uncertainty: "
            "claims become useful only when evidence, assumptions, alternatives, "
            "confidence, and dissent remain visible"
        ),
        key_distinction="separate reporting from inference, and inference from judgment",
        vocabulary=(
            ("Source descriptor", "a compact statement of where evidence came from and what it can support"),
            ("Assumption", "a claim accepted for analysis that still needs challenge"),
            ("Alternative hypothesis", "a plausible explanation that competes with the favored account"),
            ("Confidence", "a calibrated expression of evidentiary strength and analytic uncertainty"),
            ("Dissent", "a documented disagreement that preserves minority reasoning for review"),
        ),
        worked_scenario="a synthetic analyst cell evaluates whether a benign supplier delay signals normal friction or elevated risk",
        worked_input="synthetic shipment notes, public policy excerpts, and a short instructor-provided event timeline",
        worked_process="write hypotheses, list evidence for and against each, mark assumptions, and assign confidence only after alternatives are tested",
        worked_output="an analytic note with a hypothesis table, confidence statement, dissent field, and collection gap list",
        practice_focus="structured reasoning and source-integrity review",
        review_question="Which assumption would change the judgment if it were false?",
    ),
    "ai_ethics_data_governance": CoursebookProfile(
        identifier="ai_ethics_data_governance",
        disciplinary_frame=(
            "AI governance as lifecycle control: data, model, prompt, output, "
            "human reviewer, rights impact, and retention rule remain traceable"
        ),
        key_distinction="separate technical capability from lawful, accountable, and rights-respecting use",
        vocabulary=(
            ("Purpose limitation", "the bounded reason a data or model use is allowed"),
            ("Model card", "a structured record of intended use, limits, evaluation, and ownership"),
            ("Dataset card", "a structured record of origin, composition, transformations, and limits"),
            ("Bias review", "a socio-technical check for unequal error, access, or impact"),
            ("Human accountability", "the named person or role responsible for accepting or rejecting output"),
            ("Impact assessment", "a scored review that links system purpose, safeguards, and affected people"),
            ("Public register", "an accessible inventory entry that explains approved AI use and review status"),
        ),
        worked_scenario="a synthetic training office evaluates whether a summarization agent can support course readings",
        worked_input="public source excerpts, synthetic learner questions, a model-use note, and an accessibility checklist",
        worked_process="define purpose, inspect data provenance, document limits, test sample summaries, and assign a human review owner",
        worked_output="an AI/data impact card with intended use, excluded use, evaluation evidence, and refresh trigger",
        practice_focus="model/data documentation and rights-aware review",
        review_question="What part of the workflow needs human judgment even if the model output looks fluent?",
    ),
    "agentic_ai_governance": CoursebookProfile(
        identifier="agentic_ai_governance",
        disciplinary_frame=(
            "agentic AI as delegated action under control: identity, authority, "
            "tool permissions, memory, logs, stop conditions, and recoverability define "
            "what an agent may do"
        ),
        key_distinction="separate agent assistance from autonomous external action",
        vocabulary=(
            ("Agent identity", "the named software actor, role, and authorization context for a run"),
            ("Tool allowlist", "the bounded set of actions the agent may request"),
            ("Delegation", "the handoff of a task under explicit human authority and review"),
            ("Bounded autonomy", "the documented ceiling on what an agent may decide or request without review"),
            ("Recoverability", "the path back to a known-safe state after a bad output or action request"),
            ("AI incident", "a logged event where an AI system creates or plausibly creates harm or loss of control"),
            ("Prompt injection", "untrusted content that attempts to override instructions or authority boundaries"),
            ("Pattern registry", "the catalog of approved agent behaviors, prompts, and evaluation hooks"),
            ("Adversarial eval", "structured tests that probe agent misuse, injection, and over-delegation before release"),
        ),
        worked_scenario="a synthetic research assistant agent organizes public readings for an instructor",
        worked_input="public URLs, a fixed retrieval tool, a summarization prompt, a time budget, and a stop condition",
        worked_process="bind the agent identity, list allowed tools, set autonomy limits, capture sources, block unsafe requests, and log approvals",
        worked_output="an agent run card with tool calls, source links, blocked actions, reviewer notes, incident threshold, and recovery decision",
        practice_focus="least-privilege agent design and run review",
        review_question="Which permission can be removed while preserving the learning objective?",
    ),
    "osint_geoint": CoursebookProfile(
        identifier="osint_geoint",
        disciplinary_frame=(
            "OSINT and GEOINT as public-source reasoning disciplines: availability "
            "does not equal reliability, relevance, legality, or ethical reuse"
        ),
        key_distinction="separate discovery from collection expansion, and map or media interpretation from targeting",
        vocabulary=(
            ("Provenance", "the origin, chain, and transformation history of a source"),
            ("Corroboration", "the comparison of independent sources before reuse"),
            ("Recency", "the time relationship between source creation, discovery, and claim"),
            ("Geospatial quality", "accuracy, completeness, temporal fitness, and usability of location data"),
            ("Minimization", "limiting retained information to what the authorized question requires"),
        ),
        worked_scenario="a synthetic public-resilience team checks whether open data supports a non-sensitive evacuation-route map",
        worked_input="public road data, public weather notices, synthetic change examples, and instructor-provided metadata",
        worked_process="record provenance, test recency, compare independent sources, mark uncertainty, and remove unnecessary identity data",
        worked_output="a source-quality matrix and annotated map note with caveats and no tracking or targeting content",
        practice_focus="source-quality review and non-sensitive geospatial interpretation",
        review_question="Which source is available but not reliable enough for the claim?",
    ),
    "collection_management": CoursebookProfile(
        identifier="collection_management",
        disciplinary_frame=(
            "collection management as requirements discipline: a source method is "
            "considered only after the priority, authority, minimization rule, "
            "source risk, and evaluation plan are explicit"
        ),
        key_distinction="separate collection discipline concepts from operational recruitment, interception, or tasking procedures",
        vocabulary=(
            ("Priority", "the relative importance of an intelligence question"),
            ("Source discipline", "a broad evidence channel such as HUMINT, SIGINT, GEOINT, OSINT, or FININT"),
            ("Minimization", "the rule that limits acquisition, retention, or use of unnecessary information"),
            ("Source protection", "the duty to reduce risk to people, methods, and sensitive relationships"),
            ("Evaluation", "the feedback step that tests whether the evidence satisfied the requirement"),
            ("Gray-zone indicator", "an observable signal of ambiguous coercion below armed conflict thresholds"),
            ("Proxy pattern", "a relationship suggesting indirect sponsorship without confirmed operational control"),
        ),
        worked_scenario="a synthetic policy cell compares public indicators of hybrid pressure against an authorized collection plan for a benign border-disruption exercise",
        worked_input="public notices, synthetic interview summaries, public logistics records, and an instructor scope card",
        worked_process="rank requirements, choose the least intrusive source discipline, list excluded actions, and evaluate evidence quality",
        worked_output="a requirements-to-evidence matrix with discipline fit, source caveats, minimization notes, and gaps",
        practice_focus="requirements decomposition and source-discipline fit",
        review_question="Which gray-zone indicator changes the least-intrusive source choice without crossing into operational tasking?",
    ),
    "financial_economic_security": CoursebookProfile(
        identifier="financial_economic_security",
        disciplinary_frame=(
            "FININT and economic-security analysis as lawful due diligence: "
            "signals are interpreted through official lists, typology context, "
            "beneficial-ownership uncertainty, and compliance boundaries"
        ),
        key_distinction="separate compliance-oriented risk analysis from evasion, attribution certainty, or targeting",
        vocabulary=(
            ("Typology", "a recurring pattern used to recognize financial-crime or sanctions-risk signals"),
            ("Sanctions program", "the legal and policy structure behind a restricted-party or country measure"),
            ("Beneficial ownership", "the natural-person control or ownership question behind an entity"),
            ("Red flag", "an indicator that triggers review rather than a standalone conclusion"),
            ("Compliance boundary", "the line between lawful screening or resilience analysis and prohibited evasion advice"),
        ),
        worked_scenario="a sample nonprofit screens a synthetic supplier record for classroom due-diligence practice",
        worked_input="toy entity records, public sanctions-program descriptions, synthetic transaction summaries, and supplier-context notes",
        worked_process="check official list provenance, identify red flags, preserve beneficial-ownership uncertainty, and avoid evasion guidance",
        worked_output="an economic-security packet with source links, uncertainty, red-flag rationale, and a compliance review owner",
        practice_focus="defensive due diligence and uncertainty-preserving FININT",
        review_question="Which red flag requires escalation, and what evidence is still missing?",
    ),
    "counterintelligence_source_integrity": CoursebookProfile(
        identifier="counterintelligence_source_integrity",
        disciplinary_frame=(
            "counterintelligence as source-integrity defense: the class studies "
            "how institutions protect evidence, people, access, and judgment "
            "from deception and compromise"
        ),
        key_distinction="separate defensive awareness from surveillance, handling, or operational security playbooks",
        vocabulary=(
            ("Source integrity", "confidence that evidence has not been distorted, laundered, or compromised"),
            ("Compromise signal", "a clue that access, identity, or source reliability needs review"),
            ("Corroboration", "independent support that reduces single-source vulnerability"),
            ("Insider risk", "risk created by trusted access combined with motive, pressure, or control failure"),
            ("Protected disclosure", "a safe channel for reporting concerns without exposing sensitive details"),
        ),
        worked_scenario="a sample research lab reviews a synthetic source-quality anomaly after a disputed report",
        worked_input="toy access logs, public policy excerpts, synthetic source notes, and a reviewer escalation path",
        worked_process="separate identity from access, list anomaly hypotheses, seek corroboration, and route sensitive concerns to review",
        worked_output="a source-integrity memo with competing explanations, confidence, protected-disclosure note, and next-review owner",
        practice_focus="deception-aware source review and defensive escalation",
        review_question="Which explanation preserves uncertainty without ignoring a possible compromise signal?",
    ),
    "cognitive_influence_security": CoursebookProfile(
        identifier="cognitive_influence_security",
        disciplinary_frame=(
            "cognitive security as protection of attention, trust, memory, and "
            "decision quality without creating manipulation"
        ),
        key_distinction="separate analysis of influence from persuasion design",
        vocabulary=(
            ("Narrative provenance", "where a claim, frame, or story came from and how it spread"),
            ("Prebunking", "transparent education that helps people recognize misleading patterns before exposure"),
            ("Audience harm", "a privacy, dignity, autonomy, or trust risk for people receiving information"),
            ("Attribution caution", "the rule that intent and origin claims need strong evidence"),
            ("Resilience response", "a transparent education, correction, or process improvement that avoids manipulation"),
            ("MISO boundary", "the line between authorized public messaging analysis and covert influence design"),
            ("Inoculation", "building recognition of manipulation tactics without deploying persuasion against a population"),
        ),
        worked_scenario="a sample public-library class evaluates a synthetic rumor about a community service and compares transparent correction options",
        worked_input="sample posts, source timestamps, public-service facts, and a media-literacy rubric",
        worked_process="trace narrative provenance, separate observation from attribution, name audience harms, and design a transparent lesson",
        worked_output="a narrative-risk map with caveats, response options, and no microtargeted persuasion",
        practice_focus="information-integrity analysis and resilience education",
        review_question="Which response informs people without crossing into MISO-style manipulation or unverified attribution?",
    ),
    "historical_declassified_sources": CoursebookProfile(
        identifier="historical_declassified_sources",
        disciplinary_frame=(
            "historical intelligence study as declassified evidence review: "
            "archives teach institutional lessons when provenance, redaction, "
            "context, and modern boundaries are explicit"
        ),
        key_distinction="separate historical lesson from reconstruction of live tactics or current sources and methods",
        vocabulary=(
            ("Declassification context", "the release channel, date, and limits of an official historical source"),
            ("Redaction caveat", "the warning that missing text may change interpretation"),
            ("Institutional lesson", "the durable governance or analytic principle drawn from a case"),
            ("Presentism", "the error of forcing modern assumptions onto a historical record"),
            ("Modern analogy", "a bounded comparison that preserves differences between eras"),
            ("Oversight failure", "a documented breakdown in review, records, or accountability visible in the archive"),
            ("Source-protection lesson", "the historical principle about protecting people and methods without reconstructing live tradecraft"),
        ),
        worked_scenario="a sample seminar studies a declassified reform episode and extracts an oversight lesson without reconstructing current sources and methods",
        worked_input="public archive metadata, a short excerpt, a timeline template, and an oversight-question worksheet",
        worked_process="record provenance, mark redactions, build timeline, distinguish known from unknown, and extract a governance lesson",
        worked_output="a historical case card with release context, caveats, lesson, and non-operational boundary",
        practice_focus="declassified-source interpretation and case-to-principle translation",
        review_question="Which institutional lesson is defensible from the record, and which claim reconstructs live tradecraft?",
    ),
    "cyber_threat_intelligence": CoursebookProfile(
        identifier="cyber_threat_intelligence",
        disciplinary_frame=(
            "cyber threat intelligence as defensive normalization: incidents, "
            "indicators, TTPs, vendor risks, and sharing rules become useful only "
            "when scoped and validated"
        ),
        key_distinction="separate defensive mapping and incident learning from exploit, persistence, or evasion instruction",
        vocabulary=(
            ("Indicator", "an observable signal that may support defensive detection or investigation"),
            ("TTP", "a tactic, technique, or procedure used for structured defensive mapping"),
            ("Sighting", "a bounded observation of a possible indicator in a given context"),
            ("Handling rule", "a sharing, marking, or retention limit for threat information"),
            ("Lessons learned", "the post-incident evidence that changes controls or playbooks"),
        ),
        worked_scenario="a sample campus SOC reviews fabricated alert records after a tabletop incident",
        worked_input="toy alerts, synthetic asset names, public ATT&CK technique descriptions, and a sharing-policy card",
        worked_process="normalize indicators, map TTPs defensively, rate confidence, mark sharing limits, and record lessons learned",
        worked_output="a CTI packet with indicators, TTP mapping, confidence, handling rule, and remediation owner",
        practice_focus="defensive CTI normalization and tabletop incident learning",
        review_question="Which indicator is useful only after context and confidence are added?",
    ),
    "ics_ot_defense": CoursebookProfile(
        identifier="ics_ot_defense",
        disciplinary_frame=(
            "ICS/OT intelligence as safety-aware defensive reasoning: asset state, "
            "engineering consequence, operator decision, and recovery evidence "
            "matter as much as cyber indicators"
        ),
        key_distinction="separate cyber analysis from unsafe process control or live operational action",
        vocabulary=(
            ("Engineering state", "the physical or process condition that gives cyber evidence safety meaning"),
            ("Consequence", "the operational, safety, environmental, or service effect of a condition"),
            ("Defense in depth", "layered prevention, detection, response, and recovery controls"),
            ("Tabletop inject", "a synthetic event used to rehearse decisions without touching live systems"),
            ("Recovery evidence", "proof that a safe state, service, or learning objective was restored"),
        ),
        worked_scenario="a sample water-utility tabletop reviews synthetic process logs after a simulated anomaly",
        worked_input="toy HMI screenshots, fabricated network alerts, public ICS control guidance, and a safety stop card",
        worked_process="map assets to consequences, classify tabletop injects, identify human decisions, and preserve recovery evidence",
        worked_output="a cyber-physical tabletop packet with assets, consequences, ATT&CK mapping, decisions, and debrief",

        practice_focus="safety-aware tabletop readiness and defensive coverage review",
        review_question="Which cyber observation changes meaning once physical consequence is considered?",
    ),
    "legal_oversight": CoursebookProfile(
        identifier="legal_oversight",
        disciplinary_frame=(
            "legal and oversight architecture as design constraint: authority, "
            "rights, auditability, proportionality, transparency, and redress "
            "shape what work may proceed"
        ),
        key_distinction="separate having a capability from having authority and accountable review",
        vocabulary=(
            ("Authority", "the legal, institutional, or classroom basis for an activity"),
            ("Proportionality", "the test that a method is no more intrusive than the need justifies"),
            ("Oversight", "independent review that can challenge or constrain the activity"),
            ("Redress", "a path for affected people to contest or correct harm"),
            ("Audit trail", "retained evidence that enables later review of decisions and outputs"),
        ),
        worked_scenario="a sample agency training team reviews whether a classroom AI workflow is allowed",
        worked_input="public policy excerpts, synthetic workflow notes, a rights-impact checklist, and an audit-log template",
        worked_process="map authority, test proportionality, name affected groups, assign oversight, and define redress or escalation",
        worked_output="an authority-and-impact register with approvals, limits, audit owner, and review date",
        practice_focus="authority mapping and rights-aware release review",
        review_question="What control turns a capability into an accountable, reviewable workflow?",
    ),
}


def _normalized_lookup_key(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", value.lower()).strip()


def _profile_by_identifier(identifier: str) -> IntelligenceProfile:
    for profile in INTELLIGENCE_PROFILES:
        if profile.identifier == identifier:
            return profile
    raise KeyError(identifier)


def _lens_by_identifier(identifier: str) -> PracticeLens:
    for lens in PRACTICE_LENSES:
        if lens.identifier == identifier:
            return lens
    raise KeyError(identifier)


def _match_score(terms: tuple[str, ...], haystack: str) -> int:
    score = 0
    for term in terms:
        escaped = re.escape(term.lower())
        if re.search(rf"(?<![a-z0-9]){escaped}(?![a-z0-9])", haystack):
            score += 4 if " " in term or "-" in term else 2
    return score


def profile_for_titles(
    part_title: str,
    section_title: str = "",
    chapter: dict[str, object] | None = None,
) -> IntelligenceProfile:
    """Return the best content profile for a part or chapter title."""
    if chapter and chapter.get("content_profile"):
        return _profile_by_identifier(str(chapter["content_profile"]))

    haystack = f"{section_title} {part_title}".lower()
    best = INTELLIGENCE_PROFILES[0]
    best_score = -1
    for profile in INTELLIGENCE_PROFILES:
        score = _match_score(profile.match_terms, haystack)
        if score > best_score:
            best = profile
            best_score = score
    return best


def practice_lens_for_titles(
    part_title: str,
    section_title: str = "",
    chapter: dict[str, object] | None = None,
) -> PracticeLens:
    """Return the best reusable practice lens for a part, chapter, or subsection."""
    if chapter and chapter.get("practice_lens"):
        return _lens_by_identifier(str(chapter["practice_lens"]))

    part_key = _normalized_lookup_key(part_title)
    section_key = _normalized_lookup_key(section_title)
    if (
        any(term in part_key for term in ("industrial", "ics", "operational technology"))
        and any(term in section_key for term in ("incident", "attack", "att ck", "threat"))
    ):
        return _lens_by_identifier("cyber_physical_readiness")

    haystack = f"{section_title} {part_title}".lower()
    best = PRACTICE_LENSES[0]
    best_score = -1
    for lens in PRACTICE_LENSES:
        score = _match_score(lens.match_terms, haystack)
        if score > best_score:
            best = lens
            best_score = score
    return best


def anchor_references(keys: tuple[str, ...]) -> list[ResearchAnchor]:
    """Resolve anchor keys while preserving order and failing on typos."""
    missing = [key for key in keys if key not in ALL_PROFILE_ANCHORS_BY_KEY]
    if missing:
        missing_keys = ", ".join(missing)
        raise KeyError(f"Unknown AGEINT research anchor keys: {missing_keys}")
    return [ALL_PROFILE_ANCHORS_BY_KEY[key] for key in keys]


def _safe_pattern_profile(number: int | None) -> SafePatternProfile:
    if number is None:
        return SafePatternProfile(
            key="source_subsection",
            safe_name="Source-Guide Safety Treatment",
            methods="source description, safety translation, and instructor review",
            application="authorized curriculum-only exercise with public or synthetic material",
            safety_boundary="keeps source material educational, defensive, and non-operational",
        )
    return SAFE_PATTERN_PROFILES[number]


def safe_pattern_rows(patterns: list[dict[str, Any]]) -> str:
    """Render identity-preserving but safety-transformed AGEINT pattern rows."""
    rows = [
        "| Source identity | Safe curriculum treatment | Methods | Defensive application | Safety boundary |",
        "|---|---|---|---|---|",
    ]
    for pattern in patterns:
        number = int(pattern["number"])
        profile = _safe_pattern_profile(number)
        rows.append(
            "| "
            f"Pattern {number}: {pattern['name']} (source identity only) | "
            f"{profile.safe_name} | {profile.methods} | {profile.application} | "
            f"{profile.safety_boundary} |"
        )
    return "\n".join(rows)


def safe_pattern_treatment(
    section_title: str,
    active_pattern_number: int | None = None,
) -> tuple[str, int | None]:
    """Return a safe treatment for a raw pattern subsection title."""
    pattern_match = re.match(r"Pattern\s+(\d+):\s+(.+?)(?:\s+[-\u2014]|$)", section_title)
    if pattern_match:
        number = int(pattern_match.group(1))
        profile = _safe_pattern_profile(number)
        return (
            f"Pattern {number}: {profile.safe_name} "
            f"(source identity preserved in pattern registry) - {profile.safety_boundary}",
            number,
        )

    profile = _safe_pattern_profile(active_pattern_number)
    if section_title.startswith("Methods:"):
        return f"Safe methods: {profile.methods}", active_pattern_number
    if section_title.startswith("Application:"):
        return f"Safe defensive application: {profile.application}", active_pattern_number
    if section_title.startswith("Code Archetype:"):
        return (
            "Safe architecture artifact: diagram an allowlisted, logged, "
            f"revocable workflow for {profile.safe_name}",
            active_pattern_number,
        )
    return section_title, active_pattern_number
