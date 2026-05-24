# Output Conventions — AGEINT

Generated artifacts under `output/` are disposable and regeneratable. Authoritative inventory: [`output_inventory.md`](output_inventory.md).

## Layout

| Path | Role |
| --- | --- |
| `output/data/curriculum/` | Mirrored curriculum shards |
| `output/data/curriculum_outline.json` | Compact curriculum mirror |
| `output/data/manuscript_variables.json` | Runtime `{TOKEN: value}` map |
| `output/figures/` | Registry + PNG/Mermaid assets |
| `output/manuscript/` | Semantic markdown for PDF/HTML |

## Pipeline copy

Final deliverables copy to `output/AGEINT/` at repo root after Stage 09 when running the full template pipeline.

## See also

- [`architecture.md`](architecture.md)
- [`../domain_profile.yaml`](../domain_profile.yaml)
