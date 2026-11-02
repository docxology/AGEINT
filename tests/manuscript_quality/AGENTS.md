# AGENTS.md — `AGEINT/tests/manuscript_quality`

Generated-manuscript inventory tests.

## Layout
- `__init__.py`, `inventory_helpers.py` — shared constants/helpers for manuscript inventory tests; imports from `intelligence_content`, `manuscript_variables`, and `manuscript_manifest._heading_titles`.

## Gotchas
- Depends on the flat `src` path bootstrap; run tests from the project root so imports resolve.
- Some tests need the sibling template checkout and skip without it (see root AGENTS.md).
- AGEINT is a public repository (Zenodo DOI 10.5281/zenodo.20732274); its contents are committed here.
