# AGENTS.md - AGEINT Source

Keep source modules composable: parsing, research-backed content profiles,
practice lenses, template-library writing, variable generation, figure
rendering, and manifest rendering should stay separable.

Do not hard-code chapter-specific variables or numbered Markdown filenames. Concrete titles, paths, citations, and counts must derive from parsed curriculum data and generated manifests.

Do not hard-code figure numbers or section numbers. Figures must resolve through `FigureSpec`, `output/figures/figure_registry.json`, and Pandoc-crossref labels.

## Package layout

| Module / package | Role |
| --- | --- |
| `curriculum.py` | Load and query sharded curriculum under `data/curriculum/`; exports `PATTERN_REGISTRY_CHAPTER_NUMBER` (32) |
| `build_pipeline.py` | Canonical `run_build()`, `run_build_figures()`, and `BuildConfig` orchestration (`source_path` override for tests) |
| `_slug.py` | Numbered curriculum path helpers (`curriculum_sections_jsonl_path`, …) |
| `_curriculum_shards.py` | Shard load, reference dedupe, source-support hydration |
| `_data_loaders.py` | YAML loaders for concept routes, topic risk routes, and module architecture tables |
| `_markdown_split.py` | Generic Markdown fragment splitting for manuscript output |
| `prose_policy.py` | Shared reader-facing title/prose transforms |
| `safety_contract.py` | Canonical blocked operational phrases and direct-task motifs; imported by `source_grounding` and manuscript-safety tests |
| `analysis_validation.py` | Canonical analysis-validation claim-class lanes used by orientation prose, matrix rendering, and scholarship verifier contracts |
| `markdown_refs.py` | Validated Pandoc `@sec:` / `@fig:` / citekey helpers; `lesson_educational_crossrefs()` for topic-lesson cross-links |
| `citation_workflow.py` | Generated/source-section citation inventories and source-guide citation spine helpers |
| `scholarship_quality.py` | Generated-manuscript scholarship audit: source-family mix, thin claim-bearing support, and report rendering |
| `manuscript_injection.py` | Thin adapter to `infrastructure.rendering.manuscript_injection` (single import site for manifest render) |
| `output_docs.py` | Generated README/AGENTS writers for output, manuscript, and figures |
| `intelligence_content/` | Official/scholarly anchors, domain profiles, practice lenses, synthesis; see [intelligence_content/AGENTS.md](intelligence_content/AGENTS.md) |
| `manuscript_manifest/` | Semantic manuscript paths, section context, chapter fragment directories; types in `manuscript_manifest/types.py` |
| `manuscript_variables/` | Runtime variables, BibTeX generation (`write_bibtex_files`) |
| `figures/` | Registry-backed figure rendering; see [figures/AGENTS.md](figures/AGENTS.md) |
| `manuscript_templates.py` | Neutral source template library |
| `_jsonl.py`, `_paths.py` | Shared JSONL reader, project path bootstrap, and `remove_tree()` cleanup |

Public exports are declared in `src/__init__.py` (pipeline and manifest surface only; import `intelligence_content` row helpers from that package). Sharded subpackages use explicit per-shard imports in package `__init__.py` files.

Declarative routing and architecture tables live under `data/*.yaml` (loaded by `_data_loaders.py`; see that module for the authoritative list — it includes the concept-route, topic-risk/prompt/rotation, manuscript-architecture, coursebook-profile, unit-education, source-support-expansion, and safety-artifact tables).

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
extend through `ageint312`. Keep source-lane metadata auditable in generated
BibTeX and bibliography atlas rows.

Dual-use curriculum material must be bounded to accountable, synthetic, defensive, tabletop, or owned-lab contexts.

`run_build()` reads build flags through `BuildConfig.from_env()` (`AGEINT_REQUIRE_RENDERED_FIGURES=1` disables placeholder figures). `scripts/generate_figures.py` and `run_build_figures()` use the same config. See `figures/AGENTS.md`.

Tests should exercise public behavior through real guide data. Avoid mocks for
the parser, manifest, source identity lock, source-lane metadata, safety audit,
bibliography, figure registry, and generated-output contracts.
