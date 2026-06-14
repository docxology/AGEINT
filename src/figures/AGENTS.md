# AGENTS.md — `figures/`

Registry-backed figure generation for AGEINT. All PNG assets land under
`output/figures/`; metadata is written to `output/figures/figure_registry.json`.
The registry is also the accessibility and visual-semantics contract: every
figure row must carry a substantial caption, short alt text, long description,
source section, provenance, semantic role, evidence role, quantitative status,
unit, denominator, counting rule, interpretation limit, and asset hash.
Generated PNGs must embed the same compact accessibility/provenance/semantics fields as text metadata so the image remains
inspectable if copied outside the registry. The build also writes
`output/figures/visual_quality_audit.json`; update that audit contract and its
tests when adding new figure quality gates.

Part modules merge at import via `figures/__init__.py`. Keep `_02_part.py`
≤500 lines; Mermaid and placeholder helpers live in `_02b_mermaid.py`.

## Module layout

| Module | Role |
| --- | --- |
| `_01_part.py` | `FigureKind`, `FigureSpec`, `build_figure_specs()`, registry helpers |
| `_01c_artifact_evidence_spec.py` | Registry rows for verifier-first artifact-evidence visuals |
| `_01d_scholarship_quality_spec.py` | Registry rows for scholarship-quality audit visuals |
| `_01h_claim_calibration_spec.py` | Registry rows for claim-calibration and visual-semantics visuals |
| `_02_part.py` | `render_figures()`, `_render_figure_asset()`, Python/historical/AI render dispatch |
| `_02b_mermaid.py` | `render_mermaid_figure()`, `mermaid_source()`, `placeholder_or_fail()` |
| `_03_part.py` | Matplotlib/Python chart renderers, `_draw_text_plate()`, canvas normalization |
| `_03f_artifact_evidence.py` | Verifier-first artifact-evidence control-loop visual |
| `_03g_scholarship_quality.py` | Scholarship triangulation audit visual |
| `_03n_claim_calibration.py` | Claim-calibration and visual-semantics control visual |
| `_04_part.py` | Public re-exports |
| `_05_visual_style.py` | Shared palette, title/footer, wrapping, and arrow helpers |
| `_06_python_renderers.py` | Python renderer dispatch and source-metadata charts |

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

- `tests/test_figures.py` — registry integrity, substantial captions/alt text/long descriptions, square-normalized canvases, provenance, strict Mermaid (`requires_mermaid`)
- `tests/test_figure_quality_audit.py` — visual-quality audit parity, PNG metadata, and artifact-evidence figure registration
- `tests/test_file_size_inventory.py` — 500-line cap on `_02_part.py`

## Editing rules

- Add compact new Python visuals in `_03_part.py` or a small helper module, wire dispatch in `_06_python_renderers.py`, and register them through `PYTHON_VISUALS` or a data-only shard imported by it.
- Preserve the official accessibility-guidance metadata in `_01_part.py`; use Perplexity only as discovery or second-opinion research, then verify final guidance against direct official sources before encoding it.
- Do not hard-code figure numbers; use `fig:` labels and Pandoc-crossref in manuscript prose.
- Rebuild: `uv run python scripts/generate_figures.py` or full `scripts/build_curriculum.py`.
