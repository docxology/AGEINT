"""Tests for AGEINT PDF typography settings."""

from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def test_pdf_preamble_uses_compact_pdf_typography() -> None:
    preamble = (PROJECT_ROOT / "manuscript" / "preamble.md").read_text(encoding="utf-8")
    for snippet in (
        r"\changefontsizes[8.9pt]{7.8pt}",
        r"\setlength{\parskip}{0.15em}",
        r"\renewcommand{\arraystretch}{0.88}",
        r"\setlength{\LTpre}{2pt}",
        r"\setlength{\LTpost}{2pt}",
        r"\setcounter{tocdepth}{2}",
        r"\renewcommand*\l@subsection{\@dottedtocline{2}{3.8em}{5.2em}}",
    ):
        assert snippet in preamble
