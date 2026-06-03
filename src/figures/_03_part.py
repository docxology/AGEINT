from __future__ import annotations

import hashlib
from importlib import import_module
import math
from pathlib import Path
import re
import textwrap
import urllib.error
import urllib.request
from typing import Any, Sequence, cast

from ._01_part import FigureSpec

def _render_source_quality_spine(output: Path, spec: FigureSpec) -> None:
    anchors = [
        "OECD agentic AI",
        "NIST AI RMF",
        "NIST AI 600-1",
        "NSA MCP",
        "NIST OT",
        "ISA/IEC 62443",
        "ODNI ICD 203",
        "EU AI Act",
        "CISA influence",
        "NATO CIT",
    ]
    _draw_ranked_bands(output, spec.title, anchors, "#0f766e")


def _render_pattern_taxonomy(output: Path, curriculum: Curriculum, spec: FigureSpec) -> None:
    names = [pattern["name"] for pattern in curriculum.patterns]
    _draw_tile_grid(output, spec.title, names, "#7c3aed")


def _render_safety_boundary_loop(output: Path, spec: FigureSpec) -> None:
    steps = ["Authorize", "Synthetic", "Defensive", "Human review", "Log", "Rollback"]
    _draw_loop(output, spec.title, steps)


def _render_section_composability_matrix(output: Path, curriculum: Curriculum, spec: FigureSpec) -> None:
    rows = [part["title"] for part in curriculum.parts]
    cols = ["Atlas", "Course", "Textbook", "Cookbook", "Playbook", "Rubric"]
    _draw_matrix(output, spec.title, rows, cols)


def _render_reference_coverage(output: Path, curriculum: Curriculum, spec: FigureSpec) -> None:
    labels = ["Parsed guide references", "Official anchors", "Methods appendices", "AGEINT patterns"]
    values = [
        curriculum.stats["references"],
        _research_anchor_count(),
        curriculum.stats["appendices"],
        curriculum.stats["patterns"],
    ]
    _draw_bar_chart(output, spec.title, labels, values, "#0891b2")


def _render_source_verification_flow(output: Path, spec: FigureSpec) -> None:
    steps = ["Parse guide", "Lock IDs", "Verify URL", "Assign lane", "Write BibTeX", "Refresh"]
    _draw_loop(output, spec.title, steps)


def _render_claim_ledger_flow(output: Path, spec: FigureSpec) -> None:
    steps = ["Claim", "Evidence", "Caveat", "Reviewer", "Decision", "Refresh"]
    _draw_loop(output, spec.title, steps)


def _render_ai_compliance_map(output: Path, spec: FigureSpec) -> None:
    rows = [
        "AI compliance",
        "Education",
        "Public sector",
        "Data spaces",
        "Human rights",
        "Interoperability",
        "Workforce",
        "Provenance",
    ]
    cols = ["Source", "Rights", "Assure", "Artifact", "Refresh"]
    _draw_matrix(output, spec.title, rows, cols)


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
    _draw_matrix(output, spec.title, rows, cols)


def _render_instructor_assessment_lifecycle(output: Path, spec: FigureSpec) -> None:
    steps = ["Scope", "Facilitate", "Score", "Revise", "Approve", "Refresh"]
    _draw_loop(output, spec.title, steps)


def _render_accessibility_workflow(output: Path, spec: FigureSpec) -> None:
    steps = ["Baseline", "UDL", "Assistive tech", "Public duty", "Remediate", "Retest"]
    _draw_loop(output, spec.title, steps)


def _render_hria_dpia_map(output: Path, spec: FigureSpec) -> None:
    rows = ["Purpose", "Affected groups", "High-risk trigger", "Safeguards", "Residual risk"]
    cols = ["Prompt", "Evidence", "Owner", "Review", "Refresh"]
    _draw_matrix(output, spec.title, rows, cols)


def _render_procurement_oversight_loop(output: Path, spec: FigureSpec) -> None:
    steps = ["Need", "Vendor facts", "Criteria", "Contract", "Monitor", "Renew"]
    _draw_loop(output, spec.title, steps)


def _render_agent_incident_lifecycle(output: Path, spec: FigureSpec) -> None:
    steps = ["Prepare", "Detect", "Contain", "Recover", "Debrief", "Update"]
    _draw_loop(output, spec.title, steps)


def _render_bounded_autonomy_recoverability(output: Path, spec: FigureSpec) -> None:
    rows = ["Authority", "Allowed tools", "Human gate", "Stop rule", "Recovery"]
    cols = ["Assist", "Supervise", "Escalate", "Block"]
    _draw_matrix(output, spec.title, rows, cols)


def _render_public_ai_register_lifecycle(output: Path, spec: FigureSpec) -> None:
    steps = ["Use case", "Impact", "Approve", "Publish", "Feedback", "Refresh"]
    _draw_loop(output, spec.title, steps)


def _render_ai_incident_reporting_loop(output: Path, spec: FigureSpec) -> None:
    steps = ["Detect", "Triage", "Classify", "Report", "Remediate", "Learn"]
    _draw_loop(output, spec.title, steps)


def _render_ot_definitive_architecture_record(output: Path, spec: FigureSpec) -> None:
    rows = ["Assets", "Data flows", "Remote access", "Safety boundary", "Vendor support"]
    cols = ["Owner", "Evidence", "Change", "Review"]
    _draw_matrix(output, spec.title, rows, cols)


def _render_data_lineage_registry(output: Path, spec: FigureSpec) -> None:
    rows = ["Citation", "Anchor", "Dataset", "Transcript", "Artifact"]
    cols = ["Origin", "Transform", "Reviewer", "Retention", "Gate"]
    _draw_matrix(output, spec.title, rows, cols)


def _render_assessment_integrity_matrix(output: Path, spec: FigureSpec) -> None:
    rows = ["AI use", "Reasoning", "Citations", "Lab boundary", "Revision"]
    cols = ["Student", "Instructor", "Evidence", "Risk", "Disposition"]
    _draw_matrix(output, spec.title, rows, cols)


def _render_adversarial_assurance_cycle(output: Path, spec: FigureSpec) -> None:
    steps = ["Misuse case", "Challenge", "Attack evidence", "Rehearse", "Remediate", "Retest"]
    _draw_loop(output, spec.title, steps)


def _render_model_dataset_card(output: Path, spec: FigureSpec) -> None:
    rows = ["Intended use", "Composition", "Evaluation", "Lifecycle"]
    cols = ["Model", "Dataset", "Review", "Refresh"]
    _draw_matrix(output, spec.title, rows, cols)


def _render_transparency_notice_flow(output: Path, spec: FigureSpec) -> None:
    steps = ["Purpose", "Tool summary", "Impact", "Review", "Publish", "Refresh"]
    _draw_loop(output, spec.title, steps)


def _render_records_retention_audit(output: Path, spec: FigureSpec) -> None:
    rows = ["Sources", "Prompts", "Decisions", "Exceptions", "Incidents", "Artifacts"]
    cols = ["Owner", "Retain", "Limit", "Audit", "Delete"]
    _draw_matrix(output, spec.title, rows, cols)


def _render_release_change_control(output: Path, spec: FigureSpec) -> None:
    steps = ["Scope", "Rights", "Version", "Rollback", "Monitor", "Retest"]
    _draw_loop(output, spec.title, steps)


def _render_risk_exception_memo(output: Path, spec: FigureSpec) -> None:
    rows = ["Exception", "Risk basis", "Control", "Expiry"]
    cols = ["Evidence", "Owner", "Decision", "Retest"]
    _draw_matrix(output, spec.title, rows, cols)


def _render_learner_support_plan(output: Path, spec: FigureSpec) -> None:
    steps = ["Access", "Load", "Fairness", "Feedback", "Remediate", "Retest"]
    _draw_loop(output, spec.title, steps)


def _render_instructor_question_bank(output: Path, spec: FigureSpec) -> None:
    rows = ["Source", "Boundary", "Rights", "Assurance"]
    cols = ["Prompt", "Evidence", "Revision", "Disposition"]
    _draw_matrix(output, spec.title, rows, cols)


def _render_remediation_backlog(output: Path, spec: FigureSpec) -> None:
    rows = ["Claim", "Safety", "Access", "Assurance"]
    cols = ["Trigger", "Owner", "Due", "Evidence", "Closed"]
    _draw_matrix(output, spec.title, rows, cols)


def _research_anchor_count() -> int:
    try:
        from .intelligence_content import INTELLIGENCE_RESEARCH_ANCHORS
    except ImportError:  # pragma: no cover - direct script imports
        from intelligence_content import INTELLIGENCE_RESEARCH_ANCHORS  # type: ignore[no-redef]

    return len(INTELLIGENCE_RESEARCH_ANCHORS)


def _draw_bar_chart(output: Path, title: str, labels: Sequence[str], values: Sequence[int], color: str) -> None:
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (1600, 1000), "#f8fafc")
    draw = draw_mod.Draw(canvas)
    title_font = _font(font_mod, 46)
    label_font = _font(font_mod, 18)
    draw.text((60, 40), title, fill="#0f172a", font=title_font)
    chart = (80, 150, 1520, 850)
    max_value = max(values) or 1
    bar_width = max(6, (chart[2] - chart[0]) // max(1, len(values)) - 4)
    for index, value in enumerate(values):
        x0 = chart[0] + index * ((chart[2] - chart[0]) / max(1, len(values)))
        x1 = x0 + bar_width
        height = (value / max_value) * (chart[3] - chart[1])
        y0 = chart[3] - height
        draw.rectangle((x0, y0, x1, chart[3]), fill=color)
        if len(values) <= 20:
            draw.text((x0, chart[3] + 12), labels[index][:18], fill="#334155", font=label_font)
    draw.line((chart[0], chart[3], chart[2], chart[3]), fill="#334155", width=2)
    draw.text((80, 900), f"Max value: {max_value}", fill="#334155", font=_font(font_mod, 24))
    canvas.save(output, format="PNG", optimize=True)


def _draw_ranked_bands(output: Path, title: str, labels: Sequence[str], color: str) -> None:
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (1600, 1000), "#f8fafc")
    draw = draw_mod.Draw(canvas)
    draw.text((60, 40), title, fill="#0f172a", font=_font(font_mod, 46))
    for index, label in enumerate(labels):
        y = 145 + index * 76
        draw.rounded_rectangle((80, y, 1520, y + 48), radius=10, fill=color)
        draw.text((110, y + 10), label, fill="#ffffff", font=_font(font_mod, 26))
    canvas.save(output, format="PNG", optimize=True)


def _draw_tile_grid(output: Path, title: str, labels: Sequence[str], color: str) -> None:
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (1600, 1000), "#f8fafc")
    draw = draw_mod.Draw(canvas)
    draw.text((60, 40), title, fill="#0f172a", font=_font(font_mod, 46))
    cols = 4
    tile_w = 340
    tile_h = 130
    for index, label in enumerate(labels):
        row, col = divmod(index, cols)
        x = 80 + col * 380
        y = 145 + row * 150
        draw.rounded_rectangle((x, y, x + tile_w, y + tile_h), radius=8, fill="#ffffff", outline=color, width=4)
        wrapped = textwrap.wrap(label, width=26)[:3]
        for line_index, line in enumerate(wrapped):
            draw.text((x + 24, y + 24 + line_index * 30), line, fill="#111827", font=_font(font_mod, 22))
    canvas.save(output, format="PNG", optimize=True)


def _draw_loop(output: Path, title: str, steps: Sequence[str]) -> None:
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (1600, 1000), "#f8fafc")
    draw = draw_mod.Draw(canvas)
    draw.text((60, 40), title, fill="#0f172a", font=_font(font_mod, 46))
    center = (800, 520)
    radius = 310
    for index, step in enumerate(steps):
        angle = (2 * math.pi * index / len(steps)) - math.pi / 2
        x = center[0] + math.cos(angle) * radius
        y = center[1] + math.sin(angle) * radius
        draw.ellipse((x - 95, y - 55, x + 95, y + 55), fill="#0f766e", outline="#0f172a", width=3)
        draw.text((x - 70, y - 15), step, fill="#ffffff", font=_font(font_mod, 22))
    draw.ellipse((center[0] - 175, center[1] - 175, center[0] + 175, center[1] + 175), outline="#334155", width=8)
    draw.text((center[0] - 125, center[1] - 18), "Non-operational", fill="#0f172a", font=_font(font_mod, 30))
    canvas.save(output, format="PNG", optimize=True)


def _draw_matrix(output: Path, title: str, rows: Sequence[str], cols: Sequence[str]) -> None:
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (1800, 1200), "#f8fafc")
    draw = draw_mod.Draw(canvas)
    draw.text((60, 40), title, fill="#0f172a", font=_font(font_mod, 46))
    x0, y0 = 460, 150
    cell_w, cell_h = 190, 54
    for col_index, col in enumerate(cols):
        draw.text((x0 + col_index * cell_w + 10, y0 - 45), col, fill="#0f172a", font=_font(font_mod, 22))
    for row_index, row in enumerate(rows):
        y = y0 + row_index * cell_h
        draw.text((60, y + 12), row[:38], fill="#334155", font=_font(font_mod, 20))
        for col_index, _ in enumerate(cols):
            x = x0 + col_index * cell_w
            shade = "#bfdbfe" if (row_index + col_index) % 2 == 0 else "#d1fae5"
            draw.rectangle((x, y, x + cell_w - 8, y + cell_h - 8), fill=shade, outline="#64748b")
    canvas.save(output, format="PNG", optimize=True)


def _draw_concept_plate(output: Path, title: str, prompt: str, label: str) -> None:
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    digest = hashlib.sha256(f"{title}|{prompt}|{label}".encode("utf-8")).digest()
    canvas = image_mod.new("RGB", (1600, 1000), "#0f172a")
    draw = draw_mod.Draw(canvas)
    palette = ["#14b8a6", "#eab308", "#38bdf8", "#f97316", "#a78bfa", "#f8fafc"]
    for index in range(42):
        x0 = 60 + (digest[index % len(digest)] * 37 + index * 91) % 1440
        y0 = 130 + (digest[(index + 7) % len(digest)] * 41 + index * 59) % 730
        size = 40 + digest[(index + 11) % len(digest)] % 130
        color = palette[index % len(palette)]
        draw.rounded_rectangle((x0, y0, x0 + size * 1.6, y0 + size), radius=14, outline=color, width=4)
    draw.rectangle((0, 0, 1600, 120), fill="#f8fafc")
    draw.text((60, 36), title, fill="#0f172a", font=_font(font_mod, 42))
    draw.rectangle((0, 820, 1600, 1000), fill="#f8fafc")
    wrapped = textwrap.wrap(prompt, width=110)[:4]
    for idx, line in enumerate(wrapped):
        draw.text((60, 848 + idx * 34), line, fill="#334155", font=_font(font_mod, 24))
    canvas.save(output, format="PNG", optimize=True)


def _draw_text_plate(output: Path, title: str, body: str) -> None:
    image_mod, draw_mod, font_mod, _ = _pil_modules()
    output.parent.mkdir(parents=True, exist_ok=True)
    canvas = image_mod.new("RGB", (1400, 900), "#f8fafc")
    draw = draw_mod.Draw(canvas)
    draw.text((60, 60), title, fill="#0f172a", font=_font(font_mod, 42))
    for idx, line in enumerate(textwrap.wrap(body, width=80)):
        draw.text((60, 160 + idx * 34), line, fill="#334155", font=_font(font_mod, 24))
    canvas.save(output, format="PNG", optimize=True)


def _normalize_png_canvas(output: Path, size: int = 1400) -> None:
    """Fit a rendered PNG onto a square canvas for stable manuscript layout."""
    if not output.is_file():
        return
    image_mod, _, _, ops_mod = _pil_modules()
    with image_mod.open(output) as img:
        image = img.convert("RGBA")
    fitted = ops_mod.contain(image, (size - 120, size - 120))
    canvas = image_mod.new("RGBA", (size, size), "#f8fafcff")
    x = (size - fitted.width) // 2
    y = (size - fitted.height) // 2
    canvas.alpha_composite(fitted, (x, y))
    normalized = output.with_name(f".{output.stem}.normalized{output.suffix}")
    if normalized.exists():
        normalized.unlink()
    try:
        canvas.convert("RGB").save(normalized, format="PNG", optimize=True)
        normalized.replace(output)
    finally:
        if normalized.exists():
            normalized.unlink()


def _temporary_png_path(output: Path) -> Path:
    return output.with_name(f".{output.stem}.tmp{output.suffix}")


def _png_asset_is_valid(path: Path) -> bool:
    try:
        _validate_png_asset(path)
    except (OSError, SyntaxError, ValueError):
        return False
    return True


def _validate_png_asset(path: Path, spec: FigureSpec | None = None) -> None:
    """Fail if *path* is absent, empty, non-PNG, or unreadable by Pillow."""
    label = f" for {spec.label}" if spec is not None else ""
    if not path.is_file():
        raise FileNotFoundError(f"Missing figure asset{label}: {path}")
    if path.stat().st_size <= len(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"Empty or truncated figure asset{label}: {path}")
    if not path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"Figure asset is not a PNG{label}: {path}")
    image_mod, _, _, _ = _pil_modules()
    with image_mod.open(path) as image:
        width, height = image.size
        image.verify()
    if width <= 0 or height <= 0:
        raise ValueError(f"Figure asset has invalid dimensions{label}: {path}")


def _pil_modules() -> tuple[Any, Any, Any, Any]:
    return (
        import_module("PIL.Image"),
        import_module("PIL.ImageDraw"),
        import_module("PIL.ImageFont"),
        import_module("PIL.ImageOps"),
    )


def _font(font_mod: Any, size: int) -> Any:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).is_file():
            return font_mod.truetype(candidate, size)
    return font_mod.load_default()


def _download_bytes(url: str) -> bytes | None:
    request = urllib.request.Request(url, headers={"User-Agent": "AGEINT local figure generator"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:  # nosec B310 - fixed HTTPS provenance URLs.
            data = cast(bytes, response.read())
    except (urllib.error.URLError, TimeoutError):
        return None
    return data


def _entry(figure: dict[str, Any] | FigureSpec) -> dict[str, Any]:
    if isinstance(figure, FigureSpec):
        payload = asdict(figure)
        payload["kind"] = figure.kind.value
        return payload
    return dict(figure)


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "figure"


def _mermaid_label(value: str) -> str:
    # Mermaid renders HTML entities inside node text, so the ampersand survives
    # as a proper "&" (e.g. "MITRE ATT&CK") instead of the lossy "and".
    return value.replace('"', "'").replace("&", "&amp;")


def _markdown_escape(value: str) -> str:
    return value.replace("[", "(").replace("]", ")")


def _relative_posix(path: Path, start: Path) -> str:
    try:
        return Path(path).relative_to(start).as_posix()
    except ValueError:
        return _relpath(path, start)


def _relpath(path: Path, start: Path) -> str:
    import os

    return Path(os.path.relpath(path, start)).as_posix()
