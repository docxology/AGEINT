"""Figure registry helpers merged from historical part shards."""

from __future__ import annotations

from dataclasses import asdict
from importlib import import_module
import os
from pathlib import Path
import re
import urllib.error
import urllib.request
import uuid
from typing import Any, cast

from ._01_part import FigureSpec


def _normalize_png_canvas(output: Path, size: int = 1400) -> None:
    """Fit a rendered PNG onto a square canvas for stable manuscript layout."""
    if not output.is_file():
        return
    image_mod, _, _, ops_mod = _pil_modules()
    with image_mod.open(output) as img:
        image = img.convert("RGBA")
    fitted = ops_mod.contain(image, (size - 120, size - 120))
    canvas = image_mod.new("RGBA", (size, size), "#f8fafcff")
    x = (size - fitted.width) // 2
    y = (size - fitted.height) // 2
    canvas.alpha_composite(fitted, (x, y))
    normalized = output.with_name(f".{output.stem}.normalized{output.suffix}")
    if normalized.exists():
        normalized.unlink()
    try:
        canvas.convert("RGB").save(normalized, format="PNG", compress_level=3)
        normalized.replace(output)
    finally:
        if normalized.exists():
            normalized.unlink()


def _temporary_png_path(output: Path) -> Path:
    unique = f"{os.getpid()}.{uuid.uuid4().hex}"
    return output.with_name(f".{output.stem}.{unique}.tmp{output.suffix}")


def _png_asset_is_valid(path: Path) -> bool:
    try:
        _validate_png_asset(path)
    except (OSError, SyntaxError, ValueError):
        return False
    return True


def _validate_png_asset(path: Path, spec: FigureSpec | None = None) -> None:
    """Fail if *path* is absent, empty, non-PNG, or unreadable by Pillow."""
    label = f" for {spec.label}" if spec is not None else ""
    if not path.is_file():
        raise FileNotFoundError(f"Missing figure asset{label}: {path}")
    if path.stat().st_size <= len(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"Empty or truncated figure asset{label}: {path}")
    if not path.read_bytes().startswith(b"\x89PNG\r\n\x1a\n"):
        raise ValueError(f"Figure asset is not a PNG{label}: {path}")
    image_mod, _, _, _ = _pil_modules()
    with image_mod.open(path) as image:
        width, height = image.size
        image.verify()
    if width <= 0 or height <= 0:
        raise ValueError(f"Figure asset has invalid dimensions{label}: {path}")


def _pil_modules() -> tuple[Any, Any, Any, Any]:
    return (
        import_module("PIL.Image"),
        import_module("PIL.ImageDraw"),
        import_module("PIL.ImageFont"),
        import_module("PIL.ImageOps"),
    )


def _font(font_mod: Any, size: int) -> Any:
    candidates = [
        "/System/Library/Fonts/Supplemental/Arial.ttf",
        "/System/Library/Fonts/Supplemental/Helvetica.ttf",
    ]
    for candidate in candidates:
        if Path(candidate).is_file():
            return font_mod.truetype(candidate, size)
    return font_mod.load_default()


def _download_bytes(url: str) -> bytes | None:
    request = urllib.request.Request(url, headers={"User-Agent": "AGEINT local figure generator"})
    try:
        with urllib.request.urlopen(request, timeout=20) as response:  # nosec B310 - fixed HTTPS provenance URLs.
            data = cast(bytes, response.read())
    except (urllib.error.URLError, TimeoutError):
        return None
    return data


def _entry(figure: dict[str, Any] | FigureSpec) -> dict[str, Any]:
    if isinstance(figure, FigureSpec):
        payload = asdict(figure)
        payload["kind"] = figure.kind.value
        return payload
    return dict(figure)


def _slug(value: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", value.lower()).strip("-") or "figure"


def _mermaid_label(value: str) -> str:
    # Mermaid renders HTML entities inside node text, so the ampersand survives
    # as a proper "&" (e.g. "MITRE ATT&CK") instead of the lossy "and".
    return value.replace('"', "'").replace("&", "&amp;")


def _markdown_escape(value: str) -> str:
    return value.replace("[", "(").replace("]", ")")


def _relative_posix(path: Path, start: Path) -> str:
    try:
        return Path(path).relative_to(start).as_posix()
    except ValueError:
        return _relpath(path, start)


def _relpath(path: Path, start: Path) -> str:
    import os

    return Path(os.path.relpath(path, start)).as_posix()


__all__ = [
    "FigureSpec",
    "_entry",
    "_font",
    "_markdown_escape",
    "_mermaid_label",
    "_normalize_png_canvas",
    "_png_asset_is_valid",
    "_relative_posix",
    "_temporary_png_path",
    "_validate_png_asset",
]
