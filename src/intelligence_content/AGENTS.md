# AGENTS.md — `intelligence_content/`

Research-backed domain profiles, practice lenses, safe curriculum treatments,
and generated topic-lesson prose. Business logic for lesson **Concept**,
**Why it matters**, **Evidence**, **Artifact**, **Misconception**, and
**Transfer** fields lives here—not in `scripts/` or `output/manuscript/`.

Part modules (`_01_part.py` … `_12_topic_frames.py`) use **explicit imports** per shard
(no `merge_part_modules` in this package). Keep each file ≤500 lines (enforced by
`tests/test_file_size_inventory.py`). Keyword routes split across
Concept routes load from `data/concept_routes.yaml` and
`data/concept_routes_supplement.yaml` via `_data_loaders.py`; `_12_concept_routes*.py`
modules expose matchers only.

## Topic frame routing (three tiers)

Generated topic lessons resolve frames in order:

| Tier | Source | When it applies |
| --- | --- | --- |
| **A — keyword** | `_12_concept_routes*.py` → `CONCEPT_KEYWORD_ROUTES` | Token- or phrase-bound match on `display_title` + `raw_title` via `_match_keywords()` |
| **B — category** | `_12_topic_frames.py` → `CATEGORY_CONCEPT_FRAMES` | Subcategory from `_category_frame_key()` after topic-first `TopicEntry.risk_category` |
| **C — synthesis** | `_12_topic_frames.py` → `synthesized_*()` | Fallback anchored on `raw_title` when `display_title` matches `GENERIC_DISPLAY_TITLE_MARKERS` |

Public entry points (called from `_11_part.py` via `topic_lessons.py`):

| Function | Module | Role |
| --- | --- | --- |
| `resolve_topic_lesson_fields(...)` | `topic_lessons.py` | Single resolver for all lesson field strings |
| `concept_frame_for_entry(entry, coursebook, profile)` | `topic_frame_api` → `_12_topic_frames` | Tier A/B/C concept paragraph |
| `evidence_prompt_for_entry(entry, lens, coursebook)` | `topic_frame_api` → `_12_topic_frames` → `topic_prompt_routes` | Evidence-to-inspect line (YAML-backed) |
| `artifact_prompt_for_entry(entry, lens, coursebook)` | `topic_frame_api` → `_12_topic_frames` → `topic_prompt_routes` | Student artifact prompt (YAML-backed) |
| `resolve_topic_misconception(...)` | `topic_lessons.py` | Misconception via unified resolver (practice/knowledge-check paths) |
| `misconception_for_entry(...)` | `topic_frame_api` → `topic_rotation_templates` | Chapter-rotated misconception text (YAML templates + keyword branches) |
| `why_it_matters_for_entry(...)` | `topic_frame_api` → `topic_rotation_templates` | Risk-category failure hints + rotated templates |
| `lesson_intro_paragraph(...)` | `_12_topic_frames` | Opener listing up to three distinct topic titles |
| `lesson_educational_crossrefs(part, chapter)` | `markdown_refs` (called from `_11_part`) | Unit map figure, module overview, and atlas section refs in topic-lesson fragments |

Keyword matching (`_12_concept_routes._match_keywords`):

- Multi-word or hyphenated keywords: substring match on lowered title text.
- Single-word keywords: whole-token match only (prevents `cti` ⊂ `directive`, `cryptograph` ⊂ `cryptographic`).
- Multi-keyword tuples match on **any** keyword — prefer specific phrases, not bare tokens like `tradecraft` or `agent`.

## Risk and safe-title modules

| Module | Role |
| --- | --- |
| `topic_rotation.py` | Leaf module: stable `template_index()` (no upstream `intelligence_content` imports) |
| `topic_rotation_templates.py` | YAML evaluators for why-it-matters and misconception rotation |
| `topic_frame_api.py` | Stable re-export of frame helpers for `topic_lessons.py` |
| `topic_lesson_voice.py` | Reader-voice helpers (`for_topic`, evidence/artifact sentence shaping) |
| `topic_prompt_routes.py` | YAML evaluators for evidence/artifact prompts |
| `_07_risk_categories.py` | Re-exports YAML evaluator from `risk_routes.py` |
| `risk_routes.py` | Ordered rule evaluation over `data/topic_risk_routes.yaml`; import `topic_risk_category` from here |
| `_07_safe_titles.py` | `safe_curriculum_treatment()`, `GENERIC_DISPLAY_TITLE_MARKERS`, `is_generic_display_title()` |
| `_07_part.py` | Re-exports risk helpers; `REQUIRED_SOURCE_LANES` constants |

Topic-first routing applies chapter defaults (`cognitive_resilience`, `analytic_tradecraft`,
`operational_tradecraft_governance`, etc.) only after all title-specific classifiers
return `standard`. OPSEC, compartmentation, and cover topics route to
`operational_tradecraft_governance`; tradecraft core-principles chapter default is
`operational_tradecraft_governance`, not `analytic_tradecraft`.

`PRESERVE_TITLE_RISK_CATEGORIES` keeps curriculum shard titles for educational
chapters (SATs, AGEINT patterns, operator productivity, cognitive security,
HUMINT recruitment literacy, operational tradecraft governance) instead of
collapsing to generic safe fallbacks.

Display-title contract (`topic_entries.safe_topic_entries`):

- Pipeline: `load_sections` → `filter_meta_sections` → `apply_pattern_registry` → `safe_curriculum_title` → `dedupe_display_title`.
- When `safe_curriculum_treatment()` yields a generic marker, fall back to
  `clean_display_title(raw_title)` when the shard title is educational.
- Dedup qualifiers prefer section locus or raw-title anchor words when display
  keys collide.

## Topic spine

| Module | Role |
| --- | --- |
| `topic_entries.py` | `safe_topic_entries()` pipeline and display-title helpers |
| `_07_safe_titles.py` | `GENERIC_DISPLAY_TITLE_MARKERS`, preserve-title categories, `_topic_anchor_words()`, contextual titles |
| `_06_part.py` | Profile/lens matching, `COURSEBOOK_PROFILES` from `data/coursebook_profiles.yaml`, `safe_pattern_treatment()` |
| `_08_part.py` | Thin re-exports of safety/artifact tables from `data/safety_artifact_tables.yaml` |
| `_09_part.py` | Chapter briefs and row renderers |
| `_10_part.py` | Primer/outcomes/vocabulary only |
| `_11_part.py` | `chapter_topic_lessons()` via `topic_lessons.resolve_topic_lesson_fields()` |
| `topic_lessons.py` | Unified lesson-field resolver; imports `topic_frame_api` and `topic_lesson_voice` only |
| `topic_rotation.py` | Stable `template_index()` via `zlib.adler32` |

## Tests guarding this package

- `tests/test_topic_spine.py` — deduped display titles, no case-review stubs
- `tests/test_topic_content_quality.py` — anti-fallback phrases, ≥80% title-keyword anchoring, Tier C ≤15%, teams-confuse ≤20%, collapsed cogsec ≤1/chapter, 16-chapter spot-check
- `tests/test_chapter_fragment_quality.py` — overview primer, worked-practice profile refs, architecture-source echoes, required module sections
- `tests/test_topic_frame_routing.py` — token-boundary keyword regressions; OPSEC/compartmentation/ACH routing; YAML risk-, prompt-, and rotation-route parity fixtures
- `tests/test_topic_lessons.py` — rotation stability, transfer-task branches, unified resolver smoke
- `tests/test_intelligence_content_imports.py` — each shard imports without merge seeding

## Editing rules

- Add domain depth via new keyword routes, category frames, or profiles—not hand-edited `output/manuscript/`.
- Append routes to `data/concept_routes*.yaml`, `data/topic_risk_routes.yaml` (regenerate via `scripts/generate_risk_routes_yaml.py`), `data/topic_prompt_routes.yaml` (`scripts/generate_topic_prompt_routes_yaml.py`), or `data/topic_rotation_templates.yaml` (`scripts/generate_topic_rotation_templates_yaml.py`) before deleting Python tables. Edit `data/coursebook_profiles.yaml` and `data/safety_artifact_tables.yaml` directly (authoritative YAML; validate via `scripts/validate_declarative_yaml.py` and `tests/test_data_loaders.py`).
- Never expose raw unsafe source titles in student-facing misconception or transfer text; use `display_title`, `chapter_title`, and `lesson_index` rotation.
- Rebuild after changes: `uv run python scripts/build_curriculum.py`.
