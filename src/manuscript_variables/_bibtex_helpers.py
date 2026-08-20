"""BibTeX string cleaning and reference formatting helpers."""

from __future__ import annotations

import re
from typing import Any
import unicodedata


def clean_bibtex_value(value: object) -> str:
    return re.sub(r"\s+", " ", str(value).replace("{", "").replace("}", "")).strip()


def clean_bibtex_text(value: object) -> str:
    text = clean_bibtex_value(value)
    text = text.replace("\\", "/")
    replacements = {
        "\u2010": "-",
        "\u2011": "-",
        "\u2012": "-",
        "\u2013": "-",
        "\u2014": "-",
        "\u2018": "'",
        "\u2019": "'",
        "\u201c": '"',
        "\u201d": '"',
        "\u00ae": "(R)",
        "\u2122": "(TM)",
        "&": r"\&",
        "%": r"\%",
        "$": r"\$",
        "#": r"\#",
        "_": r"\_",
    }
    text = "".join(replacements.get(char, char) for char in text)
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode("ascii")
    return text


def reference_author(ref: dict[str, Any]) -> str:
    if ref.get("author"):
        return clean_bibtex_text(ref["author"])
    number = ref.get("number")
    if isinstance(number, int):
        return f"SIST Guide Reference {number:03d}"
    key_digits = re.sub(r"\D+", "", str(ref.get("key", "")))
    if key_digits:
        return f"SIST Guide Reference {int(key_digits):03d}"
    return "SIST Guide Reference"


def join_note_parts(parts: list[str]) -> str:
    return ". ".join(part.strip().rstrip(".") for part in parts if part.strip())
