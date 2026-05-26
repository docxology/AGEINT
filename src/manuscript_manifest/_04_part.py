from __future__ import annotations

try:
    from ._appendix_support import appendix_body as _appendix_body
except ImportError:  # pragma: no cover - exercised by script-level imports
    from manuscript_manifest._appendix_support import appendix_body as _appendix_body  # type: ignore[no-redef]

def _apply_section_metadata(
    sections: list[ManuscriptSection],
    figures: list[dict[str, Any]],
) -> list[ManuscriptSection]:
    labeled = [section for section in sections if section.section_label]
    previous_by_path: dict[str, str] = {}
    next_by_path: dict[str, str] = {}
    for index, section in enumerate(labeled):
        if index > 0:
            previous_by_path[section.relative_path] = labeled[index - 1].section_label
        if index + 1 < len(labeled):
            next_by_path[section.relative_path] = labeled[index + 1].section_label

    refreshed: list[ManuscriptSection] = []
    for section in sections:
        section_figures = figures_for_section(figures, section.relative_path)
        previous_label = previous_by_path.get(section.relative_path, "")
        next_label = next_by_path.get(section.relative_path, "")
        context = dict(section.context)
        if section.kind == "chapter":
            context["SECTION_CROSSREFS"] = section_ref_list(
                [
                    "sec:curriculum_orientation",
                    section.parent_label,
                    previous_label,
                    next_label,
                ]
            )
        refreshed.append(
            ManuscriptSection(
                section.kind,
                section.title,
                section.relative_path,
                section.template_name,
                context,
                section.order,
                section_label=section.section_label,
                parent_label=section.parent_label,
                previous_label=previous_label,
                next_label=next_label,
                figure_labels=tuple(entry["label"] for entry in section_figures),
                chapter_number=section.chapter_number,
                appendix_letter=section.appendix_letter,
            )
        )
    return refreshed

def _visual_synthesis(
    project_root: Path,
    out_dir: Path,
    section: ManuscriptSection,
    manifest: ManuscriptManifest,
    figures: list[dict[str, Any]],
    *,
    render_relative_path: str | None = None,
) -> str:
    if not figures:
        return (
            "No figure registry was supplied for this render. Re-run "
            "`scripts/build_curriculum.py` to refresh figure references."
        )

    own_figures = figures_for_section(figures, section.relative_path)
    reference_labels = [entry["label"] for entry in own_figures]
    for label in _fallback_figure_labels(section):
        if label not in reference_labels:
            reference_labels.append(label)

    figure_refs = figure_ref_list(reference_labels)
    nav = _section_navigation(section)
    section_noun = {
        "chapter": "the module",
        "part": "the unit",
        "appendix": "the current appendix",
        "front": "the front-matter section",
        "bibliography": "the bibliography appendix",
    }.get(section.kind, "the current section")
    artifact_context = f" Artifact path: `{section.relative_path}`."
    definitions = [
        figure_markdown(
            entry,
            project_root=project_root,
            manuscript_output_dir=out_dir,
            section_relative_path=render_relative_path or section.relative_path,
        )
        for entry in own_figures
    ]
    figure_sentence = (
        f"Visual guide for {section_noun} {figure_refs} gives this section a concrete map of evidence flow, safety boundaries, and review artifacts.{artifact_context}"
        if figure_refs
        else f"Visual guide for {section_noun} uses the adjacent part, appendix, or curriculum overview figure to orient the section.{artifact_context}"
    )
    definition_block = "\n\n".join(definitions)
    parts = [figure_sentence]
    if nav:
        parts.append(nav)
    if definition_block:
        parts.append(definition_block)
    _ = manifest
    return "\n\n".join(parts)

def _fallback_figure_labels(section: ManuscriptSection) -> list[str]:
    if section.kind == "references":
        return []
    if section.relative_path == "abstract.md":
        return ["fig:ageint-curriculum-map"]
    if section.kind == "chapter" and section.parent_label.startswith("sec:part-"):
        part_slug = section.parent_label.removeprefix("sec:part-")
        return [f"fig:part-{part_slug}-module-map"]
    if section.kind == "appendix":
        return ["fig:ageint-safety-boundary-loop"]
    return []

def _section_navigation(section: ManuscriptSection) -> str:
    refs: list[str] = []
    if section.relative_path != "orientation.md":
        refs.append("sec:curriculum_orientation")
    if section.parent_label:
        refs.append(section.parent_label)
    if section.previous_label:
        refs.append(section.previous_label)
    if section.next_label:
        refs.append(section.next_label)
    if not refs:
        return ""
    return "Course path: " + section_ref_list(refs) + "."

def build_manuscript_manifest(
    curriculum: Curriculum,
    figures: list[dict[str, Any]] | None = None,
) -> ManuscriptManifest:
    """Build ordered semantic output sections from a parsed curriculum."""
    registry = _SlugRegistry()
    sections: list[ManuscriptSection] = []
    units: list[dict[str, Any]] = []
    appendix_files: list[str] = []
    chapter_files: dict[int, str] = {}
    order = 0

    sections.append(
        ManuscriptSection(
            "front",
            "Abstract",
            "abstract.md",
            "abstract.md",
            {},
            order,
            section_label="sec:abstract",
        )
    )
    order += 1
    sections.append(
        ManuscriptSection(
            "front",
            "Curriculum Orientation",
            "orientation.md",
            "orientation.md",
            {},
            order,
            section_label="sec:curriculum_orientation",
        )
    )
    order += 1

    for part in curriculum.parts:
        part_slug = registry.unique("parts", part["title"])
        part_dir = f"parts/{part_slug}"
        chapter_names: list[str] = []
        unit: dict[str, Any] = {
            "id": part_slug,
            "directory": part_dir,
            "chapters": chapter_names,
        }
        units.append(unit)
        part_label = _label("part", part_slug)
        part_section = ManuscriptSection(
            "part",
            part["title"],
            f"{part_dir}/unit_intro.md",
            "part.md",
            {
                "SECTION_TITLE": part["title"],
                "SECTION_LABEL": part_label,
                "SECTION_SUMMARY": _part_summary(part),
                "SECTION_ROWS": "",
            },
            order,
            section_label=part_label,
        )
        sections.append(part_section)
        order += 1
        for chapter in part["chapters"]:
            chapter_slug = registry.unique(part_slug, chapter["title"])
            relative_path = f"{part_dir}/{chapter_slug}.md"
            chapter_label = _label("chapter", chapter_slug)
            chapter_files[chapter["number"]] = relative_path
            chapter_names.append(f"{chapter_slug}.md")
            sections.append(
                ManuscriptSection(
                    "chapter",
                    chapter["title"],
                    relative_path,
                    "chapter.md",
                    {
                        "SECTION_TITLE": chapter["title"],
                        "SECTION_LABEL": chapter_label,
                        "SECTION_BODY": _chapter_body(chapter, part),
                        "SECTION_NAV_CONTEXT": (
                            f"{_chapter_topic_context(chapter, part)}; "
                            f"source path begins with {_chapter_source_context(chapter)}"
                        ),
                        "SECTION_CROSSREFS": "",
                    },
                    order,
                    section_label=chapter_label,
                    parent_label=part_label,
                    chapter_number=chapter["number"],
                )
            )
            order += 1

    refreshed: list[ManuscriptSection] = []
    for section in sections:
        if section.kind != "part":
            refreshed.append(section)
            continue
        part = next(item for item in curriculum.parts if item["title"] == section.title)
        context = dict(section.context)
        context["SECTION_ROWS"] = _part_chapter_rows(part, chapter_files)
        refreshed.append(
            ManuscriptSection(
                section.kind,
                section.title,
                section.relative_path,
                section.template_name,
                context,
                section.order,
                section_label=section.section_label,
                parent_label=section.parent_label,
                previous_label=section.previous_label,
                next_label=section.next_label,
                figure_labels=section.figure_labels,
            )
        )
    sections = refreshed

    for appendix in curriculum.appendices:
        appendix_slug = registry.unique("appendices", appendix["title"])
        appendix_label = _label("appendix", appendix_slug)
        file_name = f"{appendix_slug}.md"
        appendix_files.append(file_name)
        sections.append(
            ManuscriptSection(
                "appendix",
                appendix["title"],
                f"appendices/{file_name}",
                "appendix.md",
                {
                    "SECTION_TITLE": appendix["title"],
                    "SECTION_LABEL": appendix_label,
                    "SECTION_BODY": _appendix_body(appendix),
                    "SECTION_ROWS": appendix_rows(appendix),
                },
                order,
                section_label=appendix_label,
                appendix_letter=appendix["letter"],
            )
        )
        order += 1

    appendix_files.extend(["bibliography-atlas.md", "references.md"])
    sections.append(
        ManuscriptSection(
            "bibliography",
            "Bibliography Atlas",
            "bibliography-atlas.md",
            "bibliography_atlas.md",
            {},
            order,
            section_label="sec:bibliography_atlas",
        )
    )
    order += 1
    sections.append(
        ManuscriptSection(
            "references",
            "References",
            "references.md",
            "references.md",
            {},
            order,
        )
    )
    sections = _apply_section_metadata(sections, figures or [])
    return ManuscriptManifest(sections, units, appendix_files)

def _read_template(templates_dir: Path, template_name: str) -> str:
    template_path = templates_dir / template_name
    if template_path.is_file():
        return template_path.read_text(encoding="utf-8")
    return DEFAULT_TEMPLATES[template_name]
