#!/usr/bin/env python3
"""Fix package part imports to include private symbols from prior parts."""

from __future__ import annotations

import re
from pathlib import Path

SRC = Path(__file__).resolve().parents[1] / "src"

IMPORT_BLOCK = '''def _import_prior_parts(*module_names: str) -> None:
    import importlib

    for module_name in module_names:
        mod = importlib.import_module(f".{module_name}", __package__)
        globals().update({k: v for k, v in vars(mod).items() if not k.startswith("__")})


'''


def fix_part_file(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    if "_import_prior_parts" in text:
        return

    match = re.match(r"(from __future__ import annotations\n\n)(.*)", text, re.DOTALL)
    if not match:
        return

    header, rest = match.groups()
    imports = re.findall(r"from \._(\d+[a-z]?_part) import \*.*\n", rest)
    if not imports:
        return

    call = "_import_prior_parts(" + ", ".join(f'"_{name}"' for name in imports) + ")\n\n"
    rest = re.sub(r"from \._\d+[a-z]?_part import \*.*\n", "", rest)
    path.write_text(header + IMPORT_BLOCK + call + rest, encoding="utf-8")


def main() -> None:
    for package_dir in SRC.iterdir():
        if not package_dir.is_dir() or package_dir.name.startswith("_"):
            continue
        for part in sorted(package_dir.glob("_*.py")):
            if part.name == "__init__.py":
                continue
            fix_part_file(part)


if __name__ == "__main__":
    main()
