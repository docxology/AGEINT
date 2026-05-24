# Agent Instructions — AGEINT

Operational constraints for agents editing this project. Full system map: [`../AGENTS.md`](../AGENTS.md).

## Editing rules

- Keep scripts thin; business logic in `src/` only.
- Regenerate after source, template, figure, or renderer edits: `uv run python scripts/build_curriculum.py`.
- Do not edit `output/manuscript/` by hand — update `data/curriculum/`, templates, `src/manuscript_manifest/`, or `src/intelligence_content/`.
- Preserve citation keys `ageintNNN` when source identity is unchanged; append new guide references after the locked range.
- Use label-backed cross-refs (`[@sec:…]`, `[@fig:…]`, `[@ageintNNN]`), not hard-coded figure or section numbers.

## Safety posture

Dual-use material stays defensive, educational, authorized, synthetic, and non-operational. See [`safety.md`](safety.md) and [`safety_audit.md`](safety_audit.md).

## Verification before claiming done

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run python -m infrastructure.validation.cli markdown projects/AGEINT/output/manuscript --repo-root .
```

## See also

- [`testing_philosophy.md`](testing_philosophy.md)
- [`architecture.md`](architecture.md)
- [`quickstart.md`](quickstart.md)
