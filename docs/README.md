# AGEINT Docs

Project-local documentation for the AGEINT curriculum.

## Current Source Snapshot

These counts are measured from the live source layer and should change only
after a rebuild and docs refresh:

| Surface | Current value | Source of truth |
| --- | ---: | --- |
| Parts | 16 | `data/curriculum/stats.json` |
| Chapters | 51 | `data/curriculum/stats.json` |
| Appendices | 9 | `data/curriculum/stats.json` |
| Source-guide references | 312 | `data/curriculum/references/` |
| Curated research anchors | 248 | `data/research_anchors/` |
| Registered figures | 161 | `output/figures/figure_registry.json` |

Perplexity may be used for discovery and second-opinion research. Final claims
in docs or generated output must cite direct official, standards-body,
public-domain, or scholarly sources encoded in the source layer.

## Hub (template parity)

| Doc | Purpose |
| --- | --- |
| [`agent_instructions.md`](agent_instructions.md) | Agent editing rules and verification |
| [`architecture.md`](architecture.md) | Tokenized templates and build separation |
| [`testing_philosophy.md`](testing_philosophy.md) | Test fixtures and no-mocks policy |
| [`rendering_pipeline.md`](rendering_pipeline.md) | Generated manuscript → PDF |
| [`style_guide.md`](style_guide.md) | Defensive educational prose |
| [`syntax_guide.md`](syntax_guide.md) | Citations and cross-refs |
| [`citation_workflow.md`](citation_workflow.md) | Canonical citation authoring, counting, and validation workflow |
| [`faq.md`](faq.md) | Common questions |
| [`quickstart.md`](quickstart.md) | Command entry points |
| [`output_conventions.md`](output_conventions.md) | `output/` layout |
| [`output_inventory.md`](output_inventory.md) | Generated artifact contract |
| [`troubleshooting.md`](troubleshooting.md) | Build and validation fixes |
| [`forking_guide.md`](forking_guide.md) | Fork workflow |

## Domain docs

- `safety.md`, `safety_audit.md` — non-operational dual-use boundary
- `citation_workflow.md`, `source_identity_stability.md`, `source_lane_map.md`, `source_refresh_ledger.md` — citation spine
- `research.md` — verified research anchor posture
- `instructor_guide.md`, `learner_support_assessment.md` — pedagogy
- `evidence_package_map.md`, `data_lineage_registry.md` — governance artifacts
- `accessibility_rights_review.md`, `transparency_notice_workflow.md`, `procurement_vendor_governance.md`, and related v2 lane docs

Rebuild AGEINT and update counts when generated output changes.
