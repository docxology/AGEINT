"""Supplemental domain keyword concept routes (split to keep main module under 500 lines)."""

from __future__ import annotations

DOMAIN_CONCEPT_ROUTES: tuple[tuple[tuple[str, ...], str], ...] = (
    (("opsec", "operations security"), (
        "Apply the five-step OPSEC process—identify critical information, analyze "
        "threats, analyze vulnerabilities, assess risk, apply countermeasures—in "
        "tabletop governance review only."
    )),
    (("compartmentation", "need-to-know"), (
        "Map compartment boundaries, access lists, and need-to-know fields before "
        "any information moves across teams."
    )),
    (("cover and legend", "cover identity", "legend management"), (
        "Review cover-and-legend governance as oversight, documentation, and "
        "source-protection literacy—not identity fabrication."
    )),
    (("mitre att&ck for ics", "att&ck for ics"), (
        "Use ATT&CK for ICS as defensive vocabulary for sequencing observations "
        "over synthetic process records—not adversary execution."
    )),
    (("safety instrumented system", "sis ", "sis integrity"), (
        "Focus on safety-system integrity, operator escalation, and consequence "
        "mapping in tabletop review."
    )),
    (("fincen", "financial crimes enforcement"), (
        "Read FinCEN advisories as typology-driven due-diligence signals with "
        "escalation thresholds—not proof of guilt."
    )),
    (("fatf", "financial action task force"), (
        "Use FATF typologies to structure review of transactional patterns and "
        "beneficial-ownership gaps."
    )),
    (("nist ai rmf", "ai risk management framework"), (
        "Bind AI use to NIST AI RMF functions—govern, map, measure, manage—with "
        "human review before analysis deployment."
    )),
    (("nist ai 600", "generative ai profile"), (
        "Apply NIST AI 600-1 generative-AI profile controls to logging, evaluation, "
        "and human review gates."
    )),
    (("oecd", "agentic ai"), (
        "Evaluate agentic-AI governance claims against OECD principles: transparency, "
        "accountability, and human oversight."
    )),
    (("gcsp", "geneva centre for security policy"), (
        "Use GCSP cognitive-security framing for provenance, audience harm, and "
        "transparent correction options."
    )),
    (("darpa ics", "darpa cognitive security"), (
        "Read DARPA cognitive-security research as design claims requiring "
        "assumptions, limits, and independent review."
    )),
    (("key assumptions check", "kac "), (
        "List key assumptions explicitly and test which ones would change the "
        "judgment if falsified."
    )),
    (("devil's advocacy", "devils advocacy"), (
        "Use structured devil's advocacy to surface disconfirming evidence and "
        "overconfidence before dissemination."
    )),
    (("cognitive security operations", "cogsec operations"), (
        "Map cognitive-security operations to monitoring, provenance review, and "
        "transparent correction—not influence design."
    )),
    (("pattern 1", "pattern 2", "pattern 3", "reflection pattern", "tool-use pattern"), (
        "Use the pattern name as safe architectural vocabulary for allowlisted, "
        "logged, revocable workflows."
    )),
)
