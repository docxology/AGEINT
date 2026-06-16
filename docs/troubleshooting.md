# Troubleshooting - AGEINT build, render, validation, and routing failures

## Build import errors: package path and `uv` environment checks

Run from AGEINT root or ensure template repo is on path via `src/template_resolver.py`. Set `AGEINT_TEMPLATE_REPO` or `DOCXOLOGY_TEMPLATE_REPO` when running standalone outside the template checkout.

Manuscript variable substitution goes through `src/manuscript_injection.py`, which calls `ensure_template_repo_on_path()` then delegates to `infrastructure.rendering.manuscript_injection`. Standalone AGEINT builds and template-linked `./run.sh --project AGEINT` runs share this adapter.

## Missing `output/manuscript/`: rebuild the generated manuscript tree

```bash
uv run python scripts/build_curriculum.py
```

Or run tests (session `built_output` fixture triggers build).

## Pillow and figure render errors: use the project runtime and dependencies

Root `pyproject.toml` includes `pillow` for pipeline Stage 02. Run `uv sync` at template repo root.

## Unresolved reference validation: labels, BibTeX, and generated config checks

Rebuild, then:

```bash
uv run python -m infrastructure.validation.cli markdown projects/working/AGEINT/output/manuscript --repo-root .
uv run python -m infrastructure.validation.cli prerender projects/working/AGEINT/output/manuscript --repo-root .
```

Fix cross-refs in `src/manuscript_manifest/` or `src/markdown_refs.py`, not in generated output.

## PDF Mermaid failures: Chrome, `mmdc`, and strict render setup

Install headless Chrome for `mmdc`, or use placeholder figures for smoke runs (`generate_figures.py --allow-placeholder-figures`).

## Slow first test run: session fixture build and generated-output reuse

Session fixture runs full `run_build()` once. Subsequent tests reuse `output/`.

## Evidence or artifact prompt parity failures: regenerate YAML parity fixtures

Regenerate the committed tables and parity fixture:

```bash
uv run python scripts/generate_topic_prompt_routes_yaml.py
uv run python scripts/generate_prompt_parity_fixture.py
uv run pytest tests/test_topic_frame_routing.py::test_evidence_and_artifact_prompts_match_curriculum_parity_fixture -v
uv run python scripts/build_curriculum.py
```

Risk-category parity follows the same pattern with `scripts/generate_risk_routes_yaml.py` and `tests/fixtures/risk_category_parity.json`.

## Rotation field parity failures: regenerate rotation fixtures

```bash
uv run python scripts/generate_topic_rotation_templates_yaml.py
uv run python scripts/generate_rotation_parity_fixture.py
uv run pytest tests/test_topic_frame_routing.py::test_rotation_fields_match_curriculum_parity_fixture -v
uv run python scripts/build_curriculum.py
```

## Shard import errors after intelligence-content edits: update package imports

Each `intelligence_content` part module must declare explicit imports (merge seeding is removed for that package only). Verify with:

```bash
uv run pytest tests/test_intelligence_content_imports.py -v
```

`manuscript_manifest/`, `figures/`, and `manuscript_variables/` also use explicit
cross-part imports (no merge loader). Verify with:

```bash
uv run pytest tests/test_package_imports.py -v
```

## Related documentation: quickstart, rendering, output, and tests

- [`faq.md`](faq.md)
- [`quickstart.md`](quickstart.md)
