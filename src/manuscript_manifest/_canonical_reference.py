"""Canonical, chapter-independent method and assurance tables.

These emitters hold the single source of truth for the shared method,
governance, and assurance tables that every module previously restamped. The
new ``Method & Assurance Reference`` front section
(``sec:method-assurance-reference``) renders each table exactly once, and the
per-chapter emitters point readers here with a cross-reference paragraph
instead of repeating the table body.
"""

from __future__ import annotations


def canonical_claim_ledger_rows() -> str:
    """Chapter-independent claim/evidence ledger (was _01_part._claim_evidence_ledger)."""
    return "\n".join(
        [
            "| Claim class | Evidence required | Review gate |",
            "|---|---|---|",
            ("| Source-spine claim | Parsed module title, module section map, and curriculum citation spine | Confirm the generated text does not invent counts, paths, or labels. |"),
            (
                "| Research-backed governance claim | Direct official, standards, "
                "public-domain, or scholarly anchor, exact passage, version/date, and "
                "applicability limits | Confirm the passage supports the stated obligation "
                "or recommendation; a checked URL alone does not establish entailment. |"
            ),
            (
                "| Agentic workflow claim | Tool boundary, authority contract, human "
                "review point, and rollback condition | Confirm the workflow remains "
                "educational, logged, reversible, and evidence-bounded. |"
            ),
            (
                "| Technical or theoretical claim | Direct domain source for the "
                "formal expression, protocol, architecture, or theory, with analogy limits "
                "spelled out | Confirm the prose does not cite governance guidance "
                "as proof of technical performance or autonomous agency. |"
            ),
            (
                "| Empirical or evaluated capability claim | Direct benchmark, field "
                "evaluation, user study, incident evidence, or scholarly empirical "
                "source with context and subgroup caveats | Confirm the claim is "
                "not merely inferred from the AGEINT curriculum architecture. |"
            ),
            (
                "| Source-construction claim | Search surface, query or prompt, "
                "retrieval date, inclusion and exclusion rule, deduplication note, "
                "source tier, and direct URL | Confirm discovery sources are not "
                "treated as final citations unless directly verified. |"
            ),
            (
                "| Safety claim | Explicit prohibition plus safe alternative | Confirm "
                "the module blocks live targeting, exploitation, covert collection, "
                "manipulation, and unsafe cyber-physical action. |"
            ),
            ("| Cross-module claim | Link to the current unit and adjacent curriculum modules | Confirm the handoff names inputs, outputs, uncertainty, and next-review owner. |"),
        ]
    )


def canonical_competency_rubric_rows() -> str:
    """Chapter-independent competency rubric (was _03_part._assessment_and_capstone_pathway)."""
    return "\n".join(
        [
            "| Competency | Evidence of mastery |",
            "|---|---|",
            "| Conceptual command | Defines the distinction and applies it to a new case without confusing reporting, inference, and authorization. |",
            "| Analytic rigor | Traces each material claim to an exact passage and origin, tests a credible alternative, and revises when contradictory evidence arrives. |",
            "| Agentic design | Demonstrates an allowed request, a denied request, a review handoff, and a recovery decision using synthetic records. |",
            "| Governance and rights | Identifies the applicable authority and affected party, explains necessity and proportionality, and assigns retention and contestability owners. |",
            "| Safety posture | Stops at an excluded action or unresolved authority boundary; a polished output cannot compensate for an unsafe action. |",
        ]
    )


def canonical_refresh_trigger_rows() -> str:
    """Chapter-independent refresh triggers (was _02_part._refresh_triggers)."""
    return "\n".join(
        [
            "| Trigger | Required action |",
            "|---|---|",
            "| Source guide reference changes | preserve existing `ageintNNN` identities and append new references only after the locked range |",
            "| Official or standards source updates | inspect the changed passage and version, reassess dependent claims, then update the checked date and metadata |",
            "| AI law, public-sector policy, education guidance, or rights guidance changes | distinguish jurisdiction, legal status, effective date, and local policy before rerunning the rights map |",
            "| API, protocol, data-space, or provenance specification changes | pin the new version and reassess interface, authorization, and provenance assumptions before reuse |",
            "| Safety audit finds operational wording | stop the affected exercise and replace the treatment with tabletop, audit, governance, or synthetic-data framing |",
            "| Instructor debrief finds unreproducible or contradicted evidence | mark affected claims disputed or withdrawn, notify packet recipients, and retain the correction and review decision |",
        ]
    )


def canonical_mastery_rows() -> str:
    """Chapter-independent answer-quality rubric (was knowledge-check 'Answer quality rubric')."""
    return "\n".join(
        [
            "| Level | Evidence in the answer |",
            "|---|---|",
            "| Strong | Another reviewer reproduces the source-to-claim link; the learner handles a withheld contradiction, preserves dissent, and makes a bounded transfer judgment. |",
            "| Adequate | The core claim is supported and safely bounded, but a dependency, alternative, or next-review decision needs revision before reuse. |",
            "| Revise | The answer relies on definitions, citation counts, fluency, unsupported certainty, or an untested checklist instead of inspectable evidence. |",
        ]
    )


def canonical_safety_boundary() -> str:
    """The single canonical default safety-boundary paragraph (non-pattern chapters)."""
    return (
        "Keep all practice accountable, synthetic, defensive, logged, reversible, and "
        "evidence-bounded. Do not convert any module into live targeting, evasion, "
        "exploitation, covert collection, manipulation, or unsafe cyber-physical "
        "action. Where a module inherits a risky source motif, treat it as a "
        "tabletop, audit, provenance, or governance exercise."
    )


def canonical_analysis_workflow() -> str:
    """Render one reusable analytic procedure and a complete synthetic evidence record."""
    return """
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

Stop an exercise for missing authority, private or live-target material,
unapproved external action, or an unsafe physical request. Hold a material
claim when a source cannot be inspected or a contradiction could reverse the
decision; do not replace the missing evidence with an agent consensus.
Abstention is a legitimate analytic output when it specifies the unresolved
question and next discriminating check. An analytic hold is not permission to
delay a real safety escalation: any real incident goes to the responsible
human authority under the institution's existing procedure.
""".strip()
