# Testing Philosophy — AGEINT

## No mocks

Tests use real curriculum shards, real builds, temp directories, and subprocess script smoke tests. Do not use `unittest.mock`, `MagicMock`, or `mocker.patch`. Environment isolation via pytest `monkeypatch.delenv` is limited to template-resolver branch tests.

## Session build fixture

`tests/conftest.py` defines `built_output` (session scope). It runs `run_build()` once when `output/manuscript/` or `output/figures/figure_registry.json` is missing. Integration tests depend on this generated tree.

## Test categories

| Area | Example modules |
| --- | --- |
| Curriculum shards | `test_curriculum.py`, `test_sharded_data_integrity.py` |
| Source identity | `test_source_identity.py` |
| Manuscript manifest | `test_manuscript_manifest.py`, `test_manuscript_inventory_*.py` |
| Reader quality | `test_reader_quality.py`, `test_topic_content_quality.py` |
| Safety | `test_manuscript_safety_docs.py` |
| Cross-refs | `test_manuscript_crossrefs.py` |
| Scripts | `test_scripts.py`, `test_build_curriculum_script.py` |

## Coverage gate

90% minimum on `src/` (`pyproject.toml` `fail_under = 90`). Combined multi-project pytest union is skipped via `[tool.template] skip_combined_pytest = true` because the full build is expensive.

## See also

- [`../tests/PATTERNS.md`](../tests/PATTERNS.md)
- [`agent_instructions.md`](agent_instructions.md)
