"""Mermaid figure rendering and placeholder fallbacks for AGEINT figures."""

from __future__ import annotations

import hashlib
import json
import os
import shutil
import subprocess  # nosec B404 - fixed argv, no shell, local renderer.
from pathlib import Path

from ._03_part import (
    _draw_text_plate,
    _mermaid_label,
    _normalize_png_canvas,
    _png_asset_is_valid,
    _slug,
)

from curriculum import Curriculum

from ._01_part import FigureSpec


# Shared theme header applied to every Mermaid source. Larger base font and
# generous node/rank spacing keep labels legible after the square-canvas
# normalization in _normalize_png_canvas (output is force-fit to 1280px on a
# 1400px square, so any wasted bounding-box area shrinks text). The
# subGraphTitleMargin keeps subgraph titles clear of their first child node.
_MERMAID_INIT = (
    "%%{init: {"
    "'theme':'neutral',"
    "'themeVariables':{'fontSize':'20px'},"
    "'flowchart':{'htmlLabels':true,'nodeSpacing':45,'rankSpacing':55,"
    "'subGraphTitleMargin':{'top':8,'bottom':12}}"
    "}}%%\n"
)


def _with_theme(source: str) -> str:
    """Prepend the shared init header unless one is already present."""
    if source.lstrip().startswith("%%{init"):
        return source
    return _MERMAID_INIT + source


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


def placeholder_or_fail(
    output_path: Path,
    title: str,
    message: str,
    *,
    allow_placeholder_figures: bool,
) -> None:
    if not allow_placeholder_figures:
        raise FileNotFoundError(f"Figure asset missing for {title}: {message}")
    _draw_text_plate(output_path, title, message)
    _normalize_png_canvas(output_path)


def render_mermaid_figure(
    root: Path,
    curriculum: Curriculum,
    spec: FigureSpec,
    output_path: Path,
    *,
    allow_placeholder_figures: bool = False,
) -> bool:
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
        placeholder_or_fail(
            output_path,
            spec.title,
            "Mermaid CLI unavailable; source saved locally.",
            allow_placeholder_figures=allow_placeholder_figures,
        )
        return False
    puppeteer = source_path.parent / "puppeteer-config.json"
    puppeteer_config: dict[str, object] = {
        "args": ["--no-sandbox", "--disable-setuid-sandbox"],
        "defaultViewport": {"width": 1400, "height": 1400, "deviceScaleFactor": 1},
    }
    chrome_executable = _discover_chrome_executable()
    if chrome_executable:
        puppeteer_config["executablePath"] = chrome_executable
    puppeteer.write_text(
        json.dumps(
            puppeteer_config,
            indent=2,
            sort_keys=True,
        ),
        encoding="utf-8",
    )
    cmd = [
        mmdc,
        "-i",
        str(source_path),
        "-o",
        str(output_path),
        "-p",
        str(puppeteer),
        "-b",
        "transparent",
        "-q",
    ]
    proc = subprocess.run(  # nosec B603 - fixed argv, no shell.
        cmd,
        check=False,
        capture_output=True,
        text=True,
        timeout=120,
    )
    if proc.returncode != 0 or not _png_asset_is_valid(output_path):
        message = (proc.stderr or proc.stdout or "mmdc did not create output").strip()
        placeholder_or_fail(
            output_path,
            spec.title,
            f"Mermaid fallback render\n{message[:220]}",
            allow_placeholder_figures=allow_placeholder_figures,
        )
        return False
    return True


def mermaid_source(curriculum: Curriculum, spec: FigureSpec) -> str:
    diagram = spec.provenance.get("diagram", "")
    if diagram in _SYNTHESIS_MERMAID_SOURCES:
        return _with_theme(_SYNTHESIS_MERMAID_SOURCES[diagram])
    if spec.label == "fig:ageint-curriculum-map":
        # The parts are siblings of one curriculum, not a linear dependency
        # chain. Grouping them under stacked subgraph rows lets Mermaid lay
        # them out as a wide multi-column grid that fills the square canvas and
        # keeps labels large, instead of a single 16-deep ribbon.
        parts = list(curriculum.parts)
        lines = [
            "flowchart TB",
            f'    root["AGEINT curriculum<br/>{curriculum.stats["parts"]} parts"]',
        ]
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
                label = _mermaid_label(
                    f"{part['roman']}. {part['title']}<br/>{len(part['chapters'])} modules"
                )
                lines.append(f'        {node}["{label}"]')
                row_nodes.append(node)
            # Invisible links between adjacent nodes force Mermaid to lay the row
            # out left-to-right (otherwise edgeless nodes stack vertically).
            for left, right in zip(row_nodes, row_nodes[1:]):
                lines.append(f"        {left} ~~~ {right}")
            lines.append("    end")
            row_anchors.append(row_id)
        # Spine connects root through the row groups top-to-bottom so the figure
        # reads as one curriculum while staying near-square.
        spine = ["root", *row_anchors]
        for upper, lower in zip(spine, spine[1:]):
            lines.append(f"    {upper} --> {lower}")
        return _with_theme("\n".join(lines) + "\n")

    part_slug = Path(spec.output_path).stem.removeprefix("part-").removesuffix("-module-map")
    part = next(
        item
        for item in curriculum.parts
        if _slug(item["title"]) == part_slug
    )
    # Top-to-bottom chains turn 2-6 module nodes into a tall box that fills the
    # square canvas; the old LR row collapsed to a thin band with tiny text.
    lines = [
        "flowchart TB",
        f'    part["{_mermaid_label(part["title"])}"]',
    ]
    previous = "part"
    for index, chapter in enumerate(part["chapters"], 1):
        node = f"c{index}"
        label = _mermaid_label(chapter["title"])
        lines.append(f'    {previous} --> {node}["{label}"]')
        previous = node
    return _with_theme("\n".join(lines) + "\n")


_CDR_DEGRADATION_CASCADE = """flowchart TB
    src["CSA Cognitive Degradation Resilience<br/>staged failure cascade<br/>below monitoring thresholds"]
    src --> s1["Stage 1: Trigger Injection<br/>adversarial inputs establish<br/>foothold in agent reasoning<br/>control: BC-001 starvation detection"]
    s1 --> s2["Stage 2: Resource Starvation<br/>context and compute consumed<br/>to degrade decision quality<br/>control: BC-002 token overload"]
    s2 --> s3["Stage 3: Behavioral Drift<br/>outputs deviate from policy<br/>without triggering alerts<br/>control: BC-006 entropy drift monitor"]
    s3 --> s4["Stage 4: Memory Entrenchment<br/>corrupted beliefs solidify<br/>in agent memory stores<br/>control: BC-007 memory integrity"]
    s4 --> s5["Stage 5: Functional Override<br/>adversary objectives supersede<br/>legitimate task goals<br/>control: BC-005 override resistance"]
    s5 --> s6["Stage 6: Systemic Collapse<br/>coordinated agent behavior<br/>serves adversarial ends"]
    s2 -. early-detection window .-> s3
    s3 -. decisive intervention point .-> s4
"""

_MAESTRO_SEVEN_LAYER = """flowchart LR
    subgraph STACK["MAESTRO lifecycle stack"]
        direction TB
        l7["L7: Agent Ecosystem<br/>impersonation, marketplace<br/>manipulation, goal manipulation"]
        l5["L5: Evaluation and Observability<br/>metric manipulation,<br/>detection evasion"]
        l4["L4: Deployment and Infrastructure<br/>container escape,<br/>lateral movement"]
        l3["L3: Agent Frameworks<br/>supply chain, compromised<br/>components, input validation"]
        l2["L2: Data Operations<br/>data poisoning,<br/>RAG pipeline compromise"]
        l1["L1: Foundation Models<br/>adversarial examples,<br/>model stealing, backdoors"]
        l7 --> l5 --> l4 --> l3 --> l2 --> l1
    end
    l6["L6: Security and Compliance<br/>cross-cutting layer<br/>security agents are<br/>themselves attack surfaces<br/>monitor the monitors"]
    l6 -. "spans every layer" .-> STACK
"""

_SRE_CIRCUIT_BREAKER = """flowchart TB
    closed["CLOSED<br/>normal operation<br/>autonomy earned by<br/>clean safety record"]
    open["OPEN<br/>agent suspended<br/>human takeover"]
    half["HALF_OPEN<br/>limited capability<br/>restoration"]
    trig["Activation triggers<br/>policy bypass attempts<br/>LLM provider errors<br/>tool timeout cascades<br/>trust score degradation<br/>reasoning loops and deadlocks"]
    closed -->|"safety budget exhausted<br/>PolicyCompliance below 99 percent"| open
    open -->|"recovery period<br/>plus validation"| half
    half -->|"clean record maintained"| closed
    half -->|"new violation"| open
    trig -.->|"force"| open
"""

_COGNITIVE_DECOHERENCE_CDR_ISOMORPHISM = """flowchart TB
    subgraph P1["Phase 1 — Initiation"]
        direction LR
        h1["Human orgs / CCDCOE<br/>adversary targets systemic<br/>invariants: trust, identity,<br/>epistemic standards"]
        a1["AI agents / CDR<br/>Trigger Injection: adversarial<br/>inputs establish foothold"]
        h1 -.->|"isomorphic"| a1
    end
    subgraph P2["Phase 2 — Early degradation"]
        direction LR
        h2["Human orgs / CCDCOE<br/>uncertainty amplification;<br/>inter-layer linkages weaken"]
        a2["AI agents / CDR<br/>Resource Starvation:<br/>compute and context consumed"]
        h2 -.->|"isomorphic"| a2
    end
    subgraph P3["Phase 3 — Drift"]
        direction LR
        h3["Human orgs / CCDCOE<br/>polarization rises;<br/>coordination capacity erodes"]
        a3["AI agents / CDR<br/>Behavioral Drift: outputs<br/>deviate without alerts"]
        h3 -.->|"isomorphic"| a3
    end
    subgraph P4["Phase 4 — Entrenchment"]
        direction LR
        h4["Human orgs / CCDCOE<br/>competing epistemic<br/>frameworks harden"]
        a4["AI agents / CDR<br/>Memory Entrenchment:<br/>corrupted beliefs solidify"]
        h4 -.->|"isomorphic"| a4
    end
    subgraph P5["Phase 5 — Override"]
        direction LR
        h5["Human orgs / CCDCOE<br/>adversary narrative fills<br/>the institutional vacuum"]
        a5["AI agents / CDR<br/>Functional Override: adversary<br/>goals supersede legitimate tasks"]
        h5 -.->|"isomorphic"| a5
    end
    subgraph P6["Phase 6 — Collapse"]
        direction LR
        h6["Human orgs / CCDCOE<br/>system functions formally<br/>but cannot coordinate"]
        a6["AI agents / CDR<br/>Systemic Collapse: coordinated<br/>behavior serves adversary"]
        h6 -.->|"isomorphic"| a6
    end
    P1 --> P2 --> P3 --> P4 --> P5 --> P6
"""

_UNIFIED_EPISTEMIC_STACK = """flowchart TB
    l5["Layer 5: Institutional Governance<br/>National Cognitive Security Centers<br/>AI red team programs<br/>ICD 203-equivalent analytic standards<br/>error budget governance"]
    l4["Layer 4: Epistemic Integrity<br/>KuppingerCole epistemic layer<br/>DeepMind verifier agents<br/>knowledge sanctuaries<br/>intent alignment monitoring"]
    l3["Layer 3: Structured Reasoning / Tradecraft<br/>ACH as multi-hypothesis analysis<br/>pre-mortem red teaming<br/>key assumptions auditing<br/>AI-augmented SATs at scale"]
    l2["Layer 2: Operational Security<br/>MAESTRO seven-layer modeling<br/>CDR six-stage monitoring<br/>zero-trust identity, circuit breakers<br/>compute separation, ephemeral VMs"]
    l1["Layer 1: Technical Substrate<br/>formal verification (DARPA ICS)<br/>LLM tagging, prompt infection defense<br/>sandboxing, worktree isolation<br/>SynthID, C2PA provenance"]
    l5 --> l4 --> l3 --> l2 --> l1
    note["Each layer is necessary<br/>but insufficient alone;<br/>layers are mutually reinforcing"]
    note -.-> l3
"""

_COGNITIVE_ATTACK_LAYERS = """flowchart TB
    root["NATO/INSS Cognitive Warfare 2026<br/>three layers of engagement"]
    subgraph BIO["Biological layer"]
        direction TB
        bt["Target<br/>cognitive capacity"]
        bm["Mechanism<br/>neuroscience-informed<br/>targeting of the<br/>nervous system"]
        ba["AI role<br/>optimized delivery<br/>timing and channel<br/>selection"]
        bt --> bm --> ba
    end
    subgraph PSY["Psychological layer"]
        direction TB
        pt["Target<br/>cognitive interpretation"]
        pm["Mechanism<br/>manipulating individual<br/>cognition, exploiting<br/>biases at scale"]
        pa["AI role<br/>tailored influence<br/>matched to cognitive<br/>vulnerability profiles"]
        pt --> pm --> pa
    end
    subgraph SOC["Social layer"]
        direction TB
        st["Target<br/>cognitive cohesion"]
        sm["Mechanism<br/>fracturing shared<br/>narratives, weaponizing<br/>identity, epistemic chaos"]
        sa["AI role<br/>coordinating synthetic<br/>influence campaigns<br/>across platforms"]
        st --> sm --> sa
    end
    root --> BIO
    root --> PSY
    root --> SOC
"""

_HRO_GOVERNANCE_CROSSWALK = """flowchart LR
    subgraph HRO["HRO Principles"]
        direction TB
        p1["Preoccupation with failure<br/>attention to near-misses<br/>and weak signals"]
        p2["Reluctance to simplify<br/>demand deep root cause;<br/>resist reductive explanations"]
        p3["Sensitivity to operations<br/>awareness of current<br/>operational state"]
        p4["Commitment to resilience<br/>invest in corrective<br/>and adaptive capacity"]
        p5["Deference to expertise<br/>authority follows<br/>demonstrated competence"]
    end
    subgraph GOV["AI Agent Governance"]
        direction TB
        g1["Safety SLI monitoring<br/>PolicyCompliance at or above 99 percent;<br/>CDR health probes; drift detection"]
        g2["MAESTRO seven-layer modeling;<br/>multi-hypothesis behavioral analysis"]
        g3["Real-time tool invocation auditing;<br/>context-window analysis; observability"]
        g4["Circuit breakers; chaos engineering;<br/>progressive rollout with SLO gates"]
        g5["Human-in-the-loop for high stakes;<br/>minimum necessary privilege"]
    end
    p1 --> g1
    p2 --> g2
    p3 --> g3
    p4 --> g4
    p5 --> g5
"""

# Synthesis and chapter-concept diagrams are declared as data in
# data/figures/synthesis_extra.json and merged into these structures by the
# loader below, keeping the large Mermaid sources out of this module.
_SYNTHESIS_MERMAID_SOURCES: dict[str, str] = {}
SYNTHESIS_MERMAID: tuple[dict[str, str], ...] = ()


# Synthesis and chapter-concept diagrams live as data in
# data/figures/synthesis_extra.jsonl (one JSON object per line) so the large
# Mermaid sources stay out of this module and the file stays within the 500-line
# cap. Each row carries the same fields as an inline entry plus its own
# ``mermaid_source``. Merging here keeps one rendering path: the specs flow
# through build_figure_specs and mermaid_source() exactly like the inline set.
_EXTRA_DIAGRAMS_PATH = (
    Path(__file__).resolve().parents[2] / "data" / "figures" / "synthesis_extra.jsonl"
)


def _load_extra_synthesis_diagrams() -> list[dict[str, str]]:
    """Return chapter-level synthesis diagrams declared in the JSONL data file."""
    if not _EXTRA_DIAGRAMS_PATH.is_file():
        return []
    return [
        dict(json.loads(line))
        for line in _EXTRA_DIAGRAMS_PATH.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


_EXTRA_SYNTHESIS_DIAGRAMS = _load_extra_synthesis_diagrams()
for _row in _EXTRA_SYNTHESIS_DIAGRAMS:
    _SYNTHESIS_MERMAID_SOURCES[_row["diagram"]] = _row["mermaid_source"]
SYNTHESIS_MERMAID = SYNTHESIS_MERMAID + tuple(
    {key: row[key] for key in ("slug", "title", "caption", "alt_text", "diagram", "source_section")}
    for row in _EXTRA_SYNTHESIS_DIAGRAMS
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
