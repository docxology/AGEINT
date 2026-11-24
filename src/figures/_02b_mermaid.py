"""Mermaid figure rendering and placeholder fallbacks for AGEINT figures."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess  # nosec B404 - fixed argv, no shell, local renderer.
from pathlib import Path

from ._03s_drawers import _draw_text_plate
from ._04_part import _mermaid_label, _normalize_png_canvas, _png_asset_is_valid, _slug
from .mermaid_contracts import mermaid_type_contract, validate_mermaid_source_contract

from curriculum import Curriculum

from ._01_part import FigureSpec


def _with_theme(source: str, diagram_type: str) -> str:
    """Prepend the diagram-type init header unless one is already present."""
    if source.lstrip().startswith("%%{init"):
        return source
    return mermaid_type_contract(diagram_type).init_block + source


def _discover_chrome_executable() -> str | None:
    """Return a chrome-headless-shell binary for mmdc/Puppeteer."""
    env_path = os.environ.get("CHROME_EXECUTABLE_PATH", "").strip()
    if env_path and Path(env_path).is_file():
        return env_path
    cache_root = Path.home() / ".cache" / "puppeteer"
    if not cache_root.is_dir():
        return None
    patterns = (
        "chrome-headless-shell/mac_arm-*/chrome-headless-shell-mac-arm64/chrome-headless-shell",
        "chrome-headless-shell/mac-*/chrome-headless-shell-mac-x64/chrome-headless-shell",
        "chrome-headless-shell/linux-*/chrome-headless-shell-linux64/chrome-headless-shell",
        "chrome-headless-shell/win64-*/chrome-headless-shell-win64/chrome-headless-shell.exe",
    )
    candidates: list[Path] = []
    for pattern in patterns:
        candidates.extend(cache_root.glob(pattern))
    if not candidates:
        return None
    preferred = [path for path in candidates if "131.0.6778.204" in str(path)]
    chosen = preferred[0] if preferred else sorted(candidates)[0]
    return str(chosen)


def placeholder_or_fail(output_path: Path, title: str, message: str, *, allow_placeholder_figures: bool) -> None:
    if not allow_placeholder_figures:
        raise FileNotFoundError(f"Figure asset missing for {title}: {message}")
    _draw_text_plate(output_path, title, message)
    _normalize_png_canvas(output_path)


def render_mermaid_figure(root: Path, curriculum: Curriculum, spec: FigureSpec, output_path: Path, *, allow_placeholder_figures: bool = False) -> bool:
    """Render ``spec`` to ``output_path`` via mmdc.

    Returns ``True`` only when mmdc produced a real, valid PNG; returns ``False``
    when a placeholder plate was substituted (mmdc missing, or a failed/invalid
    render). The caller uses this to decide whether the content cache may record
    this render — a placeholder must never be cached as a current diagram.
    """
    source_path = root / spec.source_artifact_path
    source_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    source = mermaid_source(curriculum, spec)
    if not source_path.is_file() or source_path.read_text(encoding="utf-8") != source:
        source_path.write_text(source, encoding="utf-8")
    mmdc = shutil.which("mmdc")
    if mmdc is None:
        placeholder_or_fail(output_path, spec.title, "Mermaid CLI unavailable; source saved locally.", allow_placeholder_figures=allow_placeholder_figures)
        return False
    puppeteer = source_path.parent / "puppeteer-config.json"
    puppeteer_config: dict[str, object] = {"args": ["--no-sandbox", "--disable-setuid-sandbox"], "defaultViewport": {"width": 1400, "height": 1400, "deviceScaleFactor": 1}}
    chrome_executable = _discover_chrome_executable()
    if chrome_executable:
        puppeteer_config["executablePath"] = chrome_executable
    puppeteer.write_text(json.dumps(puppeteer_config, indent=2, sort_keys=True), encoding="utf-8")
    cmd = [mmdc, "-i", str(source_path), "-o", str(output_path), "-p", str(puppeteer), "-b", "transparent", "-q"]
    proc = subprocess.run(  # nosec B603 - fixed argv, no shell.
        cmd, check=False, capture_output=True, text=True, timeout=120
    )
    if proc.returncode != 0 or not _png_asset_is_valid(output_path):
        message = (proc.stderr or proc.stdout or "mmdc did not create output").strip()
        placeholder_or_fail(output_path, spec.title, f"Mermaid fallback render\n{message[:220]}", allow_placeholder_figures=allow_placeholder_figures)
        return False
    return True


def mermaid_source(curriculum: Curriculum, spec: FigureSpec) -> str:
    diagram_type = str(spec.provenance.get("diagram_type", "flowchart") or "flowchart")
    reader_detail = str(spec.provenance.get("reader_detail", "") or "")
    diagram = spec.provenance.get("diagram", "")
    if diagram in _SYNTHESIS_MERMAID_SOURCES:
        return _synthesis_mermaid_source(diagram, diagram_type, reader_detail)
    if spec.label == "fig:ageint-curriculum-map":
        return _curriculum_map_mermaid_source(curriculum, diagram_type, reader_detail)

    return _part_module_map_mermaid_source(curriculum, spec, diagram_type, reader_detail)


def _synthesis_mermaid_source(diagram: str, diagram_type: str, reader_detail: str) -> str:
    source = _with_theme(_SYNTHESIS_MERMAID_SOURCES[diagram], diagram_type)
    validate_mermaid_source_contract(diagram_type, source, reader_detail)
    return source


def _curriculum_map_mermaid_source(curriculum: Curriculum, diagram_type: str, reader_detail: str) -> str:
    # The parts are siblings of one curriculum, not a linear dependency chain.
    # Grouping them under stacked subgraph rows lets Mermaid lay them out as a
    # wide multi-column grid that fills the square canvas and keeps labels large.
    parts = list(curriculum.parts)
    lines = ["flowchart TB", f'    root["AGEINT curriculum<br/>{curriculum.stats["parts"]} parts"]']
    columns = 4
    row_anchors: list[str] = []
    for row_start in range(0, len(parts), columns):
        row_parts = parts[row_start : row_start + columns]
        row_id = f"row{row_start // columns}"
        lines.append(f'    subgraph {row_id} [" "]')
        lines.append("        direction LR")
        row_nodes: list[str] = []
        for part in row_parts:
            node = f"p{part['number']}"
            label = _mermaid_label(f"{part['roman']}. {part['title']}<br/>{len(part['chapters'])} modules")
            lines.append(f'        {node}["{label}"]')
            row_nodes.append(node)
        for left, right in zip(row_nodes, row_nodes[1:]):
            lines.append(f"        {left} ~~~ {right}")
        lines.append("    end")
        row_anchors.append(row_id)
    spine = ["root", *row_anchors]
    for upper, lower in zip(spine, spine[1:]):
        lines.append(f"    {upper} --> {lower}")
    source = _with_theme("\n".join(lines) + "\n", diagram_type)
    validate_mermaid_source_contract(diagram_type, source, reader_detail)
    return source


def _part_module_map_mermaid_source(curriculum: Curriculum, spec: FigureSpec, diagram_type: str, reader_detail: str) -> str:
    part_slug = Path(spec.output_path).stem.removeprefix("part-").removesuffix("-module-map")
    part = next(item for item in curriculum.parts if _slug(item["title"]) == part_slug)
    # Top-to-bottom chains turn 2-6 module nodes into a tall box that fills the
    # square canvas; the old LR row collapsed to a thin band with tiny text.
    lines = ["flowchart TB", f'    part["{_mermaid_label(part["title"])}"]']
    previous = "part"
    for index, chapter in enumerate(part["chapters"], 1):
        node = f"c{index}"
        label = _mermaid_label(chapter["title"])
        lines.append(f'    {previous} --> {node}["{label}"]')
        previous = node
    source = _with_theme("\n".join(lines) + "\n", diagram_type)
    validate_mermaid_source_contract(diagram_type, source, reader_detail)
    return source


# Synthesis and chapter-concept diagrams are declared as data in
# data/figures/synthesis_extra.jsonl and merged into these structures by the
# loader below, keeping the large Mermaid sources out of this module.
_SYNTHESIS_MERMAID_SOURCES: dict[str, str] = {}
SYNTHESIS_MERMAID: tuple[dict[str, str], ...] = ()


# Synthesis and chapter-concept diagrams live as one JSON object per line in
# data/figures/synthesis_extra.jsonl. Each row owns its Mermaid source and reader
# metadata; build_figure_specs() and mermaid_source() share this single source.
_EXTRA_DIAGRAMS_PATH = Path(__file__).resolve().parents[2] / "data" / "figures" / "synthesis_extra.jsonl"


def _load_extra_synthesis_diagrams() -> list[dict[str, str]]:
    """Return chapter-level synthesis diagrams declared in the JSONL data file."""
    if not _EXTRA_DIAGRAMS_PATH.is_file():
        return []
    return [dict(json.loads(line)) for line in _EXTRA_DIAGRAMS_PATH.read_text(encoding="utf-8").splitlines() if line.strip()]


_EXTRA_SYNTHESIS_DIAGRAMS = _load_extra_synthesis_diagrams()
for _row in _EXTRA_SYNTHESIS_DIAGRAMS:
    _SYNTHESIS_MERMAID_SOURCES[_row["diagram"]] = _row["mermaid_source"]
SYNTHESIS_MERMAID = SYNTHESIS_MERMAID + tuple(
    {key: row[key] for key in ("slug", "title", "caption", "alt_text", "diagram", "source_section", "diagram_type", "reader_detail") if key in row} for row in _EXTRA_SYNTHESIS_DIAGRAMS
)


def _mermaid_cache_marker(root: Path, spec: FigureSpec) -> Path:
    """Sidecar path that records the source hash of the last real mermaid render."""
    return root / (spec.source_artifact_path + ".rendered")


def _mermaid_source_hash(curriculum: Curriculum, spec: FigureSpec) -> str | None:
    """SHA-256 of the themed mermaid source for ``spec`` (None if unavailable).

    The source text — theme header included — fully determines the rendered PNG
    (mmdc args and the square-canvas normalization are fixed), so it is a sound
    content-cache key: unchanged source means an unchanged diagram.
    """
    try:
        source = mermaid_source(curriculum, spec)
    except Exception:  # pragma: no cover - defensive; falls back to re-render
        return None
    return hashlib.sha256(source.encode("utf-8")).hexdigest()
