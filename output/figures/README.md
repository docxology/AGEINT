# AGEINT Figures

This generated directory contains registry-backed visual assets for `output/manuscript/`. The registry is `figure_registry.json`; manuscript sections cite figures by Pandoc-crossref labels such as `[@fig:ageint-curriculum-map]` rather than hard-coded figure numbers.

## Asset classes

- `mermaid/`: generated Mermaid source (`.mmd`) and square-normalized PNG renders.
- `python/`: deterministic charts and matrices drawn from parsed curriculum data.
- `historical/`: public-domain USGS imagery with provenance retained in the registry.
- `ai/`: deterministic synthetic concept plates; no real targets, people, or logos.

All PNGs are normalized onto a square canvas so generated and inserted figures remain stable across PDF, web, and slide-oriented layouts. `figure_registry.json` also stores captions, short alt text, long descriptions, provenance, hashes, and official accessibility-guidance metadata for rendered-output validation. The PNG files also embed a compact AGEINT metadata contract in text chunks so label, caption, alt text, long description, source section, and provenance travel with the image if it is inspected outside the registry. `visual_quality_audit.json` records the rendered-asset checks that tie the registry, PNG metadata, and readable local files together.

Refresh with `uv run python scripts/generate_figures.py` or the full `scripts/build_curriculum.py` build from the AGEINT root.
