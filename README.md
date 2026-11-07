# AGEINT — Agentic Intelligence Curriculum

AGEINT is a modular curriculum for Agentic Intelligence: atlas, library, course,
textbook, cookbook, and playbook. It composes curriculum source shards into a
semantic manuscript, registry-backed figures, generated BibTeX, and auditable
runtime variables. Complete figure, PDF, and HTML qualification uses the shared
research SDK, pinned to `docxology/template` **5.1.0**; a standalone source-data
checkout is not a substitute for that prepared rendering runtime.

The project is deliberately evidence-bounded. It can teach intelligence
tradecraft, IC-cycle governance, OSINT/GEOINT integrity, FININT/economic
security, declassified intelligence history, agentic-AI governance, cognitive
security, counterintelligence, cyber defense, and ICS/OT readiness, but all
examples stay educational, synthetic, accountable, defensive, and bounded by
legal and human oversight constraints.

## Citation and DOI

- **Repository:** <https://github.com/docxology/AGEINT>
- **Concept DOI (latest archived edition):** [10.5281/zenodo.20732274](https://doi.org/10.5281/zenodo.20732274)
- **Historical version DOI (Edition 0.1.0 only):** [10.5281/zenodo.20732275](https://doi.org/10.5281/zenodo.20732275)
- **License:** text CC BY 4.0; code Apache-2.0

> Friedman, Daniel Ari. *AGEINT: Agentic Intelligence — A Modular Atlas, Library,
> Course, Textbook, Cookbook, and Playbook for Agentic Intelligence* (Edition 0.2.0,
> 2026). Active Inference Institute. <https://github.com/docxology/AGEINT>.
> <https://doi.org/10.5281/zenodo.20732274>.

Source publication identity is included in the SDK-rendered title page and
citation block of `output/pdf/AGEINT_combined.pdf`, mirrored at `AGEINT.pdf`.
The concept DOI identifies the archived work; no new archive deposit or 0.2.0
version DOI is implied by source metadata.

## Source

- Runtime curriculum source: `data/curriculum/`
- Optional historical guide filename: `SIST-Guide-TOC-and-Bibliography-v2.md` is recognized when present but is not required for normal builds
- Source templates: `docs/manuscript/templates/*.md`
- Resolved manuscript: `output/manuscript/`
- Figure registry and assets: `output/figures/figure_registry.json`
- Bibliography: generated to `docs/manuscript/references-*.bib` and `output/manuscript/references-*.bib`
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
- Non-numbered generated visuals: 1 deterministic Python-rendered title-page cover at `output/figures/cover/ageint-cover-synthesis.png` and 1 front-matter Evidence Transit Map at `output/figures/frontmatter/ageint-evidence-transit-map.png` (both live outside the numbered registry)

These counts are rebuild-time measurements: verify with
`python3 -c "import json;print(json.load(open('output/data/curriculum_outline.json'))['stats'])"`
or re-run `scripts/build_curriculum.py`; see [`TODO.md`](TODO.md) Verified State
for the last measured pass.

## Current state and next actions

- Backlog (canonical, forward-only): [`TODO.md`](TODO.md) — its `Open` section
  holds the next useful work; `tasks.yaml` is the taskboard source of truth.
- Release changes: [`CHANGELOG.md`](CHANGELOG.md); the GitHub release and its
  exact-source verification run establish publication, not this document.
- Status: `output/reports/publication_readiness.json` (`ok` field) and
  `output/reports/current_artifact_evidence.json` are the generated status
  surfaces; re-run the audits in Commands below to refresh them.
  Readiness `ok` records the evaluated gates; it is not publication authorization
  or evidence that a tag, release, or archive deposit exists.

## Commands

The commands below use a prepared compatible SDK Python runtime. See
[`docs/rendering_pipeline.md`](docs/rendering_pipeline.md) for runtime and project
link setup; `AGEINT_TEMPLATE_REPO` selects the actual SDK checkout, not an
installation or a waiver of its version/guard requirements.

```bash
AGEINT_REQUIRE_RENDERED_FIGURES=1 python scripts/build_curriculum.py
AGEINT_REQUIRE_RENDERED_FIGURES=1 python scripts/generate_figures.py
python -m pytest tests/ --cov=src --cov-fail-under=90
python scripts/audit_release_metadata.py --expected-tag v0.2.0 --format json
python scripts/audit_artifact_evidence.py --write --format markdown
python scripts/audit_scholarship_quality.py --write --format markdown
python scripts/audit_source_metadata.py --write --format markdown
python scripts/audit_agency_source_coverage.py --write --format markdown
python scripts/audit_claim_calibration.py --write --format markdown
python scripts/audit_reference_quality.py --write --format markdown
python scripts/audit_publication_readiness.py --write --format markdown

# From the prepared SDK root, with this checkout linked as projects/working/AGEINT:
.venv/bin/python -m infrastructure.validation.cli markdown projects/working/AGEINT/output/manuscript --repo-root . --strict
.venv/bin/python -m infrastructure.validation.cli prerender projects/working/AGEINT/output/manuscript --repo-root .
.venv/bin/python scripts/pipeline/stage_03_render.py --project working/AGEINT --skip-manuscript-hydration
.venv/bin/python scripts/pipeline/stage_04_validate.py --project working/AGEINT
```

Use `--regenerate-source-template-library` only when intentionally resetting the
neutral source templates from `src/manuscript_templates.py`.

## Architecture

The source manuscript stays small and neutral. `src/curriculum.py` composes the
sharded curriculum, `src/build_pipeline.py` orchestrates the build,
`src/manuscript_manifest/` creates semantic output paths and generated section
contexts, `src/manuscript_variables/` writes runtime variables and BibTeX,
`src/intelligence_content/` owns evidence-scoped research profiles, deterministic
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
informative. The artifact-evidence manifest reports 0 single-source-family
claim-bearing review warnings under the current source-strength classifier;
the readiness gates treat any such family as a review row, not a blocker.

**The SDK owns PDF/HTML compilation; this repository owns its release gate.**
`scripts/build_curriculum.py` and `scripts/generate_figures.py` produce the
semantic manuscript, figures, and BibTeX. The shared SDK's canonical render stage
consumes those files; AGEINT does not carry a second Pandoc/TeX compiler.

[Complete manuscript verification](.github/workflows/manuscript.yml) performs a
fresh strict Mermaid build, the complete 90%-minimum test suite, canonical SDK
PDF/HTML rendering, native validators, and every aggregate readiness gate.
Missing tools, placeholders, failed compilation, stale outputs, or a skipped
parent guard cannot establish acceptance. Manual development runs may select an
explicit immutable SDK candidate commit; publication never uses that override.

[Release AGEINT](.github/workflows/release.yml) accepts only exact current `main`
with aligned source metadata and a genuine stable SDK `v5.1.0` release. It reruns
complete acceptance, checks same-run asset hashes and Source/SDK identity, then
creates a new tag/release without overwriting an existing publication.
The offline reader ZIP preserves `web/`, local assets, and sibling `figures/`;
serve its extracted root over local HTTP and open `/web/index.html`.

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

Discovery tools provide leads, not verification. The manuscript retains source
identities and records passage/metadata inspection, access limits, corrections
and unresolved claims separately. The anchor catalog includes sources from ODNI, CIA, DIA, NIST, CISA, NSA, Five Eyes partners,
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

## 2026-11-06 curriculum and workflow revision

The CogSecSkills critical review and claim-evidence audit produced 564 authored
topic notes across all 51 chapters, with over 41,000 words of domain-specific
explanations, completed fictional decisions, counterexamples and limits. All
16 units now carry concrete learning workflows; all nine methods appendices
contain distinct offline workbooks rather than repeated generic forms.

The shared method reference provides an eight-step claim-to-decision workflow,
a completed source-dependence and correction case, a reusable claim record,
bounded parallel-role contracts, and explicit hold/correction/handoff decisions.
Orientation includes a 75-minute first session and manual accessible route.
Chapter 35 works model-relative inference numerically. Chapter 36 supplies a
complete standard-library Python example with expected output and duplicate,
conflicting-copy, missing-current-record, permission and human-review controls.

Human-source and software-agent subjects are distinguished; safe identity and
chapter overrides control lesson routing. Source annotations remain editorial
context rather than manufactured topic evidence. ACH consistency is not a
Bayesian likelihood ratio; proposed cognitive-security frameworks and candidate
neuromarkers are not validated assurance, diagnostic or efficacy claims.
Corrected source notes disclose study corrections, disputed results, edition
limits and blocked primary retrieval. Missing author/year metadata is left
missing, not converted into invented authorship or the build year.

The claim verifier now rejects nonexistent official-looking citation keys.
Heading navigation uses existing labels, not borrowed citations masquerading as
evidence; bare domain and bibliographic titles remain intact. Workflow diagrams
separate permission from purpose, evidence from inference, and review from
proof. The chapter assessments include later topics and justified abstention.

### Current evidence and limits

Consult `output/reports/current_artifact_evidence.{json,md}`,
`claim_calibration.{json,md}`, `scholarship_quality.{json,md}`,
`source_metadata.{json,md}`, `source_refresh_due.{json,md}` and the figure
registry for measured artifact status. Historical page, citation and link
counts are not current release claims. These checks are structural and
heuristic: they do not establish passage entailment, independent corroboration,
learning gains, model reliability, legal compliance or production safety.

### Public identity and local revision

The repository already records the Edition 0.1 and concept DOIs above.
This local revision is not a new publication or approval to push, promote,
upload or release it. Source freshness is date- and scope-specific; a complete
metadata row or a successful rebuild is not a fresh review of every source.


## Safety posture

Dual-use subjects are represented as history, governance, tabletop exercises,
synthetic-data labs, public-domain imagery, source-integrity review, and
defensive analysis. Do not add live target lists, operational collection steps,
evasion recipes, exploit instructions, persuasion playbooks, or unsafe
cyber-physical procedures.
