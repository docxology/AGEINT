"""AGEINT orchestration contract audit report."""

from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
from typing import Any

from audit_contracts import audit_contract_report
from figures.mermaid_contracts import mermaid_contract_report
from intelligence_content.source_packs import source_pack_contract_report
from orchestration_contracts import pipeline_contract_report, render_pipeline_contract_markdown


def collect_orchestration_contract(project_root: Path) -> dict[str, Any]:
    """Collect stage, audit, source-pack, and Mermaid contract metadata."""
    root = Path(project_root)
    source_keys = _known_source_keys(root)
    pipeline = pipeline_contract_report(root)
    source_packs = source_pack_contract_report(root, known_source_keys=source_keys)
    payload = {
        "project": "AGEINT",
        "schema_version": "1.0",
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "pipeline": pipeline,
        "audits": audit_contract_report(),
        "source_packs": source_packs,
        "mermaid": mermaid_contract_report(),
    }
    payload["ok"] = (
        not pipeline["missing_output_sentinels"]
        and source_packs["issue_count"] == 0
        and payload["audits"]["contract_count"] > 0
        and payload["mermaid"]["diagram_type_count"] >= 6
    )
    return payload


def write_orchestration_contract(project_root: Path) -> tuple[Path, Path, dict[str, Any]]:
    """Write orchestration contract JSON and Markdown reports."""
    root = Path(project_root)
    payload = collect_orchestration_contract(root)
    reports = root / "output" / "reports"
    reports.mkdir(parents=True, exist_ok=True)
    json_path = reports / "orchestration_contract.json"
    md_path = reports / "orchestration_contract.md"
    json_path.write_text(json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    md_path.write_text(render_orchestration_contract_markdown(payload), encoding="utf-8")
    return json_path, md_path, payload


def render_orchestration_contract_markdown(payload: dict[str, Any]) -> str:
    """Render the orchestration contract as an operator-facing Markdown report."""
    lines = [
        "# AGEINT Contract Map",
        "",
        "| Measure | Value |",
        "|---|---:|",
        f"| OK | {str(payload['ok']).lower()} |",
        f"| Pipeline stages | {payload['pipeline']['stage_count']} |",
        f"| Audit contracts | {payload['audits']['contract_count']} |",
        f"| Source-pack registries | {payload['source_packs']['registry_count']} |",
        f"| Source-pack issues | {payload['source_packs']['issue_count']} |",
        f"| Mermaid diagram types | {payload['mermaid']['diagram_type_count']} |",
        "",
        "## Pipeline Contract",
        "",
        render_pipeline_contract_markdown(payload["pipeline"]).strip(),
        "",
        "## Audit Contracts",
        "",
        "| Contract | Check | Reports | Negative control |",
        "|---|---|---|---|",
    ]
    for contract in payload["audits"]["contracts"]:
        reports = ", ".join(f"`{path}`" for path in contract["report_paths"])
        lines.append(
            f"| `{contract['contract_id']}` | `{contract['check_id']}` | {reports} | {contract['negative_control']} |"
        )
    lines.extend(["", "## Source-Pack Contracts", "", "| Class | Packs | Routes | Issues |", "|---|---:|---:|---:|"])
    for registry in payload["source_packs"]["registries"]:
        class_issues = [
            issue
            for issue in payload["source_packs"]["issues"]
            if issue["source_class"] == registry["source_class"]
        ]
        lines.append(
            f"| `{registry['source_class']}` | {registry['pack_count']} | {registry['profile_route_count']} | {len(class_issues)} |"
        )
    lines.extend(["", "## Mermaid Diagram Types", "", "| Type | Purpose | Reader detail required |", "|---|---|---:|"])
    for diagram_type in payload["mermaid"]["diagram_types"]:
        lines.append(
            f"| `{diagram_type['diagram_type']}` | {diagram_type['purpose']} | {str(diagram_type['requires_reader_detail']).lower()} |"
        )
    return "\n".join(lines) + "\n"


def _known_source_keys(project_root: Path) -> set[str]:
    keys: set[str] = set()
    data_dir = project_root / "data" / "research_anchors"
    for path in sorted(data_dir.glob("*.jsonl")):
        if path.name != "source-quality-anchors.jsonl" and not path.name.startswith("intelligence-anchors-"):
            continue
        for line in path.read_text(encoding="utf-8").splitlines():
            if not line.strip():
                continue
            row = json.loads(line)
            key = str(row.get("key") or "")
            if key:
                keys.add(key)
    return keys


__all__ = [
    "collect_orchestration_contract",
    "render_orchestration_contract_markdown",
    "write_orchestration_contract",
]
