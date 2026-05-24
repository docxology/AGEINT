"""Domain keyword concept routes for topic lesson frames."""

from __future__ import annotations

import re

from ._12_concept_routes_domains import DOMAIN_CONCEPT_ROUTES


def _title_tokens(raw_lower: str) -> set[str]:
    return set(re.findall(r"[a-z0-9]+", raw_lower))


def _match_keywords(raw_lower: str, keywords: tuple[str, ...]) -> bool:
    tokens = _title_tokens(raw_lower)
    for keyword in keywords:
        normalized = keyword.strip().lower()
        if not normalized:
            continue
        if " " in normalized or "-" in normalized:
            if normalized in raw_lower:
                return True
        elif normalized in tokens:
            return True
    return False


def _first_matching_frame(raw_lower: str, routes: tuple[tuple[tuple[str, ...], str], ...]) -> str | None:
    for keywords, frame in routes:
        if _match_keywords(raw_lower, keywords):
            return frame
    return None


CONCEPT_KEYWORD_ROUTES: tuple[tuple[tuple[str, ...], str], ...] = (
    (("free energy", "predictive processing"), (
        "Define prediction error, generative model, and uncertainty in plain language, "
        "then show how the theory helps an analyst notice when a model is explaining "
        "too much from too little evidence."
    )),
    (("computational model", "active inference"), (
        "Treat active inference as an agent-modeling vocabulary: beliefs, actions, "
        "expected observations, and policy selection are classroom concepts, not proof "
        "that an intelligence agent should act autonomously."
    )),
    (("shared protentions", "multi-agent active inference"), (
        "Use shared protentions to discuss how several agents or analysts can hold "
        "compatible expectations while still preserving dissent, uncertainty, and "
        "human review."
    )),
    (("social organization", "intelligence communit"), (
        "Map the theory to institutions: priorities, feedback, incentives, review "
        "loops, and records shape what an intelligence community notices and ignores."
    )),
    (("verses", "multi-scale"), (
        "Read the architecture claim as a layered-systems example: separate public "
        "research claims, implementation assumptions, evaluation evidence, and "
        "governance limits."
    )),
    (("nature of intelligence", "definition of intelligence"), (
        "Define intelligence as information gathered to reduce decision uncertainty for "
        "an authorized customer, separating collection, analysis, and covert action."
    )),
    (("intelligence cycle", "intelligence process"), (
        "Trace requirements through collection, processing, analysis, dissemination, "
        "and feedback while naming authority and audience at each transition."
    )),
    (("ic architecture", "community architecture", "intelligence community"), (
        "Compare civilian, military, and technical components by mission, oversight "
        "chain, and product type rather than by organizational chart alone."
    )),
    (("tradecraft core principles", "core tradecraft principles"), (
        "State the tradecraft principle as a repeatable judgment rule with evidence "
        "burden, caveat language, and reviewer accountability."
    )),
    (("collection management", "requirements management"), (
        "Match intelligence requirements to least-intrusive source disciplines with "
        "explicit minimization and feedback to the customer."
    )),
    (("humint", "human source", "agent handling", "case officer"), (
        "Treat human-source work as a governed relationship: validation, consent, "
        "reporting, source protection, and oversight—not contact activity."
    )),
    (("mice", "rascls"), (
        "Use the motivation taxonomy to recognize recruitment-risk narratives and "
        "ethics constraints, not to design persuasion."
    )),
    (("recruitment", "spotting", "assessment and development"), (
        "Read recruitment doctrine as risk literacy: pressure, consent, validation, "
        "and the line that blocks operational contact."
    )),
    (("source protection", "source validation"), (
        "Connect source-protection duties to reporting quality, compartmentation, "
        "and counterintelligence review without recreating handling tradecraft."
    )),
    (("comint", "elint"), (
        "Distinguish communications content from electronic signatures by evidence "
        "type, authority, minimization, and uncertainty."
    )),
    (("sigint", "signals intelligence"), (
        "Frame SIGINT as authority-bound collection with minimization, handling "
        "rules, and communications-security implications."
    )),
    (("metadata", "traffic analysis"), (
        "Treat metadata as a distinct evidence class with its own minimization, "
        "correlation limits, and legal review requirements."
    )),
    (("cryptanalysis",), (
        "Explain cryptographic analysis as a technical discipline bounded by lawful "
        "access, key management policy, and communications security."
    )),
    (("cryptographic lawful", "cryptographic", "encryption"), (
        "Frame encryption as a policy and assurance trade-off among confidentiality, "
        "lawful process, communications security, and trust."
    )),
    (("lawful intercept", "lawful access"), (
        "Map lawful-access claims to authority, proportionality, oversight, and "
        "retention—not to interception mechanics."
    )),
    (("osint", "open source"), (
        "Treat open sources as publicly available evidence that still requires "
        "provenance, corroboration, legality, and minimization before reuse."
    )),
    (("verification", "claim verification"), (
        "Apply verification steps: source identity, chain, recency, corroboration, "
        "and explicit uncertainty before a claim enters analysis."
    )),
    (("social media", "platform osint"), (
        "Evaluate social-source claims by account provenance, manipulation risk, "
        "terms of use, and identity-exposure limits."
    )),
    (("dark web", "darknet"), (
        "Discuss dark-web sources only through governance: legality, safety, "
        "provenance limits, and instructor-provided synthetic records."
    )),
    (("geoint", "imagery", "geospatial", "imint"), (
        "Treat location evidence as a quality and uncertainty problem, separating "
        "map interpretation from targeting or attribution."
    )),
    (("resolution", "accuracy", "scale"), (
        "Compare resolution, accuracy, and temporal fitness before drawing a "
        "geospatial conclusion from imagery or map products."
    )),
    (("cyber intelligence", "cyber threat", "cti lifecycle"), (
        "Organize cyber intelligence as defensive evidence: indicators, context, "
        "confidence, handling rules, and control implications."
    )),
    (("kill chain", "att&ck", "attack lifecycle"), (
        "Use the model as defensive vocabulary for sequencing observations, not as "
        "a checklist of adversary actions."
    )),
    (("advanced persistent", " apt"), (
        "Study APT reporting as attribution and confidence literacy: technical "
        "similarity, context, caveats, and geopolitical inference stay separate."
    )),
    (("supply chain", "solarwinds", "sunburst", "xz utils", "sbom"), (
        "Shows how package provenance, social trust, build integrity, and "
        "assurance controls turn a software incident into reviewable evidence."
    )),
    (("stix", "taxii", "threat sharing"), (
        "Use sharing standards to document indicator context, handling, "
        "confidence, and consumer responsibilities—not raw indicator hoarding."
    )),
    (("incident response", "ir lifecycle"), (
        "Map incident phases to evidence preservation, stakeholder notification, "
        "learning loops, and defensive control updates."
    )),
    (("cve-", "backdoor", "vulnerability"), (
        "Treat the vulnerability record as an assurance case: severity, affected "
        "component, provenance, mitigation status, and uncertainty stay separate."
    )),
    (("attribution", "apt29", "svr"), (
        "Use attribution indicators cautiously by separating technical similarity, "
        "context, confidence, and geopolitical inference."
    )),
    (("sbom", "slsa", "sigstore"), (
        "Use the control framework to document package identity, build provenance, "
        "signature evidence, and gaps in supplier assurance."
    )),
    (("financial intelligence", "finint"), (
        "Read financial intelligence as due-diligence evidence that triggers review "
        "rather than proof of intent or guilt."
    )),
    (("beneficial ownership", "sanctions", "ofac"), (
        "Read ownership and sanctions signals as due-diligence evidence that "
        "triggers review rather than proof of intent."
    )),
    (("money laundering", "suspicious activity", "sar"), (
        "Use typologies to structure review of transactional patterns, source "
        "quality, and escalation thresholds—not investigative targeting."
    )),
    (("psyop", "miso", "psychological operation"), (
        "Study influence doctrine as audience analysis, message integrity, and "
        "ethics—not as manipulation technique."
    )),
    (("disinformation", "misinformation", "active measures"), (
        "Analyze influence campaigns through provenance, audience harm, "
        "attribution caution, and transparent response options."
    )),
    (("social engineering", "phishing", "pretexting"), (
        "Teach defensive recognition of manipulation attempts using fictional "
        "messages, consent boundaries, and reporting duties."
    )),
    (("prebunking", "inoculation", "debunking"), (
        "Use inoculation methods to build audience resilience with transparent "
        "labels, source checks, and non-manipulative corrections."
    )),
    (("counterintelligence", "source integrity", "mole"), (
        "Frame counterintelligence as source-vetting, anomaly review, and "
        "institutional protection—not operational entrapment."
    )),
    (("insider threat", "vetting"), (
        "Connect insider-threat review to access control, behavior indicators, "
        "and accountable escalation paths."
    )),
    (("deception detection", "deception"), (
        "Compare deception indicators with alternative explanations and "
        "uncertainty before any operational inference."
    )),
    (("hybrid warfare", "gray zone", "irregular warfare"), (
        "Identify hybrid indicators—proxy activity, ambiguous attribution, "
        "sub-threshold pressure—without prescribing response actions."
    )),
    (("non-state", "terrorist", "insurgent", "militia"), (
        "Study non-state actors through organizational indicators, funding "
        "patterns, and open-source evidence with strict minimization."
    )),
    (("special operations", "unconventional warfare"), (
        "Read special-operations intelligence as support to authorized "
        "planning with explicit authority and oversight fields."
    )),
    (("cia", "nsa", "kgb", "mi6", "mossad", "church committee"), (
        "Study the declassified record for institutional lessons about oversight, "
        "source protection, and limits on translating history into practice."
    )),
    (("agent run card", "run card", "agent identity"), (
        "Document agent identity, tool permissions, stop conditions, logs, and "
        "human approval points for every delegated run."
    )),
    (("mcp", "model context protocol", "tool governance"), (
        "Evaluate tool protocols by allowlists, logging, provenance of retrieved "
        "content, and deny-by-default policies."
    )),
    (("pattern registry", "design pattern", "archetype"), (
        "Use pattern names as architectural vocabulary for allowlisted, logged, "
        "revocable workflows—not as operational playbooks."
    )),
    (("prompt injection", "jailbreak", "adversarial prompt"), (
        "Treat prompt attacks as trust-boundary failures requiring input "
        "sanitization, tool limits, and human review."
    )),
    (("evaluation loop", "red team", "adversarial eval"), (
        "Structure evaluation as misuse-case testing with blocked outcomes, "
        "logged evidence, and reviewer disposition."
    )),
    (("cognitive security", "cognitive attack surface"), (
        "Map cognitive attack surfaces: attention, belief formation, narrative "
        "provenance, and transparent correction options."
    )),
    (("structured analytic", "analysis of competing hypotheses", "ach"), (
        "Use the method to keep alternatives, disconfirming evidence, and "
        "confidence visible."
    )),
    (("key assumptions", "assumption"), (
        "List assumptions explicitly and test which ones would change the "
        "judgment if falsified."
    )),
    (("red team", "devil's advocate"), (
        "Use structured challenge to surface disconfirming evidence and "
        "overconfidence before dissemination."
    )),
    (("confidence language", "icd 203", "analytic confidence"), (
        "Calibrate confidence to evidence strength, source quality, and "
        "alternative explanations—not to rhetorical certainty."
    )),
    (("nine tradecraft", "analytic tradecraft standard"), (
        "Apply ICD 203 tradecraft standards: sourcing, uncertainty, distinctions, "
        "alternatives, relevance, argumentation, consistency, accuracy, and visuals."
    )),
)

from ._12_concept_routes_b import CONCEPT_KEYWORD_ROUTES_B

CONCEPT_KEYWORD_ROUTES = CONCEPT_KEYWORD_ROUTES + CONCEPT_KEYWORD_ROUTES_B + DOMAIN_CONCEPT_ROUTES
