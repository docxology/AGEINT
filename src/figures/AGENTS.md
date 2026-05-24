# AGENTS.md — `figures/`

Registry-backed figure generation for AGEINT. All PNG assets land under
`output/figures/`; metadata is written to `output/figures/figure_registry.json`.

Part modules merge at import via `figures/__init__.py`. Keep `_02_part.py`
≤500 lines; Mermaid and placeholder helpers live in `_02b_mermaid.py`.

## Module layout

| Module | Role |
| --- | --- |
| `_01_part.py` | `FigureKind`, `FigureSpec`, `build_figure_specs()`, registry helpers |
| `_02_part.py` | `render_figures()`, `_render_figure_asset()`, Python/historical/AI render dispatch |
| `_02b_mermaid.py` | `render_mermaid_figure()`, `mermaid_source()`, `placeholder_or_fail()` |
| `_03_part.py` | Matplotlib/Python chart renderers, `_draw_text_plate()`, canvas normalization |
| `_04_part.py` | Public re-exports |

## Placeholder figures (CI / headless builds)

`render_figures(..., allow_placeholder_figures=True)` is the default. When
`mmdc`/Chrome is unavailable or a render fails, deterministic text-plate PNGs
are written instead of raising—keeping tests and `run_build()` green.

| Entry point | Default placeholder behavior |
| --- | --- |
| `run_build()` | Placeholders **on** unless `AGEINT_REQUIRE_RENDERED_FIGURES=1` |
| `scripts/generate_figures.py` | Same env rule; `--no-allow-placeholder-figures` for strict local renders |
| `scripts/build_curriculum.py` | Delegates to `run_build()` |

Set `AGEINT_REQUIRE_RENDERED_FIGURES=1` when validating full Mermaid PNG output locally.

Strict Mermaid renders need `mmdc` plus `chrome-headless-shell` in the Puppeteer
cache. `_02b_mermaid._discover_chrome_executable()` prefers the mmdc-pinned build
(`131.0.6778.204`) when present, then falls back to any cached shell. Override
with `CHROME_EXECUTABLE_PATH` when needed.

One-time install:

```bash
npx --yes puppeteer browsers install chrome-headless-shell@131.0.6778.204
```

Run strict figure tests: `uv run pytest tests/test_figures.py -m requires_mermaid -v`

## Public API

Import from `figures` or `src/__init__.py`:

- `build_figure_specs(curriculum, manifest)`
- `render_figures(project_root, curriculum, manifest=None, *, allow_placeholder_figures=True)`
- `load_figure_registry(path)`
- `figures_for_section(figures, section_relative_path)`
- `figure_markdown(figure, project_root=..., manuscript_output_dir=..., section_relative_path=...)`

## Tests

- `tests/test_figures.py` — registry integrity, square-normalized canvases, provenance, strict Mermaid (`requires_mermaid`)
- `tests/test_file_size_inventory.py` — 500-line cap on `_02_part.py`

## Editing rules

- Add new Python visuals in `_03_part.py` and register them in `build_figure_specs()`.
- Do not hard-code figure numbers; use `fig:` labels and Pandoc-crossref in manuscript prose.
- Rebuild: `uv run python scripts/generate_figures.py` or full `scripts/build_curriculum.py`.
