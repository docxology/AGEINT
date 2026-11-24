# AGENTS.md — `AGEINT/src/manuscript_manifest`

Builds and renders the AGEINT semantic manuscript manifest.

## Layout
- `__init__.py`, `types.py` — package surface and manifest datatypes/slug helpers.
- `_01_part.py` … `_05_part.py` — staged manifest build/render logic.
- `_appendix_support.py` — appendix body rendering.
- `_canonical_reference.py` — single source of truth for canonical chapter-independent method/assurance tables.
- `_chapter_practice_pathways.py` — topic assessment, capstone pathway, and synthesis generators.
- `_heading_titles.py` — chapter landmark title helpers.
- `_orientation_visuals.py` — orientation figure markdown helpers.

## Gotchas
- Imports come from a flat `src` path bootstrap (`_paths.ensure_project_paths`), including the sibling `curriculum` package.
- Chapters render through `_03_part._chapter_body` into five fragment roles: overview, practice studio, evidence contract, governance boundary, and assessment route. Shared governance forms remain in orientation, and chapter-independent method/assurance tables remain in `_canonical_reference.py`; do not restore per-chapter copies.
- AGEINT is a public repository (Zenodo DOI 10.5281/zenodo.20732274); its contents are committed here.
