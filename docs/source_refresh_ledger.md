# Source Refresh Ledger

AGEINT v2 uses a source-lane ledger for curated anchors and an identity lock for
the original source-guide references.

## Locked Range

- `ageint001` through `ageint231` are locked in `data/source_identity/`.
- Existing locked keys, titles, and URLs must remain stable unless the source
  identity actually changes and the lock is intentionally regenerated.
- New source-guide references are append-only and currently span `ageint232`
  through `ageint296`.

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

## Refresh Triggers

Refresh a source row when legal text, standards versions, official guidance,
source URLs, source ownership, implementation timelines, or instructor debriefs
materially change the claim supported by that source. Accessibility defects,
DPIA/HRIA triggers, procurement/vendor changes, AI red-team findings, public
transparency updates, agent incident debriefs, model and dataset cards,
transparency notices, records-retention evidence, release gates, risk
exceptions, learner support, instructor question bank findings, and remediation
backlogs also trigger refresh.
