# FAQ - AGEINT build, source identity, and validation answers

## Why is there no `01_introduction.md` under `manuscript/`?

By design. Semantic chapters are generated under `output/manuscript/parts/…/` from curriculum shards and manifest code.

## Why does Stage 02 only run `build_curriculum.py`?

`manuscript/config.yaml` declares an `analysis.scripts` allowlist so the pipeline does not triple-build. See [`../scripts/CONVENTIONS.md`](../scripts/CONVENTIONS.md).

## How do I refresh figures only?

```bash
uv run python scripts/generate_figures.py
```

Full rebuild still runs via `build_curriculum.py`.

## Where do citation keys `ageint001`–`ageint231` come from?

Locked in `data/source_identity/`. Do not renumber; append new references after the locked range.

## How do I validate before PDF render?

```bash
uv run python -m infrastructure.validation.cli markdown projects/working/AGEINT/output/manuscript --repo-root .
uv run python -m infrastructure.validation.cli prerender projects/working/AGEINT/output/manuscript --repo-root .
```

## Related documentation: build, syntax, output, and troubleshooting references

- [`quickstart.md`](quickstart.md)
- [`troubleshooting.md`](troubleshooting.md)
