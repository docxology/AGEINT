# AGENTS.md — `AGEINT/data/figures`

Source figure-concept data for the AGEINT figure registry.

## Layout
- `concept_plates.jsonl` — figure concept definitions (one JSON object per line).
- `synthesis_extra.jsonl` — additional synthesis figure specs.

## Gotchas
- Rendered PNGs land in `output/figures/` via `scripts/generate_figures.py`; edit concepts here, not the rendered output.
- Local-only path under the AGEINT checkout (`projects/ongoing/docxology/AGEINT` in the template workspace); AGEINT itself is public (Zenodo DOI 10.5281/zenodo.20732274) but this checkout is not committed from here.
