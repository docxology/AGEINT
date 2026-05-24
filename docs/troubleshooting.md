# Troubleshooting — AGEINT

## Build fails with import errors

Run from AGEINT root or ensure template repo is on path via `src/template_resolver.py`. Set `AGEINT_TEMPLATE_REPO` or `DOCXOLOGY_TEMPLATE_REPO` when running standalone outside the template checkout.

## `output/manuscript/` missing

```bash
uv run python scripts/build_curriculum.py
```

Or run tests (session `built_output` fixture triggers build).

## Pillow / figure render errors under root interpreter

Root `pyproject.toml` includes `pillow` for pipeline Stage 02. Run `uv sync` at template repo root.

## Validation: unresolved references

Rebuild, then:

```bash
uv run python -m infrastructure.validation.cli markdown projects/AGEINT/output/manuscript --repo-root .
```

Fix cross-refs in `src/manuscript_manifest/` or `src/markdown_refs.py`, not in generated output.

## PDF Mermaid failures

Install headless Chrome for `mmdc`, or use placeholder figures for smoke runs (`generate_figures.py --allow-placeholder-figures`).

## Tests slow on first run

Session fixture runs full `run_build()` once. Subsequent tests reuse `output/`.

## See also

- [`faq.md`](faq.md)
- [`quickstart.md`](quickstart.md)
