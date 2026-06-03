"""Neutral AGEINT manuscript template library generation.

The source manuscript uses a small set of reusable templates under
``manuscript/templates/``. Concrete chapter titles, labels, source spines,
section rows, paths, and bibliography material are injected into generated
files under ``output/manuscript/`` by :mod:`manuscript_manifest`.
"""

from __future__ import annotations

from pathlib import Path
from typing import Final

try:  # Support both package imports and direct script imports from ``src/``.
    from .curriculum import Curriculum
except ImportError:  # pragma: no cover - exercised by thin CLI wrappers
    from curriculum import Curriculum  # type: ignore[no-redef]


TEMPLATE_NAMES: Final[tuple[str, ...]] = (
    "abstract.md",
    "orientation.md",
    "method_assurance_reference.md",
    "part.md",
    "chapter.md",
    "appendix.md",
    "bibliography_atlas.md",
    "references.md",
)

DEFAULT_TEMPLATES: Final[dict[str, str]] = {
    "abstract.md": """# Abstract {#sec:abstract}

AGEINT, or Agentic Intelligence, names the application of autonomous and
semi-autonomous AI-agent systems to intelligence collection, processing,
exploitation, analysis, production, dissemination, and governed action. This
project turns {{CURRICULUM_SOURCE_GUIDE}} into a modular curriculum with
**{{CURRICULUM_PART_COUNT}} parts**, **{{CURRICULUM_CHAPTER_COUNT}} modules**,
**{{CURRICULUM_APPENDIX_COUNT}} methods appendices**,
**{{CURRICULUM_PATTERN_COUNT}} named AGEINT patterns**, and
**{{CURRICULUM_REFERENCE_COUNT}} parsed source-guide references**.

{{SOURCE_QUALITY_SPINE}}

{{INTELLIGENCE_RESEARCH_SPINE}}

The operational stance is defensive and educational: examples use synthetic
fixtures, public declassified materials, owned lab ranges, or tabletop
scenarios, and every module foregrounds provenance, uncertainty, legal
authority, human oversight, and cognitive security.

The scholarship layer is deliberately conservative. Perplexity and other
discovery tools can suggest candidate sources, but the manuscript cites only
directly represented official, standards, or scholarly anchors that survive
manual review and rebuild into the BibTeX corpus.

## Figures and course links

{{VISUAL_SYNTHESIS}}
""",
    "orientation.md": """# Curriculum Orientation {#sec:curriculum_orientation}

This manuscript is a runtime-hydrated curriculum atlas. The source templates
keep guide-derived values as neutral tokens, while the resolved manuscript in
`output/manuscript/` injects titles, labels, counts, source spines, semantic
paths, and bibliography rows from `data/curriculum/`.

## Runtime inventory

| Derived artifact | Runtime value |
|---|---:|
| Curriculum parts | {{CURRICULUM_PART_COUNT}} |
| Curriculum modules | {{CURRICULUM_CHAPTER_COUNT}} |
| Methods appendices | {{CURRICULUM_APPENDIX_COUNT}} |
| AGEINT patterns | {{CURRICULUM_PATTERN_COUNT}} |
| Parsed references | {{CURRICULUM_REFERENCE_COUNT}} |
| Official source-quality anchors | {{SOURCE_QUALITY_ANCHOR_COUNT}} |
| Intelligence research anchors | {{INTELLIGENCE_RESEARCH_ANCHOR_COUNT}} |
| Intelligence practice lenses | {{INTELLIGENCE_PRACTICE_LENS_COUNT}} |

## How to use this atlas

Read AGEINT as a navigable atlas rather than a linear textbook. Start with
the curriculum map to choose the part, open the part introduction to see the
module sequence, then use the chapter overview for the figures, source lane,
and assessment artifact that matter for the current decision. Keep the
bibliography atlas open when checking a claim, because it preserves source
identity, provenance type, and refresh context in one place.

## Reader paths

| Reader | Fast path | Evidence to keep |
|---|---|---|
| Instructor | Pair the part introduction with the module review checklist before assigning a studio exercise. | rubric row, excluded-action note, and source refresh trigger |
| Learner | Read the primer, topic lessons, worked safe example, and knowledge check before drafting a capstone packet. | claim ledger entry, uncertainty note, and blocked-use statement |
| Assurance reviewer | Follow the source lane map, governance card, figure registry, and bibliography row for each material claim. | source key, review owner, caveat, and reproducible artifact path |
| Builder or maintainer | Treat generated output as an audit surface; update data, templates, manifest code, or figure specs, then rebuild. | changed source file, regeneration command, and validation result |

## Consolidated glossary and index

Use this compact index to route common terms to the right audit surface before
reading a chapter in detail.

| Term | Working meaning | Primary audit surface |
|---|---|---|
| Source lane | The provenance, source tier, and refresh context that govern a claim. | Source lane map and bibliography rows |
| Claim ledger | A reviewable record of claim, evidence, caveat, confidence, and owner. | Research governance and capstone workflow |
| Safe substitution | A replacement of unsafe operational action with synthetic, public, tabletop, or governance work. | Safe substitution matrix |
| Reviewer gate | A named human approval or challenge point before reuse, presentation, or tool execution. | Assessment review and assurance rows |
| Figure registry | The reproducible map from figure label to generated asset, caption, and source section. | Figures and course links |

## Curriculum map

{{CURRICULUM_PART_ROWS}}

## Intelligence research profiles

{{INTELLIGENCE_PROFILE_ROWS}}

## Intelligence practice lenses

{{INTELLIGENCE_PRACTICE_LENS_ROWS}}

## Research anchor atlas

{{INTELLIGENCE_RESEARCH_ROWS}}

## Source lane map

{{INTELLIGENCE_SOURCE_LANE_ROWS}}

## Safe substitution matrix

{{SAFE_SUBSTITUTION_ROWS}}

## Capstone workflow

{{CAPSTONE_SCAFFOLD_ROWS}}

## Capstone model-answer exemplars

These exemplars show the expected shape of a strong answer without prescribing
a single conclusion. Use them as answer-key patterns for selected capstone
reviews.

| Capstone pattern | Model-answer evidence | What earns revision |
|---|---|---|
| Source-quality packet | Names the `ageintNNN` source key, source lane, direct evidence, caveat, uncertainty, and refresh trigger. | Claim cites a summary, omits the source key, or hides uncertainty. |
| Safe-lab packet | States the learning question, allowed inputs, excluded actions, tool allowlist, stop condition, and reviewer gate. | Uses private data, live targets, credentialed access, or an unreviewed tool path. |
| Assurance packet | Connects rubric score, rights impact, accessibility check, remediation owner, and debrief handoff. | Treats the score as proof, omits affected users, or leaves no owner for retest. |

## Accessibility and UDL review

{{ACCESSIBILITY_REVIEW_ROWS}}

## Procurement and vendor oversight

{{PROCUREMENT_OVERSIGHT_ROWS}}

## HRIA and DPIA worksheet

{{HRIA_DPIA_WORKSHEET_ROWS}}

## Data lineage registry

{{DATA_LINEAGE_REGISTRY_ROWS}}

## Assessment integrity protocol

{{ASSESSMENT_INTEGRITY_ROWS}}

## Agent incident response drill

{{AGENT_INCIDENT_RESPONSE_ROWS}}

## Role-based competency map

{{ROLE_COMPETENCY_ROWS}}

## Adversarial assurance cycle

{{ADVERSARIAL_ASSURANCE_ROWS}}

## Model and dataset documentation card

{{MODEL_DATASET_CARD_ROWS}}

## Transparency and communication notice

{{TRANSPARENCY_NOTICE_ROWS}}

## Records retention and audit trail

{{RETENTION_AUDIT_ROWS}}

## Release and change-control gate

{{RELEASE_CHANGE_CONTROL_ROWS}}

## Risk exception and acceptance memo

{{RISK_EXCEPTION_ROWS}}

## Learner support and accommodation plan

{{LEARNER_SUPPORT_ROWS}}

## Instructor question bank

{{QUESTION_BANK_ROWS}}

## Remediation backlog

{{REMEDIATION_BACKLOG_ROWS}}

## Scholarship and governance stance

AGEINT treats agentic intelligence as a governed socio-technical practice, not
as a bag of prompts or autonomous tricks. The curriculum therefore keeps AI
agent evaluation, identity, authorization, secure tool use, structured analytic
tradecraft, cognitive security, OSINT/GEOINT integrity, and ICS/OT safety in
one source-backed frame. Each source anchor has a curriculum role, a domain,
and a provenance type so readers can distinguish law, standards, official
guidance, public-domain historical material, and scholarly synthesis.

## Figures and course links

{{VISUAL_SYNTHESIS}}

## AGEINT pattern library

{{AGEINT_PATTERN_ROWS}}

## Safety rail

All exercises remain educational, lawful, defensive, historical, synthetic,
and non-operational. Modules may discuss intelligence, cyber, influence,
counterintelligence, and industrial systems as objects of study, but they do
not provide instructions for unauthorized collection, evasion, exploitation,
manipulation, covert targeting, or real-world harm.
""",
    "method_assurance_reference.md": """# Method & Assurance Reference {#sec:method-assurance-reference}

This reference holds the shared method, governance, and assurance tables that
every module applies. Each module links here instead of restamping the same
tables, so a reader maintains one canonical copy of the capstone thread, claim
ledger, competency rubric, refresh triggers, safety boundary, and mastery
evidence. Module sections name their local source spine and topic, then point
to the canonical table in this section.

## Figures and course links

{{VISUAL_SYNTHESIS}}

## Capstone phase, artifact, and review-gate ladder

{{CAPSTONE_SCAFFOLD_ROWS}}

## Claim and evidence ledger

{{CANONICAL_CLAIM_LEDGER_ROWS}}

## Competency and mastery rubric

{{CANONICAL_COMPETENCY_RUBRIC_ROWS}}

## Refresh triggers and required actions

{{CANONICAL_REFRESH_TRIGGER_ROWS}}

## Safety boundary

{{CANONICAL_SAFETY_BOUNDARY}}

## Mastery evidence standard

{{CANONICAL_MASTERY_ROWS}}
""",
    "part.md": """# {{SECTION_TITLE}} {#{{SECTION_LABEL}}}

{{SECTION_SUMMARY}}

## Figures and course links

{{VISUAL_SYNTHESIS}}

## Runtime module list

{{SECTION_ROWS}}
""",
    "chapter.md": """# {{SECTION_TITLE}} {#{{SECTION_LABEL}}}

## Figures and course links

{{VISUAL_SYNTHESIS}}

{{SECTION_BODY}}

## Cross-links

Use these links to read this module in sequence: the curriculum orientation,
the parent part, the previous module, and the next module when available. Keep
this navigation paired with the module source spine and capstone artifact so
readers can see what evidence carries forward. Context: {{SECTION_NAV_CONTEXT}}

{{SECTION_CROSSREFS}}
""",
    "appendix.md": """# {{SECTION_TITLE}} {#{{SECTION_LABEL}}}

{{SECTION_BODY}}

## Figures and course links

{{VISUAL_SYNTHESIS}}

## Runtime item map

{{SECTION_ROWS}}
""",
    "bibliography_atlas.md": """# Bibliography Atlas {#sec:bibliography_atlas}

The bibliography atlas is generated from the parsed source-guide reference
list plus official source-quality anchors. Citation keys are cited in prose
with Pandoc citations.

## Figures and course links

{{VISUAL_SYNTHESIS}}

## Source refresh ledger

{{SOURCE_REFRESH_ROWS}}

## Bibliography rows

{{BIBLIOGRAPHY_ATLAS_ROWS}}
""",
    "references.md": """# References {.unnumbered}

The render pipeline reads `references-*.bib`, which is generated from parsed
curriculum data plus official source-quality anchors. Manuscript prose should
cite with Pandoc citation keys such as `[@ageint137]`; do not paste
bibliography entries into source prose.
""",
}


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_template_library(templates_dir: Path) -> list[Path]:
    """Write the neutral source template library into ``templates_dir``."""
    templates_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for name in TEMPLATE_NAMES:
        path = templates_dir / name
        _write(path, DEFAULT_TEMPLATES[name])
        written.append(path)
    return written


def write_manuscript_templates(curriculum: Curriculum, manuscript_dir: Path) -> list[Path]:
    """Compatibility wrapper that writes only the neutral template library.

    Older AGEINT builds emitted one concrete token file per chapter directly
    under ``manuscript/``. The hardened architecture keeps source authoring
    neutral and emits concrete sections only under ``output/manuscript/``.
    """
    _ = curriculum
    return write_template_library(manuscript_dir / "templates")
