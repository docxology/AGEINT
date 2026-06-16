# Source Refresh Ledger: locked identities, curated metadata, and refresh triggers

AGEINT v2 uses a source-lane ledger for curated anchors and an identity lock for
the original source-guide references.

For the step-by-step authoring, counting, rebuild, and validation workflow, use
[`citation_workflow.md`](citation_workflow.md).

## Locked range: preserved source-guide identities and append-only additions

- `ageint001` through `ageint231` are locked in `data/source_identity/`.
- Existing locked keys, titles, and URLs must remain stable unless the source
  identity actually changes and the lock is intentionally regenerated.
- New source-guide references are append-only and currently span `ageint232`
  through `ageint312`.

## Curated anchor metadata: checked dates, cadences, triggers, and caveats

Every curated anchor in `src/intelligence_content/` should carry:

- `source_lane`
- `source_tier`
- `checked_as_of`
- `verification_method`
- `claim_scope`
- `refresh_cadence`
- `refresh_trigger`
- `stakeholder_role`
- `assurance_use`
- `rights_dimension`

Perplexity may suggest sources, but final anchors must be verified directly
from official, standards-body, public-domain, or scholarly URLs before being
encoded.

The 2026-06-13 metadata-verifier hardening pass closes the remaining fallback
dependency without changing source identities or `checked_as_of` dates. It makes
119 blank lane/tier rows explicit: 109 legacy intelligence anchors now use their
existing `domain` as `source_lane` and existing `source_type` as `source_tier`,
while the 10 rows in `data/research_anchors/source-quality-anchors.jsonl` use
`source_quality_spine` / `source_quality_anchor`. Run
`uv run python scripts/audit_source_metadata.py --write --format markdown` to
write `output/reports/source_metadata.{json,md}`; the unified artifact evidence
manifest exposes the same gate as `source_metadata_ok` and fails on any blank
lane/tier row or support-anchor semantic mismatch.

The May 24, 2026 source refresh is encoded in
`data/research_anchors/intelligence-anchors-161-172.jsonl`. It adds official
Canada, OECD, UN, NIST, and CISA anchors for bounded agentic AI governance,
algorithmic impact review, public AI registers, AI incident reporting, NIST
Dioptra assurance, secure AI deployment, OT procurement, OT asset inventory,
and definitive OT architecture evidence. These rows use
`checked_as_of: "2026-05-24"` and the same direct-verification standard as the
May 21 and May 22 shards.

The 2026-06-14 publication-readiness pass adds a refresh due-date oracle without
changing any `checked_as_of` dates. Run
`uv run python scripts/audit_source_refresh_due.py --write --format markdown` to
write `output/reports/source_refresh_due.{json,md}`. The current report covers
472 metadata rows, classifies 472 as current, and records 0 due-soon, due,
stale, unknown-cadence, or missing-date rows. Cadence buckets are 322 annual,
94 semiannual, 51 quarterly, and 5 biennial rows. The same pass adds the
registry-backed `ageint-source-refresh-due-dashboard` figure and exposes the
gate as `source_refresh_due_ok` in `current_artifact_evidence` and in the local
publication-readiness report.

A separate 2026-05-22 verified batch is encoded in
`data/research_anchors/intelligence-anchors-173-186.jsonl`. It adds NATO CCDCOE
cognitive-warfare research, DARPA Intrinsic Cognitive Security, Cloud Security
Alliance frameworks (Cognitive Degradation Resilience, MAESTRO threat modeling,
securing autonomous AI agents, and the CSA/NIST agent red-teaming standards
note), the OWASP agentic AI threats-and-mitigations reference, frontier-lab agent
research from Anthropic and Google DeepMind, the Prompt Infection and Systems
Security Foundations for Agentic Computing preprints, the Mandel-Tetlock analytic
judgment-correctives study, and the UNU Macau bounded-agency policy analysis.
These rows use `checked_as_of: "2026-05-22"`; the date records direct source
verification, not publication chronology. Any vendor or quantitative figures
inside the cited pages (readiness percentages, success-rate statistics) are
treated as ESTIMATE in the anchor notes, never asserted as fact.

A 2026-06-06 internet-citation batch is encoded in
`data/research_anchors/intelligence-anchors-187-194.jsonl`. It adds NIST AI
100-4 synthetic-content transparency, NIST AI 100-5 global AI standards
engagement, NIST AI 800-1 misuse-risk draft guidance, the International AI
Safety Report 2026, Model Context Protocol specification and security
best-practices pages, Agent2Agent protocol documentation, and NCSC secure-AI
system-development guidance. These rows use `checked_as_of: "2026-06-06"`;
`official_us_aisi_nist_ai_800_1_misuse_risk` intentionally carries
`source_tier: "official_draft"` so manuscript prose treats it as draft guidance,
not finalized policy. The 2026-06-11 internet-backed visualization pass
re-verified the NIST AI 100-4 and MCP rows in this shard without changing their
keys.

A second 2026-06-06 internet-citation batch is encoded in
`data/research_anchors/intelligence-anchors-195-202.jsonl`. It adds MITRE
D3FEND, OASIS CSAF, CycloneDX, SPDX, NIST OSCAL, SLSA, in-toto, and Sigstore
anchors for defensive-control provenance, machine-readable security advisories,
SBOM/provenance documentation, control-assessment automation, supply-chain
levels, signed attestations, and transparency-log backed release evidence. These
rows also use `checked_as_of: "2026-06-06"` and are treated as standards or
official project documentation rather than vendor marketing.

A 2026-06-06 liveness sweep refreshed moved URLs for the CIA Heuer analytic
psychology monograph, OECD public-sector AI, OECD AI and work, NIST Big Data
Interoperability Framework, and C2PA specifications anchors without changing
their citation keys. The same sweep found the UNESCO AI competency-frameworks
article had moved; a likely successor URL is recorded in the anchor note, but
UNESCO reset automated retrieval and still needs manual browser re-verification.

A 2026-06-09 Data Cards pass adds
`@scholarly_data_cards_dataset_documentation` as a directly verified scholarly
dataset-documentation anchor. The pass also routes inherited blog, vendor, and
practitioner source-guide rows to secondary context and replaces the decorative
agentic-boundary concept plate with a deterministic boundary-control figure.

A 2026-06-11 internet-backed visualization pass is encoded in
`data/research_anchors/intelligence-anchors-229-232.jsonl`. It adds NIST AI
800-2 draft benchmark-evaluation practices, the OECD agentic-AI landscape
paper, NSA MCP security design guidance, and the Science Advances psychological
inoculation study. The same pass refreshes existing NIST AI Agent Standards,
NIST AI 600-1, NIST AI 100-4, MCP specification/security, CISA/NSA AI
data-security, OWASP Agentic Applications Top 10, and MITRE ATLAS anchors with
current `checked_as_of` dates and fuller evidence-lane metadata. Draft guidance
keeps `source_tier: "official_draft"` so generated prose does not treat it as
final policy.

A 2026-06-12 visual-accessibility hardening pass used the Perplexity CLI as the
requested discovery lane, but the local Perplexity API call returned
`401 insufficient_quota`; no Perplexity-derived claim was encoded. The final
figure-registry guidance was instead verified directly against W3C WAI Complex
Images, WCAG 2.2 Understanding SC 1.1.1, Section508.gov alternative-text,
color-usage, and PDF-testing guidance, and USWDS data-visualization guidance.
The pass adds no new citation keys; it encodes those official URLs in the local
figure-registry accessibility contract, adds the
`ageint-visual-accessibility-contract` Python figure, and records label, caption,
alt text, long description, source section, and provenance as PNG text metadata.

A follow-on 2026-06-12 visualization-audit pass retried the requested
Perplexity lane and again received `401 insufficient_quota`; no Perplexity prose
was encoded. Direct official verification added W3C WCAG 2.2 Use of Color and
Non-text Contrast guidance to the registry contract. The pass also adds the
`ageint-visual-quality-audit-dashboard` Python figure and writes
`output/figures/visual_quality_audit.json`, a machine-readable audit of PNG
readability, square layout, caption/alt/long-description thresholds, metadata
parity, provenance, and source-section binding.

A 2026-06-12 verifier-first artifact-evidence pass adds no new citation keys.
It adds the `ageint-artifact-evidence-control-loop` Python figure and writes
`output/reports/current_artifact_evidence.{json,md}` after render. The manifest
binds freshness checks, source-section citation coverage, figure quality,
rendered-reference resolution, stale-output scans, PDF quality, and PDF link
targets so no copied PDF or prose evidence note can certify stale output alone.

A 2026-06-12 local scholarship-quality pass adds no new citation keys. It adds
the `ageint-scholarship-triangulation-map` Python figure, strengthens the MCP /
AutoGen and cryptographic-methods appendices with existing official, standards,
and source-guide citation keys, and writes
`output/reports/scholarship_quality.{json,md}`. A follow-on profile-anchor pass
routes existing external anchors into topic lessons, worked examples,
source-canon sections, and review-checklist sections. The report now records
source-family mix, 0 uncited claim-bearing generated files, 0 thin
claim-bearing generated files, and six single-source-family claim-bearing
review-warning rows without adding or renumbering citation keys.

A 2026-06-12 Synthetic Analytic Tradecraft orientation pass adds no new citation
keys. It strengthens the abstract and orientation reader contract around
source-governed synthetic fixtures, adds the label-backed synthetic tradecraft
thesis section, and raised the then-current rendered citation inventory to 379
generated Markdown files and 14,771 generated citation occurrences without
changing the 248-anchor source corpus.

A follow-on SAT method-contract pass adds no new citation keys. It adds the
`ageint-synthetic-tradecraft-method-contract` Python figure and extends the
scholarship-quality report so the abstract/orientation SAT thesis, source-family
triangulation language, negative-control testing language, and method-contract
figure reference are verified alongside ordinary citation counts.

A follow-on analysis-validation pass also adds no new citation keys. It adds the
`ageint-analysis-validation-matrix` Python figure, inserts a label-backed
analysis-validation protocol into the orientation, and extends the
scholarship-quality report so claim-class, validation-question, failure-mode,
and analysis-matrix references are checked alongside the SAT method contract.

A 2026-06-13 RedTeam family-coverage pass adds no new citation keys. It adds
the `ageint-analysis-validation-family-coverage` Python figure and extends the
scholarship-quality report so every claim-bearing generated manuscript family
must have a canonical analysis-validation lane, evidence signal, and failure
signal before local readiness can pass.

A 2026-06-14 official US IC source-pack pass is encoded in
`data/research_anchors/intelligence-anchors-249-304.jsonl`. It adds 56
directly verified public CIA, DIA, ODNI, Intelligence.gov, NSA, NGA, FBI, and
NRO anchors and requires `source_agency`, `source_pack`, explicit lane/tier,
checked-date, claim-scope, assurance-use, rights, and deterministic profile
routing metadata. The companion `agency_source_coverage` report and dashboard
make the source-pack layer fail-closed in artifact evidence and publication
readiness.

A 2026-06-15 literature-integration pass is encoded in
`data/research_anchors/intelligence-anchors-305-340.jsonl`. It adds 36 directly
verified scholarly, official, and public-domain sources from the synthetic
intelligence, analytic tradecraft, OPSEC, cognitive-security, adversarial-ML, AI
incident, OSINT leakage, deepfake, disinformation, social-engineering cognition,
and active-inference discovery inventories. The pasted literature reviews remain
discovery-only inputs; each new row carries explicit lane, tier, checked-date,
verification method, claim scope, refresh cadence, refresh trigger, stakeholder,
assurance, and rights metadata.

A 2026-06-15 SAT literature-integration pass is encoded in
`data/research_anchors/intelligence-anchors-341-367.jsonl`. It adds 27 directly
verified structured-analytic-technique, ACH, decision-science,
forecasting-calibration, postmortem, and pedagogy sources after dedupe against
the existing tradecraft spine. The attached SAT literature report remains
discovery-only; each new row carries explicit lane, tier, checked-date,
verification method, claim scope, refresh cadence, refresh trigger, stakeholder,
assurance, and rights metadata.

A 2026-06-11 analytic-tradecraft integration pass is encoded in
`data/research_anchors/intelligence-anchors-233-248.jsonl`. It adds CIA/Kent
tradecraft history, warning-intelligence, IRTPA, 9/11 and WMD postmortem,
NATO alternative-analysis, SAT evaluation, forecasting-calibration, and
failure-theory sources. These anchors support Chapters 41-42 and the four new
tradecraft diagrams while keeping SAT claims evidence-bounded and separating
likelihood, confidence, assumptions, dissent, and source quality.

## Refresh triggers: source changes that reopen claims before reuse

Refresh a source row when legal text, standards versions, official guidance,
source URLs, source ownership, implementation timelines, or instructor debriefs
materially change the claim supported by that source. Accessibility defects,
DPIA/HRIA triggers, procurement/vendor changes, AI red-team findings, public
transparency updates, agent incident debriefs, model and dataset cards,
transparency notices, records-retention evidence, release gates, risk
exceptions, learner support, instructor question bank findings, and remediation
backlogs also trigger refresh.
