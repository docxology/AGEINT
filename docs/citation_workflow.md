# Citation Workflow: source keys, curated anchors, and generated bibliography checks

This is the canonical workflow for adding, reviewing, and counting AGEINT
citations. Generated citation surfaces are built from source data; never hand-edit
`output/manuscript/`.

## Choose the source type: guide reference, curated anchor, or support source

| Source type | Primary edit surface | Key format | When to use |
|---|---|---|---|
| Source-guide reference | `data/curriculum/references/` | `ageintNNN` | Preserve inherited provenance; establish actual claim relevance separately. |
| Curated research anchor | `data/research_anchors/` plus `src/intelligence_content/` routing | stable descriptive key | Record the inspected scope, edition, method and access limits of official, standards, public-domain or scholarly material. |
| Source-quality anchor | `data/research_anchors/source-quality-anchors.jsonl` | stable descriptive key | A bounded governance or source-quality reference applies across modules; it is not empirical support for unrelated claims. |

## Add or extend a citation: preserve identity and record metadata

1. Preserve `ageint001` through `ageint231`; do not renumber locked source identities.
2. Append new source-guide references after the locked range. Current generated guide keys extend through `ageint312`.
3. For curated anchors, record `source_lane`, `source_tier`, `checked_as_of`, `verification_method`, `claim_scope`, `refresh_cadence`, `refresh_trigger`, `stakeholder_role`, `assurance_use`, and `rights_dimension`.
4. Use Pandoc citation syntax such as `[@ageint137]` or `[@official_nist_ai_rmf]`.
5. Use label-backed cross-references to the curriculum orientation section and curriculum-map figure rather than hard-coded section or figure numbers.
6. Rebuild from the AGEINT root:

```bash
uv run python scripts/build_curriculum.py
```

## Bind the claim, not merely the citation

For each substantive assertion, record the exact passage/locator and edition,
what it supports, what remains inference, contrary evidence, applicability and
upstream origin. Multiple keys or copies of one study are one evidence family.
Official status, a working URL, `note_verified`, note length and source-route
membership do not establish entailment or effectiveness.

Keep source inspection distinct from metadata-only review, search-index identity
and blocked full-text attempts. Do not refresh `checked_as_of` merely because a
build ran. Corrected or contested studies retain their identity and visible
limitations. Missing publication year and authorship remain absent; verification
date is not publication date. Use `and` between individual authors in a BibTeX
author field, not a comma-separated list that can be parsed as one person's name.
When authorship is absent, the generated BibTeX `key` field preserves the stable
reference identifier for native sorting and labels. It is not an author or
publication date; this also avoids `plainnat` label overflow among undated,
unattributed references that share a citation-key prefix.

Authored `teaching_note` Markdown in a source section can cite existing keys
directly for its worked reasoning; inherited citation arrays remain provenance.
Clearly label fictional quantities and exercise outcomes. Unknown citation keys
fail closed even with an official-looking prefix. The lexical claim audit is a
triage gate, not a semantic verifier; a genuine but unrelated citation still
requires manual claim-to-passage review.

Keep inherited raw source text and citation identities separate from the current
teaching title. A title without a concept route receives honest profile framing,
not a definition synthesized from its first words. Supply the topic-specific
explanation, case, limits and source locator in `teaching_note`; keyword density
and varied wording are not evidence of substantive coverage.


## Count and verify citations: source-section inventory and test gates

Run the source-section and generated-output counter:

```bash
uv run python scripts/count_citations.py --format markdown
uv run python scripts/count_citations.py --format json
```

The normal build writes `output/data/source_citation_coverage.json` from
`source_citation_coverage_summary()`, after the published-count check and before
the final build stamp. Its `summary.section_count` and
`summary.citation_occurrences` are integer-valued results; citation occurrences
include repeated entries, whereas `summary.unique_citation_keys` counts distinct
source-guide keys. The generated coverage table names the exact path and field.
The same artifact records the parsed curriculum snapshot SHA256, counting rules
and source freshness digest. It is a required build sentinel, not a restored
aggregate audit report.

Coverage counts establish structural coverage only, not citation correctness,
claim/passage entailment, empirical support or scientific quality. Source
locators such as `5.10` remain string identities, distinct from `5.1`; recognized
legal, standard and institutional identifiers are marked only for display.
Ordinary empirical and synthetic quantities remain quantitative claims.
The embedded contributor recipe is also a registered byte-level build input.

Run citation integrity tests:

```bash
uv run pytest tests/test_citation_workflow.py tests/test_manuscript_crossrefs.py -q --no-cov
```

Before claiming completion for citation edits, also run the project gate:

```bash
uv run pytest tests/ --cov=src --cov-fail-under=90
```

## Do not edit generated output: rebuild from source-owned citation surfaces

`output/manuscript/` is a rendered audit surface. If a generated section is thin,
uncited, or stale, update `data/curriculum/`, `data/research_anchors/`,
`src/intelligence_content/`, `src/manuscript_manifest/`, or neutral templates,
then rebuild. Direct edits to generated Markdown will be overwritten and are not
the source of truth.

## Verifier negative controls

The claim scanner groups Markdown soft wraps into paragraphs while retaining
separate list and table rows. A negated, quoted, conditional or misconception
claim must not become an endorsed result merely because it contains proof
vocabulary. Conversely, a limitation in one clause cannot waive an unsupported
affirmative claim in another. Regression controls exercise both directions.
Reported or conditional claims may still require manual review.

Source-lane checks reject unknown keys and editorial-verification-only
promotion. Publisher matching uses hostname boundaries, not lookalike suffixes;
source-class eligibility still does not establish passage relevance or truth.
Do not rewrite a supported limitation merely to evade the scanner, add an
unrelated official citation to turn a flag green, or treat a zero-failure audit
as scientific validation.

Use `author_mode: "literal"` for institutional, collective or deliberately
unparsed attribution; this preserves commas and words such as “and” without
inventing personal names. The default `"names"` mode requires valid BibTeX
person lists separated by `and`; retain each supplied surname/given-name order
and mark an explicitly incomplete list with `and others`, not a fictional
person named “al.”. Unknown authors remain missing. Never infer a person's
identity or expand initials merely to produce a cleaner citation.
