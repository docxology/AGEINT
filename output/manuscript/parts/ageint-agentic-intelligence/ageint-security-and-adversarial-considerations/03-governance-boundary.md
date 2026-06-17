### AGEINT Security and Adversarial Considerations governance boundary: synthesis, agent-assistance rules, rights, and assurance gates

**Evidence anchor.** [@sec:chapter-ageint-security-and-adversarial-considerations]; [@ageint234].

### AGEINT Security and Adversarial Considerations analytic synthesis: source-backed claims and forbidden leaps

**Triangulation anchors.** In module 34's governance-boundary section, directly verified anchors for the **Agentic AI Governance and Tool Security** lane include [@official_oecd_agentic_ai]; [@official_canada_agentic_ai_guide]; [@official_nist_ai_rmf]; [@official_nist_ai_600_1]. Use them to test source-guide claims, method boundaries, governance constraints, and safety gates without replacing the module's `ageintNNN` provenance.

Research lane: **Agentic AI Governance and Tool Security** for **Agent Framework Security Vulnerabilities; Python REPL sandbox and approval-gate**. [@ageint234]; [@ageint235].

**Curriculum topic spine:** **Agent Framework Security Vulnerabilities**, **Python REPL sandbox and approval-gate**, **Cyber credential-and-movement taxonomy review using fabricated alerts**.
**Verified anchor cluster:** [@official_oecd_agentic_ai]; [@official_canada_agentic_ai_guide]; [@official_nist_ai_rmf]; [@official_nist_ai_600_1]; [@official_ic_ai_ethics_principles]; [@official_ic_ai_ethics_framework]; [@official_odni_icd_505].

**Conceptual depth:** delegated action under explicit authority, identity, permissions, tool boundaries, monitoring, and human escalation.

**Method stack:** AI RMF Govern-Map-Measure-Manage, least-privilege tool design, prompt-injection review, progressive deployment, and rollback drills.

**Composability contract:** agents, tools, credentials, memory, retrieval stores, policies, and logs remain separately inspectable and revocable components.

**Known failure modes:** excessive agency, shadow tools, indirect prompt injection, memory poisoning, confused authority, and unbounded action chains.

**Defensive boundary:** agentic workflows stay synthetic, owned-lab, supervised, logged, rate-limited, and reversible unless a lawful production authority exists. Applied to **Agent Framework Security Vulnerabilities; Python REPL sandbox and approval-gate**.

| Anchor | Why it matters here |
|---|---|
| [@official_oecd_agentic_ai] | Official OECD conceptual foundation for agentic AI. Checked as of 2026-05-21; role: source_quality_anchor. |
| [@official_canada_agentic_ai_guide] | Government of Canada guide for accountable public-sector use of agentic AI, including governance, risk, transparency, testing, monitoring, and human oversight considerations. Checked as of 2026-05-24; role: curriculum_anchor. |
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
SRE circuit-breaker teaching pattern, depicted in [@fig:ageint-sre-circuit-breaker],
adapts reliability vocabulary into an author-defined governance exercise for
agents with three states. In CLOSED the agent operates normally, its autonomy
earned by a clean safety record; when the safety error budget is exhausted --
for this curriculum, when the PolicyCompliance service-level indicator falls
below 99 percent -- the breaker trips to OPEN and a human takes over; after a
recovery period plus validation it moves to HALF_OPEN with limited capability,
returning to CLOSED only if the clean record holds and snapping back to OPEN on
any new violation. Activation triggers include policy-bypass attempts,
LLM-provider errors, tool-timeout cascades, trust-score degradation, and
reasoning loops or deadlocks. Teach this as a defensive governance exercise:
define the PolicyCompliance SLI for a synthetic agent, set its error budget, and
rehearse the OPEN-state human takeover as a tabletop rather than a live
intervention [@scholarly_systems_security_agentic_computing];
[@official_unu_macau_agentic_ai_boundaries].

The PolicyCompliance service-level indicator makes the 99-percent threshold concrete. Over a
review window of $N_{\text{total}}$ governed actions with $N_{\text{violations}}$ policy
violations, define

$$\mathrm{PolicyCompliance}_{\mathrm{SLI}} =
\frac{N_{\text{total}} - N_{\text{violations}}}{N_{\text{total}}} \;\ge\; 0.99,$$

so the breaker's CLOSED state is exactly the region where this indicator clears its target. The
complementary error budget is the count of violations the window can absorb before the indicator
drops below target,

$$\text{ErrorBudget} = (1 - 0.99)\,N_{\text{total}} = 0.01\,N_{\text{total}},
\qquad \text{breaker} \to \text{OPEN when } N_{\text{violations}} > \text{ErrorBudget}.$$

The budget burns down as violations accrue and is restored when a fresh window opens, which is the
quantity the safety-error-budget figure tracks. Have students compute the SLI on a synthetic action
log, set $N_{\text{total}}$ for one window, and identify the exact violation count that trips the
breaker [@scholarly_systems_security_agentic_computing].

#### AGEINT Security and Adversarial Considerations evidence standard and citation floor: source families and discovery limits

Official
guidance supplies governance, safety, and legal constraints for the **Agentic AI Governance and Tool Security**
lane; scholarly or policy-scholarship sources supply explanatory frames; source-guide
citations preserve the inherited AGEINT bibliography. Perplexity-assisted discovery
is allowed during maintenance, but the manuscript citation itself must resolve to a
direct source URL in `references-*.bib`. Local checks start with [@ageint234]; [@ageint235].

### AGEINT Security and Adversarial Considerations agentic boundary: assist, approve, block, and record

**Evidence anchor.** [@sec:chapter-ageint-security-and-adversarial-considerations]; [@ageint234].

AGEINT translation is bounded by the **Agentic AI Governance and Tool Security** lane.
Agents may organize sources, retrieve context, compare alternatives, draft
checklists, summarize evidence, simulate benign scenarios, and audit reasoning.
They do not initiate unauthorized collection, exploitation, covert targeting,
manipulation, or cyber-physical action; examples stay tied to **Agent Framework Security Vulnerabilities; Python REPL sandbox and approval-gate**.

#### AGEINT Security and Adversarial Considerations permitted defensive utility: curriculum uses and safe outputs

**Evidence anchor.** [@sec:chapter-ageint-security-and-adversarial-considerations]; [@ageint234].

The defensive utility is curriculum design, tabletop preparation,
risk assessment, governance review, source evaluation, and resilience planning.
Work products fit the current unit's education, policy review, lab
exercises, and accountable defensive analysis for **Agent Framework Security Vulnerabilities; Python REPL sandbox and approval-gate**.

#### AGEINT Security and Adversarial Considerations excluded operational boundary: blocked actions and stop rules

Keep all practice accountable, synthetic, defensive, logged, reversible, and evidence-bounded while working from [@ageint234]; [@ageint235] and **Agent Framework Security Vulnerabilities; Python REPL sandbox and approval-gate**. Do not convert it into live targeting, evasion, exploitation, covert collection, manipulation, or unsafe cyber-physical action.

### AGEINT Security and Adversarial Considerations governance assurance: authority, rights, evidence, and human review

**Evidence anchor.** [@sec:chapter-ageint-security-and-adversarial-considerations]; [@ageint234].

Governance is practiced as a gate on the **Agentic AI Governance and Tool Security**
lane. Learners use the **Defensive Cyber-Intelligence Lens** to decide who is accountable for the exercise,
which evidence is sufficient, what rights and access issues remain, and when an
agent-assisted artifact must stop for human review while using **Agent Framework Security Vulnerabilities; Python REPL sandbox and approval-gate**.

#### AGEINT Security and Adversarial Considerations governance card: gates, retained evidence, and review owner

| Gate | Coursebook check | Evidence retained |
|---|---|---|
| Authority | The exercise has a lawful, educational, or defensive purpose and named reviewer. | scope card, excluded-action list, and reviewer initials |
| Evidence | Claims in this module remain tied to guide citations or verified anchors starting with [@ageint234]; [@ageint235]. | claim ledger, source descriptors, caveats, and confidence language |
| Rights and access | Privacy, accessibility, learner support, and affected-group impacts are considered before reuse. | rights note, accommodation path, and unresolved-risk owner |
| Agent control | Any agent assistance stays bounded to retrieval, comparison, drafting, simulation, critique, or audit. | tool allowlist, prompt/output record, stop condition, and rollback note |
| Assurance | The artifact is challenged against **Agentic AI Governance and Tool Security** failure modes and the **Defensive Cyber-Intelligence Lens** safety check. | failure-mode note, remediation item, retest result, and refresh trigger |

#### AGEINT Security and Adversarial Considerations evidence package handoff: appendices, records, and reuse

**Evidence anchor.** [@sec:chapter-ageint-security-and-adversarial-considerations]; [@ageint234].

Detailed model/data cards, transparency notices, retention
rows, release gates, risk exceptions, incident drills, procurement checks, and
learner-support workflows live in the generated appendices and source-support docs.
The local **Defensive Cyber-Intelligence Lens** evidence gate stays compact enough to apply during
reading, practice, and revision for **Agent Framework Security Vulnerabilities; Python REPL sandbox and approval-gate**.

#### AGEINT Security and Adversarial Considerations current-source assurance: verified anchors and local artifact fit

The source assurance check ties the current verified anchor set to the local chapter artifact instead of relying on discovery summaries, here covering **Agent Framework Security Vulnerabilities; Python REPL sandbox and approval-gate**. [@ageint234]; [@ageint235].

| Assurance question | Direct source evidence | Chapter artifact |
|---|---|---|
| What does the module inherit from `official_oecd_agentic_ai` for **Agent Framework Security Vulnerabilities; Python REPL sandbox and approval-gate**? | The Agentic AI Landscape and Its Conceptual Foundations; lane `source_quality_spine`; checked 2026-05-21. | defensive CTI packet with indicator context, taxonomy mapping, confidence, handling rule, and control implication; Official OECD conceptual foundation for agentic AI. |
| What does the module inherit from `official_canada_agentic_ai_guide` for **Agent Framework Security Vulnerabilities; Python REPL sandbox and approval-gate**? | Guide on the Use of Agentic Artificial Intelligence; lane `public_sector_agentic_ai`; checked 2026-05-24. | defensive CTI packet with indicator context, taxonomy mapping, confidence, handling rule, and control implication; bounded-autonomy run card, recoverability review, approval threshold, monitoring evidence, and public-sector service assurance |
| What does the module inherit from `official_nist_ai_rmf` for **Agent Framework Security Vulnerabilities; Python REPL sandbox and approval-gate**? | Artificial Intelligence Risk Management Framework (AI RMF 1.0); lane `source_quality_spine`; checked 2026-05-21. | defensive CTI packet with indicator context, taxonomy mapping, confidence, handling rule, and control implication; Official NIST.AI.100-1 risk-management framework. |
| What does the module inherit from `official_nist_ai_600_1` for **Agent Framework Security Vulnerabilities; Python REPL sandbox and approval-gate**? | Artificial Intelligence Risk Management Framework: Generative AI Profile; lane `source_quality_spine`; checked 2026-05-21. | defensive CTI packet with indicator context, taxonomy mapping, confidence, handling rule, and control implication; Official NIST AI 600-1 generative AI profile. |
| How is Perplexity handled here? | Discovery and second-opinion notes are not citable authority unless converted into direct official, standards-body, public-domain, or scholarly anchors. | Claim ledger records the direct URL, checked date, source lane, refresh trigger, and reviewer. |

**Where this sits.** This module's overview is [@sec:chapter-ageint-security-and-adversarial-considerations]; return to the curriculum atlas [@sec:curriculum_orientation] for the reader paths, evidence map, and safety gates that govern this module.
