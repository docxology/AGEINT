# Script Conventions — AGEINT

Orchestration rules for `scripts/` in the AGEINT curriculum project.

## Thin orchestrator rules

Scripts **coordinate** — they never **compute**:

```python
# Correct: delegate to src/build_pipeline.py
from build_pipeline import run_build
result = run_build(PROJECT_ROOT)
```

Business logic belongs in `src/` (`build_pipeline.py`, `curriculum.py`, `manuscript_manifest/`, etc.).

## Pipeline Stage 02 allowlist

`docs/manuscript/config.yaml` declares:

```yaml
analysis:
  scripts:
    - build_curriculum.py
```

Infrastructure reads this via `infrastructure.core.script_discovery._configured_analysis_scripts`.
The default full pipeline runs **one** canonical build per project invocation.

## Script roles

| Script | Pipeline Stage 02 | Purpose |
| --- | --- | --- |
| `build_curriculum.py` | Yes (allowlisted) | Full build: data mirror, variables, BibTeX, figures, manuscript |
| `generate_figures.py` | No | Manual figure-only refresh when curriculum data already exists |
| `z_generate_manuscript_variables.py` | No | Template compatibility shim; delegates to full `run_build()` |
| `setup_hook.py` | No | Post-clean output doc scaffolding (`_NON_ANALYSIS_SCRIPT_NAMES`) |
| `generate_topic_prompt_routes_yaml.py` | No | Regenerates `data/topic_prompt_routes.yaml` from canonical tables in `src/topic_route_tables.py` (regenerable, idempotent) |
| `generate_topic_rotation_templates_yaml.py` | No | Regenerates `data/topic_rotation_templates.yaml` from canonical tables in `src/topic_route_tables.py` (regenerable, idempotent) |
| `generate_prompt_parity_fixture.py` / `generate_rotation_parity_fixture.py` | No | Regenerate parity fixtures under `tests/fixtures/` from the live curriculum |

`AGENTS.md` is the canonical script inventory. Audit/coverage and
declarative-YAML validation scripts (`audit_*.py`, `check_rendered_references.py`,
`count_citations.py`, `validate_declarative_yaml.py`, `generate_risk_routes_yaml.py`)
are manual CLI wrappers over `src/` modules and are not pipeline-discovered.

## Archive directory

`scripts/archive/` holds one-off migration helpers. They are **not** pipeline scripts and are not discovered by Stage 02.

## Output paths

Scripts print final artifact paths to stdout for manifest collection. Generated outputs live under `output/` (disposable, regeneratable).

## See also

- [`AGENTS.md`](AGENTS.md) — script inventory
- [`../src/build_pipeline.py`](../src/build_pipeline.py) — canonical build orchestration
- [`../docs/manuscript/config.yaml`](../docs/manuscript/config.yaml) — analysis allowlist
