# Python OSINT Library {#sec:appendix-python-osint-library}

The current appendix is an evidence workbook for reusable classroom methods. It is educational and evidence-bounded: examples remain synthetic, defensive, lawful, and bounded to owned labs, public sources, or tabletop exercises. Source-item focus: Recon-ng Module Development: Custom Data Source Integration; SpiderFoot Custom Module: Target Intelligence Aggregation.

## Python OSINT Library workbook scope: purpose, safety envelope, and reuse decision

**Section anchor.** [@sec:appendix-python-osint-library].

### Python OSINT Library operating purpose
**Section anchor.** [@sec:appendix-python-osint-library].

The current appendix supports a reusable methods workbook. Each source item is treated as a reviewable classroom artifact rather than an operational instruction; examples begin with Recon-ng Module Development: Custom Data Source Integration; SpiderFoot Custom Module: Target Intelligence Aggregation.

### Python OSINT Library allowed-input boundary
**Section anchor.** [@sec:appendix-python-osint-library].

Allowed inputs for the current appendix are public official or scholarly sources, standards text, instructor-provided excerpts, synthetic datasets, owned-lab logs, toy examples, and generated rubrics that expose their provenance for Recon-ng Module Development: Custom Data Source Integration; SpiderFoot Custom Module: Target Intelligence Aggregation.

### Python OSINT Library excluded-action boundary
**Section anchor.** [@sec:appendix-python-osint-library].

Excluded actions for the current appendix are unauthorized collection, private-data processing, credential use, contact with real targets, live system interaction, exploit execution, deception, unsafe cyber-physical action, or external deployment while handling Recon-ng Module Development: Custom Data Source Integration; SpiderFoot Custom Module: Target Intelligence Aggregation.

### Python OSINT Library expected artifact package
**Section anchor.** [@sec:appendix-python-osint-library].

Expected appendix artifacts are a purpose statement, allowed-inputs card, excluded-actions card, source-lane map, provenance record, claim ledger, safe-substitution note, output schema, review rubric, and capstone handoff memo for Recon-ng Module Development: Custom Data Source Integration; SpiderFoot Custom Module: Target Intelligence Aggregation.

### Python OSINT Library safe artifact schema
**Section anchor.** [@sec:appendix-python-osint-library].

| Field | Required evidence | Reject condition |
|---|---|---|
| Purpose | lawful educational, governance, research, or defensive purpose | vague operational objective or missing authority |
| Inputs | public, official, scholarly, synthetic, owned-lab, or instructor-provided material | private data, live target data, credentialed access, or unclear provenance |
| Transform | summary, comparison, rubric scoring, tabletop simulation, or audit review | collection expansion, external action, or unsafe system interaction |
| Output | memo, matrix, checklist, ledger, rubric, or debrief packet | deployable procedure, target package, or automated action plan |
| Reviewer | human reviewer, approval gate, revision note, and refresh owner | anonymous ownership or no escalation path |

### Python OSINT Library input/output contract
**Section anchor.** [@sec:appendix-python-osint-library].

| Contract term | Input rule | Output rule |
|---|---|---|
| Source identity | retain `ageintNNN`, title, URL, and checked status | cite with Pandoc keys and avoid pasted raw URLs in prose |
| Accessibility | include plain-language labels, table headers, and figure alternatives | reject inaccessible figures, unlabeled tables, or single-modality evidence |
| Rights | identify affected groups, safeguards, and residual risk | preserve privacy, equality, access, contestability, and redress notes |
| Tooling | use allowlisted tools, visible prompts, logs, and stop conditions | keep outputs evidence-bounded, reversible, and human-reviewed |
| Refresh | record source, policy, standard, incident, or assessment trigger | assign an owner and date for revalidation |

### Python OSINT Library failure cases and required responses
**Section anchor.** [@sec:appendix-python-osint-library].

| Failure case | Signal | Required response |
|---|---|---|
| Source laundering | claim cites an agent summary instead of a verified source | rebuild the claim ledger from direct sources |
| Boundary drift | exercise starts asking for live targets, private data, or external action | stop, substitute synthetic inputs, and document the block |
| Accessibility gap | learner cannot inspect, navigate, or complete the artifact | remediate and retest before reuse |
| Rights gap | affected group, safeguard, or redress path is missing | run HRIA/DPIA worksheet and escalate unresolved risk |
| Vendor opacity | tool owner, data use, logs, or exit path is unknown | replace tool or pause until procurement evidence exists |

### Python OSINT Library evidence package schemas

**Section anchor.** [@sec:appendix-python-osint-library].

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

### Python OSINT Library rubric scoring bands
**Section anchor.** [@sec:appendix-python-osint-library].

| Band | Evidence standard | Disposition |
|---|---|---|
| 4 - ready | source identity, accessibility, rights, safety, and reviewer evidence are complete | may be reused after normal refresh review |
| 3 - revise | one evidence field is incomplete but risk is bounded and remediable | revise before reuse |
| 2 - hold | multiple evidence fields are incomplete or ownership is unclear | hold for instructor and assurance review |
| 1 - reject | unsafe action, private data, inaccessible artifact, or unverified claim appears | reject and rebuild from safe inputs |

### Python OSINT Library refresh evidence
**Section anchor.** [@sec:appendix-python-osint-library].

| Evidence item | Refresh trigger | Retained support |
|---|---|---|
| Source lane | official source, standard, or legal text changes | checked-as-of date and source note |
| Safety treatment | operational wording or unsafe motif appears | safe-substitution decision and blocked context |
| Accessibility | WCAG, UDL, or institutional accessibility duty changes | defect log, retest result, and owner |
| Rights | privacy, human-rights, public transparency, or education guidance changes | HRIA/DPIA revision note |
| Vendor/tool | contract, data-use, incident, or model capability changes | procurement packet and incident review |

### Python OSINT Library validation rubric
**Section anchor.** [@sec:appendix-python-osint-library].

| Criterion | Passing evidence |
|---|---|
| Source identity | existing `ageintNNN` keys remain stable or new references are append-only |
| Verification | official, standards, public-domain, or scholarly URL is checked directly |
| Safety | method is converted into tabletop, audit, governance, or synthetic-data treatment |
| Reproducibility | another reviewer can rebuild the artifact from retained inputs |
| Rights review | privacy, IP, human-rights, workforce, and education impacts are considered where relevant |

### Python OSINT Library debrief protocol and reuse decision
**Section anchor.** [@sec:appendix-python-osint-library].

Debrief by naming what the artifact can support, what it does not establish, what source changed, what risk was avoided by safe substitution, what human approval is still required, and when the appendix should be refreshed for Recon-ng Module Development: Custom Data Source Integration; SpiderFoot Custom Module: Target Intelligence Aggregation.

### Python OSINT Library visual navigation and evidence figures: purpose, source flow, and limits

The appendix uses [@fig:appendix-python-osint-defensive-architecture] and [@fig:ageint-safety-boundary-loop] to map its evidence flow, safety boundaries, review artifacts, and refresh cues.

Navigation links: [@sec:curriculum_orientation], [@sec:chapter-ethics-of-intelligence-and-cognitive-security], [@sec:appendix-langchain-langgraph-ageint-patterns].

![The reference OSINT library is organized as governed modules where every collector passes through rate-limiting, minimization, and provenance logging before results reach analysis. It is anchored to the python osint library appendix; use it to inspect Analyst query, Governance layer: rate limits, ToS check, minimization, Collector modules, and Web and domain while preserving the distinction between curriculum structure, evidence boundary, and accountable practice.](../../figures/mermaid/appendix-python-osint-defensive-architecture.png){#fig:appendix-python-osint-defensive-architecture}

### Python OSINT Library runtime item map and source roster: generated rows and citation support

**Section anchor.** [@sec:appendix-python-osint-library].

| Safe curriculum treatment | Blocked source motif, audit-only | Allowed fixture | Rejected action | Required artifact | Citation spine |
|---|---|---|---|---|---|
| Custom-source integration governance review using toy records | A.1 retained for audit; operational wording transformed | public sources, synthetic records, owned-lab notes, and instructor handouts | external action, private-data processing, unsafe system interaction, or deployment | claim ledger, safe-lab packet, and reviewer handoff | - |
| Automated-source aggregation governance review using toy records | A.2 retained for audit; operational wording transformed | instructor-provided source cards, toy records, and provenance notes | live collection expansion, tracking, private-data discovery, or targeting | source-quality card and minimization note | - |
| Search-exposure provenance review using instructor-provided records | A.3 retained for audit; operational wording transformed | instructor-provided source cards, toy records, and provenance notes | live collection expansion, tracking, private-data discovery, or targeting | source-quality card and minimization note | - |
| Identity-data minimization review using instructor-provided records | A.4 retained for audit; operational wording transformed | sample role records, ethics cards, and reviewer notes | impersonation, contact activity, elicitation, handling, or source exposure | source-protection ethics memo and escalation path | - |
| Social-source provenance and minimization review using toy records | A.5 retained for audit; operational wording transformed | instructor-provided source cards, toy records, and provenance notes | live collection expansion, tracking, private-data discovery, or targeting | source-quality card and minimization note | - |
| IP-geolocation uncertainty review using synthetic records | A.6 retained for audit; operational wording transformed | provided imagery metadata, synthetic change examples, and uncertainty notes | live collection expansion, tracking, private-data discovery, or targeting | source-quality card and minimization note | - |
| Sandbox policy and tool-isolation review using toy OSINT fixtures | A.7 retained for audit; operational wording transformed | toy OSINT fixtures, sandbox policy cards, and blocked-action logs | external execution, credentialed access, network calls, or unmanaged tool use | tool-isolation run card and denied-action evidence | - |
