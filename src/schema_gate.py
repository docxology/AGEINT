"""Schema-version gate for generated JSON artifacts.

Every generated artifact that carries a ``schema_version`` field (the figure
registry, the visual-quality audit, and the audit reports under
``output/reports/``) is read by downstream audits. A schema bump on the
producer side must fail the audit that reads the artifact rather than being
silently tolerated, so every read goes through :func:`load_json_with_schema`.

Producers: ``src/figures/_02_part.py`` owns
``FIGURE_REGISTRY_SCHEMA_VERSION``; the audit collectors stamp reports with
``"1.0"``. Keep the expectations here in sync when a producer bumps its
version — that edit is the intended friction point.
"""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

FIGURE_REGISTRY_SCHEMA_VERSION = "1.5"
AUDIT_REPORT_SCHEMA_VERSION = "1.0"
VISUAL_QUALITY_AUDIT_SCHEMA_VERSION = "1.0"

#: Expected ``schema_version`` per generated artifact, keyed by repo-relative
#: path under ``output/``. Every report JSON stamped by an in-repo producer is
#: listed here; its consumers must read it through :func:`load_json_with_schema`.
#: Known exception: ``output/reports/artifact_manifest.json`` is written by the
#: external build runner with no ``schema_version`` field, so it stays unlisted
#: and reads as plain JSON. Consumers of an artifact not listed here read it
#: directly (plain JSON with no declared schema).
EXPECTED_SCHEMA_VERSIONS: dict[str, str] = {
    "figures/figure_registry.json": FIGURE_REGISTRY_SCHEMA_VERSION,
    "figures/visual_quality_audit.json": VISUAL_QUALITY_AUDIT_SCHEMA_VERSION,
    "reports/source_metadata.json": AUDIT_REPORT_SCHEMA_VERSION,
}


class SchemaVersionError(ValueError):
    """Raised when a generated artifact's schema_version is missing or unsupported."""


def require_schema_version(
    payload: object,
    expected: str,
    *,
    artifact: str,
) -> None:
    """Raise :class:`SchemaVersionError` unless ``payload`` declares ``expected``."""
    if not isinstance(payload, dict):
        raise SchemaVersionError(
            f"{artifact}: expected a JSON object with schema_version {expected!r}"
        )
    found = payload.get("schema_version")
    if found != expected:
        raise SchemaVersionError(
            f"{artifact}: schema_version {found!r} unsupported by this reader "
            f"(expected {expected!r}); bump the consumer in src/schema_gate.py "
            "alongside the producer"
        )


def expected_schema_version(path: Path, *, output_root: Path) -> str | None:
    """Return the expected schema version for ``path`` under ``output_root``, if any."""
    try:
        rel = path.resolve().relative_to(Path(output_root).resolve()).as_posix()
    except ValueError:
        return None
    return EXPECTED_SCHEMA_VERSIONS.get(rel)


def load_json_with_schema(path: Path, *, output_root: Path) -> dict[str, Any]:
    """Load a generated JSON artifact, enforcing its declared schema version.

    Artifacts without an entry in :data:`EXPECTED_SCHEMA_VERSIONS` load
    unconditionally. A missing file raises ``OSError`` like a direct read.
    """
    payload = json.loads(path.read_text(encoding="utf-8"))
    expected = expected_schema_version(path, output_root=output_root)
    if expected is not None:
        require_schema_version(payload, expected, artifact=path.as_posix())
    return payload
