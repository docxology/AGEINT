# AGENTS.md — `intelligence_content/`

Research-backed domain profiles, practice lenses, safe curriculum treatments,
and generated topic-lesson prose. Business logic for lesson **Concept**,
**Why it matters**, **Evidence**, **Artifact**, **Misconception**, and
**Transfer** fields lives here—not in `scripts/` or `output/manuscript/`.

Part modules (`_01_part.py` … `_12_topic_frames.py`) merge at import time via
`__init__.py`. Keep each file ≤500 lines (enforced by
`tests/test_file_size_inventory.py`). Keyword routes split across
`_12_concept_routes.py`, `_12_concept_routes_b.py`, and
`_12_concept_routes_domains.py` (**125** routes measured at build time).

## Topic frame routing (three tiers)

Generated topic lessons resolve frames in order:

| Tier | Source | When it applies |
| --- | --- | --- |
| **A — keyword** | `_12_concept_routes*.py` → `CONCEPT_KEYWORD_ROUTES` | Token- or phrase-bound match on `display_title` + `raw_title` via `_match_keywords()` |
| **B — category** | `_12_topic_frames.py` → `CATEGORY_CONCEPT_FRAMES` | Subcategory from `_category_frame_key()` after topic-first `TopicEntry.risk_category` |
| **C — synthesis** | `_12_topic_frames.py` → `synthesized_*()` | Fallback anchored on `raw_title` when `display_title` matches `GENERIC_DISPLAY_TITLE_MARKERS` |

Public entry points (called from `_10_part.py` / `_11_part.py`):

| Function | Module | Role |
| --- | --- | --- |
| `concept_frame_for_entry(entry, coursebook, profile)` | `_12_topic_frames` | Tier A/B/C concept paragraph |
| `evidence_prompt_for_entry(entry, lens, coursebook)` | `_12_topic_frames` | Evidence-to-inspect line |
| `artifact_prompt_for_entry(entry, lens, coursebook)` | `_12_topic_frames` | Student artifact prompt |
| `misconception_for_entry(entry, coursebook, *, lesson_index, chapter_title)` | `_12_topic_frames` | Rotated misconception text |
| `why_it_matters_for_entry(entry, profile, coursebook, *, lesson_index)` | `_12_topic_frames` | Risk-category failure hints + rotated templates |
| `lesson_intro_paragraph(...)` | `_12_topic_frames` | Opener listing up to three distinct topic titles |

Keyword matching (`_12_concept_routes._match_keywords`):

- Multi-word or hyphenated keywords: substring match on lowered title text.
- Single-word keywords: whole-token match only (prevents `cti` ⊂ `directive`, `cryptograph` ⊂ `cryptographic`).
- Multi-keyword tuples match on **any** keyword — prefer specific phrases, not bare tokens like `tradecraft` or `agent`.

## Risk and safe-title modules

| Module | Role |
| --- | --- |
| `_07_risk_categories.py` | `_topic_risk_category()` — topic classifiers first; `_chapter_context_risk_category()` only when topic level is `standard` |
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

Display-title contract (`_09_part._safe_topic_entries`):

- When `safe_curriculum_treatment()` yields a generic marker, fall back to
  `_clean_display_title(raw_title)` when the shard title is educational.
- Dedup qualifiers prefer section locus or raw-title anchor words when display
  keys collide.

## Topic spine

| Module | Role |
| --- | --- |
| `_07_safe_titles.py` | `GENERIC_DISPLAY_TITLE_MARKERS`, preserve-title categories, `_topic_anchor_words()`, contextual titles |
| `_09_part.py` | `_safe_topic_entries()`, display-title dedup; re-exports `GENERIC_DISPLAY_TITLE_MARKERS` via `_07_part` merge |
| `_06_part.py` | `COURSEBOOK_PROFILES`, `safe_pattern_treatment()` for pattern registry chapter |
| `_10_part.py` | Primer/outcomes/vocabulary; delegates lesson fields to `_12_topic_frames` |
| `_11_part.py` | `chapter_topic_lessons()`, worked example, practice sequence assembly |

## Tests guarding this package

- `tests/test_topic_spine.py` — deduped display titles, no case-review stubs
- `tests/test_topic_content_quality.py` — anti-fallback phrases, ≥80% title-keyword anchoring, Tier C ≤15%, teams-confuse ≤20%, collapsed cogsec ≤1/chapter, 16-chapter spot-check
- `tests/test_chapter_fragment_quality.py` — overview primer, worked-practice profile refs, architecture-source echoes, required module sections
- `tests/test_topic_frame_routing.py` — token-boundary keyword regressions; OPSEC/compartmentation/ACH routing

## Editing rules

- Add domain depth via new keyword routes, category frames, or profiles—not hand-edited `output/manuscript/`.
- Append routes to `_12_concept_routes_domains.py` or split sibling modules before any file exceeds 500 lines.
- Never expose raw unsafe source titles in student-facing misconception or transfer text; use `display_title`, `chapter_title`, and `lesson_index` rotation.
- Rebuild after changes: `uv run python scripts/build_curriculum.py`.
