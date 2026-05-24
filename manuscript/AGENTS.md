# manuscript/ Agent Guide

- Do not hand-author source counts; derive from `data/curriculum/`.
- Author reusable manuscript structure in `templates/` with generic tokens such as `{{SECTION_TITLE}}`.
- Do not add numbered chapter Markdown files under `manuscript/`.
- Full config surface: see [`config.yaml.example`](config.yaml.example); live values in [`config.yaml`](config.yaml).
- Generated semantic prose lives only under `output/manuscript/` (not under `manuscript/`). Never hand-edit generated markdown; fix templates, `src/manuscript_manifest/`, or `src/figures/`, then rebuild.
- Cross-references use Pandoc-crossref labels (`{#sec:…}`, `{#fig:…}`, `[@sec:…]`, `[@fig:…]`), not hard-coded Figure/Section numbers and not the template exemplar `[[FIG:…]]` / `[[VAR:…]]` injector pattern.
- Use Pandoc citations (`[@ageintNNN]` or official source-anchor keys) only in generated contexts.
- Keep examples synthetic and defensive.
- If prose is expanded, do it through neutral templates or renderer context builders so cross-links stay generated and stable.
- Treat `references-*.bib` as generated from parsed guide references plus curated source anchors.
- Keep `preamble.md` and `config.yaml` manuscript-wide; do not put chapter-specific structure there.
- Generated section labels and figure references belong in `src/manuscript_manifest/` and `src/figures/`, not in source templates.
- Rebuild after edits and verify that output Markdown has no unresolved `{{TOKENS}}`, raw LaTeX refs, or hard-coded Figure/Section numbers.
