from __future__ import annotations

from ._02b_mermaid import placeholder_or_fail, render_mermaid_figure




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
                    f"The {part['title']} module map connects lessons, practice artifacts, "
                    "and review gates for the part."
                ),
                alt_text=f"Mermaid diagram of modules in {part['title']}.",
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
                    "safety": "synthetic, non-operational, no real people, no real targets",
                },
            )
        )
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


def _placeholder_or_fail(
    output_path: Path,
    title: str,
    message: str,
    *,
    allow_placeholder_figures: bool,
) -> None:
    placeholder_or_fail(output_path, title, message, allow_placeholder_figures=allow_placeholder_figures)


def _ensure_registry_asset(
    root: Path,
    spec: FigureSpec,
    *,
    allow_placeholder_figures: bool = False,
) -> None:
    """Ensure registry creation has a valid local PNG for every figure row."""
    asset = root / spec.output_path
    if not asset.is_file():
        _placeholder_or_fail(
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
    temp_path = _temporary_png_path(final_path)
    if temp_path.exists():
        temp_path.unlink()
    try:
        if spec.kind is FigureKind.MERMAID:
            render_mermaid_figure(
                root,
                curriculum,
                spec,
                temp_path,
                allow_placeholder_figures=allow_placeholder_figures,
            )
        elif spec.kind is FigureKind.PYTHON:
            _render_python_figure(root, curriculum, spec, temp_path)
        elif spec.kind is FigureKind.HISTORICAL:
            _render_historical_figure(root, spec, temp_path)
        elif spec.kind is FigureKind.AI_GENERATED:
            _render_ai_concept_figure(root, spec, temp_path)
        else:  # pragma: no cover - enum coverage is enforced by spec tests
            raise ValueError(f"Unknown AGEINT figure kind: {spec.kind}")
        if not temp_path.is_file():
            _placeholder_or_fail(
                temp_path,
                spec.title,
                "Figure renderer completed without creating an asset; generated deterministic fallback.",
                allow_placeholder_figures=allow_placeholder_figures,
            )
        try:
            _normalize_png_canvas(temp_path)
        except (OSError, SyntaxError, ValueError) as exc:
            _placeholder_or_fail(
                temp_path,
                spec.title,
                f"Figure renderer produced an unreadable PNG during normalization: {exc}",
                allow_placeholder_figures=allow_placeholder_figures,
            )
            _normalize_png_canvas(temp_path)
        if not _png_asset_is_valid(temp_path):
            _placeholder_or_fail(
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
            _placeholder_or_fail(
                final_path,
                spec.title,
                f"Published figure asset was unreadable after replacement: {exc}",
                allow_placeholder_figures=allow_placeholder_figures,
            )
            _normalize_png_canvas(final_path)
            _validate_png_asset(final_path, spec)
    finally:
        if temp_path.exists():
            temp_path.unlink()


def _render_python_figure(
    root: Path,
    curriculum: Curriculum,
    spec: FigureSpec,
    output: Path | None = None,
) -> None:
    renderer_id = spec.provenance["renderer_id"]
    if output is None:
        output = root / spec.output_path
    if renderer_id == "citation_density":
        _render_citation_density(output, curriculum, spec)
    elif renderer_id == "source_quality_spine":
        _render_source_quality_spine(output, spec)
    elif renderer_id == "pattern_taxonomy":
        _render_pattern_taxonomy(output, curriculum, spec)
    elif renderer_id == "safety_boundary_loop":
        _render_safety_boundary_loop(output, spec)
    elif renderer_id == "section_composability_matrix":
        _render_section_composability_matrix(output, curriculum, spec)
    elif renderer_id == "reference_coverage":
        _render_reference_coverage(output, curriculum, spec)
    elif renderer_id == "source_verification_flow":
        _render_source_verification_flow(output, spec)
    elif renderer_id == "claim_ledger_flow":
        _render_claim_ledger_flow(output, spec)
    elif renderer_id == "ai_compliance_map":
        _render_ai_compliance_map(output, spec)
    elif renderer_id == "agent_evaluation_loop":
        _render_agent_evaluation_loop(output, spec)
    elif renderer_id == "cross_border_data_flow":
        _render_cross_border_data_flow(output, spec)
    elif renderer_id == "capstone_workflow":
        _render_capstone_workflow(output, spec)
    elif renderer_id == "safe_substitution_matrix":
        _render_safe_substitution_matrix(output, spec)
    elif renderer_id == "instructor_assessment_lifecycle":
        _render_instructor_assessment_lifecycle(output, spec)
    elif renderer_id == "accessibility_workflow":
        _render_accessibility_workflow(output, spec)
    elif renderer_id == "hria_dpia_map":
        _render_hria_dpia_map(output, spec)
    elif renderer_id == "procurement_oversight_loop":
        _render_procurement_oversight_loop(output, spec)
    elif renderer_id == "agent_incident_lifecycle":
        _render_agent_incident_lifecycle(output, spec)
    elif renderer_id == "bounded_autonomy_recoverability":
        _render_bounded_autonomy_recoverability(output, spec)
    elif renderer_id == "public_ai_register_lifecycle":
        _render_public_ai_register_lifecycle(output, spec)
    elif renderer_id == "ai_incident_reporting_loop":
        _render_ai_incident_reporting_loop(output, spec)
    elif renderer_id == "ot_definitive_architecture_record":
        _render_ot_definitive_architecture_record(output, spec)
    elif renderer_id == "data_lineage_registry":
        _render_data_lineage_registry(output, spec)
    elif renderer_id == "assessment_integrity_matrix":
        _render_assessment_integrity_matrix(output, spec)
    elif renderer_id == "adversarial_assurance_cycle":
        _render_adversarial_assurance_cycle(output, spec)
    elif renderer_id == "model_dataset_card":
        _render_model_dataset_card(output, spec)
    elif renderer_id == "transparency_notice_flow":
        _render_transparency_notice_flow(output, spec)
    elif renderer_id == "records_retention_audit":
        _render_records_retention_audit(output, spec)
    elif renderer_id == "release_change_control":
        _render_release_change_control(output, spec)
    elif renderer_id == "risk_exception_memo":
        _render_risk_exception_memo(output, spec)
    elif renderer_id == "learner_support_plan":
        _render_learner_support_plan(output, spec)
    elif renderer_id == "instructor_question_bank":
        _render_instructor_question_bank(output, spec)
    elif renderer_id == "remediation_backlog":
        _render_remediation_backlog(output, spec)
    else:
        raise ValueError(f"Unknown AGEINT figure renderer: {renderer_id}")


def _render_historical_figure(root: Path, spec: FigureSpec, output: Path | None = None) -> None:
    if output is None:
        output = root / spec.output_path
    output.parent.mkdir(parents=True, exist_ok=True)
    data = _download_bytes(spec.provenance["asset_url"])
    if data is None:
        _draw_text_plate(
            output,
            spec.title,
            "Official historical image could not be refreshed; provenance remains in registry.",
        )
        return
    image_mod, draw_mod, font_mod, ops_mod = _pil_modules()
    try:
        img_context = image_mod.open(io.BytesIO(data))
    except (OSError, ValueError):
        _draw_text_plate(
            output,
            spec.title,
            "Official historical image response was unreadable; provenance remains in registry.",
        )
        return
    with img_context as img:
        canvas = image_mod.new("RGB", (1600, 1000), "#111827")
        fitted = ops_mod.contain(img.convert("RGB"), (1520, 820))
        x = (1600 - fitted.width) // 2
        canvas.paste(fitted, (x, 40))
        draw = draw_mod.Draw(canvas)
        font = _font(font_mod, 34)
        small = _font(font_mod, 24)
        draw.rectangle((0, 870, 1600, 1000), fill="#f8fafc")
        draw.text((42, 890), spec.title, fill="#111827", font=font)
        draw.text((42, 940), "Source: USGS EROS | Usage: Public Domain", fill="#334155", font=small)
        canvas.save(output, format="PNG", optimize=True)


def _render_ai_concept_figure(root: Path, spec: FigureSpec, output: Path | None = None) -> None:
    prompt = spec.provenance["prompt"]
    _draw_concept_plate(output or root / spec.output_path, spec.title, prompt, spec.label)


def _render_citation_density(output: Path, curriculum: Curriculum, spec: FigureSpec) -> None:
    values = [len(chapter["citations"]) for chapter in curriculum.chapters]
    labels = [str(chapter["number"]) for chapter in curriculum.chapters]
    _draw_bar_chart(output, spec.title, labels, values, "#2563eb")
