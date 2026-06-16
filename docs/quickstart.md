# Quickstart: AGEINT build, validation, and editing entry points

Run the parser/build step and tests from the AGEINT root. Run markdown/prerender validation from the sibling template root against the working checkout path.

```bash
uv run python scripts/build_curriculum.py
uv run python scripts/generate_figures.py
uv run python scripts/audit_orchestration_contract.py --format json
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run pytest tests/test_source_identity.py

# Optional: require full Mermaid/Chrome figure renders (no placeholders)
AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/build_curriculum.py

# From the template repo root:
uv run python -m infrastructure.validation.cli markdown projects/working/AGEINT/output/manuscript --repo-root .
uv run python -m infrastructure.validation.cli prerender projects/working/AGEINT/output/manuscript --repo-root .
```

## Editing workflow: update source surfaces, rebuild, and run gates

When the historical SIST guide is absent, edit curriculum content in
`data/curriculum/parts/*/chapters/*/chapter.json` and related shards first.
Each chapter shard carries `content_profile` and `practice_lens` identifiers
that drive manifest rendering. Rebuild after shard, template, or `src/` edits.

Regenerate the neutral source template library only when intentionally changing source templates:

```bash
uv run python scripts/build_curriculum.py --regenerate-source-template-library
```

The normal build already refreshes data (including `output/data/curriculum_outline.json`), variables, figures, generated BibTeX,
registry-backed figures, generated folder docs, expanded reader-facing chapter
sections, and semantic manuscript output under
`output/manuscript/parts/<part-slug>/<chapter-slug>/`. Use the figure command alone when
only checking the registry-backed visual layer. Use the template-regeneration
flag only when the neutral template library itself should be reset from code.

Outputs under `output/` are generated. If a generated file looks wrong, update
curriculum shards, `src/manuscript_manifest/`, `src/intelligence_content/`,
other `src/` helpers, or `manuscript/templates/`, then rebuild instead of
editing generated Markdown or PNGs directly.
