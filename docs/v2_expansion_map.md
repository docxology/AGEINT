# V2 And Deep Expansion Map

The major v2 pass expands AGEINT without changing its architecture:

- The source guide remains the master curriculum spine.
- `src/` remains the authoring surface for parsing, source lanes, safe
  substitutions, capstone scaffolds, figures, variables, and manifest prose.
- `output/` remains generated.
- Scripts stay thin.
- AGEINT remains local under the lifecycle workspace (`projects/working/AGEINT`
  in this checkout; parent-template workflows may link it as
  `projects/active/AGEINT` or `projects/AGEINT` during promotion/hot-seat runs).

## Structural Changes

- 51 chapters now include v2 guide bullets, deep-expansion bullets, and
  evidence-package expansion bullets.
- Appendices increased from 7 to 9 with source verification and claim ledgers
  plus instructor capstone/rubric/red-team review packs.
- Source-guide references increased from 231 to 312 by append-only expansion.
- Curated anchors increased to 248 with source-lane metadata,
  stakeholder role, assurance use, and rights dimension where relevant.
- Registered figures increased to 161, spanning curriculum and part maps,
  per-chapter concept diagrams, source verification, claim ledger, compliance,
  agent evaluation, data flow, capstone, safe-substitution, instructor
  lifecycle, accessibility, HRIA/DPIA, procurement oversight, agent incident,
  data lineage, assessment integrity, adversarial assurance, model and dataset
  card, transparency notice, records-retention, release gate, risk exception,
  learner support, question bank, remediation, bounded-autonomy,
  public-AI-register, AI-incident-reporting, OT-architecture, and
  cognitive-security synthesis visuals. The cognitive-security synthesis pass
  includes the CSA CDR six-stage degradation cascade, the MAESTRO seven-layer
  threat model, the SRE-for-agents circuit breaker, the
  cognitive-decoherence/CDR isomorphism, the unified epistemic-coherence stack,
  the cognitive attack-layer taxonomy, and the HRO-to-governance crosswalk.
- Every generated chapter now uses a reader-facing architecture: module thesis,
  learning outcomes, module architecture, evidence/source canon,
  research-backed synthesis, agentic translation boundary, governance/rights/
  assurance, domain practice studio, assessment/capstone pathway, refresh/
  safety/source maps, review checklist, and cross-links.
- Repeated governance items now sit under the expanded
  **Governance, rights, and assurance** section rather than as dozens of
  identical top-level headings.
- Source-guide pseudo-headings are normalized in visible output; provenance
  tables preserve source-guide identity where needed.
- Orientation and bibliography navigation now uses label-backed section,
  figure, and citation links: curriculum-map rows include each part intro and
  part module-map figure, and reference-key tables render Pandoc citations
  rather than backticked `@key` text.
- Current local rendered evidence after the section/reference hardening pass:
  377 generated manuscript files, 11,417 generated Markdown citation
  occurrences, 0 zero-citation source sections, and a 1,697-page combined PDF.
  Figure-reader text is also registry-enforced: all 161 captions meet the
  40-word minimum, all alt-text rows meet the 24-word minimum, and the final PDF
  annotation audit reports 0 Markdown-file link targets.

## Guardrails

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
- The template core pipeline clean stage should be used before trusting
  standalone web output after generated section labels or filenames change.
