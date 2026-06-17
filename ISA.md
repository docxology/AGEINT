---
project: AGEINT
task: Publication-prep cleanup + commit-to-main (release/publish is the next-day milestone)
effort: E4
phase: complete
started: 2026-06-03
updated: 2026-06-16
---

# AGEINT ISA Closeout And Current Ledger

## 2026-06-16 Publication-Prep + Commit-To-Main (DONE)

Final pre-publication cleanup after the three review rounds. Scope was: confirm
docs/everything clean, do low-value tidy, and commit the full working tree to
`main`. NOT a release — Daniel will do the release tomorrow (Zenodo version DOI,
public `docxology/AGEINT` repo, PDF re-render with GitHub+DOI baked in, then
publish to Zenodo + GitHub). `AGEINT-M1` stays open until that approved workflow.

- Low-value fix done: `pyproject.toml py-modules` completed from 24 → all 36 flat
  `src/*.py` modules (additive; the previous list silently dropped 12 from any
  `pip install .`; the py-modules / `packages.find` split is correct — find handles
  subpackages, py-modules the flat modules). Not the unsafe "delete py-modules"
  the round-3 reviewer proposed.
- Hygiene confirmed clean: 0 TODO/FIXME/XXX/HACK/DEBUG and 0 pdb/breakpoint in
  tracked source/docs; 0 tracked junk (`.pyc`/caches/`.DS_Store`/`coverage*.json`/
  egg-info); deterministic build (exit 0, "rewrote 0 neutral templates").
- Committing the FULL working tree (rounds 1-3 edits + the pre-existing uncommitted
  462-anchor data expansion + doc updates that predate this session). `output/`,
  coverage, and caches are gitignored and excluded. Commit gated on the final full
  suite (tests_final) being green.

## 2026-06-16 Round-3 Scope: Project-Wide Claims, Documentation, Consistency (DONE)

**Goal:** Verify every numeric/factual CLAIM project-wide (README, AGENTS, docs/, manuscript) against ground-truth runtime/registry/report values; fix documentation drift introduced over 3 rounds; ensure cross-file consistency (esp. the R1 "non-operational"→"evidence-bounded" safety-term rewording — uniform or half-applied?); confirm rounds-1-2 prose added no unsupported claim. Source/doc edits only; rebuild + full gate if any source/template changes; Forge cross-vendor (if backend available — was rate-limited round 2, resets Jun 20).

**Baseline this session (R8):** figure registry 177 (115 mermaid/52 python/4 historical/6 ai) — matches README exactly; headline counts 16/51/9/20/312 match build output. Claim-audit generators re-run — ALL authoritative audits report ok=True: `claim_calibration`, `reference_quality`, `scholarship_quality`, `publication_readiness`, `source_metadata`, `source_refresh_due`, `agency_source_coverage`, `current_artifact_evidence`, `orchestration_contract`, plus `test_results`/`validation_report` all_passed. So the manuscript's gate-enforced CLAIMS are sound after rounds 1-2; net-new round-3 value is concentrated in DOCUMENTATION drift + cross-file consistency (not gate-enforced). Round-3 review workflow (5 surfaces) dispatched.

**Criteria (round-3):** the workflow returned 12 findings; the project's gate-enforced claims were already sound, so the do-now set is doc-accuracy/hygiene. Two were genuinely WRONG documented facts (highest priority):

- [x] ISC-3A: WRONG claim-calibration counts corrected — `9,223/483/5,190` → `9,107/0/482/5,129` in `README.md:320` and `docs/rendering_pipeline.md:167` (the latter present-tense "remains green with…", so strictly wrong). Verified against `output/reports/claim_calibration.json` (candidate_rows=9107, hard_fail=0, boundary_allowed=482, warning_rows=5129).
- [x] ISC-3B: WRONG structural claim corrected — "five chapter-specific H2 landmarks" → "three (source/profile frame, practice-lens path, assurance handoff)" in `README.md:293` and `docs/v2_expansion_map.md:49`, aligning with `docs/rendering_pipeline.md:126` and `chapter_landmark_titles()` (verified: returns exactly 3 keys; the 5 names are H3 scaffolds).
- [x] ISC-3C: Doc-drift label fix — `AGENTS.md:71` "Cross-links row" → "Learning-path links row". Verified `markdown_refs.lesson_educational_crossrefs()` emits literal "**Learning-path links.**"; the `## Cross-links` heading the tests assert is a separate manuscript construct, unaffected.
- [x] ISC-3D: Drift-resistance — PDF size `34.15 MB` → `~34 MB` (un-sourced exact value re-drifts each build) in `README.md:259` + `docs/rendering_pipeline.md:156`; `src/AGENTS.md:38` routing-table line made non-exhaustive (`data/*.yaml … see that module`); `data/README.md` given a pointer to the complete `data/AGENTS.md` inventory.
- [x] ISC-3E: Repo hygiene — added `coverage*.json` (+ htmlcov/.benchmarks/.mypy_cache/.ruff_cache/tmp/.DS_Store) to `.gitignore` and `git rm --cached coverage_project.json` (828KB disposable artifact was tracked; mirrors template convention; reversible, staged for the user's commit decision).
- [x] ISC-3F: Manuscript claim-soundness CONFIRMED clean — round-1/2 added prose introduced no unsupported empirical/performance/capability claim; stays synthetic/defensive/non-operational; all restated counts match ground truth; `claim_calibration`=0 hard-fails. No edit (changing sound hedged prose would risk the gate-clean posture).
- [x] ISC-3G: No rebuild/manuscript-gate impact — all edits are hand-maintained docs + `.gitignore` (no template/src-logic/manuscript-content change). `test_docs_contract` + `test_file_size_inventory` green; no test pins any changed string; full suite stays 387/0 (tests_r2b) since no tested artifact changed.
- [DEFERRED-VERIFY] ISC-3H: `pyproject.toml py-modules` stale (24 declared vs ~36 src top-level modules) + contradictory dual-declaration with `packages.find`. DEFERRED (follow-up AGEINT-PYPROJECT-PKG): MARGINAL/latent — only bites `pip/uv install .`, not the `pythonpath=[".","src"]` test/build workflow this project uses; and the reviewer's "delete py-modules, rely on packages.find" is unsafe as stated (flat top-level modules are NOT found by `packages.find`, which discovers packages) — needs a verified fresh-install test, out of scope for a doc round.
- DEFERRED (confirmed still-deferred, not new): README anchor-history ordering (= the round-2 "orientation source ordering" item; cosmetic, churn-risk); the `fig:ageint-claim-evidence-fit-map` caption verb-frame folds into the already-deferred B2/B3 caption-tail refactor.



A second review workflow (5 surfaces: code modularization, manuscript modularization, body/appendix writing+signposting, whole-manuscript visualizations, fresh sweep + deferred backlog) returned 26 findings with explicit worth_it verdicts. Most modularization items were honestly NO (orientation already build-time modularized; _NN chunking coherent; scripts thin; token system well-factored). Implementing the 6 genuine net-new wins (one per axis), deferring MARGINAL items.

**Round-2 criteria:**
- [x] ISC-2A: Modularization — created `src/markdown_cell.py` with two named policies (`escape_table_cell`, `plain_table_cell`); 5 of 6 sites delegate (citation_workflow/pdf_quality/rendered_heading_support → plain; reference_quality/markdown_table → escape). 6th site `manuscript_manifest/_03_part.py` kept a local byte-identical copy: it sits at the 500-line modularization gate (499) and the delegate's import line breached it (→501, caught by `test_file_size_inventory`); reverted to stay ≤500. Forge confirmed both policy bodies byte-equivalent to the originals (no behavior change). Covered via delegates + `test_round2_refinements`.
- [x] ISC-2B: Signposting (D5) — chapter-unique wayfinding footer appended to every `02-evidence-contract` + `03-governance-boundary` fragment (incl. line-budget splits), keyed to each module's own `[@section.section_label]`. Verified 51/51 + 51/51 now contain `sec:curriculum_orientation`; footer is 51 distinct paragraphs, max 2 files each (clears the >6-file repeated-paragraph gate, which also gates uniqueness). `test_round2_refinements` + crossrefs green.
- [x] ISC-2C: Visualization — `_draw_bar_chart` label gate replaced with `label_stride = max(1, (len+21)//22)` so x-axis anchors always render (citation-density chart was ~45 unlabeled bars). Chart regenerated; Forge confirmed stride math + sole caller.
- [x] ISC-2D: Visualization/accessibility — `_visual_type` now resolves an explicit alt-text flow signal before the map→matrix branch; 0 of 16 module-maps still announced as "matrix-style figure". Forge verified all 16 reclassified are genuine flowcharts (no real matrix mislabeled). Regression test added.
- [x] ISC-2E: Writing — appendix `_blocked_appendix_source_label` returns "no blocked motif; source title used verbatim" when no transform occurred (was duplicating cols 1&2). Sentinel rendering in appendices; regression test added.
- [DEFERRED-VERIFY] ISC-2F: Container-heading "Evidence anchor." inheritance — DEFERRED to a focused follow-up (AGEINT-HEADING-INHERIT). Reading `rendered_heading_support.py` confirmed the fix inherently changes the anti-overclaim verifier's definition of "supported" (both `add_heading_support` injector AND the `unsupported_headings` inventory/gate must change in lockstep + a negative control). The injected line is already terse (the ~30-word filler was previously reduced to "**Evidence anchor.** [ref]" carrying a real cross-ref), so value is modest while risk (weakening the credibility-bearing gate) is the batch's highest. Not bundled — violates ISC-2H. Follow-up must include a negative control proving the gate still fails a genuinely unsupported heading.
- [x] ISC-2G: Build clean + full suite ≥90% + Forge. Build exit 0. Full suite (tests_r2): 386 passed / 1 failed (the file-size gate caught _03_part at 501) → fixed by reverting that one delegate (behavior-neutral); final re-run (tests_r2b): **387 passed, 0 failed, exit 0, coverage 91.72%**. Forge: NO correctness defects across all 6 items (byte-equivalent consolidation, correct `_visual_type` reorder, resolving cross-refs, sound stride math, preserved safety stance). HONEST DISCLOSURE: the GPT-5.4/codex cross-vendor backend hit its usage limit (resets Jun 20), so Forge's pass was its own evidence-backed analysis (real commands against the corpus), NOT an independent-vendor opinion — the cross-vendor blind-spot check is owed for this round.
- [x] ISC-2H: Anti held. No `{{TOKEN}}` deleted (build "rewrote 0 neutral templates"); no operational content; abstract untouched (still one paragraph); no verifier gate weakened — the safety-term rewording was co-enforced by updated tests (Forge-verified), and ISC-2F (the one gate-semantics change) was DEFERRED precisely to avoid weakening the heading-support gate. GOTCHA logged: a modularization dedup (function-local import) nearly breached the 500-line modularization gate on a ceiling file — consolidation-by-delegation can grow a file; check `test_file_size_inventory` when delegating in near-limit modules.

**Deferred MARGINAL (logged, not done):** orientation source ordering (cosmetic, build-risky), B2/B3 generic caption-detail tails (177-fig churn), B5 figure re-homing (NO — gallery can't re-home without rewriting embed logic), B6 reading-order figure (NO — compass already exists), B8 long-desc (NO), E3 underscore anchors (NO — cross-file rename risk), E4 nav-heading terminology (NO — two distinct constructs), lesson Concept-frame repetition + source-binding (MARGINAL).

## 2026-06-16 Comprehensive Review And Early-Section Refinement Scope (DONE)

**Goal:** Verify every manuscript section and formalism is complete, accurate, and
signposted, then refine the early/orientation sections — reader-facing opening
prose, deep-link signposting, and figure captions/placement — without weakening
any verifier gate, deleting any `{{TOKEN}}`, or adding operational content. Source
edits land in `manuscript/templates/*` and `src/figures/*`; output is rebuilt and
re-audited.

**Criteria (this scope):**

- [x] ISC-R1: Orientation opening now reader-facing. Verified: rendered `orientation/00-*.md` line 3 opens "AGEINT (Agentic Intelligence) is a curriculum-and-assurance atlas for teaching how AI agents can *assist*…"; build mechanics demoted to a `> **For maintainers.**` blockquote.
- [x] ISC-R2: Early-orientation captions self-contained. Verified: compass caption renders with a single clean limit ("navigation support, not a learning-outcome or performance claim.") and `grep -c "should be read as a map of instructor"` = 0 (duplicating auto-suffix eliminated); `test_figure_quality_audit` green (min-word gate still satisfied).
- [x] ISC-R3: Signposting gaps closed. Verified: "Govern and assure" row + reader-paths/glossary deep links render; `test_manuscript_crossrefs` (21 tests) green = all `[@sec:]`/`[@fig:]` resolve.
- [x] ISC-R4: Formalisms verified. C1 fixed 3 mis-flagged quantitative renderers (now `quantitative=False`, registry confirmed); C2 narrowed the abstract's equation/table-link overclaim; C3 reconciled SAT 4-vs-6; `test_figure_quality_audit` + `test_scholarship_quality` green.
- [x] ISC-R5: Build clean. Verified: `build_curriculum.py` exit 0 (build2 + build3), deterministic.
- [x] ISC-R6: Full test suite ≥90%. Verified: `pytest tests/ --cov=src --cov-fail-under=90` = **383 passed, 0 failed, exit 0, 91.20% coverage** (tests3, 20:51). Baseline was 382/1 (staleness, resolved by rebuild); the 2 transient post-edit failures (tests pinning changed strings) fixed without weakening assertions.
- [x] ISC-R7: Anti held. Verified: 0 `{{TOKEN}}` deleted (build "rewrote 0 neutral templates"); abstract still single-paragraph (contract intact); captions ≥40 words; no operational/deployable content added; no gate weakened (the 2 test fixes restored exact strings, did not relax assertions).
- [x] ISC-R8: Forge cross-vendor review found no defects; explicitly confirmed the D1 caption-sanitiser fix correct and the abstract single-paragraph + figure-link claim accurate.

**Test-reconciliation decision (2026-06-16):** the post-edit full run surfaced exactly 2 failures, both tests pinning strings I intentionally changed. Resolved WITHOUT weakening either test: (1) `test_figures::…creative_visuals…` asserts a signature phrase per early caption — restored the exact phrases "field-capability proof" and "authoritative status" (meaning unchanged). (2) `test_reader_quality::…front_loads_deep_link_signposts` requires the arrow-chain pipeline string — treated as an encoded signpost feature; restored the `domain part -> … -> verifier reports` pipeline on its own line while keeping the clearer "work the table in order" framing. A6's full arrow-chain removal was thus partially reverted; the readability concern is met by the framing + standalone line.

**Decisions (this scope):**

- 2026-06-16: ISA was `complete` (closeout ledger). User requested a fresh comprehensive review + early-section refinement. Reopened as a new dated scope rather than a separate task ISA — the work iterates the persistent project. `effort_source: classifier (E4) escalated to E5` given "deeply comprehensively" + explicit `/workflows` + ultrathink.
- 2026-06-16: Baseline ran `build_curriculum.py` (exit 0, deterministic — rewrote 0 neutral templates) and the full pytest suite at OBSERVE before any edit (R8 GENERATOR-PREEXEC).
- 2026-06-16: A 5-surface review workflow (early-writing, early-visuals, governance, formalisms, body+abstract) returned 30 findings + a prioritized plan. Implemented the high-value, low-risk batch; deferred/rejected several:
  - REJECTED E2 (break the abstract into paragraphs): conflicts with the gated single-continuous-paragraph abstract contract (AGEINT-ABSTRACT-PUBLIC-READINESS). Applied only C2 (narrow the overclaimed "equation/table links" — manuscript has zero `{#eq:}`/`{#tbl:}` labels).
  - D1 is a REAL BUG, not stale output (reviewer's "just rebuild" falsified — string persists after a clean rebuild): the manuscript chapter-title sanitiser (`rendered_reference_audit.py:314` → "the module") strips the chapter names the part-module-map caption embeds, yielding "from the module through the module" across all 16 parts. Registry caption is correct (no sanitiser there). Fix at the caption source: stop embedding raw chapter titles (which the sanitiser is designed to prevent anyway).
  - B1 used the prose-only fallback (forward-point the 5 named tradecraft figures to the gallery) rather than figure-re-slotting, to avoid disturbing figure-count/coverage audits.
  - Deferred (noted follow-ups, beyond early-section scope or higher risk): B2/B3 global caption-tail refactor (177 figures, min-word gated), B5 figure re-homing, B6 new reading-order figure, B8 long-description enrichment, D5 chapter-fragment wayfinding footer, E3 underscore→hyphen anchor rename (cross-file), E4 nav-heading terminology.



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
- Later expansion, visual-accessibility hardening, and metadata-verifier
  hardening increased the current project surface to 16 parts, 51 chapters,
  9 appendices, 312 source-guide references, 304 curated research anchors,
  10 source-quality support anchors, 314 source-metadata rows, and 172
  registered figures.
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

## 2026-06-12 Section/Reference Auto-Link Hardening Scope

The follow-on local hardening pass makes the generated navigation surface
reader-clickable without changing source identity or publication scope:

- Orientation navigation sections now carry stable labels for reader paths,
  curriculum map, research-anchor atlas, source-lane map, safe-substitution
  matrix, capstone workflow, figures/course links, and related governance
  surfaces.
- Early orientation prose and curriculum-map rows now use label-backed
  section/figure references for part intros, part module-map figures,
  bibliography atlas, source lane map, research anchor atlas, and figures/course
  links.
- Reference-key tables now render Pandoc citation links such as
  `[@official_cia_tradecraft_primer]`, `[@scholarly_rethlefsen_2021_prisma_s]`,
  and `[@ageint001]` instead of backticked literal `@key` cells.
- The generated-manuscript ordering assertion tracks the label-bearing
  orientation filenames emitted after the split.
- Direct render-only reuse is not sufficient after filename-bearing section
  labels change; use the template pipeline clean stage before trusting standalone
  web output directories.

## 2026-06-12 RedTeam Artifact-Evidence And Visualization Scope

The RedTeam pass classified AGEINT as a structured repo artifact with a useful
but attackable verifier oracle: individual gates could be green while a copied
PDF, standalone web directory, or prose evidence note was stale. The current
hardening pass closes that false-certification path by binding the source build,
rendered manuscript, citation inventory, figure registry, visual-quality audit,
PDF quality/link audit, rendered-reference audit, and stale-output scans into a
single current evidence manifest.

- `scripts/audit_artifact_evidence.py --write` writes
  `output/reports/current_artifact_evidence.json` and `.md`.
- `src/pdf_quality.py` now audits PDF URI annotations, local Markdown-file
  targets, `file:` targets, and launch/file actions in addition to page and
  stale-PDF checks.
- The new `ageint-artifact-evidence-control-loop` Python figure makes the
  verifier contract visible in the orientation navigation surface.
- The parent template renderer removes stale standalone HTML before per-file web
  rendering, preventing old label-derived filenames from surviving render-only
  reruns.

## 2026-06-12 Scholarship-Quality And Triangulation Scope

The current local RedTeam pass extends artifact evidence from "citations exist"
to "claim-bearing sections have enough support to be reviewable." It does not
renumber sources, publish AGEINT, or add unverified web citations.

- `src/scholarship_quality.py` classifies generated manuscript citations by
  source family, flags uncited or one-citation claim-bearing sections as hard
  failures, and keeps multi-citation single-family sections as review warnings.
- `scripts/audit_scholarship_quality.py --write` writes
  `output/reports/scholarship_quality.json` and `.md`.
- `src/artifact_evidence.py` now includes `scholarship_quality_ok` and the
  scholarship report summary in the unified current-evidence manifest.
- The new `ageint-scholarship-triangulation-map` Python figure makes the
  scholarship gate visible in the orientation navigation surface.
- The MCP/AutoGen and cryptographic-methods appendices now include direct
  official, standards, and source-guide citations from existing AGEINT keys so
  their source boundaries are informative rather than thin.

## 2026-06-13 Source-Metadata Verifier Scope

The RedTeam pass classified the artifact-evidence oracle as still incomplete:
PDF/link/citation/figure gates could pass while curated source anchors silently
fell back from blank `source_lane` / `source_tier` fields to `domain` /
`source_type`. The first-principles fix is source-layer explicitness plus a
negative-control verifier, not more generated prose.

- Closed 119 blank metadata rows: 109 legacy intelligence anchors now carry
  `source_lane` from their existing `domain` and `source_tier` from their
  existing `source_type`, and 10 source-quality support anchors now carry
  `source_quality_spine` / `source_quality_anchor`.
- Added `src/source_metadata.py` and `scripts/audit_source_metadata.py` to
  report total metadata records, curated intelligence anchors, support anchors,
  blank lane/tier counts, fallback-dependent rows, lane/tier distributions,
  refresh-cadence buckets, and issue rows.
- Wired `source_metadata_ok` into `src/artifact_evidence.py`, so the unified
  current-evidence manifest fails on blank lane/tier fields or source-quality
  semantic mismatches even when rendered artifacts are otherwise current.
- Added the registry-backed `ageint-source-metadata-integrity` Python figure to
  make the metadata-integrity and refresh-coverage gate visible in the reader
  surface.
- Deferred the parent-template artifact-manifest advisory (`missing declared
  output: projects/AGEINT/output`) to a separate pipeline contract task because
  it is not a PDF/link/citation correctness blocker.

## 2026-06-13 Cover, Abstract, And TOC Hardening Scope

This local pass improves the first-reader surface without changing the locked
curriculum order, source identities, or publication status:

- Added deterministic non-numbered cover art at
  `output/figures/cover/ageint-cover-synthesis.png` with a JSON sidecar and
  wired it through `book.cover.image` in `manuscript/config.yaml`.
- Kept the cover out of `output/figures/figure_registry.json`, so the registry
  remains 169 figures and the cover does not become a numbered manuscript
  figure.
- Replaced the former graphical-abstract wrapper with one 1,226-word plaintext
  Abstract centered on Synthetic Analytic Tradecraft, source governance,
  evidence packets, safety boundaries, refusal scope, and validation.
- Moved the former `fig:ageint-graphical-abstract` role into orientation as a
  governed-system map rather than an abstract subsection.
- Reordered early orientation around reader comprehension, renamed repeated H2
  scaffold headings, and kept the PDF TOC at H1/H2 depth with LaTeX spacing
  controls for multi-digit section numbers.

## 2026-06-13 Graphical Abstract And TOC Title Hardening Scope

This local pass supersedes the prior orientation graphical-abstract treatment
without changing the cover-art contract, locked curriculum order, source
identities, citation keys, or publication status:

- Replaced the old Mermaid-backed `fig:ageint-graphical-abstract` with the
  registry-backed Python `graphical_abstract_atlas` renderer and a deterministic
  2400px square `AGEINT Synthetic Tradecraft System Atlas` in
  `output/figures/python/ageint-graphical-abstract.png`.
- Preserved the stable label `fig:ageint-graphical-abstract` and orientation
  source-section placement while adding long caption, alt text, and
  long-description metadata that explain the source spine, discipline lanes,
  Synthetic Analytic Tradecraft core, bounded agent assistance, verification
  gates, human review, product handoff, and halt conditions.
- Replaced repeated module H2 scaffolds with five chapter-specific reader
  landmarks: orientation, practice studio, evidence contract, governance
  boundary, and assessment route. Repeated body scaffolds such as module
  architecture, evidence canon, reviewer checklist, and learning-path
  cross-links now sit below the PDF TOC depth.
- Kept part and appendix navigation titles reader-specific and preserved
  existing section, figure, citation, and formalism label semantics.

## 2026-06-14 Claim Calibration And Visual-Semantics Scope

This local RedTeam/Science/FirstPrinciples pass attacks the remaining oracle
gap: citation, figure, link, and PDF readiness could be green while claim
language, source strength, formulas, or visual semantics were overclaimed. The
fix is verifier coverage first, then calibrated manuscript wording.

- Added `src/source_support_strength.py` to classify source-guide and curated
  anchor keys as official/standard/scholarly/law-policy/public-domain primary
  support, source-quality support, source-guide context, practitioner/vendor
  context, social/video context, mirror/copy context, or unknown.
- Added `src/claim_calibration.py` and
  `scripts/audit_claim_calibration.py`; the audit scans generated manuscript
  rows for high-risk empirical, statistical, governance, safety, visualization,
  artifact-readiness, and formalism language, fails unsupported proof/p-value/
  measured-performance/formalism claims, and allows explicit boundary language.
- Wired `claim_calibration_ok` into the unified artifact evidence manifest with
  negative controls for unsupported measured-performance claims, fake p-value
  language, and weak-source-only high-risk claims.
- Extended figure-registry schema `1.4` with visual-semantics fields:
  semantic role, evidence role, quantitative flag, unit, denominator, counting
  rule, and interpretation limit. Conceptual figures now state that layout,
  color, and arrows are explanatory unless a metric is declared; quantitative
  figures declare units, denominators, counting rules, and limits.
- Added the registry-backed
  `fig:ageint-claim-calibration-and-visual-semantics` Python control visual.
- Added a manuscript method note clarifying that citation counts, file counts,
  figure counts, PDF page counts, URI-link counts, and validator outcomes are
  artifact telemetry, not empirical learning, safety, statistical, or
  operational-performance results.

## 2026-06-14 Single-Paragraph Abstract And Public-Readiness Scope

This local pass improves the first-reader contract and records the publication
boundary without changing the source corpus, curriculum order, source
identities, citation keys, or release status:

- Converts the Abstract into one continuous Markdown paragraph after
  `# Abstract {#sec:abstract}`, with source-quality and research-anchor counts
  integrated into the prose instead of emitted as standalone spine paragraphs.
- Makes the abstract more concrete about what a learner, instructor, or
  reviewer sees: part maps, source keys, evidence packets, negative controls,
  figure semantics, claim calibration, human review, rollback, and refresh
  triggers.
- Preserves the claim boundary: AGEINT can claim a traceable Synthetic Analytic
  Tradecraft architecture, but citation counts, figure counts, page counts,
  validator passes, and link audits remain artifact telemetry, not empirical
  proof of model capability, learning outcomes, operational effectiveness,
  statistical significance, or safety performance.
- Records the public-readiness assessment: local artifact evidence is strong,
  but AGEINT is not ready to publish publicly until `ageint-27` release
  preflight, confidentiality checks, source/license review, artifact-manifest
  cleanup or waiver, fresh PDF validation, and `ageint-m1` release gates pass.

## 2026-06-14 US IC Source-Pack And Agency Coverage Scope

This local pass expands the research substrate while keeping AGEINT defensive,
educational, authorized, synthetic, non-operational, and local-only. The
first-principles constraint is that new citations must be routable evidence
surfaces, not a bulk bibliography dump.

- Added `data/research_anchors/intelligence-anchors-249-304.jsonl` with 56
  directly verified official public US Intelligence Community anchors: 25 CIA,
  3 DIA, 15 ODNI, 6 Intelligence.gov, 3 NSA, 2 NGA, 1 FBI, and 1 NRO row.
- Raised curated intelligence anchors from 248 to 304 while preserving the 10
  source-quality support anchors and all locked source-guide identities.
- Added `source_agency` and `source_pack` metadata to `ResearchAnchor` reference
  dictionaries and required those fields for the new official US IC tranche.
- Added `data/agency_source_packs.yaml` plus deterministic source-pack expansion
  for profile routing, so CIA analytic uncertainty, CIA professional literature,
  DIA OSINT governance, ODNI disclosure/tearlines, ODNI privacy/oversight,
  current threat context, cyber/GEOINT history, and declassified-history packs
  can be reused modularly.
- Added `src/agency_source_coverage.py` and
  `scripts/audit_agency_source_coverage.py` with negative-control coverage for
  missing pack metadata, duplicate/collision checks, profile routing, and
  minimum CIA/DIA/ODNI-or-Intelligence.gov counts.
- Wired `agency_source_coverage_ok` into artifact evidence and publication
  readiness, and added the registry-backed
  `fig:ageint-agency-source-coverage` Python dashboard.
- Preserved claim calibration: official citations can support governance,
  source-context, uncertainty, warning, disclosure, OSINT/GEOINT, cyber, and
  professional-literature claims, but CIA Studies/CSI sources are not treated as
  current agency policy or AGEINT benchmark evidence.

## Verification Gates

Completed against verifier-hardening artifacts earlier on 2026-06-12:

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

Completed against section/reference auto-link artifacts earlier on 2026-06-12:

- `uv run pytest tests/test_manuscript_crossrefs.py tests/test_markdown_refs.py tests/test_manuscript_inventory_structure.py tests/test_manuscript_variables.py -q` → 42 passed.
- `uv run python scripts/check_rendered_references.py` → rendered reference audit passed.
- `uv run python scripts/count_citations.py --format json` → generated Markdown files 377; generated citation occurrences 11417; source sections 723; zero-citation source sections 0.
- Clean template core-pipeline project-test gate → 278 passed, 1 pre-render PDF-artifact skip, 91.38% coverage.
- `AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/build_curriculum.py` → exit 0 with 163 registered figures.
- From `/Users/4d/Documents/GitHub/template`:
  `uv run python scripts/03_render_pdf.py --project working/AGEINT` → generated `output/pdf/AGEINT_combined.pdf` at 27.87 MB after the template clean stage.
- `uv run python scripts/audit_pdf_quality.py` → 1698 pages; stale PDF false; OK true.
- From `/Users/4d/Documents/GitHub/template`:
  `uv run python -m infrastructure.validation.cli pdf output/working/AGEINT/pdf/AGEINT_combined.pdf` → 0 issues.

Completed against figure-caption and PDF-link artifacts earlier on 2026-06-12:

- Figure registry validation → 161 figures; 0 captions under 40 words; 0 alt-text rows under 24 words; 0 caption/alt placeholder rows; 0 caption/alt Markdown-file references.
- Generated-output scans → 0 Markdown-file links in generated Markdown/HTML; 0 placeholder or banned fallback phrases in generated manuscript.
- PDF annotation audit → source and copied PDFs each have 1698 pages, 33335 link annotations, and 0 `.md` / `.markdown` link targets.
- Visual PDF spot check → curriculum-map table no longer collides across columns; representative curriculum-map, part module-map, and cognitive-security figure captions fit without overlap.
- `uv run python scripts/audit_pdf_quality.py` → 1698 pages; stale PDF false; OK true.
- From `/Users/4d/Documents/GitHub/template`:
  `uv run python -m infrastructure.validation.cli markdown projects/working/AGEINT/output/manuscript --repo-root .` → no issues found.
- From `/Users/4d/Documents/GitHub/template`:
  `uv run python -m infrastructure.validation.cli prerender projects/working/AGEINT/output/manuscript --repo-root .` → no render-blocking pitfalls or undefined citations found.
- From `/Users/4d/Documents/GitHub/template`:
  `uv run python -m infrastructure.validation.cli pdf output/working/AGEINT/pdf/AGEINT_combined.pdf` → 0 issues.

Completed against visual-quality artifacts earlier on 2026-06-12:

- Perplexity CLI discovery attempt → `401 insufficient_quota`; no Perplexity-derived claim was encoded.
- Official fallback source verification → W3C WAI Complex Images, WCAG 2.2 Understanding SC 1.1.1, SC 1.4.1 Use of Color, SC 1.4.11 Non-text Contrast, Section508.gov alternative-text/PDF/color-usage guidance, and USWDS data-visualization guidance encoded into the figure-registry accessibility contract.
- `uv run ruff check src/figures/_01_part.py src/figures/_01b_accessibility.py src/figures/_02_part.py src/figures/_02b_mermaid.py src/figures/_02c_reader_text.py src/figures/_03_part.py src/figures/_03b_asset_renderers.py src/figures/_03d_accessibility.py src/figures/_05_visual_style.py src/figures/_06_python_renderers.py tests/test_figures.py` → all checks passed.
- `uv run pytest tests/test_figures.py tests/test_file_size_inventory.py -q` → 14 passed.
- `AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/build_curriculum.py` → exit 0 with 163 registered figures and figure-registry schema `1.3`.
- Figure registry validation → 163 figures; 115 Mermaid, 38 Python, 4 historical, 6 AI-generated; official accessibility-guidance metadata, PNG text-chunk accessibility metadata, and `visual_quality_audit.json` present; all captions, alt-text rows, and long descriptions pass the expanded tests.
- `uv run pytest tests/ --cov=src --cov-fail-under=90` → 284 passed; 92.15% coverage.
- From `/Users/4d/Documents/GitHub/template`:
  `AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/03_render_pdf.py --project working/AGEINT` → generated a 1,699-page, 28.06 MB combined PDF with 163/163 figure references found.
- From `/Users/4d/Documents/GitHub/template`:
  `uv run python scripts/05_copy_outputs.py --project working/AGEINT` → copied 981 output files, including 163 PNGs and the 28.06 MB combined PDF.
- From `/Users/4d/Documents/GitHub/template`: markdown, prerender, and PDF validators → 0 issues.
- `uv run python scripts/audit_pdf_quality.py` → 1,699 pages; stale PDF false; OK true.
- PDF annotation audit → source and copied PDFs each have 4,285 URI links and 0 `.md`, `.markdown`, or `file:` targets.

Completed against section-link, table-layout, and compact-typography artifacts on 2026-06-12:

- Source-owned fixes landed in `_markdown_split.py`, `citation_workflow.py`,
  `rendered_heading_support.py`, the compact PDF preamble, and focused
  regression tests; `output/manuscript/` was rebuilt rather than hand-edited.
- `uv run ruff check src/_markdown_split.py src/citation_workflow.py src/rendered_heading_support.py tests/test_markdown_split.py tests/test_citation_workflow.py tests/test_heading_support.py tests/test_manuscript_variables.py tests/test_figures.py` → all checks passed.
- Focused gate:
  `uv run pytest tests/test_markdown_split.py tests/test_heading_support.py tests/test_citation_workflow.py tests/test_manuscript_crossrefs.py tests/test_markdown_refs.py tests/test_manuscript_variables.py tests/test_figures.py -q` → 65 passed.
- `AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/build_curriculum.py` → exit 0 with 377 generated manuscript files and 163 registered figures.
- `uv run python scripts/count_citations.py --format json` → generated Markdown files 377; generated citation occurrences 12802; source sections 723; zero-citation source sections 0.
- `uv run python scripts/check_rendered_references.py` → rendered reference audit passed.
- Targeted scan for stale coverage wording, old source-section table headers, and Markdown-file links in PDF-bound generated content → no matches.
- From `/Users/4d/Documents/GitHub/template`:
  `uv run python scripts/03_render_pdf.py --project working/AGEINT` and
  `uv run python scripts/05_copy_outputs.py --project working/AGEINT` → generated and copied `AGEINT_combined.pdf` at 28.12 MB with 981 copied output files.
- From `/Users/4d/Documents/GitHub/template`: markdown, prerender, and PDF validators → 0 issues.
- `uv run python scripts/audit_pdf_quality.py` → 1671 pages; stale PDF false; OK true.
- PDF annotation audit → source and copied PDFs each have 4,180 URI links and 0 `.md`, `.markdown`, `file:`, or launch targets.
- Visual PDF spot check of the source-section coverage page confirms narrow numeric columns, a wider descriptive column, separate citation-link column, and no merged adjacent tables.
- `uv run pytest tests/ --cov=src --cov-fail-under=90` → 288 passed; 92.12% coverage.

Completed against RedTeam artifact-evidence and visualization artifacts on 2026-06-12:

- AGEINT Ruff gate for touched source, figure, script, and test files → all checks passed.
- Template renderer Ruff gate and regression for stale web artifact cleanup → all checks passed; 2 focused template tests passed.
- `uv run pytest tests/test_artifact_evidence.py tests/test_pdf_quality.py tests/test_figures.py tests/test_figure_quality_audit.py tests/test_manuscript_crossrefs.py tests/test_markdown_refs.py -q` → 64 passed.
- `AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/build_curriculum.py` → exit 0 with 378 generated manuscript files and 164 registered figures.
- Corrected template render and copy:
  `AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/03_render_pdf.py --project working/AGEINT`
  and `uv run python scripts/05_copy_outputs.py --project working/AGEINT` → source PDF 28.30 MB, 1,673 pages; copied output root PDF 29,670,685 bytes.
- Standalone web freshness check → source and copied web outputs each contain 379 HTML files: 378 section pages plus `index.html`; stale pre-label orientation filenames are absent.
- `uv run python scripts/audit_artifact_evidence.py --write --format json` → `ok: true`; 12,805 generated Markdown citation occurrences; 723 source sections; 0 zero-citation source sections; all 164 figures pass the visual-quality audit; PDF link audit reports 4,180 URI links and 0 `.md`, `.markdown`, `file:`, or launch targets.
- `uv run python scripts/check_rendered_references.py` → rendered reference audit passed.
- Targeted scan for stale coverage wording, old source-section table headers, Markdown-file links, and banned fallback phrases in generated/PDF-bound content → no matches.
- From `/Users/4d/Documents/GitHub/template`: markdown, prerender, and PDF validators → 0 issues.
- `uv run python scripts/audit_pdf_quality.py --format json` → stale PDF false, OK true, 1,673 pages, 10,779,643 extracted text characters, and clean link audit.

Completed against RedTeam scholarship-quality, profile-anchor triangulation, and
current-artifact visualization artifacts on 2026-06-12:

- AGEINT touched-file Ruff gate for scholarship, artifact-evidence, figure,
  appendix-support, manifest, intelligence-content, and focused test files →
  all checks passed.
- Parent template figure-validator Ruff gate and focused regression suite →
  all checks passed; 21 validator tests passed.
- Added `profile_triangulation_anchors(...)` and routed existing official,
  standards, scholarly, and source-guide anchors into topic lessons, worked
  examples, source-canon sections, and review-checklist sections without adding
  or renumbering citation keys.
- `uv run pytest tests/test_file_size_inventory.py tests/test_reader_quality.py tests/test_scholarship_quality.py tests/test_chapter_fragment_quality.py -q`
  after the profile-anchor pass → 19 passed.
- `AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/build_curriculum.py`
  after the profile-anchor pass → exit 0 with 378 generated manuscript files
  and 165 registered figures.
- Clean template core pipeline:
  `AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/execute_pipeline.py --project working/AGEINT --skip-llm --core-only`
  → all stages completed; infrastructure tests passed 120/120; project test
  stage passed 294/299 with 5 pre-render PDF-stage skips and 90.23% coverage;
  PDF render and copy completed.
- `uv run python scripts/audit_scholarship_quality.py --write --format json`
  → `ok: true`; 0 uncited claim-bearing files; 0 thin claim-bearing files; 0
  single-source-family claim-bearing warning rows.
- `uv run python scripts/audit_artifact_evidence.py --write --format json`
  after the profile-anchor pass → `ok: true`; 378 generated Markdown files; 14,765 generated Markdown
  citation occurrences; 723 source sections; 0 zero-citation source sections;
  all 165 figures pass visual-quality checks; rendered-reference, freshness,
  PDF quality, stale-output, and scholarship checks pass.
- `uv run python scripts/check_rendered_references.py` → rendered reference
  audit passed.
- Targeted scans for banned fallback phrases, `History of the module`, citation
  punctuation joins, Markdown-file links, and stale literal reference-key cells
  in generated manuscript output → no matches.
- `uv run python scripts/audit_pdf_quality.py` → stale PDF false, OK true,
  1,698 pages, 10,926,085 extracted text characters, 4,180 URI links, 0 file
  actions, and 0 bad PDF link targets.
- From `/Users/4d/Documents/GitHub/template`: markdown, prerender, and PDF
  validators → 0 issues. The clean pipeline still reports only the broad
  non-critical artifact-manifest advisory; AGEINT's stricter
  `current_artifact_evidence.{json,md}` report is clean.

Completed against source-metadata verifier hardening artifacts on 2026-06-13:

- Focused metadata/artifact/figure/safety gate:
  `uv run pytest tests/test_source_metadata.py tests/test_artifact_evidence.py tests/test_scholarship_quality.py tests/test_figures.py tests/test_figure_quality_audit.py tests/test_manuscript_safety_docs.py -q` → 49 passed, 1 skipped.
- `AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/build_curriculum.py`
  → exit 0 with 380 generated manuscript files and 169 registered figures.
- From `/Users/4d/Documents/GitHub/template`:
  `uv run python scripts/03_render_pdf.py --project working/AGEINT` and
  `uv run python scripts/05_copy_outputs.py --project working/AGEINT` →
  regenerated and copied the 29.69 MB combined PDF.
- `uv run python scripts/audit_artifact_evidence.py --write --format json` →
  `ok: true`; `source_metadata_ok: true`; 380 generated Markdown files; 14,771
  generated Markdown citation occurrences; 258 source-metadata rows; 248 curated
  intelligence anchors; 10 source-quality support anchors; 0 blank lane/tier
  rows; 0 fallback-dependent rows; all 169 figures pass visual-quality checks.
- `uv run python scripts/audit_pdf_quality.py --format json` → stale PDF false,
  OK true, 1,704 pages, 4,180 URI links, 0 bad PDF link targets, and 0 file
  actions.
- From `/Users/4d/Documents/GitHub/template`: markdown, prerender, and PDF
  validators → 0 issues.
- `uv run pytest tests/ --cov=src --cov-fail-under=90` → 312 passed, 1 skipped,
  91.52% coverage.
- Touched-file Ruff checks passed. The broad `uv run ruff check src tests
  scripts` gate still reports 60 pre-existing repo-wide style findings, mostly
  unused package re-exports, star-import fallout, and deferred import placement;
  track that separately from metadata-verifier correctness.

Completed against cover, abstract, and TOC hardening artifacts on 2026-06-13:

- `AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/build_curriculum.py`
  → exit 0 with 380 generated manuscript files and 169 registered figures plus
  one non-numbered cover-art PNG.
- `uv run pytest tests/test_cover_abstract_toc.py tests/test_figures.py tests/test_manuscript_crossrefs.py tests/test_manuscript_inventory_structure.py tests/test_pdf_typography.py -q`
  → 43 passed.
- From `/Users/4d/Documents/GitHub/template`:
  `AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/03_render_pdf.py --project working/AGEINT`
  and `uv run python scripts/05_copy_outputs.py --project working/AGEINT` →
  rendered and copied a 1,680-page, 31,115,574-byte / 29.67 MB PDF.
- Template markdown, prerender, and PDF validators → 0 issues.
- `uv run python scripts/check_rendered_references.py` → rendered reference
  audit passed.
- Targeted scans for `Graphical Abstract`, abstract boilerplate, Markdown-file
  links, stale generic headings, and tight TOC joins → no matches.
- `uv run python scripts/audit_pdf_quality.py` → stale PDF false, OK true,
  1,680 pages, 4,181 URI links, 0 bad PDF link targets, and 0 file actions.
- `uv run python scripts/count_citations.py --format json` → 380 generated
  Markdown files, 14,771 generated Markdown citation occurrences, 723 source
  sections, and 0 zero-citation source sections.
- `uv run python scripts/audit_artifact_evidence.py --write --format markdown`
  → `ok: true`, `source_metadata_ok: true`, `scholarship_quality_ok: true`,
  169 registered figures, 1,680 PDF pages, and 0 bad PDF link targets.
- Visual inspection of the rendered PDF title page confirmed the deterministic
  cover art appears on the cover page without clipping or missing assets.

Completed against graphical-abstract and TOC-title hardening artifacts on
2026-06-13:

- `AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/build_curriculum.py`
  → exit 0 with 383 manuscript-bound files, 369 generated Markdown files, 330
  configured manuscript files, 169 registered figures, and one non-numbered
  cover-art PNG.
- `uv run pytest tests/test_cover_abstract_toc.py tests/test_figures.py tests/test_manuscript_crossrefs.py tests/test_manuscript_inventory_structure.py tests/test_manuscript_inventory_quality.py tests/test_pdf_typography.py tests/test_scholarship_quality.py tests/test_chapter_fragment_quality.py -q`
  → 67 passed.
- `uv run ruff check` over the files touched by the graphical-abstract,
  manuscript-heading, and TOC-title pass → all checks passed. Broad repo-wide
  Ruff remains a separate cleanup task because legacy package-export and
  split-module style findings predate this pass.
- `uv run python scripts/check_rendered_references.py` → rendered reference
  audit passed.
- Targeted scans for stale graphical-abstract subsection text, abstract
  boilerplate, Markdown-file links, stale H2 scaffold headings, banned fallback
  phrases, and tight TOC joins → no matches in the rendered outputs/PDF text.
- From `/Users/4d/Documents/GitHub/template`:
  `AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/execute_pipeline.py --project working/AGEINT --skip-llm --core-only`
  → all stages completed successfully; project gate passed 313/318 tests with 5
  expected pre-render skips and 90.39% coverage; PDF render/copy completed.
- Template validators after render:
  markdown and prerender validators → 0 issues; PDF validator → 0 issues.
- `uv run python scripts/audit_pdf_quality.py` → stale PDF false, OK true,
  1,619 pages, 4,181 URI links, 0 bad PDF link targets, and 0 file actions.
- `uv run python scripts/count_citations.py --format json` → 330 generated
  citation-inventory Markdown rows, 15,382 generated Markdown citation
  occurrences, 723 source sections, and 0 zero-citation source sections.
- `uv run python scripts/audit_artifact_evidence.py --write --format json` and
  `uv run python scripts/audit_scholarship_quality.py --write --format json` →
  `ok: true`; `source_metadata_ok: true`; `scholarship_quality_ok: true`;
  six single-family claim-bearing review warnings.
- Post-render direct test chunks covered the monolithic direct-run SIGTERM gap:
  PDF/artifact tests 16/16 passed, manuscript-variable tests 5/5 passed, and
  remaining tail chunks passed 31/31, 49/49, and 52/52.

Completed against claim-calibration, source-strength, statistics, formalism, and
visual-semantics artifacts on 2026-06-14:

- `uv run ruff check src/claim_calibration.py tests/test_claim_calibration.py`
  → all checks passed.
- `uv run pytest tests/test_claim_calibration.py -q` → 9 passed.
- `uv run python scripts/audit_claim_calibration.py --write --format json` →
  `ok: true`, 8,748 candidate rows, 0 hard-fail rows, 471 boundary-allowed
  rows, and 5,181 review-warning rows.
- `uv run python scripts/audit_scholarship_quality.py --write --format json`
  → `ok: true`, 0 uncited claim-bearing files, 0 thin claim-bearing files, and
  six single-source-family claim-bearing review warnings under the stricter
  source-strength classifier.
- `uv run python scripts/audit_source_metadata.py --write --format json` →
  `ok: true`, 258 metadata records, 248 curated intelligence anchors,
  10 source-quality support anchors, 0 blank lane/tier rows, and
  0 fallback-dependent rows.
- `uv run python scripts/audit_artifact_evidence.py --write --format json` →
  `ok: true`; `claim_calibration_ok`, `source_metadata_ok`,
  `scholarship_quality_ok`, `figure_quality_ok`, `pdf_quality_ok`, rendered
  references, stale-output scans, and citation source-section coverage all true;
  170 registered figures; 15,382 generated Markdown citation occurrences; and
  that pass's 1,620-page PDF audit with 0 bad link targets.
- `uv run python scripts/check_rendered_references.py` → rendered reference
  audit passed.
- Targeted scans for stale proof wording, banned fallback phrases, and
  Markdown-file links in generated manuscript → no matches.

## Current Follow-Up Ledger

| ID | Status | Scope | Exit condition |
|---|---|---|---|
| AGEINT-VERIFY-2026-06-12 | done | Complete this verifier-hardening pass. | All gates above passed; `ageint-4` is marked done in `tasks.yaml`. |
| AGEINT-AUTOLINK-2026-06-12 | done | Complete section/reference auto-link hardening and PDF rerender. | Orientation labels, curriculum map links, citation-link tables, full tests, rendered-reference audit, template validators, and PDF audit passed; `ageint-11` is marked done in `tasks.yaml`. |
| AGEINT-FIGLINK-2026-06-12 | done | Complete figure caption, visual layout, and PDF-link hardening. | All 161 figure captions/alt-text rows pass the expanded reader-text gate; source/copy PDFs have 0 Markdown-file link annotations; visual spot checks and validators passed; `ageint-12` is marked done in `tasks.yaml`. |
| AGEINT-VISACCESS-2026-06-12 | done | Add official visual-accessibility guidance, a long-description registry contract, and a source-backed visual accessibility contract figure. | All 162 figure captions, alt-text rows, and long descriptions pass tests; strict build reports schema `1.2`; full suite, template validators, PDF audit, and annotation audit pass; `ageint-13` is marked done in `tasks.yaml`. |
| AGEINT-PNGMETA-2026-06-12 | done | Add color-safe visual guidance and embed figure accessibility/provenance metadata into generated PNGs. | Registry schema `1.2` includes Section508 color-usage guidance; all 162 generated PNGs carry metadata text chunks; full suite, strict build, rendered-reference audit, template validators, PDF validator, PDF quality audit, and PDF annotation audit pass; `ageint-14` is marked done in `tasks.yaml`. |
| AGEINT-VISQA-2026-06-12 | done | Add W3C color/contrast guidance, a generated visual-quality audit JSON artifact, and a visual-quality dashboard figure. | Registry schema `1.3` includes eight official guidance URLs; all 163 figures pass visual-quality audit checks; 284-test full suite, strict build, rendered-reference audit, template validators, PDF validator, PDF quality audit, and annotation audit pass; `ageint-15` is marked done in `tasks.yaml`. |
| AGEINT-SECLINK-TABLETYPO-2026-06-12 | done | Complete section-link, source-section coverage table, PDF-link, and compact-typography hardening. | Coverage wording no longer pairs bibliography-atlas refs with unrelated citations; adjacent tables split cleanly; source/copy PDFs have 0 Markdown-file or file-action targets; final full suite passed 288 tests with 92.12% coverage; `ageint-16` is marked done in `tasks.yaml`. |
| AGEINT-ARTIFACT-EVIDENCE-2026-06-12 | done | Add verifier-first artifact evidence, PDF link audit, stale web cleanup, and the artifact-evidence control-loop figure. | That pass proved the unified evidence manifest and stale-web cleanup path; `ageint-17` is marked done in `tasks.yaml`, with current metrics superseded by `ageint-19`. |
| AGEINT-SCHOLARSHIP-TRIANGULATION-2026-06-12 | done | Add scholarship-quality verifier, source-family report, appendix source-boundary improvements, and the scholarship triangulation figure. | `scholarship_quality.{json,md}` and `current_artifact_evidence.{json,md}` report `ok: true`; `ageint-18` introduced the verifier and `ageint-19` closes the source-family warnings it surfaced. |
| AGEINT-PROFILE-ANCHORS-2026-06-12 | done | Add profile-specific external triangulation anchors to generated claim-bearing sections and tighten the scholarship verifier. | That pass produced 378 manuscript files, 165 figures, and 14,765 generated citation occurrences before the SAT orientation pass superseded the current artifact counts; `ageint-19` is marked done in `tasks.yaml`. |
| AGEINT-SAT-ORIENTATION-2026-06-12 | done | Strengthen the abstract and early orientation sections around Synthetic Analytic Tradecraft as a source-governed, synthetic-fixture workbench. | That pass produced 379 manuscript files, 165 figures, 14,771 generated citation occurrences, and a 1,699-page PDF before the SAT method-contract pass superseded current artifact counts; `ageint-20` is marked done in `tasks.yaml`. |
| AGEINT-SAT-METHOD-2026-06-12 | done | Add a falsifiable SAT method-contract figure and verifier gate for early abstract/orientation scholarship claims. | That pass produced 379 manuscript files, 166 figures, 14,771 generated citation occurrences, and a 1,700-page 28.98 MB PDF before the analysis-validation pass superseded current artifact counts; `ageint-21` is marked done in `tasks.yaml`. |
| AGEINT-ANALYSIS-VALIDATION-2026-06-12 | done | Add a label-backed analysis-validation protocol, validation-matrix figure, and verifier gate for claim-class review. | The follow-on RedTeam lane-contract pass superseded current artifact counts; `ageint-22` is marked done in `tasks.yaml`. |
| AGEINT-ANALYSIS-LANE-CONTRACT-2026-06-12 | done | Add canonical analysis-validation lanes and a negative control for dropped claim classes. | That pass added the lane contract and is superseded for current artifact counts by `AGEINT-ANALYSIS-FAMILY-COVERAGE-2026-06-13`; `ageint-23` is marked done in `tasks.yaml`. |
| AGEINT-ANALYSIS-FAMILY-COVERAGE-2026-06-13 | done | Add canonical claim-bearing manuscript-family coverage and a registry-backed coverage visual. | That render had 380 manuscript files, 168 figures, 14,771 generated citation occurrences, a 1,703-page 29.52 MB PDF, 4,180 URI links, 0 bad PDF link targets, 0 file actions, and passing SAT method-contract, analysis-validation, lane-contract, and family-coverage checks; current counts are superseded by metadata-verifier hardening. |
| AGEINT-METADATA-VERIFIER-2026-06-13 | done | Close 119 blank lane/tier metadata rows and add source-metadata oracle coverage. | `source_metadata_ok` covers 258 metadata rows, 248 curated intelligence anchors, 10 source-quality support anchors, 0 blank lane/tier rows, 0 fallback-dependent rows, and the 109+10 closure baseline; final gates passed with 312 tests, 91.52% coverage, 0 template markdown/prerender/PDF issues, and a fresh 1,704-page 29.69 MB PDF; `ageint-10` is marked done in `tasks.yaml`. |
| AGEINT-COVER-ABSTRACT-TOC-2026-06-13 | done | Add deterministic cover art, replace the graphical-abstract wrapper with one plaintext Abstract, and harden PDF TOC depth/spacing. | That pass reported 380 manuscript files, 169 registered figures plus one non-numbered cover, 14,771 generated citation occurrences, a 1,680-page 29.67 MB PDF, 4,181 URI links, 0 bad PDF link targets, 0 file actions, 0 template markdown/prerender/PDF issues, and clean scans for abstract boilerplate, Markdown-file links, stale headings, and tight TOC joins; current counts are superseded by `AGEINT-GRAPHICAL-ABSTRACT-TOC-TITLES-2026-06-13`; `ageint-28` is marked done in `tasks.yaml`. |
| AGEINT-GRAPHICAL-ABSTRACT-TOC-TITLES-2026-06-13 | done | Replace `fig:ageint-graphical-abstract` with the Python Synthetic Tradecraft System Atlas and make chapter/part/appendix TOC landmarks reader-specific. | That pass reported 383 manuscript-bound files, 369 generated Markdown files, 330 configured manuscript files, 169 registered figures plus one non-numbered cover, 15,382 generated citation occurrences, a 1,619-page 30.26 MB PDF, 4,181 URI links, 0 bad PDF link targets, 0 file actions, 0 template markdown/prerender/PDF issues, clean rendered-reference and TOC scans, and passing post-render PDF/artifact/manuscript-variable/tail test chunks; current counts are superseded by `AGEINT-CLAIM-CALIBRATION-2026-06-14`; `ageint-29` is marked done in `tasks.yaml`. |
| AGEINT-CLAIM-CALIBRATION-2026-06-14 | done | Add claim-calibration, source-strength, statistics/formalism, and visual-semantics verifier coverage. | `claim_calibration_ok` was true for that pass with 8,748 candidate rows, 0 hard fails, 471 boundary-allowed rows, and 5,181 review-warning rows; figure registry schema `1.4` reported 170 figures with visual-semantics metadata; source metadata remained explicit; scholarship quality was OK with six non-blocking single-source-family review warnings; that pass's artifact evidence was OK with 15,382 generated citation occurrences and a 1,619-page PDF audit with 0 bad link targets; current counts are superseded by `AGEINT-V1-PREFLIGHT-2026-06-14` and `AGEINT-US-IC-SOURCE-PACK-2026-06-14`; `ageint-30` is marked done in `tasks.yaml`. |
| AGEINT-ABSTRACT-PUBLIC-READINESS-2026-06-14 | done | Convert the Abstract into one continuous show-not-tell paragraph and record public-readiness blockers. | The rendered Abstract is one 1,258-word paragraph with no graphical-abstract subsection, no standalone spine variables, no abstract boilerplate, and preserved SAT/analysis-validation refs; focused tests passed 38/38; template core pipeline passed 324 project tests with 5 expected skips and 90.3% coverage; artifact evidence was OK with 330 generated Markdown files, 15,382 generated citation occurrences, 723 source sections, 0 zero-citation source sections, 170 figures, and a non-stale 1,620-page PDF; current counts are superseded by the local publication-readiness preflight; `ageint-31` is marked done in `tasks.yaml`. |
| AGEINT-SOURCE-REFRESH-DASHBOARD-2026-06-14 | done | Add a source-refresh due-date dashboard without mutating `checked_as_of` dates. | `source_refresh_due.{json,md}` now reports 314 metadata rows, 314 current rows, 0 due-soon rows, 0 due/stale rows, 0 unknown-cadence rows, and 0 missing-date rows; cadence buckets are 210 annual, 50 semiannual, 51 quarterly, and 3 biennial; the registry-backed `ageint-source-refresh-due-dashboard` figure is rendered; `source_refresh_due_ok` is wired into artifact evidence; `ageint-25` is marked done. |
| AGEINT-TEMPLATE-MANIFEST-CONTRACT-2026-06-14 | done | Clean up the template artifact-manifest contract advisory. | Parent-template lifecycle-slug resolution now declares `projects/working/AGEINT/...` and `output/working/AGEINT/...` for symlinked/private projects; parent regression tests cover slash-qualified project IDs; current AGEINT `artifact_manifest.json` reports `issues: []`; `ageint-26` is marked done. |
| AGEINT-V1-PREFLIGHT-2026-06-14 | done | Prepare the local v1 release preflight bundle without publishing. | `publication_readiness.{json,md}` reports `ok: true`; artifact evidence, source refresh, agency source coverage, artifact manifest, parent tracked-project confidentiality guard, release-surface scan, source/license posture, and task prerequisites all pass; current evidence records 330 generated Markdown files, 15,606 generated citation occurrences, 172 registered figures plus non-numbered cover art, a fresh 1,658-page 30.89 MB PDF, 4,704 URI links, 0 file actions, and 0 bad PDF link targets; no release/push/PR/archive/promotion/publication action was taken; `ageint-27` is marked done. |
| AGEINT-US-IC-SOURCE-PACK-2026-06-14 | done | Add 56 official public US IC anchors and fail-closed agency/source-pack coverage. | `data/research_anchors/intelligence-anchors-249-304.jsonl` raises curated intelligence anchors to 304; `source_agency` and `source_pack` metadata are required for the new tranche; `data/agency_source_packs.yaml` routes packs into profiles; `agency_source_coverage.{json,md}` reports 56 new official US IC anchors, 0 missing metadata rows, 0 unrouted rows, 0 duplicate/collision rows, and CIA/DIA/ODNI-or-Intelligence.gov minimums satisfied; `agency_source_coverage_ok` is wired into artifact evidence and publication readiness; final validation passed 347 project tests with 7 expected skips and 90.43% coverage, template markdown/prerender/PDF validators reported 0 issues, and the AGEINT PDF audit reported 0 bad link targets; `ageint-32` is marked done. |
| AGEINT-REFERENCE-QUALITY-2026-06-14 | done | Add fail-closed reference-quality, section-title, and citation-context hardening. | `reference_quality.{json,md}` reports `ok: true` across 332 scanned manuscript/PDF-bound files with 0 unresolved/rendered-reference issues, 0 Markdown-file links, 0 raw literal citation-key cells, 0 generic heading issues, 0 lesson cross-link issues, and 0 citation-context issues; `reference_quality_ok` is true in artifact evidence and publication readiness; the rebuilt artifact has 330 generated Markdown files, 15,606 generated citation occurrences, 172 figures, a fresh 1,658-page 30.91 MB PDF, 4,704 URI links, 0 file actions, 0 bad PDF link targets, 0 parent markdown/prerender/PDF validator issues, and final full project tests passed with 359 tests and 91.36% coverage. |
| AGEINT-M1 | todo | Release/publish milestone. | Explicit public release approval is still required. Local publication-readiness preflight is green, but `ageint-m1` remains open until Daniel requests a release/publish workflow and the final candidate is rerun through confidentiality, source/license, artifact-evidence, template validation, PDF, and publication-readiness gates. |
