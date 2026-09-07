# Manuscript Status

- **Project:** AGEINT
- **Manuscript title:** AGEINT: Agentic Intelligence
- **Location:** `docs/manuscript/` (canonical manuscript source; the render consumes the refreshed copy under `output/manuscript/`, and the sibling template's `infrastructure.core.project_paths.resolve_source_manuscript_dir` prefers a conventional root `manuscript/` tree only when it holds real Markdown/TeX source — a config-only dir cannot shadow this one)
  **Invariant:** keep the root `manuscript/` directory absent or config-only — a tree there holding real Markdown/TeX source would win `resolve_source_manuscript_dir` and shadow this canonical one.
- **Type:** Active publication-target manuscript (0 section files)
- **Status file purpose:** Tracks publication-readiness of the manuscript content in this directory. Migrated from the legacy top-level `manuscript/` location.
