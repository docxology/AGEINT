# Curriculum Orientation: reader paths, evidence maps, and safety gates {#sec:curriculum_orientation}

This manuscript is a runtime-hydrated curriculum atlas. The source templates
keep guide-derived values as neutral tokens, while the resolved manuscript in
`output/manuscript/` injects titles, labels, counts, source spines, semantic
paths, and bibliography rows from `data/curriculum/`.

## How to use this atlas: navigation path, evidence checks, and verifier handoff {#sec:how-to-use-this-atlas}

Read AGEINT as a navigable curriculum-and-assurance atlas rather than a linear
textbook or empirical evaluation report. Start with [@sec:curriculum-map] and
[@fig:ageint-curriculum-map] to choose the part, open the linked part
introduction to see the module sequence, then use each chapter overview for the
figures, source lane, and assessment artifact that matter for the current
decision. Keep [@sec:bibliography_atlas] open when checking a claim, because it
preserves source identity, provenance type, source tier, and refresh context in
one place.

Use the first pages as signposts, not as a preface to skip. The handoff path is
intentionally explicit: domain part -> module overview -> practice studio ->
evidence contract -> governance boundary -> assessment route ->
bibliography/source lane -> verifier reports.

| Move | Deep links | What the links foreshadow |
|---|---|---|
| Start here | [@sec:curriculum-map], [@sec:synthetic-analytic-tradecraft-thesis], and [@sec:reader-paths] | Choose a domain part, name the Synthetic Analytic Tradecraft contract, and decide which reader path governs the next move. |
| Then check | [@sec:analysis-validation-protocol], [@sec:source-lane-map], and [@sec:bibliography_atlas] | Match the claim class to evidence, lane, citation identity, and refresh duty before treating prose or figures as support. |
| Before you trust | [@sec:safe-substitution-matrix], [@sec:orientation-figures-and-course-links], and [@sec:method-assurance-reference] | Confirm risky motifs were converted to bounded artifacts, figures carry their limits, and verifier reports agree with the rendered manuscript. |

Claim classes are separated at source-selection time. Governance claims,
technical and theoretical claims, empirical capability claims, and
source-construction claims each need a matching evidence type; the shared method
reference records the PRISMA-S-inspired source-reporting fields used when a
search or discovery process supports manuscript content
[@scholarly_rethlefsen_2021_prisma_s].

## Synthetic Analytic Tradecraft thesis: synthetic fixtures, source discipline, and reviewable claims {#sec:synthetic-analytic-tradecraft-thesis}

AGEINT is strongest when read as **Synthetic Analytic Tradecraft**: a governed
practice for using synthetic inputs, generated artifacts, and bounded agentic
assistance to make analytic reasoning inspectable before any real-world action
is considered. The synthetic layer supplies safe fixtures: toy records, public
declassified examples, instructor-provided evidence cards, owned-lab logs, and
rendered figures. The tradecraft layer supplies the harder standard: source
description, alternative hypotheses, assumption checks, probability/confidence
separation, dissent, and reviewer challenge
[@official_odni_icd_203]; [@official_cia_tradecraft_primer];
[@scholarly_heuer_psychology_intelligence_analysis].

This framing lets the reader regard the manuscript highly for the right reason.
It is not an operational manual and not a benchmark proving autonomous analytic
performance. It is a source-governed workbench for producing reviewable analytic
artifacts under synthetic conditions. The relevant question is whether a module
can leave behind a traceable evidence packet that another analyst, instructor,
or assurance reviewer can challenge: source keys, caveats, assumptions,
alternatives, confidence basis, negative controls, rights constraints, and
refresh triggers. The tradecraft figures make this claim visible: the governed
system map [@fig:ageint-graphical-abstract] shows the whole governed stack; the
analytic evidence ladder [@fig:ageint-analytic-tradecraft-evidence-ladder]
separates doctrine, reform, postmortem, empirical, and forecasting evidence;
the SAT evidence boundary [@fig:ageint-sat-evidence-boundary] prevents
universal debiasing claims; the SAT method contract
[@fig:ageint-synthetic-tradecraft-method-contract] binds source-family
triangulation, synthetic fixtures, analytic field separation,
negative-control testing, reviewer challenge, and artifact-evidence reporting;
and the first-principles decomposition
[@fig:ageint-first-principles-tradecraft-decomposition] forces observation,
inference, assumption, likelihood, confidence, dissent, and decision boundary
fields to remain separate.

| SAT commitment | How AGEINT implements it | Early audit surface |
|---|---|---|
| Synthetic before operational | Exercises use classroom fixtures, public or declassified examples, owned-lab traces, and tabletop records. | [@sec:safety-rail] and [@sec:safe-substitution-matrix] |
| Tradecraft before automation | Agent assistance must preserve source descriptors, alternatives, assumptions, probability/confidence boundaries, and reviewer challenge. | [@fig:ageint-sat-evidence-boundary] and [@sec:method-assurance-reference] |
| Evidence packet before claim | Claims need source keys, caveats, source-family triangulation, claim-calibration review, and refresh duties before reuse. | [@fig:ageint-synthetic-tradecraft-method-contract], [@fig:ageint-scholarship-triangulation-map], and [@fig:ageint-claim-calibration-and-visual-semantics] |
| Negative control before trust | Validators, rubrics, rendered PDFs, and figure registries are treated as attackable artifacts. | [@fig:ageint-redteam-tradecraft-negative-control-loop] and [@sec:verifier-first-artifact-evidence] |

## Reader paths: instructor, learner, reviewer, and maintainer handoffs {#sec:reader-paths}

| Reader | Fast path | Evidence to keep |
|---|---|---|
| Instructor | Pair the linked part introduction from [@sec:curriculum-map] with the module overview, practice studio, evidence contract, governance boundary, and assessment route before assigning a studio exercise. | rubric row, excluded-action note, and source refresh trigger |
| Learner | Follow the module sequence from primer to practice studio, evidence contract, governance boundary, and assessment route before drafting a capstone packet. | claim ledger entry, uncertainty note, and blocked-use statement |
| Assurance reviewer | Trace each material claim through [@sec:source-lane-map], [@sec:bibliography_atlas], governance boundary, figure/course links, and verifier reports. | source key, review owner, caveat, and reproducible artifact path |
| Builder or maintainer | Treat generated output as an audit surface; update data, templates, manifest code, or figure specs, then rebuild and compare verifier reports. | changed source file, regeneration command, and validation result |

## Curriculum map: parts, modules, and source-backed route choices {#sec:curriculum-map}

{{CURRICULUM_PART_ROWS}}

## Runtime inventory: generated counts, anchors, and method appendices {#sec:runtime-inventory}

| Derived artifact | Runtime value |
|---|---:|
| Curriculum parts | {{CURRICULUM_PART_COUNT}} |
| Curriculum modules | {{CURRICULUM_CHAPTER_COUNT}} |
| Methods appendices | {{CURRICULUM_APPENDIX_COUNT}} |
| AGEINT patterns | {{CURRICULUM_PATTERN_COUNT}} |
| Parsed references | {{CURRICULUM_REFERENCE_COUNT}} |
| Official source-quality anchors | {{SOURCE_QUALITY_ANCHOR_COUNT}} |
| Intelligence research anchors | {{INTELLIGENCE_RESEARCH_ANCHOR_COUNT}} |
| Intelligence practice lenses | {{INTELLIGENCE_PRACTICE_LENS_COUNT}} |

## Related work and contribution boundary: adjacent literatures and AGEINT limits {#sec:related-work-and-contribution-boundary}

AGEINT sits between several bodies of work rather than inside only one of them:
AI risk-management guidance, generative-AI profiles, public-sector agentic-AI
controls, model and dataset documentation practices, active-inference theory,
agent security, and source-reporting methods [@official_nist_ai_rmf];
[@official_nist_ai_600_1]; [@official_canada_agentic_ai_guide];
[@scholarly_model_cards_model_reporting];
[@scholarly_datasheets_for_datasets];
[@scholarly_data_cards_dataset_documentation];
[@scholarly_friston_2010_fep];
[@scholarly_buckley_2017_fep_mathematical_review];
[@scholarly_greshake_2023_indirect_prompt_injection];
[@scholarly_rethlefsen_2021_prisma_s]. Its contribution is not a new
agent architecture, cognitive theory, attack benchmark, or measured learning
outcome. The contribution is a versioned curriculum-and-assurance framework
that links source identity, claim classes, safe exercises, figures, capstone
artifacts, and rebuildable review gates for bounded agentic-intelligence
education.

The four-domain convergence map
[@fig:ageint-si-tradecraft-opsec-cogsec-convergence] makes that boundary visible.
Synthetic-intelligence support is treated as useful only when analytic
tradecraft standards, OPSEC and zero-trust constraints, and cognitive-security
safeguards remain separate review gates [@scholarly_dylan_stivang_2025_emerging_tech_intelligence];
[@scholarly_caballero_jenkins_2024_llm_national_security];
[@official_belfer_mcmahon_2024_ai_tradecraft_standards];
[@official_reagan_nsdd_298_opsec];
[@official_nist_zero_trust_sp_800_207];
[@public_council_europe_information_disorder];
[@scholarly_terp_breuer_2022_disarm]. The map therefore routes AI, OPSEC, and
cognitive-security claims into source-backed classroom artifacts while blocking
autonomous strategic-judgment claims, manipulation guidance, live-targeting
workflows, and unsupported efficacy claims.

## Analysis validation protocol: claim classes, evidence packets, and failure modes {#sec:analysis-validation-protocol}

The manuscript now treats analysis validation as a reader-facing method, not a
private build habit. Each major claim class must name the evidence packet that
would make it reviewable, the validation question a reviewer should ask, and
the failure mode that would force warning or remediation. The analysis
validation matrix [@fig:ageint-analysis-validation-matrix] is the compact visual
form of that protocol: design guidance needs a source family and caveat;
empirical or evaluation claims need a study, metric, or benchmark; governance
claims need law, standard, or rights-impact support; figure claims need registry
text, rendered pixels, and link-safe PDF output; artifact-readiness claims need
fresh builds and current audits; reviewer dispositions need a task ledger and
negative control.

The claim-calibration verifier adds the machine-checkable edge to that protocol
[@fig:ageint-claim-calibration-and-visual-semantics]. Artifact telemetry such as
citation counts, figure counts, page counts, link counts, and validator pass
states is useful readiness evidence, but it is not a statistical result,
learning-outcome estimate, operational-performance benchmark, or universal
safety claim. The audit therefore fails unsupported proof-language,
measured-performance claims, p-value or significance language, and decorative
formalisms without direct support and limitation text, while allowing explicit
boundary language and misconception checks that warn the reader what a source
cannot establish.

| Claim class | Validation question | Required evidence | Failure mode |
|---|---|---|---|
| Design guidance | Is the claim framed as proposed guidance rather than measured performance? | source-family support, caveat, and bounded conclusion | architecture prose is promoted into empirical proof |
| Empirical or evaluation claim | Does a cited study, metric, benchmark, or evaluation source directly support the claim? | method source, limitation note, and refresh trigger | measured language appears without direct evaluation evidence |
| Governance or rights claim | Which law, standard, public guidance, or rights-impact source constrains the advice? | source lane, affected group, owner, residual risk | compliance language appears as unsupported assurance |
| Figure or visualization claim | Does the visual carry readable text, alt text, provenance, and an inspectable source section? | registry row, PNG metadata, caption, long description | a figure works only as decoration or inaccessible evidence |
| Artifact readiness claim | Are manuscript, citations, figures, references, and PDF links from the same rebuild? | artifact-evidence manifest, rendered-reference audit, PDF audit | stale output or Markdown-file links certify as ready |
| Reviewer disposition | What would make this row pass, warn, fail, or reopen? | negative control, closure evidence, task owner | a green check hides the decision rule |

## Consolidated glossary and index: terms, audit surfaces, and reader routing {#sec:consolidated-glossary-and-index}

Use this compact index to route common terms to the right audit surface before
reading a chapter in detail.

| Term | Working meaning | Primary audit surface |
|---|---|---|
| Source lane | The provenance, source tier, and refresh context that govern a claim. | [@sec:source-lane-map] and [@sec:bibliography_atlas] |
| Source tier | The evidence role assigned to a source: official, standards, scholarly, practitioner, vendor, historical, or source-guide context. | [@sec:research-anchor-atlas] and source annotations |
| Synthetic Analytic Tradecraft | The controlled use of synthetic fixtures and bounded agent support to make analytic reasoning, evidence, uncertainty, dissent, and review gates inspectable. | [@sec:synthetic-analytic-tradecraft-thesis] and [@fig:ageint-synthetic-tradecraft-method-contract] |
| Analysis validation | The review protocol that maps claim class, validation question, evidence packet, failure mode, and disposition before a claim can be treated as ready. | [@sec:analysis-validation-protocol] and [@fig:ageint-analysis-validation-matrix] |
| Claim ledger | A reviewable record of claim, evidence, caveat, confidence, and owner. | Research governance and [@sec:capstone-workflow] |
| Safe substitution | A replacement of unsafe operational action with synthetic, public, tabletop, or governance work. | [@sec:safe-substitution-matrix] |
| Reviewer gate | A named human approval or challenge point before reuse, presentation, or tool execution. | Assessment review and assurance rows |
| Figure registry | The reproducible map from figure label to generated asset, caption, and source section. | [@sec:orientation-figures-and-course-links] |

## Intelligence research profiles: domain lanes, source roles, and profile routing {#sec:intelligence-research-profiles}

{{INTELLIGENCE_PROFILE_ROWS}}

## Intelligence practice lenses: artifact expectations, safety checks, and review questions {#sec:intelligence-practice-lenses}

{{INTELLIGENCE_PRACTICE_LENS_ROWS}}

## Research anchor atlas: curated sources, lanes, tiers, and claim scope {#sec:research-anchor-atlas}

{{INTELLIGENCE_RESEARCH_ROWS}}

## Source lane map: provenance lanes, support strength, and refresh context {#sec:source-lane-map}

{{INTELLIGENCE_SOURCE_LANE_ROWS}}

## Safe substitution matrix: defensive artifacts for risky inherited motifs {#sec:safe-substitution-matrix}

{{SAFE_SUBSTITUTION_ROWS}}

## Capstone workflow: phase sequence, artifacts, and reviewer gates {#sec:capstone-workflow}

{{CAPSTONE_SCAFFOLD_ROWS}}

## Capstone model-answer exemplars: strong evidence packets and revision triggers {#sec:capstone-model-answer-exemplars}

These exemplars show the expected shape of a strong answer without prescribing
a single conclusion. Use them as answer-key patterns for selected capstone
reviews.

| Capstone pattern | Model-answer evidence | What earns revision |
|---|---|---|
| Source-quality packet | Names the `ageintNNN` source key, source lane, direct evidence, caveat, uncertainty, and refresh trigger. | Claim cites a summary, omits the source key, or hides uncertainty. |
| Safe-lab packet | States the learning question, allowed inputs, excluded actions, tool allowlist, stop condition, and reviewer gate. | Uses private data, live targets, credentialed access, or an unreviewed tool path. |
| Assurance packet | Connects rubric score, rights impact, accessibility check, remediation owner, and debrief handoff. | Treats the score as proof, omits affected users, or leaves no owner for retest. |

## Accessibility and UDL review: learner access, modality checks, and accommodation evidence {#sec:accessibility-and-udl-review}

{{ACCESSIBILITY_REVIEW_ROWS}}

## Procurement and vendor oversight: tool governance, revocation, and vendor evidence {#sec:procurement-and-vendor-oversight}

{{PROCUREMENT_OVERSIGHT_ROWS}}

## HRIA and DPIA worksheet: rights impact, privacy review, and residual risk {#sec:hria-and-dpia-worksheet}

{{HRIA_DPIA_WORKSHEET_ROWS}}

## Data lineage registry: source identity, transformations, retention, and review {#sec:data-lineage-registry}

{{DATA_LINEAGE_REGISTRY_ROWS}}

## Assessment integrity protocol: declared agent use, grading evidence, and human judgment {#sec:assessment-integrity-protocol}

{{ASSESSMENT_INTEGRITY_ROWS}}

## Agent incident response drill: pause, revoke, preserve, recover, and debrief {#sec:agent-incident-response-drill}

{{AGENT_INCIDENT_RESPONSE_ROWS}}

## Role-based competency map: responsibilities, evidence owners, and assurance roles {#sec:role-based-competency-map}

{{ROLE_COMPETENCY_ROWS}}

## Adversarial assurance cycle: challenge rows, remediation owners, and retest evidence {#sec:adversarial-assurance-cycle}

{{ADVERSARIAL_ASSURANCE_ROWS}}

## Model and dataset documentation card: intended use, provenance, caveats, and lifecycle {#sec:model-and-dataset-documentation-card}

{{MODEL_DATASET_CARD_ROWS}}

## Transparency and communication notice: purpose, safeguards, human review, and limits {#sec:transparency-and-communication-notice}

{{TRANSPARENCY_NOTICE_ROWS}}

## Records retention and audit trail: owners, retention rules, and deletion conditions {#sec:records-retention-and-audit-trail}

{{RETENTION_AUDIT_ROWS}}

## Release and change-control gate: reuse approval, rollback, and change evidence {#sec:release-and-change-control-gate}

{{RELEASE_CHANGE_CONTROL_ROWS}}

## Risk exception and acceptance memo: residual risk, owner approval, and review clock {#sec:risk-exception-and-acceptance-memo}

{{RISK_EXCEPTION_ROWS}}

## Learner support and accommodation plan: support rows, access barriers, and escalation {#sec:learner-support-and-accommodation-plan}

{{LEARNER_SUPPORT_ROWS}}

## Instructor question bank: prompts, evidence checks, and misconception probes {#sec:instructor-question-bank}

{{QUESTION_BANK_ROWS}}

## Remediation backlog: issue owners, retest evidence, and closure boundaries {#sec:remediation-backlog}

{{REMEDIATION_BACKLOG_ROWS}}

## Scholarship and governance stance: source posture, claim limits, and public-readiness boundary {#sec:scholarship-and-governance-stance}

AGEINT treats agentic intelligence as a governed socio-technical practice, not
as a bag of prompts or autonomous tricks. The curriculum therefore keeps AI
agent evaluation, identity, authorization, secure tool use, structured analytic
tradecraft, cognitive security, OSINT/GEOINT integrity, and ICS/OT safety in
one source-backed frame. Each source anchor has a curriculum role, a domain,
and a provenance type so readers can distinguish law, standards, official
guidance, public-domain historical material, scholarly synthesis, and weaker
practitioner or vendor context. Unless a section cites an empirical study or
evaluation source for a narrower point, AGEINT language should be read as
proposed design guidance and an assurance framework rather than measured
performance evidence. Technical and theoretical analogies, including
active-inference material, remain bounded by their direct domain sources and do
not become deployment evidence without separate evaluation support.

The same stance now has a machine-checkable extension. Citation presence is
necessary but not sufficient for AGEINT scholarship, so the generated manuscript
is checked for source-family mix, uncited claim-bearing sections, thin
claim-bearing support, and sections whose support comes from only one broad
family. The audit distinguishes hard failures from review warnings: a
claim-bearing overview, lesson, worked example, architecture source section,
research-governance section, assessment review, or unit introduction with zero
or one unique citation fails the current artifact evidence; a section with
multiple citations from one source family is reported as a review target for
future triangulation. The control surface is summarized in
[@fig:ageint-scholarship-triangulation-map], and the machine-readable companion
report is written to `output/reports/scholarship_quality.json` during the
current-evidence pass. This keeps source-guide inheritance visible while still
preferring official, standards, law/policy, public-domain, and scholarly anchors
whenever a section makes a stronger governance, technical, or empirical claim
[@scholarly_rethlefsen_2021_prisma_s]; [@official_nist_ai_rmf];
[@official_nist_ai_600_1].

Claim calibration sits beside that scholarship audit. The source-strength layer
classifies source-guide rows and curated anchors by whether they can carry a
bounded claim directly or only provide context. Weak source-guide context,
vendor/practitioner commentary, social/video rows, and mirror/copy rows cannot
alone support empirical performance, statistical, governance-authority, safety,
or formalism claims. The current report is written to
`output/reports/claim_calibration.json` and `.md`, and the unified artifact
evidence manifest exposes the result as `claim_calibration_ok`.

Analysis validation adds the reader-facing disposition layer. The compact matrix
in [@fig:ageint-analysis-validation-matrix] turns claim classes into questions:
whether design guidance is bounded, whether empirical language is directly
evaluated, whether governance advice has a legal or standards anchor, whether a
figure is accessible and provenance-backed, whether the PDF and manuscript came
from the same rebuild, and whether a reviewer can reproduce the pass/warn/fail
decision. This is why the artifact-evidence manifest records both positive
counts and false-certification controls.

## Verifier-first artifact evidence: build freshness, audits, and negative controls {#sec:verifier-first-artifact-evidence}

AGEINT uses the RedTeam rule that a green validator is evidence only after the
validator has been challenged. The artifact-evidence control loop in
[@fig:ageint-artifact-evidence-control-loop] binds source-owned curriculum
inputs, generated manuscript sections, citation inventories, figure metadata,
PDF annotations, and current evidence reports into one falsifiable chain. This
keeps scholarship, visual assets, and render validation in the same audit
surface: a stale PDF, a local Markdown-file link, an uncovered source section,
or a figure-registry mismatch must fail the evidence manifest before a
maintainer can treat the render as ready. The same stance follows the
evaluation and red-team assurance guidance already encoded in the bibliography
atlas: adversarial testing is a scoped assurance method, not proof of universal
safety or permission to run live operations
[@official_cisa_ai_red_teaming_tev];
[@official_nist_aria_pilot_evaluation_report];
[@official_nist_ai_600_1_generative_ai_profile].

## Orientation figures and course links: visual evidence, source flow, and navigation {#sec:orientation-figures-and-course-links}

{{VISUAL_SYNTHESIS}}

## AGEINT pattern library: design-pattern rows, safe substitutions, and source identity {#sec:ageint-pattern-library}

{{AGEINT_PATTERN_ROWS}}

## Safety rail: authorized, synthetic, defensive, and non-operational boundaries {#sec:safety-rail}

All exercises remain educational, lawful, defensive, historical, synthetic,
and non-operational. Modules may discuss intelligence, cyber, influence,
counterintelligence, and industrial systems as objects of study, but they do
not provide instructions for unauthorized collection, evasion, exploitation,
manipulation, covert targeting, or real-world harm.
