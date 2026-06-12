# Troubleshooting — AGEINT

## Build fails with import errors

Run from AGEINT root or ensure template repo is on path via `src/template_resolver.py`. Set `AGEINT_TEMPLATE_REPO` or `DOCXOLOGY_TEMPLATE_REPO` when running standalone outside the template checkout.

Manuscript variable substitution goes through `src/manuscript_injection.py`, which calls `ensure_template_repo_on_path()` then delegates to `infrastructure.rendering.manuscript_injection`. Standalone AGEINT builds and template-linked `./run.sh --project AGEINT` runs share this adapter.

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
uv run python -m infrastructure.validation.cli markdown projects/working/AGEINT/output/manuscript --repo-root .
uv run python -m infrastructure.validation.cli prerender projects/working/AGEINT/output/manuscript --repo-root .
```

Fix cross-refs in `src/manuscript_manifest/` or `src/markdown_refs.py`, not in generated output.

## PDF Mermaid failures

Install headless Chrome for `mmdc`, or use placeholder figures for smoke runs (`generate_figures.py --allow-placeholder-figures`).

## Tests slow on first run

Session fixture runs full `run_build()` once. Subsequent tests reuse `output/`.

## Evidence or artifact prompt parity fails after YAML edits

Regenerate the committed tables and parity fixture:

```bash
uv run python scripts/generate_topic_prompt_routes_yaml.py
uv run python scripts/generate_prompt_parity_fixture.py
uv run pytest tests/test_topic_frame_routing.py::test_evidence_and_artifact_prompts_match_curriculum_parity_fixture -v
uv run python scripts/build_curriculum.py
```

Risk-category parity follows the same pattern with `scripts/generate_risk_routes_yaml.py` and `tests/fixtures/risk_category_parity.json`.

## Rotation field parity fails after YAML edits

```bash
uv run python scripts/generate_topic_rotation_templates_yaml.py
uv run python scripts/generate_rotation_parity_fixture.py
uv run pytest tests/test_topic_frame_routing.py::test_rotation_fields_match_curriculum_parity_fixture -v
uv run python scripts/build_curriculum.py
```

## Shard import errors after intelligence_content edits

Each `intelligence_content` part module must declare explicit imports (merge seeding is removed for that package only). Verify with:

```bash
uv run pytest tests/test_intelligence_content_imports.py -v
```

`manuscript_manifest/`, `figures/`, and `manuscript_variables/` also use explicit
cross-part imports (no merge loader). Verify with:

```bash
uv run pytest tests/test_package_imports.py -v
```

## See also

- [`faq.md`](faq.md)
- [`quickstart.md`](quickstart.md)
