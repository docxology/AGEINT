# AGEINT — Agentic Intelligence Curriculum

AGEINT is a modular curriculum for Agentic Intelligence: atlas, library, course,
textbook, cookbook, and playbook. It converts a source guide into a semantic
manuscript, registry-backed figures, generated BibTeX, and auditable runtime
variables while rendering as an active local project under `projects/active/AGEINT`.

The project is deliberately non-operational. It can teach intelligence
tradecraft, IC-cycle governance, OSINT/GEOINT integrity, FININT/economic
security, declassified intelligence history, agentic-AI governance, cognitive
security, counterintelligence, cyber defense, and ICS/OT readiness, but all
examples stay educational, synthetic, authorized, defensive, and bounded by
legal and human oversight constraints.

## Source

- Runtime curriculum source: `data/curriculum/`
- Optional historical guide filename: `SIST-Guide-TOC-and-Bibliography-v2.md` is recognized when present but is not required for normal builds
- Source templates: `manuscript/templates/*.md`
- Resolved manuscript: `output/manuscript/`
- Figure registry and assets: `output/figures/figure_registry.json`
- Bibliography: generated to `manuscript/references-*.bib` and `output/manuscript/references-*.bib`
- Scholarship anchors: `data/research_anchors/`, `src/intelligence_content/`, and `src/manuscript_variables/`

## Current generated scope

- Parts: 16
- Chapters: 51
- Methods appendices: 9
- AGEINT patterns: 20
- Parsed references: 312
- Curated official/scholarly research anchors: 172
- Registered figures: 57 (17 Mermaid, 33 Python, 4 historical, 3 AI-generated; square-normalized canvases; current registry has no placeholder plates)

## Commands

```bash
uv run python scripts/build_curriculum.py
AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/build_curriculum.py  # strict Mermaid PNGs
uv run python scripts/generate_figures.py
uv run pytest tests/ --cov=src --cov-fail-under=90

# Coverage floor: 90% for `src/`; use the test command above for the current measured result.
# Stage 02 pipeline analysis runs build_curriculum.py only (see manuscript/config.yaml analysis.scripts).

# From the sibling template repo root (when AGEINT is linked as projects/AGEINT):
uv run python -m infrastructure.validation.cli markdown projects/AGEINT/output/manuscript --repo-root .
uv run python -m infrastructure.validation.cli prerender projects/AGEINT/output/manuscript --repo-root .
```

Use `--regenerate-source-template-library` only when intentionally resetting the
neutral source templates from `src/manuscript_templates.py`.

## Architecture

The source manuscript stays small and neutral. `src/curriculum.py` composes the
sharded curriculum, `src/build_pipeline.py` orchestrates the build,
`src/manuscript_manifest/` creates semantic output paths and generated section
contexts, `src/manuscript_variables/` writes runtime variables and BibTeX,
`src/intelligence_content/` owns verified research profiles and three-tier topic
lesson frames (keyword → category → synthesis), and `src/figures/` renders all
registry-backed figures. Smoke builds may fall back to deterministic text plates
when Mermaid/Chrome is unavailable, but the checked-in registry should remain
free of placeholders; set `AGEINT_REQUIRE_RENDERED_FIGURES=1` to fail instead of
falling back. Generated chapter architecture lives in
`src/manuscript_manifest/`: source-guide H1 chapter titles stay stable, while
repeated governance, rights, assurance, practice, assessment, capstone,
refresh, and source-map material is composed into reader-facing sections at
build time.

Generated files under `output/` are not primary authoring surfaces. Edit
`data/curriculum/` shards first when the guide is absent; otherwise update
templates, manifest/content modules, or source-anchor data, then rebuild.
Cross-references are label-backed (`[@sec:...]`, `[@fig:...]`, `[@ageintNNN]`)
so prose points to generated identifiers instead of literal target names. Do
not improve section titles or body prose by hand-editing `output/manuscript`.
Use [`docs/citation_workflow.md`](docs/citation_workflow.md) as the canonical
recipe for adding, extending, counting, and validating citations.

See [`docs/output_inventory.md`](docs/output_inventory.md) for the generated artifact contract.

## Scholarship posture

Perplexity may be used for discovery and second opinions, but the manuscript
cites directly verified sources. The current anchor set includes official and
standards sources from ODNI, CIA, DIA, NIST, CISA, NSA, Five Eyes partners,
IMDA, OECD, ISO, IETF, OASIS, OWASP, MITRE, NATO, the EU, UNESCO, OHCHR,
World Bank, ILO, W3C, OpenAPI, Council of Europe, PCLOB, NARA, NRO, NGA,
FinCEN, OFAC, FATF, BIS, WIPO, DataCite, C2PA, and a policy-scholarship
cognitive security source from GCSP.

The v2 source layer adds lane metadata for AI conformity/compliance, education
and assessment, public-sector agentic AI, cross-border data/data spaces,
human-rights governance, agent interoperability standards, workforce
governance, and model/data provenance. The original `ageint001` through
`ageint231` source identities are locked in `data/source_identity/`;
new guide references are append-only after that range and currently extend
through `ageint312`. The deep pass adds accessibility and digital inclusion,
procurement/vendor governance, agent incident response, AI red-team assurance,
public-sector transparency, and rights-impact privacy review. The evidence
package pass adds model card reporting, dataset documentation, algorithmic
transparency reporting, records retention/auditability, secure release/change
control, risk exception governance, learner support/accommodations, assurance
evaluation evidence, and procurement performance monitoring.

The May 24, 2026 source refresh brings the curated anchor set to 172 direct
official, standards, public-domain, or scholarly sources. It adds current
Canada, OECD, UN, NIST, and CISA anchors for bounded agentic-AI governance,
algorithmic impact assessment, public AI registers, AI incident reporting,
NIST Dioptra evaluation, secure AI deployment, OT procurement, OT asset
inventory, and definitive OT architecture evidence. Earlier May 22 anchors
remain for CISA AI red teaming/TEVV, CISA AI data-security best practices,
NIST's critical-infrastructure AI RMF profile concept note, OECD public-sector
AI governance, and the NARA 2025 AI compliance plan.

## Safety posture

Dual-use subjects are represented as history, governance, tabletop exercises,
synthetic-data labs, public-domain imagery, source-integrity review, and
defensive analysis. Do not add live target lists, operational collection steps,
evasion recipes, exploit instructions, persuasion playbooks, or unsafe
cyber-physical procedures.
