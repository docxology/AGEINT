# AGENTS.md — `AGEINT/data/source_identity/lock`

The source-identity lock files.

## Layout
- `source-identity-001-075.jsonl`, `…076-150.jsonl`, `…151-225.jsonl`, `…226-231.jsonl` — 231 locked source identities across 4 shards.

## Gotchas
- Content-invariant: do not rewrite identity keys or merge shards; the lock is referenced by citation and audit tooling.
- AGEINT is a public repository (Zenodo DOI 10.5281/zenodo.20732274); its contents are committed here.
