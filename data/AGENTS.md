# AGENTS.md - AGEINT Data

Treat `data/curriculum/` as the committed runtime spine. Optional guide input
`SIST-Guide-TOC-and-Bibliography-v2.md` may be present locally, but normal builds
reload from the sharded curriculum directory.

Declarative routing tables:

| File | Role |
| --- | --- |
| `concept_routes.yaml` (+ supplement) | Keyword and category concept frames for topic lessons |
| `topic_risk_routes.yaml` | Ordered topic/chapter risk-category rules (`src/intelligence_content/risk_routes.py`) |
| `topic_prompt_routes.yaml` | Evidence/artifact prompt routes (`src/intelligence_content/topic_prompt_routes.py`) |
| `topic_rotation_templates.yaml` | Why-it-matters and misconception rotation templates (`topic_rotation_templates.py`) |
| `coursebook_profiles.yaml` | `CoursebookProfile` rows keyed by identifier (`_06_part.py`) |
| `safety_artifact_tables.yaml` | Safety substitution and assurance worksheet tables (`_08_part.py`) |
| `manuscript_architecture.yaml` | Module architecture rows by profile id |
| `unit_education_profiles.yaml` | Unit-specific lesson evidence/artifact lines |
| `source_support_expansion.yaml` | Citation routes for uncited source sections |

Regenerate `topic_risk_routes.yaml` from canonical tuples when rule logic changes:
`uv run python scripts/generate_risk_routes_yaml.py` (then verify
`tests/fixtures/risk_category_parity.json` / `tests/test_topic_frame_routing.py`).

Regenerate `topic_prompt_routes.yaml` when evidence/artifact prompt tables change:
`uv run python scripts/generate_topic_prompt_routes_yaml.py`, then refresh
`tests/fixtures/topic_prompt_parity.json` via
`uv run python scripts/generate_prompt_parity_fixture.py` before deleting Python tables.

Regenerate `topic_rotation_templates.yaml` when rotation templates change:
`uv run python scripts/generate_topic_rotation_templates_yaml.py`, then refresh
`tests/fixtures/topic_rotation_parity.json` via
`uv run python scripts/generate_rotation_parity_fixture.py`.

**Authoritative YAML (edit files directly):** `coursebook_profiles.yaml` and
`safety_artifact_tables.yaml` have no Python-canonical generator. Change the YAML
and validate with:

```bash
uv run python scripts/validate_declarative_yaml.py
uv run pytest tests/test_data_loaders.py -v
```

**Generator-backed YAML** (Python tuples in `scripts/generate_*_yaml.py`):
`topic_risk_routes.yaml`, `topic_prompt_routes.yaml`, `topic_rotation_templates.yaml`.

If counts, titles, citations, appendices, profile identifiers, or pattern data
drift, fix the shards or `src/curriculum.py`, rebuild with
`uv run python scripts/build_curriculum.py`, and run the AGEINT tests.
Downstream manuscript paths, variables, figure assignments, and bibliography
rows depend on this shape.

Keep intelligence, cyber, influence, and ICS content framed as defensive
curriculum material. No live targeting, unauthorized collection, exploitation,
evasion, manipulation, covert tasking, or operational response instructions
belong here.
