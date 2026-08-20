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
**Read the numeric prefix as a layer, not as an ordering.** `figures/__init__.py`
imports every module by explicit name, so nothing depends on filename sort order.
The prefixes group modules by role; the letter suffixes (`_03l`, `_03q`, `_03r`)
record where a layer was extended after the repo-wide 500-line cap
(`tests/test_file_size_inventory.py`) forced a split. Renaming is therefore safe
for imports, but the layer prefix is what keeps this directory legible — keep it
when adding files.

| Layer | Meaning |
| --- | --- |
| `_01*` | **Specs** — registry rows and figure metadata (data; few or no functions) |
| `_02*` | **Machinery** — spec building, render dispatch, Mermaid, reader text, audits |
| `_03*` | **Renderers** — one module per visual or closely-related family |
| `_04*` | Registry helpers and PNG canvas normalization |
| `_05*` | Shared visual style primitives |
| `_06*` | Python renderer dispatch table |

### Specs (`_01*`)

| Module | Role |
| --- | --- |
| `_01_part.py` | `FigureKind`, `FigureSpec`, `PYTHON_VISUALS`, registry helpers |
| `_01j_historical_spec.py` | `HISTORICAL_ASSETS` public-domain imagery specs |
| `_01b_accessibility.py` | Accessibility-guidance registry rows |
| `_01c_artifact_evidence_spec.py` | Rows for verifier-first artifact-evidence visuals |
| `_01d_scholarship_quality_spec.py` | Rows for scholarship-quality audit visuals |
| `_01e_sat_method_spec.py` | Rows for Synthetic Analytic Tradecraft and validation visuals |
| `_01f_source_metadata_spec.py` | Rows for source-metadata integrity visuals |
| `_01g_concept_plates.py` | Data-backed deterministic concept-plate specs |
| `_01h_claim_calibration_spec.py` | Rows for claim-calibration and visual-semantics visuals |
| `_01i_early_orientation_spec.py` | Rows for the early-orientation reader visuals |

### Machinery (`_02*`)

| Module | Role |
| --- | --- |
| `_02_part.py` | `render_figures()`, `load_figure_registry()`, render dispatch |
| `_02b_mermaid.py` | `render_mermaid_figure()`, `mermaid_source()`, `placeholder_or_fail()` |
| `_02c_reader_text.py` | Caption, alt-text, and long-description expansion |
| `_02d_quality_audit.py` | `write_visual_quality_audit()` — the figure quality gates |
| `_02e_visual_semantics.py` | Semantic-role, evidence-role, counting-rule, interpretation-limit defaults |

### Renderers (`_03*`)

| Module | Role |
| --- | --- |
| `_03_part.py` | Core matplotlib chart renderers and figure builder dispatch |
| `_03s_drawers.py` | Chart and plate drawing primitives (`_draw_bar_chart`, `_draw_loop`, `_draw_concept_plate`) |
| `_03b_asset_renderers.py` | Historical, AI-concept, and citation-density assets |
| `_03c_control_matrix.py` | `draw_control_matrix()`, `draw_evidence_dashboard()`, `draw_matrix()` |
| `_03d_accessibility.py` | Visual accessibility contract |
| `_03e_quality_dashboard.py` | Visual quality-audit dashboard |
| `_03f_artifact_evidence.py` | Verifier-first artifact-evidence control loop |
| `_03g_scholarship_quality.py` | Scholarship triangulation map |
| `_03h_sat_method.py` | Synthetic tradecraft method contract |
| `_03i_analysis_validation.py` | Analysis validation matrix |
| `_03j_analysis_family_coverage.py` | Analysis-validation family coverage |
| `_03k_source_metadata.py` | Source-metadata integrity |
| `_03l_cover_art.py` | `render_cover_art()` — cover composition |
| `_03m_graphical_abstract.py` | Graphical abstract atlas |
| `_03n_claim_calibration.py` | Claim calibration and visual semantics |
| `_03o_source_refresh_due.py` | Source-refresh due-date readiness dashboard |
| `_03p_agency_source_coverage.py` | US IC agency source-coverage dashboard |
| `_03q_frontmatter_transit.py` | `render_evidence_transit_map()` — frontmatter transit map |
| `_03r_early_orientation.py` | Reader route compass, tradecraft workbench, source constellation |

### Support

| Module | Role |
| --- | --- |
| `_04_part.py` | Registry helpers, `_normalize_png_canvas()`, PNG asset validation |
| `_05_visual_style.py` | `wrap_lines()`, `draw_title_band()`, `draw_footer()`, palette |
| `_06_python_renderers.py` | `render_python_figure()` and the `PYTHON_VISUALS` dispatch table |
| `mermaid_contracts.py` | Mermaid diagram-type contracts |

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
