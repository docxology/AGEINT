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
Set `ageint_checkout` to the absolute path of the clean source checkout. From
Template, use the dedicated `projects/working/AGEINT-assurance` slot. Registration
stops the example if that slot is already occupied.

```sh
(
    set -eu
    uv sync --locked --no-dev
    proof_parent=$(mktemp -d)
    proof_project="$proof_parent/AGEINT-assurance"
    uv run --no-sync python "$ageint_checkout/docs/examples/assurance-note/stage.py" "$proof_project"
    git -C "$proof_project" init -q
    git -C "$proof_project" add docs
    git -C "$proof_project" -c user.name="Local verification" -c user.email="verification@example.invalid" commit -qm "Stage assurance example"
    mkdir -p projects/working
    ln -s "$proof_project" projects/working/
    trap 'if [ "$(readlink projects/working/AGEINT-assurance)" = "$proof_project" ]; then unlink projects/working/AGEINT-assurance; fi' EXIT
    uv run --no-sync python scripts/pipeline/stage_03_render.py --project working/AGEINT-assurance --skip-manuscript-hydration
    uv run --no-sync python scripts/pipeline/stage_04_validate.py --project working/AGEINT-assurance
    printf 'Assurance output is in %s/output/\n' "$proof_project"
)
```

The staged project contains `docs/source_receipt.json` with the source revision
and hashes of the copied inputs, `output/assurance-results.json` with observed
outcomes, and the PDF, HTML, and validation reports under `output/`.

## Interpreting the checks

A verified digest establishes byte equality against the declared fixture value.
A changed or absent record stays visible in the outcome counts. This check
covers a self-contained example and provides no claim about the full curriculum,
its source citations, native test coverage, or release readiness.

The repository defines branch-triggered CI and a path-filtered manuscript
workflow. Check the [Actions workflow list](https://github.com/docxology/AGEINT/actions)
for current enablement. The local commands above run independently of those
workflows.
