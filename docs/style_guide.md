# Style Guide - AGEINT prose posture, source ownership, and crossrefs

Prose and naming conventions for generated curriculum content.

## Voice and posture: defensive, educational, accountable, and evidence-bounded prose

- Defensive, educational, accountable, synthetic, evidence-bounded.
- No live targets, evasion recipes, exploit instructions, or manipulation playbooks.
- Prefer governance, tabletop exercises, source-integrity review, and historical context for dual-use topics.

## Generated versus authored surfaces: where each kind of edit belongs

| Surface | Rule |
| --- | --- |
| `data/curriculum/` | Authoritative structure and titles |
| `manuscript/templates/` | Neutral tokens only (`{{SECTION_TITLE}}`, etc.) |
| `src/intelligence_content/` | Verified anchors, profiles, safety transforms |
| `output/manuscript/` | **Never hand-edit** |

## Cross-references: label-backed section, figure, table, and citation links

Use Pandoc/crossref labels: `[@sec:…]`, `[@fig:…]`, `[@ageintNNN]`. Do not hard-code literal figure, section, or equation numbers in prose.

## Figures: registry-backed assets, square layout, and readable evidence

Registry-backed figures should stay roughly square; see `src/figures/` and `test_figures.py`.

## Related documentation: safety, syntax, and project agent rules

- [`safety.md`](safety.md)
- [`syntax_guide.md`](syntax_guide.md)
- [`../AGENTS.md`](../AGENTS.md)
