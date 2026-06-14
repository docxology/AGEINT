"""Registry rows for claim-calibration and visual-semantics visuals."""

from __future__ import annotations

CLAIM_CALIBRATION_VISUALS: tuple[dict[str, object], ...] = (
    {
        "slug": "ageint-claim-calibration-and-visual-semantics",
        "title": "AGEINT Claim Calibration and Visual Semantics",
        "caption": (
            "The claim-calibration verifier figure makes the final RedTeam/Science "
            "hardening layer visible: high-risk manuscript claims are separated into "
            "empirical, governance, visualization, artifact-readiness, safety, and "
            "formalism lanes; each lane must show direct support or explicit boundary "
            "language; weak source-guide context cannot carry measured-performance or "
            "statistical claims alone; and figure metadata must state semantic role, "
            "evidence role, quantitative status, denominator, counting rule, and "
            "interpretation limit before the artifact-evidence manifest can pass."
        ),
        "alt_text": (
            "Control matrix linking claim calibration, source-support strength, "
            "formalism limits, visualization semantics, negative controls, and the "
            "artifact-evidence manifest gate."
        ),
        "renderer": "claim_calibration_and_visual_semantics",
        "source_section": "orientation.md",
        "semantic_role": "verifier_control_map",
        "evidence_role": "claim, source-strength, formalism, and visualization audit contract",
        "quantitative": False,
        "unit": "not_applicable",
        "denominator": "not_applicable",
        "counting_rule": "not_applicable",
        "interpretation_limit": (
            "This control map names verifier gates and negative controls; it is not a "
            "measured capability score, benchmark result, statistical finding, or "
            "evidence that AGEINT improves real-world analytic performance."
        ),
    },
)


__all__ = ["CLAIM_CALIBRATION_VISUALS"]
