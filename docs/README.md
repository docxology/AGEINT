# AGEINT Docs: local curriculum contracts and verification guides

Project-local documentation for the AGEINT curriculum.

## Current source snapshot: live counts, anchors, figures, and readiness limits

These counts are measured from the live source layer and should change only
after a rebuild and docs refresh:

| Surface | Current value | Source of truth |
| --- | ---: | --- |
| Parts | 16 | `data/curriculum/stats.json` |
| Chapters | 51 | `data/curriculum/stats.json` |
| Appendices | 9 | `data/curriculum/stats.json` |
| Source-guide references | 312 | `data/curriculum/references/` |
| Curated research anchors | 462 | `data/research_anchors/` |
| Source-quality support anchors | 10 | `data/research_anchors/source-quality-anchors.jsonl` |
| Source metadata rows | 472 | `output/reports/source_metadata.json` |
| Registered figures | 173 | `output/figures/figure_registry.json` |
| Non-numbered cover art | 1 | `output/figures/cover/ageint-cover-synthesis.png` |

The numbered graphical abstract is the Python-rendered
`fig:ageint-graphical-abstract` Synthetic Tradecraft System Atlas in the
orientation section. PDF TOC entries are limited to H1/H2 reader landmarks; the
repeated teaching scaffolds remain as H3/H4 body headings.

The current verifier stack includes `claim_calibration_ok`: generated
manuscript rows with proof-language, p-values, measured-performance language,
unsupported formalisms, or weak-source-only high-risk claims must fail unless
the row is explicit boundary or misconception-control prose.

The US IC source-pack verifier adds `agency_source_coverage_ok`: the 56 new
official CIA, DIA, ODNI, Intelligence.gov, NSA, NGA, FBI, and NRO anchors must
carry explicit agency, pack, lane, tier, checked-date, claim-scope, assurance,
rights, and profile-routing metadata.

Perplexity may be used for discovery and second-opinion research. Final claims
in docs or generated output must cite direct official, standards-body,
public-domain, or scholarly sources encoded in the source layer.

## Documentation hub: template-parity stubs and AGEINT-specific guides

| Doc | Purpose |
| --- | --- |
| [`agent_instructions.md`](agent_instructions.md) | Agent editing rules and verification |
| [`architecture.md`](architecture.md) | Tokenized templates and build separation |
| [`testing_philosophy.md`](testing_philosophy.md) | Test fixtures and no-mocks policy |
| [`rendering_pipeline.md`](rendering_pipeline.md) | Generated manuscript → PDF |
| [`orchestration_contract.md`](orchestration_contract.md) | Registry-backed build, audit, source-pack, and Mermaid extension contracts |
| [`style_guide.md`](style_guide.md) | Defensive educational prose |
| [`syntax_guide.md`](syntax_guide.md) | Citations and cross-refs |
| [`citation_workflow.md`](citation_workflow.md) | Canonical citation authoring, counting, and validation workflow |
| [`faq.md`](faq.md) | Common questions |
| [`quickstart.md`](quickstart.md) | Command entry points |
| [`output_conventions.md`](output_conventions.md) | `output/` layout |
| [`output_inventory.md`](output_inventory.md) | Generated artifact contract |
| [`publication_readiness.md`](publication_readiness.md) | Local preflight bundle and release boundary |
| [`troubleshooting.md`](troubleshooting.md) | Build and validation fixes |
| [`forking_guide.md`](forking_guide.md) | Fork workflow |

## Domain docs: safety, governance, source lanes, and assurance workflows

- `safety.md`, `safety_audit.md` — non-operational dual-use boundary
- `citation_workflow.md`, `source_identity_stability.md`, `source_lane_map.md`, `source_refresh_ledger.md`, `publication_readiness.md` — citation, refresh, and release-preflight spine
- `research.md` — verified research anchor posture
- `instructor_guide.md`, `learner_support_assessment.md` — pedagogy
- `evidence_package_map.md`, `data_lineage_registry.md` — governance artifacts
- `accessibility_rights_review.md`, `transparency_notice_workflow.md`, `procurement_vendor_governance.md`, and related v2 lane docs

Rebuild AGEINT and update counts when generated output changes.
