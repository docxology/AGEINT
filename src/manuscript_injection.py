"""Thin adapter to infrastructure manuscript variable injection."""

from __future__ import annotations

from pathlib import Path
from typing import Any

from template_resolver import ensure_template_repo_on_path


def substitute_manuscript_text(
    template: str,
    context: dict[str, Any],
    *,
    project_root: Path | None = None,
) -> tuple[str, list[str]]:
    """Substitute manuscript template tokens via infrastructure rendering."""
    if project_root is not None:
        ensure_template_repo_on_path(project_root)
    from infrastructure.rendering.manuscript_injection import (  # noqa: PLC0415
        substitute_manuscript_text as _substitute_manuscript_text,
    )

    return _substitute_manuscript_text(template, context)


__all__ = ["substitute_manuscript_text"]
