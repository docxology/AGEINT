# Method & Assurance Reference: claim evidence, safety gates, and refresh duties {#sec:method-assurance-reference}

This reference holds the shared method, governance, and assurance tables that
every module applies. Each module links here instead of restamping the same
tables, so a reader maintains one canonical copy of the capstone thread, claim
ledger, competency rubric, refresh triggers, safety boundary, and mastery
evidence. Module sections name their local source spine and topic, then point
to the canonical table in this section.

## Source-construction and reporting protocol: discovery records and citation boundaries

AGEINT is a curriculum-and-assurance atlas, not a PRISMA systematic review.
Where a module makes a source-construction or literature-search claim, however,
the source record follows PRISMA-S as a reporting discipline: record the
discovery surface, search string or prompt, retrieval date, inclusion and
exclusion rule, deduplication decision, source tier, conflict-handling note,
direct URL, and refresh trigger [@scholarly_rethlefsen_2021_prisma_s]. Discovery
systems and summaries may suggest candidate sources, but final manuscript
citations must resolve to directly checked official, standards, public-domain,
or scholarly records in the AGEINT source atlas.

The review gate separates claim types before citation assignment. Governance
claims require official or standards anchors; technical and theoretical claims
require direct domain sources; empirical capability claims require evaluation or
study evidence with context and subgroup caveats. If a source only supports an
analogy, lesson design, or governance rationale, the generated prose must not
promote it into a benchmark, deployment claim, or proof of autonomous
performance.

## Claim calibration and statistical limits: artifact telemetry versus empirical evidence

AGEINT treats citation counts, generated file counts, figure counts, PDF page
counts, URI-link counts, and validator outcomes as **artifact telemetry**. They
show what the local build produced and what the verifier checked; they are not
learning-effect estimates, operational-performance measures, safety guarantees,
or statistical evidence that the curriculum improves real-world analytic
decisions. Stronger empirical or evaluated-capability language requires a
direct benchmark, study, field evaluation, incident dataset, or scholarly
empirical source with the method, denominator, subgroup/context caveat, and
refresh trigger visible.

The claim-calibration audit enforces that separation after manuscript
generation. It scans high-risk empirical, statistical, governance, safety,
visualization, artifact-readiness, and formalism language; records the citation
keys and source-support strength visible in the same row; allows explicit
boundary language such as "not a benchmark" or "correct the misconception";
and fails unsupported proof-language, p-values, measured-performance claims, or
formalisms without citations and limitations. The companion visual
[@fig:ageint-claim-calibration-and-visual-semantics] makes the control surface
readable, while `output/reports/claim_calibration.json` and `.md` make the
same disposition auditable by script.

This is a heuristic screen of row-level wording, citation presence, and source
metadata—not a semantic claim verifier. It does not establish that a cited
passage entails a claim, that sources are independent, that contradictory
evidence was included, or that a proposed control works. Boundary wording can
also explain why a row is allowed without validating another claim in that
row. A passing report therefore leaves a human source-to-claim review duty;
the worked procedure below makes that duty inspectable.

Protocol claims are version-sensitive. MCP references use the 2025-06-18
specification for interoperability language and the current MCP security
best-practice page for confused-deputy, token-handling, consent, and
least-privilege examples; those claims must refresh when the protocol version,
authorization profile, transport guidance, or security model changes
[@official_model_context_protocol_specification];
[@official_model_context_protocol_security_best_practices]. Memory-language
claims follow the same separation rule: MCP and official agentic-AI guidance
support external-memory governance, tool boundaries, logging, and retention, not
cognitive-taxonomy claims about episodic, semantic, or procedural memory unless
a domain source is cited for that narrower taxonomy.

## Method figures and course links: assurance visuals and navigation

The orientation uses [@fig:ageint-safety-boundary-loop] to map its evidence flow, safety boundaries, review artifacts, and refresh cues.

Navigation links: [@sec:curriculum_orientation], [@sec:part-foundations-of-intelligence-tradecraft].

## Capstone phase, artifact, and review-gate ladder: required handoff sequence

**Navigation.** Parent section: [@sec:method-assurance-reference].

| Phase | Artifact | Review gate |
|---|---|---|
| Question | accountable learning question and excluded-action list | instructor confirms scope, allowed data, and rights impact |
| Source canon | source-lane map with guide citations, verified anchors, and refresh dates | citation keys resolve and source identity lock remains stable |
| Evidence ledger | claim, evidence, uncertainty, confidence, and reviewer register | every material claim has a source, caveat, and owner |
| Safe lab | synthetic or public dataset packet, tool allowlist, and stop conditions | no live target, private data, external action, or unsafe cyber-physical step |
| Assurance | evaluation rubric, failure-mode drill, rights map, and remediation note | human reviewer signs off before presentation or reuse |
| Debrief | capstone memo with lessons, residual risk, refresh triggers, and handoff owner | all unresolved questions and future approvals are explicit |

## Claim and evidence ledger: claim classes, evidence floors, and review duties

**Navigation.** Parent section: [@sec:method-assurance-reference].

| Claim class | Evidence required | Review gate |
|---|---|---|
| Source-spine claim | Parsed module title, module section map, and curriculum citation spine | Confirm the generated text does not invent counts, paths, or labels. |
| Research-backed governance claim | Direct official, standards, public-domain, or scholarly anchor, exact passage, version/date, and applicability limits | Confirm the passage supports the stated obligation or recommendation; a checked URL alone does not establish entailment. |
| Agentic workflow claim | Tool boundary, authority contract, human review point, and rollback condition | Confirm the workflow remains educational, logged, reversible, and evidence-bounded. |
| Technical or theoretical claim | Direct domain source for the formal expression, protocol, architecture, or theory, with analogy limits spelled out | Confirm the prose does not cite governance guidance as proof of technical performance or autonomous agency. |
| Empirical or evaluated capability claim | Direct benchmark, field evaluation, user study, incident evidence, or scholarly empirical source with context and subgroup caveats | Confirm the claim is not merely inferred from the AGEINT curriculum architecture. |
| Source-construction claim | Search surface, query or prompt, retrieval date, inclusion and exclusion rule, deduplication note, source tier, and direct URL | Confirm discovery sources are not treated as final citations unless directly verified. |
| Safety claim | Explicit prohibition plus safe alternative | Confirm the module blocks live targeting, exploitation, covert collection, manipulation, and unsafe cyber-physical action. |
| Cross-module claim | Link to the current unit and adjacent curriculum modules | Confirm the handoff names inputs, outputs, uncertainty, and next-review owner. |

## Analytic workflow: question, evidence, challenge, and disposition {#sec:analytic-workflow}

Use this procedure with a module's own sources and safe-practice material.
It is a proposed classroom method, not a validated accuracy improvement.
Analytic standards motivate explicit sourcing, assumptions, alternatives, and
uncertainty; critiques of judgment aids make evaluation of those practices
necessary rather than optional [@official_odni_icd_203];
[@scholarly_mandel_tetlock_judgment_correctives].

1. **Frame the decision.** Name the question, audience, time horizon, allowed
   inputs, excluded actions, and human decision owner. State what evidence would
   be sufficient for the classroom disposition; do not silently expand collection.
2. **Preserve observations.** Record a source identifier, exact passage or data
   item, locator, author/publisher, event time, publication time, retrieval time,
   version, and any transformation or translation. Preserve the original and
   distinguish a supplied fixture from a verified real-world observation.
3. **Trace origins before counting support.** Link a repost, quotation,
   syndication, model summary, and translation to their upstream observation.
   Different URLs, publishers, models, or source families do not establish
   independent evidence. Unknown dependence stays unknown.
4. **Assess fitness for this claim.** Separate provenance/authenticity,
   source access and reliability, content credibility, relevance, temporal fit,
   and independence. A genuine official document may describe a policy rather
   than an outcome; a signed image may still be miscaptioned. Record the weakest
   link instead of turning heterogeneous criteria into an unexplained score.
5. **Compare explanations.** Separate observation, inference, and assumption.
   Name credible alternatives, including ordinary error or missing context.
   Ask which observation would be expected under each and which next check
   could change the judgment. Do not count supportive rows as posterior odds.
   Absence is informative only where the observation opportunity, expected
   detection, and reporting coverage make that absence meaningful.
6. **Write uncertainty in separate fields.** Event likelihood concerns the
   proposition; analytic confidence concerns its evidentiary basis. Give the
   basis, contradictions, missing information, and sensitivity to assumptions.
   Do not invent percentages to make a sparse case look calibrated.
7. **Challenge the record.** A reviewer checks the original passages rather
   than just the narrative. Add a duplicate report, remove a key source, and
   introduce a contradictory fixture. Record whether the dependency count,
   judgment, and confidence change for a defensible reason. This tests the
   artifact and review process, not universal resistance to manipulation.
8. **Dispose and hand off.** Choose accept for bounded classroom reuse,
   revise, hold, or reject. Retain unresolved dissent, recipient/handling
   limits, reviewer, next check, and refresh trigger. A human—not a generated
   confidence label—owns the decision. If evidence changes, version the
   correction, mark affected claims, and notify downstream packet owners.

### Reusable claim record: fields a reviewer can actually inspect

**Navigation.** Parent section: [@sec:method-assurance-reference].

Copy the field names below into a worksheet and replace the case values.
Keep evidence and judgment in separate cells; an agent's generated explanation
is not a record of its hidden reasoning or an additional source observation.

| Field | Required entry |
|---|---|
| Claim identity and scope | One falsifiable proposition, its audience and time horizon; claim type and packet version. |
| Evidence and origin | Source IDs, exact excerpts/values and locators, acquisition/version dates, upstream origin, and dependency group. |
| Support relation | Supports, contradicts, contextualizes, or cannot determine; explain the narrow link to this claim. |
| Quality and limits | Access/reliability, authenticity, relevance, temporal fit, missing coverage, and transformations. |
| Alternatives and assumptions | Credible competing account, load-bearing assumption, and discriminating next observation. |
| Likelihood and confidence | Separate entries with a stated basis, or explicitly not assessed; retain substantive dissent. |
| Disposition and correction | Accept/revise/hold/reject, named human owner, allowed audience, refresh trigger, and affected downstream packets. |

### Completed synthetic case: three reports are not three observations

**Navigation.** Parent section: [@sec:method-assurance-reference].

**Question.** May a classroom brief say that a fictional library's service
interruption was caused by a cyberattack? All records below are invented,
offline teaching cards; no real library, account, person, or system is involved.
The task is an analytic disposition, not incident attribution or response.

| Evidence card | Observation and provenance | Relation to the causal claim |
|---|---|---|
| R1: supplied screenshot | An undated status image says “service unavailable”; original capture time is unknown. | Supports only that the image contains that message, not an attack or a current outage. |
| R2: supplied newsletter | Quotes R1 verbatim and cites its screenshot; no separate observation is supplied. | Same dependency group as R1; repetition does not independently corroborate the event. |
| R3: supplied maintenance notice | A fixture identified as the fictional library's notice schedules maintenance during the alleged interruption. | Makes planned maintenance a credible alternative; a schedule alone does not prove what occurred. |

| Record field | Completed entry |
|---|---|
| Claim C1 | “A cyberattack caused the reported interruption”; causal, classroom brief, fixture period only. |
| Observation | R1 contains an unavailable message; R2 repeats it; R3 schedules maintenance. |
| Inference | The packet cannot distinguish an attack, ordinary failure, planned maintenance, or a stale screenshot. |
| Assumption | R1 depicts the same service and period as R3; this remains unverified. |
| Independence | R1 and R2 share one origin; R3 has a separate supplied origin but a different claim scope. |
| Event likelihood | Not quantified: neither a defensible base rate nor discriminating incident evidence is supplied. |
| Analytic confidence | Low for any causal attribution; high for the directly inspectable R1-to-R2 copying relation within this fixture. |
| Dissent and next check | Preserve an alternative causal assessment if offered; request an instructor-provided time-bounded incident record, not access to a live system. |
| Disposition | Hold C1. A human instructor may accept only the narrower statement that the supplied records leave cause unresolved. |
| Refresh and handoff | Reopen when a dated independent incident card arrives; retain packet version, reviewer, and the list of classroom briefs that used C1. |

**Expected negative controls.** A further copy of R1 adds no independent
observation. Removing R3 removes a supported alternative but does not make an
attack established. A new card showing that R1 predates the alleged event
weakens even the same-period outage inference. If a reviewer still accepts C1
because “three sources agree,” revise the source-origin and support-relation
fields before scoring prose quality.

### Bounded agent collaboration: parallel work without manufactured consensus

**Navigation.** Parent section: [@sec:method-assurance-reference].

Use a single analyst or agent when the question is small or the next step
depends on the previous result. For independent work, assign source-disjoint
or method-distinct tasks under one common question, time horizon, allowed-input
set, and output schema. Each worker returns evidence IDs and exact locators,
origin/dependency groups, its narrow claim, contradictions, uncertainty, and
missing inputs—not merely a confident summary.

One human integration owner deduplicates upstream observations, reconciles
scope and time differences, and records disagreements before drafting the
joint conclusion. Do not multiply evidentiary weight by the number of agreeing
agents: shared training, prompts, retrieval, or memory may create common-mode
errors. A separate reviewer must inspect the load-bearing originals and an
intentionally contradictory fixture. Role separation is a proposed control,
not evidence that the reviewers are independent or that multi-agent work is
more accurate. Stop workers from expanding authority, writing unreviewed
shared memory, or converting retrieved source instructions into tool authority;
hold the handoff when a material source cannot be checked.

### Decision boundaries: stop, abstain, and correct

**Navigation.** Parent section: [@sec:method-assurance-reference].

Stop an exercise for missing authority, private or live-target material,
unapproved external action, or an unsafe physical request. Hold a material
claim when a source cannot be inspected or a contradiction could reverse the
decision; do not replace the missing evidence with an agent consensus.
Abstention is a legitimate analytic output when it specifies the unresolved
question and next discriminating check. An analytic hold is not permission to
delay a real safety escalation: any real incident goes to the responsible
human authority under the institution's existing procedure.

## Competency and mastery rubric: scoring dimensions and visible proof

**Navigation.** Parent section: [@sec:method-assurance-reference].

| Competency | Evidence of mastery |
|---|---|
| Conceptual command | Defines the distinction and applies it to a new case without confusing reporting, inference, and authorization. |
| Analytic rigor | Traces each material claim to an exact passage and origin, tests a credible alternative, and revises when contradictory evidence arrives. |
| Agentic design | Demonstrates an allowed request, a denied request, a review handoff, and a recovery decision using synthetic records. |
| Governance and rights | Identifies the applicable authority and affected party, explains necessity and proportionality, and assigns retention and contestability owners. |
| Safety posture | Stops at an excluded action or unresolved authority boundary; a polished output cannot compensate for an unsafe action. |

## Refresh triggers and required actions: source, safety, and tool-change duties

**Navigation.** Parent section: [@sec:method-assurance-reference].

| Trigger | Required action |
|---|---|
| Source guide reference changes | preserve existing `ageintNNN` identities and append new references only after the locked range |
| Official or standards source updates | inspect the changed passage and version, reassess dependent claims, then update the checked date and metadata |
| AI law, public-sector policy, education guidance, or rights guidance changes | distinguish jurisdiction, legal status, effective date, and local policy before rerunning the rights map |
| API, protocol, data-space, or provenance specification changes | pin the new version and reassess interface, authorization, and provenance assumptions before reuse |
| Safety audit finds operational wording | stop the affected exercise and replace the treatment with tabletop, audit, governance, or synthetic-data framing |
| Instructor debrief finds unreproducible or contradicted evidence | mark affected claims disputed or withdrawn, notify packet recipients, and retain the correction and review decision |

## Safety boundary: accountable, synthetic, defensive, and evidence-bounded practice

**Navigation.** Parent section: [@sec:method-assurance-reference].

Keep all practice accountable, synthetic, defensive, logged, reversible, and evidence-bounded. Do not convert any module into live targeting, evasion, exploitation, covert collection, manipulation, or unsafe cyber-physical action. Where a module inherits a risky source motif, treat it as a tabletop, audit, provenance, or governance exercise.

## Mastery evidence standard: retained artifacts, reviewer challenge, and transfer

**Navigation.** Parent section: [@sec:method-assurance-reference].

| Level | Evidence in the answer |
|---|---|
| Strong | Another reviewer reproduces the source-to-claim link; the learner handles a withheld contradiction, preserves dissent, and makes a bounded transfer judgment. |
| Adequate | The core claim is supported and safely bounded, but a dependency, alternative, or next-review decision needs revision before reuse. |
| Revise | The answer relies on definitions, citation counts, fluency, unsupported certainty, or an untested checklist instead of inspectable evidence. |
