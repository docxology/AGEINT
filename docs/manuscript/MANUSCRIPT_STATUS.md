# Manuscript Status

- **Project:** AGEINT
- **Manuscript title:** AGEINT: Agentic Intelligence

## Source and generated sections

`docs/manuscript/` is the canonical source directory. It holds the
configuration, preamble, and bibliography. Tokenized section templates live
under `templates/`. The renderer uses the generated sections and ordering
configuration under `output/manuscript/`.

Template's `resolve_source_manuscript_dir` gives a root `manuscript/` directory
precedence when it contains manuscript Markdown or TeX. Keep that path absent
or configuration-only to use the canonical source.

## Verification

The [citation-provenance evidence](../evidence/citation-provenance.md) covers
the retained citation audit and its isolated render. [Issue #23](https://github.com/docxology/AGEINT/issues/23)
tracks full publication verification against the current source.
