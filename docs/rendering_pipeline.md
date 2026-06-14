# Rendering Pipeline — AGEINT

AGEINT does not use numbered source chapters under `manuscript/`. The PDF pipeline reads **generated** markdown from `output/manuscript/`.

## Resolution

`infrastructure.rendering.pipeline._resolve_manuscript_dir` prefers `output/manuscript/` when it contains markdown, and refreshes `config.yaml` and `*.bib` from source `manuscript/`.

## Build before render

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
uv run python scripts/05_copy_outputs.py --project working/AGEINT
uv run python -m infrastructure.validation.cli pdf output/working/AGEINT/pdf/AGEINT_combined.pdf
```

From the AGEINT root after the rendered PDF exists, bind the current local
artifact evidence into one machine-readable report:

```bash
uv run python scripts/audit_artifact_evidence.py --write --format markdown
uv run python scripts/audit_scholarship_quality.py --write --format markdown
uv run python scripts/audit_source_metadata.py --write --format markdown
uv run python scripts/audit_claim_calibration.py --write --format markdown
```

This writes `output/reports/current_artifact_evidence.json` and
`output/reports/current_artifact_evidence.md`; the scholarship command writes
`output/reports/scholarship_quality.json` and `.md`, and the source-metadata
command writes `output/reports/source_metadata.json` and `.md`; the
claim-calibration command writes `output/reports/claim_calibration.json` and
`.md`. The artifact report joins generated manuscript counts, source-section
citation coverage, scholarship quality, source-metadata explicitness,
claim-calibration status, figure-registry quality, rendered-reference audit
status, stale-output scans, PDF quality, and PDF annotation/link checks so a
stale, overclaimed, or partially copied artifact cannot be certified by one
green gate alone.

## Pre-flight validation

```bash
uv run python -m infrastructure.validation.cli markdown projects/working/AGEINT/output/manuscript --repo-root .
uv run python -m infrastructure.validation.cli prerender projects/working/AGEINT/output/manuscript --repo-root .
```

## Mermaid figures

AGEINT renders 114 Mermaid figures via `mmdc` into `output/figures/mermaid/`:
17 curriculum and part module maps plus 97 JSONL-declared synthesis, boundary,
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

## Cover, abstract, and TOC policy

The PDF title page uses deterministic non-numbered cover art from
`output/figures/cover/ageint-cover-synthesis.png`, with a JSON sidecar beside
it. The cover is rendered by `src/figures/` and referenced from
`manuscript/config.yaml` as `book.cover.image`; it is not registered in
`output/figures/figure_registry.json` and should not be cited as a manuscript
figure.

The abstract is a single plaintext Synthetic Analytic Tradecraft contract. It
should not regain a `Graphical Abstract` subsection, an artifact-path note, a
course-path note, or an embedded image token. The governed-system map formerly
used as graphical-abstract support now belongs in orientation material.

The PDF table of contents intentionally exposes H1/H2 entries only through
`\setcounter{tocdepth}{2}` in `manuscript/preamble.md`. H3/H4 scaffolds remain
available in body text and generated HTML, but they are hidden from the PDF TOC
to keep navigation useful at the manuscript scale. Generated modules expose five
chapter-specific H2 landmarks: orientation, practice studio, evidence contract,
governance boundary, and assessment route. Repeated teaching scaffolds such as
topic lessons, evidence canon, reviewer checklist, and learning-path cross-links
are H3/H4 body headings. The same preamble owns TOC spacing controls so entries
such as `42.10 Evidence...` do not collapse into `42.10Evidence...`.

## Current local artifact evidence

The 2026-06-12 and 2026-06-13 section/reference, figure-caption, visual-accessibility,
table-layout/typography, verifier-first artifact-evidence, scholarship-quality,
profile-anchor triangulation, Synthetic Analytic Tradecraft orientation, SAT
method-contract, analysis-validation, analysis-validation family-coverage,
source-metadata, cover/abstract/TOC, and graphical-abstract/TOC-title
hardening passes render 369 generated Markdown files and 383 manuscript-bound
files with 170 registered figures plus one non-numbered cover-art PNG. Figure
PNGs carry embedded
accessibility/provenance and visual-semantics metadata in addition to the JSON registry and
`visual_quality_audit.json`. The combined AGEINT PDF rendered to
`output/pdf/AGEINT_combined.pdf` at 30.26 MB, 1,619 pages, letter page size, and
PDF version 1.7. The template PDF validator reported 0 issues, the AGEINT PDF
quality audit reported `stale PDF: false` and `OK: true`, and the integrated
PDF annotation audit found 4,181 URI links with 0 `.md`, `.markdown`, `file:`,
or launch targets in both the source and copied PDFs. The scholarship audit
reports 0 uncited claim-bearing files, 0 thin claim-bearing files, and six
single-source-family claim-bearing review-warning rows plus passing SAT method-contract,
analysis-validation, analysis-validation lane, claim-bearing family-coverage,
`source_metadata_ok`, and `claim_calibration_ok` contracts after profile-specific external triangulation was added to topic lessons,
worked examples, source-canon sections, and review-checklist sections. Local and copied web outputs now
contain 384 web files each, including 380 section pages and index/combined views, with stale
pre-label orientation filenames removed by the renderer cleanup hook.

## See also

- [`output_inventory.md`](output_inventory.md)
- [`../manuscript/SYNTAX.md`](../manuscript/SYNTAX.md)
