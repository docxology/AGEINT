# AGENTS.md - AGEINT Source

Keep source modules composable: parsing, research-backed content profiles,
practice lenses, template-library writing, variable generation, figure
rendering, and manifest rendering should stay separable.

Do not hard-code chapter-specific variables or numbered Markdown filenames. Concrete titles, paths, citations, and counts must derive from parsed curriculum data and generated manifests.

Do not hard-code figure numbers or section numbers. Figures must resolve through `FigureSpec`, `output/figures/figure_registry.json`, and Pandoc-crossref labels.

## Package layout

| Module / package | Role |
| --- | --- |
| `curriculum.py` | Load and query sharded curriculum under `data/curriculum/` |
| `build_pipeline.py` | Canonical `run_build()` orchestration (data mirror, variables, BibTeX, figures, manuscript) |
| `intelligence_content/` | Official/scholarly anchors, domain profiles, practice lenses, synthesis; see [intelligence_content/AGENTS.md](intelligence_content/AGENTS.md) |
| `manuscript_manifest/` | Semantic manuscript paths, section context, chapter fragment directories |
| `manuscript_variables/` | Runtime variables, BibTeX generation (`write_bibtex_files`) |
| `figures/` | Registry-backed figure rendering; see [figures/AGENTS.md](figures/AGENTS.md) |
| `manuscript_templates.py` | Neutral source template library |
| `_jsonl.py`, `_paths.py` | Shared JSONL reader and project path bootstrap |

Public exports are declared in `src/__init__.py`. Part modules (`_01_part.py`, …) are implementation details merged at import time; prefer importing from the package root or `__init__.py`.

Use `intelligence_content/` for official/scholarly source anchors, domain
profiles, source lanes, safe substitutions, capstone workflows, practice
lenses, and research-backed synthesis. Perplexity may
support discovery, but final manuscript citations must point to directly
verified sources.

When adding intelligence-domain depth, extend the structured anchor/profile/lens
system first. Current specialized lanes include governed IC cycle and
dissemination, AI/data ethics, AI conformity/compliance, education and
assessment, public-sector agentic AI, cross-border data/data spaces,
human-rights governance, agent interoperability standards, workforce
governance, model/data provenance, FININT and economic security, historical
declassified sources, agentic AI governance, OSINT/GEOINT, collection
management, counterintelligence, cognitive security, CTI, ICS/OT, legal
oversight, accessibility/digital inclusion, procurement/vendor governance,
agent incident response, AI red-team assurance, public-sector transparency, and
rights-impact privacy review.

Preserve `data/source_identity/` for `ageint001` through `ageint231`.
Append new guide references after that range; current append-only references
extend through `ageint296`. Keep source-lane metadata auditable in generated
BibTeX and bibliography atlas rows.

Dual-use curriculum material must be bounded to authorized, synthetic, defensive, tabletop, or owned-lab contexts.

`run_build()` defaults to placeholder figures when Mermaid/Chrome is unavailable; set `AGEINT_REQUIRE_RENDERED_FIGURES=1` for full PNG renders. `render_figures(..., allow_placeholder_figures=True)` is the default on direct calls; `scripts/generate_figures.py` mirrors the same env rule (`--no-allow-placeholder-figures` for strict local renders). See `figures/AGENTS.md`.

Tests should exercise public behavior through real guide data. Avoid mocks for
the parser, manifest, source identity lock, source-lane metadata, safety audit,
bibliography, figure registry, and generated-output contracts.
