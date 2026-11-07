"""Key-bound editorial annotations, without source-authored quotation claims.

Annotation order and length do not establish relevance. Preserve the supplied
context rather than rotating isolated sentences that may lose their antecedents.
"""

from __future__ import annotations


def curriculum_annotation(citation: str, note: str) -> str:
    """Label a complete curriculum note with the citation it actually describes."""
    return f"Curriculum annotation for {citation}: {note}" if note else ""


__all__ = ["curriculum_annotation"]
