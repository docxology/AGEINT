# Citation Workflow: source keys, curated anchors, and generated bibliography checks

This is the canonical workflow for adding, reviewing, and counting AGEINT
citations. Generated citation surfaces are built from source data; never hand-edit
`output/manuscript/`.

## Choose the source type: guide reference, curated anchor, or support source

| Source type | Primary edit surface | Key format | When to use |
|---|---|---|---|
| Source-guide reference | `data/curriculum/` and `data/curriculum/references/` | `ageintNNN` | A parsed guide source supports a curriculum title or section. |
| Curated research anchor | `data/research_anchors/` plus `src/intelligence_content/` routing | stable descriptive key | A directly verified official, standards, public-domain, or scholarly source supports generated synthesis. |
| Source-quality anchor | `src/manuscript_variables/` source-quality list | stable descriptive key | A baseline governance or source-quality standard applies across modules. |

## Add or extend a citation: preserve identity and record metadata

1. Preserve `ageint001` through `ageint231`; do not renumber locked source identities.
2. Append new source-guide references after the locked range. Current generated guide keys extend through `ageint312`.
3. For curated anchors, record `source_lane`, `source_tier`, `checked_as_of`, `verification_method`, `claim_scope`, `refresh_cadence`, `refresh_trigger`, `stakeholder_role`, `assurance_use`, and `rights_dimension`.
4. Use Pandoc citation syntax such as `[@ageint137]` or `[@official_nist_ai_rmf]`.
5. Use label-backed cross-references to the curriculum orientation section and curriculum-map figure rather than hard-coded section or figure numbers.
6. Rebuild from the AGEINT root:

```bash
uv run python scripts/build_curriculum.py
```

## Count and verify citations: source-section inventory and test gates

Run the source-section and generated-output counter:

```bash
uv run python scripts/count_citations.py --format markdown
uv run python scripts/count_citations.py --format json
```

Run citation integrity tests:

```bash
uv run pytest tests/test_citation_workflow.py tests/test_manuscript_crossrefs.py -q --no-cov
```

Before claiming completion for citation edits, also run the project gate:

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
```

## Do not edit generated output: rebuild from source-owned citation surfaces

`output/manuscript/` is a rendered audit surface. If a generated section is thin,
uncited, or stale, update `data/curriculum/`, `data/research_anchors/`,
`src/intelligence_content/`, `src/manuscript_manifest/`, or neutral templates,
then rebuild. Direct edits to generated Markdown will be overwritten and are not
the source of truth.
