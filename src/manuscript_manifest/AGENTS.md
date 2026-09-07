# AGENTS.md — `AGEINT/src/manuscript_manifest`

Builds and renders the AGEINT semantic manuscript manifest.

## Layout
- `__init__.py`, `types.py` — package surface and manifest datatypes/slug helpers.
- `_01_part.py` … `_05_part.py` — staged manifest build/render logic.
- `_appendix_support.py` — appendix body rendering.
- `_canonical_reference.py` — single source of truth for canonical chapter-independent method/assurance tables.
- `_chapter_governance.py` — governance/audit/QA section renderers (extracted from `_02_part.py`).
- `_chapter_practice_pathways.py` — practice studio, pathway assessment, synthesis generators (extracted from `_03_part.py`).
- `_heading_titles.py` — chapter landmark title helpers.
- `_orientation_visuals.py` — orientation figure markdown helpers.

## Gotchas
- Imports come from a flat `src` path bootstrap (`_paths.ensure_project_paths`), including the sibling `curriculum` package.
- Extraction modules (`_chapter_governance`, `_chapter_practice_pathways`) must stay in sync with their origin part files.
- Local-only path under the AGEINT checkout (`projects/ongoing/docxology/AGEINT` in the template workspace); AGEINT itself is public (Zenodo DOI 10.5281/zenodo.20732274) but this checkout is not committed from here.
