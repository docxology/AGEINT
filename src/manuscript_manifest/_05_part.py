from __future__ import annotations

from _markdown_split import (
    DEFAULT_MAX_TEXT_FILE_LINES,
    split_by_line_budget as _split_by_line_budget,
    split_h2_blocks as _split_h2_blocks,
)

try:
    from ..rendered_heading_support import add_heading_support, ensure_heading_support_in_tree
except ImportError:  # pragma: no cover - exercised by script-level imports
    from rendered_heading_support import (  # type: ignore[no-redef]
        add_heading_support,
        ensure_heading_support_in_tree,
    )


MAX_TEXT_FILE_LINES = DEFAULT_MAX_TEXT_FILE_LINES


def _first_fragment_path(section: ManuscriptSection) -> str:
    if section.kind == "chapter":
        path = Path(section.relative_path)
        return (path.parent / path.stem / "00-overview.md").as_posix()
    if section.relative_path == "orientation.md":
        return "orientation/00-overview.md"
    if section.kind == "bibliography":
        return "appendices/bibliography-atlas/00-overview.md"
    return section.relative_path


def _chapter_fragments(section: ManuscriptSection, rendered: str) -> list[tuple[str, str]]:
    lead, blocks = _split_h2_blocks(rendered)
    block_map = {heading: block for heading, block in blocks}
    path = Path(section.relative_path)
    base_dir = path.parent / path.stem
    grouped = [
        (
            "00-overview.md",
            [
                lead,
                block_map.get("Figures and course links", ""),
                block_map.get("Textbook primer", ""),
                block_map.get("Learning outcomes", ""),
                block_map.get("Core vocabulary", ""),
            ],
        ),
        ("01-topic-lessons.md", [block_map.get("Topic lessons", "")]),
        (
            "02-worked-practice.md",
            [
                block_map.get("Worked safe example", ""),
                block_map.get("Practice sequence", ""),
                block_map.get("Knowledge check", ""),
            ],
        ),
        (
            "03-architecture-sources.md",
            [
                block_map.get("Module architecture", ""),
                block_map.get("Evidence and source canon", ""),
            ],
        ),
        (
            "04-research-governance.md",
            [
                block_map.get("Research-backed synthesis", ""),
                block_map.get("Agentic translation boundary", ""),
                block_map.get("Governance, rights, and assurance", ""),
            ],
        ),
        (
            "05-assessment-review.md",
            [
                block_map.get("Assessment artifacts and capstone pathway", ""),
                block_map.get("Refresh, safety, and source maps", ""),
                block_map.get("Review checklist", ""),
                block_map.get("Cross-links", ""),
            ],
        ),
    ]
    fragments: list[tuple[str, str]] = []
    for file_name, parts in grouped:
        text = "\n\n".join(part for part in parts if part).rstrip()
        if text:
            fragments.extend(_split_by_line_budget((base_dir / file_name).as_posix(), text))
    return fragments


def _front_or_appendix_fragments(
    section: ManuscriptSection,
    rendered: str,
    base_dir: str,
) -> list[tuple[str, str]]:
    lead, blocks = _split_h2_blocks(rendered)
    fragments: list[tuple[str, str]] = []
    for index, (heading, block) in enumerate(blocks):
        slug = _slug(heading)
        prefix = lead + "\n\n" if index == 0 and lead else ""
        path = f"{base_dir}/{index:02d}-{slug}.md"
        fragments.extend(_split_by_line_budget(path, prefix + block))
    if not blocks:
        fragments.append((f"{base_dir}/00-overview.md", rendered.rstrip()))
    return fragments


def _rendered_fragments(section: ManuscriptSection, rendered: str) -> list[tuple[str, str]]:
    if section.kind == "chapter":
        return _chapter_fragments(section, rendered)
    if section.relative_path == "orientation.md":
        return _front_or_appendix_fragments(section, rendered, "orientation")
    if section.kind == "bibliography":
        return _front_or_appendix_fragments(section, rendered, "appendices/bibliography-atlas")
    return _split_by_line_budget(section.relative_path, rendered)


def _write_generated_config(
    project_root: Path,
    out_dir: Path,
    front_matter_files: list[str],
    units: list[dict[str, Any]],
    appendix_files: list[str],
) -> None:
    source_config = project_root / "manuscript" / "config.yaml"
    base = source_config.read_text(encoding="utf-8").rstrip() if source_config.is_file() else ""
    config = (
        f"{base}\n\n"
        "# Generated figure registry\n"
        "figures:\n"
        "  registry: ../figures/figure_registry.json\n\n"
        "# Generated manuscript ordering\n"
        f"{_ordering_config_yaml(front_matter_files, units, appendix_files)}"
    )
    out_dir.joinpath("config.yaml").write_text(config, encoding="utf-8")


def render_manuscript(
    project_root: Path,
    curriculum: Curriculum,
    variables: dict[str, str],
    figure_registry: list[dict[str, Any]] | None = None,
) -> Path:
    """Render the resolved semantic manuscript tree under ``output/manuscript``."""
    figures = figure_registry or []
    manifest = build_manuscript_manifest(curriculum, figures)
    rendered_title_rules = section_title_rules(manifest.sections)
    root = Path(project_root)
    templates_dir = root / "manuscript" / "templates"
    out_dir = root / "output" / "manuscript"
    from _paths import remove_tree

    remove_tree(out_dir)
    out_dir.mkdir(parents=True)

    rendered_units = [
        {"id": unit["id"], "directory": unit["directory"], "chapters": []}
        for unit in manifest.units
    ]
    rendered_unit_by_dir = {unit["directory"]: unit for unit in rendered_units}
    rendered_front: list[str] = []
    rendered_appendices: list[str] = []

    for section in manifest.sections:
        template = _read_template(templates_dir, section.template_name)
        visual_synthesis = _visual_synthesis(
            root,
            out_dir,
            section,
            manifest,
            figures,
            render_relative_path=_first_fragment_path(section),
        )
        context = {**variables, **section.context, "VISUAL_SYNTHESIS": visual_synthesis}
        rendered, unresolved = substitute_manuscript_text(template, context, project_root=root)
        if unresolved:
            unresolved_keys = ", ".join(sorted(set(unresolved)))
            raise ValueError(f"Unresolved AGEINT manuscript tokens: {unresolved_keys}")
        rendered = sanitize_rendered_section_title_mentions(rendered, rendered_title_rules)
        rendered = add_heading_support(rendered, section.relative_path)
        fragments = _rendered_fragments(section, rendered)
        for relative_path, text in fragments:
            target = out_dir / relative_path
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(text.rstrip() + "\n", encoding="utf-8")

        if section.kind == "front":
            rendered_front.extend(relative_path for relative_path, _ in fragments)
        elif section.kind == "chapter":
            unit_dir = Path(section.relative_path).parent.as_posix()
            rendered_unit = rendered_unit_by_dir[unit_dir]
            rendered_unit["chapters"].extend(
                Path(relative_path).relative_to(unit_dir).as_posix()
                for relative_path, _ in fragments
            )
        elif section.kind in {"appendix", "bibliography"}:
            for relative_path, _ in fragments:
                path = Path(relative_path)
                rendered_appendices.append(path.relative_to("appendices").as_posix() if path.parts[0] == "appendices" else relative_path)
        elif section.kind == "references":
            rendered_appendices.extend(relative_path for relative_path, _ in fragments)

    legacy_bib = out_dir / ("references" + ".bib")
    if legacy_bib.exists():
        legacy_bib.unlink()
    for stale in out_dir.glob("references-*.bib"):
        stale.unlink()
    if "BIBTEX_REFERENCE_FILES" in variables:
        for name, text in json.loads(variables["BIBTEX_REFERENCE_FILES"]).items():
            (out_dir / name).write_text(text, encoding="utf-8")
    elif "BIBTEX_REFERENCES" in variables:
        legacy_bib.write_text(variables["BIBTEX_REFERENCES"], encoding="utf-8")

    _write_generated_config(root, out_dir, rendered_front, rendered_units, rendered_appendices)
    preamble = root / "manuscript" / "preamble.md"
    if preamble.is_file():
        shutil.copy2(preamble, out_dir / "preamble.md")
    from output_docs import write_manuscript_output_docs

    write_manuscript_output_docs(out_dir)
    ensure_heading_support_in_tree(out_dir)
    return out_dir
