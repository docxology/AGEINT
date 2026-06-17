# Instructor Capstone, Rubric, and Red-Team Review Pack {#sec:appendix-instructor-capstone-rubric-and-red-team-review-pack}

The current appendix is an evidence workbook for reusable classroom methods. It is educational and evidence-bounded: examples remain synthetic, defensive, lawful, and bounded to owned labs, public sources, or tabletop exercises. Source-item focus: Capstone authorization card: learning question, allowed inputs, excluded actions, human oversight, and stop conditions; Instructor rubric for source quality, analytic rigor, agent control, rights mapping, reproducibility, and safe substitution.

## Instructor Capstone, Rubric, and Red-Team Review Pack workbook scope: purpose, safety envelope, and reuse decision

**Section anchor.** [@sec:appendix-instructor-capstone-rubric-and-red-team-review-pack].

### Instructor Capstone, Rubric, and Red-Team Review Pack operating purpose
**Section anchor.** [@sec:appendix-instructor-capstone-rubric-and-red-team-review-pack].

The current appendix supports a reusable methods workbook. Each source item is treated as a reviewable classroom artifact rather than an operational instruction; examples begin with Capstone authorization card: learning question, allowed inputs, excluded actions, human oversight, and stop conditions; Instructor rubric for source quality, analytic rigor, agent control, rights mapping, reproducibility, and safe substitution.

### Instructor Capstone, Rubric, and Red-Team Review Pack allowed-input boundary
**Section anchor.** [@sec:appendix-instructor-capstone-rubric-and-red-team-review-pack].

Allowed inputs for the current appendix are public official or scholarly sources, standards text, instructor-provided excerpts, synthetic datasets, owned-lab logs, toy examples, and generated rubrics that expose their provenance for Capstone authorization card: learning question, allowed inputs, excluded actions, human oversight, and stop conditions; Instructor rubric for source quality, analytic rigor, agent control, rights mapping, reproducibility, and safe substitution.

### Instructor Capstone, Rubric, and Red-Team Review Pack excluded-action boundary
**Section anchor.** [@sec:appendix-instructor-capstone-rubric-and-red-team-review-pack].

Excluded actions for the current appendix are unauthorized collection, private-data processing, credential use, contact with real targets, live system interaction, exploit execution, deception, unsafe cyber-physical action, or external deployment while handling Capstone authorization card: learning question, allowed inputs, excluded actions, human oversight, and stop conditions; Instructor rubric for source quality, analytic rigor, agent control, rights mapping, reproducibility, and safe substitution.

### Instructor Capstone, Rubric, and Red-Team Review Pack expected artifact package
**Section anchor.** [@sec:appendix-instructor-capstone-rubric-and-red-team-review-pack].

Expected appendix artifacts are a purpose statement, allowed-inputs card, excluded-actions card, source-lane map, provenance record, claim ledger, safe-substitution note, output schema, review rubric, and capstone handoff memo for Capstone authorization card: learning question, allowed inputs, excluded actions, human oversight, and stop conditions; Instructor rubric for source quality, analytic rigor, agent control, rights mapping, reproducibility, and safe substitution.

### Instructor Capstone, Rubric, and Red-Team Review Pack safe artifact schema
**Section anchor.** [@sec:appendix-instructor-capstone-rubric-and-red-team-review-pack].

| Field | Required evidence | Reject condition |
|---|---|---|
| Purpose | lawful educational, governance, research, or defensive purpose | vague operational objective or missing authority |
| Inputs | public, official, scholarly, synthetic, owned-lab, or instructor-provided material | private data, live target data, credentialed access, or unclear provenance |
| Transform | summary, comparison, rubric scoring, tabletop simulation, or audit review | collection expansion, external action, or unsafe system interaction |
| Output | memo, matrix, checklist, ledger, rubric, or debrief packet | deployable procedure, target package, or automated action plan |
| Reviewer | human reviewer, approval gate, revision note, and refresh owner | anonymous ownership or no escalation path |

### Instructor Capstone, Rubric, and Red-Team Review Pack input/output contract
**Section anchor.** [@sec:appendix-instructor-capstone-rubric-and-red-team-review-pack].

| Contract term | Input rule | Output rule |
|---|---|---|
| Source identity | retain `ageintNNN`, title, URL, and checked status | cite with Pandoc keys and avoid pasted raw URLs in prose |
| Accessibility | include plain-language labels, table headers, and figure alternatives | reject inaccessible figures, unlabeled tables, or single-modality evidence |
| Rights | identify affected groups, safeguards, and residual risk | preserve privacy, equality, access, contestability, and redress notes |
| Tooling | use allowlisted tools, visible prompts, logs, and stop conditions | keep outputs evidence-bounded, reversible, and human-reviewed |
| Refresh | record source, policy, standard, incident, or assessment trigger | assign an owner and date for revalidation |

### Instructor Capstone, Rubric, and Red-Team Review Pack failure cases and required responses
**Section anchor.** [@sec:appendix-instructor-capstone-rubric-and-red-team-review-pack].

| Failure case | Signal | Required response |
|---|---|---|
| Source laundering | claim cites an agent summary instead of a verified source | rebuild the claim ledger from direct sources |
| Boundary drift | exercise starts asking for live targets, private data, or external action | stop, substitute synthetic inputs, and document the block |
| Accessibility gap | learner cannot inspect, navigate, or complete the artifact | remediate and retest before reuse |
| Rights gap | affected group, safeguard, or redress path is missing | run HRIA/DPIA worksheet and escalate unresolved risk |
| Vendor opacity | tool owner, data use, logs, or exit path is unknown | replace tool or pause until procurement evidence exists |

### Instructor Capstone, Rubric, and Red-Team Review Pack evidence package schemas

**Section anchor.** [@sec:appendix-instructor-capstone-rubric-and-red-team-review-pack].

Model and dataset card:

| Field | Model card evidence | Dataset card evidence | Review gate |
|---|---|---|---|
| Intended use | accountable task, excluded uses, affected users, human reviewer, and accountable owner | Data Cards purpose statement, recommended use, prohibited reuse, stewardship owner, and affected stakeholder groups | claim is rejected if intended use, excluded use, affected users, or owner is missing |
| Provenance and collection | model family, version, supplier or lab, training cutoff, deployment context, and configuration hash | upstream source, collection process, annotation method, consent or authority basis, sensitivity class, and license | artifact is held if provenance, license, authority, or collection process is opaque |
| Composition and limits | capability boundary, known failure modes, tool permissions, context window limits, and unsupported conditions | population, sampling frame, coverage gaps, subgroup visibility, missingness, transformations, and known caveats | artifact is revised if population, coverage, or source limits are invisible |
| Evaluation and caveats | benchmark suite, task-specific tests, subgroup or context results, red-team findings, uncertainty notes, and failure examples | quality tests, label agreement, bias review, measurement limits, transformation log, and Data Cards answer-evaluation notes | empirical or performance claims are rejected unless test context, subgroup caveats, and uncertainty are visible |
| Lifecycle controls | release gate, rollback path, monitoring signal, incident threshold, refresh trigger, and model-card update owner | retention rule, access boundary, update cadence, deletion path, stewardship handoff, and dataset-card revision trigger | reuse is blocked without owner, retention, monitoring, rollback, and refresh evidence |

Transparency notice:

| Step | Artifact | Review gate |
|---|---|---|
| Public purpose | plain-language purpose, authority, affected service, and decision role | reader can tell why the system exists and where human judgment remains |
| Tool and data summary | model, data, supplier, provenance, validation, and accessibility summary | sensitive details are de-sensitized without hiding accountability fields |
| Impact and review | benefits, risks, safeguards, human review, appeal, and contact point | affected groups can identify recourse and oversight owners |
| Publication decision | publish, partially publish, delay, or hold decision with exemption rationale | non-public fields have a documented legal, security, privacy, or IP basis |

Records retention and audit trail:

| Record | Retained fields | Audit question |
|---|---|---|
| Source and prompt register | source identity, prompt version, tool allowlist, reviewer, timestamp, and caveat | Can a later reviewer reconstruct the evidentiary path without private or live data? |
| Decision and exception log | risk owner, accepted exception, compensating control, expiry date, and approval | Is every deviation time-bound, justified, and reviewable? |
| Artifact retention note | output type, sensitivity, access boundary, deletion rule, and refresh trigger | Does the retention choice match the educational purpose and rights impact? |
| Incident and remediation record | incident signal, containment action, root cause, owner, retest result, and closure date | Can the same failure be detected and prevented in the next reuse cycle? |

Release and change-control gate:

| Gate | Release evidence | Block condition |
|---|---|---|
| Scope freeze | accountable use case, excluded actions, tool profile, and data boundary | scope expands to external action, live data, or an unreviewed capability |
| Security and rights review | privacy, accessibility, security, bias, and human-review checks | rights impact, vulnerability, or accessibility issue has no owner |
| Version and rollback | model or prompt version, changelog, test fixture, and rollback path | change cannot be reproduced, compared, or reverted |
| Post-release monitoring | monitoring signal, incident threshold, refresh trigger, and owner | deployment or reuse occurs without logging and retest commitments |

Risk exception memo:

| Field | Minimum content | Approval rule |
|---|---|---|
| Exception requested | what requirement cannot be met, why, affected groups, and duration | exception must be specific, time-bound, and tied to a compensating control |
| Risk basis | likelihood, impact, evidence, uncertainty, alternatives, and rejected options | unsupported confidence or missing alternatives returns the memo for revision |
| Compensating control | human review, monitoring, access limit, disclosure, remediation, and owner | control must reduce risk without creating an operational workaround |
| Expiry and retest | expiry date, retest condition, review cadence, and closure criteria | open-ended exceptions are rejected |

Learner support and accommodation plan:

| Need | Support | Evidence |
|---|---|---|
| Access and modality | captions, alt text, keyboard path, plain-language summary, and structured tables | accessibility checklist, defect log, and retest result |
| Cognitive load | worked examples, staged release, glossary, checklist, and optional practice fixture | UDL design note and learner feedback record |
| Assessment fairness | allowed-tool statement, AI-use declaration, alternative submission mode, and transparent rubric | assessment-integrity note and accommodation record |
| Feedback and remediation | revision path, office-hour prompt, example correction, and due-date flexibility policy | feedback log and instructor disposition |

Instructor question bank:

| Question type | Prompt | Evidence |
|---|---|---|
| Source challenge | Which claim would fail if the strongest source were removed or downgraded? | claim ledger revision and source-lane note |
| Boundary challenge | Where could this exercise drift from analysis into action, and what safe substitute prevents it? | safe-substitution decision and excluded-action card |
| Rights challenge | Which affected group, accessibility need, privacy interest, or redress path is under-specified? | HRIA/DPIA update and accommodation note |
| Assurance challenge | What failure would the current evaluation miss, and what retest would reveal it? | adversarial assurance retest and remediation owner |

Remediation backlog:

| Backlog item | Trigger | Closure evidence |
|---|---|---|
| Unverified claim | claim lacks a guide citation or directly verified anchor | verified source, removed claim, or explicit source-guide context note |
| Unsafe phrasing | wording implies live targeting, external action, exploitation, manipulation, or unsafe control | safe substitute, blocked context, and reviewer sign-off |
| Accessibility defect | artifact cannot be inspected through an expected assistive or alternative workflow | defect fix, alternative means, and retest result |
| Assurance gap | evaluation, release, exception, incident, or vendor evidence is incomplete | owner, due date, retest, and accepted disposition |

### Instructor Capstone, Rubric, and Red-Team Review Pack rubric scoring bands
**Section anchor.** [@sec:appendix-instructor-capstone-rubric-and-red-team-review-pack].

| Band | Evidence standard | Disposition |
|---|---|---|
| 4 - ready | source identity, accessibility, rights, safety, and reviewer evidence are complete | may be reused after normal refresh review |
| 3 - revise | one evidence field is incomplete but risk is bounded and remediable | revise before reuse |
| 2 - hold | multiple evidence fields are incomplete or ownership is unclear | hold for instructor and assurance review |
| 1 - reject | unsafe action, private data, inaccessible artifact, or unverified claim appears | reject and rebuild from safe inputs |

### Instructor Capstone, Rubric, and Red-Team Review Pack refresh evidence
**Section anchor.** [@sec:appendix-instructor-capstone-rubric-and-red-team-review-pack].

| Evidence item | Refresh trigger | Retained support |
|---|---|---|
| Source lane | official source, standard, or legal text changes | checked-as-of date and source note |
| Safety treatment | operational wording or unsafe motif appears | safe-substitution decision and blocked context |
| Accessibility | WCAG, UDL, or institutional accessibility duty changes | defect log, retest result, and owner |
| Rights | privacy, human-rights, public transparency, or education guidance changes | HRIA/DPIA revision note |
| Vendor/tool | contract, data-use, incident, or model capability changes | procurement packet and incident review |

### Instructor Capstone, Rubric, and Red-Team Review Pack validation rubric
**Section anchor.** [@sec:appendix-instructor-capstone-rubric-and-red-team-review-pack].

| Criterion | Passing evidence |
|---|---|
| Source identity | existing `ageintNNN` keys remain stable or new references are append-only |
| Verification | official, standards, public-domain, or scholarly URL is checked directly |
| Safety | method is converted into tabletop, audit, governance, or synthetic-data treatment |
| Reproducibility | another reviewer can rebuild the artifact from retained inputs |
| Rights review | privacy, IP, human-rights, workforce, and education impacts are considered where relevant |

### Instructor Capstone, Rubric, and Red-Team Review Pack debrief protocol and reuse decision
**Section anchor.** [@sec:appendix-instructor-capstone-rubric-and-red-team-review-pack].

Debrief by naming what the artifact can support, what it does not establish, what source changed, what risk was avoided by safe substitution, what human approval is still required, and when the appendix should be refreshed for Capstone authorization card: learning question, allowed inputs, excluded actions, human oversight, and stop conditions; Instructor rubric for source quality, analytic rigor, agent control, rights mapping, reproducibility, and safe substitution.

## Instructor capstone workflow

**Section anchor.** [@sec:appendix-instructor-capstone-rubric-and-red-team-review-pack].

The instructor capstone, rubric, and red-team review pack binds each student artifact to source verification, safe substitution, rights review, assurance, and debrief evidence.

| Phase | Artifact | Review gate |
|---|---|---|
| Question | accountable learning question and excluded-action list | instructor confirms scope, allowed data, and rights impact |
| Source canon | source-lane map with guide citations, verified anchors, and refresh dates | citation keys resolve and source identity lock remains stable |
| Evidence ledger | claim, evidence, uncertainty, confidence, and reviewer register | every material claim has a source, caveat, and owner |
| Safe lab | synthetic or public dataset packet, tool allowlist, and stop conditions | no live target, private data, external action, or unsafe cyber-physical step |
| Assurance | evaluation rubric, failure-mode drill, rights map, and remediation note | human reviewer signs off before presentation or reuse |
| Debrief | capstone memo with lessons, residual risk, refresh triggers, and handoff owner | all unresolved questions and future approvals are explicit |

## Safe artifact rows

**Section anchor.** [@sec:appendix-instructor-capstone-rubric-and-red-team-review-pack].

| Source motif | Unsafe source motif | Safe curriculum substitute | Blocked context |
|---|---|---|---|
| AGEINT patterns | raw source motifs can imply autonomous tasking, monitoring, response, or deception | identity-preserving pattern registry plus tabletop, audit, provenance, and governance exercises | deployment, live target tasking, or external action |
| OSINT tools | broad scraping, exposed-service lookup, credentialed search, or identity exposure | tool-governance audit over instructor-provided records, toy inputs, and source-quality cards | live collection expansion or private-data discovery |
| GEOINT | facility assessment, force assessment, geolocation targeting, or pattern-of-life inference | provided imagery metadata quality audit with synthetic change examples and uncertainty notes | live facility assessment or tracking |
| SOC and CTI | autonomous response, exploitability claims, indicator publishing, or production-system action | fabricated-alert tabletop triage with ATT&CK mapping, severity rationale, and debrief evidence | production containment, exploitation, scanning, or blocking |
| HUMINT and CI | persona construction, contact handling, elicitation, deception, or source exposure | synthetic identity-and-provenance ethics audit with role-play records and review rubrics | impersonation, covert contact, or operational-security support |
| Cognitive influence | covert persuasion, microtargeting, audience manipulation, or intervention delivery | opt-in media-literacy lesson plan using synthetic materials and transparent prebunking labels | campaign design or audience-targeted persuasion |
| ICS and OT | facility monitoring, control action, safety-system interference, or cyber-physical response | owned-lab or synthetic process-safety tabletop with logs, rollback, and human approval gates | real plant operations, live devices, or unsafe control changes |

## Assessment lifecycle evidence

**Section anchor.** [@sec:appendix-instructor-capstone-rubric-and-red-team-review-pack].

| Control | Student evidence | Instructor check |
|---|---|---|
| Accountable AI use | tool-use declaration and prompt/output appendix | AI assistance is allowed, visible, bounded, and aligned with the assignment |
| Independent reasoning | assumptions, alternatives, uncertainty, and confidence statement | student judgment is separable from agent-generated drafting |
| Citation integrity | source spine, verified anchors, and claim ledger | claims are not source-laundered through agent prose |
| Synthetic lab boundary | allowed-inputs card, excluded actions, and stop conditions | activity remains public, benign, owned-lab, synthetic, defensive, and reversible |
| Feedback and revision | rubric self-score, reviewer notes, and remediation log | revision evidence addresses the actual deficiency before reuse |

## Adversarial review evidence

**Section anchor.** [@sec:appendix-instructor-capstone-rubric-and-red-team-review-pack].

| Stage | Challenge question | Artifact |
|---|---|---|
| Misuse case | How could the module be misread as operational, unfair, inaccessible, or overconfident? | misuse-case card and safe-substitution decision |
| Control challenge | Which authority, data, tool, rights, or review control would fail first? | control challenge matrix |
| Evidence attack | Can a claim survive source verification, provenance review, and counter-evidence? | challenged claim ledger |
| Incident rehearsal | What happens if an agent drifts, leaks context, fabricates support, or requests unsafe action? | synthetic incident drill and recovery note |
| Remediation | Which wording, workflow, source, figure, or assessment gate must change before reuse? | owner, due date, retest result, and refresh trigger |

### Instructor Capstone, Rubric, and Red-Team Review Pack visual navigation and evidence figures: purpose, source flow, and limits

The appendix uses [@fig:appendix-capstone-redteam-review], [@fig:ageint-capstone-workflow], [@fig:ageint-safe-substitution-matrix], [@fig:ageint-instructor-assessment-lifecycle], [@fig:ageint-assessment-integrity-matrix], [@fig:ageint-release-change-control], [@fig:ageint-learner-support-plan], [@fig:ageint-instructor-question-bank], [@fig:ageint-remediation-backlog], and [@fig:ageint-safety-boundary-loop] to map its evidence flow, safety boundaries, review artifacts, and refresh cues.

Navigation links: [@sec:curriculum_orientation], [@sec:appendix-source-verification-and-claim-ledger-workbook], [@sec:bibliography_atlas].

![The capstone journey shows the reviewer experience from packet submission through rubric scoring, safety/source/rights challenge, remediation, and final instructor handoff. In the instructor capstone rubric and red team review pack appendix, it lets readers compare learner submits packet, instructor scores mastery rubric, red team checks safety, sourcing, and rights, and weak evidence enters remediation backlog so the visual functions as a traceable course aid rather than an unscoped assertion.](../../figures/mermaid/appendix-capstone-redteam-review.png){#fig:appendix-capstone-redteam-review}

![The capstone workflow moves from an accountable question to debrief and refresh ownership. Its reader value is to make capstone workflow steps, decision gates, owner handoffs, refresh triggers, and closure evidence visible at a glance, with the instructor capstone rubric and red team review pack appendix as the source section and defensive review as the boundary.](../../figures/python/ageint-capstone-workflow.png){#fig:ageint-capstone-workflow}

![The safe substitution matrix converts risky motifs into bounded classroom alternatives. It is anchored to the instructor capstone rubric and red team review pack appendix; use it to inspect safe substitution matrix fields, row and column obligations, source records, reviewer decisions, and closure evidence while preserving the distinction between curriculum structure, evidence boundary, and accountable practice.](../../figures/python/ageint-safe-substitution-matrix.png){#fig:ageint-safe-substitution-matrix}

![The instructor lifecycle connects scope, facilitation, scoring, revision, and debrief evidence. Its reader value is to make instructor assessment lifecycle steps, decision gates, owner handoffs, refresh triggers, and closure evidence visible at a glance, with the instructor capstone rubric and red team review pack appendix as the source section and defensive review as the boundary.](../../figures/python/ageint-instructor-assessment-lifecycle.png){#fig:ageint-instructor-assessment-lifecycle}

![The assessment integrity matrix separates AI-use declarations, reasoning, citations, lab boundaries, and revision evidence. In the instructor capstone rubric and red team review pack appendix, it lets readers compare assessment integrity matrix fields, row and column obligations, source records, reviewer decisions, and closure evidence so the visual functions as a traceable course aid rather than an unscoped assertion.](../../figures/python/ageint-assessment-integrity-matrix.png){#fig:ageint-assessment-integrity-matrix}

![The release change-control gate checks scope, rights, security, versioning, rollback, monitoring, and retest. The captioned view belongs to the instructor capstone rubric and red team review pack appendix and should be read as a map of release change control labels, source records, review gates, refresh cues, and reader-use boundaries, not as a capability score or live-task instruction.](../../figures/python/ageint-release-change-control.png){#fig:ageint-release-change-control}

![The learner-support plan connects access, cognitive load, assessment fairness, and remediation. It is anchored to the instructor capstone rubric and red team review pack appendix; use it to inspect learner support plan labels, source records, review gates, refresh cues, and reader-use boundaries while preserving the distinction between curriculum structure, evidence boundary, and accountable practice.](../../figures/python/ageint-learner-support-plan.png){#fig:ageint-learner-support-plan}

![The instructor question bank prompts source, boundary, rights, and assurance challenges. It is anchored to the instructor capstone rubric and red team review pack appendix; use it to inspect instructor question bank fields, row and column obligations, source records, reviewer decisions, and closure evidence while preserving the distinction between curriculum structure, evidence boundary, and accountable practice.](../../figures/python/ageint-instructor-question-bank.png){#fig:ageint-instructor-question-bank}

![The remediation backlog tracks unverified claims, unsafe phrasing, accessibility defects, and assurance gaps. Its reader value is to make remediation backlog fields, row and column obligations, source records, reviewer decisions, and closure evidence visible at a glance, with the instructor capstone rubric and red team review pack appendix as the source section and defensive review as the boundary.](../../figures/python/ageint-remediation-backlog.png){#fig:ageint-remediation-backlog}

### Instructor Capstone, Rubric, and Red-Team Review Pack runtime item map and source roster: generated rows and citation support

| Safe curriculum treatment | Blocked source motif, audit-only | Allowed fixture | Rejected action | Required artifact | Citation spine |
|---|---|---|---|---|---|
| I.1 Capstone authorization card: learning question, allowed inputs, excluded actions, human oversight, and stop conditions | no blocked motif; source title used verbatim | public sources, synthetic records, owned-lab notes, and instructor handouts | external action, private-data processing, unsafe system interaction, or deployment | claim ledger, safe-lab packet, and reviewer handoff | [@ageint242]; [@ageint243]; [@ageint246] |
| I.2 Instructor rubric for source quality, analytic rigor, agent control, rights mapping, reproducibility, and safe substitution | no blocked motif; source title used verbatim | public sources, synthetic records, owned-lab notes, and instructor handouts | external action, private-data processing, unsafe system interaction, or deployment | claim ledger, safe-lab packet, and reviewer handoff | [@ageint237]; [@ageint242]; [@ageint238] |
| I.3 Red-team review checklist for source laundering, automation bias, boundary drift, overconfident synthesis, and unreproducible handoff | no blocked motif; source title used verbatim | public sources, synthetic records, owned-lab notes, and instructor handouts | external action, private-data processing, unsafe system interaction, or deployment | claim ledger, safe-lab packet, and reviewer handoff | [@ageint235]; [@ageint236]; [@ageint272] |
| I.4 Safe artifact packet: source-lane map, claim ledger, synthetic lab packet, interface contract, assessment lifecycle, and debrief memo | no blocked motif; source title used verbatim | public sources, synthetic records, owned-lab notes, and instructor handouts | external action, private-data processing, unsafe system interaction, or deployment | claim ledger, safe-lab packet, and reviewer handoff | [@ageint258]; [@ageint266]; [@ageint271] |
| I.5 Capstone debrief protocol that names residual uncertainty, rights impact, refresh owner, revision plan, and approvals required before reuse | no blocked motif; source title used verbatim | public sources, synthetic records, owned-lab notes, and instructor handouts | external action, private-data processing, unsafe system interaction, or deployment | claim ledger, safe-lab packet, and reviewer handoff | [@ageint239]; [@ageint240]; [@ageint264] |
