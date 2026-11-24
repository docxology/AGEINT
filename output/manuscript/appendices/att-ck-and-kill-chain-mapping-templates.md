# ATT&CK and Kill Chain Mapping Templates {#sec:appendix-att-ck-and-kill-chain-mapping-templates}

## ATT&CK and Kill Chain Mapping Templates workbook scope: purpose, safety envelope, and reuse decision

**Navigation.** Parent section: [@sec:appendix-att-ck-and-kill-chain-mapping-templates].

### ATT&CK and Kill Chain Mapping Templates operating purpose
Source-item focus: MITRE ATT&CK Navigator Layer: Enterprise; MITRE ATT&CK for ICS Navigator Layer. The source-item map preserves the curriculum identity; it does not authorize the source item's operational wording. Use only the offline substitutions below: no live queries, credentials, private records, external code execution, profiling, persuasion delivery, or cyber-physical actions.

Use the claim record and eight-step analytic procedure in [@sec:analytic-workflow], not a second local evidence schema. All inputs below are invented classroom records. Worked outputs and negative-control results are authored expectations, not executed tests, empirical findings, or evidence that a named framework is secure or effective.

## Defensive ATT&CK and timeline mapping exercise

Use the Enterprise and ICS matrices as versioned behavior taxonomies for defensive coverage, not actor-identification tools [@official_mitre_attack_enterprise]; [@official_mitre_attack_ics]. The guide's Enterprise, ICS, and Kill Chain references retain their source roles [@ageint063]; [@ageint213]; [@ageint061]. A taxonomy match alone establishes neither malicious intent nor a complete campaign.

**Input.** F1 is an invented endpoint event: `09:00; lab-host; command interpreter started; command text unavailable; maintenance ticket present`. F2 is a fictional ICS temperature alarm without process or controller logs. F3 is a failed login event. A frozen instructor excerpt contains the Enterprise `T1059` definition and its version; no system is accessed or emulated.

1. Preserve the raw event, time basis, missing fields, and source version. Separate event observation, candidate technique, contextual explanation, and detection coverage into different columns.
2. Compare F1 to the excerpt: T1059 is a candidate behavior label, while authorized maintenance remains a credible explanation. Do not select a subtechnique or malicious actor without the necessary evidence.
3. Leave F2 unmapped where only an outcome is observed; a temperature alarm does not establish an adversarial control action. Do not force an ICS technique onto an Enterprise event.
4. Put only observed events on the timeline. Mark unobserved Kill Chain phases 'unknown', not 'completed' or 'absent'. A Navigator-style color represents this packet's coverage status, not attack likelihood or severity.
5. Replace emulation planning with a defensive telemetry-gap review. A STIX-like output retains observation IDs, candidate mappings, confidence basis, and caveats; omit actor attribution and any executable action sequence.

**Example output.** `F1 | candidate T1059 | behavior compatible; intent unknown | maintenance alternative | command details missing`. `F2 | unmapped | outcome only`. `F3 | unmapped | failed login alone does not show use of valid accounts`.

**Expected negative-control result.** Relabel F1 as a known administrator's scheduled task: the observed behavior label may remain, but an unsupported 'attack' conclusion must disappear. Removing command-interpreter evidence makes T1059 unsupported; adding an actor name to the fixture title supplies no attribution evidence.

**Reuse disposition and applicability.** Accept only the bounded mapping worksheet, not a defensive-effectiveness claim. Retain matrix version, locators, unmapped events, and color legend under lineage/documentation forms; no model/vendor or live-telemetry review is needed for these invented rows. Refresh on taxonomy changes or any proposed use of real telemetry.

### ATT&CK and Kill Chain Mapping Templates shared forms and local applicability record
Complete one local record: `packet/version; applicable forms and reason; not-applicable forms and reason; missing evidence; reviewer; disposition; refresh trigger`. The workbook's applicability note is a starting point, not approval. Never replace a missing review with a bare 'N/A'.

For provenance and documentation, use [@sec:source-lane-map], [@sec:data-lineage-registry], and [@sec:model-and-dataset-documentation-card]. For communication and handling, use [@sec:transparency-and-communication-notice] and [@sec:records-retention-and-audit-trail].

For rights, access, and tool changes, use [@sec:hria-and-dpia-worksheet], [@sec:accessibility-and-udl-review], [@sec:learner-support-and-accommodation-plan], and [@sec:procurement-and-vendor-oversight]. For reuse or exceptions, use [@sec:release-and-change-control-gate] and [@sec:risk-exception-and-acceptance-memo].

For teaching and revision, use [@sec:assessment-integrity-protocol], [@sec:instructor-question-bank], [@sec:adversarial-assurance-cycle], and [@sec:remediation-backlog]. Apply the competency and answer-quality rubrics in [@sec:method-assurance-reference]; retain the relevant local evidence rather than copying every shared table into the packet.

### ATT&CK and Kill Chain Mapping Templates visual navigation and evidence figures: purpose, source flow, and limits

The appendix uses [@fig:appendix-attack-killchain-mapping] and [@fig:ageint-safety-boundary-loop] to map its evidence flow, safety boundaries, review artifacts, and refresh cues.

Navigation links: [@sec:curriculum_orientation], [@sec:appendix-cryptographic-methods], [@sec:appendix-cognitive-security-and-inoculation-methods].

![The mapping template aligns observed behaviors to kill-chain phases and ATT&CK techniques for defensive sequencing only, ending in detection coverage and mitigation, never an action plan. The captioned view belongs to the att ck and kill chain mapping templates appendix and should be read as a map of Observed behavior (defensive), Kill-chain phase labeling, ATT&CK technique mapping, and Detection coverage matrix, not as a capability score or live-task instruction.](../../figures/mermaid/appendix-attack-killchain-mapping.png){#fig:appendix-attack-killchain-mapping}

### ATT&CK and Kill Chain Mapping Templates runtime item map and source roster: generated rows and citation support

| Source item / safe study title | Provenance status | Citation context |
|---|---|---|
| F.1 MITRE ATT&CK Navigator Layer: Enterprise | no blocked motif; source title used verbatim | [@ageint063] |
| F.2 MITRE ATT&CK for ICS Navigator Layer | no blocked motif; source title used verbatim | [@ageint213] |
| F.3 Cyber Kill Chain Campaign Mapping Worksheet | no blocked motif; source title used verbatim | [@ageint061] |
| F.4 Adversary Emulation Plan Template | no blocked motif; source title used verbatim | - |
| F.5 Threat Intelligence Report Template (STIX v2.1 JSON) | no blocked motif; source title used verbatim | - |
