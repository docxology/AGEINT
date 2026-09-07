from __future__ import annotations

from pathlib import Path

from curriculum import Curriculum

from ._01_part import FigureSpec
from ._03c_control_matrix import draw_control_matrix, draw_matrix
from ._03s_drawers import _draw_loop, _draw_tile_grid


def _render_source_quality_spine(output: Path, spec: FigureSpec) -> None:
    rows = [
        ("OECD / Canada agentic AI", ("official", "public-sector use", "adoption duty", "policy refresh")),
        ("NIST AI RMF / 600-1", ("standard", "risk frame", "measure/manage", "version check")),
        ("MCP / OAuth / identity", ("protocol", "tool boundary", "auth evidence", "spec refresh")),
        ("ODNI / IC tradecraft", ("official", "analytic claim", "confidence/caveat", "directive check")),
        ("CISA / NCSC secure AI", ("official", "security control", "misuse review", "guidance check")),
        ("Scholarly anchors", ("scholarly", "theory/study", "scope caveat", "literature check")),
    ]
    draw_control_matrix(output, spec.title, rows, ("Tier", "Claim role", "Evidence use", "Refresh"), "#ccfbf1", "#bfdbfe")


def _render_pattern_taxonomy(output: Path, curriculum: Curriculum, spec: FigureSpec) -> None:
    names = [pattern["name"] for pattern in curriculum.patterns]
    _draw_tile_grid(output, spec.title, names, "#7c3aed")


def _render_safety_boundary_loop(output: Path, spec: FigureSpec) -> None:
    steps = ["Authorize", "Synthetic", "Defensive", "Human review", "Log", "Rollback"]
    _draw_loop(output, spec.title, steps)


def _render_section_composability_matrix(output: Path, curriculum: Curriculum, spec: FigureSpec) -> None:
    rows = [part["title"] for part in curriculum.parts]
    cols = ["Atlas", "Course", "Textbook", "Cookbook", "Playbook", "Rubric"]
    draw_matrix(output, spec.title, rows, cols)


def _render_reference_coverage(output: Path, curriculum: Curriculum, spec: FigureSpec) -> None:
    rows = [
        ("Parsed guide references", (str(curriculum.stats["references"]), "source guide", "locked ids", "append-only")),
        ("Curated research anchors", (str(_research_anchor_count()), "anchor atlas", "direct checks", "dated refresh")),
        ("Methods appendices", (str(curriculum.stats["appendices"]), "appendices", "student artifacts", "build refresh")),
        ("AGEINT patterns", (str(curriculum.stats["patterns"]), "pattern registry", "safe translations", "safety audit")),
    ]
    draw_control_matrix(output, spec.title, rows, ("Count", "Surface", "Use", "Refresh"), "#cffafe", "#d9f99d")


def _render_source_verification_flow(output: Path, spec: FigureSpec) -> None:
    steps = ["Parse guide", "Lock IDs", "Verify URL", "Assign lane", "Write BibTeX", "Refresh"]
    _draw_loop(output, spec.title, steps)


def _render_claim_ledger_flow(output: Path, spec: FigureSpec) -> None:
    steps = ["Claim", "Evidence", "Caveat", "Reviewer", "Decision", "Refresh"]
    _draw_loop(output, spec.title, steps)


def _render_ai_compliance_map(output: Path, spec: FigureSpec) -> None:
    rows = [
        ("AI compliance", ("AI RMF", "impact duty", "risk evidence", "card", "policy")),
        ("Education", ("UNESCO/UDL", "access", "integrity", "rubric", "course")),
        ("Public sector", ("Canada/OECD", "notice", "owner", "register", "law")),
        ("Data spaces", ("EU/W3C", "reuse", "lineage", "metadata", "spec")),
        ("Human rights", ("HRIA/DPIA", "redress", "review", "memo", "case")),
        ("Interoperability", ("MCP/A2A", "identity", "tool gate", "run log", "version")),
        ("Workforce", ("skills", "support", "role map", "plan", "debrief")),
        ("Provenance", ("PROV/cards", "transparency", "audit", "dataset", "source")),
    ]
    cols = ["Source", "Rights", "Assure", "Artifact", "Refresh"]
    draw_control_matrix(output, spec.title, rows, cols, "#bfdbfe", "#dcfce7")


def _render_agent_evaluation_loop(output: Path, spec: FigureSpec) -> None:
    steps = ["Scope", "Fixture", "Run", "Measure", "Review", "Rollback"]
    _draw_loop(output, spec.title, steps)


def _render_cross_border_data_flow(output: Path, spec: FigureSpec) -> None:
    steps = ["Origin", "Access", "Metadata", "Rights", "Reuse", "Audit"]
    _draw_loop(output, spec.title, steps)


def _render_capstone_workflow(output: Path, spec: FigureSpec) -> None:
    steps = ["Question", "Sources", "Ledger", "Lab", "Rubric", "Debrief"]
    _draw_loop(output, spec.title, steps)


def _render_safe_substitution_matrix(output: Path, spec: FigureSpec) -> None:
    rows = ["Patterns", "OSINT", "GEOINT", "SOC/CTI", "HUMINT/CI", "Cognitive", "ICS/OT"]
    cols = ["Tabletop", "Audit", "Provenance", "Govern", "Debrief"]
    draw_matrix(output, spec.title, rows, cols)


def _render_instructor_assessment_lifecycle(output: Path, spec: FigureSpec) -> None:
    steps = ["Scope", "Facilitate", "Score", "Revise", "Approve", "Refresh"]
    _draw_loop(output, spec.title, steps)


def _render_accessibility_workflow(output: Path, spec: FigureSpec) -> None:
    steps = ["Baseline", "UDL", "Assistive tech", "Public duty", "Remediate", "Retest"]
    _draw_loop(output, spec.title, steps)


def _render_hria_dpia_map(output: Path, spec: FigureSpec) -> None:
    rows = ["Purpose", "Affected groups", "High-risk trigger", "Safeguards", "Residual risk"]
    cols = ["Prompt", "Evidence", "Owner", "Review", "Refresh"]
    draw_matrix(output, spec.title, rows, cols)


def _render_procurement_oversight_loop(output: Path, spec: FigureSpec) -> None:
    steps = ["Need", "Vendor facts", "Criteria", "Contract", "Monitor", "Renew"]
    _draw_loop(output, spec.title, steps)


def _render_agent_incident_lifecycle(output: Path, spec: FigureSpec) -> None:
    steps = ["Prepare", "Detect", "Contain", "Recover", "Debrief", "Update"]
    _draw_loop(output, spec.title, steps)


def _render_bounded_autonomy_recoverability(output: Path, spec: FigureSpec) -> None:
    rows = ["Authority", "Allowed tools", "Human gate", "Stop rule", "Recovery"]
    cols = ["Assist", "Supervise", "Escalate", "Block"]
    draw_matrix(output, spec.title, rows, cols)


def _render_public_ai_register_lifecycle(output: Path, spec: FigureSpec) -> None:
    steps = ["Use case", "Impact", "Approve", "Publish", "Feedback", "Refresh"]
    _draw_loop(output, spec.title, steps)


def _render_ai_incident_reporting_loop(output: Path, spec: FigureSpec) -> None:
    steps = ["Detect", "Triage", "Classify", "Report", "Remediate", "Learn"]
    _draw_loop(output, spec.title, steps)


def _render_ot_definitive_architecture_record(output: Path, spec: FigureSpec) -> None:
    rows = ["Assets", "Data flows", "Remote access", "Safety boundary", "Vendor support"]
    cols = ["Owner", "Evidence", "Change", "Review"]
    draw_matrix(output, spec.title, rows, cols)


def _render_data_lineage_registry(output: Path, spec: FigureSpec) -> None:
    rows = ["Citation", "Anchor", "Dataset", "Transcript", "Artifact"]
    cols = ["Origin", "Transform", "Reviewer", "Retention", "Gate"]
    draw_matrix(output, spec.title, rows, cols)


def _render_assessment_integrity_matrix(output: Path, spec: FigureSpec) -> None:
    rows = ["AI use", "Reasoning", "Citations", "Lab boundary", "Revision"]
    cols = ["Student", "Instructor", "Evidence", "Risk", "Disposition"]
    draw_matrix(output, spec.title, rows, cols)


def _render_adversarial_assurance_cycle(output: Path, spec: FigureSpec) -> None:
    steps = ["Misuse case", "Challenge", "Attack evidence", "Rehearse", "Remediate", "Retest"]
    _draw_loop(output, spec.title, steps)


def _render_model_dataset_card(output: Path, spec: FigureSpec) -> None:
    cols = ["Model card", "Dataset card", "Caveats", "Owner", "Refresh"]
    rows = [
        ("Intended use", ("task scope", "purpose and reuse", "excluded use", "reviewer", "scope change")),
        ("Provenance", ("model version", "upstream source", "authority/license", "steward", "source update")),
        ("Collection", ("deployment context", "collection method", "consent basis", "data owner", "new inputs")),
        ("Composition", ("capability limits", "sampling frame", "coverage gaps", "dataset creator", "drift signal")),
        ("Evaluation", ("benchmarks/tests", "quality checks", "subgroup caveats", "assurance lead", "new test")),
        ("Failure modes", ("known failures", "bias review", "red-team notes", "risk owner", "incident")),
        ("Lifecycle", ("release/rollback", "retention/delete", "monitoring", "update owner", "review date")),
    ]
    draw_control_matrix(output, spec.title, rows, cols, "#dbeafe", "#dcfce7")


def _render_agentic_intelligence_boundary(output: Path, spec: FigureSpec) -> None:
    cols = ["Assist", "Approve", "Block", "Recover"]
    rows = [
        ("Purpose", ("learning task", "authority match", "out-of-scope use", "re-scope memo")),
        ("Tool allowlist", ("read-only tools", "signed approval", "unknown tool", "revocation log")),
        ("Data boundary", ("public/synthetic", "licensed input", "private/live data", "minimize/delete")),
        ("Human gate", ("draft support", "review decision", "irreversible act", "escalation path")),
        ("Audit log", ("prompt/run card", "evidence retained", "missing trace", "reconstruct path")),
        ("Stop/rollback", ("budget check", "release gate", "unsafe drift", "restore/debrief")),
    ]
    draw_control_matrix(output, spec.title, rows, cols, "#ede9fe", "#ccfbf1")


def _render_transparency_notice_flow(output: Path, spec: FigureSpec) -> None:
    steps = ["Purpose", "Tool summary", "Impact", "Review", "Publish", "Refresh"]
    _draw_loop(output, spec.title, steps)


def _render_records_retention_audit(output: Path, spec: FigureSpec) -> None:
    rows = ["Sources", "Prompts", "Decisions", "Exceptions", "Incidents", "Artifacts"]
    cols = ["Owner", "Retain", "Limit", "Audit", "Delete"]
    draw_matrix(output, spec.title, rows, cols)


def _render_release_change_control(output: Path, spec: FigureSpec) -> None:
    steps = ["Scope", "Rights", "Version", "Rollback", "Monitor", "Retest"]
    _draw_loop(output, spec.title, steps)


def _render_risk_exception_memo(output: Path, spec: FigureSpec) -> None:
    rows = ["Exception", "Risk basis", "Control", "Expiry"]
    cols = ["Evidence", "Owner", "Decision", "Retest"]
    draw_matrix(output, spec.title, rows, cols)


def _render_learner_support_plan(output: Path, spec: FigureSpec) -> None:
    steps = ["Access", "Load", "Fairness", "Feedback", "Remediate", "Retest"]
    _draw_loop(output, spec.title, steps)


def _render_instructor_question_bank(output: Path, spec: FigureSpec) -> None:
    rows = ["Source", "Boundary", "Rights", "Assurance"]
    cols = ["Prompt", "Evidence", "Revision", "Disposition"]
    draw_matrix(output, spec.title, rows, cols)


def _render_remediation_backlog(output: Path, spec: FigureSpec) -> None:
    rows = ["Claim", "Safety", "Access", "Assurance"]
    cols = ["Trigger", "Owner", "Due", "Evidence", "Closed"]
    draw_matrix(output, spec.title, rows, cols)


def _research_anchor_count() -> int:
    from intelligence_content import INTELLIGENCE_RESEARCH_ANCHORS

    return len(INTELLIGENCE_RESEARCH_ANCHORS)
