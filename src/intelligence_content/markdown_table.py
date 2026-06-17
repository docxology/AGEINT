"""Shared Markdown table rendering for intelligence_content row builders."""

from __future__ import annotations

from collections.abc import Iterable, Mapping, Sequence


def table_cell(value: object) -> str:
    """Escape pipes and collapse whitespace for a Markdown table cell."""
    from markdown_cell import escape_table_cell

    return escape_table_cell(value)


def render_dict_table(
    headers: Sequence[str],
    rows: Iterable[Mapping[str, object]],
    field_keys: Sequence[str],
) -> str:
    """Render a Markdown table from row dicts and ordered field keys."""
    divider = "|" + "|".join("---" for _ in headers) + "|"
    lines = [
        "| " + " | ".join(headers) + " |",
        divider,
    ]
    for row in rows:
        lines.append(
            "| "
            + " | ".join(table_cell(row[key]) for key in field_keys)
            + " |"
        )
    return "\n".join(lines)
