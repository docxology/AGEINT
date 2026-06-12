# Source Lane Map

AGEINT v2 uses source lanes to keep generated claims auditable. Lanes are not
marketing categories; they decide what evidence a claim needs before the
manuscript can rely on it.

## Required V2 Lanes

| Lane | Evidence expectation |
|---|---|
| AI conformity/compliance | official legal, regulatory, standards, impact-assessment, or audit framework sources |
| Education and assessment | education-policy, competency, teacher-support, learner-protection, and assessment-integrity sources |
| Public-sector agentic AI | government or intergovernmental sources for adoption, public value, oversight, and service accountability |
| Cross-border data/data spaces | legal and policy sources for data access, reuse, interoperability, intermediaries, and data-space governance |
| Human-rights governance | human-rights, privacy, redress, equality, and civic-space sources |
| Agent interoperability standards | W3C, IETF, OpenAPI, and related standards for APIs, identifiers, credentials, tool descriptions, and discovery |
| Workforce governance | labour, skills, future-of-work, decent-work, and social-dialogue sources |
| Model/data provenance | provenance, metadata, cataloging, content credentials, source lineage, and dataset-citation standards |
| Accessibility and digital inclusion | WCAG, UDL, ADA, assistive-technology, remediation, and inclusive-learning sources |
| Procurement/vendor governance | public procurement, contracting transparency, vendor-risk, disclosure, audit, and lifecycle monitoring sources |
| Agent incident response | incident-response, recovery, escalation, logging, containment, and post-incident review sources |
| AI red-team assurance | adversarial assurance, AI cybersecurity, TEVV, resilience, mitigation, and red-team review sources |
| Public-sector transparency | open-government, public accountability, stakeholder participation, disclosure, and civic-space sources |
| Rights-impact privacy review | DPIA, HRIA, high-risk processing, safeguards, redress, and affected-group review sources |
| Model card reporting | model and dataset cards for intended use, evaluation evidence, limitations, release context, and lifecycle controls |
| Dataset documentation | dataset motivation, stakeholder purpose, composition, collection process, recommended use, prohibited reuse, lifecycle revision, and accountability sources |
| Algorithmic transparency reporting | transparency notices, public records, publication guidance, scope, exemptions, and accessible accountability fields |
| Records retention/auditability | records-retention evidence, source/prompt registers, exception logs, incident records, and audit trails |
| Secure release/change control | release gates, rollback, monitoring, secure-development lifecycle controls, and retest evidence |
| Risk exception governance | risk exceptions, compensating controls, expiry, retest, traceability, and acceptance owner evidence |
| Learner support/accommodations | learner support, accessibility alternatives, assessment fairness, feedback, and remediation evidence |
| Assurance evaluation evidence | scenario design, model testing, red teaming, field testing, measurement trees, and evaluation evidence |
| Procurement performance monitoring | vendor demonstrations, QASP-style monitoring, performance metrics, and post-award review |

## May 24, 2026 Source Refresh

The May 24 refresh extends these lanes with official Canada, OECD, UN, NIST,
and CISA anchors. Public-sector agentic AI now includes Canada's agentic-AI
guide; rights-impact review includes Canada's Algorithmic Impact Assessment;
public-sector transparency includes Canada's AI Register; agent incident
response includes OECD AI risks/incidents and reporting-framework materials;
AI red-team assurance includes NIST Dioptra; secure release/change control
includes CISA secure AI deployment; procurement/vendor governance includes CISA
Secure by Demand for OT; and OT auditability/evidence lanes include CISA asset
inventory and definitive architecture guidance.

## Authoring Rule

Add lane metadata in `data/research_anchors/` and `src/intelligence_content/`, surface it through
`src/manuscript_variables/`, and rebuild. Do not hand-edit generated
source-lane tables under `output/`.

Inherited source-guide rows from LinkedIn, Medium, cloud-vendor guidance,
security blogs, and practitioner explainers remain useful provenance context.
They should be surfaced as secondary or illustrative evidence, while official,
standards, public-domain, and scholarly anchors carry definitions, governance
requirements, and performance-sensitive claims.

Visible generated headings should be reader-facing. Source-guide pseudo-headings
such as `V2 source-lane extension:`, `Deep expansion:`, and
`Evidence-package expansion:` are normalized by `src/manuscript_manifest/`.
Keep raw source-guide wording only where provenance/source-map tables need it.
