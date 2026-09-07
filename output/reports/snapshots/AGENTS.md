# AGENTS.md — `AGEINT/output/reports/snapshots`

GENERATED pipeline stage snapshots.

## Layout
- `stage-01-clean-output-directories.json` … `stage-08-copy-outputs.json` — per-stage run snapshots with artifact manifest hashes, evidence fact counts, and paths.

## Gotchas
- Produced by the pipeline run (stage snapshots); hashes reflect the run that produced them — regenerate by re-running the pipeline, not by editing.
- Local-only path under the AGEINT checkout (`projects/ongoing/docxology/AGEINT` in the template workspace); AGEINT itself is public (Zenodo DOI 10.5281/zenodo.20732274) but this checkout is not committed from here.
