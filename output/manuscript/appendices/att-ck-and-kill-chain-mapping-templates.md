# ATT&CK and Kill Chain Mapping Templates {#sec:appendix-att-ck-and-kill-chain-mapping-templates}

The current appendix is an evidence workbook for reusable classroom methods. It is educational and evidence-bounded: examples remain synthetic, defensive, lawful, and bounded to owned labs, public sources, or tabletop exercises. Source-item focus: MITRE ATT&CK Navigator Layer: Enterprise; the module Navigator Layer.

## ATT&CK and Kill Chain Mapping Templates workbook scope: purpose, safety envelope, and reuse decision

**Section anchor.** [@sec:appendix-att-ck-and-kill-chain-mapping-templates].

### ATT&CK and Kill Chain Mapping Templates operating purpose
**Section anchor.** [@sec:appendix-att-ck-and-kill-chain-mapping-templates].

The current appendix supports a reusable methods workbook. Each source item is treated as a reviewable classroom artifact rather than an operational instruction; examples begin with MITRE ATT&CK Navigator Layer: Enterprise; the module Navigator Layer.

### ATT&CK and Kill Chain Mapping Templates allowed-input boundary
**Section anchor.** [@sec:appendix-att-ck-and-kill-chain-mapping-templates].

Allowed inputs for the current appendix are public official or scholarly sources, standards text, instructor-provided excerpts, synthetic datasets, owned-lab logs, toy examples, and generated rubrics that expose their provenance for MITRE ATT&CK Navigator Layer: Enterprise; the module Navigator Layer.

### ATT&CK and Kill Chain Mapping Templates excluded-action boundary
**Section anchor.** [@sec:appendix-att-ck-and-kill-chain-mapping-templates].

Excluded actions for the current appendix are unauthorized collection, private-data processing, credential use, contact with real targets, live system interaction, exploit execution, deception, unsafe cyber-physical action, or external deployment while handling MITRE ATT&CK Navigator Layer: Enterprise; the module Navigator Layer.

### ATT&CK and Kill Chain Mapping Templates expected artifact package
**Section anchor.** [@sec:appendix-att-ck-and-kill-chain-mapping-templates].

Expected appendix artifacts are a purpose statement, allowed-inputs card, excluded-actions card, source-lane map, provenance record, claim ledger, safe-substitution note, output schema, review rubric, and capstone handoff memo for MITRE ATT&CK Navigator Layer: Enterprise; the module Navigator Layer.

### ATT&CK and Kill Chain Mapping Templates safe artifact schema
**Section anchor.** [@sec:appendix-att-ck-and-kill-chain-mapping-templates].

| Field | Required evidence | Reject condition |
|---|---|---|
| Purpose | lawful educational, governance, research, or defensive purpose | vague operational objective or missing authority |
| Inputs | public, official, scholarly, synthetic, owned-lab, or instructor-provided material | private data, live target data, credentialed access, or unclear provenance |
| Transform | summary, comparison, rubric scoring, tabletop simulation, or audit review | collection expansion, external action, or unsafe system interaction |
| Output | memo, matrix, checklist, ledger, rubric, or debrief packet | deployable procedure, target package, or automated action plan |
| Reviewer | human reviewer, approval gate, revision note, and refresh owner | anonymous ownership or no escalation path |

### ATT&CK and Kill Chain Mapping Templates input/output contract
**Section anchor.** [@sec:appendix-att-ck-and-kill-chain-mapping-templates].

| Contract term | Input rule | Output rule |
|---|---|---|
| Source identity | retain `ageintNNN`, title, URL, and checked status | cite with Pandoc keys and avoid pasted raw URLs in prose |
| Accessibility | include plain-language labels, table headers, and figure alternatives | reject inaccessible figures, unlabeled tables, or single-modality evidence |
| Rights | identify affected groups, safeguards, and residual risk | preserve privacy, equality, access, contestability, and redress notes |
| Tooling | use allowlisted tools, visible prompts, logs, and stop conditions | keep outputs evidence-bounded, reversible, and human-reviewed |
| Refresh | record source, policy, standard, incident, or assessment trigger | assign an owner and date for revalidation |

### ATT&CK and Kill Chain Mapping Templates failure cases and required responses
**Section anchor.** [@sec:appendix-att-ck-and-kill-chain-mapping-templates].

| Failure case | Signal | Required response |
|---|---|---|
| Source laundering | claim cites an agent summary instead of a verified source | rebuild the claim ledger from direct sources |
| Boundary drift | exercise starts asking for live targets, private data, or external action | stop, substitute synthetic inputs, and document the block |
| Accessibility gap | learner cannot inspect, navigate, or complete the artifact | remediate and retest before reuse |
| Rights gap | affected group, safeguard, or redress path is missing | run HRIA/DPIA worksheet and escalate unresolved risk |
| Vendor opacity | tool owner, data use, logs, or exit path is unknown | replace tool or pause until procurement evidence exists |

### ATT&CK and Kill Chain Mapping Templates evidence package schemas

**Section anchor.** [@sec:appendix-att-ck-and-kill-chain-mapping-templates].

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

### ATT&CK and Kill Chain Mapping Templates rubric scoring bands
**Section anchor.** [@sec:appendix-att-ck-and-kill-chain-mapping-templates].

| Band | Evidence standard | Disposition |
|---|---|---|
| 4 - ready | source identity, accessibility, rights, safety, and reviewer evidence are complete | may be reused after normal refresh review |
| 3 - revise | one evidence field is incomplete but risk is bounded and remediable | revise before reuse |
| 2 - hold | multiple evidence fields are incomplete or ownership is unclear | hold for instructor and assurance review |
| 1 - reject | unsafe action, private data, inaccessible artifact, or unverified claim appears | reject and rebuild from safe inputs |

### ATT&CK and Kill Chain Mapping Templates refresh evidence
**Section anchor.** [@sec:appendix-att-ck-and-kill-chain-mapping-templates].

| Evidence item | Refresh trigger | Retained support |
|---|---|---|
| Source lane | official source, standard, or legal text changes | checked-as-of date and source note |
| Safety treatment | operational wording or unsafe motif appears | safe-substitution decision and blocked context |
| Accessibility | WCAG, UDL, or institutional accessibility duty changes | defect log, retest result, and owner |
| Rights | privacy, human-rights, public transparency, or education guidance changes | HRIA/DPIA revision note |
| Vendor/tool | contract, data-use, incident, or model capability changes | procurement packet and incident review |

### ATT&CK and Kill Chain Mapping Templates validation rubric
**Section anchor.** [@sec:appendix-att-ck-and-kill-chain-mapping-templates].

| Criterion | Passing evidence |
|---|---|
| Source identity | existing `ageintNNN` keys remain stable or new references are append-only |
| Verification | official, standards, public-domain, or scholarly URL is checked directly |
| Safety | method is converted into tabletop, audit, governance, or synthetic-data treatment |
| Reproducibility | another reviewer can rebuild the artifact from retained inputs |
| Rights review | privacy, IP, human-rights, workforce, and education impacts are considered where relevant |

### ATT&CK and Kill Chain Mapping Templates debrief protocol and reuse decision
**Section anchor.** [@sec:appendix-att-ck-and-kill-chain-mapping-templates].

Debrief by naming what the artifact can support, what it does not establish, what source changed, what risk was avoided by safe substitution, what human approval is still required, and when the appendix should be refreshed for MITRE ATT&CK Navigator Layer: Enterprise; the module Navigator Layer.

### ATT&CK and Kill Chain Mapping Templates visual navigation and evidence figures: purpose, source flow, and limits

The appendix uses [@fig:appendix-attack-killchain-mapping] and [@fig:ageint-safety-boundary-loop] to map its evidence flow, safety boundaries, review artifacts, and refresh cues.

Navigation links: [@sec:curriculum_orientation], [@sec:appendix-cryptographic-methods], [@sec:appendix-cognitive-security-and-inoculation-methods].

![The mapping template aligns observed behaviors to kill-chain phases and ATT&CK techniques for defensive sequencing only, ending in detection coverage and mitigation, never an action plan. The captioned view belongs to the att ck and kill chain mapping templates appendix and should be read as a map of Observed behavior (defensive), Kill-chain phase labeling, ATT&CK technique mapping, and Detection coverage matrix, not as a capability score or live-task instruction.](../../figures/mermaid/appendix-attack-killchain-mapping.png){#fig:appendix-attack-killchain-mapping}

### ATT&CK and Kill Chain Mapping Templates runtime item map and source roster: generated rows and citation support

| Safe curriculum treatment | Blocked source motif, audit-only | Allowed fixture | Rejected action | Required artifact | Citation spine |
|---|---|---|---|---|---|
| F.1 MITRE ATT&CK Navigator Layer: Enterprise | no blocked motif; source title used verbatim | public sources, synthetic records, owned-lab notes, and instructor handouts | external action, private-data processing, unsafe system interaction, or deployment | claim ledger, safe-lab packet, and reviewer handoff | [@ageint063] |
| F.2 MITRE ATT&CK for ICS Navigator Layer | no blocked motif; source title used verbatim | synthetic process logs, operator-decision cards, and safety stop rules | live device interaction, process manipulation, unsafe actuation, or plant operation | tabletop packet with asset, consequence, operator decision, and recovery evidence | [@ageint213] |
| F.3 Cyber Kill Chain Campaign Mapping Worksheet | no blocked motif; source title used verbatim | fabricated alerts, published defensive taxonomy labels, and debrief notes | scanning, exploitation, credential use, blocking, containment, or evasion | defensive coverage matrix and incident debrief | [@ageint061] |
| F.4 Adversary Emulation Plan Template | no blocked motif; source title used verbatim | public sources, synthetic records, owned-lab notes, and instructor handouts | external action, private-data processing, unsafe system interaction, or deployment | claim ledger, safe-lab packet, and reviewer handoff | - |
| F.5 Threat Intelligence Report Template (STIX v2.1 JSON) | no blocked motif; source title used verbatim | public sources, synthetic records, owned-lab notes, and instructor handouts | external action, private-data processing, unsafe system interaction, or deployment | claim ledger, safe-lab packet, and reviewer handoff | - |
