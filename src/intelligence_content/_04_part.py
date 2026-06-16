from __future__ import annotations

from typing import Final

from ._01_part import IntelligenceProfile


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
        source_pack_ids=(
            "odni_governance_directives",
            "odni_disclosure_and_tearlines",
            "ic_current_threat_baseline",
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
            "official_cia_sherman_kent_profession",
            "official_cia_kent_analyst_policymaker_relations",
            "official_dia_tradecraft_primer",
            "official_army_atp_2_33_4",
            "official_irtpa_2004_analytic_integrity",
            "official_911_commission_report",
            "official_robb_silberman_wmd_report",
            "official_senate_2004_prewar_iraq_assessment",
            "official_nato_alternative_analysis_handbook",
            "official_cia_grabo_warning_intelligence_handbook",
            "official_cia_cooper_2005_analytic_pathologies",
            "official_cia_analytic_culture_us_ic",
            "scholarly_heuer_psychology_intelligence_analysis",
            "scholarly_heuer_pherson_sats",
            "scholarly_janis_1982_groupthink",
            "scholarly_wohlstetter_1962_pearl_harbor_warning_decision",
            "scholarly_rand_2016_sat_evaluation",
            "scholarly_coulthart_2016_sat_use",
            "scholarly_coulthart_2017_core_sat_evaluation",
            "scholarly_chang_2018_restructuring_sats",
            "scholarly_marcoci_2019_tradecraft_reliability",
            "scholarly_barnes_mandel_2014_forecast_accuracy",
            "scholarly_ard_2023_sat_pragmatic",
            "scholarly_stromer_galley_2020_flexible_sat",
            "scholarly_whitesmith_2019_ach_bias",
            "scholarly_karvetski_mandel_2020_ach_coherence",
            "scholarly_mandel_karvetski_dhami_2018_boosting_accuracy",
            "scholarly_dhami_mandel_mellers_tetlock_2015_decision_science",
            "scholarly_denzler_2024_sat_psychology",
            "scholarly_wilcox_mandel_2024_ach_critical_review",
            "scholarly_miksa_2024_assessment_tabling",
            "scholarly_landon_murray_2025_fusion_centre_sats",
            "scholarly_borg_gustafson_2025_teaching_sats_across_nations",
            "scholarly_mccarthy_2024_alternative_futures_analysis",
            "scholarly_ritchey_2013_general_morphological_analysis",
            "scholarly_beebe_pherson_2014_cases_intelligence_analysis",
            "scholarly_pherson_pherson_2020_critical_thinking_strategic_intelligence",
            "scholarly_betts_1978_intelligence_failure",
            "scholarly_jervis_2022_postmortems_fail",
            "scholarly_wirtz_2023_intelligence_failures_inevitable",
            "official_national_academies_2011_intelligence_analysis_tomorrow",
            "official_iarpa_ace_program",
            "official_iarpa_reason_program",
            "scholarly_dalkey_helmer_1963_delphi",
            "professional_klein_2007_project_premortem",
            "scholarly_marrin_2012_improving_intelligence_analysis",
            "official_foi_2021_structured_analytic_techniques",
            "official_jips_2021_jsat",
            "official_belfer_mcmahon_2024_ai_tradecraft_standards",
            "scholarly_reddy_2023_smartbook_intelligence_reports",
            "scholarly_dhami_2019_ach_intelligence_analysis",
            "scholarly_dhami_2024_confirmation_bias_hypotheses",
            "scholarly_gaeta_2021_situation_awareness_intelligence",
        ),
        conceptual_focus=(
            "turning uncertainty into reviewable judgment through sourcing, "
            "alternatives, separated likelihood and confidence language, warning "
            "indicators, and explicit analytic lineage"
        ),
        method_stack=(
            "key assumptions check, analysis of competing hypotheses, "
            "diagnosticity review, indicators and warnings, probability calibration, "
            "red-team review, collective tradecraft rating, and source descriptor audit"
        ),
        composability_contract=(
            "every agent output must preserve evidence, assumptions, judgments, "
            "likelihood, confidence, dissent, empirical limits, and change history "
            "as separable fields"
        ),
        failure_modes=(
            "source laundering, automation bias, hidden assumptions, collapsed "
            "likelihood/confidence language, hindsight certainty, SAT-as-bias-cure "
            "overclaiming, and visually persuasive but weakly sourced claims"
        ),
        safety_boundary=(
            "analysis remains educational and decision-supportive; it does not "
            "become tasking, targeting, covert collection, or policy advocacy"
        ),
        source_pack_ids=(
            "cia_analytic_uncertainty",
            "cia_intelligence_profession",
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
            "scholarly_model_cards_model_reporting",
            "scholarly_datasheets_for_datasets",
            "scholarly_data_cards_dataset_documentation",
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
        source_pack_ids=(
            "odni_privacy_oversight",
            "odni_disclosure_and_tearlines",
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
            "official_model_context_protocol_specification",
            "official_model_context_protocol_security_best_practices",
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
            "scholarly_dylan_stivang_2025_emerging_tech_intelligence",
            "scholarly_caballero_jenkins_2024_llm_national_security",
            "scholarly_mikhailov_2023_llm_national_security_strategy",
            "scholarly_khlaaf_2024_foundation_models_military_istar",
            "scholarly_brundage_2018_malicious_use_ai",
            "official_cset_adversarial_ml_cybersecurity_2022",
            "official_scsp_aspi_future_intelligence_analysis_ai_hmt",
            "official_unidir_synthetic_data_autonomous_systems",
            "scholarly_wasil_2024_ai_emergency_preparedness",
            "scholarly_greshake_2023_indirect_prompt_injection",
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
        source_pack_ids=(
            "cia_ai_analysis_and_production",
            "ic_cyber_geoint_history",
            "odni_privacy_oversight",
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
            "scholarly_kozera_2020_fitness_osint",
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
        source_pack_ids=(
            "dia_osint_governance",
            "ic_cyber_geoint_history",
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
            "official_reagan_nsdd_298_opsec",
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
        source_pack_ids=(
            "odni_governance_directives",
            "odni_disclosure_and_tearlines",
        ),
    ),
)
