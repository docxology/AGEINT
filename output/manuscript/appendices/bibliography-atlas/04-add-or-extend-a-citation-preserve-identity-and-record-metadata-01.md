## Add or extend a citation: preserve identity and record metadata

**Section anchor.** [@sec:bibliography_atlas].

1. Preserve `ageint001` through `ageint231`; do not renumber locked source identities.
2. Append new source-guide references after the locked range. Current generated guide keys extend through `ageint312`.
3. For curated anchors, record `source_lane`, `source_tier`, `checked_as_of`, `verification_method`, `claim_scope`, `refresh_cadence`, `refresh_trigger`, `stakeholder_role`, `assurance_use`, and `rights_dimension`.
4. Use Pandoc citation syntax such as `[@ageint137]` or `[@official_nist_ai_rmf]`.
5. Use label-backed cross-references to the curriculum orientation section and curriculum-map figure rather than hard-coded section or figure numbers.
6. Rebuild from the AGEINT root:

```bash
uv run python scripts/build_curriculum.py
```

never hand-edit `output/manuscript/` as the source of truth.

### Current citation coverage by source section

**Coverage anchor.** Parent appendix: [@sec:bibliography_atlas]. Citation coverage by source section is validated from the generated citation inventory.

| Measure | Count |
|---|---:|
| Source sections | 723 |
| Citation occurrences | 1468 |
| Unique source-guide keys | 301 |
| Zero-citation source sections | 0 |
| Distribution | 1 citation(s): 275 section(s), 2 citation(s): 154 section(s), 3 citation(s): 291 section(s), 4 citation(s): 3 section(s) |

### Citation rows by source section

| Section | Module and source section | Citations | Citation links |
|---:|---|---:|---|
| 1.99 | The Nature of Intelligence - V2 source-lane extension: bind The Nature of Intelligence to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint238]; [@ageint237]; [@ageint270] |
| 1.101 | The Nature of Intelligence - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for The Nature of Intelligence | 3 | [@ageint273]; [@ageint274]; [@ageint275] |
| 1.102 | The Nature of Intelligence - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for The Nature of Intelligence | 3 | [@ageint286]; [@ageint287]; [@ageint292] |
| 1.1 | The Nature of Intelligence - Defining Intelligence: Collection, Analysis, Production, Dissemination | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| 1.2 | The Nature of Intelligence - The Intelligence Cycle (Classic, Revised, and Critique) | 2 | [@ageint297]; [@ageint298] |
| 1.3 | The Nature of Intelligence - Types: Strategic, Operational, Tactical, Technical Intelligence | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| 1.4 | The Nature of Intelligence - Intelligence as Social and Epistemological Practice | 1 | [@ageint001] |
| 1.5 | The Nature of Intelligence - National, Corporate, and Private Intelligence: Structural Differences | 2 | [@ageint297]; [@ageint298] |
| 1.6 | The Nature of Intelligence - The Ethics of Intelligence: EO 12333, FISA, ICD 203, Allied Law | 1 | [@ageint002] |
| 1.7 | The Nature of Intelligence - Active Inference as a Unifying Cognitive Framework for Intelligence | 1 | [@ageint003] |
| 1.8 | The Nature of Intelligence - The AI Inflection Point: How Artificial Intelligence Reshapes Every Phase of the Intelligence Cycle | 2 | [@ageint004]; [@ageint005] |
| 2.99 | Intelligence Community Architectures - V2 source-lane extension: bind Intelligence Community Architectures to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint234]; [@ageint247]; [@ageint249] |
| 2.101 | Intelligence Community Architectures - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Intelligence Community Architectures | 3 | [@ageint276]; [@ageint277]; [@ageint284] |
| 2.102 | Intelligence Community Architectures - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Intelligence Community Architectures | 3 | [@ageint288]; [@ageint289]; [@ageint293] |
| 2.1 | Intelligence Community Architectures - U.S. Intelligence Community: 18 Agencies, Authorities, and Relationships | 1 | [@ageint006] |
| 2.2 | Intelligence Community Architectures - Soviet/Russian Architecture: Cheka → GPU → NKVD → MGB → KGB → SVR/FSB/GRU | 2 | [@ageint297]; [@ageint298] |
| 2.3 | Intelligence Community Architectures - British Architecture: MI5, MI6/SIS, GCHQ, DI, JIC | 1 | [@ageint007] |
| 2.4 | Intelligence Community Architectures - Israeli Architecture: Mossad, Shin Bet, Unit 8200, LAKAM | 1 | [@ageint008] |
| 2.5 | Intelligence Community Architectures - Chinese Architecture: MSS, PLA-SSF, United Front Work Department, APT Groups | 1 | [@ageint009] |
| 2.6 | Intelligence Community Architectures - Five Eyes and Allied Intelligence Sharing: BRUSA to UKUSA | 2 | [@ageint010]; [@ageint011] |
| 2.7 | Intelligence Community Architectures - Non-State Intelligence Actors: Terrorist, Criminal, PMC | 1 | [@ageint012] |
| 2.8 | Intelligence Community Architectures - Fusion Centers, JITFs, and Inter-Agency Coordination | 2 | [@ageint297]; [@ageint298] |
| 2.9 | Intelligence Community Architectures - Intelligence Oversight: Congressional, Judicial, Executive Mechanisms | 2 | [@ageint298]; [@ageint297] |
| 3.99 | Tradecraft: Core Principles - V2 source-lane extension: bind Tradecraft: Core Principles to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint237]; [@ageint266]; [@ageint269] |
| 3.101 | Tradecraft: Core Principles - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Tradecraft: Core Principles | 3 | [@ageint278]; [@ageint279]; [@ageint283] |
| 3.102 | Tradecraft: Core Principles - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Tradecraft: Core Principles | 3 | [@ageint290]; [@ageint291]; [@ageint294] |
| 3.1 | Tradecraft: Core Principles - What Is Tradecraft? Historical Definitions and Evolution | 2 | [@ageint013]; [@ageint014] |
| 3.2 | Tradecraft: Core Principles - Operational Security (OPSEC): Process and the Five-Step Method | 2 | [@ageint297]; [@ageint298] |
| 3.3 | Tradecraft: Core Principles - Compartmentation: Need-to-Know vs. Need-to-Share | 2 | [@ageint297]; [@ageint298] |
| 3.4 | Tradecraft: Core Principles - Cover: Official, Non-Official Cover (NOC), Deep Cover, Legends | 1 | [@ageint015] |
| 3.5 | Tradecraft: Core Principles - The Principle of Plausible Deniability | 2 | [@ageint297]; [@ageint298] |
| 3.6 | Tradecraft: Core Principles - Pattern-of-Life Analysis and How to Disrupt It | 1 | [@ageint016] |
| 3.7 | Tradecraft: Core Principles - Situational Awareness: Urban and Rural Tradecraft | 1 | [@ageint014] |
| 3.8 | Tradecraft: Core Principles - Code Words, Glossaries, and the Language of Espionage | 1 | [@ageint017] |
| 3.9 | Tradecraft: Core Principles - Return of Classical Tradecraft in the AI Era: Dead Drops, Brush Passes, In-Person Exchanges | 3 | [@ageint018]; [@ageint005]; [@ageint019] |
| 4.99 | Agent Recruitment - V2 source-lane extension: bind Agent Recruitment to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint238]; [@ageint239]; [@ageint240] |
| 4.101 | Agent Recruitment - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Agent Recruitment | 3 | [@ageint280]; [@ageint281]; [@ageint282] |
| 4.102 | Agent Recruitment - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Agent Recruitment | 3 | [@ageint292]; [@ageint295]; [@ageint296] |
| 4.1 | Agent Recruitment - The MICE Framework: Money, Ideology, Coercion/Compromise, Ego | 2 | [@ageint020]; [@ageint021] |
| 4.2 | Agent Recruitment - MICE Expanded: RASCLS — Reciprocity, Authority, Scarcity, Commitment, Liking, Social Proof | 2 | [@ageint298]; [@ageint297] |
| 4.3 | Agent Recruitment - Targeting, Spotting, and Initial Assessment | 2 | [@ageint020]; [@ageint021] |
| 4.4 | Agent Recruitment - Assessment and Development Operations | 2 | [@ageint020]; [@ageint021] |
| 4.5 | Agent Recruitment - The Recruitment Pitch: Methods and Psychology | 1 | [@ageint020] |
| 4.6 | Agent Recruitment - KGB Recruitment Doctrine: Psychological Methods and Manipulation | 2 | [@ageint021]; [@ageint022] |
| 4.7 | Agent Recruitment - Digital-Age Recruitment: LinkedIn, Telegram, Cryptocurrencies, Dark Web | 1 | [@ageint023] |
| 4.8 | Agent Recruitment - Shared Experience as a Recruitment Tool: Experimental Research | 1 | [@ageint024] |
| 4.9 | Agent Recruitment - How AI Lowers the Cost of Recruitment and Social Engineering | 1 | [@ageint004] |
| 4.10 | Agent Recruitment - Recruitment Ethics and Legal Constraints | 2 | [@ageint298]; [@ageint297] |
| 5.99 | Agent Handling and Management - V2 source-lane extension: bind Agent Handling and Management to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint239]; [@ageint240]; [@ageint241] |
| 5.101 | Agent Handling and Management - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Agent Handling and Management | 3 | [@ageint273]; [@ageint276]; [@ageint285] |
| 5.102 | Agent Handling and Management - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Agent Handling and Management | 3 | [@ageint286]; [@ageint290]; [@ageint294] |
| 5.1 | Agent Handling and Management - The Case Officer–Agent Relationship: Building, Maintaining, Testing Trust | 1 | [@ageint025] |
| 5.2 | Agent Handling and Management - Meeting Structures: Overt, Covert, and Clandestine | 2 | [@ageint029]; [@ageint004] |
| 5.3 | Agent Handling and Management - The Surveillance Detection Route (SDR) | 2 | [@ageint026]; [@ageint016] |
| 5.4 | Agent Handling and Management - Dead Drops: Physical and Digital Methods | 2 | [@ageint027]; [@ageint028] |
| 5.5 | Agent Handling and Management - Cutouts, Intermediaries, and Deniability Chains | 1 | [@ageint029] |
| 5.6 | Agent Handling and Management - Fronts and Shell Entities as Agent Infrastructure | 1 | [@ageint029] |
| 5.7 | Agent Handling and Management - Counter-Surveillance and Detecting Hostile Surveillance | 2 | [@ageint030]; [@ageint031] |
| 5.8 | Agent Handling and Management - Running Agents-in-Place: Frequency, Tasking, Validation | 2 | [@ageint029]; [@ageint004] |
| 5.9 | Agent Handling and Management - Burning, Exfiltrating, and Terminating Agents | 2 | [@ageint029]; [@ageint004] |
| 5.10 | Agent Handling and Management - KGB Working-with-Agents Doctrine (Declassified Manuals) | 1 | [@ageint032] |
| 5.11 | Agent Handling and Management - AI-Enhanced Micro-Expression Analysis for Source Validation | 1 | [@ageint004] |
| 5.12 | Agent Handling and Management - AI-Personalized Communication: Tailoring Persuasion to Source Personality | 1 | [@ageint004] |
| 6.99 | Source Protection and CI Integration - V2 source-lane extension: bind Source Protection and CI Integration to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint238]; [@ageint241]; [@ageint266] |
| 6.101 | Source Protection and CI Integration - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Source Protection and CI Integration | 3 | [@ageint274]; [@ageint278]; [@ageint280] |
| 6.102 | Source Protection and CI Integration - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Source Protection and CI Integration | 3 | [@ageint287]; [@ageint288]; [@ageint295] |
| 6.1 | Source Protection and CI Integration - Identifying Penetration: Signs of Compromise | 3 | [@ageint307]; [@ageint305]; [@ageint304] |
| 6.2 | Source Protection and CI Integration - Compartmentation in Agent Networks | 1 | [@ageint029] |
| 6.3 | Source Protection and CI Integration - Lie Detection, Vetting, Polygraph, and Its Alternatives | 3 | [@ageint307]; [@ageint305]; [@ageint304] |
| 6.4 | Source Protection and CI Integration - The Double-Agent Operation | 1 | [@ageint029] |
| 6.5 | Source Protection and CI Integration - Hostile Intelligence from Non-State Actors | 1 | [@ageint033] |
| 6.6 | Source Protection and CI Integration - Espionage in the AI Era: Why HUMINT Will Grow in Importance | 2 | [@ageint019]; [@ageint034] |
| 7.99 | SIGINT Fundamentals - V2 source-lane extension: bind SIGINT Fundamentals to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint255]; [@ageint258]; [@ageint261] |
| 7.101 | SIGINT Fundamentals - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for SIGINT Fundamentals | 3 | [@ageint279]; [@ageint282]; [@ageint284] |
| 7.102 | SIGINT Fundamentals - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for SIGINT Fundamentals | 3 | [@ageint289]; [@ageint291]; [@ageint296] |
| 7.1 | SIGINT Fundamentals - COMINT and ELINT: Definitions and Distinctions | 1 | [@ageint035] |
| 7.2 | SIGINT Fundamentals - Historical Foundations: WWII Axis SIGINT (NSA Declassified 9 Volumes) | 1 | [@ageint036] |
| 7.3 | SIGINT Fundamentals - Spartans in Darkness: SIGINT in the Indochina War, 1945–1975 | 1 | [@ageint037] |
| 7.4 | SIGINT Fundamentals - CIA–NSA SIGINT Relationship, 1947–1970 | 2 | [@ageint038]; [@ageint039] |
| 7.5 | SIGINT Fundamentals - NSA Basic Cryptography (Friedman Documents) | 1 | [@ageint040] |
| 8.99 | Modern SIGINT and Cryptography - V2 source-lane extension: bind Modern SIGINT and Cryptography to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint258]; [@ageint260]; [@ageint261] |
| 8.101 | Modern SIGINT and Cryptography - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Modern SIGINT and Cryptography | 3 | [@ageint275]; [@ageint276]; [@ageint283] |
| 8.102 | Modern SIGINT and Cryptography - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Modern SIGINT and Cryptography | 3 | [@ageint286]; [@ageint293]; [@ageint295] |
| 8.1 | Modern SIGINT and Cryptography - UKUSA and Five Eyes SIGINT Sharing | 2 | [@ageint041]; [@ageint042] |
| 8.2 | Modern SIGINT and Cryptography - Bulk Collection, Metadata Analysis, and Legal Frameworks | 2 | [@ageint298]; [@ageint297] |
| 8.3 | Modern SIGINT and Cryptography - The Cryptographic Arms Race: E2E Encryption and Lawful Access | 2 | [@ageint297]; [@ageint298] |
| 8.4 | Modern SIGINT and Cryptography - Covert Communications Tradecraft: OTPs, Burst Transmission, Digital Dead Drops | 2 | [@ageint027]; [@ageint028] |
| 8.5 | Modern SIGINT and Cryptography - Radio Frequency Intelligence (RFINT) and Technical Surveillance | 2 | [@ageint043]; [@ageint044] |
| 8.6 | Modern SIGINT and Cryptography - Technical Surveillance Countermeasures (TSCM): Threat Levels and Detection | 2 | [@ageint045]; [@ageint046] |
| 8.7 | Modern SIGINT and Cryptography - Non-Linear Junction Detectors, RF Spectrum Analysis, Infrared Imaging | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| 8.8 | Modern SIGINT and Cryptography - Steganography: LSB, DCT, and Network-Layer Methods | 1 | [@ageint028] |
| 8.9 | Modern SIGINT and Cryptography - Signal Authentication in the Deepfake Era | 1 | [@ageint018] |
| 9.99 | OSINT Foundations - V2 source-lane extension: bind OSINT Foundations to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint251]; [@ageint253]; [@ageint269] |
| 9.101 | OSINT Foundations - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for OSINT Foundations | 3 | [@ageint273]; [@ageint274]; [@ageint275] |
| 9.102 | OSINT Foundations - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for OSINT Foundations | 3 | [@ageint286]; [@ageint287]; [@ageint292] |
| 9.1 | OSINT Foundations - History and Rise of OSINT in the Intelligence Community | 1 | [@ageint047] |
| 9.2 | OSINT Foundations - IC OSINT Strategy 2024–2026 | 1 | [@ageint048] |
| 9.3 | OSINT Foundations - OSINT vs. HUMINT vs. SIGINT: Comparative Value and Fusion | 2 | [@ageint301]; [@ageint298] |
| 9.4 | OSINT Foundations - Legal and Ethical Constraints in OSINT Collection | 2 | [@ageint298]; [@ageint297] |
| 9.5 | OSINT Foundations - OPSEC for OSINT Operators: The Sock Puppet Problem | 2 | [@ageint301]; [@ageint298] |
| 9.6 | OSINT Foundations - Open Source Intelligence: Trends and Issues | 1 | [@ageint049] |
| 10.99 | OSINT Techniques and Tools - V2 source-lane extension: bind OSINT Techniques and Tools to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint251]; [@ageint252]; [@ageint269] |
| 10.101 | OSINT Techniques and Tools - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for OSINT Techniques and Tools | 3 | [@ageint276]; [@ageint277]; [@ageint284] |
| 10.102 | OSINT Techniques and Tools - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for OSINT Techniques and Tools | 3 | [@ageint288]; [@ageint289]; [@ageint293] |
| 10.1 | OSINT Techniques and Tools - Search Engine Tradecraft: Google Dorking, Yandex, Bing, Shodan | 2 | [@ageint050]; [@ageint051] |
| 10.2 | OSINT Techniques and Tools - Social Media OSINT: Scraping, Graph Analysis, Identity Verification | 2 | [@ageint051]; [@ageint052] |
| 10.3 | OSINT Techniques and Tools - Maltego: Graph-Based OSINT Investigation | 1 | [@ageint051] |
| 10.4 | OSINT Techniques and Tools - Recon-ng: Python-Based Reconnaissance Framework | 2 | [@ageint052]; [@ageint053] |
| 10.5 | OSINT Techniques and Tools - SpiderFoot: Automated OSINT Collection | 1 | [@ageint052] |
| 10.6 | OSINT Techniques and Tools - FOCA, TheHarvester, Sherlock: Targeted Investigation Tools | 1 | [@ageint054] |
| 10.7 | OSINT Techniques and Tools - OSINT Framework (osintframework.com): Module Taxonomy | 2 | [@ageint051]; [@ageint052] |
| 10.8 | OSINT Techniques and Tools - Offline OSINT Environments: VM Architecture and Isolation | 2 | [@ageint051]; [@ageint052] |
| 10.9 | OSINT Techniques and Tools - IntelTechniques OSINT 11th Edition Methods and Workflows | 2 | [@ageint055]; [@ageint056] |
| 11.99 | GEOINT and Imagery Intelligence - V2 source-lane extension: bind GEOINT and Imagery Intelligence to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint253]; [@ageint255]; [@ageint270] |
| 11.101 | GEOINT and Imagery Intelligence - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for GEOINT and Imagery Intelligence | 3 | [@ageint278]; [@ageint279]; [@ageint283] |
| 11.102 | GEOINT and Imagery Intelligence - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for GEOINT and Imagery Intelligence | 3 | [@ageint290]; [@ageint291]; [@ageint294] |
| 11.1 | GEOINT and Imagery Intelligence - Geospatial Intelligence Fundamentals: IMINT, GEOINT, Mapping | 1 | [@ageint057] |
| 11.2 | GEOINT and Imagery Intelligence - GEOINT Essential Body of Knowledge (USGIF) | 1 | [@ageint058] |
| 11.3 | GEOINT and Imagery Intelligence - Commercial Satellite Platforms: Maxar, Planet, Sentinel-1/2 | 1 | [@ageint059] |
| 11.4 | GEOINT and Imagery Intelligence - Change Detection and Pattern-of-Life Imagery Analysis | 2 | [@ageint302]; [@ageint297] |
| 11.5 | GEOINT and Imagery Intelligence - GEOINT in Counterinsurgency and Strike Operations | 2 | [@ageint302]; [@ageint297] |
| 11.6 | GEOINT and Imagery Intelligence - DoD GEOINT Accreditation and Training Standards | 1 | [@ageint060] |
| 11.7 | GEOINT and Imagery Intelligence - MCRP 2-10B.4: USMC GEOINT Manual | 1 | [@ageint057] |
| 11.8 | GEOINT and Imagery Intelligence - AI-Assisted Satellite Image Analysis: Object Detection and Chronolocation | 2 | [@ageint302]; [@ageint297] |
| 11.9 | GEOINT and Imagery Intelligence - Open-Source Geospatial Intelligence Library | 1 | [@ageint059] |
| 12.99 | Cyber Intelligence Fundamentals - V2 source-lane extension: bind Cyber Intelligence Fundamentals to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint258]; [@ageint261]; [@ageint266] |
| 12.101 | Cyber Intelligence Fundamentals - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Cyber Intelligence Fundamentals | 3 | [@ageint280]; [@ageint281]; [@ageint282] |
| 12.102 | Cyber Intelligence Fundamentals - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Cyber Intelligence Fundamentals | 3 | [@ageint292]; [@ageint295]; [@ageint296] |
| 12.1 | Cyber Intelligence Fundamentals - The Cyber Kill Chain (Lockheed Martin) | 2 | [@ageint061]; [@ageint062] |
| 12.2 | Cyber Intelligence Fundamentals - MITRE ATT&CK Framework: Enterprise Matrix v19 | 2 | [@ageint063]; [@ageint064] |
| 12.2.1 | Cyber Intelligence Fundamentals - Reconnaissance through Resource Development | 1 | [@ageint063] |
| 12.2.2 | Cyber Intelligence Fundamentals - Initial Access, Execution, Persistence, Privilege Escalation | 1 | [@ageint065] |
| 12.2.3 | Cyber Intelligence Fundamentals - Defense Evasion, Credential Access, Discovery, Lateral Movement | 3 | [@ageint300]; [@ageint303]; [@ageint304] |
| 12.2.4 | Cyber Intelligence Fundamentals - Collection, Command & Control, Exfiltration, Impact | 2 | [@ageint062]; [@ageint063] |
| 12.3 | Cyber Intelligence Fundamentals - Unified Kill Chain: Extending Lockheed + MITRE | 1 | [@ageint062] |
| 12.4 | Cyber Intelligence Fundamentals - Threat Intelligence Sharing: STIX/TAXII Standards | 3 | [@ageint066]; [@ageint067]; [@ageint068] |
| 12.5 | Cyber Intelligence Fundamentals - Nation-State Cyber Espionage: Motivations and Methods | 1 | [@ageint069] |
| 12.6 | Cyber Intelligence Fundamentals - Chinese State-Affiliated Hacking: APT10, APT41, Volt Typhoon | 2 | [@ageint009]; [@ageint070] |
| 12.7 | Cyber Intelligence Fundamentals - Russian Cyber Operations: Sandworm, Cozy Bear, Fancy Bear | 3 | [@ageint300]; [@ageint303]; [@ageint304] |
| 12.8 | Cyber Intelligence Fundamentals - Living-Off-The-Land (LOTL) Techniques in APT Operations | 1 | [@ageint071] |
| 13.99 | Advanced Persistent Threats (APTs) - V2 source-lane extension: bind Advanced Persistent Threats (APTs) to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint237]; [@ageint258]; [@ageint261] |
| 13.101 | Advanced Persistent Threats (APTs) - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Advanced Persistent Threats (APTs) | 3 | [@ageint273]; [@ageint276]; [@ageint285] |
| 13.102 | Advanced Persistent Threats (APTs) - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Advanced Persistent Threats (APTs) | 3 | [@ageint286]; [@ageint290]; [@ageint294] |
| 13.1 | Advanced Persistent Threats (APTs) - APT Definitions, Lifecycle, and Attribution | 1 | [@ageint072] |
| 13.2 | Advanced Persistent Threats (APTs) - APT Risk Propagation Models: ATT&CK-Based Analysis | 1 | [@ageint072] |
| 13.3 | Advanced Persistent Threats (APTs) - Nation-State vs. Ideological Actor Attack Patterns | 1 | [@ageint069] |
| 13.4 | Advanced Persistent Threats (APTs) - APT Infrastructure: C2 Frameworks, Domain Fronting, Bulletproof Hosting | 3 | [@ageint300]; [@ageint303]; [@ageint304] |
| 13.5 | Advanced Persistent Threats (APTs) - Incident Response on Nation-State Intrusions: Mandiant Methodology | 1 | [@ageint071] |
| 13.6 | Advanced Persistent Threats (APTs) - Threat Hunting Against APT Actors | 3 | [@ageint300]; [@ageint303]; [@ageint304] |
| 13.7 | Advanced Persistent Threats (APTs) - APT Attribution: Technical Indicators vs. Geopolitical Context | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| 14.99 | Supply Chain Intelligence Attacks - V2 source-lane extension: bind Supply Chain Intelligence Attacks to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint258]; [@ageint266]; [@ageint268] |
| 14.101 | Supply Chain Intelligence Attacks - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Supply Chain Intelligence Attacks | 3 | [@ageint274]; [@ageint278]; [@ageint280] |
| 14.102 | Supply Chain Intelligence Attacks - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Supply Chain Intelligence Attacks | 3 | [@ageint287]; [@ageint288]; [@ageint295] |
| 14.1 | Supply Chain Intelligence Attacks - Supply Chain Operations as Strategic Intelligence Tradecraft | 2 | [@ageint297]; [@ageint298] |
| 14.2 | Supply Chain Intelligence Attacks - SolarWinds/SUNBURST: The Six-Month Patient Operation | 1 | [@ageint073] |
| 14.3 | Supply Chain Intelligence Attacks - XZ Utils/Jia Tan: Two-Year Social Engineering and Trust Infiltration | 3 | [@ageint074]; [@ageint075]; [@ageint076] |
| 14.3.1 | Supply Chain Intelligence Attacks - Sock Puppetry as HUMINT Cover Tradecraft | 1 | [@ageint076] |
| 14.3.2 | Supply Chain Intelligence Attacks - CVE-2024-3094: CVSS 10.0 Backdoor Mechanism | 1 | [@ageint076] |
| 14.3.3 | Supply Chain Intelligence Attacks - Attribution Indicators: APT29/SVR Pattern Similarities | 1 | [@ageint076] |
| 14.3.4 | Supply Chain Intelligence Attacks - "Friendly Yet Aggressive and Persistent" Social Engineering Signature | 1 | [@ageint076] |
| 14.4 | Supply Chain Intelligence Attacks - Open-Source Maintainer Targeting as an Acquisition Operation | 1 | [@ageint076] |
| 14.5 | Supply Chain Intelligence Attacks - Countermeasures: SBOM, SLSA Framework, Sigstore | 3 | [@ageint300]; [@ageint304]; [@ageint306] |
| 14.6 | Supply Chain Intelligence Attacks - Threat Intelligence Sharing for ICS Supply Chain (arXiv Survey) | 1 | [@ageint077] |
| 15.99 | Electronic and Emanations Intelligence - V2 source-lane extension: bind Electronic and Emanations Intelligence to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint255]; [@ageint256]; [@ageint261] |
| 15.101 | Electronic and Emanations Intelligence - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Electronic and Emanations Intelligence | 3 | [@ageint279]; [@ageint282]; [@ageint284] |
| 15.102 | Electronic and Emanations Intelligence - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Electronic and Emanations Intelligence | 3 | [@ageint289]; [@ageint291]; [@ageint296] |
| 15.1 | Electronic and Emanations Intelligence - ELINT: Radar Signatures and Weapons Systems Emissions | 1 | [@ageint035] |
| 15.2 | Electronic and Emanations Intelligence - EMINT: C4I System Emanations | 1 | [@ageint078] |
| 15.3 | Electronic and Emanations Intelligence - Tempest and Van Eck Radiation: Standards and Countermeasures | 3 | [@ageint300]; [@ageint303]; [@ageint304] |
| 15.4 | Electronic and Emanations Intelligence - Software-Defined Radio (SDR) for Intelligence Applications | 3 | [@ageint303]; [@ageint304]; [@ageint305] |
| 15.5 | Electronic and Emanations Intelligence - RF Mapping and Spectrum Intelligence | 2 | [@ageint302]; [@ageint297] |
| 16.99 | Imagery Intelligence (IMINT) - V2 source-lane extension: bind Imagery Intelligence (IMINT) to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint253]; [@ageint269]; [@ageint270] |
| 16.101 | Imagery Intelligence (IMINT) - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Imagery Intelligence (IMINT) | 3 | [@ageint275]; [@ageint276]; [@ageint283] |
| 16.102 | Imagery Intelligence (IMINT) - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Imagery Intelligence (IMINT) | 3 | [@ageint286]; [@ageint293]; [@ageint295] |
| 16.1 | Imagery Intelligence (IMINT) - Types: Optical, SAR, Infrared, Hyperspectral, Multispectral | 2 | [@ageint302]; [@ageint297] |
| 16.2 | Imagery Intelligence (IMINT) - Collection Platforms: Satellites, UAVs, Aircraft, Ground-Based | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| 16.3 | Imagery Intelligence (IMINT) - Photo Interpretation and All-Source Imagery Analysis | 2 | [@ageint302]; [@ageint297] |
| 16.4 | Imagery Intelligence (IMINT) - Commercial IMINT and the Democratization of Space-Based Reconnaissance | 2 | [@ageint302]; [@ageint297] |
| 16.5 | Imagery Intelligence (IMINT) - Open-Source Geolocation Methods: Bellingcat Methodology | 2 | [@ageint302]; [@ageint297] |
| 17.99 | Financial Intelligence (FININT) - V2 source-lane extension: bind Financial Intelligence (FININT) to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint251]; [@ageint252]; [@ageint254] |
| 17.101 | Financial Intelligence (FININT) - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Financial Intelligence (FININT) | 3 | [@ageint273]; [@ageint274]; [@ageint275] |
| 17.102 | Financial Intelligence (FININT) - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Financial Intelligence (FININT) | 3 | [@ageint286]; [@ageint287]; [@ageint292] |
| 17.1 | Financial Intelligence (FININT) - FININT Foundations: Collection, Analysis, Reporting | 2 | [@ageint079]; [@ageint080] |
| 17.2 | Financial Intelligence (FININT) - Suspicious Activity Reports (SARs) and Financial Intelligence Units | 1 | [@ageint079] |
| 17.3 | Financial Intelligence (FININT) - Terrorist Financing: Identification, Typologies, Interdiction | 1 | [@ageint079] |
| 17.4 | Financial Intelligence (FININT) - The SWIFT System and Intelligence Collection | 1 | [@ageint079] |
| 17.5 | Financial Intelligence (FININT) - Cryptocurrency as Covert Finance: Monero, Mixers, Bridges | 2 | [@ageint302]; [@ageint297] |
| 17.6 | Financial Intelligence (FININT) - Economic Warfare and FININT as a Strategic Tool | 1 | [@ageint081] |
| 17.7 | Financial Intelligence (FININT) - Money Laundering Detection: Data Mining and Matching Techniques | 1 | [@ageint080] |
| 17.8 | Financial Intelligence (FININT) - FININT Supporting National Security: Pillars and Methods | 1 | [@ageint082] |
| 18.99 | PSYOP and MISO Doctrine - V2 source-lane extension: bind PSYOP and MISO Doctrine to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint238]; [@ageint239]; [@ageint242] |
| 18.101 | PSYOP and MISO Doctrine - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for PSYOP and MISO Doctrine | 3 | [@ageint276]; [@ageint277]; [@ageint284] |
| 18.102 | PSYOP and MISO Doctrine - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for PSYOP and MISO Doctrine | 3 | [@ageint288]; [@ageint289]; [@ageint293] |
| 18.1 | PSYOP and MISO Doctrine - Joint PSYOP Doctrine: JP 3-53 (1996 and 2003) | 2 | [@ageint083]; [@ageint084] |
| 18.2 | PSYOP and MISO Doctrine - Military Information Support Operations (MISO): JP 3-13.2 | 1 | [@ageint085] |
| 18.3 | PSYOP and MISO Doctrine - Tactical PSYOP TTP: FM 3-05.302 | 1 | [@ageint086] |
| 18.4 | PSYOP and MISO Doctrine - FM 3-05.301: PSYOP Process Tactics and Techniques | 1 | [@ageint087] |
| 18.5 | PSYOP and MISO Doctrine - Target Audience Analysis (TAA) and Susceptibility Mapping | 2 | [@ageint302]; [@ageint297] |
| 18.6 | PSYOP and MISO Doctrine - PSYOP in Full-Spectrum Operations: Themes and Objectives | 1 | [@ageint086] |
| 18.7 | PSYOP and MISO Doctrine - Leaflets, Loudspeakers, and Digital Media: Product Development and Dissemination | 2 | [@ageint308]; [@ageint311] |
| 19.99 | Active Measures and Disinformation - V2 source-lane extension: bind Active Measures and Disinformation to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint238]; [@ageint239]; [@ageint240] |
| 19.101 | Active Measures and Disinformation - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Active Measures and Disinformation | 3 | [@ageint278]; [@ageint279]; [@ageint283] |
| 19.102 | Active Measures and Disinformation - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Active Measures and Disinformation | 3 | [@ageint290]; [@ageint291]; [@ageint294] |
| 19.1 | Active Measures and Disinformation - Soviet Active Measures: Definitions and Doctrine | 2 | [@ageint088]; [@ageint089] |
| 19.2 | Active Measures and Disinformation - Dezinformatsiya: Forgery, Front Organizations, Media Manipulation | 2 | [@ageint090]; [@ageint091] |
| 19.3 | Active Measures and Disinformation - KGB Aktivnyye Meropriyatiya: Historical Organization | 1 | [@ageint089] |
| 19.4 | Active Measures and Disinformation - Historical Active Measures Campaigns: INFEKTION, RYAN, DENVER | 1 | [@ageint091] |
| 19.5 | Active Measures and Disinformation - Russian Active Measures in the Contemporary Era | 1 | [@ageint092] |
| 19.6 | Active Measures and Disinformation - Chinese Information Operations: United Front Work Department | 2 | [@ageint308]; [@ageint311] |
| 19.7 | Active Measures and Disinformation - Deception, Disinformation, and Strategic Communications (NDU/Brown) | 2 | [@ageint093]; [@ageint094] |
| 19.8 | Active Measures and Disinformation - AI-Driven Active Measures: Synthetic Influence at Scale | 2 | [@ageint095]; [@ageint096] |
| 19.9 | Active Measures and Disinformation - Countermeasures: Disinformation Detection and Response | 1 | [@ageint092] |
| 20.99 | Social Engineering - V2 source-lane extension: bind Social Engineering to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint238]; [@ageint240]; [@ageint242] |
| 20.101 | Social Engineering - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Social Engineering | 3 | [@ageint280]; [@ageint281]; [@ageint282] |
| 20.102 | Social Engineering - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Social Engineering | 3 | [@ageint292]; [@ageint295]; [@ageint296] |
| 20.1 | Social Engineering - The Psychology of Influence: Cialdini's Seven Principles | 1 | [@ageint097] |
| 20.2 | Social Engineering - History of Social Engineering | 1 | [@ageint097] |
| 20.3 | Social Engineering - Social Engineering: The Science of Human Hacking (Hadnagy, 2018) | 1 | [@ageint098] |
| 20.4 | Social Engineering - The Art of Human Hacking (Hadnagy, 2010) | 1 | [@ageint099] |
| 20.5 | Social Engineering - Phishing, Vishing, Smishing, Deepfake Voice Attacks | 3 | [@ageint300]; [@ageint304]; [@ageint306] |
| 20.6 | Social Engineering - Physical Social Engineering: Access, Elicitation, Impersonation | 2 | [@ageint308]; [@ageint311] |
| 20.7 | Social Engineering - AI Automation of Social Engineering at Scale | 1 | [@ageint100] |
| 20.8 | Social Engineering - Defense: Training, Simulation, Technical Controls | 2 | [@ageint308]; [@ageint311] |
| 21.99 | Information Warfare and Cognitive Security - V2 source-lane extension: bind Information Warfare and Cognitive Security to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint238]; [@ageint239]; [@ageint244] |
| 21.101 | Information Warfare and Cognitive Security - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Information Warfare and Cognitive Security | 3 | [@ageint273]; [@ageint276]; [@ageint285] |
| 21.102 | Information Warfare and Cognitive Security - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Information Warfare and Cognitive Security | 3 | [@ageint286]; [@ageint290]; [@ageint294] |
| 21.1 | Information Warfare and Cognitive Security - Information Warfare Doctrine: Definitions, Theory, Air Force Policy | 2 | [@ageint101]; [@ageint102] |
| 21.2 | Information Warfare and Cognitive Security - Military Deception: Six Principles and Historical Effectiveness | 2 | [@ageint103]; [@ageint104] |
| 21.3 | Information Warfare and Cognitive Security - Automated Influence and the Cognitive Security Challenge | 1 | [@ageint105] |
| 21.4 | Information Warfare and Cognitive Security - Cognitive Security in the Age of AI: NATO/EU Paradigm Shift | 1 | [@ageint095] |
| 21.5 | Information Warfare and Cognitive Security - Epistemic Chaos as an Adversarial Goal | 2 | [@ageint095]; [@ageint096] |
| 21.6 | Information Warfare and Cognitive Security - Active Inference and Predictive Processing as Models for Cognitive Attack/Defense | 2 | [@ageint106]; [@ageint003] |
| 21.7 | Information Warfare and Cognitive Security - Behavioral Outcomes of Human Cognitive Security (arXiv 2026) | 1 | [@ageint107] |
| 22.99 | Counterintelligence Fundamentals - V2 source-lane extension: bind Counterintelligence Fundamentals to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint238]; [@ageint240]; [@ageint241] |
| 22.101 | Counterintelligence Fundamentals - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Counterintelligence Fundamentals | 3 | [@ageint274]; [@ageint278]; [@ageint280] |
| 22.102 | Counterintelligence Fundamentals - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Counterintelligence Fundamentals | 3 | [@ageint287]; [@ageint288]; [@ageint295] |
| 22.1 | Counterintelligence Fundamentals - CI Definition, Scope, Relationship to Intelligence | 1 | [@ageint012] |
| 22.2 | Counterintelligence Fundamentals - Offensive vs. Defensive Counterintelligence | 1 | [@ageint012] |
| 22.3 | Counterintelligence Fundamentals - Insider Threat Analysis: Critical Thinking Techniques (CDSE) | 1 | [@ageint108] |
| 22.4 | Counterintelligence Fundamentals - The Double-Agent and Triple-Cross Operations | 2 | [@ageint012]; [@ageint029] |
| 22.5 | Counterintelligence Fundamentals - Penetration of Hostile Services | 2 | [@ageint297]; [@ageint298] |
| 22.6 | Counterintelligence Fundamentals - Polygraph: Use and Limitations in CI | 2 | [@ageint297]; [@ageint298] |
| 22.7 | Counterintelligence Fundamentals - Damage Assessment and Control | 2 | [@ageint297]; [@ageint298] |
| 22.8 | Counterintelligence Fundamentals - Case Studies: Hanssen, Ames, Lee, Pollard | 2 | [@ageint297]; [@ageint298] |
| 23.99 | Counterintelligence Against Non-State Actors - V2 source-lane extension: bind Counterintelligence Against Non-State Actors to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint239]; [@ageint240]; [@ageint241] |
| 23.101 | Counterintelligence Against Non-State Actors - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Counterintelligence Against Non-State Actors | 3 | [@ageint279]; [@ageint282]; [@ageint284] |
| 23.102 | Counterintelligence Against Non-State Actors - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Counterintelligence Against Non-State Actors | 3 | [@ageint289]; [@ageint291]; [@ageint296] |
| 23.1 | Counterintelligence Against Non-State Actors - CI Against Terrorist and Criminal Intelligence Networks | 1 | [@ageint012] |
| 23.2 | Counterintelligence Against Non-State Actors - The Counterintelligence Threat from Non-State Actors | 1 | [@ageint033] |
| 23.3 | Counterintelligence Against Non-State Actors - CI in Hybrid Threat Environments | 1 | [@ageint109] |
| 23.4 | Counterintelligence Against Non-State Actors - Attribution Problems in Non-State CI Operations | 1 | [@ageint033] |
| 23.5 | Counterintelligence Against Non-State Actors - Corporate Counterintelligence and Trade Secret Protection | 3 | [@ageint307]; [@ageint305]; [@ageint304] |
| 24.99 | Gray Zone Warfare - V2 source-lane extension: bind Gray Zone Warfare to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint239]; [@ageint247]; [@ageint249] |
| 24.101 | Gray Zone Warfare - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Gray Zone Warfare | 3 | [@ageint275]; [@ageint276]; [@ageint283] |
| 24.102 | Gray Zone Warfare - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Gray Zone Warfare | 3 | [@ageint286]; [@ageint293]; [@ageint295] |
| 24.1 | Gray Zone Warfare - Defining the Gray Zone: Between Peace and War | 2 | [@ageint109]; [@ageint110] |
| 24.2 | Gray Zone Warfare - Gray Zone Tactics: Competition, Crisis, and Conflict | 1 | [@ageint111] |
| 24.3 | Gray Zone Warfare - Chinese Gray Zone: South China Sea and Taiwan Straits | 2 | [@ageint308]; [@ageint311] |
| 24.4 | Gray Zone Warfare - Russian Hybrid Warfare: Ukraine, Baltic States, Information Domain | 1 | [@ageint111] |
| 24.5 | Gray Zone Warfare - Anonymous No More: Countering Gray Zone Threats (MIPB 2025) | 1 | [@ageint111] |
| 24.6 | Gray Zone Warfare - Full Spectrum Conflict Design (IWI 2025) | 1 | [@ageint110] |
| 25.99 | Non-State Actor Intelligence - V2 source-lane extension: bind Non-State Actor Intelligence to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint238]; [@ageint247]; [@ageint249] |
| 25.101 | Non-State Actor Intelligence - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Non-State Actor Intelligence | 3 | [@ageint273]; [@ageint274]; [@ageint275] |
| 25.102 | Non-State Actor Intelligence - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Non-State Actor Intelligence | 3 | [@ageint286]; [@ageint287]; [@ageint292] |
| 25.1 | Non-State Actor Intelligence - Typology: Terrorist, Criminal, Commercial, Hacktivist, Proxy | 1 | [@ageint012] |
| 25.2 | Non-State Actor Intelligence - Hezbollah, ISIS, MS-13: Intelligence Structures and Capabilities | 2 | [@ageint308]; [@ageint311] |
| 25.3 | Non-State Actor Intelligence - Private Military Corporations as Intelligence Actors | 2 | [@ageint308]; [@ageint311] |
| 25.4 | Non-State Actor Intelligence - Counterintelligence Threat from Non-State Actors | 1 | [@ageint033] |
| 25.5 | Non-State Actor Intelligence - Non-State Actor Use of Commercial AI for Intelligence Collection | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| 26.99 | Irregular Warfare and Special Operations - V2 source-lane extension: bind Irregular Warfare and Special Operations to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint239]; [@ageint249]; [@ageint266] |
| 26.101 | Irregular Warfare and Special Operations - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Irregular Warfare and Special Operations | 3 | [@ageint276]; [@ageint277]; [@ageint284] |
| 26.102 | Irregular Warfare and Special Operations - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Irregular Warfare and Special Operations | 3 | [@ageint288]; [@ageint289]; [@ageint293] |
| 26.1 | Irregular Warfare and Special Operations - SF Unconventional Warfare Doctrine: TC 18-01 | 1 | [@ageint112] |
| 26.2 | Irregular Warfare and Special Operations - FM 3-05.130: ARSOF Unconventional Warfare | 2 | [@ageint113]; [@ageint114] |
| 26.3 | Irregular Warfare and Special Operations - FM 3-05.102: ARSOF Intelligence | 2 | [@ageint115]; [@ageint116] |
| 26.4 | Irregular Warfare and Special Operations - OSS Origins and Training Manuals (1944) | 3 | [@ageint117]; [@ageint118]; [@ageint119] |
| 26.5 | Irregular Warfare and Special Operations - Principles of Tradecraft for Resistance Organizations | 1 | [@ageint120] |
| 26.6 | Irregular Warfare and Special Operations - Underground Intelligence Networks: Structure, Security, Continuity | 2 | [@ageint308]; [@ageint311] |
| 26.7 | Irregular Warfare and Special Operations - OSS Simple Sabotage Field Manual (1944) | 1 | [@ageint117] |
| 26.8 | Irregular Warfare and Special Operations - Morale Operations: OSS Psychological Warfare | 1 | [@ageint117] |
| 27.99 | Soviet and Russian Intelligence - V2 source-lane extension: bind Soviet and Russian Intelligence to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint266]; [@ageint267]; [@ageint269] |
| 27.101 | Soviet and Russian Intelligence - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Soviet and Russian Intelligence | 3 | [@ageint278]; [@ageint279]; [@ageint283] |
| 27.102 | Soviet and Russian Intelligence - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Soviet and Russian Intelligence | 3 | [@ageint290]; [@ageint291]; [@ageint294] |
| 27.1 | Soviet and Russian Intelligence - KGB Structure, Culture, and Doctrine: First Chief Directorate | 1 | [@ageint121] |
| 27.2 | Soviet and Russian Intelligence - The Lubyanka Files: 29 KGB Training Manuals, 1965–1989 | 1 | [@ageint122] |
| 27.2.1 | Soviet and Russian Intelligence - Working with Agents (Declassified Manual) | 1 | [@ageint032] |
| 27.2.2 | Soviet and Russian Intelligence - Working with Information in Intelligence (1970s) | 1 | [@ageint121] |
| 27.2.3 | Soviet and Russian Intelligence - Psychological Methods and Manipulation of Agents (1988) | 1 | [@ageint021] |
| 27.2.4 | Soviet and Russian Intelligence - Some Aspects of Training Agents Psychologically (1985) | 1 | [@ageint021] |
| 27.2.5 | Soviet and Russian Intelligence - Exposure of Disinformation in Intelligence Materials (1968) | 1 | [@ageint021] |
| 27.2.6 | Soviet and Russian Intelligence - Organizational Structure and Management of Intelligence Residency | 2 | [@ageint297]; [@ageint298] |
| 27.2.7 | Soviet and Russian Intelligence - On Organizing Work with Confidential Contacts | 1 | [@ageint122] |
| 27.2.8 | Soviet and Russian Intelligence - Tasks of a KGB Resident Abroad | 1 | [@ageint122] |
| 27.3 | Soviet and Russian Intelligence - KGB Alpha Team Training Manual | 1 | [@ageint123] |
| 27.4 | Soviet and Russian Intelligence - The Mitrokhin Archive: KGB Global Operations | 4 | [@ageint124]; [@ageint125]; [@ageint126]; [@ageint127] |
| 27.5 | Soviet and Russian Intelligence - GRU: Soviet Military Intelligence Structure | 2 | [@ageint297]; [@ageint298] |
| 27.6 | Soviet and Russian Intelligence - The Interpreter Magazine: KGB Manual Summaries | 1 | [@ageint022] |
| 28.99 | American Intelligence History - V2 source-lane extension: bind American Intelligence History to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint266]; [@ageint269]; [@ageint271] |
| 28.101 | American Intelligence History - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for American Intelligence History | 3 | [@ageint280]; [@ageint281]; [@ageint282] |
| 28.102 | American Intelligence History - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for American Intelligence History | 3 | [@ageint292]; [@ageint295]; [@ageint296] |
| 28.1 | American Intelligence History - OSS in World War II | 2 | [@ageint128]; [@ageint129] |
| 28.1.1 | American Intelligence History - OSS Secret Intelligence Manual | 1 | [@ageint117] |
| 28.1.2 | American Intelligence History - OSS Provisional Basic Field Manual | 1 | [@ageint119] |
| 28.1.3 | American Intelligence History - Special Operations Field Manual | 1 | [@ageint118] |
| 28.1.4 | American Intelligence History - OSS Special Weapons and Devices | 1 | [@ageint117] |
| 28.1.5 | American Intelligence History - Simple Sabotage Field Manual (1944) | 1 | [@ageint117] |
| 28.1.6 | American Intelligence History - Morale Operations Field Manual | 1 | [@ageint117] |
| 28.2 | American Intelligence History - CIA Cold War Operations | 2 | [@ageint297]; [@ageint298] |
| 28.2.1 | American Intelligence History - CIA Manual of Trickery and Deception (Mulholland) | 1 | [@ageint130] |
| 28.2.2 | American Intelligence History - Principles of Tradecraft (Resistance Operations) | 1 | [@ageint120] |
| 28.2.3 | American Intelligence History - Soviet Active Measures Documents (CREST Collection) | 4 | [@ageint088]; [@ageint089]; [@ageint090]; [@ageint091] |
| 28.3 | American Intelligence History - Studies in Intelligence: The CIA's Professional Journal | 3 | [@ageint131]; [@ageint132]; [@ageint133] |
| 28.3.1 | American Intelligence History - Vol. 70, No. 1 (March 2026): "Espionage in Our AI Future" (Mulligan/RAND) | 2 | [@ageint019]; [@ageint034] |
| 28.3.2 | American Intelligence History - Vol. 68, No. 2 (June 2024): OSINT in the IC | 1 | [@ageint047] |
| 28.4 | American Intelligence History - History of SIGINT at the CIA, 1947–1970 | 2 | [@ageint038]; [@ageint039] |
| 28.5 | American Intelligence History - NSA WWII Declassified: European Axis SIGINT (9 Volumes) | 1 | [@ageint036] |
| 29.99 | British and Allied Intelligence - V2 source-lane extension: bind British and Allied Intelligence to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint266]; [@ageint269]; [@ageint270] |
| 29.101 | British and Allied Intelligence - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for British and Allied Intelligence | 3 | [@ageint273]; [@ageint276]; [@ageint285] |
| 29.102 | British and Allied Intelligence - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for British and Allied Intelligence | 3 | [@ageint286]; [@ageint290]; [@ageint294] |
| 29.1 | British and Allied Intelligence - MI6/SIS: Structure and Cold War Tradecraft | 1 | [@ageint007] |
| 29.2 | British and Allied Intelligence - SOE: Special Operations Executive Training (WWII) | 1 | [@ageint134] |
| 29.3 | British and Allied Intelligence - GCHQ and the BRUSA/UKUSA Agreements | 2 | [@ageint011]; [@ageint135] |
| 29.4 | British and Allied Intelligence - Five Eyes Archive: Key Declassified Documents | 3 | [@ageint010]; [@ageint041]; [@ageint042] |
| 30.99 | Israeli and Continental Services - V2 source-lane extension: bind Israeli and Continental Services to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint266]; [@ageint267]; [@ageint271] |
| 30.101 | Israeli and Continental Services - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Israeli and Continental Services | 3 | [@ageint274]; [@ageint278]; [@ageint280] |
| 30.102 | Israeli and Continental Services - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Israeli and Continental Services | 3 | [@ageint287]; [@ageint288]; [@ageint295] |
| 30.1 | Israeli and Continental Services - Mossad: Structure, Culture, Notable Operations | 1 | [@ageint008] |
| 30.2 | Israeli and Continental Services - Eli Cohen: Deep Cover Agent in Syria | 1 | [@ageint136] |
| 30.3 | Israeli and Continental Services - Operation Wrath of God: PSYOP and Targeted Killing | 2 | [@ageint297]; [@ageint298] |
| 30.4 | Israeli and Continental Services - Unit 8200: SIGINT, AI, and Cyber Excellence | 2 | [@ageint297]; [@ageint298] |
| 30.5 | Israeli and Continental Services - SDECE/DGSE: French Intelligence Tradition | 2 | [@ageint297]; [@ageint298] |
| 30.6 | Israeli and Continental Services - BND: German Federal Intelligence Service | 2 | [@ageint297]; [@ageint298] |
| 30.7 | Israeli and Continental Services - Stasi: East German Pervasive Domestic Intelligence | 2 | [@ageint297]; [@ageint298] |
| 31.99 | Foundations of AGEINT - V2 source-lane extension: bind Foundations of AGEINT to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint232]; [@ageint235]; [@ageint247] |
| 31.100 | Foundations of AGEINT - V2 AGEINT-depth extension: add agent evaluation and public-sector adoption gates that bind agency authority, AI Office-style accountability, impact assessment, and human review before any classroom agent workflow is rehearsed | 3 | [@ageint232]; [@ageint235]; [@ageint247] |
| 31.101 | Foundations of AGEINT - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for Foundations of AGEINT | 3 | [@ageint279]; [@ageint282]; [@ageint284] |
| 31.102 | Foundations of AGEINT - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for Foundations of AGEINT | 3 | [@ageint289]; [@ageint291]; [@ageint296] |
| 31.1 | Foundations of AGEINT - Defining AGEINT: From AI Agents to Autonomous Intelligence Systems | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 31.2 | Foundations of AGEINT - From LLMs to Agents: The Cognitive Controller Stack | 1 | [@ageint137] |
| 31.3 | Foundations of AGEINT - Unified Taxonomy: Perception → Brain → Planning → Action → Collaboration | 1 | [@ageint137] |
| 31.3.1 | Foundations of AGEINT - Perception Modules: Multimodal Ingestion (Text, Vision, Audio, Sensor) | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 31.3.2 | Foundations of AGEINT - Brain/Reasoning: LLM as Cognitive Controller | 1 | [@ageint138] |
| 31.3.3 | Foundations of AGEINT - Memory: In-Context, External VectorDB, Episodic, Semantic, Procedural | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 31.3.4 | Foundations of AGEINT - Action: Tool Use, API Calls, Code Execution, Computer Use | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 31.3.5 | Foundations of AGEINT - Collaboration: A2A Messaging, Shared Context, Role Specialization | 1 | [@ageint139] |
| 31.4 | Foundations of AGEINT - The OECD Agentic AI Landscape and Conceptual Foundations (2026) | 1 | [@ageint140] |
| 31.5 | Foundations of AGEINT - MIT Sloan Explanation of Agentic AI | 1 | [@ageint141] |
| 31.6 | Foundations of AGEINT - AGEINT vs. Traditional OSINT vs. AI-Assisted Analysis: A Capability Matrix | 2 | [@ageint301]; [@ageint298] |
| 31.7 | Foundations of AGEINT - Dual-Paradigm Framework: Symbolic/Classical vs. Neural/Generative Agents | 1 | [@ageint142] |
| 31.8 | Foundations of AGEINT - The Return to HUMINT as Agentic AI Degrades Digital Trust | 2 | [@ageint004]; [@ageint005] |
| 32.99 | AGEINT Design Patterns and Archetypes - V2 source-lane extension: bind AGEINT Design Patterns and Archetypes to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint233]; [@ageint258]; [@ageint272] |
| 32.100 | AGEINT Design Patterns and Archetypes - V2 AGEINT-depth extension: transform every raw design motif into a safe registry entry, tabletop audit, provenance record, and interface contract rather than operational deployment | 3 | [@ageint233]; [@ageint258]; [@ageint272] |
| 32.101 | AGEINT Design Patterns and Archetypes - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for AGEINT Design Patterns and Archetypes | 3 | [@ageint275]; [@ageint276]; [@ageint283] |
| 32.102 | AGEINT Design Patterns and Archetypes - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for AGEINT Design Patterns and Archetypes | 3 | [@ageint286]; [@ageint293]; [@ageint295] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 1: The Solo Reasoner — Single-agent ReAct loop for focused intelligence tasks | 1 | [@ageint143] |
| module section | AGEINT Design Patterns and Archetypes - Methods: Chain-of-Thought, Self-Critique, Reflection Scoring | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| module section | AGEINT Design Patterns and Archetypes - Application: Single-source report analysis, indicator enrichment | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: LangChain LCEL ReAct agent with tool calling | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 2: The Reflection Agent — Self-evaluation after each action step | 1 | [@ageint139] |
| module section | AGEINT Design Patterns and Archetypes - Methods: Internal scoring, critic models, trajectory validation | 2 | [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Application: OSINT verification loop, analytic bias detection | 2 | [@ageint297]; [@ageint298] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: LangGraph state machine with reflexion node | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 3: The Tool-Forager — Agent with comprehensive external tool access | 1 | [@ageint144] |
| module section | AGEINT Design Patterns and Archetypes - Methods: Function calling, JSON schema execution, grounded output | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| module section | AGEINT Design Patterns and Archetypes - Application: Multi-source data harvesting, real-time collection | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: OpenAI function calling with Recon-ng, Shodan, STIX tools | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 4: The Planner-Executor — Long-horizon task decomposition | 2 | [@ageint139]; [@ageint145] |
| module section | AGEINT Design Patterns and Archetypes - Methods: Chain-of-thought with memory rehydration, execution DAGs | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Application: Multi-phase operation planning, collection management | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: LangGraph DAG flow with priority queues | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 5: The Parallel Collector — Concurrent multi-source collection | 1 | [@ageint144] |
| module section | AGEINT Design Patterns and Archetypes - Methods: Concurrent tool invocation, aggregation, deduplication | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Application: Simultaneous OSINT/SIGINT metadata collection | 2 | [@ageint301]; [@ageint298] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: CrewAI parallel task execution with consensus scoring | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 6: The Multi-Agent Crew — Specialized agents in collaborative formation | 2 | [@ageint139]; [@ageint146] |
| module section | AGEINT Design Patterns and Archetypes - Methods: Planner + Retriever + Executor + Validator + Reporter roles | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Application: All-source intelligence fusion; Red/Blue Cell simulation | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: CrewAI role-based crew with hierarchical process manager | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 7: The Debate Agent — Adversarial multi-agent reasoning | 1 | [@ageint147] |
| module section | AGEINT Design Patterns and Archetypes - Methods: Devil's Advocacy automation, competing hypotheses generation | 2 | [@ageint297]; [@ageint298] |
| module section | AGEINT Design Patterns and Archetypes - Application: Automated Analysis of Competing Hypotheses (ACH) | 2 | [@ageint297]; [@ageint298] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: AutoGen two-agent debate pattern with judge agent | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 8: The RAG-Operator — Retrieval-Augmented Generation over intelligence corpora | 1 | [@ageint148] |
| module section | AGEINT Design Patterns and Archetypes - Methods: Dense vector retrieval, hybrid BM25+dense, re-ranking | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Application: All-source fusion from live document collections | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: LangChain RAG with Chroma/Pinecone over STIX feeds | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 9: The Memory-State Machine — Persistent episodic memory agent | 1 | [@ageint138] |
| module section | AGEINT Design Patterns and Archetypes - Methods: Episodic memory write/read, consolidation, attention-weighted retrieval | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Application: Long-term asset tracking, longitudinal pattern-of-life analysis | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: LangGraph with PostgreSQL episodic memory and mem0/MemGPT | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 10: The Control Plane Agent — Modular tool routing through single interface | 1 | [@ageint145] |
| module section | AGEINT Design Patterns and Archetypes - Methods: "Control Plane as a Tool" abstraction, modular routing logic | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| module section | AGEINT Design Patterns and Archetypes - Application: Scalable multi-source collection with single interface | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: FastAPI meta-tool endpoint wrapping N sub-tools | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 11: The Surveillance Agent — Continuous monitoring and alerting | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Methods: Scheduled polling, anomaly detection, threshold alerting | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| module section | AGEINT Design Patterns and Archetypes - Application: Persistent target monitoring, dark web alerting, infrastructure tracking | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: n8n or LangGraph cron-triggered agent with Shodan/SpiderFoot APIs | 3 | [@ageint307]; [@ageint305]; [@ageint304] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 12: The Red Team Agent — Adversarial attack simulation | 1 | [@ageint147] |
| module section | AGEINT Design Patterns and Archetypes - Methods: Adversarial prompt generation, attack-tree traversal, kill chain simulation | 3 | [@ageint300]; [@ageint304]; [@ageint306] |
| module section | AGEINT Design Patterns and Archetypes - Application: Penetration testing automation, vulnerability discovery | 3 | [@ageint300]; [@ageint304]; [@ageint306] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: AutoGen code execution agent with MITRE ATT&CK tool plugin | 3 | [@ageint300]; [@ageint304]; [@ageint306] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 13: The Cover Story Generator — Legend and cover document creation | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Methods: Persona generation, document synthesis, consistency checking | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Application: NOC legend maintenance, sock puppet operational security | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: GPT-4o with structured output schemas for persona consistency | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 14: The Deception Detector — Verification and source reliability agent | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Methods: Cross-source triangulation, metadata analysis, deepfake detection API calls | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| module section | AGEINT Design Patterns and Archetypes - Application: Source vetting, product validation, disinformation identification | 2 | [@ageint308]; [@ageint311] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: LangChain agent with Hive Moderation, Sightengine, C2PA APIs | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 15: The Analyst in the Loop — Human-in-the-loop (HITL) intelligence agent | 1 | [@ageint004] |
| module section | AGEINT Design Patterns and Archetypes - Methods: Interrupt-and-query, confidence-gated human escalation | 2 | [@ageint297]; [@ageint298] |
| module section | AGEINT Design Patterns and Archetypes - Application: Supervised analysis; compliance-constrained environments | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: LangGraph with human_approval node and async interrupt handlers | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 16: The Cyber Sentinel — Autonomous threat intelligence and response | 2 | [@ageint149]; [@ageint150] |
| module section | AGEINT Design Patterns and Archetypes - Methods: SIEM integration, SOAR automation, ATT&CK technique mapping | 2 | [@ageint302]; [@ageint297] |
| module section | AGEINT Design Patterns and Archetypes - Application: Autonomous SOC tier-1 triage, IOC enrichment | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: CrewAI crew with Splunk/Elastic SIEM tools and STIX/TAXII writer | 3 | [@ageint309]; [@ageint310]; [@ageint300] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 17: The Supply Chain Inspector — Software provenance and integrity agent | 3 | [@ageint303]; [@ageint304]; [@ageint305] |
| module section | AGEINT Design Patterns and Archetypes - Methods: SBOM parsing, dependency graph analysis, commit diff analysis | 3 | [@ageint303]; [@ageint304]; [@ageint305] |
| module section | AGEINT Design Patterns and Archetypes - Application: Open-source supply chain threat hunting (post-XZ Utils) | 1 | [@ageint076] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: Python agent with Syft/Grype SBOM tools and GitHub commit analysis | 3 | [@ageint303]; [@ageint304]; [@ageint305] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 18: The GEOINT Analyst — Automated satellite imagery analysis | 2 | [@ageint302]; [@ageint297] |
| module section | AGEINT Design Patterns and Archetypes - Methods: Vision model object detection, change detection, chronolocation | 2 | [@ageint302]; [@ageint297] |
| module section | AGEINT Design Patterns and Archetypes - Application: Facility monitoring, order-of-battle assessment | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: GPT-4o Vision + Google Earth Engine API + LangChain agent loop | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 19: The Cognitive Inoculant — Prebunking and cognitive resilience agent | 1 | [@ageint151] |
| module section | AGEINT Design Patterns and Archetypes - Methods: Manipulation technique detection, inoculation content generation, user adaptation | 2 | [@ageint308]; [@ageint311] |
| module section | AGEINT Design Patterns and Archetypes - Application: Population-scale cognitive security intervention delivery | 1 | [@ageint152] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: LangChain agent with CAMBREX taxonomy + API delivery pipeline | 3 | [@ageint305]; [@ageint304]; [@ageint303] |
| module section | AGEINT Design Patterns and Archetypes - Pattern 20: The Hierarchical Command — Orchestrator-subagent architecture | 2 | [@ageint139]; [@ageint137] |
| module section | AGEINT Design Patterns and Archetypes - Methods: Goal decomposition, subagent delegation, output aggregation, failure recovery | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Application: Complex multi-domain operations with role separation | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| module section | AGEINT Design Patterns and Archetypes - Code Archetype: LangGraph supervisor pattern with specialized subagent nodes | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 33.99 | AGEINT Frameworks and Infrastructure - V2 source-lane extension: bind AGEINT Frameworks and Infrastructure to source-lane evidence, claim-ledger review, safe substitution, compliance/rights mapping, instructor deliverables, and explicit refresh triggers | 3 | [@ageint255]; [@ageint256]; [@ageint258] |
| 33.100 | AGEINT Frameworks and Infrastructure - V2 AGEINT-depth extension: map frameworks to interoperable tool descriptions, Web of Things affordances, OpenAPI contracts, credential semantics, revocation, and error-handling evidence | 3 | [@ageint255]; [@ageint256]; [@ageint258] |
| 33.101 | AGEINT Frameworks and Infrastructure - Deep expansion: add accessibility/UDL review, procurement/vendor oversight, HRIA/DPIA worksheet, data-lineage registry, assessment-integrity protocol, agent incident drill, role-based competency map, and adversarial assurance cycle for AGEINT Frameworks and Infrastructure | 3 | [@ageint273]; [@ageint274]; [@ageint275] |
| 33.102 | AGEINT Frameworks and Infrastructure - Evidence-package expansion: add model/dataset documentation cards, transparency notice, records-retention audit trail, release/change-control gate, risk-exception memo, learner support plan, instructor question bank, and remediation backlog for AGEINT Frameworks and Infrastructure | 3 | [@ageint286]; [@ageint287]; [@ageint292] |
| 33.1 | AGEINT Frameworks and Infrastructure - LangChain/LangGraph: State Machine Orchestration | 2 | [@ageint147]; [@ageint153] |
| 33.1.1 | AGEINT Frameworks and Infrastructure - LCEL: LangChain Expression Language | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 33.1.2 | AGEINT Frameworks and Infrastructure - LangGraph: Stateful, Cyclical Agentic Workflows | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 33.1.3 | AGEINT Frameworks and Infrastructure - LangSmith: Observability and Tracing | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 33.2 | AGEINT Frameworks and Infrastructure - CrewAI: Role-Based Multi-Agent Collaboration | 2 | [@ageint154]; [@ageint153] |
| 33.2.1 | AGEINT Frameworks and Infrastructure - Crew, Agent, Task, and Process Objects | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 33.2.2 | AGEINT Frameworks and Infrastructure - Sequential, Parallel, and Hierarchical Process Modes | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 33.2.3 | AGEINT Frameworks and Infrastructure - Built-in Tool Ecosystem | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 33.3 | AGEINT Frameworks and Infrastructure - AutoGen (Microsoft): Multi-Agent Conversation Patterns | 2 | [@ageint147]; [@ageint153] |
| 33.3.1 | AGEINT Frameworks and Infrastructure - AssistantAgent and UserProxyAgent Pattern | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 33.3.2 | AGEINT Frameworks and Infrastructure - GroupChat with RoundRobin and AutoSelect Managers | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 33.3.3 | AGEINT Frameworks and Infrastructure - Code Execution Risk and Sandboxing Requirements | 1 | [@ageint147] |
| 33.4 | AGEINT Frameworks and Infrastructure - Semantic Kernel: Enterprise AI Orchestration | 1 | [@ageint147] |
| 33.5 | AGEINT Frameworks and Infrastructure - AWS Agentic Patterns: Production Architecture Guide | 1 | [@ageint144] |
| 33.5.1 | AGEINT Frameworks and Infrastructure - Basic Reasoning Agents | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 33.5.2 | AGEINT Frameworks and Infrastructure - Tool-Based Agents (Function Calling and MCP Servers) | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 33.5.3 | AGEINT Frameworks and Infrastructure - Computer-Use Agents | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 33.5.4 | AGEINT Frameworks and Infrastructure - Coding Agents | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 33.5.5 | AGEINT Frameworks and Infrastructure - Speech-to-Speech Agents | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 33.5.6 | AGEINT Frameworks and Infrastructure - Orchestration Patterns: Supervisor, Parallel, Subgraph | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 33.6 | AGEINT Frameworks and Infrastructure - Model Context Protocol (MCP): The USB Standard for Agentic AI | 4 | [@ageint155]; [@ageint156]; [@ageint157]; [@ageint158] |
| 33.6.1 | AGEINT Frameworks and Infrastructure - MCP Architecture: Client, Server, Host | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 33.6.2 | AGEINT Frameworks and Infrastructure - NSA Security Design Considerations for MCP | 1 | [@ageint155] |
| 33.6.3 | AGEINT Frameworks and Infrastructure - MCP Security Risks: Tool Poisoning, Prompt Injection via Server | 1 | [@ageint159] |
| 33.6.4 | AGEINT Frameworks and Infrastructure - MCP in Intelligence Workflows: Structured Tool Registration | 3 | [@ageint299]; [@ageint306]; [@ageint312] |
| 33.7 | AGEINT Frameworks and Infrastructure - Agent-to-Agent (A2A) Protocols: Interoperability Between Frameworks | 1 | [@ageint137] |
| 33.8 | AGEINT Frameworks and Infrastructure - n8n and Make.com: No-Code/Low-Code Agentic Intelligence Pipelines | 1 | [@ageint153] |
