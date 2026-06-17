from __future__ import annotations

from pathlib import Path
from typing import Any

from figures import figure_markdown, figures_for_section

from .types import ManuscriptSection


ORIENTATION_EARLY_VISUAL_SLOTS = {
    "ORIENTATION_OPENING_VISUALS": ("opening_route_compass",),
    "ORIENTATION_TRADECRAFT_VISUALS": ("tradecraft_workbench",),
    "ORIENTATION_SOURCE_CONSTELLATION_VISUALS": ("source_constellation",),
    "ORIENTATION_ASSURANCE_VISUALS": ("assurance_cockpit",),
}
_EARLY_ORIENTATION_SLOT_VALUES = frozenset(
    slot for slots in ORIENTATION_EARLY_VISUAL_SLOTS.values() for slot in slots
)
_ORIENTATION_SLOT_BRIDGES = {
    "ORIENTATION_OPENING_VISUALS": (
        "The opening route visual turns the atlas handoff into a concrete reader "
        "choice: select the role, keep the evidence trace, and move to the next "
        "section with the right verifier question already named."
    ),
    "ORIENTATION_TRADECRAFT_VISUALS": (
        "The workbench visual makes the Synthetic Analytic Tradecraft thesis "
        "inspectable by showing how safe fixtures become reviewable claim packets "
        "rather than operational instructions; it is a classroom artifact route, not "
        "evidence of field capability."
    ),
    "ORIENTATION_SOURCE_CONSTELLATION_VISUALS": (
        "The source constellation visual ties the runtime inventory back to the "
        "evidence families and lanes that govern source choice, caveat language, "
        "and refresh duties."
    ),
    "ORIENTATION_ASSURANCE_VISUALS": (
        "The assurance cockpit visual summarizes how a reader should interpret "
        "local build telemetry: useful for routing review effort, but bounded by "
        "the generated audits that carry the authoritative pass, warn, or block state."
    ),
}


def orientation_early_visual_context(
    project_root: Path,
    out_dir: Path,
    section: ManuscriptSection,
    figures: list[dict[str, Any]],
    *,
    render_relative_path: str,
) -> dict[str, str]:
    if section.relative_path != "orientation.md":
        return {}
    return {
        token: _orientation_early_visual_block(
            project_root,
            out_dir,
            section,
            figures,
            token,
            slots,
            render_relative_path=render_relative_path,
        )
        for token, slots in ORIENTATION_EARLY_VISUAL_SLOTS.items()
    }


def is_early_orientation_figure(entry: dict[str, Any]) -> bool:
    return _entry_orientation_slot(entry) in _EARLY_ORIENTATION_SLOT_VALUES


def _orientation_early_visual_block(
    project_root: Path,
    out_dir: Path,
    section: ManuscriptSection,
    figures: list[dict[str, Any]],
    token: str,
    slots: tuple[str, ...],
    *,
    render_relative_path: str,
) -> str:
    entries = [
        entry
        for entry in figures_for_section(figures, section.relative_path)
        if _entry_orientation_slot(entry) in slots
    ]
    if not entries:
        return ""
    refs = [f"[@{entry['label']}]" for entry in entries]
    if len(refs) == 1:
        figure_group = refs[0]
    else:
        figure_group = ", ".join(refs[:-1]) + ", and " + refs[-1]
    definitions = [
        figure_markdown(
            entry,
            project_root=project_root,
            manuscript_output_dir=out_dir,
            section_relative_path=render_relative_path,
        )
        for entry in entries
    ]
    return "\n\n".join(
        [
            f"{_ORIENTATION_SLOT_BRIDGES[token]} See {figure_group}.",
            *definitions,
        ]
    )


def _entry_orientation_slot(entry: dict[str, Any]) -> str:
    provenance = entry.get("provenance", {})
    if not isinstance(provenance, dict):
        return ""
    return str(provenance.get("orientation_slot", ""))


__all__ = ["is_early_orientation_figure", "orientation_early_visual_context"]
