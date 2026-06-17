from __future__ import annotations

import json
import re
import shutil
from pathlib import Path
from typing import Any

import yaml

from curriculum import Curriculum
from manuscript_injection import substitute_manuscript_text
from rendered_heading_support import add_heading_support, ensure_heading_support_in_tree
from rendered_reference_audit import (
    sanitize_rendered_section_title_mentions,
    section_title_rules,
)
from _markdown_split import (
    DEFAULT_MAX_TEXT_FILE_LINES,
    split_by_line_budget as _split_by_line_budget,
    split_h2_blocks as _split_h2_blocks,
)

from .types import (
    ManuscriptSection,
    ordering_config_yaml as _ordering_config_yaml,
    slugify as _slug,
)
from ._04_part import (
    build_manuscript_manifest,
    _read_template,
    _visual_synthesis,
)
from ._orientation_visuals import orientation_early_visual_context
from ._heading_titles import chapter_landmark_titles, chapter_scaffold_titles


MAX_TEXT_FILE_LINES = DEFAULT_MAX_TEXT_FILE_LINES


def _demote_chapter_continuation_headings(text: str) -> str:
    return re.sub(r"^## (.+ \(continued \d+\))$", r"### \1", text, flags=re.MULTILINE)


def _split_before_h3(text: str, heading: str) -> tuple[str, str]:
    match = re.search(rf"^###\s+{re.escape(heading)}\s*$", text, flags=re.MULTILINE)
    if match is None:
        return text.rstrip(), ""
    return text[: match.start()].rstrip(), text[match.start() :].rstrip()


def _split_assurance_fragments(section: ManuscriptSection, assurance_block: str) -> tuple[str, str, str]:
    scaffolds = chapter_scaffold_titles(section.title)
    evidence_block, governance_and_assessment = _split_before_h3(
        assurance_block,
        scaffolds["governance"],
    )
    governance_block, assessment_block = _split_before_h3(
        governance_and_assessment,
        scaffolds["assessment"],
    )
    return evidence_block, governance_block, assessment_block


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
    headings = chapter_landmark_titles(
        section.title,
        profile_title=section.context.get("CHAPTER_PROFILE_TITLE", ""),
        practice_lens_title=section.context.get("CHAPTER_PRACTICE_LENS_TITLE", ""),
    )
    assurance_block = block_map.get(headings["assurance"], "")
    evidence_block, governance_block, assessment_block = _split_assurance_fragments(
        section,
        assurance_block,
    )
    path = Path(section.relative_path)
    base_dir = path.parent / path.stem
    grouped = [
        (
            "00-overview.md",
            [
                lead,
                block_map.get(headings["frame"], ""),
            ],
        ),
        ("01-practice-studio.md", [block_map.get(headings["path"], "")]),
        ("02-evidence-contract.md", [evidence_block]),
        ("03-governance-boundary.md", [governance_block]),
        ("04-assessment-route.md", [assessment_block]),
    ]
    # Mid-chapter fragments (evidence-contract, governance-boundary) read
    # standalone but, unlike 00-overview/01-practice-studio/04-assessment-route,
    # carried no route back to the orientation atlas. Give each a one-line
    # wayfinding footer keyed to THIS module's own overview anchor, so it is
    # chapter-unique (not a repeated boilerplate paragraph) and routes the reader
    # home. Bare labels, not named sections in prose (signposting rule).
    overview_ref = f"[@{section.section_label}]" if section.section_label else ""
    lead = f"This module's overview is {overview_ref}; return to" if overview_ref else "Return to"
    wayfinding_footer = (
        f"**Where this sits.** {lead} the curriculum atlas [@sec:curriculum_orientation] "
        "for the reader paths, evidence map, and safety gates that govern this module."
    )
    wayfinding_fragments = {"02-evidence-contract.md", "03-governance-boundary.md"}
    fragments: list[tuple[str, str]] = []
    for file_name, parts in grouped:
        text = "\n\n".join(part for part in parts if part).rstrip()
        if text:
            for frag_path, fragment in _split_by_line_budget(
                (base_dir / file_name).as_posix(), text
            ):
                fragment = _demote_chapter_continuation_headings(fragment)
                # Every split of the mid-chapter fragments gets the back-link, not
                # just the last one (these blocks can exceed the line budget).
                if file_name in wayfinding_fragments:
                    fragment = f"{fragment}\n\n{wayfinding_footer}"
                fragments.append((frag_path, fragment))
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
    front_matter_options = _source_front_matter_options(base)
    if front_matter_options:
        base = _strip_top_level_yaml_block(base, "front_matter")
    config = (
        f"{base}\n\n"
        "figures:\n"
        "  registry: ../figures/figure_registry.json\n\n"
        "# Generated manuscript ordering\n"
        f"{_ordering_config_yaml(front_matter_files, units, appendix_files, front_matter_options=front_matter_options)}"
    )
    out_dir.joinpath("config.yaml").write_text(config, encoding="utf-8")


def _source_front_matter_options(config_text: str) -> dict[str, Any]:
    """Return non-ordering front-matter options declared by the source config."""
    if not config_text.strip():
        return {}
    payload = yaml.safe_load(config_text) or {}
    if not isinstance(payload, dict):
        return {}
    front_matter = payload.get("front_matter", {})
    if not isinstance(front_matter, dict):
        return {}
    generated_keys = {"include_front_matter", "files"}
    return {key: value for key, value in front_matter.items() if key not in generated_keys}


def _strip_top_level_yaml_block(config_text: str, key: str) -> str:
    """Remove one top-level source block before appending generated ordering."""
    lines = config_text.splitlines()
    stripped: list[str] = []
    index = 0
    block_header = f"{key}:"
    while index < len(lines):
        line = lines[index]
        if line.startswith(block_header):
            index += 1
            while index < len(lines):
                candidate = lines[index]
                if candidate and not candidate[0].isspace() and not candidate.lstrip().startswith("#"):
                    break
                index += 1
            continue
        stripped.append(line)
        index += 1
    return "\n".join(stripped).rstrip()


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
        early_visual_context = orientation_early_visual_context(
            root,
            out_dir,
            section,
            figures,
            render_relative_path=_first_fragment_path(section),
        )
        context = {
            **variables,
            **section.context,
            **early_visual_context,
            "VISUAL_SYNTHESIS": visual_synthesis,
        }
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
