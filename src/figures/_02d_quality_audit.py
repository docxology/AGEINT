from __future__ import annotations

from collections import Counter
import json
from pathlib import Path
from typing import Any, Sequence

from ._01_part import FigureSpec
from ._02c_reader_text import (
    MIN_ALT_TEXT_WORDS,
    MIN_LONG_DESCRIPTION_WORDS,
    MIN_READER_CAPTION_WORDS,
)
from ._04_part import _pil_modules, _validate_png_asset

PNG_METADATA_KEYS = (
    "AGEINT.Label",
    "AGEINT.Title",
    "AGEINT.Caption",
    "AGEINT.AltText",
    "AGEINT.LongDescription",
    "AGEINT.SourceSection",
    "AGEINT.SectionLabel",
    "AGEINT.Kind",
    "AGEINT.SemanticRole",
    "AGEINT.EvidenceRole",
    "AGEINT.Quantitative",
    "AGEINT.Unit",
    "AGEINT.Denominator",
    "AGEINT.CountingRule",
    "AGEINT.InterpretationLimit",
    "AGEINT.Provenance",
)


def write_visual_quality_audit(
    project_root: Path,
    specs: Sequence[FigureSpec],
    *,
    registry_schema: str,
) -> dict[str, Any]:
    """Write a machine-readable audit of rendered figure quality gates."""
    rows = [_audit_row(Path(project_root), spec) for spec in specs]
    summary = _summary(rows, specs)
    audit = {
        "project": "AGEINT",
        "schema_version": "1.0",
        "registry_schema": registry_schema,
        "figure_count": len(rows),
        "pass": summary["passing_figures"] == len(rows),
        "summary": summary,
        "figures": rows,
    }
    path = Path(project_root) / "output" / "figures" / "visual_quality_audit.json"
    path.write_text(json.dumps(audit, indent=2, sort_keys=True), encoding="utf-8")
    return audit


def _audit_row(project_root: Path, spec: FigureSpec) -> dict[str, Any]:
    asset = project_root / spec.output_path
    _validate_png_asset(asset, spec)
    image_mod, _, _, _ = _pil_modules()
    with image_mod.open(asset) as image:
        width, height = image.size
        info = dict(image.info)
    expected = {
        "AGEINT.Label": spec.label,
        "AGEINT.Title": spec.title,
        "AGEINT.Caption": spec.caption,
        "AGEINT.AltText": spec.alt_text,
        "AGEINT.LongDescription": spec.long_description,
        "AGEINT.SourceSection": spec.source_section,
        "AGEINT.SectionLabel": spec.section_label,
        "AGEINT.Kind": spec.kind.value,
        "AGEINT.SemanticRole": spec.semantic_role,
        "AGEINT.EvidenceRole": spec.evidence_role,
        "AGEINT.Quantitative": str(spec.quantitative).lower(),
        "AGEINT.Unit": spec.unit,
        "AGEINT.Denominator": spec.denominator,
        "AGEINT.CountingRule": spec.counting_rule,
        "AGEINT.InterpretationLimit": spec.interpretation_limit,
    }
    metadata_matches = all(info.get(key) == value for key, value in expected.items())
    provenance_matches = _metadata_provenance(info.get("AGEINT.Provenance")) == spec.provenance
    aspect_ratio = max(width / height, height / width)
    caption_words = _word_count(spec.caption)
    alt_text_words = _word_count(spec.alt_text)
    long_description_words = _word_count(spec.long_description)
    checks = {
        "readable_png": True,
        "square_normalized": aspect_ratio <= 1.1,
        "caption_min_words": caption_words >= MIN_READER_CAPTION_WORDS,
        "alt_text_min_words": alt_text_words >= MIN_ALT_TEXT_WORDS,
        "long_description_min_words": long_description_words >= MIN_LONG_DESCRIPTION_WORDS,
        "png_metadata_complete": set(PNG_METADATA_KEYS) <= set(info),
        "png_metadata_matches_registry": metadata_matches and provenance_matches,
        "provenance_present": bool(spec.provenance),
        "source_section_present": bool(spec.source_section and spec.section_label),
        "visual_semantics_present": bool(
            spec.semantic_role
            and spec.evidence_role
            and spec.interpretation_limit
        ),
        "quantitative_semantics_complete": (
            not spec.quantitative
            or (
                spec.unit != "not_applicable"
                and spec.denominator != "not_applicable"
                and spec.counting_rule != "not_applicable"
            )
        ),
        "conceptual_limit_present": (
            spec.quantitative
            or "not a measured" in spec.interpretation_limit.lower()
        ),
    }
    return {
        "label": spec.label,
        "kind": spec.kind.value,
        "output_path": spec.output_path,
        "source_section": spec.source_section,
        "section_label": spec.section_label,
        "semantic_role": spec.semantic_role,
        "evidence_role": spec.evidence_role,
        "quantitative": spec.quantitative,
        "unit": spec.unit,
        "denominator": spec.denominator,
        "counting_rule": spec.counting_rule,
        "interpretation_limit": spec.interpretation_limit,
        "width": width,
        "height": height,
        "aspect_ratio": round(aspect_ratio, 4),
        "bytes": asset.stat().st_size,
        "caption_words": caption_words,
        "alt_text_words": alt_text_words,
        "long_description_words": long_description_words,
        "metadata_keys": sorted(key for key in info if key.startswith("AGEINT.")),
        "checks": checks,
        "pass": all(checks.values()),
    }


def _summary(rows: Sequence[dict[str, Any]], specs: Sequence[FigureSpec]) -> dict[str, Any]:
    checks = rows[0]["checks"].keys() if rows else ()
    return {
        "figure_count": len(rows),
        "passing_figures": sum(1 for row in rows if row["pass"]),
        "kind_counts": dict(sorted(Counter(spec.kind.value for spec in specs).items())),
        "quantitative_figures": sum(1 for spec in specs if spec.quantitative),
        "conceptual_figures": sum(1 for spec in specs if not spec.quantitative),
        "missing_visual_semantics": sum(
            1
            for row in rows
            if not (
                row["checks"]["visual_semantics_present"]
                and row["checks"]["quantitative_semantics_complete"]
                and row["checks"]["conceptual_limit_present"]
            )
        ),
        "check_counts": {
            check: sum(1 for row in rows if row["checks"][check])
            for check in checks
        },
        "min_caption_words": min((row["caption_words"] for row in rows), default=0),
        "min_alt_text_words": min((row["alt_text_words"] for row in rows), default=0),
        "min_long_description_words": min(
            (row["long_description_words"] for row in rows),
            default=0,
        ),
        "max_aspect_ratio": max((row["aspect_ratio"] for row in rows), default=0),
    }


def _metadata_provenance(value: str | None) -> dict[str, str]:
    if not value:
        return {}
    try:
        payload = json.loads(value)
    except json.JSONDecodeError:
        return {}
    return payload if isinstance(payload, dict) else {}


def _word_count(text: str) -> int:
    return len([word for word in text.replace("/", " ").split() if word.strip()])


__all__ = ["PNG_METADATA_KEYS", "write_visual_quality_audit"]
