# Output Conventions - AGEINT generated trees, copy paths, and rebuild rules

Generated artifacts under `output/` are disposable and regeneratable. Authoritative inventory: [`output_inventory.md`](output_inventory.md).

## Layout: generated directories and source-owned boundaries

| Path | Role |
| --- | --- |
| `output/data/curriculum/` | Mirrored curriculum shards |
| `output/data/curriculum_outline.json` | Compact curriculum mirror |
| `output/data/manuscript_variables.json` | Runtime `{TOKEN: value}` map |
| `output/figures/` | Registry + PNG/Mermaid assets |
| `output/manuscript/` | Semantic markdown for PDF/HTML |

## Pipeline copy: template-stage mirroring and artifact consumers

Final deliverables copy to `output/AGEINT/` at repo root after Stage 09 when running the full template pipeline.

## Related documentation: inventory, rendering, quickstart, and troubleshooting

- [`architecture.md`](architecture.md)
- [`../domain_profile.yaml`](../domain_profile.yaml)
