from __future__ import annotations

from typing import Final

from ._01_part import PracticeLens




PRACTICE_LENSES: Final[tuple[PracticeLens, ...]] = (
    PracticeLens(
        identifier="dissemination_marking_control",
        title="Dissemination-and-Marking Control Lens",
        match_terms=(
            "nature of intelligence",
            "intelligence community architectures",
            "dissemination",
            "classification",
            "marking",
            "information architecture",
            "productivity intelligence",
        ),
        planning_question=(
            "Which audience, release authority, marking vocabulary, records duty, "
            "and feedback loop governs this intelligence artifact?"
        ),
        evidence_artifact=(
            "dissemination map with audience, caveat, marking, records, and "
            "feedback fields"
        ),
        validation_rule=(
            "verify source authority, public/classification status, CAPCO-safe "
            "vocabulary, audience need, and records disposition before reuse"
        ),
        handoff_contract=(
            "deliver release-neutral summaries, source metadata, marking rationale, "
            "and review ownership as separate fields"
        ),
        safety_check=(
            "exclude classified content, live release decisions, source-method "
            "exposure, and improvised control markings"
        ),
    ),
    PracticeLens(
        identifier="requirements_to_evidence",
        title="Requirements-to-Evidence Lens",
        match_terms=(
            "collection",
            "requirements",
            "sigint",
            "masint",
            "humint",
            "agent recruitment",
            "agent handling",
            "source",
            "osint",
            "geoint",
            "imagery",
        ),
        planning_question=(
            "What authorized requirement justifies the evidence, and which "
            "source discipline is the least intrusive fit?"
        ),
        evidence_artifact="requirements matrix with source descriptors, caveats, and collection limits",
        validation_rule=(
            "show priority, authority, minimization, corroboration, and source "
            "quality before any claim is reused"
        ),
        handoff_contract=(
            "deliver metadata-rich evidence packets, not unscoped data piles or "
            "implicit targeting requests"
        ),
        safety_check=(
            "exclude live collection, recruitment, surveillance, interception, "
            "tracking, and identity exposure"
        ),
    ),
    PracticeLens(
        identifier="ai_data_accountability",
        title="AI/Data Accountability Lens",
        match_terms=(
            "ai ethics",
            "ethics of intelligence",
            "legal authorities",
            "governance",
            "privacy",
            "data",
        ),
        planning_question=(
            "Which purpose, authority, data provenance, model limitation, "
            "impact level, public notice, and accountable human makes the AI use acceptable?"
        ),
        evidence_artifact=(
            "AI/data impact card with authority, provenance, model version, "
            "impact score, register status, human owner, and review cadence"
        ),
        validation_rule=(
            "confirm lawful data use, limitations, bias and accuracy testing, "
            "public-register fit, human accountability, and rights escalation"
        ),
        handoff_contract=(
            "handoff separates data lineage, model configuration, generated "
            "outputs, human judgments, retained records, and unresolved risks"
        ),
        safety_check=(
            "reject automated adverse action, hidden surveillance expansion, "
            "unowned outputs, unreviewed model drift, and opaque downstream reuse"
        ),
    ),
    PracticeLens(
        identifier="active_inference_boundary",
        title="Active-Inference Boundary Lens",
        match_terms=(
            "active inference",
            "free energy",
            "predictive processing",
            "expected free energy",
            "generative model",
            "shared protentions",
        ),
        planning_question=(
            "Which layer is formal theory, which layer is classroom analogy, "
            "which implementation claim needs evidence, and which governance "
            "control prevents autonomy overreach?"
        ),
        evidence_artifact=(
            "theory-to-governance card with source, analogy limit, assumption, "
            "reviewer, and stop condition"
        ),
        validation_rule=(
            "separate formal claim, pedagogical analogy, implementation "
            "assumption, evaluation evidence, and governance duty before reuse"
        ),
        handoff_contract=(
            "handoff preserves formal source, analogy scope, source limitation, "
            "caveat, reviewer owner, and blocked autonomous-action claim"
        ),
        safety_check=(
            "reject claims that the free-energy principle proves autonomous "
            "agency, intent, detection performance, or oversight-free action"
        ),
    ),
    PracticeLens(
        identifier="structured_judgment",
        title="Structured-Judgment Lens",
        match_terms=(
            "analysis",
            "analytic",
            "tradecraft",
            "structured",
            "historical",
            "counterintelligence",
            "assessment",
        ),
        planning_question=(
            "Which assumptions, alternatives, confidence statements, and source "
            "limits must stay visible for review?"
        ),
        evidence_artifact="analytic note with hypotheses, evidence table, confidence, and dissent fields",
        validation_rule=(
            "separate raw reporting, inference, judgment, and recommendation "
            "before synthesis"
        ),
        handoff_contract=(
            "handoff preserves alternatives, uncertainty, caveats, and revision "
            "history for downstream modules"
        ),
        safety_check=(
            "avoid policy advocacy, certainty inflation, source laundering, and "
            "claims without traceable evidence"
        ),
    ),
    PracticeLens(
        identifier="operator_workload_hygiene",
        title="Operator-Workload Hygiene Lens",
        match_terms=(
            "intelligent operator",
            "cognitive athlete",
            "productivity intelligence",
            "getting things done",
            "flow state",
            "nasa-tlx",
            "cognitive load",
            "circadian intelligence",
        ),
        planning_question=(
            "Which workload signal, capture habit, focus block, and reviewer "
            "handoff must stay explicit before the operator accepts more tasking?"
        ),
        evidence_artifact=(
            "operator workload card with queue state, NASA-TLX ratings, focus plan, "
            "handoff owner, and rest boundary"
        ),
        validation_rule=(
            "separate urgency from authority, workload from quality, and personal "
            "tempo claims from measured task-switching cost"
        ),
        handoff_contract=(
            "handoff preserves open loops, TLX scores, evidence packets, reviewer "
            "ownership, and blocked-use notes for the next shift"
        ),
        safety_check=(
            "exclude live operational tempo mandates, surveillance of people, "
            "performance coercion, and unreviewed tasking under fatigue"
        ),
    ),
    PracticeLens(
        identifier="historical_case_translation",
        title="Historical Case-Translation Lens",
        match_terms=(
            "historical intelligence services",
            "historical",
            "soviet",
            "russian",
            "american intelligence history",
            "british",
            "allied",
            "israeli",
            "continental services",
            "declassified",
        ),
        planning_question=(
            "Which declassified source, release context, institutional lesson, "
            "and modern boundary can be carried forward without recreating operations?"
        ),
        evidence_artifact=(
            "historical case card with provenance, redaction caveats, timeline, "
            "lesson, and non-operational boundary"
        ),
        validation_rule=(
            "distinguish what the record shows, what remains redacted or unknown, "
            "and which governance lesson is defensibly transferable"
        ),
        handoff_contract=(
            "handoff preserves archive citation, historical context, analytic "
            "lesson, oversight implication, and modern analogy as separate fields"
        ),
        safety_check=(
            "exclude reconstruction of current sources, methods, tactics, cover, "
            "or collection workflows from historical material"
        ),
    ),
    PracticeLens(
        identifier="economic_security_due_diligence",
        title="Economic-Security Due-Diligence Lens",
        match_terms=(
            "financial",
            "finint",
            "sanctions",
            "illicit finance",
            "money laundering",
            "terrorist financing",
            "proliferation financing",
            "export control",
            "export-control",
            "economic security",
            "due diligence",
        ),
        planning_question=(
            "Which financial, sanctions, export-control, or supplier-risk signal "
            "is being interpreted for lawful compliance or resilience?"
        ),
        evidence_artifact=(
            "economic-security packet with entity evidence, sanctions program, "
            "red flags, supplier context, uncertainty, and compliance boundary"
        ),
        validation_rule=(
            "verify official list source, typology provenance, beneficial-ownership "
            "uncertainty, export-control relevance, and non-evasion framing"
        ),
        handoff_contract=(
            "handoff separates raw source, entity hypothesis, compliance control, "
            "analytic judgment, and recommended defensive next review"
        ),
        safety_check=(
            "exclude sanctions evasion, laundering methods, threshold gaming, "
            "procurement bypasses, and tailored targeting of real firms"
        ),
    ),
    PracticeLens(
        identifier="agentic_tool_governance",
        title="Agentic Tool-Governance Lens",
        match_terms=(
            "ageint",
            "agentic",
            "ai agent",
            "mcp",
            "autogen",
            "crewai",
            "langchain",
            "langgraph",

            "python",
            "framework",
        ),
        planning_question=(
            "Which human authority, agent identity, tool permission, autonomy "
            "limit, incident threshold, and recoverability condition bounds the workflow?"
        ),
        evidence_artifact="agent run card with tool allowlist, identity, logs, autonomy limit, approval gates, and recovery path",
        validation_rule=(
            "verify least privilege, prompt-injection exposure, provenance, "
            "observability, stop conditions, and incident-reporting triggers"
        ),
        handoff_contract=(
            "export agent traces, tool calls, retrieved sources, policy decisions, "
            "and human approvals separately"
        ),
        safety_check=(
            "block excessive agency, shadow tools, credential leakage, autonomous "
            "deployment, and irreversible actions"
        ),
    ),
    PracticeLens(
        identifier="defensive_cyber_intelligence",
        title="Defensive Cyber-Intelligence Lens",
        match_terms=(
            "cyber intelligence",
            "advanced persistent",
            "apt",
            "kill chain",
            "attack framework",
            "threat intelligence",
            "incident response",
            "malware",
            "phishing",
        ),
        planning_question=(
            "Which defensive observation, confidence level, handling rule, and "
            "control implication can be stated without teaching adversary action?"
        ),
        evidence_artifact=(
            "defensive CTI packet with indicator context, taxonomy mapping, "
            "confidence, handling rule, and control implication"
        ),
        validation_rule=(
            "verify that taxonomy labels are descriptive, indicators are "
            "contextualized, incident categories are reviewable, and outputs remain detection or assurance oriented"
        ),
        handoff_contract=(
            "handoff separates observations, taxonomy labels, confidence, "
            "sharing limits, and defensive control recommendations"
        ),
        safety_check=(
            "exclude exploit steps, evasion instructions, malware construction, "
            "credential misuse, phishing instructions, and live response actions"
        ),
    ),
    PracticeLens(
        identifier="software_supply_chain_assurance",
        title="Software-Supply-Chain Assurance Lens",
        match_terms=(
            "supply-chain",
            "supply chain",
            "solarwinds",
            "sunburst",
            "xz utils",
            "maintainer",
            "sbom",
            "slsa",
            "sigstore",
            "backdoor",
        ),
        planning_question=(
            "Which package, maintainer signal, build artifact, provenance claim, "
            "and assurance control needs review?"
        ),
        evidence_artifact=(
            "software-supply-chain assurance packet with package provenance, "
            "maintainer-risk notes, build-integrity evidence, and control gaps"
        ),
        validation_rule=(
            "separate provenance evidence, social-trust signals, build controls, "
            "vulnerability claims, and attribution uncertainty"
        ),
        handoff_contract=(
            "handoff preserves package identity, source evidence, build evidence, "
            "review owner, uncertainty, and remediation priority as separate fields"
        ),
        safety_check=(
            "exclude exploit reproduction, maintainer targeting, backdoor mechanics, "
            "credential hunting, and live repository interference"
        ),
    ),
    PracticeLens(
        identifier="cognitive_resilience",
        title="Cognitive-Resilience Lens",
        match_terms=(
            "cognitive",
            "influence",
            "disinformation",
            "psyop",
            "psychological",
            "social engineering",
            "prebunking",
            "information warfare",
        ),
        planning_question=(
            "How does the module protect autonomy, attention, trust, and decision "
            "quality without designing persuasion?"
        ),
        evidence_artifact="narrative-risk map with provenance, uncertainty, audience harms, and response options",
        validation_rule=(
            "distinguish observation, attribution, impact assessment, and "
            "resilience response"
        ),
        handoff_contract=(
            "handoff supports transparency, education, and resilience, not "
            "microtargeted influence or deception"
        ),
        safety_check=(
            "exclude manipulation scripts, impersonation, persuasion targeting, "
            "and operational influence planning"
        ),
    ),
    PracticeLens(
        identifier="cyber_physical_readiness",
        title="Cyber-Physical Readiness Lens",
        match_terms=(
            "ics",
            "industrial",
            "operational technology",
            "cyber-physical",
            "critical infrastructure",
            "att&ck",
            "incident",
            "supply-chain",
            "threat intelligence",
        ),
        planning_question=(
            "Which asset, architecture record, consequence, operator decision, and "
            "recovery path is being exercised defensively?"
        ),
        evidence_artifact="tabletop packet with OT asset inventory, architecture record, consequences, injects, and debrief rubric",
        validation_rule=(
            "validate against safety, availability, engineering state, incident "
            "scope, and after-action learning"
        ),
        handoff_contract=(
            "separate cyber indicators, process observations, safety impact, "
            "operator choices, and recovery evidence"
        ),
        safety_check=(
            "keep exercises lab-only or tabletop; exclude exploitation, process "
            "manipulation, unsafe actuation, and live-control actions"
        ),
    ),
    PracticeLens(
        identifier="oversight_and_rights",
        title="Oversight-and-Rights Lens",
        match_terms=("legal", "ethical", "oversight", "authority", "privacy", "governance"),
        planning_question=(
            "Which authority, impact assessment, public-register entry, audit "
            "record, and escalation path must exist before the workflow is allowed?"
        ),
        evidence_artifact="authority-and-impact register with approvals, limits, public notice, audit owners, and review dates",
        validation_rule=(
            "confirm lawful purpose, proportionality, retention, review, and "
            "appeal or redress paths"
        ),
        handoff_contract=(
            "handoff includes approvals, policy constraints, audit evidence, "
            "and unresolved legal or ethical issues"
        ),
        safety_check=(
            "reject authority laundering, privacy overreach, unmanaged retention, "
            "and governance-as-afterthought"
        ),
    ),
)
