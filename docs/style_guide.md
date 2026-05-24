# Style Guide — AGEINT

Prose and naming conventions for generated curriculum content.

## Voice and posture

- Defensive, educational, authorized, synthetic, non-operational.
- No live targets, evasion recipes, exploit instructions, or manipulation playbooks.
- Prefer governance, tabletop exercises, source-integrity review, and historical context for dual-use topics.

## Generated vs authored

| Surface | Rule |
| --- | --- |
| `data/curriculum/` | Authoritative structure and titles |
| `manuscript/templates/` | Neutral tokens only (`{{SECTION_TITLE}}`, etc.) |
| `src/intelligence_content/` | Verified anchors, profiles, safety transforms |
| `output/manuscript/` | **Never hand-edit** |

## Cross-references

Use Pandoc/crossref labels: `[@sec:…]`, `[@fig:…]`, `[@ageintNNN]`. Do not hard-code literal figure, section, or equation numbers in prose.

## Figures

Registry-backed figures should stay roughly square; see `src/figures/` and `test_figures.py`.

## See also

- [`safety.md`](safety.md)
- [`syntax_guide.md`](syntax_guide.md)
- [`../AGENTS.md`](../AGENTS.md)
