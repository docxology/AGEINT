# Source Refresh Ledger

AGEINT v2 uses a source-lane ledger for curated anchors and an identity lock for
the original source-guide references.

For the step-by-step authoring, counting, rebuild, and validation workflow, use
[`citation_workflow.md`](citation_workflow.md).

## Locked Range

- `ageint001` through `ageint231` are locked in `data/source_identity/`.
- Existing locked keys, titles, and URLs must remain stable unless the source
  identity actually changes and the lock is intentionally regenerated.
- New source-guide references are append-only and currently span `ageint232`
  through `ageint312`.

## Curated Anchor Metadata

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

The May 24, 2026 source refresh is encoded in
`data/research_anchors/intelligence-anchors-161-172.jsonl`. It adds official
Canada, OECD, UN, NIST, and CISA anchors for bounded agentic AI governance,
algorithmic impact review, public AI registers, AI incident reporting, NIST
Dioptra assurance, secure AI deployment, OT procurement, OT asset inventory,
and definitive OT architecture evidence. These rows use
`checked_as_of: "2026-05-24"` and the same direct-verification standard as the
May 21 and May 22 shards.

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

A 2026-06-11 analytic-tradecraft integration pass is encoded in
`data/research_anchors/intelligence-anchors-233-248.jsonl`. It adds CIA/Kent
tradecraft history, warning-intelligence, IRTPA, 9/11 and WMD postmortem,
NATO alternative-analysis, SAT evaluation, forecasting-calibration, and
failure-theory sources. These anchors support Chapters 41-42 and the four new
tradecraft diagrams while keeping SAT claims evidence-bounded and separating
likelihood, confidence, assumptions, dissent, and source quality.

## Refresh Triggers

Refresh a source row when legal text, standards versions, official guidance,
source URLs, source ownership, implementation timelines, or instructor debriefs
materially change the claim supported by that source. Accessibility defects,
DPIA/HRIA triggers, procurement/vendor changes, AI red-team findings, public
transparency updates, agent incident debriefs, model and dataset cards,
transparency notices, records-retention evidence, release gates, risk
exceptions, learner support, instructor question bank findings, and remediation
backlogs also trigger refresh.
