# Rendering Pipeline - AGEINT manuscript build, PDF render, and validation gates

AGEINT does not use numbered source chapters under `docs/manuscript/`. The PDF pipeline reads **generated** markdown from `output/manuscript/`.

## Resolution: generated manuscript directory and source config precedence

`infrastructure.rendering.pipeline._resolve_manuscript_dir` prefers `output/manuscript/` when it contains markdown, and refreshes `config.yaml` and `*.bib` from source `docs/manuscript/`.

## Build before render: refresh manuscript, figures, reports, and copied outputs

```bash
uv run python scripts/build_curriculum.py
```

The `source_validation` stage requires `docs/manuscript/config.yaml` in the
selected project root before creating or changing outputs, refreshing source
bibliographies or templates, or rendering figures. A missing config raises
`FileNotFoundError` naming that exact file; an existing output tree is left
untouched. `validate_declarative_tables(project_root)` checks that project's
config while retaining the built-in declarative table loaders; its no-argument
form and `scripts/validate_declarative_yaml.py` validate the current AGEINT
checkout.

For a new source configuration, copy `docs/manuscript/config.yaml.example` to
`docs/manuscript/config.yaml` and customize the author and publication fields.
The example includes `book.license` (`CC BY 4.0`), `book.code_license`
(`Apache-2.0`), cover settings, and `front_matter.page_two_visual`; generated
front-matter file ordering is supplied by the build. Keep DOI and archive-record
fields empty until that publication has its own deposited identifiers rather
than borrowing another edition's or project's identifiers.

## Shared SDK environment and canonical native renderer

Native rendering is owned by `docxology/template` at the published `v5.1.0`
tag, not a second Pandoc/XeLaTeX driver in AGEINT. The SDK requires Python 3.14
or later; AGEINT's separate standalone-core compatibility floor is unchanged.
Link or check out AGEINT under the SDK's working projects directory. From the
SDK root, prepare its frozen environment and explicitly keep nested `uv`
commands from reconciling it against AGEINT's different project metadata:

```bash
uv sync --frozen --group dev --group rendering --python 3.14
export AGEINT_TEMPLATE_REPO="$PWD"
export VIRTUAL_ENV="$PWD/.venv" UV_PROJECT_ENVIRONMENT="$PWD/.venv"
export UV_PYTHON="$PWD/.venv/bin/python" UV_NO_SYNC=1 UV_FROZEN=true
export PATH="$PWD/.venv/bin:$PATH"
export PYTHONPATH="$PWD:$PWD/projects/working/AGEINT/src"
export SOURCE_DATE_EPOCH="$(git -C projects/working/AGEINT log -1 --format=%ct)"
export AGEINT_REQUIRE_RENDERED_FIGURES=1
export ENABLE_PDF=1 ENABLE_HTML=1 ENABLE_SLIDES=0 ENABLE_DOCX=0 ENABLE_EPUB=0
(cd projects/working/AGEINT && python scripts/build_curriculum.py)
python scripts/pipeline/stage_03_render.py --project working/AGEINT --skip-manuscript-hydration
python -m infrastructure.validation.cli pdf projects/working/AGEINT/output/pdf/AGEINT_combined.pdf
python scripts/pipeline/stage_04_validate.py --project working/AGEINT
```

These local commands require the genuine Mermaid/browser, Pandoc/crossref,
XeLaTeX/BibTeX and native-reader prerequisites. Hosted verification reuses the
SDK's setup actions and source-owned document preparation rather than installing
an unpinned global `mmdc` or an obsolete fixed Chrome build. The source manuscript
config selects `render.html.asset_mode: local`; the SDK's source-locked browser
math dependency preparation supplies the offline assets.

`stage_05_copy.py` is optional copied-output packaging, not the authoritative
native renderer. `output/pdf/AGEINT_combined.pdf` is authoritative; copy it to
`AGEINT.pdf`, never render a separate root PDF.

## Blocking hosted verification and explicit publication

`ci.yml` requires the reusable `manuscript.yml` complete verification job.
The latter also supports manual dispatch and a weekly rebuild. It uses the
exact AGEINT commit, published SDK tag and frozen SDK dev/rendering environment;
it clears prior native deliverables and Mermaid render receipts, builds with
real diagrams, runs the complete test suite at **90% minimum coverage**, rebuilds
authoritative output after tests, and runs SDK markdown/prerender, canonical
PDF/HTML rendering and output validation. All source, reference, figure, license,
PDF and aggregate artifact/readiness gates block failure. Publication readiness
executes the actual SDK all-resource parent guard; skipping it is never a pass.
Failed builds are not replaced by restored committed output.

The separately named limited standalone-core jobs preserve Python compatibility
without the SDK/native toolchain. Their lower environment-specific coverage
floor does not authorize publication or replace the complete gate.

Before the SDK release exists, an explicit manual `manuscript.yml` dispatch may
select `sdk-candidate=<immutable 40-hex SDK commit>` for development verification.
It runs the same complete acceptance, never falls back to main, and records the
actual candidate SHA/version. Candidate evidence cannot authorize publication;
normal CI, scheduled and release verification require published `v5.1.0`.

Manual-only `release.yml` accepts a new `vX.Y.Z` tag, validates it with the
read-only release-metadata CLI, and runs complete verification again on exact
current main. Immediately before create-only publication it rechecks that main
still equals verified Source and that the stable published SDK identity matches.
Existing tags/releases are refused; no tag movement or asset replacement is
allowed. A green metadata check or ordinary CI result alone cannot publish.

Successful verification packages `AGEINT.pdf`, `AGEINT-reader.zip`,
`AGEINT-evidence.zip`, `source-sdk.json` and `SHA256SUMS`. The reader ZIP preserves
`web/` beside `figures/`, including local browser assets. Serve the extracted
bundle root over local HTTP and visit `/web/index.html`, not just `web/` and
not an assumed fully capable `file://` page. Scholarly URLs are user-clicked
references, not remotely fetched assets. Evidence includes actual audit reports,
test and coverage results, tool provenance and exact source/SDK identities. Only artifacts
from the successful reusable job in the same run can reach publication.
See [workflow commands and contracts](../.github/workflows/README.md) for manual
verification and authorized release dispatch.

The canonical HTML edition is `output/web/index.html`; per-section HTML files
are build previews and do not carry the book's complete global citation and
numbering context. Serve `output/`, not only `output/web/`, when checking the
edition over HTTP so `../figures/` resolves. Verify real navigation and image
disclosures in a browser; metadata and link-count gates do not establish visual
readability or accessibility conformance.

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

# Use installed Chrome when Puppeteer's managed browser is unavailable (macOS example)
CHROME_EXECUTABLE_PATH="/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" \
  AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/build_curriculum.py
```

Confirm `mmdc` and `pandoc-crossref` are on `PATH` before PDF render. Combined
PDF rendering may also require `chrome-headless-shell` for inline Mermaid in
other projects; AGEINT pre-rasterizes module maps under `output/figures/mermaid/`.
See template [`docs/operational/troubleshooting/common-errors.md`](https://github.com/docxology/template/blob/main/docs/operational/troubleshooting/common-errors.md).

Run strict figure tests:

```bash
uv run pytest tests/test_figures.py -m requires_mermaid -v
```

## Cover, abstract, and TOC policy: front matter, claim boundaries, and navigation depth

The PDF title page uses deterministic non-numbered cover art from
`output/figures/cover/ageint-cover-synthesis.png`, with a JSON sidecar beside
it. The cover is rendered by `src/figures/` and referenced from
`docs/manuscript/config.yaml` as `book.cover.image`; it is not registered in
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
`\setcounter{tocdepth}{2}` in `docs/manuscript/preamble.md`. H3/H4 scaffolds remain
available in body text and generated HTML, but they are hidden from the PDF TOC
to keep navigation useful at the manuscript scale. Generated modules expose three
chapter-specific H2 landmarks: source/profile frame, practice-lens path, and
assurance handoff. The repeated orientation, practice, evidence, governance, and
assessment scaffolds, plus teaching details such as topic lessons, transfer
architecture, evidence spine, reviewer route, and learning-path links, stay as
chapter-specific H3/H4 body headings rather than generic repeated TOC labels.
The same preamble owns TOC spacing controls so entries such as
`42.10 Evidence...` do not collapse into `42.10Evidence...`.

PDF rendering and local validation do not publish an edition. The repository
already records concept DOI `10.5281/zenodo.20732274` and Edition 0.1 DOI
`10.5281/zenodo.20732275`; a local revision does not imply a new upload, release
approval or permission to push.

## Current local artifact evidence and limits

Use `output/reports/current_artifact_evidence.{json,md}` for the artifact-specific
measurement and its timestamp. Related source-metadata, freshness, scholarship,
claim-calibration and figure reports retain their own scope and warning counts.
Do not promote old page/link/citation totals into current measurements. The
authoritative local render is `output/pdf/AGEINT_combined.pdf`; `AGEINT.pdf`
must be copied from that render, not built independently.

The 2026-11-06 revision adds source-specific teaching notes across all 51
chapters, 16 concrete unit workflows, nine offline methods workbooks, a common
analytic workflow, full-topic assessment groups and completed chapter 35/36
examples. Source counts and figure identities are retained. Source routing and
heading navigation are structural aids, not verification of a claim's meaning.
Unknown citations now fail closed, but a real unrelated citation still needs a
passage-level relevance review. Synthetic outputs establish no learning gains,
legal compliance, live-model effectiveness or production safety.

Strict figure rendering requires `mmdc` and a usable browser. If Puppeteer's
expected downloaded headless shell is absent, set `CHROME_EXECUTABLE_PATH` to
an installed Chrome/Chromium executable before building; the renderer writes
that path into its generated Puppeteer configuration. Do not substitute
placeholder plates for delivery. A render pass is incomplete until changed
diagrams and representative actual PDF/HTML surfaces are visually checked.


## Related documentation: output inventory and manuscript syntax

- [`output_inventory.md`](output_inventory.md)
- [`manuscript/SYNTAX.md`](manuscript/SYNTAX.md)
