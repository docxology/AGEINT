# AGEINT Scripts

This folder contains thin AGEINT orchestration entrypoints.

- Owner: project build and hydration workflow.
- Status: manual code; scripts should call `src/` and infrastructure helpers.
- Source of truth: `src/build_pipeline.py`, `src/curriculum.py`, `src/manuscript_manifest/`, and `src/manuscript_variables/`.
- Main command: `uv run python scripts/build_curriculum.py`.
- Figure command: `uv run python scripts/generate_figures.py`.
- Setup hook: `uv run python scripts/setup_hook.py` (output doc scaffolding after clean).
- Safety: scripts orchestrate defensive educational rendering only.

`build_curriculum.py` delegates to `src/build_pipeline.run_build`, which refreshes
parsed JSON, mirrored output data, runtime variables, BibTeX, the figure registry,
and the semantic manuscript. The figure command is useful for focused visual checks
when source data already exists. `z_generate_manuscript_variables.py` exists for
template compatibility and delegates to the full build rather than maintaining a
parallel path.

One-time migration helpers live under [`archive/`](archive/README.md); normal builds
do not invoke them.
