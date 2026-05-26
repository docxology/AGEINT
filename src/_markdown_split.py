"""Generic Markdown splitting helpers for generated manuscript files."""

from __future__ import annotations

from pathlib import Path

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
    table_start = next((index for index, line in enumerate(lines) if line.startswith("| ")), -1)
    if table_start < 0 or table_start + 1 >= len(lines):
        return []
    heading = lines[0].removeprefix("## ").strip() if lines and lines[0].startswith("## ") else "continued"
    prefix = lines[:table_start]
    header = lines[table_start : table_start + 2]
    rows = [line for line in lines[table_start + 2 :] if line.startswith("| ")]
    if not rows:
        return []
    capacity = max(25, max_lines - len(prefix) - len(header) - 8)
    fragments: list[tuple[str, str]] = []
    for index in range(0, len(rows), capacity):
        chunk = rows[index : index + capacity]
        if index == 0:
            body = [*prefix, *header, *chunk]
        else:
            body = [f"## {heading} (continued {len(fragments) + 1})", *header, *chunk]
        fragments.append((path_with_suffix(relative_path, f"{len(fragments) + 1:02d}"), "\n".join(body).rstrip()))
    return fragments


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
