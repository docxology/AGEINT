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
        # Ordinal ACH consistency cells are not numerical likelihoods. The
        # Bayesian identity is a separate illustration under explicit assumptions.
        "**Diagnosticity and Bayesian illustration.** Ordinary ACH consistency "
        "marks are not likelihood ratios, calibrated probabilities, or a posterior "
        "calculation. Separately, for mutually exclusive hypotheses $H_i, H_j$ "
        "with nonzero prior odds and justified likelihoods for evidence $E$, "
        "Bayes' rule gives "
        "$$\\frac{P(H_i \\mid E)}{P(H_j \\mid E)} = "
        "\\frac{P(E \\mid H_i)}{P(E \\mid H_j)} \\times "
        "\\frac{P(H_i)}{P(H_j)}.$$ "
        "Compatibility alone does not make evidence nondiagnostic: invented "
        "likelihoods 0.8 and 0.2 are both compatible with the observation but "
        "give a ratio of 4. Equal likelihoods give a ratio of 1. Dependence, "
        "uncertain likelihoods, omitted alternatives, and unreliable reporting "
        "must be addressed; do not add ordinal cells or repeatedly update on "
        "copied reports. This identity is not proof that ACH improves accuracy "
        "[@scholarly_karvetski_mandel_2020_ach_coherence]; "
        "[@scholarly_mandel_karvetski_dhami_2018_boosting_accuracy].",
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
        "For fixed model $p$ and observation $o$, minimizing $F$ over $q(s)$ "
        "approximates that model's posterior; it does not establish that the "
        "model or observation is true. The bound is not an equivalence between "
        "free energy and prediction error, nor evidence of deception detection "
        "or safe autonomous action [@scholarly_friston_2010_fep]; "
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
