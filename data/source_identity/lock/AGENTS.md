# AGENTS.md — `AGEINT/data/source_identity/lock`

The source-identity lock files.

## Layout
- `source-identity-001-075.jsonl`, `…076-150.jsonl`, `…151-225.jsonl`, `…226-231.jsonl` — 231 locked source identities across 4 shards.

## Gotchas
- Content-invariant: do not rewrite identity keys or merge shards; the lock is referenced by citation and audit tooling.
- Local-only path under the AGEINT checkout (`projects/ongoing/docxology/AGEINT` in the template workspace); AGEINT itself is public (Zenodo DOI 10.5281/zenodo.20732274) but this checkout is not committed from here.
