from __future__ import annotations

import hashlib
import math
from pathlib import Path
import textwrap
from typing import Sequence

from curriculum import Curriculum

from ._01_part import FigureSpec
from ._03c_control_matrix import draw_control_matrix, draw_matrix
from ._04_part import _font, _pil_modules
from ._05_visual_style import (
    CANVAS_BG,
    INK,
    MUTED,
    PALETTE,
    SOFT_PALETTE,
    draw_arrow,
    draw_centered_text,
    draw_footer,
    draw_title_band,
    draw_wrapped_text,
)

def _render_source_quality_spine(output: Path, spec: FigureSpec) -> None:
    rows = [
        ("OECD / Canada agentic AI", ("official", "public-sector use", "adoption duty", "policy refresh")),
        ("NIST AI RMF / 600-1", ("standard", "risk frame", "measure/manage", "version check")),
        ("MCP / OAuth / identity", ("protocol", "tool boundary", "auth evidence", "spec refresh")),
        ("ODNI / IC tradecraft", ("official", "analytic claim", "confidence/caveat", "directive check")),
        ("CISA / NCSC secure AI", ("official", "security control", "misuse review", "guidance check")),
        ("Scholarly anchors", ("scholarly", "theory/study", "scope caveat", "literature check")),
    ]
    draw_control_matrix(
        output,
        spec.title,
        rows,
        ("Tier", "Claim role", "Evidence use", "Refresh"),
        "#ccfbf1",
        "#bfdbfe",
    )


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
        (
            "Parsed guide references",
            (
                str(curriculum.stats["references"]),
                "source guide",
                "locked ids",
                "append-only",
            ),
        ),
        (
            "Curated research anchors",
            (
                str(_research_anchor_count()),
                "anchor atlas",
                "direct checks",
                "dated refresh",
            ),
        ),
        (
            "Methods appendices",
            (
                str(curriculum.stats["appendices"]),
                "appendices",
                "student artifacts",
                "build refresh",
            ),
        ),
        (
            "AGEINT patterns",
            (
                str(curriculum.stats["patterns"]),
                "pattern registry",
                "safe translations",
                "safety audit",
            ),
        ),
    ]
    draw_control_matrix(
        output,
        spec.title,
        rows,
        ("Count", "Surface", "Use", "Refresh"),
        "#cffafe",
        "#d9f99d",
    )


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
    try:
        from .intelligence_content import INTELLIGENCE_RESEARCH_ANCHORS
    except ImportError:  # pragma: no cover - direct script imports
        from intelligence_content import INTELLIGENCE_RESEARCH_ANCHORS  # type: ignore[no-redef]

    return len(INTELLIGENCE_RESEARCH_ANCHORS)


def _draw_bar_chart(output: Path, title: str, labels: Sequence[str], values: Sequence[int], color: str) -> None:
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (1600, 1000), CANVAS_BG)
    draw = draw_mod.Draw(canvas)
    label_font = _font(font_mod, 17)
    draw_title_band(
        draw,
        font_mod,
        _font,
        title,
        subtitle="Evidence-derived chart; values are parser counts, not capability scores.",
        accent=color,
    )
    chart = (95, 175, 1505, 835)
    max_value = max(values) or 1
    for step in range(5):
        y = chart[3] - (step / 4) * (chart[3] - chart[1])
        draw.line((chart[0], y, chart[2], y), fill="#dbe3ee", width=1)
        draw.text((45, y - 12), str(round(max_value * step / 4)), fill=MUTED, font=_font(font_mod, 16))
    bar_width = max(5, int((chart[2] - chart[0]) / max(1, len(values)) - 5))
    for index, value in enumerate(values):
        x0 = chart[0] + index * ((chart[2] - chart[0]) / max(1, len(values)))
        x1 = x0 + bar_width
        height = (value / max_value) * (chart[3] - chart[1])
        y0 = chart[3] - height
        draw.rounded_rectangle((x0, y0, x1, chart[3]), radius=5, fill=PALETTE[index % len(PALETTE)])
        if len(values) <= 26 or index % 4 == 0 or value == max_value:
            draw.text((x0, max(chart[1] + 5, y0 - 28)), str(value), fill=INK, font=_font(font_mod, 22))
        # Always show x-axis anchors: for <=20 bars show every label; above that,
        # thin to ~22 evenly-spaced labels (plus the last) so a reader can still
        # locate positions instead of facing an unlabeled wall of bars.
        label_stride = max(1, (len(values) + 21) // 22)
        if index % label_stride == 0 or index == len(values) - 1:
            words = labels[index].split()
            if len(labels[index]) > 18 and len(words) > 1:
                mid = (len(words) + 1) // 2
                draw.text((x0, chart[3] + 12), " ".join(words[:mid]), fill=MUTED, font=label_font)
                draw.text((x0, chart[3] + 34), " ".join(words[mid:]), fill=MUTED, font=label_font)
            else:
                draw.text((x0, chart[3] + 12), labels[index], fill=MUTED, font=label_font)
    draw.line((chart[0], chart[3], chart[2], chart[3]), fill="#334155", width=2)
    draw_footer(draw, font_mod, _font, f"Source: data/curriculum parser | Max value: {max_value}")
    canvas.save(output, format="PNG", optimize=True)


def _draw_ranked_bands(output: Path, title: str, labels: Sequence[str], color: str) -> None:
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (1600, 1000), CANVAS_BG)
    draw = draw_mod.Draw(canvas)
    draw_title_band(draw, font_mod, _font, title, subtitle="Ranked audit bands; order is instructional.", accent=color)
    for index, label in enumerate(labels):
        y = 150 + index * 74
        fill = PALETTE[index % len(PALETTE)]
        draw.rounded_rectangle((80, y, 1520, y + 52), radius=10, fill=fill)
        draw.text((110, y + 12), label, fill="#ffffff", font=_font(font_mod, 25))
    draw_footer(draw, font_mod, _font, "Source: AGEINT renderer | Bands are conceptual groupings.")
    canvas.save(output, format="PNG", optimize=True)


def _draw_tile_grid(output: Path, title: str, labels: Sequence[str], color: str) -> None:
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (1600, 1000), CANVAS_BG)
    draw = draw_mod.Draw(canvas)
    draw_title_band(draw, font_mod, _font, title, subtitle="Conceptual grid; each tile is a safe curriculum role.", accent=color)
    cols = 4
    tile_w = 340
    tile_h = 130
    for index, label in enumerate(labels):
        row, col = divmod(index, cols)
        x = 80 + col * 380
        y = 145 + row * 150
        outline = PALETTE[index % len(PALETTE)]
        fill = SOFT_PALETTE[index % len(SOFT_PALETTE)]
        draw.rounded_rectangle((x, y, x + tile_w, y + tile_h), radius=10, fill=fill, outline=outline, width=4)
        draw.rectangle((x, y, x + 14, y + tile_h), fill=outline)
        draw_wrapped_text(draw, (x + 30, y + 26), label, _font(font_mod, 22), width=24, max_lines=3, line_height=29)
    draw_footer(draw, font_mod, _font, "Source: curriculum pattern registry | Tiles are pedagogical categories.")
    canvas.save(output, format="PNG", optimize=True)


def _draw_loop(output: Path, title: str, steps: Sequence[str]) -> None:
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (1600, 1000), CANVAS_BG)
    draw = draw_mod.Draw(canvas)
    draw_title_band(draw, font_mod, _font, title, subtitle="Governance loop; arrows show review sequence.", accent="#0f766e")
    center = (800, 520)
    radius = 310
    angles = [(2 * math.pi * i / len(steps)) - math.pi / 2 for i in range(len(steps))]
    positions = [(center[0] + math.cos(a) * radius, center[1] + math.sin(a) * radius) for a in angles]
    count = len(positions)
    for index in range(count):
        x1, y1 = positions[index]
        x2, y2 = positions[(index + 1) % count]
        dx, dy = x2 - x1, y2 - y1
        length = math.hypot(dx, dy) or 1.0
        ux, uy = dx / length, dy / length
        sx, sy, ex, ey = x1 + ux * 102, y1 + uy * 102, x2 - ux * 102, y2 - uy * 102
        draw_arrow(draw, (sx, sy), (ex, ey), fill="#334155", width=5)
    for index, step in enumerate(steps):
        x, y = positions[index]
        fill = PALETTE[index % len(PALETTE)]
        box = (x - 108, y - 58, x + 108, y + 58)
        draw.rounded_rectangle(box, radius=36, fill=fill, outline=INK, width=3)
        draw_centered_text(draw, box, step, _font(font_mod, 21), fill="#ffffff", width=17, max_lines=2, line_height=25)
    draw.ellipse((center[0] - 175, center[1] - 175, center[0] + 175, center[1] + 175), outline="#334155", width=8)
    draw_centered_text(
        draw,
        (center[0] - 150, center[1] - 55, center[0] + 150, center[1] + 55),
        "Non-operational review boundary",
        _font(font_mod, 28),
        width=19,
        max_lines=2,
        line_height=34,
    )
    draw_footer(draw, font_mod, _font, "Source: AGEINT renderer | Loop depicts governance sequence, not autonomous action.")
    canvas.save(output, format="PNG", optimize=True)


def _draw_concept_plate(output: Path, title: str, prompt: str, label: str, visual_text: str = "") -> None:
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(f"{title}|{visual_text}|{label}".encode("utf-8")).digest()
    labels = [item.strip() for item in visual_text.split("|") if item.strip()]
    if len(labels) < 5:
        labels = ["Learning claim", "Evidence trace", "Safety boundary", "Human review", "Refresh duty"]
    canvas = image_mod.new("RGB", (1600, 1000), "#0b1220")
    draw = draw_mod.Draw(canvas)
    draw_title_band(
        draw,
        font_mod,
        _font,
        title,
        subtitle="Deterministic teaching plate; prompt retained only in registry provenance.",
        accent=PALETTE[digest[0] % len(PALETTE)],
    )
    cards = [
        (95, 180, 445, 330),
        (625, 180, 975, 330),
        (1155, 180, 1505, 330),
        (315, 610, 665, 760),
        (935, 610, 1285, 760),
    ]
    center_box = (585, 395, 1015, 545)
    for index, box in enumerate(cards):
        fill = SOFT_PALETTE[index % len(SOFT_PALETTE)]
        outline = PALETTE[(index + digest[index]) % len(PALETTE)]
        draw.rounded_rectangle(box, radius=18, fill=fill, outline=outline, width=5)
        x0, y0, x1, y1 = box
        draw.ellipse((x0 + 22, y0 + 22, x0 + 64, y0 + 64), fill=outline)
        draw_centered_text(draw, (x0 + 72, y0 + 18, x1 - 24, y1 - 18), labels[index], _font(font_mod, 26))
    draw.rounded_rectangle(center_box, radius=22, fill="#ffffff", outline="#94a3b8", width=5)
    draw_centered_text(draw, center_box, "Reviewable local record", _font(font_mod, 30), width=22, max_lines=2, line_height=34)
    for box in cards[:3]:
        draw_arrow(draw, ((box[0] + box[2]) / 2, box[3] + 10), (800, center_box[1] - 10), fill="#93c5fd", width=5)
    for box in cards[3:]:
        draw_arrow(draw, (800, center_box[3] + 10), ((box[0] + box[2]) / 2, box[1] - 10), fill="#99f6e4", width=5)
    boundary = (140, 805, 1460, 890)
    draw.rounded_rectangle(boundary, radius=16, fill="#fef3c7", outline="#b45309", width=4)
    draw_centered_text(
        draw,
        boundary,
        "Safety boundary: synthetic, defensive, no real people or targets",
        _font(font_mod, 26),
        width=64,
        max_lines=1,
    )
    draw_footer(draw, font_mod, _font, f"Provenance: local deterministic renderer | Label: {label}", width=1600)
    canvas.save(output, format="PNG", optimize=True)


def _draw_text_plate(output: Path, title: str, body: str) -> None:
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (1400, 900), CANVAS_BG)
    draw = draw_mod.Draw(canvas)
    draw_title_band(draw, font_mod, _font, title, subtitle="Deterministic fallback plate.", width=1400, accent="#64748b")
    for idx, line in enumerate(textwrap.wrap(body, width=80)):
        draw.text((60, 155 + idx * 34), line, fill=MUTED, font=_font(font_mod, 24))
    draw_footer(draw, font_mod, _font, "Source: local fallback renderer | Replace with real asset in strict builds.", width=1400, y=820)
    canvas.save(output, format="PNG", optimize=True)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()
