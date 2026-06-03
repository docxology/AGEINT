"""Mermaid figure rendering and placeholder fallbacks for AGEINT figures."""

from __future__ import annotations

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
) -> None:
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
        return
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


def mermaid_source(curriculum: Curriculum, spec: FigureSpec) -> str:
    diagram = spec.provenance.get("diagram", "")
    if diagram in _SYNTHESIS_MERMAID_SOURCES:
        return _SYNTHESIS_MERMAID_SOURCES[diagram]
    if spec.label == "fig:ageint-curriculum-map":
        lines = [
            "flowchart TB",
            f'    root["AGEINT curriculum<br/>{curriculum.stats["parts"]} parts"]',
        ]
        previous = "root"
        for part in curriculum.parts:
            node = f"p{part['number']}"
            label = _mermaid_label(f"{part['roman']}. {part['title']}<br/>{len(part['chapters'])} modules")
            lines.append(f"    {previous} --> {node}[\"{label}\"]")
            previous = node
        return "\n".join(lines) + "\n"

    part_slug = Path(spec.output_path).stem.removeprefix("part-").removesuffix("-module-map")
    part = next(
        item
        for item in curriculum.parts
        if _slug(item["title"]) == part_slug
    )
    lines = [
        "flowchart LR",
        f'    part["{_mermaid_label(part["title"])}"]',
    ]
    previous = "part"
    for index, chapter in enumerate(part["chapters"], 1):
        node = f"c{index}"
        label = _mermaid_label(chapter["title"])
        lines.append(f'    {previous} --> {node}["{label}"]')
        previous = node
    return "\n".join(lines) + "\n"


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

_MAESTRO_SEVEN_LAYER = """flowchart TB
    l7["L7: Agent Ecosystem<br/>impersonation, marketplace<br/>manipulation, goal manipulation"]
    l5["L5: Evaluation and Observability<br/>metric manipulation,<br/>detection evasion"]
    l4["L4: Deployment and Infrastructure<br/>container escape,<br/>lateral movement"]
    l3["L3: Agent Frameworks<br/>supply chain, compromised<br/>components, input validation"]
    l2["L2: Data Operations<br/>data poisoning,<br/>RAG pipeline compromise"]
    l1["L1: Foundation Models<br/>adversarial examples,<br/>model stealing, backdoors"]
    l7 --> l5 --> l4 --> l3 --> l2 --> l1
    l6["L6: Security and Compliance<br/>cross-cutting layer<br/>security agents are<br/>themselves attack surfaces<br/>monitor the monitors"]
    l6 -.-> l7
    l6 -.-> l5
    l6 -.-> l4
    l6 -.-> l3
    l6 -.-> l2
    l6 -.-> l1
"""

_SRE_CIRCUIT_BREAKER = """flowchart LR
    closed["CLOSED<br/>normal operation<br/>autonomy earned by<br/>clean safety record"]
    open["OPEN<br/>agent suspended<br/>human takeover"]
    half["HALF_OPEN<br/>limited capability<br/>restoration"]
    closed -->|"safety budget exhausted<br/>PolicyCompliance below 99 percent"| open
    open -->|"recovery period<br/>plus validation"| half
    half -->|"clean record maintained"| closed
    half -->|"new violation"| open
    trig["Activation triggers<br/>policy bypass attempts<br/>LLM provider errors<br/>tool timeout cascades<br/>trust score degradation<br/>reasoning loops and deadlocks"]
    trig -.-> open
"""

_COGNITIVE_DECOHERENCE_CDR_ISOMORPHISM = """flowchart LR
    subgraph HUM["Human Orgs: Cognitive Decoherence (CCDCOE)"]
        direction TB
        h1["Initiation<br/>adversary targets systemic<br/>invariants: trust, identity,<br/>epistemic standards"]
        h2["Early degradation<br/>uncertainty amplification;<br/>inter-layer linkages weaken"]
        h3["Drift<br/>polarization rises;<br/>coordination capacity erodes"]
        h4["Entrenchment<br/>competing epistemic<br/>frameworks harden"]
        h5["Override<br/>adversary narrative fills<br/>the institutional vacuum"]
        h6["Collapse<br/>system functions formally<br/>but cannot coordinate"]
        h1 --> h2 --> h3 --> h4 --> h5 --> h6
    end
    subgraph AGT["AI Agents: Cognitive Degradation (CDR)"]
        direction TB
        a1["Trigger Injection<br/>adversarial inputs<br/>establish foothold"]
        a2["Resource Starvation<br/>compute and context<br/>consumed"]
        a3["Behavioral Drift<br/>outputs deviate<br/>without alerts"]
        a4["Memory Entrenchment<br/>corrupted beliefs<br/>solidify"]
        a5["Functional Override<br/>adversary goals supersede<br/>legitimate tasks"]
        a6["Systemic Collapse<br/>coordinated behavior<br/>serves adversary"]
        a1 --> a2 --> a3 --> a4 --> a5 --> a6
    end
    h1 -.->|"isomorphic"| a1
    h2 -.->|"isomorphic"| a2
    h3 -.->|"isomorphic"| a3
    h4 -.->|"isomorphic"| a4
    h5 -.->|"isomorphic"| a5
    h6 -.->|"isomorphic"| a6
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
    root --> bio["Biological layer"]
    root --> psy["Psychological layer"]
    root --> soc["Social layer"]
    bio --> bt["Target: cognitive capacity"]
    bio --> bm["Mechanism: neuroscience-informed<br/>targeting of the nervous system"]
    bio --> ba["AI role: optimized delivery<br/>timing and channel selection"]
    psy --> pt["Target: cognitive interpretation"]
    psy --> pm["Mechanism: manipulating individual<br/>cognition, exploiting biases at scale"]
    psy --> pa["AI role: tailored influence matched<br/>to cognitive vulnerability profiles"]
    soc --> st["Target: cognitive cohesion"]
    soc --> sm["Mechanism: fracturing shared narratives,<br/>weaponizing identity, epistemic chaos"]
    soc --> sa["AI role: coordinating synthetic<br/>influence campaigns across platforms"]
"""

_HRO_GOVERNANCE_CROSSWALK = """flowchart LR
    subgraph HRO["HRO Principles (Weick and Sutcliffe)"]
        direction TB
        p1["Preoccupation with failure<br/>attention to near-misses<br/>and weak signals"]
        p2["Reluctance to simplify<br/>demand deep root cause;<br/>resist reductive explanations"]
        p3["Sensitivity to operations<br/>awareness of current<br/>operational state"]
        p4["Commitment to resilience<br/>invest in corrective<br/>and adaptive capacity"]
        p5["Deference to expertise<br/>authority follows<br/>demonstrated competence"]
    end
    subgraph GOV["AI Agent Governance Mechanisms"]
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

_SYNTHESIS_MERMAID_SOURCES: dict[str, str] = {
    "cdr_degradation_cascade": _CDR_DEGRADATION_CASCADE,
    "maestro_seven_layer": _MAESTRO_SEVEN_LAYER,
    "sre_circuit_breaker": _SRE_CIRCUIT_BREAKER,
    "cognitive_decoherence_cdr_isomorphism": _COGNITIVE_DECOHERENCE_CDR_ISOMORPHISM,
    "unified_epistemic_stack": _UNIFIED_EPISTEMIC_STACK,
    "cognitive_attack_layers": _COGNITIVE_ATTACK_LAYERS,
    "hro_governance_crosswalk": _HRO_GOVERNANCE_CROSSWALK,
}


# Synthesis methods figures from the cognitive-security/agentic-intelligence
# source guide. Each entry becomes a MERMAID FigureSpec in build_figure_specs;
# the "diagram" key selects the static source above via mermaid_source().
SYNTHESIS_MERMAID: tuple[dict[str, str], ...] = (
    {
        "slug": "ageint-cdr-degradation-cascade",
        "title": "AGEINT CDR Six-Stage Degradation Cascade",
        "caption": (
            "The CSA Cognitive Degradation Resilience cascade traces how an agent "
            "network slides from trigger injection to systemic collapse below "
            "conventional alerting thresholds."
        ),
        "alt_text": (
            "Mermaid flowchart of six CDR degradation stages with adversary action, "
            "observed effect, and QSAF-BC control for each stage."
        ),
        "diagram": "cdr_degradation_cascade",
        "source_section": "appendix:g",
    },
    {
        "slug": "ageint-maestro-seven-layer",
        "title": "AGEINT MAESTRO Seven-Layer Threat Model",
        "caption": (
            "The CSA MAESTRO model stacks seven layers of the agentic AI lifecycle, "
            "with the L6 Security/Compliance layer cross-cutting every other layer "
            "because security agents are themselves attack surfaces."
        ),
        "alt_text": (
            "Mermaid diagram of MAESTRO layers L1 through L7 in a vertical stack, with "
            "L6 Security and Compliance drawn as a cross-cutting node linked to all "
            "other layers."
        ),
        "diagram": "maestro_seven_layer",
        "source_section": "chapter:34",
    },
    {
        "slug": "ageint-sre-circuit-breaker",
        "title": "AGEINT SRE-for-Agents Circuit Breaker",
        "caption": (
            "Microsoft's SRE-for-agents governance circuit breaker cycles agents "
            "through CLOSED, OPEN, and HALF_OPEN states as the safety error budget "
            "burns down and is restored."
        ),
        "alt_text": (
            "Mermaid state-style flowchart showing CLOSED, OPEN, and HALF_OPEN "
            "circuit-breaker states with the transition triggers between them and a "
            "list of activation triggers."
        ),
        "diagram": "sre_circuit_breaker",
        "source_section": "chapter:34",
    },
    {
        "slug": "ageint-cognitive-decoherence-cdr-isomorphism",
        "title": "AGEINT Decoherence-Degradation Isomorphism",
        "caption": (
            "The six phases of CCDCOE cognitive decoherence in human organizations map "
            "one-to-one onto the CSA CDR cognitive-degradation stages in AI agent "
            "networks, exposing a shared adversarial dynamic."
        ),
        "alt_text": (
            "Mermaid diagram with two vertical six-step columns, human cognitive "
            "decoherence on the left and AI cognitive degradation on the right, joined "
            "by horizontal isomorphism links at each aligned phase."
        ),
        "diagram": "cognitive_decoherence_cdr_isomorphism",
        "source_section": "appendix:g",
    },
    {
        "slug": "ageint-unified-epistemic-stack",
        "title": "AGEINT Unified Epistemic Coherence Stack",
        "caption": (
            "The synthesis's five-layer architecture stacks technical substrate, "
            "operational security, structured reasoning, epistemic integrity, and "
            "institutional governance into one mutually reinforcing system for "
            "maintaining epistemic coherence."
        ),
        "alt_text": (
            "Mermaid flowchart of five stacked layers from Technical Substrate at the "
            "base to Institutional Governance at the top, each annotated with its "
            "representative mechanisms."
        ),
        "diagram": "unified_epistemic_stack",
        "source_section": "part:epistemic rigor and analytic tradecraft",
    },
    {
        "slug": "ageint-cognitive-attack-layers",
        "title": "AGEINT Cognitive Attack Layer Taxonomy",
        "caption": (
            "The NATO/INSS cognitive warfare taxonomy distinguishes biological, "
            "psychological, and social attack layers by their target, mechanism, and "
            "the role AI plays in each."
        ),
        "alt_text": (
            "Mermaid diagram with a root cognitive-attack node branching into "
            "biological, psychological, and social layers, each expanding into its "
            "attack target, mechanism, and AI role."
        ),
        "diagram": "cognitive_attack_layers",
        "source_section": "part:cognitive security",
    },
    {
        "slug": "ageint-hro-governance-crosswalk",
        "title": "AGEINT HRO-to-Governance Crosswalk",
        "caption": (
            "Weick and Sutcliffe's five High-Reliability Organization principles map "
            "directly onto concrete AI agent governance mechanisms, turning "
            "organizational theory into observable controls."
        ),
        "alt_text": (
            "Mermaid diagram pairing each of the five HRO principles on the left with "
            "its corresponding AI agent governance mechanism on the right."
        ),
        "diagram": "hro_governance_crosswalk",
        "source_section": "part:epistemic rigor and analytic tradecraft",
    },
)
