# AGENTS.md — `AGEINT/.github/workflows`

GitHub Actions workflow definitions.

## Layout

- `ci.yml`: locked Ruff, explicitly limited standalone Python compatibility checks, and required complete SDK verification.
- `manuscript.yml`: reusable complete verification, manual verification and weekly rebuild.
- `release.yml`: manual-only new-version publication after complete exact-main verification.
- `source-freshness.yml`: source refresh-due audits.

## Contracts

- The complete gate checks out `docxology/template` at `refs/tags/v5.2.0` at workspace root and exact AGEINT Source under its working projects directory. Never replace that tag with main or a fallback.
- Manual development verification alone may explicitly select an immutable 40-hex SDK candidate SHA via `sdk-candidate`. No reusable/release override is exposed. Candidate runs retain full acceptance and record actual SDK SHA/version but never authorize publication.
- Reuse SDK setup actions, frozen dev/rendering dependencies and canonical `stage_03_render.py`; do not add a second Pandoc driver here.
- SDK execution uses Python 3.14 with an explicit shared interpreter/environment and `UV_NO_SYNC=1`, including nested `uv` subprocesses. This does not raise AGEINT's standalone Python floor.
- Full acceptance requires real Mermaid rendering, at least 90% coverage, SDK PDF/HTML validation, all artifact/source/license/reference aggregates and an actually-run all-resource parent guard. Never ignore required failures or restore old output after failure.
- Render current readers before PDF consumer tests. Tests must use isolated
  fixtures; before/after reader-byte inventories refuse mutation rather than
  silently rebuilding over it. Limited standalone jobs test the declared Python
  floor and require an up-to-date lock; their lower coverage bar is not release acceptance.
- Successful exact-run artifacts alone are downloadable by release. Reader ZIP layout retains `web/` beside `figures/` and local browser assets.
- Inspection-only generated snapshots are retained before task/readiness closure
  so maintainers can inspect real readers without inventing completed tasks.
  Their explicit non-acceptance identity and distinct artifact name must never
  satisfy release handoff. Failure diagnostics are likewise not verified assets.
- Serve the extracted bundle root over local HTTP and visit `/web/index.html`; do not promise every browser feature under `file://`. Scholarly URLs are user-clicked references, never runtime asset dependencies.
- Publication checks stable-tag metadata, verifies exact main Source before verification and immediately before creating the tag, and refuses existing tags/releases. Never force, overwrite, clobber or publish from ordinary CI alone.
- A skipped guard is not acceptance. No workflow publishes except explicit `release.yml` dispatch; editing these files never authorizes a real release.
