# AGENTS.md - AGEINT Source Templates

Keep templates neutral. Use generic tokens such as `{{SECTION_TITLE}}`, `{{SECTION_BODY}}`, and `{{SECTION_ROWS}}`; do not add chapter-specific tokens or numbered filenames.

Do not place concrete source-guide counts, chapter titles, citations, or paths here. Those belong in generated variables and manifest contexts.

Safety language should default to accountable, synthetic, defensive, tabletop, owned-lab, and evidence-bounded workflows.

Template prose should describe reusable section structure, not a particular
chapter. If a sentence needs chapter title, part title, source spine, research
lane, figure reference, or navigation context, add that field in
`src/manuscript_manifest/` or `src/manuscript_variables/` and inject it at
render time.
