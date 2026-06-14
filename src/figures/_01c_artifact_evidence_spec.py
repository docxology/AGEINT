"""Registry rows for verifier-first artifact-evidence visuals."""

from __future__ import annotations

ARTIFACT_EVIDENCE_VISUALS: tuple[dict[str, str], ...] = (
    {
        "slug": "ageint-artifact-evidence-control-loop",
        "title": "AGEINT Artifact Evidence Control Loop",
        "caption": (
            "Source-backed control-loop figure showing how AGEINT binds source-owned "
            "inputs, rebuilt manuscript files, citation inventory, figure registry "
            "metadata, PDF annotation audits, and current evidence reports so validators "
            "cannot certify a stale or partially copied artifact as complete."
        ),
        "alt_text": (
            "Control matrix linking AGEINT source inputs, build outputs, citation counts, "
            "figure checks, PDF links, and evidence reports to validators and negative controls."
        ),
        "renderer": "artifact_evidence_control_loop",
        "source_section": "orientation.md",
    },
)
