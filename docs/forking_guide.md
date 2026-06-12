# Forking Guide — AGEINT

## Shard-first fork workflow

1. Copy project tree (or promote from private `projects/active/`).
2. Replace `data/curriculum/` shards with your curriculum structure (keep JSON/JSONL schema).
3. Update `manuscript/config.yaml` title, authors, keywords.
4. Reset or extend `data/source_identity/` only with a deliberate citation migration plan.
5. Adjust neutral templates in `manuscript/templates/` if section shapes change.
6. Run `uv run python scripts/build_curriculum.py` and fix test failures before render.

## Do not fork by copying `output/manuscript/`

Generated prose is an artifact. Fork the **source spine** and renderer code.

## Template parity

Keep `src/`, `tests/`, `scripts/`, `manuscript/config.yaml`, and `pyproject.toml`. See template [`docs/guides/new-project-setup.md`](../../../../template/docs/guides/new-project-setup.md) for Layer 2 conventions.

## Confidentiality

AGEINT in the public template repo is local-only (symlink). Do not commit non-exemplar projects to the public template remote.

## See also

- [`architecture.md`](architecture.md)
- [`agent_instructions.md`](agent_instructions.md)
