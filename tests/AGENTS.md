# AGENTS.md - AGEINT Tests

Write tests before implementation changes. Prefer behavior tests over implementation-detail assertions.

Keep coverage focused on parser accessors, neutral templates, manifest paths, generated variables, figure registry integrity, bibliography anchors, output hydration, and safety boundaries.

No mocks are needed for the local parser and renderer; use real guide fixtures and temporary project directories.

Tests protect semantic generated paths, token/reference resolution, stable
source identities, structured source metadata, figure integrity, and explicit
permission/error boundaries. External source section locators are not book
navigation. Renderer and audit passes are structural evidence, not proof of
truth, learning gain, safety, accessibility conformance, or legal compliance.

Shared inventory helpers live in `tests/manuscript_quality/inventory_helpers.py`.
`test_manuscript_inventory_structure.py` protects the generated structure;
`test_manuscript_inventory_quality.py` protects teaching-phase order.
`test_topic_spine.py` covers topic identity and deduplication, and
`test_topic_frame_routing.py` covers token boundaries and safe-subject
precedence under colliding raw-source terms. Native bibliography tests exercise
Pandoc and XeLaTeX/BibTeX rather than pinning copied bibliography strings.

Do not add manuscript wording snapshots, title-keyword density thresholds,
repetition percentages, or live-count/date snapshots. Inspect the actual PDF
and canonical HTML, exercise runnable examples, and review source-to-claim
fit. Honest fictional-case labels and properly attributed source locators must
not be rewritten merely to satisfy a word ban.

The session-scoped `built_output` fixture only reads existing output; it never
rebuilds missing or stale publications. Generate new editions explicitly before
validation, preserving original failures. Derive paths via `manuscript_dir()`
and isolate build mutations in temporary projects. Use environment isolation
for missing tools, not replacement of executable discovery.
