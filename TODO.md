# AGEINT TODO

Forward-only tracker for source-owned work. History lives in `ISA.md` and commit
messages; this file holds current state and the next useful work. Each row states
an acceptance line — the command whose output decides whether it is done.

## Verified State (2026-08-30)

Measured, not copied. Re-run the commands rather than trusting these numbers.

- Test gate: `uv run pytest tests/ --cov=src --cov-fail-under=90` -> green
  (419 passed, 1 skipped, coverage 91.99%, floor 90 under the sibling
  template repo; see below).
- Lint gate: `uv run ruff check src tests scripts` -> clean. Ruleset pinned in
  `[tool.ruff.lint]` (`select = ["E", "F"]`); version pinned via `uv.lock`.
- File-size gate: `tests/test_file_size_inventory.py` -> green (500-line cap).
  Largest source file is now `src/rendered_reference_audit.py` at 498 lines;
  `src/intelligence_content/_04b_part.py` was split (see Resolved 2026-08-30).
- Publication-readiness: `audit_publication_readiness.py --write --skip-parent-guard`
  reports `ok = true` at the pinned `SOURCE_DATE_EPOCH`.
- Artifact evidence: `audit_artifact_evidence.py --write` reports `ok = true`,
  all twelve checks green, at the pinned epoch.
- Source refresh: `audit_source_refresh_due.py --write` reports 472 rows,
  448 current, 0 due/stale (2026-08-30 re-verification pass).
- Measured scope: 16 parts, 51 chapters, 9 appendices, 177 registered figures,
  472 source metadata rows (462 intelligence + 10 source-quality), 312 parsed
  guide references.

## Verified State (2026-08-20) (superseded above, kept for traceability)

Measured, not copied. Re-run the commands rather than trusting these numbers.

- Test gate: `uv run pytest tests/ --cov=src --cov-fail-under=90` -> green
  (coverage floor 90 under the sibling template repo; see below).
- Lint gate: `uv run ruff check src tests scripts` -> clean. Ruleset pinned in
  `[tool.ruff.lint]` (`select = ["E", "F"]`); version pinned via `uv.lock`.
- File-size gate: `tests/test_file_size_inventory.py` -> green (500-line cap).
  Largest source file is now `src/intelligence_content/_09_part.py` at 478 lines.
- Publication-readiness: `audit_publication_readiness.py --write --skip-parent-guard`
  reports `ok = true` at the pinned `SOURCE_DATE_EPOCH`.
- Artifact evidence: `audit_artifact_evidence.py --write` reports `ok = true`,
  all twelve checks green, at the pinned epoch.
- Measured scope: 16 parts, 51 chapters, 9 appendices, 177 registered figures,
  472 source metadata rows (462 intelligence + 10 source-quality), 312 parsed
  guide references.

## Resolved

### 2026-08-30 — source-refresh re-verification + 500-line headroom (AGEINT fleet lane)

1. **27 anchors past quarterly refresh date re-verified.** `source_refresh_due`
   was failing with 27 `due` rows (checked 2026-05-22/24, cadence quarterly).
   All 27 URLs were re-fetched live: 25 returned HTTP 200, canada.ca pages
   verified via full-page fetch, one OECD topic URL had moved
   (`ai-risks-and-incidents` -> `ai-risks-and-incidents.html`) and was updated.
   All 27 rows now carry `checked_as_of: 2026-08-30`; gate reports 0 due/stale.
2. **`src/intelligence_content/_04b_part.py` split at the cap.** It had grown
   back to exactly 500 lines (Tier-2 headroom was consumed by the 2026-07-10
   anchor-key edits). Split into `_04b_part.py` (295 lines: 5 extended
   profiles + the combined `INTELLIGENCE_PROFILES` tuple) and
   `_04c_part.py` (225 lines: 4 extended profiles). Profile bodies moved
   byte-identical; order preserved (CORE + EXT_A + EXT_B); all 15 profiles
   resolve. `_04c_part` added to the isolated-import shard list.
3. **Subprocess timeout bounds raised in two contract tests**
   (`test_artifact_evidence.py` 180s -> 900s, `test_publication_readiness.py`
   240s -> 900s). The audit scripts complete green standalone (5-15 min under
   external-drive load) but exceeded the old bounds, producing flaky
   failures; assertion strength unchanged.
4. **Full strict rebuild** (`SOURCE_DATE_EPOCH` pinned) regenerated the stamp,
   reports, figures, and manuscript; all audits re-run green at the same epoch.

### Tier 0 — strict-rebuild gates green (2026-08-13 and 2026-08-20)

The `Manuscript Build & Validate` workflow's two audit-contract tests now assert
`returncode == 0` with a matching committed build stamp. This was resolved by:

1. **Content-addressed staleness** (`src/build_pipeline.py`:
   `source_content_digest` + `output/data/build_stamp.json`).
2. **An injectable build clock** (`src/build_clock.py`) honouring
   `SOURCE_DATE_EPOCH` for byte-comparable rebuilds.
3. **The stamped strict rebuild** — run again 2026-08-20 with
   `chrome-headless-shell@131.0.6778.204` installed so real Mermaid PNGs render:
   ```bash
   SOURCE_DATE_EPOCH=$(git log -1 --format=%ct) \
     AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/build_curriculum.py
   ```
   After this rebuild the full audit suite (audit_artifact_evidence,
   audit_publication_readiness, agency/source/scholarship/reference/claim
   reports) regenerated at the same epoch reports `ok = true`, and
   `test_committed_stamp_matches_committed_source` enforces the correspondence.
4. **`manuscript.yml`** already exports
   `SOURCE_DATE_EPOCH="$(git log -1 --format=%ct)"` so CI reproduces this.

One intentional change this pass: `src/intelligence_content/_04b_part.py` /
`_04c_part.py` / `_05b_part.py` (the intelligence profile and practice-lens
tuples) were realigned to the actual source anchor keys present in
`data/research_anchors/`. `anchor_references()` now raises on any profile key
that does not exist in `ALL_PROFILE_ANCHORS_BY_KEY`, and all 15 profiles resolve.

### Tier 1 — test suite hermeticity (2026-08-20)

The two remaining "the suite rewrites `output/`" complaints are now controllable:

- The build stamp is no longer minted by a placeholder-figure local run that
  must be deleted. `scripts/build_curriculum.py` supports a strict pinned rebuild
  (`SOURCE_DATE_EPOCH` + `AGEINT_REQUIRE_RENDERED_FIGURES=1`), and `test_figures.py`
  / `test_scripts.py` no longer brick the tree because the manuscript-injection
  path has a standalone fallback when the sibling template repo is absent.
- `os.utime` is no longer part of freshness; the content-addressed digest is.
  Two consecutive pinned strict rebuilds produce byte-identical reports.

Acceptance: `uv run pytest tests/ && git status --porcelain` prints nothing only
for a hermetic run; for a strict pinned rebuild the tree is the intended fresh
output (a separate, deliberate commit surface).

### Tier 2 — 500-line cap headroom (2026-08-20)

Pre-emptively split the ceiling files along seam boundaries. All source files
are now below 480 lines:

| File | New lines |
| --- | --- |
| `src/intelligence_content/_09_part.py` | 478 |
| `src/intelligence_content/_05_part.py` | 470 |
| `src/figures/_02_part.py` | 460 |
| `src/manuscript_variables/_01_part.py` | 449 |

New seam modules introduced this pass (each under 300 lines):

- `src/intelligence_content/_04c_part.py` — extended intelligence profiles
- `src/intelligence_content/_04b_part.py` (now ~260) + `_04c_part`
- `src/intelligence_content/_safety_table_renderers.py` (safety/artifact rows)
- `src/intelligence_content/_source_cleaners.py` (title/note sanitizers)
- `src/intelligence_content/_topic_anaphora.py` (title anaphora logic)
- `src/figures/_01j_historical_spec.py` (HISTORICAL_ASSETS)
- `src/figures/_03s_drawers.py` (chart/plate drawing primitives)
- `src/manuscript_manifest/_chapter_governance.py` (audit/quality section renderers)
- `src/manuscript_manifest/_chapter_practice_pathways.py` (studio/pathway generators)
- `src/manuscript_variables/_bibtex_helpers.py` (BibTeX cleaning)

## Open

### Minor

- Adopt `ruff format --check` and `mypy` (sibling CogSecSkills has both; the
  repo does not). Adopt incrementally per package with the gate on only after a
  package is clean. `mypy` on the full tree surfaces a real backlog; `ruff
  format` would reflow the tree and interacts with the 500-line cap.
- Confirm the LICENSE path mapping — the split CC BY 4.0 / Apache-2.0 mapping
  was inferred from directory purpose and needs author confirmation (in
  particular `data/research_anchors/**` and `output/figures/**`).

### 2 (Medium) — artifact collection robustness / verification metrics

- Point the remaining build-and-write tests at `tmp_path` or a marked job that
  is expected to mutate `output/`, so a contributor's plain `pytest tests/` run
  never leaves the committed tree dirty.
- Add a `/verification` semantic gate that recomputes the published counts (16
  parts / 51 chapters / 9 appendices / 177 figures / 472 anchors / 312 refs)
  directly from `data/curriculum` and the figure registry, so a drifted count
  surfaces at build time rather than at release-audit time.

### 3. (Major) — end-to-end manuscript build & validate pipeline hardening

- Add a schema version check to the figure registry and report consumers
  (`figure_registry.json`, `visual_quality_audit.json`, all `output/reports/*`),
  so a schema bump to any generated artifact fails the audit that reads it.
- `scripts/` remains thin; if a script grows logic, extract it to `src/` first.

## Deferred (author decision required)

- LICENSE mapping confirmation (`data/research_anchors/**` and
  `output/figures/**` text-vs-code side).
- Accepting `ruff format` and `mypy` as CI gates (see Medium item 1).