# Cognitive Security and Inoculation Methods {#sec:appendix-cognitive-security-and-inoculation-methods}

The current appendix is an evidence workbook for reusable classroom methods. It is educational and evidence-bounded: examples remain synthetic, defensive, lawful, and bounded to owned labs, public sources, or tabletop exercises. Source-item focus: CAMBREX Taxonomy of Manipulation Techniques (van der Linden); Python Prebunking Agent: Manipulation Detection + Inoculation Content Generation.

## Cognitive Security and Inoculation Methods workbook scope: purpose, safety envelope, and reuse decision

**Section anchor.** [@sec:appendix-cognitive-security-and-inoculation-methods].

### Cognitive Security and Inoculation Methods operating purpose
**Section anchor.** [@sec:appendix-cognitive-security-and-inoculation-methods].

The current appendix supports a reusable methods workbook. Each source item is treated as a reviewable classroom artifact rather than an operational instruction; examples begin with CAMBREX Taxonomy of Manipulation Techniques (van der Linden); Python Prebunking Agent: Manipulation Detection + Inoculation Content Generation.

### Cognitive Security and Inoculation Methods allowed-input boundary
**Section anchor.** [@sec:appendix-cognitive-security-and-inoculation-methods].

Allowed inputs for the current appendix are public official or scholarly sources, standards text, instructor-provided excerpts, synthetic datasets, owned-lab logs, toy examples, and generated rubrics that expose their provenance for CAMBREX Taxonomy of Manipulation Techniques (van der Linden); Python Prebunking Agent: Manipulation Detection + Inoculation Content Generation.

### Cognitive Security and Inoculation Methods excluded-action boundary
**Section anchor.** [@sec:appendix-cognitive-security-and-inoculation-methods].

Excluded actions for the current appendix are unauthorized collection, private-data processing, credential use, contact with real targets, live system interaction, exploit execution, deception, unsafe cyber-physical action, or external deployment while handling CAMBREX Taxonomy of Manipulation Techniques (van der Linden); Python Prebunking Agent: Manipulation Detection + Inoculation Content Generation.

### Cognitive Security and Inoculation Methods expected artifact package
**Section anchor.** [@sec:appendix-cognitive-security-and-inoculation-methods].

Expected appendix artifacts are a purpose statement, allowed-inputs card, excluded-actions card, source-lane map, provenance record, claim ledger, safe-substitution note, output schema, review rubric, and capstone handoff memo for CAMBREX Taxonomy of Manipulation Techniques (van der Linden); Python Prebunking Agent: Manipulation Detection + Inoculation Content Generation.

### Cognitive Security and Inoculation Methods safe artifact schema
**Section anchor.** [@sec:appendix-cognitive-security-and-inoculation-methods].

| Field | Required evidence | Reject condition |
|---|---|---|
| Purpose | lawful educational, governance, research, or defensive purpose | vague operational objective or missing authority |
| Inputs | public, official, scholarly, synthetic, owned-lab, or instructor-provided material | private data, live target data, credentialed access, or unclear provenance |
| Transform | summary, comparison, rubric scoring, tabletop simulation, or audit review | collection expansion, external action, or unsafe system interaction |
| Output | memo, matrix, checklist, ledger, rubric, or debrief packet | deployable procedure, target package, or automated action plan |
| Reviewer | human reviewer, approval gate, revision note, and refresh owner | anonymous ownership or no escalation path |

### Cognitive Security and Inoculation Methods input/output contract
**Section anchor.** [@sec:appendix-cognitive-security-and-inoculation-methods].

| Contract term | Input rule | Output rule |
|---|---|---|
| Source identity | retain `ageintNNN`, title, URL, and checked status | cite with Pandoc keys and avoid pasted raw URLs in prose |
| Accessibility | include plain-language labels, table headers, and figure alternatives | reject inaccessible figures, unlabeled tables, or single-modality evidence |
| Rights | identify affected groups, safeguards, and residual risk | preserve privacy, equality, access, contestability, and redress notes |
| Tooling | use allowlisted tools, visible prompts, logs, and stop conditions | keep outputs evidence-bounded, reversible, and human-reviewed |
| Refresh | record source, policy, standard, incident, or assessment trigger | assign an owner and date for revalidation |

### Cognitive Security and Inoculation Methods failure cases and required responses
**Section anchor.** [@sec:appendix-cognitive-security-and-inoculation-methods].

| Failure case | Signal | Required response |
|---|---|---|
| Source laundering | claim cites an agent summary instead of a verified source | rebuild the claim ledger from direct sources |
| Boundary drift | exercise starts asking for live targets, private data, or external action | stop, substitute synthetic inputs, and document the block |
| Accessibility gap | learner cannot inspect, navigate, or complete the artifact | remediate and retest before reuse |
| Rights gap | affected group, safeguard, or redress path is missing | run HRIA/DPIA worksheet and escalate unresolved risk |
| Vendor opacity | tool owner, data use, logs, or exit path is unknown | replace tool or pause until procurement evidence exists |

### Cognitive Security and Inoculation Methods evidence package schemas

**Section anchor.** [@sec:appendix-cognitive-security-and-inoculation-methods].

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

### Cognitive Security and Inoculation Methods rubric scoring bands
**Section anchor.** [@sec:appendix-cognitive-security-and-inoculation-methods].

| Band | Evidence standard | Disposition |
|---|---|---|
| 4 - ready | source identity, accessibility, rights, safety, and reviewer evidence are complete | may be reused after normal refresh review |
| 3 - revise | one evidence field is incomplete but risk is bounded and remediable | revise before reuse |
| 2 - hold | multiple evidence fields are incomplete or ownership is unclear | hold for instructor and assurance review |
| 1 - reject | unsafe action, private data, inaccessible artifact, or unverified claim appears | reject and rebuild from safe inputs |

### Cognitive Security and Inoculation Methods refresh evidence
**Section anchor.** [@sec:appendix-cognitive-security-and-inoculation-methods].

| Evidence item | Refresh trigger | Retained support |
|---|---|---|
| Source lane | official source, standard, or legal text changes | checked-as-of date and source note |
| Safety treatment | operational wording or unsafe motif appears | safe-substitution decision and blocked context |
| Accessibility | WCAG, UDL, or institutional accessibility duty changes | defect log, retest result, and owner |
| Rights | privacy, human-rights, public transparency, or education guidance changes | HRIA/DPIA revision note |
| Vendor/tool | contract, data-use, incident, or model capability changes | procurement packet and incident review |

### Cognitive Security and Inoculation Methods validation rubric
**Section anchor.** [@sec:appendix-cognitive-security-and-inoculation-methods].

| Criterion | Passing evidence |
|---|---|
| Source identity | existing `ageintNNN` keys remain stable or new references are append-only |
| Verification | official, standards, public-domain, or scholarly URL is checked directly |
| Safety | method is converted into tabletop, audit, governance, or synthetic-data treatment |
| Reproducibility | another reviewer can rebuild the artifact from retained inputs |
| Rights review | privacy, IP, human-rights, workforce, and education impacts are considered where relevant |

### Cognitive Security and Inoculation Methods debrief protocol and reuse decision
**Section anchor.** [@sec:appendix-cognitive-security-and-inoculation-methods].

Debrief by naming what the artifact can support, what it does not establish, what source changed, what risk was avoided by safe substitution, what human approval is still required, and when the appendix should be refreshed for CAMBREX Taxonomy of Manipulation Techniques (van der Linden); Python Prebunking Agent: Manipulation Detection + Inoculation Content Generation.

## Cognitive degradation as a staged cascade

The Cloud Security Alliance Cognitive Degradation Resilience model treats an attack on an agent network not as a single breach but as a six-stage slide that stays below conventional alerting thresholds, illustrated for this appendix in [@fig:ageint-cdr-degradation-cascade]. Stage one is trigger injection, where adversarial inputs win a foothold in agent reasoning; stage two is resource starvation, in which context windows and compute are deliberately consumed to degrade decision quality; stage three is behavioral drift, where outputs deviate from policy without tripping alerts; stage four is memory entrenchment, where corrupted beliefs solidify in agent memory stores; stage five is functional override, where adversary objectives supersede the legitimate task; and stage six is systemic collapse, where coordinated agent behavior serves adversarial ends. The decisive observation is that the intervention window opens early -- between resource starvation and behavioral drift -- because once beliefs entrench in memory, remediation cost rises sharply [@official_csa_cdr_framework].

Each stage is paired in the QSAF-BC control set with a named, testable countermeasure rather than a single catch-all monitor: starvation detection (BC-001) and token-overload limits (BC-002) defend the early stages, an entropy-drift monitor (BC-006) and a memory-integrity check (BC-007) defend the middle, and override resistance (BC-005) defends the late stages. Treat this cascade as a classroom tabletop: map a synthetic incident onto the six stages, identify which control would have fired first, and record the evidence a reviewer would need to confirm the agent recovered [@official_csa_securing_autonomous_ai_agents]; [@scholarly_agentic_ai_security_survey].

## The decoherence-degradation isomorphism

The same dynamic appears one scale up. The CCDCOE reconception of cognitive warfare describes how an adversary degrades a human organization by attacking systemic invariants -- shared trust, identity, and epistemic standards -- driving it through initiation, uncertainty amplification, polarization, hardened competing frameworks, narrative capture, and a final state where the institution functions formally but can no longer coordinate. As [@fig:ageint-cognitive-decoherence-cdr-isomorphism] makes explicit, those six human-organization phases map one-to-one onto the CDR degradation stages in an agent network, phase for phase from initiation to collapse [@scholarly_ccdcoe_cognitive_warfare_reconception]. The pedagogical payoff is that a single defensive vocabulary -- early detection, drift monitoring, integrity of stored belief -- transfers across both the human and the machine layer, which is why this appendix teaches them together rather than as separate disciplines.

### Cognitive Security and Inoculation Methods visual navigation and evidence figures: purpose, source flow, and limits

The appendix uses [@fig:ageint-cdr-degradation-cascade], [@fig:ageint-cognitive-decoherence-cdr-isomorphism], and [@fig:ageint-safety-boundary-loop] to map its evidence flow, safety boundaries, review artifacts, and refresh cues.

Navigation links: [@sec:curriculum_orientation], [@sec:appendix-att-ck-and-kill-chain-mapping-templates], [@sec:appendix-source-verification-and-claim-ledger-workbook].

![The CDR timeline places six degradation stages in chronological order and marks the control window where reviewer intervention can still preserve synthetic, evidence-bounded agent behavior. Its reader value is to make six chronological CDR stages, defensive QSAF-BC controls for starvation, overload, entropy drift, memory integrity, and override resistance, early-detection and decisive-intervention windows, and evidence-bounded classroom review boundary visible at a glance, with the cognitive security and inoculation methods appendix as the source section and defensive review as the boundary.](../../figures/mermaid/ageint-cdr-degradation-cascade.png){#fig:ageint-cdr-degradation-cascade}

![The six phases of CCDCOE cognitive decoherence in human organizations map one-to-one onto the CSA CDR cognitive-degradation stages in AI agent networks, exposing a shared adversarial dynamic. It is anchored to the cognitive security and inoculation methods appendix; use it to inspect Phase 1 — Initiation, Human orgs / CCDCOE adversary targets systemic invariants: trust, identity, epistemic standards, AI agents / CDR Trigger Injection: adversarial inputs establish foothold, and Phase 2 — Early degradation while preserving the distinction between curriculum structure, evidence boundary, and accountable practice.](../../figures/mermaid/ageint-cognitive-decoherence-cdr-isomorphism.png){#fig:ageint-cognitive-decoherence-cdr-isomorphism}

### Cognitive Security and Inoculation Methods runtime item map and source roster: generated rows and citation support

| Safe curriculum treatment | Blocked source motif, audit-only | Allowed fixture | Rejected action | Required artifact | Citation spine |
|---|---|---|---|---|---|
| G.1 CAMBREX Taxonomy of Manipulation Techniques (van der Linden) | no blocked motif; source title used verbatim | public sources, synthetic records, owned-lab notes, and instructor handouts | external action, private-data processing, unsafe system interaction, or deployment | claim ledger, safe-lab packet, and reviewer handoff | - |
| Psychological inoculation and prebunking literacy review | G.2 retained for audit; operational wording transformed | public sources, synthetic records, owned-lab notes, and instructor handouts | external action, private-data processing, unsafe system interaction, or deployment | claim ledger, safe-lab packet, and reviewer handoff | [@ageint151] |
| G.3 NASA-TLX Cognitive Load Measurement Implementation | no blocked motif; source title used verbatim | sample messages, transparent labels, and opt-in classroom discussion cards | covert persuasion, microtargeting, impersonation, or campaign design | narrative-risk map and transparent education note | [@ageint179] |
| G.4 Active Inference Agent: FEP-Based Decision Under Uncertainty (pymdp) | no blocked motif; source title used verbatim | public sources, synthetic records, owned-lab notes, and instructor handouts | external action, private-data processing, unsafe system interaction, or deployment | claim ledger, safe-lab packet, and reviewer handoff | [@ageint106] |
| G.5 Bias Detection Pipeline: Automated ACH with Cognitive Bias Flagging | no blocked motif; source title used verbatim | sample messages, transparent labels, and opt-in classroom discussion cards | covert persuasion, microtargeting, impersonation, or campaign design | narrative-risk map and transparent education note | - |
