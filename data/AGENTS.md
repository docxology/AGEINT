# AGENTS.md - AGEINT Data

Treat `data/curriculum/` as the committed runtime spine. Optional guide input
`SIST-Guide-TOC-and-Bibliography-v2.md` may be present locally, but normal builds
reload from the sharded curriculum directory.

Declarative routing tables:

| File | Role |
| --- | --- |
| `concept_routes.yaml` (+ supplement) | Keyword and category concept frames for topic lessons |
| `topic_risk_routes.yaml` | Ordered topic/chapter risk-category rules (`src/intelligence_content/risk_routes.py`) |
| `manuscript_architecture.yaml` | Module architecture rows by profile id |
| `unit_education_profiles.yaml` | Unit-specific lesson evidence/artifact lines |
| `source_support_expansion.yaml` | Citation routes for uncited source sections |

Regenerate `topic_risk_routes.yaml` from canonical tuples when rule logic changes:
`uv run python scripts/generate_risk_routes_yaml.py` (then verify
`tests/fixtures/risk_category_parity.json` / `tests/test_topic_frame_routing.py`).

If counts, titles, citations, appendices, profile identifiers, or pattern data
drift, fix the shards or `src/curriculum.py`, rebuild with
`uv run python scripts/build_curriculum.py`, and run the AGEINT tests.
Downstream manuscript paths, variables, figure assignments, and bibliography
rows depend on this shape.

Keep intelligence, cyber, influence, and ICS content framed as defensive
curriculum material. No live targeting, unauthorized collection, exploitation,
evasion, manipulation, covert tasking, or operational response instructions
belong here.
