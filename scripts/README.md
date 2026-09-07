# AGEINT Scripts

This folder contains thin AGEINT orchestration entrypoints: argparse, path
bootstrap, status output, and one delegated call into `src/`. Business logic
lives in `src/`; see [`AGENTS.md`](AGENTS.md) for the thin-orchestrator
contract and [`CONVENTIONS.md`](CONVENTIONS.md) for pipeline-stage rules.

- Owner: project build and hydration workflow.
- Status: manual code; scripts should call `src/` and infrastructure helpers.
- Source of truth: `src/build_pipeline.py`, `src/curriculum.py`, `src/manuscript_manifest/`, and `src/manuscript_variables/`.
- Main command: `uv run python scripts/build_curriculum.py`.
- Safety: scripts orchestrate defensive educational rendering only.

## Inventory

| Script | Purpose | Delegates to | Command |
| --- | --- | --- | --- |
| `build_curriculum.py` | Full build: data mirror, variables, BibTeX, figures, manuscript | `src/build_pipeline.run_build` | `uv run python scripts/build_curriculum.py` |
| `generate_figures.py` | Figure-only refresh and figure registry | `src/build_pipeline.run_build_figures`, `src/figures` | `uv run python scripts/generate_figures.py` |
| `z_generate_manuscript_variables.py` | Template-compatibility shim (runs the full build) | `src/build_pipeline.run_build` | `uv run python scripts/z_generate_manuscript_variables.py` |
| `setup_hook.py` | Output doc scaffolding after clean | `src/output_docs.write_output_directory_docs` | `uv run python scripts/setup_hook.py` |
| `audit_orchestration_contract.py` | Stage, audit, source-pack, and Mermaid contract report | `src/orchestration_audit` | `uv run python scripts/audit_orchestration_contract.py [--write]` |
| `audit_source_metadata.py` | Source-anchor metadata coverage report | `src/source_metadata` | `uv run python scripts/audit_source_metadata.py [--write]` |
| `audit_agency_source_coverage.py` | US IC agency-source pack coverage report | `src/agency_source_coverage` | `uv run python scripts/audit_agency_source_coverage.py [--write]` |
| `audit_claim_calibration.py` | Generated-manuscript claim calibration report | `src/claim_calibration` | `uv run python scripts/audit_claim_calibration.py [--write]` |
| `audit_scholarship_quality.py` | Generated-manuscript scholarship quality report | `src/scholarship_quality` | `uv run python scripts/audit_scholarship_quality.py [--write]` |
| `audit_reference_quality.py` | Generated-reference quality report | `src/reference_quality` | `uv run python scripts/audit_reference_quality.py [--write]` |
| `audit_publication_readiness.py` | Publication-readiness preflight report | `src/publication_readiness` | `uv run python scripts/audit_publication_readiness.py [--write]` |
| `audit_source_refresh_due.py` | Source-refresh due-date readiness report | `src/source_refresh_due` | `uv run python scripts/audit_source_refresh_due.py [--write]` |
| `audit_artifact_evidence.py` | Artifact evidence manifest report | `src/artifact_evidence` | `uv run python scripts/audit_artifact_evidence.py [--write]` |
| `audit_pdf_quality.py` | Rendered-PDF staleness and banned-phrase audit (informational; PDF rendered by the sibling template repo) | `src/pdf_quality` | `uv run python scripts/audit_pdf_quality.py` |
| `audit_heading_support.py` | Heading reference-support audit | `src/rendered_heading_support` | `uv run python scripts/audit_heading_support.py` |
| `check_rendered_references.py` | Hard-coded section-reference scan of rendered output | `src/rendered_reference_audit.audit_rendered_references` | `uv run python scripts/check_rendered_references.py [output_root]` |
| `count_citations.py` | Source and generated-markdown citation counts | `src/citation_workflow`, `src/curriculum.load_curriculum` | `uv run python scripts/count_citations.py` |
| `generate_risk_routes_yaml.py` | Validates `data/topic_risk_routes.yaml` through the loader (name is historical) | `src/_data_loaders.topic_risk_routes_payload` | `uv run python scripts/generate_risk_routes_yaml.py` |
| `validate_declarative_yaml.py` | Validates authoritative declarative YAML tables | `src/_data_loaders.validate_declarative_tables` | `uv run python scripts/validate_declarative_yaml.py` |
| `generate_topic_prompt_routes_yaml.py` | Regenerates `data/topic_prompt_routes.yaml` from canonical tables (regenerable, idempotent) | `src/topic_route_tables.write_topic_prompt_routes_yaml` | `uv run python scripts/generate_topic_prompt_routes_yaml.py` |
| `generate_topic_rotation_templates_yaml.py` | Regenerates `data/topic_rotation_templates.yaml` from canonical tables (regenerable, idempotent) | `src/topic_route_tables.write_topic_rotation_templates_yaml` | `uv run python scripts/generate_topic_rotation_templates_yaml.py` |
| `generate_prompt_parity_fixture.py` | Regenerates `tests/fixtures/topic_prompt_parity.json` | `src/intelligence_content` prompt resolvers | `uv run python scripts/generate_prompt_parity_fixture.py` |
| `generate_rotation_parity_fixture.py` | Regenerates `tests/fixtures/topic_rotation_parity.json` | `src/intelligence_content` rotation resolvers | `uv run python scripts/generate_rotation_parity_fixture.py` |

`build_curriculum.py` delegates to `src/build_pipeline.run_build`, which refreshes
parsed JSON, mirrored output data, runtime variables, BibTeX, the figure registry,
and the semantic manuscript. The figure command is useful for focused visual checks
when source data already exists. `z_generate_manuscript_variables.py` exists for
template compatibility and delegates to the full build rather than maintaining a
parallel path.

One-time migration helpers live under [`archive/`](archive/README.md); normal builds
do not invoke them.
