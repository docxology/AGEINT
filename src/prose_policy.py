"""Shared reader-facing prose transforms for AGEINT titles and labels."""

from __future__ import annotations


def reader_source_title(value: str) -> str:
    """Replace scaffold-oriented wording in contributor-facing source titles."""
    return (
        value.replace("Scaffolding", "Documentation")
        .replace("scaffolding", "documentation")
        .replace("Scaffolds", "Workflows")
        .replace("scaffolds", "workflows")
        .replace("Scaffold", "Workflow")
        .replace("scaffold", "workflow")
    )


__all__ = ["reader_source_title"]
