# Adversarial Assurance: challenge cycles, remediation owners, and retest evidence

AGEINT uses adversarial assurance to stress-test generated chapters, appendices,
source lanes, rendered PDFs, figure assets, and instructor artifacts before
reuse. This is the RedTeam-style quality gate for bloat, unsafe wording,
unverified claims, brittle tests, stale docs, broken cross-references,
Markdown-file PDF links, and boundary drift.

The current implementation treats the validator itself as an artifact. A render
is not considered locally ready until `scripts/audit_artifact_evidence.py` can
bind the rebuilt manuscript, citation inventory, scholarship-quality audit,
source-metadata audit, source-refresh due audit, claim-calibration audit, figure
quality audit, PDF quality report, PDF annotation audit, and rendered-reference
audit into `output/reports/current_artifact_evidence.json`. The separate
`scripts/audit_publication_readiness.py` preflight then attacks the release
surface: private/local path leaks, Markdown-file links, stale PDFs, bad PDF link
targets, artifact-manifest issues, missing source/license posture, incomplete
release-prerequisite tasks, and parent-template confidentiality guard failures
are blockers even if the manuscript render itself is valid.

The reference-quality gate adds a reader-facing negative control to that stack:
a generated `.md` link, unresolved rendered reference, stale generic body
heading, incomplete lesson cross-link, raw literal citation key, or citation-only
table row with no source title/role context makes `reference_quality_ok` fail
and blocks the unified artifact-evidence report.

## Assurance cycle: challenge, remediate, retest, and record

- Misuse case: identify how the module could be misread as operational,
  inaccessible, unfair, or overconfident.
- Control challenge: test authority, data, tool, rights, procurement, and review
  controls.
- Evidence attack: challenge source identity, provenance, counter-evidence, and
  confidence.
- Verifier attack: introduce a negative control that should fail, such as a
  Markdown-file PDF link, stale generated output, unresolved section reference,
  old source-section coverage table shape, or claim-bearing generated section
  collapsed to one citation key. For the Synthetic Analytic Tradecraft claim,
  remove the method-contract figure reference or the source-family triangulation
  language from the abstract/orientation; for analysis validation, remove the
  analysis-matrix figure reference, the protocol section, or the failure-mode
  language. A second negative-control path removes a claim-class lane such as
  artifact readiness or reviewer disposition while leaving the protocol heading
  and figure reference intact; the scholarship-quality verifier must still fail
  even if ordinary citation counts remain high. A third negative-control path
  adds a curated source-anchor row with an empty `source_lane` or `source_tier`,
  or a source-quality support row whose lane/tier is not
  `source_quality_spine` / `source_quality_anchor`; `source_metadata_ok` must
  fail even if the PDF, citations, and figure registry are otherwise current.
  A fourth negative-control path adds proof-language, p-value language,
  measured-performance language, or an unsupported formalism whose only support
  is weak source-guide context; `claim_calibration_ok` must fail even if
  citation counts and PDF links remain green. A fifth path injects a private
  local path, Markdown-file link, stale artifact-manifest issue, or due/stale
  source-refresh row into a release-facing surface; the publication-readiness
  preflight must fail even when the ordinary PDF validator remains green.
- Incident rehearsal: use synthetic tickets to test pause, revoke, preserve,
  recover, and debrief actions.
- Remediation: assign owner, due date, retest result, refresh trigger, and the
  evidence-manifest field that proves closure.

## Source rules: direct anchors for adversarial assurance claims

Adversarial assurance cites directly verified sources such as CISA AI
red-teaming/TEVV guidance, NIST ARIA evaluation work, NIST AI 600-1,
NIST Dioptra, MITRE ATLAS, OWASP agentic-AI security guidance, and the
source-guide citation spine. Perplexity remains a discovery lane only.

## Local command: run and interpret the assurance audit

After a strict build and PDF render, run:

```bash
uv run python scripts/audit_artifact_evidence.py --write --format markdown
uv run python scripts/audit_scholarship_quality.py --write --format markdown
uv run python scripts/audit_source_metadata.py --write --format markdown
uv run python scripts/audit_source_refresh_due.py --write --format markdown
uv run python scripts/audit_claim_calibration.py --write --format markdown
uv run python scripts/audit_publication_readiness.py --write --format markdown
```

The JSON report is the preferred machine-readable evidence surface. The
Markdown report is for review notes and ISA/task closeout summaries.

The analysis-validation lane source of truth is `src/analysis_validation.py`.
It feeds the Python matrix renderer and the scholarship-quality lane contract,
while the generated orientation output must retain the same claim classes,
validation questions, evidence packets, and failure modes.
The same module also maps claim-bearing generated manuscript families to
analysis-validation lanes. A new family that carries claim-bearing prose but has
no lane mapping is a verifier failure, even if citation counts and rendered
references still pass.

## Safety boundary: synthetic red-team exercises and blocked misuse

Adversarial assurance is a classroom audit and tabletop exercise. It does not
authorize exploitation, evasion, live target interaction, private-data
processing, manipulation, or unsafe cyber-physical action.
