# Architecture: shard-first curriculum build and generated manuscript flow

AGEINT follows the template code-project shape: `src/`, `scripts/`, `tests/`, `manuscript/`, `docs/`, `data/`, and `output/`.

The build loads the committed curriculum spine from `data/curriculum/` (optional
guide input when present). The renderer builds a manifest of semantic manuscript
sections and hydrates neutral templates from `manuscript/templates/` into
`output/manuscript/`. Long chapters render as fragment directories such as
`parts/ageint-agentic-intelligence/foundations-of-ageint/00-overview.md`.
Concrete titles, labels, citations, counts, and file paths are generated data.

Research-backed intelligence content lives in the `src/intelligence_content/`
package. Research anchors load from `data/research_anchors/*.jsonl`; domain
profiles and practice lenses are declared on chapter shards via
`content_profile` and `practice_lens`. `src/manuscript_manifest/` injects the
matched profile and practice lens into each generated chapter.

The architecture intentionally separates four surfaces:

- **Source spine:** sharded curriculum under `data/curriculum/` (optional historical SIST guide when present) and neutral manuscript templates.
- **Knowledge spine:** verified source anchors and reusable domain profiles.
- **Renderer spine:** manifest, variables, bibliography, and figure registry code.
- **Output spine:** generated semantic Markdown, BibTeX, figures, and audit data.

This separation keeps the project reproducible. To change prose structure,
visible section titles, or generated body composition, update templates or
manifest context builders. To change scholarship, update source anchors and
profiles. To change counts, paths, or citations, update curriculum shards or parser logic and
rebuild.

## Contract registries: modular extension points with verifier ownership

AGEINT treats build stages, audit gates, source packs, and Mermaid diagram
types as typed registries rather than scattered hard-coded lists. The contracts
live in `src/orchestration_contracts.py`, `src/audit_contracts.py`,
`src/intelligence_content/source_packs.py`, and
`src/figures/mermaid_contracts.py`. They preserve the current source-owned
pipeline while making new extension points explicit: every new stage, audit,
pack route, or diagram type must declare inputs, outputs, failure modes, and a
negative-control or reader-detail obligation.

Run `uv run python scripts/audit_orchestration_contract.py --format json` to
inspect the combined contract map. Use
[`orchestration_contract.md`](orchestration_contract.md) for the operator-facing
extension workflow.

## Topic lesson frames: declarative routing, safe titles, and source-backed fields

Topic lessons inside each chapter resolve through `topic_lessons.resolve_topic_lesson_fields()`:

1. **Keyword routes** — token-bound matches on display/raw titles (`_12_concept_routes*.py`; data in `data/concept_routes*.yaml`).
2. **Category frames** — topic-first risk categories from `risk_routes.py` + `data/topic_risk_routes.yaml`; chapter defaults only when topic-level classification is `standard`.
3. **Synthesis** — topic-anchored fallback prose; when `display_title` matches `GENERIC_DISPLAY_TITLE_MARKERS`, anchors on `raw_title` (`_12_topic_frames.py`).

Evidence and artifact prompt strings resolve through `topic_prompt_routes.py` over
`data/topic_prompt_routes.yaml`. Why-it-matters and misconception rotation resolve
through `topic_rotation_templates.py` over `data/topic_rotation_templates.yaml`.
`_12_topic_frames.py` keeps concept synthesis and delegates prompts/rotation to those modules.

Coursebook profiles and safety worksheet tables load from `data/coursebook_profiles.yaml`
and `data/safety_artifact_tables.yaml` via `_data_loaders.py` (`_06_part.py`, `_08_part.py`).

`intelligence_content` shards use explicit imports (no `merge_part_modules`); package
`__init__.py` re-exports the public API only.

### Import model: deferred P4 package-boundary cleanup

| Package | Import style |
| --- | --- |
| `intelligence_content/` | Explicit per-shard imports (P3 complete except `_01_part` / `_11_part` sibling-package fallbacks) |
| `manuscript_manifest/`, `figures/`, `manuscript_variables/` | Explicit per-shard imports in package `__init__.py` (P5.5) |

When adding code under the merged packages, follow existing shard patterns; do not
assume `intelligence_content`-style explicit imports apply repo-wide yet.

`topic_entries.safe_topic_entries()` builds `TopicEntry` rows from curriculum sections before frame resolution. Template rotation uses `topic_rotation.template_index()` (`zlib.adler32`) with per-chapter offsets so adjacent modules do not repeat identical misconception strings. `topic_lessons.py` imports frame helpers through `topic_frame_api.py` and reader-voice helpers through `topic_lesson_voice.py`.

See [`src/intelligence_content/AGENTS.md`](../src/intelligence_content/AGENTS.md) for the full routing table.

Quality gates in `tests/test_topic_content_quality.py` and
`tests/test_chapter_fragment_quality.py` cap Tier C `in the … lane:` markers
(≤15% per chapter), `"teams confuse source material"` boilerplate (≤20%),
collapsed cognitive-security base titles (≤1 per chapter), governance-bounded
lesson headers (0), and category-concept repetition (≤25% per chapter). Sixteen
representative chapters (one per part) are spot-checked for domain titles.
