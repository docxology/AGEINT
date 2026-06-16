# AGEINT Manuscript Syntax

- Cite sources with Pandoc citation keys such as `[@ageint137]`.
- Curated official or scholarly anchors use stable keys such as `[@official_nist_ai_rmf]`.
- Section anchors use generated semantic labels such as `{#sec:chapter-foundations-of-ageint}`.
- Section references use Pandoc-crossref labels such as `[@sec:curriculum_orientation]`; do not name target sections in prose when a label is available.
- Topic-lesson bodies include a **Learning-path links** line with the unit module map `[@fig:part-…-module-map]`, module overview `[@sec:chapter-…]`, and atlas `[@sec:curriculum_orientation]`.
- Figures use registry-backed Pandoc-crossref definitions with a caption, a relative generated-figure path, and a `{#fig:...}` label; references use tokens such as `[@fig:ageint-curriculum-map]`.
- Equations and tables use the same label-backed pattern with `[@eq:...]` and `[@tbl:...]` references when present.
- Mermaid source files live under `output/figures/mermaid/*.mmd`; generated PNGs are square-normalized before insertion.
- Source-derived chapter modules are generated from `data/curriculum/`.
- Keep raw LaTeX references and hard-coded Figure/Section/Equation numbers out of generated Markdown.
- Keep operational examples non-deployable: toy data, local fixtures, explicit oversight, and no live-target instructions.
- Contributor workflow: `../docs/citation_workflow.md`.
