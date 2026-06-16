# AGENTS.md - AGEINT Scripts

Keep scripts thin. Business logic belongs in `src/`; scripts parse arguments, route paths, call helpers, and print concise status.

Do not add scraping, exploitation, live collection, target tracking, or operational response logic. Any dual-use topic must remain synthetic, authorized, tabletop, or owned-lab only.

## Script roles

| Script | Role |
| --- | --- |
| `build_curriculum.py` | CLI wrapper → `src/build_pipeline.run_build()` |
| `generate_figures.py` | Figure-only pass; loads curriculum data and calls `src/figures/` (placeholder default matches `run_build()` via `AGEINT_REQUIRE_RENDERED_FIGURES`) |
| `audit_orchestration_contract.py` | CLI wrapper → `src/orchestration_audit` for stage, audit, source-pack, and Mermaid contract reports |
| `setup_hook.py` | Post-clean output doc scaffolding (README/AGENTS under `output/`) |
| `z_generate_manuscript_variables.py` | Template compatibility; delegates to full `run_build()` |

`build_curriculum.py` is the canonical entry point: mirror curriculum data to
`output/data/`, refresh variables and BibTeX, render figures, and render the
semantic manuscript under `output/manuscript/`. `z_generate_manuscript_variables.py`
is compatibility glue and should continue to delegate to the canonical build
path rather than maintaining a parallel pipeline.

Figure generation belongs in `src/figures/`; `generate_figures.py` should
remain a wrapper that loads curriculum data, calls the renderer, and reports
the registry path. By default, placeholders are allowed unless
`AGEINT_REQUIRE_RENDERED_FIGURES=1`; pass `--no-allow-placeholder-figures` for
strict local validation.

If a script needs new behavior, add a tested helper in `src/` first and keep
the script limited to argument parsing, path setup, function calls, and status
output.
