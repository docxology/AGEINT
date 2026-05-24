"""Topic risk-category classification for safe curriculum treatment."""

from __future__ import annotations


def _chapter_context_risk_category(chapter_lower: str) -> str | None:
    """Chapter-wide default applied only when topic-level classification is standard."""
    if "counterintelligence" in chapter_lower:
        return "counterintelligence_vetting"
    if "cognitive security" in chapter_lower:
        return "cognitive_resilience"
    if any(
        phrase in chapter_lower
        for phrase in (
            "structured analytic techniques",
            "advanced analysis methods",
            "the nature of intelligence",
        )
    ):
        return "analytic_tradecraft"
    if "tradecraft" in chapter_lower and "core principles" in chapter_lower:
        return "operational_tradecraft_governance"
    if "threat intelligence sharing" in chapter_lower:
        return "critical_infrastructure_sharing"
    if chapter_lower == "foundations of ageint" or "ageint frameworks" in chapter_lower:
        return "ageint_pattern_registry"
    if "intelligent operator" in chapter_lower or "cognitive athlete" in chapter_lower:
        return "operator_decision_hygiene"
    if any(
        phrase in chapter_lower
        for phrase in (
            "american intelligence history",
            "israeli and continental",
            "british intelligence history",
        )
    ):
        return "historical_humint_source_protection"
    if "cyber intelligence fundamentals" in chapter_lower:
        return "cyber_taxonomy"
    if any(
        phrase in chapter_lower
        for phrase in ("imagery intelligence", "geoint and imagery")
    ):
        return "geoint_data_quality"
    if any(
        phrase in chapter_lower
        for phrase in (
            "electronic and emanations intelligence",
            "sigint fundamentals",
        )
    ):
        return "sigint_authority"
    if any(
        phrase in chapter_lower
        for phrase in (
            "gray zone warfare",
            "irregular warfare and special operations",
            "non-state actor intelligence",
        )
    ):
        return "gray_zone_governance"
    if "social engineering" in chapter_lower:
        return "cognitive_resilience"
    if "neurocognitive mechanisms" in chapter_lower:
        return "cognitive_resilience"
    return None


def _topic_risk_category(title: str, part_title: str = "", chapter_title: str = "") -> str:
    """Classify high-risk or context-sensitive source-guide topic labels."""
    lower = title.lower()
    context = f"{part_title} {chapter_title}".lower()
    chapter_lower = chapter_title.lower()

    if "supply chain" in context and any(
        phrase in lower
        for phrase in (
            "social engineering",
            "sock puppetry",
            "maintainer targeting",
            "friendly yet aggressive",
            "jia tan",
            "xz utils",
        )
    ):
        return "software_supply_chain_social_trust"
    if any(
        phrase in lower
        for phrase in (
            "automated weaponization",
            "malware generation",
            "phishing automation",
            "spear-phishing automation",
            "autonomous cyberattacks",
            "cyberattacks",
            "cyberattack",
            "code-execution",
            "code execution",
            "exploit chain",
            "arbitrary code execution",
            "unsandboxed code execution",
        )
    ):
        return "agentic_cyber_misuse"
    if any(
        phrase in lower
        for phrase in (
            "working with agents",
            "working-with-agents",
            "manipulation of agents",
            "confidential contacts",
            "resident abroad",
            "alpha team",
            "training manual",
            "psychological methods",
            "deep cover agent",
            "targeted killing",
        )
    ):
        return "historical_humint_source_protection"
    if any(
        phrase in lower
        for phrase in (
            "rootkit",
            "masquerading",
            "indicator removal",
        )
    ):
        return "ics_evasion_coverage"
    if any(
        phrase in lower
        for phrase in (
            "i/o image",
            "monitor process state",
            "point & tag",
            "point and tag",
        )
    ):
        return "ics_collection_detection"
    if any(
        tool in lower
        for tool in (
            "shodan",
            "spiderfoot",
            "recon-ng",
            "theharvester",
            "maltego",
            "google dorking",
            "social media osint",
            "graph scraping",
            "scraping",
            "email harvesting",
            "domain enumeration",
            "reconnaissance framework",
            "automated osint collection",
            "targeted investigation tools",
        )
    ):
        return "osint_tool_governance"
    if "geolocation and ip attribution" in lower or "geolocation attribution" in lower:
        return "geoint_uncertainty"
    if "sandbox" in lower or "vm deployment" in lower:
        return "agentic_tool_isolation"
    if "google earth engine" in lower:
        return "geoint_data_quality"
    if any(
        phrase in lower
        for phrase in (
            "targeting, spotting",
            "assessment and development operations",
            "recruitment pitch",
            "recruitment doctrine",
            "digital-age recruitment",
            "personalized communication",
        )
    ):
        return "humint_recruitment_risk"
    if (
        ("sigint" in context or "signals" in context)
        and ("covert communications" in lower or "dead drops" in lower)
    ):
        return "sigint_authority"
    if any(
        phrase in lower
        for phrase in (
            "meeting structures",
            "surveillance detection",
            "dead drops",
            "cutouts",
            "fronts and shell entities",
            "counter-surveillance",
            "running agents",
            "exfiltrating",
            "terminating agents",
            "covert communications",
            "digital dead drops",
        )
    ):
        return "humint_handling_history"
    if any(
        phrase in lower
        for phrase in (
            "bulk collection",
            "metadata analysis",
            "rfint",
            "technical surveillance",
            "non-linear junction",
            "rf spectrum",
            "steganography",
            "emanations",
            "interception",
        )
    ):
        return "sigint_authority"
    if any(
        phrase in lower
        for phrase in (
            "initial access",
            "privilege escalation",
            "defense evasion",
            "credential access",
            "lateral movement",
            "command & control",
            "exfiltration",
            "domain fronting",
            "bulletproof hosting",
            "living-off-the-land",
        )
    ):
        return "cyber_taxonomy"
    if any(
        phrase in lower
        for phrase in (
            "modify controller",
            "modify firmware",
            "project file infection",
            "network sniffing",
            "block communications",
            "alarm suppression",
            "impair process control",
            "damage to property",
            "loss of safety",
            "manipulation of control",
            "autonomous ics incident response",
            "process manipulation",
        )
    ):
        return "ics_safety"
    if any(
        phrase in lower
        for phrase in (
            "microtargeting",
            "persuasion",
            "psychological operations",
            "psyop",
            "active measures",
            "social engineering",
            "synthetic influence",
            "intervention systems",
        )
    ):
        if "recruitment" in context:
            return "humint_recruitment_risk"
        if "supply chain" in context:
            return "software_supply_chain_social_trust"
        return "cognitive_resilience"
    if "target intelligence" in lower or "target monitoring" in lower:
        return "target_monitoring"
    if "facility monitoring" in lower or "order-of-battle" in lower:
        return "geoint_uncertainty"
    if "real-time collection" in lower or "multi-source data harvesting" in lower:
        return "public_source_comparison"
    if "autonomous soc" in lower:
        return "soc_tabletop"
    if (
        "long-term asset tracking" in lower
        or "longitudinal target tracking" in lower
        or "target tracking" in lower
        or "pattern-of-life" in lower
    ):
        return "evidence_change_memory"
    if "penetration testing automation" in lower or "vulnerability discovery" in lower:
        return "control_coverage"
    if "noc legend" in lower or "sock puppet" in lower or "cover document" in lower:
        return "identity_provenance"
    if "population-scale" in lower or "intervention delivery" in lower:
        return "media_literacy"
    if any(
        phrase in lower
        for phrase in (
            "hybrid warfare",
            "gray zone",
            "irregular warfare",
            "proxy war",
            "special operations",
            "unconventional warfare",
        )
    ):
        return "gray_zone_governance"
    if any(
        phrase in lower
        for phrase in (
            "non-state actor",
            "terrorist financing",
            "insurgent",
            "militia",
            "violent extremist",
        )
    ):
        return "non_state_actor_governance"
    if any(
        phrase in lower
        for phrase in (
            "money laundering",
            "suspicious activity",
            "sar ",
            "typology",
            "trade-based",
            "shell company",
        )
    ):
        return "financial_due_diligence"
    if any(
        phrase in lower
        for phrase in (
            "insider threat",
            "mole hunt",
            "vetting failure",
            "background investigation",
        )
    ):
        return "counterintelligence_vetting"
    if any(
        phrase in lower
        for phrase in (
            "prebunking",
            "inoculation",
            "debunking",
            "misinformation",
            "disinformation campaign",
        )
    ):
        return "cognitive_resilience"
    if any(
        phrase in lower
        for phrase in (
            "cognitive load",
            "decision fatigue",
            "information overload",
            "operator wellness",
        )
    ):
        return "operator_decision_hygiene"
    if any(
        phrase in lower
        for phrase in (
            "cia history",
            "nsa history",
            "kgb",
            "mi6",
            "mossad",
            "church committee",
            "oversight failure",
        )
    ):
        return "historical_humint_source_protection"
    if any(
        phrase in lower
        for phrase in (
            "opsec",
            "operations security",
            "compartmentation",
            "need-to-know",
            "cover and legend",
            "cover identity",
            "legend management",
        )
    ):
        return "operational_tradecraft_governance"
    if any(
        phrase in lower
        for phrase in (
            "analysis of competing hypotheses",
            "competing hypotheses",
            "key assumptions check",
            "devil's advocacy",
            "devils advocacy",
            "red team analysis",
            "structured analytic",
        )
    ):
        return "analytic_tradecraft"
    if any(
        phrase in lower
        for phrase in (
            "icd 203",
            "analytic tradecraft standard",
            "nine tradecraft",
            "analytic confidence",
            "sourcing standard",
        )
    ):
        return "analytic_tradecraft"
    if any(
        phrase in lower
        for phrase in ("mice", "rascls", "recruitment", "spotting")
    ) and "humint" in context:
        return "humint_recruitment_risk"

    chapter_default = _chapter_context_risk_category(chapter_lower)
    if chapter_default:
        return chapter_default
    return "standard"
