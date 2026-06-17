"""Canonical Markdown table-cell formatters.

Two deliberate policies, previously copied (and silently drifting) across seven
modules:

- :func:`escape_table_cell` keeps literal pipes by backslash-escaping them and
  collapses only newlines. Use for tables that should preserve a verbatim ``|``.
- :func:`plain_table_cell` collapses all whitespace and replaces ``|`` with
  ``/``. Use for plain-text, PDF-safe tables where a literal pipe is unwanted.

Call sites keep their existing private ``_table_cell``/``table_cell`` names as
thin delegates, so import paths are unchanged; the policy choice is now explicit
and a fix to one policy propagates to every site that shares it.
"""

from __future__ import annotations

import re


def escape_table_cell(value: object) -> str:
    """Backslash-escape pipes and collapse newlines for a Markdown table cell."""
    return str(value).replace("|", "\\|").replace("\n", " ").strip()


def plain_table_cell(value: object) -> str:
    """Collapse whitespace and replace pipes with ``/`` for a plain-text cell."""
    return re.sub(r"\s+", " ", str(value)).replace("|", "/").strip()


__all__ = ["escape_table_cell", "plain_table_cell"]
