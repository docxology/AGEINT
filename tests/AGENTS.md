# AGENTS.md - AGEINT Tests

Write tests before implementation changes. Prefer behavior tests over implementation-detail assertions.

Keep coverage focused on parser accessors, neutral templates, manifest paths, generated variables, figure registry integrity, bibliography anchors, output hydration, and safety boundaries.

No mocks are needed for the local parser and renderer; use real guide fixtures and temporary project directories.

Tests should protect the architectural contract: semantic generated paths, no
numbered source modules, no unresolved tokens, no raw LaTeX refs, no hard-coded
Figure/Section numbers, readable square-normalized figures, stable source
anchors, source identity lock stability, source-lane metadata, safety-audit
blocking rules, v2 appendix rendering, and generated README/AGENTS coverage for
meaningful folders. Deep-pass tests should also protect accessibility/UDL
review, procurement/vendor oversight, HRIA/DPIA worksheet, data lineage,
assessment-integrity, agent incident response, role-competency, and
adversarial-assurance sections.

Shared inventory constants and helpers live in `tests/manuscript_quality/inventory_helpers.py`.
Manuscript inventory checks are split across `test_manuscript_inventory_structure.py`
(structural contracts) and `test_manuscript_inventory_quality.py` (reader-facing
prose quality). Topic spine integrity lives in `test_topic_spine.py` (deduped
display titles, no case-review stubs). Generated lesson anti-fallback gates live in `test_topic_content_quality.py`
(`REMOVED_GENERIC_CONCEPT_PHRASES`, ≥80% title-keyword anchoring per chapter,
Tier C repetition caps ≤15% per chapter, `"teams confuse source material"` caps
≤20%, collapsed cognitive-security base titles ≤1/chapter, governance-bounded
lesson headers 0, category-concept repetition ≤25%, 16-chapter part spot-check).
Fragment quality across all six module sections lives in
`test_chapter_fragment_quality.py` (overview primer distinct titles, worked-practice
profile/lens references, architecture-source echo caps, required module section
lengths). Token-boundary keyword routing regressions live in
`test_topic_frame_routing.py`. The session-scoped `built_output` fixture in `conftest.py` ensures generated output exists before integration tests run (rebuilds when manuscript or figure registry is missing). A cold full `run_build()` can take several minutes locally; CI should cache `output/` when possible. Output-dependent tests request `built_output` and derive manuscript paths via `manuscript_dir()`.
