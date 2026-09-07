# AGEINT TODO

Forward-only tracker for source-owned work. History lives in `ISA.md` and commit
messages; this file holds current state and the next useful work. Each row states
an acceptance line — the command whose output decides whether it is done.

## Verified State (2026-09-07)

Measured, not copied. Re-run the commands rather than trusting these numbers.

- Test gate: `uv run pytest tests/ --cov=src --cov-fail-under=90` -> green
  (437 passed, coverage 91.70%, floor 90).
- Lint gate: `uv run ruff check src tests scripts` -> clean. Ruleset pinned in
  `[tool.ruff.lint]` (`select = ["E", "F"]`); version pinned via `uv.lock`.
- File-size gate: `tests/test_file_size_inventory.py` -> green (500-line cap).
- Publication-readiness: `audit_publication_readiness.py --write --skip-parent-guard`
  -> `ok = true` (exit 0, 2026-09-07 re-run after the canonicalization rebuild).
- Artifact evidence: `audit_artifact_evidence.py --write` -> `ok = true`
  (exit 0, 2026-09-07 re-run).
- Source refresh: `audit_source_refresh_due.py --write` -> 472 rows, 0 due/stale
  (2026-09-07 re-run).
- Measured scope: 16 parts, 51 chapters, 9 appendices, 177 registered figures,
  472 source metadata rows (462 intelligence + 10 source-quality), 312 parsed
  guide references (rebuild log 2026-09-07).

## Open

### 1 (Medium) — fail source validation when the manuscript config is missing

`_write_generated_config()` (`src/manuscript_manifest/_05_part.py`) now hard-fails
on a missing `docs/manuscript/config.yaml` at render time (added 2026-09-07; see
Resolved). Move the check earlier: `validate_declarative_tables()` in
`src/_data_loaders.py` (the `source_validation` stage) should assert the file
exists so a broken tree fails before any figure-rendering work, not after.

Acceptance: on a scratch copy with `docs/manuscript/config.yaml` deleted,
`uv run python scripts/build_curriculum.py` exits non-zero naming the missing
config before rendering any figures.

### 2 (Minor) — regenerate `docs/manuscript/config.yaml.example`

The example predates the current shape: it has no `book:` section (license,
code_license, cover) and no `front_matter:` block, while
`collect_source_license_posture()` reads exactly those keys from
`docs/manuscript/config.yaml`. Regenerate the example from the real config with
placeholder values so a copy-to-config workflow produces a gate-green file.

Acceptance: `docs/manuscript/config.yaml.example` contains `book.license` and
`book.code_license` keys.

## Deferred (author decision required)

- Adopt `ruff format --check` and `mypy` as CI gates (sibling CogSecSkills has
  both). `ruff format` would reflow the tree and interacts with the 500-line
  cap (line-length is pinned at 200 with `skip-magic-trailing-comma` for that
  reason); `mypy` on the full tree surfaces a real backlog. Adopt incrementally
  per package with the gate on only after a package is clean.
- Confirm the LICENSE path mapping — the split CC BY 4.0 / Apache-2.0 mapping
  was inferred from directory purpose and needs author confirmation (in
  particular `data/research_anchors/**` and `output/figures/**`).

## Resolved

### 2026-09-07 — manuscript canonicalization completed (`docs/manuscript/` is the only manuscript source dir)

The 2026-08-31 migration to `docs/manuscript/` left a shadow legacy surface:
`src/` still read config/templates/preamble from top-level `manuscript/`, the
build still wrote BibTeX there, several tests still asserted against it, and
commit `d44e3e7` partially resurrected the directory with a byte-identical
duplicate of `docs/manuscript/` content. Consequences on `main` before this
pass: 6 red tests, and `output/manuscript/config.yaml` silently lost its
`book`/`paper` sections (generated config fell back to empty when the legacy
`manuscript/config.yaml` was absent, until `d44e3e7` masked it). Completed:

1. **Legacy path removed.** `manuscript/` (19 files, 6349 lines; 17 byte-identical
   duplicates of `docs/manuscript/`, 2 fresher copies of
   `references-research-anchors-151-200.bib` / `-201-250.bib` carrying the
   2026-09-06 anchor re-verification dates) deleted via `git rm`.
2. **Source repointed to `docs/manuscript/`.** `_write_generated_config()`,
   `render_manuscript()` templates + preamble reads
   (`src/manuscript_manifest/_05_part.py`), `write_template_library()` +
   `write_bibtex_files()` targets (`src/build_pipeline.py`), stage-contract
   input/output paths (`src/orchestration_contracts.py`), and
   `collect_source_license_posture()` config read + issue surface labels
   (`src/publication_readiness.py`).
3. **Missing-config silent fallback replaced with a hard fail**
   (`_write_generated_config` raises `FileNotFoundError` naming the missing
   path) — the exact silent-corruption path that produced the degraded output
   config. `tests/test_build_curriculum_script.py::test_missing_source_config_fails_the_build`
   covers it; tmp-project fixtures now carry a minimal source config.
4. **Bibliography drift closed.** The build now refreshes the canonical
   `docs/manuscript/references-*.bib` (matching README's documented contract);
   the two stale shards again carry `Checked as of 2026-09-06` for the 8
   re-verified anchors, and `output/manuscript/preamble.md` is produced again
   (the preamble copy had been silently skipped since the migration).
5. **Tests repointed and gaps fixed.** Template/config/preamble reads and
   required-folder lists in `test_cover_abstract_toc.py`,
   `test_manuscript_templates.py`, `test_manuscript_safety_docs.py`,
   `test_pdf_typography.py`, `test_manuscript_crossrefs.py`,
   `tests/manuscript_quality/inventory_helpers.py`; staleness and tmp-project
   fixtures in `test_scripts.py`, `test_build_curriculum_script.py`,
   `test_manuscript_variables.py`, `test_publication_readiness.py`. Also fixed
   three pre-existing red `test_publication_readiness.py` fixtures (registry
   payloads missing `schema_version: "1.5"` and `source_metadata.json` missing
   `schema_version: "1.0"` — the 2026-08-31 schema gate landed without a full
   -suite run) and two stale `manuscript/SYNTAX.md` link labels in
   `docs/rendering_pipeline.md` / `docs/syntax_guide.md` (targets were already
   correct; display text was pre-migration).
6. **Full rebuild + audits at `SOURCE_DATE_EPOCH=1788754689`**: regenerated
   `output/` (config.yaml with `book`/`paper` restored, fresh bibs, stamp
   matching the new source digest) and re-ran artifact-evidence /
   publication-readiness / source-refresh-due audits — all exit 0.
7. **16 `due_soon` anchors re-verified before their quarterly due dates** (rows
   checked 2026-06-11/14; NIST AI agent standards, MITRE ATLAS, MCP
   specification + security best practices, NIST AI 800-2 IPD PDF, NSA MCP
   security CSI, six intelligence.gov pages, three NSA pages, FBI
   counterintelligence). All 16 URLs re-fetched live: HTTP 200 (10
   bot-protected nsa.gov/intelligence.gov URLs verified via real-browser
   full-page fetch with matching page titles); rows bumped to
   `checked_as_of: 2026-09-07`. `audit_source_refresh_due` now reports 472
   rows, all current, 0 due/due-soon/stale, and
   `test_source_refresh_due_current_rows_are_not_due`'s pinned `as_of` moved to
   2026-09-07 per its own comment (the 2026-09-06 pass had left it at
   2026-08-30, below the newest `checked_as_of`, red since `231d552`).

Also closed from the previous Open list, verified 2026-09-07:

- **Entry-doc orientation ladder** (fixed 2026-08-31, verified): `README.md`
  and `AGENTS.md` link `TODO.md` as the canonical next-actions pointer; the
  "keep `output/` count prose synced" concern is covered by the published-counts
  gate, which recomputes counts from source at every build.
- **Medium 2 — artifact collection robustness / verification metrics**: both
  halves done. (a) Only two template-repo-guarded integration tests
  (`test_build_curriculum_script_smoke`, the `test_scripts.py` variables
  subprocess) run against the real `output/` tree, both documented and guarded
  by `requires_template_repo`; every other build-and-write test is
  `tmp_path`-isolated. (b) The `/verification` semantic gate is
  `src/published_counts_gate.py` (`verify_published_counts`, 116 lines), wired
  into `run_build` at `src/build_pipeline.py:201` with 7 focused tests in
  `tests/test_published_counts_gate.py`.
- **Major 3 — schema version check**: `src/schema_gate.py`
  (`require_schema_version` / `load_json_with_schema`) is wired into
  `artifact_evidence.py` and `publication_readiness.py`, with 6 negative-control
  tests in `tests/test_schema_gate.py`. It is load-bearing: this pass's fixture
  fixes were driven by it catching schema-less fixtures.
- **Major 3 — scripts stay thin**: enforced 2026-09-06 (commit `231d552`);
  `scripts/generate_topic_{prompt_routes,rotation_templates}_yaml.py` are thin
  wrappers over `src/topic_route_tables.py`, and the orchestration-contract
  audit gates the stage graph.

### 2026-09-06 — quarterly refresh re-verification + thin-orchestrator remediation (C08 scripts audit fleet)

1. **8 anchors past quarterly refresh date re-verified.** All 8 URLs re-fetched
   live: HTTP 200, no redirects (NIST AI 800-1 IPD PDF, A2A protocol, MITRE
   D3FEND, CycloneDX, NIST OSCAL, SLSA v1.1, in-toto, Sigstore docs). All 8
   rows now carry `checked_as_of: 2026-09-06`; `audit_source_refresh_due.py`
   reports 472 rows, 456 current, 0 due/stale.
2. **Canonical topic route tables moved out of scripts** (2026-09 scripts-audit
   remediation): `scripts/generate_topic_{prompt_routes,rotation_templates}_yaml.py`
   are now thin wrappers over `src/topic_route_tables.py`;
   `scripts/AGENTS.md`/`README.md` carry the full 23-script inventory.

### 2026-08-31 — docs/manuscript canonicalization committed (agent-ergonomics fleet)

The `manuscript/` -> `docs/manuscript/` migration (424 files moved, workflow
path updates, doc path-reference sweep, per-directory AGENTS/README stubs
across data/, output/, src/, tests/, .github/) was committed as `1285a63` and
pushed to `main`; the follow-up gates landed as `2b1cd51` (published-counts
verification gate + schema-version gate), the template-resolver canonical-path
fix as `9a7a842`, entry-doc ladder fixes as `333a06c`, and the comprehensive
improvement pass as `23a8903`. Completion of this migration's leftover shadow
paths is the 2026-09-07 Resolved entry above.

### 2026-08-30 — source-refresh re-verification + 500-line headroom (AGEINT fleet lane)

1. **27 anchors past quarterly refresh date re-verified.** `source_refresh_due`
   was failing with 27 `due` rows (checked 2026-05-22/24, cadence quarterly).
   All 27 URLs were re-fetched live: 25 returned HTTP 200, canada.ca pages
   verified via full-page fetch, one OECD topic URL had moved
   (`ai-risks-and-incidents` -> `ai-risks-and-incidents.html`) and was updated.
   All 27 rows now carry `checked_as_of: 2026-08-30`; gate reports 0 due/stale.
2. **`src/intelligence_content/_04b_part.py` split at the cap.** It had grown
   back to exactly 500 lines. Split into `_04b_part.py` (295 lines: 5 extended
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

The `Manuscript Build & Validate` workflow's two audit-contract tests assert
`returncode == 0` with a matching committed build stamp. Resolved by:

1. **Content-addressed staleness** (`src/build_pipeline.py`:
   `source_content_digest` + `output/data/build_stamp.json`).
2. **An injectable build clock** (`src/build_clock.py`) honouring
   `SOURCE_DATE_EPOCH` for byte-comparable rebuilds.
3. **The stamped strict rebuild** with `chrome-headless-shell@131.0.6778.204`
   so real Mermaid PNGs render:
   ```bash
   SOURCE_DATE_EPOCH=$(git log -1 --format=%ct) \
     AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/build_curriculum.py
   ```
4. **`manuscript.yml`** exports
   `SOURCE_DATE_EPOCH="$(git log -1 --format=%ct)"` so CI reproduces this.

One intentional change this pass: `src/intelligence_content/_04b_part.py` /
`_04c_part.py` / `_05b_part.py` were realigned to the actual source anchor keys
present in `data/research_anchors/`. `anchor_references()` raises on any
profile key that does not exist in `ALL_PROFILE_ANCHORS_BY_KEY`, and all 15
profiles resolve.

### Tier 1 — test suite hermeticity (2026-08-20)

- The build stamp is no longer minted by a placeholder-figure local run that
  must be deleted. `scripts/build_curriculum.py` supports a strict pinned
  rebuild (`SOURCE_DATE_EPOCH` + `AGEINT_REQUIRE_RENDERED_FIGURES=1`), and
  `test_figures.py` / `test_scripts.py` no longer brick the tree because the
  manuscript-injection path has a standalone fallback when the sibling template
  repo is absent.
- `os.utime` is no longer part of freshness; the content-addressed digest is.
  Two consecutive pinned strict rebuilds produce byte-identical reports.

Acceptance: `uv run pytest tests/ && git status --porcelain` prints nothing
only for a hermetic run; for a strict pinned rebuild the tree is the intended
fresh output (a separate, deliberate commit surface).

### Tier 2 — 500-line cap headroom (2026-08-20)

Pre-emptively split the ceiling files along seam boundaries. New seam modules
introduced (each under 300 lines): `src/intelligence_content/_04c_part.py`,
`src/intelligence_content/_safety_table_renderers.py`,
`src/intelligence_content/_source_cleaners.py`,
`src/intelligence_content/_topic_anaphora.py`,
`src/figures/_01j_historical_spec.py`, `src/figures/_03s_drawers.py`,
`src/manuscript_manifest/_chapter_governance.py`,
`src/manuscript_manifest/_chapter_practice_pathways.py`,
`src/manuscript_variables/_bibtex_helpers.py`.
