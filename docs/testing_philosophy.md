# Testing Philosophy - AGEINT no-mocks gates and verifier-first evidence

## No mocks: real parser, source locks, figures, and generated outputs

Tests use real curriculum shards, real builds, temp directories, and subprocess script smoke tests. Do not use `unittest.mock`, `MagicMock`, or `mocker.patch`. Environment isolation via pytest `monkeypatch.delenv` is limited to template-resolver branch tests.

## Read-only published-output fixture

`tests/conftest.py` defines session-scoped `built_output`, which returns the
existing `output/` tree without invoking a builder. Missing artifacts and stale
publication evidence must remain visible to their real guards; discovering an
SDK does not authorize a test to repair the publication it is validating.

Generate a new edition explicitly in a development or fresh acceptance checkout
using the [build and verification recipes](../README.md#commands), then run the
complete suite in the same prepared SDK environment. Preserve an original
checked-in publication failure before rebuilding; generation is not promotion.

## Test categories: source identity, safety, figures, prose, and readiness

| Area | Example modules |
| --- | --- |
| Curriculum shards | `test_curriculum.py`, `test_sharded_data_integrity.py` |
| Source identity | `test_source_identity.py` |
| Manuscript manifest | `test_manuscript_manifest.py`, `test_manuscript_inventory_*.py` |
| Reader output | `test_pdf_quality.py`, real PDF page inspection, and canonical HTML browser smoke |
| Safety | `test_manuscript_safety_docs.py` |
| Cross-refs | `test_manuscript_crossrefs.py` |
| Artifact evidence | `test_artifact_evidence.py`, `test_pdf_quality.py`, `test_figure_quality_audit.py` |
| Scholarship quality | `test_scholarship_quality.py` |
| Scripts | `test_scripts.py`, `test_build_curriculum_script.py` |

## Coverage gate: per-project 90 percent source coverage

90% minimum on `src/` (`pyproject.toml` `fail_under = 90`). Combined multi-project pytest union is skipped via `[tool.template] skip_combined_pytest = true` because the full build is expensive.

Do not pin manuscript wording, full copied paragraphs, incidental live counts,
or historical review dates. Keep tests for source identity, parser boundaries,
precedence, transitions, errors, and native-format behavior. A fictional-case
label is an honest disclosure, not evidence of unfinished prose. External source
section locators are not hard-coded navigation within this book.

## Verifier-first evidence: audit artifacts and negative controls before polish

`scripts/audit_artifact_evidence.py --write` writes the current render evidence
manifest after a build/PDF render. It is deliberately stricter than a prose
checklist: the report fails if generated output is stale, rendered references
do not resolve, stale-output scans hit, figure quality fails, source-section
coverage has gaps, or the PDF quality/link audit finds banned phrases,
Markdown-file targets, `file:` targets, launch actions, or thin claim-bearing
scholarship support. `scripts/audit_scholarship_quality.py --write` also writes
the standalone source-family and triangulation report used by the combined
artifact manifest. That report also protects the early Synthetic Analytic
Tradecraft method contract: abstract and orientation output must retain the SAT
thesis, source-family triangulation, negative-control testing language, and the
`fig:ageint-synthetic-tradecraft-method-contract` cross-reference. It also
protects the analysis-validation protocol: the abstract/orientation output must
retain the `fig:ageint-analysis-validation-matrix` reference, the
`sec:analysis-validation-protocol` section, claim-class validation questions,
and failure-mode language. The follow-on lane contract is stricter: it derives
the required claim classes from `src/analysis_validation.py` and fails if a
manuscript keeps the section and figure reference but drops a lane such as
artifact readiness, governance/rights support, or reviewer disposition.

## Related documentation: agent rules, quickstart, and output inventory

- [`../tests/PATTERNS.md`](../tests/PATTERNS.md)
- [`agent_instructions.md`](agent_instructions.md)
