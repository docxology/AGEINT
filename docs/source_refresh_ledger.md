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

A further 2026-05-22 verified batch is encoded in
`data/research_anchors/intelligence-anchors-173-186.jsonl`. It adds NATO CCDCOE
cognitive-warfare research, DARPA Intrinsic Cognitive Security, Cloud Security
Alliance frameworks (Cognitive Degradation Resilience, MAESTRO threat modeling,
securing autonomous AI agents, and the CSA/NIST agent red-teaming standards
note), the OWASP agentic AI threats-and-mitigations reference, frontier-lab agent
research from Anthropic and Google DeepMind, the Prompt Infection and Systems
Security Foundations for Agentic Computing preprints, the Mandel-Tetlock analytic
judgment-correctives study, and the UNU Macau bounded-agency policy analysis.
These rows use `checked_as_of: "2026-05-22"`. Any vendor or quantitative figures
inside the cited pages (readiness percentages, success-rate statistics) are
treated as ESTIMATE in the anchor notes, never asserted as fact.

## Refresh Triggers

Refresh a source row when legal text, standards versions, official guidance,
source URLs, source ownership, implementation timelines, or instructor debriefs
materially change the claim supported by that source. Accessibility defects,
DPIA/HRIA triggers, procurement/vendor changes, AI red-team findings, public
transparency updates, agent incident debriefs, model and dataset cards,
transparency notices, records-retention evidence, release gates, risk
exceptions, learner support, instructor question bank findings, and remediation
backlogs also trigger refresh.
