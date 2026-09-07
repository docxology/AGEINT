# AGENTS.md - AGEINT Scripts

Keep scripts thin. Business logic belongs in `src/`; scripts parse arguments,
bootstrap paths, call helpers, and print concise status. A thin orchestrator
is: argparse (when it takes flags) + path bootstrap via
`src/_paths.ensure_project_paths()` + logging/status output + a single
delegated call into a `src/<pkg>/` entrypoint. No business, data, plot, or
analysis logic lives in `scripts/`: authoritative data-as-code tables belong
in `src/` or a `data/` file the `src/` loader reads, never inline in a script.

Do not add scraping, exploitation, live collection, target tracking, or
operational response logic. Any dual-use topic must remain synthetic,
authorized, tabletop, or owned-lab only.

## Script inventory

| Script | Role |
| --- | --- |
| `build_curriculum.py` | CLI wrapper → `src/build_pipeline.run_build()` (canonical entry point) |
| `generate_figures.py` | Figure-only pass → `src/build_pipeline.run_build_figures()` + `src/figures/` registry |
| `z_generate_manuscript_variables.py` | Template compatibility; delegates to full `run_build()` |
| `setup_hook.py` | Post-clean output doc scaffolding → `src/output_docs.write_output_directory_docs()` |
| `audit_orchestration_contract.py` | CLI wrapper → `src/orchestration_audit` for stage, audit, source-pack, and Mermaid contract reports |
| `audit_source_metadata.py` | CLI wrapper → `src/source_metadata` source-anchor metadata coverage report |
| `audit_agency_source_coverage.py` | CLI wrapper → `src/agency_source_coverage` US IC agency-source pack coverage report |
| `audit_claim_calibration.py` | CLI wrapper → `src/claim_calibration` generated-manuscript claim calibration report |
| `audit_scholarship_quality.py` | CLI wrapper → `src/scholarship_quality` generated-manuscript scholarship report |
| `audit_reference_quality.py` | CLI wrapper → `src/reference_quality` generated-reference quality report |
| `audit_publication_readiness.py` | CLI wrapper → `src/publication_readiness` publication preflight (parent guard unless `--skip-parent-guard`) |
| `audit_source_refresh_due.py` | CLI wrapper → `src/source_refresh_due` source-refresh due-date readiness report |
| `audit_artifact_evidence.py` | CLI wrapper → `src/artifact_evidence` artifact evidence manifest report |
| `audit_pdf_quality.py` | CLI wrapper → `src/pdf_quality` rendered-PDF staleness/banned-phrase audit (informational here; the PDF is rendered by the sibling template repo) |
| `audit_heading_support.py` | CLI wrapper → `src/rendered_heading_support` heading reference-support audit |
| `check_rendered_references.py` | CLI wrapper → `src/rendered_reference_audit.audit_rendered_references` hard-coded section-reference scan |
| `count_citations.py` | CLI wrapper → `src/citation_workflow` + `src/curriculum.load_curriculum` citation coverage counts |
| `generate_risk_routes_yaml.py` | Validation wrapper → `src/_data_loaders.topic_risk_routes_payload` (name is historical; it validates `data/topic_risk_routes.yaml`) |
| `validate_declarative_yaml.py` | Validation wrapper → `src/_data_loaders.validate_declarative_tables` |
| `generate_topic_prompt_routes_yaml.py` | Thin regenerable generator → `src/topic_route_tables.write_topic_prompt_routes_yaml` (emits `data/topic_prompt_routes.yaml`) |
| `generate_topic_rotation_templates_yaml.py` | Thin regenerable generator → `src/topic_route_tables.write_topic_rotation_templates_yaml` (emits `data/topic_rotation_templates.yaml`) |
| `generate_prompt_parity_fixture.py` | Fixture generator → curriculum prompt resolvers; writes `tests/fixtures/topic_prompt_parity.json` |
| `generate_rotation_parity_fixture.py` | Fixture generator → curriculum rotation resolvers; writes `tests/fixtures/topic_rotation_parity.json` |

Report/audit scripts share the same shape: `--format {markdown,json}` for
stdout reporting and `--write` to refresh `output/reports/<name>.{json,md}`;
they exit non-zero when the underlying report is not ok.

### One-shot vs regenerable

- `generate_topic_prompt_routes_yaml.py` and
  `generate_topic_rotation_templates_yaml.py` are **regenerable**, not
  one-shot: their canonical tables live in `src/topic_route_tables.py`, and
  rerunning them rewrites `data/topic_prompt_routes.yaml` /
  `data/topic_rotation_templates.yaml` idempotently.
  `tests/test_topic_route_tables.py` fails on drift between the canonical
  tables and the committed YAML. Edit the tables in `src/`, then regenerate;
  never change the committed YAML without the matching edit in
  `src/topic_route_tables.py`.
- `generate_prompt_parity_fixture.py` and `generate_rotation_parity_fixture.py`
  regenerate parity fixtures in `tests/fixtures/` when curriculum data or
  resolver behavior changes intentionally; regenerate rather than hand-edit.
- One-time migration helpers live under [`archive/`](archive/README.md); they
  are retained for history only, are not pipeline scripts, and are excluded
  from this inventory's contracts.

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
