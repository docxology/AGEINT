# AGEINT TODO

Forward-only tracker for source-owned work. History lives in `ISA.md` and commit
messages; this file holds current state and the next useful work. Each row states
an acceptance line — the command whose output decides whether it is done.

## Verified State (2026-08-13)

Measured, not copied. Re-run the commands rather than trusting these numbers.

- Test gate: `uv run pytest tests/ --cov=src --cov-fail-under=90` ->
  `394 passed, 1 skipped`, `91.84%` coverage (floor 90).
- Lint gate: `uv run ruff check src tests scripts` -> clean. Ruleset pinned in
  `[tool.ruff.lint]`; version pinned via `uv.lock` (`ruff==0.16.2`).
- File-size gate: `tests/test_file_size_inventory.py` -> green (500-line cap on
  all `.py`/`.md`/`.json`/`.yaml`/`.toml` under the included roots).
- CI `CI` workflow: green (Lint, Content & Scholarship Gates, Test py3.10, py3.12).
- CI `Manuscript Build & Validate` workflow: **red** — see Tier 0 below.
- Measured scope: 16 parts, 51 chapters, 9 appendices, 177 registered figures,
  462 research anchors, 10 source-quality support anchors, 312 parsed guide
  references. All seven verified against the live tree 2026-08-12.

## Tier 0: `Manuscript Build & Validate` has been red since at least 2026-07-27

Failing runs: 30282225037 (07-27), 30829743498 (08-03), 31403445967 (08-10),
31654561415 (08-13). Two tests fail in the strict-rebuild job:

- `tests/test_artifact_evidence.py::test_audit_artifact_evidence_script_writes_json_contract`
- `tests/test_publication_readiness.py::test_audit_publication_readiness_script_writes_json_contract`

Both assert `result.returncode == 0`. Of publication-readiness's 16 checks
exactly one is false — `artifact_evidence_ok` — which resolves to
`generated_output_fresh` in `collect_artifact_evidence`
(`src/artifact_evidence.py:72`).

**Root cause.** `generated_output_is_stale` (`src/build_pipeline.py:89`) compares
the newest **mtime** among `source_freshness_roots()` against the oldest mtime
among `output_build_sentinels()`. Git does not preserve mtimes, so after any
clone or `git checkout` every file carries approximately the checkout time in
arbitrary order, and the comparison no longer means "source changed after the
build". `STALE_OUTPUT_TOLERANCE_SECONDS = 30.0` widens the window but cannot
make the signal meaningful.

This makes the outcome **environment- and ordering-dependent, not deterministic**.
Observed locally on the same commit within one session: the standalone
`scripts/audit_artifact_evidence.py` reported `ok: true` with all twelve checks
true, while the aggregating publication-readiness run reported
`artifact_evidence_ok: false`; and the publication-readiness test failed in one
full-suite run and passed in the next with no source change between them.

**Two candidate fixes — this needs a decision, not a patch.**

1. *Content-addressed staleness.* Hash the bytes of every
   `source_freshness_roots()` path, write the digest to a build stamp under
   `output/data/`, and compare digests instead of mtimes. Deterministic and
   clone-safe. Two consequences to weigh first: it requires a full rebuild to
   mint the first stamp, and `pyproject.toml` currently sits in the freshness
   roots, so an unrelated edit (a `[tool.ruff]` change, say) would mark the
   manuscript stale even though no generated content depends on it. The roots
   list probably wants narrowing in the same change.
2. *Separate the two claims the tests conflate.* Each test's name says
   `writes_json_contract` — the JSON shape and the written report files — but the
   body also asserts release readiness via `returncode == 0`. Note
   `.github/workflows/ci.yml` already runs the same script with
   `continue-on-error: true` and documents that its `ok` "only turns true once
   both [known pre-existing gaps] are cleared and a release is actually being
   prepared". So the suite currently asserts an exit code the project's own CI
   documents as legitimately non-zero pre-release. Splitting the contract
   assertion from the readiness assertion would keep all coverage.

Deliberately **not** patched by relaxing an assertion: that would turn a real
signal green without changing what it measures.

- Acceptance: `gh run list --workflow="Manuscript Build & Validate" --limit 1`
  reports success, and the chosen fix is recorded in `ISA.md` under Decisions.

## Tier 1: the test suite is not hermetic

Running `uv run pytest tests/` rewrites tracked files under `output/` — 19 of
them, measured 2026-08-12. A contributor who runs the suite gets a dirty tree
and may commit build noise without meaning to.

Compounding it, some generated reports embed wall-clock and therefore drift
daily by construction: between 2026-08-03 and 2026-08-12,
`output/reports/source_refresh_due.md` moved `Current 445 -> 431` and
`Due soon 27 -> 41` with no source change, purely because anchors aged past
their refresh thresholds. `Generated at` timestamps guarantee diff noise on
every regeneration.

- Point the build fixtures at `tmp_path` for test runs, or split the
  build-and-write tests into a marked job that is expected to mutate `output/`.
- Consider whether date-relative report fields belong in committed artifacts at
  all, versus being computed at read time.
- Acceptance: `uv run pytest tests/ && git status --porcelain` prints nothing.

## Tier 2: 500-line cap headroom

`tests/test_file_size_inventory.py` enforces `MAX_LINES = 500` repo-wide. Files
now sitting at the ceiling, where the next edit fails the gate with no room:

| File | Lines |
| --- | --- |
| `src/intelligence_content/_04b_part.py` | 500 |
| `src/manuscript_manifest/_03_part.py` | 499 |
| `src/intelligence_content/_11_part.py` | 498 |
| `src/manuscript_manifest/_02_part.py` | 496 |
| `src/intelligence_content/source_grounding.py` | 496 |
| `src/figures/_01_part.py` | 496 |

Split the top few pre-emptively along their existing internal seams. Note the
prefix convention is a *layer*, not a load order — `figures/__init__.py` imports
by explicit name — so a split may take a semantic name rather than another
letter suffix. See `src/figures/AGENTS.md`.

- Acceptance: `git ls-files 'src/**/*.py' | xargs wc -l | sort -rn | head -5`
  shows no file above 480.

## Tier 2: no LICENSE file

`README.md` declares "text CC BY 4.0; code Apache-2.0" and `CITATION.cff` /
`codemeta.json` now record both, but the repository has no `LICENSE`. A public,
DOI-bearing repo should carry the actual instrument. This needs an author
decision on which paths fall under which licence (the text/code split is not
inferable from the tree), so it is intentionally left unauthored here.

- Acceptance: `LICENSE` exists and states the split explicitly.

## Tier 3: absent lint and type gates the sibling repo has

CogSecSkills gates on `ruff format --check` and `mypy`; AGEINT gates on neither.
Both are worth adopting, and both are wide changes rather than free wins —
`ruff format` would reflow the tree (and interacts with the 500-line cap), and
`mypy` on 208 files will surface a real backlog. Adopt incrementally, per
package, with the gate turned on only once that package is clean.

- Acceptance: CI runs both, and `[tool.mypy]` lists the packages already covered.
