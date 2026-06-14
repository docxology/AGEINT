# Evidence Package Map

AGEINT now treats every generated chapter as an evidence package, not only as
curriculum prose. The package adds model and dataset cards, transparency
notices, records-retention evidence, release gates, risk exceptions, learner
support, instructor questions, and remediation backlogs.

## Evidence Package Rows

| Artifact | Minimum evidence | Reject condition |
|---|---|---|
| Model and dataset card | intended use, excluded use, stakeholders, provenance, collection process, rights/license, evaluation context, subgroup caveats, failure modes, owner, rollback path, and refresh trigger | model or dataset claims appear without provenance, caveats, or lifecycle controls |
| Transparency notice | purpose, authority, data summary, human review, safeguards, contact point, and publication decision | public accountability fields are missing or hidden without justification |
| Records-retention trail | source, prompt, decision, exception, incident, output, retention rule, and deletion or refresh condition | later reviewers cannot reconstruct the evidence path |
| Release/change gate | scope, rights, security, version, rollback, monitoring, incident threshold, and retest | reuse occurs after material change without approval |
| Risk exception memo | requirement, risk basis, compensating control, expiry, owner, and retest | an exception is broad, open-ended, or unsupported |
| Learner support plan | accessibility route, cognitive-load support, allowed-tool statement, feedback path, and remediation owner | a learner-facing artifact lacks an accessible alternative or fair assessment route |
| Instructor question bank | source, boundary, rights, and assurance challenge prompts with retained evidence | questions do not lead to revision, proof, or a documented no-change decision |
| Remediation backlog | trigger, owner, due date, closure evidence, and retest result | findings are noted but not closed |

These rows are authored in `src/intelligence_content/`, surfaced through
`src/manuscript_variables/`, rendered into every chapter by
`src/manuscript_manifest/`, and checked by tests. Do not hand-edit generated
copies under `output/`.

Figure provenance for the May 24 refresh is registry-backed, not pasted into
manuscript prose. `src/figures/` now covers bounded autonomy and
recoverability, public AI register lifecycle, AI incident reporting, and the OT
definitive architecture record as square Python figures with local PNG assets
and `figure_registry.json` entries after rebuild.

The Data Cards pass extends the model/dataset card row with stakeholder-centered
dataset documentation, collection-process evidence, and answer-evaluation
caveats. It also replaces the decorative agentic-boundary plate with a
deterministic boundary-control matrix while keeping the same cross-reference
label.

The 2026-06-11 through 2026-06-13 hardening passes keep this package tied to the
expanded source and figure surface: 248 curated research anchors, 10 source-quality
support anchors, 170 registered figures (114 Mermaid, 46 Python, 4 historical,
and 6 AI-generated) plus one non-numbered cover-art PNG, refreshed CSAF / International AI Safety Report URL metadata, and
label-backed navigation across the orientation, curriculum map, source-lane
map, research-anchor atlas, bibliography atlas, figure/course-link, and
bibliography-atlas source-section coverage surfaces. The current local artifact
evidence is 369 generated Markdown files, 383 manuscript-bound files, 15,382 generated Markdown citation
occurrences, 0 zero-citation source sections, and a 1,619-page combined PDF
with 4,181 URI links and 0 template PDF-validator issues. Figure captions, alt text, and long
descriptions are registry-enforced reader aids: all 170 rows now meet the
expanded 40-word caption, 24-word alt-text, and 70-word long-description gates.
The PNG files also embed compact accessibility, provenance, and visual-semantics metadata,
`visual_quality_audit.json` records the machine-readable visual-quality
pass/fail surface, `current_artifact_evidence.{json,md}` binds those checks to
the current PDF/citation/link/source-metadata/claim-calibration audit,
`source_metadata.{json,md}` reports 258 metadata rows, 0 blank lane/tier fields,
0 fallback-dependent rows, and the 119-row fallback closure baseline, and
`scholarship_quality.{json,md}` reports
source-family mix with 0 uncited or thin claim-bearing failures and six
single-source-family claim-bearing review warnings plus passing SAT method-contract, analysis-validation,
analysis-validation lane-contract, and claim-bearing family-coverage checks;
`claim_calibration.{json,md}` reports hard-fail proof/statistical/performance/formalism
claim checks and source-support strength; and the compact PDF preamble
now uses 7.8 pt body text with 8.9 pt leading.
The title-page cover art is intentionally outside the registry and is governed
by `book.cover.image` in `manuscript/config.yaml`; the abstract is plaintext
rather than a figure-bearing graphical abstract. The orientation graphical
abstract is the registered Python `ageint-graphical-abstract` Synthetic
Tradecraft System Atlas, with its caption, alt text, long description, and PNG
metadata governed by the figure registry.
