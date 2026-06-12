"""Per-lesson mathematical definitions for topics whose sources warrant them.

Each entry is gated on a distinctive substring of the lesson title so the math
fires ONLY for the lesson whose cited sources support it, and never sprays across
unrelated lessons. Every formula is definitional and sourced to the anchors the
lesson already carries; none is decorative.

The rendered field label deliberately avoids the literal word that the manuscript
cross-reference gate bans in prose; each label instead names the specific object
it defines (a diagnosticity ratio, a free-energy bound).
"""

from __future__ import annotations

# (title-substring, rendered field) pairs. The rendered field is one body field
# appended after the six required lesson fields, so it never disturbs the
# required-field set or the per-lesson repetition caps for any other lesson.
_LESSON_FORMULAS: tuple[tuple[str, str], ...] = (
    (
        "Analysis of Competing Hypotheses",
        # Heuer's diagnosticity scoring is a likelihood-ratio judgment: an item of
        # evidence shifts belief between hypotheses only insofar as it is more
        # likely under one than another. The posterior-odds form makes the
        # "weigh disconfirming evidence" rule precise.
        "**Diagnosticity ratio.** The diagnosticity an ACH table scores is a "
        "likelihood ratio. For two hypotheses $H_i, H_j$ and an item of evidence "
        "$E$, the posterior odds update as "
        "$$\\frac{P(H_i \\mid E)}{P(H_j \\mid E)} = "
        "\\frac{P(E \\mid H_i)}{P(E \\mid H_j)} \\times "
        "\\frac{P(H_i)}{P(H_j)}.$$ "
        "Evidence is diagnostic only when the likelihood ratio "
        "$P(E \\mid H_i)/P(E \\mid H_j)$ departs from $1$; evidence consistent "
        "with every hypothesis (ratio $\\approx 1$) carries no diagnostic weight, "
        "which is exactly Heuer's rule to weigh disconfirming evidence over "
        "confirming evidence [@ageint192]; [@ageint297].",
    ),
    (
        "Free Energy Principle",
        # Variational free energy is an upper bound on surprise; minimizing it over
        # the recognition density tightens the bound. One definitional display line
        # only -- full active-inference derivations are out of scope here.
        "**Free-energy bound.** Variational free energy $F$ upper-bounds surprise "
        "$-\\ln p(o)$ for observations $o$ and hidden states $s$ under a "
        "recognition density $q(s)$: "
        "$$F = D_{\\mathrm{KL}}\\!\\big(q(s)\\,\\|\\,p(s \\mid o)\\big) - "
        "\\ln p(o) \\;\\ge\\; -\\ln p(o).$$ "
        "Because the Kullback-Leibler term is non-negative, minimizing $F$ over "
        "$q(s)$ tightens the bound on surprise -- the precise statement of this "
        "lesson's plain-language warning about a model explaining too much from "
        "too little evidence [@scholarly_friston_2010_fep]; "
        "[@scholarly_buckley_2017_fep_mathematical_review].",
    ),
)


def lesson_formalism_field(display_title: str) -> str:
    """Return a sourced math field for a lesson whose sources warrant one.

    Gated on a distinctive title substring so the formula appears only in the
    lesson whose cited sources support it. Returns an empty string otherwise, so
    the per-lesson required-field set and repetition caps are untouched for every
    other lesson in the corpus.
    """
    for needle, field in _LESSON_FORMULAS:
        if needle in display_title:
            return field
    return ""
