# AutoGen and MCP Patterns {#sec:appendix-autogen-and-mcp-patterns}

The current appendix is an evidence workbook for reusable classroom methods. It is educational and evidence-bounded: examples remain synthetic, defensive, lawful, and bounded to owned labs, public sources, or tabletop exercises. Source-item focus: AutoGen Code-Execution Exploit Chain (with Sandboxing Countermeasure); MCP Server: Building a STIX/TAXII Intelligence Tool Server.

## AutoGen and MCP Patterns workbook scope: purpose, safety envelope, and reuse decision

**Section anchor.** [@sec:appendix-autogen-and-mcp-patterns].

### AutoGen and MCP Patterns operating purpose
**Section anchor.** [@sec:appendix-autogen-and-mcp-patterns].

The current appendix supports a reusable methods workbook. Each source item is treated as a reviewable classroom artifact rather than an operational instruction; examples begin with AutoGen Code-Execution Exploit Chain (with Sandboxing Countermeasure); MCP Server: Building a STIX/TAXII Intelligence Tool Server.

### AutoGen and MCP Patterns allowed-input boundary
**Section anchor.** [@sec:appendix-autogen-and-mcp-patterns].

Allowed inputs for the current appendix are public official or scholarly sources, standards text, instructor-provided excerpts, synthetic datasets, owned-lab logs, toy examples, and generated rubrics that expose their provenance for AutoGen Code-Execution Exploit Chain (with Sandboxing Countermeasure); MCP Server: Building a STIX/TAXII Intelligence Tool Server.

### AutoGen and MCP Patterns excluded-action boundary
**Section anchor.** [@sec:appendix-autogen-and-mcp-patterns].

Excluded actions for the current appendix are unauthorized collection, private-data processing, credential use, contact with real targets, live system interaction, exploit execution, deception, unsafe cyber-physical action, or external deployment while handling AutoGen Code-Execution Exploit Chain (with Sandboxing Countermeasure); MCP Server: Building a STIX/TAXII Intelligence Tool Server.

### AutoGen and MCP Patterns expected artifact package
**Section anchor.** [@sec:appendix-autogen-and-mcp-patterns].

Expected appendix artifacts are a purpose statement, allowed-inputs card, excluded-actions card, source-lane map, provenance record, claim ledger, safe-substitution note, output schema, review rubric, and capstone handoff memo for AutoGen Code-Execution Exploit Chain (with Sandboxing Countermeasure); MCP Server: Building a STIX/TAXII Intelligence Tool Server.

### AutoGen and MCP Patterns safe artifact schema
**Section anchor.** [@sec:appendix-autogen-and-mcp-patterns].

| Field | Required evidence | Reject condition |
|---|---|---|
| Purpose | lawful educational, governance, research, or defensive purpose | vague operational objective or missing authority |
| Inputs | public, official, scholarly, synthetic, owned-lab, or instructor-provided material | private data, live target data, credentialed access, or unclear provenance |
| Transform | summary, comparison, rubric scoring, tabletop simulation, or audit review | collection expansion, external action, or unsafe system interaction |
| Output | memo, matrix, checklist, ledger, rubric, or debrief packet | deployable procedure, target package, or automated action plan |
| Reviewer | human reviewer, approval gate, revision note, and refresh owner | anonymous ownership or no escalation path |

### AutoGen and MCP Patterns input/output contract
**Section anchor.** [@sec:appendix-autogen-and-mcp-patterns].

| Contract term | Input rule | Output rule |
|---|---|---|
| Source identity | retain `ageintNNN`, title, URL, and checked status | cite with Pandoc keys and avoid pasted raw URLs in prose |
| Accessibility | include plain-language labels, table headers, and figure alternatives | reject inaccessible figures, unlabeled tables, or single-modality evidence |
| Rights | identify affected groups, safeguards, and residual risk | preserve privacy, equality, access, contestability, and redress notes |
| Tooling | use allowlisted tools, visible prompts, logs, and stop conditions | keep outputs evidence-bounded, reversible, and human-reviewed |
| Refresh | record source, policy, standard, incident, or assessment trigger | assign an owner and date for revalidation |

### AutoGen and MCP Patterns failure cases and required responses
**Section anchor.** [@sec:appendix-autogen-and-mcp-patterns].

| Failure case | Signal | Required response |
|---|---|---|
| Source laundering | claim cites an agent summary instead of a verified source | rebuild the claim ledger from direct sources |
| Boundary drift | exercise starts asking for live targets, private data, or external action | stop, substitute synthetic inputs, and document the block |
| Accessibility gap | learner cannot inspect, navigate, or complete the artifact | remediate and retest before reuse |
| Rights gap | affected group, safeguard, or redress path is missing | run HRIA/DPIA worksheet and escalate unresolved risk |
| Vendor opacity | tool owner, data use, logs, or exit path is unknown | replace tool or pause until procurement evidence exists |

### AutoGen and MCP Patterns evidence package schemas

**Section anchor.** [@sec:appendix-autogen-and-mcp-patterns].

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

### AutoGen and MCP Patterns rubric scoring bands
**Section anchor.** [@sec:appendix-autogen-and-mcp-patterns].

| Band | Evidence standard | Disposition |
|---|---|---|
| 4 - ready | source identity, accessibility, rights, safety, and reviewer evidence are complete | may be reused after normal refresh review |
| 3 - revise | one evidence field is incomplete but risk is bounded and remediable | revise before reuse |
| 2 - hold | multiple evidence fields are incomplete or ownership is unclear | hold for instructor and assurance review |
| 1 - reject | unsafe action, private data, inaccessible artifact, or unverified claim appears | reject and rebuild from safe inputs |

### AutoGen and MCP Patterns refresh evidence
**Section anchor.** [@sec:appendix-autogen-and-mcp-patterns].

| Evidence item | Refresh trigger | Retained support |
|---|---|---|
| Source lane | official source, standard, or legal text changes | checked-as-of date and source note |
| Safety treatment | operational wording or unsafe motif appears | safe-substitution decision and blocked context |
| Accessibility | WCAG, UDL, or institutional accessibility duty changes | defect log, retest result, and owner |
| Rights | privacy, human-rights, public transparency, or education guidance changes | HRIA/DPIA revision note |
| Vendor/tool | contract, data-use, incident, or model capability changes | procurement packet and incident review |

### AutoGen and MCP Patterns validation rubric
**Section anchor.** [@sec:appendix-autogen-and-mcp-patterns].

| Criterion | Passing evidence |
|---|---|
| Source identity | existing `ageintNNN` keys remain stable or new references are append-only |
| Verification | official, standards, public-domain, or scholarly URL is checked directly |
| Safety | method is converted into tabletop, audit, governance, or synthetic-data treatment |
| Reproducibility | another reviewer can rebuild the artifact from retained inputs |
| Rights review | privacy, IP, human-rights, workforce, and education impacts are considered where relevant |

### AutoGen and MCP Patterns debrief protocol and reuse decision
**Section anchor.** [@sec:appendix-autogen-and-mcp-patterns].

Debrief by naming what the artifact can support, what it does not establish, what source changed, what risk was avoided by safe substitution, what human approval is still required, and when the appendix should be refreshed for AutoGen Code-Execution Exploit Chain (with Sandboxing Countermeasure); MCP Server: Building a STIX/TAXII Intelligence Tool Server.

## MCP and AutoGen source boundary

This appendix separates protocol claims, framework-pattern claims, and security claims before learners build any classroom artifact. MCP interoperability language is grounded in the version-pinned official specification; tool-consent, confused-deputy, token-handling, and least-privilege language is grounded in the official MCP security guidance and NSA security-design guidance. STIX/TAXII examples are treated as standards-governed data-exchange examples, not as permission to connect to external systems [@official_model_context_protocol_specification]; [@official_model_context_protocol_security_best_practices]; [@official_nsa_mcp_security_design_considerations]; [@official_oasis_stix_21]; [@official_oasis_taxii_21].

AutoGen and multi-agent framework rows remain a safe-substitution exercise: the learner may compare orchestration patterns, sandbox policies, denied-action logs, and reviewer evidence, but may not run external code, contact live services, or treat framework names as assurance evidence. When the source guide supplies only framework or security context, this appendix records the limitation and routes normative claims back to the official protocol, standards, and security anchors rather than laundering them through an agent-generated summary [@ageint147]; [@ageint153]; [@ageint155]; [@ageint299]; [@ageint309]; [@ageint310].

### AutoGen and MCP Patterns visual navigation and evidence figures: purpose, source flow, and limits

The appendix uses [@fig:appendix-mcp-host-client-server], [@fig:ageint-mcp-version-boundary], and [@fig:ageint-safety-boundary-loop] to map its evidence flow, safety boundaries, review artifacts, and refresh cues.

Navigation links: [@sec:curriculum_orientation], [@sec:appendix-crewai-multi-agent-operations], [@sec:appendix-cryptographic-methods].

![MCP standardizes how an agent host connects through clients to servers that expose resources, prompts, and tools under capability negotiation and least-privilege scoping. In the autogen and mcp patterns appendix, it lets readers compare Agent host, Client A, Client B, and Capability negotiation so the visual functions as a traceable course aid rather than an unscoped assertion.](../../figures/mermaid/appendix-mcp-host-client-server.png){#fig:appendix-mcp-host-client-server}

![Conceptual schematic showing that MCP tool access depends on host, client, server, version, identity, authorization, and audit evidence rather than protocol names alone. In the autogen and mcp patterns appendix, it lets readers compare Host policy, MCP client, Identity and authorization, and Block or isolate so the visual functions as a traceable course aid rather than an unscoped assertion.](../../figures/mermaid/ageint-mcp-version-boundary.png){#fig:ageint-mcp-version-boundary}

### AutoGen and MCP Patterns runtime item map and source roster: generated rows and citation support

| Safe curriculum treatment | Blocked source motif, audit-only | Allowed fixture | Rejected action | Required artifact | Citation spine |
|---|---|---|---|---|---|
| AutoGen sandbox and code-execution approval review | D.1 retained for audit; operational wording transformed | toy OSINT fixtures, sandbox policy cards, and blocked-action logs | external execution, credentialed access, network calls, or unmanaged tool use | tool-isolation run card and denied-action evidence | - |
| D.2 MCP Server: Building a STIX/TAXII Intelligence Tool Server | no blocked motif; source title used verbatim | public sources, synthetic records, owned-lab notes, and instructor handouts | external action, private-data processing, unsafe system interaction, or deployment | claim ledger, safe-lab packet, and reviewer handoff | - |
| D.3 MCP Security: NSA Guidance Implementation in Python | no blocked motif; source title used verbatim | public sources, synthetic records, owned-lab notes, and instructor handouts | external action, private-data processing, unsafe system interaction, or deployment | claim ledger, safe-lab packet, and reviewer handoff | [@ageint155] |
| D.4 AutoGen GroupChat for Competing Hypothesis Analysis | no blocked motif; source title used verbatim | public sources, synthetic records, owned-lab notes, and instructor handouts | external action, private-data processing, unsafe system interaction, or deployment | claim ledger, safe-lab packet, and reviewer handoff | - |
