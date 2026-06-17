from __future__ import annotations

from pathlib import Path
from typing import Any

from curriculum import Curriculum
from figures import figure_markdown, figures_for_section
from intelligence_content import practice_lens_for_titles, profile_for_titles
from markdown_refs import section_ref_list
from manuscript_templates import template_text
from manuscript_variables import appendix_rows

from .types import (
    ManuscriptManifest,
    ManuscriptSection,
    SlugRegistry as _SlugRegistry,
    section_label as _label,
)
from ._appendix_support import appendix_body as _appendix_body
from ._01_part import (
    _chapter_source_context_inline,
    _chapter_topic_context,
    _part_chapter_rows,
    _part_summary,
)
from ._03_part import _chapter_body
from ._canonical_reference import (
    canonical_claim_ledger_rows,
    canonical_competency_rubric_rows,
    canonical_mastery_rows,
    canonical_refresh_trigger_rows,
    canonical_safety_boundary,
)
from ._orientation_visuals import is_early_orientation_figure

# Rotated framing for the per-chapter learning-path links block. The structural links
# themselves (orientation, parent unit, previous/next module) are emitted as
# ``[@sec:...]`` crossrefs by SECTION_CROSSREFS; this prose only frames them.
# Rotating by part domain and embedding the chapter's own topic cluster keeps
# the framing from collapsing into one verbatim block stamped across every module.
_NAV_PROSE_VARIANTS = (
    "Read this module in sequence with the curriculum orientation, its parent unit, "
    "and the adjacent modules so the evidence behind {topic} carries forward intact. "
    "Source anchors for this module begin at {sources}.",
    "Use the cross-links below to place {topic} in the wider unit: the orientation "
    "sets the frame, the parent unit supplies the shared safety posture, and the "
    "neighbouring modules show what evidence enters and leaves. Lead sources: {sources}.",
    "These links keep {topic} paired with the orientation atlas, the parent unit, and "
    "the previous and next modules, so a reader can trace which claims and caveats are "
    "inherited rather than re-derived here. Anchored at {sources}.",
    "Follow the cross-links to move between {topic} and the rest of the curriculum "
    "without losing the source spine: orientation first, then the parent unit, then the "
    "modules on either side. Primary sources: {sources}.",
)


def _chapter_nav_prose(chapter: dict[str, Any], part: dict[str, Any]) -> str:
    """Return per-chapter cross-link prose that varies by part domain and topic.

    The structural navigation itself (orientation, parent unit, previous/next
    module) is emitted as ``[@sec:...]`` crossrefs by ``SECTION_CROSSREFS``; this
    prose only frames those links. Rotating by ``part['title']`` and embedding the
    chapter's actual topic cluster keeps the framing from collapsing into one
    verbatim block stamped across every module.
    """
    from intelligence_content.topic_rotation import template_index

    topic = _chapter_topic_context(chapter, part)
    sources = _chapter_source_context_inline(chapter)
    variant = _NAV_PROSE_VARIANTS[
        template_index(str(part["title"]), count=len(_NAV_PROSE_VARIANTS))
    ]
    return variant.format(topic=topic, sources=sources)


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
    if section.relative_path == "orientation.md":
        own_figures = [
            entry for entry in own_figures if not is_early_orientation_figure(entry)
        ]
    reference_labels = [entry["label"] for entry in own_figures]
    for label in _fallback_figure_labels(section):
        if label not in reference_labels:
            reference_labels.append(label)

    nav = _section_navigation(section)
    section_word = {
        "chapter": "module",
        "part": "unit",
        "appendix": "appendix",
        "front": "orientation",
        "bibliography": "bibliography appendix",
    }.get(section.kind, "section")
    # Join the figure references as a conjoined list ("Figure 1 and Figure 2",
    # "Figure 1, Figure 2, and Figure 3") instead of space-joined bare refs. Each
    # reference stays in its own [@fig:…] bracket so link-validation resolves it.
    _refs = [f"[@{label}]" for label in reference_labels]
    if len(_refs) <= 1:
        figure_group = _refs[0] if _refs else ""
    elif len(_refs) == 2:
        figure_group = f"{_refs[0]} and {_refs[1]}"
    else:
        figure_group = ", ".join(_refs[:-1]) + ", and " + _refs[-1]
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
        f"The {section_word} uses {figure_group} to map its evidence flow, safety boundaries, review artifacts, and refresh cues."
        if figure_group
        else f"The {section_word} is oriented by the adjacent part, appendix, or curriculum-overview figure."
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
    if section.relative_path == "method-assurance-reference.md":
        return ["fig:ageint-safety-boundary-loop"]
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
    return "Navigation links: " + section_ref_list(refs) + "."

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
            "Abstract: Synthetic Analytic Tradecraft contract",
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
            "Curriculum Orientation: reader paths, evidence maps, and safety gates",
            "orientation.md",
            "orientation.md",
            {},
            order,
            section_label="sec:curriculum_orientation",
        )
    )
    order += 1
    sections.append(
        ManuscriptSection(
            "front",
            "Method & Assurance Reference: claim evidence, safety gates, and refresh duties",
            "method-assurance-reference.md",
            "method_assurance_reference.md",
            {
                "CANONICAL_CLAIM_LEDGER_ROWS": canonical_claim_ledger_rows(),
                "CANONICAL_COMPETENCY_RUBRIC_ROWS": canonical_competency_rubric_rows(),
                "CANONICAL_REFRESH_TRIGGER_ROWS": canonical_refresh_trigger_rows(),
                "CANONICAL_MASTERY_ROWS": canonical_mastery_rows(),
                "CANONICAL_SAFETY_BOUNDARY": canonical_safety_boundary(),
            },
            order,
            section_label="sec:method-assurance-reference",
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
            profile = profile_for_titles(str(part["title"]), str(chapter["title"]), chapter=chapter)
            lens = practice_lens_for_titles(str(part["title"]), str(chapter["title"]), chapter=chapter)
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
                        "SECTION_NAV_PROSE": _chapter_nav_prose(chapter, part),
                        "SECTION_CROSSREFS": "",
                        "CHAPTER_PROFILE_TITLE": profile.title,
                        "CHAPTER_PRACTICE_LENS_TITLE": lens.title,
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
            "Bibliography Atlas: source keys, refresh evidence, and citation workflow",
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
    return template_text(template_name)
