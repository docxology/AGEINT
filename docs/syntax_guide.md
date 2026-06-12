# Syntax Guide — AGEINT

Canonical citation and cross-reference syntax for AGEINT manuscripts.

Full reference: [`../manuscript/SYNTAX.md`](../manuscript/SYNTAX.md).
Contributor workflow: [`citation_workflow.md`](citation_workflow.md).

## Citations

- Guide and anchor keys: `[@ageint001]` ... `[@ageint312]` (append-only after locked range).
- Official/scholarly keys from generated BibTeX shards.

## Cross-references

- Sections: `[@sec:curriculum_orientation]` (label-backed).
- Figures: `[@fig:ageint-curriculum-map]`.
- Topic-lesson fragments: generated **Cross-links** row with unit module map, module overview, and curriculum atlas refs (see `markdown_refs.lesson_educational_crossrefs()`).

## Tokens

Runtime counts and paths inject via `output/data/manuscript_variables.json` at build time — do not hard-code part/chapter counts in source templates.

## See also

- [`rendering_pipeline.md`](rendering_pipeline.md)
- [`docs/guides/manuscript-semantics.md`](../../../../template/docs/guides/manuscript-semantics.md)
