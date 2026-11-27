# Offline publication assurance example

This independent documentation example checks the integrity of synthetic
publication records. It describes which files the local check observed and
which parts of the native publication workflow require separate review.

| Path | Role |
| --- | --- |
| `docs/manuscript/` | Native publication configuration, references, and reusable templates |
| `data/` | Native authoring inputs |
| `output/manuscript/` | Generated native manuscript |
| [`docs/examples/assurance-note/`](examples/assurance-note/) | Independent example text, synthetic fixture, and staging command |

Staging copies only the example into a new Git workspace. The staged
`docs/manuscript/` is disposable. The existing repository and its release
artifacts remain intact.

## Reproduce the example locally

Use a clean AGEINT checkout containing this documentation and a separate
[Template checkout at revision `87704feae0a4490ef7dad9c931d268e8c30273c2`](https://github.com/docxology/template/tree/87704feae0a4490ef7dad9c931d268e8c30273c2).
Use the [Template prerequisites](https://github.com/docxology/template/blob/87704feae0a4490ef7dad9c931d268e8c30273c2/docs/RUN_GUIDE.md) for Pandoc, pandoc-crossref and XeLaTeX.
Set `ageint_checkout` to the absolute path of the clean source checkout. Run
from Template, using an unused `projects/working/AGEINT` slot.

```sh
uv sync --locked --no-dev
proof_parent=$(mktemp -d)
proof_project="$proof_parent/AGEINT"
uv run --no-sync python "$ageint_checkout/docs/examples/assurance-note/stage.py" "$proof_project"
git -C "$proof_project" init -q
git -C "$proof_project" add docs
git -C "$proof_project" -c user.name="Local verification" -c user.email="verification@example.invalid" commit -qm "Stage assurance example"
mkdir -p projects/working
ln -s "$proof_project" projects/working/AGEINT
uv run --no-sync python scripts/pipeline/stage_03_render.py --project working/AGEINT --skip-manuscript-hydration
uv run --no-sync python scripts/pipeline/stage_04_validate.py --project working/AGEINT
```

The staged project contains `docs/source_receipt.json` with the source revision
and hashes of the copied inputs, `output/assurance-results.json` with observed
outcomes, and the PDF, HTML, and validation reports under `output/`.

## Interpreting the checks

A verified digest establishes byte equality against the declared fixture value.
A changed or absent record stays visible in the outcome counts. This check
covers a self-contained example and provides no claim about the full curriculum,
its source citations, native test coverage, or release readiness.

The existing public CI workflow runs on pull requests targeting the default
branch and on pushes to that branch. The native manuscript workflow also has
path-filtered triggers, a manual trigger, and a schedule. Its rebuilt output
and reports can be retained as workflow artifacts. The local commands above
do not invoke those workflows.
