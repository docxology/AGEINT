from __future__ import annotations

def _import_prior_parts(*module_names: str) -> None:
    import importlib

    for module_name in module_names:
        mod = importlib.import_module(f".{module_name}", __package__)
        globals().update({k: v for k, v in vars(mod).items() if not k.startswith("__")})


_import_prior_parts("_01_part", "_02_part")



ANCHORS_BY_KEY: Final[dict[str, ResearchAnchor]] = {
    anchor.key: anchor for anchor in INTELLIGENCE_RESEARCH_ANCHORS
}

SOURCE_QUALITY_REFERENCE_FALLBACKS: Final[dict[str, ResearchAnchor]] = {
    "official_oecd_agentic_ai": ResearchAnchor(
        key="official_oecd_agentic_ai",
        title="The Agentic AI Landscape and Its Conceptual Foundations",
        author="OECD",
        year="2026",
        url="https://www.oecd.org/en/publications/the-agentic-ai-landscape-and-its-conceptual-foundations_396cf758-en.html",
        note="Official OECD conceptual foundation for agentic AI.",
        domain="agentic_ai_governance",
        source_type="official_primary",
        citation_role="source_quality_anchor",
        source_lane="source_quality_spine",
        source_tier="source_quality_anchor",
    ),
    "official_nist_ai_rmf": ResearchAnchor(
        key="official_nist_ai_rmf",
        title="Artificial Intelligence Risk Management Framework (AI RMF 1.0)",
        author="National Institute of Standards and Technology",
        year="2023",
        url="https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.100-1.pdf",
        note="Official NIST.AI.100-1 risk-management framework.",
        domain="ai_ethics_data_governance",
        source_type="official_primary",
        citation_role="source_quality_anchor",
        source_lane="source_quality_spine",
        source_tier="source_quality_anchor",
    ),
    "official_nist_ai_600_1": ResearchAnchor(
        key="official_nist_ai_600_1",
        title="Artificial Intelligence Risk Management Framework: Generative AI Profile",
        author="National Institute of Standards and Technology",
        year="2024",
        url="https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf",
        note="Official NIST AI 600-1 generative AI profile.",
        domain="ai_ethics_data_governance",
        source_type="official_primary",
        citation_role="source_quality_anchor",
        source_lane="source_quality_spine",
        source_tier="source_quality_anchor",
    ),
    "official_nsa_mcp_security": ResearchAnchor(
        key="official_nsa_mcp_security",
        title="Security Design Considerations for AI-Driven Automation Leveraging MCP",
        author="National Security Agency",
        year="2025",
        url="https://www.nsa.gov/Press-Room/Press-Releases-Statements/Press-Release-View/Article/4496698/nsa-releases-security-design-considerations-for-ai-driven-automation-leveraging/",
        note="Official NSA security guidance for Model Context Protocol automation.",
        domain="agentic_ai_governance",
        source_type="official_primary",
        citation_role="source_quality_anchor",
        source_lane="source_quality_spine",
        source_tier="source_quality_anchor",
    ),
    "official_nist_sp_800_82r3": ResearchAnchor(
        key="official_nist_sp_800_82r3",
        title="Guide to Operational Technology Security, NIST SP 800-82 Rev. 3",
        author="National Institute of Standards and Technology",
        year="2024",
        url="https://csrc.nist.gov/pubs/sp/800/82/r3/final",
        note="Official NIST operational technology security guidance.",
        domain="ics_ot_defense",
        source_type="official_primary",
        citation_role="source_quality_anchor",
        source_lane="source_quality_spine",
        source_tier="source_quality_anchor",
    ),
    "official_isa_iec_62443": ResearchAnchor(
        key="official_isa_iec_62443",
        title="ISA/IEC 62443 Series of Standards",
        author="International Society of Automation",
        year="2026",
        url="https://www.isa.org/standards-and-publications/isa-standards/isa-iec-62443-series-of-standards",
        note="Official ISA overview of industrial automation and control security standards.",
        domain="ics_ot_defense",
        source_type="international_standard",
        citation_role="source_quality_anchor",
        source_lane="source_quality_spine",
        source_tier="source_quality_anchor",
    ),
    "official_odni_icd_203": ResearchAnchor(
        key="official_odni_icd_203",
        title="Intelligence Community Directive 203: Analytic Standards",
        author="Office of the Director of National Intelligence",
        year="2015",
        url="https://www.intel.gov/assets/documents/Intelligence%20Community%20Directives/ICD_203.pdf",
        note="Official ODNI analytic tradecraft standards directive.",
        domain="analytic_tradecraft",
        source_type="official_primary",
        citation_role="source_quality_anchor",
        source_lane="source_quality_spine",
        source_tier="source_quality_anchor",
    ),
    "official_eu_ai_act": ResearchAnchor(
        key="official_eu_ai_act",
        title="Regulation (EU) 2024/1689: Artificial Intelligence Act",
        author="European Union",
        year="2024",
        url="https://eur-lex.europa.eu/eli/reg/2024/1689/oj/eng",
        note="Official EU Artificial Intelligence Act legal text.",
        domain="ai_ethics_data_governance",
        source_type="official_primary",
        citation_role="source_quality_anchor",
        source_lane="source_quality_spine",
        source_tier="source_quality_anchor",
    ),
    "official_cisa_foreign_influence": ResearchAnchor(
        key="official_cisa_foreign_influence",
        title="Preparing for and Mitigating Foreign Influence Operations",
        author="Cybersecurity and Infrastructure Security Agency",
        year="2024",
        url="https://www.cisa.gov/resources-tools/resources/cisa-insights-preparing-and-mitigating-foreign-influence-operations-targeting-critical",
        note="Official CISA guidance on foreign influence operations targeting critical infrastructure.",
        domain="cognitive_security",
        source_type="official_primary",
        citation_role="source_quality_anchor",
        source_lane="source_quality_spine",
        source_tier="source_quality_anchor",
    ),
    "official_nato_counter_information_threats": ResearchAnchor(
        key="official_nato_counter_information_threats",
        title="Countering Information Threats",
        author="North Atlantic Treaty Organization",
        year="2026",
        url="https://www.nato.int/cps/en/natohq/topics_219728.htm",
        note="Official NATO counter-information-threat guidance.",
        domain="cognitive_security",
        source_type="official_primary",
        citation_role="source_quality_anchor",
        source_lane="source_quality_spine",
        source_tier="source_quality_anchor",
    ),
}

ALL_PROFILE_ANCHORS_BY_KEY: Final[dict[str, ResearchAnchor]] = {
    **SOURCE_QUALITY_REFERENCE_FALLBACKS,
    **ANCHORS_BY_KEY,
}

SAFE_PATTERN_PROFILES: Final[dict[int, SafePatternProfile]] = {
    1: SafePatternProfile(
        key="solo_reasoner",
        safe_name="Focused Analytic Reasoner",
        methods="bounded source reading, explicit assumptions, self-critique, and confidence notes",
        application="single public-source report critique with provenance and uncertainty fields",
        safety_boundary="keeps reasoning reviewable without exposing hidden reasoning or delegating action",
    ),
    2: SafePatternProfile(
        key="reflection_agent",
        safe_name="Reflection and Bias-Check Agent",
        methods="rubric-based critique, source-quality scoring, and trajectory validation",
        application="analytic-bias review over a synthetic or public-source evidence packet",
        safety_boundary="supports quality review and never replaces accountable human judgment",
    ),
    3: SafePatternProfile(
        key="tool_forager",
        safe_name="Tool-Allowlist Research Assistant",
        methods="schema-bound tool calls, public-source retrieval, allowlisted connectors, and grounded summaries",
        application="authorized bibliography, source inventory, or standards-mapping exercise",
        safety_boundary="excludes broad scraping, credentialed collection, and exposure-search tooling",
    ),
    4: SafePatternProfile(
        key="planner_executor",
        safe_name="Governed Planner-Executor",
        methods="milestone decomposition, approval gates, dependency checks, and rollback notes",
        application="classroom project plan for evidence review, policy analysis, or tabletop preparation",
        safety_boundary="plans curriculum artifacts only and does not create live operational tasking",
    ),
    5: SafePatternProfile(
        key="parallel_collector",
        safe_name="Parallel Source-Corroboration Agent",
        methods="bounded concurrent retrieval, deduplication, contradiction capture, and source descriptors",
        application="side-by-side comparison of public official, standards, and scholarly sources",
        safety_boundary="uses public or provided materials and avoids intelligence collection expansion",
    ),
    6: SafePatternProfile(
        key="multi_agent_crew",
        safe_name="Role-Separated Review Crew",
        methods="planner, retriever, validator, safety reviewer, and reporter roles",
        application="tabletop red-team critique of an analytic memo, not an operational exercise",
        safety_boundary="keeps roles educational, logged, and constrained to benign artifacts",
    ),
    7: SafePatternProfile(
        key="debate_agent",
        safe_name="Competing-Hypotheses Debate Agent",
        methods="alternative generation, evidence challenge, dissent capture, and judge rubric",
        application="ACH-style review of a classroom claim with clearly separated evidence and judgment",
        safety_boundary="does not generate adversarial persuasion or policy advocacy content",
    ),
    8: SafePatternProfile(
        key="rag_operator",
        safe_name="Provenance-Bound Retrieval Operator",
        methods="curated corpus retrieval, hybrid ranking, source snippets, and citation audits",
        application="course-pack retrieval over provided readings, standards, and official guidance",
        safety_boundary="does not connect to live sensitive stores or unapproved data collections",
    ),
    9: SafePatternProfile(
        key="memory_state_machine",
        safe_name="Evidence-Memory State Machine",
        methods="episodic note cards, retention limits, consolidation, and source change logs",
        application="longitudinal claim ledger for curriculum evidence and revision history",
        safety_boundary="tracks claims and sources, not people, assets, or behavioral patterns",
    ),
    10: SafePatternProfile(
        key="control_plane_agent",
        safe_name="Permissioned Control Plane Agent",
        methods="single-interface routing, policy checks, budget limits, and audit logs",
        application="tool-governance demo that routes among benign summarization and validation utilities",
        safety_boundary="keeps every tool revocable, observable, and constrained to non-operational actions",
    ),
    11: SafePatternProfile(
        key="surveillance_agent",
        safe_name="Monitoring-Governance Tabletop Agent",
        methods="synthetic event polling, threshold rationale, alert review, and escalation logging",
        application="authorized monitoring governance exercise over toy asset-health records",
        safety_boundary="prohibits tracking real people, real targets, private forums, or infrastructure",
    ),
    12: SafePatternProfile(
        key="red_team_agent",
        safe_name="Control-Coverage Critique Agent",
        methods="policy-safe scenario cards, control mapping, misuse-case review, and mitigation scoring",
        application="defensive tabletop review of controls against published high-level tactics",
        safety_boundary="does not automate exploitation, weakness discovery, or attack-chain execution",
    ),
    13: SafePatternProfile(
        key="cover_story_generator",
        safe_name="Identity-and-Provenance Fiction Audit",
        methods="synthetic persona-risk critique, provenance labeling, and consistency-error detection",
        application="ethics exercise that detects fabricated identity artifacts in clearly fictional materials",
        safety_boundary="prohibits impersonation, false identity creation, and operational-security support",
    ),
    14: SafePatternProfile(
        key="deception_detector",
        safe_name="Source-Reliability Verification Agent",
        methods="corroboration, metadata review, provenance checks, and content-authenticity labels",
        application="public-source validation packet with uncertainty and review escalations",
        safety_boundary="supports verification and does not accuse, deanonymize, or profile real people",
    ),
    15: SafePatternProfile(
        key="analyst_in_loop",
        safe_name="Analyst-in-the-Loop Review Agent",
        methods="interrupt gates, confidence thresholds, human approvals, and audit handoffs",
        application="supervised classroom analysis workflow for compliance-constrained exercises",
        safety_boundary="requires accountable human review before any external communication or decision",
    ),
    16: SafePatternProfile(
        key="cyber_sentinel",
        safe_name="SOC Tabletop Triage Agent",
        methods="synthetic alert enrichment, ATT&CK mapping, severity rationale, and debrief notes",
        application="tier-1 incident tabletop over fabricated logs and published technique descriptions",
        safety_boundary="does not run response actions, touch production systems, or publish indicators as fact",
    ),
    17: SafePatternProfile(
        key="supply_chain_inspector",
        safe_name="Software Provenance Review Agent",
        methods="SBOM reading, dependency graph review, advisory matching, and integrity questions",
        application="defensive package-governance exercise over sample manifests and public advisories",
        safety_boundary="does not hunt real maintainers or produce exploitability claims without evidence",
    ),
    18: SafePatternProfile(
        key="geoint_analyst",
        safe_name="GEOINT Data-Quality Audit Agent",
        methods="provided-image annotation, quality flags, geospatial metadata review, and caveat writing",
        application="synthetic imagery-change exercise focused on uncertainty and data quality",

        safety_boundary=(
            "limits work to non-sensitive metadata quality, uncertainty notes, "
            "and synthetic location examples"
        ),
    ),
    19: SafePatternProfile(
        key="cognitive_inoculant",
        safe_name="Cognitive-Resilience Education Agent",
        methods="manipulation-technique labeling, transparent prebunking, and audience-harm review",
        application="opt-in media-literacy micro-lesson for a fictional classroom scenario",
        safety_boundary="does not design persuasion campaigns, microtargeting, or covert influence content",
    ),
    20: SafePatternProfile(
        key="hierarchical_command",
        safe_name="Hierarchical Curriculum Orchestrator",
        methods="role delegation, output aggregation, exception routing, and failure recovery drills",
        application="multi-domain capstone coordination across benign module artifacts",
        safety_boundary="orchestrates learning artifacts only and preserves human authorization gates",
    ),
}
