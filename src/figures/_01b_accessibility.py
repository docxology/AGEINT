from __future__ import annotations

"""Official accessibility guidance encoded into the figure registry contract."""

FIGURE_ACCESSIBILITY_GUIDANCE: tuple[dict[str, str], ...] = (
    {
        "source": "W3C WAI Complex Images",
        "url": "https://www.w3.org/WAI/tutorials/images/complex/",
        "registry_rule": (
            "Complex charts, diagrams, maps, and infographics need a short text "
            "alternative plus a longer equivalent description."
        ),
    },
    {
        "source": "WCAG 2.2 Understanding SC 1.1.1 Non-text Content",
        "url": "https://www.w3.org/WAI/WCAG22/Understanding/non-text-content.html",
        "registry_rule": (
            "Short alternatives may point readers to a programmatically associated "
            "or nearby full text description when the figure carries complex content."
        ),
    },
    {
        "source": "WCAG 2.2 Understanding SC 1.4.1 Use of Color",
        "url": "https://www.w3.org/WAI/WCAG22/Understanding/use-of-color.html",
        "registry_rule": (
            "Color must not be the only visual channel for meaning; labels, position, "
            "shape, text, or another cue must preserve the distinction."
        ),
    },
    {
        "source": "WCAG 2.2 Understanding SC 1.4.11 Non-text Contrast",
        "url": "https://www.w3.org/WAI/WCAG22/Understanding/non-text-contrast.html",
        "registry_rule": (
            "Meaningful graphical objects and visual cues need enough contrast to "
            "be perceived without relying on low-contrast marks."
        ),
    },
    {
        "source": "Section508.gov Authoring Meaningful Alternative Text",
        "url": "https://www.section508.gov/create/alternative-text/",
        "registry_rule": (
            "Complex figure text should identify the chart or diagram type, purpose, "
            "important relationships, and highlighted evidence."
        ),
    },
    {
        "source": "U.S. Web Design System Data Visualizations",
        "url": "https://designsystem.digital.gov/components/data-visualizations/",
        "registry_rule": (
            "Data visuals should prefer simple common forms, direct labels, limited "
            "concept load, and lossless textual equivalents."
        ),
    },
    {
        "source": "Section508.gov Making Color Usage Accessible",
        "url": "https://www.section508.gov/create/making-color-usage-accessible/",
        "registry_rule": (
            "Figures must not rely on color alone; rendered text, symbols, labels, "
            "and contrast should preserve meaning for readers who do not perceive "
            "the palette."
        ),
    },
    {
        "source": "Section508.gov PDF accessibility training",
        "url": "https://www.section508.gov/training/pdfs/aed-cop-pdf02/",
        "registry_rule": (
            "Rendered PDF figures must be checked as figures with useful alternative "
            "text, not only as source Markdown rows."
        ),
    },
)

__all__ = ["FIGURE_ACCESSIBILITY_GUIDANCE"]
