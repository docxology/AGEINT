## Cyber-Physical Readiness Lens path for Industrial Control Systems (ICS) and Operational Technology: lesson cluster, safe artifact, and review

**Navigation.** Parent section: [@sec:chapter-industrial-control-systems-ics-and-operational-technology].

### Industrial Control Systems (ICS) and Operational Technology practice studio: topic lessons, safe worked example, and knowledge check

**Navigation.** Parent section: [@sec:chapter-industrial-control-systems-ics-and-operational-technology].

### Industrial Control Systems (ICS) and Operational Technology topic lessons: source-backed concepts and transfer tasks

**Industrial Control Systems (ICS) and Operational Technology** builds ICS/OT intelligence as safety-aware defensive reasoning: asset state, engineering consequence, operator decision, and recovery evidence matter as much as cyber indicators. The sequence opens with **ICS Architecture: SCADA, DCS, PLC, HMI — Definitions and Roles**, **SCADA: Supervisory Control and Data Acquisition — Large Geographic Systems**, **DCS: Distributed Control Systems — Chemical, Refining, Power** and applies the **Cyber-Physical Readiness Lens** practice frame through concept, evidence, artifact, misconception, and transfer tasks.

**Learning-path links.** Unit module map [@fig:part-industrial-and-cyber-physical-intelligence-module-map]; module overview [@sec:chapter-industrial-control-systems-ics-and-operational-technology]; curriculum atlas [@sec:curriculum_orientation].

**Contextual source routes.** For module 45's topic-lessons section, the **ICS/OT Cyber-Physical Defense and Tabletop Readiness** catalog routes include [@official_nist_csf_2]; [@official_nist_sp_800_160r1]; [@official_nist_sp_800_82r3]; [@official_isa_iec_62443]. Check the actual passage, edition, claim scope and access limitations before use. Route membership does not establish relevance, independent corroboration or efficacy.

#### Lesson 1: ICS Architecture: SCADA, DCS, PLC, HMI — Definitions and Roles

**Concept.** **ICS Architecture: SCADA, DCS, PLC, HMI — Definitions and Roles** maps industrial assets, safety interlocks, operator roles, and consequence before any cyber-physical inference.

**Worked reasoning and limits.** ICS describes systems that monitor or control industrial processes; a PLC performs local control, an HMI presents state to a human, and a historian stores observations rather than independently verifying physical truth [@ageint208]. A safety instrumented system provides a protective function distinct from ordinary process control; an architectural claim of independence requires evidence about shared dependencies, not just a separate box. In a wholly fictional, non-executable tank diagram, sensor S reports 40 units to controller C, HMI H displays 40, and historian R records 40: these are three representations of one measurement, not three independent confirmations. A second paper observation of 65 creates an unresolved discrepancy; the asset/consequence row is 'S→C→H/R; visibility disputed; control state unknown; physical harm unestablished', and the analyst records possible sensor, timing, or transcription error, withholds a physical-state conclusion, and sends the question to the designated process-safety reviewer without connecting to or controlling anything. Apply the claim-record procedure in Section [@sec:analytic-workflow] to this evidence boundary.

**Why it matters.** **ICS Architecture: SCADA, DCS, PLC, HMI — Definitions and Roles** matters in the **ICS/OT Cyber-Physical Defense and Tabletop Readiness** lane because safety-aware tabletop readiness and defensive coverage evidence must stay separate from judgment; IT-first assumptions is a common failure.

**Source support.** Inherited source-guide context for **ICS Architecture: SCADA, DCS, PLC, HMI — Definitions and Roles**: [@ageint208] and [@ageint209]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_nist_csf_2]; [@official_nist_sp_800_160r1].

**Evidence to inspect.** For **ICS Architecture: SCADA, DCS, PLC, HMI — Definitions and Roles**, inspect the original passages. Curriculum annotation for [@ageint208]: This article provides a comprehensive overview of cybersecurity for Industrial Control Systems, covering SCADA, distributed control systems, and programmable logic controllers as they have evolved from isolated architectures to networked, cloud-connected deployments. Curriculum annotation for [@ageint209]: A glossary entry from the cybersecurity company Bitsight explaining Industrial Control Systems (ICS), defined as integrated hardware and software used to control, monitor, and automate industrial processes across manufacturing, energy, and critical infrastructure. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **ICS Architecture**, build a **tabletop packet with OT asset inventory, architecture record, consequences, injects, and debrief rubric** for this safety-aware tabletop readiness and defensive coverage review topic. The artifact must name the source descriptor, the bounded claim about **ICS Architecture**, the caveat that limits it, the uncertainty note, the out-of-scope-use boundary, and the reviewer accountable for challenge. Shape **ICS Architecture: SCADA, DCS, PLC, HMI — Definitions and Roles** work as a **cyber-physical tabletop evidence packet** that states the evidence used, what stays uncertain, who reviews it, and when to stop.

**Misconception check.** Correct the misconception that ICS Architecture: SCADA, DCS, PLC, HMI — Definitions and Roles establishes intent without reviewing alternative explanations.

**Transfer task.** Transfer **ICS Architecture: SCADA, DCS, PLC, HMI — Definitions and Roles** to a second module by preserving safety-aware tabletop readiness and defensive coverage review, changing the source evidence, and naming a new reviewer.

#### Lesson 2: SCADA: Supervisory Control and Data Acquisition — Large Geographic Systems

**Concept.** **SCADA: Supervisory Control and Data Acquisition — Large Geographic Systems** maps industrial assets, safety interlocks, operator roles, and consequence before any cyber-physical inference.

**Worked reasoning and limits.** SCADA combines supervisory oversight and data acquisition, often across geographically dispersed assets; it is not synonymous with every industrial controller [@ageint209]. A supervisory display can be stale while local control continues, so loss of visibility and loss of control require separate evidence. Ask which timestamp belongs to the measurement, transport, and display before inferring a process interruption.

**Why it matters.** Without explicit treatment of **SCADA: Supervisory Control and Data Acquisition — Large Geographic Systems**, IT-first assumptions undermines safety-aware tabletop readiness and defensive coverage review; the lesson builds the habit to separate cyber analysis from unsafe process control or live operational action.

**Source support.** Inherited source-guide context for **SCADA: Supervisory Control and Data Acquisition — Large Geographic Systems**: [@ageint209]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_nist_csf_2]; [@official_nist_sp_800_160r1].

**Evidence to inspect.** For **SCADA: Supervisory Control and Data Acquisition — Large Geographic Systems**, inspect the original passages. Curriculum annotation for [@ageint209]: A glossary entry from the cybersecurity company Bitsight explaining Industrial Control Systems (ICS), defined as integrated hardware and software used to control, monitor, and automate industrial processes across manufacturing, energy, and critical infrastructure. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **SCADA**, build a **tabletop packet with OT asset inventory, architecture record, consequences, injects, and debrief rubric** for this safety-aware tabletop readiness and defensive coverage review topic. The artifact must name the source descriptor, the bounded claim about **SCADA**, the caveat that limits it, the uncertainty note, the out-of-scope-use boundary, and the reviewer accountable for challenge. Shape **SCADA: Supervisory Control and Data Acquisition — Large Geographic Systems** work as a **cyber-physical tabletop evidence packet** that states the evidence used, what stays uncertain, who reviews it, and when to stop.

**Misconception check.** Correct the misconception that SCADA: Supervisory Control and Data Acquisition — Large Geographic Systems replaces human review whenever evidence looks plausible.

**Transfer task.** Transfer **SCADA: Supervisory Control and Data Acquisition — Large Geographic Systems** to a second module by preserving safety-aware tabletop readiness and defensive coverage review, changing the source evidence, and naming a new reviewer.

#### Lesson 3: DCS: Distributed Control Systems — Chemical, Refining, Power

**Concept.** **DCS: Distributed Control Systems — Chemical, Refining, Power** maps industrial assets, safety interlocks, operator roles, and consequence before any cyber-physical inference.

**Worked reasoning and limits.** A DCS distributes control functions among coordinated components, commonly within a plant; distribution is an architectural property, not a guarantee of independent failure domains [@ageint209]. Several controllers can share power, engineering tools, or configuration dependencies. A paper architecture comparison therefore marks common dependencies rather than counting controllers as redundant protection.

**Why it matters.** **DCS: Distributed Control Systems — Chemical, Refining, Power** matters in the **ICS/OT Cyber-Physical Defense and Tabletop Readiness** lane because safety-aware tabletop readiness and defensive coverage evidence must stay separate from judgment; IT-first assumptions is a common failure.

**Source support.** Inherited source-guide context for **DCS: Distributed Control Systems — Chemical, Refining, Power**: [@ageint209]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_nist_csf_2]; [@official_nist_sp_800_160r1].

**Evidence to inspect.** For **DCS: Distributed Control Systems — Chemical, Refining, Power**, inspect the original passages. Curriculum annotation for [@ageint209]: A glossary entry from the cybersecurity company Bitsight explaining Industrial Control Systems (ICS), defined as integrated hardware and software used to control, monitor, and automate industrial processes across manufacturing, energy, and critical infrastructure. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **DCS**, build a **tabletop packet with OT asset inventory, architecture record, consequences, injects, and debrief rubric** for this safety-aware tabletop readiness and defensive coverage review topic. The artifact must name the source descriptor, the bounded claim about **DCS**, the caveat that limits it, the uncertainty note, the out-of-scope-use boundary, and the reviewer accountable for challenge. Shape **DCS: Distributed Control Systems — Chemical, Refining, Power** work as a **cyber-physical tabletop evidence packet** that states the evidence used, what stays uncertain, who reviews it, and when to stop.

**Misconception check.** Correct the misconception that DCS: Distributed Control Systems — Chemical, Refining, Power can be used while ignoring the rule to separate cyber analysis from unsafe process control or live operational action.

**Transfer task.** Transfer **DCS: Distributed Control Systems — Chemical, Refining, Power** to a second module by preserving safety-aware tabletop readiness and defensive coverage review, changing the source evidence, and naming a new reviewer.

#### Lesson 4: PLC: Programmable Logic Controllers — Field-Level Execution

**Concept.** **PLC: Programmable Logic Controllers — Field-Level Execution** maps industrial assets, safety interlocks, operator roles, and consequence before any cyber-physical inference.

**Worked reasoning and limits.** A PLC processes inputs and executes configured control logic to produce outputs; a log of a requested change does not establish that an output changed or that the physical process followed it [@ageint209]. Distinguish requested, acknowledged, executed, and independently observed states. Classroom records remain inert text: no controller code, device commands, or executable process model is required.

**Why it matters.** **PLC: Programmable Logic Controllers — Field-Level Execution** matters in the **ICS/OT Cyber-Physical Defense and Tabletop Readiness** lane because safety-aware tabletop readiness and defensive coverage evidence must stay separate from judgment; IT-first assumptions is a common failure.

**Source support.** Inherited source-guide context for **PLC: Programmable Logic Controllers — Field-Level Execution**: [@ageint209]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_nist_csf_2]; [@official_nist_sp_800_160r1].

**Evidence to inspect.** For **PLC: Programmable Logic Controllers — Field-Level Execution**, inspect the original passages. Curriculum annotation for [@ageint209]: A glossary entry from the cybersecurity company Bitsight explaining Industrial Control Systems (ICS), defined as integrated hardware and software used to control, monitor, and automate industrial processes across manufacturing, energy, and critical infrastructure. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **PLC**, build a **tabletop packet with OT asset inventory, architecture record, consequences, injects, and debrief rubric** for this safety-aware tabletop readiness and defensive coverage review topic. The artifact must name the source descriptor, the bounded claim about **PLC**, the caveat that limits it, the uncertainty note, the out-of-scope-use boundary, and the reviewer accountable for challenge. Shape **PLC: Programmable Logic Controllers — Field-Level Execution** work as a **cyber-physical tabletop evidence packet** that records its evidence, the residual uncertainty, the named reviewer, and the stop condition.

**Misconception check.** Correct the misconception that PLC: Programmable Logic Controllers — Field-Level Execution is optional whenever separate cyber analysis from unsafe process control or live operational action feels inconvenient.

**Transfer task.** Transfer **PLC: Programmable Logic Controllers — Field-Level Execution** to a second module by preserving safety-aware tabletop readiness and defensive coverage review, changing the source evidence, and naming a new reviewer.

#### Lesson 5: OT and IT: Process-dependent Safety, Availability, and Information Constraints

**Concept.** **OT and IT: Process-dependent Safety, Availability, and Information Constraints** is taught in the **ICS/OT Cyber-Physical Defense and Tabletop Readiness** lane. The analytic distinction is to separate cyber analysis from unsafe process control or live operational action. Apply it to the supplied evidence; a topic label alone establishes neither a mechanism nor a conclusion.

**Worked reasoning and limits.** OT supports interaction with physical processes, whereas IT emphasizes information processing; the categories overlap, and neither has one universal security-priority ordering [@ageint210]. Safety, availability, integrity, confidentiality, latency, and recovery constraints depend on the process and its hazards. A familiar IT action such as interruption or rapid software change is not automatically safe for OT; analysts identify the constraint and defer any operational decision to authorized engineering and safety personnel.

**Why it matters.** Analysts use **OT and IT: Process-dependent Safety, Availability, and Information Constraints** to separate cyber analysis from unsafe process control or live operational action. A defensible treatment names the judgment it enables for safety-aware tabletop readiness and defensive coverage review, the proof limit that IT-first assumptions would otherwise hide, and the reviewer accountable for challenge.

**Source support.** Inherited source-guide context for **OT and IT: Process-dependent Safety, Availability, and Information Constraints**: [@ageint209] and [@ageint210]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_nist_csf_2]; [@official_nist_sp_800_160r1].

**Evidence to inspect.** For **OT and IT: Process-dependent Safety, Availability, and Information Constraints**, inspect the original passages. Curriculum annotation for [@ageint209]: A glossary entry from the cybersecurity company Bitsight explaining Industrial Control Systems (ICS), defined as integrated hardware and software used to control, monitor, and automate industrial processes across manufacturing, energy, and critical infrastructure. Curriculum annotation for [@ageint210]: A Palo Alto Networks Cyberpedia article explaining the relationship among operational technology (OT), industrial control system (ICS), and SCADA security. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **OT and IT**, build a **tabletop packet with OT asset inventory, architecture record, consequences, injects, and debrief rubric** for this safety-aware tabletop readiness and defensive coverage review topic. The artifact must name the source descriptor, the bounded claim about **OT and IT**, the caveat that limits it, the uncertainty note, the out-of-scope-use boundary, and the reviewer accountable for challenge. Shape **OT and IT: Process-dependent Safety, Availability, and Information Constraints** work as a **cyber-physical tabletop evidence packet** that logs the evidence, the uncertainty, the responsible reviewer, and the halt condition.

**Misconception check.** Correct the misconception that OT and IT: Process-dependent Safety, Availability, and Information Constraints establishes intent without reviewing alternative explanations.

**Transfer task.** Transfer **OT and IT: Process-dependent Safety, Availability, and Information Constraints** to a second module by preserving safety-aware tabletop readiness and defensive coverage review, changing the source evidence, and naming a new reviewer.

#### Lesson 6: Air-gap Claims and Changing Connectivity Assumptions

**Concept.** **Air-gap Claims and Changing Connectivity Assumptions** is taught in the **ICS/OT Cyber-Physical Defense and Tabletop Readiness** lane. The analytic distinction is to separate cyber analysis from unsafe process control or live operational action. Apply it to the supplied evidence; a topic label alone establishes neither a mechanism nor a conclusion.

**Worked reasoning and limits.** An air-gap claim concerns specified connectivity at a specified time; it does not establish the absence of removable-media, maintenance, supply-chain, or human transfer paths. Conversely, a digital-transformation label does not prove that any particular connection exists. In an offline architecture exercise, annotate documented paths and unknown paths separately; do not discover them by scanning or live connection.

**Why it matters.** **Air-gap Claims and Changing Connectivity Assumptions** connects classroom vocabulary to ICS/OT Cyber-Physical Defense and Tabletop Readiness practice: learners document evidence, caveats, and reviewer ownership rather than repeating labels.

**Source support.** Inherited source-guide context for **Air-gap Claims and Changing Connectivity Assumptions**: [@ageint209]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_nist_csf_2]; [@official_nist_sp_800_160r1].

**Evidence to inspect.** For **Air-gap Claims and Changing Connectivity Assumptions**, inspect the original passages. Curriculum annotation for [@ageint209]: A glossary entry from the cybersecurity company Bitsight explaining Industrial Control Systems (ICS), defined as integrated hardware and software used to control, monitor, and automate industrial processes across manufacturing, energy, and critical infrastructure. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **Air-gap Claims**, build a **tabletop packet with OT asset inventory, architecture record, consequences, injects, and debrief rubric** for this safety-aware tabletop readiness and defensive coverage review topic. The artifact must name the source descriptor, the bounded claim about **Air-gap Claims and Changing Connectivity**, the caveat that limits it, the uncertainty note, the out-of-scope-use boundary, and the reviewer accountable for challenge. Shape **Air-gap Claims and Changing Connectivity Assumptions** work as a **cyber-physical tabletop evidence packet** that logs the evidence, the uncertainty, the responsible reviewer, and the halt condition.

**Misconception check.** Correct the misconception that Air-gap Claims and Changing Connectivity Assumptions replaces human review whenever evidence looks plausible.

**Transfer task.** Transfer **Air-gap Claims and Changing Connectivity Assumptions** to a second module by preserving safety-aware tabletop readiness and defensive coverage review, changing the source evidence, and naming a new reviewer.

#### Lesson 7: Securing ICS: Components, Protocols, Performance, Vulnerability

**Concept.** **Securing ICS: Components, Protocols, Performance, Vulnerability** treats the vulnerability record as an assurance case: severity, affected component, provenance, mitigation status, and uncertainty stay separate.

**Worked reasoning and limits.** The cited review discusses components, protocols, design constraints, and defensive approaches; it is not a site-specific safety assessment or proof that a proposed machine-learning control works [@ageint208]. A vulnerability listing identifies a possible software condition, while a process consequence additionally requires exposure, configuration, dependencies, and physical context. Record those missing links instead of multiplying a generic severity score into a physical-loss prediction.

**Why it matters.** **Securing ICS: Components, Protocols, Performance, Vulnerability** connects classroom vocabulary to ICS/OT Cyber-Physical Defense and Tabletop Readiness practice: learners document evidence, caveats, and reviewer ownership rather than repeating labels.

**Source support.** Inherited source-guide context for **Securing ICS: Components, Protocols, Performance, Vulnerability**: [@ageint208]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_nist_csf_2]; [@official_nist_sp_800_160r1].

**Evidence to inspect.** For **Securing ICS: Components, Protocols, Performance, Vulnerability**, inspect the original passages. Curriculum annotation for [@ageint208]: This article provides a comprehensive overview of cybersecurity for Industrial Control Systems, covering SCADA, distributed control systems, and programmable logic controllers as they have evolved from isolated architectures to networked, cloud-connected deployments. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **Securing ICS**, build a **tabletop packet with OT asset inventory, architecture record, consequences, injects, and debrief rubric** for this safety-aware tabletop readiness and defensive coverage review topic. The artifact must name the source descriptor, the bounded claim about **Securing ICS**, the caveat that limits it, the uncertainty note, the out-of-scope-use boundary, and the reviewer accountable for challenge. Shape **Securing ICS: Components, Protocols, Performance, Vulnerability** work as a **cyber-physical tabletop evidence packet** that names evidence, uncertainty, reviewer, and stop condition.

**Misconception check.** Correct the misconception that Securing ICS: Components, Protocols, Performance, Vulnerability can be used while ignoring the rule to separate cyber analysis from unsafe process control or live operational action.

**Transfer task.** Transfer **Securing ICS: Components, Protocols, Performance, Vulnerability** to a second module by preserving safety-aware tabletop readiness and defensive coverage review, changing the source evidence, and naming a new reviewer.

#### Lesson 8: 2026 Cybersecurity Guide to ICS (Claroty)

**Concept.** **2026 Cybersecurity Guide to ICS (Claroty)** is taught in the **ICS/OT Cyber-Physical Defense and Tabletop Readiness** lane. The analytic distinction is to separate cyber analysis from unsafe process control or live operational action. Apply it to the supplied evidence; a topic label alone establishes neither a mechanism nor a conclusion.

**Worked reasoning and limits.** Treat a vendor guide as an attributed account of recommended capabilities, not an independent comparative evaluation [@ageint211]. Asset inventory, segmentation, and monitoring describe different control functions: knowing an asset exists neither blocks access nor proves detection. A defensible comparison identifies what each capability would observe or constrain and leaves effectiveness unknown without applicable evaluation evidence.

**Why it matters.** **2026 Cybersecurity Guide** matters in the **ICS/OT Cyber-Physical Defense and Tabletop Readiness** lane because safety-aware tabletop readiness and defensive coverage evidence must stay separate from judgment; IT-first assumptions is a common failure.

**Source support.** Inherited source-guide context for **2026 Cybersecurity Guide to ICS (Claroty)**: [@ageint211]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_nist_csf_2]; [@official_nist_sp_800_160r1].

**Evidence to inspect.** For **2026 Cybersecurity Guide**, inspect the original passages. Curriculum annotation for [@ageint211]: A Claroty guide to securing industrial control systems (ICS) amid IT and operational technology convergence. It identifies challenges including an expanded attack surface, legacy systems lacking modern protections, third-party access gaps, patching delays due to uptime requirements, and advanced adversaries targeting ICS. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **2026 Cybersecurity Guide**, build a **tabletop packet with OT asset inventory, architecture record, consequences, injects, and debrief rubric** for this safety-aware tabletop readiness and defensive coverage review topic. The artifact must name the source descriptor, the bounded claim about **Cybersecurity Guide to ICS**, the caveat that limits it, the uncertainty note, the out-of-scope-use boundary, and the reviewer accountable for challenge. Shape **2026 Cybersecurity Guide** work as a **cyber-physical tabletop evidence packet** that names evidence, uncertainty, reviewer, and stop condition.

**Misconception check.** Correct the misconception that 2026 Cybersecurity Guide to ICS (Claroty) is optional whenever separate cyber analysis from unsafe process control or live operational action feels inconvenient.

**Transfer task.** Transfer **2026 Cybersecurity Guide** to a second module by preserving safety-aware tabletop readiness and defensive coverage review, changing the source evidence, and naming a new reviewer.

#### Lesson 9: OT vs. ICS vs. SCADA Security (Palo Alto Networks)

**Concept.** **OT vs. ICS vs. SCADA Security (Palo Alto Networks)** maps industrial assets, safety interlocks, operator roles, and consequence before any cyber-physical inference.

**Worked reasoning and limits.** The cited vendor taxonomy places SCADA within ICS and ICS within the broader OT category [@ageint210]. This is a useful organizing model, not a rule that every real installation has cleanly separated layers. Classify a fictional component by function and dependencies rather than by its product name or vendor category.

**Why it matters.** **OT vs. ICS vs. SCADA Security (Palo Alto Networks)** connects classroom vocabulary to ICS/OT Cyber-Physical Defense and Tabletop Readiness practice: learners document evidence, caveats, and reviewer ownership rather than repeating labels.

**Source support.** Inherited source-guide context for **OT vs. ICS vs. SCADA Security (Palo Alto Networks)**: [@ageint210]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_nist_csf_2]; [@official_nist_sp_800_160r1].

**Evidence to inspect.** For **OT vs. ICS vs. SCADA Security (Palo Alto Networks)**, inspect the original passages. Curriculum annotation for [@ageint210]: A Palo Alto Networks Cyberpedia article explaining the relationship among operational technology (OT), industrial control system (ICS), and SCADA security. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **OT vs. ICS vs. SCADA Security (Palo Alto Networks)**, build a **tabletop packet with OT asset inventory, architecture record, consequences, injects, and debrief rubric** for this safety-aware tabletop readiness and defensive coverage review topic. The artifact must name the source descriptor, the bounded claim about **OT vs ICS vs SCADA**, the caveat that limits it, the uncertainty note, the out-of-scope-use boundary, and the reviewer accountable for challenge. Shape the same topic work as a **cyber-physical tabletop evidence packet** that names evidence, uncertainty, reviewer, and stop condition.

**Misconception check.** Correct the misconception that OT vs. ICS vs. SCADA Security (Palo Alto Networks) establishes intent without reviewing alternative explanations.

**Transfer task.** Transfer **OT vs. ICS vs. SCADA Security (Palo Alto Networks)** to a second module by preserving safety-aware tabletop readiness and defensive coverage review, changing the source evidence, and naming a new reviewer.

#### Lesson 10: Operational Technology Cybersecurity (Idaho National Laboratory)

**Concept.** **Operational Technology Cybersecurity (Idaho National Laboratory)** maps industrial assets, safety interlocks, operator roles, and consequence before any cyber-physical inference.

**Worked reasoning and limits.** An institutional research page can locate OT expertise and research topics; its existence is not evidence that a specific architecture or response is certified safe [@ageint212]. For the tank example, neither an institutional affiliation nor agreement between copied displays resolves the discrepant measurement. The classroom outcome remains an evidence hold until the designated human reviewer receives an independent, authorized account of process context.

**Why it matters.** **Operational Technology Cybersecurity (Idaho National Laboratory)** connects classroom vocabulary to ICS/OT Cyber-Physical Defense and Tabletop Readiness practice: learners document evidence, caveats, and reviewer ownership rather than repeating labels.

**Source support.** Inherited source-guide context for **Operational Technology Cybersecurity (Idaho National Laboratory)**: [@ageint212]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_nist_csf_2]; [@official_nist_sp_800_160r1].

**Evidence to inspect.** For **Operational Technology Cybersecurity (Idaho National Laboratory)**, inspect the original passages. No displayable curriculum annotation is available for [@ageint212]. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **Operational Technology Cybersecurity (Idaho National Laboratory)**, build a **tabletop packet with OT asset inventory, architecture record, consequences, injects, and debrief rubric** for this safety-aware tabletop readiness and defensive coverage review topic. The artifact must name the source descriptor, the bounded claim about **Operational Technology Cybersecurity**, the caveat that limits it, the uncertainty note, the out-of-scope-use boundary, and the reviewer accountable for challenge. Shape the same topic work as a **cyber-physical tabletop evidence packet** that records its evidence, the residual uncertainty, the named reviewer, and the stop condition.

**Misconception check.** Correct the misconception that Operational Technology Cybersecurity (Idaho National Laboratory) replaces human review whenever evidence looks plausible.

**Transfer task.** Transfer **Operational Technology Cybersecurity (Idaho National Laboratory)** to a second module by preserving safety-aware tabletop readiness and defensive coverage review, changing the source evidence, and naming a new reviewer.

### Industrial Control Systems (ICS) and Operational Technology worked safe example: synthetic inputs, evidence, and review

Worked example: a sample water-utility tabletop reviews synthetic process logs after a simulated anomaly. [@ageint255]; [@ageint256].

**Contextual source routes.** For module 45's worked-example section, the **ICS/OT Cyber-Physical Defense and Tabletop Readiness** catalog routes include [@official_nist_csf_2]; [@official_nist_sp_800_160r1]; [@official_nist_sp_800_82r3]; [@official_isa_iec_62443]. Check the actual passage, edition, claim scope and access limitations before use. Route membership does not establish relevance, independent corroboration or efficacy.

**Unit discipline spine.** Discipline: **safety-aware ICS and OT intelligence**. Learners use a **cyber-physical tabletop evidence packet** and keep this boundary visible: No live device control, unsafe process change, exploit sequence, evasion, or operational response.

**Frame.** The classroom question centers on **ICS Architecture: SCADA, DCS, PLC, HMI — Definitions and Roles**. Excluded actions stay explicit, and the **Cyber-Physical Readiness Lens** planning question is: Which asset, architecture record, consequence, operator decision, and recovery path is being exercised defensively?

**Inputs.** For the **ICS Architecture: SCADA, DCS, PLC, HMI** scenario, use a fictional tank display reading high at 09:10, two toy sensors reading normal, a same-time network alert, pre-change display values, a scaling-change note, and an instructor safety stop card; no equipment is connected. The Cyber-Physical Readiness Lens intake note records provenance, sensitivity, fit-to-purpose, and why the fixture is enough for this bounded exercise.

**Analysis.** For **ICS Architecture: SCADA, DCS, PLC, HMI**, students first map display, sensor, process consequence, and operator role and align clocks; then compare scaling error, sensor fault, and cyber interference; use the second sensor and pre-change values as controls against treating the network alert as proof of a physical excursion. Invoke the safety stop and hand the discrepancy to the engineering instructor without device commands or process changes. Pause whenever an inference about ICS Architecture: SCADA, DCS, PLC, HMI appears without evidence, confidence outruns support, or an agent output is treated as judgment.

**Completed synthetic result.** a tabletop packet distinguishing the display anomaly from unresolved physical level and cause, recording only supported defensive mappings, and withholding a recovery declaration until consistent readings and fictional operator acceptance are supplied; no attacker identity or safe plant state is established Retain it as the **cyber-physical tabletop evidence packet** for this classroom fixture, with the stated source IDs, uncertainty, review disposition, and excluded-action boundary.

**Flawed answer to revise.** Treating **ICS Architecture: SCADA, DCS, PLC, HMI** as "Cyber-Physical Readiness Lens confirms it" is not enough. The revision ties the claim to safety-aware tabletop readiness and defensive coverage review, adds the missing caveat, states confidence, and records the reviewer who accepted the bounded judgment.

**Debrief.** The reuse note for **ICS Architecture: SCADA, DCS, PLC, HMI** records the defensible claim, the assumption most likely to fail, the evidence that would change confidence, and the review condition for stopping reuse.



### Industrial Control Systems (ICS) and Operational Technology practice sequence: studio moves, artifact steps, and limits

The studio sequence uses the **Cyber-Physical Readiness Lens** practice lens. Moves 1-3 form the compressed path; the full seminar path adds challenge, handoff, and a review memo for **ICS Architecture: SCADA, DCS, PLC, HMI; SCADA: Supervisory Control and Data Acquisition**.

**Contextual source routes.** For module 45's practice-sequence section, the **ICS/OT Cyber-Physical Defense and Tabletop Readiness** catalog routes include [@official_nist_csf_2]; [@official_nist_sp_800_160r1]; [@official_nist_sp_800_82r3]; [@official_isa_iec_62443]. Check the actual passage, edition, claim scope and access limitations before use. Route membership does not establish relevance, independent corroboration or efficacy.

| Move | Learner action | Output | Check |
|---|---|---|---|
| 1. Distinguish | Compare ICS Architecture: SCADA, DCS, PLC, HMI, SCADA: Supervisory Control and Data Acquisition, DCS: Distributed Control Systems; name what each topic can and cannot prove. | Glossary-and-contrast card. | Terms match the **ICS/OT Cyber-Physical Defense and Tabletop Readiness** lane. |
| 2. Frame | Answer the lens question: Which asset, architecture record, consequence, operator decision, and recovery path is being exercised defensively? | Scope card. | Authority, excluded actions, data boundary, and reviewer are explicit. |
| 3. Evidence | Fill the artifact fields for ICS Architecture: SCADA, DCS, PLC, HMI: tabletop packet with OT asset inventory, architecture record, consequences, injects, and debrief rubric. | Evidence packet. | Sources, caveats, confidence, and uncertainty stay separable. |
| 3a. Unit artifact | Add the cyber-physical tabletop evidence packet fields for ICS Architecture: SCADA, DCS, PLC, HMI. | Unit profile note. | Evidence artifacts include asset-consequence map, operator decision log. |
| 4. Challenge | Test the misconception that ICS Architecture: SCADA, DCS, PLC, HMI — Definitions and Roles establishes intent without reviewing alternative explanations. | Failure-mode note. | The artifact applies the key distinction: separate cyber analysis from unsafe process control or live operational action. |
| 5. Handoff | Prepare the artifact for another reviewer. | Handoff memo. | Inputs, transformations, reviewer, refresh trigger, and residual risk are visible. |

#### Industrial Control Systems (ICS) and Operational Technology instructor notes: source reasoning, review points, and studio focus

Ask learners to verbalize the difference between a source, an inference, and a decision. Require a revision whenever a claim cannot be traced to a source descriptor or a human review point. Keep the focus on **ICS Architecture: SCADA, DCS, PLC, HMI; SCADA: Supervisory Control and Data Acquisition**. [@ageint255]; [@ageint256].

#### Industrial Control Systems (ICS) and Operational Technology extension exercise: peer validation and refresh trigger review

**Navigation.** Parent section: [@sec:chapter-industrial-control-systems-ics-and-operational-technology].

Have learners swap artifacts and apply the **Cyber-Physical Readiness Lens** validation rule to someone else's work. The receiving learner must identify one strength, one missing caveat, and one refresh trigger for **ICS Architecture: SCADA, DCS, PLC, HMI; SCADA: Supervisory Control and Data Acquisition**.

### Industrial Control Systems (ICS) and Operational Technology knowledge check: misconceptions, evidence, and reviewer prompts

**Navigation.** Parent section: [@sec:chapter-industrial-control-systems-ics-and-operational-technology].

1. For every topic in this module, identify a source-supported distinction, an unsupported inference to reject, and the exact evidence needed to decide. Start with **ICS Architecture: SCADA, DCS, PLC, HMI — Definitions and Roles**.
2. Transfer the **Cyber-Physical Readiness Lens** artifact from **ICS Architecture: SCADA, DCS, PLC, HMI** to the final topic, **Operational Technology Cybersecurity**; explain what changes and what cannot transfer.
3. Identify one failure mode from the **ICS/OT Cyber-Physical Defense and Tabletop Readiness** lane and the evidence that would reveal it.
4. Answer the coursebook review question: Which cyber observation changes meaning once physical consequence is considered?
5. Correct this misconception: that ICS Architecture: SCADA, DCS, PLC, HMI — Definitions and Roles establishes intent without reviewing alternative explanations.

#### Industrial Control Systems (ICS) and Operational Technology answer quality rubric: source evidence, uncertainty, and safe transfer

Judge answers with the canonical mastery evidence standard in the shared method-and-assurance reference ([@sec:method-assurance-reference]): a strong answer uses source evidence, distinguishes observation from judgment, names uncertainty, and states the safe boundary, while a revise-level answer gives a memorized definition of **ICS Architecture: SCADA, DCS, PLC, HMI** without source evidence, uncertainty, or a safe transfer task.
