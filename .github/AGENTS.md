# AGENTS.md — `AGEINT/.github`

Repository-level GitHub configuration.

## Layout
- `dependabot.yml` — dependency update schedule.
- `workflows/` — GitHub Actions workflow definitions (see subdirectory doc).

## Gotchas
- Workflows require explicit `uv` setup; a first CI run failed with "uvx: command not found" and was fixed with `astral-sh/setup-uv` (commented in `workflows/ci.yml`).
- AGEINT is a public repository (Zenodo DOI 10.5281/zenodo.20732274); its contents are committed here.
