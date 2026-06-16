# Research Spine: verified additions, source lanes, and encoded evidence

AGEINT uses Perplexity as a discovery and second-opinion lane, not as a cited authority. Final manuscript citations point to direct official, standards, or scholarly URLs encoded in `data/research_anchors/`, `src/intelligence_content/`, and `src/manuscript_variables/`.

The current research profiles cover:

- Analytic tradecraft and source integrity (ODNI [ICD 203 Analytic Standards](https://www.dni.gov/files/documents/ICD/ICD-203.pdf): five analytic standards plus nine tradecraft standards — sourcing, uncertainty, distinctions, alternatives, relevance, argumentation, consistency, accuracy, visuals).
- Governed intelligence cycle and dissemination architecture.
- Operator productivity and cognitive performance (GTD external memory, NASA-TLX workload review, flow preconditions).
- AI ethics, data governance, and civil-liberties review.
- Agentic AI governance and tool security.
- Open-source and geospatial intelligence integrity.
- Collection management and multi-INT requirements discipline.
- Financial intelligence and economic-security due diligence.
- Counterintelligence and source-integrity defense.
- Cognitive security and influence resilience.
- Historical and declassified intelligence services.
- Cyber threat intelligence, incident response, and supply-chain defense.
- ICS/OT cyber-physical defense and tabletop readiness.
- Legal, ethical, and oversight architecture.
- AI conformity/compliance.
- Education and assessment.
- Public-sector agentic AI.
- Cross-border data and data spaces.
- Human-rights governance.
- Agent interoperability standards.
- Workforce governance.
- Model and data provenance.
- Accessibility and digital inclusion.
- Procurement/vendor governance.
- Agent incident response.
- AI red-team assurance.
- Public-sector transparency.
- Rights-impact privacy review.
- Model card reporting.
- Dataset documentation.
- Algorithmic transparency reporting.
- Records retention/auditability.
- Secure release/change control.
- Risk exception governance.
- Learner support/accommodations.
- Assurance evaluation evidence.
- Procurement performance monitoring.

The practice-lens layer sits underneath the source-profile layer. It gives every
part, chapter, and runtime subsection a reusable design question, expected
evidence artifact, validation rule, handoff contract, and safety check. This is
the fractal content contract for AGEINT: the same authority, evidence, tool,
output, and safety logic appears at curriculum, module, and subsection scale.

When adding intelligence content:

- Add new official or scholarly anchors as structured entries in `src/intelligence_content/`.
- Attach anchors to a reusable profile instead of writing chapter-specific prose.
- Cite sources with Pandoc keys generated into `output/manuscript/references-*.bib`.
- Keep Perplexity notes out of the bibliography unless the cited source is a directly verified external publication.
- Preserve the non-operational boundary: no live targeting, exploitation, evasion, manipulation, unsafe cyber-physical action, or unauthorized collection.

The May 2026 research pass adds IC-cycle governance, CAPCO dissemination
marking, IC AI ethics, ICD 505 AI governance, ICD 504 data management, PCLOB
oversight, federal data strategy, declassified historical-source practice, and
FININT/economic-security anchors. These additions remain source-profile entries:
generated chapters select them through reusable profiles and practice lenses
rather than through hand-authored chapter prose.

The v2, deep-expansion, evidence-package, Data Cards, local auto-link, US
IC source-pack, literature-integration, and SAT-integration hardening passes add source-lane metadata to curated anchors and
expand the curated anchor set to 462 official, standards,
public-domain, scholarly, and professional sources. New lanes cover AI conformity/compliance,
education and assessment, public-sector agentic AI, cross-border data/data
spaces, human-rights governance, agent interoperability standards, workforce
governance, model/data provenance, accessibility and digital inclusion,
procurement/vendor governance, agent incident response, AI red-team assurance,
public-sector transparency, rights-impact privacy review, model card reporting,
dataset documentation, algorithmic transparency reporting, records
retention/auditability, secure release/change control, risk exception
governance, learner support/accommodations, assurance evaluation evidence, and
procurement performance monitoring.

Primary research lanes currently include ODNI analytic standards and sourcing
directives, ODNI ICD 204 and the National Intelligence Priorities Framework,
Intelligence.gov's intelligence-cycle overview, ICD 504 data management, ICD
505 AI governance, the CAPCO Register, PCLOB oversight reports, the Federal
Data Strategy, JP 2-0 joint-intelligence doctrine, Army ATP 2-33.4 analytic
doctrine, CIA and DIA structured analytic technique primers, Heuer's
analytic-cognition work, the IC OSINT Strategy, NGA strategy, the National
Counterintelligence Strategy, Executive Order 12333, NSA FISA oversight
material, IC AI ethics principles and framework, NIST AI RMF and SSDF, NIST
agent identity/authorization, UK AISI agent-evaluation guidance, IMDA and Five
Eyes agentic-AI governance guidance, NSA MCP and AI-in-OT guidance, OWASP LLM
and agentic-application security guidance, MITRE ATLAS, NIST CSF 2.0, NIST SP
800-150, NIST SP 800-160, NIST SP 800-61 Rev. 3, NIST SP 800-161, CISA
ICS/tabletop guidance, NIST SP 800-82 and SP 800-84, MITRE ATT&CK for ICS,
ISA/IEC 62443, CIA CSI, NSA historical releases, NRO declassified programs,
NARA CIA records, FinCEN advisories, OFAC sanctions programs, FATF
Recommendations, BIS export enforcement, NATO/CISA influence-operation
guidance, GCSP cognitive-security policy scholarship, the EU AI Act, European
Commission AI Office/GPAI/Data Act/Data Governance Act/data-space sources,
UNESCO AI ethics and education guidance, OHCHR digital-rights and privacy
materials, World Bank GovTech AI resources, ILO and OECD work sources, W3C
WoT/VC/DID/PROV/DCAT/Data-on-the-Web recommendations, OpenAPI, DataCite, C2PA
provenance specifications, Model Context Protocol specification and security
best-practices pages, Agent2Agent protocol documentation, MITRE D3FEND, OASIS
CSAF, CycloneDX, SPDX, NIST OSCAL, SLSA, in-toto, Sigstore, W3C WCAG, CAST UDL, DOJ ADA Title II accessibility
guidance, EDPB DPIA materials, OECD public procurement and open government
legal instruments, the Open Contracting Data Standard, NIST SP 800-61 Rev. 3,
ENISA AI cybersecurity guidance, NIST AI security/resilience resources, and W3C
Verifiable Credential Data Integrity.
The evidence-package source family adds model cards, datasheets for datasets,
Data Cards for purposeful dataset documentation,
the UK Algorithmic Transparency Recording Standard, NIST SP 800-218A, the U.S.
Access Board Revised 508 Standards, NIST ARIA, NARA AI use-case inventory, OMB
M-25-21, OMB M-25-22, NIST AI 600-1, and the NIST AI Agent Standards
Initiative. The 2026-06-06 internet-citation pass adds NIST AI 100-4
synthetic-content transparency, NIST AI 100-5 global AI standards engagement,
NIST AI 800-1 misuse-risk draft guidance, the International AI Safety Report
2026, MCP specification/security pages, the A2A protocol, NCSC secure-AI
system-development guidance, MITRE D3FEND, OASIS CSAF, CycloneDX, SPDX, NIST
OSCAL, SLSA, in-toto, and Sigstore. The May 22, 2026 refresh adds CISA AI red teaming/TEVV, CISA AI
data-security best practices, NIST's critical-infrastructure AI RMF profile
concept note, OECD public-sector AI governance, and the NARA 2025 AI compliance
plan.
The May 24, 2026 refresh adds directly verified official anchors for Canada's
agentic-AI guide, Algorithmic Impact Assessment, AI Register, and public-service
AI strategy; OECD AI risks/incidents and AI incident-reporting framework; the UN
Global Digital Compact; NIST Dioptra; and CISA secure AI deployment,
Secure-by-Demand OT procurement, OT asset-inventory, and definitive OT
architecture guidance. These anchors support bounded autonomy, recoverability,
public AI registers, incident reporting, OT evidence, and source-refresh
governance without adding vendor or blog citations.

The June 15, 2026 literature-integration pass adds verified sources for
synthetic intelligence, LLM support to national-security analysis, synthetic
reality and deepfake provenance, adversarial ML, AI incident regimes, ACH and
confirmation-bias evidence, OPSEC doctrine, OSINT leakage, DISARM and
disinformation analysis, cognitive warfare, social-engineering cognition, and
active-inference theory. The two pasted literature reviews remain discovery
inventories only; cited manuscript support comes from directly verified source
URLs encoded in `data/research_anchors/intelligence-anchors-305-340.jsonl`.

The June 15, 2026 SAT literature-integration pass adds verified sources for
analytic pathologies, groupthink, SAT adoption, SAT evidence evaluation, ACH
experiments and critiques, decision science, forecasting calibration, Delphi,
premortem, morphological analysis, Alternative Futures Analysis, official
IARPA ACE/REASON programs, official FOI/JIPS method guides, Senate Iraq WMD
postmortem evidence, and SAT pedagogy texts. The attached SAT report remains a
discovery inventory only; cited manuscript support comes from directly verified
source URLs encoded in `data/research_anchors/intelligence-anchors-341-367.jsonl`.

Generated chapters now use a compact reader-facing architecture instead of a
flat repeated scaffold. `src/manuscript_manifest/` keeps source-guide H1
titles stable, converts pseudo-headings such as `V2 source-lane extension:`,
`Deep expansion:`, and `Evidence-package expansion:` into polished visible
titles, and preserves source-guide provenance in runtime/source-map tables.
Improve section titles and body composition in the generator, templates, and
source-profile anchors, never by editing `output/manuscript`.

The governing rule is evidence separation. Source-guide `ageintNNN` citations
preserve the inherited bibliography; curated anchors provide official,
standards, or scholarly grounding for generated synthesis; Perplexity remains
only a discovery trail. A new anchor should include title, authoring
organization, year, direct URL, source type, domain, and a short curriculum-use
note. New v2 anchors should also include source lane, source tier, checked date,
verification method, claim scope, refresh cadence, and refresh trigger. New
official US IC anchors also require `source_agency` and `source_pack`, and the
named pack must route deterministically through `data/agency_source_packs.yaml`.

Do not cite broad web summaries, vendor marketing, uncited Perplexity prose, or
unverified claims. If a source is volatile or current, verify the direct URL
again before changing the anchor year, title, or note.

## May 2026 full-section content pass: verified encode-only source expansion

Perplexity (`llm -m sonar-pro`) is used as a discovery and second-opinion lane
for current source coverage. The May 24, 2026 pass checked agentic-AI
governance, AI red-team assurance, public-sector transparency, privacy and
rights-impact review, model/dataset documentation, procurement/vendor
governance, records retention, secure release/change control, learner support,
and assurance-evaluation evidence. Vendor/blog results from discovery are not
encoded. Only verified official, standards-body, public-domain, or scholarly
pages are admitted to `data/research_anchors/`, `src/intelligence_content/`,
and generated BibTeX:

| Batch | Domain | Verified encode targets |
| --- | --- | --- |
| A | Analytic tradecraft | [ICD 203 PDF](https://www.dni.gov/files/documents/ICD/ICD-203.pdf) — ACH, KAC, devil's advocacy, nine-tradecraft routes |
| B | Cognitive / epistemic security | GCSP cognitive-security framing, epistemic security, prebunking/inoculation routes |
| C | ICS / ATT&CK ICS | MITRE ATT&CK for ICS, NERC CIP, Stuxnet/Triton tabletop routes |
| D | OPSEC / CI tradecraft | OPSEC five-step, compartmentation, cover/legend governance routes |
| E | FININT / sanctions | FinCEN advisories, FATF typologies, beneficial-ownership routes |
| F | Agentic AI governance | NIST AI RMF, NIST AI 600-1, OECD agentic-AI routes |
| G | Public-sector agentic AI | Government of Canada agentic-AI guide, AI Strategy 2025-2027, and AI Register |
| H | Rights and incident governance | Canada Algorithmic Impact Assessment, OECD AI risks/incidents, and OECD incident-reporting framework |
| I | Assurance and release control | NIST Dioptra, CISA secure AI deployment, CISA AI data-security best practices, and CISA AI red teaming/TEVV |
| J | OT procurement and auditability | CISA Secure by Demand OT procurement, OT asset-inventory guidance, and definitive OT architecture guidance |
| K | Current AI safety, misuse, interoperability, and evaluation | NIST AI 100-4/100-5/800-1/800-2, International AI Safety Report 2026, MCP specification/security, A2A protocol, OECD agentic-AI foundations, NSA MCP security design, and NCSC secure-AI-development guidance |
| L | Supply-chain evidence and defensive-control provenance | MITRE D3FEND, OASIS CSAF, CycloneDX, SPDX, NIST OSCAL, SLSA, in-toto, and Sigstore |
| M | Analytic tradecraft, warning, and failure evidence | CIA/Kent professionalization, ICD 203, IRTPA, 9/11 and WMD postmortems, NATO alternative analysis, warning-intelligence sources, SAT empirical evaluation, forecasting calibration, and intelligence-failure theory |
| N | Official US IC source-pack spine | CIA analytic uncertainty and professional literature, DIA defense OSINT governance, ODNI directives and tearlines, Intelligence.gov transparency pages, NSA agentic-AI and cyber guidance, NGA doctrine/data strategy, NRO history, and FBI counterintelligence context |

Measured source-layer coverage after the current refresh: **462** curated
research anchors and **125** keyword concept routes. The exact project test and
coverage result is intentionally not hard-coded here; run
`uv run pytest tests/ --cov=src --cov-fail-under=90` for the current gate.

The 2026-06-11 analytic-tradecraft shard
(`data/research_anchors/intelligence-anchors-233-248.jsonl`) adds CIA/Kent,
warning-intelligence, post-9/11 and Iraq WMD postmortem, NATO
alternative-analysis, SAT evaluation, forecasting-calibration, and
failure-theory sources. These are routed as curriculum anchors for Chapters
41-42 and for the new source-backed Mermaid boundary diagrams; they do not
license universal claims that SATs cure bias or eliminate intelligence failure.

The 2026-06-14 official US IC shard
(`data/research_anchors/intelligence-anchors-249-304.jsonl`) adds 56 directly
verified public CIA, DIA, ODNI, Intelligence.gov, NSA, NGA, FBI, and NRO
anchors. These sources are routed through named source packs for analytic
uncertainty, intelligence professional literature, defense OSINT governance,
disclosure/tearlines, privacy/oversight, current threat context, cyber/GEOINT
governance, and declassified history. CIA Studies/CSI professional literature is
encoded as official public professional context, not automatically as current
agency policy or AGEINT benchmark evidence.

The 2026-06-15 literature-integration shard
(`data/research_anchors/intelligence-anchors-305-340.jsonl`) adds 36 directly
verified scholarly, official, and public-domain anchors from the attached
literature inventories after dedupe against the existing source layer. They are
routed through analytic tradecraft, agentic AI governance, OSINT/GEOINT,
collection management, cognitive influence security, cognitive active inference,
cyber threat intelligence, and legal oversight profiles. Bounded support remains
explicit: no autonomous strategic-judgment claim, OPSEC playbook, manipulation
guidance, live-targeting workflow, or unsupported cognitive-security efficacy
claim is licensed by the new sources.

The 2026-06-15 SAT literature-integration shard
(`data/research_anchors/intelligence-anchors-341-367.jsonl`) adds 27 directly
verified scholarly, official, public, and publisher-backed SAT sources after
dedupe against existing Heuer, Heuer/Pherson, CIA tradecraft, ICD 203, RAND,
Dhami, Mandel/Tetlock, Barnes/Mandel, Ard, and related tradecraft anchors. They
are routed through analytic tradecraft, SAT evidence, analytic cognition,
forecasting calibration, warning, postmortem, method-pedagogy, and
agentic-analytic-assistance lanes. Bounded support remains explicit: SATs are
reasoning-visibility, diagnostic, and review scaffolds; the sources do not
license autonomous strategic judgment, operational targeting, or claims that
SATs are proven universal debiasing tools.

The 2026-06-16 citation-expansion tranche reviews 106 proposed citation
headings from the pasted import document. It treats that file as a candidate
set, not paste-ready manuscript prose: 102 records have full citation fields,
95 are accepted after direct-source review, deduplication, weak-host
replacement, and tier/key normalization, and 11 are deferred in
[`citation_expansion_2026_06_16.md`](citation_expansion_2026_06_16.md). The
accepted shards are
`data/research_anchors/intelligence-anchors-368-417.jsonl` and
`data/research_anchors/intelligence-anchors-418-462.jsonl`. They route through
`data/research_source_packs.yaml` rather than the agency-source pack file, so
non-agency scholarly, professional, public-domain, and international-body
sources enrich chapter evidence while the official US IC audit remains scoped
to the 56-anchor agency tranche.

The 2026-06-12 verifier-hardening pass refreshes two older URL metadata rows:
OASIS CSAF now points at the canonical OASIS Standard HTML page, and the
International AI Safety Report 2026 anchor points at the official report
landing page, with the PDF and arXiv record treated as secondary evidence.

The 2026-06-12 section/reference auto-link, profile-anchor, and Synthetic
Analytic Tradecraft orientation passes keep the same source corpus while turning
the generated navigation and bibliography surfaces into real links and making
the early reader contract explicit: orientation sections carry stable labels,
curriculum-map rows link each part intro and module-map figure, and research-anchor /
bibliography / source-refresh key tables use Pandoc citations rather than
literal `@key` text. The
verifier-first artifact-evidence manifest now reports 330 generated Markdown files,
16,057 generated Markdown citation occurrences, 723 source sections, and 0
zero-citation source sections. The same local artifact manifest confirms 173
registered figures plus one non-numbered cover-art PNG, with substantial
captions, alt text, long descriptions,
official accessibility guidance metadata, embedded PNG accessibility/provenance
and visual-semantics metadata, machine-readable visual-quality audit metadata, a 1,854-page combined
PDF, 6,289 URI links, 0 Markdown-file link targets in PDF annotations, and passing
`source_metadata_ok` over 472 metadata rows plus `agency_source_coverage_ok` for
the official US IC source-pack tranche. The bibliography-atlas
source-section coverage output now uses explicit coverage-anchor prose rather
than generic evidence prose, and its citation rows use compact numeric columns
with wider descriptive/citation-link columns for PDF readability.
The scholarship-quality audit additionally reports 0 uncited claim-bearing
generated files, 0 thin claim-bearing generated files, and six single-source-family
claim-bearing review-warning rows. Topic lessons, worked examples, source-canon
sections, and review-checklist sections now carry profile-specific external
triangulation anchors while preserving the locked source-guide citation spine.
The follow-on SAT method-contract check makes the early abstract/orientation
framing testable: the generated manuscript must keep the Synthetic Analytic
Tradecraft thesis, the source-family triangulation language, the negative-control
testing language, and the registry-backed
`fig:ageint-synthetic-tradecraft-method-contract` reference. The analysis-validation
check likewise requires the abstract figure reference, the
`sec:analysis-validation-protocol` orientation section, claim-class validation
questions, failure-mode language, and the
`fig:ageint-analysis-validation-matrix` reference. If those terms are removed
while citation counts remain high, `scripts/audit_scholarship_quality.py` and
the unified artifact-evidence manifest must fail.
The RedTeam family-coverage follow-up also requires every claim-bearing
generated manuscript family to map to a canonical analysis-validation lane,
evidence signal, and failure signal before it can be treated as current.

The 2026-06-13 metadata-verifier hardening pass adds no new external citations
and does not change `checked_as_of` dates. It makes the source metadata explicit
for 119 rows that previously depended on fallback semantics: 109 legacy
intelligence anchors now carry `source_lane` from their existing `domain` and
`source_tier` from their existing `source_type`, and 10 source-quality support
anchors use `source_quality_spine` / `source_quality_anchor`. The new
`source_metadata_ok` artifact-evidence check fails on blank lane/tier fields,
fallback-dependent rows, or source-quality semantic mismatches. The same pass
raised the then-current figure registry to 169 with the source-metadata integrity visual.

The 2026-06-14 claim-calibration and visual-semantics pass adds no new external
citations and does not change `checked_as_of` dates. It adds
`src/claim_calibration.py`, `scripts/audit_claim_calibration.py`, source-support
strength classification for source-guide and curated-anchor keys, registry
schema `1.5` visual-semantics fields, and the
`fig:ageint-claim-calibration-and-visual-semantics` control-map figure. The
unified artifact-evidence manifest exposes `claim_calibration_ok`, so
unsupported proof-language, p-value language, measured-performance claims,
decorative formalisms, or weak-source-only high-risk claims fail even when
ordinary citation counts, PDF links, and figure rendering remain green.

The 2026-06-13 cover, abstract, and TOC hardening pass also adds no new
external citations. It moves the former graphical-abstract role into
orientation support, gives the PDF title page deterministic non-numbered cover
art, and keeps the abstract as one plaintext Synthetic Analytic Tradecraft
contract. The follow-up graphical-abstract/TOC-title pass makes
`fig:ageint-graphical-abstract` a Python-rendered Synthetic Tradecraft System
Atlas and changes module H2 entries into chapter-specific orientation,
practice-studio, evidence-contract, governance-boundary, and assessment-route
landmarks. The PDF TOC intentionally exposes H1/H2 entries only; deeper
generated scaffolds remain in the body and generated HTML for local navigation.

## 2026-05-22 cognitive-security synthesis pass: verified encode-only anchors

This pass added 14 directly verified anchors, raising the curated set from 172
to 186, and 7 Mermaid methods diagrams synthesizing them. As with every
refresh, vendor and blog discovery results are not encoded — only official,
standards-body, or scholarly pages are admitted.

| Anchor | Source | Role in synthesis |
| --- | --- | --- |
| `scholarly_ccdcoe_cognitive_warfare_reconception` | NATO CCDCOE | Cognitive warfare as a contest over interpretive structures and epistemic standards |
| `official_darpa_intrinsic_cognitive_security` | DARPA | Intrinsic cognitive security framing |
| `official_csa_cdr_framework` | Cloud Security Alliance | Cognitive Degradation/Recovery six-stage cascade |
| `official_csa_maestro_threat_modeling` | Cloud Security Alliance | MAESTRO seven-layer agentic threat model |
| `official_csa_securing_autonomous_ai_agents` | Cloud Security Alliance | Securing autonomous agents controls |
| `official_csa_nist_ai_agent_red_teaming_standards` | CSA / NIST | Agent red-teaming standards |
| `official_owasp_agentic_ai_threats_mitigations` | OWASP | Agentic AI threats-and-mitigations reference |
| `scholarly_deepmind_epistemic_agent_trust` | Google DeepMind | Epistemic agent trust |
| `scholarly_anthropic_building_effective_agents` | Anthropic | Effective-agent reliability patterns |
| `scholarly_prompt_infection_multi_agent` | Preprint | Multi-agent prompt-infection threat |
| `scholarly_systems_security_agentic_computing` | Preprint | Systems-security framing for agentic computing |
| `scholarly_agentic_ai_security_survey` | Scholarly survey | Agentic AI security landscape |
| `scholarly_mandel_tetlock_judgment_correctives` | Mandel & Tetlock | Analytic-debiasing / judgment correctives |
| `official_unu_macau_agentic_ai_boundaries` | UNU Macau | Bounded-agency policy analysis |

Two synthesis themes organize this material. **Epistemic coherence** treats
trust, identity, and analytic standards as the systemic invariants that
cognitive attacks degrade; the CDR cascade, decoherence/CDR isomorphism, and
unified epistemic-coherence stack figures render this as a single defensible
spine. The **tradecraft–reliability bridge** maps classical analytic tradecraft
(ICD 203 standards, Mandel-Tetlock correctives) onto agentic-system reliability
engineering (MAESTRO layers, SRE-for-agents circuit breakers, HRO governance),
showing the same failure-and-recovery logic at human and machine scale.
