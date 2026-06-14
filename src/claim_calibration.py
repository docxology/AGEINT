"""Claim-calibration audit for generated AGEINT manuscript output."""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from datetime import UTC, datetime
import json
from pathlib import Path
import re
from typing import Any

try:
    from .source_support_strength import SourceSupportProfile, support_profiles_for_keys
except ImportError:  # pragma: no cover - direct script imports
    from source_support_strength import SourceSupportProfile, support_profiles_for_keys  # type: ignore[no-redef]


PROJECT_ROOT = Path(__file__).resolve().parents[1]
SUPPORT_DOC_NAMES = {"AGENTS.md", "README.md", "references.md"}
CITATION_RE = re.compile(r"(?<!`)\[@([^\]]+)\]")
CROSSREF_PREFIXES = ("fig:", "sec:", "eq:", "tbl:")
TABLE_SEPARATOR_RE = re.compile(r"^\|?\s*:?-{3,}:?\s*(\|\s*:?-{3,}:?\s*)+\|?$")

CLAIM_PATTERNS: tuple[tuple[str, re.Pattern[str]], ...] = (
    (
        "empirical_or_evaluation",
        re.compile(
            r"\b("
            r"measured performance|operational performance|learning gains?|"
            r"statistically significant|p[- ]?value|confidence interval|"
            r"benchmark(?:s|ed|ing)?|evaluat(?:e|ed|ion|ions)|"
            r"validated capability|capability improvement|"
            r"accuracy|precision|recall|false positive|false negative|"
            r"improves?|reduces?|increases?|decreases?|proves?"
            r")\b",
            re.IGNORECASE,
        ),
    ),
    (
        "governance_or_rights",
        re.compile(
            r"\b("
            r"compliance|compliant|law|legal|statutory|regulatory|rights?|"
            r"authorization|authorized|policy|standard|accountability|redress"
            r")\b",
            re.IGNORECASE,
        ),
    ),
    (
        "figure_or_visualization",
        re.compile(
            r"\b("
            r"figure|visual|visualization|caption|alt text|long description|"
            r"png metadata|registry|chart|graph"
            r")\b",
            re.IGNORECASE,
        ),
    ),
    (
        "artifact_readiness",
        re.compile(
            r"\b("
            r"pdf|validator|artifact evidence|rendered references?|generated output|"
            r"citation count|stale output|markdown-file link|current evidence"
            r")\b",
            re.IGNORECASE,
        ),
    ),
    (
        "safety_or_assurance",
        re.compile(
            r"\b("
            r"safety|safe|red[- ]?team|assurance|incident|risk|misuse|"
            r"human review|stop condition|rollback"
            r")\b",
            re.IGNORECASE,
        ),
    ),
)

FORMALISM_RE = re.compile(
    r"(\$[^$\n]{2,80}=[^$\n]{1,120}\$|\\\(|\\\[|\\begin\{equation\})"
)
HARD_FAIL_RE = re.compile(
    r"\b("
    r"proves?|proof of|certif(?:y|ies|ied)|statistically significant|"
    r"p[- ]?value|measured performance|operational performance|"
    r"validated capability|capability improvement|learning gains?"
    r")\b",
    re.IGNORECASE,
)
DIRECT_SUPPORT_REQUIRED_RE = re.compile(
    r"\b("
    r"statistically significant|p[- ]?value|measured performance|"
    r"operational performance|validated capability|capability improvement|"
    r"learning gains?|benchmark(?:ed|ing)?"
    r")\b",
    re.IGNORECASE,
)
BOUNDARY_PHRASES = (
    "not a benchmark",
    "not proof",
    "not a proof",
    "not a claim",
    "does not claim",
    "does not prove",
    "do not claim",
    "do not prove",
    "reject claims",
    "rejected unless",
    "must not promote",
    "proof limit",
    "not as a capability score",
    "not a measured capability score",
    "not measured performance",
    "what it does not establish",
    "what remains unsupported",
    "correct the misconception",
    "correct this misconception",
    "test the misconception",
    "can and cannot prove",
    "rather than proof",
    "rather than measured performance",
    "measured language appears without direct evaluation evidence",
    "direct benchmark, field evaluation",
    "direct benchmark, study, field evaluation",
    "learning-outcome estimate, operational-performance benchmark",
    "measured-performance claims, p-value or significance language",
    "confirm the claim is not",
    "not merely inferred",
    "stale output or markdown-file links certify as ready",
    "attack benchmark, or measured learning",
    "empirical or evaluation claim",
    "promote it into a benchmark",
    "fails unsupported proof-language",
)


@dataclass(frozen=True)
class ClaimCalibrationRow:
    """One high-risk claim-language row from generated manuscript output."""

    path: str
    line: int
    claim_class: str
    matched_terms: tuple[str, ...]
    text: str
    citation_keys: tuple[str, ...]
    source_support_profiles: tuple[SourceSupportProfile, ...]
    disposition: str
    fix_hint: str

    def as_dict(self) -> dict[str, Any]:
        return {
            "path": self.path,
            "line": self.line,
            "claim_class": self.claim_class,
            "matched_terms": list(self.matched_terms),
            "text": self.text,
            "citation_keys": list(self.citation_keys),
            "source_support_profiles": [
                profile.as_dict() for profile in self.source_support_profiles
            ],
            "disposition": self.disposition,
            "fix_hint": self.fix_hint,
        }


@dataclass(frozen=True)
class ClaimCalibrationReport:
    """Claim-calibration report for generated manuscript output."""

    payload: dict[str, Any]

    @property
    def ok(self) -> bool:
        return bool(self.payload["ok"])


def collect_claim_calibration(
    manuscript_dir: Path,
    *,
    project_root: Path | None = None,
) -> ClaimCalibrationReport:
    """Collect high-risk claim-language evidence from generated Markdown."""

    root = Path(manuscript_dir)
    support_root = Path(project_root) if project_root is not None else PROJECT_ROOT
    rows = _scan_claim_rows(root, support_root)
    hard_fail_rows = [row for row in rows if row.disposition == "fail"]
    warning_rows = [row for row in rows if row.disposition == "review"]
    payload = {
        "project": "AGEINT",
        "schema_version": "1.0",
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "ok": not hard_fail_rows,
        "summary": _summary(rows, hard_fail_rows, warning_rows),
        "thresholds": {
            "strong_claims_require_direct_support": True,
            "boundary_language_is_allowed": True,
            "headings_are_not_claim_rows": True,
            "citation_presence_alone_is_not_sufficient": True,
        },
        "hard_fail_rows": [row.as_dict() for row in hard_fail_rows],
        "warning_row_count": len(warning_rows),
        "warning_rows": [row.as_dict() for row in warning_rows[:50]],
        "rows": [row.as_dict() for row in rows],
    }
    return ClaimCalibrationReport(payload)


def write_claim_calibration(project_root: Path) -> tuple[Path, Path, ClaimCalibrationReport]:
    """Write JSON and Markdown claim-calibration reports under ``output/reports``."""

    root = Path(project_root)
    report = collect_claim_calibration(root / "output" / "manuscript", project_root=root)
    reports_dir = root / "output" / "reports"
    reports_dir.mkdir(parents=True, exist_ok=True)
    json_path = reports_dir / "claim_calibration.json"
    md_path = reports_dir / "claim_calibration.md"
    json_path.write_text(json.dumps(report.payload, indent=2, sort_keys=True), encoding="utf-8")
    md_path.write_text(render_claim_calibration_markdown(report), encoding="utf-8")
    return json_path, md_path, report


def render_claim_calibration_markdown(report: ClaimCalibrationReport) -> str:
    """Render a compact Markdown claim-calibration report."""

    payload = report.payload
    summary = payload["summary"]
    lines = [
        "# AGEINT Claim Calibration",
        "",
        "| Measure | Value |",
        "|---|---:|",
        f"| OK | {str(payload['ok']).lower()} |",
        f"| Generated at | {payload['generated_at']} |",
        f"| Candidate rows | {summary['candidate_rows']} |",
        f"| Hard-fail rows | {summary['hard_fail_rows']} |",
        f"| Review-warning rows | {summary['warning_rows']} |",
        f"| Boundary-allowed rows | {summary['boundary_allowed_rows']} |",
        "",
        "## Claim Class Distribution",
        "",
        "| Claim class | Rows |",
        "|---|---:|",
    ]
    for claim_class, count in summary["claim_class_counts"].items():
        lines.append(f"| {claim_class} | {count} |")
    lines.extend(
        [
            "",
            "## Source Support Distribution",
            "",
            "| Source support distribution | Mentions |",
            "|---|---:|",
        ]
    )
    for strength, count in summary["source_support_distribution"].items():
        lines.append(f"| {strength} | {count} |")
    lines.extend(
        [
            "",
            "## Hard-Fail Rows",
            "",
            "| Path | Line | Claim class | Terms | Fix hint |",
            "|---|---:|---|---|---|",
        ]
    )
    if payload["hard_fail_rows"]:
        for row in payload["hard_fail_rows"]:
            lines.append(
                f"| {row['path']} | {row['line']} | {row['claim_class']} | "
                f"{', '.join(row['matched_terms'])} | {row['fix_hint']} |"
            )
    else:
        lines.append("| None | 0 | - | - | - |")
    lines.extend(
        [
            "",
            "## Calibration Rule",
            "",
            "Citation presence is necessary but not sufficient. Strong empirical, "
            "statistical, performance, governance, safety, formalism, and visual "
            "claims must either cite direct support or state a clear boundary that "
            "keeps the prose from becoming proof-language.",
        ]
    )
    return "\n".join(lines) + "\n"


def _scan_claim_rows(manuscript_dir: Path, project_root: Path) -> list[ClaimCalibrationRow]:
    rows: list[ClaimCalibrationRow] = []
    for path in _iter_markdown(manuscript_dir):
        in_fence = False
        for line_number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
            stripped = line.strip()
            if stripped.startswith("```"):
                in_fence = not in_fence
                continue
            if in_fence or not _candidate_text_line(stripped):
                continue
            claim_class, matched_terms = _claim_class(stripped)
            if not claim_class:
                continue
            citation_keys = tuple(_citation_keys(stripped))
            profiles = tuple(support_profiles_for_keys(citation_keys, project_root))
            disposition, fix_hint = _disposition(stripped, claim_class, citation_keys, profiles)
            rows.append(
                ClaimCalibrationRow(
                    path=path.relative_to(manuscript_dir).as_posix(),
                    line=line_number,
                    claim_class=claim_class,
                    matched_terms=matched_terms,
                    text=_clean_text(stripped),
                    citation_keys=citation_keys,
                    source_support_profiles=profiles,
                    disposition=disposition,
                    fix_hint=fix_hint,
                )
            )
    return rows


def _candidate_text_line(stripped: str) -> bool:
    if stripped.startswith("#"):
        return False
    if stripped.startswith("!["):
        return False
    if TABLE_SEPARATOR_RE.fullmatch(stripped):
        return False
    if stripped in {"---", "***"}:
        return False
    return True


def _claim_class(text: str) -> tuple[str, tuple[str, ...]]:
    if FORMALISM_RE.search(text):
        terms = tuple(dict.fromkeys(match.group(0)[:48] for match in FORMALISM_RE.finditer(text)))
        return "formalism_or_statistical_expression", terms
    matches: list[tuple[str, str]] = []
    for claim_class, pattern in CLAIM_PATTERNS:
        for match in pattern.finditer(text):
            matches.append((claim_class, match.group(0).lower()))
    if not matches:
        return "", ()
    priority = {
        "empirical_or_evaluation": 0,
        "governance_or_rights": 1,
        "figure_or_visualization": 2,
        "artifact_readiness": 3,
        "safety_or_assurance": 4,
    }
    claim_class = min((item[0] for item in matches), key=lambda value: priority[value])
    terms = tuple(dict.fromkeys(term for cls, term in matches if cls == claim_class))
    return claim_class, terms


def _disposition(
    text: str,
    claim_class: str,
    citation_keys: tuple[str, ...],
    profiles: tuple[SourceSupportProfile, ...],
) -> tuple[str, str]:
    lowered = text.lower()
    if _boundary_language(lowered):
        return "boundary_allowed", "explicit boundary language keeps the claim calibrated"
    has_primary = any(profile.primary_support for profile in profiles)
    if claim_class == "formalism_or_statistical_expression" and not citation_keys:
        return "fail", _direct_support_hint("Add a citation and limitation language")
    if DIRECT_SUPPORT_REQUIRED_RE.search(text) and not has_primary:
        return "fail", _direct_support_hint("Narrow the empirical/statistical claim")
    if HARD_FAIL_RE.search(text) and not has_primary:
        return "fail", _direct_support_hint("Replace proof language or add direct support")
    if claim_class in {"governance_or_rights", "safety_or_assurance"} and citation_keys and not has_primary:
        return "review", "review weak-context-only support before treating this as a governing constraint"
    if not citation_keys and claim_class == "empirical_or_evaluation":
        return "review", "review empirical/evaluation vocabulary for direct support before reuse"
    if not citation_keys and claim_class in {"governance_or_rights", "safety_or_assurance"}:
        return "review", "review governance or safety vocabulary before treating it as an authority-backed claim"
    return "pass", "claim language has citation support or remains bounded"


def _direct_support_hint(prefix: str) -> str:
    return (
        f"{prefix}: use direct official, standards, scholarly, law/policy, or "
        "source-quality support, or rewrite as bounded design guidance."
    )


def _boundary_language(lowered: str) -> bool:
    return any(phrase in lowered for phrase in BOUNDARY_PHRASES)


def _citation_keys(text: str) -> list[str]:
    keys: list[str] = []
    for match in CITATION_RE.finditer(text):
        for raw in re.split(r"\s*;\s*", match.group(1)):
            key = raw.strip().split()[0].lstrip("@")
            if key and not key.startswith(CROSSREF_PREFIXES):
                keys.append(key)
    return list(dict.fromkeys(keys))


def _iter_markdown(root: Path) -> list[Path]:
    if root.is_file() and root.suffix == ".md" and root.name not in SUPPORT_DOC_NAMES:
        return [root]
    if not root.is_dir():
        return []
    return sorted(
        path for path in root.rglob("*.md") if path.is_file() and path.name not in SUPPORT_DOC_NAMES
    )


def _summary(
    rows: list[ClaimCalibrationRow],
    hard_fail_rows: list[ClaimCalibrationRow],
    warning_rows: list[ClaimCalibrationRow],
) -> dict[str, Any]:
    classes = Counter(row.claim_class for row in rows)
    dispositions = Counter(row.disposition for row in rows)
    strengths = Counter(
        profile.strength
        for row in rows
        for profile in row.source_support_profiles
    )
    return {
        "candidate_rows": len(rows),
        "hard_fail_rows": len(hard_fail_rows),
        "warning_rows": len(warning_rows),
        "boundary_allowed_rows": dispositions.get("boundary_allowed", 0),
        "claim_class_counts": dict(sorted(classes.items())),
        "disposition_counts": dict(sorted(dispositions.items())),
        "source_support_distribution": dict(sorted(strengths.items())),
    }


def _clean_text(text: str) -> str:
    return re.sub(r"\s+", " ", text).replace("|", "/").strip()[:420]


__all__ = [
    "ClaimCalibrationReport",
    "ClaimCalibrationRow",
    "collect_claim_calibration",
    "render_claim_calibration_markdown",
    "write_claim_calibration",
]
