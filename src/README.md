# AGEINT Source

This folder contains the AGEINT parser, neutral template helpers,
research-backed intelligence content profiles and practice lenses,
generated-variable logic, registry-backed figure renderer, and semantic
manuscript renderer.

- Owner: AGEINT implementation.
- Status: manual code.
- Source of truth: code in this folder plus `data/curriculum/`.
- Test: `uv run pytest tests/ --cov=src --cov-fail-under=90` from the AGEINT root.
- Safety: encode defensive, accountable, synthetic, evidence-bounded defaults in generated prose.

Public exports are declared in `src/__init__.py`. Package layout:

| Module / package | Role |
| --- | --- |
| `build_pipeline.py` | Canonical `run_build()` orchestration |
| `orchestration_contracts.py`, `orchestration_audit.py` | Registry-backed build-stage and extension contract reports |
| `audit_contracts.py` | Fail-closed audit metadata, report paths, readiness gates, and negative controls |
| `curriculum.py` | Load and query sharded curriculum |
| `intelligence_content/` | Research anchors, domain profiles, practice lenses, topic-frame routing (see `intelligence_content/AGENTS.md`) |
| `manuscript_manifest/` | Semantic paths, section context, chapter fragments |
| `manuscript_variables/` | Runtime variables and BibTeX |
| `figures/` | Registry-backed figure rendering (see `figures/AGENTS.md`; Mermaid split in `_02b_mermaid.py`) |
| `manuscript_templates.py` | Neutral source template library |
| `_jsonl.py`, `_paths.py` | Shared JSONL reader and path bootstrap |

`intelligence_content/` is the modular source for external research anchors,
domain profiles, source lanes, safe substitutions, capstone workflows, and
subsection-scale practice lenses. It also owns accessibility review,
procurement oversight, HRIA/DPIA worksheets, data lineage, assessment
integrity, agent incident response, role competencies, and adversarial
assurance rows. Add official or scholarly sources there, then rebuild; do not
paste new intelligence prose into `output/manuscript/`.

The content layer separates IC-cycle governance, AI/data ethics,
declassified historical records, FININT/economic security, agentic AI,
OSINT/GEOINT, collection management, counterintelligence, cognitive security,
cyber threat intelligence, ICS/OT defense, and legal oversight into reusable
profiles. Keep new additions in that profile/lens shape so every generated
chapter can inherit the same source-backed, evidence-bounded contract.

`figures/` owns every generated visual asset and the registry contract,
renders Mermaid, Python, historical, and synthetic figure classes, then
normalizes PNGs onto square canvases so inserted manuscript figures do not
drift into narrow strips or oversized landscapes. Default builds allow
deterministic placeholder PNGs when Mermaid/Chrome is unavailable; set
`AGEINT_REQUIRE_RENDERED_FIGURES=1` for strict rendered output.

`intelligence_content/` topic lessons use three-tier frame routing (keyword →
category → synthesis). See `intelligence_content/AGENTS.md` for module map and
quality gates enforced in `tests/test_topic_content_quality.py`.

`manuscript_manifest/` is where generated section prose becomes concrete. Add
reusable paragraphs, research-synthesis blocks, visual-synthesis behavior, and
navigation logic there when the change depends on parsed curriculum data.

`source_identity.py` owns the source-guide identity lock helpers. The committed
lock in `data/source_identity/` preserves `ageint001` through
`ageint231`; append new guide references after that range instead of
renumbering existing entries. Current append-only references extend through
`ageint312`.
