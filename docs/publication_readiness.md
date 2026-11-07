# Publication Readiness: local preflight evidence and release boundary

AGEINT publication readiness is a local preflight packet, not a publication
action. A green packet means the checkout has enough current evidence for an
explicit release decision; it does not push, archive, promote, upload, mint a
DOI, open a PR, or create a public record.

## Readiness oracle: artifact evidence, source refresh, and release blockers

Run the publication-readiness audit from the AGEINT root after a strict rebuild,
PDF render, output copy, and artifact-evidence refresh:

```bash
uv run python scripts/audit_publication_readiness.py --write --format markdown
```

The audit writes `output/reports/publication_readiness.json` and `.md`. It fails
when any release-facing surface contains private/local path leaks, Markdown-file
links, stale PDFs, bad PDF link targets, PDF file actions, unresolved artifact
evidence, artifact-manifest issues, missing source/license posture, due or stale
source-refresh rows, hard claim/scholarship failures, misaligned release metadata,
missing or malformed current-version release milestones, incomplete declared
prerequisite tasks, or a parent-template confidentiality guard that did not
complete with a zero exit status.

### Versioned source metadata and task contract

The canonical release version is the stable `X.Y.Z` string at
`pyproject.toml` `[project].version`. `CITATION.cff` `version`,
`docs/manuscript/config.yaml` `paper.version`, and `book.edition` must match it
exactly. The SDK binding is `[tool.template].platform_version = "5.1.0"`.
The read-only source metadata audit supports both output formats:

```bash
uv run python scripts/audit_release_metadata.py --format json --expected-tag v0.2.0
uv run python scripts/audit_release_metadata.py --format markdown
```

`--expected-tag` must be exactly `v` plus the canonical stable version;
foreign prefixes, missing `v`, suffixes, malformed versions, and a different
version fail with nonzero exit status. This check must pass before a
publication operation. Without the flag, metadata alignment is still required
but no externally supplied tag has been checked. The command writes nothing,
contacts no service, and does not prove that a tag, SDK release, or DOI exists.
SDK v5.1.0 must independently exist and pass its own acceptance; a floating
branch is not a substitute. Metadata alignment is not artifact acceptance.

Metadata CLI JSON keys are `project`, `schema_version` (`1.0`), `ok`,
`version`, `tag`, `expected_tag`, `template_platform_version`, `versions`,
`checks`, `issue_count`, and `issues`. `versions` contains `package`,
`citation`, `paper`, and `book`; `checks` contains `canonical_version_valid`,
`versions_match`, `template_platform_version_ok`, and `expected_tag_matches`.
Unknown or malformed source metadata fails closed. Invalid/non-string source
version values are represented as null.

The publication-readiness report is schema **2.0**, not compatible with its
old 1.0 task fields. `release_metadata` embeds the source metadata report;
`checks.release_metadata_ok` is required alongside every existing artifact,
PDF, source, reference, figure, license, and executed-parent-guard gate.

For version `0.2.0`, `tasks.yaml` must declare `ageint-release-0-2-0`;
in general the ID is `ageint-release-` plus the version with dots replaced by
hyphens. It must have `milestone: true`, status `todo`, `in_progress`, or
`done`, and explicit nonempty unique `deps`. Every declared dependency must
exist and have status `done`; historical or unrelated tasks cannot replace
those prerequisites. Missing, wrong-version, blocked, duplicate, malformed,
or dependency-free milestones fail closed.

`task_status` now contains `version`, `release_milestone_id`,
`release_milestone_status`, `required_done_tasks`, `prerequisites_done`,
`release_milestone_ready`, `issue_count`, and `issues`.
`checks.task_prerequisites_done` checks the declared dependencies and
`checks.release_milestone_ready` replaces the obsolete still-todo check.
A completed milestone remains locally re-checkable: publication does not
invalidate the artifact's ongoing checks, and completion grants no authority
to publish it again.

### Parent confidentiality guard

The audit uses the shared `template_resolver` discovery rules, including a sibling
`template` checkout and the configured template environment variables. It runs
`scripts/audit/check_tracked_all.py` with the current prepared Python
(`sys.executable`) from that checkout's root, covering projects, fonds, tools,
and rules rather than the retired project-only entry point. It does not invoke
`uv`, reconcile sibling dependencies, or install anything. The caller must
prepare a compatible environment before this read-only guard executes.

`parent_confidentiality_guard.status` distinguishes `passed`, `failed`,
`unavailable`, `timeout`, and `skipped`. `checked` means the process completed;
only `passed` with `checked: true`, `ok: true`, and `returncode: 0` satisfies
`checks.parent_confidentiality_guard_ok`. Missing checkout/script/executable,
timeouts, and skipped runs have `checked: false`, `ok: false`, and a null return
code. A completed nonzero exit is checked but fails readiness.

For local diagnostics without running the parent guard:

```bash
uv run python scripts/audit_publication_readiness.py --skip-parent-guard --format json
```

This explicit informational mode still reports all other gates, but always
leaves readiness false and exits nonzero. It is not full release authorization.

## Current evidence: local status, validators, and remaining release limits

The following values were recorded for the 2026-06-16 local preflight; they are
historical, not a current release authorization. In particular, a historical
`ok: true` without checked-success parent-guard evidence must not be treated as
a passing preflight under the current contract:

- `publication_readiness.ok: true`
- `artifact_manifest.issues: []`
- `release_surface_scan.issue_count: 0`
- `source_license_posture.ok: true`
- `source_refresh_due.summary.row_count: 472`
- `source_refresh_due.summary.due_or_stale_count: 0`
- `artifact_evidence.summary.generated_markdown_files: 330`
- `artifact_evidence.summary.generated_markdown_citation_occurrences: 16604`
- `artifact_evidence.summary.figures: 177`
- `artifact_evidence.checks.agency_source_coverage_ok: true`
- `artifact_evidence.summary.pdf_pages: 1858`
- `artifact_evidence.summary.pdf_stale: false`
- AGEINT PDF audit: 6,289 URI links, 0 file actions, 0 bad link targets

The source/license posture records the book as CC BY 4.0, code as Apache-2.0,
and source metadata as CC-BY-4.0. Generated figures are deterministic local
assets or explicitly classified synthetic/historical assets with registry
provenance; the non-numbered cover art is generated by the local Python cover
renderer.

## Release boundary: what local readiness does not publish or approve

Historical task completion does not replace a current release decision or
checked-success parent-guard evidence. Before executing an actual public
release, rerun the strict build, artifact-evidence audit,
publication-readiness audit, parent template
validators, parent all-resource confidentiality guard, and PDF quality audit
from the final release candidate.
