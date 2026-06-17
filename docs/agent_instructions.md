# Agent Instructions - AGEINT editing, safety, and verification contract

Operational constraints for agents editing this project. Full system map: [`../AGENTS.md`](../AGENTS.md).

## Editing rules: source-owned changes and generated-output discipline

- Keep scripts thin; business logic in `src/` only.
- Regenerate after source, template, figure, or renderer edits: `uv run python scripts/build_curriculum.py`.
- Do not edit `output/manuscript/` by hand — update `data/curriculum/`, templates, `src/manuscript_manifest/`, or `src/intelligence_content/`.
- Preserve citation keys `ageintNNN` when source identity is unchanged; append new guide references after the locked range.
- Use label-backed cross-refs (`[@sec:…]`, `[@fig:…]`, `[@ageintNNN]`), not hard-coded figure or section numbers.
- Keep figure captions, alt text, and long descriptions source-owned, substantial, and reader-informative; generated PDFs must link to sections, figures, citations, or external sources, not local `.md` files.

## Safety posture: defensive, educational, accountable, and evidence-bounded work

Dual-use material stays defensive, educational, accountable, synthetic, and evidence-bounded. See [`safety.md`](safety.md) and [`safety_audit.md`](safety_audit.md).

## Verification before claiming done: rebuild, audits, tests, and validators

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run python -m infrastructure.validation.cli markdown projects/working/AGEINT/output/manuscript --repo-root .
uv run python -m infrastructure.validation.cli prerender projects/working/AGEINT/output/manuscript --repo-root .
```

## Related documentation: source rules, syntax, rendering, and tests

- [`testing_philosophy.md`](testing_philosophy.md)
- [`architecture.md`](architecture.md)
- [`quickstart.md`](quickstart.md)
