# V2 and Deep Expansion Map: source lanes, governance depth, and guardrails

The major v2 pass expands AGEINT without changing its architecture:

- The source guide remains the master curriculum spine.
- `src/` remains the authoring surface for parsing, source lanes, safe
  substitutions, capstone scaffolds, figures, variables, and manifest prose.
- `output/` remains generated.
- Scripts stay thin.
- AGEINT remains local under the lifecycle workspace (`projects/working/AGEINT`
  in this checkout; parent-template workflows may link it as
  `projects/active/AGEINT` or `projects/AGEINT` during promotion/hot-seat runs).

## Structural changes: source anchors, figures, reports, and reader contracts

- 51 chapters now include v2 guide bullets, deep-expansion bullets, and
  evidence-package expansion bullets.
- Appendices increased from 7 to 9 with source verification and claim ledgers
  plus instructor capstone/rubric/red-team review packs.
- Source-guide references increased from 231 to 312 by append-only expansion.
- Curated anchors increased to 462 with source-lane metadata,
  stakeholder role, assurance use, and rights dimension where relevant.
- Registered figures increased to 173, spanning curriculum and part maps,
  per-chapter concept diagrams, source verification, claim ledger, compliance,
  agent evaluation, data flow, capstone, safe-substitution, instructor
  lifecycle, accessibility, HRIA/DPIA, procurement oversight, agent incident,
  data lineage, assessment integrity, adversarial assurance, model and dataset
  card, transparency notice, records-retention, release gate, risk exception,
  learner support, question bank, remediation, bounded-autonomy,
  public-AI-register, AI-incident-reporting, OT-architecture, visual
  accessibility contract, verifier-first artifact evidence, scholarship
  triangulation, analysis-validation, analysis-validation family coverage,
  source-metadata integrity, source-refresh due-date readiness,
  agency-source coverage and profile routing,
  claim-calibration and visual-semantics control,
  cognitive-security synthesis visuals. The cognitive-security synthesis pass
  includes the CSA CDR six-stage degradation cascade, the MAESTRO seven-layer
  threat model, the SRE-for-agents circuit breaker, the
  cognitive-decoherence/CDR isomorphism, the unified epistemic-coherence stack,
  the cognitive attack-layer taxonomy, and the HRO-to-governance crosswalk.
- A deterministic non-numbered cover-art PNG now lives outside the figure
  registry at `output/figures/cover/ageint-cover-synthesis.png`; it is consumed
  by the PDF title page and should not become a numbered manuscript figure.
- The orientation graphical abstract is now the Python-rendered
  `ageint-graphical-abstract` Synthetic Tradecraft System Atlas rather than a
  Mermaid stack; it preserves the stable figure label while adding a richer
  source-spine, tradecraft-core, agentic-boundary, verification, and human-review
  layout.
- Every generated chapter now uses five reader-facing H2 landmarks: orientation,
  practice studio, evidence contract, governance boundary, and assessment route.
  Repeated scaffold headings such as topic lessons, evidence canon, agentic
  translation, reviewer challenge checklist, and learning-path cross-links are
  retained as H3/H4 body headings so they do not flood the PDF TOC.
- Repeated governance items now sit under the expanded
  **Governance, rights, and assurance** section rather than as dozens of
  identical top-level headings.
- Source-guide pseudo-headings are normalized in visible output; provenance
  tables preserve source-guide identity where needed.
- Orientation and bibliography navigation now uses label-backed section,
  figure, and citation links: curriculum-map rows include each part intro and
  part module-map figure, and reference-key tables render Pandoc citations
  rather than backticked `@key` text.
- Current local rendered evidence after the section/reference, visual-quality,
  table-layout, typography, verifier-first artifact-evidence, scholarship,
  Synthetic Analytic Tradecraft orientation, SAT method-contract, analysis-validation,
  family-coverage, source-metadata, cover/abstract/TOC, and graphical-abstract/TOC-title hardening passes:
  330 configured generated Markdown files, 16,057 generated Markdown citation
  occurrences, 0 zero-citation source sections, and a 1,854-page combined PDF
  with 6,289 URI links.
  Source metadata is also verifier-enforced: 472 metadata rows cover 462
  curated anchors plus 10 source-quality support anchors, with 0 blank lane/tier
  fields and 0 fallback-dependent rows after the 119-row hardening baseline.
  The agency-source coverage report separately verifies the 56-anchor official
  US IC expansion for agency, pack, lane, tier, checked-date, claim-scope,
  assurance, rights, duplicate/collision, and profile-routing completeness.
  Figure-reader text is also registry-enforced: all 173 captions meet the
  40-word minimum, all alt-text
  rows meet the 24-word minimum, all long descriptions meet the 70-word
  minimum, generated PNGs embed compact accessibility/provenance and visual-semantics metadata,
  `visual_quality_audit.json` records the rendered-asset checks, the
  `source_metadata.{json,md}` reports lane/tier distributions and refresh-cadence
  buckets, `scholarship_quality.{json,md}` reports source-family mix, 0 uncited
  claim-bearing files, 0 thin claim-bearing files, and six single-source-family
  claim-bearing review-warning rows, with passing SAT method-contract, analysis-validation, lane-contract, and family-coverage checks,
  `claim_calibration.{json,md}` reports high-risk claim-language and source-strength dispositions, the
  bibliography-atlas source-section coverage rows use narrow numeric columns
  and wider descriptive citation-link columns, and the final PDF annotation
  audit reports 0 Markdown-file link targets.
- The PDF table of contents is intentionally limited to H1/H2 entries; H3/H4
  scaffolds remain in the body and HTML output but are hidden from the PDF TOC.
  Module H2 entries are chapter-specific landmarks rather than repeated generic
  scaffold labels.

## Guardrails: safety, citation, metadata, and publication boundaries

- `data/source_identity/` protects `ageint001` through `ageint231`.
- Tests assert all generated chapters contain the expanded reader-facing
  section set and do not expose raw source-guide pseudo-heading prefixes.
- Tests assert the source-verification and instructor-capstone appendices render
  safe artifact rows.
- Tests assert the deep-pass sections, required source lanes, and new figures
  render from source code rather than hand-edited output.
- Tests assert operational phrases appear only in explicit prohibition,
  source-audit, or safe-substitution contexts.
- Template validation is run from the sibling `template` checkout against the
  active AGEINT output path.
- The template renderer removes stale standalone HTML before per-file web
  rendering; the template core pipeline clean stage remains the safest path
  after generated section labels or filenames change.
