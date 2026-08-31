# AGENTS.md — `AGEINT/src/manuscript_variables`

Runtime manuscript-variable generation for the AGEINT curriculum atlas.

## Layout
- `__init__.py` — exports (incl. `SOURCE_QUALITY_ANCHORS`).
- `_01_part.py` — variable generation entry logic.
- `_02_part.py` — additional variable assembly from `curriculum` data.
- `_bibtex_helpers.py` — BibTeX string cleaning and reference formatting.

## Gotchas
- Invoked via `scripts/z_generate_manuscript_variables.py`; feeds the render pipeline's variable injection.
- Local-only path under the AGEINT checkout (`projects/ongoing/docxology/AGEINT` in the template workspace); AGEINT itself is public (Zenodo DOI 10.5281/zenodo.20732274) but this checkout is not committed from here.
