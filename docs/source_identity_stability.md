# Source Identity Stability

AGEINT preserves the source identity of the original guide references while
allowing v2 expansion.

## Contract

- Preserve `ageint001` through `ageint231` exactly as locked in
  `data/source_identity/`.
- Append new guide references after the locked range.
- The prior deep-pass checkpoint ended at `ageint285`; current append-only
  references extend through `ageint312`.
- Keep generated citations, BibTeX rows, and bibliography atlas rows derived
  from parser output and source-anchor metadata.
- Do not hand-edit generated bibliography files as the primary source of truth.

## Verification

Run:

```bash
uv run pytest tests/test_source_identity.py
```

The test rebuilds the locked reference projection from the current guide and
compares it with the committed identity lock.
