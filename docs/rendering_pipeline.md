# Rendering Pipeline — AGEINT

AGEINT does not use numbered source chapters under `manuscript/`. The PDF pipeline reads **generated** markdown from `output/manuscript/`.

## Resolution

`infrastructure.rendering.pipeline._resolve_manuscript_dir` prefers `output/manuscript/` when it contains markdown, and refreshes `config.yaml` and `*.bib` from source `manuscript/`.

## Build before render

```bash
uv run python scripts/build_curriculum.py
```

From template repo root after build and PDF render:

```bash
uv run python scripts/03_render_pdf.py --project AGEINT
uv run python scripts/05_copy_outputs.py --project AGEINT
uv run python -m infrastructure.validation.cli pdf output/AGEINT/pdf/AGEINT_combined.pdf
```

## Pre-flight validation

```bash
uv run python -m infrastructure.validation.cli markdown projects/AGEINT/output/manuscript --repo-root .
uv run python -m infrastructure.validation.cli prerender projects/AGEINT/output/manuscript --repo-root .
```

## Mermaid figures

AGEINT renders 24 Mermaid figures via `mmdc` into `output/figures/mermaid/`: 17
curriculum and part module maps plus 7 synthesis methods diagrams (CDR cascade,
MAESTRO layers, SRE circuit breaker, decoherence-degradation isomorphism, unified
epistemic stack, cognitive attack layers, HRO governance crosswalk). Strict
verification requires real diagram PNGs, not deterministic text-plate fallbacks.

```bash
# Strict build (fail instead of placeholder PNGs when mmdc/Chrome is missing)
AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/build_curriculum.py

# One-time Chrome install for mmdc (if renders fail)
npx --yes puppeteer browsers install chrome-headless-shell@131.0.6778.204
```

Confirm `mmdc` and `pandoc-crossref` are on `PATH` before PDF render. Combined
PDF rendering may also require `chrome-headless-shell` for inline Mermaid in
other projects; AGEINT pre-rasterizes module maps under `output/figures/mermaid/`.
See template [`docs/operational/troubleshooting/common-errors.md`](../../../docs/operational/troubleshooting/common-errors.md).

Run strict figure tests:

```bash
uv run pytest tests/test_figures.py -m requires_mermaid -v
```

## See also

- [`output_inventory.md`](output_inventory.md)
- [`../manuscript/SYNTAX.md`](../manuscript/SYNTAX.md)
