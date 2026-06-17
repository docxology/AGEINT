# Rendering Pipeline - AGEINT manuscript build, PDF render, and validation gates

AGEINT does not use numbered source chapters under `manuscript/`. The PDF pipeline reads **generated** markdown from `output/manuscript/`.

## Resolution: generated manuscript directory and source config precedence

`infrastructure.rendering.pipeline._resolve_manuscript_dir` prefers `output/manuscript/` when it contains markdown, and refreshes `config.yaml` and `*.bib` from source `manuscript/`.

## Build before render: refresh manuscript, figures, reports, and copied outputs

```bash
uv run python scripts/build_curriculum.py
```

For local continuation hardening, prefer the template core pipeline so the clean
stage removes stale standalone web/PDF files before rebuild and copy:

```bash
AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/execute_pipeline.py --project working/AGEINT --skip-llm --core-only
```

From template repo root after a direct build and PDF render:

```bash
uv run python scripts/03_render_pdf.py --project working/AGEINT
uv run python -m infrastructure.validation.cli pdf projects/working/AGEINT/output/pdf/AGEINT_combined.pdf
```

Run `uv run python scripts/05_copy_outputs.py --project working/AGEINT` only
when the template-side copied output package is explicitly needed; the
authoritative local PDF path is `projects/working/AGEINT/output/pdf/AGEINT_combined.pdf`.

From the AGEINT root after the rendered PDF exists, bind the current local
artifact evidence into one machine-readable report:

```bash
uv run python scripts/audit_artifact_evidence.py --write --format markdown
uv run python scripts/audit_scholarship_quality.py --write --format markdown
uv run python scripts/audit_source_metadata.py --write --format markdown
uv run python scripts/audit_claim_calibration.py --write --format markdown
uv run python scripts/audit_reference_quality.py --write --format markdown
```

This writes `output/reports/current_artifact_evidence.json` and
`output/reports/current_artifact_evidence.md`; the scholarship command writes
`output/reports/scholarship_quality.json` and `.md`, and the source-metadata
command writes `output/reports/source_metadata.json` and `.md`; the
claim-calibration command writes `output/reports/claim_calibration.json` and
`.md`; the reference-quality command writes `output/reports/reference_quality.json`
and `.md`. The artifact report joins generated manuscript counts,
source-section citation coverage, scholarship quality, source-metadata
explicitness, claim-calibration status, reference-quality status,
figure-registry quality, rendered-reference audit status, stale-output scans,
PDF quality, and PDF annotation/link checks so a stale, overclaimed,
under-linked, or partially copied artifact cannot be certified by one green gate
alone.

## Pre-flight validation: markdown and prerender checks before PDF work

```bash
uv run python -m infrastructure.validation.cli markdown projects/working/AGEINT/output/manuscript --repo-root .
uv run python -m infrastructure.validation.cli prerender projects/working/AGEINT/output/manuscript --repo-root .
```

## Mermaid figures: strict diagram rendering, hashes, and placeholder policy

AGEINT renders 115 Mermaid figures via `mmdc` into `output/figures/mermaid/`:
17 curriculum and part module maps plus 98 JSONL-declared synthesis, boundary,
chapter, part, cross-cutting, and appendix diagrams. The graphical abstract no
longer lives in this Mermaid set; it is the Python-rendered
`ageint-graphical-abstract` atlas under `output/figures/python/`. The remaining
Mermaid rows cover CDR/MAESTRO/SRE agent-safety boundaries, analytic-tradecraft
evidence boundaries, chapter concept maps, part maps, and appendix diagrams (the
intelligence cycle, oversight architecture, minimization gating, ACH workflow,
ICS defensive zones, and more). Strict verification requires real diagram PNGs,
not deterministic text-plate fallbacks. Unchanged Mermaid sources are not
re-rendered: a per-figure content hash in `<diagram>.mmd.rendered` skips `mmdc`
when the source is byte-identical to the last real render.

```bash
# Strict build (fail instead of placeholder PNGs when mmdc/Chrome is missing)
AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/build_curriculum.py

# One-time Chrome install for mmdc (if renders fail)
npx --yes puppeteer browsers install chrome-headless-shell@131.0.6778.204
```

Confirm `mmdc` and `pandoc-crossref` are on `PATH` before PDF render. Combined
PDF rendering may also require `chrome-headless-shell` for inline Mermaid in
other projects; AGEINT pre-rasterizes module maps under `output/figures/mermaid/`.
See template [`docs/operational/troubleshooting/common-errors.md`](../../../../template/docs/operational/troubleshooting/common-errors.md).

Run strict figure tests:

```bash
uv run pytest tests/test_figures.py -m requires_mermaid -v
```

## Cover, abstract, and TOC policy: front matter, claim boundaries, and navigation depth

The PDF title page uses deterministic non-numbered cover art from
`output/figures/cover/ageint-cover-synthesis.png`, with a JSON sidecar beside
it. The cover is rendered by `src/figures/` and referenced from
`manuscript/config.yaml` as `book.cover.image`; it is not registered in
`output/figures/figure_registry.json` and should not be cited as a manuscript
figure.

The abstract is a single plaintext Synthetic Analytic Tradecraft contract: one
Markdown paragraph after
`# Abstract: Synthetic Analytic Tradecraft contract {#sec:abstract}`, roughly
1,200-1,600 rendered words, with source-quality and research-anchor counts integrated into
the prose rather than emitted as standalone spine paragraphs. It should not
regain a `Graphical Abstract` subsection, an artifact-path note, a course-path
note, an embedded image token, or raw spine variables. The governed-system map
formerly used as graphical-abstract support now belongs in orientation material.
The abstract may claim source traceability, evidence-packet discipline,
negative controls, human review, rollback, and refresh triggers; it must not
frame citation counts, page counts, figure counts, validator passes, or link
audits as a benchmark for model capability, learning outcomes, operational
effectiveness, statistical significance, or safety performance.

The PDF table of contents intentionally exposes H1/H2 entries only through
`\setcounter{tocdepth}{2}` in `manuscript/preamble.md`. H3/H4 scaffolds remain
available in body text and generated HTML, but they are hidden from the PDF TOC
to keep navigation useful at the manuscript scale. Generated modules expose three
chapter-specific H2 landmarks: source/profile frame, practice-lens path, and
assurance handoff. The repeated orientation, practice, evidence, governance, and
assessment scaffolds, plus teaching details such as topic lessons, transfer
architecture, evidence spine, reviewer route, and learning-path links, stay as
chapter-specific H3/H4 body headings rather than generic repeated TOC labels.
The same preamble owns TOC spacing controls so entries such as
`42.10 Evidence...` do not collapse into `42.10Evidence...`.

PDF readiness is not public-release readiness. A successful local render and
zero-issue markdown/prerender/PDF validation feed the local publication
preflight, but they do not perform a release. The 2026-06-14 preflight closes
`ageint-27`: artifact evidence, source refresh, artifact-manifest status,
parent confidentiality guard, release-surface scan, source/license posture, and
task prerequisites all report green. `ageint-m1` remains todo until a public
release, push, PR, archive, promotion, publication upload, DOI, or release
record is explicitly approved and executed.

## Current local artifact evidence: latest counts, audits, PDF status, and limits

The 2026-06-12 through 2026-06-14 section/reference, figure-caption,
visual-accessibility, table-layout/typography, verifier-first artifact-evidence,
scholarship-quality, profile-anchor triangulation, Synthetic Analytic
Tradecraft orientation, SAT method-contract, analysis-validation,
analysis-validation family-coverage, source-metadata, cover/abstract/TOC,
graphical-abstract/TOC-title, claim-calibration, visual-semantics, US IC
agency-source coverage, early orientation visualization, and
single-paragraph abstract hardening passes now render 330 configured manuscript
Markdown files with 177 registered figures plus one non-numbered cover-art PNG.
Figure PNGs carry embedded accessibility/provenance and visual-semantics
metadata in addition to the JSON registry and `visual_quality_audit.json`. The
combined AGEINT PDF rendered to `output/pdf/AGEINT_combined.pdf` at ~34 MB,
1,858 pages, letter page size, and PDF version 1.7. The template PDF validator
reported 0 issues, the AGEINT PDF quality audit reported `stale PDF: false` and
`OK: true`, and the integrated PDF annotation audit found 6,289 URI links with
0 `.md`, `.markdown`, `file:`, or launch targets in both the source and copied
PDFs. The scholarship audit reports 0 uncited claim-bearing files, 0 thin
claim-bearing files, and six single-source-family claim-bearing review-warning
rows plus passing SAT method-contract, analysis-validation, analysis-validation
lane, claim-bearing family-coverage, `source_metadata_ok`, and
`claim_calibration_ok` contracts after profile-specific external triangulation
was added to topic lessons, worked examples, source-canon sections, and
review-checklist sections. Claim calibration remains green with 9,107 candidate
rows, 0 hard fails, 482 boundary-allowed rows, and 5,129 review rows. The
source-refresh due report is green with 472 current rows and 0 due-soon,
due/stale, unknown-cadence, or missing-date rows. Local web output now contains
331 HTML files: one combined manuscript and 330 standalone section views, with
stale pre-label orientation filenames removed by the renderer cleanup hook.

## Related documentation: output inventory and manuscript syntax

- [`output_inventory.md`](output_inventory.md)
- [`../manuscript/SYNTAX.md`](../manuscript/SYNTAX.md)
