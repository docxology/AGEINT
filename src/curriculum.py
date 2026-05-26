"""Parsing and query helpers for the AGEINT curriculum."""

from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
import re
from typing import Any

from _slug import curriculum_chapter_dir_name, curriculum_part_dir_name, slug_for_path

PATTERN_REGISTRY_CHAPTER_NUMBER = 32

ROMAN = {
    "I": 1,
    "II": 2,
    "III": 3,
    "IV": 4,
    "V": 5,
    "VI": 6,
    "VII": 7,
    "VIII": 8,
    "IX": 9,
    "X": 10,
    "XI": 11,
    "XII": 12,
    "XIII": 13,
    "XIV": 14,
    "XV": 15,
    "XVI": 16,
}


@dataclass(frozen=True)
class Curriculum:
    """Loaded curriculum payload with convenience accessors."""

    payload: dict[str, Any]

    @property
    def stats(self) -> dict[str, int]:
        return dict(self.payload["stats"])

    @property
    def parts(self) -> list[dict[str, Any]]:
        return list(self.payload["parts"])

    @property
    def chapters(self) -> list[dict[str, Any]]:
        return [chapter for part in self.parts for chapter in part["chapters"]]

    @property
    def patterns(self) -> list[dict[str, Any]]:
        return list(self.payload["patterns"])

    @property
    def appendices(self) -> list[dict[str, Any]]:
        return list(self.payload["appendices"])

    @property
    def references(self) -> list[dict[str, Any]]:
        return list(self.payload["references"])

    def part(self, number: int) -> dict[str, Any]:
        for part in self.parts:
            if part["number"] == number:
                return part
        raise KeyError(f"No part {number}")

    def chapter(self, number: int) -> dict[str, Any]:
        for chapter in self.chapters:
            if chapter["number"] == number:
                return chapter
        raise KeyError(f"No chapter {number}")

    def appendix(self, letter: str) -> dict[str, Any]:
        normalized = letter.upper()
        for appendix in self.appendices:
            if appendix["letter"] == normalized:
                return appendix
        raise KeyError(f"No appendix {letter}")

    def reference(self, key_or_number: str | int) -> dict[str, Any]:
        if isinstance(key_or_number, int):
            key = f"ageint{key_or_number:03d}"
        else:
            key = key_or_number
            if key.isdigit():
                key = f"ageint{int(key):03d}"
        for reference in self.references:
            if reference["key"] == key or reference["number"] == key_or_number:
                return reference
        raise KeyError(f"No reference {key_or_number}")

    def citations_for_chapter(self, number: int) -> list[str]:
        return [f"ageint{n:03d}" for n in self.chapter(number)["citations"]]

    def citation_keys(self) -> list[str]:
        return [reference["key"] for reference in self.references]

    def part_titles(self) -> list[str]:
        return [part["title"] for part in self.parts]


def _strip_markdown(value: str) -> str:
    value = re.sub(r"\[\^(\d+)\]", "", value)
    return value.replace("**", "").replace("*", "").strip()


def parse_curriculum_guide(text: str) -> dict[str, Any]:
    """Parse the SIST guide into parts, chapters, appendices, patterns, and references."""
    lines = text.splitlines()
    references: dict[int, dict[str, Any]] = {}
    in_refs = False
    for line in lines:
        if line.strip() == "## References":
            in_refs = True
            continue
        if not in_refs:
            continue
        match = re.match(r"^(\d+)\. \[(.*?)\]\((.*?)\)(?: - (.*))?$", line.strip())
        if match:
            number = int(match.group(1))
            references[number] = {
                "number": number,
                "key": f"ageint{number:03d}",
                "title": match.group(2).strip(),
                "url": match.group(3).strip(),
                "note": (match.group(4) or "").strip(),
            }

    parts: list[dict[str, Any]] = []
    appendices: list[dict[str, Any]] = []
    current_part: dict[str, Any] | None = None
    current_chapter: dict[str, Any] | None = None
    current_appendix: dict[str, Any] | None = None
    mode = "toc"
    for line_no, line in enumerate(lines, 1):
        if line.startswith("## CODE SNIPPETS"):
            mode = "appendix"
            current_part = None
            current_chapter = None
            continue
        if line.startswith("## COMPREHENSIVE"):
            break
        if mode == "toc":
            part_match = re.match(r"^### PART ([IVX]+):\s*(.+)$", line)
            if part_match:
                current_part = {
                    "number": ROMAN[part_match.group(1)],
                    "roman": part_match.group(1),
                    "title": part_match.group(2).strip(),
                    "chapters": [],
                    "source_line": line_no,
                }
                parts.append(current_part)
                current_chapter = None
                continue
            chapter_match = re.match(r"^\*\*Chapter (\d+) — (.+?)\*\*", line)
            if chapter_match and current_part is not None:
                current_chapter = {
                    "number": int(chapter_match.group(1)),
                    "title": chapter_match.group(2).strip(),
                    "sections": [],
                    "citations": [],
                    "source_line": line_no,
                }
                current_part["chapters"].append(current_chapter)
                continue
            bullet_match = re.match(r"^(\s*)-\s+(.+)$", line)
            if bullet_match and current_chapter is not None:
                raw = bullet_match.group(2).strip()
                citation_numbers = [int(n) for n in re.findall(r"\[\^(\d+)\]", raw)]
                for citation_number in citation_numbers:
                    if citation_number not in current_chapter["citations"]:
                        current_chapter["citations"].append(citation_number)
                stripped = _strip_markdown(raw)
                section_match = re.match(r"([0-9]+(?:\.[0-9]+)*)\s+(.+)", stripped)
                current_chapter["sections"].append(
                    {
                        "level": 1 + len(bullet_match.group(1)) // 2,
                        "number": section_match.group(1) if section_match else None,
                        "title": section_match.group(2) if section_match else stripped,
                        "raw": raw,
                        "citations": citation_numbers,
                    }
                )
        elif mode == "appendix":
            appendix_match = re.match(r"^### Appendix ([A-Z]) — (.+)$", line)
            if appendix_match:
                current_appendix = {
                    "letter": appendix_match.group(1),
                    "title": appendix_match.group(2).strip(),
                    "items": [],
                    "source_line": line_no,
                }
                appendices.append(current_appendix)
                continue
            bullet_match = re.match(r"^(\s*)-\s+(.+)$", line)
            if bullet_match and current_appendix is not None:
                raw = bullet_match.group(2).strip()
                current_appendix["items"].append(
                    {
                        "level": 1 + len(bullet_match.group(1)) // 2,
                        "title": _strip_markdown(raw),
                        "raw": raw,
                        "citations": [int(n) for n in re.findall(r"\[\^(\d+)\]", raw)],
                    }
                )

    patterns: list[dict[str, Any]] = []
    chapter_32 = next(
        (
            chapter
            for part in parts
            for chapter in part["chapters"]
            if chapter["number"] == PATTERN_REGISTRY_CHAPTER_NUMBER
        ),
        None,
    )
    current_pattern: dict[str, Any] | None = None
    for section in chapter_32["sections"] if chapter_32 else []:
        pattern_match = re.match(r"\*\*Pattern (\d+):\s*(.+?)\*\*\s*—\s*(.*)", section["raw"])
        if pattern_match:
            current_pattern = {
                "number": int(pattern_match.group(1)),
                "name": pattern_match.group(2).strip(),
                "definition": _strip_markdown(pattern_match.group(3)),
                "methods": "",
                "application": "",
                "code_archetype": "",
                "citations": section["citations"],
            }
            patterns.append(current_pattern)
            continue
        if current_pattern is not None:
            detail_match = re.match(r"\*(Methods|Application|Code Archetype)\*:\s*(.*)", section["raw"])
            if detail_match:
                key = detail_match.group(1).lower().replace(" ", "_")
                current_pattern[key] = _strip_markdown(detail_match.group(2))

    return {
        "project": "AGEINT",
        "title": "Agentic Intelligence Modular Curriculum",
        "parts": parts,
        "appendices": appendices,
        "patterns": patterns,
        "references": list(references.values()),
        "stats": {
            "parts": len(parts),
            "chapters": sum(len(part["chapters"]) for part in parts),
            "appendices": len(appendices),
            "patterns": len(patterns),
            "references": len(references),
        },
    }


from _curriculum_shards import load_curriculum_shards_payload as _load_curriculum_shards
def write_curriculum_shards(payload: dict[str, Any], directory: Path) -> Path:
    """Write curriculum payload shards under ``directory``."""
    directory.mkdir(parents=True, exist_ok=True)
    (directory / "metadata.json").write_text(
        json.dumps(
            {key: payload[key] for key in ("project", "title") if key in payload},
            indent=2,
            ensure_ascii=False,
        )
        + "\n",
        encoding="utf-8",
    )
    (directory / "stats.json").write_text(
        json.dumps(payload["stats"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    (directory / "patterns.json").write_text(
        json.dumps(payload["patterns"], indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    for part in payload["parts"]:
        part_dir = directory / "parts" / curriculum_part_dir_name(part)
        part_dir.mkdir(parents=True, exist_ok=True)
        part_payload = {key: value for key, value in part.items() if key != "chapters"}
        part_payload["chapter_files"] = [
            f"{curriculum_chapter_dir_name(chapter)}/chapter.json"
            for chapter in part["chapters"]
        ]
        (part_dir / "part.json").write_text(
            json.dumps(part_payload, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
        chapter_dir = part_dir / "chapters"
        chapter_dir.mkdir(exist_ok=True)
        for chapter in part["chapters"]:
            chapter_path = chapter_dir / curriculum_chapter_dir_name(chapter)
            chapter_path.mkdir(exist_ok=True)
            chapter_payload = {key: value for key, value in chapter.items() if key != "sections"}
            (chapter_path / "chapter.json").write_text(
                json.dumps(chapter_payload, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            section_rows = "".join(
                json.dumps(section, ensure_ascii=False, sort_keys=True) + "\n"
                for section in chapter["sections"]
            )
            (chapter_path / "sections.jsonl").write_text(section_rows, encoding="utf-8")
    appendix_dir = directory / "appendices"
    appendix_dir.mkdir(exist_ok=True)
    for appendix in payload["appendices"]:
        (appendix_dir / f"{appendix['letter'].lower()}-{slug_for_path(appendix['title'])}.json").write_text(
            json.dumps(appendix, indent=2, ensure_ascii=False) + "\n",
            encoding="utf-8",
        )
    reference_dir = directory / "references"
    reference_dir.mkdir(exist_ok=True)
    for stale in reference_dir.glob("source-guide-*.jsonl"):
        stale.unlink()
    references = payload["references"]
    for start in range(1, len(references) + 1, 75):
        end = min(start + 74, len(references))
        chunk = [ref for ref in references if start <= int(ref["number"]) <= end]
        text = "".join(json.dumps(ref, ensure_ascii=False, sort_keys=True) + "\n" for ref in chunk)
        (reference_dir / f"source-guide-{start:03d}-{end:03d}.jsonl").write_text(text, encoding="utf-8")
    return directory


def write_compact_curriculum_payload(payload: dict[str, Any], output_path: Path) -> Path:
    """Write a one-line compatibility JSON payload without creating a long file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(
        json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "\n",
        encoding="utf-8",
    )
    return output_path


def resolve_curriculum_payload(
    source_path: Path,
    *,
    shard_path: Path | None = None,
) -> dict[str, Any]:
    """Resolve a curriculum payload from the guide file or sharded data."""
    if source_path.is_file():
        if source_path.suffix == ".json":
            return json.loads(source_path.read_text(encoding="utf-8"))
        return parse_curriculum_guide(source_path.read_text(encoding="utf-8"))
    if source_path.is_dir():
        return load_curriculum(source_path).payload

    candidates: list[Path] = []
    if shard_path is not None:
        candidates.append(shard_path)
    candidates.append(source_path.parent / "data" / "curriculum")
    for candidate in candidates:
        if candidate.exists():
            return load_curriculum(candidate).payload
    raise FileNotFoundError(
        f"No AGEINT curriculum source found: {source_path} or "
        f"{', '.join(str(path) for path in candidates)}"
    )


def build_curriculum(source_path: Path, output_path: Path) -> Curriculum:
    """Build a curriculum payload from the guide or sharded structured data."""
    if source_path.exists():
        payload = parse_curriculum_guide(source_path.read_text(encoding="utf-8"))
    else:
        payload = resolve_curriculum_payload(
            source_path,
            shard_path=output_path if output_path.exists() else None,
        )
    if output_path.suffix == ".json":
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")
    else:
        write_curriculum_shards(payload, output_path)
    return Curriculum(payload)


def load_curriculum(path: Path) -> Curriculum:
    """Load a curriculum JSON file or sharded curriculum directory."""
    if path.is_dir():
        return Curriculum(_load_curriculum_shards(path))
    if path.is_file():
        return Curriculum(json.loads(path.read_text(encoding="utf-8")))
    if path.name == "curriculum_outline.json":
        shard_dir = path.parent / "curriculum"
        if shard_dir.is_dir():
            return Curriculum(_load_curriculum_shards(shard_dir))
    raise FileNotFoundError(f"No AGEINT curriculum payload found: {path}")
