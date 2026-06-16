"""Reusable audit contracts for AGEINT evidence and readiness reports."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class AuditContract:
    """One fail-closed audit surface and its negative-control obligation."""

    contract_id: str
    check_id: str
    title: str
    report_paths: tuple[str, ...]
    purpose: str
    negative_control: str
    publication_readiness_gate: bool = False

    def as_dict(self) -> dict[str, Any]:
        return {
            "contract_id": self.contract_id,
            "check_id": self.check_id,
            "title": self.title,
            "report_paths": list(self.report_paths),
            "purpose": self.purpose,
            "negative_control": self.negative_control,
            "publication_readiness_gate": self.publication_readiness_gate,
        }


AUDIT_CONTRACTS: tuple[AuditContract, ...] = (
    AuditContract(
        contract_id="generated_output_freshness",
        check_id="generated_output_fresh",
        title="Generated output freshness",
        report_paths=("output/reports/current_artifact_evidence.json",),
        purpose="Prove source inputs are not newer than core generated output sentinels.",
        negative_control="Touch a source-owned route, template, or figure file after build; the evidence manifest must fail freshness.",
        publication_readiness_gate=True,
    ),
    AuditContract(
        contract_id="rendered_reference_resolution",
        check_id="rendered_references_resolve",
        title="Rendered reference resolution",
        report_paths=("output/reports/current_artifact_evidence.json",),
        purpose="Reject unresolved rendered references and local Markdown targets in generated artifacts.",
        negative_control="Insert a generated link to a local .md or .markdown target; rendered-reference evidence must fail.",
        publication_readiness_gate=True,
    ),
    AuditContract(
        contract_id="reference_quality",
        check_id="reference_quality_ok",
        title="Reference quality",
        report_paths=("output/reports/reference_quality.json", "output/reports/reference_quality.md"),
        purpose="Reject generic headings, raw citation-key cells, weak cross-links, and citation-only table rows.",
        negative_control="Restore a generic generated scaffold heading, incomplete lesson cross-link, or citation-only table row.",
        publication_readiness_gate=True,
    ),
    AuditContract(
        contract_id="stale_output_scan",
        check_id="stale_output_scans_clean",
        title="Stale output scan",
        report_paths=("output/reports/current_artifact_evidence.json",),
        purpose="Catch known stale strings that previously certified outdated rendered output.",
        negative_control="Restore the old source-section coverage table header or stale scholarly source phrase.",
        publication_readiness_gate=True,
    ),
    AuditContract(
        contract_id="pdf_quality",
        check_id="pdf_quality_ok",
        title="PDF quality",
        report_paths=("output/reports/current_artifact_evidence.json", "output/reports/pdf_quality.json"),
        purpose="Reject stale PDFs, bad PDF links, and unsafe annotation targets.",
        negative_control="Make the PDF older than the combined manuscript or add a file: PDF target.",
        publication_readiness_gate=True,
    ),
    AuditContract(
        contract_id="figure_quality",
        check_id="figure_quality_ok",
        title="Figure quality",
        report_paths=("output/figures/visual_quality_audit.json",),
        purpose="Require readable, square-normalized visual assets with caption, alt text, long description, and provenance.",
        negative_control="Remove figure alt text, provenance, or readable PNG metadata from a registered figure.",
        publication_readiness_gate=True,
    ),
    AuditContract(
        contract_id="citation_source_section_coverage",
        check_id="citation_source_sections_covered",
        title="Citation source-section coverage",
        report_paths=("output/reports/current_artifact_evidence.json",),
        purpose="Require source sections to retain at least one supporting citation.",
        negative_control="Collapse a source section to zero citations while retaining claim-bearing text.",
    ),
    AuditContract(
        contract_id="scholarship_quality",
        check_id="scholarship_quality_ok",
        title="Scholarship quality",
        report_paths=("output/reports/scholarship_quality.json", "output/reports/scholarship_quality.md"),
        purpose="Keep claim-bearing manuscript sections triangulated and method-boundary terms present.",
        negative_control="Remove the SAT figure reference, analysis-validation matrix reference, or one required claim class from orientation prose.",
        publication_readiness_gate=True,
    ),
    AuditContract(
        contract_id="source_metadata",
        check_id="source_metadata_ok",
        title="Source metadata explicitness",
        report_paths=("output/reports/source_metadata.json", "output/reports/source_metadata.md"),
        purpose="Require every source-anchor row to carry explicit lane, tier, checked-date, and refresh metadata.",
        negative_control="Add one curated source-anchor row with an empty source_lane or source_tier.",
        publication_readiness_gate=True,
    ),
    AuditContract(
        contract_id="source_refresh_due",
        check_id="source_refresh_due_ok",
        title="Source refresh due",
        report_paths=("output/reports/source_refresh_due.json", "output/reports/source_refresh_due.md"),
        purpose="Reject stale or undated source anchors before local readiness is certified.",
        negative_control="Set checked_as_of blank or past the allowed cadence for one source row.",
        publication_readiness_gate=True,
    ),
    AuditContract(
        contract_id="agency_source_coverage",
        check_id="agency_source_coverage_ok",
        title="Agency source coverage",
        report_paths=("output/reports/agency_source_coverage.json", "output/reports/agency_source_coverage.md"),
        purpose="Require new official US IC anchors to carry agency, pack, lane, tier, and deterministic profile routing.",
        negative_control="Add a new official US IC anchor without source_agency, source_pack, or pack routing.",
        publication_readiness_gate=True,
    ),
    AuditContract(
        contract_id="claim_calibration",
        check_id="claim_calibration_ok",
        title="Claim calibration",
        report_paths=("output/reports/claim_calibration.json", "output/reports/claim_calibration.md"),
        purpose="Reject unsupported proof, p-value, measured-performance, and weak-source-only high-risk claims.",
        negative_control="Add an unsupported measured-performance, p-value, or proof-language claim backed only by weak context.",
        publication_readiness_gate=True,
    ),
)


def audit_contracts() -> tuple[AuditContract, ...]:
    """Return all AGEINT audit contracts in evidence-report order."""
    return AUDIT_CONTRACTS


def audit_contract_by_check_id() -> dict[str, AuditContract]:
    """Return audit contracts keyed by evidence ``checks`` id."""
    return {contract.check_id: contract for contract in AUDIT_CONTRACTS}


def publication_readiness_audit_check_ids() -> tuple[str, ...]:
    """Return artifact-evidence check ids that publication readiness must surface."""
    return tuple(
        contract.check_id
        for contract in AUDIT_CONTRACTS
        if contract.publication_readiness_gate
        and contract.check_id
        not in {
            "generated_output_fresh",
            "stale_output_scans_clean",
            "citation_source_sections_covered",
        }
    )


def false_certification_control() -> dict[str, Any]:
    """Return an aggregate false-certification scenario derived from contracts."""
    return {
        "scenario": (
            "A reviewer trusts a copied PDF, citation count, current-evidence note, or green local report "
            "without proving that all registered audits passed against the same rebuilt artifact set."
        ),
        "negative_control": " ".join(contract.negative_control for contract in AUDIT_CONTRACTS),
        "audit_contracts": [contract.as_dict() for contract in AUDIT_CONTRACTS],
    }


def audit_contract_report() -> dict[str, Any]:
    """Return machine-readable audit contract metadata."""
    return {
        "schema_version": "1.0",
        "contract_count": len(AUDIT_CONTRACTS),
        "contracts": [contract.as_dict() for contract in AUDIT_CONTRACTS],
    }


__all__ = [
    "AUDIT_CONTRACTS",
    "AuditContract",
    "audit_contract_by_check_id",
    "audit_contract_report",
    "audit_contracts",
    "false_certification_control",
    "publication_readiness_audit_check_ids",
]
