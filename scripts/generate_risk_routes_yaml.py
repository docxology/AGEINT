#!/usr/bin/env python3
"""One-shot generator for data/topic_risk_routes.yaml from canonical rule tuples."""

from __future__ import annotations

from pathlib import Path

import yaml

TOPIC_RULES: list[dict[str, object]] = [
    {
        "category": "software_supply_chain_social_trust",
        "context_any": ["supply chain"],
        "title_any": [
            "social engineering",
            "sock puppetry",
            "maintainer targeting",
            "friendly yet aggressive",
            "jia tan",
            "xz utils",
        ],
    },
    {
        "category": "agentic_cyber_misuse",
        "title_any": [
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
        ],
    },
    {
        "category": "historical_humint_source_protection",
        "title_any": [
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
        ],
    },
    {
        "category": "ics_evasion_coverage",
        "title_any": ["rootkit", "masquerading", "indicator removal"],
    },
    {
        "category": "ics_collection_detection",
        "title_any": [
            "i/o image",
            "monitor process state",
            "point & tag",
            "point and tag",
        ],
    },
    {
        "category": "osint_tool_governance",
        "title_any": [
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
        ],
    },
    {
        "category": "geoint_uncertainty",
        "title_any": ["geolocation and ip attribution", "geolocation attribution"],
    },
    {
        "category": "agentic_tool_isolation",
        "title_any": ["sandbox", "vm deployment"],
    },
    {
        "category": "geoint_data_quality",
        "title_any": ["google earth engine"],
    },
    {
        "category": "humint_recruitment_risk",
        "title_any": [
            "targeting, spotting",
            "assessment and development operations",
            "recruitment pitch",
            "recruitment doctrine",
            "digital-age recruitment",
            "personalized communication",
        ],
    },
    {
        "category": "sigint_authority",
        "context_any": ["sigint", "signals"],
        "title_any": ["covert communications", "dead drops"],
    },
    {
        "category": "humint_handling_history",
        "title_any": [
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
        ],
    },
    {
        "category": "sigint_authority",
        "title_any": [
            "bulk collection",
            "metadata analysis",
            "rfint",
            "technical surveillance",
            "non-linear junction",
            "rf spectrum",
            "steganography",
            "emanations",
            "interception",
        ],
    },
    {
        "category": "cyber_taxonomy",
        "title_any": [
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
        ],
    },
    {
        "category": "ics_safety",
        "title_any": [
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
        ],
    },
    {
        "category": "cognitive_resilience",
        "title_any": [
            "microtargeting",
            "persuasion",
            "psychological operations",
            "psyop",
            "active measures",
            "social engineering",
            "synthetic influence",
            "intervention systems",
        ],
        "context_overrides": [
            {
                "category": "humint_recruitment_risk",
                "context_any": ["recruitment"],
            },
            {
                "category": "software_supply_chain_social_trust",
                "context_any": ["supply chain"],
            },
        ],
    },
    {
        "category": "target_monitoring",
        "title_any": ["target intelligence", "target monitoring"],
    },
    {
        "category": "geoint_uncertainty",
        "title_any": ["facility monitoring", "order-of-battle"],
    },
    {
        "category": "public_source_comparison",
        "title_any": ["real-time collection", "multi-source data harvesting"],
    },
    {
        "category": "soc_tabletop",
        "title_any": ["autonomous soc"],
    },
    {
        "category": "evidence_change_memory",
        "title_any": [
            "long-term asset tracking",
            "longitudinal target tracking",
            "target tracking",
            "pattern-of-life",
        ],
    },
    {
        "category": "control_coverage",
        "title_any": ["penetration testing automation", "vulnerability discovery"],
    },
    {
        "category": "identity_provenance",
        "title_any": ["noc legend", "sock puppet", "cover document"],
    },
    {
        "category": "media_literacy",
        "title_any": ["population-scale", "intervention delivery"],
    },
    {
        "category": "gray_zone_governance",
        "title_any": [
            "hybrid warfare",
            "gray zone",
            "irregular warfare",
            "proxy war",
            "special operations",
            "unconventional warfare",
        ],
    },
    {
        "category": "non_state_actor_governance",
        "title_any": [
            "non-state actor",
            "terrorist financing",
            "insurgent",
            "militia",
            "violent extremist",
        ],
    },
    {
        "category": "financial_due_diligence",
        "title_any": [
            "money laundering",
            "suspicious activity",
            "sar ",
            "typology",
            "trade-based",
            "shell company",
        ],
    },
    {
        "category": "counterintelligence_vetting",
        "title_any": [
            "insider threat",
            "mole hunt",
            "vetting failure",
            "background investigation",
        ],
    },
    {
        "category": "cognitive_resilience",
        "title_any": [
            "prebunking",
            "inoculation",
            "debunking",
            "misinformation",
            "disinformation campaign",
        ],
    },
    {
        "category": "operator_decision_hygiene",
        "title_any": [
            "cognitive load",
            "decision fatigue",
            "information overload",
            "operator wellness",
        ],
    },
    {
        "category": "historical_humint_source_protection",
        "title_any": [
            "cia history",
            "nsa history",
            "kgb",
            "mi6",
            "mossad",
            "church committee",
            "oversight failure",
        ],
    },
    {
        "category": "operational_tradecraft_governance",
        "title_any": [
            "opsec",
            "operations security",
            "compartmentation",
            "need-to-know",
            "cover and legend",
            "cover identity",
            "legend management",
        ],
    },
    {
        "category": "analytic_tradecraft",
        "title_any": [
            "analysis of competing hypotheses",
            "competing hypotheses",
            "key assumptions check",
            "devil's advocacy",
            "devils advocacy",
            "red team analysis",
            "structured analytic",
        ],
    },
    {
        "category": "analytic_tradecraft",
        "title_any": [
            "icd 203",
            "analytic tradecraft standard",
            "nine tradecraft",
            "analytic confidence",
            "sourcing standard",
        ],
    },
    {
        "category": "humint_recruitment_risk",
        "title_any": ["mice", "rascls", "recruitment", "spotting"],
        "context_any": ["humint"],
    },
]

CHAPTER_CONTEXT_RULES: list[dict[str, object]] = [
    {
        "category": "counterintelligence_vetting",
        "any_in_chapter": ["counterintelligence"],
    },
    {
        "category": "cognitive_resilience",
        "any_in_chapter": [
            "cognitive security",
            "social engineering",
            "neurocognitive mechanisms",
        ],
    },
    {
        "category": "analytic_tradecraft",
        "any_in_chapter": [
            "structured analytic techniques",
            "advanced analysis methods",
            "the nature of intelligence",
        ],
    },
    {
        "category": "operational_tradecraft_governance",
        "all_in_chapter": ["tradecraft", "core principles"],
    },
    {
        "category": "critical_infrastructure_sharing",
        "any_in_chapter": ["threat intelligence sharing"],
    },
    {
        "category": "ageint_pattern_registry",
        "chapter_exact": "foundations of ageint",
    },
    {
        "category": "ageint_pattern_registry",
        "any_in_chapter": ["ageint frameworks"],
    },
    {
        "category": "operator_decision_hygiene",
        "any_in_chapter": ["intelligent operator", "cognitive athlete"],
    },
    {
        "category": "historical_humint_source_protection",
        "any_in_chapter": [
            "american intelligence history",
            "israeli and continental",
            "british intelligence history",
        ],
    },
    {
        "category": "cyber_taxonomy",
        "any_in_chapter": ["cyber intelligence fundamentals"],
    },
    {
        "category": "geoint_data_quality",
        "any_in_chapter": ["imagery intelligence", "geoint and imagery"],
    },
    {
        "category": "sigint_authority",
        "any_in_chapter": [
            "electronic and emanations intelligence",
            "sigint fundamentals",
        ],
    },
    {
        "category": "gray_zone_governance",
        "any_in_chapter": [
            "gray zone warfare",
            "irregular warfare and special operations",
            "non-state actor intelligence",
        ],
    },
]


def main() -> None:
    root = Path(__file__).resolve().parents[1]
    payload = {
        "topic_rules": TOPIC_RULES,
        "chapter_context_rules": CHAPTER_CONTEXT_RULES,
    }
    out = root / "data" / "topic_risk_routes.yaml"
    out.write_text(yaml.safe_dump(payload, sort_keys=False, allow_unicode=True), encoding="utf-8")
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
