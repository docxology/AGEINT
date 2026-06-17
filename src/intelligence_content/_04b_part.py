from __future__ import annotations

from typing import Final

from ._01_part import IntelligenceProfile
from ._04_part import _INTELLIGENCE_PROFILES_CORE


_INTELLIGENCE_PROFILES_EXTENDED: Final[tuple[IntelligenceProfile, ...]] = (
    IntelligenceProfile(
        identifier="financial_economic_security",
        title="Financial Intelligence and Economic-Security Due Diligence",
        match_terms=(
            "financial",
            "finint",
            "sanctions",
            "illicit finance",
            "money laundering",
            "terrorist financing",
            "proliferation financing",
            "export control",
            "export-control",
            "economic security",
            "due diligence",
        ),
        anchor_keys=(
            "official_fincen_advisories",
            "official_fincen_boi",
            "official_ofac_sanctions_programs",
            "official_ofac_compliance_commitments",
            "official_fatf_recommendations",
            "official_fatf_virtual_assets_guidance",
            "official_bis_fintech_digital_transformation",
            "official_bis_export_enforcement",
            "official_nist_sp_800_161r1",
            "official_odni_icd_206",
            "official_odni_icd_203",
        ),
        conceptual_focus=(
            "defensive economic intelligence that links financial-crime signals, "
            "sanctions programs, export controls, beneficial-ownership uncertainty, "
            "and supply-chain due diligence to lawful compliance and policy analysis"
        ),
        method_stack=(
            "typology-to-control mapping, sanctions-program review, beneficial "
            "ownership uncertainty notes, export-control red-flag triage, supplier "
            "risk registers, and compliance-oriented analytic memos"
        ),
        composability_contract=(
            "entities, transactions, sanctions programs, red flags, supplier "
            "evidence, legal constraints, and analytic judgments remain separately "
            "reviewable"
        ),
        failure_modes=(
            "evasion playbooks, threshold gaming, overconfident attribution, "
            "stale sanctions data, unverified beneficial ownership, and confusing "
            "compliance screening with intelligence certainty"
        ),
        safety_boundary=(
            "FININT and economic-security examples remain compliance, policy, "
            "and resilience oriented; they do not explain how to launder funds, "
            "evade sanctions, bypass export controls, or target real firms"
        ),
        source_pack_ids=("odni_governance_directives",),
    ),
    IntelligenceProfile(
        identifier="counterintelligence_source_integrity",
        title="Counterintelligence and Source-Integrity Defense",
        match_terms=(
            "counterintelligence",
            "ci",
            "source validation",
            "source protection",
            "insider",
            "non-state",
            "agent handling",
            "agent recruitment",
            "deception",
        ),
        anchor_keys=(
            "official_ncsc_counterintelligence_strategy",
            "official_odni_eo_12333",
            "official_odni_icd_206",
            "official_odni_icd_203",
            "official_cia_tradecraft_primer",
            "scholarly_heuer_psychology_intelligence_analysis",
            "official_cia_burkett_rascls",
            "scholarly_meissner_2017_hig",
            "scholarly_brimbal_2020_rapport",
            "scholarly_nunan_2020_chis_rapport",
            "scholarly_kelly_2013_interrogation_taxonomy",
        ),
        conceptual_focus=(
            "defending institutions, sources, and judgments against deception, "
            "insider risk, foreign-intelligence targeting, and source contamination"
        ),
        method_stack=(
            "threat awareness, source-descriptor audit, corroboration, anomaly "
            "review, red-team challenge, and protected disclosure paths"
        ),
        composability_contract=(
            "identity, access, reporting, corroboration, caveats, and confidence "
            "are modeled independently so defensive review can happen without exposure"
        ),
        failure_modes=(
            "source compromise, deception acceptance, identity overconfidence, "
            "insider blind spots, and collapsing CI concerns into undifferentiated IT-security triage"
        ),
        safety_boundary=(
            "CI content supports defensive awareness, source protection, and "
            "analytic integrity; it does not provide surveillance or handling playbooks"
        ),
        source_pack_ids=(
            "odni_privacy_oversight",
            "ic_current_threat_baseline",
        ),
    ),
    IntelligenceProfile(
        identifier="cognitive_influence_security",
        title="Cognitive Security and Influence Resilience",
        match_terms=(
            "cognitive",
            "psychological",
            "psyop",
            "influence",
            "disinformation",
            "social engineering",
            "information warfare",
            "prebunking",
        ),
        anchor_keys=(
            "official_cisa_foreign_influence",
            "official_nato_counter_information_threats",
            "official_cisa_election_security_influence",
            "official_nato_hybrid_threats",
            "official_oecd_disinformation_misinformation",
            "scholarly_gcsp_cognitive_security",
            "official_ic_ai_ethics_framework",
            "official_nist_ai_rmf",
            "scholarly_heuer_psychology_intelligence_analysis",
            "scholarly_mcguire_1961_inoculation",
            "scholarly_cardenuto_2023_synthetic_realities",
            "public_council_europe_information_disorder",
            "official_csis_crossing_deepfake_rubicon",
            "official_nsa_cisa_contextualizing_deepfake_threats",
            "scholarly_huang_2023_ai_cognitive_security_safety",
            "scholarly_deppe_schaal_2024_cognitive_warfare_nato",
            "scholarly_terp_breuer_2022_disarm",
            "scholarly_shah_2024_llm_disinformation",
            "scholarly_williams_2025_llm_election_disinformation",
            "scholarly_uchendu_2023_llm_disinformation_detection",
            "scholarly_farid_bohacek_2022_deepfake_leaders",
            "scholarly_golob_2020_social_engineering_cognition",
        ),
        conceptual_focus=(
            "protecting attention, belief formation, and decision quality without "
            "turning resilience education into manipulation"
        ),
        method_stack=(
            "claim decomposition, narrative provenance, inoculation framing, "
            "bias checks, audience-risk review, and after-action learning"
        ),
        composability_contract=(
            "separate descriptive analysis, normative assessment, response "
            "options, and protected-audience considerations"
        ),
        failure_modes=(
            "counter-messaging as manipulation, overclaiming intent, pathologizing "
            "audiences, and collapsing uncertainty into moral certainty"
        ),
        safety_boundary=(
            "practice uses benign simulations and resilience education; it does "
            "not create persuasion campaigns, impersonation, or deception plans"
        ),
    ),
    IntelligenceProfile(
        identifier="cognitive_active_inference",
        title="Active-Inference Theory and Governed Agent Analogy",
        match_terms=(
            "active inference",
            "free energy",
            "predictive processing",
            "expected free energy",
            "generative model",
            "shared protentions",
        ),
        anchor_keys=(
            "scholarly_friston_2010_fep",
            "scholarly_buckley_2017_fep_mathematical_review",
            "scholarly_friston_2017_active_inference_process",
            "scholarly_dacosta_2020_discrete_active_inference",
            "scholarly_parr_2022_active_inference_textbook",
            "scholarly_friston_2015_active_inference_epistemic_value",
            "scholarly_friston_2017_uncertainty_epistemics",
            "scholarly_smith_2022_active_inference_tutorial",
            "scholarly_friedman_2021_active_inference_conflict",
            "official_nist_ai_rmf",
            "official_nist_ai_600_1",
            "official_canada_agentic_ai_guide",
        ),
        conceptual_focus=(
            "using free-energy and active-inference theory as a bounded "
            "computational vocabulary for perception, action, uncertainty, and "
            "policy selection while keeping AGEINT governance claims separate"
        ),
        method_stack=(
            "formal-source review, theory-to-analogy mapping, assumption listing, "
            "implementation-evidence check, governance-control mapping, and "
            "human-review caveat"
        ),
        composability_contract=(
            "formal claim, pedagogical analogy, implementation assumption, "
            "evaluation evidence, and governance duty remain distinct fields"
        ),
        failure_modes=(
            "treating a formal theory as product evidence, using analogy as "
            "architecture proof, citing policy guidance for mathematical claims, "
            "and letting autonomy language outrun evaluation evidence"
        ),
        safety_boundary=(
            "active-inference material stays theoretical and classroom bounded; "
            "it does not prove autonomous action, intent detection, operational "
            "performance, or deployment without explicit authority and review"
        ),
    ),
    IntelligenceProfile(
        identifier="historical_declassified_sources",
        title="Historical and Declassified Intelligence Services",
        match_terms=(
            "historical intelligence services",
            "historical",
            "soviet",
            "russian",
            "american intelligence history",
            "british",
            "allied",
            "israeli",
            "continental services",
            "declassified",
        ),
        anchor_keys=(
            "official_cia_center_for_study_of_intelligence",
            "official_nsa_historical_releases",
            "official_nro_declassified_programs",
            "official_nara_cia_records",
            "official_odni_objectivity",
            "scholarly_heuer_psychology_intelligence_analysis",
            "official_cia_tradecraft_primer",
        ),
        conceptual_focus=(
            "turning declassified records and official histories into safe "
            "institutional lessons about analytic judgment, secrecy, oversight, "
            "technical-intelligence evolution, and reform"
        ),
        method_stack=(
            "provenance review, declassification-status notation, institutional "
            "timeline building, case-to-principle translation, and uncertainty "
            "about redacted records"
        ),
        composability_contract=(
            "archive source, release channel, historical context, analytic lesson, "
            "oversight implication, and modern analogy remain explicitly separated"
        ),
        failure_modes=(
            "romanticized tradecraft, presentist interpretation, redaction "
            "overclaiming, decontextualized case reuse, and translating history "
            "into operational instructions"
        ),
        safety_boundary=(
            "historical modules use declassified or public records for analysis "
            "and governance lessons only; they do not reconstruct live tactics, "
            "sources, methods, or current field procedures"
        ),
        source_pack_ids=(
            "declassified_history",
            "cia_intelligence_profession",
        ),
    ),
    IntelligenceProfile(
        identifier="cyber_threat_intelligence",
        title="Cyber Threat Intelligence, Incident Response, and Supply-Chain Defense",
        match_terms=(
            "cyber intelligence",
            "advanced persistent",
            "apt",
            "supply-chain",
            "supply chain",
            "threat intelligence",
            "cyber response",
            "incident",
            "sharing",
        ),
        anchor_keys=(
            "official_nist_sp_800_150",
            "official_oasis_stix_21",
            "official_oasis_taxii_21",
            "official_mitre_attack_enterprise",
            "official_cisa_kev_catalog",
            "official_nist_sp_800_61r3",
            "official_oecd_ai_incident_reporting_framework",
            "official_nist_sp_800_161r1",
            "official_nist_sp_800_137",
            "official_nist_sp_800_172",
            "official_nist_csf_2",
            "official_nist_ssdf",
            "official_mitre_atlas",
            "official_cisa_deploying_ai_systems_securely",
            "official_cset_adversarial_ml_cybersecurity_2022",
            "scholarly_taddeo_floridi_2018_ai_cyber_arms_race",
            "official_darpa_active_social_engineering_defense",
            "scholarly_penmetsa_2025_adversarial_ml_cybersecurity",
            "scholarly_wasil_2024_ai_emergency_preparedness",
        ),
        conceptual_focus=(
            "turning indicators, TTPs, incidents, vendor risk, and response "
            "lessons into shareable defensive intelligence with clear handling rules"
        ),
        method_stack=(
            "threat-information sharing goals, indicator/TTP normalization, "
            "incident-response review, supply-chain risk assessment, and lessons learned"
        ),
        composability_contract=(
            "indicators, TTP mappings, affected assets, supplier evidence, "
            "response actions, and sharing constraints remain independently reusable"
        ),
        failure_modes=(
            "indicator fixation, unvetted sharing, vendor-assurance drift, "
            "weak incident scoping, and treating CTI as a feed instead of a workflow"
        ),
        safety_boundary=(
            "cyber material stays defensive and tabletop-based; it does not "
            "provide exploit, persistence, evasion, or live-response instructions"
        ),
        source_pack_ids=(
            "ic_cyber_geoint_history",
            "odni_governance_directives",
        ),
    ),
    IntelligenceProfile(
        identifier="ics_ot_defense",
        title="ICS/OT Cyber-Physical Defense and Tabletop Readiness",
        match_terms=(
            "ics",
            "industrial",
            "operational technology",
            "cyber-physical",
            "critical infrastructure",
            "mitre",
            "att&ck",
        ),
        anchor_keys=(
            "official_nist_csf_2",
            "official_nist_sp_800_160r1",
            "official_nist_sp_800_82r3",
            "official_isa_iec_62443",
            "official_cisa_cross_sector_cpg",
            "official_cisa_ics_recommended_practices",
            "official_mitre_attack_ics",
            "official_cisa_tabletop_exercises",
            "official_nist_sp_800_84",
            "official_nsa_ai_ot_integration",
            "official_nist_cyber_physical_framework",
            "official_nist_sp_1800_10_ics_integrity",
            "official_nist_ai_rmf_critical_infrastructure_profile_concept",
            "official_cisa_secure_by_demand_ot_procurement",
            "official_cisa_ot_asset_inventory_guidance",
            "official_cisa_ot_definitive_architecture",
        ),
        conceptual_focus=(
            "defensive intelligence for safety-critical environments where "
            "availability, engineering state, and physical consequence matter"
        ),
        method_stack=(
            "asset/consequence mapping, ATT&CK-for-ICS coverage review, "
            "defense-in-depth audit, remote-access check, and tabletop injects"
        ),
        composability_contract=(
            "separate cyber indicators, engineering observations, safety impacts, "
            "operator decisions, and recovery actions"
        ),
        failure_modes=(
            "IT-first assumptions, unsafe automation, untested shutdown logic, "
            "poor remote-access control, and missing after-action learning"
        ),
        safety_boundary=(
            "all ICS work remains tabletop, lab, or accountable defensive review; "
            "no exploitation, unsafe process manipulation, or live control actions"
        ),
    ),
    IntelligenceProfile(
        identifier="legal_oversight",
        title="Legal, Ethical, and Oversight Architecture",
        match_terms=("legal", "ethical", "oversight", "authority", "governance", "privacy"),
        anchor_keys=(
            "official_odni_eo_12333",
            "official_nsa_fisa",
            "official_eu_ai_act",
            "official_council_europe_ai_convention",
            "official_pclob_oversight_reports",
            "official_ic_ai_ethics_principles",
            "official_ic_ai_ethics_framework",
            "official_odni_icd_505",
            "official_nist_ai_rmf",
            "official_imda_agentic_ai_framework",
            "official_nist_privacy_framework",
            "official_nist_sp_800_53r5",
            "official_nist_sp_800_30r1",
            "official_nist_sp_800_37r2",
            "official_nist_sp_800_39",
            "official_nist_ir_8477_mappings",
            "official_oecd_governing_with_ai_public_sector",
            "official_canada_algorithmic_impact_assessment",
            "official_canada_ai_register",
            "official_un_global_digital_compact",
            "official_nara_2025_ai_compliance_plan",
            "official_us_copyright_ai_training_report",
            "official_wipo_ai_ip_policy",
            "official_odni_icd_203",
            "official_odni_icd_206",
            "scholarly_ortega_2025_ai_incident_regime",
        ),
        conceptual_focus=(
            "turning authority, accountability, transparency, and review into "
            "design constraints rather than post-hoc paperwork"
        ),
        method_stack=(
            "authority mapping, role assignment, impact assessment, documentation "
            "review, escalation triggers, and independent oversight"
        ),
        composability_contract=(
            "policies, approvals, audit logs, evidence, and action permissions "
            "remain linked but independently inspectable"
        ),
        failure_modes=(
            "authority laundering through tools, missing audit trails, privacy "
            "overreach, and treating governance as a static checklist"
        ),
        safety_boundary=(
            "governance content supports lawful design, education, and review; it "
            "does not justify unauthorized collection or deployment"
        ),
        source_pack_ids=(
            "odni_privacy_oversight",
            "odni_disclosure_and_tearlines",
        ),
    ),
    IntelligenceProfile(
        identifier="operator_productivity",
        title="Operator Productivity and Cognitive Performance",
        match_terms=(
            "intelligent operator",
            "cognitive athlete",
            "productivity intelligence",
            "getting things done",
            "flow state",
            "nasa-tlx",
            "cognitive load",
            "circadian intelligence",
        ),
        anchor_keys=(
            "official_odni_icd_203",
            "scholarly_heuer_psychology_intelligence_analysis",
            "official_nist_sp_800_161r1",
        ),
        conceptual_focus=(
            "sustained intelligence work as cognitive performance engineering: "
            "external memory, workload measurement, flow conditions, and "
            "decision hygiene under operational tempo"
        ),
        method_stack=(
            "GTD capture-clarify-organize cycles, NASA-TLX workload review, "
            "flow precondition checklists, task-switching audits, and "
            "reviewer handoff under fatigue"
        ),
        composability_contract=(
            "requirements queues, workload signals, focus blocks, evidence "
            "packets, and reviewer checkpoints remain separable artifacts"
        ),
        failure_modes=(
            "heroic overtime, invisible cognitive debt, context-switch thrash, "
            "uncalibrated confidence under load, and skipping handoff review"
        ),
        safety_boundary=(
            "productivity material stays educational and synthetic; it does not "
            "prescribe live operational tempo, surveillance of people, or "
            "performance coercion"
        ),
    ),
)

INTELLIGENCE_PROFILES: Final[tuple[IntelligenceProfile, ...]] = (
    _INTELLIGENCE_PROFILES_CORE + _INTELLIGENCE_PROFILES_EXTENDED
)
