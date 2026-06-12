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

The 2026-06-11 and 2026-06-12 hardening passes keep this package tied to the
expanded source and figure surface: 248 curated research anchors, 161 registered
figures, and refreshed CSAF / International AI Safety Report URL metadata.
