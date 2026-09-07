# AGENTS.md — `AGEINT/data/source_identity`

Source-identity metadata for the AGEINT source corpus (`ageint001`-`ageint231`).

## Layout
- `metadata.json` — identity-scheme metadata.
- `lock/` — the identity lock: 4 JSONL shards covering identities 001-231.

## Gotchas
- The lock is the provenance invariant: citations resolve to locked identities; preserve identity keys when extending sources.
- Local-only path under the AGEINT checkout (`projects/ongoing/docxology/AGEINT` in the template workspace); AGEINT itself is public (Zenodo DOI 10.5281/zenodo.20732274) but this checkout is not committed from here.
