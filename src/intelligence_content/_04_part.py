from __future__ import annotations

from ._01_part import *  # noqa: F403
from ._02_part import *  # noqa: F403
from ._03_part import *  # noqa: F403


_INTELLIGENCE_PROFILES_CORE: Final[tuple[IntelligenceProfile, ...]] = (
    IntelligenceProfile(
        identifier="governed_intelligence_cycle",
        title="Governed Intelligence Cycle and Dissemination Architecture",
        match_terms=(
            "nature of intelligence",
            "intelligence community architectures",
            "dissemination",
            "classification",
            "marking",
            "information architecture",
        ),
        anchor_keys=(
            "official_intelligence_gov_how_ic_works",
            "official_odni_icd_203",
            "official_odni_icd_204",
            "official_odni_icd_504",
            "official_odni_capco_register",
            "official_federal_data_strategy",
            "official_pclob_oversight_reports",
        ),
        conceptual_focus=(
            "treating the intelligence cycle as a governed information system "
            "whose collection, processing, analysis, dissemination, evaluation, "
            "marking, and records obligations stay explicit"
        ),
        method_stack=(
            "cycle mapping, priority-to-product traceability, data-lifecycle "
            "mapping, classification vocabulary review, dissemination-caveat "
            "audit, customer feedback, and oversight checkpointing"
        ),
        composability_contract=(
            "requirements, data provenance, analytic judgments, markings, "
            "dissemination permissions, records obligations, and feedback remain "
            "separable artifacts"
        ),
        failure_modes=(
            "cycle theater, undocumented dissemination, classification drift, "
            "unclear release authority, stale records assumptions, and feedback loops "
            "that hide bias"
        ),
        safety_boundary=(
            "cycle and marking material remains public-source and educational; "
            "it never handles classified content, live release decisions, or "
            "source-method exposure"
        ),
    ),
    IntelligenceProfile(
        identifier="analytic_tradecraft",
        title="Analytic Tradecraft and Source Integrity",
        match_terms=(
            "analysis",
            "analytic",
            "intelligence community",
            "tradecraft",
            "epistemic",
            "structured",
            "historical",
        ),
        anchor_keys=(
            "official_odni_icd_203",
            "official_odni_icd_206",
            "official_odni_objectivity",
            "official_cia_tradecraft_primer",
            "official_dia_tradecraft_primer",
            "official_army_atp_2_33_4",
            "scholarly_heuer_psychology_intelligence_analysis",
            "scholarly_heuer_pherson_sats",
        ),
        conceptual_focus=(
            "turning uncertainty into reviewable judgment through sourcing, "
            "alternatives, confidence language, and explicit analytic lineage"
        ),
        method_stack=(
            "key assumptions check, analysis of competing hypotheses, "
            "indicators and warnings, red-team review, and source descriptor audit"
        ),
        composability_contract=(
            "every agent output must preserve evidence, assumptions, judgments, "
            "confidence, dissent, and change history as separable fields"
        ),
        failure_modes=(
            "source laundering, automation bias, hidden assumptions, collapsed "
            "confidence language, and visually persuasive but weakly sourced claims"
        ),
        safety_boundary=(
            "analysis remains educational and decision-supportive; it does not "
            "become tasking, targeting, covert collection, or policy advocacy"
        ),
    ),
    IntelligenceProfile(
        identifier="ai_ethics_data_governance",
        title="AI Ethics, Data Governance, and Civil-Liberties Review",
        match_terms=(
            "ai ethics",
            "ethics of intelligence",
            "legal authorities",
            "governance",
            "privacy",
            "data",
            "active inference",
            "adversarial considerations",
        ),
        anchor_keys=(
            "official_ic_ai_ethics_principles",
            "official_ic_ai_ethics_framework",
            "official_odni_icd_505",
            "official_odni_icd_504",
            "official_nist_ai_rmf",
            "official_nist_ai_600_1",
            "official_nist_ai_rmf_playbook",
            "official_oecd_ai_principles",
            "official_oecd_governing_with_ai_public_sector",
            "official_canada_algorithmic_impact_assessment",
            "official_canada_ai_register",
            "official_un_global_digital_compact",
            "official_iso_iec_42001_ai_management",
            "official_iso_iec_23894_ai_risk_management",
            "official_nist_sp_1270_ai_bias",
            "official_cisa_ai_data_security_best_practices",
            "official_nara_2025_ai_compliance_plan",
            "official_federal_data_strategy",
            "official_pclob_oversight_reports",
        ),
        conceptual_focus=(
            "aligning AI-enabled intelligence with lawful purpose, human "
            "accountability, data provenance, bias mitigation, records management, "
            "privacy, civil liberties, and periodic review"
        ),
        method_stack=(
            "authority and purpose review, model/data provenance cards, bias "
            "and accuracy assessment, human-accountability assignment, lifecycle "
            "documentation, and civil-liberties escalation"
        ),
        composability_contract=(
            "data, model, prompt, output, evaluator, accountable human, audit "
            "evidence, and retention rule are independently inspectable and versioned"
        ),
        failure_modes=(
            "ethics slogans without controls, undocumented model drift, hidden "
            "training-data limits, unowned AI outputs, civil-liberties blind spots, "
            "and unreviewed downstream reuse"
        ),
        safety_boundary=(
            "AI governance content uses synthetic or public examples and remains "
            "review-oriented; it does not authorize surveillance, targeting, or "
            "automated adverse action"
        ),
    ),
    IntelligenceProfile(
        identifier="agentic_ai_governance",
        title="Agentic AI Governance and Tool Security",
        match_terms=(
            "ageint",
            "agentic",
            "ai agent",
            "mcp",
            "autogen",
            "crewai",
            "langchain",
            "langgraph",
            "framework",
            "python",
        ),
        anchor_keys=(
            "official_oecd_agentic_ai",
            "official_canada_agentic_ai_guide",
            "official_nist_ai_rmf",
            "official_nist_ai_600_1",
            "official_ic_ai_ethics_principles",
            "official_ic_ai_ethics_framework",
            "official_odni_icd_505",
            "official_imda_agentic_ai_framework",
            "official_five_eyes_agentic_ai_adoption",
            "official_nsf_ai_agent_ecosystems",
            "official_cdc_agentic_research_public_health",
            "official_nsa_mcp_security",
            "official_nist_ai_agent_standards_initiative",
            "official_cisa_ai_red_teaming_tev",
            "official_nist_dioptra",
            "official_cisa_ai_data_security_best_practices",
            "official_cisa_deploying_ai_systems_securely",
            "official_oecd_governing_with_ai_public_sector",
            "official_oecd_ai_risks_incidents",
            "official_oecd_ai_incident_reporting_framework",
            "official_nist_agent_identity_authorization",
            "official_nist_digital_identity_sp_800_63_4",
            "official_nist_zero_trust_sp_800_207",
            "official_rfc_9700_oauth_security",
            "official_rfc_9449_oauth_dpop",
            "official_uk_aisi_agent_evaluations",
            "official_owasp_agentic_top_10",
            "official_owasp_llm_top_10",
            "official_mitre_atlas",
            "official_nist_ssdf",
            "official_cisa_secure_by_design",
            "official_nist_ai_100_2_adversarial_ml",
            "scholarly_friston_2010_fep",
            "scholarly_friston_2017_active_inference_process",
            "scholarly_dacosta_2020_discrete_active_inference",
            "scholarly_parr_2022_active_inference_textbook",
            "scholarly_yao_2023_react",
            "scholarly_shinn_2023_reflexion",
            "scholarly_park_2023_generative_agents",
            "scholarly_wei_2022_chain_of_thought",
            "scholarly_schick_2023_toolformer",
            "scholarly_wooldridge_1995_intelligent_agents",
            "scholarly_wooldridge_2009_multiagent_systems",
        ),
        conceptual_focus=(
            "delegated action under explicit authority, identity, permissions, "
            "tool boundaries, monitoring, and human escalation"
        ),
        method_stack=(
            "AI RMF Govern-Map-Measure-Manage, least-privilege tool design, "
            "prompt-injection review, progressive deployment, and rollback drills"
        ),
        composability_contract=(
            "agents, tools, credentials, memory, retrieval stores, policies, and "
            "logs remain separately inspectable and revocable components"
        ),
        failure_modes=(
            "excessive agency, shadow tools, indirect prompt injection, memory "
            "poisoning, confused authority, and unbounded action chains"
        ),
        safety_boundary=(
            "agentic workflows stay synthetic, owned-lab, supervised, logged, "
            "rate-limited, and reversible unless a lawful production authority exists"
        ),
    ),
    IntelligenceProfile(
        identifier="osint_geoint",
        title="Open-Source and Geospatial Intelligence Integrity",
        match_terms=(
            "osint",
            "open-source",
            "geoint",
            "imagery",
            "imint",
            "source",
        ),
        anchor_keys=(
            "official_ic_osint_strategy",
            "official_state_osint_strategy",
            "official_nga_strategy",
            "official_nga_geoint_ai",
            "official_iso_19157_data_quality",
            "official_odni_icd_206",
            "official_odni_icd_203",
            "official_cia_tradecraft_primer",
        ),
        conceptual_focus=(
            "public-source discovery converted into accountable intelligence "
            "through provenance, corroboration, minimization, and relevance tests"
        ),
        method_stack=(
            "source triage, provenance capture, corroboration matrix, recency "
            "audit, geospatial context review, and confidence calibration"
        ),
        composability_contract=(
            "collection notes, source metadata, transformations, caveats, and "
            "analytic judgments remain separately exportable"
        ),
        failure_modes=(
            "privacy drift, stale data, context collapse, platform bias, "
            "over-collection, and mistaking availability for reliability"
        ),
        safety_boundary=(
            "OSINT work uses lawful public or authorized sources and avoids "
            "doxxing, harassment, live tracking, or operational targeting"
        ),
    ),
    IntelligenceProfile(
        identifier="collection_management",
        title="Collection Management and Multi-INT Requirements Discipline",
        match_terms=(
            "collection",
            "requirements",
            "sigint",
            "masint",
            "humint",
            "agent recruitment",
            "agent handling",
            "source protection",
            "emanations",
            "electronic",
            "imagery",
        ),
        anchor_keys=(
            "official_intelligence_gov_how_ic_works",
            "official_odni_icd_204",
            "official_joint_pub_2_0",
            "official_ic_osint_strategy",
            "official_odni_eo_12333",
            "official_nsa_fisa",
            "official_odni_icd_206",
            "official_nist_fips_197_aes",
            "official_nist_fips_186_5_dss",
            "official_nist_fips_180_4_shs",
            "official_nist_sp_800_57pt1r5_key_management",
        ),
        conceptual_focus=(
            "requirements-driven, authority-bounded collection where priorities, "
            "legal basis, minimization, source protection, and evaluation are explicit"
        ),
        method_stack=(
            "priority mapping, requirement decomposition, source-discipline fit, "
            "coverage-gap review, legal-authority check, and collection-feedback loop"
        ),
        composability_contract=(
            "requirements, authorities, source disciplines, collection notes, "
            "retention limits, caveats, and evaluation metrics remain separable"
        ),
        failure_modes=(
            "opportunistic collection, priority drift, over-collection, weak "
            "minimization, source exposure, and confusing availability with authority"
        ),
        safety_boundary=(
            "collection material remains doctrinal and governance-oriented; it does "
            "not teach recruitment, interception, surveillance, or tasking procedures"
        ),
    ),
)
