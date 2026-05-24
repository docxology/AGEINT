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

`manuscript/config.yaml` declares:

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

The `z_` prefix signals a compatibility entry that runs **after** analysis scripts when discovered alphabetically without an allowlist. With the allowlist, it is for manual invocation only.

## Archive directory

`scripts/archive/` holds one-off migration helpers. They are **not** pipeline scripts and are not discovered by Stage 02.

## Output paths

Scripts print final artifact paths to stdout for manifest collection. Generated outputs live under `output/` (disposable, regeneratable).

## See also

- [`AGENTS.md`](AGENTS.md) — script inventory
- [`../src/build_pipeline.py`](../src/build_pipeline.py) — canonical build orchestration
- [`../manuscript/config.yaml`](../manuscript/config.yaml) — analysis allowlist
