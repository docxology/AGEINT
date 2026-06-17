# AGEINT Data

Declarative inputs consumed by `src/` loaders and the curriculum build.

| Path | Role |
| --- | --- |
| `curriculum/` | Sharded curriculum parts, chapters, sections, references |
| `concept_routes.yaml` | Primary keyword concept routes |
| `concept_routes_supplement.yaml` | Supplemental keyword, domain, and category concept routes |
| `manuscript_architecture.yaml` | Chapter profile architecture tables (inputs/transforms/outputs/failures) |
| `research_anchors/` | Curated official and scholarly anchor metadata |
| `source_identity/` | Locked source-guide identity records |

This table lists the primary surfaces; see [`data/AGENTS.md`](AGENTS.md) for the
full declarative-input inventory (the source packs, routing tables, profiles,
and `figures/` data consumed by `src/`).

Edit these surfaces, then rebuild with `uv run python scripts/build_curriculum.py`.
