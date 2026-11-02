# AGENTS.md — `AGEINT/data/source_identity`

Source-identity metadata for the AGEINT source corpus (`ageint001`-`ageint231`).

## Layout
- `metadata.json` — identity-scheme metadata.
- `lock/` — the identity lock: 4 JSONL shards covering identities 001-231.

## Gotchas
- The lock is the provenance invariant: citations resolve to locked identities; preserve identity keys when extending sources.
- AGEINT is a public repository (Zenodo DOI 10.5281/zenodo.20732274); its contents are committed here.
