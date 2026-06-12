from __future__ import annotations

"""Registry-backed AGEINT figure generation.

The figure pipeline keeps visual assets generated and auditable. Mermaid
sources, Python visualizations, historical public-domain imagery, and
synthetic conceptual plates all resolve to local PNG files under
``output/figures/`` and a registry JSON that manuscript rendering consumes.
"""


from dataclasses import asdict, dataclass
from enum import Enum
import hashlib
from importlib import import_module
import io
import json
import math
from pathlib import Path
import re
import shutil
import subprocess  # nosec B404 - fixed argv, no shell, local renderer.
import textwrap
import urllib.error
import urllib.request
from typing import Any, Sequence, cast

from curriculum import Curriculum
from markdown_refs import figure_ref


class FigureKind(str, Enum):
    """Supported AGEINT visual asset classes."""

    MERMAID = "mermaid"
    PYTHON = "python"
    HISTORICAL = "historical"
    AI_GENERATED = "ai_generated"


@dataclass(frozen=True)
class FigureSpec:
    """One registry-backed AGEINT figure."""

    label: str
    title: str
    caption: str
    alt_text: str
    kind: FigureKind
    output_path: str
    source_section: str
    section_label: str
    provenance: dict[str, str]
    source_artifact_path: str = ""

    def registry_entry(self, project_root: Path) -> dict[str, Any]:
        """Return a JSON-serializable registry row with current file hash."""
        from ._03_part import _sha256, _validate_png_asset

        asset = project_root / self.output_path
        _validate_png_asset(asset, self)
        payload = asdict(self)
        payload["kind"] = self.kind.value
        payload["sha256"] = _sha256(asset)
        payload["bytes"] = asset.stat().st_size
        return payload


HISTORICAL_ASSETS: tuple[dict[str, str], ...] = (
    {
        "slug": "historical-hexagon-quang-tri",
        "title": "HEXAGON Satellite Image of Vietnam War Bomb Craters",
        "caption": (
            "Public-domain USGS EROS declassified HEXAGON image used as a "
            "historical example of imagery becoming a governed analytic source."
        ),
        "alt_text": "Black-and-white declassified satellite imagery of Quang Tri bomb craters.",
        "source_page": "https://www.usgs.gov/media/images/hexagon-satellite-image-vietnam-war-bomb-craters",
        "asset_url": "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/media/images/19730320_HEXAGON_QuangTri.png",
        "source_section": "chapter:16",
        "date": "1973-03-20",
    },
    {
        "slug": "historical-forbidden-city",
        "title": "Declassified Satellite Imagery of the Forbidden City",
        "caption": (
            "Public-domain USGS EROS declassified imagery of the Forbidden City "
            "as a local historical image for GEOINT source-provenance discussion."
        ),
        "alt_text": "Black-and-white satellite image of the Forbidden City in Beijing.",
        "source_page": "https://www.usgs.gov/media/images/declassified-satellite-imagery-forbidden-city-beijing-china",
        "asset_url": "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/media/images/Declassified%20imagery%20D3C1205-100021A081_Bejing_03121973.jpg",
        "source_section": "chapter:11",
        "date": "1966 approx.",
    },
    {
        "slug": "historical-dakar-kh7",
        "title": "KH-7 Imagery of Dakar",
        "caption": (
            "Public-domain USGS EROS KH-7 image used to show how historical "
            "collection becomes reproducible open-source imagery analysis."
        ),
        "alt_text": "Black-and-white KH-7 imagery of the western edge of Dakar, Senegal.",
        "source_page": "https://www.usgs.gov/media/images/declassified-satellite-imagery-declass-1",
        "asset_url": "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/thumbnails/image/dmiddeclass1senegalafrica.jpg",
        "source_section": "chapter:16",
        "date": "1966 approx.",
    },
    {
        "slug": "historical-missouri-river-kh9",
        "title": "KH-9 Imagery of the Missouri River",
        "caption": (
            "Public-domain USGS EROS KH-9 image used as a historical example "
            "of declassified remote-sensing material with explicit provenance."
        ),
        "alt_text": "Declassified satellite imagery and modern map view of the Missouri River.",
        "source_page": "https://www.usgs.gov/media/images/declassified-satellite-imagery-declass-3",
        "asset_url": "https://d9-wret.s3.us-west-2.amazonaws.com/assets/palladium/production/s3fs-public/thumbnails/image/dmiddeclass3moriversd.jpg",
        "source_section": "chapter:11",
        "date": "1982-07-22",
    },
)

PYTHON_VISUALS: tuple[dict[str, str], ...] = (
    {
        "slug": "ageint-citation-density",
        "title": "AGEINT Citation Density",
        "caption": (
            "Method-backed audit chart reporting direct external citation counts "
            "per generated module; labels, denominators, and counting rule come "
            "from the curriculum parser."
        ),
        "alt_text": (
            "Bar chart of direct citation counts by generated AGEINT module, "
            "used as a source-review workload signal rather than capability evidence."
        ),
        "renderer": "citation_density",
        "source_section": "orientation.md",
    },
    {
        "slug": "ageint-source-quality-spine",
        "title": "AGEINT Source-Quality Spine",
        "caption": (
            "Compact audit matrix listing official source-quality anchors, their "
            "source tier, claim role, evidence use, and refresh duty; it is a "
            "source-management view, not quantitative evidence."
        ),
        "alt_text": "Audit matrix of official source-quality anchors, source tiers, roles, and refresh duties.",
        "renderer": "source_quality_spine",
        "source_section": "bibliography-atlas.md",
    },
    {
        "slug": "ageint-source-freshness-coverage",
        "title": "AGEINT Source Freshness and Coverage",
        "caption": (
            "Evidence-derived chart summarizing curated research-anchor freshness, "
            "source lanes, and evidence tiers from local metadata; counts are audit "
            "coverage signals, not source-quality scores."
        ),
        "alt_text": (
            "Chart of AGEINT research-anchor counts by freshness bucket, evidence "
            "tier, and largest source lanes."
        ),
        "renderer": "source_freshness_coverage",
        "source_section": "bibliography-atlas.md",
    },
    {
        "slug": "ageint-analytic-source-quality-boundary",
        "title": "Analytic Tradecraft Source Quality Boundary",
        "caption": (
            "Source-backed evidence-derived chart from local research-anchor metadata showing "
            "official, standards, statutory, postmortem, scholarly evaluation, and "
            "forecasting evidence lanes for analytic-tradecraft claims."
        ),
        "alt_text": (
            "Chart grouping analytic-tradecraft research anchors by source lane, "
            "evidence tier, verification method, and claim boundary."
        ),
        "renderer": "analytic_source_quality_boundary",
        "source_section": "chapter:41",
    },
    {
        "slug": "ageint-pattern-taxonomy",
        "title": "AGEINT Pattern Taxonomy",
        "caption": "The pattern taxonomy groups AGEINT design patterns by safe curriculum role.",
        "alt_text": "Grid visualization of AGEINT design-pattern families.",
        "renderer": "pattern_taxonomy",
        "source_section": "chapter:32",
    },
    {
        "slug": "ageint-safety-boundary-loop",
        "title": "AGEINT Safety Boundary Loop",
        "caption": (
            "Conceptual governance schematic showing how authorization, synthetic "
            "fixtures, human oversight, logging, and non-operational practice stay connected."
        ),
        "alt_text": "Loop diagram showing defensive safety gates around AGEINT practice.",
        "renderer": "safety_boundary_loop",
        "source_section": "orientation.md",
    },
    {
        "slug": "ageint-section-composability-matrix",
        "title": "AGEINT Section Composability Matrix",
        "caption": "The section composability matrix shows which reusable curriculum artifacts support each part.",
        "alt_text": "Matrix of AGEINT parts and reusable artifact types.",
        "renderer": "section_composability_matrix",
        "source_section": "orientation.md",
    },
    {
        "slug": "ageint-reference-coverage",
        "title": "AGEINT Reference Coverage",
        "caption": (
            "Audit table defining heterogeneous count types: parsed source-guide "
            "references, curated research anchors, methods appendices, and named "
            "AGEINT patterns."
        ),
        "alt_text": "Reference coverage table with count type, denominator, source surface, and use.",
        "renderer": "reference_coverage",
        "source_section": "bibliography-atlas.md",
    },
    {
        "slug": "ageint-source-verification-flow",
        "title": "AGEINT Source Verification Flow",
        "caption": "The source-verification workflow connects locked references, v2 source lanes, checked dates, and refresh triggers.",
        "alt_text": "Loop diagram for AGEINT source verification, locking, lane assignment, and refresh.",
        "renderer": "source_verification_flow",
        "source_section": "appendix:h",
    },
    {
        "slug": "ageint-claim-ledger-flow",
        "title": "AGEINT Claim Ledger Flow",
        "caption": "The claim-ledger flow keeps evidence, uncertainty, review ownership, and refresh triggers visible.",
        "alt_text": "Loop diagram showing AGEINT claim ledger evidence flow.",
        "renderer": "claim_ledger_flow",
        "source_section": "appendix:h",
    },
    {
        "slug": "ageint-ai-compliance-map",
        "title": "AGEINT AI Compliance Map",
        "caption": (
            "Conceptual compliance matrix with rows as governance lanes and "
            "columns as source, rights, assurance, artifact, and refresh "
            "obligations; color groups cells only."
        ),
        "alt_text": "Conceptual matrix mapping governance lanes to source, rights, assurance, artifact, and refresh obligations.",
        "renderer": "ai_compliance_map",
        "source_section": "orientation.md",
    },
    {
        "slug": "ageint-agent-evaluation-loop",
        "title": "AGEINT Agent Evaluation Loop",
        "caption": "The agent evaluation loop places assurance, human review, and rollback before reuse.",
        "alt_text": "Loop diagram for AGEINT agent evaluation and assurance.",
        "renderer": "agent_evaluation_loop",
        "source_section": "chapter:34",
    },
    {
        "slug": "ageint-cross-border-data-flow",
        "title": "AGEINT Cross-Border Data Flow",
        "caption": "The cross-border data flow shows how access, metadata, rights, and reuse decisions are governed.",
        "alt_text": "Loop diagram showing cross-border data flow controls for AGEINT.",
        "renderer": "cross_border_data_flow",
        "source_section": "chapter:44",
    },
    {
        "slug": "ageint-capstone-workflow",
        "title": "AGEINT Capstone Workflow",
        "caption": "The capstone workflow moves from an authorized question to debrief and refresh ownership.",
        "alt_text": "Loop diagram of AGEINT capstone phases.",
        "renderer": "capstone_workflow",
        "source_section": "appendix:i",
    },
    {
        "slug": "ageint-safe-substitution-matrix",
        "title": "AGEINT Safe Substitution Matrix",
        "caption": "The safe substitution matrix converts risky motifs into bounded classroom alternatives.",
        "alt_text": "Matrix of AGEINT risky source motifs and safe curriculum substitute categories.",
        "renderer": "safe_substitution_matrix",
        "source_section": "appendix:i",
    },
    {
        "slug": "ageint-instructor-assessment-lifecycle",
        "title": "AGEINT Instructor Assessment Lifecycle",
        "caption": "The instructor lifecycle connects scope, facilitation, scoring, revision, and debrief evidence.",
        "alt_text": "Loop diagram showing AGEINT instructor assessment lifecycle.",
        "renderer": "instructor_assessment_lifecycle",
        "source_section": "appendix:i",
    },
    {
        "slug": "ageint-accessibility-workflow",
        "title": "AGEINT Accessibility Workflow",
        "caption": "The accessibility workflow joins WCAG, UDL, remediation, and refresh evidence.",
        "alt_text": "Loop diagram for AGEINT accessibility and UDL review.",
        "renderer": "accessibility_workflow",
        "source_section": "orientation.md",
    },
    {
        "slug": "ageint-hria-dpia-map",
        "title": "AGEINT HRIA/DPIA Map",
        "caption": "The HRIA/DPIA map separates purpose, affected groups, high-risk triggers, safeguards, and residual risk.",
        "alt_text": "Matrix showing AGEINT human-rights and data-protection impact assessment fields.",
        "renderer": "hria_dpia_map",
        "source_section": "appendix:h",
    },
    {
        "slug": "ageint-procurement-oversight-loop",
        "title": "AGEINT Procurement Oversight Loop",
        "caption": "The procurement oversight loop connects need, transparency, criteria, contract controls, and lifecycle monitoring.",
        "alt_text": "Loop diagram for AGEINT procurement and vendor oversight.",
        "renderer": "procurement_oversight_loop",
        "source_section": "orientation.md",
    },
    {
        "slug": "ageint-agent-incident-lifecycle",
        "title": "AGEINT Agent Incident Lifecycle",
        "caption": "The agent incident lifecycle organizes preparation, detection, containment, recovery, and debrief learning.",
        "alt_text": "Loop diagram for AGEINT agent incident response lifecycle.",
        "renderer": "agent_incident_lifecycle",
        "source_section": "chapter:34",
    },
    {
        "slug": "ageint-bounded-autonomy-recoverability",
        "title": "AGEINT Bounded Autonomy and Recoverability",
        "caption": "The bounded-autonomy view pairs delegated action with approval thresholds, stop conditions, and recovery evidence.",
        "alt_text": "Matrix showing AGEINT bounded autonomy, authority, tool control, logging, and recoverability evidence.",
        "renderer": "bounded_autonomy_recoverability",
        "source_section": "chapter:34",
    },
    {
        "slug": "ageint-public-ai-register-lifecycle",
        "title": "AGEINT Public AI Register Lifecycle",
        "caption": "The public AI register lifecycle keeps use-case purpose, impact review, publication, feedback, and refresh visible.",
        "alt_text": "Loop diagram for AGEINT public AI register and transparency lifecycle.",
        "renderer": "public_ai_register_lifecycle",
        "source_section": "orientation.md",
    },
    {
        "slug": "ageint-ai-incident-reporting-loop",
        "title": "AGEINT AI Incident Reporting Loop",
        "caption": "The AI incident reporting loop turns detection, classification, reporting, remediation, and learning into evidence.",
        "alt_text": "Loop diagram for AGEINT AI incident detection, classification, reporting, remediation, and learning.",
        "renderer": "ai_incident_reporting_loop",
        "source_section": "chapter:34",
    },
    {
        "slug": "ageint-ot-definitive-architecture-record",
        "title": "AGEINT OT Definitive Architecture Record",
        "caption": "The OT architecture record ties assets, communications, owners, change evidence, and review cadence together.",
        "alt_text": "Matrix showing AGEINT OT assets, data flows, remote access, safety boundaries, and architecture evidence.",
        "renderer": "ot_definitive_architecture_record",
        "source_section": "chapter:45",
    },
    {
        "slug": "ageint-data-lineage-registry",
        "title": "AGEINT Data Lineage Registry",
        "caption": "The data lineage registry traces source citations, verified anchors, datasets, transcripts, and final artifacts.",
        "alt_text": "Matrix showing AGEINT data lineage registry objects and quality gates.",
        "renderer": "data_lineage_registry",
        "source_section": "appendix:h",
    },
    {
        "slug": "ageint-assessment-integrity-matrix",
        "title": "AGEINT Assessment Integrity Matrix",
        "caption": "The assessment integrity matrix separates AI-use declarations, reasoning, citations, lab boundaries, and revision evidence.",
        "alt_text": "Matrix showing AGEINT assessment integrity controls.",
        "renderer": "assessment_integrity_matrix",
        "source_section": "appendix:i",
    },
    {
        "slug": "ageint-adversarial-assurance-cycle",
        "title": "AGEINT Adversarial Assurance Cycle",
        "caption": "The adversarial assurance cycle turns misuse cases, control challenges, evidence attacks, incident rehearsal, and remediation into review evidence.",
        "alt_text": "Loop diagram for AGEINT adversarial assurance cycle.",
        "renderer": "adversarial_assurance_cycle",
        "source_section": "chapter:34",
    },
    {
        "slug": "ageint-model-dataset-card",
        "title": "AGEINT Model and Dataset Card",
        "caption": "The model and dataset card keeps purpose, provenance, collection process, evaluation caveats, lifecycle controls, and review ownership visible for model and dataset claims.",
        "alt_text": "Matrix showing AGEINT model-card and dataset-card fields for intended use, provenance, composition limits, evaluation caveats, lifecycle controls, and review gates.",
        "renderer": "model_dataset_card",
        "source_section": "orientation.md",
    },
    {
        "slug": "ageint-agentic-intelligence-boundary",
        "title": "AGEINT Agentic Intelligence Boundary Controls",
        "caption": "The boundary-control matrix shows how purpose, tool permissions, data access, human review, logging, and rollback constrain agentic assistance before any external action can occur.",
        "alt_text": "Matrix showing AGEINT agentic boundary controls across assist, approve, block, and recover states.",
        "renderer": "agentic_intelligence_boundary",
        "source_section": "orientation.md",
    },
    {
        "slug": "ageint-transparency-notice-flow",
        "title": "AGEINT Transparency Notice Flow",
        "caption": "The transparency notice flow links public purpose, tool and data summary, impact review, and publication decisions.",
        "alt_text": "Loop diagram for AGEINT transparency notice preparation.",
        "renderer": "transparency_notice_flow",
        "source_section": "orientation.md",
    },
    {
        "slug": "ageint-records-retention-audit",
        "title": "AGEINT Records Retention Audit",
        "caption": "The records retention audit ties retained records to audit questions, exceptions, and remediation evidence.",
        "alt_text": "Matrix showing AGEINT records retention and audit trail controls.",
        "renderer": "records_retention_audit",
        "source_section": "appendix:h",
    },
    {
        "slug": "ageint-release-change-control",
        "title": "AGEINT Release Change Control",
        "caption": "The release change-control gate checks scope, rights, security, versioning, rollback, monitoring, and retest.",
        "alt_text": "Loop diagram for AGEINT release and change-control gates.",
        "renderer": "release_change_control",
        "source_section": "appendix:i",
    },
    {
        "slug": "ageint-risk-exception-memo",
        "title": "AGEINT Risk Exception Memo",
        "caption": "The risk exception memo keeps exception basis, compensating controls, expiry, and retest evidence together.",
        "alt_text": "Matrix showing AGEINT risk exception and acceptance memo fields.",
        "renderer": "risk_exception_memo",
        "source_section": "appendix:h",
    },
    {
        "slug": "ageint-learner-support-plan",
        "title": "AGEINT Learner Support Plan",
        "caption": "The learner-support plan connects access, cognitive load, assessment fairness, and remediation.",
        "alt_text": "Loop diagram for AGEINT learner support and accommodation planning.",
        "renderer": "learner_support_plan",
        "source_section": "appendix:i",
    },
    {
        "slug": "ageint-instructor-question-bank",
        "title": "AGEINT Instructor Question Bank",
        "caption": "The instructor question bank prompts source, boundary, rights, and assurance challenges.",
        "alt_text": "Matrix showing AGEINT instructor question prompts and evidence.",
        "renderer": "instructor_question_bank",
        "source_section": "appendix:i",
    },
    {
        "slug": "ageint-remediation-backlog",
        "title": "AGEINT Remediation Backlog",
        "caption": "The remediation backlog tracks unverified claims, unsafe phrasing, accessibility defects, and assurance gaps.",
        "alt_text": "Matrix showing AGEINT remediation backlog items, triggers, and closure evidence.",
        "renderer": "remediation_backlog",
        "source_section": "appendix:i",
    },
)

_CONCEPT_PLATES_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "figures" / "concept_plates.jsonl"
)


def _load_concept_plates() -> tuple[dict[str, str], ...]:
    """Load deterministic teaching-plate specifications from JSONL data."""
    if not _CONCEPT_PLATES_PATH.is_file():
        return ()
    rows: list[dict[str, str]] = []
    for line in _CONCEPT_PLATES_PATH.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rows.append(dict(json.loads(line)))
    return tuple(rows)


AI_CONCEPTUAL_PLATES: tuple[dict[str, str], ...] = _load_concept_plates()
