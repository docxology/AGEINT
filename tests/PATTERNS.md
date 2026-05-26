# Test Patterns — AGEINT

## Path bootstrap

`conftest.py` inserts `src/` and `tests/` on `sys.path`, calls `ensure_project_paths`, and resolves the sibling template repo via `template_resolver.ensure_template_repo_on_path`.

## Session fixture: `built_output`

```python
@pytest.fixture(scope="session")
def built_output() -> Path:
    ...
```

Runs `run_build(PROJECT_ROOT)` when manuscript or figure registry is absent. Most inventory and reader-quality tests depend on this.

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

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
```

## See also

- [`../docs/testing_philosophy.md`](../docs/testing_philosophy.md)
