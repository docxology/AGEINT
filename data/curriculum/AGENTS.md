# AGENTS.md — `data/curriculum`

runtime source of the AGEINT curriculum data: the semantic representation of the 16-part, 51-chapter atlas.

## Layout
- `metadata.json` — project title metadata.
- `stats.json` — measured counts (parts, chapters, appendices, patterns, references).
- `patterns.json` — curriculum pattern registry.
- `parts/` — one directory per part, each with `part.json` and `chapters/<NN-slug>/` holding `chapter.json` (number, title, citations, content profile) and `sections.jsonl` (one JSON object per section: level, number, raw markdown, citation keys).
- `appendices/` — appendix A-I JSON payloads.
- `references/` — parsed source-guide reference shards (`source-guide-*.jsonl`).

## Gotchas
- This is the source spine: edits here flow into `output/` only via a `scripts/build_curriculum.py` rebuild.
- Section numbering in `sections.jsonl` includes governance/extension sections (e.g. `1.99`) beyond the human-facing chapter numbering.
- Local-only path under the AGEINT checkout (`projects/ongoing/docxology/AGEINT` in the template workspace); AGEINT itself is public (Zenodo DOI 10.5281/zenodo.20732274) but this checkout is not committed from here.
