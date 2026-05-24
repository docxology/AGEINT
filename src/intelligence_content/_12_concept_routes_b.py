"""Mid-section domain keyword concept routes (split to keep modules under 500 lines)."""

from __future__ import annotations

CONCEPT_KEYWORD_ROUTES_B: tuple[tuple[tuple[str, ...], str], ...] = (
    (("information architecture", "knowledge management"), (
        "Design information flows so requirements, sources, judgments, and "
        "records remain discoverable and auditable."
    )),
    (("cognitive load", "decision fatigue", "operator"), (
        "Manage analyst workload through prioritization, checklists, rest "
        "boundaries, and explicit handoff—not heroics."
    )),
    (("scada", "dcs", "plc", "operational technology", "industrial control"), (
        "Map industrial assets, safety interlocks, operator roles, and "
        "consequence before any cyber-physical inference."
    )),
    (("purdue model", "isa-95"), (
        "Use the Purdue model to separate IT and OT zones, monitoring points, "
        "and safety-critical controls in tabletop review."
    )),
    (("isac", "information sharing", "critical infrastructure"), (
        "Evaluate ISAC sharing by handling rules, anonymization, confidence, "
        "and consumer responsibilities."
    )),
    (("executive order", "fisa", "icd ", "e.o."), (
        "Map the legal source to authority, oversight, retention, and redress "
        "fields before any workflow is allowed."
    )),
    (("proportionality", "privacy", "civil liberties", "pcplob"), (
        "Test whether a method is no more intrusive than the authorized need "
        "justifies and whether affected groups have redress."
    )),
    (("human rights", "hria", "dpia"), (
        "Connect rights-impact review to affected groups, mitigation, "
        "documentation, and accountable oversight."
    )),
    (("ai governance", "ai ethics", "icd 505"), (
        "Bind AI use to purpose, evaluation, human review, rights impact, "
        "and retention before deployment in analysis."
    )),
    (("ukusa", "five eyes"), (
        "Use the sharing arrangement to distinguish alliance governance, handling "
        "rules, legal authority, and source caveats."
    )),
    (("tu delft", "thesis", "dissertation"), (
        "Read the thesis as a scholarly application source: identify its question, "
        "method, assumptions, and limits before borrowing any intelligence lesson."
    )),
    (("perception", "memory", "reasoning", "brain"), (
        "Connect cognitive science claims to analytic bias literacy: what the "
        "brain prioritizes, what it misses, and how review compensates."
    )),
    (("agent", "multi-agent", "llm agent"), (
        "Treat agents as software actors with explicit permissions, logs, stop "
        "conditions, and human approval—not autonomous decision makers."
    )),
    (("rag", "retrieval", "vector"), (
        "Evaluate retrieval pipelines by source provenance, injection risk, "
        "citation fidelity, and reviewer verification of answers."
    )),
    (("workflow", "orchestration", "pipeline"), (
        "Document workflow stages with inputs, transforms, reviewers, and "
        "blocked actions at each handoff."
    )),
    (("getting things done", "gtd"), (
        "Use GTD as a decision-hygiene framework: capture, clarify, organize, "
        "review, and engage—with explicit authority for what enters analysis."
    )),
    (("zettelkasten",), (
        "Treat linked notes as provenance-aware evidence cards, not a substitute "
        "for source validation or dissemination marking."
    )),
    (("obsidian", "roam research", "logseq", "pkm", "personal knowledge"), (
        "Evaluate PKM tools by provenance, access control, exportability, and "
        "review gates—not by collection volume."
    )),
    (("information diet", "source hygiene", "distraction architecture"), (
        "Design intake boundaries so requirements, sources, and judgments stay "
        "separate from noise and unverified feeds."
    )),
    (("stuxnet", "olympic games"), (
        "Study the incident as a tabletop lesson in safety consequence, attribution "
        "caution, and defensive coverage—not as attack replication."
    )),
    (("blackenergy", "ukraine power"), (
        "Read the outage case through engineering state, operator decisions, and "
        "recovery evidence in a fictional tabletop."
    )),
    (("triton", "trisis", "safety instrumented"), (
        "Focus on safety-system integrity, operator escalation, and consequence "
        "mapping—not live process manipulation."
    )),
    (("crashoverride", "industroyer"), (
        "Map protocol-aware disruption to defensive detection questions and "
        "recovery evidence in synthetic records."
    )),
    (("havex", "irongate"), (
        "Use supply-chain and HMI-trust motifs to review provenance, segmentation, "
        "and tabletop detection gaps."
    )),
    (("nerc cip", "nerc"), (
        "Connect NERC CIP requirements to asset inventory, access control, and "
        "audit evidence—not operational bypass."
    )),
    (("executive order 12333", "eo 12333"), (
        "Map EO 12333 authorities to collection limits, oversight, retention, and "
        "accountable review before any workflow proceeds."
    )),
    (("whistleblow", "leaking", "epistemic duty"), (
        "Separate lawful disclosure channels, source protection, and oversight "
        "from unauthorized release or targeting narratives."
    )),
    (("gdpr", "ripa", "investigatory powers"), (
        "Compare allied legal frameworks by authority scope, retention, redress, "
        "and proportionality—not by capability alone."
    )),
    (("proxy", "proxy war", "proxy indicator"), (
        "Treat proxy indicators as attribution-cautious evidence of indirect "
        "sponsorship, not proof of operational control."
    )),
    (("information warfare", "info warfare"), (
        "Analyze information warfare through narrative provenance, audience harm, "
        "and transparent resilience—not influence operations design."
    )),
    (("flow state", "flow experience", "csikszentmihalyi", "peak performance"), (
        "Treat flow claims as operator-performance literacy: define task clarity, "
        "feedback, and review boundaries—not unsustainable pace."
    )),
    (("nasa-tlx", "nasa tlx", "task load index"), (
        "Use workload indexes as review triggers for prioritization, handoff, "
        "and rest—not as heroics metrics."
    )),
    (("biometric", "physiological monitoring"), (
        "Evaluate biometric monitoring by consent, minimization, purpose limits, "
        "and human review of alerts."
    )),
    (("circadian", "chronotype", "sleep debt"), (
        "Connect circadian timing to scheduling, rest boundaries, and error-risk "
        "review—not operational timing advice."
    )),
    (("red cell", "adversarial wargam"), (
        "Use red-cell review to surface disconfirming evidence and assumptions "
        "before dissemination."
    )),
    (("network analysis", "link chart", "social network analysis"), (
        "Build link charts from fictional entities with provenance, confidence, "
        "and explicit gaps—not live targeting."
    )),
    (("timeline analysis", "event sequencing"), (
        "Sequence events with source timestamps, uncertainty bands, and "
        "alternative orderings before inferring causality."
    )),
    (("collection management", "requirements gap", "tasking"), (
        "Map requirements to collection gaps, priorities, and reviewer sign-off."
    )),
    (("writing intelligence", "intelligence products", "estimates", "warning"), (
        "Draft intelligence products with analytic line, caveats, audience, "
        "and dissemination marks."
    )),
    (("communicating uncertainty", "analytic line", "raw reporting"), (
        "Separate raw reporting from assessed analytic line with explicit "
        "confidence and dissent."
    )),
    (("machine-assisted", "when to automate"), (
        "Decide automation boundaries with logging, evaluation, and mandatory "
        "human review gates."
    )),
    (("counterintelligence", "double-agent", "triple-cross", "polygraph", "damage assessment"), (
        "Frame CI topics as source-vetting, anomaly review, and institutional "
        "protection—not operational entrapment."
    )),
    (("oss ", "office of strategic services", "simple sabotage", "morale operations"), (
        "Study OSS declassified manuals for oversight, ethics, and limits on "
        "translating history into practice."
    )),
    (("alternative futures", "brainstorming", "divergent thinking"), (
        "Use structured ideation to widen alternatives before converging on "
        "evidence-tested judgments."
    )),
    (("imint", "imagery intelligence"), (
        "Audit imagery products for resolution, temporal fit, and uncertainty "
        "before geospatial claims."
    )),
    (("epistemic security", "epistemic governance", "malign influence"), (
        "Protect knowledge production with provenance, dissent channels, and "
        "transparent correction—not narrative control."
    )),
    (("formal methods", "cognitive guarantees"), (
        "Evaluate formal guarantees as design claims requiring assumptions, "
        "limits, and independent review."
    )),
    (("langchain", "langgraph", "langsmith", "crewai", "autogen", "semantic kernel"), (
        "Evaluate agent frameworks by logging, tool allowlists, human approval, "
        "and blocked external actions—not production deployment recipes."
    )),
    (("lcel", "expression language"), (
        "Treat orchestration languages as auditable workflow specs with "
        "reviewer gates at each transform."
    )),
)
