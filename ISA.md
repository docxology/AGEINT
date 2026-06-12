---
project: AGEINT
task: Verifier hardening, TODO execution, and current-ledger cleanup
effort: E5
phase: complete
started: 2026-06-03
updated: 2026-06-12
---

# AGEINT ISA Closeout And Current Ledger

## Historical Closeout

AGEINT's earlier manuscript-quality ISA is closed as historical work, not a live
blocker list. The useful lessons that remain binding are:

- Generated output is downstream. Fix `src/`, `data/`, templates, or manifest
  code, then rebuild before trusting `output/`.
- Strict figure rendering matters. PNG existence and registry rows are not proof
  that Mermaid diagrams rendered; use `AGEINT_REQUIRE_RENDERED_FIGURES=1` when
  figure truth is in scope.
- The source identity lock for `ageint001` through `ageint231` is immutable;
  append new source-guide references rather than renumbering.
- Dual-use material stays defensive, educational, authorized, synthetic, and
  non-operational.

Historical checkpoints from the closed ISA remain useful context only:

- Canonical Method & Assurance reference landed; the repeated mastery,
  competency, claim-ledger, and refresh tables were collapsed to canonical
  surfaces and cross-links.
- The original 7 synthesis methods figures landed and rendered, including the
  CDR cascade, MAESTRO, SRE circuit breaker, decoherence/CDR isomorphism,
  unified epistemic stack, cognitive attack layers, and HRO crosswalk.
- Later expansion increased the current project surface to 16 parts, 51
  chapters, 9 appendices, 312 source-guide references, 248 curated research
  anchors, and 161 registered figures.
- Previous URL follow-ups for OASIS CSAF and the International AI Safety Report
  are closed in the 2026-06-12 pass by switching to directly verified official
  pages.

## 2026-06-12 Verifier-Hardening Scope

The current pass executes the residual TODOs that were still real after the
later expansions:

- Add a non-stale generated-output oracle: `built_output` now rebuilds when
  source data, templates, scripts, or `src/` are newer than build sentinels.
- Add `source_citation_spine_inline(...)` so manifest prose can join citations
  mid-sentence without producing `]. and` or `]..`.
- Route chapter 36 STIX/TAXII, vulnerability scanner, inoculation, SBOM, and
  ICS/OT rows to precise `data/source_support_expansion.yaml` citations, while
  preserving non-default authored citations such as section `36.99`.
- Preserve authored lesson-title fragments through explicit bold phrasing rather
  than weakening the rendered-reference sanitizer's bare-crossref behavior.
- Relayout `ageint-maestro-seven-layer` to a top-to-bottom Mermaid graph.
- Refresh OASIS CSAF and International AI Safety Report 2026 anchor URLs and
  `checked_as_of` metadata.
- Sync docs and command paths to the current working checkout.

## Verification Gates

Completed against current artifacts on 2026-06-12:

- `uv run pytest tests/test_manuscript_crossrefs.py tests/test_citation_workflow.py tests/test_sharded_data_integrity.py tests/test_figures.py tests/test_scripts.py -q` → 50 passed.
- `AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/build_curriculum.py` → exit 0.
- `rg "History of the module|\]\. and|\]\.\." output/manuscript/` → no matches.
- `rg "defensible claim whose meaning|treats each source topic through|parsed AGEINT source spine" output/manuscript/` → no matches.
- `uv run python scripts/count_citations.py --format markdown` → source sections 723; citation occurrences 1468; zero-citation source sections 0.
- `uv run python scripts/count_citations.py --format json` → generated Markdown files 377; generated citation occurrences 9951.
- `uv run pytest tests/ --cov=src --cov-fail-under=90` → 276 passed; 92.15% coverage.
- From `/Users/4d/Documents/GitHub/template`:
  `uv run python -m infrastructure.validation.cli markdown projects/working/AGEINT/output/manuscript --repo-root .` → no issues found.
- From `/Users/4d/Documents/GitHub/template`:
  `uv run python -m infrastructure.validation.cli prerender projects/working/AGEINT/output/manuscript --repo-root .` → no render-blocking pitfalls or undefined citations found.

## Current Follow-Up Ledger

| ID | Status | Scope | Exit condition |
|---|---|---|---|
| AGEINT-VERIFY-2026-06-12 | done | Complete this verifier-hardening pass. | All gates above passed; `ageint-4` is marked done in `tasks.yaml`. |
| AGEINT-METADATA-LEGACY-1 | todo | 109 legacy anchors still rely on `domain` / `source_type` fallback semantics for lane/tier. | Each legacy anchor has explicit `source_lane` and `source_tier`, plus tests or inventory proving no unintended lane drift. |
| AGEINT-M1 | todo | Release/publish milestone. | Daniel explicitly requests release or publication workflow, confidentiality checks pass, and `ageint-m1` gates are updated from current evidence. |
