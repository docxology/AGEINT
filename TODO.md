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

**Both halves of the mechanism now exist. One adoption step remains.**

1. *Content-addressed staleness* — **implemented.** `source_content_digest`
   hashes each source path plus its bytes in sorted order;
   `write_build_stamp` records the digest to `output/data/build_stamp.json` as
   the last step of `run_build`; `generated_output_is_stale` compares digests
   when a stamp is present and keeps the mtime heuristic only as the fallback for
   un-stamped trees, so nothing regresses. Verified: the digest is unchanged by
   `os.utime`, unchanged across two checkout locations, and changes on a
   one-byte content edit.
2. *An injectable clock* — **implemented** (`src/build_clock.py`, see above), so
   a rebuild at a pinned `SOURCE_DATE_EPOCH` is byte-comparable.

**Remaining: one stamped rebuild.** `output/` carries no stamp yet, so freshness
still falls back to mtimes and the failing tests still fail.
`tests/test_build_stamp.py::test_committed_stamp_matches_committed_source` skips
until that lands and then enforces it automatically.

The stamp was deliberately **not** minted without rebuilding — writing a digest
that claims the committed output came from the current source, when it did not,
would be worse than the mtime bug it replaces. Doing it properly needs a strict
rebuild, which needs `chrome-headless-shell` for the real Mermaid PNGs:

```bash
npx --yes puppeteer browsers install chrome-headless-shell@131.0.6778.204
SOURCE_DATE_EPOCH=$(git log -1 --format=%ct) \
  AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/build_curriculum.py
```

Without that browser the build writes placeholder PNGs over the published
figures, so never run a non-strict rebuild for this purpose.

3. *Still open — separate the two claims the tests conflate.* Even with a stamp,
   consider that each test's name says `writes_json_contract` — the JSON shape and
   the written report files — while the body also asserts release readiness via
   `returncode == 0`. `.github/workflows/ci.yml` runs the same script with
   `continue-on-error: true` and documents that its `ok` "only turns true once
   both [known pre-existing gaps] are cleared and a release is actually being
   prepared", so the suite asserts an exit code the project's own CI documents as
   legitimately non-zero pre-release. Splitting the two keeps all coverage.

Deliberately **not** patched by relaxing an assertion: that would turn a real
signal green without changing what it measures.

**The deeper problem, and why fix (1) alone is not enough.** *Both* freshness
signals this workflow relies on are noise-dominated, because the generated
artifacts are not reproducible:

- Reports embed wall-clock. `output/reports/*.md` carry a `Generated at` field,
  and date-relative fields move on their own: `source_refresh_due` went
  `Current 445 -> 431`, `Due soon 27 -> 41` between 2026-08-03 and 2026-08-12
  with no source change, because anchors aged past their thresholds.
- Figure PNGs embed the renderer version. Measured `bytes 302267 -> 301875` for
  one figure across runs; matplotlib writes its version into the PNG `Software`
  text chunk, so a toolchain bump alone changes every figure's bytes.

That is why the job's other signal — the "Fresh strict rebuild differs from the
committed output/ tree" annotation — also fires on every run and cannot
distinguish real drift from timestamp churn. Making the artifacts reproducible is
the root fix, and it is a project rather than a patch:

- Pass `metadata={"Software": None}` (and any date field) to matplotlib
  `savefig` so figure bytes depend only on figure content.
- Make the "as of" date an injected parameter rather than `today()`, so a report
  is a pure function of (source, date) and CI can pin the date.
- Move `Generated at` out of the committed artifact, or exclude it from
  comparison explicitly.

**The enabling mechanism now exists: `src/build_clock.py`.** Every report clock
routes through it, and it honours `SOURCE_DATE_EPOCH` (the cross-ecosystem
reproducible-builds convention). Pinning it makes a rebuild reproducible in both
respects — verified 2026-08-13:

```
$ SOURCE_DATE_EPOCH=1781699696 uv run python -c "...collect_source_refresh_due..."
generated_at 2026-06-17T12:34:56+00:00   bucket_counts {"current": 472}
# unpinned, same commit: generated_at = now, bucket_counts {"current": 431, "due_soon": 41}
```

Both the timestamp *and* the date-derived buckets become a function of the pinned
instant, so two rebuilds at one epoch agree. What remains is adopting it:

- Set `SOURCE_DATE_EPOCH` in `manuscript.yml`'s strict-rebuild job, then
  regenerate and commit `output/` once at that epoch so the committed tree and a
  fresh rebuild are comparable. Until that one-time regeneration, the committed
  reports still carry real timestamps and the drift check still fires.
- Decide the epoch policy: a fixed release epoch (fully stable, but "as of" dates
  freeze until bumped) or the commit timestamp via
  `git log -1 --format=%ct` (moves per commit, still reproducible for that
  commit). The second is usually what projects want.

Only once artifacts are reproducible does either freshness check become a signal
worth gating on. Until then, prefer fix (2) — separate the contract assertion
from the readiness assertion — and treat drift as informational, which is what
`ci.yml` already does.

- Acceptance: `gh run list --workflow="Manuscript Build & Validate" --limit 1`
  reports success, and the chosen fix is recorded in `ISA.md` under Decisions.
- Acceptance for reproducibility: two consecutive
  `AGEINT_REQUIRE_RENDERED_FIGURES=1` rebuilds on one commit produce
  byte-identical `output/figures/*.png` and byte-identical `output/reports/*`.

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

The build stamp makes this sharper. `run_build` now writes
`output/data/build_stamp.json`, and because the suite runs a real build against
the repository tree, **running the tests mints a stamp** — observed 2026-08-13.
That stamp records a *placeholder-figure* build (no `chrome-headless-shell`
locally), so committing it would assert a correspondence to a build nobody wants
published. Until the tests are hermetic, delete the stamp after a local run
unless it came from a deliberate strict rebuild:

```bash
uv run pytest tests/ ; git checkout -- output/ && rm -f output/data/build_stamp.json
```

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

## Tier 2: confirm the LICENSE path mapping

`LICENSE` now exists and encodes the split `README.md` already declared ("text
CC BY 4.0; code Apache-2.0"), mapping CC BY 4.0 onto `data/curriculum/**`,
`manuscript/**`, `output/manuscript/**`, `docs/**`, `AGEINT.pdf`,
`output/pdf/**`, `output/figures/**`, `data/research_anchors/**`, and Apache-2.0
onto `src/**`, `scripts/**`, `tests/**`, `pyproject.toml`, `.github/**`. The
Apache-2.0 body is the canonical unmodified text (byte-identical to the sibling
CogSecSkills `LICENSE`).

**That path mapping was inferred from directory purpose, not from an explicit
statement, so it needs author confirmation.** In particular decide whether
`data/research_anchors/**` (curated citation metadata) and `output/figures/**`
(generated assets) belong on the text or the code side.

- Acceptance: the mapping in `LICENSE` is confirmed or corrected by the author.

## Tier 3: absent lint and type gates the sibling repo has

CogSecSkills gates on `ruff format --check` and `mypy`; AGEINT gates on neither.
Both are worth adopting, and both are wide changes rather than free wins —
`ruff format` would reflow the tree (and interacts with the 500-line cap), and
`mypy` on 208 files will surface a real backlog. Adopt incrementally, per
package, with the gate turned on only once that package is clean.

- Acceptance: CI runs both, and `[tool.mypy]` lists the packages already covered.
