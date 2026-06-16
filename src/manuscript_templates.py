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

SOURCE_OWNED_TEMPLATE_NAMES: Final[frozenset[str]] = frozenset(
    {"abstract.md", "orientation.md"}
)

DEFAULT_TEMPLATES: Final[dict[str, str]] = {
    # Abstract and orientation are authored source templates. Keeping stale
    # embedded fallbacks for them risks silently dropping reader-contract
    # changes in non-repo render contexts.
    "method_assurance_reference.md": """# Method & Assurance Reference: claim evidence, safety gates, and refresh duties {#sec:method-assurance-reference}

This reference holds the shared method, governance, and assurance tables that
every module applies. Each module links here instead of restamping the same
tables, so a reader maintains one canonical copy of the capstone thread, claim
ledger, competency rubric, refresh triggers, safety boundary, and mastery
evidence. Module sections name their local source spine and topic, then point
to the canonical table in this section.

## Method figures and course links: assurance visuals and navigation

{{VISUAL_SYNTHESIS}}

## Capstone phase, artifact, and review-gate ladder: required handoff sequence

{{CAPSTONE_SCAFFOLD_ROWS}}

## Claim and evidence ledger: claim classes, evidence floors, and review duties

{{CANONICAL_CLAIM_LEDGER_ROWS}}

## Competency and mastery rubric: scoring dimensions and visible proof

{{CANONICAL_COMPETENCY_RUBRIC_ROWS}}

## Refresh triggers and required actions: source, safety, and tool-change duties

{{CANONICAL_REFRESH_TRIGGER_ROWS}}

## Safety boundary: authorized, synthetic, defensive, and non-operational practice

{{CANONICAL_SAFETY_BOUNDARY}}

## Mastery evidence standard: retained artifacts, reviewer challenge, and transfer

{{CANONICAL_MASTERY_ROWS}}
""",
    "part.md": """# {{SECTION_TITLE}} {#{{SECTION_LABEL}}}

## {{SECTION_TITLE}} learning spine and source route: unit purpose, module order, and evidence handoff

{{SECTION_SUMMARY}}

### {{SECTION_TITLE}} visual navigation and module map: evidence flow, order, and safety cues

{{VISUAL_SYNTHESIS}}

### {{SECTION_TITLE}} module roster and source-lane inventory: citations, lanes, and learner route

{{SECTION_ROWS}}
""",
    "chapter.md": """# {{SECTION_TITLE}} {#{{SECTION_LABEL}}}

### {{SECTION_TITLE}} figures and course links: visual evidence, source flow, and navigation

{{VISUAL_SYNTHESIS}}

{{SECTION_BODY}}

### {{SECTION_TITLE}} learning-path links: module map, overview, and curriculum atlas

{{SECTION_NAV_PROSE}}

{{SECTION_CROSSREFS}}
""",
    "appendix.md": """# {{SECTION_TITLE}} {#{{SECTION_LABEL}}}

{{SECTION_BODY}}

### {{SECTION_TITLE}} visual navigation and evidence figures: purpose, source flow, and limits

{{VISUAL_SYNTHESIS}}

### {{SECTION_TITLE}} runtime item map and source roster: generated rows and citation support

{{SECTION_ROWS}}
""",
    "bibliography_atlas.md": """# Bibliography Atlas: source keys, refresh evidence, and citation workflow {#sec:bibliography_atlas}

The bibliography atlas is generated from the parsed source-guide reference
list plus official source-quality anchors. Citation keys are cited in prose
with Pandoc citations. Treat this appendix as the source-audit surface: each
curated anchor keeps its source URL, source lane, checked date, refresh trigger,
and verification note visible so moved pages, blocked automated fetches, and
volatile standards can be reviewed without changing citation keys.

## Bibliography atlas navigation figures and source links: visual route through citation evidence

{{VISUAL_SYNTHESIS}}

## Current-source additions and refreshes: newly checked anchors and changed caveats {#sec:current-source-additions-and-refreshes}

The current-source table isolates anchors added or materially refreshed in the
latest internet-citation pass. It is deliberately narrower than the full ledger:
rows appear here only when the source URL was verified for this pass, a moved URL
was refreshed, or a retrieval caveat changed the claim boundary. Draft sources
retain draft-status caveats rather than being treated as final guidance.

{{CURRENT_SOURCE_UPDATE_ROWS}}

## Source refresh ledger: cadence, checked dates, and due-status evidence {#sec:source-refresh-ledger}

{{SOURCE_REFRESH_ROWS}}

## Bibliography atlas rows: guide keys, curated anchors, and support-source roles {#sec:bibliography-rows}

{{BIBLIOGRAPHY_ATLAS_ROWS}}
""",
    "references.md": """# References {.unnumbered}

The render pipeline reads `references-*.bib`, which is generated from parsed
curriculum data plus official source-quality anchors. Manuscript prose should
cite with Pandoc citation keys such as `[@ageint137]`; do not paste
bibliography entries into source prose.
""",
}


def template_text(name: str) -> str:
    """Return the canonical template text for ``name``."""

    canonical = Path(__file__).resolve().parents[1] / "manuscript" / "templates" / name
    if canonical.is_file():
        return canonical.read_text(encoding="utf-8")
    if name in SOURCE_OWNED_TEMPLATE_NAMES:
        raise FileNotFoundError(
            f"{name} is a source-owned manuscript template and has no embedded "
            "fallback; keep manuscript/templates available to avoid stale "
            "abstract or orientation prose."
        )
    return DEFAULT_TEMPLATES[name]


def _write(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text.rstrip() + "\n", encoding="utf-8")


def write_template_library(templates_dir: Path) -> list[Path]:
    """Write the neutral source template library into ``templates_dir``."""
    templates_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for name in TEMPLATE_NAMES:
        path = templates_dir / name
        _write(path, template_text(name))
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
