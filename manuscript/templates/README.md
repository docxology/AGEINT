# AGEINT Source Templates

This folder is the source-authoring surface for AGEINT manuscript sections.

- Owner: AGEINT manuscript renderer.
- Status: manual neutral templates; may be regenerated explicitly.
- Source of truth: `src/manuscript_templates.py`.
- Regenerate: `uv run python scripts/build_curriculum.py --regenerate-source-template-library` from the AGEINT root.
- Safety: templates must stay generic, tokenized, defensive, educational, and non-operational.

The template library currently covers abstract, orientation, part intro,
chapter, appendix, bibliography atlas, and references pages. Templates should
name stable tokens only; generated source spines, research briefs, visual
synthesis, and navigation references are supplied by renderer context.

The v2 orientation and bibliography templates also expose generated source-lane
maps, source-refresh rows, safe-substitution rows, capstone workflows,
accessibility review rows, procurement/vendor oversight rows, HRIA/DPIA rows,
data-lineage rows, assessment-integrity rows, agent incident rows,
role-competency rows, and adversarial-assurance rows. Keep those as neutral
tokens; the concrete counts and rows belong in `src/manuscript_variables/`.
