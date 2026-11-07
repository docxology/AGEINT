from __future__ import annotations

from typing import Final

from ._01_part import ResearchAnchor, SafePatternProfile
from ._02_part import INTELLIGENCE_RESEARCH_ANCHORS, SOURCE_QUALITY_RESEARCH_ANCHORS


ANCHORS_BY_KEY: Final[dict[str, ResearchAnchor]] = {anchor.key: anchor for anchor in INTELLIGENCE_RESEARCH_ANCHORS}

SOURCE_QUALITY_REFERENCE_FALLBACKS: Final[dict[str, ResearchAnchor]] = {anchor.key: anchor for anchor in SOURCE_QUALITY_RESEARCH_ANCHORS}

ALL_PROFILE_ANCHORS_BY_KEY: Final[dict[str, ResearchAnchor]] = {**SOURCE_QUALITY_REFERENCE_FALLBACKS, **ANCHORS_BY_KEY}

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
        application="accountable bibliography, source inventory, or standards-mapping exercise",
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
        safety_boundary="keeps every tool revocable, observable, and constrained to evidence-bounded actions",
    ),
    11: SafePatternProfile(
        key="surveillance_agent",
        safe_name="Monitoring-Governance Tabletop Agent",
        methods="synthetic event polling, threshold rationale, alert review, and escalation logging",
        application="accountable monitoring governance exercise over toy asset-health records",
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
        application="ethics exercise that detects fabricated identity artifacts in clearly synthetic materials",
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
        safety_boundary=("limits work to non-sensitive metadata quality, uncertainty notes, and synthetic location examples"),
    ),
    19: SafePatternProfile(
        key="cognitive_inoculant",
        safe_name="Cognitive-Resilience Education Agent",
        methods="manipulation-technique labeling, transparent prebunking, and audience-harm review",
        application="opt-in media-literacy micro-lesson for a sample classroom scenario",
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
