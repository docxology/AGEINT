# AGENTS.md - AGEINT Data

Treat `data/curriculum/` as the committed runtime spine. Optional guide input
`SIST-Guide-TOC-and-Bibliography-v2.md` may be present locally, but normal builds
reload from the sharded curriculum directory.

If counts, titles, citations, appendices, profile identifiers, or pattern data
drift, fix the shards or `src/curriculum.py`, rebuild with
`uv run python scripts/build_curriculum.py`, and run the AGEINT tests.
Downstream manuscript paths, variables, figure assignments, and bibliography
rows depend on this shape.

Keep intelligence, cyber, influence, and ICS content framed as defensive
curriculum material. No live targeting, unauthorized collection, exploitation,
evasion, manipulation, covert tasking, or operational response instructions
belong here.
