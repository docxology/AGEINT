# Python OSINT Library {#sec:appendix-python-osint-library}

## Python OSINT Library workbook scope: purpose, safety envelope, and reuse decision

**Navigation.** Parent section: [@sec:appendix-python-osint-library].

### Python OSINT Library operating purpose
Source-item focus: Recon-ng Module Development: Custom Data Source Integration; SpiderFoot Custom Module: Target Intelligence Aggregation. The source-item map preserves the curriculum identity; it does not authorize the source item's operational wording. Use only the offline substitutions below: no live queries, credentials, private records, external code execution, profiling, persuasion delivery, or cyber-physical actions.

Use the claim record and eight-step analytic procedure in [@sec:analytic-workflow], not a second local evidence schema. All inputs below are invented classroom records. Worked outputs and negative-control results are authored expectations, not executed tests, empirical findings, or evidence that a named framework is secure or effective.

## Offline source-adapter and provenance exercise

**Input.** Fixture A1 is a fictional municipal service notice: `id=n1; event_day=12; status=maintenance`. A2 is a mirror quoting n1 verbatim. A3 is an invented exposure-inventory row, `asset=lab-router; observation_day=3; service_label=unknown`; it contains no address, account, or person. The question is whether these records support a current service-exposure claim.

1. Give each fixture a source ID, upstream origin, event date, and supplied-as-of date. Preserve the raw row alongside the normalized one; never silently turn `unknown` into a detected service.
2. Design a paper adapter contract: input fixture, permitted fields, normalized output, parse-error field, and provenance pointer. Recon-ng/SpiderFoot module motifs become adapter reviews; Shodan/theHarvester motifs become static inventory and field-minimization reviews, not queries or harvesting.
3. Mark A2 dependent on A1. Compare the dates and meanings of A1 and A3 before joining them; a stale inventory label cannot establish the notice's cause or current exposure.
4. Replace social-graph scraping with a graph of document-to-document citations. Treat geolocation/IP-attribution motifs as a worksheet on missing precision and identity evidence, not a location or ownership finding. Represent sandboxing as an isolation checklist, with no deployment.

**Example output.** `claim=A-current-exposure; origins=2; n1-mirror=dependent; current-exposure=not-established; gap=dated-owned-inventory; owner=instructor; disposition=hold`. The notice is evidence only of what the fictional publisher reported; the inventory describes an older fixture.

**Expected negative-control result.** Add A4, another mirror of n1: the origin count and judgment must not strengthen. Remove A3: the exposure question becomes unassessable, not 'safe'. A malformed date must produce a parse exception record rather than a guessed date.

**Reuse disposition and applicability.** Reuse the parser contract after a second reader can trace every normalized field to its fixture. Retain fixture versions, transformation notes, and correction history under the lineage/retention forms; document that no model or vendor is used in this paper exercise. Any later tool-assisted variant needs its own documentation and tool review. Refresh when field semantics or allowed inputs change. OSINT strategy provides context for tradecraft, not permission to collect [@official_ic_osint_strategy]; analytic standards support separating sourcing and inference [@official_odni_icd_203].

### Python OSINT Library shared forms and local applicability record
Complete one local record: `packet/version; applicable forms and reason; not-applicable forms and reason; missing evidence; reviewer; disposition; refresh trigger`. The workbook's applicability note is a starting point, not approval. Never replace a missing review with a bare 'N/A'.

For provenance and documentation, use [@sec:source-lane-map], [@sec:data-lineage-registry], and [@sec:model-and-dataset-documentation-card]. For communication and handling, use [@sec:transparency-and-communication-notice] and [@sec:records-retention-and-audit-trail].

For rights, access, and tool changes, use [@sec:hria-and-dpia-worksheet], [@sec:accessibility-and-udl-review], [@sec:learner-support-and-accommodation-plan], and [@sec:procurement-and-vendor-oversight]. For reuse or exceptions, use [@sec:release-and-change-control-gate] and [@sec:risk-exception-and-acceptance-memo].

For teaching and revision, use [@sec:assessment-integrity-protocol], [@sec:instructor-question-bank], [@sec:adversarial-assurance-cycle], and [@sec:remediation-backlog]. Apply the competency and answer-quality rubrics in [@sec:method-assurance-reference]; retain the relevant local evidence rather than copying every shared table into the packet.

### Python OSINT Library visual navigation and evidence figures: purpose, source flow, and limits

The appendix uses [@fig:appendix-python-osint-defensive-architecture] and [@fig:ageint-safety-boundary-loop] to map its evidence flow, safety boundaries, review artifacts, and refresh cues.

Navigation links: [@sec:curriculum_orientation], [@sec:chapter-ethics-of-intelligence-and-cognitive-security], [@sec:appendix-langchain-langgraph-ageint-patterns].

![Illustrative workbook architecture, not an implemented OSINT collection library. The appendix is runnable manually with supplied records; it does not provide working collectors or authorize live searches. Availability, terms-of-service checks and provenance do not by themselves establish permission, independence or factual truth.](../../figures/mermaid/appendix-python-osint-defensive-architecture.png){#fig:appendix-python-osint-defensive-architecture}

### Python OSINT Library runtime item map and source roster: generated rows and citation support

**Navigation.** Parent section: [@sec:appendix-python-osint-library].

| Source item / safe study title | Provenance status | Citation context |
|---|---|---|
| Custom-source integration governance review using toy records | A.1 retained for audit; operational wording transformed | - |
| Automated-source aggregation governance review using toy records | A.2 retained for audit; operational wording transformed | - |
| Search-exposure provenance review using instructor-provided records | A.3 retained for audit; operational wording transformed | - |
| Identity-data minimization review using instructor-provided records | A.4 retained for audit; operational wording transformed | - |
| Social-source provenance and minimization review using toy records | A.5 retained for audit; operational wording transformed | - |
| IP-geolocation uncertainty review using synthetic records | A.6 retained for audit; operational wording transformed | - |
| Sandbox policy and tool-isolation review using toy OSINT fixtures | A.7 retained for audit; operational wording transformed | - |
