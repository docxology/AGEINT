# docs/ Agent Notes

Keep docs synchronized with the generated data counts in
`data/curriculum/`, the source-anchor taxonomy in
`src/intelligence_content/`, figure behavior in
[`src/figures/AGENTS.md`](../src/figures/AGENTS.md), and the semantic output
contract in `output/manuscript/config.yaml`.

Avoid stale counts, manual bibliography claims, and hard-coded generated paths.
When parser, renderer, figure, or source-anchor logic changes, rebuild first,
then update docs against the rebuilt output and run the AGEINT tests.

Project docs preserve the same safety boundary as the manuscript:
defensive, educational, authorized, synthetic, and non-operational.

## Current Count Contract

The live documentation count contract is 16 parts, 51 chapters, 9 appendices,
312 source-guide references, 186 curated research anchors, and 64 registered
figures. If a source-anchor shard, curriculum shard, or figure registry changes,
refresh these counts in `README.md`, `docs/README.md`, `docs/output_inventory.md`,
and related docs before claiming the documentation is current.

## Documentation hub (template parity)

AGEINT uses an **extended domain doc set** plus thin hub stubs (not a duplicate of code-exemplar prose):

| Hub file | Role |
| --- | --- |
| [`agent_instructions.md`](agent_instructions.md) | Agent editing rules |
| [`architecture.md`](architecture.md) | Shard-first build architecture |
| [`testing_philosophy.md`](testing_philosophy.md) | No-mocks, fixtures, coverage |
| [`rendering_pipeline.md`](rendering_pipeline.md) | `output/manuscript/` → PDF |
| [`style_guide.md`](style_guide.md) | Defensive prose conventions |
| [`syntax_guide.md`](syntax_guide.md) | Citations and cross-refs |
| [`faq.md`](faq.md) | Common questions |
| [`quickstart.md`](quickstart.md) | Command entry points |
| [`output_conventions.md`](output_conventions.md) | `output/` layout |
| [`output_inventory.md`](output_inventory.md) | Artifact contract |
| [`troubleshooting.md`](troubleshooting.md) | Build and validation fixes |
| [`forking_guide.md`](forking_guide.md) | Shard-first fork workflow |

Domain-specific docs (safety, source lanes, instructor guide, etc.) extend this hub.
