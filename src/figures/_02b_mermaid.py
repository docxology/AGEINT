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
