from __future__ import annotations


def chapter_landmark_titles(chapter_title: str) -> dict[str, str]:
    """Return reader-facing H2 landmarks for a generated module chapter."""
    title = chapter_title.strip()
    return {
        "orientation": f"{title} orientation: reader task, learning outcomes, and core vocabulary",
        "practice": f"{title} practice studio: topic lessons, safe example, and knowledge check",
        "evidence": f"{title} evidence contract: source spine, verified anchors, and transfer architecture",
        "governance": f"{title} governance boundary: synthesis, agent assistance, rights, and assurance",
        "assessment": f"{title} assessment route: capstone artifacts, refresh duties, and reviewer challenges",
    }


__all__ = ["chapter_landmark_titles"]
