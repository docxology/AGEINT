### AGEINT Security and Adversarial Considerations governance boundary: synthesis, agent-assistance rules, rights, and assurance gates

**Navigation.** Parent section: [@sec:chapter-ageint-security-and-adversarial-considerations].

### AGEINT Security and Adversarial Considerations analytic synthesis: source-backed claims and forbidden leaps

**Contextual source routes.** For module 34's governance-boundary section, the **Agentic AI Governance and Tool Security** catalog routes include [@official_oecd_agentic_ai]; [@official_canada_agentic_ai_guide]; [@official_nist_ai_rmf]; [@official_nist_ai_600_1]. Check the actual passage, edition, claim scope and access limitations before use. Route membership does not establish relevance, independent corroboration or efficacy.

Research lane: **Agentic AI Governance and Tool Security** for **Agent Framework Security Vulnerabilities; PythonREPLTool risk: execution capability versus authorization**. [@ageint234]; [@ageint235].

**Curriculum topic spine:** **Agent Framework Security Vulnerabilities**, **PythonREPLTool risk: execution capability versus authorization**, **Cross-agent permission and contamination risk: source-guide CrewAI example**.
**Recorded source cluster; inspection and scope limits apply:** [@official_oecd_agentic_ai]; [@official_canada_agentic_ai_guide]; [@official_nist_ai_rmf]; [@official_nist_ai_600_1]; [@official_ic_ai_ethics_principles]; [@official_ic_ai_ethics_framework]; [@official_odni_icd_505].

**Conceptual depth:** delegated action under explicit authority, identity, permissions, tool boundaries, monitoring, and human escalation.

**Method stack:** AI RMF Govern-Map-Measure-Manage, least-privilege tool design, prompt-injection review, progressive deployment, and rollback drills.

**Composability contract:** agents, tools, credentials, memory, retrieval stores, policies, and logs remain separately inspectable and revocable components.

**Known failure modes:** excessive agency, shadow tools, indirect prompt injection, memory poisoning, confused authority, and unbounded action chains.

**Defensive boundary:** agentic workflows stay synthetic, owned-lab, supervised, logged, rate-limited, and reversible unless a lawful production authority exists. Applied to **Agent Framework Security Vulnerabilities; PythonREPLTool risk: execution capability versus authorization**.

| Anchor | Why it matters here |
|---|---|
| [@official_oecd_agentic_ai] | Official OECD conceptual foundation for agentic AI. Checked as of 2026-05-21; role: source_quality_anchor. |
| [@official_canada_agentic_ai_guide] | Government of Canada guide for accountable public-sector use of agentic AI, including governance, risk, transparency, testing, monitoring, and human oversight considerations. Checked as of 2026-08-30; role: curriculum_anchor. |
| [@official_nist_ai_rmf] | Official NIST.AI.100-1 risk-management framework. Checked as of 2026-05-21; role: source_quality_anchor. |
| [@official_nist_ai_600_1] | Official NIST AI 600-1 generative AI profile. Checked as of 2026-05-21; role: source_quality_anchor. |
| [@official_ic_ai_ethics_principles] | Official IC principles for lawful, accountable, objective, human-centered, secure, resilient, and science-informed AI. Checked as of 2026-05-21; role: curriculum_anchor. |
| [@official_ic_ai_ethics_framework] | Official IC framework for AI goals, authorities, human judgment, bias mitigation, testing, documentation, explainability, and review. Checked as of 2026-05-21; role: curriculum_anchor. |
| [@official_odni_icd_505] | Official IC AI governance directive covering CAIO roles, oversight, interoperability, civil-liberties review, training data, and impact assessment. Checked as of 2026-05-21; role: curriculum_anchor. |

#### Threat-model framework: MAESTRO seven layers

The CSA MAESTRO model gives a concrete map of where an agentic
system can be attacked, shown in [@fig:ageint-maestro-seven-layer]. It stacks seven layers of
the agent lifecycle: foundation models (L1: adversarial examples, model stealing, backdoors),
data operations (L2: poisoning, RAG-pipeline compromise), agent frameworks (L3: supply chain and
input validation), deployment and infrastructure (L4: container escape, lateral movement),
evaluation and observability (L5: metric manipulation, detection evasion), and the agent ecosystem
(L7: impersonation, marketplace and goal manipulation). The layer that carries the sharpest
lesson is L6, Security and Compliance, which is drawn cross-cutting every other layer rather than
stacked among them: the security agents you deploy to watch the system are themselves an attack
surface, so a mature design must monitor the monitors [@official_csa_maestro_threat_modeling];
[@official_owasp_agentic_ai_threats_mitigations].

#### Governance control: SRE circuit breaker

Knowing where attacks land is not the same as bounding their blast radius. The
author-defined SRE circuit-breaker teaching pattern, depicted in
[@fig:ageint-sre-circuit-breaker], borrows reliability vocabulary for a synthetic
governance tabletop, not a validated agent-safety threshold. In CLOSED the agent
operates only within explicit human-approved permissions. An illustrative
reliability budget may cover non-safety failures such as unavailable service or
tool timeouts; its limits must be declared for that exercise, not generalized
into a universal compliance percentage.

Authorization violations, private-data disclosure, and unsafe-action attempts
or execution are zero-tolerance breaches: immediately pause the affected agent
workflow, move to OPEN, preserve the record, and escalate to the accountable human.
Successful routine actions cannot offset these breaches in an averaged SLI.
Human review must establish containment and validate remediation before approving
limited restoration in HALF_OPEN, with restricted permissions and explicit stop
conditions. Any recurrence returns the workflow to OPEN. Returning to CLOSED
requires a separate, recorded human approval; a clean record or elapsed recovery
period never authorizes more autonomy automatically. Rehearse these transitions
with synthetic incident records, not live actions
[@scholarly_systems_security_agentic_computing].

#### AGEINT Security and Adversarial Considerations evidence standard and citation floor: source families and discovery limits

Official
guidance supplies governance, safety, and legal constraints for the **Agentic AI Governance and Tool Security**
lane; scholarly or policy-scholarship sources supply explanatory frames; source-guide
citations preserve the inherited AGEINT bibliography. Perplexity-assisted discovery
is allowed during maintenance, but the manuscript citation itself must resolve to a
direct source URL in `references-*.bib`. Local checks start with [@ageint234]; [@ageint235].

### AGEINT Security and Adversarial Considerations agentic boundary: assist, approve, block, and record

**Navigation.** Parent section: [@sec:chapter-ageint-security-and-adversarial-considerations].

AGEINT translation is bounded by the **Agentic AI Governance and Tool Security** lane.
Agents may organize sources, retrieve context, compare alternatives, draft
checklists, summarize evidence, simulate benign scenarios, and audit reasoning.
They do not initiate unauthorized collection, exploitation, covert targeting,
manipulation, or cyber-physical action; examples stay tied to **Agent Framework Security Vulnerabilities; PythonREPLTool risk: execution capability versus authorization**.

#### AGEINT Security and Adversarial Considerations permitted defensive utility: curriculum uses and safe outputs

**Navigation.** Parent section: [@sec:chapter-ageint-security-and-adversarial-considerations].

The defensive utility is curriculum design, tabletop preparation,
risk assessment, governance review, source evaluation, and resilience planning.
Work products fit the current unit's education, policy review, lab
exercises, and accountable defensive analysis for **Agent Framework Security Vulnerabilities; PythonREPLTool risk: execution capability versus authorization**.

#### AGEINT Security and Adversarial Considerations excluded operational boundary: blocked actions and stop rules

Keep all practice accountable, synthetic, defensive, logged, reversible, and evidence-bounded while working from [@ageint234]; [@ageint235] and **Agent Framework Security Vulnerabilities; PythonREPLTool risk: execution capability versus authorization**. Do not convert it into live targeting, evasion, exploitation, covert collection, manipulation, or unsafe cyber-physical action.

### AGEINT Security and Adversarial Considerations governance assurance: authority, rights, evidence, and human review

**Navigation.** Parent section: [@sec:chapter-ageint-security-and-adversarial-considerations].

Governance is practiced as a gate on the **Agentic AI Governance and Tool Security**
lane. Learners use the **Defensive Cyber-Intelligence Lens** to decide who is accountable for the exercise,
which evidence is sufficient, what rights and access issues remain, and when an
agent-assisted artifact must stop for human review while using **Agent Framework Security Vulnerabilities; PythonREPLTool risk: execution capability versus authorization**.

#### AGEINT Security and Adversarial Considerations governance card: gates, retained evidence, and review owner

| Gate | Coursebook check | Evidence retained |
|---|---|---|
| Authority | A legitimate educational or defensive purpose AND documented permission for the exact activity, data and tools are required, with a named reviewer. Classroom approval covers only the permitted fictional exercise; unknown or missing authority is a hold. | applicable rule and scope, data-use permission, excluded-action list, and accountable reviewer |
| Evidence | Separate contextual citations from the claim-specific passage, version, source dependence and limitations; begin the source review with [@ageint234]; [@ageint235]. | claim ledger, locators, source descriptors, alternatives, and separate likelihood/confidence fields |
| Rights and access | Privacy, accessibility, learner support, and affected-group impacts are considered before reuse. | rights note, accommodation path, and unresolved-risk owner |
| Agent control | Any agent assistance stays bounded to retrieval, comparison, drafting, simulation, critique, or audit. | tool allowlist, prompt/output record, stop condition, and rollback note |
| Assurance | The artifact is challenged against **Agentic AI Governance and Tool Security** failure modes and the **Defensive Cyber-Intelligence Lens** safety check. | failure-mode note, remediation item, retest result, and refresh trigger |

#### AGEINT Security and Adversarial Considerations evidence package handoff: appendices, records, and reuse

Detailed model/data cards, transparency notices, retention rows, release gates,
risk exceptions, incident drills, procurement and learner-support forms live in
the shared orientation sections and [@sec:method-assurance-reference]. The methods
appendices apply and link those forms rather than duplicating them.
The local **Defensive Cyber-Intelligence Lens** evidence gate stays compact enough to apply during
reading, practice, and revision for **Agent Framework Security Vulnerabilities; PythonREPLTool risk: execution capability versus authorization**.

#### AGEINT Security and Adversarial Considerations current-source assurance: verified anchors and local artifact fit

The source assurance check ties the current verified anchor set to the local chapter artifact instead of relying on discovery summaries, here covering **Agent Framework Security Vulnerabilities; PythonREPLTool risk: execution capability versus authorization**. [@ageint234]; [@ageint235].

| Assurance question | Direct source evidence | Chapter artifact |
|---|---|---|
| What does the module inherit from `official_oecd_agentic_ai` for **Agent Framework Security Vulnerabilities; PythonREPLTool risk: execution capability versus authorization**? | The Agentic AI Landscape and Its Conceptual Foundations; lane `source_quality_spine`; checked 2026-05-21. | defensive CTI packet with indicator context, taxonomy mapping, confidence, handling rule, and control implication; source-quality triangulation and claim-boundary review |
| What does the module inherit from `official_canada_agentic_ai_guide` for **Agent Framework Security Vulnerabilities; PythonREPLTool risk: execution capability versus authorization**? | Guide on the Use of Agentic Artificial Intelligence; lane `public_sector_agentic_ai`; checked 2026-08-30. | defensive CTI packet with indicator context, taxonomy mapping, confidence, handling rule, and control implication; bounded-autonomy run card, recoverability review, approval threshold, monitoring evidence, and public-sector service assurance |
| What does the module inherit from `official_nist_ai_rmf` for **Agent Framework Security Vulnerabilities; PythonREPLTool risk: execution capability versus authorization**? | Artificial Intelligence Risk Management Framework (AI RMF 1.0); lane `source_quality_spine`; checked 2026-05-21. | defensive CTI packet with indicator context, taxonomy mapping, confidence, handling rule, and control implication; source-quality triangulation and claim-boundary review |
| What does the module inherit from `official_nist_ai_600_1` for **Agent Framework Security Vulnerabilities; PythonREPLTool risk: execution capability versus authorization**? | Artificial Intelligence Risk Management Framework: Generative AI Profile; lane `source_quality_spine`; checked 2026-05-21. | defensive CTI packet with indicator context, taxonomy mapping, confidence, handling rule, and control implication; source-quality triangulation and claim-boundary review |
| How is Perplexity handled here? | Discovery and second-opinion notes are not citable authority unless converted into direct official, standards-body, public-domain, or scholarly anchors. | Claim ledger records the direct URL, checked date, source lane, refresh trigger, and reviewer. |

**Where this sits.** This module's overview is [@sec:chapter-ageint-security-and-adversarial-considerations]; return to the curriculum atlas [@sec:curriculum_orientation] for the reader paths, evidence map, and safety gates that govern this module.
