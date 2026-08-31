# AGENTS.md — `07-sigint-fundamentals` (chapter data)

One chapter of the AGEINT curriculum.

## Layout
- `chapter.json` — chapter number, title, citation keys, `content_profile`, source line.
- `sections.jsonl` — one JSON object per section: `level`, `number`, `raw` markdown, `citations`.

## Gotchas
- Section numbers may include governance extensions (e.g. `NN.99`).
- Local-only path under the AGEINT checkout (`projects/ongoing/docxology/AGEINT` in the template workspace); AGEINT itself is public (Zenodo DOI 10.5281/zenodo.20732274) but this checkout is not committed from here.
