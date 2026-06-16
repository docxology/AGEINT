from __future__ import annotations

from pathlib import Path

from ._01_part import FigureSpec
from ._03c_control_matrix import draw_evidence_dashboard


def _render_claim_calibration_and_visual_semantics(output: Path, spec: FigureSpec) -> None:
    rows = [
        (
            "Claim language",
            (
                "proof, benchmark, p-value",
                "direct support or boundary",
                "fail unsupported strong claim",
                "claim_calibration_ok",
            ),
        ),
        (
            "Source strength",
            (
                "official, standard, scholarly",
                "weak guide context separated",
                "fail weak-only evidence",
                "support profiles",
            ),
        ),
        (
            "Formalisms",
            (
                "source-owned formula",
                "citation plus limitation",
                "no decorative equation",
                "formalism row",
            ),
        ),
        (
            "Visual semantics",
            (
                "semantic role",
                "unit and denominator",
                "interpretation limit",
                "registry schema 1.5",
            ),
        ),
        (
            "Artifact gate",
            (
                "report JSON/Markdown",
                "negative controls",
                "evidence manifest fails",
                "local-only readiness",
            ),
        ),
    ]
    draw_evidence_dashboard(
        output,
        spec.title,
        rows,
        ("Trigger", "Required evidence", "Failure rule", "Report surface"),
        "#bae6fd",
        "#dcfce7",
        subtitle="Claim calibration joins prose, source-support profiles, formalism checks, and figure semantics into one reviewer gate.",
        denominator="Current generated manuscript, figure registry, source-support profiles, and audit reports.",
        failure_path="Unsupported strong claims, weak-only evidence, missing limitations, or absent visual semantics fail closed",
        reviewer_action="Downgrade the claim, add direct support, bind the denominator, or revise the figure semantics before release.",
        footer="Source: AGEINT claim calibration and visual semantics audits | Local verifier telemetry, not a capability score.",
    )


__all__ = ["_render_claim_calibration_and_visual_semantics"]
