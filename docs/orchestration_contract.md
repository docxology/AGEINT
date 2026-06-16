# AGEINT Orchestration Contract: modular extension points and fail-closed reports

AGEINT is flexible only when extension points remain source-owned and testable.
The contract layer describes the existing build, audit, source-pack, and
Mermaid seams without turning them into dynamic plugins. New methods should be
registered in the smallest relevant contract and then proved by a focused test.

## Pipeline-stage registry for source-to-output reproducibility

`src/orchestration_contracts.py` defines `PipelineStageContract` rows for source
validation, curriculum build, optional template refresh, variables and
bibliography, figures, manuscript rendering, evidence transit, and artifact
reports. The build freshness check derives its source roots and output
sentinels from that registry, so a new stage must declare source-owned inputs,
generated outputs or report paths, upstream dependencies, the gate that proves
the stage, and the false-certification failure mode.

Run the contract audit after adding or moving a stage:

```bash
uv run python scripts/audit_orchestration_contract.py --format json
```

## Audit-contract registry for evidence and readiness gates

`src/audit_contracts.py` defines one `AuditContract` per fail-closed report:
reference quality, scholarship quality, source metadata, refresh due, agency
coverage, claim calibration, figure quality, PDF quality, rendered references,
stale-output scans, citation coverage, and freshness. Artifact evidence uses
these rows to order `checks`, publish report paths, and assemble negative
controls.

When adding an audit, add the contract first, connect its collector to
`src/artifact_evidence.py`, surface any release-relevant check through
publication readiness, and add a negative-control test that proves a known-wrong
artifact fails.

## Source-pack registry for agency and research routing

`src/intelligence_content/source_packs.py` exposes a shared
`SourcePackRegistry` while preserving the current helper functions for agency
and research packs. Agency packs remain in `data/agency_source_packs.yaml`;
non-agency scholarly, professional, standards, and public-domain packs remain in
`data/research_source_packs.yaml`.

Every pack must have unique source keys, deterministic order, source-class
specific error text, and keys that exist in the source-anchor universe. Research
profile routes must reference known research packs.

## Mermaid-type registry for visual information design

`src/figures/mermaid_contracts.py` declares supported Mermaid chart types:
`flowchart`, `stateDiagram-v2`, `sequenceDiagram`, `journey`, `timeline`, and
`quadrantChart`. Non-flowchart diagrams must carry informative `reader_detail`
because reader text cannot be safely inferred from flowchart node parsing.

When adding a diagram type, add a contract with its source prefix, render init
policy, reader-detail requirement, and a test that rejects a mismatched source
prefix.

## Contract-audit report for operator handoff

The combined audit emits one report with pipeline stages, audit contracts,
source-pack registries, Mermaid support, output sentinels, and failure modes:

```bash
uv run python scripts/audit_orchestration_contract.py --format markdown --write
```

This writes `output/reports/orchestration_contract.json` and
`output/reports/orchestration_contract.md`. The report is local readiness
evidence only; it does not publish, push, promote, archive, or create a release
record.
