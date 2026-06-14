"""Generic Markdown splitting helpers for generated manuscript files."""

from __future__ import annotations

from pathlib import Path
import re

DEFAULT_MAX_TEXT_FILE_LINES = 500


def path_with_suffix(relative_path: str, suffix: str) -> str:
    path = Path(relative_path)
    return (path.parent / f"{path.stem}-{suffix}{path.suffix}").as_posix()


def split_h2_blocks(text: str) -> tuple[str, list[tuple[str, str]]]:
    lead: list[str] = []
    blocks: list[tuple[str, str]] = []
    current_heading = ""
    current: list[str] = []
    for line in text.splitlines():
        if line.startswith("## ") and not line.startswith("### "):
            if current:
                blocks.append((current_heading, "\n".join(current).rstrip()))
            current_heading = line.removeprefix("## ").strip()
            current = [line]
            continue
        if current:
            current.append(line)
        else:
            lead.append(line)
    if current:
        blocks.append((current_heading, "\n".join(current).rstrip()))
    return "\n".join(lead).rstrip(), blocks


def line_count(text: str) -> int:
    return len(text.splitlines())


def split_long_table(
    relative_path: str,
    text: str,
    *,
    max_lines: int = DEFAULT_MAX_TEXT_FILE_LINES,
) -> list[tuple[str, str]]:
    lines = text.splitlines()
    table_spans = _pipe_table_spans(lines)
    if not table_spans:
        return []
    table_start, table_end = max(table_spans, key=lambda span: span[1] - span[0])
    heading = lines[0].removeprefix("## ").strip() if lines and lines[0].startswith("## ") else "continued"
    prefix = lines[:table_start]
    header = lines[table_start : table_start + 2]
    rows = lines[table_start + 2 : table_end]
    suffix = lines[table_end:]
    if not rows:
        return []
    first_capacity = max_lines - len(prefix) - len(header) - 2
    if first_capacity < 1:
        return []
    continued_capacity = max_lines - len(header) - 3
    if continued_capacity < 1:
        return []
    fragments: list[tuple[str, str]] = []
    index = 0
    while index < len(rows):
        capacity = first_capacity if index == 0 else continued_capacity
        chunk = rows[index : index + capacity]
        if index == 0:
            body = [*prefix, *header, *chunk]
        else:
            body = [f"## {heading} (continued {len(fragments) + 1})", *header, *chunk]
        index += len(chunk)
        if index >= len(rows) and suffix and len(body) + len(suffix) <= max_lines:
            body.extend(suffix)
        fragments.append((path_with_suffix(relative_path, f"{len(fragments) + 1:02d}"), "\n".join(body).rstrip()))
    if suffix and not fragments[-1][1].splitlines()[-len(suffix) :] == suffix:
        fragments.append(
            (
                path_with_suffix(relative_path, f"{len(fragments) + 1:02d}"),
                "\n".join([f"## {heading} (continued {len(fragments) + 1})", *suffix]).rstrip(),
            )
        )
    return fragments


def _pipe_table_spans(lines: list[str]) -> list[tuple[int, int]]:
    spans: list[tuple[int, int]] = []
    index = 0
    while index < len(lines) - 1:
        if _is_pipe_table_row(lines[index]) and _is_pipe_table_separator(lines[index + 1]):
            start = index
            index += 2
            while index < len(lines) and _is_pipe_table_row(lines[index]):
                index += 1
            spans.append((start, index))
            continue
        index += 1
    return spans


def _is_pipe_table_row(line: str) -> bool:
    stripped = line.strip()
    return stripped.startswith("|") and stripped.endswith("|")


def _is_pipe_table_separator(line: str) -> bool:
    stripped = line.strip().strip("|")
    cells = [cell.strip() for cell in stripped.split("|")]
    return bool(cells) and all(re.fullmatch(r":?-{3,}:?", cell) for cell in cells)


def split_at_h3(
    relative_path: str,
    text: str,
    *,
    max_lines: int = DEFAULT_MAX_TEXT_FILE_LINES,
) -> list[tuple[str, str]]:
    lines = text.splitlines()
    first_h3 = next((index for index, line in enumerate(lines) if line.startswith("### ")), -1)
    if first_h3 < 0:
        return []
    heading = lines[0].removeprefix("## ").strip() if lines and lines[0].startswith("## ") else "continued"
    lead = lines[:first_h3]
    h3_blocks: list[list[str]] = []
    current: list[str] = []
    for line in lines[first_h3:]:
        if line.startswith("### ") and current:
            h3_blocks.append(current)
            current = [line]
        else:
            current.append(line)
    if current:
        h3_blocks.append(current)

    fragments: list[tuple[str, str]] = []
    current_lines = list(lead)
    for block in h3_blocks:
        if len(current_lines) + len(block) > max_lines - 8 and current_lines != lead:
            fragments.append(
                (
                    path_with_suffix(relative_path, f"{len(fragments) + 1:02d}"),
                    "\n".join(current_lines).rstrip(),
                )
            )
            current_lines = [f"## {heading} (continued {len(fragments) + 1})"]
        current_lines.extend(block)
    if current_lines:
        fragments.append(
            (
                path_with_suffix(relative_path, f"{len(fragments) + 1:02d}"),
                "\n".join(current_lines).rstrip(),
            )
        )
    return fragments


def split_by_line_budget(
    relative_path: str,
    text: str,
    *,
    max_lines: int = DEFAULT_MAX_TEXT_FILE_LINES,
) -> list[tuple[str, str]]:
    text = text.rstrip()
    if line_count(text) <= max_lines:
        return [(relative_path, text)]
    for splitter in (split_at_h3, split_long_table):
        fragments = splitter(relative_path, text, max_lines=max_lines)
        if fragments and all(line_count(fragment) <= max_lines for _, fragment in fragments):
            return fragments
    lines = text.splitlines()
    fragments: list[tuple[str, str]] = []
    for index in range(0, len(lines), max_lines - 5):
        fragments.append(
            (
                path_with_suffix(relative_path, f"{len(fragments) + 1:02d}"),
                "\n".join(lines[index : index + max_lines - 5]).rstrip(),
            )
        )
    return fragments
