# Test Patterns — AGEINT

## Path bootstrap

`conftest.py` inserts `src/` and `tests/` on `sys.path`, calls `ensure_project_paths`, and resolves the sibling template repo via `template_resolver.ensure_template_repo_on_path`.

## Session fixture: `built_output`

The session-scoped fixture returns the existing project `output/` directory.
It never builds missing artifacts or refreshes stale evidence, even when the
SDK is discoverable. Run the explicit generation workflow in a development or
fresh acceptance checkout before validating a newly built edition; do not
regenerate a checked-in publication to hide its original failures.

## Inventory helpers

`tests/manuscript_quality/inventory_helpers.py` provides:

- `manuscript_dir(built_output)` — path to `output/manuscript/`
- `generated_chapter_files`, `generated_output_files`
- `chapter_text`, `section_text` — load generated markdown for assertions

Split across `test_manuscript_inventory_structure.py` and `test_manuscript_inventory_quality.py` to keep files under the 500-line inventory gate.

## Script smoke tests

`test_scripts.py` subprocess-invokes `setup_hook.py`, `generate_figures.py`, and `z_generate_manuscript_variables.py` without mocks.

## Branch coverage

`test_coursebook_branch_coverage.py` uses `monkeypatch.delenv` only for template-repo resolution error paths.

## Running

Use the same prepared SDK environment as the [full workflow](../README.md#commands):

```bash
python -m pytest tests/ --cov=src --cov-fail-under=90
```

## See also

- [`../docs/testing_philosophy.md`](../docs/testing_philosophy.md)
