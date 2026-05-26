"""Safe display titles for high-risk curriculum topics."""

from __future__ import annotations

import re

from typing import Final

from ._07_risk_categories import _topic_risk_category

# Titles that must not stand alone as the sole lesson header without a domain suffix.
GENERIC_DISPLAY_TITLE_MARKERS: Final[tuple[str, ...]] = (
    "Cognitive-security resilience lesson using sample materials and transparent labels",
    "Governance-bounded intelligence topic review using instructor-provided sample records",
    "AI-enabled recruitment-risk ethics and source-protection case study",
)

# Chapter-context categories whose curriculum shards already use educational titles.
PRESERVE_TITLE_RISK_CATEGORIES: Final[frozenset[str]] = frozenset(
    {
        "analytic_tradecraft",
        "ageint_pattern_registry",
        "operator_decision_hygiene",
        "critical_infrastructure_sharing",
        "cognitive_resilience",
        "operational_tradecraft_governance",
        "humint_recruitment_risk",
    }
)


def is_generic_display_title(title: str) -> bool:
    """Return True when a display title is a category fallback, not a curriculum topic."""
    lower = title.lower()
    return any(marker.lower() in lower for marker in GENERIC_DISPLAY_TITLE_MARKERS)


def _clean_shard_title(title: str) -> str:
    cleaned = title.strip()
    cleaned = cleaned.split(":", 1)[-1].strip() if cleaned.lower().startswith("case ") else cleaned
    return cleaned or title


def _safe_title_for_risk(risk_category: str) -> str:
    labels = {
        "agentic_cyber_misuse": (
            "Agentic cyber-misuse control review using sample prompt records, "
            "fabricated logs, and deny-by-default tool policies"
        ),
        "historical_humint_source_protection": (
            "Declassified source-protection and institutional-control case study"
        ),
        "ics_evasion_coverage": (
            "ICS evasion coverage-control review using defensive detection questions"
        ),
        "ics_collection_detection": (
            "ICS collection-risk detection review using synthetic tag records"
        ),
        "osint_tool_governance": (
            "OSINT tool-governance source-audit exercise using instructor-provided "
            "records, toy inputs, and provenance checklists"
        ),
        "geoint_data_quality": (
            "GEOINT data-quality audit using provided imagery metadata and "
            "non-sensitive synthetic change examples"
        ),
        "humint_recruitment_risk": (
            "AI-enabled recruitment-risk ethics and source-protection case study"
        ),
        "humint_handling_history": (
            "HUMINT handling history and source-protection ethics tabletop"
        ),
        "sigint_authority": (
            "SIGINT legal-authority and communications-security governance exercise"
        ),
        "cyber_taxonomy": (
            "Cyber defensive taxonomy mapping using published labels and fabricated alerts"
        ),
        "ics_safety": (
            "ICS defensive coverage and safety tabletop using synthetic process records"
        ),
        "cognitive_resilience": (
            "Cognitive-security resilience lesson using sample materials and transparent labels"
        ),
        "software_supply_chain_social_trust": (
            "Maintainer-contact and social-engineering resilience review for software supply-chain governance"
        ),
        "agentic_tool_isolation": (
            "Tool-isolation lab using toy fixtures, sandbox policy review, and no external execution"
        ),
        "target_monitoring": (
            "Requirements-scoped source-card aggregation exercise with no real targets"
        ),
        "geoint_uncertainty": (
            "synthetic GEOINT uncertainty exercise focused on data quality and caveats"
        ),
        "public_source_comparison": (
            "Bounded public-source comparison exercise with fixed inputs and deduplication"
        ),
        "soc_tabletop": "SOC tabletop triage exercise over fabricated alerts and debrief notes",
        "evidence_change_memory": (
            "Claim-ledger memory exercise that tracks evidence changes rather than people"
        ),
        "control_coverage": (
            "Control-coverage tabletop critique using high-level defensive tactics"
        ),
        "identity_provenance": (
            "Identity-and-provenance ethics audit with no impersonation"
        ),
        "media_literacy": "Opt-in media-literacy lesson plan for a sample classroom scenario",
        "gray_zone_governance": (
            "Hybrid-threat indicator review using sample scenarios and policy thresholds"
        ),
        "non_state_actor_governance": (
            "Non-state actor indicator review with attribution caution and governance boundaries"
        ),
        "financial_due_diligence": (
            "Financial due-diligence typology exercise using synthetic records and compliance boundaries"
        ),
        "counterintelligence_vetting": (
            "Source-vetting and insider-threat review using sample personnel records"
        ),
        "operator_decision_hygiene": (
            "Operator decision-hygiene tabletop using workload, evidence, and review checkpoints"
        ),
        "operational_tradecraft_governance": (
            "Operational tradecraft governance review using sample scenarios and oversight checkpoints"
        ),
    }
    return labels.get(
        risk_category,
        "Governance-bounded intelligence topic review using instructor-provided sample records",
    )


def _contextual_safe_title(raw_title: str, risk_category: str, base_title: str) -> str:
    lower = raw_title.lower()
    if risk_category == "software_supply_chain_social_trust":
        if "xz" in lower or "jia tan" in lower:
            return "XZ Utils maintainer-trust case review for software supply-chain governance"
        if "friendly yet aggressive" in lower:
            return "Maintainer-pressure communication signature review for software supply-chain governance"
        if "maintainer targeting" in lower:
            return "Maintainer-risk escalation review for software supply-chain governance"
        if "sock" in lower:
            return "Maintainer-contact provenance review for software supply-chain governance"
        return base_title
    if risk_category == "agentic_cyber_misuse":
        if "pythonrepl" in lower or "python repl" in lower:
            return "Python REPL sandbox and approval-gate review"
        if "autogen" in lower or "unsandboxed code" in lower:
            return "AutoGen sandbox and code-execution approval review"
        if "llm-based" in lower or "autonomous cyberattacks" in lower:
            return "LLM-agent cyber-misuse taxonomy review using sample reports"
        if "multi-agent collaboration" in lower:
            return "Multi-agent cyber-misuse coordination review using sample reports"
        if "6g" in lower or "iot" in lower or "satellite" in lower or "uav" in lower:
            return "Networked-device cyber-misuse risk review using sample scenarios"
        if "malware" in lower or "weaponization" in lower:
            return "Malware-misuse control review using sample agent logs"
        if "phishing" in lower:
            return "Phishing-resilience control review using sample messages"
        if "arbitrary code" in lower or "unsandboxed code" in lower:
            return "Code-execution sandbox and approval-gate review"
        return base_title
    if risk_category == "agentic_tool_isolation":
        return "Sandbox policy and tool-isolation review using toy OSINT fixtures"
    if risk_category == "sigint_authority":
        if "bulk" in lower or "metadata" in lower:
            return "SIGINT metadata minimization and authority review"
        if "covert communications" in lower or "dead drops" in lower:
            return "Communications-security history and lawful-access boundary review"
        if "radio" in lower or "rf" in lower or "spectrum" in lower:
            return "RF-spectrum governance and communications-security review"
        if "steganography" in lower:
            return "Steganography detection-literacy and communications-security review"
        return base_title
    if risk_category == "humint_handling_history":
        if "meeting structures" in lower:
            return "Historical meeting-structure ethics review"
        if "dead drops" in lower or "covert communications" in lower:
            return "Historical clandestine-communications ethics review"
        if "surveillance" in lower:
            return "Historical surveillance-risk and source-protection review"
        if "cutouts" in lower:
            return "Historical cutout-and-intermediary provenance review"
        if "fronts" in lower:
            return "Historical front-entity provenance review"
        if "running agents" in lower or "tasking" in lower:
            return "Historical agent-tasking oversight review"
        if "exfiltrating" in lower or "terminating agents" in lower:
            return "Historical extraction-and-termination ethics review"
        return base_title
    if risk_category == "historical_humint_source_protection":
        if "lubyanka" in lower or "training manuals" in lower:
            return "Declassified training-manual archive review"
        if "working with agents" in lower or "working-with-agents" in lower:
            return "Declassified source-protection and agent-handling ethics review"
        if "psychological methods" in lower or "manipulation" in lower:
            return "Declassified psychological-pressure ethics review"
        if "confidential contacts" in lower:
            return "Declassified confidential-contact oversight review"
        if "resident abroad" in lower:
            return "Declassified residency-management oversight review"
        if "alpha team" in lower:
            return "Declassified special-unit oversight case review"
        if "deep cover" in lower:
            return "Declassified cover-identity and source-protection case review"
        if "targeted killing" in lower or "wrath of god" in lower or "psyop" in lower:
            return "Declassified covert-action oversight and source-protection case review"
        return base_title
    if risk_category == "osint_tool_governance":
        if "google dorking" in lower or "search engine" in lower or "shodan" in lower:
            return "Search-exposure provenance review using instructor-provided records"
        if "social media" in lower or "scraping" in lower:
            return "Social-source provenance and minimization review using toy records"
        if "maltego" in lower or "graph-based" in lower:
            return "Graph-analysis provenance review using instructor-provided records"
        if "recon-ng" in lower or "reconnaissance framework" in lower:
            return "Custom-source integration governance review using toy records"
        if "spiderfoot" in lower or "automated osint collection" in lower:
            return "Automated-source aggregation governance review using toy records"
        if "theharvester" in lower or "sherlock" in lower or "foca" in lower:
            return "Identity-data minimization review using instructor-provided records"
        if "graph scraping" in lower:
            return "Social-platform provenance and minimization review using toy records"
        if "email harvesting" in lower or "domain enumeration" in lower:
            return "Domain-source provenance and minimization review using toy records"
        return base_title
    if risk_category == "geoint_uncertainty":
        if "geolocation" in lower or "ip attribution" in lower:
            return "IP-geolocation uncertainty review using synthetic records"
        return base_title
    if risk_category == "cyber_taxonomy":
        if "initial access" in lower or "execution" in lower:
            return "Cyber access-and-execution taxonomy review using fabricated alerts"
        if "credential" in lower or "lateral" in lower:
            return "Cyber credential-and-movement taxonomy review using fabricated alerts"
        if "command" in lower or "exfiltration" in lower or "impact" in lower:
            return "Cyber command, data-loss, and impact taxonomy review using fabricated alerts"
        if "domain fronting" in lower or "bulletproof" in lower:
            return "Cyber infrastructure-abuse indicator review using fabricated records"
        return base_title
    if risk_category == "ics_safety":
        if "controller" in lower:
            return "ICS controller-change coverage review using synthetic process records"
        if "firmware" in lower or "project file" in lower:
            return "ICS firmware and project-integrity coverage review"
        if "communications" in lower or "alarm" in lower:
            return "ICS alarm and communications-resilience tabletop"
        if "process" in lower:
            return "ICS process-safety consequence review using synthetic records"
        return base_title
    if risk_category == "cognitive_resilience":
        if "epistemic security" in lower or "epistemic governance" in lower:
            return "Epistemic security and knowledge-integrity review"
        if "darpa" in lower and ("ics" in lower or "cognitive" in lower):
            return "DARPA cognitive-security research literacy review"
        if "prebunking" in lower or "inoculation" in lower or "debunking" in lower:
            return "Psychological inoculation and prebunking literacy review"
        if "mixed-reality" in lower or "mixed reality" in lower:
            return "Mixed-reality influence typology literacy review"
        if "resaid" in lower or "neurips" in lower:
            return "Neurocognitive resilience research literacy review"
        if "what is cognitive security" in lower or "cognitive security definition" in lower:
            return "Cognitive security definitions and scope review"
        if "psyop" in lower or "active measures" in lower or "synthetic influence" in lower:
            return "Cognitive influence-analysis case review using sample materials"
        if "intervention" in lower or "ai-assisted" in lower:
            return "AI-assisted resilience-tool governance review using sample materials"
        if "microtargeting" in lower or "persuasion" in lower:
            return "Audience-resilience and persuasion-literacy review using sample materials"
        return _clean_shard_title(raw_title)
    if risk_category == "geoint_data_quality":
        if any(
            token in lower
            for token in ("optical", "sar", "infrared", "hyperspectral", "multispectral")
        ):
            return "Imagery modality literacy: resolution, scale, and sensor-fit review"
        if "collection platform" in lower or "satellite" in lower or "uav" in lower:
            return "Imagery collection-platform literacy: resolution and revisit tradeoffs"
        if "photo interpretation" in lower or "all-source" in lower:
            return "Photo-interpretation literacy: resolution, uncertainty, and scale review"
        if "commercial imint" in lower or "democratization" in lower:
            return "Commercial imagery literacy: resolution tiers, licensing, and provenance review"
        if "geolocation" in lower or "bellingcat" in lower:
            return "Open-source geolocation literacy: resolution, corroboration, and uncertainty review"
        if "imagery" in lower or "imint" in lower:
            return "Imagery quality literacy: resolution, temporal fit, and uncertainty review"
        return base_title
    if risk_category == "humint_recruitment_risk":
        if "mice" in lower:
            return "MICE Framework for recruitment-risk literacy"
        if "rascls" in lower:
            return "RASCLS tradecraft vocabulary for recruitment-risk literacy"
        if "spotting" in lower:
            return "Spotting indicators literacy for recruitment-risk review"
        if "assessment" in lower and "development" in lower:
            return "Assessment-and-development ethics literacy review"
        if "pitch" in lower or "doctrine" in lower:
            return "Recruitment-doctrine ethics and source-protection literacy"
        if "digital-age" in lower or "personalized communication" in lower:
            return "Digital-age recruitment-risk and consent-boundary review"
        return _clean_shard_title(raw_title)
    if risk_category == "operational_tradecraft_governance":
        if "opsec" in lower or "operations security" in lower:
            return "Operations security (OPSEC) governance review"
        if "compartmentation" in lower or "need-to-know" in lower:
            return "Compartmentation and need-to-know governance review"
        if "cover" in lower and "legend" in lower:
            return "Cover and legend governance literacy review"
        if "cover" in lower:
            return "Cover identity governance literacy review"
        return _clean_shard_title(raw_title)
    if risk_category == "operator_decision_hygiene":
        if "mice framework" in lower and "moral" in lower:
            return (
                "MICE motivation literacy and ethical-boundary review "
                "for operator psychology"
            )
        if "spycraft" in lower and "cognitive performance" in lower:
            return (
                "Spycraft psychology literacy: stress, trust, and "
                "reviewer-boundary review"
            )
        return base_title
    if risk_category == "analytic_tradecraft":
        return base_title
    if risk_category in ("ageint_pattern_registry", "critical_infrastructure_sharing"):
        return base_title
    return base_title


def safe_curriculum_treatment(title: str, part_title: str = "", chapter_title: str = "") -> str:
    """Rewrite high-risk source-guide treatment labels into safe curriculum labels."""
    risk_category = _topic_risk_category(title, part_title, chapter_title)
    if risk_category == "standard":
        return title
    base_title = (
        title
        if risk_category in PRESERVE_TITLE_RISK_CATEGORIES
        else _safe_title_for_risk(risk_category)
    )
    return _contextual_safe_title(title, risk_category, base_title)


def _topic_anchor_words(topic: str, limit: int = 3) -> str:
    words = [
        word
        for word in re.findall(r"[A-Za-z][A-Za-z0-9]+", topic)
        if word.lower()
        not in {
            "and",
            "the",
            "for",
            "with",
            "from",
            "into",
            "using",
            "source",
            "safe",
            "exercise",
            "intelligence",
            "to",
            "of",
            "as",
            "vs",
            "or",
        }
    ]
    return ", ".join(words[:limit]) if words else topic
