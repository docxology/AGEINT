# AGENTS.md — `AGEINT/data/research_anchors`

Curated research-anchor registry backing AGEINT citations.

## Layout
- 10 JSONL shard files (`intelligence-anchors-001-050.jsonl` …), ~462 anchors total, one JSON object per line with keys: `key`, `author`, `domain`, `citation_role`, `source_lane`, `source_tier`, `claim_scope`, `assurance_use`, `checked_as_of`, `refresh_cadence`, `refresh_trigger`, `rights_dimension`, `stakeholder_role`, `note`.
- `citation-expansion-2026-06-16-report.json` — report from the 2026-06 citation expansion pass.

## Gotchas
- Source metadata is explicit per anchor (checked dates, refresh triggers); `scripts/audit_source_refresh_due.py` consumes these fields.
- Local-only path under the AGEINT checkout (`projects/ongoing/docxology/AGEINT` in the template workspace); AGEINT itself is public (Zenodo DOI 10.5281/zenodo.20732274) but this checkout is not committed from here.
