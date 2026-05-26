from __future__ import annotations



SAFE_SUBSTITUTION_PATTERNS: Final[tuple[dict[str, str], ...]] = (
    {
        "motif": "AGEINT patterns",
        "source_risk": "raw source motifs can imply autonomous tasking, monitoring, response, or deception",
        "substitute": "identity-preserving pattern registry plus tabletop, audit, provenance, and governance exercises",
        "blocked_context": "deployment, live target tasking, or external action",
    },
    {
        "motif": "OSINT tools",
        "source_risk": "broad scraping, exposed-service lookup, credentialed search, or identity exposure",
        "substitute": "tool-governance audit over instructor-provided records, toy inputs, and source-quality cards",
        "blocked_context": "live collection expansion or private-data discovery",
    },
    {
        "motif": "GEOINT",
        "source_risk": "facility assessment, force assessment, geolocation targeting, or pattern-of-life inference",
        "substitute": "provided imagery metadata quality audit with synthetic change examples and uncertainty notes",
        "blocked_context": "live facility assessment or tracking",
    },
    {
        "motif": "SOC and CTI",
        "source_risk": "autonomous response, exploitability claims, indicator publishing, or production-system action",
        "substitute": "fabricated-alert tabletop triage with ATT&CK mapping, severity rationale, and debrief evidence",
        "blocked_context": "production containment, exploitation, scanning, or blocking",
    },
    {
        "motif": "HUMINT and CI",
        "source_risk": "persona construction, contact handling, elicitation, deception, or source exposure",
        "substitute": "synthetic identity-and-provenance ethics audit with role-play records and review rubrics",
        "blocked_context": "impersonation, covert contact, or operational-security support",
    },
    {
        "motif": "Cognitive influence",
        "source_risk": "covert persuasion, microtargeting, audience manipulation, or intervention delivery",
        "substitute": "opt-in media-literacy lesson plan using synthetic materials and transparent prebunking labels",
        "blocked_context": "campaign design or audience-targeted persuasion",
    },
    {
        "motif": "ICS and OT",
        "source_risk": "facility monitoring, control action, safety-system interference, or cyber-physical response",
        "substitute": "owned-lab or synthetic process-safety tabletop with logs, rollback, and human approval gates",
        "blocked_context": "real plant operations, live devices, or unsafe control changes",
    },
)

CAPSTONE_SCAFFOLDS: Final[tuple[dict[str, str], ...]] = (
    {
        "phase": "Question",
        "artifact": "authorized learning question and excluded-action list",
        "review_gate": "instructor confirms scope, allowed data, and rights impact",
    },
    {
        "phase": "Source canon",
        "artifact": "source-lane map with guide citations, verified anchors, and refresh dates",
        "review_gate": "citation keys resolve and source identity lock remains stable",
    },
    {
        "phase": "Evidence ledger",
        "artifact": "claim, evidence, uncertainty, confidence, and reviewer register",
        "review_gate": "every material claim has a source, caveat, and owner",
    },
    {
        "phase": "Safe lab",
        "artifact": "synthetic or public dataset packet, tool allowlist, and stop conditions",
        "review_gate": "no live target, private data, external action, or unsafe cyber-physical step",
    },
    {
        "phase": "Assurance",
        "artifact": "evaluation rubric, failure-mode drill, rights map, and remediation note",
        "review_gate": "human reviewer signs off before presentation or reuse",
    },
    {
        "phase": "Debrief",
        "artifact": "capstone memo with lessons, residual risk, refresh triggers, and handoff owner",
        "review_gate": "all unresolved questions and future approvals are explicit",
    },
)

ACCESSIBILITY_REVIEW_STEPS: Final[tuple[dict[str, str], ...]] = (
    {
        "step": "Access baseline",
        "artifact": "WCAG/UDL needs note",
        "review_question": "Can every learner perceive, operate, understand, and complete the artifact without a hidden access barrier?",
    },
    {
        "step": "Learner variability",
        "artifact": "multiple-means design note",
        "review_question": "Are engagement, representation, and action or expression options available before remediation is requested?",
    },
    {
        "step": "Assistive technology",
        "artifact": "screen-reader, keyboard, contrast, caption, and plain-language check",
        "review_question": "Can the artifact be reviewed with common assistive workflows and documented alternatives?",
    },
    {
        "step": "Public-service duty",
        "artifact": "Title II or institutional-accessibility obligation note",
        "review_question": "If a public or institutional audience uses this artifact, are contractor and service-access duties visible?",
    },
    {
        "step": "Remediation evidence",
        "artifact": "defect log, owner, due date, and retest result",
        "review_question": "Are accessibility defects tracked to closure before the artifact is reused?",
    },
)

PROCUREMENT_OVERSIGHT_STEPS: Final[tuple[dict[str, str], ...]] = (
    {
        "step": "Need and authority",
        "artifact": "procurement rationale and legal authority card",
        "review_question": "Is the vendor capability tied to a valid learning, governance, or defensive need?",
    },
    {
        "step": "Market and vendor transparency",
        "artifact": "vendor disclosure, subcontractor, data-use, and conflict-of-interest register",
        "review_question": "Can reviewers see who provides the tool, what data it touches, and which dependencies matter?",
    },
    {
        "step": "Evaluation criteria",
        "artifact": "weighted criteria for accessibility, privacy, security, provenance, and reversibility",
        "review_question": "Are evaluation criteria explicit before tool selection rather than rationalized afterward?",
    },
    {
        "step": "Contract controls",
        "artifact": "logging, deletion, audit, incident, accessibility, and termination clauses",
        "review_question": "Can the institution pause, audit, remediate, or exit the vendor relationship?",
    },
    {
        "step": "Lifecycle monitoring",
        "artifact": "renewal evidence, performance review, incident record, and refresh trigger",
        "review_question": "Does oversight continue after award and before classroom reuse?",
    },
)

HRIA_DPIA_WORKSHEET: Final[tuple[dict[str, str], ...]] = (
    {
        "dimension": "Purpose and authority",
        "prompt": "What public, educational, or defensive purpose justifies the processing or analysis?",
        "evidence": "scope card, excluded-action list, and decision owner",
    },
    {
        "dimension": "Data subjects and affected groups",
        "prompt": "Who could be affected directly, indirectly, or through downstream reuse?",
        "evidence": "stakeholder map, vulnerability note, and accessibility considerations",
    },
    {
        "dimension": "High-risk processing trigger",
        "prompt": "Does the activity involve sensitive data, profiling, automated evaluation, large-scale processing, or systematic monitoring?",
        "evidence": "DPIA trigger checklist and mitigation owner",
    },
    {
        "dimension": "Rights and safeguards",
        "prompt": "How are privacy, equality, expression, access, contestability, and redress protected?",
        "evidence": "rights-impact note, safeguard register, and escalation path",
    },
    {
        "dimension": "Residual risk and refresh",
        "prompt": "What remains uncertain, who accepts it, and what source or incident would reopen review?",
        "evidence": "residual-risk decision, review date, and source-refresh trigger",
    },
)

DATA_LINEAGE_REGISTRY: Final[tuple[dict[str, str], ...]] = (
    {
        "object": "Source citation",
        "lineage_field": "`ageintNNN`, title, URL, checked date, and source identity status",
        "quality_gate": "citation key resolves and reference identity is locked or append-only",
    },
    {
        "object": "Verified anchor",
        "lineage_field": "lane, tier, verification method, claim scope, stakeholder role, and assurance use",
        "quality_gate": "direct official, standards, public-domain, or scholarly URL was reviewed",
    },
    {
        "object": "Dataset or scenario",
        "lineage_field": "origin, license, sensitivity class, transformations, and retention rule",
        "quality_gate": "public, synthetic, owned-lab, or instructor-provided data only",
    },
    {
        "object": "Agent transcript",
        "lineage_field": "prompt, model context, tool allowlist, budget, reviewer, and blocked actions",
        "quality_gate": "no external action, live target, private data, or unsafe cyber-physical step",
    },
    {
        "object": "Final artifact",
        "lineage_field": "claim ledger, uncertainty note, accessibility status, rights review, and refresh owner",
        "quality_gate": "another reviewer can reproduce and challenge the artifact",
    },
)

ASSESSMENT_INTEGRITY_PROTOCOL: Final[tuple[dict[str, str], ...]] = (
    {
        "control": "Authorized AI use",
        "student_evidence": "tool-use declaration and prompt/output appendix",
        "instructor_check": "AI assistance is allowed, visible, bounded, and aligned with the assignment",
    },
    {
        "control": "Independent reasoning",
        "student_evidence": "assumptions, alternatives, uncertainty, and confidence statement",
        "instructor_check": "student judgment is separable from agent-generated drafting",
    },
    {
        "control": "Citation integrity",
        "student_evidence": "source spine, verified anchors, and claim ledger",
        "instructor_check": "claims are not source-laundered through agent prose",
    },
    {
        "control": "Synthetic lab boundary",
        "student_evidence": "allowed-inputs card, excluded actions, and stop conditions",
        "instructor_check": "activity remains public, benign, owned-lab, synthetic, defensive, and reversible",
    },
    {
        "control": "Feedback and revision",
        "student_evidence": "rubric self-score, reviewer notes, and remediation log",
        "instructor_check": "revision evidence addresses the actual deficiency before reuse",
    },
)

AGENT_INCIDENT_RESPONSE_DRILL: Final[tuple[dict[str, str], ...]] = (
    {
        "phase": "Prepare",
        "drill_action": "define agent scope, tool permissions, logs, escalation roles, and stop conditions",
        "artifact": "incident play card and contact matrix",
    },
    {
        "phase": "Detect",
        "drill_action": "identify anomalous output, policy drift, source-laundering, data exposure, or unsafe tool request",
        "artifact": "synthetic incident ticket and evidence snapshot",
    },
    {
        "phase": "Contain",
        "drill_action": "pause the workflow, revoke tool access, preserve records, and route to human review",
        "artifact": "containment decision and access-change log",
    },
    {
        "phase": "Recover",
        "drill_action": "restore a known-safe prompt, dataset, tool profile, or rubric state",
        "artifact": "rollback note and retest result",
    },
    {
        "phase": "Debrief",
        "drill_action": "record root cause, learner impact, rights impact, vendor implication, and refresh trigger",
        "artifact": "post-incident memo and owner assignment",
    },
)

ROLE_BASED_COMPETENCY_MAP: Final[tuple[dict[str, str], ...]] = (

    {
        "role": "Learner analyst",
        "competency": "separate claim, evidence, uncertainty, confidence, and source quality",
        "evidence": "claim ledger and reflective memo",
    },
    {
        "role": "Instructor",
        "competency": "facilitate safe labs, assess integrity, and preserve accessibility",
        "evidence": "rubric, UDL review, and debrief notes",
    },
    {
        "role": "Source steward",
        "competency": "lock source identities, verify new anchors, and maintain refresh triggers",
        "evidence": "source lane map and source refresh ledger",
    },
    {
        "role": "Assurance reviewer",
        "competency": "test failure modes, adversarial assumptions, tool boundaries, and incident response",
        "evidence": "red-team review, incident drill, and remediation record",
    },
    {
        "role": "Rights and procurement reviewer",
        "competency": "evaluate privacy, accessibility, vendor, public transparency, and human-rights impacts",
        "evidence": "HRIA/DPIA worksheet and procurement oversight packet",
    },
)

ADVERSARIAL_ASSURANCE_CYCLE: Final[tuple[dict[str, str], ...]] = (
    {
        "stage": "Misuse case",
        "question": "How could the module be misread as operational, unfair, inaccessible, or overconfident?",
        "artifact": "misuse-case card and safe-substitution decision",
    },
    {
        "stage": "Control challenge",
        "question": "Which authority, data, tool, rights, or review control would fail first?",
        "artifact": "control challenge matrix",
    },
    {
        "stage": "Evidence attack",
        "question": "Can a claim survive source verification, provenance review, and counter-evidence?",
        "artifact": "challenged claim ledger",
    },
    {
        "stage": "Incident rehearsal",
        "question": "What happens if an agent drifts, leaks context, fabricates support, or requests unsafe action?",
        "artifact": "synthetic incident drill and recovery note",
    },
    {
        "stage": "Remediation",
        "question": "Which wording, workflow, source, figure, or assessment gate must change before reuse?",
        "artifact": "owner, due date, retest result, and refresh trigger",
    },
)

MODEL_DATASET_CARD: Final[tuple[dict[str, str], ...]] = (
    {
        "field": "Intended use",
        "model_card": "authorized task, out-of-scope uses, affected users, and reviewer",
        "dataset_card": "collection purpose, recommended use, prohibited reuse, and stewardship owner",
        "review_gate": "claim is rejected if intended use or excluded use is missing",
    },
    {
        "field": "Composition and scope",
        "model_card": "model version, capability boundary, test context, and known limitations",
        "dataset_card": "data origin, composition, sampling frame, sensitivity class, and license",
        "review_gate": "artifact is held if population, coverage, or source limits are not visible",
    },
    {
        "field": "Evaluation evidence",
        "model_card": "benchmarks, subgroup results, stress tests, and uncertainty notes",
        "dataset_card": "quality tests, missingness, bias review, transformation log, and caveats",
        "review_gate": "artifact is revised if performance or data-quality claims lack evidence",
    },
    {
        "field": "Lifecycle controls",
        "model_card": "release gate, rollback path, monitoring signal, and refresh trigger",
        "dataset_card": "retention rule, access boundary, update cadence, and deletion path",
        "review_gate": "reuse is blocked without owner, retention, monitoring, and refresh evidence",
    },
)

TRANSPARENCY_NOTICE_WORKFLOW: Final[tuple[dict[str, str], ...]] = (
    {
        "step": "Public purpose",
        "artifact": "plain-language purpose, authority, affected service, and decision role",
        "review_gate": "reader can tell why the system exists and where human judgment remains",
    },
    {
        "step": "Tool and data summary",
        "artifact": "model, data, supplier, provenance, validation, and accessibility summary",
        "review_gate": "sensitive details are de-sensitized without hiding accountability fields",
    },
    {
        "step": "Impact and review",
        "artifact": "benefits, risks, safeguards, human review, appeal, and contact point",
        "review_gate": "affected groups can identify recourse and oversight owners",
    },
    {
        "step": "Publication decision",
        "artifact": "publish, partially publish, delay, or hold decision with exemption rationale",
        "review_gate": "non-public fields have a documented legal, security, privacy, or IP basis",
    },
)

RETENTION_AUDIT_TRAIL: Final[tuple[dict[str, str], ...]] = (
    {
        "record": "Source and prompt register",
        "retained_fields": "source identity, prompt version, tool allowlist, reviewer, timestamp, and caveat",
        "audit_question": "Can a later reviewer reconstruct the evidentiary path without private or live data?",
    },
    {
        "record": "Decision and exception log",
        "retained_fields": "risk owner, accepted exception, compensating control, expiry date, and approval",
        "audit_question": "Is every deviation time-bound, justified, and reviewable?",
    },
    {
        "record": "Artifact retention note",
        "retained_fields": "output type, sensitivity, access boundary, deletion rule, and refresh trigger",
        "audit_question": "Does the retention choice match the educational purpose and rights impact?",
    },
    {
        "record": "Incident and remediation record",
        "retained_fields": "incident signal, containment action, root cause, owner, retest result, and closure date",
        "audit_question": "Can the same failure be detected and prevented in the next reuse cycle?",
    },
)

RELEASE_CHANGE_CONTROL_GATE: Final[tuple[dict[str, str], ...]] = (
    {
        "gate": "Scope freeze",
        "release_evidence": "authorized use case, excluded actions, tool profile, and data boundary",
        "block_condition": "scope expands to external action, live data, or an unreviewed capability",
    },
    {
        "gate": "Security and rights review",
        "release_evidence": "privacy, accessibility, security, bias, and human-review checks",
        "block_condition": "rights impact, vulnerability, or accessibility issue has no owner",
    },
    {
        "gate": "Version and rollback",
        "release_evidence": "model or prompt version, changelog, test fixture, and rollback path",
        "block_condition": "change cannot be reproduced, compared, or reverted",
    },
    {
        "gate": "Post-release monitoring",
        "release_evidence": "monitoring signal, incident threshold, refresh trigger, and owner",
        "block_condition": "deployment or reuse occurs without logging and retest commitments",
    },
)

RISK_EXCEPTION_MEMO: Final[tuple[dict[str, str], ...]] = (
    {
        "field": "Exception requested",
        "minimum_content": "what requirement cannot be met, why, affected groups, and duration",
        "approval_rule": "exception must be specific, time-bound, and tied to a compensating control",
    },
    {
        "field": "Risk basis",
        "minimum_content": "likelihood, impact, evidence, uncertainty, alternatives, and rejected options",
        "approval_rule": "unsupported confidence or missing alternatives returns the memo for revision",
    },
    {
        "field": "Compensating control",
        "minimum_content": "human review, monitoring, access limit, disclosure, remediation, and owner",
        "approval_rule": "control must reduce risk without creating an operational workaround",
    },
    {
        "field": "Expiry and retest",
        "minimum_content": "expiry date, retest condition, review cadence, and closure criteria",
        "approval_rule": "open-ended exceptions are rejected",
    },
)

LEARNER_SUPPORT_PLAN: Final[tuple[dict[str, str], ...]] = (
    {
        "need": "Access and modality",
        "support": "captions, alt text, keyboard path, plain-language summary, and structured tables",
        "evidence": "accessibility checklist, defect log, and retest result",
    },
    {
        "need": "Cognitive load",
        "support": "worked examples, staged release, glossary, checklist, and optional practice fixture",
        "evidence": "UDL design note and learner feedback record",
    },
    {
        "need": "Assessment fairness",
        "support": "allowed-tool statement, AI-use declaration, alternative submission mode, and transparent rubric",
        "evidence": "assessment-integrity note and accommodation record",
    },
    {
        "need": "Feedback and remediation",
        "support": "revision path, office-hour prompt, example correction, and due-date flexibility policy",
        "evidence": "feedback log and instructor disposition",
    },
)

INSTRUCTOR_QUESTION_BANK: Final[tuple[dict[str, str], ...]] = (
    {
        "question_type": "Source challenge",
        "prompt": "Which claim would fail if the strongest source were removed or downgraded?",
        "evidence": "claim ledger revision and source-lane note",
    },
    {
        "question_type": "Boundary challenge",
        "prompt": "Where could this exercise drift from analysis into action, and what safe substitute prevents it?",
        "evidence": "safe-substitution decision and excluded-action card",
    },
    {
        "question_type": "Rights challenge",
        "prompt": "Which affected group, accessibility need, privacy interest, or redress path is under-specified?",
        "evidence": "HRIA/DPIA update and accommodation note",
    },
    {
        "question_type": "Assurance challenge",
        "prompt": "What failure would the current evaluation miss, and what retest would reveal it?",
        "evidence": "adversarial assurance retest and remediation owner",
    },
)
