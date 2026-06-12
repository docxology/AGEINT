from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Sequence, cast

from curriculum import Curriculum

from ._01_part import (
    AI_CONCEPTUAL_PLATES,
    FigureKind,
    FigureSpec,
    HISTORICAL_ASSETS,
    PYTHON_VISUALS,
)
from ._03b_asset_renderers import (
    _render_ai_concept_figure,
    _render_historical_figure,
)
from ._04_part import (
    _entry,
    _markdown_escape,
    _normalize_png_canvas,
    _png_asset_is_valid,
    _relative_posix,
    _temporary_png_path,
    _validate_png_asset,
)
from ._02b_mermaid import SYNTHESIS_MERMAID, placeholder_or_fail, render_mermaid_figure
from ._02b_mermaid import _mermaid_cache_marker, _mermaid_source_hash
from ._02c_reader_text import _with_informative_reader_text
from ._06_python_renderers import render_python_figure


def build_figure_specs(curriculum: Curriculum, manifest: Any) -> list[FigureSpec]:
    """Build deterministic figure specifications from curriculum and manifest data."""
    section_lookup = _section_lookup(manifest)
    specs: list[FigureSpec] = [
        FigureSpec(
            label="fig:ageint-curriculum-map",
            title="AGEINT Curriculum Map",
            caption="The curriculum map links AGEINT parts into a source-backed learning sequence.",
            alt_text="Mermaid diagram showing AGEINT curriculum parts.",
            kind=FigureKind.MERMAID,
            output_path="output/figures/mermaid/ageint-curriculum-map.png",
            source_artifact_path="output/figures/mermaid/ageint-curriculum-map.mmd",
            source_section="orientation.md",
            section_label="sec:curriculum_orientation",
            provenance={
                "renderer": "mmdc",
                "source": "data/curriculum/",
                "diagram": "curriculum_map",
            },
        )
    ]

    for part in curriculum.parts:
        part_section = section_lookup[f"part:{part['title'].lower()}"]
        part_slug = Path(part_section.relative_path).parent.name
        specs.append(
            FigureSpec(
                label=f"fig:part-{part_slug}-module-map",
                title=f"{part['title']} Module Map",
                caption=(
                    f"The {part['title']} module map traces the part's chapters as a "
                    "linear reading sequence."
                ),
                alt_text=f"Flow chart of {part['title']} chapter titles in reading order.",
                kind=FigureKind.MERMAID,
                output_path=f"output/figures/mermaid/part-{part_slug}-module-map.png",
                source_artifact_path=f"output/figures/mermaid/part-{part_slug}-module-map.mmd",
                source_section=part_section.relative_path,
                section_label=part_section.section_label,
                provenance={
                    "renderer": "mmdc",
                    "source": "data/curriculum/",
                    "diagram": "part_module_map",
                },
            )
        )

    for diagram in SYNTHESIS_MERMAID:
        section = _resolve_source_section(diagram["source_section"], section_lookup)
        specs.append(
            FigureSpec(
                label=f"fig:{diagram['slug']}",
                title=diagram["title"],
                caption=diagram["caption"],
                alt_text=diagram["alt_text"],
                kind=FigureKind.MERMAID,
                output_path=f"output/figures/mermaid/{diagram['slug']}.png",
                source_artifact_path=f"output/figures/mermaid/{diagram['slug']}.mmd",
                source_section=section.relative_path,
                section_label=section.section_label,
                provenance={
                    "renderer": "mmdc",
                    "source": (
                        "/Users/4d/Downloads/"
                        "cognitive-security-agentic-intelligence.md"
                    ),
                    "diagram": diagram["diagram"],
                },
            )
        )

    for visual in PYTHON_VISUALS:
        section = _resolve_source_section(visual["source_section"], section_lookup)
        specs.append(
            FigureSpec(
                label=f"fig:{visual['slug']}",
                title=visual["title"],
                caption=visual["caption"],
                alt_text=visual["alt_text"],
                kind=FigureKind.PYTHON,
                output_path=f"output/figures/python/{visual['slug']}.png",
                source_section=section.relative_path,
                section_label=section.section_label,
                provenance={
                    "renderer": "python",
                    "renderer_id": visual["renderer"],
                    "source": "data/curriculum/",
                },
            )
        )

    for asset in HISTORICAL_ASSETS:
        section = _resolve_source_section(asset["source_section"], section_lookup)
        specs.append(
            FigureSpec(
                label=f"fig:{asset['slug']}",
                title=asset["title"],
                caption=asset["caption"],
                alt_text=asset["alt_text"],
                kind=FigureKind.HISTORICAL,
                output_path=f"output/figures/historical/{asset['slug']}.png",
                source_section=section.relative_path,
                section_label=section.section_label,
                provenance={
                    "source_url": asset["source_page"],
                    "asset_url": asset["asset_url"],
                    "usage": "Public Domain",
                    "source_agency": "U.S. Geological Survey",
                    "date": asset["date"],
                },
            )
        )

    for plate in AI_CONCEPTUAL_PLATES:
        section = _resolve_source_section(plate["source_section"], section_lookup)
        specs.append(
            FigureSpec(
                label=f"fig:{plate['slug']}",
                title=plate["title"],
                caption=plate["caption"],
                alt_text=plate["alt_text"],
                kind=FigureKind.AI_GENERATED,
                output_path=f"output/figures/ai/{plate['slug']}.png",
                source_section=section.relative_path,
                section_label=section.section_label,
                provenance={
                    "model": "local deterministic conceptual renderer",
                    "prompt": plate["prompt"],
                    "visual_text": plate.get("visual_text", ""),
                    "safety": "synthetic, non-operational, no real people, no real targets",
                },
            )
        )
    specs = [_with_informative_reader_text(spec, curriculum) for spec in specs]
    _validate_specs(specs)
    return specs


def render_figures(
    project_root: Path,
    curriculum: Curriculum,
    manifest: Any | None = None,
    *,
    allow_placeholder_figures: bool = False,
) -> Path:
    """Render all AGEINT figures and write ``figure_registry.json``."""
    if manifest is None:
        try:
            from .manuscript_manifest import build_manuscript_manifest
        except ImportError:  # pragma: no cover - direct script import
            from manuscript_manifest import build_manuscript_manifest  # type: ignore

        manifest = build_manuscript_manifest(curriculum)

    root = Path(project_root)
    figures_dir = root / "output" / "figures"
    figures_dir.mkdir(parents=True, exist_ok=True)
    specs = build_figure_specs(curriculum, manifest)
    for spec in specs:
        _render_figure_asset(root, curriculum, spec, allow_placeholder_figures=allow_placeholder_figures)
    for spec in specs:
        _ensure_registry_asset(root, spec, allow_placeholder_figures=allow_placeholder_figures)

    registry = {
        "project": "AGEINT",
        "schema_version": "1.0",
        "figure_count": len(specs),
        "figures": [spec.registry_entry(root) for spec in specs],
    }
    registry_path = figures_dir / "figure_registry.json"
    registry_path.write_text(json.dumps(registry, indent=2, sort_keys=True), encoding="utf-8")
    from output_docs import write_figures_output_docs

    write_figures_output_docs(figures_dir)
    return registry_path


def load_figure_registry(path: Path) -> dict[str, Any]:
    """Load a generated figure registry JSON file."""
    return cast(dict[str, Any], json.loads(path.read_text(encoding="utf-8")))


def figures_for_section(
    figures: Sequence[dict[str, Any] | FigureSpec],
    section_relative_path: str,
) -> list[dict[str, Any]]:
    """Return registry entries assigned to a manuscript section."""
    entries = [_entry(figure) for figure in figures]
    return [entry for entry in entries if entry["source_section"] == section_relative_path]


def figure_markdown(
    figure: dict[str, Any] | FigureSpec,
    *,
    project_root: Path,
    manuscript_output_dir: Path,
    section_relative_path: str,
) -> str:
    """Render a Pandoc-crossref image definition for ``figure``."""
    entry = _entry(figure)
    image_path = project_root / entry["output_path"]
    section_path = manuscript_output_dir / section_relative_path
    rel = _relative_posix(image_path, section_path.parent)
    caption = _markdown_escape(entry["caption"])
    return f"![{caption}]({rel}){{#{entry['label']}}}"


def _section_lookup(manifest: Any) -> dict[str, Any]:
    lookup: dict[str, Any] = {}
    for section in manifest.sections:
        lookup[section.relative_path] = section
        lookup[f"title:{section.title.lower()}"] = section
        if section.kind == "part":
            lookup[f"part:{section.title.lower()}"] = section
        if section.chapter_number is not None:
            lookup[f"chapter:{section.chapter_number}"] = section
        if section.appendix_letter is not None:
            lookup[f"appendix:{section.appendix_letter.lower()}"] = section
    return lookup


def _resolve_source_section(key: str, lookup: dict[str, Any]) -> Any:
    if key.startswith("part:"):
        normalized = f"part:{key.removeprefix('part:').lower()}"
        return lookup[normalized]
    return lookup[key]


def _validate_specs(specs: Sequence[FigureSpec]) -> None:
    labels = [spec.label for spec in specs]
    paths = [spec.output_path for spec in specs]
    if len(labels) != len(set(labels)):
        raise ValueError("AGEINT figure labels must be unique")
    if len(paths) != len(set(paths)):
        raise ValueError("AGEINT figure output paths must be unique")
    for spec in specs:
        if not spec.label.startswith("fig:"):
            raise ValueError(f"Figure label must start with fig:: {spec.label}")
        if not spec.caption or not spec.alt_text:
            raise ValueError(f"Figure {spec.label} needs caption and alt text")
        if not spec.output_path.startswith("output/figures/"):
            raise ValueError(f"Figure {spec.label} must render under output/figures")
        if not spec.provenance:
            raise ValueError(f"Figure {spec.label} needs provenance")


def _ensure_registry_asset(
    root: Path,
    spec: FigureSpec,
    *,
    allow_placeholder_figures: bool = False,
) -> None:
    """Ensure registry creation has a valid local PNG for every figure row."""
    asset = root / spec.output_path
    if not asset.is_file():
        placeholder_or_fail(
            asset,
            spec.title,
            "Figure asset was unavailable after rendering; generated deterministic fallback.",
            allow_placeholder_figures=allow_placeholder_figures,
        )
        _normalize_png_canvas(asset)
    _validate_png_asset(asset, spec)


def _render_figure_asset(
    root: Path,
    curriculum: Curriculum,
    spec: FigureSpec,
    *,
    allow_placeholder_figures: bool = False,
) -> None:
    """Render one figure through a validated temporary PNG before publishing it."""
    final_path = root / spec.output_path
    final_path.parent.mkdir(parents=True, exist_ok=True)
    # Mermaid content cache: skip the costly mmdc render when the diagram source
    # is byte-identical to the source that last produced a REAL PNG on disk. The
    # marker is written only after a verified real render, so plates never cache.
    cache_marker: Path | None = None
    cache_key: str | None = None
    if spec.kind is FigureKind.MERMAID:
        cache_key = _mermaid_source_hash(curriculum, spec)
        cache_marker = _mermaid_cache_marker(root, spec)
        if (
            cache_key is not None
            and final_path.is_file()
            and _png_asset_is_valid(final_path)
            and cache_marker.is_file()
            and cache_marker.read_text(encoding="utf-8").strip() == cache_key
        ):
            return
    temp_path = _temporary_png_path(final_path)
    if temp_path.exists():
        temp_path.unlink()
    real_render = True
    try:
        if spec.kind is FigureKind.MERMAID:
            real_render = render_mermaid_figure(
                root,
                curriculum,
                spec,
                temp_path,
                allow_placeholder_figures=allow_placeholder_figures,
            )
        elif spec.kind is FigureKind.PYTHON:
            render_python_figure(root, curriculum, spec, temp_path)
        elif spec.kind is FigureKind.HISTORICAL:
            _render_historical_figure(root, spec, temp_path)
        elif spec.kind is FigureKind.AI_GENERATED:
            _render_ai_concept_figure(root, spec, temp_path)
        else:  # pragma: no cover - enum coverage is enforced by spec tests
            raise ValueError(f"Unknown AGEINT figure kind: {spec.kind}")
        if not temp_path.is_file():
            real_render = False
            placeholder_or_fail(
                temp_path,
                spec.title,
                "Figure renderer completed without creating an asset; generated deterministic fallback.",
                allow_placeholder_figures=allow_placeholder_figures,
            )
        try:
            _normalize_png_canvas(temp_path)
        except (OSError, SyntaxError, ValueError) as exc:
            real_render = False
            placeholder_or_fail(
                temp_path,
                spec.title,
                f"Figure renderer produced an unreadable PNG during normalization: {exc}",
                allow_placeholder_figures=allow_placeholder_figures,
            )
            _normalize_png_canvas(temp_path)
        if not _png_asset_is_valid(temp_path):
            real_render = False
            placeholder_or_fail(
                temp_path,
                spec.title,
                "Figure renderer produced an invalid or missing asset; generated deterministic fallback.",
                allow_placeholder_figures=allow_placeholder_figures,
            )
            _normalize_png_canvas(temp_path)
        _validate_png_asset(temp_path, spec)
        temp_path.replace(final_path)
        try:
            _validate_png_asset(final_path, spec)
        except (OSError, SyntaxError, ValueError) as exc:
            real_render = False
            placeholder_or_fail(
                final_path,
                spec.title,
                f"Published figure asset was unreadable after replacement: {exc}",
                allow_placeholder_figures=allow_placeholder_figures,
            )
            _normalize_png_canvas(final_path)
            _validate_png_asset(final_path, spec)
        if cache_marker is not None:
            if real_render and cache_key is not None:
                cache_marker.write_text(cache_key, encoding="utf-8")
            elif cache_marker.exists():
                cache_marker.unlink()
    finally:
        if temp_path.exists():
            temp_path.unlink()
