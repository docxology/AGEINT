"""Thin adapter to infrastructure manuscript variable injection."""

from __future__ import annotations

from pathlib import Path
import re
from typing import Any

from template_resolver import ensure_template_repo_on_path

_TOKEN_RE = re.compile(r"\{\{([A-Z][A-Z0-9_]*)\}\}")


def substitute_manuscript_text(template: str, context: dict[str, Any], *, project_root: Path | None = None) -> tuple[str, list[str]]:
    """Substitute manuscript template tokens via infrastructure rendering or standalone fallback."""
    if project_root is not None:
        ensure_template_repo_on_path(project_root)
    try:
        from infrastructure.rendering.manuscript_injection import (  # type: ignore[import-not-found]  # noqa: PLC0415
            substitute_manuscript_text as _substitute_manuscript_text,
        )

        return _substitute_manuscript_text(template, context)
    except (ImportError, ModuleNotFoundError):
        unresolved: list[str] = []

        def _replace(match: re.Match[str]) -> str:
            key = match.group(1)
            if key in context:
                return str(context[key])
            unresolved.append(key)
            return match.group(0)

        resolved = _TOKEN_RE.sub(_replace, template)
        return resolved, unresolved


__all__ = ["substitute_manuscript_text"]
