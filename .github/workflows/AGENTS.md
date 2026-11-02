# AGENTS.md — `AGEINT/.github/workflows`

GitHub Actions workflow definitions.

## Layout
- `AGENTS.md`
- `README.md`
- `ci.yml`
- `manuscript.yml`
- `source-freshness.yml`

## Gotchas
- `ci.yml` runs lint (ruff) and test jobs; some tests skip without the sibling template checkout, which is why the CI coverage floor is lower than `pyproject.toml`.
- AGEINT is a public repository (Zenodo DOI 10.5281/zenodo.20732274); its contents are committed here.
