"""Mermaid diagram-type contracts for AGEINT figure rendering."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True)
class MermaidDiagramTypeContract:
    """One supported Mermaid diagram type and its reader-facing contract."""

    diagram_type: str
    purpose: str
    source_prefix: str
    requires_reader_detail: bool = False
    init_block: str = ""

    def as_dict(self) -> dict[str, Any]:
        return {
            "diagram_type": self.diagram_type,
            "purpose": self.purpose,
            "source_prefix": self.source_prefix,
            "requires_reader_detail": self.requires_reader_detail,
        }


_FLOWCHART_INIT = (
    "%%{init: {"
    "'theme':'neutral',"
    "'themeVariables':{'fontSize':'18px','fontFamily':'Arial, sans-serif',"
    "'primaryColor':'#dbeafe','primaryBorderColor':'#475569',"
    "'primaryTextColor':'#0f172a','lineColor':'#475569',"
    "'secondaryColor':'#dcfce7','tertiaryColor':'#fef3c7'},"
    "'flowchart':{'htmlLabels':true,'nodeSpacing':38,'rankSpacing':46,'curve':'basis',"
    "'subGraphTitleMargin':{'top':8,'bottom':12}}"
    "}}%%\n"
)

_GENERIC_INIT = (
    "%%{init: {"
    "'theme':'neutral',"
    "'themeVariables':{'fontSize':'18px','fontFamily':'Arial, sans-serif',"
    "'primaryColor':'#dbeafe','primaryBorderColor':'#475569',"
    "'primaryTextColor':'#0f172a','lineColor':'#475569',"
    "'secondaryColor':'#dcfce7','tertiaryColor':'#fef3c7'}"
    "}}%%\n"
)

MERMAID_DIAGRAM_TYPE_CONTRACTS: tuple[MermaidDiagramTypeContract, ...] = (
    MermaidDiagramTypeContract(
        diagram_type="flowchart",
        purpose="Structural maps, routing diagrams, and governance boundary flows.",
        source_prefix="flowchart",
        init_block=_FLOWCHART_INIT,
    ),
    MermaidDiagramTypeContract(
        diagram_type="stateDiagram-v2",
        purpose="State, recovery, and circuit-breaker transitions.",
        source_prefix="stateDiagram-v2",
        requires_reader_detail=True,
        init_block=_GENERIC_INIT,
    ),
    MermaidDiagramTypeContract(
        diagram_type="sequenceDiagram",
        purpose="Actor interactions, evidence handoffs, and verification exchanges.",
        source_prefix="sequenceDiagram",
        requires_reader_detail=True,
        init_block=_GENERIC_INIT,
    ),
    MermaidDiagramTypeContract(
        diagram_type="journey",
        purpose="Reviewer and learner experience paths across staged work.",
        source_prefix="journey",
        requires_reader_detail=True,
        init_block=_GENERIC_INIT,
    ),
    MermaidDiagramTypeContract(
        diagram_type="timeline",
        purpose="Temporal degradation, incident, and refresh sequences.",
        source_prefix="timeline",
        requires_reader_detail=True,
        init_block=_GENERIC_INIT,
    ),
    MermaidDiagramTypeContract(
        diagram_type="quadrantChart",
        purpose="Two-axis evidence-fit and claim-risk classification maps.",
        source_prefix="quadrantChart",
        requires_reader_detail=True,
        init_block=_GENERIC_INIT,
    ),
)


def mermaid_type_contracts() -> tuple[MermaidDiagramTypeContract, ...]:
    """Return supported Mermaid diagram-type contracts."""
    return MERMAID_DIAGRAM_TYPE_CONTRACTS


def mermaid_type_contract(diagram_type: str) -> MermaidDiagramTypeContract:
    """Return one supported Mermaid diagram-type contract."""
    for contract in MERMAID_DIAGRAM_TYPE_CONTRACTS:
        if contract.diagram_type == diagram_type:
            return contract
    raise ValueError(f"Unsupported AGEINT Mermaid diagram type: {diagram_type}")


def validate_mermaid_source_contract(diagram_type: str, source: str, reader_detail: str = "") -> None:
    """Validate source prefix and reader-detail requirements for a Mermaid diagram."""
    contract = mermaid_type_contract(diagram_type)
    stripped = source.lstrip()
    if stripped.startswith("%%{init"):
        after_init = stripped.split("%%", 2)[-1].lstrip()
    else:
        after_init = stripped
    if not after_init.startswith(contract.source_prefix):
        raise ValueError(
            f"Mermaid diagram type {diagram_type} must start with {contract.source_prefix!r}"
        )
    if contract.requires_reader_detail and len(reader_detail.split()) < 12:
        raise ValueError(f"Mermaid diagram type {diagram_type} requires informative reader_detail")


def mermaid_contract_report() -> dict[str, Any]:
    """Return machine-readable Mermaid diagram-type support metadata."""
    return {
        "schema_version": "1.0",
        "diagram_type_count": len(MERMAID_DIAGRAM_TYPE_CONTRACTS),
        "diagram_types": [contract.as_dict() for contract in MERMAID_DIAGRAM_TYPE_CONTRACTS],
    }


__all__ = [
    "MERMAID_DIAGRAM_TYPE_CONTRACTS",
    "MermaidDiagramTypeContract",
    "mermaid_contract_report",
    "mermaid_type_contract",
    "mermaid_type_contracts",
    "validate_mermaid_source_contract",
]
