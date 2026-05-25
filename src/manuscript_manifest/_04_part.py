from __future__ import annotations

def _import_prior_parts(*module_names: str) -> None:
    import importlib

    for module_name in module_names:
        mod = importlib.import_module(f".{module_name}", __package__)
        globals().update({k: v for k, v in vars(mod).items() if not k.startswith("__")})

_import_prior_parts("_01_part", "_02_part", "_03_part")

def _appendix_topic_context(appendix: dict[str, Any], *, limit: int = 2) -> str:
    """Return an appendix-specific source-item cue without repeating its generated title."""

    titles = [
        re.sub(r"^[A-Z]\.\d+\s+", "", str(item.get("title", "")).strip())
        for item in appendix.get("items", [])[:limit]
    ]
    titles = [title for title in titles if title]
    if not titles:
        return "the appendix source-item set"
    return "; ".join(titles)

def _appendix_body(appendix: dict[str, Any]) -> str:
    letter = appendix["letter"]
    topic_context = _appendix_topic_context(appendix)
    specialized = ""
    if letter == "H":
        specialized = (
            "\n\n## Source verification workflow\n\n"
            "The source-verification and claim-ledger workbook preserves "
            "`ageint001` through `ageint231`, appends new references after "
            "the locked range, and records lane, tier, checked date, "
            "verification method, claim scope, refresh cadence, and refresh "
            "trigger for every curated anchor.\n\n"
            f"{source_lane_rows()}\n\n"
            "## Source refresh evidence\n\n"
            f"{data_lineage_registry_rows()}\n\n"
            "## HRIA/DPIA evidence bridge\n\n"
            f"{hria_dpia_worksheet_rows()}"
        )
    elif letter == "I":
        specialized = (
            "\n\n## Instructor capstone workflow\n\n"
            "The instructor capstone, rubric, and red-team review pack binds "
            "each student artifact to source verification, safe substitution, "
            "rights review, assurance, and debrief evidence.\n\n"
            f"{capstone_scaffold_rows()}\n\n"
            "## Safe artifact rows\n\n"
            f"{safe_substitution_rows()}\n\n"
            "## Assessment lifecycle evidence\n\n"
            f"{assessment_integrity_rows()}\n\n"
            "## Adversarial review evidence\n\n"
            f"{adversarial_assurance_rows()}"
        )

    return "\n".join(
        [
            (
                "The current appendix is an evidence workbook for "
                "reusable classroom methods. It is educational and non-operational: "
                "examples remain synthetic, defensive, lawful, and bounded to owned "
                f"labs, public sources, or tabletop exercises. Source-item focus: {topic_context}."
            ),
            "",
            "## Purpose",
            (
                "The current appendix supports a reusable methods "
                "workbook. Each source item is treated as a reviewable "
                f"classroom artifact rather than an operational instruction; examples begin with {topic_context}."
            ),
            "",
            "## Allowed inputs",
            (
                "Allowed inputs for the current appendix are public official or scholarly sources, "
                "standards text, instructor-provided excerpts, synthetic "
                "datasets, owned-lab logs, toy examples, and generated rubrics "
                f"that expose their provenance for {topic_context}."
            ),
            "",
            "## Excluded actions",
            (
                "Excluded actions for the current appendix are unauthorized collection, private-data "
                "processing, credential use, contact with real targets, live "
                "system interaction, exploit execution, deception, unsafe "
                f"cyber-physical action, or external deployment while handling {topic_context}."
            ),
            "",
            "## Expected artifacts",
            (
                "Expected appendix artifacts are a purpose statement, allowed-inputs "
                "card, excluded-actions card, source-lane map, provenance "
                "record, claim ledger, safe-substitution note, output schema, "
                f"review rubric, and capstone handoff memo for {topic_context}."
            ),
            "",
            "## Safe artifact schema",
            "| Field | Required evidence | Reject condition |",
            "|---|---|---|",
            "| Purpose | lawful educational, governance, research, or defensive purpose | vague operational objective or missing authority |",
            "| Inputs | public, official, scholarly, synthetic, owned-lab, or instructor-provided material | private data, live target data, credentialed access, or unclear provenance |",
            "| Transform | summary, comparison, rubric scoring, tabletop simulation, or audit review | collection expansion, external action, or unsafe system interaction |",
            "| Output | memo, matrix, checklist, ledger, rubric, or debrief packet | deployable procedure, target package, or automated action plan |",
            "| Reviewer | human reviewer, approval gate, revision note, and refresh owner | anonymous ownership or no escalation path |",
            "",
            "## Input/output contract",
            "| Contract term | Input rule | Output rule |",
            "|---|---|---|",
            "| Source identity | retain `ageintNNN`, title, URL, and checked status | cite with Pandoc keys and avoid pasted raw URLs in prose |",
            "| Accessibility | include plain-language labels, table headers, and figure alternatives | reject inaccessible figures, unlabeled tables, or single-modality evidence |",
            "| Rights | identify affected groups, safeguards, and residual risk | preserve privacy, equality, access, contestability, and redress notes |",
            "| Tooling | use allowlisted tools, visible prompts, logs, and stop conditions | keep outputs non-operational, reversible, and human-reviewed |",

            "| Refresh | record source, policy, standard, incident, or assessment trigger | assign an owner and date for revalidation |",
            "",
            "## Failure cases",
            "| Failure case | Signal | Required response |",
            "|---|---|---|",
            "| Source laundering | claim cites an agent summary instead of a verified source | rebuild the claim ledger from direct sources |",
            "| Boundary drift | exercise starts asking for live targets, private data, or external action | stop, substitute synthetic inputs, and document the block |",
            "| Accessibility gap | learner cannot inspect, navigate, or complete the artifact | remediate and retest before reuse |",
            "| Rights gap | affected group, safeguard, or redress path is missing | run HRIA/DPIA worksheet and escalate unresolved risk |",
            "| Vendor opacity | tool owner, data use, logs, or exit path is unknown | replace tool or pause until procurement evidence exists |",
            "",
            "## Evidence package schemas",
            "Model and dataset card:",
            "",
            model_dataset_card_rows(),
            "",
            "Transparency notice:",
            "",
            transparency_notice_rows(),
            "",
            "Records retention and audit trail:",
            "",
            retention_audit_rows(),
            "",
            "Release and change-control gate:",
            "",
            release_change_control_rows(),
            "",
            "Risk exception memo:",
            "",
            risk_exception_rows(),
            "",
            "Learner support and accommodation plan:",
            "",
            learner_support_rows(),
            "",
            "Instructor question bank:",
            "",
            question_bank_rows(),
            "",
            "Remediation backlog:",
            "",
            remediation_backlog_rows(),
            "",
            "## Rubric scoring bands",
            "| Band | Evidence standard | Disposition |",
            "|---|---|---|",
            "| 4 - ready | source identity, accessibility, rights, safety, and reviewer evidence are complete | may be reused after normal refresh review |",
            "| 3 - revise | one evidence field is incomplete but risk is bounded and remediable | revise before reuse |",
            "| 2 - hold | multiple evidence fields are incomplete or ownership is unclear | hold for instructor and assurance review |",
            "| 1 - reject | unsafe action, private data, inaccessible artifact, or unverified claim appears | reject and rebuild from safe inputs |",
            "",
            "## Refresh evidence",
            "| Evidence item | Refresh trigger | Retained proof |",
            "|---|---|---|",
            "| Source lane | official source, standard, or legal text changes | checked-as-of date and source note |",
            "| Safety treatment | operational wording or unsafe motif appears | safe-substitution decision and blocked context |",
            "| Accessibility | WCAG, UDL, or institutional accessibility duty changes | defect log, retest result, and owner |",
            "| Rights | privacy, human-rights, public transparency, or education guidance changes | HRIA/DPIA revision note |",
            "| Vendor/tool | contract, data-use, incident, or model capability changes | procurement packet and incident review |",
            "",
            "## Validation rubric",
            "| Criterion | Passing evidence |",
            "|---|---|",
            "| Source identity | existing `ageintNNN` keys remain stable or new references are append-only |",
            "| Verification | official, standards, public-domain, or scholarly URL is checked directly |",
            "| Safety | method is converted into tabletop, audit, governance, or synthetic-data treatment |",
            "| Reproducibility | another reviewer can rebuild the artifact from retained inputs |",
            "| Rights review | privacy, IP, human-rights, workforce, and education impacts are considered where relevant |",
            "",
            "## Debrief protocol",
            (
                "Debrief by naming what the artifact proves, what it does not "
                "prove, what source changed, what risk was avoided by safe "
                "substitution, what human approval is still required, and when "
                "the appendix should be refreshed."
            ),
            "",
            specialized.strip(),
        ]
    ).strip()

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
