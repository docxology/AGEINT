# AGEINT Manuscript Source

This folder contains manuscript configuration, bibliography output, preamble settings, and the neutral source template library under `templates/`.

The resolved manuscript is generated under `output/manuscript/` with semantic paths and generated ordering config.

Regenerate from the source guide with `uv run python scripts/build_curriculum.py` from the AGEINT root. Regenerate the neutral template library only with `--regenerate-source-template-library`.

## Authoring model

Source templates stay generic and tokenized. Concrete module titles, labels,
section maps, source spines, research briefs, visual synthesis blocks, and
navigation references are injected by `src/manuscript_manifest/` and
`src/manuscript_variables/`.

`references-*.bib` is generated. Add official or scholarly anchors in `src/` and
rebuild rather than editing bibliography entries by hand. Generated manuscript
files should appear only under `output/manuscript/`.
