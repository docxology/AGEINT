# AGENTS.md — `data/curriculum/parts`

Container for the 16 curriculum parts of the AGEINT atlas. Each child `<NN-slug>/` holds `part.json` and a `chapters/` directory.

## Gotchas
- Edit part content here; output copies regenerate via `scripts/build_curriculum.py`.
- Local-only path under the AGEINT checkout (`projects/ongoing/docxology/AGEINT` in the template workspace); AGEINT itself is public (Zenodo DOI 10.5281/zenodo.20732274) but this checkout is not committed from here.
