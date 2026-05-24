# AGEINT Data

This folder holds the committed curriculum spine for AGEINT.

- Owner: AGEINT parser and build pipeline.
- Primary spine: `data/curriculum/` sharded JSON (parts, chapters, appendices, patterns, references).
- Optional archive input: `SIST-Guide-TOC-and-Bibliography-v2.md` when present locally.
- Refresh: `uv run python scripts/build_curriculum.py` from the AGEINT root.
- Safety: data supports educational, authorized, synthetic, defensive, and non-operational workflows only.

`data/curriculum/` is the runtime source of truth for parts, chapters, appendices,
patterns, and parsed `ageintNNN` references. Each chapter shard may also declare
`content_profile` and `practice_lens` identifiers used by the manuscript renderer.
The build also writes a compact mirror at `output/data/curriculum_outline.json`.

`data/source_identity/` preserves the original `ageint001` through `ageint231`
source identities. New source-guide references are append-only after that locked
range and currently extend through `ageint296`.

`data/research_anchors/` stores JSONL shards for intelligence research anchors
loaded at runtime by `src/intelligence_content/`.
