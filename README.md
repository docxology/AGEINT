# AGEINT — Agentic Intelligence Curriculum

AGEINT is a modular curriculum for Agentic Intelligence: atlas, library, course,
textbook, cookbook, and playbook. It converts a source guide into a semantic
manuscript, registry-backed figures, generated BibTeX, and auditable runtime
variables while rendering from the local lifecycle checkout. This copy currently
lives under `projects/working/AGEINT`; parent-template runs may link it as
`projects/active/AGEINT` or `projects/AGEINT` when it is promoted or hot-seated.

The project is deliberately evidence-bounded. It can teach intelligence
tradecraft, IC-cycle governance, OSINT/GEOINT integrity, FININT/economic
security, declassified intelligence history, agentic-AI governance, cognitive
security, counterintelligence, cyber defense, and ICS/OT readiness, but all
examples stay educational, synthetic, accountable, defensive, and bounded by
legal and human oversight constraints.

## Citation and DOI

- **Repository:** <https://github.com/docxology/AGEINT>
- **Concept DOI (cite this — resolves to the latest version):** [10.5281/zenodo.20732274](https://doi.org/10.5281/zenodo.20732274)
- **Version DOI (Edition 0.1):** [10.5281/zenodo.20732275](https://doi.org/10.5281/zenodo.20732275)
- **License:** text CC BY 4.0; code Apache-2.0

> Friedman, Daniel Ari. *AGEINT: Agentic Intelligence — A Modular Atlas, Library,
> Course, Textbook, Cookbook, and Playbook for Agentic Intelligence* (Edition 0.1,
> 2026). Active Inference Institute. <https://github.com/docxology/AGEINT>.
> <https://doi.org/10.5281/zenodo.20732274>.

The DOI and repository are baked into the rendered title page and citation block
of `output/pdf/AGEINT_combined.pdf`.

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
- Curated official/scholarly/professional research anchors: 462
- Source-quality support anchors: 10
- Registered figures: 177 (115 Mermaid, 52 Python, 4 historical, 6 AI-generated; square-normalized canvases; current registry has no placeholder plates and every row carries caption, alt text, long-description metadata, PNG metadata, and visual-semantics fields)
- Non-numbered cover art: 1 deterministic Python-rendered title-page image at `output/figures/cover/ageint-cover-synthesis.png`

## Commands

```bash
uv run python scripts/build_curriculum.py
AGEINT_REQUIRE_RENDERED_FIGURES=1 uv run python scripts/build_curriculum.py  # strict Mermaid PNGs
uv run python scripts/generate_figures.py
uv run pytest tests/ --cov=src --cov-fail-under=90
uv run python scripts/audit_artifact_evidence.py --write --format markdown
uv run python scripts/audit_scholarship_quality.py --write --format markdown
uv run python scripts/audit_source_metadata.py --write --format markdown
uv run python scripts/audit_agency_source_coverage.py --write --format markdown
uv run python scripts/audit_claim_calibration.py --write --format markdown
uv run python scripts/audit_reference_quality.py --write --format markdown

# Coverage floor: 90% for `src/`; use the test command above for the current measured result.
# Stage 02 pipeline analysis runs build_curriculum.py only (see manuscript/config.yaml analysis.scripts).

# From the sibling template repo root (when AGEINT is linked as projects/AGEINT):
uv run python -m infrastructure.validation.cli markdown projects/AGEINT/output/manuscript --repo-root .
uv run python -m infrastructure.validation.cli prerender projects/AGEINT/output/manuscript --repo-root .

# PDF render (from the sibling template repo root, AGEINT linked under
# projects/working/AGEINT): re-renders the combined PDF and copies it back
# into this repo — the render/copy stages this repo does not itself carry.
uv run python scripts/maintenance/rerender_working_pdfs.py --project AGEINT
```

Use `--regenerate-source-template-library` only when intentionally resetting the
neutral source templates from `src/manuscript_templates.py`.

## Architecture

The source manuscript stays small and neutral. `src/curriculum.py` composes the
sharded curriculum, `src/build_pipeline.py` orchestrates the build,
`src/manuscript_manifest/` creates semantic output paths and generated section
contexts, `src/manuscript_variables/` writes runtime variables and BibTeX,
`src/intelligence_content/` owns verified research profiles, deterministic
agency source packs, and three-tier topic lesson frames (keyword → category →
synthesis), `src/source_metadata.py` audits
explicit lane/tier metadata for curated and support anchors, and `src/figures/`
renders all registry-backed figures. Smoke builds may fall back to deterministic text plates
when Mermaid/Chrome is unavailable, but the checked-in registry should remain
free of placeholders; set `AGEINT_REQUIRE_RENDERED_FIGURES=1` to fail instead of
falling back. Generated chapter architecture lives in
`src/manuscript_manifest/`: source-guide H1 chapter titles stay stable, while
repeated governance, rights, assurance, practice, assessment, capstone,
refresh, and source-map material is composed into reader-facing sections at
build time. `src/scholarship_quality.py` audits generated claim-bearing
sections for uncited or thin support and flags single-source-family sections as
review warnings; `src/source_metadata.py` audits the 462 curated anchors plus
10 source-quality support anchors so blank lane/tier fields cannot silently
fall back while rendered artifacts remain green; `src/agency_source_coverage.py`
audits the 56-anchor official US IC expansion for agency, pack, lane, tier,
checked-date, claim-scope, assurance, rights, and profile-routing metadata; and
`src/claim_calibration.py`
audits high-risk empirical, statistical, governance, safety, visual,
artifact-readiness, and formalism language against source-support strength and
boundary wording. `src/reference_quality.py` audits generated section/module
links, Markdown-file links, generic body headings, lesson cross-links, and
citation-table context so reader-facing references are both resolvable and
informative. The current rendered output has six single-source-family
claim-bearing review warnings under the stricter source-strength classifier;
they are visible review rows, not readiness blockers.

**PDF rendering is external to this repository.** The combined PDF
(`AGEINT.pdf` at the repo root, mirrored at `output/pdf/AGEINT_combined.pdf`)
is produced by a shared research-project template's pandoc/xelatex render
stage, not by any script inside this repo. `scripts/build_curriculum.py` and
`scripts/generate_figures.py` produce everything that render step consumes —
the semantic manuscript, the figure registry, and the generated BibTeX — but
the PDF composition itself runs from the template checkout against this
project linked under its `projects/working/` tree. Refreshing the PDF is
therefore a manual, out-of-band step rather than something this repo's own
CI performs; `scripts/audit_pdf_quality.py` (and the two audit scripts whose
aggregate verdict includes it) stay informational in
[`.github/workflows/ci.yml`](.github/workflows/ci.yml) and
[`.github/workflows/manuscript.yml`](.github/workflows/manuscript.yml) for
that reason.

Generated files under `output/` are not primary authoring surfaces. Edit
`data/curriculum/` shards first when the guide is absent; otherwise update
templates, manifest/content modules, or source-anchor data, then rebuild.
Cross-references are label-backed (`[@sec:...]`, `[@fig:...]`, `[@ageintNNN]`)
so prose points to generated identifiers instead of literal target names. Do
not improve section titles or body prose by hand-editing `output/manuscript`.
Generated chapter H3/H4 scaffolds are chapter-specific reader landmarks, while
lesson-level navigation uses **Learning-path links** with unit-map, module, and
curriculum-atlas references.
Use [`docs/citation_workflow.md`](docs/citation_workflow.md) as the canonical
recipe for adding, extending, counting, and validating citations.

See [`docs/output_inventory.md`](docs/output_inventory.md) for the generated artifact contract.

## Scholarship posture

Perplexity may be used for discovery and second opinions, but the manuscript
cites directly verified sources. The current anchor set includes official and
standards sources from ODNI, CIA, DIA, NIST, CISA, NSA, Five Eyes partners,
IMDA, OECD, ISO, IETF, OASIS, OWASP, MITRE, NATO, the EU, UNESCO, OHCHR,
World Bank, ILO, W3C, OpenAPI, Council of Europe, PCLOB, NARA, NRO, NGA,
FinCEN, OFAC, FATF, BIS, WIPO, DataCite, C2PA, the Model Context Protocol
Project, the Agent2Agent Protocol project, the UK NCSC, the International AI
Safety Report, and a policy-scholarship cognitive security source from GCSP.

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

The May 24, 2026 source refresh brought the curated anchor set to 172 directly
verified official, standards, public-domain, or scholarly sources. It adds
Canada, OECD, UN, NIST, and CISA anchors for bounded agentic-AI governance,
algorithmic impact assessment, public AI registers, AI incident reporting,
NIST Dioptra evaluation, secure AI deployment, OT procurement, OT asset
inventory, and definitive OT architecture evidence. Earlier May 22 anchors
remain for CISA AI red teaming/TEVV, CISA AI data-security best practices,
NIST's critical-infrastructure AI RMF profile concept note, OECD public-sector
AI governance, and the NARA 2025 AI compliance plan. A separate 2026-05-22
verified batch raises the curated set to 186 anchors, adding NATO CCDCOE
cognitive-warfare research, DARPA Intrinsic Cognitive Security, CSA frameworks
(CDR, MAESTRO, securing autonomous agents, NIST agent red-teaming), the OWASP
agentic threats-and-mitigations reference, frontier-lab agent research from
Anthropic and Google DeepMind, multi-agent prompt-injection and agentic
systems-security preprints, the Mandel-Tetlock analytic-debiasing study, and the
UNU Macau bounded-agency policy analysis. Two 2026-06-06 internet-citation
passes raise the curated set to 202 anchors by adding NIST AI 100-4
synthetic-content transparency, NIST AI 100-5 global AI standards engagement,
the U.S. AI Safety Institute/NIST AI 800-1 misuse-risk draft, the International
AI Safety Report 2026, MCP specification and security best practices, the A2A
protocol specification, NCSC secure-AI-development guidance, MITRE D3FEND,
OASIS CSAF, CycloneDX, SPDX, NIST OSCAL, SLSA, in-toto, and Sigstore. Draft
status is retained where applicable rather than treated as final policy.

A 2026-06-08 primary-literature pass added the foundational primaries behind the curriculum's theoretical and
technical claims: Friston's free-energy-principle and active-inference papers
plus the Parr-Pezzulo-Friston textbook (the unifying cognitive framework); the
canonical agentic-LLM architecture papers (ReAct, Reflexion, Generative Agents,
Chain-of-Thought, Toolformer) and the Wooldridge multi-agent-systems foundations;
peer-reviewed HUMINT elicitation science (the CIA MICE-to-RASCLS article and the
High-Value Detainee Interrogation Group / rapport-based-interviewing literature);
Heuer & Pherson's structured-analytic-techniques reference; the NIST FIPS 197 /
186-5 / 180-4 and SP 800-57 cryptographic standards behind the SIGINT assurance
material; and McGuire's 1961 founding inoculation-theory experiment. These
upgrade provenance for claims previously anchored to secondary sources without
changing any argument.

A 2026-06-09 Data Cards pass raises the curated set to 225 anchors by adding
the Data Cards dataset-documentation paper, tightening source-tier language for
practitioner and vendor source-guide rows, and replacing the decorative AGEINT
boundary plate with a deterministic control matrix.

A 2026-06-10 source-method and active-inference pass raises the curated set to
228 anchors by adding Buckley et al. on active inference, PRISMA-S for
source-construction reporting, and Greshake et al. on indirect prompt injection.

A 2026-06-11 internet-backed visualization pass raises the curated set to 232
anchors by adding NIST AI 800-2 benchmark-evaluation draft guidance, OECD's
agentic-AI landscape paper, NSA MCP security design guidance, and the Science
Advances psychological-inoculation study. It also raises the figure registry to
154 with source-backed standards, evaluation, synthetic-content, data-security,
source-refresh, and freshness/coverage visuals.

A 2026-06-11 analytic-tradecraft integration pass raises the curated set to 248
anchors by adding CIA/Kent tradecraft history, warning-intelligence, post-9/11
and Iraq WMD reform/postmortem sources, NATO alternative analysis, SAT
evaluation evidence, forecasting calibration, and failure-theory sources. It
also raised the then-current figure registry to 163 with source-backed tradecraft
schematics and one evidence-derived chart for source-quality boundaries,
first-principles claim decomposition, red-team negative controls, evidence
ladders, probability/confidence separation, SAT evidence boundaries, and
warning/failure feedback.

A 2026-06-14 official US Intelligence Community source-pack pass raises the
curated set to 304 anchors by adding 56 directly verified CIA, DIA, ODNI,
Intelligence.gov, NSA, NGA, FBI, and NRO public sources. The new shard is
functional, not just numerical: `data/agency_source_packs.yaml` routes named
packs into intelligence profiles, `source_agency` and `source_pack` metadata
travel through reference dictionaries, `agency_source_coverage_ok` joins the
artifact-evidence and publication-readiness gates, and the registry grows to 172
figures with an agency-source coverage dashboard. CIA Studies/CSI professional
literature is treated as official public professional context, not automatically
as current agency policy or measured AGEINT benchmark evidence.

A 2026-06-15 SI/OPSEC/cognitive-security literature-integration pass adds 36
directly verified scholarly, official, and public-domain sources
from the synthetic-intelligence, analytic-tradecraft, OPSEC, cognitive-security,
adversarial-ML, AI incident, OSINT leakage, deepfake, disinformation, social
engineering, and active-inference discovery inventories. The pasted literature
reviews remain discovery inputs only; final manuscript citations point to the
verified source URLs in `data/research_anchors/intelligence-anchors-305-340.jsonl`.
The registry grows to 177 figures with a source-backed SI/tradecraft/OPSEC/
cognitive-security convergence map.

A 2026-06-15 SAT literature-integration pass raises the curated set to 367
anchors by adding 27 directly verified scholarly, official, public, and
publisher-backed structured-analytic-technique sources after dedupe against
Heuer, Heuer/Pherson, CIA tradecraft, ICD 203, RAND, Dhami, Mandel/Tetlock,
Barnes/Mandel, Ard, and other existing anchors. The new shard is
`data/research_anchors/intelligence-anchors-341-367.jsonl`; it routes through
analytic tradecraft, SAT evidence, analytic cognition, failure postmortem,
warning, forecasting-calibration, and analyst-assistance profiles while keeping
SAT claims bounded as review artifacts rather than universal bias remedies or
autonomous judgment replacements.

A 2026-06-16 citation-expansion pass reviews 106 proposed citation headings,
imports 95 directly verified and deduplicated anchors, and records 11 deferred
candidates in `docs/citation_expansion_2026_06_16.md`. The new
`data/research_anchors/intelligence-anchors-368-417.jsonl` and
`data/research_anchors/intelligence-anchors-418-462.jsonl` shards are routed
through non-agency research packs in `data/research_source_packs.yaml` so
collection, cyber/ICS, influence/CI, history/legal/SAT, and agentic-AI
chapters inherit richer evidence without overloading the agency-source pack
contract. Accepted rows use bounded claim scopes and explicitly exclude
collection tasking, exploit steps, covert-action guidance, manipulation
playbooks, unsafe cyber-physical actions, and live-target procedures.

A 2026-06-12 local verifier-first, scholarship-quality, and Synthetic Analytic
Tradecraft orientation pass keeps the same source corpus but raises the figure
registry to 168 with the
`ageint-artifact-evidence-control-loop` and
`ageint-scholarship-triangulation-map` control figures and the
`ageint-synthetic-tradecraft-method-contract` and
`ageint-analysis-validation-matrix` method figures plus the
`ageint-analysis-validation-family-coverage` coverage figure. It adds generated
evidence manifests that bind the rebuilt manuscript, citation inventory,
scholarship source-family audit, figure quality audit, rendered-reference audit,
PDF quality/link audit, and stale-output scans into
`output/reports/current_artifact_evidence.{json,md}` and
`output/reports/scholarship_quality.{json,md}`. The current local manifest
reports 330 configured generated Markdown files, 16,604 generated Markdown
citation occurrences, 177 registered figures plus one non-numbered cover-art
PNG, a non-stale 1,858-page ~34 MB PDF, 6,289 PDF URI links, 0 Markdown-file,
`file:`, or launch-action PDF targets, 0 uncited or thin claim-bearing generated
files, and six single-source-family claim-bearing review warnings, with passing
SAT method and analysis-validation contracts plus source-metadata explicitness
and claim-calibration checks. A follow-on RedTeam pass makes the analysis-validation claim classes
canonical in `src/analysis_validation.py`, so the prose protocol, matrix
renderer, scholarship audit, and artifact-evidence manifest now fail if a lane
such as artifact readiness or reviewer disposition drops out while the heading
and figure reference still remain. A second RedTeam follow-up adds a canonical
manuscript-family-to-validation-lane map so a new claim-bearing generated family
cannot enter the manuscript surface without a matching review lane, evidence
signal, failure signal, and registry-backed coverage visual.

A 2026-06-13 metadata-verifier hardening pass keeps the same source corpus but
closes the legacy lane/tier fallback dependency. It makes 119 previously blank
metadata rows explicit: 109 legacy intelligence anchors now carry
`source_lane` from their existing `domain` and `source_tier` from their existing
`source_type`, while 10 source-quality support anchors carry
`source_quality_spine` / `source_quality_anchor` semantics. The new
`scripts/audit_source_metadata.py` report writes
`output/reports/source_metadata.{json,md}` and is wired into
`current_artifact_evidence.{json,md}` as `source_metadata_ok`, so a blank
lane/tier row or support-anchor semantic mismatch fails local readiness. The
same pass raised the then-current registry to 169 figures with
`ageint-source-metadata-integrity`, a Python control-matrix figure for source
metadata explicitness and refresh coverage.

A 2026-06-13 cover, abstract, and TOC hardening pass keeps the same source
corpus and figure registry count while adding deterministic cover art outside
the numbered figure registry. The abstract is now one substantial plaintext
Synthetic Analytic Tradecraft contract rather than a graphical-abstract wrapper.
The graphical abstract itself is now the registry-backed Python
`ageint-graphical-abstract` Synthetic Tradecraft System Atlas in orientation,
not a Mermaid stack or title-page cover. The PDF table of contents is
intentionally limited to H1/H2 entries; each module exposes three chapter-specific
H2 landmarks (source/profile frame, practice-lens path, assurance handoff), while
H3/H4 scaffolds remain in the body for local navigation and
cross-reference targets. The compact LaTeX preamble also carries TOC spacing
controls so multi-digit section numbers do not collide with headings.

A 2026-06-14 claim-calibration and visual-semantics hardening pass keeps the
same source corpus and adds the registry-backed
`ageint-claim-calibration-and-visual-semantics` control figure. The figure
registry schema is now `1.5`: every row declares semantic role, evidence role,
quantitative status, unit, denominator, counting rule, and interpretation limit,
and generated PNG metadata embeds the same fields. The new
`scripts/audit_claim_calibration.py` report writes
`output/reports/claim_calibration.{json,md}` and is wired into
`current_artifact_evidence.{json,md}` as `claim_calibration_ok`, so unsupported
proof-language, p-value language, measured-performance claims, unsupported
formalisms, or weak-source-only high-risk claims fail local readiness.

A 2026-06-14 abstract/readiness hardening pass makes the Abstract one continuous
reader-facing Synthetic Analytic Tradecraft paragraph instead of a multi-block
front-matter summary. That paragraph integrates source-quality and research
anchor counts inline, shows the learner/reviewer path through evidence packets,
negative controls, human review, rollback, refresh triggers, figure semantics,
and validator gates, and explicitly states that artifact telemetry is not a
benchmark for model capability, learning outcomes, operational effectiveness,
statistical significance, or safety performance. This is still a local-readiness
claim, not a publication decision.

After this pass, claim calibration reports 9,107 candidate rows, 0 hard fails,
482 boundary-allowed rows, and 5,129 review rows; scholarship quality reports 0
hard fails and keeps six single-source-family rows as non-blocking review
warnings.

These counts are rebuild-time measurements, not hand-authored release claims:
`output/data/curriculum_outline.json` carries the curriculum stats, and
`output/figures/figure_registry.json` carries the figure count, hashes, and
rendering provenance. Source-anchor rows include `checked_as_of` metadata and
must be refreshed when source URLs, standards versions, legal text, or supported
claim scope changes.

## Public readiness

AGEINT is locally publication-ready as a preflight packet, not as a public
release. The 2026-06-16 `publication_readiness` report is `ok: true`: artifact
evidence is green, the source-refresh dashboard reports 472 current metadata
rows and 0 due-soon/due/stale rows, the artifact manifest has `issues: []`, the
parent tracked-project confidentiality guard passes, the release-surface scan
finds 0 private/local path or Markdown-file-link issues, the source/license
posture is recorded, and the fresh PDF audit reports 1,858 pages, 6,289 URI
links, 0 file actions, and 0 bad link targets. `ageint-27` is therefore closed.
`ageint-m1` remains todo because no public release, push, PR, archive,
promotion, publication upload, DOI, or release record has been approved or
performed.

## Safety posture

Dual-use subjects are represented as history, governance, tabletop exercises,
synthetic-data labs, public-domain imagery, source-integrity review, and
defensive analysis. Do not add live target lists, operational collection steps,
evasion recipes, exploit instructions, persuasion playbooks, or unsafe
cyber-physical procedures.
