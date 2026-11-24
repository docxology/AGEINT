## Requirements-to-Evidence Lens path for OSINT Techniques and Tools: lesson cluster, safe artifact, and review

**Navigation.** Parent section: [@sec:chapter-osint-techniques-and-tools].

### OSINT Techniques and Tools practice studio: topic lessons, safe worked example, and knowledge check

**Navigation.** Parent section: [@sec:chapter-osint-techniques-and-tools].

### OSINT Techniques and Tools topic lessons: source-backed concepts and transfer tasks

**OSINT Techniques and Tools** builds OSINT and GEOINT as public-source reasoning disciplines: availability does not equal reliability, relevance, legality, or ethical reuse. The sequence opens with **Search-exposure provenance review using instructor-provided records**, **Social-source provenance and minimization review using toy records**, **Graph-analysis provenance review using instructor-provided records** and applies the **Requirements-to-Evidence Lens** practice frame through concept, evidence, artifact, misconception, and transfer tasks.

**Learning-path links.** Unit module map [@fig:part-open-source-intelligence-osint-module-map]; module overview [@sec:chapter-osint-techniques-and-tools]; curriculum atlas [@sec:curriculum_orientation].

**Contextual source routes.** For module 10's topic-lessons section, the **Open-Source and Geospatial Intelligence Integrity** catalog routes include [@official_ic_osint_strategy]; [@official_state_osint_strategy]; [@official_iso_19157_data_quality]; [@official_nga_strategy]. Check the actual passage, edition, claim scope and access limitations before use. Route membership does not establish relevance, independent corroboration or efficacy.

#### Lesson 1: Search-exposure provenance review using instructor-provided records

**Concept.** **Search-exposure provenance review using instructor-provided records** evaluates the tool class by provenance, legality, rate limits, identity exposure, and reproducibility before any public-source claim is reused.

**Worked reasoning and limits.** A search index is a selected, delayed representation of records, not the underlying service and not permission to inspect it. Compare only instructor-supplied result snapshots: absence can mean indexing, access or query differences rather than absence of the event. The inherited Reddit discussion and tool survey do not establish current engine syntax, provider behaviour or lawful collection authority; no live queries, device searches or scanning are part of this lesson.

**Why it matters.** **Search-exposure provenance review** matters in the **Open-Source and Geospatial Intelligence Integrity** lane because source-quality review and non-sensitive geospatial interpretation evidence must stay separate from judgment; privacy drift is a common failure.

**Source support.** Inherited source-guide context for **Search-exposure provenance review using instructor-provided records**: [@ageint050] and [@ageint051]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_ic_osint_strategy]; [@official_state_osint_strategy].

**Evidence to inspect.** For **Search-exposure provenance review**, inspect the original passages. No displayable curriculum annotation is available for [@ageint050] and [@ageint051]. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **Search-exposure provenance review**, build a **requirements matrix with source descriptors, caveats, and collection limits** for this source-quality review and non-sensitive geospatial interpretation topic. The artifact must record the tool-and-terms descriptor, the bounded claim about **Search-exposure provenance review using instructor-provided**, the minimization caveat, the reproducibility uncertainty, the identity-exposure boundary, and the reviewer who approves the use. Shape **Search-exposure provenance review** work as an **OSINT provenance and minimization matrix** that states the evidence used, what stays uncertain, who reviews it, and when to stop.

**Misconception check.** Correct the misconception about **Search-exposure provenance review**: that a source being publicly accessible means collecting it is unrestricted, ungoverned, and free of legal, ethical, and scoping limits.

**Transfer task.** Apply this module's safe boundary for **Search-exposure provenance review** to another artifact while keeping source-quality review and non-sensitive geospatial interpretation and reviewer ownership explicit.

#### Lesson 2: Social-source provenance and minimization review using toy records

**Concept.** **Social-source provenance and minimization review using toy records** evaluates the tool class by provenance, legality, rate limits, identity exposure, and reproducibility before any public-source claim is reused.

**Worked reasoning and limits.** A matching handle or display name is an unresolved string match, not identity verification, account control or evidence of coordination. In a fixed synthetic packet, records R1 and R2 share handle 'museum_updates' but carry different supplied account IDs, A7 and A8; R3 republishes R1 with origin A7. Normalizing case yields one handle group but two distinct account records, and deduplicating by origin leaves R1/R3 as one lineage. The output is 'two account IDs share a label; ownership unknown'; treating R3 as independent support is the negative control, and removing account IDs requires downgrading even the record linkage rather than looking up a real person.

**Why it matters.** **Social-source provenance** matters in the **Open-Source and Geospatial Intelligence Integrity** lane because source-quality review and non-sensitive geospatial interpretation evidence must stay separate from judgment; privacy drift is a common failure.

**Source support.** Inherited source-guide context for **Social-source provenance and minimization review using toy records**: [@ageint051] and [@ageint052]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_ic_osint_strategy]; [@official_state_osint_strategy].

**Evidence to inspect.** For **Social-source provenance**, inspect the original passages. Curriculum annotation for [@ageint052]: This article defines open source intelligence as the practice of gathering information from publicly available data for security, business, and investigative purposes, drawing on websites, social media, government records, and public databases. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **Social-source provenance**, build a **requirements matrix with source descriptors, caveats, and collection limits** for this source-quality review and non-sensitive geospatial interpretation topic. The artifact must record the tool-and-terms descriptor, the bounded claim about **Social-source provenance and minimization review**, the minimization caveat, the reproducibility uncertainty, the identity-exposure boundary, and the reviewer who approves the use. Shape **Social-source provenance** work as an **OSINT provenance and minimization matrix** that records its evidence, the residual uncertainty, the named reviewer, and the stop condition.

**Misconception check.** Correct the misconception about **Social-source provenance**: that a source being publicly accessible means collecting it is unrestricted, ungoverned, and free of legal, ethical, and scoping limits.

**Transfer task.** Reuse the **Social-source provenance** audit pattern from this module on a different sample record set with a new reviewer and blocked-use note.

#### Lesson 3: Graph-analysis provenance review using instructor-provided records

**Concept.** **Graph-analysis provenance review using instructor-provided records** evaluates the tool class by provenance, legality, rate limits, identity exposure, and reproducibility before any public-source claim is reused.

**Worked reasoning and limits.** A graph distinguishes entities, observed relations and hypothesized relations; proximity in a drawing has no evidential meaning. In a fictional static export, E1 says document D mentions project P and E2 says D mentions project Q, both derived from D version 1, paragraph 3, at the same capture time. The typed output is D→P 'mentions' and D→Q 'mentions'; the proposed P→Q 'same owner' edge is rejected because co-mention is not ownership evidence. Retain source/version/time on each edge and log extraction as the transformation; a tool-generated candidate edge does not authenticate identity, and copying D cannot strengthen the rejected relation.

**Why it matters.** Analysts use **Graph-analysis provenance review** to separate discovery from collection expansion, and map or media interpretation from targeting. A defensible treatment names the judgment it enables for source-quality review and non-sensitive geospatial interpretation review, the proof limit that privacy drift would otherwise hide, and the reviewer accountable for challenge.

**Source support.** Inherited source-guide context for **Graph-analysis provenance review using instructor-provided records**: [@ageint051]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_ic_osint_strategy]; [@official_state_osint_strategy].

**Evidence to inspect.** For **Graph-analysis provenance review**, inspect the original passages. No displayable curriculum annotation is available for [@ageint051]. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **Graph-analysis provenance review**, build a **requirements matrix with source descriptors, caveats, and collection limits** for this source-quality review and non-sensitive geospatial interpretation topic. The artifact must record the tool-and-terms descriptor, the bounded claim about **Graph-analysis provenance review using instructor-provided**, the minimization caveat, the reproducibility uncertainty, the identity-exposure boundary, and the reviewer who approves the use. Shape **Graph-analysis provenance review** work as an **OSINT provenance and minimization matrix** that logs the evidence, the uncertainty, the responsible reviewer, and the halt condition.

**Misconception check.** Correct the misconception about **Graph-analysis provenance review**: that a source being publicly accessible means collecting it is unrestricted, ungoverned, and free of legal, ethical, and scoping limits.

**Transfer task.** Transfer **Graph-analysis provenance review** from this module to a second motif by preserving source-quality review and non-sensitive geospatial interpretation, replacing action with audit, and naming the blocked use.

#### Lesson 4: Custom-source integration governance review using toy records

**Concept.** **Custom-source integration governance review using toy records** evaluates the tool class by provenance, legality, rate limits, identity exposure, and reproducibility before any public-source claim is reused.

**Worked reasoning and limits.** Treat the framework here as a model of typed input, transformation and output, using a static export rather than executing reconnaissance modules. Record module/version, supplied input identifier, transformation and returned field so a reviewer can distinguish a source assertion from a tool-derived value. The inherited vendor overview and LinkedIn guide cannot establish current module behaviour; unavailable fields remain unknown, not fabricated defaults.

**Why it matters.** Without explicit treatment of **Custom-source integration governance review**, privacy drift undermines source-quality review and non-sensitive geospatial interpretation review; the lesson builds the habit to separate discovery from collection expansion, and map or media interpretation from targeting.

**Source support.** Inherited source-guide context for **Custom-source integration governance review using toy records**: [@ageint052] and [@ageint053]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_ic_osint_strategy]; [@official_state_osint_strategy].

**Evidence to inspect.** For **Custom-source integration governance review**, inspect the original passages. Curriculum annotation for [@ageint052]: This article defines open source intelligence as the practice of gathering information from publicly available data for security, business, and investigative purposes, drawing on websites, social media, government records, and public databases. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **Custom-source integration governance review**, build a **requirements matrix with source descriptors, caveats, and collection limits** for this source-quality review and non-sensitive geospatial interpretation topic. The artifact must record the tool-and-terms descriptor, the bounded claim about **Custom-source integration governance review using**, the minimization caveat, the reproducibility uncertainty, the identity-exposure boundary, and the reviewer who approves the use. Shape **Custom-source integration governance review** work as an **OSINT provenance and minimization matrix** that names evidence, uncertainty, reviewer, and stop condition.

**Misconception check.** Correct the misconception about **Custom-source integration governance review**: that a source being publicly accessible means collecting it is unrestricted, ungoverned, and free of legal, ethical, and scoping limits.

**Transfer task.** Transfer **Custom-source integration governance review** from this module to a second motif by preserving source-quality review and non-sensitive geospatial interpretation, replacing action with audit, and naming the blocked use.

#### Lesson 5: Automated-source aggregation governance review using toy records

**Concept.** **Automated-source aggregation governance review using toy records** evaluates the tool class by provenance, legality, rate limits, identity exposure, and reproducibility before any public-source claim is reused.

**Worked reasoning and limits.** Automation can multiply dependent findings and propagate one mistaken entity match across many output types. On a supplied event export, group records by upstream origin before counting corroboration and distinguish an event's observation time from the export time. A long results list is neither independent evidence nor permission for live collection; this lesson performs record analysis only.

**Why it matters.** **Automated-source aggregation governance review** matters in the **Open-Source and Geospatial Intelligence Integrity** lane because source-quality review and non-sensitive geospatial interpretation evidence must stay separate from judgment; privacy drift is a common failure.

**Source support.** Inherited source-guide context for **Automated-source aggregation governance review using toy records**: [@ageint052]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_ic_osint_strategy]; [@official_state_osint_strategy].

**Evidence to inspect.** For **Automated-source aggregation governance review**, inspect the original passages. Curriculum annotation for [@ageint052]: This article defines open source intelligence as the practice of gathering information from publicly available data for security, business, and investigative purposes, drawing on websites, social media, government records, and public databases. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **Automated-source aggregation governance review**, build a **requirements matrix with source descriptors, caveats, and collection limits** for this source-quality review and non-sensitive geospatial interpretation topic. The artifact must record the tool-and-terms descriptor, the bounded claim about **Automated-source aggregation governance review using**, the minimization caveat, the reproducibility uncertainty, the identity-exposure boundary, and the reviewer who approves the use. Shape **Automated-source aggregation governance review** work as an **OSINT provenance and minimization matrix** that records its evidence, the residual uncertainty, the named reviewer, and the stop condition.

**Misconception check.** Correct the misconception about **Automated-source aggregation governance review**: that a source being publicly accessible means collecting it is unrestricted, ungoverned, and free of legal, ethical, and scoping limits.

**Transfer task.** Apply this module's safe boundary for **Automated-source aggregation governance review** to another artifact while keeping source-quality review and non-sensitive geospatial interpretation and reviewer ownership explicit.

#### Lesson 6: Identity-data minimization review using instructor-provided records

**Concept.** **Identity-data minimization review using instructor-provided records** evaluates the tool class by provenance, legality, rate limits, identity exposure, and reproducibility before any public-source claim is reused.

**Worked reasoning and limits.** Document metadata, harvested strings and username-match candidates are different artifact classes with different error modes; none alone proves a person's identity, location or conduct. A metadata author field can be a template default, a harvested address can be stale, and a same-name account can belong to someone else. The Reddit preference thread is not a primary technical specification, so current capabilities and accuracy are unsupported here; use fictional pre-exported artifacts, not live tools or identity lookups.

**Why it matters.** Analysts use **Identity-data minimization review** to separate discovery from collection expansion, and map or media interpretation from targeting. A defensible treatment names the judgment it enables for source-quality review and non-sensitive geospatial interpretation review, the proof limit that privacy drift would otherwise hide, and the reviewer accountable for challenge.

**Source support.** Inherited source-guide context for **Identity-data minimization review using instructor-provided records**: [@ageint054]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_ic_osint_strategy]; [@official_state_osint_strategy].

**Evidence to inspect.** For **Identity-data minimization review**, inspect the original passages. Curriculum annotation for [@ageint054]: Recommended OSINT tools and their benefits. Top open source intelligence websites. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **Identity-data minimization review**, build a **requirements matrix with source descriptors, caveats, and collection limits** for this source-quality review and non-sensitive geospatial interpretation topic. The artifact must record the tool-and-terms descriptor, the bounded claim about **Identity-data minimization review using instructor-provided**, the minimization caveat, the reproducibility uncertainty, the identity-exposure boundary, and the reviewer who approves the use. Shape **Identity-data minimization review** work as an **OSINT provenance and minimization matrix** that logs the evidence, the uncertainty, the responsible reviewer, and the halt condition.

**Misconception check.** Correct the misconception about **Identity-data minimization review**: that a source being publicly accessible means collecting it is unrestricted, ungoverned, and free of legal, ethical, and scoping limits.

**Transfer task.** Transfer **Identity-data minimization review** from this module to a second motif by preserving source-quality review and non-sensitive geospatial interpretation, replacing action with audit, and naming the blocked use.

#### Lesson 7: OSINT Framework (osintframework.com): Module Taxonomy

**Concept.** **OSINT Framework (osintframework.com): Module Taxonomy** treats open sources as publicly available evidence that still requires provenance, corroboration, legality, and minimization before reuse.

**Worked reasoning and limits.** A directory organizes possible resources; inclusion is not validation of a tool's accuracy, safety, independence or licence. Compare categories by the evidence they could produce, such as a document version versus a candidate relation, rather than by tool count. A missing or outdated entry changes the directory assessment, not the underlying factual claim.

**Why it matters.** **OSINT Framework (osintframework.com)** connects classroom vocabulary to Open-Source and Geospatial Intelligence Integrity practice: learners document evidence, caveats, and reviewer ownership rather than repeating labels.

**Source support.** Inherited source-guide context for **OSINT Framework (osintframework.com): Module Taxonomy**: [@ageint051] and [@ageint052]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_ic_osint_strategy]; [@official_state_osint_strategy].

**Evidence to inspect.** For **OSINT Framework (osintframework.com)**, inspect the original passages. Curriculum annotation for [@ageint052]: This article defines open source intelligence as the practice of gathering information from publicly available data for security, business, and investigative purposes, drawing on websites, social media, government records, and public databases. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **OSINT Framework (osintframework.com)**, build a **requirements matrix with source descriptors, caveats, and collection limits** for this source-quality review and non-sensitive geospatial interpretation topic. The artifact must name the source descriptor, the bounded claim about **OSINT Framework**, the caveat that limits it, the uncertainty note, the out-of-scope-use boundary, and the reviewer accountable for challenge. Shape **OSINT Framework (osintframework.com)** work as an **OSINT provenance and minimization matrix** that states the evidence used, what stays uncertain, who reviews it, and when to stop.

**Misconception check.** Correct the misconception that OSINT Framework (osintframework.com): Module Taxonomy is optional whenever separate discovery from collection expansion, and map or media interpretation from targeting feels inconvenient.

**Transfer task.** Transfer **OSINT Framework (osintframework.com)** to a second module by preserving source-quality review and non-sensitive geospatial interpretation, changing the source evidence, and naming a new reviewer.

#### Lesson 8: Offline OSINT Environments: VM Architecture and Isolation

**Concept.** **Offline OSINT Environments: VM Architecture and Isolation** treats open sources as publicly available evidence that still requires provenance, corroboration, legality, and minimization before reuse.

**Worked reasoning and limits.** Offline means no external retrieval or interaction, not merely running inside a VM. Use supplied inert files with network access disabled, no shared credentials and an explicit manifest of inputs; record any text extraction or normalization without overwriting originals. A VM is not proof of containment, and an input that needs active content or a network connection is excluded rather than opened to complete the exercise.

**Why it matters.** **Offline OSINT Environments** matters in the **Open-Source and Geospatial Intelligence Integrity** lane because source-quality review and non-sensitive geospatial interpretation evidence must stay separate from judgment; privacy drift is a common failure.

**Source support.** Inherited source-guide context for **Offline OSINT Environments: VM Architecture and Isolation**: [@ageint051] and [@ageint052]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_ic_osint_strategy]; [@official_state_osint_strategy].

**Evidence to inspect.** For **Offline OSINT Environments**, inspect the original passages. Curriculum annotation for [@ageint052]: This article defines open source intelligence as the practice of gathering information from publicly available data for security, business, and investigative purposes, drawing on websites, social media, government records, and public databases. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **Offline OSINT Environments**, build a **requirements matrix with source descriptors, caveats, and collection limits** for this source-quality review and non-sensitive geospatial interpretation topic. The artifact must name the source descriptor, the bounded claim about **Offline OSINT Environments**, the caveat that limits it, the uncertainty note, the out-of-scope-use boundary, and the reviewer accountable for challenge. Shape **Offline OSINT Environments** work as an **OSINT provenance and minimization matrix** that logs the evidence, the uncertainty, the responsible reviewer, and the halt condition.

**Misconception check.** Correct the misconception that Offline OSINT Environments: VM Architecture and Isolation establishes intent without reviewing alternative explanations.

**Transfer task.** Transfer **Offline OSINT Environments** to a second module by preserving source-quality review and non-sensitive geospatial interpretation, changing the source evidence, and naming a new reviewer.

#### Lesson 9: IntelTechniques OSINT 11th Edition Methods and Workflows

**Concept.** **IntelTechniques OSINT 11th Edition Methods and Workflows** treats open sources as publicly available evidence that still requires provenance, corroboration, legality, and minimization before reuse.

**Worked reasoning and limits.** The publisher's listing can support edition identity, not the validity of every technique or continued availability of a service [@ageint055]. The inherited third-party PDF link is bibliographic provenance, not a licence to obtain or redistribute the book; no exercise depends on it. Compare an edition-dated claim against the supplied snapshot's date, and leave current functionality unknown when no authorized primary specification is available.

**Why it matters.** **IntelTechniques OSINT 11th Edition Methods** connects classroom vocabulary to Open-Source and Geospatial Intelligence Integrity practice: learners document evidence, caveats, and reviewer ownership rather than repeating labels.

**Source support.** Inherited source-guide context for **IntelTechniques OSINT 11th Edition Methods and Workflows**: [@ageint055] and [@ageint056]. These citations preserve source identity, not automatic topical relevance, empirical validation or normative authority. No claim-specific primary support is established by this source-guide association alone. Profile context—not claim-specific validation—uses [@official_ic_osint_strategy]; [@official_state_osint_strategy].

**Evidence to inspect.** For **IntelTechniques OSINT 11th Edition Methods**, inspect the original passages. Curriculum annotation for [@ageint055]: OSINT Techniques. Resources for Uncovering Online Information - 11th Edition (2024). Curriculum annotation for [@ageint056]: All tutorials in this book were confirmed accurate as of November 1, 2024. These editorial descriptions are not source-authored quotations or independently verified lesson support. Record a passage and locator, distinguishing primary findings, normative requirements, proposals and context using [@sec:analytic-workflow]; unsupported claims remain gaps.

**Student artifact.** For **IntelTechniques OSINT 11th Edition Methods**, build a **requirements matrix with source descriptors, caveats, and collection limits** for this source-quality review and non-sensitive geospatial interpretation topic. The artifact must name the source descriptor, the bounded claim about **IntelTechniques OSINT 11th Edition Methods**, the caveat that limits it, the uncertainty note, the out-of-scope-use boundary, and the reviewer accountable for challenge. Shape **IntelTechniques OSINT 11th Edition Methods** work as an **OSINT provenance and minimization matrix** that records its evidence, the residual uncertainty, the named reviewer, and the stop condition.

**Misconception check.** Correct the misconception that IntelTechniques OSINT 11th Edition Methods and Workflows replaces human review whenever evidence looks plausible.

**Transfer task.** Transfer **IntelTechniques OSINT 11th Edition Methods** to a second module by preserving source-quality review and non-sensitive geospatial interpretation, changing the source evidence, and naming a new reviewer.

### OSINT Techniques and Tools worked safe example: synthetic inputs, evidence, and review

Worked example: a synthetic public-resilience team checks whether open data supports a non-sensitive evacuation-route map. [@ageint251]; [@ageint252].

**Contextual source routes.** For module 10's worked-example section, the **Open-Source and Geospatial Intelligence Integrity** catalog routes include [@official_ic_osint_strategy]; [@official_state_osint_strategy]; [@official_iso_19157_data_quality]; [@official_nga_strategy]. Check the actual passage, edition, claim scope and access limitations before use. Route membership does not establish relevance, independent corroboration or efficacy.

**Unit discipline spine.** Discipline: **open-source intelligence governance**. Learners use a **OSINT provenance and minimization matrix** and keep this boundary visible: No exposed-service lookup, credentialed access, identity exposure, doxxing, or live collection expansion.

**Frame.** The classroom question centers on **Search-exposure provenance review using instructor-provided records**. Excluded actions stay explicit, and the **Requirements-to-Evidence Lens** planning question is: What accountable requirement justifies the evidence, and which source discipline is the least intrusive fit?

**Inputs.** For the **Search-exposure provenance review using instructor-provided records** scenario, use saved fictional road layer A with 100-metre uncertainty and a 2023 date, notice B closing one of two nearby bridges in 2026, repost C copying B, and supplied capture metadata and classroom reuse terms. The Requirements-to-Evidence Lens intake note records provenance, sensitivity, fit-to-purpose, and why the fixture is enough for this bounded exercise.

**Analysis.** For **Search-exposure provenance review using instructor-provided records**, students first record origin, reuse terms, spatial reference, resolution, and relevant dates; then compare the notice with both bridge footprints and trace C to B; remove C as a control so corroboration does not increase through copying. Minimize personal fields and stop a route recommendation when the old layer cannot resolve bridge identity; hand the gap to the mapping instructor. Pause whenever an inference about Search-exposure provenance review using instructor-provided records appears without evidence, confidence outruns support, or an agent output is treated as judgment.

**Completed synthetic result.** a source-quality matrix and map note recording one underlying closure notice, unresolved bridge identity and present conditions, and no safe-route judgment; the allowed classroom reuse is documented separately from source reliability, with no live tracking, collection expansion, or identity exposure Retain it as the **OSINT provenance and minimization matrix** for this classroom fixture, with the stated source IDs, uncertainty, review disposition, and excluded-action boundary.

**Flawed answer to revise.** Treating **Search-exposure provenance review using instructor-provided records** as "Requirements-to-Evidence Lens confirms it" is not enough. The revision ties the claim to source-quality review and non-sensitive geospatial interpretation, adds the missing caveat, states confidence, and records the reviewer who accepted the bounded judgment.

**Debrief.** The reuse note for **Search-exposure provenance review using instructor-provided records** records the defensible claim, the assumption most likely to fail, the evidence that would change confidence, and the review condition for stopping reuse.



### OSINT Techniques and Tools practice sequence: studio moves, artifact steps, and limits

The studio sequence uses the **Requirements-to-Evidence Lens** practice lens. Moves 1-3 form the compressed path; the full seminar path adds challenge, handoff, and a review memo for **Search-exposure provenance review using instructor-provided records; Social-source provenance and minimization review using toy records**.

**Contextual source routes.** For module 10's practice-sequence section, the **Open-Source and Geospatial Intelligence Integrity** catalog routes include [@official_ic_osint_strategy]; [@official_state_osint_strategy]; [@official_iso_19157_data_quality]; [@official_nga_strategy]. Check the actual passage, edition, claim scope and access limitations before use. Route membership does not establish relevance, independent corroboration or efficacy.

| Move | Learner action | Output | Check |
|---|---|---|---|
| 1. Distinguish | Compare Search-exposure provenance review using instructor-provided records, Social-source provenance and minimization review using toy records, Graph-analysis provenance review using instructor-provided records; name what each topic can and cannot prove. | Glossary-and-contrast card. | Terms match the **Open-Source and Geospatial Intelligence Integrity** lane. |
| 2. Frame | Answer the lens question: What accountable requirement justifies the evidence, and which source discipline is the least intrusive fit? | Scope card. | Authority, excluded actions, data boundary, and reviewer are explicit. |
| 3. Evidence | Fill the artifact fields for Search-exposure provenance review using instructor-provided records: requirements matrix with source descriptors, caveats, and collection limits. | Evidence packet. | Sources, caveats, confidence, and uncertainty stay separable. |
| 3a. Unit artifact | Add the OSINT provenance and minimization matrix fields for Search-exposure provenance review using instructor-provided records. | Unit profile note. | Evidence artifacts include provenance chain, terms-of-use note. |
| 4. Challenge | Test the misconception that a source being publicly accessible means collecting it is unrestricted, ungoverned, and free of legal, ethical, and scoping limits. | Failure-mode note. | The artifact applies the key distinction: separate discovery from collection expansion, and map or media interpretation from targeting. |
| 5. Handoff | Prepare the artifact for another reviewer. | Handoff memo. | Inputs, transformations, reviewer, refresh trigger, and residual risk are visible. |

#### OSINT Techniques and Tools instructor notes: source reasoning, review points, and studio focus

Ask learners to verbalize the difference between a source, an inference, and a decision. Require a revision whenever a claim cannot be traced to a source descriptor or a human review point. Keep the focus on **Search-exposure provenance review using instructor-provided records; Social-source provenance and minimization review using toy records**. [@ageint251]; [@ageint252].

#### OSINT Techniques and Tools extension exercise: peer validation and refresh trigger review

**Navigation.** Parent section: [@sec:chapter-osint-techniques-and-tools].

Have learners swap artifacts and apply the **Requirements-to-Evidence Lens** validation rule to someone else's work. The receiving learner must identify one strength, one missing caveat, and one refresh trigger for **Search-exposure provenance review using instructor-provided records; Social-source provenance and minimization review using toy records**.

### OSINT Techniques and Tools knowledge check: misconceptions, evidence, and reviewer prompts

**Navigation.** Parent section: [@sec:chapter-osint-techniques-and-tools].

1. For every topic in this module, identify a source-supported distinction, an unsupported inference to reject, and the exact evidence needed to decide. Start with **Search-exposure provenance review using instructor-provided records**.
2. Transfer the **Requirements-to-Evidence Lens** artifact from **Search-exposure provenance review using instructor-provided records** to the final topic, **IntelTechniques OSINT 11th Edition Methods and Workflows**; explain what changes and what cannot transfer.
3. Identify one failure mode from the **Open-Source and Geospatial Intelligence Integrity** lane and the evidence that would reveal it.
4. Answer the coursebook review question: Which source is available but not reliable enough for the claim?
5. Correct this misconception: that a source being publicly accessible means collecting it is unrestricted, ungoverned, and free of legal, ethical, and scoping limits.

#### OSINT Techniques and Tools answer quality rubric: source evidence, uncertainty, and safe transfer

Judge answers with the canonical mastery evidence standard in the shared method-and-assurance reference ([@sec:method-assurance-reference]): a strong answer uses source evidence, distinguishes observation from judgment, names uncertainty, and states the safe boundary, while a revise-level answer gives a memorized definition of **Search-exposure provenance review using instructor-provided records** without source evidence, uncertainty, or a safe transfer task.
